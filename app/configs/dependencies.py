from utils.repository import AbstractRepository, MongoDBRepository
from services.employees_service import AbstractDocsService, EmployeesService
from services.validation_service import AbstractValidationService, ValidationService
from services.filter_service import AbstractFilterService, FilterService
from services.work_with_file_service import AbstractWorkWithFileService, WorkWithFileService


def get_employees_service() -> AbstractDocsService:
    '''Получение сервиса работы с документами'''
    return EmployeesService()


def get_validation_service() -> AbstractValidationService:
    '''Получение сервиса для валидации'''
    return ValidationService()


def get_filter_service() -> AbstractFilterService:
    '''Получение сеервиса для работы с фильтрами'''
    return FilterService()


def get_work_with_file_service() -> AbstractWorkWithFileService:
    '''Получение сервиса для работы с файлами'''
    return WorkWithFileService()


def get_repository() -> AbstractRepository:
    '''Получение репозитория'''
    return MongoDBRepository
