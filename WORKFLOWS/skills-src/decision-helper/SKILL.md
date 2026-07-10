---
name: decision-helper
description: Triage and support a decision CRE brings — categorize it quick vs in-depth, assemble options, recommend one with a stated one-line basis, and log proportionally to the DECISIONS/ ledger so the un-chosen branch stops occupying working memory. Use whenever CRE asks to "help me decide," "run the decision helper," "triage this decision," "weigh this fork," "branch check," "should I do X or Y," or brings any life/logistics choice OR a dev-layer story fork (which reveal lands where, this branch or that) he wants measured. Built as an anti-decision-fatigue instrument — uniform ratify-or-dig-in surface regardless of decision weight; the backend absorbs the complexity. MEASURES branches CRE articulated; NEVER invents story options (organic-process guard). Do NOT use it to diagnose a chapter in progress (workshop-chapter), rule spec-check verdicts (reconcile), respond to a blind read (blind-response), surface dev gaps (dev-readiness), or generate ideas of any kind.
---

# Decision Helper

One skill, two lanes (life / creative), three backend modes (quick / research / triangulate), **one surface**: options → recommended pick → CRE ratifies, digs in, or parks.

Design intent: CRE is neurodivergent; decision fatigue and analysis paralysis are the enemy. Every design choice below exists to keep his cognitive load constant no matter how heavy the decision is. The machine does the deliberating; CRE does one binary-ish ruling.

## Position & guards

- **Gate pattern (house rule):** the helper proposes, CRE rules. Nothing self-executes, no decision is ever made for him.
- **Organic-process guard:** in the creative lane this skill is a **branch evaluator, not a branch generator**. It weighs options CRE brought. If it catches itself drafting a story option CRE did not articulate, it stops and says so. (Same line dev-readiness holds.)
- **Recombination boundary (CRE-ruled 2026-07-10, dec-001 pilot):** resurfacing or recombining **CRE's own captured dev** (floored takes, items/arc notes, held seams) is in-bounds and MAY be the recommendation — provided every element traces to his material and the receipts show the provenance. What stays out is new story substance the vault can't source to him. Rationale: a stated-branches-only limit would have missed his own no-quest-aids signal in the pilot.
- **Upstream of workshop-chapter:** creative use is for fork-in-the-road moments during dev, not chapter diagnosis.
- Ledger writes are safe ops (append/new-file); overwrites of existing entries are gated.
- DIR-004 applies: serialized YAML in all ledger frontmatter.

## Step 1 — Intake (derive, don't interrogate)

Take the decision as CRE states it. **Infer** goals, constraints, and criteria from what he said ("need it by Friday, budget's tight" → deadline + cost criteria). Confirm the inference in ONE line — never run an intake questionnaire. A form is decision fatigue wearing a helpful hat.

If the decision is too vague to triage, ask ONE question, the smallest one that unblocks.

## Step 2 — Triage gate

Classify before any deliberation. This gate is the fatigue fix — in-depth process on a two-way-door decision is the paralysis engine.

| | **QUICK** | **IN-DEPTH** |
|---|---|---|
| Test | Reversible, low-cost, low-regret ("two-way door") | Irreversible, expensive, high-regret, or canon-touching |
| Options | Cap at 3 | As many as the decision genuinely holds |
| Standard | Satisfice — first option that clears the bar wins | Criteria + weights, triangulated/researched |
| Log | One line (or nothing, below threshold) | Full ledger entry + review date |

Lane detection: story/dev forks → **creative lane** (triangulate backend). Everything else → **life lane** (quick or research backend). Creative forks are almost always in-depth; a genuinely trivial craft call may still go quick.

State the triage call in the response ("Quick — reversible, cheap to undo"). CRE can overrule it; his overrule is itself ledger data.

## Step 3 — Backend (invisible unless he digs in)

### Mode A — QUICK (life lane)
No research. Assemble ≤3 options from what's known, pick the satisficing recommendation, one-line basis, done. The skill's job here is to give CRE **permission to stop deliberating**.

### Mode B — RESEARCH (life lane, in-depth)
Pull context (vault, web as needed), assemble options, weigh against the confirmed criteria.
- **Research-briefing discipline inherited:** corroborate load-bearing claims across independent sources; flag thin or single-source ones. A recommendation built on one blog post says so.
- **May run async:** "bring me the decision, I'll have options ready" — park it, work, present when done. Never make CRE sit through a synthesis he didn't ask to watch.
- **Receipts as it goes:** sources pulled, criteria weighed, options considered-and-discarded (with why they lost) are written to the ledger entry DURING synthesis, not reconstructed after. Invisible ≠ unaccountable.

