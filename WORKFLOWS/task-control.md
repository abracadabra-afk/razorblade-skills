---
type: workflow
lane: meta / os
status: active
created: 2026-06-15
purpose: Pause/resume scheduled tasks from chat, without opening Cowork's schedule section.
triggers: ["task status", "what's running", "pause the pollers", "resume the pollers", "pause all tasks", "resume the operational tasks"]
---

# task-control

Chat-driven pause/resume for the scheduled tasks. CRE wanted a one-place way to stop the frequent intake pollers (and other recurring tasks) when the pipeline is empty, without entering Cowork's schedule UI.

> **Why not an artifact?** A dashboard artifact was attempted (2026-06-15) and failed: the artifact sandbox's `window.cowork.callMcpTool` only reaches **connector** MCP servers, not the **system** `scheduled-tasks` server — every call returned `400` even though the tool was allowlisted. The only scheduled-task capability exposed to artifacts is `runScheduledTask(taskId)` (run, not list/pause). So control lives in chat, where the agent can call the scheduled-tasks MCP directly. (`^obs-088`.)

## Mechanic

The agent uses two MCP tools:
- `mcp__scheduled-tasks__list_scheduled_tasks` — read current state (`enabled`, `cronExpression`, `schedule`, `lastRunAt`, `nextRunAt`).
- `mcp__scheduled-tasks__update_scheduled_task` with `{ taskId, enabled }` — flip a task. `enabled: false` pauses automatic runs (manual runs still work); `enabled: true` resumes.

Always `list` first to get current state and exact `taskId`s; never assume the roster. Derive a task's **frequency group** from its cron rather than a hardcoded list:
- minute field has `/` or `,` and hour is `*` → **frequent poller (sub-hourly)**
- hour is `*` → **hourly**
- a day-of-week is set → **weekly**
- otherwise → **daily**
- no cron → **manual only** (nothing to pause)

## Triggers → action

| CRE says | Action |
|---|---|
| "task status" / "what's running" / "which tasks are running" | `list`; report all tasks grouped by frequency with running/paused + last/next run. Read-only. |
| "pause the pollers" / "pause the intake pollers" | Disable the **frequent pollers**: `dictation-runner`, `file-inbox-runner`. |
| "resume the pollers" | Enable `dictation-runner`, `file-inbox-runner`. |
| "pause all tasks" / "pause everything" | Disable every currently-`enabled` recurring task (skip manual-only). Report what was paused. |
| "resume the operational tasks" / "resume everything" | Enable the **operational set** (below). **Gated:** do NOT auto-enable any task whose `lastRunAt` is >7 days ago or null — list those and ask before enabling, so parked/legacy tasks don't get silently revived. |

## Operational set (current — verify live each run)

The tasks that are part of the live system and are safe to resume as a group:
- **Intake pollers (sub-hourly):** `dictation-runner`, `file-inbox-runner`
- **Hourly:** `vault-backlog-agent`
- **Daily:** `books-daily-ingest-weave` (7am), `research-runner` (7:45am)
- **Weekly (Mon):** `skills-sweep`, `backlog-sweep`, `vault-health`

**On-demand pipeline (currently off; enable deliberately during a drafting/ingest push, not via "resume everything"):** `witchwood-pipeline-advance`, `ghost-river-ingest`.

**Parked / legacy — leave OFF (the >7-day-dormant guard catches these):** `router` (Inkwell, parked), `daily-thinker`, `weekly-thinker`, `daily-catchup-auditor`, `auditor-subsystem-rotation`, `skillmd-protocol-drift-check`.

**Manual-only (no schedule to pause):** `pm-session`, `mount-the-vault`.

## Safety

- **Pausing is always safe** and reversible — it only stops automatic dispatch; a paused task can still be run manually and resumed later.
- **Resuming is gated** by the >7-day-dormant rule above to avoid reviving dead tasks.
- Never `create`/`delete` a task under these triggers — only flip `enabled`.
- A static reference card listing these phrases also lives as the Cowork artifact `scheduled-task-control` (no live data — chat is the control surface).
