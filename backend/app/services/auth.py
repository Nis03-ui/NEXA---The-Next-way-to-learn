from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_refresh_token,
    create_token,
    hash_refresh_token,
)
from app.models.auth_session import AuthSession
from app.models.user import User


def utc_now() -> datetime:
    """
    Return the current UTC time as a naive datetime.

    PostgreSQL column is currently DateTime without timezone.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


async def create_auth_session(
    user: User,
    db: AsyncSession,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> tuple[str, AuthSession]:
    """
    Create a refresh-token session for a user.

    The raw refresh token is returned to the caller.
    Only its SHA-256 hash is stored in PostgreSQL.
    """

    refresh_token = create_refresh_token()

    refresh_token_hash = hash_refresh_token(
        refresh_token
    )

    expires_at = (
        utc_now()
        + timedelta(
            days=settings.refresh_token_expire_days
        )
    )

    session = AuthSession(
        user_id=user.id,
        refresh_token_hash=refresh_token_hash,
        user_agent=user_agent,
        ip_address=ip_address,
        expires_at=expires_at,
    )

    db.add(session)

    await db.flush()

    return refresh_token, session


async def rotate_refresh_token(
    refresh_token: str,
    db: AsyncSession,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> tuple[User, str, str]:
    """
    Validate a refresh token and rotate it.

    Returns:

        user
        new access token
        new refresh token
    """

    token_hash = hash_refresh_token(
        refresh_token
    )

    result = await db.execute(
        select(AuthSession).where(
            AuthSession.refresh_token_hash == token_hash
        )
    )

    session = result.scalar_one_or_none()

    if session is None:
        raise ValueError(
            "Invalid refresh token"
        )

    now = utc_now()

    if session.revoked_at is not None:
        raise ValueError(
            "Refresh token has been revoked"
        )

    if session.expires_at <= now:
        raise ValueError(
            "Refresh token has expired"
        )

    user = await db.get(
        User,
        session.user_id,
    )

    if user is None:
        raise ValueError(
            "User not found"
        )

    # Revoke the old refresh token.
    session.revoked_at = now

    # Create a new refresh-token session.
    new_refresh_token, _ = await create_auth_session(
        user=user,
        db=db,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    new_access_token = create_token(
        user.id
    )

    return (
        user,
        new_access_token,
        new_refresh_token,
    )


async def revoke_refresh_token(
    refresh_token: str,
    db: AsyncSession,
) -> bool:
    """
    Revoke a refresh-token session.

    Returns True if a session was found and revoked.
    """

    token_hash = hash_refresh_token(
        refresh_token
    )

    result = await db.execute(
        select(AuthSession).where(
            AuthSession.refresh_token_hash == token_hash
        )
    )

    session = result.scalar_one_or_none()

    if session is None:
        return False

    if session.revoked_at is None:
        session.revoked_at = utc_now()

    return True