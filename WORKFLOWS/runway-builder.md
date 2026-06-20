---
type: workflow
name: runway-builder
trigger: build the runway
aliases: [build the runway for chapter N, make the runway, derive the runway, prep the runway, runway from the brief, build the dictation runway, runway this chapter]
inputs: [a chapter folder using the per-chapter convention with a filled brief.md]
outputs: [a runway.md written into the chapter folder — a scene-segmented forensic logic-beat speaking outline (each beat a plain forensic action line + GOAL→BUT→THEREFORE; see "Forensic logic-beat runway"), wrapped in the flow-entry conditions block and a receipts close]
lane: fiction
status: draft
last_updated: 2026-06-19
consumes: [the chapter's brief.md (Beats to hit + Seal schedule + goal + weight), envelope.md (segment names + POV + roster, when present), REFERENCE/threads.md (thread labels the brief references)]
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). First adopter — Witchwood.
pipeline_position: Construction (confirmed brief.md) → THIS → Phase 3 forensic-draft dictation; parallel-upstream sibling of [[WORKFLOWS/dictation-preflight]]
sources: KNOWLEDGE/RESEARCH 2026-06-15 — [[KNOWLEDGE/RESEARCH/2026-06-15 dictation-practice-fiction]] · [[KNOWLEDGE/RESEARCH/2026-06-15 flow-state-writing-dictation]] · [[KNOWLEDGE/RESEARCH/2026-06-15 outlines-adhd-dictation-flow]]
---

# WORKFLOW: Runway Builder (brief → dictation speaking outline)

> Derivation pass that reads a chapter's `brief.md` and writes a `runway.md` into the chapter folder — the thin **speaking outline** CRE actually dictates from. It re-cuts the brief's beats into glance-able keyword **prompts** (never sentences), adds the `→` forward-pointers that keep working memory externalized, seals what the brief's seal schedule says to seal, and wraps the whole thing in the four flow-entry conditions + a receipts close. The codified form of the three 2026-06-15 dictation research briefings and the briefing-runway template. Sits at the **Construction → forensic-draft seam**: after the brief is confirmed, before CRE records dictation.

## When to use

When a chapter using the per-chapter folder convention has a `brief.md` with **Beats to hit**, and CRE wants the dictation runway for it. Trigger phrases: "build the runway," "build the runway for chapter N," "make the runway," "derive the runway," "runway from the brief." Do NOT use it to fill the envelope (that is [[WORKFLOWS/dictation-preflight]]) or to slate dictation (that is [[WORKFLOWS/transcoder]]). The runway is what CRE dictates **from**; the envelope is what the Transcoder cuts **against** — different artifacts, different passes.

## Inputs

- **The chapter folder** (per-chapter convention).
- **`<chapter>/brief.md`** — the source of truth for this pass. Read **Beats to hit**, **Seal schedule**, **Register / tempo notes**, and the `weight` field.
- **`<chapter>/envelope.md`** (optional) — for segment short-names, when already authored.
- **`REFERENCE/threads.md`** (optional) — to resolve any `T##` thread label the brief cites.

## Outputs

- **`<chapter>/runway.md`** — the speaking outline: a Conditions block (blank, for CRE to fill per session), one Scene block per scene (forensic logic-beats in the GOAL→BUT→THEREFORE form — see "Forensic logic-beat runway"; a `[SEALED]` line when the seal schedule applies), the during-pass guardrails, and a receipts Close. Scaffold lines are **bare action lifted from the brief's structure**, never invented prose or pre-chosen imagery.
- A short **derivation note** in the reply: which beats mapped to which prompts, anything tagged `<<UNCERTAIN>>`, and any divergence from the brief worth CRE's eye.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Load and classify the brief
Read `<chapter>/brief.md`. If it has no **Beats to hit** (status `unfilled`, an empty scaffold), halt — there is nothing to derive from; tell CRE to fill the brief first (workshop / pipeline S2). If `status` is `drafted` (not yet `confirmed`), proceed but note the runway inherits unconfirmed intent. Read `weight` — it scopes depth (see Step 5).

### Step 2 — Group beats into scenes, derive prompts
Group the brief's beats into scenes (single-location runs of beats; cross-reference `envelope.md` segment names when present). For each scene, turn **each beat into one prompt**: strip it to a few trigger keywords in delivery order, cap **3–5 prompts per scene**. Add a `→` forward-pointer (the next beat in 1–3 words) after each prompt; the last prompt's pointer is the cut. **Never write a full sentence** — if a derived prompt reads as prose, cut it back to keywords. This pass lifts the brief's own language; it does not generate fiction (cross-cutting rule + DIR). **Dictation-route form:** the per-scene output is the **forensic logic-beat runway** (a plain forensic action line + GOAL→BUT→THEREFORE per beat), which supersedes the keyword-prompt form described here — see "Forensic logic-beat runway" below.

