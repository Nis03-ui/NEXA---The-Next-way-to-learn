"""
Health check endpoints for liveness and readiness probes.
"""
from typing import Any

import redis.asyncio as aioredis
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import engine

health_router = APIRouter(tags=["Health"])
logger = get_logger(__name__)


@health_router.get("/health", summary="Basic health check")
async def health() -> dict[str, str]:
    """Returns 200 if the application is running."""
    return {"status": "ok", "version": settings.APP_VERSION}


@health_router.get("/health/ready", summary="Readiness check")
async def readiness() -> JSONResponse:
    """
    Returns 200 if the application is ready to serve traffic.
    Checks database and Redis connectivity.
    """
    checks: dict[str, Any] = {"status": "ok", "checks": {}}
    status_code = 200

    # Database check
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        checks["checks"]["database"] = "ok"
    except Exception as e:
        logger.error("Readiness check: database failed", error=str(e))
        checks["checks"]["database"] = "error"
        checks["status"] = "degraded"
        status_code = 503

    # Redis check
    try:
        redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await redis.ping()
        await redis.close()
        checks["checks"]["redis"] = "ok"
    except Exception as e:
        logger.warning("Readiness check: redis failed", error=str(e))
        checks["checks"]["redis"] = "unavailable"
        # Redis failure is not fatal — downgrade to warning only

    return JSONResponse(content=checks, status_code=status_code)
