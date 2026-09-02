---
type: workflow
name: record-script
trigger: "build the record script"
aliases: ["prep the prompter", "make the performance script", "record script for EP N"]
inputs: [record-ready draft.md, wrapper/liturgy reference (optional), performance-notes prep sheet (optional)]
outputs: [record-script.md in the piece's folder — a one-way derived, prompter-formatted performance script]
lane: writing-ops
status: draft
last_updated: 2026-09-01
---

# WORKFLOW: record-script

> **The prep sheet is for rehearsal; the prompter is for performance.** Prose notes on a teleprompter are rules at the mic — the DIR-017 failure shape applied to the record stage. This workflow derives a *performance surface*: the full running order, verbatim, with a three-mark grammar glanceable at reading distance and nothing else. Everything explanatory stays in `performance-notes.md`.

## When to use

CRE says "build the record script," "prep the prompter," or names a piece he's about to record. The piece has a record-ready `draft.md` (WIW episode, audiobook chapter, any narrated work). Project-agnostic.

**Not for:** revising prose (`register-pass` / `line-edit`), building the prep sheet itself (that's a line-edit/panel byproduct), or dictation-side runways (`runway-builder`, `episode-runway`).

## Inputs

1. **The draft** — `<piece>/draft.md`, the current landed text. **It is the authority (DIR-019):** if a `record-script.md` already exists and its `derived_from` predates the draft, the script is stale by definition — regenerate it, don't ask. Whether a line-level pass has run is **stated, not gated**: the script's frontmatter carries a `readiness:` line (which passes have and have not run on this draft — DIR-018) and a `record_licensed: YES | NO — <basis>` field set from the **board's sequencing** (e.g. `TASKS/` chunks ordering line-edit before record), never from a chat confirmation. Build either way; the prompter is disposable and regenerates after the line pass.
2. **The wrapper** (optional) — the project's locked intro/outro reference (WIW: [[WRITING/SHORTS/REFERENCE/liturgy]]). Filled variables (e.g. the story title) are mechanical fills of defined blanks, not authored prose. No wrapper → story-only script; say so.
3. **The prep sheet** (optional) — `<piece>/performance-notes.md` or equivalent CRE-ruled mic-side notes. No prep sheet → clean unmarked script; say so.

## Outputs

`<piece>/record-script.md` — a **one-way derived artifact**. `draft.md` stays the single source of truth; any text problem found at rehearsal routes back through the draft pipeline and the script **regenerates**. Never edit the script directly (two diverging texts = the Substack/podcast versions inherit the wrong one).

## The three-mark grammar (hard cap)

Marks appear **only where a CRE-ruled note licenses them**. The skill never invents delivery direction — performance interpretation is CRE's. Any unlicensed suggestion goes to a gated `## Proposed marks (rule before use)` section at the bottom, never inline.

| Mark | Meaning | Source |
|---|---|---|
| `**bold**` | ruled stress word | a delivery ruling naming the word |
| `[cue]` | ≤3-word delivery cue before a line (e.g. `[killer voice]`, `[slow]`) | a delivery ruling naming the treatment |
| `⚑N` | rehearsal flag at the start of a marked paragraph; N keys to the prep-sheet item | a rehearsal flag in the prep sheet |

The *why* never appears inline — it lives in the prep sheet under the same number. Draft italics are content (feed text, thoughts) and are preserved verbatim; the draft carries no bold, so added bold is unambiguous.

## Steps

### Step 0 — Vault sentinel
Standard gate (`^obs-004`): `_DIRECTIVES.md` frontmatter `type: ai-os-brain` + `file: directives`, else halt and ask.

### Step 1 — Locate + state record-readiness
Find the piece's folder, read `draft.md` frontmatter and the piece's `changelog.md` (the changelog is the authority on which passes ran — a `status` field describes one landing and goes stale the moment a later ruling lands, `^obs-279`). Record the readiness facts for the frontmatter; do not gate on them. Locate wrapper + prep sheet. Name all three files in the reply so a wrong pick is visible. **Prep-sheet triage (DIR-019 §2):** a delivery ruling or rehearsal flag whose span is gone from the current draft is moot — stamp it `superseded_by` in the prep sheet, one log line, no mark, no ask; a reworded-but-surviving span goes to `## Proposed marks` at the bottom (gated) rather than being applied blind.

### Step 2 — Assemble the running order, verbatim
```
PRE-FLIGHT (decide/recall before the light goes on)
■ INTRO (wrapper, title filled)
■ STORY (draft body, byte-faithful except formatting + licensed marks)
■ OUTRO (wrapper)
— END —
Post / engineer notes
Proposed marks (only if any)
```
**Pre-flight block:** any prep-sheet item tagged decide-before-record, a one-line pointer to the prep sheet, and standing reminders from the wrapper doc (e.g. advisories are referenced, never read aloud).

**Post / engineer notes:** items addressed to the edit sitting, not the read (deliberate elisions post must not "fix", advisory-template reminder, scrub-tier note). They travel with the script but sit below `— END —` so they never scroll on the prompter.

### Step 3 — Prompter-format the story
- Every paragraph starts with `▸ ` on its own visual block (blank line above). Paragraph tops are the **rolling-restart re-entry points**: flub → clap → eyes jump to the nearest `▸` → go.
- Text inside a paragraph is verbatim — words, punctuation, italics untouched. No reflow that changes wording; no "reading ease" edits, ever.
- Dialogue/caption lines keep their own lines (already short).

### Step 4 — Apply licensed marks
Walk the prep sheet. Each delivery ruling → its bold/cue at the exact spot. Each rehearsal flag → `⚑N` at the paragraph top. Anything the skill *thinks* would help but no ruling covers → `## Proposed marks` at bottom, gated.

### Step 5 — Frontmatter + provenance
Simple, safe YAML (DIR-004 spirit — plain scalars, quote anything with apostrophes): `type: record-script`, `derived_from` (draft path + its `source_revision`, wrapper path, prep-sheet path, all with dates), `readiness:` (passes run / not run on this draft, from the changelog), `record_licensed: YES | NO — <board basis>`, `status: derived — regenerate, never hand-edit`, `last_updated`. Verify the write by re-reading through the file tools (DIR-005).

### Step 6 — Log
DIR-003: `_CHANGELOG` entry (writing-ops lane). Piece-level changelog if the folder keeps one.

## Stop conditions

- Sentinel fails → halt.
- No `draft.md` → halt; nothing to derive.
- ~~Draft status shows no line-level pass → surface + confirm before building.~~ **Retired 2026-09-01 (DIR-019):** build anyway; state readiness and set `record_licensed` from the board. A confirm-before-building gate was making CRE ratify a sequencing decision the board already carried.
- A prep-sheet note requires *changing the text* to execute → that's an edit, not a mark: route it back to the draft pipeline and leave the spot unmarked.

## What this workflow is NOT

- Not an editor. Zero word changes, ever. Improvement is `register-pass` / `line-edit`.
- Not a director. Marks transcribe CRE's rulings; the skill proposes at the gate, never inline.
- Not a second source of truth. The script is disposable; the draft is canon.

## Logging

Per Step 6. First live run: EP 01 *Happening Near You*, 2026-07-29.

---

_Canonical doc for the `record-script` Cowork skill. Source: `WORKFLOWS/skills-src/record-script/SKILL.md`. Per [[_SKILLS MAP#Cowork skills]], procedure changes land here first, then propagate to the skill source; pack on the desktop per DIR-009._
