---
type: workflow
name: week-shape
trigger: shape the week
aliases: [plan the week, week shape, run the week shape, what's this week]
inputs: [TASKS/PORTFOLIO.md, TASKS/TASKS.md open items, TASKS/TODAY.md receipts roll, project backlogs of the resident story + ops lane]
outputs: [TASKS/TASKS.md seeded with the week's items, a ratified week header block in TASKS/TASKS.md]
lane: life
status: draft
last_updated: 2026-07-11
---

# WORKFLOW: week-shape

## When to use

Sunday evening or Monday morning in the medicated window, weekly. CRE says **"shape the week"** → the helper reads [[TASKS/PORTFOLIO]] + open [[TASKS/TASKS]] items + the receipts roll, proposes the week in one screen, CRE ratifies in one pass, and the week's concrete items land in `TASKS.md` — so `day-launch` never wakes to an empty candidate pool again (the 2026-07-11 zero-candidate morning is the founding bug).

This is the middle layer of the productivity spine ([[SYSTEM/reports/2026-07-11-productivity-spine-proposal]], ratified 2026-07-11): PORTFOLIO decides quarterly → **week-shape decides weekly** → day-launch executes daily. Every decision is made at the highest, least-frequent layer possible.

## Design intent (the pattern map is the spec)

- **Pattern #3 (planning-as-procrastination): HARD CAP 15 MINUTES.** This is a menu CRE approves, not a plan he builds. One proposal screen, one pass. If the run wants a second round of refinement, it's over-engineering — ship the menu.
- **Pattern #8 (working memory):** the week lives in `TASKS.md`, never in his head.
- **Pattern #4 / interest-drift:** the proposal *derives* from the portfolio's ratified priority order — it never re-opens the value fight. If CRE wants a different order, that's a portfolio edit or a decision-helper run, flagged, not silently absorbed.
- **Pattern #2 (abandonment):** restart-friendly. A skipped week costs nothing; the next run just reads a longer receipts gap and proposes normally. No streaks.
- **Pattern #19 (validation):** the proposal OPENS with last week's roll-up — receipts first, plans second.

## Position & guards

- **Gate pattern:** proposes, CRE rules. Nothing writes to `TASKS.md` until his one-pass ratify.
- **Vault sentinel** (`^obs-004`) before any write; **file tools only**, verify by re-read (DIR-005).
- **Never invents projects or priorities** — everything derives from `PORTFOLIO.md` (ratified) + existing backlogs. If the portfolio is `status: proposed`, halt and ask for the ratify first.
- **Never schedules the content of CRE's fiction** — "morning block: Witchwood" is an item; the prose is his.
- **Residency is read-only here.** If the resident story looks finished/blocked, week-shape *flags* a residency question for decision-helper — it never switches residency itself (R1).

## Steps

1. **Receipts roll-up (the validation open) — derive first.** Before rolling up, reconcile last week's seeds against ground truth (the day-launch v2.1 derive-pass evidence sources: project artifacts → `_CHANGELOG` → backlogs → ledger) — anything completed out-of-band gets checked with a `<!-- derived: … -->` stamp, and off-list work lands in the roll-up as its own line. CRE never reports completions; the artifacts do. Then: one honest paragraph — beats/sequences dictated, chapters landed, posts shipped, X/Y day-plan average. Zero weeks get one neutral line.
2. **Read the strategy.** `PORTFOLIO.md`: resident story, ops-lane flagship, priority order, energy map. Read the resident story's backlog + pipeline state for what's actually next (the real next milestone, not a guess). **Also sweep the build queues** (`_BACKLOG` #p1–#p2 items tagged for CRE + any `status: growing` self-inventories like [[LIFE/MENTAL HEALTH/AI Helper Targets]]): surface at most ONE build/infra candidate for the ops lane per week — proposed, never auto-slotted. This is the downstream half of decision-helper Step 5b (no-stranded-rulings, `^obs-164`): rulings emit queue items; week-shape is where queue items meet a week.
3. **Propose the week — one screen:**
   - **Morning lane (resident story):** the week's creative target in pipeline terms ("dictate SEQ 61–63" / "CH2 S12 promote + CH8 brief"), derived from where the pipeline actually sits.
   - **Ops lane (afternoons):** ONE theme from the flagship ("Substack: name the pub, port the content plan, draft post 1") + at most 2 batch items behind it.
   - **Personal window (late afternoon / early eve):** the week's `win:personal` items (family, health, personal admin, appointments), placed by their `due:` dates so a deadline lands in the right week rather than surfacing late. Pull any `win:personal` item whose `due:` falls in or near the week; flag any carrying `due:?` for a `triage-the-tasks` pass. *(Added 2026-07-14, task-scheduling layer — [[TASKS/TASK-SCHEMA]].)*
   - **1–3 milestones** for the week — concrete, receipt-checkable.
   - **Flags** (if any): residency seam approaching, a #p1 blocker (e.g., credential rotation before ads work), calendar collisions (once the calendar increment lands).
4. **Gate.** CRE ratifies / edits in one pass. 15-minute total cap includes this.
5. **Seed `TASKS.md`.** Write the ratified items under `## Active` (source-tagged `<!-- week-shape YYYY-MM-DD -->`), each phrased day-launch-ready: concrete, starting-action-shaped, one per work session where possible, and **schema-tagged per [[TASKS/TASK-SCHEMA]]** (`win:`, `#p`, and `due:` where the item has a real date; `due:?` if a deadline is known but undated). Update a small `## This week` header block (week of, lanes, milestones). Verify by re-read.
6. **Stop.** No Odysseus pushes (day-launch owns the accountability layer), no portfolio edits, no backlog dispatch.

## Fortnight review hook

The day-launch fortnight review extends here: every ~2 weeks, one proposed tuning based on receipts ("ops-lane themes that fit in 3 afternoons ship; 5-afternoon themes stall"). One finding, CRE rules, logged in this doc's changelog block.

## What this workflow never does

- Build project plans, break down epics, or produce anything longer than one screen (that's the project-breaker helper, unbuilt — [[LIFE/MENTAL HEALTH/AI Helper Targets]] #3)
- Switch story residency or reorder the portfolio (decision-helper + CRE only)
- Invent tasks, schedule fiction content, or push notifications
- Run longer than 15 minutes, ever
- Guilt. A skipped/zero week is a data point, not a failure state.

<!-- v1 authored 2026-07-11 per ^backlog-productivity-spine (spine proposal ratified same day). Packaging into .skill: desktop pack-skills.ps1, pending. -->
