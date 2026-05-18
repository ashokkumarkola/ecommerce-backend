# Single class config
from enum import Enum
from typing import List
from functools import lru_cache
from pydantic import Field, PostgresDsn, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Environment Enum
class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # ======== APP SETTINGS ========
    APP_NAME: str = "My FastAPI Guide"
    APP_VERSION: str = "1.0.0"

    # Environment
    ENVIRONMENT: str = Environment.LOCAL
    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1" # API_V1_STR

    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Docs
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"

    # ======== SECURITY ========
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ======== CORS ========
    ALLOWED_ORIGINS: list[AnyHttpUrl] = []

    # ======== DATABASE ========
    DATABASE_URL: PostgresDsn
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 1800
    DATABASE_POOL_PRE_PING: bool = True

    # ======== FILE UPLOADS ========
    BASE_UPLOAD_DIR: str = "uploads"

    # ======== REDIS ========
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600

    # ======== LOGGING ========
    # LOGS: bool = True
    LOG_LEVEL: str = "INFO"
    FORMATTER: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # ======== VALIDATORS ========
    @field_validator("SECRET_KEY", mode="before")
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v
    
    # ======== CONFIGURING MODELS ========
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        # env_ignore_empty=True, 
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
