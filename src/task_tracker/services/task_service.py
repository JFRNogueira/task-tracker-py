from __future__ import annotations
from typing import List, Optional, Dict, Any
from ..constants import ALL_STATUSES, DEFAULT_STATUS, STATUS_DONE, STATUS_IN_PROGRESS
from ..exceptions import TaskNotFound, InvalidStatus
from ..models.task import Task
from ..utils.time import now_iso

class TaskService:
    """Business logic for managing tasks."""

    def __init__(self, storage) -> None:
        # storage must expose list() -> List[dict] and save_all(List[dict]) -> None
        self.storage = storage

    # ---------- internals ----------
    def _load(self) -> List[Task]:
        return [Task.from_dict(d) for d in self.storage.list()]

    def _save(self, tasks: List[Task]) -> None:
        self.storage.save_all([t.to_dict() for t in tasks])

    def _next_id(self, tasks: List[Task]) -> int:
        return (max((t.id for t in tasks), default=0) + 1)

    def _find(self, tasks: List[Task], task_id: int) -> Task:
        for t in tasks:
            if t.id == task_id:
                return t
        raise TaskNotFound(f"Task {task_id} não encontrada")

    # ---------- public API ----------
    def add(self, description: str) -> Task:
        tasks = self._load()
        now = now_iso()
        new = Task(
            id=self._next_id(tasks),
            description=description,
            status=DEFAULT_STATUS,
            createdAt=now,
            updatedAt=now,
        )
        tasks.append(new)
        self._save(tasks)
        return new

    def update(self, task_id: int, description: str) -> Task:
        tasks = self._load()
        t = self._find(tasks, task_id)
        t.description = description
        t.updatedAt = now_iso()
        self._save(tasks)
        return t

    def delete(self, task_id: int) -> None:
        tasks = self._load()
        new_tasks = [t for t in tasks if t.id != task_id]
        if len(new_tasks) == len(tasks):
            raise TaskNotFound(f"Task {task_id} não encontrada")
        self._save(new_tasks)

    def set_status(self, task_id: int, status: str) -> Task:
        if status not in ALL_STATUSES:
            raise InvalidStatus(f"Status inválido: {status}")
        tasks = self._load()
        t = self._find(tasks, task_id)
        t.status = status
        t.updatedAt = now_iso()
        self._save(tasks)
        return t

    def mark_in_progress(self, task_id: int) -> Task:
        return self.set_status(task_id, STATUS_IN_PROGRESS)

    def mark_done(self, task_id: int) -> Task:
        return self.set_status(task_id, STATUS_DONE)

    def list(self, status: Optional[str] = None) -> List[Task]:
        tasks = self._load()
        if status is None:
            return tasks
        if status not in ALL_STATUSES:
            raise InvalidStatus(f"Status inválido: {status}")
        return [t for t in tasks if t.status == status]
