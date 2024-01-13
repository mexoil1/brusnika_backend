from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.collection import Collection
import redis
from redis import StrictRedis

from .config import Settings


async def get_collection() -> Collection:
    '''Получение коллекции MongoDB'''
    # async with AsyncIOMotorClient(Settings.MONGO_URI) as client:
    #     collection = client[Settings.DATABASE_NAME][Settings.COLLECTION_NAME]
    #     print("ХУЕСОС")
    #     print(collection)
    #     return collection
    # Подключение к MongoDB
    client = AsyncIOMotorClient(Settings.MONGO_URI)
    db = client[Settings.DATABASE_NAME]
    collection = db[Settings.COLLECTION_NAME]
    return collection


def get_redis() -> StrictRedis:
    '''Получение подключения к Redis'''
    return redis.StrictRedis(host=Settings.REDIS_HOST,
                             port=Settings.REDIS_PORT,
                             db=Settings.REDIS_DB,
                             decode_responses=True)
