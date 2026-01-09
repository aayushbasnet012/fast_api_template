"""MongoDB Note schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NoteBase(BaseModel):
    """Base note schema."""

    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    is_archived: bool = False


class NoteCreate(NoteBase):
    """Note creation schema."""

    pass


class NoteUpdate(BaseModel):
    """Note update schema."""

    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list[str]] = None
    is_archived: Optional[bool] = None


class NoteInDB(NoteBase):
    """Note in database schema."""

    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True)


class Note(NoteInDB):
    """Note response schema."""

    pass

