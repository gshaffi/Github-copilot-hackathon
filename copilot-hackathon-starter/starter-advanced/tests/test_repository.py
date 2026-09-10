from app import repository


def test_list_tasks_returns_seeded_rows():
    tasks = repository.list_tasks()
    assert len(tasks) >= 1
    assert "title" in tasks[0]


def test_detailed_listing_includes_tags():
    tasks = repository.list_tasks_with_tags()
    assert any(task["tags"] for task in tasks)
