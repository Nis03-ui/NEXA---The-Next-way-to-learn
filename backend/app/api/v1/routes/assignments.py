from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import CurrentUser, require_roles
from app.core.exceptions import AuthorizationException, ConflictException, ResourceNotFoundException, ValidationException
from app.db.session import get_db
from app.models.assignment import Assignment, Submission
from app.models.user import Role
from app.repositories.assignment_repository import AssignmentRepository, SubmissionRepository
from app.repositories.course_repository import CourseRepository
from app.schemas.assignment import AssignmentCreate, AssignmentResponse, AssignmentUpdate, SubmissionCreate, SubmissionResponse, SubmissionUpdate
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse

router = APIRouter(tags=["Assignments"])


def meta(page: int, size: int, total: int) -> PaginationMeta:
    return PaginationMeta(page=page, page_size=size, total=total, total_pages=(total + size - 1) // size if total else 0)


async def require_course_owner(db: AsyncSession, course_id: UUID, user: CurrentUser) -> None:
    course = await CourseRepository(db).get_by_id(course_id)
    if course is None:
        raise ResourceNotFoundException("Course not found")
    if user.role != Role.ADMIN and course.teacher_id != user.id:
        raise AuthorizationException("You do not own this course")


@router.get("/course/{course_id}", response_model=PaginatedResponse[AssignmentResponse])
async def list_assignments(course_id: UUID, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    repo = AssignmentRepository(db)
    skip = (page - 1) * page_size
    data = await repo.get_by_course(course_id, skip, page_size)
    total = await repo.count_by_course(course_id)
    return PaginatedResponse(data=data, pagination=meta(page, page_size, total))


@router.post("", response_model=SuccessResponse[AssignmentResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def create_assignment(payload: AssignmentCreate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    await require_course_owner(db, payload.course_id, current_user)
    assignment = await AssignmentRepository(db).create(course_id=payload.course_id, title=payload.title.strip(), description=payload.description, deadline=payload.deadline)
    return SuccessResponse(data=assignment, message="Assignment created successfully")


@router.get("/{assignment_id}", response_model=SuccessResponse[AssignmentResponse])
async def get_assignment(assignment_id: UUID, db: AsyncSession = Depends(get_db)):
    assignment = await AssignmentRepository(db).get_by_id(assignment_id)
    if assignment is None:
        raise ResourceNotFoundException("Assignment not found")
    return SuccessResponse(data=assignment)


@router.patch("/{assignment_id}", response_model=SuccessResponse[AssignmentResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def update_assignment(assignment_id: UUID, payload: AssignmentUpdate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    repo = AssignmentRepository(db)
    assignment = await repo.get_by_id(assignment_id)
    if assignment is None:
        raise ResourceNotFoundException("Assignment not found")
    await require_course_owner(db, assignment.course_id, current_user)
    assignment = await repo.update(assignment, **payload.model_dump(exclude_unset=True))
    return SuccessResponse(data=assignment, message="Assignment updated successfully")


@router.delete("/{assignment_id}", response_model=SuccessResponse[dict], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def delete_assignment(assignment_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    repo = AssignmentRepository(db)
    assignment = await repo.get_by_id(assignment_id)
    if assignment is None:
        raise ResourceNotFoundException("Assignment not found")
    await require_course_owner(db, assignment.course_id, current_user)
    await repo.delete(assignment)
    return SuccessResponse(data={}, message="Assignment deleted successfully")


@router.post("/{assignment_id}/submissions", response_model=SuccessResponse[SubmissionResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.STUDENT))])
async def submit_assignment(assignment_id: UUID, payload: SubmissionCreate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    if not payload.content and not payload.file_url:
        raise ValidationException("A submission must contain content or a file URL")
    assignment = await AssignmentRepository(db).get_by_id(assignment_id)
    if assignment is None:
        raise ResourceNotFoundException("Assignment not found")
    repo = SubmissionRepository(db)
    existing = await repo.get_by_assignment_and_student(assignment_id, current_user.id)
    if existing:
        raise ConflictException("You have already submitted this assignment")
    submission = await repo.create(assignment_id=assignment_id, student_id=current_user.id, content=payload.content, file_url=payload.file_url, submitted_at=datetime.now(timezone.utc))
    return SuccessResponse(data=submission, message="Assignment submitted successfully")


@router.get("/{assignment_id}/submissions", response_model=PaginatedResponse[SubmissionResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def list_submissions(assignment_id: UUID, current_user: CurrentUser, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    assignment = await AssignmentRepository(db).get_by_id(assignment_id)
    if assignment is None:
        raise ResourceNotFoundException("Assignment not found")
    await require_course_owner(db, assignment.course_id, current_user)
    repo = SubmissionRepository(db)
    skip = (page - 1) * page_size
    data = await repo.get_by_assignment(assignment_id, skip, page_size)
    stats = await repo.get_submission_stats_for_assignment(assignment_id)
    return PaginatedResponse(data=data, pagination=meta(page, page_size, stats["total"]))


@router.patch("/submissions/{submission_id}", response_model=SuccessResponse[SubmissionResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def grade_submission(submission_id: UUID, payload: SubmissionUpdate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    repo = SubmissionRepository(db)
    submission = await repo.get_by_id(submission_id)
    if submission is None:
        raise ResourceNotFoundException("Submission not found")
    assignment = await AssignmentRepository(db).get_by_id(submission.assignment_id)
    if assignment is None:
        raise ResourceNotFoundException("Assignment not found")
    await require_course_owner(db, assignment.course_id, current_user)
    submission = await repo.update(submission, **payload.model_dump(exclude_unset=True))
    return SuccessResponse(data=submission, message="Submission graded successfully")
