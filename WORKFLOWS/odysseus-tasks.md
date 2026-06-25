---
type: workflow
name: odysseus-tasks
trigger: push my reminders
aliases: [sync tasks to odysseus, send this to odysseus, push tasks to odysseus, sync my reminders, push the reminders, reminder bridge]
inputs: [time-bearing open tasks in TASKS/TASKS.md (a date/time or "remind me")]
outputs: [Odysseus todos with a due_date that fire a notification, the source vault line stamped with `<!-- ody: <id> -->` (+ open_url), a short run report]
lane: os
status: active
last_updated: 2026-06-25
---

# WORKFLOW: odysseus-tasks

## When to use
CRE has **time-bearing** to-dos in [[TASKS/TASKS|Tasks]] — anything that should *fire a reminder* ("call the dentist Tuesday 5pm", "AC filters next week"). Markdown can't notify; Odysseus can (ntfy / email / browser via its todo `due_date`). Triggers: **"push my reminders"**, "sync tasks to odysseus", or — for a single item CRE just dictated — **"send this to odysseus"**. This is the push leg of the **Obsidian ↔ Odysseus bridge**: the vault is where CRE *authors*; Odysseus is where a dated task becomes *operational*.

This is the **Tasks & Reminders** flow of the broader integration. See [[SYSTEM/odysseus-bridge]] for the full architecture (the other flows — capture→INBOX, RAG-over-vault — are separate increments).

## Core discipline
- **For a time-bearing task, Odysseus is the source of truth; the vault derives.** Once pushed, the vault line carries an `<!-- ody: <id> -->` stamp and is thereafter a *pointer* to the canonical Odysseus todo — the same "external system is source of truth, the vault derives" rule as `canon-sync`/`storyline-sync`, extended to this connector ([[_VAULT MAP]] connector discipline).
- **Dateless to-dos stay vault-only.** A passive "buy paint" with no time has nothing to fire — leave it in Tasks untouched. Only items with a real time signal cross the boundary. Don't inflate the operational layer with things that don't need to notify.
- **Idempotent via the stamp.** An item already carrying `<!-- ody: … -->` is skipped — never double-create. Piggybacks on the vault's existing trailing-comment provenance convention (`<!-- research-runner … -->`).
- **Push-only in v1.** No two-way completion (checking off in Odysseus → ticking the vault) and no calendar-events yet — those are increments (see Non-goals). v1 does one thing well.
- **Creating reminders is an outward action → attended by default.** Show CRE the batch + the *parsed* due times and get a go before creating real notifications. Flip to unattended only when CRE says so.
- **Guards:** vault sentinel before any write (`^obs-004`); file-tool edits to `TASKS.md` + verify by re-reading through the file tools, never `patch_vault_file`/whole-file MCP rewrite (DIR-005 / `^obs-020` / `^obs-014`); never put a secret in a todo title (DIR-001).

## Prerequisites
- The Odysseus Claude Agent skill is installed (`~/.claude/skills/odysseus/`) and `ODYSSEUS_URL` + `ODYSSEUS_API_TOKEN` are in the environment. **Non-interactive Bash does not source `~/.bashrc`** — `export` both inline before calling the helper. See [[SYSTEM/odysseus-bridge]].
- The token has `todos:write` enabled (verify via `odysseus_api.py capabilities`). If not, stop and tell CRE to enable the toggle in Odysseus → Settings → Integrations → Claude Agent; do not work around a `403`.

## Modes
- **Batch (default — "push my reminders").** Scan all of `TASKS/TASKS.md`, collect every eligible (time-bearing, unstamped) open item, present the batch, push on confirm.
- **Single ("send this to odysseus").** CRE points at one task (just-dictated or named); push only that one. If it isn't in Tasks yet, add it under ⚡ Inbox first so the vault stays the authoring surface, then push.
- **Scheduled (future).** A poller could run Batch unattended once trusted — deferred until v1 is proven and CRE opts in (it creates outward notifications, so it stays gated until then).

## Detection (what counts as time-bearing)
An open `- [ ]` line in [[TASKS/TASKS]] (any section) is eligible when it carries a **time signal** AND is **not already stamped** `<!-- ody: … -->`:
- an explicit date (`2026-07-01`, `Jul 1`, `7/1`), a weekday (`Tuesday`), a clock time (`5pm`, `17:00`),
- a relative phrase (`tomorrow`, `next week`, `in 2 hours`, `Friday morning`),
- or an explicit cue (`remind me …`, a `due:` token).

Pass the time phrase **verbatim** as the todo `due_date` — Odysseus's backend parses natural language ("tomorrow 5pm", "next Monday 9am") and anchors to CRE's timezone. Do **not** pre-parse it into an ISO string yourself; let the backend own the parse so it matches what the UI would do.

When the time signal is ambiguous (e.g. "soon", "this week" with no day), do **not** guess a datetime — surface it in the batch as `<<NEEDS A TIME>>` and let CRE supply one or skip.

## Steps

### Step 1 — Sentinel + capability check
Verify `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`) — the `^obs-004` vault sentinel. Then `export` the Odysseus env vars inline and run `odysseus_api.py capabilities`; confirm `todos.write: true`. Missing env or no scope → stop with the fix, don't proceed.

### Step 2 — Collect eligible items
Read `TASKS/TASKS.md` via the file tools. Walk every open `- [ ]` line; keep those that match **Detection** and lack an `<!-- ody: … -->` stamp. Record each item's exact line text + the section it's in (so the write-back in Step 4 is surgical).

### Step 3 — Present the batch (gate)
Show CRE a compact table: task title · the time phrase that will be sent as `due_date` · which section it's from. Flag `<<NEEDS A TIME>>` items. Await CRE's go (he can drop or edit any). In **Single** mode with an unambiguous item, a one-line confirm is enough.

### Step 4 — Push + stamp back
For each confirmed item:
1. `POST /api/codex/todos` with `{"action":"add","title":"<task text, time phrase stripped from the title if it reads cleaner>","due_date":"<verbatim time phrase>"}` via the helper's generic POST form (the `todos add TITLE` shortcut can't set `due_date`).
2. Capture the returned `note_id` (short id) + `open_url`.
3. **File-tool Edit** the matching `TASKS.md` line: append ` <!-- ody: <short-id> -->` (and, optionally, the `open_url` as a trailing pointer). Keep the task text and checkbox as-is — the line is now a derived pointer, not a deletion.
4. Re-read `TASKS.md` through the file tools to verify the stamp landed (`^obs-014` — never trust a bash/mount read here).

### Step 5 — Report
Return a tight summary: N reminders created, each with its title, the due time Odysseus parsed, and its Odysseus link; any `<<NEEDS A TIME>>` items left for CRE; any `403`/scope problems. No noisy logging on a no-op (nothing eligible → say so in one line and stop).

## Non-goals (tracked as increments)
- **Two-way completion** — completing/deleting a todo in Odysseus reflecting back into the vault line. Needs a pull + reconcile leg.
- **Calendar events** — time *ranges* / meetings → Odysseus calendar (`/api/codex/calendar/events`) instead of a todo. v1 is todos/reminders only. (Per the skill's own rule: a bare "remind me + time" is a TODO with `due_date`, NOT a calendar event.)
- **Scheduled unattended push** — a poller running Batch on a cron, once CRE trusts the gate enough to drop it.
- **`.skill` packaging** — currently a workflow doc run by trigger; package once v1 is proven.

<!-- v1 authored 2026-06-25 as the first flow of the Obsidian↔Odysseus bridge. Push-only, attended. -->
