# Prompt Files Walkthrough

Prompt files are reusable task templates for GitHub Copilot. They let a team
run the same well-scoped request repeatedly without rewriting its acceptance
criteria each time.

Workspace prompt files live under `.github/prompts/` and use the
`.prompt.md` extension. This repository includes:

- [`add-endpoint.prompt.md`](../.github/prompts/add-endpoint.prompt.md)
- [`review-my-diff.prompt.md`](../.github/prompts/review-my-diff.prompt.md)
- [`generate-azure-infra.prompt.md`](../.github/prompts/generate-azure-infra.prompt.md)

Unlike repository instructions, a prompt applies only when a user chooses it.
In VS Code, type `/` in Chat and select the prompt, run **Chat: Run Prompt**
from the Command Palette, or open the prompt file and use its run button.

## When to use a prompt file

Create a prompt when a task is:

- performed repeatedly by one person or several team members;
- focused enough to have a clear outcome;
- improved by consistent inputs and acceptance criteria;
- specific to a workflow rather than every repository interaction;
- valuable to keep, review, and version alongside the code.

Good examples include adding an API endpoint, generating tests, reviewing the
current diff, preparing release notes, or investigating a known class of
failure.

Do not create a prompt for stable project-wide conventions; those belong in
repository instructions. A long workflow with multiple stages, scripts, and
supporting assets may be better represented by a skill or custom agent.

## Instructions and prompts working together

The two customization types should complement rather than duplicate each
other:

- Repository instructions define **how this team builds software**.
- A prompt file defines **what task Copilot should perform now**.

For this Task API, the repository instructions already say where HTTP and SQL
code belong. An endpoint prompt should refer to those conventions and focus on
the requested route, behavior, acceptance criteria, and validation.

## Prompt file structure

A prompt normally has YAML frontmatter followed by Markdown instructions:

```markdown
---
name: "Add API endpoint"
description: "Add a Task API endpoint with repository access and tests"
argument-hint: "Describe the HTTP method, route, and behavior"
agent: "agent"
---

Add the requested endpoint following the repository instructions.

Ask for any required input that is missing. Implement the change, add tests,
run the repository validation commands, and summarize the result.
```

Useful frontmatter fields include:

| Field | Purpose |
|---|---|
| `name` | Human-readable name shown when selecting the prompt. |
| `description` | Explains when and why to use it. |
| `argument-hint` | Shows which input the user should provide. |
| `agent` | Selects a chat mode such as `agent`, `ask`, or `plan`. |
| `tools` | Optionally limits the tools available to the prompt. |
| `model` | Optionally selects a model when the workflow requires one. |

Only add fields that improve the workflow. Avoid pinning a model or listing
many tools without a concrete reason.

## Walkthrough: create an endpoint prompt

### 1. Define one outcome

Choose a task with a clear finish line:

> Add one API endpoint and its tests, then run validation.

Avoid combining unrelated work such as adding an endpoint, redesigning the
database, provisioning Azure, and writing release notes in one prompt.

### 2. Identify the variable input

The reusable workflow stays the same, but each invocation needs a method,
route, and behavior. Expose that through `argument-hint`:

```yaml
argument-hint: "Method, route, behavior, and expected status codes"
```

Tell Copilot to ask only for required information that is missing. This lets a
participant invoke the prompt either interactively or with complete input:

```text
/add-endpoint PATCH /tasks/{task_id}; update title; return 404 when missing
```

### 3. State acceptance criteria

Acceptance criteria should describe observable results rather than prescribe
every implementation detail. Repository-specific architectural rules can be
referenced instead of copied.

```markdown
Acceptance criteria:

- The route returns the documented success status and response body.
- A missing task returns HTTP 404.
- Happy-path and missing-task behavior have API tests.
- Existing behavior remains unchanged.
```

### 4. Set scope and autonomy

An implementation prompt should make it clear whether Copilot may edit files
and run commands. Using `agent: "agent"` supports an implementation workflow.
Also state boundaries such as:

```markdown
Follow the repository instructions. Modify only files required for this
endpoint and its tests. Do not perform unrelated refactoring.
```

For a review-only prompt, explicitly say not to edit files.

### 5. Require verification and a useful final response

