from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client = None
    db = None

db_state = Database()

async def connect_db():
    db_state.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_state.db = db_state.client[settings.DB_NAME]
    try:
        await db_state.db.users.create_index("email", unique=True)
        await db_state.db.resumes.create_index("user_id")
    except Exception as e:
        logger.warning(f"Index creation warning: {e}")
    logger.info(f"Connected to MongoDB: {settings.DB_NAME}")

async def disconnect_db():
    if db_state.client:
        db_state.client.close()

def get_db():
    return db_state.db