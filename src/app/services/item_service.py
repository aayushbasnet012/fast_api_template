"""Item service."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Item service."""

    @staticmethod
    async def get_item(db: AsyncSession, item_id: int) -> Item:
        """Get an item by ID."""
        result = await db.execute(select(Item).filter(Item.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        return item

    @staticmethod
    async def get_items(
        db: AsyncSession, skip: int = 0, limit: int = 100, owner_id: Optional[int] = None
    ) -> list[Item]:
        """Get multiple items."""
        query = select(Item)
        if owner_id:
            query = query.filter(Item.owner_id == owner_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create_item(db: AsyncSession, item_create: ItemCreate, owner_id: int) -> Item:
        """Create a new item."""
        db_item = Item(**item_create.model_dump(), owner_id=owner_id)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def update_item(db: AsyncSession, item_id: int, item_update: ItemUpdate) -> Item:
        """Update an item."""
        item = await ItemService.get_item(db, item_id)
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def delete_item(db: AsyncSession, item_id: int) -> None:
        """Delete an item."""
        item = await ItemService.get_item(db, item_id)
        await db.delete(item)
        await db.commit()

    @staticmethod
    async def check_ownership(db: AsyncSession, item_id: int, user_id: int) -> bool:
        """Check if user owns the item."""
        item = await ItemService.get_item(db, item_id)
        return item.owner_id == user_id

