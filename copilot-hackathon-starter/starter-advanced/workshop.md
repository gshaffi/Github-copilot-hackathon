# GitHub Copilot Hackathon: Advanced Workshop

Use this guide during the session instead of copying tasks from the slides.
The live workshop focuses on one tested application change and one coherent
Azure deployment path. Additional architecture, database, and AI challenges
are available after the session.

## Workshop outcomes

By the end of the live session, you should have:

- a green local baseline;
- repository-specific Copilot instructions;
- one tested application or data-layer improvement;
- a structured review of the generated diff;
- an approved Azure architecture with an explicit persistence decision;
- generated deployment artifacts, if your Azure access permits;
- no secrets committed to the repository.

## Working agreement

Copilot can plan, edit files, and run commands. You remain responsible for the
result.

For every exercise:

1. Read the agent's plan before it edits files.
2. Inspect the diff rather than accepting it automatically.
3. Run the relevant validation commands.
4. Do not accept code you cannot explain.
5. Do not commit credentials, connection strings, tokens, or subscription IDs.

## 1. Set up the repository

From the `starter-advanced` directory, create an environment and establish a
green baseline. Use Python 3.11, which is the version exercised by CI. Check
with `python --version` or `py -3.11 --version` before creating the environment.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ruff check .
pytest -q
uvicorn app.main:app --reload
```

### macOS or Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ruff check .
pytest -q
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` and confirm that the FastAPI documentation
loads.

### Setup troubleshooting

- A `PytestCacheWarning` about access to `.pytest_cache` can occur when the
  repository is inside OneDrive or another synchronized folder. If the tests
  pass, the warning does not change the result. Use a local, non-synchronized
  development folder to restore pytest caching.
- If dependencies emit deprecation warnings on a newer Python release, first
  recreate `.venv` with Python 3.11 before treating the warning as an
  application defect.
- Run Uvicorn from `starter-advanced`; otherwise Python cannot import
  `app.main`.

### Ask Copilot to explain the repo

Use Ask mode so this task does not change files:

```text
Explain this repository to a new engineer. Cover the request flow, database
initialization, test isolation, CI checks, and deliberate weaknesses. Cite the
files that support each conclusion. Do not edit anything.
```

Check that the answer identifies:

- FastAPI routes in `app/main.py`;
- SQLite setup and seed data in `app/db.py`;
- data access in `app/repository.py`;
- temporary test databases configured by `tests/conftest.py`;
- Ruff and pytest in `.github/workflows/ci.yml`;
- the missing-record, direct-coupling, and N+1 weaknesses.

## 2. Configure Copilot for the repository

Open `.github/copilot-instructions.md`. Repository instructions should contain
stable guidance that applies to many tasks, including architecture, testing,
security, and validation commands.

Use this prompt:

```text
Audit .github/copilot-instructions.md against the code, tests, Ruff config,
and CI workflow. Identify inaccurate, ambiguous, missing, or redundant rules.
Make only high-value changes that apply to most repository tasks. Show the
proposed diff before editing.
```

Confirm that the instructions:

- keep HTTP concerns in `app/main.py`;
- keep SQL and connection management in `app/repository.py`;
- require bound SQL parameters;
- require tests for behavior changes;
- require `ruff check .` and `pytest -q`;
- prevent secrets and customer-specific Azure values from being committed;
- remain concise and do not copy the README.

More detail is available in
[`examples/repo-instructions-walkthrough.md`](examples/repo-instructions-walkthrough.md).

## 3. Choose one live coding task

Complete either task A or task B during the live session. You can complete the
other task after the session.

### Task A: add `PATCH /tasks/{task_id}`

Use the shipped endpoint prompt or provide the following request in Agent mode:

```text
/add-endpoint PATCH /tasks/{task_id}. Accept optional title and done fields,
require at least one field, return the updated task, and return 404 when the
task does not exist. Add happy-path, partial-update, empty-body, and missing-task
tests. Run Ruff and pytest.
```

Acceptance checks:

- The handler performs a partial update.
- Omitted fields retain their existing values.
- An empty update has a defined validation response.
- A missing task returns HTTP 404.
- Request values are passed to SQL as bound parameters.
- The updated state is persisted and returned.
- New and existing tests pass.

### Task B: fix the N+1 query

Use Agent mode:

```text
Inspect the data-access layer for N+1 queries. Demonstrate each occurrence,
replace it with the smallest set-based query, preserve response shape and
ordering, add regression coverage including a task with no tags, and run Ruff
and pytest. Show the diff and explain the query count.
```

Acceptance checks:

- `list_tasks_with_tags` no longer runs one tag query per task.
- The result still contains `id`, `title`, `done`, and `tags`.
- Tasks with no tags remain in the result with an empty list.
- Tasks with multiple tags retain all labels.
- Ordering is deterministic.
- Database connections close on success and failure.
- New and existing tests pass.

## 4. Review the generated change

Run the shipped review prompt:

```text
/review-my-diff
```

Or use this focused version in Ask mode:

