"""In-memory task store.

Kept deliberately simple. There is no persistence and no locking - if you
need either, that is a good thing to ask Copilot for.
"""

_tasks = {}
_next_id = 1


def list_tasks():
    return list(_tasks.values())


def get_task(task_id):
    return _tasks.get(task_id)


def add_task(title, done=False):
    global _next_id
    task = {"id": _next_id, "title": title, "done": done}
    _tasks[_next_id] = task
    _next_id += 1
    return task


def delete_task(task_id):
    return _tasks.pop(task_id, None)


def seed():
    if not _tasks:
        add_task("Clone the starter repo")
        add_task("Check Copilot is signed in")
        add_task("Run the app locally")
