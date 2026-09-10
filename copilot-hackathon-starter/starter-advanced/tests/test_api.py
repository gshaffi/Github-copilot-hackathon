from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_tasks_are_seeded():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_and_delete_task():
    created = client.post("/tasks", json={"title": "Write the demo script"})
    assert created.status_code == 201
    task_id = created.json()["id"]

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 200
    assert deleted.json() == {"deleted": task_id}
