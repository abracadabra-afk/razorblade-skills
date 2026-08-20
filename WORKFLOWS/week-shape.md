---
type: workflow
name: week-shape
trigger: shape the week
aliases: [plan the week, week shape, run the week shape, what's this week]
inputs: [TASKS/PORTFOLIO.md, TASKS/TASKS.md open items, TASKS/TODAY.md receipts roll, project backlogs of the resident story + ops lane]
outputs: [TASKS/TASKS.md seeded with the week's items, a ratified week header block in TASKS/TASKS.md]
lane: life
status: draft
last_updated: 2026-08-19
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
2. **Read the strategy.** `PORTFOLIO.md`: resident story, ops-lane flagship, priority order, energy map. Read the resident story's backlog + pipeline state for what's actually next (the real next milestone, not a guess). **Chunk-supply sweep (2026-07-28, CRE-ratified — the self-healing loop):** read `TASKS/PROJECTS/*.md` against the portfolio's active lanes. Any project that is (i) portfolio-active in a served lane but has **no plan file**, or (ii) has a plan whose **current milestone's chunks are all closed** with the next milestone unchunked, gets a seeded task: `#p2 win:ops ⚙️ plan the project: <X> (project-plan session)`. **Max ONE chunking seed per week** (Pattern #3 — a board of planning tasks is procrastination with receipts); if several qualify, seed the highest portfolio rank and name the rest in the proposal's Flags. The project-plan run itself stays gated and attended. This is the upstream half of day-launch v2.8's re-chunk cascade — together they keep the chunk pool fed without anyone remembering to say "plan the project" (the 2026-07-28 starvation review's founding defect: GR 1e marketing sat unchunked while WIW monopolized every board). Stamp obvious `#quick` items ([[TASKS/TASK-SCHEMA]]) while seeding. **Also sweep the build queues** (`_BACKLOG` #p1–#p2 items tagged for CRE + any `status: growing` self-inventories like [[LIFE/MENTAL HEALTH/AI Helper Targets]]): surface at most ONE build/infra candidate for the ops lane per week — proposed, never auto-slotted. This is the downstream half of decision-helper Step 5b (no-stranded-rulings, `^obs-164`): rulings emit queue items; week-shape is where queue items meet a week.
3. **Propose the week — one screen:**
   - **Morning lane (resident story):** the week's creative target in pipeline terms ("dictate SEQ 61–63" / "CH2 S12 promote + CH8 brief"), derived from where the pipeline actually sits.
   - **Ops lane (afternoons):** ONE theme from the flagship ("Substack: name the pub, port the content plan, draft post 1") + at most 2 batch items behind it. *(v2.7 growth split, 2026-07-28):* seed flagship marketing/readership/income items tagged **`#growth`** ([[TASKS/TASK-SCHEMA]]) so day-launch serves them ahead of untagged admin — the flagship theme should virtually always yield 1–2 `#growth` seeds.
   - **Personal window (late afternoon / early eve):** the week's `win:personal` items (family, health, personal admin, appointments), placed by their `due:` dates so a deadline lands in the right week rather than surfacing late. Pull any `win:personal` item whose `due:` falls in or near the week; flag any carrying `due:?` for a `triage-the-tasks` pass. *(Added 2026-07-14, task-scheduling layer — [[TASKS/TASK-SCHEMA]].)*
   - **1–3 milestones** for the week — concrete, receipt-checkable.
   - **Flags** (if any): residency seam approaching, a #p1 blocker (e.g., credential rotation before ads work), calendar collisions (once the calendar increment lands).
4. **Gate — re-verify state, THEN present.** CRE ratifies / edits in one pass. 15-minute total cap includes this.

   **4a. State diff (mandatory when the proposal was composed in an earlier session — i.e. every unattended Sunday → Monday ratify).** A proposal is a **dated claim about a pipeline that moves faster than this workflow's own cadence**; it sits 12–14 h between compose and ratify, and one attended day on this vault can dictate, clean, split and rename a chapter. So before the proposal is shown to CRE:

   - Read `_CHANGELOG.md` entries dated **after the proposal's `composed:` stamp** (clause 2 of Unattended mode writes it). Cheap by construction — newest-first, so you stop at the first entry older than the stamp.
   - For every seed that **names an artifact** (a chapter, an episode, a project plan), read that artifact's own current state — `_status.md` / `draft.md` frontmatter / the plan file's milestone table. Frontmatter only; do not re-read prose.
   - **Re-point any seed the newer entries contradict**, and mark it inline `CORRECTED at ratify` with one line saying what moved. A correction that preserves the lane's *intent* is a safe-op — make it, don't ask (don't-rule-on-trivia). A correction that changes what the lane is **for** is a flag CRE rules in the same one pass.
   - **Never invent the replacement.** If a seed is contradicted and the live state doesn't supply an obvious re-point, drop the seed to a flag and say so. The no-invention guard outranks a tidy board.
   - **Say what you did not check** (DIR-018). This diff covers `_CHANGELOG` + named-artifact frontmatter. It does **not** cover off-vault work (Drive drafts, external console actions, anything CRE did by hand and never logged), and it cannot see a chapter that moved without a changelog entry. State the residue in one line at the gate rather than presenting the diff as a clean bill.

   Founding instance (`^obs-248`, 2026-08-10): the 08-09 proposal's morning lane read *"open Part 3 — CH15 → runway → dictate"*; by Monday's ratify CH15 had been dictated **and** run through the full `chapter-clean` stretch that morning (`register-swept`, dec-027 split CH15/CH16), and its real state was an **open Gate B sheet holding the land**. Seeded verbatim it would have put "build the runway" on the board for a chapter three stages past that, with the actual blocker surfaced nowhere. Caught only because that session happened to read `_CHANGELOG` first — which is exactly why it is now a step and not a habit. This is DIR-010's authored-artifact corollary arriving on the productivity spine.
5. **Seed `TASKS.md`.** Write the ratified items under `## Active` (source-tagged `<!-- week-shape YYYY-MM-DD -->`), each phrased day-launch-ready: concrete, starting-action-shaped, one per work session where possible, and **schema-tagged per [[TASKS/TASK-SCHEMA]]** (`win:`, `#p`, and `due:` where the item has a real date; `due:?` if a deadline is known but undated). Update a small `## This week` header block (week of, lanes, milestones). Verify by re-read.
6. **Stop.** No Odysseus pushes (day-launch owns the accountability layer), no portfolio edits, no backlog dispatch.

## Unattended mode — propose-only (2026-07-28, CRE-ratified; the cadence fix)

Runs on the **`week-shape-runner` scheduled task (Sunday ~18:00)** so the weekly feeder can never silently die again (the founding defect: the week of 07-13's seeds were spent day one and no re-shape came for 15 days — day-launch starved down to a WIW monopoly). Unattended rules, per DIR-012:

1. **Steps 1–3 run; Steps 4–5 defer.** The derive pass writes its safe-ops (derived checks with provenance stamps, the receipts roll-up); the proposal is composed in full — including the chunk-supply sweep seed and lane targets — but **NO Active items are seeded and nothing is ratified.**
2. **The proposal lands rendering-visible** as the `## This week` header block in `TASKS.md`, stamped **`(PROPOSED — composed YYYY-MM-DD HH:MM — ratify at Monday's launch)`**, replacing the stale week header. Prose, never an HTML comment (DIR-012 cl. 4). **The `composed:` timestamp is load-bearing, not decoration** — it is the date boundary Step 4a diffs `_CHANGELOG` against, so a bare date with no time is a defect (a proposal written Sunday 18:00 and a chapter landed Sunday 09:00 are not distinguishable without it). Write the real compose time, not the schedule slot.
2a. **A PROPOSED block is ADVISORY, never gating (v1.2, 2026-08-19, CRE-ratified).** The propose-only conservatism above (compose in full, seed nothing) was correct about *writes* and wrong about *authority*: the unratified block kept sequencing day-launch's candidate pool, so open, unblocked tasks were excluded on the strength of a proposal nobody had ruled. Measured 2026-08-19: the week of 08-17 sat PROPOSED for three days while `ETI-1.4` and `GR1-2.2` — both open, both unblocked, both `#growth` — were excluded from all three boards *because the proposal sequenced them behind the EP 01 theme*, and the days scored zero. **A proposal may ORDER the pool; it may never EXCLUDE from it.** Day-launch v3.0 auto-adopts a stale PROPOSED block as the default week (lane intents and ordering hints only) and restamps it `(ADOPTED as default YYYY-MM-DD — advisory)`; the week's seeds still land in Active only on CRE's real ratify. Nothing downstream ever waits on that ratify again — it is **confirm-by-exception**, and a week that is never ratified costs its Active seeds, not the working days.

3. **Monday's day-launch closes the loop:** the standing **`every:mon` "Ratify the week" task in `TASKS.md`** (`#p1 win:ops #quick`, CRE-ratified 2026-07-28) surfaces on Monday's board through the normal recurrence machinery — a first-class task, so it reaches CRE's board and phone even with every cadence running unattended; day-launch's v2.9 staleness escalation is the backstop (same item, deduped). **The ratify leg runs Step 4a (state diff) BEFORE presenting** — the conservatism that makes this mode safe (propose, seed nothing) is the same thing that opens the staleness window, so the attended half is the only actor positioned to close it (`^obs-248`). On CRE's go — attended, one pass — the seeds land in Active per Step 5 and the block drops its PROPOSED stamp.
4. The 15-minute cap, the one-screen rule, and every never-does above apply unchanged. A Sunday where nothing changed still writes the proposal — a fresh menu costs one block; a dead feeder costs a week.

## Fortnight review hook

The day-launch fortnight review extends here: every ~2 weeks, one proposed tuning based on receipts ("ops-lane themes that fit in 3 afternoons ship; 5-afternoon themes stall"). One finding, CRE rules, logged in this doc's changelog block.

## What this workflow never does

- Build project plans, break down epics, or produce anything longer than one screen (that's the project-breaker helper, unbuilt — [[LIFE/MENTAL HEALTH/AI Helper Targets]] #3)
- Switch story residency or reorder the portfolio (decision-helper + CRE only)
- Invent tasks, schedule fiction content, or push notifications
- Run longer than 15 minutes, ever
- Guilt. A skipped/zero week is a data point, not a failure state.
- **Gate the working day on its own ratify (v1.2).** An unratified proposal orders the pool; it never excludes from it, and it never stops day-launch running.
- **Carry a stale flag forward unchanged.** A flag repeating verbatim for a third week (the residency seam, 08-03→08-19) is not a flag — it is a question the proposal is failing to close. Fold it, retire it, or route it to decision-helper with a named next action.

<!-- v1 authored 2026-07-11 per ^backlog-productivity-spine (spine proposal ratified same day). Packaging into .skill: desktop pack-skills.ps1, pending. -->
<!-- v1.2 2026-08-19, CRE-ratified (attended spine review, same session as day-launch v3.0): new Step 2a — a PROPOSED `## This week` block is ADVISORY, never gating. The propose-only mode was right about writes and wrong about authority: an unratified proposal was still sequencing day-launch's candidate pool, excluding open unblocked tasks on a ruling that had never happened. Measured: the week of 08-17 sat PROPOSED 3 days; ETI-1.4 + GR1-2.2 (open, unblocked, #growth) excluded from all three boards "because the proposal sequences them behind the flagship theme"; three zero days. Rule: a proposal ORDERS, it never EXCLUDES; day-launch v3.0 auto-adopts a stale block as the advisory default; ratify becomes confirm-by-exception and only ever gates the Active SEEDS, never the working day. Also added two never-does: don't gate the day on this workflow's own ratify, and don't carry a flag verbatim into a third week (the residency seam did exactly that, 08-03→08-19 — retired at this review on CRE's ruling: Witchwood default-continues, re-raise at the end of Part 3). No .skill layer exists for week-shape (still unpacked) — the live surface is the `week-shape-runner` task prompt, updated the same session (DIR-016). -->
<!-- v1.1 2026-08-10 (CRE-ruled: "please fix") — Step 4a ratify-time state diff added, unattended cl. 2 upgraded to a timestamped `composed:` stamp (the boundary 4a diffs against), unattended cl. 3 points at 4a. Source: ^obs-248 / ^backlog-weekshape-ratify-reverify — the 08-09 proposal's CH15 morning lane was 3 pipeline stages stale by Monday's ratify. DIR-016 surfaces covered same session: this doc + the live `week-shape-runner` task prompt + the every:mon "Ratify the week" item in TASKS.md. No .skill layer exists for week-shape (still unpacked), so there is no installed copy to drift. -->
