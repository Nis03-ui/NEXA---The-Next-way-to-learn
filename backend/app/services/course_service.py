"""Course, Chapter, and Note services for NEXA LMS."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AuthorizationException,
    ResourceNotFoundException,
)
from app.core.logging import get_logger
from app.models.course import Chapter, Course, CourseStatus, Note
from app.models.user import Role, User
from app.repositories.course_repository import (
    ChapterRepository,
    CourseRepository,
    NoteRepository,
)

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# CourseService
# ---------------------------------------------------------------------------


class CourseService:
    """Business logic for course lifecycle management."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = CourseRepository(db)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    async def create(
        self,
        teacher_id: UUID,
        title: str,
        description: str | None,
        status: CourseStatus,
    ) -> Course:
        """Create a new course owned by *teacher_id*."""
        course = await self._repo.create(
            teacher_id=teacher_id,
            title=title.strip(),
            description=description,
            status=status,
        )
        logger.info(
            "Course created: id=%s title=%r teacher_id=%s", course.id, title, teacher_id
        )
        return course

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    async def get_by_id(self, course_id: UUID) -> Course:
        """Return a course or raise :class:`ResourceNotFoundException`."""
        course = await self._repo.get_by_id(course_id)
        if course is None:
            raise ResourceNotFoundException(f"Course '{course_id}' not found.")
        return course

    async def get_all(
        self, skip: int, limit: int, status: str | None = None
    ) -> tuple[list[Course], int]:
        """Return all courses with optional status filter."""
        return await self._repo.get_all(skip=skip, limit=limit, status=status)

    async def get_published(
        self, skip: int, limit: int
    ) -> tuple[list[Course], int]:
        """Return only PUBLISHED courses (student-facing endpoint)."""
        return await self._repo.get_all(
            skip=skip, limit=limit, status=CourseStatus.PUBLISHED.value
        )

    async def get_teacher_courses(
        self, teacher_id: UUID, skip: int, limit: int
    ) -> tuple[list[Course], int]:
        """Return courses owned by *teacher_id*."""
        return await self._repo.get_by_teacher(
            teacher_id=teacher_id, skip=skip, limit=limit
        )

    async def search(
        self, query: str, skip: int, limit: int
    ) -> tuple[list[Course], int]:
        """Search courses by title / description substring."""
        return await self._repo.search(query=query, skip=skip, limit=limit)

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    async def update(self, course: Course, requester: User, **kwargs) -> Course:
        """Update a course after checking ownership.

        Raises:
            AuthorizationException: If *requester* is not the owner or an admin.
        """
        await self._check_ownership(course, requester)
        updated = await self._repo.update(course, **kwargs)
        logger.info("Course updated: id=%s by user=%s", course.id, requester.id)
        return updated

    async def delete(self, course_id: UUID, requester: User) -> None:
        """Delete a course after checking ownership."""
        course = await self.get_by_id(course_id)
        await self._check_ownership(course, requester)
        await self._repo.delete(course)
        logger.info("Course deleted: id=%s by user=%s", course_id, requester.id)

    async def publish(self, course_id: UUID, requester: User) -> Course:
        """Set course status to PUBLISHED."""
        course = await self.get_by_id(course_id)
        await self._check_ownership(course, requester)
        updated = await self._repo.update(course, status=CourseStatus.PUBLISHED)
        logger.info("Course published: id=%s by user=%s", course_id, requester.id)
        return updated

    async def unpublish(self, course_id: UUID, requester: User) -> Course:
        """Set course status to DRAFT."""
        course = await self.get_by_id(course_id)
        await self._check_ownership(course, requester)
        updated = await self._repo.update(course, status=CourseStatus.DRAFT)
        logger.info("Course unpublished: id=%s by user=%s", course_id, requester.id)
        return updated

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _check_ownership(self, course: Course, requester: User) -> None:
        """Raise :class:`AuthorizationException` if *requester* has no rights."""
        if requester.role == Role.ADMIN:
            return
        if course.teacher_id != requester.id:
            raise AuthorizationException(
                "You do not have permission to modify this course."
            )


# ---------------------------------------------------------------------------
# ChapterService
# ---------------------------------------------------------------------------


