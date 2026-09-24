"""
Authentication Pydantic v2 schemas for the NEXA LMS API.

Covers login, registration, token issuance, token refresh, and
password-change workflows.
"""

import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    """Payload for the ``POST /auth/login`` endpoint."""

    email: EmailStr = Field(..., description="Registered e-mail address.")
    password: str = Field(..., min_length=1, description="Account password.")


class RegisterRequest(BaseModel):
    """
    Payload for the ``POST /auth/register`` endpoint.

    Password rules:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    """

    name: str = Field(..., min_length=1, max_length=255, description="Full display name.")
    email: EmailStr = Field(..., description="Unique e-mail address for the new account.")
    password: str = Field(..., min_length=8, description="Password (see complexity rules).")

    @field_validator("password")
    @classmethod
    def password_complexity(cls, value: str) -> str:
        """Enforce uppercase, lowercase, and digit requirements."""
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")
        return value

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        """Reject names that consist solely of whitespace."""
        if not value.strip():
            raise ValueError("Name must not be blank.")
        return value.strip()


class TokenResponse(BaseModel):
    """
    JWT token pair returned after a successful authentication event
    (login, registration, or token refresh).
    """

    access_token: str = Field(..., description="Short-lived JWT access token.")
    refresh_token: str = Field(..., description="Long-lived JWT refresh token.")
    token_type: str = Field(default="bearer", description="OAuth2 token type.")
    expires_in: int = Field(
        ...,
        gt=0,
        description="Number of seconds until the access token expires.",
    )


class RefreshRequest(BaseModel):
    """Payload for the ``POST /auth/refresh`` endpoint."""

    refresh_token: str = Field(..., description="A valid, non-expired refresh token.")


class PasswordChangeRequest(BaseModel):
    """
    Payload for the ``POST /auth/change-password`` endpoint.

    The ``new_password`` field is subject to the same complexity rules as
    :class:`RegisterRequest`.
    """

    current_password: str = Field(..., min_length=1, description="The user's current password.")
    new_password: str = Field(..., min_length=8, description="The desired new password.")

    @field_validator("new_password")
    @classmethod
    def new_password_complexity(cls, value: str) -> str:
        """Enforce uppercase, lowercase, and digit requirements on the new password."""
        if not re.search(r"[A-Z]", value):
            raise ValueError("New password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("New password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("New password must contain at least one digit.")
        return value
