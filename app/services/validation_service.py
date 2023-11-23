from abc import ABC, abstractmethod
from typing import List
from fastapi import HTTPException


class AbstractValidationService(ABC):
    @abstractmethod
    async def cleaning_filters(self):
        raise NotImplementedError

    @abstractmethod
    async def validate_filters(self):
        raise NotImplementedError

    @abstractmethod
    async def validate_result(self):
        raise NotImplementedError


class ValidationService:
    async def cleaning_filters(self, ul: str = None,
                               location: str = None,
                               subdivision: str = None,
                               department: str = None,
                               group: str = None,
                               job_title: str = None,
                               type_of_work: str = None) -> dict:
        '''Приведение фильтров в словарь'''
        filters = {
            'ul': {'$in': ul} if ul else None,
            'location': {'$in': location} if location else None,
            'subdivision': {'$in': subdivision} if subdivision else None,
            'department': {'$in': department} if department else None,
            'group': {'$in': group} if group else None,
            'job_title': {'$in': job_title} if job_title else None,
            'type_of_work': {'$in': type_of_work} if type_of_work else None,
        }
        return filters

    async def validate_filters(self, ul: str = None,
                               location: str = None,
                               subdivision: str = None,
                               department: str = None,
                               group: str = None,
                               job_title: str = None,
                               type_of_work: str = None) -> dict:
        '''Переформатирование фильтров в понятный для mongodb формат'''
        filters = await self.cleaning_filters(ul,
                                              location,
                                              subdivision,
                                              department,
                                              group,
                                              job_title,
                                              type_of_work)
        clean_filters = {}
        filters = {key: value for key,
                   value in filters.items() if value is not None}
        for key, value in filters.items():
            if 'Не указан' in value['$in']:
                clean_filters['$and'] = []
        for key, value in filters.items():
            if 'Не указан' in value['$in']:
                clean_filters['$and'].append({
                    '$or': [
                        {
                            key: {
                                '$type': 1,
                                '$eq': float('nan')
                            }
                        },
                        {key: value}
                    ]
                })
            else:
                clean_filters[key] = value
        return clean_filters

    async def validate_result(self, result: List[dict | str]) -> List[dict | str]:
        '''Валидация результата'''
        if not result:
            raise HTTPException(status_code=404, detail='Документы не найдены')
        return result
