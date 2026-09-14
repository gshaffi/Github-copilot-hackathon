# Hackathon Starter — Beginner Room

A tiny Task API you can run in one command. It is deliberately small and
deliberately imperfect: the exercises in the session ask GitHub Copilot to
improve it.

## Run it

Use Python 3.11 for the workshop.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

### macOS or Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Then open http://localhost:8000/docs

## Check it works

```bash
curl http://localhost:8000/health
```

If pytest passes but reports that `.pytest_cache` cannot be created, the
workspace may be in OneDrive or another synchronized folder. The warning does
not invalidate the result, but a local, non-synchronized development folder
avoids it.

Follow [`workshop.md`](workshop.md) for the complete participant session.

## What is here

| Path | What it is |
|---|---|
| `app/main.py` | The API. Health check plus task endpoints. |
| `app/store.py` | Where tasks are kept. Simple on purpose. |
| `tests/test_health.py` | One test, so you know the setup works. |
| `.env.example` | Copy to `.env` if you add settings. |
| `workshop.md` | Step-by-step participant guide for the session. |

## What is deliberately missing

No Dockerfile, no deployment config, no error handling to speak of. You will
add those with Copilot during the session.

## Before the second half

```bash
az login
az account show --output table
```

Confirm which subscription you are in. Everyone is bringing their own, so
check this early rather than at deploy time.
