from pydantic_settings import BaseSettings
from functools import cached_property


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # Database
    database_url: str

    # App
    app_name: str = "Themis"
    debug: bool = False
    secret_key: str

    # Session
    session_cookie_max_age: int = 28800  # 8 hours
    session_cookie_name: str = "themis_session"
    session_cookie_secure: bool = False
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "Lax"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
