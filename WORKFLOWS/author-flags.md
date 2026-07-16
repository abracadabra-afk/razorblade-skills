---
type: workflow
name: author-flags
trigger: harvest my flags
aliases: [run the author flags, author flags, harvest my holds, what am I holding, dump my flags, my concerns list]
inputs: [project + CRE's held concerns (spoken in the harvest interview, or accumulated in DEV/_AUTHOR FLAGS.md via the dictation cue)]
outputs: [author flags captured verbatim (^af-NNN ledger entries); per-flag tree-research resolutions; cascade-weight classifications; routes (resolved-confirm / DECISIONS fork with descent-keyed wake / deliberate hold to _DEV.md / build-task); a _CHANGELOG entry]
lane: fiction
status: draft
last_updated: 2026-07-15
revision_note: spec authored 2026-07-15, CRE-directed — "in the interests of momentum there are areas that I glossed over… my list of flags should be analyzed/decided/ruled before descent." The AUTHOR-side complement to dev-readiness (which is referenced-only and confesses this blind spot every run). Type specimen - the Witch ontology (dec-013), mis-parked to act revision when its cascade shapes Vale-interior scene design. Runs attended; packs after 2-3 runs (dec-008 discipline). Pilot = this same session.
---

# WORKFLOW: author-flags

> **status: spec.** The fourth leg of the layer-lock battery — **the head**. Every other pass reads the tree; this one harvests what never reached it: the concerns CRE glossed over to protect momentum. It exists because dev-readiness's mandatory blind-spot caveat (*"pieces you've discussed but not yet captured won't appear here"*) named this gap every run and nothing owned closing it.

## When to use

At a **layer boundary**, after dev-reconcile + arc-audit and before the dev-readiness gate — or any time CRE says "harvest my flags" / wants his held-concerns list emptied and triaged. Also passively, any time: the dictation cue ("flag —" / "concern —" / "I glossed —") appends to the ledger mid-momentum without breaking flow.

## Position in the pipeline

```
dev-reconcile (seams) → arc-audit (shape) → AUTHOR-FLAGS (the head) → dev-readiness (the gate sees everything) → descend
```

- **Not dev-readiness** — that detects what the tree references; this harvests what only CRE holds. Together they close the referenced-only blind spot.
- **Not decision-helper** — this is the *feeder* (like dev-reconcile): it captures, researches, classifies, and routes; the helper measures the forks one at a time.
- **Not dev-capture** — dev-capture routes development *content*; this routes development *worries*. A flag that turns out to be content ("actually, here's the answer…") hands off to dev-capture mid-harvest.

## The two surfaces

**1. The ledger (standing, write-side): `DEV/_AUTHOR FLAGS.md`.** Append-only `^af-NNN` entries, each CRE's concern **verbatim** — one spoken sentence suffices. Fed by the `_DEV_MAP` cue ("flag —" / "concern —" / "I glossed —") so capture never costs momentum, or by chat.

**2. The harvest interview (the skill, at boundaries).** The pass ASKS — *"what did you gloss over to keep moving on this layer?"* — then works the accumulated + newly-spoken list. Interview discipline: open questions, one at a time, never leading; CRE's phrasing is the record.

**3. The session-close micro-harvest (CRE-ratified 2026-07-15).** Every dev/battery session (dev-capture, dev-reconcile, arc-audit, shape-the-part) closes with one line — *"anything you glossed?"* — and any answer lands in the ledger verbatim (`^af-NNN`). Rationale: pilot run 1 showed 6 of 10 flags were **uncaptured answers** that aged ~3 weeks because the "flag —" cue misses answers spoken mid-flow. Inside sessions only — this is a closing line in work already underway, never a scheduled prompt (the never-nag rule holds).

## Per-flag processing (the pipeline each flag runs)

1. **Capture verbatim** → `^af-NNN` (his words, never paraphrased into blandness).
2. **Resolve-before-flag research (`^obs-188`)** — registry, rulings floors, `DECISIONS/`, the anchor. Some of CRE's worries his own material already answers; those present as *"resolved against [[Entry]] — confirm,"* and the relief is the deliverable.
3. **Cascade-weight classification** — the load-bearing step, from the type specimen: a flag's rank is **how much downstream design its answer shapes, and WHICH descent it blocks.** (The Witch's foundation → how the Vale's darkness operates → every Vale-interior scene. Cascade-bearing ≠ big; a huge question with no downstream dependents can wait.) Each flag gets: *cascade: none / local (one sequence's grain) / layer (an act's scenes) / global (world-operating rules)* + *blocks: <the specific descent>*.
4. **Route** (proposed by the pass, ruled by CRE):
   - **Tree-answered** → resolved-confirm; stale pointers synced.
   - **Fork-shaped** → `DECISIONS/` entry in the wake convention, **wake keyed to the descent the cascade blocks** — never a vaguer seat. A blend CRE articulated is a measurable branch (dec-001 recombination boundary).
   - **Deliberate hold** → preserve the kind; recorded in `_DEV.md` § Open questions (the anchor's existing home for held ambiguity).
   - **Build-task** → a placed dictation/editing task (the dec-009/010 class).
   - **Content, not worry** → hand to dev-capture; it was development talk wearing a flag's clothes.
5. **Write ruled state** — ledger status per flag (`held / routed:dec-NNN / resolved / captured`), DECISIONS entries, `_DEV.md` holds. File tools; DIR-004/005; notes above provenance footers (`^obs-187`).

## Scope guards (must-not)

- **Never answers a flag.** It researches, classifies, and routes; the answer is CRE's, at the seat the route names. (Organic-process guard — same line as dev-readiness's surface-never-fill.)
- **Never invents branches** — forks carry only CRE's articulated options/blends, with provenance.
- **Never nags.** Unharvested concerns stay in CRE's head until HE opens the interview or speaks the cue; no scheduled prompting, no guilt (restart-friendly, the day-launch principle).
- Bounded: one sitting per boundary; a flag that outgrows the sitting routes to DECISIONS and the interview moves on.

## Stop conditions

- Secret/credential in a flag → DIR-001/006.
- CRE stops mid-list → harvested flags stay routed; the rest of the list stays his; resume any time (append-only ledger, no re-interview of settled items).

## Run log

- **Run 1 (pilot) — 2026-07-15, Witchwood, at the Parts/Acts→descent boundary.** Type specimen: the Witch ontology (`^af-001` → dec-013, wake re-ruled from "act revision" to "before the Vale-interior scene descent" on cascade grounds — the mis-park that motivated the skill). Harvest run in-session; see the ledger + `_CHANGELOG`.

## Packaging plan

Attended runs from this doc; after 2–3 runs author `skills-src/author-flags/SKILL.md`, desktop pack, sha-verify, Save-skill (DIR-009). The full layer-lock battery (reconcile → arc-audit → author-flags → readiness) stays un-orchestrated until all legs pack.
