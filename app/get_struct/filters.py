from typing import List

from configs.database import collection
from .enums import Constants


async def get_new_filters(documents: list) -> dict:
    '''Получение фильтров исходя из доступных сотрудников'''
    not_filters = ('_id', 'number_position', 'full_name')
    result = {item: set()
              for document in documents for item in document if item not in not_filters}
    for document in documents:
        for item in result:
            if document[item] is None:
                document[item] = 'not_specified'
            result[item].add(document[item])
    return result


async def get_all_documents(proj: dict, filters: dict = None) -> List[dict]:
    documents = []
    print(proj)
    async for document in collection.find(filters, projection=proj):
        clean_document = {key: value if value ==
                          value else None for key, value in document.items()}
        documents.append(clean_document)
    return documents


async def validate_filters(filters: dict) -> dict:
    '''Переформатирование фильтров в понятный для mongodb формат'''
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


async def filter_documents_by_search(documents: List[dict], search: str) -> List[dict]:
    '''Функция для фильтрации документов по поиску'''
    await collection.create_index([('$**', 'text')])
    searched_docs = await collection.find({'$text': {'$search': search}},
                                          projection=Constants.PROJ_FOR_SEARCH).to_list(length=100)
    searched_positions = []
    for item in searched_docs:
        searched_positions.append(item['number_position'])
    filtered_documents = [
        doc for doc in documents if doc['number_position'] in searched_positions]
    return filtered_documents


async def get_filters_by_one_filter(clean_filters: dict, new_filters: dict) -> dict:
    '''Функция для получения фильтров если выбран лишь один'''
    all_docs = await get_all_documents(Constants.PROJ_FOR_ORDINARY)
    for doc in all_docs:
        if doc[list(clean_filters.keys())[0]] is None:
            doc[list(clean_filters.keys())[0]] = 'not_specified'
        new_filters[list(clean_filters.keys())[0]].add(
            doc[list(clean_filters.keys())[0]])
    return new_filters
