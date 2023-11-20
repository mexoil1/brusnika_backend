from abc import ABC, abstractmethod
from typing import List

from configs.database import collection


class AbstractRepository(ABC):
    @abstractmethod
    async def find_docs():
        raise NotImplementedError

    @abstractmethod
    async def insert_doc():
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
