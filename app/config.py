from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # Database
    database_url: str

    # App
    app_name: str = "AuditPro"
    debug: bool = False
    secret_key: str

    # Session
    session_cookie_max_age: int = 28800  # 8 hours
    session_cookie_name: str = "auditpro_session"
    session_cookie_secure: bool = False
    session_cookie_httponly: bool = True
    session_cookie_samesite: str = "Lax"

    # Azure AD SSO
    azure_ad_enabled: bool = False
    azure_ad_tenant_id: str = ""
    azure_ad_client_id: str = ""
    azure_ad_client_secret: str = ""
    azure_ad_redirect_uri: str = "http://localhost:8000/auth/azure/callback"
    azure_ad_scopes: str = "User.Read"
    azure_default_tenant_slug: str = ""

    # Logging
    log_level: str = "INFO"
    log_dir: str = "logs"
    log_max_bytes: int = 10 * 1024 * 1024
    log_backup_count: int = 5
    db_log_queries: bool = False
    db_slow_query_ms: int = 500

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env


@lru_cache
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
