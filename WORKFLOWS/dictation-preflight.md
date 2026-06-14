---
type: workflow
name: dictation-preflight
trigger: prep the envelope
aliases: [preflight this chapter, fill the envelope, ready the envelope, envelope prep, set up the envelope, prep for the transcoder, run preflight]
inputs: [a chapter folder using the per-chapter convention, the newest unslated dictation in its dictation/]
outputs: [a filled envelope.md (POV + conditions + state per segment), synced _status.md segment names, a clarification block for any uncertain fields]
lane: fiction
status: active
last_updated: 2026-06-03
consumes: [REFERENCE/story-so-far.md, REFERENCE/bible.md, REFERENCE/threads.md (via canon-sync) — back-walk across prior chapters is the fallback; the chapter's brief.md as intent context when present]
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). First adopter — Witchwood.
pipeline_position: upstream of [[WORKFLOWS/transcoder]]
---

# WORKFLOW: Dictation Pre-Flight (envelope prep)

> Authoring pass that reads a chapter's queued dictation and fills in its `envelope.md` **before** any slate is run. This is the codified fix for [[_OBSERVATIONS#^obs-005]] — a new chapter's envelope is usually a verbatim blank-template copy, so the Transcoder trips its empty-envelope gate on the first run. Pre-flight removes that halt by authoring the envelope (or surfacing a confident best guess to confirm) up front. Sits **upstream** of [[WORKFLOWS/transcoder]].

## When to use

When CRE has dropped dictation into a chapter that uses the per-chapter folder convention but the chapter's `envelope.md` is still blank, a stale template copy, or only partly filled. Trigger phrases: "prep the envelope," "preflight this chapter," "fill the envelope," "ready the envelope for the transcoder." Do NOT use it to slate or transcode — that is [[WORKFLOWS/transcoder]] ("slate this dictation"), which runs after this.

## Inputs

- **The chapter folder** (per-chapter convention: `envelope.md` + `dictation/` + `slate/`).
- **The newest unslated dictation** in `<chapter>/dictation/` — the file with no matching `slate/YYYY-MM-DD-NN/` yet.

## Outputs

- `<chapter>/envelope.md` — POV + conditions + state for each perceptual segment, **fill-gaps-only** (author-written fields are never overwritten; placeholders, ellipses, and stale frontmatter are). Uncertain fields are written as a tagged best guess `<<UNCERTAIN: …; confirm?>>`, never a silent guess.
- `<chapter>/_status.md` — the Envelope column's segment names, gaps only.
- A **clarification block** in the reply: every uncertain field, the best guess, and what's needed to confirm it. The chapter is slate-ready only once those are confirmed.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault. (The `^obs-004` mitigation, shared with the Transcoder.)

### Step 1 — Classify the existing envelope
Read `<chapter>/envelope.md`. Mark each field as scaffold (angle-bracket placeholder, `…`, empty) or author-filled. A frontmatter `chapter:` that doesn't match the folder name = a verbatim template copy; distrust the whole file and correct the frontmatter on write. Fully filled + matching frontmatter → nothing to do; stop.

### Step 2 — Segment by perceptual envelope
Read the dictation. Mark where the perceptual world changes — light, temperature, location, who the POV attends to. For each segment derive: short name, boundaries (quote-anchored first→last beat), POV, conditions, state. Segment on perceptual world only, never maturity or plot.

### Step 3 — Confidence + context resolution
For each field, judge whether it's readable off the dictation. POV and place names are most often implicit. When unclear, resolve in this order:

1. **Project state first:** `REFERENCE/story-so-far.md`, `REFERENCE/bible.md`, and `REFERENCE/threads.md` (maintained by [[WORKFLOWS/canon-sync]]) — current state, entity facts, canonical names/spellings, open promises, where things stood at the end of the last landed chapter. The chapter's own `brief.md` (when present) is intent context — useful for segment naming and for flagging when the dictation visibly diverges from the chapter's stated job (note it; never block on it).
2. **Back-walk as fallback:** when REFERENCE is missing, empty, or stale relative to the prior chapter (compare `last_updated` / synced chapters against the newest landed draft), walk back across prior chapters (nearest first): prior `envelope.md` → prior `continuity.md`/`draft.md` → this chapter's `notes.md` and the project entry note. If the back-walk was needed because REFERENCE was stale, say so — that's a signal to run canon-sync.

Re-assess, and cite which file resolved each field.

### Step 4 — Write confident fields; tag + ask on uncertain ones
Write every confident field straight in (gaps only); fix `chapter:` and bump `last_updated`. For fields still uncertain after the walk-back, write the best guess tagged `<<UNCERTAIN: best-guess — reason; confirm?>>` and collect them into a clarification block. Tell CRE the chapter is not slate-ready until the tagged fields are confirmed.

### Step 5 — Sync `_status.md`
Fill the Envelope column's `<name from envelope.md>` placeholders with the new segment short-names. Gaps only; never change phases or blockers.

## Files this workflow does NOT touch
`draft.md`, `slate/`, `open-loops.md`, `continuity.md`, `notes.md`, `revisions/`, and the dictation files. It authors the envelope and produces no prose.

## Logging
DIR-003 applies. Append a session line to `<chapter>/changelog.md` and the vault `_CHANGELOG.md`; file notable fragilities to `_OBSERVATIONS.md`.

## Pipeline relationship
**dictation-preflight (this) → transcoder → dictation-cleanup.** Pre-flight authors the envelope; the Transcoder consumes it to generate the slate; dictation-cleanup polishes downstream. On projects that haven't adopted the per-chapter folder convention, none of these envelope steps apply — only [[WORKFLOWS/dictation-cleanup]].
