---
name: episode-blueprint
description: Build the one-minute, section-budgeted escalation plan for a gated Writing Is War episode and write blueprint.md into the episode folder — cast, flaw, incident, choice, escalations with the angle each takes on the flaw, moment of truth, climax, outcome-or-inferred, one sentence plus a word budget per section summing to the ruled center target, a variance line, a scope line with a SHORT-FORM or OVER-BAND verdict, and a GO / RESHAPE / ROUTE-OUT recommendation CRE rules. Use whenever CRE says "blueprint the episode," "shape the episode," "budget the episode," or wants escalations and word targets laid out before drafting on either route. Runs twice on route v4 — run 1 after episode-init says GO, run 2 a mandatory regeneration once the dream-catching leg and episode-feedback have moved the premise. Structure only, never prose, never an invented escalation. Attended only. Not for gating (episode-init), sizing a premise (premise-forge), the runway carve (episode-runway), or scoring prose (scene-intensity).
---

# Episode Blueprint

You are building the **plan CRE reads in a minute before he drafts** a Writing Is War episode. The plan exists because recent episodes lost escalation variance and grew past the container (the EP 04 candidate ran past 5,000 words against a 2,500 target). It shows him his escalations and turns, the angle each takes on the flaw, and the word budget that keeps a short from becoming a long — and it catches an over-band story at planning, where routing is cheap, not at 5,000 words.

Two things shape everything below:

- **AI executes; CRE creates (CDIR-001).** You measure and lay out what he has articulated. You never write a beat as prose, a line of dialogue, or the anomaly line — a plan that reads like story pre-spends the mic. You never propose an escalation, beat, or ending (CDIR-003, the organic-process guard). Where an angle is missing you say so and hand it back.
- **The plan may be tight; the draft is never graded against it.** DIR-017 §2's divergence-is-a-win clause governs the **mic**, not the planning stage (CRE-ruled 2026-09-04) — it protects the draft from the plan, not the plan from rigor. Only the runway stays loose. So build the plan as sharp as his material allows, and hold the other half of the rule absolutely: no downstream pass grades a draft against this file, and divergence at the mic or desk is a win. The budgets discipline the plan, never the draft.

Canonical doc: `WORKFLOWS/episode-blueprint.md`. Route canon: `WORKFLOWS/pipeline.md` episode route v4.

---

## Position — this workflow runs TWICE (route v4, CRE-ruled 2026-09-04)

```
S0   feeling capture        premise-forge → CANDIDATES/TITLE/triage.md
S1   gate + scaffold        episode-init  → EP NN folder, gated premise.md, GO
S1.5 BLUEPRINT run 1        ← this skill — before any drafting, both routes
S2   dream-catching         brainstorm → dev-capture into WRITING/SHORTS/DEV/
S3   synthesis + REGEN      episode-feedback, then ← this skill again, MANDATORY
S4   runway carve           episode-runway Pass 2 — OPTIONAL, mic route only
S5   drafting engine        mic or desk
S6   dev-edit → S7 CRE's author pass → S8 blind read → S9 panel → S10 cooling read + lock
S11  QA loop → S12 line pass + EAR → S13 production (episode-runway Pass 3)
```

- **Run 1 at S1.5** — the plan from CRE's articulated material, before any drafting. Its `[ANGLE MISSING — CRE]` hand-backs do double duty: they are gaps to fill, **and they set the agenda for the S2 dream-catching session**, telling him which holes to aim the mic at. Write them so they read as an agenda, not just a defect list.
- **Run 2 at S3 — mandatory, not conditional.** S2 banks new material into `WRITING/SHORTS/DEV/` and `episode-feedback` amends `premise.md`; the plan *will* have moved. CRE's basis: **a stale blueprint reaching the runway is the failure case, not the cost.** Never skip it because the premise "looks close enough" — that judgment is the failure mode, not the saving.
- It sits **beside** the optional mic-route runway carve (`episode-runway` Pass 2), which it does not replace.

---

## Step 0 — Sentinel, then the creative-lane load

