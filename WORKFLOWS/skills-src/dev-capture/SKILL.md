---
name: dev-capture
description: Capture a fiction project's upstream-of-the-brief DEVELOPMENT talk — the "what is this about / what has to happen here" thinking — into the project's DEV/ tree, WITHOUT drafting prose. Use whenever CRE asks to "capture the dev," "develop this," "route the dev intake," "sort the dev transcript," "file the development," or "run the dev router," handing over a cleaned dictation transcript for a project's DEV/ layer. It segments the transcript, routes by spoken cue (else inferred content, else holds), sharpens scene entries against the _DEV.md taste anchor, logs contradictions to _LEDGER.md, and notes process patterns in _POETICS.md. Do NOT use it to draft prose from dictation (that is dictation-transcoder, "slate this dictation"), to build a forensic outline from a filled brief (that is runway-builder), or to copy-edit a transcript (that is dictation-cleanup). Sits below the brief; never promotes into REFERENCE canon (gated, separate). Requires the project's DEV/ tree; if absent, run the scaffolder first.
---

# dev-capture

You are capturing **development talk**, not drafting. CRE has talked himself through a piece of the story at some level — project down to scene — and wants it **captured and organized** into the project's `DEV/` tree. You **never generate his prose**: development is *reaching-toward*; drafting is *committing*; keep the registers distinct even though the medium (voice) is identical.

**Governing principle:** the work moves as it moves; the system follows CRE's flow, not the reverse. Capture is permissive. Rigor lives at exactly two seams — the gated crossing into REFERENCE canon (separate skill, not here) and the deferred contradiction ledger. Everywhere else the marble falls: a wrong routing call is cheap to reverse because **nothing downstream trusts this layer yet.**

Canonical reference: `WORKFLOWS/dev-capture.md`. This skill is the AI-trigger surface; that doc is the in-vault canon.

---

## Step 0 — Vault sentinel (^obs-004)
From the mounted folder root, read `_DIRECTIVES.md`; confirm its frontmatter has `type: ai-os-brain` and `file: directives`. If missing/mismatched, **halt and ask** which folder is the vault. Write nothing.

## Step 1 — Resolve project + load
- **Target project** — the folder with `CHAPTERS/` and/or `REFERENCE/` (DEV/ is their sibling). If a cue or CRE names one, use it; if exactly one project qualifies, use it and say so; else ask. Never scatter across projects.
- **DEV/ must exist.** If `<project>/DEV/` is absent → **halt** and offer to scaffold it first:
  `python3 <skill>/scripts/scaffold_dev.py --project "<project-root>" --profile {short|novella|novel}`
  (novel = full tree; novella = movements/ instead of sequences/; short = no sequences or project.md). The scaffolder gates on the vault sentinel, refuses to overwrite an existing DEV/, and refuses any unsubstituted placeholder.
- **Load the map + anchor.** Read `DEV/_DEV_MAP.md` (cue table + any *graduated* `_POETICS` patterns — only graduated ones bind the router) and `DEV/_DEV.md` (the taste anchor — so you can measure drift and propagate it down).

## Step 2 — Segment
Split the cleaned transcript into discrete segments: on explicit cues first (hard boundaries), then on topic shifts. **One developed thought = one segment.** Don't merge unrelated talk; don't split a single continuous thought.

## Step 3 — Classify (cue → reason → hold)
Per segment, apply the **segmentation contract** with graceful degradation:
1. **Explicit cue wins, always** — a spoken cue (see the cue table in `_DEV_MAP.md`) is a hard boundary *and* a hard destination. No inference.
2. **Missed cue → infer from content, with confidence, and TAG the boundary `(inferred)`** — sustained character focus → `registry/characters`; a GOAL→BUT→THEREFORE chain → `sequences/`; a concrete sensory moment + stumbled dialogue → `scenes/`. An inferred segment must be visually distinct from a cued one in the result (set `boundary: inferred` in frontmatter + the footer).
3. **Below the confidence bar → HOLD in `_intake/`** — never force-file. A confident misfile costs more than an unrouted fragment.

**Recognized braid:** if a segment legitimately feeds two buckets (e.g. character transformation braided with plot intensity), route to **both**, wikilinked — *only* once that braid pattern has **graduated** in `_POETICS.md`. Until then, treat genuine two-bucket ambiguity as a HOLD.

**Three things to watch every segment:**
- **Preserve the kind.** A question CRE left open stays a question ("maybe she knows" ≠ "she knows"). Manufacturing canon he never committed to is the cardinal sin.
- **Stumbled dialogue** is captured as a *target to reach toward*, flagged un-pressure-tested («…») — never as committed prose.
- **Secret/credential (DIR-001)** → never file; flag and advise rotate.

