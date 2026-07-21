---
type: workflow
name: project-plan
trigger: plan the project
aliases: [break down this project, chunk this project, plan this out, replan the project, close the project]
inputs: [TASKS/PORTFOLIO.md, TASKS/PROJECTS/*.md, DECISIONS/, _BACKLOG.md, the project's own domain folder, TASKS/TODAY.md receipts]
outputs: [TASKS/PROJECTS/<slug>.md, chunks seeded into TASKS/TASKS.md, the project's Next milestone slot in PORTFOLIO.md]
lane: life
status: draft
created: 2026-07-20
last_updated: 2026-07-20
---

# WORKFLOW: project-plan

## When to use

CRE names a goal, or points at a project already in [[TASKS/PORTFOLIO]], and wants it turned into a runway. This is the **project layer** — the rung between PORTFOLIO (quarterly: which projects matter) and week-shape (weekly: what this week is).

Founding bug: every `**Next milestone:**` slot in `PORTFOLIO.md` sat empty from its 2026-07-11 ratify while `week-shape` Step 2 was instructed to read "the real next milestone, not a guess." Same shape as the zero-candidate `TODAY.md` that founded week-shape — a layer reaching down for input no layer above it produced.

Design: [[SYSTEM/reports/2026-07-20-project-layer-proposal]] (ratified 2026-07-20). Convention: [[TASKS/PROJECT-SCHEMA]]. Read-side sibling: `project-pulse` (velocity + slippage; unbuilt, deliberately deferred).

**Scope: ops and life lanes only.** Fiction keeps `brief → runway → beats` ([[WORKFLOWS/pipeline]]). See PROJECT-SCHEMA § Scope.

## Modes

| Mode | Trigger | What it does |
|---|---|---|
| **create** (default) | "plan the project X" | new plan file from scratch |
| **replan** | "replan X" | re-cut milestones/targets on an existing plan; appends to its Replan log |
| **close** | "close out X" | retro → `landed` or `abandoned`; both are valid outcomes |

Replan and close are modes, not separate skills — deliberately (Pattern #3: a suite of instruments is planning-as-procrastination with a build queue attached).

## Design intent (the pattern map is the spec)

- **Pattern #3 (planning-as-procrastination) is the primary threat, and a project planner is its ideal habitat.** Governing rule: **cheap to make, expensive to elaborate.** 20-minute cap. One screen at the gate. **Only the current milestone gets chunked.**
- **Pattern #8 (working memory):** the project lives in a file, never in CRE's head.
- **Pattern #2 (abandonment):** `abandoned` is a logged, valid outcome. No streaks, no guilt.
- **Top-down thinking ([[_ME]]):** CRE sees the goal; this produces the steps. Lead with the proposed spine, then the chunks.
- **DIR-015:** executional lane only. If a project is stalled for affective reasons, **name it once and stop** — do not work it, and do not turn the plan into a pep talk.

## Position & guards

- **Gate pattern:** proposes, CRE rules. Nothing is written until his one-pass ratify.
- **Vault sentinel** (`^obs-004`) before any write; **file tools only**, verify by re-read (DIR-005).
- **Never invents a project or its rank** — projects and priority order are PORTFOLIO's, i.e. CRE's. A plan for a project not in PORTFOLIO is proposed *with* a PORTFOLIO addition, both gated.
- **Never chunks fiction work** and never writes into a chapter folder.
- **Never pushes to Odysseus** (CRE-ruled 2026-07-20 — `day-launch` keeps sole ownership of the accountability layer).
- **Never creates calendar events** — events are CalDAV's (dec-007); the router is the sole write-path into a connector.

## Steps

1. **Prior-ruling check — first, always.** Sweep `DECISIONS/`, `PORTFOLIO.md`, `_BACKLOG`, and the project's own domain folder before proposing anything (DIR-010's vault-content corollary). If the thing is already ruled, already planned, or already scoped, **lead with that** — *"you ruled this on <date>; here is what you ruled"* — and re-open only if CRE says it's stale. `"I've been meaning to do this for ages"` is a retrieval trigger, not a planning trigger.

2. **Elicit `done looks like` — one falsifiable sentence, CRE's words.** If he can't state it, **the project isn't ready to plan.** Say so plainly and stop; that's a `decision-helper` run or a dev session, not a planning failure. Do not paper over a fuzzy goal with a tidy milestone list.

3. **Propose the spine — 3–7 milestones, each with a receipt.** Derived from vault material (project backlogs, BUSINESS/LIFE docs, `_BACKLOG` anchors, existing notes), never invented. **Every milestone names the artifact that proves it** (PROJECT-SCHEMA R2). If a milestone's receipt can't be named, the milestone is wrong — re-cut it before showing it.

4. **Chunk milestone 1 only.** Each chunk: one work session in the project's `win:` window, with a **physical first action** ("open Substack, type three candidate names" — not "decide on branding"). Stamp `chunk:<ID>` and any `needs:<ID>`. A chunk that needs two sessions is two chunks. Later milestones stay one-line.

5. **Reality check — before the gate, not after.** Run the velocity model against the proposed target: chunks remaining ÷ recent per-lane rate from `chunk:` receipts in `TODAY.md`. State the result **at the gate**, in the number. If history is thin (< ~3–4 weeks of chunk receipts), say **"insufficient history to project"** and do not manufacture a date — DIR-013 clause 2. **Never ship a plan the model calls fiction and stay quiet about it.** Report flatly: *"target 09-15, derived 10-12, gap +27d."* No commentary on CRE (DIR-015 clause 5).

6. **Gate.** One screen, one pass. CRE edits, ratifies, or kills it.

7. **Write.** `TASKS/PROJECTS/<slug>.md` per PROJECT-SCHEMA (frontmatter serialized, DIR-004) → seed milestone 1's chunks into `TASKS.md` under `## Active`, schema-tagged and source-stamped `<!-- project-plan YYYY-MM-DD -->` → fill that project's `**Next milestone:**` slot in `PORTFOLIO.md` from milestone 1. **Verify each by re-read.**

8. **Stop.** No week planning (week-shape's), no day serving (day-launch's), no notifications, no backlog dispatch.

## Replan mode

Same steps, but Step 1 reads the existing plan and Step 3 proposes a **diff**, not a fresh spine — what moves, what's cut, what the new target is. Append one line to the Replan log with the reason. **A replan is normal maintenance, not a failure** — say it that way.

The common trigger is a `project-pulse` slippage flag. `project-pulse` never re-cuts a plan itself; it hands CRE the gap and he decides whether to replan, move the target, or cut scope.

## Close mode

1. Confirm the `done looks like` receipt exists (or that CRE is killing it).
2. **One retro question, not a form:** what made this take the time it took? Log the answer in the Replan log.
3. Set `status: landed` or `abandoned`, close remaining chunks in `TASKS.md`, clear the PORTFOLIO milestone slot.
4. If the retro surfaced a *system* finding (not a project one), it goes to `_OBSERVATIONS`, not into the plan file.

## What this workflow never does

- Chunk more than the current milestone, or run longer than 20 minutes
- Plan fiction work, or write into a chapter folder
- Set or reorder PORTFOLIO priority (CRE + decision-helper only)
- Push notifications, create calendar events, or dispatch the backlog
- Estimate effort, compute percent-complete, or draw a chart
- Ship a plan whose own velocity check says it doesn't fit, without saying so at the gate
- Comment on CRE's performance. Receipts are numbers (DIR-015 clause 5)

<!-- v1 authored 2026-07-20 per ^backlog-project-layer (proposal ratified same day; absorbs ^backlog-project-breaker-helper). project-pulse deferred by design until chunk receipts accumulate. Packaging into .skill: desktop pack-skills.ps1, pending (DIR-009). -->
