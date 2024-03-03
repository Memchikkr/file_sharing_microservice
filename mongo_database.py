from motor.motor_asyncio import AsyncIOMotorClient

from config import ProjectConfig

client = AsyncIOMotorClient(ProjectConfig.MONGO_URL)

database = client.files_sharing