"""Task API.

Endpoints:
    GET    /health
    GET    /tasks
    GET    /tasks/detailed
    GET    /tasks/{task_id}
    POST   /tasks
    DELETE /tasks/{task_id}
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from app import db, repository


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    db.init_db()
    yield


app = FastAPI(title="Task API", lifespan=lifespan)


class NewTask(BaseModel):
    title: str
    done: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return repository.list_tasks()


@app.get("/tasks/detailed")
def list_tasks_detailed():
    return repository.list_tasks_with_tags()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    # Returns null rather than a 404 today.
    return repository.get_task(task_id)


@app.post("/tasks", status_code=201)
def create_task(payload: NewTask):
    return repository.add_task(payload.title, payload.done)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    repository.delete_task(task_id)
    return {"deleted": task_id}
