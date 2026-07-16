---
type: workflow
name: shape-the-part
trigger: shape the part
aliases: [shape part N, separate the scenes, run the descent operator, scene-shape the part, descend the part]
inputs: [project + the part CRE names (its sequence runways, locked by the layer battery)]
outputs: [DEV/scenes/ entries for the part (SC NN, linked to SEQ); a CRE-ruled seq->scene separation; a CRE-ruled chapter map (containers cut across the scene run); handoff state for chapter-init/brief/runway; _CHANGELOG entry]
lane: fiction
status: draft
last_updated: 2026-07-15
revision_note: spec authored 2026-07-15, CRE-designed — the DESCENT OPERATOR of the dev fractal (parts/sequences <-> scenes <-> beats; chapters are containers). Runs attended, packs after 2-3 runs (dec-008 discipline). Run 1 = Part 2 (the Last Mountain, SEQ 13-22).
---

# WORKFLOW: shape-the-part

> **status: spec.** The **descent operator** — the same move at any rung of the dev fractal: shape the next rung down from the one the layer battery just locked. This spec instantiates it for **sequence → scene**. Chapters are cut LAST, as containers across the scene run — *"chapters usually are products the scenes shape inside of them; to know the shape of a chapter is to know the shapes of the scenes"* (CRE, 2026-07-15).

## The energy principle (CRE, 2026-07-15 — the battery's design rationale, verbatim-in-spirit)

*"I like that the reconciliation 2 can happen after the descent pass so I do not spend any dictation energy on words that are not in alignment. So I can dictate the acts/sequences → reconcile and rule → descent operator → reconcile and rule 2 → runways for prose — **this is my energy saved until the most effective part**."*

Dictation energy is the scarce resource; the battery + descent operator exist so it is only ever spent on prose whose entire upstream is aligned. Structure is corrected at the altitude where it is cheap; the voice is spent where it counts.

## Position in the pipeline (the fractal loop)

```
MILESTONE (layer locked by the battery: reconcile → arc-audit → author-flags → readiness)
   └─ SHAPE-THE-PART  ← this: sequences → scenes (+ chapters cut last, as containers)
        └─ battery run on the SCENE layer (bounded, small — "reconcile and rule 2")
             └─ chapter-init → brief (pulls from scene entries) → runway-builder (scenes → beats)
                  └─ DICTATION (the energy spend) → slate/cleanup → QA → land → canon-sync
                       └─ landed part = next MILESTONE → repeat, one rung down or one part forward
```

- **Not runway-builder** — that descends scene → beats (the speaking outline). This descends sequence → scenes.
- **Not chapter-init** — that scaffolds the containers this pass defines.
- **Not dev-capture** — a sequence that turns out to need real development talk before it can shape is a "flag —" or a dev-capture session, not scope creep here.
- Authority flows **up** (`_DEV_MAP`: scene = truth); this pass fills the truth rung the sequences have been standing in for.

## Steps

### Step 1 — Sentinel + scope + gate check
`_DIRECTIVES` sentinel. Resolve the part. **Precondition: the layer battery has passed the part's rung** (sequences locked — seams ruled, arcs locked, author flags harvested, readiness verdict clear). Load the part's sequence runways + the registry entries they touch + any parked items whose wake names this part (dev-readiness 5b state).

### Step 2 — Derive candidate scene seams (the runway-builder precedent: structure only, never sensation)
Per sequence, derive candidate scene boundaries **from the read's own beats** — GOAL→BUT→THEREFORE turns, location shifts, POV-time cuts the read already carries. Provenance on every candidate. **The pass proposes seams, never scene content.**

### Step 3 — The walk: CRE rules the separation
Reconcile-style, one sequence at a time: ratify / merge / split / reorder the scene seams. Batched where rubber-stamp, individual where structural (the dev-reconcile Step-4 discipline whole). A sequence may rule "one scene, whole" — that is a valid shape.

