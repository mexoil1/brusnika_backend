from typing import List
import numpy as np

from .validation_service import ValidationService

from .constants import Constants
from utils.repository import AbstractRepository


class EmployeesService:
    async def filter_documents_by_search(self, repository: AbstractRepository,
                                         documents: List[dict], search: str = None) -> List[dict]:
        '''Функция для фильтрации документов по поиску'''
        await repository.create_index([('$**', 'text')])
        filters = {'$text': {'$search': search}}
        searched_docs = await repository.get_docs(filters, Constants.PROJ_FOR_SEARCH)
        searched_positions = []
        for item in searched_docs:
            searched_positions.append(item['number_position'])
        filtered_documents = [
            doc for doc in documents if doc['number_position'] in searched_positions]
        return filtered_documents

    async def get_all_documents(self, repository: AbstractRepository,
                                filters: dict = None, search: str =None) -> List[dict]:
        '''Возвращает всех найденных сотрудников'''
        documents = await repository.get_docs(filters=filters, proj=Constants.PROJ_FOR_ORDINARY)
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
        for document in await repository.get_docs():
            clean_document = {key: 'NaN' if isinstance(value, float) and np.isnan(
                value) else value for key, value in document.items()}
            if clean_document[field] != 'NaN':
                fields.add(clean_document[field])
        val = ValidationService()
        result = await val.validate_result(list(fields))
        return result
