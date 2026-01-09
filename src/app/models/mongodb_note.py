"""MongoDB Note model."""

from typing import Optional
from app.models.mongodb_base import MongoDBBaseModel, PyObjectId
from pydantic import Field


class Note(MongoDBBaseModel):
    """Note model for MongoDB."""

    title: str
    content: str
    user_id: PyObjectId
    tags: list[str] = Field(default_factory=list)
    is_archived: bool = False

    class Config:
        collection_name = "notes"

