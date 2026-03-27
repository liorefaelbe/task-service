from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.task import Task

def get_all(db: Session):
    return db.query(Task).all()

def get_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create(db: Session, title: str):
    task = Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update(db: Session, task_id: int, title: str):
    task = get_by_id(db, task_id)
    if task:
        task.title = title
        db.commit()
        db.refresh(task)
        return task
    return None 

def delete(db: Session, task_id: int):
    task = get_by_id(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

def delete_all(db: Session):
    if db.query(Task).count() > 0:
        db.query(Task).delete()
        db.commit() 
        return True
    return False

def reset_tasks_table(db: Session):
    db.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY"))
    db.commit()