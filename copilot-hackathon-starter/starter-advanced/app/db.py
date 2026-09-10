"""SQLite connection and schema bootstrap."""

import os
import sqlite3

DATABASE_PATH = os.environ.get("DATABASE_PATH", "tasks.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    title  TEXT NOT NULL,
    done   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tags (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id  INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    label    TEXT NOT NULL
);
"""

SEED_TASKS = [
    ("Clone the starter repo", 1, ["setup"]),
    ("Confirm agent mode is available", 1, ["setup", "copilot"]),
    ("Get a green local baseline", 0, ["setup", "tests"]),
    ("Check subscription, region and quota", 0, ["azure"]),
]


def connect(path: str | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(path or DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: str | None = None) -> None:
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
        existing = conn.execute("SELECT COUNT(*) AS n FROM tasks").fetchone()["n"]
        if existing == 0:
            for title, done, labels in SEED_TASKS:
                cursor = conn.execute(
                    "INSERT INTO tasks (title, done) VALUES (?, ?)", (title, done)
                )
                for label in labels:
                    conn.execute(
                        "INSERT INTO tags (task_id, label) VALUES (?, ?)",
                        (cursor.lastrowid, label),
                    )
        conn.commit()
    finally:
        conn.close()
