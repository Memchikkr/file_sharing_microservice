from motor.motor_asyncio import AsyncIOMotorClient
from src.file_sharing.models.file import FileDoc
from src.file_sharing.models.security import SecurityDoc
from beanie import init_beanie
from src.config import ProjectConfig


async def init_db():
    client_mongo = AsyncIOMotorClient(ProjectConfig.MONGO_URL)
    mongo_db = client_mongo['file_sharing']

    await init_beanie(database=mongo_db, document_models=[FileDoc, SecurityDoc])

