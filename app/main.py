from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.core.config import APP_NAME, APP_VERSION
from app.core.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    yield
    # shutdown 


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan
)

app.include_router(router)