"""
Request middleware: correlation IDs, structured request logging, security headers.
"""
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from app.core.logging import get_logger, set_request_id

logger = get_logger(__name__)

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Injects a unique request ID into every request and response.
    Attaches it to request.state and the logging context.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        set_request_id(request_id)
        request.state.request_id = request_id

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        response.headers["X-Request-ID"] = request_id

        user_id = getattr(request.state, "user_id", None)
        logger.info(
            "HTTP request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            user_id=user_id,
            request_id=request_id,
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds security-related HTTP response headers."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response