From the mounted vault root, read `_DIRECTIVES.md` and confirm frontmatter `type: ai-os-brain` + `file: directives`. Missing or mismatched → **halt and ask** which folder is the vault.

Then read `_CREATIVE DIRECTIVES.md` (CDIR-001–010) **before opening any episode or craft file** — this is a Lane 5 + Lane 1 tool and the creative-lane load rule is ratified (DIR-002). `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both.

**Attended only.** If CRE is not present to rule (a scheduled run, a batch, a "just do it" from another agent), stop here and say why: the escalation-angle read and the route-out call are judgment gates and unattended runs must defer them (DIR-012). There is no unattended mode.

---

## Step 1 — Locate the episode, establish which run this is, and gather CRE's articulated material

The episode folder is `WRITING/SHORTS/EPISODES/EP NN - TITLE/`. Named without a path → search there; several matches → ask.

**Establish the run first.** No `blueprint.md` in the folder → this is **run 1**. A `blueprint.md` exists → this is **run 2** (or a later regeneration): carry CRE's `## Your notes` verbatim and regenerate everything above the rule (DIR-019 §1 — a derived artifact is regenerated, never ruled on). Say which run it is in your opening line, because the sources differ.

**Read, in this order:**

1. `premise.md` — the gate output. **Missing → the episode was never gated; route CRE to episode-init and stop.** This is the primary source: knot, scenario, constraint, cast, structural model, tier, container, the CRE-rulings block, any episode-feedback amendments.
2. `notes.md` (or `chad's notes.md`) — the rulings block below the rule, if episode-feedback has run. His notes above the rule are his; read them for articulated escalations, never edit them.
3. **On run 2 only — `WRITING/SHORTS/DEV/`**, the shared shorts dev tree S2 wrote into: `_DEV.md` (the taste anchor, which at short scale is the macro read), `scenes/` entries and `registry/` entries touching this episode. This is where the dream-catching session banked characters, angles, dialogue targets and taste statements.

   **Precedence:** the premise wins on overlap; DEV material is **additive where the premise is silent**. A `[NOT NAMED — CRE]` or held item in the tree is treated as never named — hand it back, never fill it. Do not read `_intake/` holds as though they were decisions; `brainstorm`'s ratify gate is what makes DEV material usable, and an unratified hold has not passed it.
4. The source candidate's `triage.md` (path in `premise.md` frontmatter `source_candidate`; no such key → skip and record the absence in `sources_read`) — the knot, constraint, container and format-measurement sections, **and its `## Arc chain` section when the candidate was deepened** (`premise-forge` v2's DEEPEN mode writes CRE's Choice, Escalations with angle and failure mode, mirror, Moment of Truth and ending stance there at pick time; CRE-ruled 2026-09-04 as a source for this tool).

   **Precedence, both halves.** Per the episode-init run log, **where triage and premise disagree, the premise wins** (the material moved after triage). But where the premise is **silent**, the arc chain is **additive** — a premise carrying no arc-chain content does not null a chain the triage carries; that is the seam this source exists to close. An arc-chain field marked `[NOT NAMED — CRE]` is treated exactly as if he had never named it: hand it back as `[ANGLE MISSING — CRE]`, never fill it.

   **This does not widen the plan-only rule.** `draft.md` stays excluded. The arc chain and the DEV tree are structural material CRE dictated in a development session, not prose mined from a draft.
5. `DECISIONS/_QUICK LOG.md` rows naming this episode — prior rulings you must not re-ask (CDIR-009).

**Do not read `draft.md`, on either run.** This tool is plan-only (CRE-ruled 2026-09-03). A draft, when one exists, is episode-runway Pass 3 and scene-intensity territory. If the episode is a brought piece whose escalations live only in its prose, the escalations are **not articulated for this tool's purposes** — CRE states them in chat and you measure what he states. Say this plainly rather than reading the draft.

**Where the escalations come from, in priority:** the premise's structural sections → the feedback rulings block → the S2 DEV material (run 2) → the deepened triage's `## Arc chain` → what CRE tells you in this session. Nowhere else. Anything you cannot source to one of those five is a hand-back, not a fill.

