"""
Quiz, Question, and Attempt Pydantic v2 schemas for the NEXA LMS API.

Key design decisions
--------------------
- :class:`QuestionPublicResponse` omits ``correct_answer`` so that students
  cannot retrieve answers via the API before submitting an attempt.
- :class:`QuizDetailResponse` exposes ``correct_answer`` (for teacher/admin
  views only — route-level permission guards must enforce this).
- :class:`QuizAttemptSubmit` accepts answers as a mapping of
  ``question_id (str) -> chosen_answer (str)`` to align with the JSONB
  column in :class:`~app.models.quiz.QuizAttempt`.
"""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.quiz import QuizSource


# ---------------------------------------------------------------------------
# Question schemas
# ---------------------------------------------------------------------------


class QuestionCreate(BaseModel):
    """
    Payload for a single question within :class:`QuizCreate`.

    The ``options`` list must contain at least 2 items, and
    ``correct_answer`` must exactly match one of the provided options.
    """

    question: str = Field(..., min_length=1, description="The question text.")
    options: list[str] = Field(
        ...,
        min_length=2,
        description="Answer choices; must have at least 2 entries.",
    )
    correct_answer: str = Field(
        ..., description="The exact option string that is the correct answer."
    )
    explanation: str | None = Field(
        default=None,
        description="Optional explanation shown after an attempt is graded.",
    )

    @field_validator("options")
    @classmethod
    def options_not_empty(cls, value: list[str]) -> list[str]:
        """Ensure no option is a blank string."""
        for opt in value:
            if not opt.strip():
                raise ValueError("Each option must be a non-empty string.")
        return value

    @field_validator("correct_answer")
    @classmethod
    def correct_answer_in_options(cls, value: str, info: Any) -> str:
        """Validate that correct_answer is one of the provided options."""
        options: list[str] = (info.data or {}).get("options", [])
        if options and value not in options:
            raise ValueError(
                f"'correct_answer' must be one of the provided options. Got: {value!r}"
            )
        return value


class QuestionResponse(BaseModel):
    """
    Full question record including the correct answer.

    **Only expose this schema to teachers and administrators.**
    Students should receive :class:`QuestionPublicResponse` instead.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique question identifier.")
    quiz_id: uuid.UUID = Field(..., description="UUID of the parent quiz.")
    question: str = Field(..., description="The question text.")
    options: list[str] = Field(..., description="All answer choices.")
    correct_answer: str = Field(..., description="The correct answer string.")
    explanation: str | None = Field(
        default=None, description="Post-attempt explanation, if provided."
    )


class QuestionPublicResponse(BaseModel):
    """
    Student-facing question record — **correct_answer is intentionally omitted**.

    Route handlers must return this schema (not :class:`QuestionResponse`)
    when serving active quiz attempts to enrolled students.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique question identifier.")
    quiz_id: uuid.UUID = Field(..., description="UUID of the parent quiz.")
    question: str = Field(..., description="The question text.")
    options: list[str] = Field(..., description="All answer choices.")


# ---------------------------------------------------------------------------
# Quiz schemas
# ---------------------------------------------------------------------------


class QuizCreate(BaseModel):
    """
    Payload for ``POST /courses/{course_id}/quizzes``.

    All questions are created atomically with the quiz.
    """

    course_id: uuid.UUID = Field(..., description="UUID of the course this quiz belongs to.")
    title: str = Field(..., min_length=1, max_length=500, description="Quiz title.")
    description: str | None = Field(default=None, description="Optional quiz description.")
    questions: list[QuestionCreate] = Field(
        ...,
        min_length=1,
        description="One or more questions to create with the quiz.",
    )


class QuizUpdate(BaseModel):
    """
    Partial-update payload for ``PATCH /quizzes/{quiz_id}``.

    Questions are managed separately through their own endpoints.
    """

    title: str | None = Field(default=None, min_length=1, max_length=500, description="Updated title.")
    description: str | None = Field(default=None, description="Updated description.")


