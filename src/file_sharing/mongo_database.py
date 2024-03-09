from motor.motor_asyncio import AsyncIOMotorClient
from mongo_models import FileModel, Security
from beanie import init_beanie
from config import ProjectConfig


async def init_db():
    client_mongo = AsyncIOMotorClient(ProjectConfig.MONGO_URL)
    mongo_db = client_mongo['file_sharing']

    await init_beanie(database=mongo_db, document_models=[FileModel, Security])

