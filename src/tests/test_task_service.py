import unittest
import time
from datetime import datetime
from task_tracker.services.task_service import TaskService
from task_tracker.constants import STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE
from task_tracker.exceptions import TaskNotFound, InvalidStatus

class MemoryStorage:
    """Storage em memória para testes do serviço (não toca filesystem)."""
    def __init__(self):
        self._data = []
    def list(self):
        return self._data
    def save_all(self, tasks):
        self._data = tasks

class TaskServiceTests(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryStorage()
        self.service = TaskService(self.storage)

    def test_add_creates_task_with_defaults(self):
        t = self.service.add("Comprar pão")
        self.assertEqual(t.id, 1)
        self.assertEqual(t.description, "Comprar pão")
        self.assertEqual(t.status, STATUS_TODO)
        # ISO-8601 check (starts with year and has 'T')
        self.assertIn("T", t.createdAt)
        self.assertIn("T", t.updatedAt)

    def test_update_changes_description_and_timestamp(self):
        t1 = self.service.add("A")
        before = t1.updatedAt
        # Adiciona um pequeno delay para garantir que o timestamp seja diferente
        time.sleep(0.001)  # 1 milissegundo
        t2 = self.service.update(t1.id, "B")
        self.assertEqual(t2.description, "B")
        self.assertNotEqual(before, t2.updatedAt)

    def test_delete_removes_task(self):
        t1 = self.service.add("A")
        self.service.delete(t1.id)
        self.assertEqual(len(self.service.list()), 0)
        with self.assertRaises(TaskNotFound):
            self.service.delete(t1.id)

    def test_set_status_and_filters(self):
        a = self.service.add("A")
        b = self.service.add("B")
        c = self.service.add("C")

        self.service.mark_in_progress(b.id)
        self.service.mark_done(c.id)

        todos = self.service.list(STATUS_TODO)
        inprog = self.service.list(STATUS_IN_PROGRESS)
        done = self.service.list(STATUS_DONE)

        self.assertEqual({t.id for t in todos}, {a.id})
        self.assertEqual({t.id for t in inprog}, {b.id})
        self.assertEqual({t.id for t in done}, {c.id})

    def test_invalid_status_raises(self):
        a = self.service.add("A")
        with self.assertRaises(InvalidStatus):
            self.service.set_status(a.id, "invalid")

    def test_task_not_found_raises(self):
        with self.assertRaises(TaskNotFound):
            self.service.update(999, "X")

if __name__ == "__main__":
    unittest.main()
