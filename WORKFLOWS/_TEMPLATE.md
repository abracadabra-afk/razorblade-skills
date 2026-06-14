---
type: workflow-template
purpose: Copy this when creating a new workflow.
---

# WORKFLOW TEMPLATE

> **For any AI reading this:** Workflow files describe a named sequence of prompts/steps the AI executes on user trigger. Each step is run in order. Outputs of step N feed step N+1 unless otherwise noted.

---

## Frontmatter (required)

```yaml
---
type: workflow
name: <slug-case-name>
trigger: <natural-language phrase the user will say to invoke this>
aliases: [<alt phrase 1>, <alt phrase 2>]
inputs: [<what the user provides>]
outputs: [<what gets produced>]
lane: <fiction | inkwell | personal | writing-ops>
status: active | draft | deprecated
last_updated: YYYY-MM-DD
---
```

---

## Body sections (suggested)

```
# WORKFLOW: <name>

## When to use
1–3 sentences. Trigger phrases the user might say. Common cases.

## Inputs
What the user provides (raw text, file, paste, etc.).

## Outputs
What the AI returns (cleaned text, summary, list, etc.).

## Steps

### Step 1 — <name>
**Prompt source:** [[link to canonical prompt file]] (or inline below)
**Input:** raw input
**Output:** intermediate-1
**Notes:** anything the AI should know about this step

(inline prompt text if not linked)

### Step 2 — <name>
**Prompt source:** [[link]]
**Input:** intermediate-1
**Output:** intermediate-2

...

### Step N — <name>
**Output:** final output to return to user

## Stop conditions
When to halt mid-workflow (e.g., "if Step 2 returns >10 [AUTHOR:] flags, surface them and pause for review").

## Logging
On completion, append entry to [[_CHANGELOG]] under the relevant lane.
```
