from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser
from app.db.session import get_db
from app.schemas.auth import LoginRequest, PasswordChangeRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.schemas.common import SuccessResponse
from app.schemas.user import UserProfileResponse
from app.services.auth_service import AuthService

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=SuccessResponse[UserProfileResponse], status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await AuthService(db).register(payload.name, payload.email, payload.password)
    return SuccessResponse(data=user, message="Account created successfully")


@router.post("/login", response_model=SuccessResponse[TokenResponse])
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    tokens = await AuthService(db).login(payload.email, payload.password)
    return SuccessResponse(data=tokens, message="Login successful")


@router.post("/refresh", response_model=SuccessResponse[TokenResponse])
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    tokens = await AuthService(db).refresh_access_token(payload.refresh_token)
    return SuccessResponse(data=tokens, message="Access token refreshed")


@router.get("/me", response_model=SuccessResponse[UserProfileResponse])
async def me(current_user: CurrentUser):
    return SuccessResponse(data=current_user)


@router.post("/change-password", response_model=SuccessResponse[dict])
async def change_password(payload: PasswordChangeRequest, current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    await AuthService(db).change_password(current_user, payload.current_password, payload.new_password)
    return SuccessResponse(data={}, message="Password changed successfully")
