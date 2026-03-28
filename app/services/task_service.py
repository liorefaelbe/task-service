from datetime import UTC, datetime, timedelta
from sqlalchemy.orm import Session
import logging

from app.repositories import task_repository
from app.core.exceptions import NotFoundError

logger = logging.getLogger(__name__)

def get_all_tasks(db: Session):
    logger.info("Fetching all tasks")
    return task_repository.get_all(db)

def get_task(db: Session, task_id: int):
    logger.info(f"Fetching task with ID: {task_id}")
    task = task_repository.get_by_id(db, task_id)
    if not task:
        raise NotFoundError("Task not found")
    return task

def create_task(db: Session, title: str, info: str = None, execute_at: datetime = None):
    info = info if info is not None else ""
    created_at = datetime.now(UTC)
    execute_at = execute_at if execute_at is not None else created_at + timedelta(minutes=1)

    logger.info(f"Creating task: {title}")
    return task_repository.create(db, title, info, created_at, execute_at)

def patch_task(db: Session, task_id: int, title: str = None, info: str = None, execute_at: datetime = None):
    task = task_repository.get_by_id(db, task_id)
    if not task:
        raise NotFoundError("Task not found")
    
    new_title = title if title is not None else task.title
    new_info = info if info is not None else task.info
    new_execute_at = execute_at if execute_at is not None else task.execute_at
    
    logger.info(f"Patching task with ID: {task_id}")
    return task_repository.update(db, task, new_title, new_info, new_execute_at)

def replace_task(db: Session, task_id: int, title: str, info: str, execute_at: datetime):
    task = task_repository.get_by_id(db, task_id)
    if not task:
        raise NotFoundError("Task not found")

    logger.info(f"Replacing task with ID: {task_id}")
    return task_repository.update(db, task, title, info, execute_at)

def delete_task(db: Session, task_id: int):
    task = task_repository.get_by_id(db, task_id)
    if not task:
        raise NotFoundError("Task not found")
    logger.info(f"Deleting task with ID: {task_id}")
    task_repository.delete(db, task)

def delete_all_tasks(db: Session):
    logger.info("Deleting all tasks")
    task_repository.delete_all(db)

def reset_tasks_table(db: Session):
    logger.info("Resetting tasks table")
    task_repository.reset_tasks_table(db)  