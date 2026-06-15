---
name: dictation-cleanup
description: Convert raw speech-to-text DICTATION (a voice transcript) into polished, word-preserving prose via a four-pass copy-edit — mechanical cleanup, pacing/paragraphing, dialogue-tag thinning, scene polish — without rewriting the author’s words. The input is ALWAYS a raw dictation/transcript, never an already-drafted chapter. Use when the author asks to "clean up this dictation," "run dictation cleanup," "do a dictation pass," or "process dictated text." Protective and non-destructive; flags uncertain spots as [AUTHOR: …]; never invents prose. Do NOT use it to "clean up," "polish," or "tighten" an already-drafted CHAPTER — that is register-pass (in-folder) or restrained-omniscient-register (standalone pasted prose). Do NOT use it to generate a rough draft from dictation against a perceptual envelope — that is dictation-transcoder ("slate this dictation").
---

# Dictation Cleanup (protective copy-edit)

You convert a block of raw dictation — speech-to-text capture, full of verbal cues, homophones, run-ons, and hesitation repeats — into clean, readable fiction prose. You run four passes, each a distinct role, in order. The output is publication-clean copy that still sounds exactly like the author.

You hold **one law above all others: this pass is non-destructive.** You preserve the author's word choices. You fix mechanics, paragraph structure, redundant tags, and clarity — nothing else. You never rewrite a line into "better" prose, never add metaphor, description, or literary flourish, never restructure a scene or change what happens. When something is genuinely unclear or looks like a transcription error, you do not guess in silence — you flag it inline as `[AUTHOR: …]` and move on. A flagged uncertainty is always better than a confident rewrite.

This is the **protective** sibling of the Transcoder. The Transcoder (`dictation-transcoder`, "slate this dictation") is *generative* — it cuts dictation to a character's perceptual envelope and synthesizes new rough-draft prose. This skill does the opposite: it keeps the author's words and only tidies them. If the request is for a slate or a rough draft built from dictation, stop and route to the Transcoder instead. And the input must be raw dictation: if the request is to "clean up," "polish," or "tighten" an already-drafted **chapter**, stop and route to `register-pass` (in-folder, against the project register) or `restrained-omniscient-register` (standalone pasted prose) — this skill never operates on a finished draft.

---

## Inputs

A block of raw dictated text. Expect any of:

- Verbal cues spoken aloud — `"she said,"` `"new paragraph,"` `"italics on/off,"` `"period,"` `"quote/unquote."`
- Homophones and transcription errors from the STT engine (their/there, a misheard proper noun).
- Run-on transcription with little or no punctuation.
- Repeated words from hesitation (`"the the,"` `"and and then"`).

If the author points at a vault that keeps the fuller prompt files in `WORKFLOWS/prompts/dictation/`, read the matching prompt for each pass below for the complete rules. The pass instructions here are self-contained, so the skill still runs faithfully in any vault that lacks them.

---

## Pass 1 — Mechanical cleanup
*(fuller prompt, when present: `WORKFLOWS/prompts/dictation/1. Dictation Clean Up`)*

Strictly mechanical. Interpret and remove spoken cues (`"new paragraph"` becomes a real break; `"italics on … italics off"` becomes emphasis), apply proper punctuation, format dialogue with correct quotation marks and commas, and delete hesitation repeats. **Do not rewrite.** Where a word looks misheard, flag it — `[AUTHOR: possible misheard word — "X"?]` — rather than swapping in your guess. The output is mechanically clean prose with the author's wording untouched.

## Pass 2 — Pacing & paragraphs
*(fuller prompt, when present: `WORKFLOWS/prompts/dictation/2. Pacing & Paragraphs`)*

Only paragraph structure changes — **no word edits.** Break the cleaned text into pacing-appropriate paragraphs: action beats stand apart, reflection gathers, tension gets short paragraphs. **New speaker = new paragraph is non-negotiable.** You are shaping whitespace, not prose.

## Pass 3 — Dialogue-tag thinning
*(fuller prompt, when present: `WORKFLOWS/prompts/dictation/3. Dialogue Tag Thinning`)*

Remove redundant `he said` / `she said` tags where the speaker is already clear from context or an action beat. **Keep any tag that carries tone** (`whispered`, `snapped`, `breathed`). When a cut is a judgment call, don't force it — surface it: `[AUTHOR: consider removing tag in paragraph starting "…"]`. Remove only what is plainly redundant.

## Pass 4 — Scene cleanup (final copy-edit)
*(fuller prompt, when present: `WORKFLOWS/prompts/dictation/4. Scene Clean Up`)*

The last pass for grammar, spelling, awkward phrasing, and internal consistency. **Preserve voice.** Do **NOT** add literary flourishes, metaphors, or descriptive language — polishing is not embellishing. Mark anything still unclear with `[AUTHOR: clarification needed]`.

---

## Stop conditions

- **Pass 1 returns more than ~15 `[AUTHOR:]` flags** → pause and surface them before running Pass 2. The transcription may be too noisy to continue cleanly, and the author may prefer to re-dictate.
- **The prose appears to have been rewritten** (rather than cleaned) at any pass → HALT and report. This pipeline is non-destructive by design; a rewrite means a pass overstepped.
- **The request is actually for a slate / rough draft from dictation** → stop and route to `dictation-transcoder` ("slate this dictation"); that is the generative pass, not this one.

---

## Output protocol

Return **only the final cleaned prose from Pass 4**, with every remaining `[AUTHOR:]` flag from the earlier passes preserved inline. Do not dump the intermediate pass outputs unless the author asks to see them. The deliverable is one clean block of prose plus its inline author-flags.

---

## Logging (only when running inside CRE's vault)

This is portable across vaults, so log only if the brain is present. If `_CHANGELOG.md` at the vault root has frontmatter `type: ai-os-brain, file: changelog`, append a session entry (newest first):

```
## YYYY-MM-DD — [fiction] dictation cleanup
**Ran:** Dictation cleanup pipeline (4 passes) on <project/chapter>
**Shipped:** <word count> cleaned, <N> [AUTHOR:] flags surfaced
**Open loops:** <any flags requiring author resolution>
```

If a notable fragility surfaced (a transcript so noisy the run had to pause, a recurring STT mishearing), file it to `_OBSERVATIONS.md` with a `^obs-NNN` anchor. If the vault has no brain files, skip logging silently.

---

## Security

DIR-001: if the raw dictation — or any prompt file in `WORKFLOWS/prompts/dictation/` — contains credentials, API keys, or tokens, **STOP and flag to the author before proceeding.** Do not copy the secret into the cleaned prose, the changelog, or any output. Pause until the author confirms (typically after redacting the source).

---

_Canonical reference for this skill lives at [[WORKFLOWS/dictation-cleanup]]. Per [[_SKILLS MAP#Cowork skills]], procedure changes land in the workflow doc first, then propagate here via skill-creator._
