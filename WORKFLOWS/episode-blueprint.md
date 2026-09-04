---
type: workflow
name: episode-blueprint
status: draft — source authored 2026-09-03 off the ratified intent; PACKED + INSTALLED 2026-09-04 (desktop pack-skills.ps1, DIR-009); graduates after 2–3 live runs
triggers: ["blueprint the episode", "shape the episode", "budget the episode"]
lane: 5 (writing-ops) + 1 (fiction)
intent: "[[WORKFLOWS/intents/episode-blueprint]]"
created: 2026-09-03
last_updated: 2026-09-04
revision_note: "2026-09-04 (route v4) — runs TWICE: run 1 at S1.5 as before, run 2 at S3 as a MANDATORY regeneration after the new S2 dream-catching leg and episode-feedback move the premise (CRE: a stale blueprint reaching the runway is the failure case). Run 2 may read WRITING/SHORTS/DEV/ as an additive escalation source; premise still wins on overlap; draft.md stays excluded on both runs. Run 1's [ANGLE MISSING — CRE] hand-backs now set the S2 agenda. DIR-017's divergence clause clarified as governing the mic, not the planning stage — the plan may be tight. Re-pack owed (DIR-009). Prior note: CRE ruled the deepened triage's `## Arc chain` in as a fourth escalation source (Inputs, Step 2, guards; mirrored in skills-src/episode-blueprint/SKILL.md Step 1). Closes the S0.5 to S1.5 seam premise-forge v2 opened upstream. The plan-only rule is unchanged: draft.md stays excluded. Precedence: premise wins on overlap, the arc chain is additive where the premise is silent. Re-packed + installed 2026-09-04; installed body verified to carry the fourth source."
---

# episode-blueprint

