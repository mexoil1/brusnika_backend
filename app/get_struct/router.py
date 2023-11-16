import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
import numpy as np
import redis

from configs.database import collection
from .filters import get_new_filters, get_all_documents
from .enums import FieldType, PROJ

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
    """Получение всех значений поля"""
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
                         None, description='Тип работы')):
    """Получение всех работников"""
    filters = {
        'ul': {'$in': ul} if ul else None,
        'location': {"$in": location} if location else None,
        'subdivision': {'$in': subdivision} if subdivision else None,
        'department': {'$in': department} if department else None,
        'group': {'$in': group} if group else None,
        'job_title': {'$in': job_title} if job_title else None,
        'type_of_work': {'$in': type_of_work} if type_of_work else None,
    }
    filters = {key: value for key,
               value in filters.items() if value is not None}
    clean_filters = {}
    for key, value in filters.items():
        if 'Не указан' in value['$in']:
            clean_filters["$and"] = []
    for key, value in filters.items():
        if 'Не указан' in value['$in']:
            clean_filters["$and"].append({
                "$or": [
                    {
                        key: {
                            "$type": 1,
                            "$eq": float('nan')
                        }
                    },
                    {key: value}
                ]
            })
        else:
            clean_filters[key] = value
    print(1, filters)
    documents = await get_all_documents(collection, PROJ, clean_filters)
    if not documents:
        raise HTTPException(status_code=404, detail='Документы не найдены')
    new_filters = await get_new_filters(documents)
    if len(filters) == 1:
        all_docs = await get_all_documents(collection, PROJ)
        for doc in all_docs:
            # if doc[list(filters.keys())[0]] is not None:
            new_filters[list(filters.keys())[0]].add(
                doc[list(filters.keys())[0]])

    result = {
        'employees': documents,
        'new_filters': new_filters,
    }
    return result


@get_struct_router.get('/field', response_model=List[str])
async def get_subdivisions(field: FieldType = Query(..., description='Поле, значения которого надо получить')):
    """Получение всех значений указанного поля"""
    result = await get_values_of_field(field)
    if result == []:
        raise HTTPException(status_code=404, detail='Документы не найдены')
    return result
