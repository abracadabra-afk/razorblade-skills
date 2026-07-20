---
type: workflow
name: work-through
trigger: help me work through
aliases: [work through this, let's work through this, I'm stuck, why am I stuck, work-through, why isn't this moving]
inputs: [CRE's stated struggle, LIFE/MENTAL HEALTH/ADHD Patterns, TASKS/TODAY.md receipts, _CHANGELOG.md, the relevant project artifacts]
outputs: [a verdict (one pattern or none), a physical first action, one dated line in the pattern map's Field observations, an optional research seed on CRE's word]
lane: life
status: spec — packs after 2–3 live runs (run 1 completed 2026-07-19)
governed-by: DIR-015
last_updated: 2026-07-19
---

# WORKFLOW: work-through

## When to use

CRE says **"help me work through this"** / **"I'm stuck"** / **"why isn't this moving"** — he has a struggle, a stall, or a piece of work that isn't happening, and wants the *source* found rather than the task re-proposed. Sits beside [[WORKFLOWS/decision-helper]] (which handles forks — options on the table, pick one) and downstream of [[WORKFLOWS/day-launch]] (which handles initiation at 7am from the task pool). Neither of those answers *"I'm stuck and I don't know why."* This does.

**Hard cap: minutes, not a session** (DIR-015 clause 7). If it needs a session, it is not this instrument.

## Position & guards

- **Governed by [[_DIRECTIVES#DIR-015]]** — read it before running. The executional/affective split, the no-validation-drip rule, and the terminate-in-a-move requirement are law, not preferences.
- **Reads [[LIFE/MENTAL HEALTH/ADHD Patterns]] as a lookup surface.** This skill exists substantially *because* nothing else does — the map was a CRE ruling that bound no tool (DIR-014 in the life domain).
- **Never generates CRE's prose, never schedules his fiction's content, never invents a task.**
- **Read-only except two writes:** one dated line to the map's `## Field observations` section, and (on his word only) a research task line in `TASKS/TASKS.md`.
- **Gate pattern:** proposes a verdict, CRE rules it. A pattern he rejects is recorded as rejected — corrections are the training data.

## Design intent — what run 1 taught

The first live run (2026-07-19, by hand) **very nearly diagnosed an avoidance pattern that did not exist.** It read ten days of `TODAY.md` receipts, found two dictation items apparently carrying 3 and 5 days against a large system-building haul, and was ready to call it Pattern #3 + #5. Both legs were wrong: the carry counts were inflated by weekend days the board scored as workdays, and CRE had in fact dictated and drafted a whole chapter that never reached the board because it arrived as a co-author dependency the schema could not express.

**An instrument that reads only the task board will diagnose the author for the board's blind spots.** Steps 1 and 2 below exist entirely because of that, and they run *before* the map is ever opened. The correct verdict in run 1 was **"no pattern"** — and it was only reachable by checking the boring things first.

## Steps

### 0. Sentinel + frame

Verify `_DIRECTIVES.md` frontmatter (`^obs-004`). Take the struggle **as CRE stated it** — infer the referent, confirm it in **ONE line** so he can redirect in one word. Never run an intake questionnaire (the `decision-helper` Step-1 discipline; an ADHD user asking for help does not want a form).

### 1. Completeness check — is the record even right?

**Before any analysis.** The evidence base is usually the task board, and the task board is usually incomplete. Check:

- **Off-board work.** Read `_CHANGELOG.md` for the window and the relevant project artifacts (`dictation/`, `DEV/_intake/`, `slate/`, `revisions/`, chapter `changelog.md`, `_OBSERVATIONS`). Did the work happen somewhere the board can't see? The Step-0 derive pass in `day-launch` is built for exactly this — reuse its evidence order.
- **External dependencies.** Did a request arrive from a named person outside the vault (co-author, editor, family) and get done, or get silently prioritised over the board? Check for `blocks:<who>` ([[TASKS/TASK-SCHEMA]]) — and remember the tag fixes *ranking*, not *capture*.
- **Counter integrity.** Is an "Nth-day carry" counting non-working days? Weekend days are excluded from carry counts (`day-launch` v2.4); a stall measured in calendar days is not a stall measured in working days.

**If the record was incomplete, stop here and say so.** That is a complete and successful run. Fix the instrument, not the man.

### 2. Mundane check — logistics before psychology

Still before the map. The competing explanations that are not patterns at all:

- **Day-of-week / medication window.** Is the stalled work scheduled into a window where the meds have worn off, or onto a weekend that is structurally different by design?
- **Physical preconditions the board can't model.** Dictation needs an empty house. Some work needs a closed door, a machine, a file someone else holds. A task board tracks priority, not preconditions.
- **A genuine blocker upstream** — a dependency, an unmade decision, a missing runway. If the thing is actually blocked, it is not being avoided. Route unmade decisions to `decision-helper`, not here.

**Ask at most ONE question**, the smallest that discriminates between live hypotheses. State what each answer would change.

### 3. Pattern — one, evidence-bound, executional only

Only now open [[LIFE/MENTAL HEALTH/ADHD Patterns]].

- **Cap at one primary pattern** (DIR-015 clause 4). The map has 19 entries and will match anything if allowed to; precision collapses faster than recall improves (DIR-014's measured corollary).
- **Cite the evidence** — something CRE actually said, or a vault artifact. Never a vibe.
- **"No pattern — this is just a hard problem" is a valid and expected verdict.** So is "not enough evidence yet; the count is two and the threshold is four."
- **Executional patterns only** (#1, #2, #3, #5, #6, #7, #8, #10, #15, #16, #17, #18): name it, apply the map's own intervention.
- **Affective patterns** (#4, #11, #12, #13, #14, #19): **name once, plainly, and stop.** No reframing, no reassurance, no processing. On CRE's word only, seed a research task → [[WORKFLOWS/research-briefing]] → `KNOWLEDGE/RESEARCH/` (clinical sources preferred, practitioner figures marked `<<UNCERTAIN>>`, reports what is evidenced and never prescribes).

### 4. The move — terminate in a physical first action

The pass ends in **the smallest physical action on the actually-stalled work**, stated as a motion, not an outcome: *"open `runway.md` and read the cold open aloud, once"* — never *"work on EP 01."* Borrow `day-launch`'s first-domino discipline and the map's 5-minute rule.

**Two things that are NOT terminal moves** (DIR-015 clause 6):

- **A research seed.** "I filed a research task about shame" leaves the work stalled and the stall feeling addressed.
- **A systems fix.** Improving the board, the counter, or this skill is the exact category of satisfying admin work a stall hides inside. File it; do not do it now, and do not hand it back as the move.

If Step 1 or 2 ended the run, the move may legitimately be *"nothing today"* — say that plainly, with no framing.

### 5. Log — two lines, no ceremony

- One dated line to the pattern map's existing `## Field observations` section: what was stated, what was checked, the verdict, the move. That section already invites this (*"CRE folds them into the map when ready"*) — this closes the read→write loop.
- An **outcome field**, unfilled, for later review (briefing item 6 — the field can't measure; this measures itself). Feeds `DECISIONS/_WEIGHTS.md` only via a ratified review finding.

Below-trivial runs log nothing. A `_CHANGELOG` entry only if the vault changed (DIR-003's carve-out).

## What this skill never does

- **Work the affective lane** — name and stop, always (DIR-015 clause 1)
- **Answer struggle with praise, comfort, or encouragement** — Pattern #19 is explicit that on-demand validation is the dependency the research names (clause 5)
- **Name more than one primary pattern**, or match one without citing evidence
- **Diagnose before verifying the record is complete** — the run-1 failure, and the reason Steps 1–2 exist
- **End without a move**, or end in a research seed / systems fix dressed as one
- **Guilt, streaks, "you said you would"** — restarts are the design (inherited from `day-launch`)
- **Run long.** Minutes. An analysis that needs a session has become the avoidance.

## Non-goals

- Not a check-in loop, a companion, or anything invoked on a schedule — CRE invokes it, always
- Not `decision-helper` (forks), `day-launch` (initiation), or `workshop-chapter` (craft diagnosis)
- Not a substitute for a human professional on anything in the affective lane

<!-- v1 spec authored 2026-07-19 per ^backlog-work-through-skill, against DIR-015 (ratified same day). Run 1 was executed by hand before this doc existed — CRE fired the trigger mid-design — and its findings are baked into Steps 1-2 and the Design intent section. Packs after 2-3 live runs per the house convention (dev-reconcile / arc-audit / author-flags precedent). Not yet mirrored to skills-src/ or packed. -->
