from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


TutorMode = Literal[
    "normal",
    "explain",
    "study",
    "code",
    "quiz",
]


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=12000,
    )

    session_id: int | None = None

    mode: TutorMode = "normal"


class AISource(BaseModel):
    content_id: int
    title: str
    subject: str
    chunk_index: int
    distance: float


class ChatResponse(BaseModel):
    answer: str
    session_id: int
    agent: str
    sources: list[AISource] = Field(
        default_factory=list
    )


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ChatSessionOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ChatSessionDetail(ChatSessionOut):
    messages: list[ChatMessageOut] = Field(
        default_factory=list
    )