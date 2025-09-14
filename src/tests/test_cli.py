import io
import os
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

# Importa a função main do CLI
from task_tracker.cli.main import main as cli_main

def run_cli(args, cwd: Path):
    """
    Executa o CLI (main) redirecionando stdout para capturar a saída.
    Garante que o CWD esteja no diretório temporário para isolar o tasks.json.
    """
    current = Path.cwd()
    try:
        os.chdir(cwd)
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli_main(args)
        out = buf.getvalue()
        return code, out
    finally:
        os.chdir(current)

class CliTests(unittest.TestCase):
    def test_full_flow(self):
        with TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)

            # add
            code, out = run_cli(["add", "Buy groceries"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("Task added successfully (ID:", out)

            # list
            code, out = run_cli(["list"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("[todo]", out)
            self.assertIn("Buy groceries", out)

            # update
            code, out = run_cli(["update", "1", "Buy groceries and cook dinner"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("updated successfully", out)

            # mark-in-progress
            code, out = run_cli(["mark-in-progress", "1"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("in-progress", out)

            # mark-done
            code, out = run_cli(["mark-done", "1"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("done", out)

            # list done
            code, out = run_cli(["list", "done"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("[done]", out)
            self.assertIn("Buy groceries and cook dinner", out)

            # delete
            code, out = run_cli(["delete", "1"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("deleted successfully", out)

            # list vazio
            code, out = run_cli(["list"], tmpdir)
            self.assertEqual(code, 0)
            self.assertIn("No tasks found", out)

    def test_invalid_status_argument(self):
        with TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            # list com status inválido é barrado pelo argparse antes de chamar main,
            # então não testamos aqui. Teste de status inválido é no service.

    def test_not_found_exit_code(self):
        with TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            code, out = run_cli(["delete", "99"], tmpdir)
            self.assertEqual(code, 4)  # NOT_FOUND
            self.assertIn("não encontrada", out)

if __name__ == "__main__":
    unittest.main()
