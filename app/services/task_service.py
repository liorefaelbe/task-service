from sqlalchemy.orm import Session
from app.repositories import task_repository

def get_all_tasks(db: Session):
    return task_repository.get_all(db)

def get_task(db: Session, task_id: int):
    return task_repository.get_by_id(db, task_id)

def create_task(db: Session, title: str):
    return task_repository.create(db, title)

def patch_task(db, task_id, title):
    task = task_repository.get_by_id(db, task_id)
    if not task:
        return None

    new_title = title if title is not None else task.title
    return task_repository.update(db, task_id, new_title)

def replace_task(db: Session, task_id: int, title: str):
    return task_repository.replace(db, task_id, title)

def delete_task(db: Session, task_id: int):
    return task_repository.delete(db, task_id)

def delete_all_tasks(db: Session):
    task_repository.delete_all(db)

def reset_tasks_table(db: Session):
    task_repository.reset_tasks_table(db)  