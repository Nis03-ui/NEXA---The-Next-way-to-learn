"""Authentication service for NEXA LMS."""

from __future__ import annotations

import re
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AuthenticationException,
    ConflictException,
    ValidationException,
)
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    needs_rehash,
    verify_password,
)
from app.models.user import Role, User
from app.repositories.user_repository import UserRepository

logger = get_logger(__name__)

# Minimum password requirements
_PASSWORD_MIN_LENGTH = 8
_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
)

# Token TTL exposed in the response (seconds)
_ACCESS_TOKEN_EXPIRES_IN = 1800  # 30 minutes


class AuthService:
    """Business logic for authentication and authorization."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = UserRepository(db)

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    async def register(
        self,
        name: str,
        email: str,
        password: str,
        role: Role = Role.STUDENT,
    ) -> User:
        """Register a new user account.

        Args:
            name: Display name.
            email: Unique email address.
            password: Plain-text password (will be hashed).
            role: Role to assign (default STUDENT).

        Returns:
            The newly created :class:`User` instance.

        Raises:
            ConflictException: If the email is already registered.
            ValidationException: If the password does not meet strength requirements.
        """
        email = email.strip().lower()

        existing = await self._repo.get_by_email(email)
        if existing is not None:
            logger.warning("Registration attempted with duplicate email: %s", email)
            raise ConflictException(f"An account with email '{email}' already exists.")

        self._validate_password_strength(password)

        hashed = hash_password(password)
        user = await self._repo.create(
            name=name.strip(),
            email=email,
            password_hash=hashed,
            role=role,
        )

        logger.info("New user registered: id=%s email=%s role=%s", user.id, email, role)
        return user

    async def login(self, email: str, password: str) -> dict:
        """Authenticate a user and return JWT tokens.

        Args:
            email: Registered email address.
            password: Plain-text password to verify.

        Returns:
            Dictionary containing ``access_token``, ``refresh_token``,
            ``token_type``, and ``expires_in``.

        Raises:
            AuthenticationException: If credentials are invalid or account is inactive.
        """
        email = email.strip().lower()

        user = await self._repo.get_by_email(email)
        if user is None or not user.is_active:
            logger.warning("Login failed for email: %s (not found or inactive)", email)
            raise AuthenticationException("Invalid credentials or account is inactive.")

        if not verify_password(password, user.password_hash):
            logger.warning("Login failed for user id=%s: bad password", user.id)
            raise AuthenticationException("Invalid credentials or account is inactive.")

        # Opportunistic rehash if the stored hash is outdated
        if needs_rehash(user.password_hash):
            logger.info("Rehashing password for user id=%s", user.id)
            new_hash = hash_password(password)
            await self._repo.update(user, password_hash=new_hash)

        access_token = create_access_token(subject=str(user.id), role=user.role.value)
        refresh_token = create_refresh_token(subject=str(user.id))

        logger.info("User logged in: id=%s role=%s", user.id, user.role)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": _ACCESS_TOKEN_EXPIRES_IN,
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Issue a new access token from a valid refresh token.

        Args:
            refresh_token: A previously issued refresh JWT.

        Returns:
            Dictionary with ``access_token``, ``token_type``, and ``expires_in``.

        Raises:
            AuthenticationException: If the token is invalid, expired, or the user
                is inactive.
        """
        try:
            payload = decode_refresh_token(refresh_token)
            user_id: str = payload["sub"]
        except Exception as exc:
            logger.warning("Refresh token decode failed: %s", exc)
            raise AuthenticationException("Invalid or expired refresh token.") from exc

        user = await self._repo.get_by_id(UUID(user_id))
        if user is None or not user.is_active:
            logger.warning("Refresh attempted for missing/inactive user id=%s", user_id)
            raise AuthenticationException("User account not found or inactive.")

        access_token = create_access_token(subject=str(user.id), role=user.role.value)

        logger.info("Access token refreshed for user id=%s", user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": _ACCESS_TOKEN_EXPIRES_IN,
        }

    async def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        """Change a user's password after verifying the current one.

        Args:
            user: The authenticated user requesting the change.
            current_password: The user's existing plain-text password.
            new_password: The desired new plain-text password.

        Raises:
            AuthenticationException: If the current password is incorrect.
            ValidationException: If the new password fails strength validation.
        """
        if not verify_password(current_password, user.password_hash):
            logger.warning("Change-password: wrong current password for user id=%s", user.id)
            raise AuthenticationException("Current password is incorrect.")

        self._validate_password_strength(new_password)

        new_hash = hash_password(new_password)
        await self._repo.update(user, password_hash=new_hash)

        logger.info("Password changed for user id=%s", user.id)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_password_strength(password: str) -> None:
        """Raise :class:`ValidationException` if *password* is too weak."""
        if len(password) < _PASSWORD_MIN_LENGTH:
            raise ValidationException(
                f"Password must be at least {_PASSWORD_MIN_LENGTH} characters long."
            )
        if not _PASSWORD_PATTERN.match(password):
            raise ValidationException(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, and one digit."
            )
