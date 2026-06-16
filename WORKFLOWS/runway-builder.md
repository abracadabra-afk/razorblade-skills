---
type: workflow
name: runway-builder
trigger: build the runway
aliases: [build the runway for chapter N, make the runway, derive the runway, prep the runway, runway from the brief, build the dictation runway, runway this chapter]
inputs: [a chapter folder using the per-chapter convention with a filled brief.md]
outputs: [a runway.md written into the chapter folder — a thin speaking outline derived from the brief's beats, wrapped in the flow-entry conditions block and a receipts close]
lane: fiction
status: draft
last_updated: 2026-06-15
consumes: [the chapter's brief.md (Beats to hit + Seal schedule + Register/tempo + weight), envelope.md (segment names, when present), REFERENCE/threads.md (thread labels the brief references)]
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). First adopter — Witchwood.
pipeline_position: Construction (confirmed brief.md) → THIS → Phase 3 forensic-draft dictation; parallel-upstream sibling of [[WORKFLOWS/dictation-preflight]]
sources: KNOWLEDGE/RESEARCH 2026-06-15 — [[KNOWLEDGE/RESEARCH/2026-06-15 dictation-practice-fiction]] · [[KNOWLEDGE/RESEARCH/2026-06-15 flow-state-writing-dictation]] · [[KNOWLEDGE/RESEARCH/2026-06-15 outlines-adhd-dictation-flow]]
---

# WORKFLOW: Runway Builder (brief → dictation speaking outline)

> Derivation pass that reads a chapter's `brief.md` and writes a `runway.md` into the chapter folder — the thin **speaking outline** CRE actually dictates from. It re-cuts the brief's beats into glance-able keyword **prompts** (never sentences), adds the `→` forward-pointers that keep working memory externalized, seals what the brief's seal schedule says to seal, and wraps the whole thing in the four flow-entry conditions + a receipts close. The codified form of the three 2026-06-15 dictation research briefings and the briefing-runway template. Sits at the **Construction → forensic-draft seam**: after the brief is confirmed, before CRE records dictation.

## When to use

When a chapter using the per-chapter folder convention has a `brief.md` with **Beats to hit**, and CRE wants the dictation runway for it. Trigger phrases: "build the runway," "build the runway for chapter N," "make the runway," "derive the runway," "runway from the brief." Do NOT use it to fill the envelope (that is [[WORKFLOWS/dictation-preflight]]) or to slate dictation (that is [[WORKFLOWS/transcoder]]). The runway is what CRE dictates **from**; the envelope is what the Transcoder cuts **against** — different artifacts, different passes.

## Inputs

- **The chapter folder** (per-chapter convention).
- **`<chapter>/brief.md`** — the source of truth for this pass. Read **Beats to hit**, **Seal schedule**, **Register / tempo notes**, and the `weight` field.
- **`<chapter>/envelope.md`** (optional) — for segment short-names, when already authored.
- **`REFERENCE/threads.md`** (optional) — to resolve any `T##` thread label the brief cites.

## Outputs

- **`<chapter>/runway.md`** — the speaking outline: a Conditions block (blank, for CRE to fill per session), one Scene block per scene (3–5 keyword prompts with `→` forward-pointers, one `★` write-in-full slot, a `[SEALED]` line when the seal schedule applies), the four during-pass guardrails, and a receipts Close. Prompts are **keyword triggers lifted from the brief**, never invented prose.
- A short **derivation note** in the reply: which beats mapped to which prompts, anything tagged `<<UNCERTAIN>>`, and any divergence from the brief worth CRE's eye.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Load and classify the brief
Read `<chapter>/brief.md`. If it has no **Beats to hit** (status `unfilled`, an empty scaffold), halt — there is nothing to derive from; tell CRE to fill the brief first (workshop / pipeline S2). If `status` is `drafted` (not yet `confirmed`), proceed but note the runway inherits unconfirmed intent. Read `weight` — it scopes depth (see Step 5).

### Step 2 — Group beats into scenes, derive prompts
Group the brief's beats into scenes (single-location runs of beats; cross-reference `envelope.md` segment names when present). For each scene, turn **each beat into one prompt**: strip it to a few trigger keywords in delivery order, cap **3–5 prompts per scene**. Add a `→` forward-pointer (the next beat in 1–3 words) after each prompt; the last prompt's pointer is the cut. **Never write a full sentence** — if a derived prompt reads as prose, cut it back to keywords. This pass lifts the brief's own language; it does not generate fiction (cross-cutting rule + DIR).

### Step 3 — Seal + the one write-in-full
From the brief's **Seal schedule "must NOT yet learn"**, write a `[SEALED]` line per affected scene: name what to enact-and-withhold, never narrate. If the brief already specifies a line of dialogue / a concrete image CRE "already hears," lift exactly one into the `★` write-in-full slot; otherwise leave the slot empty for CRE. One `★` per scene, max.

### Step 4 — Scaffold the conditions + close (blank)
Write the Conditions block (medicated-window gate, single-next-goal line, pre-committed stop, inputs-killed checklist, capture path) and the receipts Close **blank** — these are CRE's per-session fills, not derivations. Pre-fill only what the brief makes unambiguous (e.g. "Cut on:" from the brief's curtain instruction).

### Step 5 — Write `runway.md` (never-overwrite; weight-scaled)
Write `<chapter>/runway.md`. **Never overwrite** an existing `runway.md` — if one exists, stop and ask whether to replace or version it. Scale depth by `weight`: `load-bearing` → full runway, every scene; `bridge` → lean (fewer prompts, may collapse to one scene block); `standard` → default. Tag anything you couldn't resolve `<<UNCERTAIN: best guess — reason; confirm?>>` and surface it in the reply rather than guessing silently.

## Files this workflow does NOT touch
`draft.md`, `envelope.md`, `dictation/`, `slate/`, `revisions/`, `open-loops.md`, `continuity.md`, `notes.md`, `_status.md`, and `brief.md` itself (read-only). It writes one file — `runway.md` — and produces no prose.

## Logging
DIR-003 applies. Append a session line to `<chapter>/changelog.md` and the vault `_CHANGELOG.md` (newest-first, file-tool top-insert per DIR-005). File notable fragilities to `_OBSERVATIONS.md`.

## Pipeline relationship
**brief.md (confirmed) → runway-builder (this) → CRE dictates from runway.md → dictation-preflight → transcoder.** The runway is the dictation *input habit* scaffold; the envelope is the Transcoder's cut-test. They are independent prep passes off the same chapter — neither consumes the other.