### Step 4 — Write the scene rung
`DEV/scenes/SC NN - <name>.md` per ruled scene (light, reaching-toward: the scene's **job**, its beats-so-far from the sequence read, its SEQ link, boundary tag, plants/payoffs it carries — e.g. the true-strike plant rides the SEQ 18 scene that hosts the play beat). Serialized frontmatter (DIR-004); working names router-derived, pending CRE (the `^poe-009` sub-rule). Sequence reads get a one-line pointer to their scenes (above the provenance footer, `^obs-187`).

### Step 5 — Cut the chapters (containers, LAST)
CRE rules how the scene run bundles into chapters — sized for dictation sessions, cut at the seams the scene shapes expose. Output: the part's **chapter map** (chapter → scenes → sequences), written to the part's plan surface. The map is packaging; renumbering later is cheap by design.

### Step 6 — Handoff + log
Name the handoff explicitly: battery run on the new scene layer ("reconcile and rule 2" — bounded, expect it small) → `chapter-init` per mapped chapter (**its Step 4b is the brief-fill owner**: seeds each `brief.md`'s beats/plants/seals from the chapter's mapped scene entries as tagged proposals — the seam between the scene rung and S2 is mechanical derive + CRE confirm, never re-development) → CRE confirms the briefs (S2) → `runway-builder` → dictation. `_CHANGELOG` entry; observations; follow-ups.

**The scene-layer battery profile (default until run 2 proves it — CRE-ratified 2026-07-15):** reconcile bounded to the part's scenes · the arc lens folded into the reconcile sweep as a source (arc-audit run-1's own fold-in candidate), not a separate leg · author-flags as cue-harvest only, no full interview · readiness inline (the dev-reconcile run-1 precedent). The relock must stay cheap or the energy principle breaks from the inside; an undefined battery defaults to full-size by habit.

**Close the session with the gloss question** — *"anything you glossed?"* — one line, answers feed `DEV/_AUTHOR FLAGS.md` (`^af-NNN`). Inside sessions only, never scheduled (author-flags' never-nag rule; CRE-ratified 2026-07-15 — run 1 proved the "flag —" cue misses answers spoken mid-flow).

## Scope guards (must-not)

- Never authors scene content, sensation, or prose — seams and containers only, from CRE's own captured beats (dec-001 recombination boundary).
- Never re-develops a locked sequence — structural surprises route to author-flags/dev-capture.
- One part per run (just-in-time — later parts will reshape as landed prose flows upstream; shaping ahead is a momentum tax that goes stale).
- Bounded: one sitting per part; an unresolved seam parks as a held flag on the touched sequence.

## Stop conditions

- Part's rung not battery-locked → stop, run the battery first (the energy principle depends on it).
- A sequence proves undeveloped at scene grain → pause that sequence to dev-capture; shape the rest.
- Secret encountered → DIR-001/006.

## Run log

- **Run 1 — 2026-07-16 · Part 2 (the Last Mountain, SEQ 13–22) · attended, clean.** Gate: battery-locked 07-15 (reconcile → arc-audit → author-flags → readiness READY). **17 scenes** cut from the ten reads (13→2 · 14→3 · 15→2 · 16→2 · 17→2 · 18–21→1 each · 22→2), every seam CRE-ruled in the walk — recommended path ratified throughout; SEQ 18–21 batch-ratified as one-scene-wholes (the batched-where-rubber-stamp discipline held). dec-012 parked to SC 15's grain (CRE-ruled). Chapter map: **7 containers, CH 8–14** (CRE-ruled; 17+18 and 19–21 merged thematically). Scene numbering default: SC 01–17 scoped to Part 2 (`part: 2` in frontmatter; earlier parts never scene-shaped — renumbering cheap). One sitting, no seams parked. Handoff named: scene-layer battery (lean profile) → chapter-init ×7.

## Packaging plan

Attended from this doc; after 2–3 runs (Part 2, then Part 3…) author `skills-src/shape-the-part/SKILL.md`, desktop pack, sha-verify, Save-skill (DIR-009). Run 1 = **Part 2 — the Last Mountain (SEQ 13–22)**, seeded in TASKS as the descent's first domino.
