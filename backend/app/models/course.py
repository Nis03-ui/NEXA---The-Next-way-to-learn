"""
Course, Chapter, and Note ORM models.
"""
import uuid
from enum import Enum

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CourseStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class Course(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "courses"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[CourseStatus] = mapped_column(
        String(20), nullable=False, default=CourseStatus.DRAFT
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    teacher: Mapped["User"] = relationship(  # type: ignore[name-defined]
        "User", back_populates="courses_teaching", foreign_keys=[teacher_id]
    )
    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter", back_populates="course", cascade="all, delete-orphan", order_by="Chapter.order"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(  # type: ignore[name-defined]
        "Enrollment", back_populates="course", cascade="all, delete-orphan"
    )
    assignments: Mapped[list["Assignment"]] = relationship(  # type: ignore[name-defined]
        "Assignment", back_populates="course", cascade="all, delete-orphan"
    )
    quizzes: Mapped[list["Quiz"]] = relationship(  # type: ignore[name-defined]
        "Quiz", back_populates="course", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Course id={self.id} title={self.title!r}>"


class Chapter(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "chapters"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # ── Relationships ─────────────────────────────────────────────────────────
    course: Mapped[Course] = relationship("Course", back_populates="chapters")
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="chapter", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Chapter id={self.id} title={self.title!r} order={self.order}>"


class Note(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "notes"

    chapter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    file_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    chapter: Mapped[Chapter] = relationship("Chapter", back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note id={self.id} title={self.title!r}>"
