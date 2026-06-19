---
type: workflow
name: workshop-chapter
trigger: workshop chapter
aliases: [workshop this chapter, workshop the chapter, let's workshop chapter N, help me workshop this chapter, talk through this chapter, develop this chapter with me, be my editor on this chapter]
inputs: [the in-progress chapter folder (working text = draft.md if present, else newest slate/clean-draft, else dictation), the chapter's brief.md (forward intent), continuity.md, open-loops.md, REFERENCE/story-so-far.md + bible.md + threads.md (trajectory + open reader-promises), the StoryLine project under WRITING/STORYLINE/<Project>/ if one exists, the scene-intensity engine for the pacing read]
outputs: [an interactive, intent-first workshop conversation about the chapter; a dated workshop.md saved to the chapter folder capturing stated intent, the informed read by dimension, the decisions/next moves CRE landed on, and open questions. NO change to draft.md, slate/, revisions/, REFERENCE/, or StoryLine — read-only on everything but workshop.md]
lane: fiction
status: draft
last_updated: 2026-06-18
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). REFERENCE/ and StoryLine deepen the read but are not required — the workshop degrades gracefully when either is thin or absent. First intended adopter — Witchwood.
pipeline_position: A mid-draft DEVELOPMENTAL thinking partner that sits UPSTREAM of the QA/revision machinery, not inside it. It is the deliberate inverse of [[WORKFLOWS/spec-check]] Pass 1 (`blind-read`), which reads cold and ignorant; workshop-chapter reads fully project-informed and in dialogue with the author. It does not revise (`blind-response` / [[WORKFLOWS/register-pass]] do that), does not run the line passes ([[WORKFLOWS/spec-check]]), and does not derive state ([[WORKFLOWS/canon-sync]] / [[WORKFLOWS/storyline-sync]]). It INVOKES the scene-intensity engine for the pacing read (caller, not owner). It answers the question those tools can't: "what is this chapter trying to do, and is the draft on track to do it — given everything the project has set up?" When invoked by [[WORKFLOWS/chapter-pipeline]] (the dictation route) it gains two roles — **Workshop-1** (sequence-plan: authors the sequence envelope, derives chapter envelopes, scaffolds the chapters) and **Workshop-2** (prose-read: reconciles the clean-room blind-read findings before CRE rules). See "Pipeline integration".
---

# WORKFLOW: Workshop Chapter (intent meets an informed collaborator)

> An interactive, **intent-first**, project-fluent workshop on a chapter you're mid-draft on. It loads everything that makes it well-versed in the project — the chapter folder, the rolling REFERENCE canon, and the StoryLine mirror — then opens by asking what *you* are trying to accomplish, and only then brings an informed read on content, pacing, reader expectation, character-arc service, continuity, and trajectory. This is where author intent meets a collaborator who actually knows the book. It is **read-only**: it never touches the draft and never writes your fiction for you. Its one write is a dated `workshop.md` that captures the session.

## Key principles

1. **Intent leads; analysis serves.** The session opens with *your* intent for the chapter/scene, captured in your words, before any analysis. The informed read is then organized around that stated intent — "is this doing what you said you wanted, and where is it fighting you?" — not against a generic checklist. An analysis that doesn't start from your goal is just a writing-advice bot; the goal is the spec the rest of the session is measured against.

2. **AI executes; CRE creates — so this skill never writes the fiction.** This is the load-bearing guardrail (the [[_ME]] / [[_SKILLS MAP#Cross-cutting rules]] rule applied). The workshop works at the level of intent, structure, pacing, reader expectation, arc, and continuity. It may quote the existing draft to point at a spot, and it may describe *what kind of* move would serve the intent (e.g. "this turn lands flat because the cost was never shown — the reader needs to feel what she's risking before she risks it"). It does **not** generate replacement prose, drafted rewrites, or sample paragraphs for the chapter. The craft call and the words are CRE's; the skill is the informed administrative/analytical collaborator around them. If CRE explicitly asks for prose, decline the long-form generation and redirect to a developmental option he can execute himself.

3. **Well-versed before opinionated.** Load the full context pack (Step 1) before saying one word about the chapter. The entire value over a generic editor is project fluency — what the book has promised, where the arc stands, what the trajectory is. Reading the chapter without the context is malpractice here, the mirror-image of why `blind-read` refuses the spec.

4. **Read-only / non-destructive.** The workshop touches no `draft.md`, no `slate/`, no `revisions/`, no `REFERENCE/`, no StoryLine file. Its only write is the chapter's `workshop.md` (plus the session logs). Actual revision is a separate, downstream, gated act — hand off to `blind-response` (structure/reader-experience) or [[WORKFLOWS/register-pass]] (line/voice). Keeping diagnosis and revision separate is the same discipline the rest of the pipeline runs on. **Exception — pipeline plan mode (see "Pipeline integration").** When run as the chapter-pipeline's **Workshop-1**, the skill additionally authors *planning artifacts* — the sequence envelope and each chapter's `envelope.md` — and may scaffold chapter folders via [[WORKFLOWS/chapter-init]]. These are constraint specs, not prose: the rules that it never writes the fiction and never touches `draft.md` / `slate/` / `revisions/` / `REFERENCE/` / StoryLine still hold in full.

5. **Reader expectation is measured against the project's own promises, not generic genre beats.** Judge "what is the reader owed here / what does this plant, advance, or pay / what does it raise that the book must later honor" against `REFERENCE/threads.md` (open reader-promises: planted → advanced → paid) and the trajectory in `story-so-far.md` — not against a stock structure template. This is the continuity-and-trajectory lens CRE asked for, and it's only possible because of principle 3.

6. **Pacing uses the instrument, not vibes — but degrades honestly.** Where pacing is genuinely in question, invoke the scene-intensity engine rather than eyeballing a contour (same discipline as [[WORKFLOWS/storyline-sync]] principle 4). But a chapter in progress is often rough or unsegmentable; if the engine can't run cleanly, say so plainly and give a qualitative contour **explicitly flagged as a qualitative estimate**, not a score. Never present an eyeballed number as if the engine produced it.

7. **Surface options with a recommended path; CRE rules.** Every observation pairs with a recommended next move (CRE works top-down and wants the pick led with), and every critique comes with at least one solution or option ([[_ME]] voice rule). But the workshop never decides a creative call — it lays out the trade-offs and reader-experience consequences and lets CRE choose. Don't stack low-stakes questions; pick sensible defaults on trivia and move.

8. **Degrade gracefully on missing context.** No StoryLine project → skip that lens and say so. Thin/absent `brief.md` or REFERENCE → workshop from what exists, flag the gap, and (if `brief.md` is empty) note that filling it first would sharpen the session. Missing context narrows the read; it is never a hard halt (except the vault sentinel).

## Inputs

- **The chapter** — the in-progress per-chapter folder. If not named, ask. **Working text** = `draft.md` if present; else the newest `slate/…clean-draft.md`; else the raw `dictation/`. State which was used and how rough it is (a dictation-stage workshop is about intent and shape, not line-level anything).
- **The chapter's intent surface** — `brief.md` (forward intent: job, beats, setups to plant, payoffs due, seal schedule), `open-loops.md`, `continuity.md`.
- **Project trajectory + promises** — `REFERENCE/story-so-far.md`, `REFERENCE/bible.md`, `REFERENCE/threads.md`.
- **Analytical lens (optional)** — the StoryLine project under `WRITING/STORYLINE/<Project>/` (scene contour, Codex character arcs, plotlines), and the scene-intensity engine for the pacing read.

## Outputs

| What | Destination |
|---|---|
| The workshop conversation (intent capture → informed read → iterate) | the session itself |
| A dated workshop record (stated intent, context snapshot, findings by dimension, decisions/next moves, open questions) | `<chapter>/workshop.md` (append a new dated section per session) |
| Everything else | **unchanged** — read-only on draft/slate/revisions/REFERENCE/StoryLine |

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. Write nothing.

### Step 1 — Locate the chapter + assemble the context pack (silent)
Resolve the chapter folder (ask if not named). Determine the working text (`draft.md` → newest slate clean-draft → dictation) and note how rough it is. Then **load, don't yet opine**: the working text, `brief.md`, `continuity.md`, `open-loops.md`; `REFERENCE/story-so-far.md` + `bible.md` + `threads.md`; and, if a `WRITING/STORYLINE/<Project>/` exists, the relevant scene files + Codex entries (character arcs, plotline tags, the existing intensity contour). Build a private working model of *where this chapter sits* — what precedes it, what the open promises are, whose arc it should be moving — but do not present analysis yet. Note any context that's missing or thin (it shapes how confident the read can be).

### Step 2 — Open with intent (the author leads)
Before any analysis, ask CRE what he's trying to accomplish in this chapter (or the specific scene in focus): the job it does in the book, the turn or shift, the feeling the reader should leave with, what has to be true by the end. Let him state it fresh and in his own words. If `brief.md` carries a stated intent, you may offer it back as a one-line prompt ("the brief had this chapter doing X — still the goal, or has it moved?") to surface drift between the written brief and the live intent — but CRE's spoken intent is the spec for this session, not the brief. Capture the intent before moving on.

### Step 3 — Bring the informed read, organized around that intent
Now present the project-fluent analysis, structured around CRE's stated intent and led with the highest-leverage observation. Cover the dimensions that are live for this chapter (not all are always relevant — don't pad):

- **Content / does the chapter do its job.** Is the stated intent actually on the page? What's carrying it; what's underbuilt or merely asserted (told-not-shown); what's present but not pulling weight?
- **Pacing.** Where this chapter sits in the contour and whether it earns its length — relentlessness, sag, a missing or premature peak. Use the scene-intensity engine if it can run on the working text; otherwise a qualitative read **flagged as such** (principle 6).
- **Reader expectation.** Measured against `threads.md` open promises + `story-so-far.md` trajectory (principle 5): what the reader is owed at this point, what this chapter plants / advances / pays, and what it newly raises that the book must later honor. Flag promises it leaves cold or pays prematurely.
- **Character-arc service.** Against `bible.md` + the StoryLine Codex: is this beat moving the arc the project set up, and does anyone act out of established character?
- **Continuity & trajectory.** Does anything contradict canon or bend the established direction? Pull back-refs from `continuity.md`. (Flag contradictions for CRE to rule — continuity error vs. intentional turn — never silently "correct" them; this skill doesn't write canon.)

Each finding gets a recommended path and at least one option (principle 7). Present as a discussion opener, not a verdict.

### Step 4 — Workshop (the conversation)
Iterate with CRE. This is the heart of the skill: pressure-test his intent against reader experience, weigh options, surface consequences, help him decide. Stay at the level of intent/structure/pacing/expectation/arc — offer the *shape* of a fix, never the drafted prose (principle 2). When he rules a direction, capture it as a next move. Keep leading with a recommended path; keep critiques paired with solutions; don't moralize and don't stack trivia.

### Step 5 — Capture the session → workshop.md
Write (or append a new dated section to) `<chapter>/workshop.md`:
- **Stated intent** (Step 2), in CRE's framing.
- **Context snapshot** — working text used + how rough; what was loaded; any missing/thin context noted.
- **Findings by dimension** (Step 3) — concise, each with its recommended path.
- **Decisions / next moves** — what CRE ruled, in actionable form (these are the hand-off to `blind-response` / `register-pass` / dictation work).
- **Open questions** — anything left unresolved for a later session.
Frontmatter: `type: workshop`, `chapter: <N>`, `status: workshopped`, `last_updated`. This is the **only** file the skill writes besides logs.

### Step 6 — Verify (non-destructive guarantee)
Confirm via the **file tools, not a bash read** (`^obs-014`): `workshop.md` wrote and parses, and `draft.md` / `slate/` / `revisions/` / `REFERENCE/` / the StoryLine files are **unchanged** (this is the read-only promise — if anything else changed, that's a bug; surface it). If the scene-intensity engine ran, note its version and that the numbers are the engine's, not eyeballed.

### Step 7 — Log
Append to the chapter `changelog.md` and the vault [[_CHANGELOG]] (fiction lane): chapter workshopped, stated intent in one line, the next moves CRE landed on, any contradictions flagged for ruling. File new fragilities to [[_OBSERVATIONS]]; add follow-up tasks (e.g. "run blind-response on the Step-4 decisions") to [[_BACKLOG]]. (DIR-003.)

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- Chapter folder not found / has no working text at any stage (no draft, no slate, no dictation) → halt: there's nothing to workshop yet (suggest `dictation-preflight` / the Transcoder first).
- CRE asks the skill to write the chapter's prose → decline the long-form generation (principle 2), redirect to a developmental option he can execute, and continue the workshop.

## Logging
On completion append an entry to [[_CHANGELOG]] (fiction lane) and the chapter's `changelog.md`; new follow-ups to [[_BACKLOG]]; fragilities to [[_OBSERVATIONS]]. (DIR-003.)

---

## Pipeline integration (chapter-pipeline) — two roles

When invoked by [[WORKFLOWS/chapter-pipeline]] (the dictation route), workshop-chapter runs in one of two modes. Standalone "workshop chapter N" use is unchanged — it is **Mode B without the blind-read input**.

### Mode A — Workshop-1 (sequence-plan)

> **Driven by [[KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework]]** (the spine): the transformation *is* the POV character's **fault line** + refusal arc; each chapter slice **closes one escape** along it; the closing chapter **forces the gated choice** (external win gated on the internal decision); scenes are chosen **scene-vs-sequel by contour position** (a peak is a proactive *scene* goal→conflict→disaster; after a peak, a reactive *sequel* reaction→dilemma→decision). Structure is *derived from the refusal*, not guessed.
Runs **once per sequence**, at plan stage, before any dictation. The only mode that writes planning artifacts (per the principle-4 exception). Additive to Steps 0–2; Step 1 loads at **sequence scope** — the whole arc's REFERENCE plus the *prior* sequence's landed canon (so this sequence is planned against the psychological state the last threshold left behind), **plus the working-canon overlay** (`SEQUENCES/.../working-canon.md`) so a chapter's roster can read the carried state of chapters dictated-but-not-yet-landed.

1. **Capture sequence intent** (Step 2 at sequence scope): the transformation the sequence carries, **how many chapters** the transformation needs and what each spans (opening / middle(s) / closing) — the count set by how the threshold's stages distribute, each stage getting the room it needs (e.g. a pact deserving its own chapter); proposed, CRE rules — and the reader experience across the run.
2. **Author the sequence envelope** → `<project>/SEQUENCES/SEQUENCE <N> - <NAME>/sequence-envelope.md` (schema below). This is the parent spec for the whole sequence.
3. **Scaffold the chapters** via [[WORKFLOWS/chapter-init]] (opening/middle/closing).
4. **Derive each chapter `envelope.md` from the sequence envelope** — POV frame and register band inherited verbatim; each chapter gets its *slice* of the transformation (the portion of entry→exit it advances) and its own perceptual segments (the existing per-segment Boundaries/POV/Conditions/State form). **Determine the scenes here** — those segments *are* the chapter's scenes: how many, and for each scene: its **goal** (character goal + story goal — the goal sets the beat structure), its **roster** (who is present), each present character's **carried state** (entry state / active intent, read from `arcs.md` / the prior `continuity.md` / the working-canon overlay), plus POV / conditions, from the chapter's slice (POV / location / time / who-enters-or-leaves shifts). Every present character with a live arc is an **agent the runway must give a beat-thread** — never decor. These scenes are what `runway-builder` turns into scene-beat runways. Stamp `derived_from: "SEQUENCE <N> - <NAME>"`. On this route the envelope is **prescriptive** — the POV/perceptual contract the dictation honors — not the Transcoder's retro-derived input (the line in the envelope header about being "Required input for the Transcoder" is superseded on the dictation route).
5. **Seed each `brief.md`** from the sequence's seeds/payoffs (job, beats, setups to plant, payoffs due), tagged `<<PROPOSED — CRE to rule>>` as chapter-init already does.

**Cap: one sequence per Mode-A run** (the chapter-pipeline "one sequence ahead" rule — never plan past a threshold that changes the input state).

**The decomposition cascades top-down** — sequence → chapter count → scenes per chapter → beats — each level's structure setting up the next ("as you build them, the rest builds"). Mode A sets the decomposition *skeleton* (counts + each scene's job); the beat-level runway is **scene-beat, not chapter-beat** (5–7 chapter beats leave large gaps to improvise across; scene beats are adjacent moments) and is filled **per chapter by `runway-builder` as CRE reaches it**, not all up front. Counts are craft proposals, CRE rules.

### Mode B — Workshop-2 (prose-read + blind reconciliation)
Runs **once per chapter**, post-dictation/cleanup, as the pipeline's Phase 3. Read-only (writes only `workshop.md`), exactly like the standalone workshop, with **one added input**: the chapter's clean-room blind-read findings at `spec-check/<run>/pass-1-blind.md`, produced by the `blind-read` subagent immediately before (its isolation is preserved because it ran in its own context with no spec/brief/envelope). In **Step 3**, reconcile the cold blind read against the warm project-fluent read: present them side by side, mark each finding **PROBLEM vs WORKING-AS-INTENDED** with reasoning, and capture CRE's rulings. The ruled fixes are the hand-off to `blind-response` run **execute-only** (it no longer does its own triage — that now lives here). Also reconcile the chapter `envelope.md` to the actual drafted segments if the dictation drifted from the prescriptive plan.

### Sequence-envelope schema

```yaml
---
type: sequence-envelope
project: <PROJECT>
sequence: "SEQUENCE <N> - <NAME>"
chapters: ["CHAPTER <a> - …", "CHAPTER <b> - …", "CHAPTER <c> - …"]   # opening / middle(s) / closing
sequence_type: <one of the 16 — e.g. Confrontation>     # KNOWLEDGE/REFERENCES/Sequences
threshold: <Awareness|Commitment|Testing|Crisis|Revelation|Decision|Sacrifice|Rebirth>
fault_line: <what the POV character will NOT surrender — the seam>   # Tension & Transformation Framework
arc: <positive | flat | negative>                                   # the refusal's outcome (sets the sign)
curve: <rising | spike | oscillating | plateau | slow-burn | inverted | spike-collapse>
last_updated: YYYY-MM-DD
---
```

Body fields:
- **POV frame** — the POV lock for the sequence (e.g. close-third, the hunter). Inherited verbatim by every chapter envelope.
- **Transformation (entry → exit, signed)** — the character's psychological state coming in → going out, **and the polarity: `ascent | descent | flat`.** Witchwood's grieving journey is *descent* (exit lower than entry); recording the sign makes the downward arc intentional so QA never "fixes" it as a sag. See [[KNOWLEDGE/REFERENCES/Methods/Fractal Envelope Model]].
- **Register band** — the emotional-logical ratio + tonal notes; the band each chapter must stay inside.
- **Escalation range** — where the sequence enters and exits on the conflict/dread curve.
- **Entry canon** — what's true coming in (read from REFERENCE at plan time).
- **Exit canon / threshold crossed** — what must be true going out; the new canon the sequence establishes (reconciled into REFERENCE at the sequence boundary by `canon-sync`).
- **Seeds & payoffs (sequence scope)** — setups to plant / payoffs due across the sequence; distributed into the chapter briefs in step 5.

### Derivation chain (one-way)
story (`bible`/`arcs`/`threads`) → `sequence-envelope` → chapter `envelope.md` → segment. Each level derives from its parent; the draft is the leaf. **Constraint inherits down** — a chapter may not exceed its sequence's threshold allocation or leave its register band (a *detectable* defect); the line/scene QA passes check each child against its parent envelope. **Derived YAML is serialized + parse-gated** (DIR-004).

> **One redirectable decision:** the sequence envelope is stored under a new `<project>/SEQUENCES/SEQUENCE <N> - <NAME>/` folder (parallel to `CHAPTERS/`). This keeps the prescriptive sequence spec out of `REFERENCE/` (which holds *derived* canon — mixing prescriptive + derived would break the one-way discipline). If CRE prefers another home (e.g. in the opening chapter's folder), it's a one-line change here before build.

---

## Notes

- **Why intent-first (ruled 2026-06-12).** CRE chose intent-first over context-first: the author states the goal, the informed collaborator responds to it. This keeps the skill faithful to the cross-cutting rule — CRE's creative intent is the fixed point, AI supplies the project-fluent read around it — and stops the workshop from imposing a direction the chapter was never reaching for.
- **Why read-only (ruled 2026-06-12).** Diagnosis and revision stay separate, as everywhere else in the pipeline. The workshop produces decisions; `blind-response` and `register-pass` execute them. Blurring the two would let an analysis pass quietly rewrite the book.
- **Relationship to `blind-read`.** Exact inverses by design. `blind-read` is a cold first-reader who must NOT see the spec; `workshop-chapter` is a warm collaborator who must see everything. Run a blind read when you want to know how the chapter lands on a naive reader; run a workshop when you want to think through what it should do. They answer different questions and can both feed `blind-response`.
- **Relationship to `scene-intensity`.** workshop-chapter is a *caller*. It does not reimplement pacing scoring; it runs the engine for the contour and, when the engine can't run on rough text, falls back to a flagged qualitative read.

## Skill packaging
Bundled as `SKILLS/workshop-chapter.skill` per the [[_SKILLS MAP#Cowork skills]] convention. Install via "Save skill". The skill is a conversation/orchestration skill — single `SKILL.md`, no bundled script; it references the installed `scene-intensity` engine rather than carrying its own. If the procedure changes, edit this doc first, then propagate to the skill via `skill-creator` (the canonical-doc-leads rule). Eval note: this is a **subjective, conversational** skill — per `skill-creator`, objective assertion-based evals aren't the natural fit; validate it instead via a live pilot on a real in-progress chapter (see [[_BACKLOG]]).