```text
Review the current diff without editing files. Prioritize behavioral
regressions, SQL safety, connection cleanup, API status codes, and missing
tests. Put findings first, ordered by severity. For each finding, provide the
file and line, impact, and smallest fix. If there are no findings, say so and
name any remaining validation gap.
```

Then run:

```powershell
ruff check .
pytest -q
git diff --check
git diff
```

Do not merge or commit the change until you understand the diff and the checks
are green.

## 5. Confirm Azure access

The Azure exercises use your own subscription. Confirm the active context
before generating or deploying resources:

```powershell
az login
az account show --output table
az vm list-usage --location <your-region> --output table
```

Do not put the selected subscription ID or tenant-specific values into tracked
files. If your subscription does not allow resource creation, pair with another
participant and continue reviewing the generated artifacts.

## 6. Propose the Azure architecture

Do not begin by naming resources. Ask Copilot to inspect the workload and
explain its persistence assumptions first:

```text
Read this repository and propose the smallest viable Azure architecture for a
four-day hackathon.

Before changing files:

1. Explain how the application currently stores data.
2. Explain what happens to SQLite data when the application runs in Azure
   Container Apps and restarts or scales.
3. Separate required demo resources from optional modernization resources.
4. Identify cost drivers, quota requirements, and required permissions.
5. Prefer managed identity and least-privilege access.
6. Wait for approval before generating code or infrastructure.

Do not add Cosmos DB, Key Vault, or Azure OpenAI unless you identify a concrete
application requirement for each service.
```

For the core workshop path, a reasonable proposal is:

- Azure Container Apps consumption environment;
- Azure Container Registry;
- Log Analytics and Application Insights;
- a system-assigned managed identity with minimal permissions;
- no Key Vault when the application has no secret;
- one maximum replica while SQLite remains local;
- SQLite explicitly treated as disposable demonstration data.

This is not a production persistence design. Container restarts and new
revisions can lose local SQLite data. A durable design requires a repository
adapter for a managed database and migration tests.

Review the proposed services, cost controls, identity model, and SQLite tradeoff
before approving generation.

## 7. Generate the core deployment artifacts

After approving the architecture, run the infrastructure prompt:

```text
/generate-azure-infra

Optimize for a short-lived demo. Use the approved Container Apps, Container
Registry, Log Analytics, and Application Insights architecture. Keep SQLite
only as explicitly non-durable demo data, set the app to at most one replica,
parameterize location and capacity, and use managed identity. Do not add Cosmos
DB or Key Vault unless you first explain the application changes that require
them. Wait for approval before editing.
```

Expected artifacts include:

```text
Dockerfile
azure.yaml
infra/
  main.bicep
  main.parameters.json
.github/workflows/deploy.yml
```

The exact Bicep module layout may differ. Judge the behavior rather than the
number of files.

Acceptance checks:

- The Dockerfile starts Uvicorn on the Container Apps target port.
- `/health` is used for health checks.
- Bicep parameters contain no subscription-specific values or secrets.
- Resource names are derived from parameters and unique values.
- Minimum replicas can be zero for cost control.
- Maximum replicas is one while SQLite remains local.
- Managed identity and least-privilege RBAC are used where access is required.
- `azure.yaml`, Bicep outputs, and application settings agree.
- The generated infrastructure is validated before deployment.

Generation is not deployment. Inspect the plan and diff before running
`azd up`.

## 8. Add a secure deployment workflow

The existing workflow validates pull requests. The deployment workflow should
deploy only trusted code and should use federated identity rather than a stored
Azure client secret.

Use Agent mode:

```text
Add a GitHub Actions deployment workflow for the approved azd architecture.
Use GitHub OIDC federation to Azure rather than a client secret. Run Ruff and
pytest before deployment, deploy only from main or manual dispatch, use a
GitHub environment for production approval, and document required repository
variables and federated credentials. Do not change the existing pull-request
CI behavior.
```

Acceptance checks:

- The workflow grants `id-token: write` and `contents: read` only where needed.
- Authentication uses OIDC federation.
- Tenant, subscription, and client identifiers are configuration, not values
  hardcoded into the workflow.
- Pull requests cannot deploy untrusted code.
- Ruff and pytest run before deployment.
- Deployment concurrency prevents overlapping production deployments.
- Provisioning and application deployment behavior are explicit.

## 9. Add observability

Use Agent mode:

```text
Instrument this FastAPI service with the Azure Monitor OpenTelemetry
distribution. Capture incoming HTTP requests and supported outbound calls,
configure telemetry through environment variables, avoid logging task titles
or request bodies, and keep tests independent of Azure. Update pinned
dependencies and document local and Azure configuration. Run Ruff and pytest.
```

Acceptance checks:

- The Azure Monitor OpenTelemetry dependency is pinned.
- Instrumentation is configured once during application startup.
- Telemetry configuration is read from the environment.
- Request bodies, credentials, and task content are not logged by default.
- Service and environment attributes make telemetry identifiable.
- Unit tests do not contact Application Insights.
- The application still starts when local telemetry is disabled.

## 10. Audit the result

Use Ask mode so the audit does not edit files:

