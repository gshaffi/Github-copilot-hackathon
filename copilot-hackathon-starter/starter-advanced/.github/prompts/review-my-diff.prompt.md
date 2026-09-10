---
mode: agent
description: Review the current diff the way a staff engineer would.
---

Review the changes currently in my working tree.

For each issue, give me:

- the file and line,
- what is wrong,
- why it matters in a four-day hackathon specifically,
- the smallest change that fixes it.

Prioritise, in this order: correctness, security (secrets, injection, input
validation), cost and quota risk on Azure, test coverage, then readability.

Be blunt. If a change should not be merged, say so and say why. Do not
compliment the code.
