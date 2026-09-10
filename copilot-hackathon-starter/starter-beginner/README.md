# Hackathon Starter — Beginner Room

A tiny Task API you can run in one command. It is deliberately small and
deliberately imperfect: the exercises in the session ask GitHub Copilot to
improve it.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://localhost:8000/docs

## Check it works

```bash
curl http://localhost:8000/health
pytest -q
```

## What is here

| Path | What it is |
|---|---|
| `app/main.py` | The API. Health check plus task endpoints. |
| `app/store.py` | Where tasks are kept. Simple on purpose. |
| `tests/test_health.py` | One test, so you know the setup works. |
| `.env.example` | Copy to `.env` if you add settings. |

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

## Deploy to Azure App Service

The `infra` folder contains subscription-scoped Bicep and an idempotent
PowerShell deployment script. The deployment creates:

- a resource group;
- a Linux App Service plan and web app;
- a user-assigned managed identity;
- Application Insights and a Log Analytics workspace; and
- App Service diagnostic settings.

The default `P0v3` plan incurs charges. Review
`infra/main.parameters.json` before deployment if you need to change the
region, SKU, or allowed CORS origins.

Preview the Azure changes without creating resources:

```powershell
./infra/deploy.ps1 -Preview
```

Deploy the infrastructure and application code:

```powershell
./infra/deploy.ps1
```

The script generates a short resource token on its first run and stores it
under `.azure` so later runs update the same resources. You can instead pass a
stable token containing up to five lowercase letters:

```powershell
./infra/deploy.ps1 -ResourceToken abcde
```

After deployment, the script prints the application, health-check, and API
documentation URLs. Allow two to three minutes for the first build and start.

To remove the workshop resources, find the resource group printed in the
deployment output and delete it explicitly:

```powershell
az group delete --name <resource-group-name> --yes --no-wait
```
