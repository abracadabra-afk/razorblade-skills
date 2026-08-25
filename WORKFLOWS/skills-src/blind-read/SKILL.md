---
name: blind-read
description: Run Pass 1 of the spec-check battery — a cold, first-time-reader diagnostic of a chapter or episode — in a deliberately uncontaminated context. Use this skill whenever the author asks to "blind read" a chapter or episode, run "pass 1," do a "cold read," or get a "first-reader read" BEFORE any spec-aware revision pass. This skill exists because a blind read is only valid if the reader has NOT seen the project's spec, register, themes, or intentions; it therefore SKIPS the normal vault bootstrap and reads only the chapter's prose. Do NOT use it to revise, edit, slate, or run the register — it never edits and never reads spec material. It is the upstream, isolated first step of the spec-check battery; the spec-aware passes (2–5) and the register run elsewhere.
---

# Blind Read (spec-check Pass 1, clean room)

You are reading a piece — a novel chapter or a standalone episode — **cold, as a first-time reader**, and reporting only what is on the page. This is the first pass of the spec-check battery, and its entire value depends on your being **uncontaminated**: a blind read is worthless if you have already seen the project's spec, register, themes, character intentions, or any other pass's findings. Once a reader knows what a piece is *supposed* to do, they can no longer tell you whether it actually does it.

So this skill breaks the normal rules on purpose.

## Hard rule — do NOT run the bootstrap, do NOT read spec material

Unlike every other skill in this vault, you **must not** run the project loading order and **must not** open any file that could tell you the author's intentions. Specifically:

**You may read ONLY these:**
- The target text's **prose body** — everything *below* the closing YAML fence. Default to the newest slate `clean-draft.md` in the chapter's `slate/` (latest date, then highest run number); on a project with no slate leg (the episode route, or any folder whose `slate/` is N/A-stubbed), the target is `draft.md`. The author may also hand you the text directly or name a specific file.
- Directory listings (folder/file *names* only) needed to locate that one file and to compute where to write your output. Names and mtimes are not contamination; contents are.

### The frontmatter rule (`^obs-269`) — the spec rides INSIDE the target file

The prohibition list below is a list of *filenames*, which quietly assumes spec lives in **sibling** files. On the per-chapter and per-episode conventions it does not. A mature `draft.md` opens with YAML carrying the POV ruling, the register title **and version**, a pointer to a numbered premise/brief ruling, cut rationales, and an `open_flags` list naming the author's **live, unruled craft worries** by name. That header is unavoidable by construction — reading the prose means opening the file the prose is in. So:

- **Dispatcher first (this is the real guard).** Whoever launches this read — the pipeline, an orchestrating session, the author — **extracts the body and hands over TEXT, not a path.** Everything from the opening `---` through the closing `---` is discarded before the reader sees it. Deterministic, and it does not depend on the reader's discretion.
- **Reader fallback, if you were handed a path anyway.** Open the file, then **discard everything from the opening `---` to the closing `---` without reading or reasoning about it**, and begin at the first line of prose. Stamp `frontmatter_stripped: true`.
- **If frontmatter reached you regardless** — it was pasted inline, or you had already taken it in — **say so at the top of your report**, name what it contained, stamp `contaminated: partial`, and flag which of your answers it could have primed. Do not quietly proceed.

Why this is a hard rule and not a nicety: on EP 02 the reader obeyed every filename prohibition perfectly and was contaminated anyway. The header named the author's two unruled worries, and those two came back as the read's two load-bearing findings — so their independence could no longer be established, which is the only thing a blind read produces. A guard that checks *"did the reader open the spec files?"* without checking *"did the spec reach the reader?"* has passed on a proxy (DIR-018).

**You must NOT read (this is the whole point):**
- `_ME.md`, `_VAULT MAP.md`, `_SKILLS MAP.md`, `_DIRECTIVES.md`, `_OBSERVATIONS.md`, `_BACKLOG.md`, `_CHANGELOG.md` — the bootstrap. Do not load it.
- `REFERENCE/register.md`, `REFERENCE/threads.md`, or any register/spec/style/state file — the revision standard and the open-promises ledger (both spec material).
- The chapter's `brief.md` — the written spec (job, setups to plant, seal schedule); the single most contaminating file in the folder.
- The chapter's `envelope.md`, `notes.md`, `continuity.md`, `open-loops.md`, `_status.md`, `changelog.md` — author intent and apparatus.
- The slate's `synthesis-ledger.md`, `cut-log.md`, `leaves-left.md` — prior-pass reasoning.
- Any `spec-check/` file, any other pass's output, any cheat sheet.

