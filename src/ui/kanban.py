# src/task_tracker/ui/kanban_app.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

import streamlit as st

from task_tracker.constants import (
    STATUS_TODO,
    STATUS_IN_PROGRESS,
    STATUS_DONE,
    ALL_STATUSES,
)
from task_tracker.services.task_service import TaskService
from task_tracker.storage.json_storage import JsonStorage
from task_tracker.exceptions import TaskNotFound, InvalidStatus


def get_service(file_path: Optional[Path]) -> TaskService:
    """Instancia o service usando um tasks.json escolhido na sidebar ou o cwd."""
    path = Path(file_path) if file_path else Path.cwd() / "tasks.json"
    storage = JsonStorage(file_path=path)
    return TaskService(storage)


def render_header():
    st.set_page_config(page_title="Task Tracker — Kanban", page_icon="✅", layout="wide")
    st.title("✅ Task Tracker — Kanban")
    st.markdown("""
        <style>
            /* deixa os botões mais discretos */
            .stButton>button {
                padding: 0.25rem 0.4rem;
                border-radius: 10px;
                min-width: 36px;
            }
            /* container do card */
            .task-card {
                padding: 10px;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                margin-bottom: 10px;
                background: #000;
            }
            .task-title {
                font-weight: 600;
            }
            .task-meta {
                font-size: 12px;
                color: #667085;
                margin-top: 4px;
            }
            .task-toolbar {
                display: flex;
                gap: .25rem;
                margin-top: .25rem;
            }
        </style>
        """, unsafe_allow_html=True)



def sidebar_controls() -> TaskService:
    st.sidebar.header("⚙️ Configurações")
    default_path = str(Path.cwd() / "tasks.json")
    file_path = st.sidebar.text_input("Caminho do tasks.json", value=default_path)

    with st.sidebar.expander("➕ Nova tarefa"):
        desc = st.text_input("Descrição", key="new_desc")
        if st.button("Adicionar", use_container_width=True):
            if desc.strip():
                service = get_service(file_path)
                service.add(desc.strip())
                st.success("Tarefa adicionada!")
                st.rerun()
            else:
                st.warning("Informe a descrição da tarefa.")

    st.sidebar.markdown("---")
    st.sidebar.caption("Dica: você pode apontar para diferentes arquivos `tasks.json`.")

    return get_service(file_path)


def task_card(t, service: TaskService, column_label: str):
    """Card compacto com barra de ações por ícones."""
    with st.container():
        # Cabeçalho do card
        st.markdown(
            f"""
            <div class="task-card">
              <div class="task-title">#{t.id} — {t.description}</div>
              <div class="task-meta">
                Criado em {t.createdAt[0:10]} às {t.createdAt[11:16]}<br/>
                Atualizado em {t.updatedAt[0:10]} às {t.updatedAt[11:16]}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Barra de ações (ícones apenas)
        c = st.columns([1,1,1,1,1])  # editar | excluir | mover-esq | mover-dir | concluir | (placeholder)
        # ✏️ Editar
        with c[0]:
            if st.button("✏️", key=f"edit_{column_label}_{t.id}", help="Editar descrição", use_container_width=True):
                st.session_state[f"edit_mode_{t.id}"] = True
                st.rerun()

        # 🗑️ Excluir
        with c[1]:
            if st.button("🗑️", key=f"del_{column_label}_{t.id}", help="Excluir tarefa", use_container_width=True):
                service.delete(t.id)
                st.rerun()

        # ⬅️ mover para a esquerda (quando aplicável)
        with c[2]:
            if t.status == STATUS_IN_PROGRESS:
                if st.button("⬅️", key=f"left_to_todo_{t.id}", help="Mover para To Do", use_container_width=True):
                    service.set_status(t.id, STATUS_TODO)
                    st.rerun()
            elif t.status == STATUS_DONE:
                if st.button("⬅️", key=f"left_to_inprog_{t.id}", help="Mover para In Progress", use_container_width=True):
                    service.set_status(t.id, STATUS_IN_PROGRESS)
                    st.rerun()
            else:
                st.write("")

        # ➡️ mover para a direita (quando aplicável)
        with c[3]:
            if t.status == STATUS_TODO:
                if st.button("➡️", key=f"right_to_inprog_{t.id}", help="Mover para In Progress", use_container_width=True):
                    service.set_status(t.id, STATUS_IN_PROGRESS)
                    st.rerun()
            elif t.status == STATUS_IN_PROGRESS:
                if st.button("➡️", key=f"right_to_done_{t.id}", help="Mover para Done", use_container_width=True):
                    service.set_status(t.id, STATUS_DONE)
                    st.rerun()
            else:
                st.write("")

        # ✅ concluir (aparece só se ainda não estiver done)
        with c[4]:
            if t.status != STATUS_DONE:
                if st.button("✅", key=f"quick_done_{t.id}", help="Marcar como Done", use_container_width=True):
                    service.set_status(t.id, STATUS_DONE)
                    st.rerun()
            else:
                st.write("")


        # Modo edição inline (abre abaixo do toolbar)
        if st.session_state.get(f"edit_mode_{t.id}"):
            st.info(f"Editando tarefa #{t.id}")
            new_desc = st.text_input("Nova descrição", value=t.description, key=f"desc_{t.id}")
            b1, b2 = st.columns(2)
            with b1:
                if st.button("💾 Salvar", key=f"save_{t.id}", use_container_width=True):
                    service.update(t.id, new_desc.strip() or t.description)
                    st.session_state[f"edit_mode_{t.id}"] = False
                    st.rerun()
            with b2:
                if st.button("✖️ Cancelar", key=f"cancel_{t.id}", use_container_width=True):
                    st.session_state[f"edit_mode_{t.id}"] = False
                    st.rerun()


def render_board(service: TaskService):
    # Filtros simples
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            q = st.text_input("🔎 Buscar por texto (descrição)", value="")
        with c2:
            sort_by = st.selectbox("Ordenar por", ["id", "createdAt", "updatedAt"])
        with c3:
            if st.button("🔄 Atualizar", use_container_width=True):
                st.rerun()

    # Carrega tasks
    all_tasks = service.list()
    # filtro por texto
    if q.strip():
        ql = q.strip().lower()
        all_tasks = [t for t in all_tasks if ql in t.description.lower()]

    # ordenação simples
    if sort_by == "id":
        all_tasks.sort(key=lambda t: t.id)
    else:
        all_tasks.sort(key=lambda t: getattr(t, sort_by))

    todo = [t for t in all_tasks if t.status == STATUS_TODO]
    inprog = [t for t in all_tasks if t.status == STATUS_IN_PROGRESS]
    done = [t for t in all_tasks if t.status == STATUS_DONE]

    st.header('📌 Quadro Kanban', divider=True, help="Visualize e gerencie suas tarefas em um quadro Kanban simples.")
    col_todo, col_inprog, col_done = st.columns(3, gap="large")

    with col_todo:
        st.subheader("🧩 To Do", divider=True)
        for t in todo:
            task_card(t, service, "todo")

    with col_inprog:
        st.subheader("🛠️ In Progress", divider=True)
        for t in inprog:
            task_card(t, service, "inprog")

    with col_done:
        st.subheader("✅ Done", divider=True)
        for t in done:
            task_card(t, service, "done")


def main():
    render_header()
    service = sidebar_controls()
    try:
        render_board(service)
    except (TaskNotFound, InvalidStatus) as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