## Step 4 — Route (confident + cued segments)
Write each into its destination using the matching entry template (`templates/_scene-entry.md`, `_sequence-entry.md`, `_character-entry.md`, `_location-entry.md`, `_lore-entry.md`), substituting the route-time placeholders (`{{NAME}}`, `{{NN}}`, `{{TODAY}}`, `{{CUED_OR_INFERRED}}`, `{{PROJECT_NAME}}`).

**Scene-level overwrite in place (sculptor, not historian):**
1. If the scene/entry exists, the new take **replaces** the body so the entry holds the current sharpest version — do **not** keep old prose inline.
2. **Sweep the source transcript to `_intake/_audit/<date>-<source>.md`** (verbatim — the recoverable floor).
3. Leave a one-line pointer in the entry footer: `superseded prior take: see intake <date>`.
4. **Taste is first-class** — fill the entry's *What I love / why it matters* field; never discard taste as meta-commentary.

**Authority flows up:** after changing a scene, re-derive the sequence read above it (`sequences/SEQ NN`), and note silently in `project.md` if the macro read may have shifted (no ceremony). Registry entries are **wikilinked** so Obsidian's graph *is* the connection map.

**Taste propagates down:** measure each routed scene's taste against `_DEV.md`. If it drifts from the anchor, **surface the drift** for CRE — never rewrite the scene to match.

## Step 5 — Hold the rest
Below-bar / unsplittable segments → `_intake/HOLD-<date>-<n>.md` with the candidate destinations + one line on why held. Never auto-file these.

## Step 6 — Ledger (deferred contradictions)
If a discovery collides with **already-banked manuscript material** (a landed `draft.md`, a sealed thread, a paid-off plant), append one line to `_intake/_LEDGER.md` — **silently. Do not surface it now.** Honor the ledger's `surface_trigger` frontmatter (`editing-seat` for novels, `ship-boundary` for serial). Resolving the ledger is a separate future editing workflow.

## Step 7 — Poetics (observe the process, slowly)
File any repeated **routing reality** as a `^poe-NNN` noticing in `_POETICS.md` (dated, with a sighting count). **Process only — never story content.** A noticing binds nothing and **does not surface for CRE's ruling until it has recurred.** Never graduate a pattern on first sighting.

## Step 8 — Log + report
- **Routing log (early-trust mode):** show the router's reasoning per segment (`segment 3 → registry/characters/Halloran.md (inferred: sustained character focus, no cue); segment 7 → _intake, held (sequence beat or scene?)`) so CRE can see where the calls match his intent. Mute on request once trust is established.
- **Report** a compact *segment → destination* table + the held list.
- **Vault `_CHANGELOG.md`:** one dated entry under the `fiction` lane (file tools only — DIR-005). File any build surprise to `_OBSERVATIONS.md`.

---

## Build status (this skill is being built in stages — see `WORKFLOWS/dev-capture.md` build order)
- **Live now (steps 1–3 of build order):** the `DEV/` scaffolder; the **scene-capture path** (cued/inferred scene → evolving `scenes/` entry, sculptor-overwrite, transcript to floor, pointer left); the **`_DEV.md` taste anchor + downward propagation**.
- **Layer two (not yet hardened):** the full cue-or-reason router across *all* buckets (sequences/registry/lore/locations), the deferred ledger automation, the poetics graduation loop, and the gated REFERENCE-promotion crossing. The templates and steps for these exist; treat their routing as proposal-and-confirm with CRE until proven, and prefer HOLD over a confident multi-bucket call.

## Files this skill writes — and must not
**Writes:** the `DEV/` tree (via the scaffolder); `scenes/` (+ later `sequences/`, `registry/`, `project.md`) entries; `_intake/` holds + `_audit/` floor; `_LEDGER.md`; `_POETICS.md`; the routing log; a vault `_CHANGELOG` entry.
**Must NOT write:** any `REFERENCE/` file, any chapter `draft.md`/`brief.md`, or any prose that commits what CRE left open. No promotion into canon — that crossing is separate and gated.

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- No transcript / empty input → "nothing to capture," stop.
- No resolvable target project → ask; don't scatter.
- `DEV/` doesn't exist → halt, offer to scaffold first.
- Secret detected → never file; flag + advise rotate (DIR-001).
- About to resolve an ambiguity CRE left open, or graduate a poetics pattern on first sighting → stop; preserve the question / wait for recurrence.

## What this skill is NOT
- Not the transcoder (no prose drafting from dictation).
- Not runway-builder (no forensic outline from a filled brief — this sits *below* the brief).
- Not dictation-cleanup (it consumes an already-cleaned transcript).
- Not a canon writer — REFERENCE promotion is a separate, gated, downstream act.