class QuizResponse(BaseModel):
    """
    Lightweight quiz record without questions.

    ``question_count`` is computed by the service layer (or a DB aggregate)
    and must be populated before serialisation.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique quiz identifier.")
    course_id: uuid.UUID = Field(..., description="UUID of the parent course.")
    title: str = Field(..., description="Quiz title.")
    description: str | None = Field(default=None, description="Quiz description.")
    source: QuizSource = Field(..., description="Whether the quiz was created manually or by AI.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    question_count: int = Field(..., ge=0, description="Total number of questions in this quiz.")


class StudentQuizDetailResponse(BaseModel):
    """Student-facing quiz detail that never exposes correct answers."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    course_id: uuid.UUID
    title: str
    description: str | None = None
    source: QuizSource
    created_at: datetime
    question_count: int
    questions: list[QuestionPublicResponse] = Field(default_factory=list)


class QuizDetailResponse(BaseModel):
    """
    Detailed quiz record including all questions with correct answers.

    **Only expose this schema to teachers and administrators.**
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique quiz identifier.")
    course_id: uuid.UUID = Field(..., description="UUID of the parent course.")
    title: str = Field(..., description="Quiz title.")
    description: str | None = Field(default=None, description="Quiz description.")
    source: QuizSource = Field(..., description="Manual or AI-generated.")
    created_at: datetime = Field(..., description="UTC timestamp of creation.")
    question_count: int = Field(..., ge=0, description="Total number of questions.")
    questions: list[QuestionResponse] = Field(
        default_factory=list,
        description="All questions including correct answers.",
    )


# ---------------------------------------------------------------------------
# Quiz attempt schemas
# ---------------------------------------------------------------------------


class QuizAttemptSubmit(BaseModel):
    """
    Payload for ``POST /quizzes/{quiz_id}/attempts``.

    ``answers`` is a mapping of ``question_id (str UUID) -> chosen_answer (str)``.
    All question IDs in the mapping must belong to the quiz being attempted;
    this is validated at the service layer.
    """

    answers: dict[str, str] = Field(
        ...,
        min_length=1,
        description="Mapping of question UUID (as string) to the chosen answer string.",
    )

    @field_validator("answers")
    @classmethod
    def answers_not_empty_values(cls, value: dict[str, str]) -> dict[str, str]:
        """Ensure no answer value is blank."""
        for q_id, answer in value.items():
            if not answer.strip():
                raise ValueError(f"Answer for question '{q_id}' must not be blank.")
        return value


class QuizAttemptResponse(BaseModel):
    """Full quiz attempt record returned after grading."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique attempt identifier.")
    quiz_id: uuid.UUID = Field(..., description="UUID of the attempted quiz.")
    student_id: uuid.UUID = Field(..., description="UUID of the student who made the attempt.")
    score: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Percentage score (0–100) calculated after grading.",
    )
    started_at: datetime = Field(..., description="UTC timestamp when the attempt was started.")
    completed_at: datetime | None = Field(
        default=None, description="UTC timestamp when the attempt was submitted and graded."
    )
    answers: dict[str, str] = Field(
        default_factory=dict,
        description="Submitted answers: question_id -> chosen_answer.",
    )


# ---------------------------------------------------------------------------
# AI quiz generation schemas
# ---------------------------------------------------------------------------


class AIQuizGenerateRequest(BaseModel):
    """
    Payload for ``POST /ai/quiz-generate``.

    Instructs the AI service to generate a quiz for the given course and topic.
    The resulting quiz will have ``source=AI_GENERATED``.
    """

    course_id: uuid.UUID = Field(..., description="UUID of the course to attach the generated quiz to.")
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Topic or subject matter the questions should cover.",
    )
    num_questions: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of questions to generate (1–20, default 5).",
    )
    difficulty: str = Field(
        default="medium",
        description="Desired difficulty level: 'easy', 'medium', or 'hard'.",
    )

    @field_validator("difficulty")
    @classmethod
    def difficulty_valid(cls, value: str) -> str:
        """Restrict difficulty to the three supported levels."""
        allowed = {"easy", "medium", "hard"}
        normalised = value.strip().lower()
        if normalised not in allowed:
            raise ValueError(f"difficulty must be one of {sorted(allowed)}; got {value!r}.")
        return normalised
