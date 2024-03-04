import uvicorn

from fastapi import FastAPI
from src.file_sharing.config import ProjectConfig
from src.file_sharing.router import router as files
from mongo_database import client


app = FastAPI()
app.state.mongo_client = client
app.include_router(files)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, ws_ping_interval=300, ws_ping_timeout=300, host=ProjectConfig.FASTAPI_HOST)
