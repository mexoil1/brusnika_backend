from abc import ABC, abstractmethod
from typing import List
import numpy as np
from pandas import DataFrame

from .validation_service import ValidationService
from .constants import Constants
from utils.repository import AbstractRepository


class AbstractDocsService(ABC):
    @abstractmethod
    async def filter_documents_by_search(self):
        '''Абстрактный метод фильтрации документов по поиску'''
        raise NotImplementedError

    @abstractmethod
    async def get_all_documents(self):
        '''Абстрактный метод получения документов'''
        raise NotImplementedError

    @abstractmethod
    async def get_values_of_field(self):
        '''Абстрактный метод получения значений поля'''
        raise NotImplementedError
    
    @abstractmethod
    async def create_many_from_dataframe(self):
        '''Абстрактный создания объектов из датафрейма'''
        raise NotImplementedError


class EmployeesService(AbstractDocsService):
    async def filter_documents_by_search(self, repository: AbstractRepository,
                                         documents: List[dict], search: str = None) -> List[dict]:
        '''Функция для фильтрации документов по поиску'''
        await repository.create_index([Constants.SEARCH_INDEX])
        filters = {'$text': {'$search': search}}
        searched_docs = await repository.get_data(filters, Constants.PROJ_FOR_SEARCH)
        searched_positions = []
        for item in searched_docs:
            searched_positions.append(item['number_position'])
        filtered_documents = [
            doc for doc in documents if doc['number_position'] in searched_positions]
        return filtered_documents

    async def get_all_documents(self, repository: AbstractRepository,
                                filters: dict = None, search: str = None) -> List[dict]:
        '''Возвращает всех найденных сотрудников'''
        documents = await repository.get_data(filters=filters, proj=Constants.PROJ_FOR_ORDINARY)
        clean_documents = []
        for document in documents:
            clean_document = {key: value if value ==
                              value else None for key, value in document.items()}
            clean_documents.append(clean_document)
        if search:
            clean_documents = await self.filter_documents_by_search(repository, clean_documents, search)
        val = ValidationService()
        result = await val.validate_result(clean_documents)
        return result

    async def get_values_of_field(self,
                                  repository: AbstractRepository,
                                  field: str) -> List[str]:
        '''Получение всех значений поля'''
        fields = set()
        for document in await repository.get_data():
            clean_document = {key: 'NaN' if isinstance(value, float) and np.isnan(
                value) else value for key, value in document.items()}
            if clean_document[field] != 'NaN':
                fields.add(clean_document[field])
        val = ValidationService()
        result = await val.validate_result(list(fields))
        return result
    
    async def create_many_from_dataframe(self, df: DataFrame, repository: AbstractRepository) -> int:
        '''Создание объектов из pandas dataframe'''
        i = 0
        for _, row in df.iterrows():
            count_of_items += 1
            data = {
                'number_position': row['Номер позиции'],
                'ul': row['ЮЛ'],
                'location': row['Локация'],
                'subdivision': row['Подразделение'],
                'department': row['Отдел'],
                'group': row['Группа'],
                'job_title': row['Должность'],
                'full_name': row['ФИО'],
                'type_of_work': row['Тип работы']
            }
            await repository.create_data(data)
        return i
