# GitHub Copilot Hackathon Starter

This project contains two versions of a small **Task API** used in a hands-on GitHub Copilot hackathon. Both tracks implement the same basic application, but they begin at different levels of complexity so participants can work on exercises appropriate to their experience.

The code is intentionally incomplete. Missing features and known weaknesses provide realistic tasks for participants to investigate and improve with GitHub Copilot.

## What the application does

The application is a Python REST API built with FastAPI. It supports:

- Checking service health
- Listing tasks
- Retrieving a task by ID
- Creating tasks
- Deleting tasks

FastAPI also generates interactive API documentation at `/docs` while the application is running.

## The two tracks

| Track | Intended audience | Starting point | Main learning goals |
|---|---|---|---|
| [Beginner](copilot-hackathon-starter/starter-beginner/) | Participants new to GitHub Copilot or agent-assisted development | Small FastAPI app with an in-memory task store and basic tests | Understand a repository, add error handling, write tests, refactor code, and create a Dockerfile |
| [Intermediate and advanced](copilot-hackathon-starter/starter-advanced/) | Participants comfortable with Python, APIs, testing, and CI | FastAPI app with SQLite, repository functions, a larger test suite, CI, and reusable Copilot prompts | Improve repository instructions, extend the API, refactor architecture, optimize SQL, review changes, and generate Azure deployment assets |

### Beginner track

The beginner track keeps the codebase deliberately small:

- `app/main.py` defines the FastAPI routes.
- `app/store.py` stores tasks in memory.
- `tests/test_health.py` provides a working test baseline.
- `requirements.txt` pins the Python dependencies.

Tasks disappear when the process restarts, and the API has very little error handling. There is no Dockerfile, CI workflow, or deployment configuration. These omissions are intentional workshop exercises rather than accidental production gaps.

See the [beginner track README](copilot-hackathon-starter/starter-beginner/README.md) for setup instructions.

### Intermediate and advanced track

The advanced track adds realistic application structure and development automation:

- `app/main.py` contains the API layer.
- `app/db.py` creates and seeds the SQLite database.
- `app/repository.py` contains SQL data-access functions.
- `tests/` covers the API and repository behavior using temporary databases.
- `.github/workflows/ci.yml` runs linting and tests on Windows and Ubuntu.
- `.github/copilot-instructions.md` defines repository-wide guidance for Copilot.
- `.github/prompts/` contains reusable prompts for common workshop activities.

This track also contains deliberate weaknesses, including an N+1 query, direct coupling between the API and repository module, and incomplete HTTP error handling. Participants are expected to identify and improve them during the hackathon.

See the [advanced track README](copilot-hackathon-starter/starter-advanced/README.md) for setup instructions.

## Repository layout

```text
├── README.md
└── copilot-hackathon-starter/
    ├── FACILITATOR.md
    ├── starter-beginner/
    │   ├── app/
    │   ├── tests/
    │   ├── README.md
    │   └── requirements.txt
    └── starter-advanced/
        ├── .github/
        ├── app/
        ├── tests/
        ├── README.md
        ├── requirements.txt
        └── ruff.toml
```

## How the repository is intended to be used

This workspace is the authoring source for the workshop. Before distribution, each starter folder should be published as a separate repository:

1. Publish `starter-beginner/` for the beginner room.
2. Publish `starter-advanced/` for the intermediate and advanced room.
3. Give participants only the repository URL for their selected track.
4. Keep the facilitator guide with the workshop organizers.

Separating the tracks gives each participant a focused starting point and prevents advanced configuration from distracting beginner participants.

## Facilitators

Workshop setup, publishing guidance, exercise mappings, and subscription preparation are documented in the [facilitator guide](copilot-hackathon-starter/FACILITATOR.md).
