"""Authentication API tests."""

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_register(client, test_user_data):
    """Test user registration."""
    response = await client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate(client, test_user_data):
    """Test duplicate user registration."""
    await client.post("/api/v1/auth/register", json=test_user_data)
    response = await client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_login(client, test_user_data):
    """Test user login."""
    # Register first
    await client.post("/api/v1/auth/register", json=test_user_data)
    # Login
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"],
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword",
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

