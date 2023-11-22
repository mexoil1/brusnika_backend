from abc import ABC, abstractmethod
from typing import List

from configs.database import collection


class AbstractRepository(ABC):
    @abstractmethod
    async def get_docs():
        raise NotImplementedError

    @abstractmethod
    async def create_doc():
        raise NotImplementedError
    
    async def create_index(self):
        raise NotImplementedError


class MongoDBRepository(AbstractRepository):
    '''Репозиторий работы с MongoDB'''
    async def get_docs(filters: dict = None, proj: dict = None) -> List[dict]:
        """Поиск документов"""
        documents = []
        async for document in collection.find(filters, projection=proj):
            documents.append(document)
        return documents

    async def create_doc(data: dict = None) -> None:
        '''Создание одного документа'''
        collection.insert_one(data)
        return None

    async def create_index(indexes: List[tuple]) -> None:
        '''Создание индекса'''
        collection.create_index(indexes)
        return None

# def get_redis_client():
#     return redis.StrictRedis(host='brusnika_redis', port=6379, db=0, decode_responses=True)


# def get_cached_data(redis_client, cache_key):
#     cached_data = redis_client.get(cache_key)
#     if cached_data:
#         return json.loads(cached_data)
#     return None


# def set_cached_data(redis_client, cache_key, data, expire_time):
#     redis_client.setex(cache_key, expire_time, json.dumps(data))
