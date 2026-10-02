from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_token,
    current_user,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    ResendVerificationRequest,
    TokenResponse,
    UserOut,
    VerificationResponse,
    VerifyEmailRequest,
)
from app.services.auth import (
    create_auth_session,
    revoke_refresh_token,
    rotate_refresh_token,
)
from app.services.email_verification import (
    create_email_verification_token,
    verify_email,
)
from app.services.password_reset import (
    create_password_reset_token,
    reset_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# ============================================================
# Current User
# ============================================================

@router.get(
    "/me",
    response_model=UserOut,
)
async def get_current_user(
    user: User = Depends(current_user),
):
    return user


# ============================================================
# Forgot Password
# ============================================================

@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
)
async def forgot_password(
    data: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    user = (
        await db.execute(
            select(User).where(
                User.email == data.email
            )
        )
    ).scalar_one_or_none()

    # Keep the response generic so the endpoint does not
    # reveal whether an email is registered.
    if user is None:
        return ForgotPasswordResponse(
            message=(
                "If the account exists, "
                "a password reset token has been created."
            )
        )

    reset_token = await create_password_reset_token(
        user=user,
        db=db,
    )

    await db.commit()

    # Development only.
    # In production, this token will be sent through email
    # instead of being returned by the API.
    return ForgotPasswordResponse(
        message=(
            "If the account exists, "
            "a password reset token has been created."
        ),
        reset_token=reset_token,
    )


# ============================================================
# Reset Password
# ============================================================

@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
async def reset_user_password(
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        await reset_password(
            token=data.token,
            new_password=data.new_password,
            db=db,
        )

    except ValueError as exc:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    await db.commit()

    return MessageResponse(
        message="Password reset successfully",
    )


# ============================================================
# Email Verification
# ============================================================

@router.post(
    "/verify-email",
    response_model=VerificationResponse,
)
async def verify_user_email(
    data: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        await verify_email(
            token=data.token,
            db=db,
        )

    except ValueError as exc:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    await db.commit()

    return VerificationResponse(
        message="Email verified successfully",
    )


@router.post(
    "/resend-verification",
    response_model=VerificationResponse,
)
async def resend_verification(
    data: ResendVerificationRequest,
    db: AsyncSession = Depends(get_db),
):
    user = (
        await db.execute(
            select(User).where(
                User.email == data.email
            )
        )
    ).scalar_one_or_none()

    # Do not reveal whether an email exists.
    if user is None:
        return VerificationResponse(
            message=(
                "If the account exists and is not verified, "
                "a verification token has been created."
            )
        )

    if user.email_verified:
        return VerificationResponse(
            message="Email is already verified",
        )

    verification_token = await create_email_verification_token(
        user=user,
        db=db,
    )

    await db.commit()

    # Development only.
    # Production will send this token through email.
    return VerificationResponse(
        message=(
            "If the account exists and is not verified, "
            "a verification token has been created."
        ),
        verification_token=verification_token,
    )


# ============================================================
# Register
# ============================================================

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    existing_user = (
        await db.execute(
            select(User).where(
                User.email == data.email
            )
        )
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(
            data.password
        ),
        email_verified=False,
    )

    db.add(user)
    await db.flush()

    refresh_token, _ = await create_auth_session(
        user=user,
        db=db,
        user_agent=request.headers.get("user-agent"),
        ip_address=(
            request.client.host
            if request.client
            else None
        ),
    )

    access_token = create_token(user.id)

    await db.commit()
    await db.refresh(user)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


# ============================================================
# Login
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    user = (
        await db.execute(
            select(User).where(
                User.email == data.email
            )
        )
    ).scalar_one_or_none()

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    refresh_token, _ = await create_auth_session(
        user=user,
        db=db,
        user_agent=request.headers.get("user-agent"),
        ip_address=(
            request.client.host
            if request.client
            else None
        ),
    )

    access_token = create_token(
        user.id
    )

    await db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


# ============================================================
# Refresh Token
# ============================================================

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh(
    data: RefreshRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    try:
        (
            user,
            access_token,
            refresh_token,
        ) = await rotate_refresh_token(
            refresh_token=data.refresh_token,
            db=db,
            user_agent=request.headers.get("user-agent"),
            ip_address=(
                request.client.host
                if request.client
                else None
            ),
        )

    except ValueError as exc:
        await db.rollback()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    await db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


# ============================================================
# Logout
# ============================================================

@router.post(
    "/logout",
    response_model=MessageResponse,
)
async def logout(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    revoked = await revoke_refresh_token(
        refresh_token=data.refresh_token,
        db=db,
    )

    await db.commit()

    if not revoked:
        return MessageResponse(
            message="Session already logged out",
        )

    return MessageResponse(
        message="Logged out successfully",
    )