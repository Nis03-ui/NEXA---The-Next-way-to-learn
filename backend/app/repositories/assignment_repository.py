"""
Assignment and Submission repositories — all data access for assignment-related models.
"""
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assignment import Assignment, Submission
from app.repositories.base_repository import BaseRepository


class AssignmentRepository(BaseRepository[Assignment]):
    """Repository for :class:`~app.models.assignment.Assignment` records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Assignment)

    async def get_by_course(
        self, course_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Assignment]:
        """Return paginated assignments belonging to a course."""
        result = await self._session.execute(
            select(Assignment)
            .where(Assignment.course_id == course_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_by_course(self, course_id: UUID) -> int:
        """Return the total number of assignments in a course."""
        result = await self._session.execute(
            select(func.count())
            .select_from(Assignment)
            .where(Assignment.course_id == course_id)
        )
        return result.scalar_one()


class SubmissionRepository(BaseRepository[Submission]):
    """Repository for :class:`~app.models.assignment.Submission` records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Submission)

    # ── Point lookups ─────────────────────────────────────────────────────────

    async def get_by_assignment_and_student(
        self, assignment_id: UUID, student_id: UUID
    ) -> Submission | None:
        """
        Return the submission for a specific assignment/student pair,
        or None if the student has not yet submitted.
        """
        result = await self._session.execute(
            select(Submission).where(
                Submission.assignment_id == assignment_id,
                Submission.student_id == student_id,
            )
        )
        return result.scalars().first()

    # ── Filtered lists ────────────────────────────────────────────────────────

    async def get_by_assignment(
        self, assignment_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Submission]:
        """Return paginated submissions for a given assignment."""
        result = await self._session.execute(
            select(Submission)
            .where(Submission.assignment_id == assignment_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_student(
        self, student_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Submission]:
        """Return paginated submissions made by a student."""
        result = await self._session.execute(
            select(Submission)
            .where(Submission.student_id == student_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    # ── Counts ────────────────────────────────────────────────────────────────

    async def count_by_student(self, student_id: UUID) -> int:
        """Return total submissions made by a student."""
        result = await self._session.execute(
            select(func.count())
            .select_from(Submission)
            .where(Submission.student_id == student_id)
        )
        return result.scalar_one()

    async def count_graded_by_student(self, student_id: UUID) -> int:
        """Return the number of submissions that have been graded (score is not NULL)."""
        result = await self._session.execute(
            select(func.count())
            .select_from(Submission)
            .where(
                Submission.student_id == student_id,
                Submission.score.is_not(None),
            )
        )
        return result.scalar_one()

    # ── Aggregated stats ──────────────────────────────────────────────────────

    async def get_submission_stats_for_assignment(
        self, assignment_id: UUID
    ) -> dict:
        """
        Return a summary statistics dict for all submissions on an assignment.

        Returns:
            ``{'total': int, 'graded': int, 'avg_score': float | None}``
            where ``avg_score`` is ``None`` when no graded submissions exist.
        """
        total_result = await self._session.execute(
            select(func.count())
            .select_from(Submission)
            .where(Submission.assignment_id == assignment_id)
        )
        total: int = total_result.scalar_one()

        graded_result = await self._session.execute(
            select(func.count())
            .select_from(Submission)
            .where(
                Submission.assignment_id == assignment_id,
                Submission.score.is_not(None),
            )
        )
        graded: int = graded_result.scalar_one()

        avg_result = await self._session.execute(
            select(func.avg(Submission.score)).where(
                Submission.assignment_id == assignment_id,
                Submission.score.is_not(None),
            )
        )
        avg_score: float | None = avg_result.scalar_one_or_none()

        return {
            "total": total,
            "graded": graded,
            "avg_score": float(avg_score) if avg_score is not None else None,
        }
