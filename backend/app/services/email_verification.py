from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.email_verification import EmailVerificationToken
from app.models.user import User


def utc_now() -> datetime:
    """
    Return the current UTC time as a naive datetime.

    PostgreSQL currently stores our timestamps as timezone-naive
    DateTime values, so we normalize UTC timestamps accordingly.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create_verification_token() -> str:
    """
    Generate a cryptographically secure email verification token.
    """
    return secrets.token_urlsafe(48)


def hash_verification_token(token: str) -> str:
    """
    Hash the verification token before storing it in the database.
    """
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


async def create_email_verification_token(
    user: User,
    db: AsyncSession,
) -> str:
    """
    Create a new email verification token.

    Any previous unused verification tokens for the same user
    are invalidated before creating a new token.
    """

    now = utc_now()

    # Invalidate previous unused verification tokens.
    result = await db.execute(
        select(EmailVerificationToken).where(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.verified_at.is_(None),
        )
    )

    existing_tokens = result.scalars().all()

    for verification_token in existing_tokens:
        verification_token.verified_at = now

    # Generate raw token.
    raw_token = create_verification_token()

    # Store only the hash.
    token_hash = hash_verification_token(raw_token)

    expires_at = (
        now
        + timedelta(
            minutes=settings.email_verification_expire_minutes
        )
    )

    verification_record = EmailVerificationToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(verification_record)

    await db.flush()

    return raw_token


async def verify_email(
    token: str,
    db: AsyncSession,
) -> User:
    """
    Validate an email verification token and verify the user's email.

    The token becomes unusable immediately after successful verification.
    """

    token_hash = hash_verification_token(token)

    result = await db.execute(
        select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == token_hash
        )
    )

    verification_record = result.scalar_one_or_none()

    if verification_record is None:
        raise ValueError(
            "Invalid email verification token"
        )

    now = utc_now()

    if verification_record.verified_at is not None:
        raise ValueError(
            "Email verification token has already been used"
        )

    if verification_record.expires_at <= now:
        raise ValueError(
            "Email verification token has expired"
        )

    user = await db.get(
        User,
        verification_record.user_id,
    )

    if user is None:
        raise ValueError("User not found")

    if user.email_verified:
        verification_record.verified_at = now
        await db.flush()
        return user

    # Verify the user's email.
    user.email_verified = True

    # Consume the token.
    verification_record.verified_at = now

    await db.flush()

    return user