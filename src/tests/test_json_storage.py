import io
import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from task_tracker.storage.json_storage import JsonStorage

class JsonStorageTests(unittest.TestCase):
    def test_creates_file_and_persists(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            storage = JsonStorage(file_path=path)

            # criado automaticamente como lista vazia
            self.assertTrue(path.exists())
            self.assertEqual(storage.list(), [])

            # salva e lê de volta
            payload = [{"id": 1, "description": "A", "status": "todo",
                        "createdAt": "x", "updatedAt": "x"}]
            storage.save_all(payload)
            self.assertEqual(storage.list(), payload)

    def test_handles_missing_and_corrupted_json(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            storage = JsonStorage(file_path=path)

            # corrompe o arquivo manualmente
            path.write_text("{ invalid json", encoding="utf-8")
            # deve retornar lista vazia (tolerante a erro)
            self.assertEqual(storage.list(), [])

            # se o arquivo for removido, deve recriar como []
            path.unlink()
            self.assertFalse(path.exists())
            self.assertEqual(storage.list(), [])  # força recriação interna?
            # JsonStorage por padrão cria no __init__, mas se removermos depois,
            # a leitura deve tolerar e retornar [] sem quebrar.

if __name__ == "__main__":
    unittest.main()
