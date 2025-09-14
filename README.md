# ✅ Task Tracker CLI (Python)

> A **simple yet powerful task manager** for your terminal.  
> Organize what you need to do, track what’s in progress, and celebrate your completed tasks!  
> Everything is stored in a **JSON file** in the current directory — no database, no external dependencies. 🚀

---

## ✨ Features

- ➕ **Add** new tasks
- ✏️ **Update** a task’s description
- ❌ **Delete** tasks
- ⏳ **Mark as in progress**
- ✅ **Mark as done**
- 📋 **List** all tasks or filter by status:
  - `todo`
  - `in-progress`
  - `done`

Each task includes:

- 🔑 **Unique ID**
- 📝 **Description**
- 📌 **Status**
- 📅 **Creation date**
- 🔄 **Last updated date**

---

## 🛠️ Installation

Requires **Python 3.10+**

```bash
# Clone this repository
git clone https://github.com/johannesnogueira/task-tracker-cli.git
cd task-tracker-cli

# Install in editable mode
pip install -e .

# Now you can use the CLI
task-cli --help

# Or run directly with Python
python -m task_tracker.cli.main --help
```

## 📁 Project Structure

```bash
task-tracker/
├─ src/
│  └─ task_tracker/         # Application package
│     ├─ __init__.py
│     ├─ constants.py       # Domain constants (statuses, defaults)
│     ├─ exceptions.py      # Specific exceptions (TaskNotFound, InvalidStatus, etc.)
│     ├─ models/
│     │  ├─ __init__.py
│     │  └─ task.py         # Task entity (dataclass) + dict (de)serialization
│     ├─ storage/
│     │  ├─ __init__.py
│     │  └─ json_storage.py # JSON persistence in the CWD (tasks.json)
│     ├─ services/
│     │  ├─ __init__.py
│     │  └─ task_service.py # Business logic: add/update/delete/list
│     ├─ cli/
│     │  ├─ __init__.py
│     │  └─ main.py         # Argument parser (argparse) and commands
│     ├─ utils/
│     │  ├─ __init__.py
│     │  └─ time.py         # Time utility (UTC ISO-8601)
│     ├─ tests/             # Unit tests
│     └─ ui/                # Graphical interface (bonus)
│        └─ kanban.py       # Streamlit application with Kanban board
├─ docs/                    # Project documentation
├─ tasks.json               # Stores tasks (created automatically)
├─ README.md                # Usage guide
└─ pyproject.toml           # Project configuration and entry point
```

## 📖 Usage

### Available commands:

```bash
# Add a new task
task-cli add "My new task"

# List all tasks
task-cli list

# List tasks by status
task-cli list todo
task-cli list in-progress
task-cli list done

# Update a task description
task-cli update 1 "New description"

# Mark a task as in progress
task-cli mark-in-progress 1

# Mark a task as done
task-cli mark-done 1

# Delete a task
task-cli delete 1
```

### Example:

```bash
$ task-cli add "Study Python"
Task added successfully (ID: 1)

$ task-cli add "Do exercises"
Task added successfully (ID: 2)

$ task-cli list
1   [todo]   Study Python   (created: 2024-01-15T10:30:00Z | updated: 2024-01-15T10:30:00Z)
2   [todo]   Do exercises   (created: 2024-01-15T10:31:00Z | updated: 2024-01-15T10:31:00Z)

$ task-cli mark-in-progress 1
Task 1 marked as in-progress

$ task-cli mark-done 1
Task 1 marked as done

$ task-cli list done
1   [done]   Study Python   (created: 2024-01-15T10:30:00Z | updated: 2024-01-15T10:32:00Z)
```

## 🎨 Graphical Interface (Bonus)

> In addition to the traditional CLI, this project includes a Kanban-style graphical interface built with Streamlit for users who prefer visual interaction.

How to use the Kanban interface:

```bash
# Install the additional dependency
pip install streamlit

# Run the graphical interface
streamlit run src/ui/kanban.py
```

The interface offers:

- 📋 Kanban board view (To Do, In Progress, Done)
- ➕ Add tasks via sidebar
- ✏️ Inline editing of descriptions
- 🔄 Move tasks between columns with buttons
- 🗑️ Delete tasks with confirmation
- 🔍 Search and filter tasks
- 📁 Choose a custom tasks.json file

## 🚀 Going Beyond (Next Steps)

Features that could be added to enhance the project

1. Add priority labels (low, medium, high)
1. Add tag labels (#studies, #work, #market, #marriage, ...)
1. Add dueDate and highlight overdue tasks
1. Add URL links, small descriptions, or attach small files
