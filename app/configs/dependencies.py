from utils.repository import MongoDBRepository
from services.employees_service import EmployeesService
from services.validation_service import ValidationService
from services.filter_service import FilterService


def get_employees_service():
    return EmployeesService()

def get_validation_service():
    return ValidationService()

def get_filter_service():
    return FilterService()

def get_repository():
    return MongoDBRepository