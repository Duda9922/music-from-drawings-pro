"""
Database configuration and connection management
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import structlog
from app.models.drawing import Drawing
from app.models.user import User
from app.models.music import MusicGeneration
from app.core.config import settings

logger = structlog.get_logger()

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def init_db():
    """Initialize database connection"""
    try:
        # Create MongoDB client
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.DATABASE_NAME]
        
        # Initialize Beanie with document models
        await init_beanie(
            database=db.database,
            document_models=[Drawing, User, MusicGeneration]
        )
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def close_db():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Database connection closed")

def get_database():
    """Get database instance"""
    return db.database
