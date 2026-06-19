---
type: workflow
name: chapter-pipeline
trigger: run the chapter pipeline
aliases: [run the sequence, draft the sequence, work the sequence, run the pipeline, chapter pipeline]
inputs: [a sequence brief / the next sequence to draft, the project REFERENCE/ canon, the per-chapter folders the sequence spans]
outputs: [a fully landed sequence of chapters (draft.md per chapter), derived REFERENCE canon, a StoryLine mirror, one run report per chapter + one sequence-level report]
lane: fiction
status: approved  # rulings settled 2026-06-18 (register every chapter + package as orchestrator); build + skill-audit + packaging pending (^backlog-chapter-pipeline-build)
last_updated: 2026-06-18
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]) that keep a REFERENCE/ folder. First intended adopter — Witchwood. This is the dictation-route successor to the slate/Transcoder pipeline; it never runs the generative Transcoder.
pipeline_position: The end-to-end orchestrator for the *dictation* route. A two-loop structure — a SEQUENCE outer loop wrapped around a CHAPTER inner loop — that consolidates the steps CRE ran by hand across Witchwood CH5–7 and restores the QA the slate route used to provide, without resurrecting the generative Transcoder. Holds no logic of its own; it sequences existing skills and the two new rewires.
---

# WORKFLOW: Chapter Pipeline (the dictation route, sequence-batched)

