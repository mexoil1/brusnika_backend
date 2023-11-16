from enum import Enum

PROJ={'_id': False}
class FieldType(str, Enum):
    location = "location"
    subdivision = "subdivision"
