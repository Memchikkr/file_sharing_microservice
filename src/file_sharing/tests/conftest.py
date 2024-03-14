import pytest
import asyncio

from httpx import AsyncClient
from beanie import init_beanie
from src.main import app
from mongomock_motor import AsyncMongoMockClient
from minio import Minio
from pytest_minio_mock.plugin import MockMinioClient

from src.config import ProjectConfig
from src.file_sharing.tests.fixtures.fixture_to_upload import fixture_give_upload_file

# MONGO
mongo_client = AsyncMongoMockClient()
mongo_db = mongo_client.test



@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
async def init_and_clear_mongo():
    await init_beanie(database=mongo_db, document_models=
        [
            'src.file_sharing.models.file.FileDoc',
            'src.file_sharing.models.security.SecurityDoc',
        ]
    )

    yield

    list_collections = await mongo_db.list_collection_names()
    for collection in list_collections:
        await mongo_db.drop_collection(collection)


@pytest.fixture(scope='function', autouse=True)
async def init_and_clear_minio(minio_mock, mocker):
    client_minio = Minio(
        ProjectConfig.MINIO_URL,
        access_key=ProjectConfig.MINIO_ROOT_USER,
        secret_key=ProjectConfig.MINIO_ROOT_PASSWORD,
        secure=False
    )
    mocker.patch('src.file_sharing.services.minio_service.client_minio', client_minio)
    yield


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
