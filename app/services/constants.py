from enum import Enum


class Constants:
    PROJ_FOR_ORDINARY = {'_id': 0}
    PROJ_FOR_SEARCH = {
        '_id': 0,
        'number_position': 1
    }
    NOT_FILTERS = ('_id', 'number_position', 'full_name')
    NOT_SPECIFIED = 'not_specified'
    SEARCH_INDEX = ('$**', 'text')


class FieldType(str, Enum):
    location = 'location'
    subdivision = 'subdivision'
