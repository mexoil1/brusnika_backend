from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
import redis
from redis import StrictRedis

from .config import Settings


def get_collection() -> Collection:
    '''Получение коллекции MongoDB'''
    client = AsyncIOMotorClient(Settings.MONGO_URI)
    collection = client[Settings.DATABASE_NAME][Settings.COLLECTION_NAME]
    return collection


def get_redis() -> StrictRedis:
    '''Получение подключения к Redis'''
    return redis.StrictRedis(host=Settings.REDIS_HOST,
                             port=Settings.REDIS_PORT,
                             db=Settings.REDIS_DB,
                             decode_responses=True)
