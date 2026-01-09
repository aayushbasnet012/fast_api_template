"""FastAPI application factory."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.api.v1.router import api_router
from app.middleware.logging import LoggingMiddleware
from app.middleware.cors import setup_cors
from app.workers.scheduler import start_scheduler, shutdown_scheduler
from app.workers.tasks import setup_scheduled_jobs
from app.database.mongodb import connect_to_mongodb, close_mongodb_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    start_scheduler()
    setup_scheduled_jobs()
    await connect_to_mongodb()
    yield
    # Shutdown
    shutdown_scheduler()
    await close_mongodb_connection()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    # Setup CORS
    setup_cors(app)

    # Add middleware
    app.add_middleware(LoggingMiddleware)

    # Include routers
    app.include_router(api_router)

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
        }

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_app()

