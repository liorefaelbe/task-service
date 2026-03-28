from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    info = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(UTC))
    execute_at = Column(DateTime, nullable=True)