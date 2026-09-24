"""
NEXA LMS — FastAPI application entry point.
"""
import contextlib
from typing import AsyncGenerator

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestContextMiddleware, SecurityHeadersMiddleware
from app.db.session import engine

logger = get_logger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle."""
    configure_logging()
    logger.info(
        "NEXA LMS starting",
        environment=settings.ENVIRONMENT,
        version=settings.APP_VERSION,
    )

    # Verify database connectivity on startup
    try:
        from sqlalchemy import text
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection verified")
    except Exception as e:
        logger.error("Database connection failed on startup", error=str(e))

    # Verify Redis connectivity on startup
    try:
        redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await redis.ping()
        await redis.close()
        logger.info("Redis connection verified")
    except Exception as e:
        logger.warning("Redis connection failed on startup", error=str(e))

    yield

    logger.info("NEXA LMS shutting down")
    await engine.dispose()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "NEXA — The Next Way to Learn. "
            "AI-powered Learning Management System backend API."
        ),
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
        openapi_tags=[
            {"name": "Authentication", "description": "User registration and login"},
            {"name": "Users", "description": "User management (Admin)"},
            {"name": "Courses", "description": "Course catalog and management"},
            {"name": "CMS", "description": "Chapter and note management"},
            {"name": "Enrollments", "description": "Student course enrollment"},
            {"name": "Assignments", "description": "Assignment management and submissions"},
            {"name": "Quizzes", "description": "Quiz creation and attempts"},
            {"name": "AI", "description": "AI tutor, summarizer, and study planner"},
            {"name": "Analytics", "description": "Learning analytics and reporting"},
            {"name": "Admin", "description": "Administrative platform management"},
            {"name": "Health", "description": "Service health checks"},
        ],
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # ── Custom middleware (applied inside-out) ────────────────────────────────
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)

    # ── Exception handlers ────────────────────────────────────────────────────
    register_exception_handlers(app)

    # ── API routes ────────────────────────────────────────────────────────────
    from app.api.v1.router import api_router  # noqa: PLC0415

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # ── Health checks ─────────────────────────────────────────────────────────
    from app.api.health import health_router  # noqa: PLC0415

    app.include_router(health_router)

    return app


app = create_application()
