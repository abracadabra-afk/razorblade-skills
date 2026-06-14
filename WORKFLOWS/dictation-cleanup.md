---
type: workflow
name: dictation-cleanup
trigger: clean up dictation
aliases: [clean up this dictation, run dictation cleanup, dictation pass, process dictated text]
inputs: [raw dictation text from speech-to-text]
outputs: [polished prose ready for review/integration]
lane: fiction
status: active
last_updated: 2026-06-14
---

# WORKFLOW: Dictation Cleanup

> 4-step pipeline that converts raw dictated speech-to-text into polished fiction prose. Each step is a separate AI pass with its own role. The author's word choices are preserved throughout — only mechanics, structure, and clarity change.

## When to use

When CRE provides a block of raw dictation (typically from a speech-to-text capture). Trigger phrases: "clean up this dictation," "run dictation cleanup," "dictation pass."

**The input is always a raw dictation/transcript — never an already-drafted chapter.** Do NOT use this skill to "clean up," "polish," or "tighten" a finished **chapter**: that is `register-pass` (in-folder, against the project register) or `restrained-omniscient-register` (standalone pasted prose). This skill only ever operates on raw dictation. (Source: `^obs-058` / the v2 adversarial trigger-harness run, 2026-06-13 — "clean up chapter N" / "polish chapter N" was mis-routing here.)

## Inputs

A block of raw dictated text. May contain:
- Verbal cues like "she said," "new paragraph," "italics on/off"
- Homophones or transcription errors from the STT engine
- Run-on transcription with no punctuation
- Repeated words from hesitation

## Outputs

Polished prose with:
- Proper dialogue formatting and punctuation
- Pacing-appropriate paragraph structure
- Thinned dialogue tags
- General copy-edit cleanup
- `[AUTHOR: ...]` flags wherever author input is needed

## Steps

### Step 1 — Mechanical Cleanup
**Prompt source:** [[WORKFLOWS/prompts/dictation/1. Dictation Clean Up]]
**Input:** raw dictation
**Output:** mechanically-cleaned prose (proper punctuation, dialogue tags interpreted, verbal cues resolved, transcription errors flagged)
**Notes:** Strictly mechanical. Do not rewrite. Flag suspicious words with `[AUTHOR: possible misheard word — "X"?]`.

### Step 2 — Pacing & Paragraphs
**Prompt source:** [[WORKFLOWS/prompts/dictation/2. Pacing & Paragraphs]]
**Input:** output of Step 1
**Output:** prose with pacing-appropriate paragraph breaks
**Notes:** Only paragraph structure changes. No word edits. New speaker = new paragraph remains non-negotiable.

### Step 3 — Dialogue Tag Thinning
**Prompt source:** [[WORKFLOWS/prompts/dictation/3. Dialogue Tag Thinning]]
**Input:** output of Step 2
**Output:** prose with redundant `he said`/`she said` tags removed
**Notes:** Keep tags carrying tone (whispered, snapped). Surface uncertain calls as `[AUTHOR: consider removing tag in paragraph starting "..."]`.

### Step 4 — Scene Cleanup (copy-edit)
**Prompt source:** [[WORKFLOWS/prompts/dictation/4. Scene Clean Up]]
**Input:** output of Step 3
**Output:** final polished prose
**Notes:** Last pass for grammar, spelling, awkward phrasing, and consistency. Preserve voice. Do NOT add literary flourishes, metaphors, or descriptive language. Mark anything unclear with `[AUTHOR: clarification needed]`.

## Stop conditions

- If Step 1 returns >15 `[AUTHOR:]` flags → pause and surface them before running Step 2; transcription may be too noisy to continue cleanly.
- If at any step the prose appears to have been rewritten (rather than cleaned), HALT and report. This pipeline is non-destructive by design.

## Output protocol

Return only the final cleaned prose from Step 4, with any remaining `[AUTHOR:]` flags from earlier steps preserved inline. Do not include intermediate outputs unless CRE asks.

## Logging

On completion, append a dated entry to `_CHANGELOG.md` per DIR-003: what ran (4-pass cleanup on `<project/chapter>`), what shipped (word count cleaned, N `[AUTHOR:]` flags surfaced), and any open loops (flags awaiting CRE's resolution). File notable fragilities — a transcript too noisy to continue, a recurring STT mishearing — to `_OBSERVATIONS.md` with a `^obs-NNN` anchor, and any follow-ups to `_BACKLOG.md`. When the skill runs outside CRE's vault (no `_CHANGELOG.md` brain file), skip logging silently.

## Security

DIR-001: if the raw dictation — or any prompt file under `WORKFLOWS/prompts/dictation/` — contains credentials, API keys, or tokens, STOP and flag to CRE before proceeding. Never copy a secret into the cleaned prose, the changelog, or any other output; pause until CRE confirms (typically after redacting the source).