### Step 3 — Seal + the one write-in-full
From the brief's **Seal schedule "must NOT yet learn"**, write a `[SEALED]` line per affected scene: name what to enact-and-withhold, never narrate. If the brief already specifies a line of dialogue / a concrete image CRE "already hears," lift exactly one into the `★` write-in-full slot; otherwise leave the slot empty for CRE. One `★` per scene, max.

### Step 4 — Scaffold the conditions + close (blank)
Write the Conditions block (medicated-window gate, single-next-goal line, pre-committed stop, inputs-killed checklist, capture path) and the receipts Close **blank** — these are CRE's per-session fills, not derivations. Pre-fill only what the brief makes unambiguous (e.g. "Cut on:" from the brief's curtain instruction).

### Step 5 — Write `runway.md` (never-overwrite; weight-scaled)
Write `<chapter>/runway.md`. **Never overwrite** an existing `runway.md` — if one exists, stop and ask whether to replace or version it. Scale depth by `weight`: `load-bearing` → full runway, every scene; `bridge` → lean (fewer prompts, may collapse to one scene block); `standard` → default. Tag anything you couldn't resolve `<<UNCERTAIN: best guess — reason; confirm?>>` and surface it in the reply rather than guessing silently.

## Forensic logic-beat runway — the GOAL→BUT→THEREFORE spine (2026-06-19)

> **Supersedes the 2026-06-18 "beat-envelope / temperature-tag" form.** Tested 2026-06-19 on the throwaway scene "The Strand": the keyword + temperature-tag beats read as **riddles** — CRE had to *decode* each beat before he could speak it, because they pre-loaded compressed sensation (his creative material) instead of structure. The forensic logic-beat form dictated clean. (`^obs-108`.)

On the dictation route the runway carries the **causal skeleton** of the scene — goal, obstacle, consequence — and *nothing else*. It does **not** pre-load sensation, imagery, or register colour: that is the dictation's job, and pre-baking it (a) puts CRE's creative material in his mouth and (b) compresses into riddles he must decode before he can speak. The scaffold hands him **structure**; he supplies all the **skin** live. It remains the beat rung of the [[KNOWLEDGE/REFERENCES/Methods/Fractal Envelope Model]], materialized transiently — but the [[KNOWLEDGE/STYLE/REGISTER LEGEND]] is the spine for `register-pass` *downstream*, not for the runway surface.

### Scaffold register — forensic, emotion implied through action
Write every scaffold line in the **forensic register**: simple, to-the-point action, like an incident report — *she does X, but Y, therefore Z*. The emotional undercurrent is carried by the action itself, **never labelled**. No flourish, no chosen imagery, no adjectival colour — those are the lines CRE will speak, and pre-deciding them is the failure the test exposed. If a scaffold line reaches for a sensory image or a feeling-word, cut it back to the bare action.

