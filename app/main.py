"""A tiny todo API used as the demo target for ku coding agents."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="ku-agent-demo")


class TodoIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class Todo(TodoIn):
    id: int


_todos: dict[int, Todo] = {}
_next_id = 1


def reset() -> None:
    """Clear state (used by tests)."""
    global _next_id
    _todos.clear()
    _next_id = 1


STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", response_model=None)
def root(request: Request) -> FileResponse | dict[str, str]:
    """Landing page for browsers; JSON service info for everything else."""
    if "text/html" in request.headers.get("accept", ""):
        return FileResponse(STATIC_DIR / "index.html")
    return {"service": "ku-agent-demo"}


@app.get("/todos")
def list_todos() -> list[Todo]:
    return list(_todos.values())


@app.post("/todos", status_code=201)
def create_todo(todo: TodoIn) -> Todo:
    global _next_id
    item = Todo(id=_next_id, **todo.model_dump())
    _todos[item.id] = item
    _next_id += 1
    return item


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int) -> Todo:
    if todo_id not in _todos:
        raise HTTPException(status_code=404, detail="todo not found")
    return _todos[todo_id]


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    if todo_id not in _todos:
        raise HTTPException(status_code=404, detail="todo not found")
    del _todos[todo_id]
