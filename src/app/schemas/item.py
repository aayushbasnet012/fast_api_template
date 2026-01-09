"""Item schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base item schema."""

    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """Item creation schema."""

    pass


class ItemUpdate(BaseModel):
    """Item update schema."""

    title: Optional[str] = None
    description: Optional[str] = None


class ItemInDB(ItemBase):
    """Item in database schema."""

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Item(ItemInDB):
    """Item response schema."""

    pass

