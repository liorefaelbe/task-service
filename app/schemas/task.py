from pydantic import BaseModel

# Task schema for creating a new task
class TaskCreate(BaseModel):
    title: str