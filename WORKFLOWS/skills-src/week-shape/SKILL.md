---
name: week-shape
description: Shape CRE's working week — the 15-minute weekly menu between the quarterly PORTFOLIO and the daily day-launch. Reads TASKS/PORTFOLIO.md + open TASKS + the receipts roll, derives completions from artifacts (never asks CRE what he finished), proposes ONE screen — morning-lane creative target for the resident story, one afternoon ops-lane theme, 1-3 receipt-checkable milestones — gates on CRE's one-pass ratify, then seeds TASKS/TASKS.md so day-launch never wakes to an empty pool. Use whenever CRE says "shape the week," "plan the week," "week shape," or "what's this week." Hard-capped at 15 minutes — a menu he approves, not a plan he builds. Do NOT use it to launch or close a day (day-launch), switch story residency or reorder the portfolio (decision-helper + CRE only), break a goal into steps (project-breaker, unbuilt), or dispatch _BACKLOG ("dispatch" is reserved). It never invents tasks or priorities and never schedules the content of CRE's fiction.
---

# Week Shape

The middle layer of the productivity spine (ratified 2026-07-11): PORTFOLIO decides quarterly → **week-shape decides weekly** → day-launch executes daily. Every decision is made at the highest, least-frequent layer possible, so mornings hold zero decisions. Founding bug: the 2026-07-11 zero-candidate morning — day-launch worked perfectly on an empty pool.

Canonical doc: `WORKFLOWS/week-shape.md`. Spec: `LIFE/MENTAL HEALTH/ADHD Patterns.md` (#2 abandonment, #3 planning-as-procrastination, #4 interest-drift, #8 working memory, #19 validation).

## Position & guards

- **Gate pattern:** proposes, CRE rules. Nothing writes to `TASKS.md` until his one-pass ratify.
- **Vault sentinel:** confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`) before any write; mismatch → halt and ask.
- **File tools only**; verify every write by re-read (DIR-005).
- **HARD CAP 15 MINUTES** (Pattern #3 armor). One proposal screen, one pass. A second refinement round is over-engineering — ship the menu.
- **Derives, never re-opens:** priority order and residency come from `PORTFOLIO.md` ratified state. If the portfolio is `status: proposed`, halt and ask for the ratify. A wished-for different order → flag for a portfolio edit / decision-helper run, never silently absorbed.
- **Residency is read-only.** Resident story finished/blocked → FLAG a residency question for decision-helper; never switch it here (rule R1).
- **Never** invents projects, schedules fiction content, pushes Odysseus notifications, or answers "dispatch."
- **Restart rule (Pattern #2):** a skipped or zero week costs one neutral line. No streaks, no guilt.

## Steps

1. **Receipts roll-up — derive first (the validation open).** Reconcile last week's seeds against ground truth before rolling up (evidence order: project artifacts — new files/mtimes in `dictation/`, `DEV/_intake/`, `slate/`, `revisions/`, frontmatter, chapter changelogs → `_CHANGELOG.md` → project backlogs → `DECISIONS/_QUICK LOG.md`). Verifiable out-of-band completions get checked with a `<!-- derived: artifact, date -->` stamp; off-list work gets its own roll-up line. CRE never reports completions — the artifacts do. Then one honest paragraph: sequences dictated, chapters landed, posts shipped, X/Y day average. Zero week → one neutral line.
2. **Read the strategy.** `TASKS/PORTFOLIO.md`: resident story, ops-lane flagship, priority order, energy map, rules R1 (residency) + R2 (forward motion). Read the resident story's backlog + pipeline/DEV state for what's *actually* next — the real forward edge, not a guess. **Sweep the build queues** (`_BACKLOG` #p1–#p2 CRE-facing items + `status: growing` self-inventories like `LIFE/MENTAL HEALTH/AI Helper Targets.md`): surface at most ONE build/infra candidate per week — proposed, never auto-slotted (the no-stranded-rulings backstop, `^obs-164`).
3. **Propose the week — one screen:**
   - **Morning lane (resident story):** the week's creative target in pipeline terms ("dictate Part N front to back"), derived from where the pipeline actually sits. Forward-only per R2 — never a revision target unless the pipeline stage says revision.
   - **Ops lane (afternoons):** ONE theme from the flagship + at most 2 batch items behind it.
   - **1–3 milestones**, concrete and receipt-checkable. Include one small-win milestone where available.
   - **Flags** (if any): approaching residency seam, #p1 blockers, calendar collisions.
4. **Gate.** CRE ratifies/edits in one pass. The 15-minute cap includes this.
5. **Seed `TASKS.md`.** Ratified items land under `## Active`, source-tagged `<!-- week-shape YYYY-MM-DD -->`, each phrased day-launch-ready (concrete, starting-action-shaped, one per work session where possible). Update the `## This week` header block (week-of, lanes, milestones — the cascade order day-launch v2.1 pulls from). Verify by re-read.
6. **Stop.** No notifications, no portfolio edits, no backlog dispatch, no second pass.

## Fortnight review hook

Every ~2 weeks (rides the day-launch fortnight review): surface ONE receipts-based tuning as a proposal CRE ratifies ("themes that fit 3 afternoons ship; 5-afternoon themes stall"). Ratified findings append to the canon doc's changelog block.

## What this skill never does

- Build project plans or step breakdowns (that's the project-breaker helper, `^backlog-project-breaker-helper`)
- Switch residency or reorder the portfolio (decision-helper + CRE)
- Invent tasks, generate CRE's prose, or schedule his fiction's content
- Push notifications (day-launch owns the accountability layer)
- Run past 15 minutes, produce more than one screen, or guilt a skipped week
