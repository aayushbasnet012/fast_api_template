"""User service tests."""

import pytest
from app.services.user_service import UserService
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_user(db_session, test_user_data):
    """Test creating a user."""
    user_create = UserCreate(**test_user_data)
    user = await UserService.create_user(db_session, user_create)
    assert user.email == test_user_data["email"]
    assert user.username == test_user_data["username"]
    assert user.hashed_password != test_user_data["password"]


@pytest.mark.asyncio
async def test_get_user(db_session, test_user_data):
    """Test getting a user."""
    user_create = UserCreate(**test_user_data)
    created_user = await UserService.create_user(db_session, user_create)
    user = await UserService.get_user(db_session, created_user.id)
    assert user.id == created_user.id
    assert user.email == test_user_data["email"]

