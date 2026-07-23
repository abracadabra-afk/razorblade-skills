---
type: workflow
name: dictation-cleanup
trigger: clean up dictation
aliases: [clean up this dictation, run dictation cleanup, dictation pass, process dictated text]
inputs: [raw dictation text from speech-to-text]
outputs: [polished prose ready for review/integration]
lane: fiction
status: active
last_updated: 2026-07-22
---

# WORKFLOW: Dictation Cleanup (v1.1)

> 4-step pipeline that converts raw dictated speech-to-text into polished fiction prose. Each step is a separate AI pass with its own role. The author's word choices are preserved throughout — only mechanics, structure, and clarity change.

## v1.1 changelog (2026-07-22 — amended off the doomscroller ground-truth test, aligned with transcoder v5.1)

Test: reran the raw doomscroller transcript with the landed, CRE-corrected `draft.md` as ground truth — full scorecard in `SYSTEM/reports/2026-07-22-dictation-cleanup-test.md`. The previous live run fixed 5 garbles silently (right answers, no record), missed 2, left 2 spans unreadable, lost all 8 of its claimed `[AUTHOR:]` flags, and silently mis-punctuated the climax line into an inverted meaning. Root cause: prompt 1 said both "fix obvious artifacts" and "never silently correct," and the strict flag-everything law puts an ordinary clean dictation at 15 flags — its own too-noisy threshold — so flag-fatigue guaranteed drift. Six amendments:

1. **Two-lane garble policy** (shared vocabulary with transcoder v5.1): *mechanical* garbles with exactly one plausible reading fix silently and land in a **Corrections table** in the output header (visible, reversible, no inline clutter); *meaning-splitting* garbles ("layer"/"lair", displaced clauses) flag `[AUTHOR:]` inline. Resolves prompt 1's internal contradiction. On the test: 15 flags → 7, every survivor a genuine CRE call.
2. **Flag ledger — flags must survive.** Every inline `[AUTHOR:]` is also listed in a `## Flags` block at the end of the output with a count in the header. A downstream copy that drops inline flags is now detectable by count mismatch (the lost-8-flags bug).
3. **Climax guard.** In the final two paragraphs, any comma/clause-boundary ambiguity — especially a sentence-final clause — is **flag-don't-touch**. A displaced comma inverted the meaning of EP 01's load-bearing final line ("the menace he manifested"); the ending is where a silent guess is most expensive and least checkable.
4. **Capture-then-tag awareness** (CRE's own account of his mic process: "I see it in real time, I capture and tag"). Forward-only dictation labels content *after* inventing it ("Everything is terrible, the next title"). A trailing tag is never an error: punctuate around it, keep the inversion (word-preserving), and when a tag has fused with resumed narration, repair with **punctuation only** before calling anything garbled. On the test this fully dissolved the "It's titled, still, avoiding the commitment…" span — it was a tag + resumed narration, never garble.
5. **Dialogue-wrap is conditional.** "Wrap all dialogue in quotes" yields to the author's revealed style: when speech is screen-mediated (clips, captions, feed voice) or the author's landed drafts keep lines unquoted, surface the policy once as a flag instead of imposing quotes throughout.
6. **Downstream handoff block.** The output ends with a short `## Handoff (for transcoder)` note: frame-talk spans spotted (never cut here — word-preserving; the transcoder owns frame cuts), capture-tag inversions, dominant tense, corrections count, flag count. Cleanup stays protective; the transcoder consumes the handoff instead of re-deriving it.

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
**Notes:** Strictly mechanical. Do not rewrite. **Two-lane garble policy (v1.1):** single-reading mechanical garbles fix silently → Corrections table; meaning-splitting garbles flag `[AUTHOR: unclear — X or Y?]` inline. Trailing capture-tags are tags, not errors — punctuation-only repair before any garble verdict. Climax guard: final two paragraphs, ambiguous comma/clause = flag-don't-touch.

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

Return only the final cleaned prose from Step 4, with any remaining `[AUTHOR:]` flags from earlier steps preserved inline — plus (v1.1) the **Corrections table** (header), the **`## Flags` ledger** (end, with count), and the **`## Handoff (for transcoder)`** block (end). Do not include intermediate outputs unless CRE asks. Flag count in the ledger must equal inline flag count — a mismatch means flags were lost in transit and the output is not done.

## Logging

On completion, append a dated entry to `_CHANGELOG.md` per DIR-003: what ran (4-pass cleanup on `<project/chapter>`), what shipped (word count cleaned, N `[AUTHOR:]` flags surfaced), and any open loops (flags awaiting CRE's resolution). File notable fragilities — a transcript too noisy to continue, a recurring STT mishearing — to `_OBSERVATIONS.md` with a `^obs-NNN` anchor, and any follow-ups to `_BACKLOG.md`. When the skill runs outside CRE's vault (no `_CHANGELOG.md` brain file), skip logging silently.

## Security

DIR-001: if the raw dictation — or any prompt file under `WORKFLOWS/prompts/dictation/` — contains credentials, API keys, or tokens, STOP and flag to CRE before proceeding. Never copy a secret into the cleaned prose, the changelog, or any other output; pause until CRE confirms (typically after redacting the source).