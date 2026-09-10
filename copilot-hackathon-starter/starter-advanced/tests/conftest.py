import os
import tempfile

import pytest

from app import db


@pytest.fixture(autouse=True)
def temp_database(monkeypatch):
    handle, path = tempfile.mkstemp(suffix=".db")
    os.close(handle)
    monkeypatch.setattr(db, "DATABASE_PATH", path)
    db.init_db(path)
    yield path
    os.remove(path)
