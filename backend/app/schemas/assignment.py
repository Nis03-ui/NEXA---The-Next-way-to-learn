"""
Assignment and Submission Pydantic v2 schemas for the NEXA LMS API.

Covers assignment creation / update, submission by students, and
grading / feedback by teachers.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Assignment schemas
# ---------------------------------------------------------------------------


class AssignmentCreate(BaseModel):
    """Payload for ``POST /courses/{course_id}/assignments``."""

    course_id: uuid.UUID = Field(..., description="UUID of the course this assignment belongs to.")
    title: str = Field(..., min_length=1, max_length=500, description="Assignment title.")
    description: str | None = Field(default=None, description="Full assignment instructions.")
    deadline: datetime | None = Field(
        default=None,
        description="Optional submission deadline (timezone-aware UTC datetime).",
    )


class AssignmentUpdate(BaseModel):
    """
    Partial-update payload for ``PATCH /assignments/{assignment_id}``.

    All fields are optional; only supplied fields are applied.
    """

    title: str | None = Field(default=None, min_length=1, max_length=500, description="Updated title.")
    description: str | None = Field(default=None, description="Updated instructions.")
    deadline: datetime | None = Field(default=None, description="Updated deadline (set to null to remove).")


class AssignmentResponse(BaseModel):
    """Assignment record returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique assignment identifier.")
    course_id: uuid.UUID = Field(..., description="UUID of the parent course.")
    title: str = Field(..., description="Assignment title.")
    description: str | None = Field(default=None, description="Assignment instructions.")
    deadline: datetime | None = Field(default=None, description="Submission deadline (UTC), if set.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")


# ---------------------------------------------------------------------------
# Submission schemas
# ---------------------------------------------------------------------------


class SubmissionCreate(BaseModel):
    """
    Payload for ``POST /assignments/{assignment_id}/submissions``.

    A submission must have at least one of ``content`` or ``file_url``;
    this invariant is enforced at the service layer.
    """

    content: str | None = Field(default=None, description="Text body of the submission.")
    file_url: str | None = Field(
        default=None,
        max_length=2048,
        description="URL of the uploaded submission file.",
    )


class SubmissionUpdate(BaseModel):
    """
    Payload for ``PATCH /submissions/{submission_id}`` (teacher grading).

    Only ``score`` and ``feedback`` may be updated after submission.
    """

    score: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Numeric grade (0–100) awarded by the teacher.",
    )
    feedback: str | None = Field(
        default=None,
        description="Written feedback provided by the teacher.",
    )


class SubmissionResponse(BaseModel):
    """Full submission record returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique submission identifier.")
    assignment_id: uuid.UUID = Field(..., description="UUID of the parent assignment.")
    student_id: uuid.UUID = Field(..., description="UUID of the submitting student.")
    content: str | None = Field(default=None, description="Text body of the submission.")
    file_url: str | None = Field(default=None, description="URL of the uploaded file, if any.")
    submitted_at: datetime | None = Field(
        default=None, description="UTC timestamp when the submission was finalised."
    )
    score: float | None = Field(default=None, description="Teacher-assigned score (0–100).")
    feedback: str | None = Field(default=None, description="Teacher feedback text.")
    created_at: datetime = Field(..., description="UTC timestamp of record creation.")
