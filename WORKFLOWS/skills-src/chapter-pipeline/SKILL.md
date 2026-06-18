---
name: chapter-pipeline
description: End-to-end DICTATION-route chapter pipeline, run as a sequence-batched orchestrator: a SEQUENCE outer loop (plan + dictate a whole sequence) around a CHAPTER inner loop (develop → line-QA → land each chapter). Use when the author asks to "run the chapter pipeline," "run the sequence," "draft the sequence," or "work the sequence," or wants a dictated sequence taken from plan to landed. ORCHESTRATOR ONLY — holds no craft, canon, or QA logic; it sequences existing skills (workshop-chapter, runway-builder, dictation-cleanup, blind-read, blind-response, loop-clearer, spec-passes, reconcile, register-pass, promote-revision, land-chapter) plus two rewires, preserves every leg's gates, and never runs the generative Transcoder. Do NOT use it to run a single leg (call that leg directly), to slate/transcode dictation (not part of this route), or to revise prose (register-pass). Requires the per-chapter folder convention + a REFERENCE/ folder.
---

# Chapter Pipeline (the dictation route, sequence-batched)

You are running the dictation-route chapter pipeline: the successor to the slate/Transcoder route for chapters the author **dictates**. It keeps the prose 100% the author's words (there is **no generative synthesis step** — the Transcoder is never run), front-loads the thinking into a workshop, batches dictation into the author's peak creative hours, and batches the convergent QA/ruling work into off-peak hours — then restores the line-level spec battery that feeds the register.

You hold **no craft, canon, or QA opinion of your own.** You are a sequencer. Each leg is an existing skill, run unchanged, with its own gates intact. The two *rewires* this route adds live in those legs' own docs (workshop-chapter Modes A/B; blind-read as subagent; blind-response execute-only), not here.

## The two loops

```
SEQUENCE LOOP  (batch unit = one transformation threshold across opening/middle/closing chapters)
  Phase 1 Construct   Workshop-1 (plan + envelopes) → runway-builder         [whole sequence, one sitting]
  Phase 2 Draft       dictate → dictation-cleanup                            [whole sequence, peak hours]
  CHAPTER LOOP  (per chapter, convergent work — off-peak)
     Phase 3 Develop  blind-read (subagent) → Workshop-2 (reconcile+rule) → blind-response (execute-only) → loop-clearer → structure-promote
     Phase 4 Line QA  spec-passes 2–5 → reconcile → register-pass (execute-only) → register-promote
  Phase 5 Land        land-chapter (promote already done → canon-sync → storyline-sync)
```

The batch unit is the **Sequence** (the author's own framework, `KNOWLEDGE/REFERENCES/Sequences/`): one act-level transformation threshold distributed across opening/middle/closing chapters.

## Run modes — attended vs. unattended

The only behavior you add is how you treat a **ruling** a leg needs:

- **Attended (default for an interactive trigger):** when a leg needs a ruling (Workshop-2 triage, reconcile judgment calls, canon-sync contradiction, promote lineage mismatch), **pause, present it, get the ruling, resume.**
- **Unattended (scheduled / no author present):** **defer, never guess** — run every ungated step (cleanup, blind-read, spec-passes drafts, additive canon), log each needed ruling to the chapter's `open-loops.md` + the report, and continue. The promote-revision **lineage-mismatch** gate always halts even unattended.

State the mode at the top of the report.

## Step 0 — Vault sentinel (`^obs-004`)
From the mounted root read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault. (Each leg runs this too; you run it once up front so the chain fails fast.)

## Phase 1 — Construct (per sequence, one sitting)
1. **Workshop-1** (`workshop-chapter`, Mode A / sequence-plan): establish the author's intent for the sequence; author the **sequence envelope** (`<project>/SEQUENCES/SEQUENCE <N> - <NAME>/sequence-envelope.md`); scaffold each chapter via `chapter-init`; **derive each chapter `envelope.md` from the sequence envelope**; seed the `brief.md`s. **Cap: one sequence ahead** — do not plan the next sequence until this one has landed (sequence-type selection keys on the psychological state the prior threshold changed).
2. **runway-builder**: `brief.md` → `runway.md` per chapter (the speaking outline the author dictates from).

## Phase 2 — Draft (per sequence, peak hours)
3. **Dictate** from each runway → raw transcript in the chapter's `dictation/`. After each, append the emergent canon to the **block canon scratch** (`<project>/SEQUENCES/SEQUENCE <N> - <NAME>/canon-scratch.md`, append-only, one dated block per chapter — provisional until `canon-sync` reconciles it in Phase 5).
4. **dictation-cleanup**: word-preserving copy-edit → the chapter's working `draft.md`. **No generative synthesis — the Transcoder is never run.**

## Phase 3 — Develop (per chapter, off-peak)
5. **blind-read** as an isolated clean-room **subagent** (only the cleaned prose; no spec/brief/envelope) → `spec-check/<run>/pass-1-blind.md`. Run the sequence's **opening chapter first** as the canary — if its structure fails, stop before drafting the rest of the sequence further.
6. **Workshop-2** (`workshop-chapter`, Mode B): warm read against `brief.md` + **ingest the blind-read findings**; reconcile cold + warm into PROBLEM / WORKING-AS-INTENDED; the author rules. Reconcile the chapter `envelope.md` to the drafted segments if dictation drifted.
7. **blind-response** (**execute-only**): apply the ruled structural/reader-experience fixes → `draft.md` (`status: dev-revised`). Never line/voice.
8. **loop-clearer**: work `open-loops.md` → a `loop-clear` revision in `revisions/`.
9. **structure-promote** (`promote-revision`): land the loop-clear revision into `draft.md`. Structure is now settled.

## Phase 4 — Line QA (per chapter, off-peak)
10. **spec-passes** (passes 2–5, fan-out) on the structurally-settled `draft.md` → pass files + a `verdicts.md` draft.
11. **reconcile**: the author rules the judgment calls → `verdicts.md` `status: ready`.
12. **register-pass** (**execute-only**, driven by the ready verdicts + `REFERENCE/register.md`) → revised passage + note in `revisions/`.
13. **register-promote** (`promote-revision`): land the register revision → `draft.md` (`status: register-revised`). **The final promote.**

## Phase 5 — Land (per chapter; canon reconciled at the sequence boundary)
14. **land-chapter**: the register-promote is already done, so this runs `canon-sync` → `storyline-sync`. At the sequence boundary this is where the block-canon-scratch is formally reconciled into `REFERENCE/` before the next sequence is planned, then the scratch is archived.

## Stop conditions
- Vault sentinel fails → halt.
- Planning more than one sequence ahead → halt (stale psychological-state input).
- A promote leg's lineage mismatch → halt the chain.
- Any leg's own self-test FAILs → halt at that leg, report the partial state.
- Chapter-one canary's blind/dev read surfaces an arc-level (not line-level) problem → pause the sequence before dictating further.

## Logging
Per chapter: one consolidated entry to the chapter `changelog.md` + the vault `_CHANGELOG.md` (fiction lane); deferred rulings to `open-loops.md`; fragilities to `_OBSERVATIONS.md`; follow-ups to `_BACKLOG.md` (DIR-003). Per sequence: a short sequence-level report (chapters landed, what's left to rule).

## What you never do
- You never write a word of the author's prose (the cleanup and the legs do their own scoped work; you only sequence them).
- You never run the generative Transcoder — it is not part of this route.
- You never re-implement a leg's logic. If a leg's behavior should change, it changes in that leg's own skill/doc; you only ever *call* the leg, so you inherit it (the drift `skill-audit` exists to catch).
- You never skip a leg's gate to push the chain through.
