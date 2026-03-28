from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import logging
import time

from app.api.routes import router
from app.core.config import APP_NAME, APP_VERSION
from app.core.db import init_db
from app.core.exceptions import (NotFoundError, not_found_exception_handler, generic_exception_handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# init Database and create tables before the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    init_db()
    yield
    # shutdown 

# FastAPI application instance
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan
)

# Register exception handlers   
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler) 

# Middleware for logging requests and responses
logger = logging.getLogger("app.middleware")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    # request info
    method = request.method
    path = request.url.path

    response = await call_next(request)

    # response info
    status_code = response.status_code
    duration = (time.perf_counter() - start_time) * 1000

    client_ip = request.client.host
    logger.info(f"client: {client_ip} - {method} {path} -> {status_code} ({duration:.2f}ms)")
    
    return response

# Include API routes
app.include_router(router)