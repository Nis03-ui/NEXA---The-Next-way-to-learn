"""
Common Pydantic v2 schemas used across the NEXA LMS API.

Provides generic response wrappers, pagination metadata, and error
structures so every endpoint returns a consistent JSON envelope.
"""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Metadata describing a paginated result set."""

    page: int = Field(..., ge=1, description="Current page number (1-indexed).")
    page_size: int = Field(..., ge=1, le=200, description="Number of items per page.")
    total: int = Field(..., ge=0, description="Total number of items across all pages.")
    total_pages: int = Field(..., ge=0, description="Total number of pages.")


class SuccessResponse(BaseModel, Generic[T]):
    """
    Generic success envelope returned for single-item operations.

    Example::

        SuccessResponse[UserResponse](data=user, message="User created.")
    """

    success: bool = True
    data: T
    message: str = "Operation successful"


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic success envelope returned for list / paginated operations.

    Example::

        PaginatedResponse[CourseResponse](data=courses, pagination=meta)
    """

    success: bool = True
    data: list[T]
    pagination: PaginationMeta
    message: str = "Operation successful"


class ErrorDetail(BaseModel):
    """Structured error payload embedded inside an :class:`ErrorResponse`."""

    code: str = Field(..., description="Machine-readable error code, e.g. 'NOT_FOUND'.")
    message: str = Field(..., description="Human-readable description of the error.")
    details: Optional[Any] = Field(
        default=None,
        description="Optional additional context (validation errors, field names, etc.).",
    )


class ErrorResponse(BaseModel):
    """
    Standardised error envelope returned on all 4xx / 5xx responses.

    The ``request_id`` field mirrors the ``X-Request-ID`` response header so
    clients can correlate log entries with API responses.
    """

    success: bool = False
    error: ErrorDetail
    request_id: str = Field(..., description="Unique identifier for the failed request.")