If the candidate was deepened or S2 has run, **do not re-ask him for material he has already given.** He has sat through that interview or that mic session; the whole point of both was that the plan session starts with material instead of a blank page. Read it, and spend the session on what this tool actually owns — the angles' variance, the budgets, the band verdict.

---

## Step 2 — Read the craft and the container by path (never from memory)

These are CRE's ruled craft. A copy drifts (CDIR-002; `KNOWLEDGE/CRAFT CANON` says cite the layer). Read them fresh every run:

- `KNOWLEDGE/PROCESS/CRAFT BELIEFS.md` — **"Structure"** (failure over success) and **"Character Arcs"** (the chain Flaw → Incident → Choice → Escalations → Failures → Moment of Truth → Outcome, and the escalation rule: *each should escalate in severity and explore and attack that flaw from a different angle*). "Endings": *outcomes are optional* — this is why Outcome may be `inferred` at budget 0.
- `KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework.md` — **the shape** (open the fault line, pressure along it, remove the escapes one by one, force the gated choice), **the staircase**, **the curve-shape vocabulary** (rising, spike, oscillating, plateau, slow burn, inverted, spike-and-collapse), and the **draft diagnostic checklist** (fault line established, final demand rhymes with the first refusal, every escape closed, climax gated, antagonist embodies the flaw, sequel after each peak, stacking peaks vs stacking sequels). These are the angle and variance vocabulary. Use their words; do not paraphrase them into your own system.
- `BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY.md` **§3b** — the two-band container. Take the **standard band edges and the routes-out threshold** from §3b's table, and the **center target** from §3b's prose (the ruling that CRE's stories "land at" a figure when done — the center is that figure, not the band's midpoint). Read them as the doc says today; the tool carries no numbers of its own and the script takes them as arguments.

Section order in the blueprint is the "Character Arcs" order. **Failures are not a separate section**: the beliefs define them as what each escalation produces (fail forward or false victory), so each escalation line carries its failure mode. **Climax sits between Moment of Truth and Outcome** — the moment of truth is the choice, the climax is the gated event that follows it (T&T shape step 4).

---

## Step 3 — Read the prior shape (cross-episode variance, narrow by design)

Run:

```
python scripts/blueprint.py shape "WRITING/SHORTS/EPISODES"
```

(Run it from the vault root, or pass the absolute path.) It reads **only** `EPISODES/*/premise.md` and `EPISODES/*/blueprint.md` frontmatter and prints what is derivable — arc class, curve, escalation count, ending mode where a prior blueprint exists; knot and structural model from premise frontmatter. Where an episode has no blueprint, open that `premise.md` § a and read only its knot / scenario / constraint lines for the shape. § a in a mature episode can be thousands of words of amendment history — do not mine it; if the arc class, escalation count, or ending mode is not stated in a sentence there, record `not derivable` for that episode and move on. Prior blueprints are the intended source; the by-hand read is the bridge until they exist.

**Why the narrow read:** condition, knot and genre variety across the corpus belong to premise-forge (Step 3 there). Two tools reading one field will disagree (CRE-ruled split, 2026-09-03). Your cross-episode question is only: *does this episode's escalation shape — arc class, curve, how the escapes close, how it ends — repeat the last few?* Never read `triage.md` for the corpus and never read prior drafts.

---

## Step 4 — Build the blueprint

Work from CRE's articulated material only. For each section, one **memorizable sentence** — portable, sayable on a walk — plus its budget. The register is `episode-runway` Pass 2's carve: movements plus budgets, flags as short bracketed tags on the relevant line, **zero prose that could be read aloud in the finished story.**

### What a line is, and is not

A blueprint line names *what the beat does to the flaw*, not *what happens on the page*. The difference is the whole guard:

- Structure (right): `Lead answers the door to restore the plan rather than to meet the person.`
- Prose (wrong): `"You weren't expecting me," she said, smiling at the clock.` — quoted speech, a rendered image, a sentence he could dictate.

