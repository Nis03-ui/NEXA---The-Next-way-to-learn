"""
Enrollment ORM model.
"""
import uuid
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class EnrollmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"


class Enrollment(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "enrollments"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    enrolled_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    status: Mapped[EnrollmentStatus] = mapped_column(
        String(20), nullable=False, default=EnrollmentStatus.ACTIVE
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    student: Mapped["User"] = relationship("User", back_populates="enrollments")  # type: ignore[name-defined]
    course: Mapped["Course"] = relationship("Course", back_populates="enrollments")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Enrollment student={self.student_id} course={self.course_id}>"
