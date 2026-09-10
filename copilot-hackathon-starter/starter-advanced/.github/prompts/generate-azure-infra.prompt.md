---
mode: agent
description: Generate Bicep and an azd template for this repo.
---

Read this repository and generate infrastructure as code for it.

Requirements:

- Bicep under `infra/`, with a `main.bicep` and a `main.parameters.json`.
- Parameterise the environment name, location and SKU. Hardcode nothing that
  is specific to one subscription.
- Use managed identity for any service-to-service access. No keys in code.
- Include a cost guardrail: the smallest viable SKU, and scale-to-zero where
  the service supports it.
- Add an `azure.yaml` so `azd up` provisions and deploys this app.
- Add a `.github/workflows/deploy.yml` that builds, tests and deploys.

Before you write anything, tell me which Azure services you have chosen and
why, in no more than five lines. Wait for me to confirm.
