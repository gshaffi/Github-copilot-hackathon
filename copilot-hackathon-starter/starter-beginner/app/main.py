"""Task API.

Endpoints:
    GET    /health
    GET    /tasks
    GET    /tasks/{task_id}
    POST   /tasks
    DELETE /tasks/{task_id}

There is very little error handling here on purpose.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from app import store

app = FastAPI(title="Task API")
store.seed()


class NewTask(BaseModel):
    title: str
    done: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return store.list_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    # No 404 handling yet. Ask Copilot about this one.
    return store.get_task(task_id)


@app.post("/tasks", status_code=201)
def create_task(payload: NewTask):
    return store.add_task(payload.title, payload.done)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    store.delete_task(task_id)
    return {"deleted": task_id}
