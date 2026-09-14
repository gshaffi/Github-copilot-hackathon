# Hackathon Starter — Intermediate & Advanced Room

A small Task API with a SQLite data layer, a test suite and CI already wired
up. It runs, it is green, and it has a few deliberate weaknesses for you to
find with GitHub Copilot's agent.

## Run it

Use Python 3.11, which matches the version used by CI.

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ruff check .
pytest -q
uvicorn app.main:app --reload
```

macOS or Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ruff check .
pytest -q
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs — you should have a green test run and a
running app before the first exercise.

If pytest passes but reports that `.pytest_cache` cannot be created, the
workspace may be in OneDrive or another synchronized folder with restrictive
file handling. The warning does not invalidate the test result, but cloning to
a local, non-synchronized development folder avoids it. Deprecation warnings
on newer Python releases should first be checked by recreating the environment
with Python 3.11.

## What is already configured

| Path | What it is |
|---|---|
| `.github/copilot-instructions.md` | Repo-wide standards Copilot reads on every request |
| `.github/prompts/*.prompt.md` | Reusable prompts the whole room can run identically |
| `.github/workflows/ci.yml` | Lint and test on every push |
| `app/repository.py` | The data layer. Look closely at `list_tasks_with_tags`. |
| `tests/` | Health, task and repository tests |

## What is deliberately missing

No Dockerfile, no infrastructure as code, no deploy workflow, no telemetry.
Those are the second-half exercises.

## Known weaknesses (on purpose)

1. `repository.list_tasks_with_tags` issues one query per task — a classic N+1.
2. The API talks to `repository` directly, so there is no seam to test against
   or swap out.
3. Errors surface as unhandled exceptions rather than useful status codes.

## Before the second half

```bash
az login
az account show --output table
az vm list-usage --location uksouth --output table    # sanity-check your quota
```

Everyone is bringing their own subscription. Confirm your subscription,
region and quota now rather than at deploy time.