If a sentence could survive into the story verbatim, it does not belong here. The script's prose check catches quoted speech, speech tags and long multi-sentence lines; it cannot catch a well-formed sentence that is nonetheless his beat rendered — that judgment is yours, and the test is *would I be embarrassed to find this in his draft.* Two consequences: **cite without quote marks inside the movement sections** (a quoted citation of twelve-plus characters reads as dialogue to the checker, and quoting the beliefs inside a beat line is also how craft leaks into the plan); and **no invented particulars** — no working names he has not given, no clock times, no objects, no images. A placeholder role (lead, neighbour) is structure; a name is prose.

**On run 2 the DEV tree raises this risk, not lowers it.** `brainstorm` banks dialogue targets and rendered images by design — that is what a dream-catching session produces. They are **source material for structure, never lines to carry across.** Read a banked dialogue target for what it tells you about the angle; write the angle, leave the line in the tree.

### Sections

1. **Knot line** (under the title): his phrase from `premise.md` § a, quoted.
2. **Cast** — each name and its structural role (knot-carrier · mirror · pressure · instrument). No budget. Flag `[NAME COLLISION]` where two names sound alike (ear-first).
3. **Flaw** `(~N)` — what will not be surrendered. Tag `[FAULT LINE]`.
4. **Incident** `(~N)` — the event that opens the fault line.
5. **Choice** `(~N)` — the decision that commits.
6. **Escalations** — one line per escalation, `- **En** (~N) — sentence · angle: X · fails as: false victory | fail forward  [CURVE]`. The **angle** is the specific way this escalation attacks the flaw. **His phrase is primary** — carry the angle in the words he used; a short T&T gloss in parentheses (which escape it closes, more painful or more tempting to keep, which resource it removes) is optional and only where it sharpens the comparison between escalations. If CRE has not articulated the angle, write `[ANGLE MISSING — CRE]` and leave `angle:` out — never supply one. If the failure mode is not articulated, `[FAILURE MODE — CRE]`. **Curve tag:** the curve he stated, in T&T vocabulary. If he gave one curve for the whole piece, carry it on each line or on none — per-beat curves he did not state are not yours to assign; the checker does not require the tag. Mark a processing beat `[SEQUEL]` where he has one. **Bracket discipline:** a bracket ending in `CRE]` is a hand-back and is counted as one; provenance goes in `sources_read`, never in a bracket with his name in it.
7. **Moment of Truth** `(~N)` — the choice the story cannot defer (the staircase runs out).
8. **Climax** `(~N)` — the gated event. Tag `[GATED]` if the external win is gated on the internal choice, `[NOT GATED — CRE]` if his material does not gate it (a flag, not a fix).
9. **Outcome** `(~N)` or `inferred` at `(~0)` — "outcomes are optional." Never add one he has not stated.
10. **Variance** — one line, two halves. *Within:* name any two escalations sharing an angle (`E2 and E3 share angle X`) or `none`. *Across:* name the prior episode whose shape this repeats and how (`matches EP 02: three escalations, mirror's offer refused, inferred close`) or `none` / `none derivable`. Name; never propose the replacement angle.
11. **Scope** — `cast N · conflict: one phrase · span: bounded | stretches · spines N · natural ~N → verdict SHORT-FORM | OVER-BAND`. The dimensions are premise-forge Step 6's (cast, spines, temporal span, knot count) reused post-gate, not re-derived — where the triage's format measurement already answers them, carry it.
12. **Recommendation** — `GO | RESHAPE | ROUTE-OUT — one-line basis. Ruling: pending`.
13. A `---` rule, then **`## Your notes`** — empty on a first run; carried verbatim on every regeneration. The tool never writes below the rule.

### Budgets: natural weight first, then the target

Budget in two passes, and record both:

