from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import get_database_settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

db = Database()

async def connect_to_mongo():
    settings = get_database_settings()

    logger.info(f"Connecting to MongoDB at {settings.mongodb_url}...")

    db.client = AsyncIOMotorClient(
        settings.mongodb_url,
        minPoolSize=settings.mongodb_min_pool_size,
        maxPoolSize=settings.mongodb_max_pool_size,
        serverSelectionTimeoutMS=5000,  # Optional: Set a timeout for server selection
        connectTimeoutMS=5000,  # Optional: Set a timeout for connection
        socketTimeoutMS=5000  # Optional: Set a timeout for socket operations
    )

    db.database = db.client[settings.mongodb_database]

    try:
        await db.client.admin.command("ping")
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise e  # Re-raise the exception to handle it in the calling context

async def close_mongo_connection() -> None:
    if db.client:
        logger.info("Closing MongoDB connection...")
        db.client.close()
        logger.info("MongoDB connection closed.")
        db.client = None
        db.database = None


async def get_server_status() -> str:
    if db.client is None:
        return "MongoDB client is not initialized."
    try:
        await client.admin.command("ping")
        return "MongoDB server is reachable."   
    except Exception as e:
        return f"Failed to connect: {e}"
    finally:
        db.client.close()

def get_database() -> AsyncIOMotorDatabase:
    if db.database is None:
        raise RuntimeError("Database connection is not established. Call connect_to_mongo() first.")
    return db.database