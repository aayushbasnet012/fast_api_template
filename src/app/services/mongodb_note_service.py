"""MongoDB Note service."""

from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status

from app.models.mongodb_note import Note
from app.schemas.mongodb_note import NoteCreate, NoteUpdate
from datetime import datetime


class MongoDBNoteService:
    """MongoDB Note service."""

    @staticmethod
    async def get_note(db: AsyncIOMotorDatabase, note_id: str, user_id: str) -> dict:
        """Get a note by ID."""
        note = await db.notes.find_one(
            {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)}
        )
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with id {note_id} not found",
            )
        note["_id"] = str(note["_id"])
        note["user_id"] = str(note["user_id"])
        return note

    @staticmethod
    async def get_notes(
        db: AsyncIOMotorDatabase,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        archived: Optional[bool] = None,
    ) -> List[dict]:
        """Get multiple notes."""
        query = {"user_id": ObjectId(user_id)}
        if archived is not None:
            query["is_archived"] = archived

        cursor = db.notes.find(query).skip(skip).limit(limit).sort("created_at", -1)
        notes = await cursor.to_list(length=limit)
        for note in notes:
            note["_id"] = str(note["_id"])
            note["user_id"] = str(note["user_id"])
        return notes

    @staticmethod
    async def create_note(
        db: AsyncIOMotorDatabase, note_create: NoteCreate, user_id: str
    ) -> dict:
        """Create a new note."""
        note_dict = note_create.model_dump()
        note_dict["user_id"] = ObjectId(user_id)
        note_dict["created_at"] = datetime.utcnow()
        note_dict["updated_at"] = datetime.utcnow()

        result = await db.notes.insert_one(note_dict)
        created_note = await db.notes.find_one({"_id": result.inserted_id})
        created_note["_id"] = str(created_note["_id"])
        created_note["user_id"] = str(created_note["user_id"])
        return created_note

    @staticmethod
    async def update_note(
        db: AsyncIOMotorDatabase, note_id: str, note_update: NoteUpdate, user_id: str
    ) -> dict:
        """Update a note."""
        # Check if note exists and belongs to user
        await MongoDBNoteService.get_note(db, note_id, user_id)

        update_data = note_update.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await db.notes.update_one(
                {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)},
                {"$set": update_data},
            )

        updated_note = await db.notes.find_one(
            {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)}
        )
        updated_note["_id"] = str(updated_note["_id"])
        updated_note["user_id"] = str(updated_note["user_id"])
        return updated_note

    @staticmethod
    async def delete_note(db: AsyncIOMotorDatabase, note_id: str, user_id: str) -> None:
        """Delete a note."""
        # Check if note exists and belongs to user
        await MongoDBNoteService.get_note(db, note_id, user_id)
        await db.notes.delete_one({"_id": ObjectId(note_id), "user_id": ObjectId(user_id)})

    @staticmethod
    async def search_notes(
        db: AsyncIOMotorDatabase,
        user_id: str,
        search_term: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[dict]:
        """Search notes by title or content."""
        query = {
            "user_id": ObjectId(user_id),
            "$or": [
                {"title": {"$regex": search_term, "$options": "i"}},
                {"content": {"$regex": search_term, "$options": "i"}},
            ],
        }

        cursor = db.notes.find(query).skip(skip).limit(limit).sort("created_at", -1)
        notes = await cursor.to_list(length=limit)
        for note in notes:
            note["_id"] = str(note["_id"])
            note["user_id"] = str(note["user_id"])
        return notes

