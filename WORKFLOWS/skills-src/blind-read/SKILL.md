---
name: blind-read
description: Run Pass 1 of the Witchwood spec-check battery — a cold, first-time-reader diagnostic of a chapter — in a deliberately uncontaminated context. Use this skill whenever the author asks to "blind read" a chapter, run "pass 1," do a "cold read," or get a "first-reader read" of a chapter BEFORE any spec-aware revision pass. This skill exists because a blind read is only valid if the reader has NOT seen the project's spec, register, themes, or intentions; it therefore SKIPS the normal vault bootstrap and reads only the chapter's prose. Do NOT use it to revise, edit, slate, or run the register — it never edits and never reads spec material. It is the upstream, isolated first step of the spec-check battery; the spec-aware passes (2–5) and the register run elsewhere.
---

# Blind Read (spec-check Pass 1, clean room)

You are reading a chapter of a folk-tale novel **cold, as a first-time reader**, and reporting only what is on the page. This is the first pass of the spec-check battery, and its entire value depends on your being **uncontaminated**: a blind read is worthless if you have already seen the book's spec, register, themes, character intentions, or any other pass's findings. Once a reader knows what a chapter is *supposed* to do, they can no longer tell you whether it actually does it.

So this skill breaks the normal rules on purpose.

## Hard rule — do NOT run the bootstrap, do NOT read spec material

Unlike every other skill in this vault, you **must not** run the project loading order and **must not** open any file that could tell you the author's intentions. Specifically:

**You may read ONLY these:**
- The chapter's prose itself — the target text. Default to the newest slate `clean-draft.md` in the chapter's `slate/` (latest date, then highest run number), unless the author hands you the text directly or names a specific file. You read the prose body; ignore any spec implied by its surroundings.
- Directory listings (folder/file *names* only) needed to locate that one file and to compute where to write your output. Names and mtimes are not contamination; contents are.

**You must NOT read (this is the whole point):**
- `_ME.md`, `_VAULT MAP.md`, `_SKILLS MAP.md`, `_DIRECTIVES.md`, `_OBSERVATIONS.md`, `_BACKLOG.md`, `_CHANGELOG.md` — the bootstrap. Do not load it.
- `REFERENCE/register.md`, `REFERENCE/threads.md`, or any register/spec/style/state file — the revision standard and the open-promises ledger (both spec material).
- The chapter's `brief.md` — the written spec (job, setups to plant, seal schedule); the single most contaminating file in the folder.
- The chapter's `envelope.md`, `notes.md`, `continuity.md`, `open-loops.md`, `_status.md`, `changelog.md` — author intent and apparatus.
- The slate's `synthesis-ledger.md`, `cut-log.md`, `leaves-left.md` — prior-pass reasoning.
- Any `spec-check/` file, any other pass's output, any cheat sheet.

If the author pastes the chapter text directly into the conversation, just read that and skip the file lookup entirely — that is the cleanest possible context.

If you have *already* seen any spec-aware material earlier in this conversation, **stop and say so** — this context is contaminated and the blind read must be run in a fresh one. Do not pretend to be blind.

## The read

Read the chapter once, as a first-time reader. Do not edit. Do not guess at the author's intentions or themes. Answer only from what is on the page, and **quote a specific line for every answer.**

1. **Drift.** Mark the first place, if any, where your attention slipped or you started skimming. Quote the line you were on. If you never drifted, say so.
2. **The mother's fear.** At what point — if any — did you understand what the mother is most afraid of? Quote the earliest line that gave it to you, and state in one sentence what you think that fear is. If you never formed a clear sense of it, say that plainly.
3. **Narrator vs. character knowledge.** Is there any point where the narration seems to understand the mother more deeply than she understands herself — where the narrator's knowledge outruns the character's? Quote the earliest such line and say what the narrator seems to know that she doesn't.
4. **Prediction.** At the end of the chapter, what do you expect to happen next? What is the mother carrying, planning, or hiding that the chapter has set up? List what you can infer and quote what planted it.
5. **The boy.** Who is the boy to you, on this evidence alone? What is his relationship to the mother — who is taking care of whom?
6. **Earned or asserted.** Name one moment that landed emotionally, and one that felt told-to-you rather than shown. Quote both.

Report only what the text supports. Where it supports nothing, say nothing was there. Do not soften, hedge toward what you suspect the author wanted, or fill gaps — the gaps are the data.

## Output

Write your answers to `<chapter>/spec-check/<slate-run-id>/pass-1-blind.md`, where `<slate-run-id>` is the slate folder name whose `clean-draft.md` you read (e.g. `2026-06-03-01`). Create the `spec-check/<slate-run-id>/` folder if it doesn't exist. Front it with:

```yaml
---
pass: 1-blind
slate_run: <slate-run-id>
source: slate/<slate-run-id>/clean-draft.md   # or "pasted in conversation"
read: YYYY-MM-DD HH:MM
contaminated: false
---
```

If the author handed you the text directly (no file), still write the output if you can locate the chapter folder; otherwise return the read in the conversation and tell the author where to save it.

**Do not grade yourself.** The comparison of your cold findings against the spec is the author's private job — you never see the spec, so you cannot and must not score your own read. Just report.

## What this skill never does

- Never edits, rewrites, or suggests fixes. It diagnoses by reporting a reader's experience.
- Never reads or references the spec, register, envelope, or any other pass.
- Never runs the bootstrap or logs to `_CHANGELOG`/`_OBSERVATIONS` *from inside the blind context* — logging would require reading brain files and contaminate the read. The author (or a later, spec-aware session) records that this blind read ran.

## Stop conditions

- **Context already contaminated** by spec-aware material in this conversation → halt; tell the author to run the blind read in a fresh context.
- **No chapter text** locatable and none pasted → ask the author for the chapter text or its path.
- **The author asks you to also do Passes 2–5, the register, or any edit here** → decline within this context; those are spec-aware and would retroactively justify nothing — point them to `WORKFLOWS/spec-check.md` and `register-pass`, run separately.
