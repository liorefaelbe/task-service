from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    info: Optional[str] = None
    execute_at: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    info: Optional[str] = None
    execute_at: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    info: Optional[str] = None
    created_at: datetime
    execute_at: Optional[datetime] = None

    class Config:
        from_attributes = True