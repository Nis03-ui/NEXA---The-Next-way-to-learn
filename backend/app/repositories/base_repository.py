"""
Generic base repository providing common CRUD operations for all ORM models.
All methods are async and use SQLAlchemy 2.x query style.
"""
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """
    Generic repository that wraps common async SQLAlchemy operations.

    Sub-classes should call super().__init__(session, ModelClass) and may
    add model-specific query methods on top.
    """

    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self._session = session
        self._model = model

    # ── Read ──────────────────────────────────────────────────────────────────

    async def get_by_id(self, id: UUID) -> ModelT | None:
        """Return a single instance by primary key, or None if not found."""
        result = await self._session.execute(
            select(self._model).where(self._model.id == id)  # type: ignore[attr-defined]
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 20) -> list[ModelT]:
        """Return a paginated list of all records."""
        result = await self._session.execute(
            select(self._model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        """Return the total number of records in the table."""
        result = await self._session.execute(
            select(func.count()).select_from(self._model)
        )
        return result.scalar_one()

    # ── Write ─────────────────────────────────────────────────────────────────

    async def create(self, obj: ModelT) -> ModelT:
        """
        Persist a new model instance.

        Adds the object to the session, flushes to obtain DB-generated values
        (e.g. ``id``, ``created_at``), then refreshes the in-memory state.
        """
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update(self, obj: ModelT) -> ModelT:
        """
        Persist changes made to an already-tracked model instance.

        Flushes the pending changes and refreshes the object so callers
        receive the DB-current state.
        """
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        """Delete the model instance and flush the change to the DB."""
        await self._session.delete(obj)
        await self._session.flush()
