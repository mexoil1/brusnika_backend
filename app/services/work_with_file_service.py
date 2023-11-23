import os
import pandas
from abc import ABC, abstractmethod
from pandas import DataFrame


class AbstractWorkWithFileService(ABC):
    @abstractmethod
    async def get_directory_of_file(self):
        '''Абстрактный метод получения директории файла'''
        raise NotImplementedError
    
    @abstractmethod
    async def read_file(self):
        '''Абстрактный метод чтения файла'''
        raise NotImplementedError
    
class WorkWithFileService(AbstractWorkWithFileService):
    
    async def get_directory_of_file(self, file_name: str) -> str:
        '''Метод для получения директории файла'''
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        file_path = os.path.join(current_directory, file_name)
        return file_path
    
    async def read_file(self, file_name: str) -> DataFrame:
        '''Создание датафрейма из файла excel'''
        file_path = await self.get_directory_of_file(file_name)
        df = pandas.read_excel(file_path)
        return df
    
    