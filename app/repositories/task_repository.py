from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.task import Task

def get_all(db: Session):
    return db.query(Task).order_by(Task.id.asc()).all()

def get_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create(db: Session, title: str, info: str, created_at: int, execute_at: int):
    task = Task(title = title, 
                info = info, 
                created_at = created_at, 
                execute_at = execute_at)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update(db: Session, task: Task, title: str, info: str, execute_at: int):
    task.title = title
    task.info = info
    task.execute_at = execute_at
    
    db.commit()
    db.refresh(task)
    return task 

def delete(db: Session, task: Task):
    db.delete(task)
    db.commit()

def delete_all(db: Session):
    db.query(Task).delete()
    db.commit()

def reset_tasks_table(db: Session):
    db.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY"))
    db.commit()