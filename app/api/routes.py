from fastapi import APIRouter

from app.services.task_service import get_all_tasks, get_task, create_task, delete_task 
from app.schemas.task import TaskCreate

router = APIRouter()

# Basic endpoints
@router.get("/")
def root():
    return {"message": "Welcome to the Task Service"}

@router.get("/health")
def health():
    return {"status": "ok"}

# Task endpoints
@router.get("/tasks")
def read_tasks():
    return get_all_tasks()

@router.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = get_task(task_id)
    if task:
        return task
    return {"error": "Task not found"}

@router.post("/tasks")
def add_task(task: TaskCreate):  
    return create_task(task.title)

@router.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    status = delete_task(task_id)
    if status:
        return {"message": "Task deleted"}
    return {"error": "Task not found"}