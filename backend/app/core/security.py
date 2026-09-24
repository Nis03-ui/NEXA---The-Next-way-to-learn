"""
Security utilities: password hashing (Argon2), JWT creation/validation.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHashError
from jose import JWTError, jwt

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
)

# ── Password utilities ────────────────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Return an Argon2 hash of the plaintext password."""
    return _ph.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against an Argon2 hash.
    Returns False on any mismatch or verification error.
    """
    try:
        return _ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(hashed_password: str) -> bool:
    """Return True if the hash should be upgraded (parameters changed)."""
    return _ph.check_needs_rehash(hashed_password)


# ── JWT utilities ─────────────────────────────────────────────────────────────

def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra_claims: Optional[dict[str, Any]] = None,
) -> str:
    now = datetime.now(tz=timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str, role: str) -> str:
    """Create a short-lived JWT access token."""
    return _create_token(
        subject=user_id,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        extra_claims={"role": role},
    )


def create_refresh_token(user_id: str) -> str:
    """Create a long-lived JWT refresh token."""
    return _create_token(
        subject=user_id,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.
    Raises JWTError on failure.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "access":
            raise JWTError("Token type mismatch")
        return payload
    except JWTError:
        raise


def decode_refresh_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT refresh token.
    Raises JWTError on failure.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "refresh":
            raise JWTError("Token type mismatch")
        return payload
    except JWTError:
        raise
