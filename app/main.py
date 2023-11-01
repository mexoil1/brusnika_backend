from fastapi import FastAPI
from parser.parse_xlsx import parse_router


app = FastAPI()


app.include_router(parse_router)


