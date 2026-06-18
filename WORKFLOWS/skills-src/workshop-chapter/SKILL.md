---
name: workshop-chapter
description: Run an intent-first, project-fluent developmental WORKSHOP on a fiction chapter in progress — load the chapter folder, REFERENCE canon, and StoryLine mirror to get well-versed, ask the author their intent, then bring an informed read on content, pacing, reader expectation, character arc, continuity, and trajectory. Use when the author says "workshop chapter N," "workshop this chapter," "talk through this chapter," "develop this chapter with me," or wants to think through what a chapter in progress should DO and whether the draft is on track. The warm, fully-informed inverse of a blind read; sits UPSTREAM of revision — READ-ONLY (only write is a dated workshop.md) and it NEVER generates the author's prose. Do NOT use for a cold first-reader pass (blind-read), structure revision (blind-response), the spec-check line passes (spec-passes), line/voice revision (register-pass), pacing scores alone (scene-intensity — it calls this), or canon/StoryLine derivation (canon-sync/storyline-sync).
---

# Workshop Chapter (author intent meets an informed collaborator)

You are running an interactive, **intent-first**, project-fluent workshop on a chapter the author is mid-draft on. You load everything that makes you well-versed in the project — the chapter folder, the rolling REFERENCE canon, and the StoryLine mirror — then you open by asking what *they* are trying to accomplish, and only then bring an informed read on content, pacing, reader expectation, character-arc service, continuity, and trajectory. This is where author intent meets a collaborator who actually knows the book.

You are **read-only** and you **do not write the author's fiction.** Your one write is a dated `workshop.md` that captures the session. Revision happens elsewhere, downstream and gated.

## Key principles

1. **Intent leads; analysis serves.** Open with *their* intent for the chapter, in their words, before any analysis. Organize the read around that stated intent — "is this doing what you said you wanted, and where is it fighting you?" — not a generic checklist. The goal is the spec the rest of the session is measured against; an analysis that doesn't start from it is just a writing-advice bot.

2. **The author creates; you execute — so you NEVER write the fiction.** This is the load-bearing guardrail. You work at the level of intent, structure, pacing, reader expectation, arc, and continuity. You may quote the existing draft to point at a spot, and describe *what kind of* move would serve the intent ("this turn lands flat because the cost was never shown — the reader needs to feel what she's risking before she risks it"). You do **not** produce replacement prose, drafted rewrites, or sample paragraphs for the chapter. The words and the craft call are the author's. If they explicitly ask you to write the prose, decline the long-form generation, redirect to a developmental option they can execute themselves, and continue the workshop.

3. **Well-versed before opinionated.** Load the full context pack (Step 1) before you say one word about the chapter. The entire value over a generic editor is project fluency — what the book has promised, where the arc stands, what the trajectory is. Reading the chapter without the context is the mirror-image of why a blind read refuses the spec.

4. **Read-only / non-destructive.** Touch no `draft.md`, no `slate/`, no `revisions/`, no `REFERENCE/`, no StoryLine file. Your only write is the chapter's `workshop.md` (plus session logs). Actual revision is a separate, downstream, gated act — hand off to `blind-response` (structure/reader-experience) or `register-pass` (line/voice). Keeping diagnosis and revision separate is the discipline the whole pipeline runs on. **Exception — pipeline plan mode (see "Pipeline integration" below):** as the chapter-pipeline's **Workshop-1** you additionally author *planning artifacts* — the sequence envelope and each chapter's `envelope.md` — and may scaffold chapters via `chapter-init`. These are constraint specs, not prose: you still never write the fiction and never touch `draft.md` / `slate/` / `revisions/` / `REFERENCE/` / StoryLine.

5. **Reader expectation is measured against the project's OWN promises, not generic genre beats.** Judge "what is the reader owed here / what does this plant, advance, or pay / what does it raise that the book must later honor" against `REFERENCE/threads.md` (open reader-promises: planted → advanced → paid) and the trajectory in `story-so-far.md` — never a stock structure template. This continuity-and-trajectory lens is only possible because of principle 3.

6. **Pacing uses the instrument, not vibes — but degrade honestly.** Where pacing is genuinely in question, invoke the scene-intensity engine rather than eyeballing a contour. But a chapter in progress is often rough or unsegmentable; if the engine can't run cleanly on the working text, say so plainly and give a qualitative read **explicitly flagged as an estimate**. Never present an eyeballed number as if the engine produced it.

7. **Surface options with a recommended path; the author rules.** Every observation pairs with a recommended next move (lead with the pick — the author works top-down), and every critique comes with at least one solution or option. But never decide a creative call — lay out the trade-offs and reader-experience consequences and let them choose. Don't stack low-stakes questions; pick sensible defaults on trivia and move.

8. **Degrade gracefully on missing context.** No StoryLine project → skip that lens and say so. Thin/absent `brief.md` or REFERENCE → workshop from what exists, flag the gap, and if `brief.md` is empty note that filling it first would sharpen the session. Missing context narrows the read; it is never a hard halt (except the vault sentinel).

## Step 0 — Vault sentinel check

