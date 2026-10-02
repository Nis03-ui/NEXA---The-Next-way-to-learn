from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import current_user
from app.db.session import get_db
from app.models.chat import ChatMessage, ChatSession
from app.models.user import User
from app.schemas.ai import (
    AISource,
    ChatRequest,
    ChatResponse,
    ChatSessionDetail,
    ChatSessionOut,
)
from app.services.ai import answer


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


# ============================================================
# HELPERS
# ============================================================


async def get_owned_session(
    session_id: int,
    user_id: int,
    db: AsyncSession,
) -> ChatSession:
    """
    Return a chat session belonging to the current user.

    A session owned by another user is intentionally treated
    as not found to avoid exposing its existence.
    """

    session = await db.get(
        ChatSession,
        session_id,
    )

    if session is None or session.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    return session


async def build_conversation(
    session_id: int,
    db: AsyncSession,
    limit: int = 20,
) -> str:
    """
    Build recent conversation history for the AI.

    The newest `limit` messages are used while preserving
    chronological order.
    """

    result = await db.execute(
        select(ChatMessage)
        .where(
            ChatMessage.session_id == session_id
        )
        .order_by(
            ChatMessage.created_at.desc(),
            ChatMessage.id.desc(),
        )
        .limit(limit)
    )

    messages = list(
        reversed(result.scalars().all())
    )

    return "\n".join(
        f"{message.role}: {message.content}"
        for message in messages
    )


def build_sources(result) -> list[AISource]:
    """
    Convert internal agent sources into API response schemas.
    """

    return [
        AISource(
            content_id=source.content_id,
            title=source.title,
            subject=source.subject,
            chunk_index=source.chunk_index,
            distance=source.distance,
        )
        for source in result.sources
    ]


# ============================================================
# CHAT
# ============================================================


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(
    data: ChatRequest,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message to NEXA.

    Behavior:

    - Creates a new session when `session_id` is omitted.
    - Reuses an existing session when provided.
    - Stores the user's message.
    - Builds recent conversation history.
    - Runs the NEXA agent system.
    - Stores the assistant response.
    - Returns the answer, selected agent, and RAG sources.
    """

    try:
        # --------------------------------------------------------
        # Resolve or create chat session
        # --------------------------------------------------------

        session: ChatSession | None = None

        if data.session_id is not None:
            session = await get_owned_session(
                session_id=data.session_id,
                user_id=user.id,
                db=db,
            )

        if session is None:
            session = ChatSession(
                user_id=user.id,
                title=data.message[:50],
            )

            db.add(session)

            # Generate the session ID before creating
            # the first message.
            await db.flush()

        # --------------------------------------------------------
        # Save user message
        # --------------------------------------------------------

        user_message = ChatMessage(
            session_id=session.id,
            role="user",
            content=data.message,
        )

        db.add(user_message)

        await db.flush()

        # --------------------------------------------------------
        # Build conversation history
        # --------------------------------------------------------

        conversation = await build_conversation(
            session_id=session.id,
            db=db,
            limit=20,
        )

        # --------------------------------------------------------
        # Run NEXA
        # --------------------------------------------------------

        result = await answer(
            message=data.message,
            conversation=conversation,
            db=db,
            mode=data.mode,
        )

        # --------------------------------------------------------
        # Save assistant response
        # --------------------------------------------------------

        assistant_message = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=result.answer,
        )

        db.add(assistant_message)

        # --------------------------------------------------------
        # Commit conversation
        # --------------------------------------------------------

        await db.commit()

        return ChatResponse(
            answer=result.answer,
            session_id=session.id,
            agent=result.agent,
            sources=build_sources(result),
        )

    except HTTPException:
        await db.rollback()
        raise

    except Exception as exc:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="NEXA AI service is currently unavailable.",
        ) from exc


# ============================================================
# CHAT SESSIONS
# ============================================================


@router.get(
    "/sessions",
    response_model=list[ChatSessionOut],
)
async def get_sessions(
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Return the current user's chat sessions.
    """

    result = await db.execute(
        select(ChatSession)
        .where(
            ChatSession.user_id == user.id
        )
        .order_by(
            ChatSession.created_at.desc()
        )
    )

    return result.scalars().all()


# ============================================================
# SINGLE CHAT SESSION
# ============================================================


@router.get(
    "/sessions/{session_id}",
    response_model=ChatSessionDetail,
)
async def get_session(
    session_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Return one chat session and its messages.
    """

    session = await get_owned_session(
        session_id=session_id,
        user_id=user.id,
        db=db,
    )

    result = await db.execute(
        select(ChatMessage)
        .where(
            ChatMessage.session_id == session.id
        )
        .order_by(
            ChatMessage.created_at.asc(),
            ChatMessage.id.asc(),
        )
    )

    messages = result.scalars().all()

    return ChatSessionDetail(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        messages=messages,
    )


# ============================================================
# DELETE CHAT SESSION
# ============================================================


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_session(
    session_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a user's chat session and its messages.
    """

    session = await get_owned_session(
        session_id=session_id,
        user_id=user.id,
        db=db,
    )

    try:
        await db.execute(
            delete(ChatMessage).where(
                ChatMessage.session_id == session.id
            )
        )

        await db.delete(session)

        await db.commit()

        return {
            "message": "Chat session deleted successfully."
        }

    except Exception as exc:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete chat session.",
        ) from exc