class ChapterService:
    """Business logic for course chapters."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = ChapterRepository(db)
        self._course_repo = CourseRepository(db)

    async def create(
        self,
        course_id: UUID,
        requester: User,
        title: str,
        description: str | None,
        order: int | None,
    ) -> Chapter:
        """Create a chapter inside a course.

        Raises:
            ResourceNotFoundException: If the course does not exist.
            AuthorizationException: If the requester is not the teacher or admin.
        """
        course = await self._course_repo.get_by_id(course_id)
        if course is None:
            raise ResourceNotFoundException(f"Course '{course_id}' not found.")
        self._check_course_ownership(course, requester)

        # Default order to the next available position
        if order is None:
            existing = await self._repo.get_by_course(course_id)
            order = len(existing) + 1

        chapter = await self._repo.create(
            course_id=course_id,
            title=title.strip(),
            description=description,
            order=order,
        )
        logger.info(
            "Chapter created: id=%s course_id=%s by user=%s",
            chapter.id, course_id, requester.id,
        )
        return chapter

    async def get_by_course(self, course_id: UUID) -> list[Chapter]:
        """Return all chapters for a course ordered by their *order* field."""
        return await self._repo.get_by_course(course_id)

    async def get_by_id(self, chapter_id: UUID) -> Chapter:
        """Return a chapter or raise :class:`ResourceNotFoundException`."""
        chapter = await self._repo.get_by_id(chapter_id)
        if chapter is None:
            raise ResourceNotFoundException(f"Chapter '{chapter_id}' not found.")
        return chapter

    async def update(
        self, chapter_id: UUID, requester: User, **kwargs
    ) -> Chapter:
        """Update a chapter after verifying course ownership."""
        chapter = await self.get_by_id(chapter_id)
        course = await self._course_repo.get_by_id(chapter.course_id)
        self._check_course_ownership(course, requester)
        updated = await self._repo.update(chapter, **kwargs)
        logger.info("Chapter updated: id=%s by user=%s", chapter_id, requester.id)
        return updated

    async def delete(self, chapter_id: UUID, requester: User) -> None:
        """Delete a chapter after verifying course ownership."""
        chapter = await self.get_by_id(chapter_id)
        course = await self._course_repo.get_by_id(chapter.course_id)
        self._check_course_ownership(course, requester)
        await self._repo.delete(chapter)
        logger.info("Chapter deleted: id=%s by user=%s", chapter_id, requester.id)

    async def reorder(
        self, chapter_id: UUID, requester: User, new_order: int
    ) -> Chapter:
        """Change the ordinal position of a chapter."""
        chapter = await self.get_by_id(chapter_id)
        course = await self._course_repo.get_by_id(chapter.course_id)
        self._check_course_ownership(course, requester)
        updated = await self._repo.update(chapter, order=new_order)
        logger.info(
            "Chapter reordered: id=%s new_order=%d by user=%s",
            chapter_id, new_order, requester.id,
        )
        return updated

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _check_course_ownership(course: Course, requester: User) -> None:
        if requester.role == Role.ADMIN:
            return
        if course.teacher_id != requester.id:
            raise AuthorizationException(
                "You do not have permission to modify chapters of this course."
            )


# ---------------------------------------------------------------------------
# NoteService
# ---------------------------------------------------------------------------


class NoteService:
    """Business logic for notes (learning materials) within chapters."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = NoteRepository(db)
        self._chapter_repo = ChapterRepository(db)
        self._course_repo = CourseRepository(db)

    async def create(
        self,
        chapter_id: UUID,
        requester: User,
        title: str,
        content: str | None,
        file_url: str | None,
        file_name: str | None,
        content_type: str | None,
    ) -> Note:
        """Create a note inside a chapter.

        Raises:
            ResourceNotFoundException: If the chapter or its course does not exist.
            AuthorizationException: If the requester is not the teacher or admin.
        """
        chapter = await self._chapter_repo.get_by_id(chapter_id)
        if chapter is None:
            raise ResourceNotFoundException(f"Chapter '{chapter_id}' not found.")

        course = await self._course_repo.get_by_id(chapter.course_id)
        self._check_course_ownership(course, requester)

        note = await self._repo.create(
            chapter_id=chapter_id,
            title=title.strip(),
            content=content,
            file_url=file_url,
            file_name=file_name,
            content_type=content_type,
        )
        logger.info(
            "Note created: id=%s chapter_id=%s by user=%s",
            note.id, chapter_id, requester.id,
        )
        return note

    async def get_by_chapter(self, chapter_id: UUID) -> list[Note]:
        """Return all notes for a given chapter."""
        return await self._repo.get_by_chapter(chapter_id)

    async def get_by_id(self, note_id: UUID) -> Note:
        """Return a note or raise :class:`ResourceNotFoundException`."""
        note = await self._repo.get_by_id(note_id)
        if note is None:
            raise ResourceNotFoundException(f"Note '{note_id}' not found.")
        return note

    async def update(self, note_id: UUID, requester: User, **kwargs) -> Note:
        """Update a note after verifying ownership."""
        note = await self.get_by_id(note_id)
        chapter = await self._chapter_repo.get_by_id(note.chapter_id)
        course = await self._course_repo.get_by_id(chapter.course_id)
        self._check_course_ownership(course, requester)
        updated = await self._repo.update(note, **kwargs)
        logger.info("Note updated: id=%s by user=%s", note_id, requester.id)
        return updated

    async def delete(self, note_id: UUID, requester: User) -> None:
        """Delete a note after verifying ownership."""
        note = await self.get_by_id(note_id)
        chapter = await self._chapter_repo.get_by_id(note.chapter_id)
        course = await self._course_repo.get_by_id(chapter.course_id)
        self._check_course_ownership(course, requester)
        await self._repo.delete(note)
        logger.info("Note deleted: id=%s by user=%s", note_id, requester.id)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _check_course_ownership(course: Course, requester: User) -> None:
        if requester.role == Role.ADMIN:
            return
        if course.teacher_id != requester.id:
            raise AuthorizationException(
                "You do not have permission to modify notes in this course."
            )
