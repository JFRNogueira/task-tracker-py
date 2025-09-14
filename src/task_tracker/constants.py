from typing import Literal

STATUS_TODO: Literal["todo"] = "todo"
STATUS_IN_PROGRESS: Literal["in-progress"] = "in-progress"
STATUS_DONE: Literal["done"] = "done"

ALL_STATUSES = {STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE}
DEFAULT_STATUS = STATUS_TODO
