from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import orchestrator
from app.core.dependencies import CurrentUser, require_roles
from app.core.exceptions import AuthorizationException, ResourceNotFoundException, ValidationException
from app.db.session import get_db
from app.models.ai_chat import AIConversation, StudyPlan
from app.models.quiz import Question, Quiz, QuizSource
from app.models.user import Role
from app.repositories.course_repository import CourseRepository
from app.schemas.ai import ChatRequest, ChatResponse, ConversationHistoryResponse, StudyPlanRequest, StudyPlanResponse, SummarizeRequest, SummarizeResponse
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.quiz import AIQuizGenerateRequest, QuizResponse

router = APIRouter(tags=["AI"])


def meta(page: int, size: int, total: int) -> PaginationMeta:
    return PaginationMeta(page=page, page_size=size, total=total, total_pages=(total + size - 1) // size if total else 0)


@router.post("/chat", response_model=SuccessResponse[ChatResponse])
async def chat(payload: ChatRequest, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    session_id = payload.session_id or str(uuid4())
    response = await orchestrator.tutor.answer(payload.question, payload.context)
    conversation = AIConversation(user_id=current_user.id, session_id=session_id, question=payload.question, response=response, agent_type="tutor")
    db.add(conversation)
    await db.flush()
    await db.refresh(conversation)
    data = {"response": response, "session_id": session_id, "agent_type": "tutor", "conversation_id": conversation.id}
    return SuccessResponse(data=data, message="AI response generated")


@router.get("/conversations", response_model=PaginatedResponse[ConversationHistoryResponse])
async def conversations(current_user: CurrentUser, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    base = select(AIConversation).where(AIConversation.user_id == current_user.id).order_by(AIConversation.created_at.desc())
    total = await db.scalar(select(func.count()).select_from(AIConversation).where(AIConversation.user_id == current_user.id))
    rows = (await db.execute(base.offset((page - 1) * page_size).limit(page_size))).scalars().all()
    return PaginatedResponse(data=list(rows), pagination=meta(page, page_size, int(total or 0)))


@router.get("/conversations/{session_id}", response_model=SuccessResponse[list[ConversationHistoryResponse]])
async def conversation_session(session_id: str, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(AIConversation).where(AIConversation.user_id == current_user.id, AIConversation.session_id == session_id).order_by(AIConversation.created_at.asc()))).scalars().all()
    return SuccessResponse(data=list(rows))


@router.post("/summarize", response_model=SuccessResponse[SummarizeResponse])
async def summarize(payload: SummarizeRequest, current_user: CurrentUser):
    result = await orchestrator.summarizer.summarize(payload.text, payload.focus)
    data = {"summary": result.summary, "key_points": result.key_points, "created_at": datetime.now(timezone.utc)}
    return SuccessResponse(data=data, message="Content summarized successfully")


@router.post("/study-plan", response_model=SuccessResponse[StudyPlanResponse])
async def study_plan(payload: StudyPlanRequest, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    if payload.end_date < payload.start_date:
        raise ValidationException("end_date must be on or after start_date")
    result = await orchestrator.study_planner.create_plan(payload.goal, payload.available_hours_per_week, payload.start_date, payload.end_date, payload.subjects)
    plan = StudyPlan(student_id=current_user.id, goal=payload.goal, start_date=payload.start_date, end_date=payload.end_date, plan_data=result.model_dump())
    db.add(plan)
    await db.flush()
    await db.refresh(plan)
    return SuccessResponse(data=plan, message="Study plan generated successfully")


@router.post("/quiz-generate", response_model=SuccessResponse[QuizResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def generate_quiz(payload: AIQuizGenerateRequest, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):

    course = await CourseRepository(db).get_by_id(payload.course_id)
    if course is None:
        raise ResourceNotFoundException("Course not found")
    if current_user.role.value == "TEACHER" and course.teacher_id != current_user.id:
        raise AuthorizationException("Only the course teacher can generate a quiz for this course")
    questions = await orchestrator.quiz.generate_questions(payload.topic, payload.num_questions, payload.difficulty)
    quiz = Quiz(course_id=payload.course_id, title=f"AI Quiz: {payload.topic}", description=f"AI-generated {payload.difficulty} quiz on {payload.topic}", created_by=current_user.id, source=QuizSource.AI_GENERATED)
    db.add(quiz)
    await db.flush()
    for q in questions:
        db.add(Question(quiz_id=quiz.id, question=q.question, options=q.options, correct_answer=q.correct_answer, explanation=q.explanation))
    await db.flush()
    await db.refresh(quiz)
    data = {"id": quiz.id, "course_id": quiz.course_id, "title": quiz.title, "description": quiz.description, "source": quiz.source, "created_at": quiz.created_at, "question_count": len(questions)}
    return SuccessResponse(data=data, message="AI quiz generated successfully")
