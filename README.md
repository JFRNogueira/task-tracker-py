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

## 📁 Estrutura de pastas

```bash
task-tracker/
├─ src/
│  └─ task_tracker/         # Pacote da aplicação
│     ├─ __init__.py
│     ├─ constants.py       # Constantes de domínio (status, defaults)
│     ├─ exceptions.py      # Exceções específicas (TaskNotFound, InvalidStatus, etc.)
│     ├─ models/
│     │  ├─ __init__.py
│     │  └─ task.py         # Entidade Task (dataclass) + (de)serialização dict
│     ├─ storage/
│     │  ├─ __init__.py
│     │  └─ json_storage.py # Persistência em JSON no CWD (tasks.json)
│     ├─ services/
│     │  ├─ __init__.py
│     │  └─ task_service.py # Regras de negócio: add/update/delete/list
│     ├─ cli/
│     │  ├─ __init__.py
│     │  └─ main.py         # Parser de argumentos (argparse) e comandos
│     ├─ utils/
│     │  ├─ __init__.py
│     │  └─ time.py         # Utilitário de tempo (UTC ISO-8601)
│     ├─ tests/             # Testes unitários
│     └─ ui/                # Interface gráfica (bonus)
│        └─ kanban.py       # Aplicação Streamlit com quadro Kanban
├─ docs/                    # Documentação do projeto
├─ tasks.json               # Armazena as tarefas (criado automaticamente)
├─ README.md                # Guia de uso
└─ pyproject.toml           # Configuração do projeto e entry point
```

## 📖 Uso

### Comandos disponíveis:

```bash
# Adicionar uma nova tarefa
task-cli add "Minha nova tarefa"

# Listar todas as tarefas
task-cli list

# Listar tarefas por status
task-cli list todo
task-cli list in-progress
task-cli list done

# Atualizar descrição de uma tarefa
task-cli update 1 "Nova descrição"

# Marcar tarefa como em progresso
task-cli mark-in-progress 1

# Marcar tarefa como concluída
task-cli mark-done 1

# Excluir uma tarefa
task-cli delete 1
```

### Exemplo de uso:

```bash
$ task-cli add "Estudar Python"
Task added successfully (ID: 1)

$ task-cli add "Fazer exercícios"
Task added successfully (ID: 2)

$ task-cli list
1	[todo]	Estudar Python	(created: 2024-01-15T10:30:00Z | updated: 2024-01-15T10:30:00Z)
2	[todo]	Fazer exercícios	(created: 2024-01-15T10:31:00Z | updated: 2024-01-15T10:31:00Z)

$ task-cli mark-in-progress 1
Task 1 marked as in-progress

$ task-cli mark-done 1
Task 1 marked as done

$ task-cli list done
1	[done]	Estudar Python	(created: 2024-01-15T10:30:00Z | updated: 2024-01-15T10:32:00Z)
```

## 🎨 Interface Gráfica (Bonus)

**Além da CLI tradicional**, este projeto inclui uma **interface gráfica Kanban** desenvolvida com Streamlit para facilitar a interação de usuários que preferem interfaces visuais.

### Como usar a interface Kanban:

```bash
# Instalar dependência adicional
pip install streamlit

# Executar a interface gráfica
streamlit run src/ui/kanban.py
```

A interface oferece:

- 📋 **Visualização em quadro Kanban** (To Do, In Progress, Done)
- ➕ **Adicionar tarefas** via sidebar
- ✏️ **Editar descrições** inline
- 🔄 **Mover tarefas** entre colunas com botões
- 🗑️ **Excluir tarefas** com confirmação
- 🔍 **Buscar e filtrar** tarefas
- 📁 **Escolher arquivo** tasks.json personalizado

## Going beyond (next steps)

> Features that may be added to improve the project

1. Add priority label (`low`, `medium` and `high`)
1. Add tag label (`#stidies`, `#work`, `#market`, `#marriage`, ...)
1. Add `dueDate` and highlight overdue tasks
1. Add a URL link, small description or append small files