The **Writing Is War episode plan** — the one-minute, section-budgeted escalation plan CRE reads before he drafts. Takes a gated premise (episode-init has said GO, the folder exists) and writes `blueprint.md` into the episode folder: the cast, the flaw, the incident, the choice, the escalations with the angle each takes on the flaw, the moment of truth, the climax, and the outcome or `inferred` — one memorizable sentence and a word budget per section, summing to the ruled center target. It adds a **variance line** (any escalation repeating another's angle inside the episode, or repeating the shape of the last few episodes), a **scope line** (cast, conflict, span, spines) with a SHORT-FORM / OVER-BAND verdict, and a **GO / RESHAPE / ROUTE-OUT** recommendation with a one-line basis that CRE rules.

**The problem it exists to kill:** episodes losing escalation variance and growing past the container. EP 01 and 02 followed the model and landed near target; EP 03 was reshaped from earlier material; the EP 04 candidate (*The Coda of John Grady*) is past 5,000 words against a 2,500 target — a chore to narrate and impossible to replicate weekly. The tool moves the length call and the variance read to planning, where they are cheap.

> **Route v4 (CRE-ruled 2026-09-04) — this workflow now runs TWICE, and the second run is mandatory.**
>
> - **Run 1 at S1.5**, unchanged: the plan from CRE's articulated material, before any drafting. Its `[ANGLE MISSING — CRE]` hand-backs are not just gaps to fill later — **they set the agenda for the S2 dream-catching session**, telling him which holes to aim the mic at.
> - **Run 2 at S3 — the regeneration, and it is no longer conditional.** S2 banks new material into `WRITING/SHORTS/DEV/` and `episode-feedback` amends `premise.md`; the plan *will* have moved. CRE's basis: **a stale blueprint reaching the runway is the failure case, not the cost.** So the regeneration is a named route step, run every time, not a DIR-019 §1 side-effect noticed if someone remembers. Carry `## Your notes` verbatim across the regeneration as always.
> - **Run 2 may read the S2 DEV material** — `DEV/_DEV.md` (taste anchor), `DEV/scenes/`, `DEV/registry/` — as an escalation source alongside the premise and the arc chain. Precedence unchanged: the premise wins on overlap; DEV material is additive where the premise is silent. **`draft.md` stays excluded on both runs** (plan-only, CRE-ruled 2026-09-03).
> - **The plan may be tight.** DIR-017's divergence-is-a-win clause governs the **mic**, not the planning stage (CRE-ruled 2026-09-04): it protects the draft from the plan, not the plan from rigor. Only the runway stays loose. Nothing downstream grades a draft against this blueprint — that rule is untouched.
>
> Route canon: [[WORKFLOWS/pipeline]] episode route v4. Provenance: [[WORKFLOWS/intents/wiw-route-v4]].

> **Two ratified positions this tool carries (CRE, 2026-09-03):** (1) **the band is prescriptive at plan time** — an over-band plan gets RESHAPE / ROUTE-OUT recommended and CRE rules; the 07-30 "descriptive" treatment still governs finished drafts (`DECISIONS/_QUICK LOG` 2026-09-03 row). (2) **The blueprint sits beside the mic carve, not in place of it** — `episode-runway` Pass 2 stays the optional mic-route instrument; the blueprint is the plan both routes read.

## Pipeline position — S1.5 of the episode route

```
S0   feeling capture        premise-forge → CANDIDATES/<title>/triage.md
S1   gate + scaffold        episode-init  → EP NN folder, gated premise.md, GO
S1.5 BLUEPRINT              ← this workflow — run 1, before any drafting, both routes
S2   dream-catching         brainstorm → dev-capture into WRITING/SHORTS/DEV/ (route v4)
S3   synthesis + REGEN      episode-feedback, then ← this workflow again, MANDATORY (route v4)
S4   runway carve           episode-runway Pass 2 — OPTIONAL, mic route only (dec 2026-08-23)
S5   drafting engine        mic or desk
S6   dev-edit → S7 CRE's author pass → S8 blind read → S9 panel → S10 cooling read + lock
S11  QA loop → S12 line pass + EAR → S13 production (episode-runway Pass 3)
```

## When to use

CRE says "blueprint the episode," "shape the episode," or "budget the episode" on a gated WIW episode, or wants an episode's escalations and word targets laid out before a word is drafted. Runs **twice**, on both routes (route v4, 2026-09-04): **run 1 at S1.5**, after the gate and before any drafting; **run 2 at S3**, a mandatory regeneration once S2's dream-catching and `episode-feedback` have moved `premise.md`. Every regeneration rewrites above the notes rule, carrying `## Your notes` verbatim. Do NOT use it to gate or scaffold (episode-init), forge or size a premise or read corpus variety (premise-forge), carve the runway or check a finished draft (episode-runway), or score prose (scene-intensity).

## Inputs

- `premise.md` — the gate output (required; missing → not gated → episode-init).
- `notes.md` rulings block (if episode-feedback has run) · the source candidate's `triage.md` (knot, constraint, container, format measurement, **and its `## Arc chain` section when the candidate was deepened**) · `DECISIONS/_QUICK LOG.md` rows naming the episode.
- **CRE's articulated escalations** — from the premise, the rulings block, **the deepened triage's `## Arc chain`**, or the session. Nowhere else. **`draft.md` is never read** (plan-only, CRE-ruled 2026-09-03): a brought piece whose escalations live only in its prose has them stated by CRE in the run.
- The craft, **by path at run time** (CDIR-002): `KNOWLEDGE/PROCESS/CRAFT BELIEFS` ("Structure," "Character Arcs," and **"Endings"** — the chain's Outcome term is a binary and the *stance* lives in Endings; CRE's pointer, ruled 2026-09-04) and `KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework` (shape, staircase, curve vocabulary, diagnostic checklist).
- The container, **by path at run time**: `BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY` §3b — standard band edges, routes-out threshold, center. The tool carries no numbers.
- Prior shape: `EPISODES/*/premise.md` + `EPISODES/*/blueprint.md` frontmatter **only**.

> **The fourth source (CRE-ruled 2026-09-04).** `premise-forge` v2's DEEPEN mode writes CRE's Choice, Escalations with angle and failure mode, mirror, Moment of Truth and ending stance into the picked candidate's `triage.md` at pick time. That is articulated material, written down, in his words — so it is read here rather than re-asked. It does **not** widen the plan-only rule: `draft.md` stays excluded, and this source is a structural section CRE dictated, not prose. **Precedence:** where the premise and the arc chain speak to the same thing, the **premise wins** (the material moved after triage — the episode-init run-log rule). Where the premise is silent, the arc chain is **additive**, not overridden into nothing — a premise with no arc-chain fields does not null a chain the triage carries. An arc-chain field marked `[NOT NAMED — CRE]` is a hand-back exactly as if he had never named it: `[ANGLE MISSING — CRE]`, never a fill.

## Output — `blueprint.md`

Serialized frontmatter (DIR-004): `type: episode-blueprint`, episode, the four band numbers as read + `band_source`, `natural_estimate`, `scope_verdict`, `recommendation`, `ruling`, `arc_class`, `curve`, `escalation_count`, `ending_mode`, `sources_read`, `prior_shape_read`, `generated`. Body, one screen, in the episode-runway Pass 2 carve register:

```
# EP NN - TITLE · blueprint
**Knot:** his phrase from premise § a
## Cast                      name — knot-carrier | mirror | pressure | instrument   [NAME COLLISION]
## Flaw (~N)                 one sentence                                            [FAULT LINE]
## Incident (~N)             one sentence
## Choice (~N)               one sentence
## Escalations
- **E1** (~N) — sentence · angle: X · fails as: false victory | fail forward         [CURVE] [SEQUEL]
- **E2** (~N) — …                                                                    [REPEATS E1 ANGLE] [ANGLE MISSING — CRE]
## Moment of Truth (~N)      one sentence
## Climax (~N)               one sentence                                            [GATED] | [NOT GATED — CRE]
## Outcome (~N | ~0)         one sentence | inferred
## Variance                  Within: … · Across: …
## Scope                     cast N · conflict: … · span: bounded | stretches · spines N · natural ~N → verdict SHORT-FORM | OVER-BAND
## Recommendation            GO | RESHAPE | ROUTE-OUT — one-line basis. Ruling: pending | "GO — CRE, date"
---
## Your notes                CRE's; appended below the rule, never interleaved, carried verbatim on re-runs
```

**Section order** is CRAFT BELIEFS "Character Arcs." Two derivations, recorded so no session re-derives them: **Failures are not a section** — the beliefs define them as what each escalation produces, so each E line carries its failure mode; **Climax sits between Moment of Truth and Outcome** — the moment of truth is the choice, the climax the gated event (T&T shape step 4). Cast carries no budget; Outcome is `(~0)` when inferred ("outcomes are optional").

## Steps

1. **Sentinel** (`^obs-004`), then **`_CREATIVE DIRECTIVES`** before any episode or craft file (DIR-002 creative-lane load). **Attended only** — not attended → stop (DIR-012).
2. **Locate + gather** — premise, rulings block, triage (**including its `## Arc chain` when deepened**; premise wins on overlap, the chain is additive where the premise is silent), DECISIONS rows, any prior blueprint (re-run: carry `## Your notes` verbatim). Never `draft.md`.
3. **Read the craft and the container by path.**
4. **Prior shape** — `python scripts/blueprint.py shape "WRITING/SHORTS/EPISODES"` (frontmatter of premise + blueprint only; where no blueprint exists, premise § a by hand).
5. **Build** — one sentence per section from articulated material; angle per escalation in T&T / beliefs terms; missing angle → `[ANGLE MISSING — CRE]`, never supplied. **Natural weights first** (what each section needs at the size articulated; recorded in frontmatter `natural_weights`, summed as `natural_estimate`, sum-checked by the script); then target budgets summing to the center. His angle phrasing is primary, a T&T gloss optional; curve tags are the curve he stated, never per-beat curves he did not. Verdict from the natural estimate against §3b as read: at/under the upper edge → SHORT-FORM / GO; over it, under the routes-out threshold → OVER-BAND / RESHAPE; at/over the threshold → OVER-BAND / ROUTE-OUT. RESHAPE names the over dimension, never the cut; ROUTE-OUT offers §3b's routes (two-parter · TEASE long-form · SHORTS proper). Variance names repeats, never replacements. **DIR-011:** every tag resolved against the tree before it surfaces; hand-backs batched.
6. **Scaffold → fill → check → re-read** — `scripts/blueprint.py scaffold` with the numbers read in step 3 (serialized frontmatter); file-tool fills; `scripts/blueprint.py check` (sections present + ordered, budgets sum to target ±25, band verdict consistent with the numbers, no quoted speech / speech tags / multi-sentence or 45+-word movement lines, notes section last and below a rule, no placeholders); re-read through the file tools (DIR-005). The check names what it did not check (DIR-018): whether a sentence is CRE's material or an invented beat, whether two angles are the same angle, whether the natural weights are honest.
7. **The gate** — present in response-contract voice (verdict + recommendation in one sentence, then the plan, then the batched hand-backs). CRE rules; stamp `ruling`. His ruling outranks the table and is not re-asked (CDIR-009). RESHAPE → he reshapes, regenerate above the rule, re-check. ROUTE-OUT to a two-parter → each part blueprints when gated; this file stays as the record. Not ruled → `ruling: pending` is the visible deferral.
8. **Log** — `_CHANGELOG` top-insert; `_OBSERVATIONS` for tool surprises; `_CREATIVE OBSERVATIONS` (`^cobs`) for craft observations about the plan's shape, automatically (DIR-003).

## Stop conditions

Sentinel fails · not attended · no folder / ambiguous · no `premise.md` (route to episode-init) · no escalations articulated anywhere (a plan with every escalation handed back is not a plan — ask CRE to talk them through first).

## Guards (each with its reason)

- **Reads craft by path every run** — CRE's ruled craft; a copy drifts (CDIR-002; CRAFT CANON says cite the layer).
- **Creative-lane load** — Lane 5 + Lane 1 tool (DIR-002).
- **Structure only: sections, angles, budgets, flags** — AI executes, CRE creates (CDIR-001); a plan that reads like story pre-spends the mic.
- **Measures articulated escalations; names shared angles; hands back missing ones; never proposes** — the organic-process guard (CDIR-003).
- **Flow-kickstarter, not a spec** — no pass grades the draft against it; divergence is a win (DIR-017 §2). Budgets discipline the plan, not the draft.
- **No container numbers of its own** — §3b is ruled; numbers travel as script arguments and frontmatter.
- **Over band → RESHAPE / ROUTE-OUT recommended, CRE rules** — routing is his; the point of planning is to make the call before drafting.
- **Cross-episode read is `premise.md` + `blueprint.md` only** — corpus variety of condition/knot/genre is premise-forge's; two tools on one field will disagree.
- **The deepened triage is read, never re-ruled** — premise-forge captured his angles and deliberately did not judge them; this tool judges variance and deliberately does not re-capture. Each still owns one field.
- **Resolve before you flag** (DIR-011) — a tree-answered question is a one-tap confirm.
- **Serialized, parse-gated frontmatter; file-tool writes; re-read** (DIR-004, DIR-005).
- **Attended only** — angle read and route-out are judgment gates (DIR-012).

## Evals

Objective parts only (`WORKFLOWS/skills-src/episode-blueprint/evals/`): every section present and ordered, budgets sum to target, the over-band verdict and recommendation fire from the numbers, no prose-like lines, notes section last below a rule. Run: `python scripts/blueprint.py check <fixture>` — `pass-*` fixtures exit 0, `fail-*` exit 1. Craft judgments (angle repetition, route-out basis) are deliberately not eval'd; they are CRE's gate.

## Relationship to the rest of the OS

- **Upstream:** [[WORKFLOWS/premise-forge]] (S0) → [[WORKFLOWS/episode-init]] (S1 gate + scaffold).
- **Beside:** [[WORKFLOWS/episode-runway]] Pass 2 — the optional mic carve. If the desk route ever grows a mic leg the carve's optionality is void (DIR-013); the blueprint is unaffected either way.
- **Downstream:** [[WORKFLOWS/brainstorm]] + [[WORKFLOWS/dev-capture]] (S2 — run 1's `[ANGLE MISSING — CRE]` hand-backs set their agenda) → [[WORKFLOWS/episode-feedback]] (S3 — **then this workflow regenerates, mandatory in v4**) → the drafting engine → [[WORKFLOWS/episode-runway]] Pass 3 (which measures the *draft* against §3b; this tool measured the *plan*).
- **Craft read by path:** [[KNOWLEDGE/PROCESS/CRAFT BELIEFS]] · [[KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework]] · index [[KNOWLEDGE/CRAFT CANON]].
- **Container canon:** [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]] §3b.
- **Siblings / not this:** `episode-init` (gate + folder) · `premise-forge` (bag, sizing, corpus variety) · `episode-runway` (Pass 2 carve, Pass 3 check) · `scene-intensity` (realized curve on prose) · `runway-builder` (novel chapters).

## Run log

**2026-09-03 — build evals (synthetic fixtures, outside the vault).** Two with-skill subagent runs + two no-skill baselines on fixture premises (a standard-band two-hander with one repeated angle; a six-cast, two-spine overflow). With skill: 12/12 and 12/12 on the objective assertions, checker PASS first run both times; verdicts SHORT-FORM/GO (natural ~2,400) and OVER-BAND/ROUTE-OUT (natural ~4,200). Baselines: 6/12 each — the standard-band baseline invented a replacement angle, character names and a clock time; the overflow baseline recommended RESHAPE at a 4,000+ scope and listed cuts. Subagent feedback folded into the source same session: where the center lives in §3b, cite without quote marks in movement lines, § a read limited to knot/scenario/constraint, curve tag = his stated curve, his angle phrase primary, `natural_weights` frontmatter convention, hand-back bracket keyed on a trailing `CRE]`. Iteration-2 rerun owed after CRE's review of `review.html`. First live target: the EP 04 slot once its candidate is gated.
