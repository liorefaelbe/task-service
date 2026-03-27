from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DB_URL
from app.models.task import Base

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()