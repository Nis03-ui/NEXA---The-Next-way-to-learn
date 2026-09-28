from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser, require_roles
from app.core.exceptions import AuthorizationException, ResourceNotFoundException
from app.db.session import get_db
from app.models.course import CourseStatus
from app.models.user import Role
from app.repositories.course_repository import CourseRepository
from app.repositories.user_repository import UserRepository
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.course import (
    ChapterCreate, ChapterDetailResponse, ChapterResponse, ChapterUpdate,
    CourseCreate, CourseDetailResponse, CourseResponse, CourseUpdate,
    NoteCreate, NoteResponse, NoteUpdate,
)
from app.services.course_service import ChapterService, CourseService, NoteService

router = APIRouter(tags=["Courses"])


def page_meta(page: int, page_size: int, total: int) -> PaginationMeta:
    return PaginationMeta(page=page, page_size=page_size, total=total, total_pages=(total + page_size - 1) // page_size if total else 0)


@router.get("", response_model=PaginatedResponse[CourseResponse])
async def list_courses(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = CourseService(db)
    skip = (page - 1) * page_size
    if search:
        courses, total = await service.search(search, skip, page_size)
    else:
        courses, total = await service.get_published(skip, page_size)
    return PaginatedResponse(data=courses, pagination=page_meta(page, page_size, total))


@router.get("/mine", response_model=PaginatedResponse[CourseResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def my_courses(current_user: CurrentUser, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    service = CourseService(db)
    skip = (page - 1) * page_size
    if current_user.role == Role.ADMIN:
        courses, total = await service.get_all(skip, page_size)
    else:
        courses, total = await service.get_teacher_courses(current_user.id, skip, page_size)
    return PaginatedResponse(data=courses, pagination=page_meta(page, page_size, total))


@router.post("", response_model=SuccessResponse[CourseResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def create_course(payload: CourseCreate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    # New courses are owned by the authenticated teacher/admin.
    course = await CourseService(db).create(current_user.id, payload.title, payload.description, payload.status)
    return SuccessResponse(data=course, message="Course created successfully")


@router.get("/{course_id}", response_model=SuccessResponse[CourseDetailResponse])
async def get_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = CourseRepository(db)
    course, enrollment_count = await repo.get_with_enrollment_count(course_id)
    if course is None:
        raise ResourceNotFoundException(f"Course '{course_id}' not found.")
    teacher = await UserRepository(db).get_by_id(course.teacher_id)
    if teacher is None:
        raise ResourceNotFoundException("Course teacher not found.")
    data = {
        "id": course.id, "title": course.title, "description": course.description,
        "teacher_id": course.teacher_id, "status": course.status,
        "created_at": course.created_at, "updated_at": course.updated_at,
        "teacher": teacher, "enrollment_count": enrollment_count,
    }
    return SuccessResponse(data=data)


@router.patch("/{course_id}", response_model=SuccessResponse[CourseResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def update_course(course_id: UUID, payload: CourseUpdate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    service = CourseService(db)
    course = await service.get_by_id(course_id)
    course = await service.update(course, current_user, **payload.model_dump(exclude_unset=True))
    return SuccessResponse(data=course, message="Course updated successfully")


@router.delete("/{course_id}", response_model=SuccessResponse[dict], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def delete_course(course_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    await CourseService(db).delete(course_id, current_user)
    return SuccessResponse(data={}, message="Course deleted successfully")


@router.post("/{course_id}/publish", response_model=SuccessResponse[CourseResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def publish_course(course_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    return SuccessResponse(data=await CourseService(db).publish(course_id, current_user), message="Course published")


@router.post("/{course_id}/unpublish", response_model=SuccessResponse[CourseResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def unpublish_course(course_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    return SuccessResponse(data=await CourseService(db).unpublish(course_id, current_user), message="Course moved to draft")


@router.get("/{course_id}/chapters", response_model=SuccessResponse[list[ChapterResponse]])
async def list_chapters(course_id: UUID, db: AsyncSession = Depends(get_db)):
    await CourseService(db).get_by_id(course_id)
    return SuccessResponse(data=await ChapterService(db).get_by_course(course_id))


@router.post("/{course_id}/chapters", response_model=SuccessResponse[ChapterResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def create_chapter(course_id: UUID, payload: ChapterCreate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    chapter = await ChapterService(db).create(course_id, current_user, payload.title, payload.description, payload.order)
    return SuccessResponse(data=chapter, message="Chapter created successfully")


@router.patch("/chapters/{chapter_id}", response_model=SuccessResponse[ChapterResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def update_chapter(chapter_id: UUID, payload: ChapterUpdate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    chapter = await ChapterService(db).update(chapter_id, current_user, **payload.model_dump(exclude_unset=True))
    return SuccessResponse(data=chapter, message="Chapter updated successfully")


@router.delete("/chapters/{chapter_id}", response_model=SuccessResponse[dict], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def delete_chapter(chapter_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    await ChapterService(db).delete(chapter_id, current_user)
    return SuccessResponse(data={}, message="Chapter deleted successfully")


@router.get("/chapters/{chapter_id}/notes", response_model=SuccessResponse[list[NoteResponse]])
async def list_notes(chapter_id: UUID, db: AsyncSession = Depends(get_db)):
    await ChapterService(db).get_by_id(chapter_id)
    return SuccessResponse(data=await NoteService(db).get_by_chapter(chapter_id))


@router.post("/chapters/{chapter_id}/notes", response_model=SuccessResponse[NoteResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def create_note(chapter_id: UUID, payload: NoteCreate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    note = await NoteService(db).create(chapter_id, current_user, payload.title, payload.content, payload.file_url, None, None)
    return SuccessResponse(data=note, message="Note created successfully")


@router.patch("/notes/{note_id}", response_model=SuccessResponse[NoteResponse], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def update_note(note_id: UUID, payload: NoteUpdate, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    note = await NoteService(db).update(note_id, current_user, **payload.model_dump(exclude_unset=True))
    return SuccessResponse(data=note, message="Note updated successfully")


@router.delete("/notes/{note_id}", response_model=SuccessResponse[dict], dependencies=[Depends(require_roles(Role.TEACHER, Role.ADMIN))])
async def delete_note(note_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    await NoteService(db).delete(note_id, current_user)
    return SuccessResponse(data={}, message="Note deleted successfully")
