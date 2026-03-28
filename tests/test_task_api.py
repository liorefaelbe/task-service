import unittest
from datetime import UTC, datetime
from unittest import mock

from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import routes
from app.core.exceptions import NotFoundError
from app.models.task import Base
from app.schemas.task import TaskCreate, TaskUpdate

class TaskApiTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.SessionLocal = sessionmaker(bind=self.engine)

        Base.metadata.create_all(bind=self.engine)
        self.db = self.SessionLocal()

        self.engine_patcher = mock.patch.object(routes, "engine", self.engine)
        self.engine_patcher.start()

    def tearDown(self):
        self.engine_patcher.stop()
        self.db.close()
        self.engine.dispose()

    def test_root_and_health_routes(self):
        self.assertEqual(
            routes.root(),
            {"service": "task-service", "status": "running"},
        )
        self.assertEqual(routes.liveness(), {"status": "ok"})
        self.assertEqual(
            routes.readiness(),
            {"status": "ok", "database": "connected"},
        )

    def test_create_and_read_task(self):
        created = routes.add_task(
            TaskCreate(
                title="  Write project tests  ",
                info="  Cover the happy path  ",
            ),
            db=self.db,
        )

        self.assertEqual(created.title, "Write project tests")
        self.assertEqual(created.info, "Cover the happy path")
        self.assertEqual(
            int((created.execute_at - created.created_at).total_seconds()),
            60,
        )

        saved = routes.read_task(created.id, db=self.db)
        self.assertEqual(saved.id, created.id)
        self.assertEqual(saved.title, "Write project tests")

        tasks = routes.read_tasks(db=self.db)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, created.id)

    def test_patch_and_replace_task(self):
        created = routes.add_task(
            TaskCreate(
                title="Ship feature",
                info="Initial note",
                execute_at=datetime(2026, 3, 29, 10, 0, tzinfo=UTC),
            ),
            db=self.db,
        )

        patched = routes.modify_task(
            created.id,
            TaskUpdate(info="Updated note"),
            db=self.db,
        )
        self.assertEqual(patched.title, "Ship feature")
        self.assertEqual(patched.info, "Updated note")
        self.assertEqual(
            patched.execute_at.replace(tzinfo=None),
            datetime(2026, 3, 29, 10, 0),
        )

        replaced = routes.replace_task(
            created.id,
            TaskCreate(
                title="Ship final feature",
                info=None,
                execute_at=None,
            ),
            db=self.db,
        )
        self.assertEqual(replaced.title, "Ship final feature")
        self.assertIsNone(replaced.info)
        self.assertIsNone(replaced.execute_at)

    def test_delete_routes_remove_tasks(self):
        first = routes.add_task(TaskCreate(title="First task"), db=self.db)
        second = routes.add_task(TaskCreate(title="Second task"), db=self.db)

        response = routes.remove_task(first.id, db=self.db)
        self.assertEqual(response.status_code, 204)

        tasks_after_single_delete = routes.read_tasks(db=self.db)
        self.assertEqual([task.id for task in tasks_after_single_delete], [second.id])

        response = routes.remove_all_tasks(db=self.db)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(routes.read_tasks(db=self.db), [])

    def test_missing_task_raises_not_found(self):
        with self.assertRaises(NotFoundError):
            routes.read_task(999, db=self.db)

        with self.assertRaises(NotFoundError):
            routes.remove_task(999, db=self.db)

    def test_task_validation_rejects_blank_title(self):
        with self.assertRaises(ValidationError):
            TaskCreate(title="   ")

        with self.assertRaises(ValidationError):
            TaskUpdate(title="   ")


if __name__ == "__main__":
    unittest.main()
