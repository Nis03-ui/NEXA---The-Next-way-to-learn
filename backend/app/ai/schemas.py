"""
Pydantic schemas for validating structured AI output.
AI-generated content is never trusted without validation.
"""
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class GeneratedQuestion(BaseModel):
    """Validated AI-generated quiz question."""

    question: str = Field(..., min_length=10)
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=10)

    @field_validator("correct_answer")
    @classmethod
    def correct_answer_must_be_in_options(cls, v: str, info: object) -> str:
        # Validated after options are set
        return v

    def model_post_init(self, __context: object) -> None:
        if self.correct_answer not in self.options:
            raise ValueError(
                f"correct_answer '{self.correct_answer}' must be one of the options"
            )


class AIQuizOutput(BaseModel):
    """Structured output from the Quiz Agent."""

    questions: list[GeneratedQuestion] = Field(..., min_length=1)


class AISummaryOutput(BaseModel):
    """Structured output from the Summarizer Agent."""

    summary: str = Field(..., min_length=10)
    key_points: list[str] = Field(..., min_length=1, max_length=10)


class StudyTask(BaseModel):
    """A single task within a study plan week."""

    task: str = Field(..., min_length=5)
    duration_hours: float = Field(..., gt=0, le=24)
    priority: Literal["high", "medium", "low"] = "medium"


class StudyMilestone(BaseModel):
    """Weekly milestone in a study plan."""

    week: int = Field(..., ge=1)
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    tasks: list[StudyTask] = Field(..., min_length=1)


class AIStudyPlanOutput(BaseModel):
    """Structured output from the Study Planner Agent."""

    overview: str = Field(..., min_length=20)
    weekly_hours: float = Field(..., gt=0)
    total_weeks: int = Field(..., ge=1)
    milestones: list[StudyMilestone] = Field(..., min_length=1)
    tips: list[str] = Field(..., min_length=2, max_length=10)
