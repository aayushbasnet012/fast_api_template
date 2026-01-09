"""Authentication service."""

from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from fastapi import HTTPException, status

from app.core.security import verify_password, get_password_hash, create_access_token
from app.config.settings import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token


class AuthService:
    """Authentication service."""

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
        """Authenticate a user."""
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def login(db: AsyncSession, user_login: UserLogin) -> Token:
        """Login a user and return access token."""
        user = await AuthService.authenticate_user(db, user_login.username, user_login.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    async def register(db: AsyncSession, user_create: UserCreate) -> User:
        """Register a new user."""
        # Check if user already exists
        result = await db.execute(
            select(User).filter(
                or_(User.email == user_create.email, User.username == user_create.username)
            )
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email or username already exists",
            )
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            is_active=user_create.is_active,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