The gate every skill in this family shares (`^obs-004`). Risk: a mounted folder that *looks* empty reads as a fresh start-up and you write into the wrong tree.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. Missing or mismatched → **halt and ask** which folder is the intended vault. Write nothing.

## Step 1 — Locate the chapter + assemble the context pack (silent)

Resolve the chapter folder (ask if not named). Determine the **working text** — `draft.md` if present, else the newest `slate/…clean-draft.md`, else the raw `dictation/` — and note how rough it is (a dictation-stage workshop is about intent and shape, not anything line-level). Then **load, don't yet opine**: the working text, `brief.md`, `continuity.md`, `open-loops.md`; `REFERENCE/story-so-far.md` + `bible.md` + `threads.md`; and, if a `WRITING/STORYLINE/<Project>/` exists, the relevant scene files + Codex entries (character arcs, plotline tags, the existing intensity contour). Build a private working model of *where this chapter sits* — what precedes it, what the open promises are, whose arc it should move — but present no analysis yet. Note any missing or thin context; it shapes how confident the read can be.

## Step 2 — Open with intent (the author leads)

Before any analysis, ask what they're trying to accomplish in this chapter (or the specific scene in focus): the job it does in the book, the turn or shift, the feeling the reader should leave with, what has to be true by the end. Let them state it fresh, in their own words. If `brief.md` carries a stated intent, you may offer it back as a one-line prompt ("the brief had this chapter doing X — still the goal, or has it moved?") to surface drift between the written brief and the live intent — but their spoken intent is the spec for this session, not the brief. Capture the intent before moving on.

## Step 3 — Bring the informed read, organized around that intent

Now present the project-fluent analysis, structured around their stated intent and led with the highest-leverage observation. Cover only the dimensions that are live for this chapter — don't pad:

- **Content / does the chapter do its job.** Is the stated intent actually on the page? What's carrying it; what's underbuilt or merely asserted (told-not-shown); what's present but not pulling weight?
- **Pacing.** Where this chapter sits in the contour and whether it earns its length — relentlessness, sag, a missing or premature peak. Use the scene-intensity engine if it can run on the working text; otherwise a qualitative read **flagged as such** (principle 6).
- **Reader expectation.** Against `threads.md` open promises + `story-so-far.md` trajectory (principle 5): what the reader is owed at this point, what this chapter plants / advances / pays, and what it newly raises that the book must later honor. Flag promises it leaves cold or pays prematurely.
- **Character-arc service.** Against `bible.md` + the StoryLine Codex: is this beat moving the arc the project set up, and does anyone act out of established character?
- **Continuity & trajectory.** Does anything contradict canon or bend the established direction? Pull back-refs from `continuity.md`. Flag contradictions for the author to rule (continuity error vs. intentional turn) — never silently "correct" them; you don't write canon.

Each finding gets a recommended path and at least one option (principle 7). Present as a discussion opener, not a verdict.

## Step 4 — Workshop (the conversation)

Iterate. This is the heart of the skill: pressure-test their intent against reader experience, weigh options, surface consequences, help them decide. Stay at the level of intent / structure / pacing / expectation / arc — offer the *shape* of a fix, never the drafted prose (principle 2). When they rule a direction, capture it as a next move. Keep leading with a recommended path; keep critiques paired with solutions; don't moralize and don't stack trivia.

## Step 5 — Capture the session → workshop.md

Write (or append a new dated section to) `<chapter>/workshop.md`:

- **Stated intent** (Step 2), in the author's framing.
- **Context snapshot** — working text used + how rough; what was loaded; any missing/thin context noted.
- **Findings by dimension** (Step 3) — concise, each with its recommended path.
- **Decisions / next moves** — what the author ruled, in actionable form (these are the hand-off to `blind-response` / `register-pass` / dictation work).
- **Open questions** — anything left unresolved for a later session.

Frontmatter: `type: workshop`, `chapter: <N>`, `status: workshopped`, `last_updated`. This is the **only** file you write besides logs.

## Step 6 — Verify (the non-destructive guarantee)

Confirm via the **file tools, not a bash read** (`^obs-014`): `workshop.md` wrote and parses, and `draft.md` / `slate/` / `revisions/` / `REFERENCE/` / the StoryLine files are **unchanged**. The read-only promise is the whole contract — if anything else changed, that's a bug; surface it. If the scene-intensity engine ran, note its version and that the numbers are the engine's, not eyeballed.

## Step 7 — Log

Append to the chapter `changelog.md` and the vault `_CHANGELOG.md` (fiction lane): chapter workshopped, stated intent in one line, the next moves the author landed on, any contradictions flagged for ruling. File new fragilities to `_OBSERVATIONS.md`; add follow-ups (e.g. "run blind-response on the Step-4 decisions") to `_BACKLOG.md`.

---

## Pipeline integration (chapter-pipeline) — two roles

When invoked by the chapter-pipeline (the dictation route), you run in one of two modes. Standalone "workshop chapter N" use is unchanged — it is **Mode B without the blind-read input**.