If the author pastes the chapter text directly into the conversation, just read that and skip the file lookup entirely — that is the cleanest possible context.

If you have *already* seen any spec-aware material earlier in this conversation, **stop and say so** — this context is contaminated and the blind read must be run in a fresh one. Do not pretend to be blind.

## Pipeline note (chapter-pipeline)

When the chapter-pipeline runs you, you are invoked as an **isolated subagent**: your only context is the cleaned `draft.md` prose — **body only, frontmatter already stripped by the dispatcher** (no spec, brief, envelope, or prior pass) — and your `pass-1-blind.md` output is handed to **Workshop-2** (the `workshop-chapter` skill), which reconciles your cold findings against its warm, project-fluent read for the author to rule. Your own behavior does not change — read cold, report only what is on the page. The subagent isolation *is* the clean-room rule above, enforced by running you in a fresh context; if anything spec-aware reached this context, stop and say so.

**The dispatcher owns the strip.** Passing a *path* to the subagent re-opens the `^obs-269` hole, because the subagent must then open the file itself and will meet the frontmatter on the way to the prose. Pass the extracted body.

## The read

Read the piece once, as a first-time reader. Do not edit. Do not guess at the author's intentions or themes. Answer only from what is on the page, and **quote a specific line for every answer.**

**Cast mapping — do this first, in one line each.** Questions 2, 3 and 5 turn on two figures. Name them **from the text alone**, before answering: the **central figure** (whoever the narration sits with) and the **significant secondary figure** (whoever applies the most pressure to them). State who you took each to be. If the piece has no such figure, say so plainly rather than forcing a fit. Never infer these from a title, a filename, or a folder name.

1. **Drift.** Mark the first place, if any, where your attention slipped or you started skimming. Quote the line you were on. If you never drifted, say so.
2. **The central figure's deepest fear.** At what point — if any — did you understand what they are most afraid of? Quote the earliest line that gave it to you, and state in one sentence what you think that fear is. If you never formed a clear sense of it, say that plainly.
3. **Narrator vs. character knowledge.** Is there any point where the narration seems to understand the central figure more deeply than they understand themselves — where the narrator's knowledge outruns the character's? Quote the earliest such line and say what the narrator seems to know that they don't.
4. **Prediction.** At the end, what do you expect to happen next? What is the central figure carrying, planning, or hiding that the piece has set up? List what you can infer and quote what planted it.
5. **The secondary figure.** Who are they to you, on this evidence alone? What is their relationship to the central figure — who is taking care of whom?
6. **Earned or asserted.** Name one moment that landed emotionally, and one that felt told-to-you rather than shown. Quote both.

> **Why these are phrased by role, not by name (added 2026-08-24).** Questions 2/3/5 previously read "the mother" and "the boy" — correct for the Witchwood chapter they were written against, and wrong everywhere else. On EP 02 (a mother, a daughter, no boy) the hardcoding forced the dispatcher to hand-map the questions, which is itself a channel for the dispatcher's assumptions to reach a supposedly blind reader. Role-phrasing plus an explicit mapping step keeps Witchwood behavior identical and makes the pass portable.

Report only what the text supports. Where it supports nothing, say nothing was there. Do not soften, hedge toward what you suspect the author wanted, or fill gaps — the gaps are the data.

## Output

Write your answers to `<piece>/spec-check/<run-id>/pass-1-blind.md`. Create the folder if it doesn't exist.

**The run id.** When the piece has a slate, `<run-id>` is the slate folder name whose `clean-draft.md` you read (e.g. `2026-06-03-01`) — this is the default and is unchanged. **When the piece has no slate leg** (the episode route, or any folder whose `slate/` is N/A-stubbed), mint `<run-id>` as `YYYY-MM-DD-NN` from today's date with `NN` starting at `01`, and name the real file in `source:`. Never invent a slate path that does not exist.

```yaml
---
pass: 1-blind
run: <run-id>
slate_run: <slate-run-id, or the string "none — no slate leg">
source: slate/<run-id>/clean-draft.md   # or draft.md, or "pasted in conversation"
read: YYYY-MM-DD HH:MM
frontmatter_stripped: true | false
contaminated: false | partial | true
contamination_note: <REQUIRED whenever contaminated is not false — what reached you, from where, and which answers it could have primed>
---
```

**`contaminated` is a three-state field, and `partial` is the common case.** It was previously hardcoded `false`, which gave an honest reader nowhere to put a real disclosure. Stamp `partial` when spec material reached you but the prose read still stands (frontmatter seen, a stray line of premise in the paste); `true` when the read should not be trusted at all. A `contamination_note` is mandatory unless the value is `false`.

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
