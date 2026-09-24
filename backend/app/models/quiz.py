"""
Quiz, Question, and QuizAttempt ORM models.
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class QuizSource(str, Enum):
    MANUAL = "MANUAL"
    AI_GENERATED = "AI_GENERATED"


class Quiz(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "quizzes"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    source: Mapped[QuizSource] = mapped_column(
        String(20), nullable=False, default=QuizSource.MANUAL
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    course: Mapped["Course"] = relationship("Course", back_populates="quizzes")  # type: ignore[name-defined]
    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )
    attempts: Mapped[list["QuizAttempt"]] = relationship(
        "QuizAttempt", back_populates="quiz", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Quiz id={self.id} title={self.title!r}>"


class Question(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "questions"

    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    # JSONB array of option strings, e.g. ["A. ...", "B. ...", ...]
    options: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    correct_answer: Mapped[str] = mapped_column(String(500), nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    quiz: Mapped[Quiz] = relationship("Quiz", back_populates="questions")

    def __repr__(self) -> str:
        return f"<Question id={self.id}>"


class QuizAttempt(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "quiz_attempts"

    quiz_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # JSONB mapping of question_id -> chosen_answer
    answers: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    quiz: Mapped[Quiz] = relationship("Quiz", back_populates="attempts")
    student: Mapped["User"] = relationship("User", back_populates="quiz_attempts")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<QuizAttempt id={self.id} score={self.score}>"