```text
Audit this repository and proposed Azure changes without editing files. Report
findings first, ordered by severity. Check for committed secrets, unsafe SQL,
missing input validation, excessive RBAC, public network exposure, resources
without explicit scaling limits, missing cost controls, and deployment steps
that cannot be reproduced. For each finding, give evidence and the smallest
fix. Do not invent findings.
```

Review at least:

- tracked files for secrets and customer-specific identifiers;
- application input validation and error responses;
- SQL parameterization;
- managed identity and RBAC scope;
- public ingress and registry access;
- minimum and maximum replica settings;
- Azure service SKUs and major cost drivers;
- telemetry data collection;
- reproducibility of Bicep, azd, and the deployment workflow.

A subscription budget is recommended but may require permissions you do not
have. Record that limitation rather than treating it as an application failure.

## Live-session completion checklist

Before the live session ends, confirm:

- [ ] The local baseline was green.
- [ ] Repository instructions were reviewed.
- [ ] One coding task was implemented and tested.
- [ ] The generated diff was reviewed.
- [ ] The Azure architecture was approved before generation.
- [ ] SQLite persistence limitations were documented.
- [ ] Generated infrastructure contains scaling and cost controls.
- [ ] Deployment authentication uses identity rather than a client secret.
- [ ] No credentials or subscription-specific values were committed.
- [ ] Any blocked deployment step and its required permission were recorded.

# After the session: optional stretch tasks

These exercises build on the live session. Complete them separately so each
architectural change can be reviewed and tested.

## Stretch 1: complete the other coding exercise

If you added the PATCH endpoint during the session, fix the N+1 query. If you
fixed the N+1 query, add the PATCH endpoint. Use the prompts and acceptance
checks in section 3.

## Stretch 2: put persistence behind an interface

The current API imports repository functions directly. Introduce a small
interface without changing storage technology:

```text
Refactor task persistence behind a small TaskRepository protocol and a concrete
SQLiteTaskRepository. Inject the repository into FastAPI handlers using one
consistent mechanism. Preserve all HTTP behavior and keep tests isolated on a
temporary SQLite database. Do not add an ORM or change storage technology. Run
Ruff and pytest.
```

Acceptance checks:

- The interface describes task operations rather than raw connections or SQL.
- SQLite remains the concrete implementation.
- API handlers depend on the interface.
- Tests demonstrate that the implementation can be substituted.
- Existing behavior remains green.

## Stretch 3: migrate to durable managed storage

Do not provision Cosmos DB and stop there. Design and implement the complete
persistence change:

```text
Design a migration from SQLite to a managed Azure data service. Compare Cosmos
DB, Azure SQL, and Azure Database for PostgreSQL against the current access
patterns. Recommend one and explain the data model, keys or partitioning,
repository adapter, managed-identity roles, local development behavior,
migration or seed strategy, tests, cost, and scaling implications. Wait for
approval before editing or provisioning resources.
```

If Cosmos DB is selected, acceptance checks include:

- The partition key follows the demonstrated query patterns.
- Task and tag document shapes are explicit.
- A Cosmos implementation satisfies the repository interface.
- Authentication uses managed identity on Azure.
- Data-plane RBAC is scoped to the required account or database.
- Local tests use a fake or approved emulator strategy.
- Seed or migration behavior is repeatable.
- The SQLite implementation is removed only after equivalent behavior passes.
- Bicep includes throughput and scaling limits with clear cost implications.

Provisioning a database that the application never calls is not a completed
migration.

## Stretch 4: add a defined Azure OpenAI feature

Add a product behavior rather than an isolated SDK call:

```text
Add POST /tasks/suggest. It accepts a short project goal and returns three
concise suggested task titles using an approved Azure OpenAI model deployment.
Put the call behind a TaskSuggester interface, validate input, use managed
identity, configure explicit timeouts and bounded retries, avoid logging prompt
content, return a defined 503 response when the upstream service is unavailable,
and test with a fake client. Unit tests must not call Azure.
```

Acceptance checks:

- The endpoint has documented request and response models.
- Input length and empty input are validated.
- The route depends on a testable application interface.
- Azure authentication uses managed identity rather than an API key.
- Endpoint and deployment name come from environment configuration.
- Timeouts, rate limits, and transient failures have defined behavior.
- Prompts and generated content are not logged by default.
- Unit tests use a fake client and do not require Azure access.
- Model availability, region, quota, and permissions are confirmed separately.

## Stretch 5: run a final staff-level review

Run `/review-my-diff` again across the completed stretch work. Pay particular
attention to persistence semantics, partitioning, retries, telemetry privacy,
RBAC, cost limits, and failure behavior.

## Supporting material

- [`README.md`](README.md): setup and repository overview
- [`examples/repo-instructions-walkthrough.md`](examples/repo-instructions-walkthrough.md): repository instruction guidance
- [`examples/prompt-files-walkthrough.md`](examples/prompt-files-walkthrough.md): prompt file guidance
- [`examples/advanced-session-example-answers.md`](examples/advanced-session-example-answers.md): facilitator examples and expected answers