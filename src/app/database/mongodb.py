"""MongoDB database configuration."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client
mongodb_client: AsyncIOMotorClient | None = None
mongodb_database: AsyncIOMotorDatabase | None = None


async def connect_to_mongodb():
    """Connect to MongoDB."""
    global mongodb_client, mongodb_database
    try:
        mongodb_client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
        )
        mongodb_database = mongodb_client[settings.MONGODB_DB_NAME]
        # Test connection
        await mongodb_client.admin.command("ping")
        logger.info("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongodb_connection():
    """Close MongoDB connection."""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        logger.info("MongoDB connection closed")


def get_mongodb_database() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance."""
    if mongodb_database is None:
        raise RuntimeError("MongoDB database not initialized. Call connect_to_mongodb() first.")
    return mongodb_database


def get_mongodb_client() -> AsyncIOMotorClient:
    """Get MongoDB client instance."""
    if mongodb_client is None:
        raise RuntimeError("MongoDB client not initialized. Call connect_to_mongodb() first.")
    return mongodb_client

