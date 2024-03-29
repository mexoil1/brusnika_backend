from typing import List, Optional
from fastapi import APIRouter, Depends, Query

from services.constants import FieldType
from services.employees_service import AbstractDocsService
from services.filter_service import AbstractFilterService
from services.validation_service import AbstractValidationService
from utils.repository import AbstractRepository
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


@get_struct_router.get('/get', response_model=dict)
async def get_struct(employees: AbstractDocsService = Depends(get_employees_service),
                     filters: AbstractFilterService = Depends(
                         get_filter_service),
                     validator: AbstractValidationService = Depends(
                         get_validation_service),
                     repository: AbstractRepository = Depends(get_repository),
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
                         None, description='Поле для поиска'),
                     page: int = Query(
                         1, description='Страница'),
                     limit: int = Query(
                         30, description='Лимит объектов')):
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
        'pagination': {
            'page': page,
            'limit': limit
        },
        'service_info': {
            'count_of_objects': len(documents),
            'count_of_pages': int(len(documents)/limit)+1
        },
        'employees': documents[limit*(page-1):limit*(page)],
        'new_filters': new_filters,
    }
    return result


@get_struct_router.get('/field', response_model=List[str])
async def get_subdivisions(employees: AbstractDocsService = Depends(get_employees_service),
                           repository: AbstractRepository = Depends(
                               get_repository),
                           field: FieldType = Query(..., description='Поле, значения которого надо получить')):
    '''Получение всех значений указанного поля'''
    result = await employees.get_values_of_field(repository, field)
    return result


@get_struct_router.get('/search_human', response_model=dict)
async def search_human(filters: AbstractFilterService = Depends(get_filter_service),
                       employees: AbstractDocsService = Depends(
                           get_employees_service),
                       repository: AbstractRepository = Depends(
                           get_repository),
                       search_field: Optional[str] = Query(..., description='ФИО или номер позиции')):
    '''Поиск человека по его ФИО или номеру позиции'''
    condition = await filters.get_filters_by_search(search_field)
    docs = await employees.get_all_documents(repository, condition)
    result = docs[0]
    return result
