from abc import ABC, abstractmethod

from .constants import Constants
from .employees_service import AbstractDocsService
from utils.repository import AbstractRepository


class AbstractFilterService(ABC):
    @abstractmethod
    async def get_new_filters(self):
        '''Абстрактный метод получения новых фильтров'''
        raise NotImplementedError

    @abstractmethod
    async def get_filters_by_one_filter(self):
        '''Абстрактный метод получения фильтров по одному фильтру'''
        raise NotImplementedError

    @abstractmethod
    async def get_filters_by_search(self):
        '''Абстрактный метод получения фильтров по поиску'''
        raise NotImplementedError


class FilterService:

    async def get_new_filters(self,
                              repository: AbstractRepository,
                              employees: AbstractDocsService,
                              documents: list,
                              clean_filters: dict) -> dict:
        '''Получение фильтров исходя из доступных сотрудников'''
        new_filters = {item: set()
                       for document in documents for item in document if item not in Constants.NOT_FILTERS}
        for document in documents:
            for item in new_filters:
                if document[item] is None:
                    document[item] = Constants.NOT_SPECIFIED
                new_filters[item].add(document[item])
        if len(clean_filters) == 1:
            new_filters = await self.get_filters_by_one_filter(repository,
                                                               employees,
                                                               new_filters,
                                                               clean_filters)
        for filter in new_filters:
            new_filters[filter] = sorted(list(new_filters[filter]))
        return new_filters

    async def get_filters_by_one_filter(self,
                                        repository: AbstractRepository,
                                        employees: AbstractDocsService,
                                        new_filters: dict,
                                        clean_filters: dict) -> dict:
        '''Функция для получения фильтров если выбран лишь один'''
        all_docs = await employees.get_all_documents(repository=repository)
        for doc in all_docs:
            if doc[list(clean_filters.keys())[0]] is None:
                doc[list(clean_filters.keys())[0]] = Constants.NOT_SPECIFIED
            new_filters[list(clean_filters.keys())[0]].add(
                doc[list(clean_filters.keys())[0]])
        return new_filters

    async def get_filters_by_search(self, search_field: str) -> dict:
        '''Получение фильтра для поиска'''
        condition = {
            "$or": [
                    {"full_name": {"$regex": search_field, "$options": "i"}},
                    {"number_position": search_field}
            ]
        }
        return condition
