"""
Assignment and Submission ORM models.
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Assignment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "assignments"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    course: Mapped["Course"] = relationship("Course", back_populates="assignments")  # type: ignore[name-defined]
    submissions: Mapped[list["Submission"]] = relationship(
        "Submission", back_populates="assignment", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Assignment id={self.id} title={self.title!r}>"


class Submission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "submissions"

    assignment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assignments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    assignment: Mapped[Assignment] = relationship(
        "Assignment", back_populates="submissions"
    )
    student: Mapped["User"] = relationship("User", back_populates="submissions")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Submission id={self.id} assignment={self.assignment_id}>"
