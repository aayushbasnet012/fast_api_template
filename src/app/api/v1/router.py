"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, items, mongodb_notes
from app.config.settings import settings

api_router = APIRouter(prefix=settings.API_V1_PREFIX)

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(mongodb_notes.router, prefix="/notes", tags=["notes"])

