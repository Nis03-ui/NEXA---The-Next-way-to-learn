"""
AI feature Pydantic v2 schemas for the NEXA LMS API.

Covers the conversational chat agent, document summarisation, study-plan
generation, and conversation history retrieval.
"""

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Chat schemas
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    """
    Payload for ``POST /ai/chat``.

    ``session_id`` lets the frontend maintain a conversation thread across
    multiple turns.  If omitted, the backend generates a new session ID.
    ``context`` is optional free-text context (e.g. a course description or
    chapter excerpt) injected into the system prompt to ground the response.
    """

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's question or message (max 2 000 characters).",
    )
    session_id: str | None = Field(
        default=None,
        description="Existing conversation session ID.  Omit to start a new session.",
    )
    context: str | None = Field(
        default=None,
        description="Optional contextual text to help ground the AI response.",
    )


class ChatResponse(BaseModel):
    """Response returned by the ``POST /ai/chat`` endpoint."""

    model_config = ConfigDict(from_attributes=True)

    response: str = Field(..., description="The AI-generated answer.")
    session_id: str = Field(
        ..., description="Session ID to include in the next turn of this conversation."
    )
    agent_type: str = Field(
        ..., description="Identifier of the AI agent that handled the request, e.g. 'tutor'."
    )
    conversation_id: uuid.UUID = Field(
        ..., description="UUID of the persisted :class:`~app.models.ai_chat.AIConversation` record."
    )


# ---------------------------------------------------------------------------
# Summarisation schemas
# ---------------------------------------------------------------------------


class SummarizeRequest(BaseModel):
    """
    Payload for ``POST /ai/summarize``.

    ``focus`` narrows the summary to a specific aspect of the provided text,
    e.g. "key formulae" or "historical timeline".
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=50_000,
        description="The text to summarise (max 50 000 characters).",
    )
    focus: str | None = Field(
        default=None,
        max_length=500,
        description="Optional instruction on which aspect of the text to emphasise.",
    )


class SummarizeResponse(BaseModel):
    """Response returned by the ``POST /ai/summarize`` endpoint."""

    model_config = ConfigDict(from_attributes=True)

    summary: str = Field(..., description="Concise summary of the provided text.")
    key_points: list[str] = Field(
        default_factory=list,
        description="Bulleted list of the most important points extracted from the text.",
    )
    created_at: datetime = Field(
        ..., description="UTC timestamp at which the summary was generated."
    )


# ---------------------------------------------------------------------------
# Study-plan schemas
# ---------------------------------------------------------------------------


class StudyPlanRequest(BaseModel):
    """
    Payload for ``POST /ai/study-plan``.

    The AI service uses ``goal``, the date range, and ``available_hours_per_week``
    to produce a day-by-day or week-by-week study schedule stored as structured
    JSON in :class:`~app.models.ai_chat.StudyPlan`.
    """

    goal: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The learning goal or objective the plan should achieve.",
    )
    available_hours_per_week: int = Field(
        ...,
        ge=1,
        le=168,
        description="Hours the student can dedicate to studying each week (1–168).",
    )
    start_date: date = Field(..., description="Plan start date (inclusive).")
    end_date: date = Field(..., description="Plan end date (inclusive).")
    subjects: list[str] | None = Field(
        default=None,
        description="Optional list of subjects / topics to prioritise within the plan.",
    )


class StudyPlanResponse(BaseModel):
    """Response returned by the ``POST /ai/study-plan`` endpoint."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique study-plan identifier.")
    goal: str = Field(..., description="The learning goal the plan targets.")
    start_date: date = Field(..., description="Plan start date.")
    end_date: date = Field(..., description="Plan end date.")
    plan_data: dict[str, Any] = Field(
        ...,
        description=(
            "Structured plan produced by the AI, e.g. a list of weekly milestones "
            "and daily tasks represented as a JSON object."
        ),
    )
    created_at: datetime = Field(..., description="UTC timestamp of plan creation.")


# ---------------------------------------------------------------------------
# Conversation history schema
# ---------------------------------------------------------------------------


class ConversationHistoryResponse(BaseModel):
    """
    A single persisted conversation turn returned by
    ``GET /ai/conversations`` or ``GET /ai/conversations/{session_id}``.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique record identifier.")
    user_id: uuid.UUID = Field(..., description="UUID of the user who asked the question.")
    session_id: str = Field(..., description="Conversation session grouping key.")
    question: str = Field(..., description="The original question submitted by the user.")
    response: str | None = Field(
        default=None, description="The AI response; null if generation failed."
    )
    agent_type: str = Field(..., description="AI agent that handled this turn.")
    created_at: datetime = Field(..., description="UTC timestamp of the conversation turn.")
