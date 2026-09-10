# Copilot instructions

These apply to every request in this repository.

## Stack

- Python 3.11, FastAPI, Pydantic v2, SQLite via the standard `sqlite3` module.
- Tests use pytest and FastAPI's `TestClient`. Lint with ruff.
- No ORM. If you think one is needed, say why before adding it.

## How to write code here

- Type-hint every public function signature.
- Keep the web layer in `app/main.py` thin: validate, call, return.
- Data access belongs in `app/repository.py`. Nothing else opens a connection.
- Prefer a single parameterised query over a loop of queries.
- Never build SQL by string concatenation. Always use bound parameters.
- Raise `HTTPException` with a real status code rather than returning `None`.

## Tests

- Every behaviour change comes with a test in the same change.
- Tests must pass against a temporary database; use the `temp_database` fixture.
- Do not weaken or delete an existing assertion to make a change pass.

## Things not to do

- Do not add a secret, connection string or key to any tracked file.
- Do not add a dependency without adding it to `requirements.txt` with a pin.
- Do not reformat files you were not asked to change.
- Do not invent Azure resource names, regions or subscription IDs. Ask.

## Azure

- Everyone runs this in their own subscription, so never hardcode a
  subscription ID, resource group, region or SKU. Take them as parameters.
- Prefer managed identity over keys. If a key is unavoidable, read it from
  Key Vault at runtime.
