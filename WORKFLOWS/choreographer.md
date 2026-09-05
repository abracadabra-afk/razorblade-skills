---
type: workflow
name: choreographer
trigger: choreograph the scene
aliases: [run the choreographer, choreograph this, choreograph the event, block the scene, choreo session]
inputs: [the choreo flag/outcome note (from dictation or stated live), the chapter's brief.md + envelope.md + continuity.md, REFERENCE canon (threads.md, arcs.md, bible.md), the project register's taste surface]
outputs: [a ratified event arc (beat map) written to the chapter folder, an updated open-loops entry closed or converted, a dictation-ready gap for CRE to fill at the mic]
lane: fiction
status: spec — packs after 2–3 live runs
governed-by: DIR-017 (protected forward-flow), DIR-014 (cue binding), DIR-016 (runner wiring)
last_updated: 2026-09-04
---

# WORKFLOW: choreographer

## When to use

CRE says **"choreograph the scene"** / **"run the choreographer"** — a dictated chapter carries one or more **choreo flags** (events he moved over at the mic, noting only the outcome), and he now wants the dramaturgical structure of that event designed with him before he dictates the gap. Covers fight scenes, action set-pieces, horror/murder scenes, intimate/romance scenes, and tense conversations — **one instrument, one rubric, per-event-type move vocabularies.**

Sits between the slate landing and the gap-fill dictation. It is the desk-side half of a two-layer mechanism whose mic-side half (the spoken cue, below) exists so choreography never stalls dictation (DIR-017).

## Taste anchor — CRE verbatim (2026-07-29, ratified)

> "This would allow me, while I'm dictating, to move over events that require choreography such as fight scenes, action — that way as I dictate I can make note with the outcome of the action, with a note to follow up with the choreographer to really make the action shine. […] Normally I could choreograph fight scenes, action scenes, horror scenes, murder scenes, even sex scenes. Similar to choreographer, I'm also thinking of dialogue skill as a way to choreograph conversations — the attacking and defending that makes compelling dialogue so pertinent."

> "What I mean by 'Make the Action Shine' is not to write the action for me, but to work with me to build the storytelling scaffolding of one of these events […] There is a back and forth: escalations, fallbacks, defense mechanisms, submission, etc. All of these create **a narrative through action that should be thematically resonant when shown, not told.** This skill would help me create the arc of the event, and I, of course, would supply the words and ratify the decisions. I am not looking for the words. I am looking for the compelling structure that should take into consideration: stakes, where they are in the story; character flaws that hold them back; what level of intimacy should be explored […]; it is very close, and every movement and breath is captured as part of the escalations and tensions. If there is a larger action scene at play, the camera might pull out a little bit […] This is a pacing and positioning question, a storytelling question, and a structural design skill. The words themselves are not in its lane, but […] the choreography, the moves on the field, so to speak, are in its wheelhouse."

**The boundary: dramaturgy in, diction out.** Escalation dynamics, stakes-positioning, flaw-driven limits, camera distance, thematic resonance through action — all in-lane (structure/analysis). The prose is CRE's, always. Precedent: runway-builder's *structure only, never prose* and the DIALOGUE BANK's *conversations, never lines*.

## Position & guards

- **Placement (route v3, CRE-ruled 2026-08-09 — EP 01 post-mortem):** the choreographer is execution-tier machinery and obeys the affirmed-sections gate — **it never runs on a section carrying an open CONTENT flag.** Default home: post-author-pass, nested in [[WORKFLOWS/panel-response]] as ruled 07-29. Pre-author-pass it is available only as a **CRE-triggered call from the [[WORKFLOWS/dev-edit]] walk**, on an event whose content he has ruled (affirmed, or a rework where *what happens* is settled and staging is the open question); the dev-editor may offer, never auto-run. Evidence pair: EP 01's climax-inversion map (content-affirmed) survived to record-ready; its video-2-escalation map (content-contested) died whole with the sorority sequence. A ratified map is a dated authored artifact (DIR-010 corollary) — every pre-author-pass map is a bet the pass won't move the content under it.
- **Project-fluent, not context-free** — the workshop-chapter loadout, not loop-clearer's. To weigh *stakes where they are in the story* and *the flaws that hold characters back*, it must read the chapter brief, continuity, threads/arcs, and REFERENCE canon before proposing anything.
- **Conversational and two-phase gated.** It brings an informed read; CRE pushes back; the arc is ratified beat by beat before anything is written. Nothing lands unratified.
- **Never writes CRE's prose.** No lines, no rendered action, no sample sentences beyond naming a move ("she feints toward the door"). If a beat needs demonstration language, that is a loop-clearer-class structural moment — one demonstration block maximum, original kept, never committed for him.
- **Never grades the finished draft against the choreo map.** Divergence at the mic is a win (DIR-017 clause 2). The map is a flow-kickstarter for the gap-fill dictation, not a spec.
- **Camera distance respects the perceptual envelope.** The close mode (every movement and breath) and the pulled-out wide view are proposed per beat, and any pull-out that strains close third gets flagged against `envelope.md` — the pipeline's existing enforcement surface for exactly this. The choreographer plugs into that machinery; it does not duplicate it.
- **Unattended posture:** this is an attended, CRE-in-the-loop instrument. An unattended run may at most *inventory* choreo flags into a report (DIR-012); the session itself never runs headless.

