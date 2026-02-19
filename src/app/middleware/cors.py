"""CORS middleware configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings


def setup_cors(app: FastAPI) -> None:
    """Setup CORS middleware."""
    # Convert list to set for methods if needed, or use as-is
    allow_methods = settings.CORS_ALLOW_METHODS
    if "*" in allow_methods:
        allow_methods = ["*"]
    
    allow_headers = settings.CORS_ALLOW_HEADERS
    if "*" in allow_headers:
        allow_headers = ["*"]
    else:
        # Add common headers if not using wildcard
        common_headers = ["Content-Type", "Authorization", "Accept"]
        allow_headers = list(set(allow_headers + common_headers))
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        expose_headers=["X-Process-Time", "X-Request-ID"],
        max_age=3600,
    )

