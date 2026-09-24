"""
Analytics Pydantic v2 schemas for the NEXA LMS API.

Provides role-specific analytics payloads for students, teachers, and
platform administrators.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StudentAnalytics(BaseModel):
    """
    Aggregated learning statistics returned for the authenticated student.

    ``recent_activity`` is a time-ordered list of lightweight activity dicts,
    e.g. ``[{"action": "quiz_attempt", "resource_id": "<uuid>", "at": "<iso>"}]``.
    """

    model_config = ConfigDict(from_attributes=True)

    courses_enrolled: int = Field(..., ge=0, description="Total courses the student has enrolled in.")
    courses_completed: int = Field(..., ge=0, description="Courses whose enrollment status is COMPLETED.")
    quiz_attempts_total: int = Field(..., ge=0, description="Lifetime number of quiz attempts.")
    quiz_average_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Average quiz score expressed as a percentage (0–100).",
    )
    assignments_submitted: int = Field(..., ge=0, description="Assignments with at least one submission.")
    assignments_graded: int = Field(..., ge=0, description="Submissions that have received a score.")
    recent_activity: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Up to 20 most-recent activity log entries for the student.",
    )


class TeacherAnalytics(BaseModel):
    """
    Aggregated teaching statistics returned for the authenticated teacher.

    ``course_stats`` contains per-course breakdowns, e.g.
    ``[{"course_id": "<uuid>", "title": "...", "enrolled": 30, "avg_score": 72.5}]``.
    """

    model_config = ConfigDict(from_attributes=True)

    total_courses: int = Field(..., ge=0, description="Courses created by this teacher.")
    total_students_enrolled: int = Field(
        ..., ge=0, description="Unique students enrolled across all teacher courses."
    )
    total_quizzes: int = Field(..., ge=0, description="Quizzes created across all teacher courses.")
    total_assignments: int = Field(
        ..., ge=0, description="Assignments created across all teacher courses."
    )
    average_quiz_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Mean quiz score across all attempts on teacher-owned quizzes (0–100).",
    )
    submission_rate: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description=(
            "Ratio of submitted assignments to total expected submissions "
            "(enrolled students × assignments), expressed as a value between 0 and 1."
        ),
    )
    course_stats: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Per-course breakdown of enrollment and performance metrics.",
    )


class AdminAnalytics(BaseModel):
    """
    Platform-wide statistics returned for administrators.

    ``recent_registrations`` counts new user accounts created in the last 30
    calendar days.  ``platform_activity`` is a time-series list suitable for
    rendering a dashboard chart.
    """

    model_config = ConfigDict(from_attributes=True)

    total_users: int = Field(..., ge=0, description="Total registered users across all roles.")
    total_students: int = Field(..., ge=0, description="Users with role STUDENT.")
    total_teachers: int = Field(..., ge=0, description="Users with role TEACHER.")
    total_admins: int = Field(..., ge=0, description="Users with role ADMIN.")
    total_courses: int = Field(..., ge=0, description="Total courses on the platform.")
    total_enrollments: int = Field(..., ge=0, description="Total enrollment records.")
    total_quiz_attempts: int = Field(..., ge=0, description="Total quiz attempt records.")
    recent_registrations: int = Field(
        ...,
        ge=0,
        description="Number of new user accounts created in the last 30 days.",
    )
    platform_activity: list[dict[str, Any]] = Field(
        default_factory=list,
        description=(
            "Time-series activity data, e.g. daily active users or event counts, "
            "suitable for dashboard charts."
        ),
    )
