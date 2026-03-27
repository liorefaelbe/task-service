import os

APP_NAME = os.getenv("APP_NAME", "Task Service")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

DB_URL = os.getenv(
    "DB_URL",
    "postgresql://user:password@localhost:5432/tasks_db"
)