from typing import List, Optional
from fastapi import APIRouter, Depends,  Query
import numpy as np

from configs.database import collection
from .enums import FieldType
from configs.dependencies import (
    get_employees_service,
    get_filter_service,
    get_repository,
    get_validation_service
    )


get_struct_router = APIRouter(
    prefix='/structure',
    tags=['struct']
)


async def get_values_of_field(field: str) -> List[str]:
    '''Получение всех значений поля'''
    fields = set()
    async for document in collection.find({}):
        clean_document = {key: 'NaN' if isinstance(value, float) and np.isnan(
            value) else value for key, value in document.items()}
        if clean_document[field] != 'NaN':
            fields.add(clean_document[field])
    return list(fields)


@get_struct_router.get('/get', response_model=dict)
async def get_struct(employees=Depends(get_employees_service),
                     filters=Depends(get_filter_service),
                     validator=Depends(get_validation_service),
                     repository=Depends(get_repository),
                     ul: List[Optional[str]] = Query(
                         None, description='ЮЛ'),
                     location: List[Optional[str]] = Query(
                         None, description='Локация'),
                     subdivision: List[Optional[str]] = Query(
                         None, description='Подразделение'),
                     department: List[Optional[str]] = Query(
                         None, description='Отдел'),
                     group: List[Optional[str]] = Query(
                         None, description='Группа'),
                     job_title: List[Optional[str]] = Query(
                         None, description='Должность'),
                     type_of_work: List[Optional[str]] = Query(
                         None, description='Тип работы'),
                     search: Optional[str] = Query(
                         None, description='Поле для поиска')):
    '''Получение всех работников'''
    clean_filters = await validator.validate_filters(ul=ul,
                                                     location=location,
                                                     subdivision=subdivision,
                                                     department=department,
                                                     group=group,
                                                     job_title=job_title,
                                                     type_of_work=type_of_work)
    documents = await employees.get_all_documents(repository=repository,
                                                  filters=clean_filters,
                                                  search=search)
    new_filters = await filters.get_new_filters(repository=repository,
                                                employees=employees,
                                                documents=documents,
                                                clean_filters=clean_filters)
    result = {
        'employees': documents,
        'new_filters': new_filters,
    }
    return result


@get_struct_router.get('/field', response_model=List[str])
async def get_subdivisions(employees=Depends(get_employees_service),
                           repository=Depends(get_repository),
                           field: FieldType = Query(..., description='Поле, значения которого надо получить')):
    '''Получение всех значений указанного поля'''
    result = await employees.get_values_of_field(repository, field)
    return result


@get_struct_router.get('/search_human', response_model=dict)
async def search_human(filters=Depends(get_filter_service),
                       employees=Depends(get_employees_service),
                       repository=Depends(get_repository),
                       search_field: Optional[str] = Query(..., description='ФИО или номер позиции')):
    '''Поиск человека по его ФИО или номеру позиции'''
    condition = await filters.get_filters_by_search(search_field)
    docs = await employees.get_all_documents(repository, condition)
    result = docs[0]
    return result
