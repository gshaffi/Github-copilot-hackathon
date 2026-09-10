---
mode: agent
description: Add a new API endpoint with a test, following this repo's conventions.
---

Add a new endpoint to `app/main.py`.

Ask me for the route, method and behaviour if I have not already given them.

Then:

1. Add the route to `app/main.py`, keeping the handler thin.
2. Put any data access in `app/repository.py` as a single parameterised query.
3. Return a real status code. Use `HTTPException(404)` for a missing record.
4. Add a test in `tests/test_api.py` covering the happy path and one failure.
5. Run `pytest -q` and show me the result before you finish.

Do not change unrelated files.
