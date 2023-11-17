import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
import numpy as np
import redis

from configs.database import collection
from .filters import get_new_filters, get_all_documents, validate_filters, filter_documents_by_search, get_filters_by_one_filter
from .enums import FieldType, Constants

get_struct_router = APIRouter(
    prefix='/structure',
    tags=['struct']
)


def get_redis_client():
    return redis.StrictRedis(host='brusnika_redis', port=6379, db=0, decode_responses=True)


def get_cached_data(redis_client, cache_key):
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    return None


def set_cached_data(redis_client, cache_key, data, expire_time):
    redis_client.setex(cache_key, expire_time, json.dumps(data))


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
async def get_struct(redis_client: redis.StrictRedis = Depends(get_redis_client),
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
    filters = {
        'ul': {'$in': ul} if ul else None,
        'location': {'$in': location} if location else None,
        'subdivision': {'$in': subdivision} if subdivision else None,
        'department': {'$in': department} if department else None,
        'group': {'$in': group} if group else None,
        'job_title': {'$in': job_title} if job_title else None,
        'type_of_work': {'$in': type_of_work} if type_of_work else None,
    }
    clean_filters = await validate_filters(filters)
    documents = await get_all_documents(Constants.PROJ_FOR_ORDINARY, clean_filters)
    if search:
        documents = await filter_documents_by_search(documents, search)
    if not documents:
        raise HTTPException(status_code=404, detail='Документы не найдены')
    new_filters = await get_new_filters(documents)
    if len(clean_filters) == 1:
        new_filters = await get_filters_by_one_filter(clean_filters, new_filters)
    for filter in new_filters:
        new_filters[filter] = sorted(list(new_filters[filter]))
        

    result = {
        'employees': documents,
        'new_filters': new_filters,
    }
    return result


@get_struct_router.get('/field', response_model=List[str])
async def get_subdivisions(field: FieldType = Query(..., description='Поле, значения которого надо получить')):
    '''Получение всех значений указанного поля'''
    result = await get_values_of_field(field)
    if result == []:
        raise HTTPException(status_code=404, detail='Документы не найдены')
    return result

@get_struct_router.get('/search_human', response_model=dict)
async def search_human(search_field: Optional[str] = Query(..., description='ФИО или номер позиции')):
    '''Поиск человека по его ФИО или номеру позиции'''
    condition = {
            "$or": [
                {"full_name": {"$regex": search_field, "$options": "i"}},
                {"number_position": search_field}
            ]
        }
    docs = await get_all_documents(Constants.PROJ_FOR_ORDINARY, condition)
    if not docs:
        raise HTTPException(status_code=404, detail="Humans not found")
    result = docs[0]
    return result
