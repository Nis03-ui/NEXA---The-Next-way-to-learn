"""
Course, Chapter, and Note repositories — all data access for course-related models.
"""
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Chapter, Course, CourseStatus, Note
from app.models.enrollment import Enrollment
from app.repositories.base_repository import BaseRepository


class CourseRepository(BaseRepository[Course]):
    """Repository for :class:`~app.models.course.Course` records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Course)

    # ── Filtered lists ────────────────────────────────────────────────────────

    async def get_by_teacher(
        self, teacher_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Course]:
        """Return paginated courses that belong to the given teacher."""
        result = await self._session.execute(
            select(Course)
            .where(Course.teacher_id == teacher_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_published(self, skip: int = 0, limit: int = 20) -> list[Course]:
        """Return paginated courses whose status is PUBLISHED."""
        result = await self._session.execute(
            select(Course)
            .where(Course.status == CourseStatus.PUBLISHED)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def search(
        self, query: str, skip: int = 0, limit: int = 20
    ) -> list[Course]:
        """
        Substring search on ``title`` and ``description`` using ILIKE.
        Only returns PUBLISHED courses.
        """
        pattern = f"%{query}%"
        result = await self._session.execute(
            select(Course)
            .where(
                Course.status == CourseStatus.PUBLISHED,
                or_(
                    Course.title.ilike(pattern),
                    Course.description.ilike(pattern),
                ),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    # ── Aggregated lookups ────────────────────────────────────────────────────

    async def get_with_enrollment_count(
        self, course_id: UUID
    ) -> tuple[Course | None, int]:
        """
        Return a course alongside its current enrollment count.

        Returns:
            ``(course, enrollment_count)`` — course is None when not found.
        """
        course_result = await self._session.execute(
            select(Course).where(Course.id == course_id)
        )
        course = course_result.scalars().first()

        count_result = await self._session.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(Enrollment.course_id == course_id)
        )
        enrollment_count = count_result.scalar_one()
        return course, enrollment_count

    async def get_all_with_count(
        self,
        skip: int = 0,
        limit: int = 20,
        status: str | None = None,
    ) -> tuple[list[Course], int]:
        """
        Return a paginated list of courses with total count, optionally
        filtered by status string (e.g. ``"PUBLISHED"``).

        Returns:
            ``(courses, total_count)``
        """
        base_query = select(Course)
        count_query = select(func.count()).select_from(Course)

        if status is not None:
            status_filter = Course.status == status
            base_query = base_query.where(status_filter)
            count_query = count_query.where(status_filter)

        courses_result = await self._session.execute(
            base_query.offset(skip).limit(limit)
        )
        count_result = await self._session.execute(count_query)

        return list(courses_result.scalars().all()), count_result.scalar_one()

    async def get_teacher_courses_with_count(
        self, teacher_id: UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[Course], int]:
        """
        Return paginated courses owned by a teacher alongside the total count.

        Returns:
            ``(courses, total_count)``
        """
        filter_clause = Course.teacher_id == teacher_id

        courses_result = await self._session.execute(
            select(Course).where(filter_clause).offset(skip).limit(limit)
        )
        count_result = await self._session.execute(
            select(func.count()).select_from(Course).where(filter_clause)
        )
        return list(courses_result.scalars().all()), count_result.scalar_one()


class ChapterRepository(BaseRepository[Chapter]):
    """Repository for :class:`~app.models.course.Chapter` records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Chapter)

    async def get_by_course(self, course_id: UUID) -> list[Chapter]:
        """Return all chapters for a course, ordered by ``Chapter.order`` ascending."""
        result = await self._session.execute(
            select(Chapter)
            .where(Chapter.course_id == course_id)
            .order_by(Chapter.order.asc())
        )
        return list(result.scalars().all())

    async def get_max_order(self, course_id: UUID) -> int:
        """
        Return the current maximum ``order`` value for chapters in a course.

        Returns 0 when the course has no chapters yet, making it safe to use
        directly as ``max_order + 1`` for the next chapter's order.
        """
        result = await self._session.execute(
            select(func.coalesce(func.max(Chapter.order), 0)).where(
                Chapter.course_id == course_id
            )
        )
        return result.scalar_one()


class NoteRepository(BaseRepository[Note]):
    """Repository for :class:`~app.models.course.Note` records."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Note)

    async def get_by_chapter(self, chapter_id: UUID) -> list[Note]:
        """Return all notes belonging to the given chapter."""
        result = await self._session.execute(
            select(Note).where(Note.chapter_id == chapter_id)
        )
        return list(result.scalars().all())
