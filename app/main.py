from fastapi import FastAPI
from parser.router import parse_router
from get_struct.router import get_struct_router


app = FastAPI()


app.include_router(parse_router)
app.include_router(get_struct_router)