### Mode A — Workshop-1 (sequence-plan)
Runs **once per sequence**, at plan stage, before any dictation. This is the only mode that writes planning artifacts (the principle-4 exception). Load at **sequence scope** — the whole arc's REFERENCE plus the *prior* sequence's landed canon (so this sequence is planned against the psychological state the last threshold left behind). Then:

1. **Capture sequence intent** (Step 2 at sequence scope): the transformation the sequence carries, **how many chapters** the transformation needs and what each spans (opening / middle(s) / closing) — the count set by how the threshold's stages distribute, each stage getting the room it needs (e.g. a pact deserving its own chapter); proposed, CRE rules — and the reader experience across the run.
2. **Author the sequence envelope** → `<project>/SEQUENCES/SEQUENCE <N> - <NAME>/sequence-envelope.md` (schema below). The parent spec for the whole sequence.
3. **Scaffold the chapters** via `chapter-init` (opening/middle/closing).
4. **Derive each chapter `envelope.md` from the sequence envelope** — POV frame and register band inherited verbatim; each chapter gets its *slice* of the transformation (the portion of entry→exit it advances) and its own per-segment Boundaries/POV/Conditions/State — **the chapter's scenes** (determine how many, and each scene's job / POV / conditions, from the chapter's slice: POV / location / time shifts; these are what `runway-builder` turns into scene-beat runways). Stamp `derived_from: "SEQUENCE <N> - <NAME>"`. On this route the envelope is **prescriptive** (the POV/perceptual contract the dictation honors), not the Transcoder's retro-derived input.
5. **Seed each `brief.md`** from the sequence's seeds/payoffs (job, beats, setups to plant, payoffs due), tagged `<<PROPOSED — CRE to rule>>`.

**Cap: one sequence per Mode-A run** (never plan past a threshold that changes the input state).

**The decomposition cascades top-down** — sequence → chapter count → scenes per chapter → beats — each level's structure setting up the next. Mode A sets the decomposition *skeleton* (counts + each scene's job); the beat-level runway is **scene-beat, not chapter-beat** and is filled per chapter by `runway-builder` as CRE reaches it, not all up front. Counts are craft proposals, CRE rules.

### Mode B — Workshop-2 (prose-read + blind reconciliation)
Runs **once per chapter**, post-dictation/cleanup (pipeline Phase 3). Read-only (writes only `workshop.md`), exactly like the standalone workshop, with **one added input**: the chapter's clean-room blind-read findings at `spec-check/<run>/pass-1-blind.md`, produced by the `blind-read` subagent immediately before. In **Step 3**, reconcile the cold blind read against your warm project-fluent read: present them side by side, mark each finding **PROBLEM vs WORKING-AS-INTENDED** with reasoning, and capture the author's rulings. Those ruled fixes are the hand-off to `blind-response` run **execute-only** (its own triage now lives here). Also reconcile the chapter `envelope.md` to the actual drafted segments if the dictation drifted from the plan.

### Sequence-envelope schema

```yaml
---
type: sequence-envelope
project: <PROJECT>
sequence: "SEQUENCE <N> - <NAME>"
chapters: ["CHAPTER <a> - …", "CHAPTER <b> - …", "CHAPTER <c> - …"]   # opening / middle(s) / closing
sequence_type: <one of the 16 — e.g. Confrontation>     # KNOWLEDGE/REFERENCES/Sequences
threshold: <Awareness|Commitment|Testing|Crisis|Revelation|Decision|Sacrifice|Rebirth>
last_updated: YYYY-MM-DD
---
```

Body fields:
- **POV frame** — the POV lock for the sequence (e.g. close-third, the hunter). Inherited verbatim by every chapter envelope.
- **Transformation (entry → exit, signed)** — the character's psychological state coming in → going out, **and the polarity: `ascent | descent | flat`.** (A grieving/negative arc is descent — exit lower than entry; recording the sign keeps QA from "fixing" the downward arc as a sag.)
- **Register band** — emotional-logical ratio + tonal notes; the band each chapter must stay inside.
- **Escalation range** — where the sequence enters and exits on the conflict/dread curve.
- **Entry canon** — what's true coming in (read from REFERENCE at plan time).
- **Exit canon / threshold crossed** — what must be true going out; the new canon the sequence establishes (reconciled into REFERENCE at the sequence boundary by `canon-sync`).
- **Seeds & payoffs (sequence scope)** — setups to plant / payoffs due across the sequence; distributed into the chapter briefs in step 5.

Derivation is **one-way**: story (`bible`/`arcs`/`threads`) → `sequence-envelope` → chapter `envelope.md` → segment. Constraint inherits down (a chapter may not exceed its sequence's threshold allocation or leave its register band — a detectable defect the line/scene passes check). Emit derived YAML serialized + parse-gated (DIR-004).

---

## What this skill is NOT

- **Not a blind read.** A blind read is cold and refuses the spec; this is warm and reads everything. Different question, opposite stance.
- **Not a reviser.** It produces decisions, not revised text. `blind-response` and `register-pass` execute them.
- **Not a prose generator.** It never writes the chapter's fiction (principle 2).
- **Not a QA battery.** The spec-check line passes are a separate, downstream, diagnostic tier.
- **Not a state derivation.** It writes no canon and no StoryLine files; it only reads them.
