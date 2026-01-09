"""Authentication endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.token import Token
from app.schemas.user import UserLogin, UserCreate, User
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Login endpoint."""
    return await AuthService.login(db, user_login)


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register endpoint."""
    return await AuthService.register(db, user_create)