> The successor to the slate/Transcoder pipeline for chapters CRE **dictates**. It keeps the prose 100% his words (no generative synthesis step), front-loads the thinking into a workshop, batches dictation into his peak creative hours, and batches the convergent QA/ruling work into off-peak hours — then restores the line-level spec battery the slate route used to feed the register. Born from the [[_OBSERVATIONS#^obs-104]] route analysis of how CH5–7 were actually made vs. how CH1–3 were.

## Why this exists

The last three Witchwood chapters skipped the **slate / Transcoder / verdicts** stages and went workshop → scaffold → runway → dictate → cleanup → workshop-2 → loop-clear → land. That route **gained** the thing that matters most (the Transcoder's "Synthesize" step is the one place AI compressed/rewrote CRE's dictation into prose; dropping it makes the prose entirely his) and **lost** one thing worth recovering: the instrumented line-level register QA (spec-check passes 2–5 → `verdicts.md` → `register-pass` execute-only). `dictation-cleanup` is protective/word-preserving, not a register reviser, and `workshop-2` is content/structure, not a line scan — so without the battery that QA layer was running on CRE's eye alone. This workflow puts it back at the right seam.

## The two loops

```
SEQUENCE LOOP  (the batch unit — one transformation threshold, opening/middle/closing chapters)
  └─ Phase 1  Construct      Workshop-1 (plan + envelopes) → runway-builder        [whole sequence, one sitting]
  └─ Phase 2  Draft          dictate → dictation-cleanup                           [whole sequence, peak hours]
  CHAPTER LOOP  (per chapter, the convergent work — off-peak)
     └─ Phase 3  Develop     blind-read (subagent) → Workshop-2 (reconcile+rule) → blind-response (execute) → loop-clearer → structure-promote
     └─ Phase 4  Line QA     spec-passes 2–5 → reconcile → register-pass (execute-only) → register-promote
  └─ Phase 5  Land           land-chapter (promote already done → canon-sync → storyline-sync)
```

The batch unit is the **Sequence** (per CRE's own framework, `KNOWLEDGE/REFERENCES/Sequences/`): the mid-level structure that carries one act-level transformation threshold, distributed across opening/middle/closing chapters. CH5–7 is exactly one sequence — the mother commits to the journey-that-is-a-mercy-kill (CH5 establishes the bargain, CH6 develops the pact, CH7 implements the departure). See [[KNOWLEDGE/REFERENCES/Methods/Fractal Envelope Model]] for why the loops nest.

## The four consolidations (vs. the old slate route)

1. **Envelope authoring folds into Workshop-1.** Workshop-1 already loads REFERENCE/StoryLine and locks POV at plan stage. It now authors the **sequence envelope** first (POV frame, transformation threshold entry→exit *with sign*, emotional-logical register band, escalation range, entry/exit canon), then **derives each chapter's `envelope.md`** from it. The chapter envelope is the sequence envelope projected onto one chapter's perceptual segment — consistent by construction, not authored three times independently. This **retires `dictation-preflight`** from the route (it reverse-derived the envelope from dictation; the sequence envelope is prescriptive instead). The Transcoder is not run, so nothing consumes the envelope for a generative cut — its consumers are now the dictation discipline + the QA POV checks + canon-sync.

2. **Blind-read becomes a subagent feeding Workshop-2.** `blind-read` runs first in its own clean-room subagent context (sees only the cleaned prose — never brief/workshop/envelope/spec; the isolation is preserved by ordering, the same way `spec-passes` isolates). It returns `pass-1-blind.md`. Then **Workshop-2** — fully spec-aware — ingests those cold findings alongside its own warm read and CRE rules both in one sitting. This folds the old `blind-response` *triage* (its phase 1) into Workshop-2. `blind-response` survives demoted to **executor only**: it writes the already-ruled structural fixes into `draft.md` (`status: dev-revised`), which keeps Workshop read-only (its design invariant).

3. **Every chapter is load-bearing → the battery is standard, not weight-scoped.** CRE rules every chapter load-bearing ("a chapter that is not load-bearing is a missed opportunity"). So the full spec battery (passes 2–5 + reconcile + register execute-only) runs on every chapter; the `chapter-weight` lean/bridge branch is **not used** on this route.

4. **The line battery runs after structure-promote, before the register.** Spec-passes 2–5 are line-level (carries/descriptor/dialogue/theme) and want structurally-final prose, so they run **after** the developmental + loop revisions are promoted in (Phase 3's structure-promote) and **before** `register-pass` + the final promote. The `verdicts.md` sheet exists to drive `register-pass` execute-only; placing the battery after the *final* promote would orphan the verdicts or force a second register/re-promote cycle. Net: **two promotes** — a structure-promote (loops) and a register-promote (final).

## The sequence batch model (how far ahead, and the safety rails)

- **Scaffold exactly one sequence ahead — no more.** Workshop-1 plans the whole sequence (all its chapters) in one sitting; that is the batch. Do not plan the *next* sequence until this one has landed: sequence-type selection depends on "current character psychological state," and crossing this sequence's threshold *changes* that state, so planning ahead plans against a stale starting point. **Feed-forward belongs between sequences (formal canon-sync); held-in-head canon belongs within one (bounded, cheap).**
- **Batch by cognitive mode.** Generative work (Workshop-1 intent, dictation) takes CRE's peak morning hours; convergent work (cleanup, the reads, reconcile, register, land) is lower-energy + AI-assisted and goes to off-peak. The AI front-runs every ungated step on the whole sequence while CRE is away (cleanup, the blind-read subagents, the spec-passes fan-outs produce verdict *drafts*), so the off-peak session is pure ruling — the only irreducibly-human part.
- **Working canon — the in-flight overlay.** The sequence keeps a regenerable, disposable canon overlay so forward chapters are legible *before* anything lands (the fix for the land-only blind spot, `^obs-107`). `canon-sync` runs in **`working` mode**, re-derived at each seam: after **Construct** (from the skeletons — sequence envelope + briefs + runways), after each **dictation-cleanup** (deepening *planned* facts into *drafted* ones), and after each **promote**. **Stored at `<project>/SEQUENCES/SEQUENCE <N> - <NAME>/working-canon.md`** — story-so-far / threads / arcs deltas, each fact tagged `(planned)` or `(drafted CH<N>)`. It is a one-way mirror of the current drafts: never gated, never rolled back, regenerated wholesale, so a draft change can't corrupt it. Workshop-1 / Workshop-2 and runway-builder read `REFERENCE/` **+** this overlay (overlay wins for in-flight chapters). At the sequence boundary, land-mode `canon-sync` promotes each landed chapter's facts into `REFERENCE/` and its overlay entries retire. (Supersedes the earlier "block canon scratch" — same disposable in-flight ledger, now a proper canon layer.)
- **Chapter-one canary.** Run the cold read + dev read on the sequence's **opening** chapter early (it's async/AI-cheap). It establishes the transformation context, so if it's wrong the whole sequence is at risk. Line-level findings defer happily; an arc-level problem in the opening chapter is the one thing not to discover after the middle and close are already dictated.

## Phases (steps)

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md` at the mounted root; confirm `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault. (Each leg runs this too; the orchestrator runs it once up front.)

### Phase 1 — Construct (per sequence, one sitting)
1. **Workshop-1** ([[WORKFLOWS/workshop-chapter]], plan mode) — establish CRE's intent for the sequence; author the **sequence envelope**; scaffold each chapter folder ([[WORKFLOWS/chapter-init]] if it doesn't exist) and **derive each chapter `envelope.md`** from the sequence envelope; write the per-chapter `brief.md`. Output: briefs + envelopes for the whole sequence.
2. **runway-builder** ([[WORKFLOWS/runway-builder]]) — `brief.md` + the chapter envelope → `runway.md` for each chapter, as a **scene-level beat-envelope** scaffold: each beat phrased in its mode's register with a single temperature tag (cold default, heat at the contour's peaks), off the [[KNOWLEDGE/STYLE/REGISTER LEGEND]] spine. This is what CRE dictates from — the per-beat register decision pre-paid so dictation is pure speaking. Then **derive the initial working canon** (`canon-sync` working mode) from the skeletons, so forward chapters have context before a word is dictated.

### Phase 2 — Draft (per sequence, peak hours)
3. **Dictate** from each runway → raw transcript in the chapter's `dictation/`.
4. **dictation-cleanup** ([[WORKFLOWS/dictation-cleanup]]) — word-preserving copy-edit → the chapter's working `draft.md` (`status: drafting`/cleaned). **No generative synthesis — the Transcoder is never run.**

### Phase 3 — Develop (per chapter, off-peak)
5. **blind-read** (subagent, clean room) → `spec-check/<run>/pass-1-blind.md`. Runs the opening chapter first as the canary.
6. **Workshop-2** ([[WORKFLOWS/workshop-chapter]], prose-read mode, read-only) — warm read against the `brief.md` + **ingest the blind-read findings**; reconcile cold + warm; CRE rules the triage. Reconcile the chapter `envelope.md` to the actual segments if they drifted. Captures the ruled decisions in `workshop.md`.
7. **blind-response** ([[WORKFLOWS/blind-response]], execute-only) — apply the ruled structural/reader-experience fixes → `draft.md` (`status: dev-revised`). Pass-1 findings + structure only, never line/voice.
8. **loop-clearer** ([[WORKFLOWS/loop-clearer]]) — work `open-loops.md`; in-voice surgical fixes + `<<DEMO>>` structural blocks CRE rules → a `loop-clear` revision in `revisions/`.
9. **structure-promote** ([[WORKFLOWS/promote-revision]]) — land the loop-clear revision into `draft.md`. Structure is now settled.

### Phase 4 — Line QA (per chapter, off-peak)
10. **spec-passes** ([[WORKFLOWS/spec-check]] passes 2–5 via the `spec-passes` runner) — fan-out on the structurally-settled `draft.md`; write the pass files + a `verdicts.md` draft.
11. **reconcile** ([[WORKFLOWS/spec-check]] grader's gate) — CRE rules the judgment calls → `verdicts.md` `status: ready`.
12. **register-pass** ([[WORKFLOWS/register-pass]], execute-only) — driven by the ready verdicts + the project `REFERENCE/register.md`; revised passage + note into `revisions/`.
13. **register-promote** ([[WORKFLOWS/promote-revision]]) — land the register revision into `draft.md` (`status: register-revised`). **This is the final promote.**

### Phase 5 — Land (per chapter)
14. **land-chapter** ([[WORKFLOWS/land-chapter]]) — the register-promote is already done, so this runs `canon-sync` (**land mode**) → `storyline-sync` to bring REFERENCE current and regenerate the StoryLine mirror. This is where each landed chapter's facts are promoted from the working-canon overlay into the sacrosanct `REFERENCE/` (gated, provenance-tagged) and its overlay entries retire — the in-flight provisional becoming authoritative before the next sequence is planned.

## Run modes — attended vs. unattended

Same discipline as [[WORKFLOWS/land-chapter]]: the rulings (Workshop-2 triage, reconcile judgment calls, canon contradictions) **pause for CRE when attended**; when unattended, the AI runs every ungated step (cleanup, blind-read, spec-passes drafts, additive canon) and **defers every ruling to `open-loops.md` + the report — never guesses.** The promote legs' lineage-mismatch gate always halts. State the mode at the top of each report.

## Stop conditions
- Vault sentinel fails → halt.
- Planning more than one sequence ahead → halt (stale psychological-state input; see the batch model).
- A promote leg's lineage mismatch → halt the chain.
- Any leg's own self-test FAILs → halt at that leg, report the partial state.

## Logging
Per chapter: one consolidated entry to the chapter `changelog.md` + the vault [[_CHANGELOG]] (fiction lane); deferred rulings to `open-loops.md`; fragilities to [[_OBSERVATIONS]]; follow-ups to [[_BACKLOG]] (DIR-003). Per sequence: a short sequence-level report (which chapters landed, what's left to rule).

## Rulings (settled 2026-06-18, CRE)
1. **Register on every chapter — YES.** `register-pass` (Phase 4) runs on every chapter, alongside `dictation-cleanup` (Phase 2). They do different jobs (cleanup makes the dictation readable; the register makes it Witchwood) and every chapter is load-bearing. The CH5–7 gap (register never ran) is closed by this pipeline.
2. **Package as one orchestrator skill — YES.** Build `chapter-pipeline.skill` as an orchestrator (the `land-chapter` pattern) that sequences the existing legs + the two rewires and holds no logic of its own. Build + packaging tracked at `^backlog-chapter-pipeline-build`.

## Notes
- **No new prose logic, by design.** Procedure changes belong in the leg docs; this orchestrator inherits them by only ever *calling* the legs (same relationship `land-chapter` has to its three).
- **The Transcoder is not retired globally** — it stays available for any project that wants generative compression. This route just never calls it.
- **Relationship to the fractal envelope.** The two-loop shape is not arbitrary: the story is fractal (story → sequence → chapter → scene → beat), each level has an envelope, and the workflow nests because the structure does. See [[KNOWLEDGE/REFERENCES/Methods/Fractal Envelope Model]].

## Skill packaging
Pending Open Ruling 2. If built, `chapter-pipeline.skill` is orchestration-only and must not duplicate the leg procedures (skill-audit would flag the drift). Until packaged it triggers only after the bootstrap. Add the trigger row to [[_SKILLS MAP]] once ruled (`^backlog-chapter-pipeline-skillsmap`).
