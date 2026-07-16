---
type: workflow
name: chapter-init
trigger: "scaffold chapter N"
aliases: ["start a new chapter", "init chapter N", "new chapter folder", "scaffold the next chapter"]
inputs: [project (defaults to the only project with a CHAPTERS/ dir), chapter number N, chapter TITLE]
outputs: [a complete per-chapter folder with stamped frontmatter, a seeded brief.md, init entries in the chapter changelog + pipeline board]
lane: fiction
status: active
last_updated: 2026-07-15
revision_note: 2026-07-15 — Step 4b added (CRE-ratified): when the shape-the-part descent has run, the brief seed also pulls beats/plants/seals from the chapter's mapped DEV/scenes entries (the brief-fill seam now has an owner).
---

# WORKFLOW: chapter-init

> Pipeline step **S1**. Scaffolds `CHAPTERS/CHAPTER N - <TITLE>/` with every file of the per-chapter folder convention, each stamped with the **correct** `chapter:` frontmatter — killing the `^obs-005` template-copy class (CH2/CH3 shipped with files still claiming `chapter: CHAPTER 1 - KNOTS`). Orchestration-only: it creates structure, proposes a thread harvest into `brief.md`, and writes nothing creative.

## When to use

A new chapter is starting and its folder doesn't exist yet. Trigger phrases: "scaffold chapter 4," "start a new chapter," "init chapter 4 — TITLE." Runs before S2 (brief fill with CRE) and S3 (dictation).

## Inputs

- **Project** — the project root containing `CHAPTERS/` and `REFERENCE/` (currently WITCHWOOD). If more than one project qualifies, ask.
- **N and TITLE** — from CRE. If TITLE is missing, ask; never invent a title. Folder name is `CHAPTER <N> - <TITLE>` (title uppercased, matching siblings).

## Outputs

```
CHAPTER N - <TITLE>/
├── brief.md          status: unfilled, spec_material: true; weight: standard (CRE confirms at S2 — see [[WORKFLOWS/chapter-weight]]); "Payoffs due" pre-seeded from REFERENCE/threads.md open threads (proposals, tagged for CRE); beats/plants/seals pre-seeded from mapped DEV/scenes entries when the descent has run (Step 4b, proposals likewise)
├── envelope.md       blank segment template (dictation-preflight fills it at S4)
├── changelog.md      carries the S1 init entry
├── draft.md          status: scaffold, placeholder body
├── open-loops.md     empty sections (register ambiguity / image-doubling / left-for-later / resolved)
├── continuity.md     end-state + Character state @ end of chapter sections (canon-sync-owned, `^obs-048`), pointing at REFERENCE/ (not the archive relics)
├── notes.md          empty
├── _status.md        phase table, no segment rows yet (segments come from envelope.md)
├── dictation/README.md
├── slate/README.md
└── revisions/README.md
```

`spec-check/` is **not** scaffolded — the battery creates it per run.

## Steps

### Step 1 — Vault sentinel (`^obs-004`)
Verify `_DIRECTIVES.md` exists at the vault root with frontmatter `type: ai-os-brain`, `file: directives`. Fail → halt, ask which folder is the vault.

### Step 2 — Gates
- Folder `CHAPTER <N> - *` already exists → **halt**; never overwrite, never fill gaps in an existing chapter (that's not this workflow's job).
- N is not (highest existing chapter + 1) → surface and confirm before proceeding.
- Project lacks `CHAPTERS/` or `REFERENCE/` → the convention isn't adopted here; ask before fabricating structure.

### Step 3 — Scaffold
Create the folder and all files from the templates (canonical copies live in the `chapter-init` skill's `templates/`; the skill's `scripts/scaffold.py` writes them deterministically). Every file gets `chapter: CHAPTER <N> - <TITLE>` and `last_updated: <today>` stamped. No file body is copied from a sibling chapter — that is the trap this workflow exists to kill.

### Step 4 — Seed brief.md (proposal only)
Read `REFERENCE/threads.md`. For each thread not yet `PAID`/closed, add one line under the brief's **Payoffs / advances due**: `- **T<NN> <name>** — open since CH<M>; <one-line state>. <<PROPOSED — CRE to rule: pays / advances / dormant>>`. Everything else in the brief stays template. Stamp `weight: standard` in the brief frontmatter as the safe default (see [[WORKFLOWS/chapter-weight]]) — CRE confirms or changes it (`load-bearing` / `bridge`) at S2. `status: unfilled` — S2 (with CRE) flips it to `drafted`/`confirmed`. No `REFERENCE/threads.md`? Skip, note it.

### Step 4b — Seed from the scene rung (the brief-fill seam; only when the descent has run)
If the project's `DEV/scenes/` holds entries mapped to this chapter (the [[WORKFLOWS/shape-the-part]] **chapter map**), seed the brief from them in addition to the threads harvest:
- **Beats to hit** ← one line per mapped scene: the scene's **job** + its beats-so-far, with the `[[SC NN]]` link kept (provenance travels with the beat).
- **Setups to plant / Seal schedule** ← the plants/payoffs/seals the scene entries carry (e.g. a `PLANT:`-flagged beat like the true-strike at SEQ 18 grain) — these are the lines the runway's `PLANT:` flags depend on downstream; dropping one here is how a battery-locked setup gets improvised away at the mic.
- Every seeded line is a **proposal**: `<<PROPOSED — from [[SC NN]]; CRE to rule>>`. The seed is an inventory of CRE's own ruled scene shapes — it recombines nothing, invents nothing, and S2 stays CRE's (the brief author is still him). Wording stays the scene entries' own language, never sharpened here.
No mapped scenes (project has no descent, or the part's shape hasn't run) → skip, note it — Step 4's threads harvest alone is the original mode.

### Step 5 — Log (record the ruling in the same gesture, `^obs-012`)
- Chapter `changelog.md`: init entry (what was scaffolded, what was seeded, open S2 gate).
- Project `PIPELINE.md` board, if present: add/update the chapter row — S1 done, S2 next, owner CRE+AI.
- Vault `_CHANGELOG.md`: one session entry.

## Stop conditions

Sentinel fails · folder exists · no TITLE given · ambiguous project · convention not adopted.

## What this workflow is NOT

- Not the brief author — S2 is CRE's; the seed is an inventory, not intent.
- Not the envelope author — that's [[WORKFLOWS/dictation-preflight]].
- Not a migrator/repairer of existing chapters — it only ever creates a folder that doesn't exist.

## Skill

Installable Cowork skill: `chapter-init` (auto-triggers on the phrases above). This doc is canonical; changes land here first, then propagate via skill-creator.
