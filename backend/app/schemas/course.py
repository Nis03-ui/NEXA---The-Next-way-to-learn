"""
Course, Chapter, and Note Pydantic v2 schemas for the NEXA LMS API.

Schemas are structured in dependency order:
    Note → Chapter → Course
so that nested response types reference already-defined classes.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.course import CourseStatus


# ---------------------------------------------------------------------------
# Note schemas
# ---------------------------------------------------------------------------


class NoteCreate(BaseModel):
    """Payload for ``POST /chapters/{chapter_id}/notes``."""

    title: str = Field(..., min_length=1, max_length=500, description="Note title.")
    content: str | None = Field(default=None, description="Rich-text or plain-text body of the note.")
    file_url: str | None = Field(
        default=None,
        max_length=2048,
        description="Optional URL of an uploaded file associated with this note.",
    )


class NoteUpdate(BaseModel):
    """
    Partial-update payload for ``PATCH /notes/{note_id}``.

    All fields are optional; only supplied fields are applied.
    """

    title: str | None = Field(default=None, min_length=1, max_length=500, description="Updated title.")
    content: str | None = Field(default=None, description="Updated note body.")
    file_url: str | None = Field(default=None, max_length=2048, description="Updated file URL.")


class NoteResponse(BaseModel):
    """Full note record returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique note identifier.")
    chapter_id: uuid.UUID = Field(..., description="UUID of the parent chapter.")
    title: str = Field(..., description="Note title.")
    content: str | None = Field(default=None, description="Note body.")
    file_url: str | None = Field(default=None, description="URL of the attached file, if any.")
    file_name: str | None = Field(default=None, description="Original filename of the attached file.")
    content_type: str | None = Field(
        default=None, description="MIME type of the attached file, e.g. 'application/pdf'."
    )
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")


# ---------------------------------------------------------------------------
# Chapter schemas
# ---------------------------------------------------------------------------


class ChapterCreate(BaseModel):
    """Payload for ``POST /courses/{course_id}/chapters``."""

    title: str = Field(..., min_length=1, max_length=500, description="Chapter title.")
    description: str | None = Field(default=None, description="Optional chapter description.")
    order: int = Field(default=0, ge=0, description="Display order within the course (0-indexed).")


class ChapterUpdate(BaseModel):
    """
    Partial-update payload for ``PATCH /chapters/{chapter_id}``.

    All fields are optional; only supplied fields are applied.
    """

    title: str | None = Field(default=None, min_length=1, max_length=500, description="Updated title.")
    description: str | None = Field(default=None, description="Updated description.")
    order: int | None = Field(default=None, ge=0, description="Updated display order.")


class ChapterResponse(BaseModel):
    """Minimal chapter record without nested notes."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique chapter identifier.")
    course_id: uuid.UUID = Field(..., description="UUID of the parent course.")
    title: str = Field(..., description="Chapter title.")
    description: str | None = Field(default=None, description="Chapter description.")
    order: int = Field(..., description="Display order within the course.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")


class ChapterDetailResponse(BaseModel):
    """
    Detailed chapter record including all nested notes.

    Used on chapter detail pages where note content must be rendered inline.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique chapter identifier.")
    course_id: uuid.UUID = Field(..., description="UUID of the parent course.")
    title: str = Field(..., description="Chapter title.")
    description: str | None = Field(default=None, description="Chapter description.")
    order: int = Field(..., description="Display order within the course.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")
    notes: list[NoteResponse] = Field(
        default_factory=list, description="All notes belonging to this chapter."
    )


# ---------------------------------------------------------------------------
# Course schemas
# ---------------------------------------------------------------------------


class CourseCreate(BaseModel):
    """Payload for ``POST /courses``."""

    title: str = Field(..., min_length=1, max_length=500, description="Course title.")
    description: str | None = Field(default=None, description="Optional course description.")
    status: CourseStatus = Field(
        default=CourseStatus.DRAFT,
        description="Initial publication status; defaults to DRAFT.",
    )


class CourseUpdate(BaseModel):
    """
    Partial-update payload for ``PATCH /courses/{course_id}``.

    All fields are optional; only supplied fields are applied.
    """

    title: str | None = Field(default=None, min_length=1, max_length=500, description="Updated title.")
    description: str | None = Field(default=None, description="Updated description.")
    status: CourseStatus | None = Field(default=None, description="Updated publication status.")


class CourseResponse(BaseModel):
    """Minimal course record without nested objects."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique course identifier.")
    title: str = Field(..., description="Course title.")
    description: str | None = Field(default=None, description="Course description.")
    teacher_id: uuid.UUID = Field(..., description="UUID of the teacher who owns this course.")
    status: CourseStatus = Field(..., description="Publication status.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")


class CourseDetailResponse(BaseModel):
    """
    Detailed course record including the teacher profile and enrollment count.

    Used on course detail pages and admin dashboards.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique course identifier.")
    title: str = Field(..., description="Course title.")
    description: str | None = Field(default=None, description="Course description.")
    teacher_id: uuid.UUID = Field(..., description="UUID of the teacher who owns this course.")
    status: CourseStatus = Field(..., description="Publication status.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")

    # Resolved after UserResponse is importable (see model_rebuild below).
    teacher: "UserResponse"  # type: ignore[name-defined]
    enrollment_count: int = Field(..., ge=0, description="Number of active enrollments for this course.")


# ---------------------------------------------------------------------------
# Resolve forward references
# ---------------------------------------------------------------------------
from app.schemas.user import UserResponse  # noqa: E402

CourseDetailResponse.model_rebuild()