## Layer 1 — the spoken cue (mic-side; the DIR-017 mechanism)

At the mic, CRE moves over the event with only its **outcome** and a flag:

> "…choreo note: they fight, he loses the ear, she gets to the stairwell — pick it up there."

Convention (binds per DIR-014 once wired):

- **Cue phrase:** "choreo note" (variants: "choreography note," "flag for the choreographer").
- **Payload:** outcome + any hard constraints CRE already knows (who's standing at the end, injuries that are canon, where bodies end up). Nothing else required — the whole point is not to stall.
- **Landing:** the transcoder preserves the cue verbatim and hands it back as an `open-loops.md` entry typed **`choreo`**, with the surrounding text anchored so the desk session can find the gap.

**Wiring caveat (DIR-016):** teaching the transcoder / dictation-runner this cue is a staged-runner change — deterministic code, canon doc, live task `SKILL.md` prompt, and the poll/early-exit gate must all be edited and re-read in the same session. Until wired, the cue still works socially: any pass that reads the transcript treats "choreo note" as a flag by convention. Tracked in `_BACKLOG`.

## Layer 2 — the desk session

### Step 0 — Sentinel + locate

Verify `_DIRECTIVES.md` frontmatter (`^obs-004`). Identify the target: a `choreo`-typed open loop, a flagged stretch CRE names, or an event he brings live. Confirm the event and its outcome note in one line so he can redirect in one word.

### Step 1 — Load the context (read-only)

Chapter `brief.md` (job, seals, payoffs due), `envelope.md` (POV + conditions for the stretch), `continuity.md`, REFERENCE `threads.md` / `arcs.md` / `bible.md` entries for the participants, and the register's taste surface. Do not preload beyond the participants and the stretch (DIR-002 discipline at chapter scale).

**Supersession triage — as you load, before Step 2 frames the event (DIR-019, added 2026-09-04).** What this session loads that names a span: the `choreo`-typed `open-loops.md` entry and the surrounding text the transcoder anchored it to; an existing ratified map at `choreo/<event-slug>.md` whose beats quote or anchor draft text; and, on the [[WORKFLOWS/panel-response]] nesting, the panel finding and CRE's ruling that binned this event CHOREO, both of which quote banked prose. The working text is the chapter's current `draft.md` — the banked stretch, on the second exit door. **Span present → carry silently** into Step 2. **Span gone → moot:** retire the flag or ruling with a `superseded_by: draft.md (<date>)` stamp in place, one changelog line — **never asked**, and never designed around. **Span reworded but surviving → the only case that surfaces**, as one batched line at the head of the Step 2 dials, tree-researched first (DIR-011). A ratified map whose stamp predates the current `draft.md` is a §1 derived artifact: **regenerate it or retire it in place with the stamp, never put it to him as a map to re-ratify** — and never re-open an event his own later draft already restaged (§3 — a hand-landing is the newest ruling).

**What this does not touch.** The triage runs on maps and flags *entering* a session as inputs, never on a map after its gap has been dictated. A delivered map is spent, not stale: divergence between the finished prose and the map that kickstarted it stays a win, never a supersession finding, and the guard against grading the draft against the map (DIR-017 clause 2) is unchanged. **Scope lock (§4):** staleness noticed outside this event, its chapter folder, and its direct derives is one line in `SYSTEM/drift-ledger.md`, not a beat and not a mid-session aside.

### Step 2 — Frame the event (propose, one screen)

Before any beats, propose the four dials and get them ratified:

1. **Stakes-position** — what this event risks and where the story is when it happens; which seals/payoffs it touches.
2. **Flaws in play** — the character limits that shape what each participant *can't* do, drawn from canon, cited.
3. **Intimacy level** — how close the event runs (a fight and a love scene sit on the same dial), and what that closeness is *for* thematically.
4. **Camera default** — close (every breath) vs. pulled wide, with the envelope constraint stated.

### Step 3 — Propose the arc

The beat map: escalation → fallback → counter → submission/turn → outcome, shaped to a tension curve at event scale (the runway-builder curve zoomed in). Per beat:

- **The move** — what happens, in what order, where the bodies are (geography, reach, sightlines, cause-and-effect chain, injury continuity).
- **The tactic** (dialogue vocabulary) — objective, attack/defend posture, power shift.
- **Camera + envelope** — proposed distance, flagged if it strains the POV.
- **Resonance note** — one line on what the beat *shows* thematically; never how to phrase it.

Move vocabularies by event type — **fight/action** (physics, positioning, injury logic), **intimate** (approach, consent/withdrawal dynamics, closeness escalation), **horror/murder** (dread staging, reveal order, the withheld thing), **dialogue** (attack/defend, feint, concession, silence as a move). Same skeleton, different vocabulary file.

### Step 4 — Ratify (gate)

Walk the map with CRE beat by beat. He rules: keep / amend / cut / replace. **The skill never invents a beat he vetoed a sibling of, and never argues past one push-back** (his instincts override analysis). Amendments are his; the skill records them.

### Step 5 — Write the map

Ratified map → `choreo/<event-slug>.md` inside the chapter folder (a small opt-in extension of the per-chapter convention, sibling to `dictation/` and `slate/`; default chosen, CRE can re-route). Frontmatter serialized per DIR-004. The source `open-loops.md` entry is marked resolved-to-choreo with a link. Chapter `changelog.md` gets one line.

### Step 6 — Exit to the mic

The session ends by pointing at the gap: the map is a **speaking outline for a gap-fill dictation** — new material into a stretch that was never written, which is forward flow, not the re-dictation DIR-017 bans. The map's beats stay plain and chronological (no craft rules as preconditions — DIR-017 clause 2); register/craft constraints stay in the edit-stage docs downstream.

**Second exit door (post-panel use, added 2026-07-29):** when the event is **banked prose** flagged by a panel/blind read rather than a dictation gap — the [[WORKFLOWS/panel-response]] nesting — the ratified map exits to that pass's **Phase 2 revision as its spec**, never to the mic. Re-dictating banked material is DIR-017 clause 1's named mistake. Same instrument, different exit door.

## Stop conditions

- The event's outcome contradicts canon (continuity/threads) → surface the contradiction for ruling before any beats are proposed; do not design around an unruled contradiction.
- CRE starts dictating prose mid-session → capture it verbatim as his (never absorb it into the map as the skill's proposal) and offer to route it through the normal dictation intake.
- The map wants craft/register rules as beat preconditions → they move to the edit-stage doc, not the map (DIR-017).

## What this skill never does

- **Write the words.** No prose, no lines of dialogue, no rendered action. Dramaturgy in, diction out.
- **Author story content uninvited.** It proposes structure for an event CRE defined the outcome of; it never invents the event, the outcome, or a new plot turn (organic-process guard).
- **Grade the finished dictation against the map** — divergence is a win; only CRE notices the feeling drift, at the mic.
- **Gate dictation.** The mic-side cue is the entire mic-side footprint. No precondition ever attaches to the act of dictating.
- **Run headless.** Attended only; unattended runs inventory flags to a report at most.

## Non-goals

- Not `runway-builder` (chapter-scale outline; this is event-scale, invoked per flag)
- Not `loop-clearer` (general open-loops resolution; `choreo`-typed loops route here instead)
- Not `workshop-chapter` (whole-chapter developmental read) or `scene-intensity` (scoring; may be borrowed as a lens on a proposed arc, later)
- Not a fight-realism fact-checker — research questions route to `notes.md` / research-briefing

## Logging

Per DIR-003: a session that writes a choreo map logs one `_CHANGELOG` line and a chapter `changelog.md` line. Flag-inventory-only runs are trivial — don't log.

<!-- v1 spec authored 2026-07-29 from CRE's ratified scope (this doc's Taste anchor, verbatim from the 2026-07-29 session). Design rulings: one skill, one rubric, per-event-type move vocabularies (CRE's two-skill instinct merged after his "same instrument" clarification); dramaturgy-in/diction-out boundary; camera-as-envelope-dial; two-layer split so DIR-017 forward flow is never stalled. Packs after 2-3 live runs per house convention. Not yet mirrored to skills-src/ or packed. Cue wiring into transcoder/dictation-runner is DIR-016-gated and tracked in _BACKLOG. -->
