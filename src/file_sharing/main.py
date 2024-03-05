import uvicorn

from fastapi import FastAPI
from config import ProjectConfig
from router import router as files
from mongo_database import client_mongo
from minio_storage import client_minio


app = FastAPI()
app.state.mongo_client = client_mongo
app.state.minio_client = client_minio

app.include_router(files)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, ws_ping_interval=300, ws_ping_timeout=300, host=ProjectConfig.FASTAPI_HOST)
