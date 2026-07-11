---
type: workflow
name: decision-helper
trigger: help me decide
aliases: [run the decision helper, triage this decision, weigh this fork, branch check, should I do X or Y, review decisions]
lane: cross-lane — life (personal/logistics) + creative (dev-layer story forks)
profile: vault-wide; ledger at vault root DECISIONS/
status: draft
last_updated: 2026-07-10
---

# decision-helper — decision triage + proportional ledger

> **What this is:** an anti-decision-fatigue instrument. One skill, two lanes (life / creative), three backend modes (quick / research / triangulate), **one surface**: options → recommended pick + one-line basis → CRE ratifies, digs in, or parks. The machine does the deliberating; CRE does one binary-ish ruling. The un-chosen branch stops occupying working memory because the ledger answers it later, cheaply.
>
> **Skill source:** `WORKFLOWS/skills-src/decision-helper/` (SKILL.md + `references/ledger-schema.md`). Build artifact: `WORKFLOWS/skills/decision-helper.skill`.

---

## Position & guards

- **Gate pattern (house rule):** the helper proposes, CRE rules. Nothing self-executes; no decision is ever made for him.
- **Organic-process guard:** in the creative lane this is a **branch evaluator, not a branch generator**. It weighs options CRE brought. If it catches itself drafting a story option CRE did not articulate, it stops and says so. (Same line `dev-readiness` holds.)
- **Recombination boundary (CRE-ruled 2026-07-10, dec-001 pilot):** resurfacing or recombining **CRE's own captured dev** (floored takes, items/arc notes, held seams) is in-bounds and MAY be the recommendation — provided every element traces to his material and the receipts show the provenance. What stays out is new story substance the vault can't source to him. Rationale: a stated-branches-only limit would have missed his own no-quest-aids signal in the pilot.
- **Upstream of `workshop-chapter`:** creative use is for fork-in-the-road moments during dev, not chapter diagnosis.
- Ledger writes are safe ops (append/new-file); overwrites of existing entries are gated.
- DIR-004 applies: serialized YAML in all ledger frontmatter.

## What it is NOT

- Not `workshop-chapter` (chapter diagnosis), `reconcile` (verdict rulings), `blind-response` (blind-read response), or `dev-readiness` (gap surfacing).
- Not an idea generator of any kind.

---

## Step 1 — Intake (derive, don't interrogate)

Take the decision as CRE states it. **Infer** goals, constraints, and criteria from what he said; confirm the inference in ONE line — never run an intake questionnaire. If too vague to triage, ask ONE question, the smallest one that unblocks.

## Step 2 — Triage gate

Classify before any deliberation — in-depth process on a two-way-door decision is the paralysis engine.

| | **QUICK** | **IN-DEPTH** |
|---|---|---|
| Test | Reversible, low-cost, low-regret ("two-way door") | Irreversible, expensive, high-regret, or canon-touching |
| Options | Cap at 3 | As many as the decision genuinely holds |
| Standard | Satisfice — first option that clears the bar wins | Criteria + weights, triangulated/researched |
| Log | One line (or nothing, below threshold) | Full ledger entry + review date |

Lane detection: story/dev forks → **creative lane** (triangulate backend); everything else → **life lane** (quick or research). State the triage call; CRE can overrule it — his overrule is itself ledger data.

## Step 3 — Backend (invisible unless he digs in)

- **Mode A — QUICK (life):** no research; ≤3 options from what's known; satisficing pick + one-line basis. Gives CRE **permission to stop deliberating**.
- **Mode B — RESEARCH (life, in-depth):** pull context (vault, web); weigh against confirmed criteria. Research-briefing discipline inherited (corroborate load-bearing claims; flag thin sources). May run async. **Receipts written to the ledger entry DURING synthesis**, never reconstructed after.
- **Mode C — TRIANGULATE (creative):** no invention — pull across instruments the vault maintains: **"Chad likes"** (project `_DEV.md` taste anchor + reconcile/loop-clearer/blind-response ruling history) · **"the story prefers"** (`threads.md` payoffs, `arcs.md` trajectory, `bible.md`) · **"reader experience"** (blind-read findings + scene-intensity contours). Where lenses **disagree, surface the tension** — never average it away. Load project material on demand only (DIR-002).

## Step 4 — The surface (identical in every mode)

1. Triage call (one phrase) → 2. the options (his branches verbatim in creative lane) → 3. **recommended pick + one-line basis** → 4. three exits: **ratify / dig in / park**. A recommendation never ships without a basis — the basis is what CRE corrects, and corrections are training data.

- **RATIFY:** record, close, proportional log. Seconds.
- **DIG IN:** unfold the ledger entry — full criteria/weights, per-lens findings, sources, discards with why each lost. **A view over the log, not a separate mode** (one write, two reads; nothing drifts).
- **PARK (a real resolution):** `status: parked` + `parked-until:` (a condition, not just a date). Parked creative forks are load-bearing dev gaps — `dev-readiness` should see them.

## Step 5 — Proportional logging

Ledger at vault root `DECISIONS/` (one ledger, both lanes — cross-lane patterns are the most interesting weights). Full schema: `skills-src/decision-helper/references/ledger-schema.md` — read before the first write of a session.

- **Quick:** one line to `DECISIONS/_QUICK LOG.md` (`date | decision | pick | basis | ruling`). Below-trivial: no log.
- **In-depth:** one entry `DECISIONS/YYYY-MM-DD <slug>.md` — goals, criteria + weights, options **incl. discards with reasons**, receipts, recommendation + basis, ruling, `review-date`.

## Step 5b — Discharge the ruling (the no-stranded-rulings rule, 2026-07-11)

A ratified pick that implies **work** is not done at the log line. Before the session moves on: if the pick is a build/action, emit its queue item — a `_BACKLOG` anchor (OS/skill builds) or a `TASKS/TASKS.md` line (CRE to-dos) — and stamp the ledger row/entry with a pointer to it. If the pick explicitly defers the un-chosen branch ("later"), that branch ALSO gets a queue item or a named revisit condition — parked visibly, not dropped. A ruling with no downstream artifact is a leak (`^obs-164`: the 2026-07-10 AI-Helper-Targets picks left two of three targets stranded in the note — captured, scored, ratified-adjacent, queued nowhere). week-shape reads the queues, so this rule is what connects a ruling to a week.

## Step 6 — Review & weight learning

Weights update **at review time, not decision time**. "Review decisions" (or a due review-date) → pull due entries, ask outcomes, fill `outcome`. Pattern findings surface as **proposals CRE ratifies** — never silently adjusted; ratified blocks land in `DECISIONS/_WEIGHTS.md` (each citing its entry IDs).

## Optional first-run: retrospective seeding (separate, gated)

A one-time read-only mining pass over historical rulings can seed apparent *tendencies* — offered, never assumed; CRE ratifies or corrects before anything enters `_WEIGHTS.md`. Skip entirely if he'd rather start clean.

## What this skill never does

- Invent options, branches, or story content of any kind
- Decide for CRE, or nag him toward a ruling
- Run in-depth process on a quick decision (or interrogate with intake forms)
- Ship a recommendation without a stated basis
- Adjust weights without a ratified review finding
- Touch `draft.md`, `REFERENCE/`, or any project file — reads instruments, writes only `DECISIONS/`
