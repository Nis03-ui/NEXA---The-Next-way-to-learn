"""
User Pydantic v2 schemas for the NEXA LMS API.

Covers user creation, updates, and the various response shapes used by
different API consumers (admin views vs. public profile views).
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import Role
from app.schemas.auth import RegisterRequest


class UserBase(BaseModel):
    """Shared user fields used as a base for other user schemas."""

    name: str = Field(..., min_length=1, max_length=255, description="Full display name.")
    email: EmailStr = Field(..., description="Unique e-mail address.")
    role: Role = Field(default=Role.STUDENT, description="RBAC role assigned to this user.")
    is_active: bool = Field(default=True, description="Whether the account is active and can log in.")


class UserCreate(BaseModel):
    """
    Payload used by administrators to create a new user with an explicit role.

    Unlike :class:`RegisterRequest`, this schema does not enforce password
    complexity through a validator on the *create* path because the admin may
    be setting a temporary password; complexity is enforced at the service
    layer when hashing.
    """

    name: str = Field(..., min_length=1, max_length=255, description="Full display name.")
    email: EmailStr = Field(..., description="Unique e-mail address for the new account.")
    password: str = Field(..., min_length=8, description="Initial password (min 8 chars).")
    role: Role = Field(default=Role.STUDENT, description="RBAC role to assign.")


class UserUpdate(BaseModel):
    """
    Partial-update payload for ``PATCH /users/{id}``.

    All fields are optional; only supplied fields are applied.
    """

    name: str | None = Field(default=None, min_length=1, max_length=255, description="Updated display name.")
    email: EmailStr | None = Field(default=None, description="Updated e-mail address (must be unique).")
    is_active: bool | None = Field(default=None, description="Set to false to deactivate the account.")


class UserResponse(BaseModel):
    """
    Full user record returned to administrators and internal services.

    Includes the ``is_active`` flag which is hidden from the public profile.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique user identifier (UUID v4).")
    name: str = Field(..., description="Full display name.")
    email: EmailStr = Field(..., description="Registered e-mail address.")
    role: Role = Field(..., description="RBAC role.")
    is_active: bool = Field(..., description="Account active status.")
    created_at: datetime = Field(..., description="UTC timestamp of account creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")


class UserProfileResponse(BaseModel):
    """
    Public-facing user profile.

    Identical to :class:`UserResponse` but omits ``is_active`` to avoid
    leaking internal account-status information to end-users.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="Unique user identifier (UUID v4).")
    name: str = Field(..., description="Full display name.")
    email: EmailStr = Field(..., description="Registered e-mail address.")
    role: Role = Field(..., description="RBAC role.")
    created_at: datetime = Field(..., description="UTC timestamp of account creation.")
    updated_at: datetime = Field(..., description="UTC timestamp of last update.")
