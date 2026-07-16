---
type: workflow
name: arc-audit
trigger: audit the arcs
aliases: [run the arc audit, arc audit, run the arc pass, arc contour, run the arc contour, check the arcs, lock the arcs]
inputs: [project + the completed DEV layer CRE names (the same layer dev-reconcile just passed)]
outputs: [a SYSTEM/reports/ arc-contour report; rulable flags binned + walked; ruled annotations to DEV reads; parked forks to DECISIONS (wake convention); prose-time watch items handed to the register/blind-read passes; a _CHANGELOG entry]
lane: fiction
status: draft
last_updated: 2026-07-15
revision_note: spec authored 2026-07-15 from run 1 (Witchwood Parts/Acts, attended, CRE-directed — "my goal is having each layer locked in before descent"). Runs ATTENDED + manual until 2-3 live runs prove the lenses; packages after (dec-008 episode-runway discipline). Run 1 report - SYSTEM/reports/2026-07-15-witchwood-arc-contour-report.md.
---

# WORKFLOW: arc-audit

> **status: spec.** Run attended from this doc; pack after 2–3 runs. **The SHAPE leg of the layer-lock battery** — dev-reconcile judges what's *wrong in the facts*; this pass judges whether the layer *works as arcs*. Read-only through the report; writes only CRE-ruled annotations.

## When to use

A layer has just passed **dev-reconcile** (continuity seams ruled) and CRE wants the layer **locked before descent** — character arcs, emotional arcs, pacing shape, POV architecture, and taste-anchor fidelity verified at altitude, where a missing beat moves in one edit. Trigger: "audit the arcs," "run the arc pass," "lock the arcs."

## Position in the pipeline

```
dev-capture → dev-capture-audit → dev-reconcile → ARC-AUDIT ← this pass
                                                      └─ dev-readiness (exit gate: forward gaps + ripe-fork triage)
                                                           └─ descend (sequence → scene)
```

