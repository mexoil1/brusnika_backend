from motor.motor_asyncio import AsyncIOMotorClient

from .config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


client = AsyncIOMotorClient(MONGO_URI)
collection = client[DATABASE_NAME][COLLECTION_NAME]