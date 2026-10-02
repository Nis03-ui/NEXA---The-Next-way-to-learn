from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NEXA API"
    environment: str = "development"

    database_url: str = "sqlite+aiosqlite:///./nexa.db"

    jwt_secret_key: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    password_reset_expire_minutes: int = 30
    email_verification_expire_minutes: int = 30

    frontend_origin: str = "http://localhost:3000"

    gemini_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()