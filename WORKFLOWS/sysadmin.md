---
type: workflow
name: sysadmin
trigger: run the admin pass
aliases: [walk the sweep, admin pass, sysadmin, walk the maintenance, rule the sweep findings, work the sweep, rule the sheet, walk the sheet, rule the week's system sheet]
inputs: [SYSTEM/backlog-queue/_rulings/<sunday>-rulings.md — the supervisor's weekly rulings sheet, and nothing else; SYSTEM/reports/<sunday>-vault-briefing.md for context, never as a work list]
outputs: [ruled lines executed as safe ops, the walked sheet stamped and moved to SYSTEM/backlog-queue/_rulings/closed/, unruled lines left on it for the next Sunday's carry, brain-log entries per DIR-003]
lane: meta
status: draft
version: 2
last_updated: 2026-09-04
---

# WORKFLOW: sysadmin (the weekly sitting)

## When to use

CRE says **"run the admin pass"** / "rule the sheet" / "walk the sheet" / "work the sweep" — normally on a Monday, after Sunday's close-out has compiled the week's rulings sheet. It is CRE's **one system-facing sitting a week**: he walks `SYSTEM/backlog-queue/_rulings/<sunday>-rulings.md` and nothing else. Every line on it is already researched and in one-tap form; the sitting rules, the pass executes.

**This workflow is ATTENDED ONLY. It is never scheduled and never runs headless.** Since v2 (2026-09-04) the reason is narrower than it was: an unattended run *can* now rule the reversible auto-ratify class (DIR-012 clause 6, on CRE's word), and the supervisor's close-out does. What survives to this sitting is exactly what the class excludes — forks, priorities, graduations, cadences, prompt edits, desktop trips, anything touching `WRITING/`, `REFERENCE/`, a directive, a decision, or an anchor. Those are CRE's, and a scheduled version of this workflow would be auto-ruling them, which is the one thing the class is built not to do.

## The problem it solves — v1, then v2

**v1 (2026-08-03).** Five sweepers each deferred their judgment calls to a different surface. CRE had to remember to open five artifacts, on his own initiative, and work each one separately — so in practice he opened none of them and the findings aged silently. The failure was never information; it was initiation and dispersal. v1 fixed the dispersal by aggregating eight sources into one list, by hand, at the sitting.

**v2 (2026-09-04, CRE-ruled — [[TASKS/PROJECTS/vault-self-management]]).** v1 fixed the reading and left the ruling where it was: every judgment call still ended as a line he had to tap, including the ones the tree already answered, and once the supervisor's gate bin existed there were two attended channels for the same deferrals. v2 moves the aggregation, the research, and the reversible executions **upstream into the supervisor's evening close-out** (`WORKFLOWS/backlog-supervisor.md` § Intake, § The auto-ratify class, § The weekly sheet and the briefing). This pass keeps only the sitting. The list it walks is compiled, not aggregated here; it arrives on his board through the `every:mon` seed in `TASKS.md`, so it is served, never fetched.

## Core discipline

- **It walks the sheet and nothing else.** No other bin, report, ledger, or queue folder is opened as a work list. If a finding is missing from the sheet, that is a defect in the supervisor's intake table — file it as one line for the next sheet — not a gap to fill by opening the sweepers' reports here.
- **It does not re-run the sweeps and does not re-research.** DIR-011's research sits on the presenting pass, which is now the close-out. A line that arrives unresearched is sent back (*"unresearched — return to the supervisor"*), not researched at the sitting; that is how the sheet stays cheap.
- **Cleared, not capped** (CRE-ruled 2026-09-04: a cap creates a snowball). The v1 12-item cap and 20-minute box are **superseded**. The sheet is walked to zero; what CRE skips carries with its age onto next Sunday's sheet, and the briefing reports the length so he can see a bad week coming. If a week proves overwhelming, a cap is his to add later.
- **It writes only what CRE rules**, plus its own stamp on the sheet. It never rules on his behalf and never edits `_DIRECTIVES.md` — a graduation he ratifies here lands in a follow-up attended edit, reference doc first, slim entry same session.

## Input — the one surface

| Source | Surface | What it carries |
|---|---|---|
| `backlog-supervisor` close-out, Sunday | `SYSTEM/backlog-queue/_rulings/<YYYY-MM-DD>-rulings.md` | **1 Confirm in one tap** — tree-resolved lines, every auto-ratified action executed this week (*executed, reversible — spot check*, with path and undo), and every `(would auto-ratify)` line while the class is unarmed · **2 Rule** — the genuine calls, one at a time, each with a recommended default, the reason, the cost of deferring, and the research cited · **3 Desktop trips** — a checklist grouped by trip with the drafted body or command and a verification step · **4 Fiction, thin** — what a chapter or episode is owed, nothing proposed · **5 Carried** — last week's unruled lines with age |

The eight v1 sources — `backlog-sweep`'s two bins, `task-audit`, `link-audit`, `skills-sweep`, `vault-health`, the supervisor's own bin, the drift ledger — are all rows in the supervisor's § Intake table now. They keep writing where they write; the close-out reads them. **Not one of them is read here.**

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). Mismatch → halt and ask which folder is the vault (`^obs-004`).

### Step 1 — Find the sheet

Open `SYSTEM/backlog-queue/_rulings/` (host route or a pathed `Glob`, empty result confirmed by a direct `Read` of the folder's `README.md`). The sheet is the newest `<YYYY-MM-DD>-rulings.md` not yet in `closed/`. **No sheet** → the Sunday close-out did not compile one: check `SYSTEM/reports/backlog-supervisor-runs.md` for a `CLOSE-OUT` receipt dated Sunday (a receipt with no sheet is a supervisor defect; no receipt at all is a scheduler-silence finding — say which), and stop. **Never improvise a sheet from the sweepers' reports** — that is the v1 aggregation, and doing it here re-opens the second channel.

Read the briefing (`SYSTEM/reports/<sunday>-vault-briefing.md`) for context only. Its § Health line on receipts present / absent is the window-completeness report v1's Step 1 used to compute here.

### Step 2 — Walk the sheet, section by section

The sheet's own order is the sitting's order:

1. **Confirm in one tap** — read the count, scan the list, one word closes the block. Each *executed, reversible — spot check* line names the path and the undo; a spot check is CRE's eye on one or two of them, never a re-verification of all. A line he does not accept is ruled individually and its undo executed in Step 3.
2. **Rule** — one at a time. Each line already carries a recommended default, so *"yes"* is a valid full ruling; *"no"*, *"B"*, or a short question is the ruling too (a short question is the ruling, not an opening — check the premise it points at). A fork routes to `decision-helper` with the evidence attached unless he rules it inline.
3. **Desktop trips** — a checklist he executes at the desk, in the order that shares a trip. This pass records what he reports done and re-probes each trip's verification step by direct read (an installed skill's frontmatter, a task's `lastRunAt`, a carve's size stamp) — never off his claim alone, never off the sheet's.
4. **Fiction, thin** — read, not worked. The morning lane is his; this sitting does not schedule it.
5. **Carried** — same as Rule, with age. At three weeks the line proposes drop-or-his-forever; either is a valid ruling.

### Step 3 — Execute the rulings

Apply exactly what CRE ruled, nothing adjacent. File tools only; verify each write by re-reading through the file tools (DIR-005). For anything that touches a scheduled task, read the live `SKILL.md` to EOF via the host route first, then `update_scheduled_task` **body-only** (`^obs-138`, `^obs-249`) and re-read to confirm — the drafted body the sheet links is a draft, not a template to paste blind. Anything ruled but desktop-only that he does not do at the sitting stays on the sheet's desktop section for next week, not as a new `_BACKLOG` item.

**If a ruling changes a workflow, honour DIR-016**: the canon doc, the live task prompt, any deterministic code, and any poll/early-exit gate all get edited and **re-read in this same session**. A route updated on two surfaces of four is the most expensive failure shape available here, because the record then says it works. A graduation he ratifies lands reference-doc first, slim entry same session, heading compare identical.

### Step 4 — Stamp and close the sheet

Stamp each line with its ruling and the date; stamp the sheet's frontmatter `walked: <date>`; move it to `SYSTEM/backlog-queue/_rulings/closed/`. Unruled lines stay on it as written — the next Sunday close-out reads `closed/` for carries, re-probes each against its own condition, and re-emits the survivors with age. **No separate admin-pass receipt file** (v1's `SYSTEM/reports/<date>-admin-pass.md` is retired): the stamped sheet *is* the receipt, and the briefing reports the counts.

### Step 5 — Log (DIR-003)

`_CHANGELOG.md` top-insert (meta lane): sheet date, counts per section confirmed / ruled / executed / carried, notable rulings. New fragility → `_OBSERVATIONS.md` with a `^obs-NNN` anchor — **re-scan for the highest anchor immediately before writing and re-read the heading afterward** to confirm no duplicate (`^obs-236`; Obsidian resolves a duplicate to the *first* match, so every later citation silently points at the wrong entry). Follow-ups → `_BACKLOG.md`.

## Stop conditions

- Sentinel fails → halt.
- **No sheet in `_rulings/`** → do not improvise one. Report which of the two failures it is (close-out receipt present / absent), and stop.
- **A line arrives unresearched** (no default, no cited research, a flag he would have to look into) → do not research it here. Mark it *"returned — unresearched"* on the sheet; the next close-out re-presents it researched or drops it. DIR-011 sits on the presenting pass.
- **A line asks this sitting to write `WRITING/`, `REFERENCE/`, a chapter folder, or CRE's prose** → the sheet may name what a chapter is owed; the sitting never does the fiction. Route to the morning lane in his words, or leave it.
- **The sheet is long** → walk it anyway. Cleared, not capped. If it cannot be cleared, the carry section says so with ages and the briefing shows the trend; a cap is CRE's to add.

## Boundaries — what this is NOT

- **Not `dispatch`.** "Dispatch" reads `_BACKLOG` and proposes top items on demand; this walks the week's rulings sheet.
- **Not the supervisor.** It never aggregates, never researches, never routes a finding, never compiles the sheet. If it finds itself opening a sweeper's report, it has left its lane.
- **Not a sweeper.** It never re-derives counts, re-runs a linter, or re-scans for links.
- **Not `day-launch`.** It does not build a board or arm accountability.
- **Not a decision-helper session.** A fork routes to `decision-helper` with its evidence attached unless CRE rules it inline; it is not deliberated here.
- **Not scheduled, ever.** What reaches this sheet is by definition what the auto-ratify class excludes.

## Packaging

Source lives at `WORKFLOWS/skills-src/sysadmin/` when packed. Per DIR-009: author the source via the file tools → pack on the **desktop** with `pack-skills.ps1` → sha-verify the packaged `SKILL.md` against source → Save-skill. Never package from the sandbox mount (`^obs-156`). Runs from the trigger index until packaged.
