from dotenv import find_dotenv, load_dotenv
from starlette.config import Config
from os import environ


config = Config('.env')
load_dotenv(find_dotenv())


class ProjectConfig:

    MONGO_HOST = environ.get('MONGO_HOST')
    MONGO_PORT = environ.get('MONGO_PORT')
    MONGO_URL = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/files_info'

    FASTAPI_HOST = environ.get('FASTAPI_HOST')

    MINIO_HOST = environ.get('MINIO_HOST')
    MINIO_PORT = environ.get('MINIO_PORT')
    MINIO_ROOT_USER = environ.get('MINIO_ROOT_USER')
    MINIO_ROOT_PASSWORD = environ.get('MINIO_ROOT_PASSWORD')
    MINIO_URL = f'{MINIO_HOST}:{MINIO_PORT}'
    