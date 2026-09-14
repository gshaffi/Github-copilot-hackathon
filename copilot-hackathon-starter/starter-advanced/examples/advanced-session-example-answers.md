# Advanced Session Example Answers

These examples help facilitators evaluate participant work. They describe the
expected reasoning and observable outcomes, not one mandatory implementation.
Generated code and infrastructure still need review against the repository and
the participant's Azure context.

## 1. Local baseline

A successful baseline should show:

- Python 3.11 in the activated `.venv`;
- `ruff check .` completing without violations;
- five tests passing before an exercise changes the application;
- Uvicorn starting from `starter-advanced`;
- `GET /health` returning `{"status": "ok"}`;
- Swagger UI loading at `http://localhost:8000/docs`.

A pytest cache warning caused by a synchronized folder is not a test failure.
Move the clone to a local, non-synchronized development folder if participants
need clean cache behavior.

## 2. Repository explanation

A strong explanation should trace this request flow:

1. FastAPI creates the application and routes in `app/main.py`.
2. The lifespan function calls `db.init_db()` during startup.
3. Route handlers call functions in `app/repository.py` directly.
4. Repository functions open SQLite connections through `app/db.py`.
5. Tests replace `db.DATABASE_PATH` with a temporary database through the
   autouse fixture in `tests/conftest.py`.
6. CI installs dependencies, runs Ruff, and runs pytest on Windows and Ubuntu.

It should also identify the intentional weaknesses:

- a missing task is returned as `null` instead of HTTP 404;
- the API is directly coupled to module-level repository functions;
- `list_tasks_with_tags` executes one tag query for every task;
- several repository functions do not guarantee connection cleanup when an
  operation raises.

## 3. Repository instruction audit

The useful instruction set is concise and stable. It should establish that:

- HTTP validation and response handling belong in `app/main.py`;
- SQL and connection management belong in `app/repository.py`;
- SQL values use bound parameters;
- behavior changes include tests using the temporary database fixture;
- validation includes `ruff check .` and `pytest -q`;
- dependencies are pinned;
- secrets and customer-specific Azure values are never committed;
- Azure authentication prefers managed identity.

An audit should flag instructions that contradict the current code or prescribe
a one-off workshop task as permanent repository policy.

## 4. Task A: partial task update

An acceptable `PATCH /tasks/{task_id}` implementation should:

- define a request model with optional `title` and `done` fields;
- reject a body where both fields are omitted with a defined 4xx response;
- update only supplied fields and retain omitted values;
- use bound SQL parameters for values and avoid user-controlled SQL fragments;
- return the complete persisted task;
- return HTTP 404 when the task does not exist.

Expected tests cover updating both fields, updating each field independently,
an empty body, and a missing task. A follow-up read or direct repository check
should demonstrate that the returned state was persisted.

## 5. Task B: N+1 query

A suitable set-based implementation can use one ordered `LEFT JOIN` across
tasks and tags, then group rows by task in Python. The left join is important:
an inner join would remove tasks with no tags.

The answer should explain the query count explicitly:

- before: one task query plus one tag query per task;
- after: one query regardless of the number of tasks.

Regression coverage should include no tags, one tag, multiple tags, and
deterministic task and tag ordering. Connection cleanup should use `try/finally`
or an equivalent pattern that closes on success and failure.

## 6. Diff review

A useful review puts findings before summary and checks:

- partial-update semantics and missing-record behavior;
- SQL parameterization;
- connection cleanup on exceptions;
- API status codes and response shapes;
- tests for success, edge cases, and persistence;
- unrelated changes.

The review should not edit files. If there are no findings, it should say so
and identify any validation that has not been run.

## 7. Azure architecture proposal

The current application stores data in a local SQLite file. In Azure Container
Apps, that file belongs to an ephemeral container or revision. A restart,
replacement, or new revision can lose it, and multiple replicas would not share
one consistent database.

For a short-lived demonstration, the smallest reasonable core is:

- Azure Container Apps on the consumption plan;
- Azure Container Registry for the image;
- Log Analytics and Application Insights for diagnostics;
- a system-assigned managed identity with only required roles;
- zero minimum replicas and one maximum replica;
- SQLite documented as disposable demonstration data.

Key Vault is not required when the application has no secret. Cosmos DB, Azure
SQL, PostgreSQL, and Azure OpenAI are modernization choices only after an
application requirement and repository change justify them.

Primary cost drivers include registry SKU, log ingestion and retention,
Application Insights ingestion, Container Apps CPU and memory, and any managed
database added later. Participants need permission to create resources and
role assignments, plus quota in their chosen region.

## 8. Deployment artifacts

Generated artifacts should agree on service name, image, target port, and
outputs:

- the Dockerfile runs Uvicorn on the Container Apps target port;
- a health probe calls `/health`;
- `azure.yaml` maps the application service to the Bicep outputs;
- Bicep parameters contain no tenant, subscription, or participant-specific
  identifiers;
- names derive from parameters and a deterministic unique suffix;
- scaling permits zero minimum replicas and enforces one maximum replica;
- RBAC is scoped to the resource that requires access;
- Bicep and azd validation run before deployment.

Generation alone is not proof that `azd up` will work. Participants should
inspect the diff and run preflight validation first.

## 9. Secure deployment workflow

An acceptable workflow:

- triggers deployment only from `main` or `workflow_dispatch`;
- runs Ruff and pytest before deployment;
- grants `contents: read` and `id-token: write` only where required;
- authenticates to Azure with GitHub OIDC federation;
- reads client, tenant, and subscription identifiers from repository or
  environment configuration rather than hardcoding values;
- uses a protected GitHub environment for production approval;
- prevents overlapping production deployments with concurrency;
- makes provisioning and application deployment steps explicit.

No client secret should be stored in GitHub.

## 10. Observability and final audit

Telemetry should initialize once, read configuration from environment
variables, and leave local tests independent of Azure. It should identify the
service and environment without recording task titles, request bodies,
credentials, or prompt content.

The final audit should report evidence for:

- committed secrets or customer-specific identifiers;
- unsafe SQL or missing validation;
- excessive RBAC scope;
- public ingress and registry exposure;
- missing replica or cost limits;
- telemetry privacy risks;
- deployment steps that cannot be reproduced.

A blocked budget, role assignment, quota check, or deployment should be
recorded with the required permission. It should not be reported as an
application-code failure.