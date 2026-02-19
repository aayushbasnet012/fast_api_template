"""Application settings using Pydantic.

Settings are loaded in the following order (highest priority first):
1. Environment variables (from system environment or .env file)
2. Default values defined in the class

The .env file is automatically loaded if it exists in the project root.
If a variable is not found in .env or environment, the default value is used.
"""

import os
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import warnings
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings.
    
    Settings are loaded from:
    1. Environment variables (system env or .env file) - highest priority
    2. Default values below - used if not found in environment
    
    Create a .env file in the project root to override defaults.
    See .env.example for a template.
    """

    # Application
    APP_NAME: str = "FastAPI Template"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database (PostgreSQL)
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    DATABASE_ECHO: bool = False

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "fastapi_db"
    MONGODB_MAX_POOL_SIZE: int = 100
    MONGODB_MIN_POOL_SIZE: int = 10

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Redis (optional, for caching)
    REDIS_URL: Optional[str] = None

    # APScheduler
    SCHEDULER_TIMEZONE: str = "UTC"
    SCHEDULER_JOBSTORES: Optional[dict] = None
    SCHEDULER_EXECUTORS: Optional[dict] = None

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key is not using default value in production."""
        default_key = "your-secret-key-change-in-production"
        if v == default_key:
            if os.getenv("ENVIRONMENT", "development").lower() == "production":
                raise ValueError(
                    "SECRET_KEY must be changed from default value in production. "
                    "Generate a secure key using: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
                )
            else:
                warnings.warn(
                    f"Using default SECRET_KEY. This is insecure for production. "
                    f"Generate a secure key using: python -c 'import secrets; print(secrets.token_urlsafe(32))'",
                    UserWarning,
                )
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    model_config = SettingsConfigDict(
        # Load from .env file if it exists (in project root)
        env_file=".env",
        env_file_encoding="utf-8",
        # Also check system environment variables (takes precedence over .env)
        env_ignore_empty=True,
        # Case sensitive for environment variable names
        case_sensitive=True,
        # Ignore extra fields in .env that aren't defined in this class
        extra="ignore",
        # Allow reading from nested env files (e.g., .env.local, .env.production)
        env_nested_delimiter="__",
    )

    def __init__(self, **kwargs):
        """Initialize settings and log .env file status."""
        super().__init__(**kwargs)
        
        # Check if .env file exists and log status
        # Try to find .env in project root (parent of src directory)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent  # Go up from src/app/config/settings.py
        env_file_path = project_root / ".env"
        
        if env_file_path.exists():
            logger.info(f"Loading settings from .env file: {env_file_path}")
        else:
            # Also check current working directory as fallback
            cwd_env = Path(".env")
            if cwd_env.exists():
                logger.info(f"Loading settings from .env file: {cwd_env.absolute()}")
            else:
                logger.warning(
                    f".env file not found. Checked: {env_file_path} and {cwd_env.absolute()}. "
                    "Using default values. Create a .env file based on .env.example to customize settings."
                )


settings = Settings()

