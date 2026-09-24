"""
Enrollment repository — all data access for the Enrollment model.
"""
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrollment import Enrollment, EnrollmentStatus
from app.repositories.base_repository import BaseRepository


class EnrollmentRepository(BaseRepository[Enrollment]):
    """Repository for :class:`~app.models.enrollment.Enrollment` records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Enrollment)

    # ── Point lookups ─────────────────────────────────────────────────────────

    async def get_by_student_and_course(
        self, student_id: UUID, course_id: UUID
    ) -> Enrollment | None:
        """
        Return the enrollment record for a specific student/course pair,
        or None if no such enrollment exists.
        """
        result = await self._session.execute(
            select(Enrollment).where(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id,
            )
        )
        return result.scalars().first()

    # ── Filtered lists ────────────────────────────────────────────────────────

    async def get_by_student(
        self, student_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Enrollment]:
        """Return paginated enrollments for a student."""
        result = await self._session.execute(
            select(Enrollment)
            .where(Enrollment.student_id == student_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_course(
        self, course_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Enrollment]:
        """Return paginated enrollments for a course."""
        result = await self._session.execute(
            select(Enrollment)
            .where(Enrollment.course_id == course_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    # ── Counts ────────────────────────────────────────────────────────────────

    async def count_by_course(self, course_id: UUID) -> int:
        """Return the total number of enrollments in a course."""
        result = await self._session.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(Enrollment.course_id == course_id)
        )
        return result.scalar_one()

    async def count_by_student(self, student_id: UUID) -> int:
        """Return the total number of courses a student is enrolled in."""
        result = await self._session.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(Enrollment.student_id == student_id)
        )
        return result.scalar_one()

    async def count_completed_by_student(self, student_id: UUID) -> int:
        """Return the number of COMPLETED enrollments for a student."""
        result = await self._session.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(
                Enrollment.student_id == student_id,
                Enrollment.status == EnrollmentStatus.COMPLETED,
            )
        )
        return result.scalar_one()
