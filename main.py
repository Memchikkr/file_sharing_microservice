import uvicorn

from fastapi import FastAPI
from config import ProjectConfig
from router import router as files


app = FastAPI()
app.include_router(files)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, ws_ping_interval=300, ws_ping_timeout=300, host=ProjectConfig.FASTAPI_HOST)