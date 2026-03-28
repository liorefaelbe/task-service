from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.db import engine, get_db
from app.services import task_service

router = APIRouter()

# Root endpoint
@router.get("/")
def root():
    return {
        "service": "task-service",
        "status": "running"
    }

# Health check endpoints
@router.get("/health/live")
def liveness():
    return {"status": "ok"}

@router.get("/health/ready")
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "details": str(e)}

# Task endpoints
@router.get("/tasks", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return task_service.get_all_tasks(db)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)

@router.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task.title, task.info, task.execute_at)

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def modify_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.patch_task(db, task_id, task.title, task.info, task.execute_at)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def replace_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.replace_task(db, task_id, task.title, task.info, task.execute_at)

@router.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete_task(db, task_id)
    return {"message": "Task deleted"}

@router.delete("/tasks")
def remove_all_tasks(db: Session = Depends(get_db)):
    task_service.delete_all_tasks(db)
    return {"message": "All tasks deleted"}

@router.post("/tasks/reset")
def reset_tasks(db: Session = Depends(get_db)):
    task_service.reset_tasks_table(db)
    return {"message": "Tasks table reset"}