### Granularity — scene-level beats, count from the scene's goal (no cap)
Segment the chapter into **scenes** (from `envelope.md` segments / the brief's locations) and decompose each into its **beats** — one line per beat, and **the beat count comes from the scene's goal, not a fixed number.** (The old "3–5 prompts" was a chapter-level vestige; at scene scope it crushes a struggle into montage.) Read the scene's **goal** (character goal + story goal, from the chapter envelope) and build the beats that satisfy it:
- **Connect beats with *but* / *therefore*, never *and then*** ([[KNOWLEDGE/REFERENCES/Methods/But and Therefore/But and Therefore Method|the But-and-Therefore method]]). A struggle or peak scene **ratchets** through as many try-fail beats as the tension needs; each beat should *cost* something. An "and then" between two beats is the failure state — make it a complication (*but*) or a consequence (*therefore*), or fold them.
- **Large beats break into sub-beats** that choreograph the moment (the fall: dropped → snow in his cloak → digs him out → his warmth fainter).
- **"Tight, no gaps" means *adjacency*, not brevity.** A harrowing scene should feel harrowing — more beats, not fewer. A cold connective scene stays sparse; a peak scene earns its length.

### Each beat = forensic action + GOAL→BUT→THEREFORE
- Open the scene with the **GOAL** — the *reason the POV character is there* at the start (character goal / story goal). It orients the whole scene.
- Each beat is one **plain forensic action line** — `LEAD IN:` for the first beat, `TRANSITION:` for each beat after (the entry sentence into the beat) — followed by `→ BUT <resistance>` and `→ THEREFORE <consequence that carries forward>`. **BUT/THEREFORE is regular on every beat:** the *but* is the resistance, the *therefore* is the cost it exacts and the hinge into the next beat. An "and then" between beats is the failure state — make it a *but* or a *therefore*, or fold the beats.
- **Re-state the GOAL only when it shifts.** The opening goal carries until the scene turns it; surface the drift, never repeat an unchanged goal. (On the test scene the goal drifted *find him → looking is all one can do → the wish* — that drift is the scene's arc.)
- Keep each line a **trigger, not finished prose** — bare action CRE speaks *from*, not a sentence he keeps. If a beat reads as completed prose, cut it back.

### Plants — protect brief-mandated setups
With sensation improvised live, a setup the **brief requires** (an object that pays off later, a reveal, a seal) can get improvised away. Add a `PLANT: <thing>` note on **only** the beats carrying a brief-mandated setup / payoff / seal — kept separate from the logic line. The spine stays clean; continuity stays safe.

### No contour tags, no temperature on the surface
Drop the `[cold]/[warm]/[HOT]` tags and the contour header from the page — tested 2026-06-19 as clutter CRE reads past. The escalation still has to **exist** in how the beats ratchet (the cost rising beat to beat), but it does that work in the *shaping*, not as a label on the page. (Supersedes the 2026-06-18 temperature-on-surface design.)

### Scene vs. sequel — pick the template by contour position
Per [[KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework]], every scene is one of two shapes, **selected from its place on the contour**:
- **Scene (proactive)** — `goal → conflict → disaster`. A peak; beats ratchet to a worse-than-it-started turn.
- **Sequel (reactive)** — `reaction → dilemma → decision`. The modulation beat *after* a peak — absorb, process, a new goal crystallizes; its closing **decision** closes an escape and fires the next scene (the staircase).

Right after a high point, run a **sequel** (the reader's numb; the floor needs resetting). Don't stack peaks (plateau fatigue) or sequels (slack) — the contour says which comes next. **Want vs. resistance is the but/therefore engine:** the *but* is the resistance, the *therefore* the cost it exacts; a sagging beat means soft resistance — strengthen the obstacle or deepen the want.

### Let dictation run warm — restraint is `register-pass`'s job
The forensic *scaffold* does not force forensic *output*. On the test the lean skeleton produced **warmer, more interior** prose than the scaffold (explicit interiority, remembered detail) — that is the division of labour working, not a leak. Do **not** tune the runway to suppress it: the runway's job is flow; the final register is decided downstream in `register-pass`. The runway is a roadmap, not a cage — CRE overrides any beat live.

### Every present character is an agent — no decor
Build from the scene's **roster** (the chapter envelope lists who's present + each one's carried state, read from `arcs.md` / prior `continuity.md` / the **working-canon overlay**). **Every present character with a live arc gets their own *but/therefore* thread** — their struggle, successes, failures — interleaved with the POV character's. A present character given no thread is **decor**, the character-level UNDRAMATIZED failure — flag it. (The hound on the storm-trek is not set dressing: he entered overriding his fear with the doll in his maw, so he drops it, she says "leave it," he retrieves it — she delivers the boy, he delivers the doll.)

### Form
```
SCENE — <name>   POV: <who>   present: <roster + carried state>
GOAL: <reason the POV character is here — character goal / story goal>
──────────────────────────────────────────────
LEAD IN: <plain forensic action — beat 1>
   → BUT <resistance>
   → THEREFORE <consequence that carries forward>
TRANSITION: <plain forensic action — next beat>
   → BUT <resistance>
   → THEREFORE <consequence>
   PLANT: <only if the brief mandates a setup/payoff/seal here>
TRANSITION: <another present character's thread — same GOAL/BUT/THEREFORE shape>
   → BUT <resistance>   → THEREFORE <what it costs / the parallel>
GOAL: <restate only when the goal shifts>
TRANSITION: <plain forensic action>
   → BUT <resistance>   → THEREFORE <consequence>
END: <the closing action>
[SEALED] <what to enact-and-withhold, per the seal schedule>
```

This supersedes Step 2's keyword output **and** the 2026-06-18 beat-envelope/temperature form on the dictation route; the Conditions block + receipts Close (Step 4) and never-overwrite + weight-scaling (Step 5) are unchanged. The Register Legend remains the spine for `register-pass` downstream, not for the runway surface.

## Files this workflow does NOT touch
`draft.md`, `envelope.md`, `dictation/`, `slate/`, `revisions/`, `open-loops.md`, `continuity.md`, `notes.md`, `_status.md`, and `brief.md` itself (read-only). It writes one file — `runway.md` — and produces no prose.

## Logging
DIR-003 applies. Append a session line to `<chapter>/changelog.md` and the vault `_CHANGELOG.md` (newest-first, file-tool top-insert per DIR-005). File notable fragilities to `_OBSERVATIONS.md`.

## Pipeline relationship
**brief.md (confirmed) → runway-builder (this) → CRE dictates from runway.md → dictation-preflight → transcoder.** The runway is the dictation *input habit* scaffold; the envelope is the Transcoder's cut-test. They are independent prep passes off the same chapter — neither consumes the other.
