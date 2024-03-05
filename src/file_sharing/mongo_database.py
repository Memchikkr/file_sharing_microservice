from motor.motor_asyncio import AsyncIOMotorClient

from config import ProjectConfig

client_mongo = AsyncIOMotorClient(ProjectConfig.MONGO_URL)
