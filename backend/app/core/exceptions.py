"""
Custom exception hierarchy and global FastAPI exception handlers.
All API errors return a consistent JSON structure.
"""
from typing import Any, Optional
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger(__name__)


# ── Base exception ────────────────────────────────────────────────────────────

class AppException(Exception):
    """Root exception for all NEXA application errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred"

    def __init__(
        self,
        message: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message or self.__class__.message
        self.error_code = error_code or self.__class__.error_code
        self.details = details
        super().__init__(self.message)


# ── Specific exceptions ───────────────────────────────────────────────────────

class AuthenticationException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "AUTHENTICATION_FAILED"
    message = "Authentication failed"


class AuthorizationException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "FORBIDDEN"
    message = "You do not have permission to perform this action"


class ResourceNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "RESOURCE_NOT_FOUND"
    message = "The requested resource was not found"


class ValidationException(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "VALIDATION_ERROR"
    message = "Request validation failed"


class ConflictException(AppException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "CONFLICT"
    message = "A conflict occurred with the current state"


class ExternalServiceException(AppException):
    status_code = status.HTTP_502_BAD_GATEWAY
    error_code = "EXTERNAL_SERVICE_ERROR"
    message = "An external service returned an error"


class RateLimitException(AppException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = "RATE_LIMIT_EXCEEDED"
    message = "Too many requests. Please try again later"


class FileUploadException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "FILE_UPLOAD_ERROR"
    message = "File upload failed"


class AIServiceException(AppException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "AI_SERVICE_ERROR"
    message = "AI service is temporarily unavailable"


# ── Response helpers ──────────────────────────────────────────────────────────

def _error_response(
    request: Request,
    status_code: int,
    error_code: str,
    message: str,
    details: Optional[Any] = None,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid4()))
    body: dict[str, Any] = {
        "success": False,
        "error": {"code": error_code, "message": message},
        "request_id": request_id,
    }
    if details is not None:
        body["error"]["details"] = details  # type: ignore[index]
    return JSONResponse(status_code=status_code, content=body)


# ── Handlers ──────────────────────────────────────────────────────────────────

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning(
        "Application exception",
        error_code=exc.error_code,
        message=exc.message,
        path=request.url.path,
        method=request.method,
    )
    return _error_response(
        request, exc.status_code, exc.error_code, exc.message, exc.details
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    error_code_map = {
        400: "BAD_REQUEST",
        401: "AUTHENTICATION_FAILED",
        403: "FORBIDDEN",
        404: "RESOURCE_NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_ERROR",
        502: "BAD_GATEWAY",
        503: "SERVICE_UNAVAILABLE",
    }
    error_code = error_code_map.get(exc.status_code, "HTTP_ERROR")
    return _error_response(request, exc.status_code, error_code, str(exc.detail))


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = []
    for error in exc.errors():
        field = " → ".join(str(loc) for loc in error["loc"])
        errors.append({"field": field, "message": error["msg"]})
    return _error_response(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "VALIDATION_ERROR",
        "Request validation failed",
        errors,
    )


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        exc_info=exc,
    )
    return _error_response(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "INTERNAL_ERROR",
        "An unexpected error occurred",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
