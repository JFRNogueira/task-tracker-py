class TaskError(Exception):
    """Base exception for task domain errors."""


class TaskNotFound(TaskError):
    """Raised when a task is not found by id."""


class InvalidStatus(TaskError):
    """Raised when an invalid task status is provided."""
