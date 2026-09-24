"""
User repository — all data access operations for the User model.
No business logic; callers (service layer) are responsible for raising
HTTP exceptions on None returns.
"""
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Role, User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for :class:`~app.models.user.User` records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    # ── Lookups ───────────────────────────────────────────────────────────────

    async def get_by_email(self, email: str) -> User | None:
        """Return a user matching the given email address, or None."""
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_by_role(
        self, role: Role, skip: int = 0, limit: int = 20
    ) -> list[User]:
        """Return paginated users that have the specified role."""
        result = await self._session.execute(
            select(User)
            .where(User.role == role)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_by_role(self, role: Role) -> int:
        """Return the number of users with the given role."""
        result = await self._session.execute(
            select(func.count()).select_from(User).where(User.role == role)
        )
        return result.scalar_one()

    async def search(
        self, query: str, skip: int = 0, limit: int = 20
    ) -> list[User]:
        """
        Full-text substring search across ``name`` and ``email`` columns
        using case-insensitive ILIKE.
        """
        pattern = f"%{query}%"
        result = await self._session.execute(
            select(User)
            .where(or_(User.name.ilike(pattern), User.email.ilike(pattern)))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_all_with_count(
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[User], int]:
        """
        Return a page of users alongside the total count in a single round-trip.

        Returns:
            A tuple of ``(users, total_count)``.
        """
        users_result = await self._session.execute(
            select(User).offset(skip).limit(limit)
        )
        count_result = await self._session.execute(
            select(func.count()).select_from(User)
        )
        users = list(users_result.scalars().all())
        total = count_result.scalar_one()
        return users, total
