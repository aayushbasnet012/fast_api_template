"""Item endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.item import Item as ItemSchema, ItemCreate, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter()


@router.get("/", response_model=List[ItemSchema])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all items for the current user."""
    items = await ItemService.get_items(db, skip=skip, limit=limit, owner_id=current_user.id)
    return items


@router.get("/{item_id}", response_model=ItemSchema)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get an item by ID."""
    item = await ItemService.get_item(db, item_id)
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return item


@router.post("/", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_create: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new item."""
    return await ItemService.create_item(db, item_create, owner_id=current_user.id)


@router.put("/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update an item."""
    if not await ItemService.check_ownership(db, item_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return await ItemService.update_item(db, item_id, item_update)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an item."""
    if not await ItemService.check_ownership(db, item_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    await ItemService.delete_item(db, item_id)
    return None

