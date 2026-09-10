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
