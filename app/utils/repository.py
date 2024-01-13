import json
import asyncio
from abc import ABC, abstractmethod
from typing import List
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.collection import Collection
from redis import StrictRedis

from configs.database import get_collection, get_redis


class AbstractRepository(ABC):
    @abstractmethod
    async def get_data():
        '''Абстрактный метод получения данных'''
        raise NotImplementedError

    @abstractmethod
    async def create_data():
        '''Абстрактный метод создания данных'''
        raise NotImplementedError

    async def create_index(self):
        '''Абстрактный метод создания индекса'''
        raise NotImplementedError


class MongoDBRepository(AbstractRepository):
    '''Репозиторий работы с MongoDB'''
    async def get_data(collection: Collection = None, filters: dict = None, proj: dict = None) -> List[dict]:
        """Получение документов"""
        documents = []
        if collection is None:
            collection = await get_collection()
        print(collection)
        print("ПИДАРАС")
        async for document in collection.find(filters, projection=proj):
            print('хуй')
            documents.append(document)
        return documents

    async def create_data(collection: Collection = Depends(get_collection), data: List[dict] = None) -> None:
        '''Создание одного документа'''
        if data:
            await collection.insert_many(data)
        return None

    async def create_index(collection: Collection = Depends(get_collection), indexes: List[tuple] = None) -> None:
        '''Создание индекса'''
        collection.create_index(indexes)
        return None


class RedisRepository(AbstractRepository):

    @staticmethod
    async def get_data(cache_key: str) -> None | dict | list:

        return await asyncio.to_thread(RedisRepository._get_data_sync, cache_key)

    @staticmethod
    def _get_data_sync(cache_key: str, redis_client: StrictRedis = Depends(get_redis),) -> None | dict | list:
        '''Получение кэша'''
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        return None

    @staticmethod
    async def create_data(cache_key: str, data: dict | list, expire_time: int) -> None:
        await asyncio.to_thread(RedisRepository._create_data_sync, cache_key, data, expire_time)

    @staticmethod
    def _create_data_sync(cache_key: str, data: dict | list, expire_time: int, redis_client: StrictRedis = Depends(get_redis),) -> None:
        '''Создание кэша'''
        redis_client.setex(cache_key, expire_time, data)
