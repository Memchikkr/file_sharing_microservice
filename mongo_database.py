from motor.motor_asyncio import AsyncIOMotorClient

from src.file_sharing.config import ProjectConfig

client = AsyncIOMotorClient(ProjectConfig.MONGO_URL)

database = client.files_sharing

files_names = database.files