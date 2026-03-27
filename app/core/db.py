from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DB_URL
from app.models.task import Base

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DB_URL
from app.models.task import Base

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    retries = 10
    delay = 2

    for i in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("DB connected successfully")
            return
        except Exception as e:
            print(f"DB not ready, retry {i+1}/{retries}...")
            time.sleep(delay)

    raise Exception("Could not connect to DB")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()