"""
Application configuration using Pydantic Settings.
All settings are loaded from environment variables.
"""
from functools import lru_cache
from typing import List

from pydantic import field_validator, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ─────────────────────────────────────────────────────────
    APP_NAME: str = "NEXA LMS API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | production | testing
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ── Security ─────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str  # postgresql+asyncpg://user:pass@host/db

    # ── Redis ────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── AI / Gemini ──────────────────────────────────────────────────────────
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_TIMEOUT_SECONDS: int = 30
    GEMINI_MAX_RETRIES: int = 3

    # ── Storage / Cloudinary ─────────────────────────────────────────────────
    CLOUDINARY_URL: str = ""
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # ── CORS ─────────────────────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # ── Logging ──────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    # ── File Uploads ─────────────────────────────────────────────────────────
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_CONTENT_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    ]

    # ── Rate Limiting ────────────────────────────────────────────────────────
    RATE_LIMIT_AUTH_PER_MINUTE: int = 10
    RATE_LIMIT_AI_PER_MINUTE: int = 20
    RATE_LIMIT_GENERAL_PER_MINUTE: int = 100

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "production", "testing"}
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


settings = get_settings()
