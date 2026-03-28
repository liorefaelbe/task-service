import logging
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DB_URL
from app.models.task import Base

logger = logging.getLogger(__name__)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    retries = 10
    delay = 2

    for i in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialized successfully")
            return
        except Exception as e:
            logger.warning(f"Database connection failed (attempt {i + 1}/{retries}): {e}")
            time.sleep(delay)

    raise Exception("Could not connect to DB")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()