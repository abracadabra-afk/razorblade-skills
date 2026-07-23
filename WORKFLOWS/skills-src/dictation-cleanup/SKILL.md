---
name: dictation-cleanup
description: Convert raw speech-to-text DICTATION (a voice transcript) into polished, word-preserving prose via a four-pass copy-edit — mechanical cleanup, pacing/paragraphing, dialogue-tag thinning, scene polish — without rewriting the author’s words. The input is ALWAYS a raw dictation/transcript, never an already-drafted chapter. Use when the author asks to "clean up this dictation," "run dictation cleanup," "do a dictation pass," or "process dictated text." Protective and non-destructive; flags uncertain spots as [AUTHOR: …]; never invents prose. Do NOT use it to "clean up," "polish," or "tighten" an already-drafted CHAPTER — that is register-pass (in-folder) or restrained-omniscient-register (standalone pasted prose). Do NOT use it to generate a rough draft from dictation against a perceptual envelope — that is dictation-transcoder ("slate this dictation").
---

# Dictation Cleanup (protective copy-edit, v1.1)

> v1.1 (2026-07-22): two-lane garble policy, flag ledger, climax guard, capture-then-tag awareness, conditional dialogue-wrap, transcoder handoff block — amended off the doomscroller ground-truth test (`SYSTEM/reports/2026-07-22-dictation-cleanup-test.md`), aligned with transcoder v5.1's artifact vocabulary.

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

Strictly mechanical. Interpret and remove spoken cues (`"new paragraph"` becomes a real break; `"italics on … italics off"` becomes emphasis), apply proper punctuation, format dialogue, and delete hesitation repeats. **Do not rewrite.** The output is mechanically clean prose with the author's wording untouched.

**Two-lane garble policy (v1.1 — replaces flag-everything).** The old law ("flag every suspected mishear") put an ordinary clean dictation at its own too-noisy threshold and trained flag-fatigue — which is how a prior run drifted into silent fixes with no record and a silent climax mis-punctuation:

- **Lane 1 — mechanical:** a garble with exactly ONE plausible reading in context ("chainsaw *shade*" beside "bike chain"; "gas *camp*"; "*porn* apart"; "un*kept*"; "*worse* of all") → fix silently, and record every fix in a **Corrections table** at the top of the output (`heard → fixed`). Visible, reversible, no inline clutter.
- **Lane 2 — meaning-splitting:** two readings both parse ("layer"/"lair"), a displaced clause, an unrecoverable span → keep the dictated form, flag `[AUTHOR: unclear — X or Y?]` inline. A rescue may ask a question; it may never make a decision.

**Capture-then-tag awareness (v1.1 — shared with transcoder v5.1).** The author dictates forward-only and labels content after inventing it: *"Everything is terrible, the next title"* ("I see it in real time, I capture and tag"). A trailing tag ("…, the next title", "…, the caption", "…, it's titled") is a tag, not an error: punctuate around it and keep the inversion (this pass is word-preserving). When a tag has fused with resumed narration into an apparent garble, attempt a **punctuation-only** repair first — reattach the tag to its content and re-read what remains as narration. Only if that fails is it Lane-2 garble. First suspect on any odd span containing a naming word (title, caption, called, tagged).

**Climax guard (v1.1).** In the final two paragraphs of any piece, an ambiguous comma or clause boundary — above all on a sentence-final clause — is **flag-don't-touch**, Lane 1 exemptions included. A displaced comma there can invert the story's meaning (the "menace he manifested" instance), and the ending is where a silent guess is most expensive.

**Dialogue-wrap is conditional (v1.1).** Wrap plainly conversational speech in quotes per the mechanical rules — but when speech is screen-mediated (clips, captions, feed voice) or the author's landed drafts keep lines unquoted, do not impose quotes throughout; surface the policy once as a single `[AUTHOR: quote policy?]` flag and leave the lines as dictated.

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

- **Pass 1 returns more than ~15 Lane-2 `[AUTHOR:]` flags** → pause and surface them before running Pass 2. The transcription may be too noisy to continue cleanly, and the author may prefer to re-dictate. (v1.1: Lane-1 silent fixes do NOT count toward this threshold — under the old flag-everything law an ordinary clean dictation hit 15 and the threshold measured the law, not the audio.)
- **The prose appears to have been rewritten** (rather than cleaned) at any pass → HALT and report. This pipeline is non-destructive by design; a rewrite means a pass overstepped.
- **The request is actually for a slate / rough draft from dictation** → stop and route to `dictation-transcoder` ("slate this dictation"); that is the generative pass, not this one.

---

## Output protocol

Return **only the final cleaned prose from Pass 4**, with every remaining `[AUTHOR:]` flag from the earlier passes preserved inline — plus three v1.1 blocks:

1. **Corrections table** (top): every Lane-1 silent fix, `heard → fixed`, one per line.
2. **`## Flags` ledger** (end): every inline `[AUTHOR:]` flag restated with a count in the header. **Ledger count must equal inline count** — a mismatch means flags were lost in transit (the bug that once dropped 8 of 8) and the output is not done.
3. **`## Handoff (for transcoder)`** (end): frame-talk spans spotted (do NOT cut them — this pass is word-preserving; the transcoder's `frame` reason owns that cut), capture-tag inversions noted, dominant tense, corrections count, flag count. The transcoder consumes this instead of re-deriving it.

Do not dump the intermediate pass outputs unless the author asks to see them.

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
