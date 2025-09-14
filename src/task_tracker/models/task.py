from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Task:
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str


    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }


    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(
            id=int(data["id"]),
            description=str(data["description"]),
            status=str(data["status"]),
            createdAt=str(data["createdAt"]),
            updatedAt=str(data["updatedAt"]),
        )