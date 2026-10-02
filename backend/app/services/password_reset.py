from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.models.auth_session import AuthSession
from app.models.password_reset import PasswordResetToken
from app.models.user import User


def utc_now() -> datetime:
    """
    Return the current UTC time as a naive datetime.

    PostgreSQL currently stores our timestamps as timezone-naive
    DateTime values, so we normalize UTC timestamps accordingly.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create_reset_token() -> str:
    """
    Generate a cryptographically secure password-reset token.
    """
    return secrets.token_urlsafe(48)


def hash_reset_token(token: str) -> str:
    """
    Hash a reset token before storing it in the database.
    """
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


async def create_password_reset_token(
    user: User,
    db: AsyncSession,
) -> str:
    """
    Create a password-reset token for a user.

    Any previous unused reset tokens for the same user are
    invalidated before creating a new one.
    """

    now = utc_now()

    # Invalidate existing unused reset tokens.
    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
    )

    existing_tokens = result.scalars().all()

    for reset_token in existing_tokens:
        reset_token.used_at = now

    # Generate the new raw token.
    raw_token = create_reset_token()

    token_hash = hash_reset_token(raw_token)

    expires_at = (
        now
        + timedelta(
            minutes=settings.password_reset_expire_minutes
        )
    )

    reset_record = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(reset_record)

    await db.flush()

    return raw_token


async def reset_password(
    token: str,
    new_password: str,
    db: AsyncSession,
) -> User:
    """
    Validate a password-reset token and update the user's password.

    The reset token becomes unusable immediately after successful use.
    All existing authentication sessions are also revoked.
    """

    token_hash = hash_reset_token(token)

    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash
        )
    )

    reset_record = result.scalar_one_or_none()

    if reset_record is None:
        raise ValueError("Invalid password reset token")

    now = utc_now()

    if reset_record.used_at is not None:
        raise ValueError("Password reset token has already been used")

    if reset_record.expires_at <= now:
        raise ValueError("Password reset token has expired")

    user = await db.get(
        User,
        reset_record.user_id,
    )

    if user is None:
        raise ValueError("User not found")

    # Update password.
    user.password_hash = hash_password(new_password)

    # Consume the reset token.
    reset_record.used_at = now

    # Revoke all existing authentication sessions.
    await db.execute(
        update(AuthSession)
        .where(
            AuthSession.user_id == user.id,
            AuthSession.revoked_at.is_(None),
        )
        .values(
            revoked_at=now,
        )
    )

    await db.flush()

    return user