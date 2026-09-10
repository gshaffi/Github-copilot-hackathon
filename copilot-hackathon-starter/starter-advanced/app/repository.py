"""Data access for tasks.

Note: the API imports these functions directly, so there is no seam between
the web layer and the database. That is one of the things worth changing.
"""

from app import db


def list_tasks():
    conn = db.connect()
    rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def list_tasks_with_tags():
    """Return every task with its tags.

    This runs one query for the tasks and then one more query per task to
    fetch that task's tags. It works, and it gets slower with every row.
    """
    conn = db.connect()
    tasks = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()

    result = []
    for task in tasks:
        tags = conn.execute(
            "SELECT label FROM tags WHERE task_id = ?", (task["id"],)
        ).fetchall()
        item = dict(task)
        item["tags"] = [tag["label"] for tag in tags]
        result.append(item)

    conn.close()
    return result


def get_task(task_id):
    conn = db.connect()
    row = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def add_task(title, done=False):
    conn = db.connect()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", (title, int(done))
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {"id": task_id, "title": title, "done": int(done)}


def delete_task(task_id):
    conn = db.connect()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
