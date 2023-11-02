from fastapi import APIRouter, HTTPException
from configs.database import collection


get_struct_router = APIRouter(
prefix='/structure',
tags = ['parser']
)

@get_struct_router.get('/get')
async def get_struct():
    documents = []
    async for document in collection.find({}):
        documents.append(document)
    
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    
    # Преобразуем документы в список словарей (или модель данных, если определена)
    result = [doc for doc in documents]

    return result