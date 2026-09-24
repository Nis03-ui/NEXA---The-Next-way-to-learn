"""
User model with role-based access control.
"""
import uuid
from enum import Enum

from sqlalchemy import Boolean, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Role(str, Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(320), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    role: Mapped[Role] = mapped_column(
        String(20), nullable=False, default=Role.STUDENT
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    courses_teaching: Mapped[list["Course"]] = relationship(  # type: ignore[name-defined]
        "Course", back_populates="teacher", foreign_keys="Course.teacher_id"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(  # type: ignore[name-defined]
        "Enrollment", back_populates="student"
    )
    submissions: Mapped[list["Submission"]] = relationship(  # type: ignore[name-defined]
        "Submission", back_populates="student"
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(  # type: ignore[name-defined]
        "QuizAttempt", back_populates="student"
    )
    ai_conversations: Mapped[list["AIConversation"]] = relationship(  # type: ignore[name-defined]
        "AIConversation", back_populates="user"
    )
    study_plans: Mapped[list["StudyPlan"]] = relationship(  # type: ignore[name-defined]
        "StudyPlan", back_populates="student"
    )
    activity_logs: Mapped[list["ActivityLog"]] = relationship(  # type: ignore[name-defined]
        "ActivityLog", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"
