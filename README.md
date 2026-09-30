# ku-agent-demo

A deliberately tiny FastAPI todo service. It exists so that [ku](https://github.com/meghancampbel9/k-u)
coding agents have something real to change and test.

```bash
uv sync
uv run pytest -q
uv run uvicorn app.main:app --reload
```

Endpoints: `GET /`, `GET /todos`, `POST /todos`, `GET /todos/{id}`, `DELETE /todos/{id}`.
