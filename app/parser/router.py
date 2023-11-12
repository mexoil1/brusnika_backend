import os
import pandas as pd
from fastapi import APIRouter
from configs.database import collection


parse_router = APIRouter(
prefix='/parser',
tags = ['parser']
)

async def parse_and_upload_to_mongodb(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        data = {
            "number_position": row["Номер позиции"],
            "ul": row["ЮЛ"],
            "location": row["Локация"],
            "subdivision": row["Подразделение"],
            "department": row["Отдел"],
            "group": row["Группа"],
            "job_title": row["Должность"],
            "full_name": row["ФИО"],
            "type_of_work": row["Тип работы"]
        }
        await collection.insert_one(data)
    
@parse_router.get('/excel')
async def parse_xlsx():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    file_name = "data.xlsx"
    file_path = os.path.join(current_directory, file_name)
    await parse_and_upload_to_mongodb(file_path)
    return {"message": "success"}


