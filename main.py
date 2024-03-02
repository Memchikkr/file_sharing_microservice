from fastapi import FastAPI
from router import router as files


app = FastAPI()
app.include_router(files)