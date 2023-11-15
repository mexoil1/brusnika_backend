import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
import numpy as np
import redis

from configs.database import collection

get_struct_router = APIRouter(
    prefix='/structure',
    tags=['parser']
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


@get_struct_router.get('/get', response_model=List[dict])
async def get_struct(redis_client: redis.StrictRedis = Depends(get_redis_client),
                     number_position: Optional[str] = Query(None, title='Номер позиции'),
                     ul: Optional[str] = Query(None, title='ЮЛ'),
                     location: Optional[str] = Query(None, title='Локация'),
                     subdivision: Optional[str] = Query(None, title='Подразделение'),
                     department: Optional[str] = Query(None, title='Отдел'),
                     group: Optional[str] = Query(None, title='Группа'),
                     job_title: Optional[str] = Query(None, title='Должность'),
                     full_name: Optional[str] = Query(None, title='ФИО'),
                     type_of_work: Optional[str] = Query(None, title='Тип работы')):
    cache_key = 'get_struct_data'
    cached_data = get_cached_data(redis_client, cache_key)
    # if cached_data:
    #     return cached_data
    filters = {
        'number_position': number_position,
        'ul': ul,
        'location': location,
        'subdivision': subdivision,
        'department': department,
        'group': group,
        'job_title': job_title,
        'full_name': full_name,
        'type_of_work': type_of_work,
    }
    filters = {key: value for key, value in filters.items() if value is not None}

    documents = []
    async for document in collection.find(filters):
        document['_id'] = str(document['_id'])
        clean_document = {key: value if value == value else None for key, value in document.items()}
        documents.append(clean_document)

    if not documents:
        raise HTTPException(status_code=404, detail='Документы не найдены')

    set_cached_data(redis_client, cache_key, documents, 60*15)
    return documents


@get_struct_router.get('/locations', response_model=List[str])
async def get_locations(redis_client: redis.StrictRedis = Depends(get_redis_client)):
    cache_key = 'get_locations_data'
    cached_data = get_cached_data(redis_client, cache_key)
    if cached_data:
        return cached_data

    locations = set()
    async for document in collection.find({}):
        clean_document = {key: 'NaN' if isinstance(value, float) and np.isnan(
            value) else value for key, value in document.items()}
        if clean_document['location'] != 'NaN':
            locations.add(clean_document['location'])

    if not locations:
        raise HTTPException(status_code=404, detail='Документы не найдены')

    set_cached_data(redis_client, cache_key, list(locations), 60*15)

    return list(locations)
