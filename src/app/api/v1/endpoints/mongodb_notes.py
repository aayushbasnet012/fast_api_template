"""MongoDB Notes endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.mongodb import get_mongodb_database
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.mongodb_note import Note as NoteSchema, NoteCreate, NoteUpdate
from app.services.mongodb_note_service import MongoDBNoteService

router = APIRouter()


async def get_mongodb_db() -> AsyncIOMotorDatabase:
    """Dependency for getting MongoDB database."""
    return get_mongodb_database()


@router.get("/", response_model=List[NoteSchema])
async def read_notes(
    skip: int = 0,
    limit: int = 100,
    archived: Optional[bool] = None,
    db: AsyncIOMotorDatabase = Depends(get_mongodb_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get all notes for the current user."""
    notes = await MongoDBNoteService.get_notes(
        db, str(current_user.id), skip=skip, limit=limit, archived=archived
    )
    return notes


@router.get("/search", response_model=List[NoteSchema])
async def search_notes(
    q: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorDatabase = Depends(get_mongodb_db),
    current_user: User = Depends(get_current_active_user),
):
    """Search notes by title or content."""
    notes = await MongoDBNoteService.search_notes(
        db, str(current_user.id), q, skip=skip, limit=limit
    )
    return notes


@router.get("/{note_id}", response_model=NoteSchema)
async def read_note(
    note_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongodb_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get a note by ID."""
    return await MongoDBNoteService.get_note(db, note_id, str(current_user.id))


@router.post("/", response_model=NoteSchema, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_create: NoteCreate,
    db: AsyncIOMotorDatabase = Depends(get_mongodb_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new note."""
    return await MongoDBNoteService.create_note(db, note_create, str(current_user.id))


@router.put("/{note_id}", response_model=NoteSchema)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    db: AsyncIOMotorDatabase = Depends(get_mongodb_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a note."""
    return await MongoDBNoteService.update_note(db, note_id, note_update, str(current_user.id))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    db: AsyncIOMotorDatabase = Depends(get_mongodb_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a note."""
    await MongoDBNoteService.delete_note(db, note_id, str(current_user.id))
    return None

