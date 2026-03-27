from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True