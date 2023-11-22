from utils.repository import AbstractRepository


class FilterService:
    
    async def get_new_filters(self,
                              repository: AbstractRepository,
                              employees,
                              documents: list,
                              clean_filters: dict) -> dict:
        '''Получение фильтров исходя из доступных сотрудников'''
        not_filters = ('_id', 'number_position', 'full_name')
        new_filters = {item: set()
                for document in documents for item in document if item not in not_filters}
        for document in documents:
            for item in new_filters:
                if document[item] is None:
                    document[item] = 'not_specified'
                new_filters[item].add(document[item])
        if len(clean_filters) == 1:
            new_filters = await self.get_filters_by_one_filter(repository,
                                                               employees,
                                                               new_filters,
                                                               clean_filters)
        for filter in new_filters:
            new_filters[filter] = sorted(list(new_filters[filter]))
        return new_filters
    
    async def get_filters_by_one_filter(self,
                                        repository: AbstractRepository,
                                        employees,
                                        new_filters: dict,
                                        clean_filters: dict) -> dict:
        '''Функция для получения фильтров если выбран лишь один'''
        all_docs = await employees.get_all_documents(repository=repository)
        for doc in all_docs:
            if doc[list(clean_filters.keys())[0]] is None:
                doc[list(clean_filters.keys())[0]] = 'not_specified'
            new_filters[list(clean_filters.keys())[0]].add(
                doc[list(clean_filters.keys())[0]])
        return new_filters
    
    async def get_filters_by_search(self, search_field: str) -> dict:
        '''Получение фильтра для поиска'''
        condition = {
            "$or": [
                    {"full_name": {"$regex": search_field, "$options": "i"}},
                    {"number_position": search_field}
            ]
        }
        return condition