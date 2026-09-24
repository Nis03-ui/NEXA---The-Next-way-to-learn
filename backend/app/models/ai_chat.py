"""
AI Conversation, Study Plan, and Activity Log ORM models.
"""
import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AIConversation(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "ai_conversations"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str | None] = mapped_column(Text, nullable=True)
    agent_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="ai_conversations")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<AIConversation id={self.id} agent={self.agent_type}>"


class StudyPlan(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "study_plans"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Structured plan from AI — list of tasks/milestones
    plan_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    student: Mapped["User"] = relationship("User", back_populates="study_plans")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<StudyPlan id={self.id} student={self.student_id}>"


class ActivityLog(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "activity_logs"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource: Mapped[str | None] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="activity_logs")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<ActivityLog id={self.id} action={self.action}>"
