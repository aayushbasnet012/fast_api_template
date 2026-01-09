"""Auth service tests."""

import pytest
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin


@pytest.mark.asyncio
async def test_register_user(db_session, test_user_data):
    """Test registering a user."""
    user_create = UserCreate(**test_user_data)
    user = await AuthService.register(db_session, user_create)
    assert user.email == test_user_data["email"]
    assert user.username == test_user_data["username"]


@pytest.mark.asyncio
async def test_authenticate_user(db_session, test_user_data):
    """Test authenticating a user."""
    user_create = UserCreate(**test_user_data)
    await AuthService.register(db_session, user_create)
    user_login = UserLogin(
        username=test_user_data["username"],
        password=test_user_data["password"],
    )
    user = await AuthService.authenticate_user(
        db_session, user_login.username, user_login.password
    )
    assert user is not None
    assert user.email == test_user_data["email"]