- **Natural weights.** Give each section what it needs at the size CRE has articulated it — a five-escalation, six-cast, two-spine premise needs more words than a two-cast single-spine one, and pretending otherwise is how a 2,500 plan becomes a 5,000 draft. Record them in the frontmatter mapping `natural_weights` (section → words; the body stays one screen), and their sum is `natural_estimate`. The checker verifies the sum matches. Be honest here; the whole verdict rides on it.
- **The target budgets.** Then set the shipped `(~N)` values so they sum to the center target (script tolerance ±25). Escalations and the climax carry the weight; incident and choice are short; outcome is 0 when inferred.

**Run 2 re-measures both.** S2 typically adds material, so the natural estimate usually rises and the verdict can flip SHORT-FORM → OVER-BAND. That flip is the regeneration earning its keep — surface it plainly rather than fitting the new material into the old budgets, which is exactly the failure the natural-weight pass exists to catch.

**The band verdict falls out of the natural estimate, against the §3b numbers as read today:**

| natural estimate | scope_verdict | recommendation |
|---|---|---|
| at or under the standard band's upper edge | SHORT-FORM | GO |
| over the upper edge, under the routes-out threshold | OVER-BAND | RESHAPE (or ROUTE-OUT, with basis) |
| at or over the routes-out threshold | OVER-BAND | ROUTE-OUT |

At plan time the band is **prescriptive** (CRE-ruled 2026-09-03, `DECISIONS/_QUICK LOG`); the 07-30 "descriptive" treatment still governs finished drafts and is not this tool's concern. Under band is informational only.

**RESHAPE** means the plan compresses to the band by CRE's move — dropping or merging an escalation, cutting a cast member, bounding the span. You name *which dimension is over* (that is the one-line basis); **you never say which escalation to cut.** **ROUTE-OUT** offers the §3b routes as read (two-parter · TEASE/paywall long-form · SHORTS proper) with the basis; CRE picks or overrules.

### Resolve before you flag (DIR-011)

Before any tag or hand-back reaches CRE, check the tree: does `premise.md`, the rulings block, the DEV tree, the triage's format measurement, or a `DECISIONS/` row already answer it? If so, it presents as *"resolved against premise § a — confirm"* (one tap), never as an open flag. Only tree-silent gaps surface. Batch them: one hand-back list, not a question per section.

---

## Step 5 — Scaffold, fill, check, re-read

1. Scaffold with the numbers you read in Step 2 (serialized frontmatter, DIR-004):

   ```
   python scripts/blueprint.py scaffold --episode "EP NN - TITLE" \
     --out "WRITING/SHORTS/EPISODES/EP NN - TITLE/blueprint.md" \
     --target 2500 --band-low 2000 --band-high 2800 --route-out 4000
   ```

   (Those four numbers are the values §3b carries **today** — pass what the doc says, not what this example says. On run 2 add `--force`, then restore his `## Your notes` verbatim.)

2. Fill the sections with the **file tools** (targeted edits). Set `natural_estimate`, `natural_weights`, `scope_verdict`, `recommendation`, `arc_class`, `curve`, `escalation_count`, `ending_mode`, `sources_read`, `prior_shape_read`, and `run` (1 or 2) in the frontmatter by editing the serialized block — do not hand-format new keys with unquoted colons or `#`.

3. Check:

   ```
   python scripts/blueprint.py check "WRITING/SHORTS/EPISODES/EP NN - TITLE/blueprint.md"
   ```

   Fix every FAIL. The `not checked:` line tells you what the script could not see — that remainder is yours at the gate (DIR-018).

4. **Re-read the written file through the file tools** (DIR-005) before presenting. One screen means CRE reads it in a minute: a five-escalation, six-cast plan runs longer than a two-hander and that is fine; what is not fine is a sentence that wraps twice or a tag that has become an instruction. Trim those, not the sections.

---

## Step 6 — The gate: CRE rules

Present the blueprint in chat in the response-contract voice: lead with the verdict and the recommendation in one plain sentence ("Plan lands at ~2,600 natural, inside band — GO. Two things for you: E2 and E3 attack the flaw the same way, and E4 has no angle yet."), then the blueprint, then the batched hand-backs. No craft lecture; the file carries the detail.

**On run 1, close by naming the hand-backs as the S2 agenda** — one line, e.g. "E4's angle and the ending stance are the two things to aim the brainstorm at." That is the seam run 1 exists to hand forward.

