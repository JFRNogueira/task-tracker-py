import argparse
import sys
from pathlib import Path
from ..constants import STATUS_DONE, STATUS_IN_PROGRESS, STATUS_TODO
from ..exceptions import TaskNotFound, InvalidStatus
from ..services.task_service import TaskService
from ..storage.json_storage import JsonStorage

# Exit codes
SUCCESS = 0
INVALID = 2
NOT_FOUND = 4

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-cli",
        description="Task Tracker CLI (Python)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Adicionar nova task")
    p_add.add_argument("description", type=str, help="Descrição da task")

    # update
    p_upd = sub.add_parser("update", help="Atualizar descrição da task")
    p_upd.add_argument("id", type=int)
    p_upd.add_argument("description", type=str)

    # delete
    p_del = sub.add_parser("delete", help="Excluir task")
    p_del.add_argument("id", type=int)

    # mark-in-progress
    p_mip = sub.add_parser("mark-in-progress", help="Marcar como em progresso")
    p_mip.add_argument("id", type=int)

    # mark-done
    p_md = sub.add_parser("mark-done", help="Marcar como concluída")
    p_md.add_argument("id", type=int)

    # list
    p_list = sub.add_parser("list", help="Listar tasks")
    p_list.add_argument(
        "status",
        nargs="?",
        choices=[STATUS_TODO, STATUS_IN_PROGRESS, STATUS_DONE],
        help="Filtro por status (opcional)",
    )

    return parser

def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    storage = JsonStorage(file_path=Path.cwd() / "tasks.json")
    service = TaskService(storage)

    try:
        if args.command == "add":
            task = service.add(args.description)
            print(f"Task added successfully (ID: {task.id})")
            return SUCCESS

        if args.command == "update":
            task = service.update(args.id, args.description)
            print(f"Task {task.id} updated successfully")
            return SUCCESS

        if args.command == "delete":
            service.delete(args.id)
            print(f"Task {args.id} deleted successfully")
            return SUCCESS

        if args.command == "mark-in-progress":
            task = service.mark_in_progress(args.id)
            print(f"Task {task.id} marked as in-progress")
            return SUCCESS

        if args.command == "mark-done":
            task = service.mark_done(args.id)
            print(f"Task {task.id} marked as done")
            return SUCCESS

        if args.command == "list":
            tasks = service.list(status=args.status)
            if not tasks:
                print("No tasks found")
                return SUCCESS
            for t in tasks:
                print(
                    f"{t.id}\t[{t.status}]\t{t.description}\t"
                    f"(created: {t.createdAt} | updated: {t.updatedAt})"
                )
            return SUCCESS

    except TaskNotFound as e:
        print(str(e))
        return NOT_FOUND
    except InvalidStatus as e:
        print(str(e))
        return INVALID
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
