from dotenv import find_dotenv, load_dotenv
from starlette.config import Config
from os import environ


config = Config('.env')
load_dotenv(find_dotenv())


class ProjectConfig:

    MONGO_HOST = environ.get('MONGO_HOST')
    MONGO_PORT = environ.get('MONGO_PORT')
    MONGO_URL = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/'

    FASTAPI_HOST = environ.get('FASTAPI_HOST')
    