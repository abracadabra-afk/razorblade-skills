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
2. **Sweep the source transcript to `_intake/_audit/<date>-<source>.md`** (verbatim — the recoverable floor), then **remove the routed transcript from `_intake/` once it is fully processed** (every segment routed or held-as-its-own-file). The floor is the canonical copy; `_intake/` holds only *unrouted* material (pending + holds).
3. Leave a one-line pointer in the entry footer: `superseded prior take: see intake <date>`.
4. **Taste is first-class** — fill the entry's *What I love / why it matters* field; never discard taste as meta-commentary.

**Authority flows up:** after changing a scene, re-derive the sequence read above it (`sequences/SEQ NN`), and note silently in `project.md` if the macro read may have shifted (no ceremony). Registry entries are **wikilinked** (basename form — `[[Entry]]` / `[[items#Heading]]`) so Obsidian's graph *is* the connection map.

**Taste propagates down:** measure each routed scene's taste against `_DEV.md`. If it drifts from the anchor, **surface the drift** for CRE — never rewrite the scene to match.

## Step 5 — Hold the rest
Below-bar / unsplittable segments → `_intake/HOLD-<date>-<n>.md` with the candidate destinations + one line on why held. Never auto-file these.

## Step 6 — Ledger (deferred contradictions)
If a discovery collides with **already-banked manuscript material** (a landed `draft.md`, a sealed thread, a paid-off plant), append one line to `_intake/_LEDGER.md` — **silently. Do not surface it now.** Honor the ledger's `surface_trigger` frontmatter (`editing-seat` for novels, `ship-boundary` for serial). Resolving the ledger is a separate future editing workflow.

## Step 7 — Poetics (observe the process, slowly) — the graduation loop
File any repeated **routing reality** as a `^poe-NNN` noticing in `_POETICS.md` (dated, with a sighting count). **Assign the anchor collision-safe** — scan the *whole* file for the highest existing `^poe-NNN` and take max+1; never reuse a number a concurrent run or manual edit may already hold (the `^obs-122` duplicate-anchor class). **Process only — never story content.** Walk the loop:

1. **Notice (sighting 1).** New process pattern → write the `^poe-NNN` block, `**Status:** noticing`. It binds nothing. One session is an anecdote — **never** graduate or surface on first sighting.
2. **Recur (sighting ≥2).** Same pattern seen again → bump the **Sightings** count + date, flip `**Status:** recurred`. Still binds nothing; still silent.
3. **Propose (recurred + steady).** Once recurred and stable, flip `**Status:** <<PROPOSED — CRE to promote>>` and surface it to CRE in the routing log (Step 8) — *as a proposal, never as an applied change.* This is the only moment a poetics pattern reaches CRE.
4. **Promote (CRE rules).** Only on CRE's explicit promotion: write a one-line **binding rule** into `_DEV_MAP.md` § *Graduated poetics patterns* (format: `- ^poe-NNN — <rule the router now applies> (promoted YYYY-MM-DD)`), and flip the `_POETICS` entry to `**Status:** promoted → _DEV_MAP`. **Only now does the pattern bind the router** — Step 1 reads only *graduated* patterns from `_DEV_MAP`.

**Canonical worked example — the recognized braid (dual-route).** Until a braid pattern is promoted, a genuine two-bucket segment **HOLDs** (Step 3/5). After CRE promotes `^poe-NNN — character-transformation×plot-intensity braids dual-route`, that same segment routes to **both** buckets, wikilinked, instead of holding. The graduation loop is exactly what converts a recurring HOLD into a recognized shape. Same mechanism for any other promoted routing rule.

The log models *process only* — where things go, what cues mean, what order CRE thinks in. It learns the shape of the hand, never holds the brush.

## Step 8 — Log + report
- **Routing log (early-trust mode):** show the router's reasoning per segment (`segment 3 → registry/characters/Halloran.md (inferred: sustained character focus, no cue); segment 7 → _intake, held (sequence beat or scene?)`) so CRE can see where the calls match his intent. Mute on request once trust is established.
- **Report** a compact *segment → destination* table + the held list.
- **Vault `_CHANGELOG.md`:** one dated entry under the `fiction` lane (file tools only — DIR-005). File any build surprise to `_OBSERVATIONS.md`.
- **Leave the floor clean (cleanup).** After your file-tool writes finish, sweep atomic-write orphans *you* created: for each file you wrote (DEV entries, `_CHANGELOG`), delete only `<basename>.tmp.<pid>.<hex>` siblings **whose real target file exists and is non-empty**, matched by exact basename — never a blind `*.tmp` wipe, never a temp whose target is missing (it may be another process's in-flight write). Vault-wide orphan sweeps are the janitor pass, not this skill.

---

## Build status (see `WORKFLOWS/dev-capture.md` build order)
- **Live (build-order steps 1–3):** the `DEV/` scaffolder; the **scene-capture path** (cued/inferred scene → evolving `scenes/` entry, sculptor-overwrite, transcript to floor, pointer left); the **`_DEV.md` taste anchor + downward propagation**.
- **Live (build-order step 4 — layer two, hardened 2026-06-21):** the full **cue-or-reason router across *all* buckets** (sequences / registry characters / locations / lore / items), the **deferred ledger** with its configurable `surface_trigger` (editing-seat ↔ ship-boundary), and the **poetics graduation loop** (Step 7). Proven end-to-end against a sandbox copy of the Witchwood `DEV/` tree (every bucket routes; inferred boundaries tagged; stumbled dialogue flagged; ledger logs silently; the ungraduated braid correctly HOLDs; first-sighting poetics binds nothing). Standing discipline still holds: **HOLD beats a confident misfile**, and a multi-bucket segment routes to two buckets **only** once its braid pattern has graduated (else HOLD).
- **Live (2026-06-22 — cleanup discipline):** the **intake-removal invariant** (`_intake/` holds only *unrouted* material; the routed transcript is removed once swept to the `_audit/` floor, the canonical copy) and a **scoped, guarded `.tmp` orphan sweep** (exact-basename + target-intact only; never a blind `*.tmp` wipe). Source-ahead of the installed skill until the next repack (`^backlog-dev-capture-cleanup-repack`).
- **Not built here (build-order item 4, last clause — a separate, gated downstream workflow):** promoting DEV material into trusted **REFERENCE** canon (bible / threads / arcs). The dev layer's permissiveness is safe *precisely because* nothing crosses into canon silently; that crossing is named in `WORKFLOWS/dev-capture.md` § *The one gated crossing* and is its own future skill, not part of capture.

## Files this skill writes — and must not
**Writes:** the `DEV/` tree (via the scaffolder); `scenes/` (+ later `sequences/`, `registry/`, `project.md`) entries; `_intake/` holds + `_audit/` floor; `_LEDGER.md`; `_POETICS.md`; the routing log; a vault `_CHANGELOG` entry.
**Deletes (bounded cleanup):** the routed transcript from `_intake/` once it is floored; atomic-write `.tmp` orphans of files it wrote (exact-basename + target-intact guard only — never a blind `*.tmp` wipe).
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
