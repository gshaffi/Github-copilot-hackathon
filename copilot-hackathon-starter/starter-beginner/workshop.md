# GitHub Copilot Hackathon: Beginner Workshop

Use this guide during the session instead of copying tasks from the slides.
The first half introduces GitHub Copilot through a small FastAPI application.
The second half uses Copilot to containerize the application and plan a simple
Azure deployment.

## Workshop outcomes

By the end of the session, you should have:

- a green local baseline;
- an explanation of the application that you can verify against the code;
- one small, tested API improvement;
- a reviewed working-tree diff;
- a locally tested container, if Docker is available;
- a small Azure service proposal with cost and permission considerations;
- deployment steps you understand before you run them;
- no credentials or subscription-specific values committed to the repository.

## Working agreement

GitHub Copilot can explain, plan, edit files, and run commands. You remain
responsible for the result.

For every exercise:

1. Name the relevant file or select the relevant code.
2. Describe the outcome rather than asking Copilot to "make it better."
3. Work in small steps and inspect each change.
4. Run the application or tests before accepting an answer.
5. Do not commit credentials, tokens, connection strings, or subscription IDs.
6. Do not run an Azure command that creates paid resources until you understand
   the command and approve the expected cost.

## 1. Set up the repository

From the `starter-beginner` directory, use Python 3.11 and establish a green
baseline.

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

Open `http://localhost:8000/docs` and confirm that the FastAPI documentation
loads. In a second terminal, check the health endpoint:

```bash
curl http://localhost:8000/health
```

The baseline should have two passing tests, and the health endpoint should
return `{"status":"ok"}`.

### Setup troubleshooting

- Run Uvicorn from `starter-beginner`; otherwise Python cannot import
  `app.main`.
- A `PytestCacheWarning` about `.pytest_cache` can occur in OneDrive or another
  synchronized folder. If the tests pass, the warning does not change the
  result. A local, non-synchronized development folder avoids it.
- If `py -3.11` or `python3.11` is unavailable, install Python 3.11 before the
  session rather than changing the application's dependency versions.

## 2. Ask Copilot to explain the repository

Use Ask mode so this exercise does not change files:

```text
Explain this repository to me as if I am new to the codebase. Cover how to run
it, how an HTTP request reaches the in-memory task store, how tasks are seeded,
and what the tests currently prove. Cite the files that support each answer.
Do not edit files.
```

Check the answer against the repository:

- `app/main.py` defines the FastAPI application and routes;
- `app/store.py` keeps tasks in a module-level dictionary;
- `store.seed()` adds starter tasks when the application module loads;
- `tests/test_health.py` covers health and seeded-task behavior;
- tasks disappear when the process restarts;
- missing-task and delete behavior do not return useful HTTP errors yet.

If the answer is vague, add a file as context or ask for the evidence behind
one claim.

## 3. Practice giving Copilot context

Copilot works best when a request identifies the code, outcome, and
constraints. Compare these prompts:

```text
Make this better.
```

```text
#app/main.py Explain how GET /tasks/{task_id} behaves when the task does not
exist. Do not edit files.
```

Use Ask mode for explanations and Agent mode when you want Copilot to edit
files and run validation. Always inspect the proposed plan and diff.

## 4. Make one tested application improvement

Start with the missing-task behavior shown in the slides. Use Agent mode:

```text
#app/main.py Update GET /tasks/{task_id} to return HTTP 404 when the task does
not exist. Keep the successful response unchanged. Add tests for an existing
task and a missing task, then run pytest -q. Do not change unrelated behavior.
```

Acceptance checks:

- an existing task still returns HTTP 200 and the task body;
- a missing task returns HTTP 404 rather than `null` with HTTP 200;
- the failure response does not expose internal details;
- new and existing tests pass;
- the diff contains only files required for this behavior.

Try one additional prompt only if time permits:

```text
#app/store.py Add focused unit tests for delete_task. Cover deleting an
existing task and deleting a missing task. Keep test state isolated and run
pytest -q.
```

Or select a function that has become difficult to read and ask:

```text
Refactor the selected code into smaller functions, one change at a time.
Preserve behavior, add or update tests, and run pytest -q after each step.
```

Do not refactor merely to create more functions. Each extracted function
should make one responsibility easier to understand or test.

## 5. Review the change

Use Ask mode for a read-only review:

```text
Review my current working-tree diff without editing files. Put findings first,
ordered by severity. Check behavior, HTTP status codes, test isolation, and
unrelated changes. For each finding, give the file, impact, and smallest fix.
If there are no findings, say so and name any remaining validation gap.
```

Then run:

```powershell
pytest -q
git diff --check
git diff
```

Do not commit code that you cannot explain.

## 6. Confirm Azure access

The second half uses your own Azure subscription. Confirm the active context
before asking Copilot to generate deployment commands:

```powershell
az login
az account show --output table
```

Check the subscription name carefully. Do not copy subscription or tenant IDs
into tracked files. If you cannot create resources, continue through planning,
container validation, and command review without running the deployment.

## 7. Choose a small Azure deployment path

Ask Copilot to inspect the application before recommending services. Use Plan
or Ask mode:

```text
Read this FastAPI repository and recommend at most two Azure services for the
fastest reasonable hackathon deployment. Explain why each service is needed,
whether it can scale to zero, the main cost and quota risks, required
permissions, and what happens to the in-memory tasks when the app restarts or
scales. Do not edit files or create resources. Wait for my approval before
generating deployment commands.
```

Check that the proposal recognizes:

- this is a Python HTTP API, not a static website;
- tasks are held only in process memory and are not durable;
- multiple instances would have different task collections;
- a short demonstration does not need a database unless durable data is a
  stated requirement;
- public ingress, scaling limits, region availability, and cleanup affect the
  deployment decision;
- the lowest-cost suitable option should be preferred for a short-lived demo.

Do not add a database, Key Vault, or AI service without a concrete application
requirement.

## 8. Add and test a container

After reviewing the service proposal, use Agent mode:

```text
Add a Dockerfile and .dockerignore for this FastAPI app. Use a supported slim
Python base image, install the pinned requirements, run as a non-root user,
start Uvicorn on port 8000, and include only files needed at runtime. Do not
add credentials. Build the image, run it locally, and verify /health.
```

Review the generated files, then run commands equivalent to:

```powershell
docker build --tag task-api:local .
docker run --rm --publish 8000:8000 task-api:local
```

In a second terminal:

```bash
curl http://localhost:8000/health
```

Acceptance checks:

- the image builds from a clean checkout;
- the container starts without the local virtual environment;
- `/health` returns HTTP 200;
- Uvicorn listens on `0.0.0.0`, not only localhost inside the container;
- dependency versions come from `requirements.txt`;
- `.venv`, caches, Git metadata, and local environment files are excluded;
- no credentials are copied into the image.

If Docker is unavailable, review the generated files and record that local
container execution remains a validation gap.

## 9. Generate and review deployment commands

After approving one Azure service, ask Copilot for steps before commands:

```text
For the approved Azure service, give me the shortest reproducible deployment
plan for this containerized FastAPI app. Separate one-time setup from repeat
deployments, identify every resource that will be created, include cost and
quota checks, and include cleanup. Do not run commands yet.
```

Then ask for commands:

```text
Write the Azure CLI commands for the approved plan and explain each command.
Use variables or placeholders for subscription-specific values, choose the
smallest suitable paid SKU or a scale-to-zero option, configure the health
endpoint and port correctly, and include a preview or validation step when the
service supports one. Do not include secrets and do not execute resource-
creating commands until I approve them.
```

Before running anything, verify:

- the selected region supports the service and SKU;
- your subscription has the required quota and permissions;
- resource names are unique and contain no customer data;
- scaling has an explicit upper bound;
- authentication does not place credentials in source control;
- the application port and health endpoint match the container;
- cleanup commands identify every billable resource.

If you approve deployment, run one command at a time and inspect its output.
Record the public application, `/health`, and `/docs` URLs. Delete short-lived
resources after the demonstration.

## 10. Prepare the repository for judges

Use Agent mode:

```text
#README.md Add concise setup and demo instructions for the judges. Include
prerequisites, local startup, tests, container startup, the public demo URL as
a placeholder, the three endpoints to demonstrate, known limitations, and
resource cleanup. Do not add credentials or customer-specific Azure values.
Run the documented local checks before finishing.
```

The README should let another person reproduce the demo without relying on
your terminal history.

## Completion checklist

Before leaving the session, confirm:

- [ ] The local baseline passed.
- [ ] Copilot's repository explanation was checked against the code.
- [ ] One API behavior was improved and tested.
- [ ] The working-tree diff was reviewed.
- [ ] The container was reviewed and tested, or the validation gap was noted.
- [ ] The Azure service choice was limited and justified.
- [ ] Cost, quota, permissions, scaling, and cleanup were checked.
- [ ] Resource-creating commands were approved before execution.
- [ ] No credentials or subscription-specific identifiers were committed.
- [ ] The demo instructions and public URL are ready for judges.

The goal for day one is a thin, working demonstration. Add complexity only
when it supports the behavior you plan to show.