### Mode C — TRIANGULATE (creative lane)
No invention — pull-and-triangulate across instruments the vault already maintains:

| Lens | Instrument |
|---|---|
| **"Chad likes"** | Project `_DEV.md` taste anchor + his reconcile / loop-clearer / blind-response ruling history (revealed preference) |
| **"The story prefers"** | REFERENCE canon: `threads.md` payoff obligations, `arcs.md` trajectory, `bible.md` — does this branch honor or strand a plant? |
| **"Reader experience"** | Blind-read findings + scene-intensity contours at this point in the work |

Where the lenses **disagree, surface the tension** — "Chad likes it but the story resists it" is the finding, never average it away. Load project material on demand only (DIR-002).

## Step 4 — The surface (identical in every mode)

Present, in this order, briefly:

1. Triage call (one phrase)
2. The options (his branches verbatim in creative lane; discards exist in the log, not here)
3. **Recommended pick + one-line basis** ("Recommending A: pays the ch. 19 plant, matches your ruling pattern on early reveals — though it front-loads intensity where the contour wants a valley.")
4. The three exits: **ratify / dig in / park**

A recommendation never ships without a basis — the basis is what CRE corrects, and his corrections are the training data.

### Exit: RATIFY
Record the ruling, close the loop, proportional log (Step 5). Seconds, not minutes.

### Exit: DIG IN
Unfold the ledger entry — full criteria + weights, per-lens findings, sources, and the discarded options with why each lost. **Dig-in is a view over the log, not a separate mode**: one write, two reads; nothing can drift between what he sees and what was reasoned. Discuss, adjust weights if he corrects the reasoning, then back to ratify/park.

### Exit: PARK (a real resolution, not a failure)
Some forks aren't decidable yet — the dev layer hasn't descended far enough. Log `status: parked` with `parked-until:` (a condition, not just a date — "not decidable until the SEQ 20 dev fills in"). Parked creative forks are load-bearing gaps by definition; note that dev-readiness should see them.

## Step 5 — Proportional logging

Ledger lives at vault root: `DECISIONS/` (one ledger, both lanes — cross-lane patterns are the most interesting weights). Full schema: `references/ledger-schema.md` — read it before the first write of a session.

- **Quick:** one line appended to `DECISIONS/_QUICK LOG.md` (date | decision | pick | basis). Below-trivial: no log at all. If logging costs more than the decision did, don't.
- **In-depth:** one entry file `DECISIONS/YYYY-MM-DD <slug>.md` with goals, criteria + weights, all options **including discards with reasons**, sources/receipts, recommendation + basis, CRE's ruling, `review-date`.
- **The entry is what kills the second-guessing.** The un-chosen branch nags weeks later; the entry answers it cheaply — either the reasoning still holds (close the loop) or something changed (a NEW decision with new inputs, not a haunting). Same move open-loops.md makes for pending calls.

## Step 6 — Review & weight learning

Weights update **at review time, not decision time**.

- When CRE asks to "review decisions" (or a review date arrives in session): pull due entries, ask how each turned out, fill the `outcome` field.
- After enough outcomes, surface pattern findings as **proposals CRE ratifies** — "you chronically overweight cost and underweight energy drain" — never silently adjust. Ratified patterns get recorded in `DECISIONS/_WEIGHTS.md` and inform future recommendation bases.

## Optional first-run: retrospective seeding (separate, gated)

Historical vault data (changelogs, verdict sheets, ruling history) can seed initial *tendencies* — but it records rulings without criteria and almost never outcomes, and it's overwhelmingly creative-pipeline decisions. Offer, don't assume: a one-time read-only mining pass producing an "apparent decision patterns" report CRE ratifies or corrects before anything seeds `_WEIGHTS.md`. Skip entirely if he'd rather start clean; the forward ledger captures what history can't.

## What this skill never does

- Invent options, branches, or story content of any kind
- Decide for CRE, or nag him toward a ruling
- Run in-depth process on a quick decision (or interrogate him with intake forms)
- Ship a recommendation without a stated basis
- Adjust weights without a ratified review finding
- Touch draft.md, REFERENCE/, or any project file — it reads instruments, writes only DECISIONS/
