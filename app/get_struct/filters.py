async def get_new_filters(documents: list) -> dict:
    """Получение фильтров исходя из доступных сотрудников"""
    not_filters = ('_id', 'number_position', 'full_name')
    result = {item: set() for document in documents for item in document if item not in not_filters}
    for document in documents:
        for item in result:
            if document[item] is not None:
                result[item].add(document[item])
    return result