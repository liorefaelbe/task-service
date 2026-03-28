from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    info: Optional[str] = None
    execute_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty or whitespace only")
        return value

    @field_validator("info")
    @classmethod
    def normalize_info(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()
        return value if value else None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    info: Optional[str] = None
    execute_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty or whitespace only")
        return value

    @field_validator("info")
    @classmethod
    def normalize_info(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()
        return value if value else None

class TaskResponse(BaseModel):
    id: int
    title: str
    info: Optional[str] = None
    created_at: datetime
    execute_at: Optional[datetime] = None

    class Config:
        from_attributes = True