- **Not dev-reconcile** — that rules contradictions/redundancy/stranded setups (backward seams). This reads the *same* layer as shape: do the transformations have their beats, in order, complete?
- **Not scene-intensity** — that grades PROSE pacing (scene-local + carried dread). This pass only reads contour at altitude and *hands off* pacing exposures to a scene-intensity run at drafting; it never scores outlines as if they were prose (false-confidence guard).
- **Not workshop-chapter / blind-read** — those are chapter-scoped, downstream of a draft. Register-execution risks found here (sentiment heat, Death's wordlessness at the line level) are **watch items handed forward**, never dev-layer fixes.
- Feeds **dev-readiness**: arc flags that park become forks/holds the readiness verdict must see.

## Steps

### Step 1 — Sentinel + scope
`_DIRECTIVES.md` sentinel (`^obs-004`). Resolve project + layer. Precondition: **dev-reconcile has passed this layer** (running the shape lens over unreconciled facts wastes the walk — seams masquerade as arc gaps). Load `_DEV.md` (the taste anchor is the measuring stick), `project.md`, and the layer's reads.

### Step 2 — Extraction fan-out (read-only)
Parallel read-only subagents by range (run 1: three agents over ~25 reads each). Each returns ONE compact row per sequence — `SEQ | POV (only as the read states it; never fabricate) | emotional register in 3–6 words USING THE READ'S OWN LANGUAGE | strand beats with short quotes` — plus three sections: strand state at range exit · crossing/teaching-beat evidence · register-drift notes against the anchor's tone targets verbatim.

**Strand codes are project-derived, not fixed:** name one code per transformation track the taste anchor claims (run 1: H present / H-past / B / D / W-presence-contour). The anchor's claimed arcs define what to trace — the pass verifies the anchor against the spine, both directions.

### Step 3 — Stitch + compile the report
The orchestrator stitches strand traces across range boundaries and compiles, in order:
1. **Verdict line** — arc-complete or not, one line.
2. **Strand traces** — each transformation's beats verified on the spine with SEQ numbers + quotes; each strand's **completion beat named** (or its absence flagged).
3. **POV architecture** — the map, plus any structural observation (who never holds POV; where a strand's POV ends vs where its arc ends).
4. **Emotional contour by part** — from the reads' own register language, checked against the anchor's felt shape. Pacing exposures noted → handed to scene-intensity at drafting, never graded here.
5. **Taste-anchor fidelity** — anchor claims supported/unsupported on the spine, both directions.
6. **RULABLE FLAGS** — binned per the dev-reconcile convention: QUICK (one-word ratifies — "deliberate design?") / STRUCTURAL (an uncarried beat, a turn with no carrier — CRE rules where it lives or parks it) / prose-time WATCH items (no bin; named recipients: register-pass, blind-read, scene-intensity).

Report → `SYSTEM/reports/<date>-<project>-arc-contour-report.md`. **The report describes; it never prescribes.** When flagging an uncarried beat, candidate carriers may be listed ONLY from beats already captured in the reads (recombination boundary, dec-001) — never invented.

**Resolve-before-flag (`^obs-188`, CRE-directed 2026-07-15):** before any finding reaches the RULABLE FLAGS section, research it against the tree — registry entries, rulings floors, `DECISIONS/`, the taste anchor's own text. A question the tree decisively answers presents as "resolved against [[Entry]] — confirm," never as an open flag. Only tree-silent findings cost CRE a ruling.

### Step 4 — The walk (CRE rules)
Same discipline as dev-reconcile Step 4: **batch the ratifies** (design-confirmation QUICKs go en-bloc with a pull-out option), walk STRUCTURAL finds individually **with the evidence quoted** (an unrulable flag is an under-evidenced flag). Expect rebins. Nothing writes until ruled.

### Step 5 — Write ruled state
Ruled annotations into the touched reads (file tools; notes ABOVE the provenance footer, `^obs-187`); the report updated to its ruled state; parked forks → `DECISIONS/` in the wake convention (`decision-helper (ripe)` / `CRE-articulation` / `milestone: <name>`); watch items recorded with their named prose-time recipient. `_CHANGELOG` entry; observations; backlog follow-ups. **Close with the gloss question** — *"anything you glossed?"* — answers feed `DEV/_AUTHOR FLAGS.md`; inside sessions only, never scheduled (CRE-ratified 2026-07-15).

## Scope guards (must-not)

- Never proposes story content; candidate carriers for an uncarried beat come only from CRE's own captured beats, with provenance.
- Never grades outline pacing as prose pacing — contour observations at altitude, scoring only via scene-intensity on drafts.
- Never writes REFERENCE/, draft.md, or any prose file.
- Never resolves a held flag from inference (`^poe-010`); a deliberate hold ("preserve the kind") is reported as held, never re-opened.
- Bounded: one session per layer; a finding that outgrows the session parks (the dev-reconcile bounded-gate rule applies whole).

## Stop conditions

- Layer not yet dev-reconciled → stop, run the seams first.
- No DEV tree / layer empty → nothing to audit.
- Secret encountered → DIR-001/006.
- Session ends mid-walk → unruled flags persist in the report (status noted); the pass resumes from the report, never re-extracts.

## Run log

- **Run 1 — 2026-07-15, Witchwood Parts/Acts (SEQ 01–75), attended.** Verdict: arc-complete → arc-locked same session. 4 rulable flags, all ruled (F1 STRUCTURAL: the boy's despair→readiness turn was uncarried — CRE ruled the game/reunion IS the turn, annotated SEQ 69/70; F2–F4 ratified as design: boy-never-holds-POV withholding, the Part-7 dread-gap juxtaposition, the prologue's loud-Death inversion). 3 watch items handed to prose passes. Proved: the extraction template, the anchor-as-measuring-stick, the binning, and that the pass generates reconcile-class rulable flags. Report: `SYSTEM/reports/2026-07-15-witchwood-arc-contour-report.md`.

## Packaging plan

Attended runs from this doc; after 2–3 runs (next: the Act-2 descent's scene layer, or another project's spine) author `skills-src/arc-audit/SKILL.md`, desktop `pack-skills.ps1`, sha-verify, Save-skill (DIR-009). A possible later orchestrator ("lock the layer": dev-reconcile → arc-audit → dev-readiness) stays out of scope until both legs are packaged.
