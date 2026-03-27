from sqlalchemy.orm import Session
from app.repositories import task_repository

def get_all_tasks(db: Session):
    return task_repository.get_all(db)

def get_task(db: Session, task_id: int):
    return task_repository.get_by_id(db, task_id)

def create_task(db: Session, title: str):
    return task_repository.create(db, title)

def update_task(db: Session, task_id: int, title: str):
    return task_repository.update(db, task_id, title)

def delete_task(db: Session, task_id: int):
    return task_repository.delete(db, task_id)

def reset_tasks_table(db: Session):
    return task_repository.reset_tasks_table(db)  