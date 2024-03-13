import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import ProjectConfig
from src.mongo_database import init_db
from src.file_sharing.routers.router import router as files

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(files)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, ws_ping_interval=300, ws_ping_timeout=300, host=ProjectConfig.FASTAPI_HOST)
