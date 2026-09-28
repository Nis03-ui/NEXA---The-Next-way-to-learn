from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import CurrentUser, require_roles
from app.core.exceptions import AuthorizationException, ResourceNotFoundException, ValidationException
from app.db.session import get_db
from app.models.quiz import Question, Quiz, QuizAttempt, QuizSource
from app.models.user import Role
from app.repositories.course_repository import CourseRepository
from app.schemas.common import SuccessResponse
from app.schemas.quiz import QuizCreate, QuizDetailResponse, StudentQuizDetailResponse, QuizResponse, QuizAttemptSubmit, QuizAttemptResponse, QuestionPublicResponse, QuestionResponse, QuizUpdate

router = APIRouter(tags=["Quizzes"])


async def get_quiz(db: AsyncSession, quiz_id: UUID) -> Quiz:
    result = await db.execute(select(Quiz).options(selectinload(Quiz.questions)).where(Quiz.id == quiz_id))
    quiz = result.scalars().first()
    if quiz is None:
        raise ResourceNotFoundException("Quiz not found")
    return quiz


async def require_course_owner(db: AsyncSession, course_id: UUID, user: CurrentUser):
    course = await CourseRepository(db).get_by_id(course_id)
    if course is None:
        raise ResourceNotFoundException("Course not found")
    if user.role != Role.ADMIN and course.teacher_id != user.id:
        raise AuthorizationException("You do not own this course")


@router.post("", response_model=SuccessResponse[QuizResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def create_quiz(payload: QuizCreate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    await require_course_owner(db, payload.course_id, current_user)
    quiz = Quiz(course_id=payload.course_id, title=payload.title.strip(), description=payload.description, created_by=current_user.id, source=QuizSource.MANUAL)
    db.add(quiz)
    await db.flush()
    for item in payload.questions:
        db.add(Question(quiz_id=quiz.id, question=item.question, options=item.options, correct_answer=item.correct_answer, explanation=item.explanation))
    await db.flush()
    await db.refresh(quiz)
    return SuccessResponse(data={"id": quiz.id, "course_id": quiz.course_id, "title": quiz.title, "description": quiz.description, "source": quiz.source, "created_at": quiz.created_at, "question_count": len(payload.questions)}, message="Quiz created successfully")


@router.get("/{quiz_id}", response_model=SuccessResponse[dict])
async def get_quiz_detail(quiz_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    quiz = await get_quiz(db, quiz_id)
    if current_user.role == Role.STUDENT:
        questions = [QuestionPublicResponse.model_validate(q) for q in quiz.questions]
        return SuccessResponse(data={"id": quiz.id, "course_id": quiz.course_id, "title": quiz.title, "description": quiz.description, "source": quiz.source, "created_at": quiz.created_at, "question_count": len(quiz.questions), "questions": questions})
    questions = [QuestionResponse.model_validate(q) for q in quiz.questions]
    return SuccessResponse(data={"id": quiz.id, "course_id": quiz.course_id, "title": quiz.title, "description": quiz.description, "source": quiz.source, "created_at": quiz.created_at, "question_count": len(quiz.questions), "questions": questions})


@router.patch("/{quiz_id}", response_model=SuccessResponse[QuizResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def update_quiz(quiz_id: UUID, payload: QuizUpdate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    quiz = await get_quiz(db, quiz_id)
    await require_course_owner(db, quiz.course_id, current_user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(quiz, key, value)
    await db.flush()
    return SuccessResponse(data={"id": quiz.id, "course_id": quiz.course_id, "title": quiz.title, "description": quiz.description, "source": quiz.source, "created_at": quiz.created_at, "question_count": len(quiz.questions)}, message="Quiz updated successfully")


@router.post("/{quiz_id}/attempts", response_model=SuccessResponse[QuizAttemptResponse], dependencies=[Depends(require_roles(Role.STUDENT))])
async def submit_quiz(quiz_id: UUID, payload: QuizAttemptSubmit, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    quiz = await get_quiz(db, quiz_id)
    question_map = {str(q.id): q for q in quiz.questions}
    unknown = set(payload.answers) - set(question_map)
    if unknown:
        raise ValidationException("One or more question IDs do not belong to this quiz")
    correct = sum(1 for qid, answer in payload.answers.items() if question_map[qid].correct_answer == answer)
    score = round((correct / len(quiz.questions)) * 100, 2) if quiz.questions else 0.0
    attempt = QuizAttempt(quiz_id=quiz_id, student_id=current_user.id, answers=payload.answers, score=score, started_at=datetime.now(timezone.utc), completed_at=datetime.now(timezone.utc))
    db.add(attempt)
    await db.flush()
    await db.refresh(attempt)
    return SuccessResponse(data=attempt, message="Quiz submitted successfully")