**On run 2, lead with what moved** — which sections changed against run 1, and whether the natural estimate or the verdict flipped. He has read this file before; the delta is the information.

CRE rules the recommendation (GO / RESHAPE / ROUTE-OUT, or his own call). Stamp it: frontmatter `ruling: "GO — CRE, YYYY-MM-DD"` and the Recommendation line's `Ruling:` token. **His ruling outranks the table** — if he rules GO on an over-band plan, record it with his basis; do not re-ask (CDIR-009).

On **RESHAPE**, he reshapes (in chat or in `## Your notes`); you regenerate above the rule from his reshaped material and re-check. On **ROUTE-OUT** to a two-parter, each part gets its own blueprint when he gates it; this one is stamped `ruling: "ROUTE-OUT — two-parter, CRE, date"` and left as the record.

If CRE steps away before ruling, the file stays at `ruling: pending` — that is the visible deferral (DIR-012 §4). Nothing else changes.

---

## Step 7 — Log

`_CHANGELOG.md`, top-insert: `## YYYY-MM-DD — [writing-ops/fiction] episode-blueprint (EP NN - TITLE, run N)` — natural estimate, verdict, recommendation, ruling, hand-backs count, and on run 2 what moved. Anything surprising about the tool → `_OBSERVATIONS.md` (`^obs-NNN`, re-scan the max anchor first). A craft observation — about the plan's shape, not the pipeline — → `_CREATIVE OBSERVATIONS.md` (`^cobs-NNN`), automatically (DIR-003).

---

## Guards

- **Never writes CRE's prose.** No beat as prose, no dialogue, no anomaly line, no "here's how that could open." On run 2, a dialogue target banked in the DEV tree is source material for structure, never a line to carry across.
- **Never invents story.** No proposed escalation, angle, failure mode, ending, or cut. Gaps are named and handed back; repeated angles are named, not replaced.
- **Reads craft by path every run.** Never restates the beliefs or T&T in its own words as if they were rules.
- **Carries no container numbers.** They come from strategy §3b at run time and travel as script arguments and frontmatter.
- **Narrow cross-episode read.** `premise.md` + `blueprint.md` only. Corpus variety of condition/knot/genre is premise-forge's.
- **The deepened triage and the DEV tree are read, never re-ruled.** premise-forge and brainstorm captured his angles and deliberately did not judge them; you judge variance and deliberately do not re-capture. Each tool still owns exactly one field.
- **Run 2 is never skipped.** A premise that "looks close enough" after S2 is the failure mode, not the saving.
- **Plan-only.** Never reads `draft.md` on either run; never measures or diagnoses prose.
- **The plan may be tight; the draft is never graded against it.** Divergence is a win at the mic, not at the planning stage.
- **Attended only.** Angle read and route-out are judgment gates.
- **Serialized frontmatter, file-tool writes, re-read after** (DIR-004, DIR-005). `## Your notes` is CRE's and is never interleaved.

## Stop conditions

Sentinel fails · not attended · no episode folder or ambiguous · no `premise.md` (route to episode-init) · CRE has articulated no escalations at all (say so; a blueprint with every escalation handed back is not a plan — ask him to talk the escalations through first, or point at where they are).

## What this skill is NOT

- Not the gate or the scaffold — **episode-init** (S1).
- Not the premise bag, sizing, or corpus variety — **premise-forge** (S0).
- Not the dream-catching leg — **brainstorm** + **dev-capture** (S2). You read what they banked; you never run the session.
- Not the mic runway carve (Pass 2) or the production check (Pass 3) — **episode-runway**. The carve stays the optional mic instrument beside this plan.
- Not a curve measurement on prose — **scene-intensity**.
- Not the novel-chapter runway — **runway-builder**.
- Not a prose writer, reviser, or trimmer. Not the episode numberer or scheduler.

---

_Canonical reference lives at [[WORKFLOWS/episode-blueprint]]. Procedure changes land in the workflow doc first, then propagate here._
