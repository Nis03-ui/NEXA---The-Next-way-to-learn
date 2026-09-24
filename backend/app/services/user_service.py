"""User management service for NEXA LMS."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.core.logging import get_logger
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = get_logger(__name__)


class UserService:
    """Business logic for user management (CRUD, activate/deactivate, search)."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = UserRepository(db)

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    async def get_by_id(self, user_id: UUID) -> User:
        """Return a user by primary key.

        Raises:
            ResourceNotFoundException: If no user with *user_id* exists.
        """
        user = await self._repo.get_by_id(user_id)
        if user is None:
            logger.debug("User not found: id=%s", user_id)
            raise ResourceNotFoundException(f"User with id '{user_id}' was not found.")
        return user

    async def get_all(self, skip: int, limit: int) -> tuple[list[User], int]:
        """Return a paginated list of all users with total count.

        Args:
            skip: Number of records to skip.
            limit: Maximum records to return.

        Returns:
            Tuple of (users, total_count).
        """
        users, total = await self._repo.get_all(skip=skip, limit=limit)
        logger.debug("get_all users: skip=%d limit=%d total=%d", skip, limit, total)
        return users, total

    async def search(
        self, query: str, skip: int, limit: int
    ) -> tuple[list[User], int]:
        """Search users by name or email substring.

        Args:
            query: Search string (case-insensitive).
            skip: Pagination offset.
            limit: Maximum records to return.

        Returns:
            Tuple of (matching_users, total_count).
        """
        users, total = await self._repo.search(query=query, skip=skip, limit=limit)
        logger.debug("search users query=%r total=%d", query, total)
        return users, total

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    async def update(
        self,
        user: User,
        name: str | None,
        email: str | None,
        is_active: bool | None,
    ) -> User:
        """Update mutable fields on *user*.

        Args:
            user: The user to update.
            name: New display name (``None`` to leave unchanged).
            email: New email address (``None`` to leave unchanged).
            is_active: Active flag override (``None`` to leave unchanged).

        Returns:
            The updated :class:`User` instance.

        Raises:
            ConflictException: If the new email is already taken by another user.
        """
        updates: dict = {}

        if name is not None:
            updates["name"] = name.strip()

        if email is not None:
            email = email.strip().lower()
            if email != user.email:
                existing = await self._repo.get_by_email(email)
                if existing is not None and existing.id != user.id:
                    raise ConflictException(
                        f"Email '{email}' is already registered to another account."
                    )
                updates["email"] = email

        if is_active is not None:
            updates["is_active"] = is_active

        if not updates:
            logger.debug("update user id=%s: no changes requested", user.id)
            return user

        updated = await self._repo.update(user, **updates)
        logger.info("User updated: id=%s fields=%s", user.id, list(updates.keys()))
        return updated

    async def delete(self, user_id: UUID) -> None:
        """Permanently delete a user by id.

        Raises:
            ResourceNotFoundException: If the user does not exist.
        """
        user = await self.get_by_id(user_id)
        await self._repo.delete(user)
        logger.info("User deleted: id=%s", user_id)

    async def deactivate(self, user_id: UUID) -> User:
        """Set a user's ``is_active`` flag to ``False``.

        Raises:
            ResourceNotFoundException: If the user does not exist.
        """
        user = await self.get_by_id(user_id)
        updated = await self._repo.update(user, is_active=False)
        logger.info("User deactivated: id=%s", user_id)
        return updated

    async def activate(self, user_id: UUID) -> User:
        """Set a user's ``is_active`` flag to ``True``.

        Raises:
            ResourceNotFoundException: If the user does not exist.
        """
        user = await self.get_by_id(user_id)
        updated = await self._repo.update(user, is_active=True)
        logger.info("User activated: id=%s", user_id)
        return updated