For this repository, finish with:

```markdown
Run `ruff check .` and `pytest -q`. Report the files changed, the behavior
added, and the validation results. If a command cannot run, explain why.
```

This produces a checkable result rather than an unsupported claim that the
task is complete.

### 6. Run and evaluate the prompt

Invoke the prompt with a concrete task:

```text
/add-endpoint GET /tasks/{task_id}/tags; return tag labels; return 404 when the
task does not exist
```

Check whether Copilot:

- asks only for genuinely missing information;
- follows the repository's architectural boundaries;
- changes the smallest reasonable set of files;
- handles both success and failure behavior;
- runs the requested validation;
- reports blockers rather than hiding them.

Refine the prompt when the same ambiguity appears across multiple runs.

## Complete example for this repository

```markdown
---
name: "Add Task API endpoint"
description: "Implement one Task API endpoint with repository access and tests"
argument-hint: "Method, route, behavior, and expected status codes"
agent: "agent"
---

Implement the requested Task API endpoint, following the repository
instructions.

Ask for any essential input that has not been provided. Then:

1. Add the route in `app/main.py` and keep its handler focused on HTTP concerns.
2. Add data access to `app/repository.py` only when required.
3. Return appropriate HTTP status codes, including 404 for a missing task.
4. Add happy-path and failure coverage in `tests/test_api.py`.
5. Run `ruff check .` and `pytest -q`.

Do not modify unrelated files. Finish with a concise summary of the behavior,
files changed, and validation results.
```

## Other useful prompt examples

### Review the current diff

Use a review prompt to make review priorities and output consistent:

```markdown
---
name: "Review current diff"
description: "Review uncommitted changes for correctness, security, and tests"
agent: "ask"
---

Review the current working-tree diff. Do not edit files.

List findings first, ordered by severity. For each finding, include the file
and line, impact, and smallest reasonable fix. Prioritize correctness,
security, Azure cost or quota risk, and missing tests. If there are no
findings, say so and identify any remaining validation gap.
```

Example invocation:

```text
/review-current-diff
```

### Investigate a performance problem

This repository deliberately contains an N+1 query in
`list_tasks_with_tags`. A focused investigation prompt could be:

```markdown
---
name: "Investigate data-access performance"
description: "Find repeated database queries and propose a tested optimization"
argument-hint: "Function, endpoint, or observed performance symptom"
agent: "agent"
---

Investigate the supplied performance concern. Measure or demonstrate the
problem where practical, identify its root cause, and make the smallest tested
change that fixes it. Preserve response behavior and follow the repository
instructions. Run `ruff check .` and `pytest -q` before finishing.
```

Example invocation:

```text
/investigate-data-access-performance list_tasks_with_tags becomes slow as the
number of tasks increases
```

## General best practices

1. Give each prompt one clear purpose and completion condition.
2. Write a specific description so users can discover the right prompt.
3. Expose variable inputs through `argument-hint` or an explicit question.
4. Reference repository instructions instead of duplicating stable rules.
5. Include acceptance criteria and executable validation commands.
6. State whether the prompt should edit files, review only, or produce a plan.
7. Restrict scope to reduce unrelated changes.
8. Specify an output format only when consistency adds real value.
9. Keep prompts in source control and review changes like code.
10. Test prompts with both complete and incomplete user input.

## Common mistakes

- Writing a vague description such as "helps with code."
- Combining planning, implementation, deployment, and review into one large
  prompt without checkpoints.
- Repeating the full repository instruction file inside every prompt.
- Omitting inputs, success criteria, or validation commands.
- Selecting tools or a model that the task does not require.
- Asking Copilot to claim success without running a check.
- Allowing an implementation prompt to modify unrelated files.
- Using a prompt as a substitute for tests, CI, or human review.

## Review checklist

Before committing a prompt file, confirm that:

- its filename ends in `.prompt.md` and it is under `.github/prompts/`;
- its name and description make its purpose obvious;
- it represents one focused, repeatable task;
- required user input is clear;
- acceptance criteria are observable;
- repository rules are referenced rather than duplicated;
- editing permissions and scope are explicit;
- validation commands match the actual repository;
- the expected final response is useful;
- the prompt has been run at least once with a realistic example.