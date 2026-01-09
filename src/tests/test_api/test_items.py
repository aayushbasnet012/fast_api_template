"""Item API tests."""

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_item(client, test_user_data):
    """Test creating an item."""
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

    # Create item
    item_data = {
        "title": "Test Item",
        "description": "Test Description",
    }
    response = await client.post(
        "/api/v1/items/",
        json=item_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]


@pytest.mark.asyncio
async def test_read_items(client, test_user_data):
    """Test reading items."""
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

    # Get items
    response = await client.get(
        "/api/v1/items/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

