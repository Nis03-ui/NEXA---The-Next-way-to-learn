"""
Enrollment Pydantic v2 schemas for the NEXA LMS API.

Covers enrollment creation and the response shapes returned at different
levels of detail.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enrollment import EnrollmentStatus


class EnrollRequest(BaseModel):
    """Payload for ``POST /enrollments`` — enroll the authenticated student in a course."""

    course_id: uuid.UUID = Field(..., description="UUID of the course to enroll in.")


class EnrollmentResponse(BaseModel):
    """
    Minimal enrollment record.

    Returned for list endpoints where embedding full course and student
    objects would be too expensive.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique enrollment identifier.")
    student_id: uuid.UUID = Field(..., description="UUID of the enrolled student.")
    course_id: uuid.UUID = Field(..., description="UUID of the course.")
    enrolled_at: datetime = Field(..., description="UTC timestamp when the enrollment was created.")
    status: EnrollmentStatus = Field(..., description="Current enrollment status.")


class EnrollmentDetailResponse(BaseModel):
    """
    Detailed enrollment record with nested course and student objects.

    Used when the caller needs full context, e.g. on an admin dashboard or a
    student's enrollment detail page.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique enrollment identifier.")
    student_id: uuid.UUID = Field(..., description="UUID of the enrolled student.")
    course_id: uuid.UUID = Field(..., description="UUID of the course.")
    enrolled_at: datetime = Field(..., description="UTC timestamp when the enrollment was created.")
    status: EnrollmentStatus = Field(..., description="Current enrollment status.")

    # Deferred import to avoid circular imports at module load time.
    # Pydantic v2 resolves forward references lazily via model_rebuild().
    course: "CourseResponse"  # type: ignore[name-defined]
    student: "UserResponse"  # type: ignore[name-defined]


# ---------------------------------------------------------------------------
# Resolve forward references after both dependency modules are importable.
# ---------------------------------------------------------------------------
from app.schemas.course import CourseResponse  # noqa: E402
from app.schemas.user import UserResponse  # noqa: E402

EnrollmentDetailResponse.model_rebuild()
