"""User API tests."""

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_read_users_me(client, test_user_data):
    """Test reading current user."""
    # Register and login
    await client.post("/api/v1/auth/register", json=test_user_data)
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        },
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]


@pytest.mark.asyncio
async def test_read_users_me_unauthorized(client):
    """Test reading current user without authentication."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

