---
name: record-script
description: Derive a prompter-friendly performance script from a record-ready draft — assemble the full running order (locked intro liturgy with title filled, story, outro) verbatim, prompter-format it with paragraph re-entry points, and apply a strict three-mark grammar (ruled stress bolds, short bracketed delivery cues, numbered rehearsal flags) sourced ONLY from the piece's CRE-ruled performance notes. Use whenever the author asks to "build the record script," "prep the prompter," "make the performance script," or "record script for EP N" on a piece with a record-ready draft.md (WIW episodes, any narrated work). Output is a one-way derived record-script.md in the piece's folder — draft.md stays the source of truth, the script regenerates and is never hand-edited. Do NOT use it to revise or line-edit prose (register-pass / line-edit), to build the performance notes themselves, or for dictation-side runways (runway-builder / episode-runway). It changes zero words, ever, and never invents delivery direction.
---

# Record Script

You are deriving a **performance surface** from a record-ready draft: the full running order, verbatim, formatted for a teleprompter, marked only where the author has already ruled a delivery. The principle behind every choice below: **the prep sheet is for rehearsal; the prompter is for performance.** Prose notes on a prompter are rules at the mic — they split attention mid-read and produce exactly the fumbling this artifact exists to prevent.

You hold **no craft opinion and no directorial opinion.** You change zero words. You transcribe the author's mic-side rulings into glanceable marks; anything you merely *think* would help goes to a gate at the bottom, never inline.

One invariant makes this safe:

> **`record-script.md` is a disposable, one-way derive.** `draft.md` is the single source of truth. A text problem found at rehearsal routes back through the draft pipeline (register-pass / line-edit), and the script regenerates. The script is never hand-edited — two diverging texts means the other platform versions inherit the wrong one.

---

## Step 0 — Vault sentinel check

Before anything else (`^obs-004`): read `_DIRECTIVES.md` at the mounted vault root and confirm frontmatter `type: ai-os-brain` + `file: directives`. Missing or mismatched → **halt and ask** which folder is the vault. Never scaffold, never write.

**Creative-lane load (ratified 2026-09-03):** then read `_CREATIVE DIRECTIVES.md` from the mounted root (CDIR-001–010 — how AI behaves around CRE's craft) before opening any piece file. `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both. Missing → proceed and note it; it is not a sentinel.

---

## Step 1 — Locate the inputs and verify record-readiness

1. **The draft** — `<piece>/draft.md`. Read its frontmatter. Confirm the status/lineage shows a **line-level pass** (register-pass or line-edit promoted; "record-ready"). If it shows only structural passes (blind read, dev), **surface that and confirm before building** — a script off an unfinished draft invites edit-at-the-mic.
2. **The wrapper** (optional) — the project's locked intro/outro reference. For WIW: `WRITING/SHORTS/REFERENCE/liturgy.md`. Filling its defined blank (the story title) is a mechanical fill, not authored prose. No wrapper → build a story-only script and say so.
3. **The prep sheet** (optional) — `<piece>/performance-notes.md` or equivalent CRE-ruled notes. No prep sheet → clean unmarked script and say so.

Name all three files (or their absence) in your reply so a wrong pick is immediately visible.

---

## Step 2 — Assemble the running order

Build the body in this order, each section headed so the eye finds it:

```
PRE-FLIGHT  (decide/recall before the light goes on)
■ INTRO     (wrapper text, title filled)
■ STORY     (draft body — verbatim, formatted per Step 3)
■ OUTRO     (wrapper text)
— END —
Post / engineer notes
Proposed marks (rule before use)   [only if any exist]
```

- **PRE-FLIGHT** holds: any prep-sheet item tagged decide-before-record (e.g. "decide one spoken rendering"), a one-line pointer to the prep sheet ("read at rehearsal, not here"), and standing wrapper reminders (e.g. advisories are referenced, never read aloud).
- **Post / engineer notes** holds items addressed to the edit sitting, not the read: deliberate elisions post must not "fix," the content-advisory template reminder, scrub-tier notes. Below `— END —` so they never scroll on the prompter.

---

## Step 3 — Prompter-format the story (zero word changes)

- Every paragraph becomes its own visual block: blank line above, the paragraph prefixed `▸ `. Paragraph tops are the **rolling-restart re-entry points** — on a flub the author claps, jumps eyes to the nearest `▸`, and re-reads from there.
- Inside a paragraph the text is **verbatim**: words, punctuation, and italics untouched. Draft italics are content (feed captions, thoughts) — preserve them exactly. No reflow that alters wording; no readability edits, ever.
- Short dialogue/caption lines keep their own lines.

---

## Step 4 — Apply the three-mark grammar (licensed marks only)

Marks appear **only where a ruled note in the prep sheet licenses them**:

| Mark | Meaning | License required |
|---|---|---|
| `**bold**` | ruled stress word | a delivery ruling naming the word |
| `[cue]` | delivery cue, 3 words max, placed before the line (e.g. `[killer voice]`, `[slow]`) | a delivery ruling naming the treatment |
| `⚑N` | rehearsal flag at the paragraph top; N = the prep-sheet item number | a rehearsal flag in the prep sheet |

The *why* never appears inline — it lives in the prep sheet under the same number. The draft carries no bold of its own, so added bold is unambiguous as a mark.

If executing a note would require **changing the text**, that is an edit, not a mark: route it back to the draft pipeline, leave the spot unmarked, and say so.

Anything you would suggest that no ruling covers → `## Proposed marks (rule before use)` at the bottom, one line each, gated on the author. Never inline.

---

## Step 5 — Frontmatter, write, verify

Write `<piece>/record-script.md` with simple, safe YAML (plain scalars; quote anything containing apostrophes — the DIR-004 discipline):

```yaml
type: record-script
piece: <title>
derived_from: <draft path + its source_revision, wrapper path, prep-sheet path — each with its date>
status: 'derived — regenerate from draft.md, never hand-edit'
last_updated: YYYY-MM-DD
```

Verify the write by re-reading through the file tools, never a bash/mount read (DIR-005).

---

## Step 6 — Log

DIR-003: one `_CHANGELOG.md` entry (writing-ops lane, top-insert). Piece-level changelog only if the folder keeps one. Anything fragile → `_OBSERVATIONS.md`.

---

## Stop conditions

- Sentinel fails → halt, ask.
- No `draft.md` → halt; nothing to derive.
- Draft shows no line-level pass → surface + confirm before building.
- A note requires a text change → not yours; route to the draft pipeline.

## What this skill is NOT

- **Not an editor.** Zero word changes. Improvement is `register-pass` / `line-edit`.
- **Not a director.** It transcribes rulings; it proposes only at the gate.
- **Not a second source of truth.** The script is disposable; the draft is canon.

---

_Canonical reference lives at [[WORKFLOWS/record-script]]. Procedure changes land in the workflow doc first, then propagate here; pack on the desktop via pack-skills.ps1 per DIR-009 — never sandbox packaging._
