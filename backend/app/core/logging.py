"""
Structured application logging with request correlation IDs.
Logs are JSON-formatted in production and human-readable in development.
"""
import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any, Optional

import structlog

from app.core.config import settings

# ── Context variable for request correlation ID ──────────────────────────────
request_id_var: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    return request_id_var.get() or str(uuid.uuid4())


def set_request_id(request_id: str) -> None:
    request_id_var.set(request_id)


def _add_request_id(
    logger: Any, method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Structlog processor that injects the current request ID."""
    rid = request_id_var.get()
    if rid:
        event_dict["request_id"] = rid
    return event_dict


def _censor_secrets(
    logger: Any, method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Remove sensitive keys before they reach any renderer."""
    sensitive = {
        "password",
        "password_hash",
        "access_token",
        "refresh_token",
        "api_key",
        "secret",
        "token",
        "authorization",
    }
    for key in list(event_dict.keys()):
        if key.lower() in sensitive:
            event_dict[key] = "***REDACTED***"
    return event_dict


def configure_logging() -> None:
    """Configure structlog and stdlib logging for the application."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        _add_request_id,
        _censor_secrets,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.is_production:
        renderer: Any = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(log_level)

    # Silence noisy third-party loggers in production
    for noisy in ("uvicorn.access", "httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """Return a named structlog logger."""
    return structlog.get_logger(name)
