# Repository Instructions Walkthrough

Repository instructions tell GitHub Copilot how work should be done in a
specific codebase. They capture stable project facts, engineering conventions,
and validation requirements that should influence many different requests.

In this repository, the active instructions are in
[`.github/copilot-instructions.md`](../.github/copilot-instructions.md).
Because the file is committed to source control, everyone who clones the
repository receives the same guidance.

## When to use repository instructions

Use repository instructions for guidance that is:

- true for most work in the repository;
- specific enough to affect Copilot's implementation decisions;
- agreed by the team rather than personal preference;
- expected to remain valid across multiple tasks;
- useful during code generation, review, testing, or documentation work.

Examples include the supported technology stack, architectural boundaries,
security requirements, test commands, and rules for handling dependencies.

Do not use repository instructions for a single feature request, temporary
workshop task, or lengthy material already explained in the README. Put a
repeatable task in a prompt file and link to existing documentation instead of
copying it.

## How Copilot uses the file

Instructions are automatically added to Copilot's context when someone works
in the repository. A participant does not need to invoke them as a slash
command.

For example, a request such as:

> Add an endpoint that returns a task by title.

is short and leaves many implementation choices open. The repository
instructions tell Copilot to keep the HTTP handler in `app/main.py`, put SQL in
`app/repository.py`, use bound SQL parameters, add a test, and avoid unrelated
changes.

Instructions guide the model, but they are not an enforcement mechanism.
Linters, tests, branch policies, and code review still enforce the rules.

## Walkthrough: create useful instructions

### 1. Inspect the repository before writing rules

Identify facts that can be verified from the code and configuration:

- [`app/main.py`](../app/main.py) contains the FastAPI routes.
- [`app/repository.py`](../app/repository.py) owns data access.
- [`app/db.py`](../app/db.py) configures SQLite.
- [`tests/conftest.py`](../tests/conftest.py) provides an isolated temporary
  database for every test.
- [`ruff.toml`](../ruff.toml) configures linting.
- [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs Ruff and pytest
  on Windows and Ubuntu.

This evidence is more useful than broad statements such as "write clean code."

### 2. Separate stable rules from task instructions

Ask of every proposed line: should this affect most future changes?

Good repository rule:

> Data access belongs in `app/repository.py`; other application modules do not
> open database connections.

Task-specific statement that belongs in a prompt or chat request:

> Add `PATCH /tasks/{task_id}` and test updates to the title.

### 3. Write instructions that change an observable decision

Prefer precise, actionable language:

| Weak instruction | Better instruction |
|---|---|
| Write good tests. | Add or update pytest coverage for every behavior change. |
| Use secure SQL. | Use bound parameters; never concatenate values into SQL. |
| Follow the architecture. | Keep HTTP concerns in `app/main.py` and database access in `app/repository.py`. |
| Check your work. | Run `ruff check .` and `pytest -q` after code changes. |

### 4. Include the cheapest validation commands

For this project, the useful commands are:

```powershell
pip install -r requirements.txt
ruff check .
pytest -q
```

The instructions should tell Copilot which commands are expected, while CI
remains the final source of enforcement.

### 5. Test the instructions with a realistic request

Start a new chat so the updated context is loaded, then ask:

> Add an endpoint to mark a task complete. Include tests and verify the change.

Inspect the resulting plan or diff:

- Is the route in `app/main.py`?
- Is SQL isolated in `app/repository.py`?
- Are query values passed as bound parameters?
- Does the API return an appropriate status for a missing task?
- Were Ruff and pytest run?

If Copilot repeatedly misses a repository-specific requirement, make that rule
more explicit. Do not add instructions merely to correct a one-off mistake.

## Suggested file for this repository

The existing file already contains most of the right information. A concise
version could look like this:

```markdown
# Project guidelines

## Stack

- Use Python 3.11, FastAPI, Pydantic v2, and the standard `sqlite3` module.
- Do not introduce an ORM without first explaining why it is needed.

## Architecture

- Keep HTTP validation and response handling in `app/main.py`.
- Keep SQL and connection management in `app/repository.py`.
- Use bound SQL parameters and prefer one query over a loop of queries.
- Repository functions return domain data or `None`; API handlers translate
  missing results into appropriate HTTP responses.

## Tests and validation

- Add or update tests for every behavior change.
- Use the temporary database fixture in `tests/conftest.py`.
- Do not remove or weaken assertions to make a change pass.
- Run `ruff check .` and `pytest -q` after code changes.

## Dependencies and security

- Pin new Python dependencies in `requirements.txt`.
- Never commit secrets, keys, connection strings, or subscription IDs.
- Parameterize Azure location, resource names, and SKU.
- Prefer managed identity for service-to-service authentication.

## Scope

- Do not reformat or modify unrelated files.
```

Treat this as a starting point, not a universal standard. A frontend, data
science, or multi-service repository needs different boundaries and commands.

## General best practices

1. Keep the file short enough to remain useful on every request.
2. Record decisions that are not obvious from language defaults or tooling.
3. Use exact paths and executable commands where they improve clarity.
4. Explain architectural ownership, especially where code should and should
   not go.
5. Prefer measurable requirements over subjective wording.
6. Link to detailed documentation instead of duplicating it.
7. Update instructions when the architecture or toolchain changes.
8. Keep personal preferences in user-level instructions, not the shared repo.

For a larger repository, use targeted instruction files under
`.github/instructions/` with narrow `applyTo` patterns, for example one file
for `**/*.py` and another for `infra/**/*.bicep`. Avoid applying every detailed
instruction to every file type.

## Common mistakes

- Copying the entire README into the instruction file.
- Including temporary feature requirements as permanent policy.
- Using vague statements such as "follow best practices."
- Repeating rules already fully enforced and explained by the formatter.
- Mixing contradictory rules from multiple instruction files.
- Assuming instructions guarantee compliance without tests or review.
- Adding secrets, environment-specific identifiers, or customer data.

## Review checklist

Before committing repository instructions, confirm that:

- each rule applies to many likely tasks;
- each rule is accurate for the current repository;
- architectural responsibilities are explicit;
- build, lint, and test commands are executable;
- security requirements are concrete;
- detailed documentation is linked rather than duplicated;
- no secret or environment-specific value is present;
- the file has been tried against at least one realistic request.