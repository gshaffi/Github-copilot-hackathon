# Hackathon starter repos — facilitator guide

Two repositories, one per room. Same app, different starting line.

| Folder | Room | Ships with | Deliberately missing |
|---|---|---|---|
| `starter-beginner/` | Beginner | FastAPI app, in-memory store, one test file, README | Dockerfile, error handling, deploy config |
| `starter-advanced/` | Intermediate & advanced | SQLite data layer, full test suite, `copilot-instructions.md`, three prompt files, CI workflow, ruff config | Dockerfile, Bicep, azd template, deploy workflow, telemetry |

## Publishing them

Publish each folder as its own repository, then put both URLs in the
hackathon invite so people can clone before they sit down.

```bash
cd starter-beginner
git init && git add -A && git commit -m "Hackathon starter (beginner)"
gh repo create <org>/copilot-hackathon-starter --public --source=. --push

cd ../starter-advanced
git init && git add -A && git commit -m "Hackathon starter (advanced)"
gh repo create <org>/copilot-hackathon-starter-advanced --public --source=. --push
```

Update slide 3 of each deck with the matching URL.

## Why the repos are imperfect on purpose

Every exercise in the decks maps to something that is genuinely wrong or
genuinely absent. Copilot has real work to do, and people see a real diff.

### Beginner room

| Exercise | What it lands on |
|---|---|
| Explain this repo | Four small files, so the explanation is checkable |
| `#main.py` add error handling | `GET /tasks/{id}` returns `null` for a missing task |
| `/tests` write unit tests | `app/store.py` has no tests at all |
| Refactor into smaller functions | `app/main.py` mixes validation and storage |
| Add a Dockerfile | There isn't one |

### Intermediate & advanced room

| Exercise | What it lands on |
|---|---|
| Improve `copilot-instructions.md` | A real one ships, so this is editing not inventing |
| Add an endpoint + test + CI | `.github/prompts/add-endpoint.prompt.md` runs it |
| Refactor the data layer behind an interface | `app/main.py` imports `repository` directly — no seam |
| Find and fix the N+1 query | `repository.list_tasks_with_tags` queries once per task |
| Review your own diff | `.github/prompts/review-my-diff.prompt.md` |
| Generate Bicep and an azd template | `.github/prompts/generate-azure-infra.prompt.md` |

## Bring-your-own-subscription notes

Both READMEs end with an `az login` / `az account show` check, and the
advanced one adds a quota check. Run this at minute three, not at deploy
time. The infra prompt is written to refuse hardcoded subscription IDs,
regions and SKUs, so generated Bicep stays portable across the room.

Have a pairing fallback ready: anyone whose subscription blocks resource
creation works alongside someone whose does not, and still gets the full
Copilot half of the session.

## Running it yourself first

macOS/Linux:

```bash
cd starter-advanced
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q          # should be green
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
cd starter-advanced
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q          # should be green
uvicorn app.main:app --reload
```

Do this once before the session so you can demo from a known-good state.
