---
type: workflow
name: sysadmin
trigger: run the admin pass
aliases: [walk the sweep, admin pass, sysadmin, walk the maintenance, rule the sweep findings, work the sweep]
inputs: [_BACKLOG.md § Standing queue, _BACKLOG.md § Needs CRE ruling bin, SYSTEM/reports/<date>-task-audit.md, SYSTEM/reports/<date>-link-audit.md, SYSTEM/reports/<date>-skills-sweep.md, SYSTEM/reports/brain-doc-sizes.json]
outputs: [ruled findings executed as safe ops, a carried-forward unruled list stamped with age, a dated SYSTEM/reports/<date>-admin-pass.md receipt, brain-log entries per DIR-003]
lane: meta
status: draft
last_updated: 2026-08-03
---

# WORKFLOW: sysadmin (the admin pass)

## When to use

CRE says **"run the admin pass"** / "walk the sweep" / "work the sweep" / "rule the sweep findings" — normally on a Monday, after Sunday's maintenance window has run. It is the **attended consumer** of everything the window deferred: one session, one bounded list, every open ruling in one place.

**This workflow is ATTENDED ONLY. It is never scheduled and never runs headless.** That is the entire point of it. The five sweepers are unattended and therefore constitutionally unable to rule anything (DIR-012 clause 1); every judgment call they hit gets deferred. This is where those deferrals get answered. A scheduled version of this workflow would be a contradiction — it would be auto-ruling, which is the one thing the window is built not to do.

## The problem it solves

Five sweepers each defer their judgment calls to a different surface. CRE had to remember to open five artifacts, on his own initiative, and work each one separately — so in practice he opened none of them and the findings aged silently. **The failure was never information; it was initiation and dispersal.** This pass fixes the dispersal (one list) and `backlog-sweep`'s Step 4c seed fixes the initiation (the list arrives on his board).

## Core discipline

- **It does not re-run the sweeps.** It reads what they already wrote. If a finding is missing, that is a window defect to report, not a gap to fill by re-deriving.
- **DIR-011 is load-bearing here, not decorative.** *Every* finding is researched against the tree **before** it reaches CRE. A finding the vault decisively answers is resolved and presented as a one-tap confirmation — never as an open question. A flag CRE has to research himself is a flag that cost him the thing this vault exists to protect.
- **Bounded.** Hard cap: **12 items** surfaced per pass, plus the batch-ratify block (which is one decision, not twelve). Overflow carries forward, ranked. An unbounded list is one CRE will not work — the same finding that bounds `backlog-sweep`'s Step 4b at 5 directives and `day-launch`'s board at 7.
- **Time-boxed.** Target 20 minutes. If the surfaced list cannot be worked in one sitting, the cap was wrong — reduce it next pass and say so.
- **It writes only what CRE rules**, plus its own receipt. It never rules on his behalf and never edits `_DIRECTIVES.md`.

## Inputs — where the window's findings already live

**No shared report schema exists and none is needed.** Each sweeper already writes to a known surface; this pass aggregates from those. Read all eight:

| Source | Surface | What it carries |
|---|---|---|
| `backlog-sweep` | `_BACKLOG.md` § **Standing queue** | lane counts · the ranked 3 attended picks · the `vault-backlog-agent` toggle recommendation |
| `backlog-sweep` | `_BACKLOG.md` § **Needs CRE ruling** bin | consolidations, stale-item drops, re-prioritizations, compressions, partial derive-closures, up to 5 observation-graduation proposals |
| `task-audit` | `SYSTEM/reports/<date>-task-audit.md` | prompt-vs-doc drift punch list, doc-deferral recommendations |
| `link-audit` | `SYSTEM/reports/<date>-link-audit.md` | dangling refs, broken anchors, duplicate-anchor findings |
| `skills-sweep` | `SYSTEM/reports/<date>-skills-sweep.md` | install queue, repackage handoff, STALE/SOURCE-AHEAD rows |
| `vault-health` | `_BACKLOG.md` items + `SYSTEM/reports/brain-doc-sizes.json` | rotation bands, desktop carve handoffs |
| `backlog-supervisor` | `_BACKLOG.md` § **Needs CRE ruling (backlog-supervisor …)** bin | items ruled ATTENDED with the research already done, escalations after two failed fix rounds (both logs named by path), and already-addressed close proposals. Deliberately the same bin surface as its siblings rather than a parallel channel — DIR-012 cl. 4–5. Run receipts (incl. stand-downs) at `SYSTEM/reports/backlog-supervisor-runs.md` and `-agent-runs.md`. (Eighth source, added 2026-09-04.) |
| any session (DIR-019 §4 scope lock) | `SYSTEM/drift-ledger.md` § OPEN | out-of-scope staleness noticed mid-task and parked silently — default bin **BATCH-RATIFY** (retire/stamp per DIR-019 §1–2); only a line touching channel/project *law* goes to RULE. Move ruled lines to § CLOSED. (Seventh source, added 2026-09-01.) |

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). Mismatch → halt and ask which folder is the vault (`^obs-004`).

### Step 1 — Window freshness gate (run this before reading anything else)

Establish **which window you are working** and whether it completed. `list_scheduled_tasks` and check each sweeper's `lastRunAt` against the expected Sunday slot:

`skills-sweep` 13:05 → `task-audit` 13:53 → `backlog-sweep` 14:38 → `vault-health` 15:39 → `link-audit` 16:21

Then confirm each expected artifact exists **by direct `Read`/`Grep`, never `Glob`** — a `Glob` miss is not evidence of absence (`^obs-198`, DIR-005). Report, in visible prose:

- **which sweepers ran**, and which did not;
- **any artifact a sweeper should have written and did not** — that is a live defect, surface it as its own finding;
- if `vault-health` did not run, note that `link-audit`'s findings are **provisional** (it audits post-rotation state by design).

**Do not proceed silently past a partial window.** A pass that walks four of five sweepers and says nothing teaches CRE the list is complete when it is not.

### Step 2 — Aggregate + de-duplicate

Pull every open finding from the eight sources into one list. Then **collapse duplicates across sweepers** — the same underlying defect routinely surfaces in two reports (a renamed workflow doc shows up as `task-audit` `BROKEN-REF` *and* `link-audit` `DANGLING`; a carved brain doc shows up in `vault-health` *and* as broken anchors). One defect, one line, both sources cited. Counting it twice inflates the list and burns the budget the cap is protecting.

Carry forward any unruled items from the previous pass's receipt, **stamped with age** (`carried 2 passes`). Nothing vanishes by being skipped.

### Step 3 — Research every finding against the tree (DIR-011)

**This is the step that makes the pass worth running.** For each finding, attempt resolution *before* it reaches CRE:

- **Tree-answered** → resolve it, cite the evidence, and present as *"resolved against [[X]] — confirm"*. One tap. Not a question.
- **Tree-silent** → it survives as a genuine ruling.
- **Phantom** → the finding is wrong. Say so plainly, name the mechanism, and do not surface it as work. The commonest cause is a stale-mount or enumeration artifact (`^obs-183`, `^obs-198`): a dangling-link flag whose target a direct `Read` finds present; a `DRIFT-EXACT` computed off a stale partial; a "missing" report the mount could not enumerate. **Confirm every negative through the file tools before it reaches him** — a false flag reported and retracted one turn later has happened here before, and it is corrosive: it teaches CRE to distrust the gate.

Check every proposed drop/cancel against `_OBSERVATIONS.md`, `_SKILLS MAP.md`, `DECISIONS/`, and the filesystem before presenting it as stale.

### Step 4 — Bin, then present

Three bins, presented in this order:

1. **BATCH-RATIFY** — mechanical, reversible, no author intent at stake: formatting normalizations, tree-answered resolutions, stale-pointer syncs, `PARKED`/`NOT A RULE` stamps already applied, doc-deferral collapses with no behavior change. **One decision for the whole block.** Show the count and a scannable list; do not walk them individually.
2. **RULE** — genuine judgment calls, **one at a time**, each as: the finding · the proposed action · the one-clause reason · what it costs to defer. Never more than the cap. This bin includes the observation-graduation proposals (which land in `_DIRECTIVES` only on CRE's word, in a follow-up attended edit — never here, never automatically).
3. **PARK** — surfaced for awareness, no action asked. Desktop-gated items CRE cannot action from this seat, `#blocked`/`#waiting` items, provisional findings from an incomplete window.

Lead with the **Standing queue serving** — the 3 ranked attended backlog picks and the agent-toggle recommendation — because that is the answer to *"what should I actually work on,"* and it should not be buried under maintenance noise.

### Step 5 — Execute the rulings

Apply exactly what CRE ruled, nothing adjacent. File tools only; verify each write by re-reading through the file tools (DIR-005). For anything that touches a scheduled task, use `update_scheduled_task` **body-only** (`^obs-138`) and re-read the host `SKILL.md` to confirm. Anything ruled but desktop-only (pack/Save/install, a `_CHANGELOG` carve) becomes a `#desktop` `_BACKLOG` item with its next action written out — never attempted from the sandbox (DIR-007).

**If a ruling changes a workflow, honour DIR-016**: the canon doc, the live task prompt, any deterministic code, and any poll/early-exit gate all get edited and **re-read in this same session**. A route updated on two surfaces of four is the most expensive failure shape available here, because the record then says it works.

### Step 6 — Receipt + carry-forward

Write `SYSTEM/reports/<YYYY-MM-DD>-admin-pass.md`: what was ratified, what was ruled and executed, what was parked, and **the unruled carry-forward list with age stamps**. This is the next pass's input — it is the mechanism by which a skipped item survives instead of aging out silently.

### Step 7 — Log (DIR-003)

`_CHANGELOG.md` top-insert (meta lane): window completeness, counts per bin, notable rulings. New fragility → `_OBSERVATIONS.md` with a `^obs-NNN` anchor — **re-scan for the highest anchor immediately before writing and re-read the heading afterward** to confirm no duplicate (`^obs-236`; Obsidian resolves a duplicate to the *first* match, so every later citation silently points at the wrong entry). Follow-ups → `_BACKLOG.md`.

## Stop conditions

- Sentinel fails → halt.
- **No window artifacts found at all** → do not improvise a maintenance pass. Report that the window did not run, check whether the app was closed across Sunday (scheduled tasks run on next launch), and stop.
- **Surfaced list would exceed the cap even after de-duplication** → present the capped list, state the overflow count plainly, and recommend a dedicated working session rather than silently truncating. Mirrors `backlog-sweep`'s ⅓-of-items stop condition.

## Boundaries — what this is NOT

- **Not `dispatch`.** "Dispatch" reads `_BACKLOG` and proposes top items on demand; this walks a specific window's deferred findings on a cadence. They overlap only at the Standing queue serving, which this pass *reads* rather than recomputes.
- **Not a sweeper.** It never re-derives counts, re-runs a linter, or re-scans for links.
- **Not `day-launch`.** It does not build a board or arm accountability; it hands `day-launch` better-ranked input.
- **Not a decision-helper session.** A finding that turns out to be a genuine architecture fork routes to `decision-helper` with its evidence attached, and comes back as a ruling — it does not get settled inline under a 20-minute clock.

## Packaging

Source lives at `WORKFLOWS/skills-src/sysadmin/` when packed. Per DIR-009: author the source via the file tools → pack on the **desktop** with `pack-skills.ps1` → sha-verify the packaged `SKILL.md` against source → Save-skill. Never package from the sandbox mount (`^obs-156`). Runs from the trigger index until packaged.
