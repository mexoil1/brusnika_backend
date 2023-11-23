import os
from dotenv import load_dotenv


load_dotenv()
class Settings:
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    REDIS_HOST=os.getenv('REDIS_HOST')
    REDIS_PORT=os.getenv('REDIS_PORT')
    REDIS_DB=os.getenv('REDIS_DB')
    FILE_NAME=os.getenv('FILE_NAME')
    
