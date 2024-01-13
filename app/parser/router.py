from fastapi import APIRouter, Depends
from services.work_with_file_service import AbstractWorkWithFileService
from configs.dependencies import get_employees_service, get_repository, get_work_with_file_service
from services.employees_service import AbstractDocsService
from utils.repository import AbstractRepository
from configs.config import Settings


parse_router = APIRouter(
    prefix='/parser',
    tags=['parser']
)


@parse_router.get('/excel', response_model=dict)
async def parse_xlsx(employees: AbstractDocsService = Depends(get_employees_service),
                     repository: AbstractRepository = Depends(get_repository),
                     reader: AbstractWorkWithFileService = Depends(get_work_with_file_service)):
    df = await reader.read_file(Settings.FILE_NAME)
    result = await employees.create_many_from_dataframe(df, repository)
    return {'message': f'Parsed {result} documents'}
