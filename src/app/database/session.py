"""Database session utilities."""

from app.database.base_class import Base
from app.config.database import engine


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

