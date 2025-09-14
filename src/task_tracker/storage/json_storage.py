import json
from pathlib import Path
from typing import List, Dict, Any

DEFAULT_FILE_NAME = "tasks.json"

class JsonStorage:
    """JSON file persistence in current working directory."""

    def __init__(self, file_path: Path | None = None) -> None:
        self.file_path = file_path or Path.cwd() / DEFAULT_FILE_NAME
        if not self.file_path.exists():
            self._write_all([])

    def _read_all(self) -> List[Dict[str, Any]]:
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            # If removed meanwhile, recreate as empty list
            self._write_all([])
            return []
        except json.JSONDecodeError:
            # If file is corrupted, do not crash the CLI; start fresh
            return []

    def _write_all(self, tasks: List[Dict[str, Any]]) -> None:
        tmp = self.file_path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        tmp.replace(self.file_path)

    # Public API for service
    def list(self) -> List[Dict[str, Any]]:
        return self._read_all()

    def save_all(self, tasks: List[Dict[str, Any]]) -> None:
        self._write_all(tasks)
