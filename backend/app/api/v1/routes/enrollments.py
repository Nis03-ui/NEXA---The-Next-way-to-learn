from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser, require_roles
from app.core.exceptions import ConflictException, ResourceNotFoundException
from app.db.session import get_db
from app.models.enrollment import EnrollmentStatus
from app.models.user import Role
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.enrollment import EnrollRequest, EnrollmentResponse

router = APIRouter(tags=["Enrollments"])


def meta(page: int, size: int, total: int) -> PaginationMeta:
    return PaginationMeta(page=page, page_size=size, total=total, total_pages=(total + size - 1) // size if total else 0)


@router.post("", response_model=SuccessResponse[EnrollmentResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.STUDENT))])
async def enroll(payload: EnrollRequest, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    course = await CourseRepository(db).get_by_id(payload.course_id)
    if course is None or course.status.value != "PUBLISHED":
        raise ResourceNotFoundException("Published course not found.")
    repo = EnrollmentRepository(db)
    existing = await repo.get_by_student_and_course(current_user.id, payload.course_id)
    if existing:
        raise ConflictException("You are already enrolled in this course.")
    enrollment = await repo.create(student_id=current_user.id, course_id=payload.course_id, status=EnrollmentStatus.ACTIVE)
    return SuccessResponse(data=enrollment, message="Enrollment created successfully")


@router.get("/me", response_model=PaginatedResponse[EnrollmentResponse], dependencies=[Depends(require_roles(Role.STUDENT))])
async def my_enrollments(current_user: CurrentUser, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    repo = EnrollmentRepository(db)
    skip = (page - 1) * page_size
    data = await repo.get_by_student(current_user.id, skip, page_size)
    total = await repo.count_by_student(current_user.id)
    return PaginatedResponse(data=data, pagination=meta(page, page_size, total))


@router.get("/courses/{course_id}", response_model=PaginatedResponse[EnrollmentResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def course_enrollments(course_id: UUID, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    repo = EnrollmentRepository(db)
    skip = (page - 1) * page_size
    data = await repo.get_by_course(course_id, skip, page_size)
    total = await repo.count_by_course(course_id)
    return PaginatedResponse(data=data, pagination=meta(page, page_size, total))
