from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser, require_roles
from app.db.session import get_db
from app.models.user import Role
from app.schemas.common import PaginatedResponse, PaginationMeta, SuccessResponse
from app.schemas.user import UserCreate, UserProfileResponse, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=SuccessResponse[UserProfileResponse])
async def get_profile(current_user: CurrentUser):
    return SuccessResponse(data=current_user)


@router.get("", response_model=PaginatedResponse[UserResponse], dependencies=[Depends(require_roles(Role.ADMIN))])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    skip = (page - 1) * page_size
    if search:
        users, total = await service.search(search, skip, page_size)
    else:
        users, total = await service.get_all(skip, page_size)
    pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(data=users, pagination=PaginationMeta(page=page, page_size=page_size, total=total, total_pages=pages))


@router.post("", response_model=SuccessResponse[UserResponse], status_code=201, dependencies=[Depends(require_roles(Role.ADMIN))])
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    from app.services.auth_service import AuthService
    user = await AuthService(db).register(payload.name, payload.email, payload.password, payload.role)
    return SuccessResponse(data=user, message="User created successfully")


@router.get("/{user_id}", response_model=SuccessResponse[UserResponse], dependencies=[Depends(require_roles(Role.ADMIN))])
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await UserService(db).get_by_id(user_id)
    return SuccessResponse(data=user)


@router.patch("/{user_id}", response_model=SuccessResponse[UserResponse], dependencies=[Depends(require_roles(Role.ADMIN))])
async def update_user(user_id: UUID, payload: UserUpdate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_by_id(user_id)
    user = await service.update(user, **payload.model_dump(exclude_unset=True))
    return SuccessResponse(data=user)


@router.delete("/{user_id}", response_model=SuccessResponse[dict], dependencies=[Depends(require_roles(Role.ADMIN))])
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    await UserService(db).delete(user_id)
    return SuccessResponse(data={}, message="User deleted successfully")
