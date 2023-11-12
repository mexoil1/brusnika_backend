import json
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
        document['_id'] = str(document['_id'])

        clean_document = {key: value if value == value else None for key, value in document.items()}
        documents.append(clean_document)
    
    if not documents:
        raise HTTPException(status_code=404, detail="Документы не найдены")

    json_data = json.dumps(documents, default=str)

    return json_data