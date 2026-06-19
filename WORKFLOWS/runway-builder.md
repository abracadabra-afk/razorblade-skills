---
type: workflow
name: runway-builder
trigger: build the runway
aliases: [build the runway for chapter N, make the runway, derive the runway, prep the runway, runway from the brief, build the dictation runway, runway this chapter]
inputs: [a chapter folder using the per-chapter convention with a filled brief.md]
outputs: [a runway.md written into the chapter folder — a scene-segmented beat-envelope speaking outline (each beat phrased in its mode's register with a single temperature tag; see "Beat-envelope runway"), wrapped in the flow-entry conditions block and a receipts close]
lane: fiction
status: draft
last_updated: 2026-06-18
consumes: [the chapter's brief.md (Beats to hit + Seal schedule + Register/tempo + weight), envelope.md (segment names + POV + the planned contour, when present), REFERENCE/threads.md (thread labels the brief references), KNOWLEDGE/STYLE/REGISTER LEGEND (the temperature/mode spine — the beat-envelope source)]
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

- **`<chapter>/runway.md`** — the speaking outline: a Conditions block (blank, for CRE to fill per session), one Scene block per scene (3–5 keyword prompts with `→` forward-pointers, one `★` write-in-full slot, a `[SEALED]` line when the seal schedule applies), the four during-pass guardrails, and a receipts Close. Prompts are **keyword triggers lifted from the brief**, never invented prose.
- A short **derivation note** in the reply: which beats mapped to which prompts, anything tagged `<<UNCERTAIN>>`, and any divergence from the brief worth CRE's eye.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Load and classify the brief
Read `<chapter>/brief.md`. If it has no **Beats to hit** (status `unfilled`, an empty scaffold), halt — there is nothing to derive from; tell CRE to fill the brief first (workshop / pipeline S2). If `status` is `drafted` (not yet `confirmed`), proceed but note the runway inherits unconfirmed intent. Read `weight` — it scopes depth (see Step 5).

### Step 2 — Group beats into scenes, derive prompts
Group the brief's beats into scenes (single-location runs of beats; cross-reference `envelope.md` segment names when present). For each scene, turn **each beat into one prompt**: strip it to a few trigger keywords in delivery order, cap **3–5 prompts per scene**. Add a `→` forward-pointer (the next beat in 1–3 words) after each prompt; the last prompt's pointer is the cut. **Never write a full sentence** — if a derived prompt reads as prose, cut it back to keywords. This pass lifts the brief's own language; it does not generate fiction (cross-cutting rule + DIR). **Dictation-route form:** the per-scene output is the **beat-envelope runway** (in-mode beat phrasing + one temperature tag per beat), which supersedes the 3–5-keyword-prompt form described here — see "Beat-envelope runway" below.

### Step 3 — Seal + the one write-in-full
From the brief's **Seal schedule "must NOT yet learn"**, write a `[SEALED]` line per affected scene: name what to enact-and-withhold, never narrate. If the brief already specifies a line of dialogue / a concrete image CRE "already hears," lift exactly one into the `★` write-in-full slot; otherwise leave the slot empty for CRE. One `★` per scene, max.

### Step 4 — Scaffold the conditions + close (blank)
Write the Conditions block (medicated-window gate, single-next-goal line, pre-committed stop, inputs-killed checklist, capture path) and the receipts Close **blank** — these are CRE's per-session fills, not derivations. Pre-fill only what the brief makes unambiguous (e.g. "Cut on:" from the brief's curtain instruction).

### Step 5 — Write `runway.md` (never-overwrite; weight-scaled)
Write `<chapter>/runway.md`. **Never overwrite** an existing `runway.md` — if one exists, stop and ask whether to replace or version it. Scale depth by `weight`: `load-bearing` → full runway, every scene; `bridge` → lean (fewer prompts, may collapse to one scene block); `standard` → default. Tag anything you couldn't resolve `<<UNCERTAIN: best guess — reason; confirm?>>` and surface it in the reply rather than guessing silently.

## Beat-envelope runway — the register-legend spine (2026-06-18)

On the dictation route, the runway's job is to **pre-pay the per-beat register decision** so dictation is pure speaking — it kills the 10–30s "how do I present this?" pause by making the only convergent micro-decision (temperature) ahead of time, in planning. It is the **beat rung of the [[KNOWLEDGE/REFERENCES/Methods/Fractal Envelope Model]], materialized transiently**, with the [[KNOWLEDGE/STYLE/REGISTER LEGEND]] as its spine.

### Granularity — scene-level beats, count from the scene's goal (no cap)
Segment the chapter into **scenes** (from `envelope.md` segments / the brief's locations) and decompose each into its **beats** — one line per beat, and **the beat count comes from the scene's goal, not a fixed number.** (The old "3–5 prompts" was a chapter-level vestige; at scene scope it crushes a struggle into montage.) Read the scene's **goal** (character goal + story goal, from the chapter envelope) and build the beats that satisfy it:
- **Connect beats with *but* / *therefore*, never *and then*** ([[KNOWLEDGE/REFERENCES/Methods/But and Therefore/But and Therefore Method|the But-and-Therefore method]]). A struggle or peak scene **ratchets** through as many try-fail beats as the tension needs; each beat should *cost* something. An "and then" between two beats is the failure state — make it a complication (*but*) or a consequence (*therefore*), or fold them.
- **Large beats break into sub-beats** that choreograph the moment (the fall: dropped → snow in his cloak → digs him out → his warmth fainter).
- **"Tight, no gaps" means *adjacency*, not brevity.** A harrowing scene should feel harrowing — more beats, not fewer. A cold connective scene stays sparse; a peak scene earns its length.

### Each beat = in-mode phrasing + one temperature tag
- **Phrase the beat in its mode's register**, so the *form* carries the mode and no mode label is needed (Register Legend, Beat structure):
  - *watching* → sensory fragments — "the lake far off — birds, wildflowers, the crowd by the water"
  - *doing* → a flowing action phrase — "crossing toward the shore, past the strangers"
  - *thinking* → a reveal/contrast cue, never a restatement — "her choice — let him drown"
  Keep it a **trigger, not the finished sentence** — keywords in the mode's shape; CRE speaks the actual line. If a beat reads as completed prose, cut it back (the no-prose rule still holds).
- **Tag only the temperature** — `[cold]` / `[warm]` / `[HOT]`. It is the one dial not recoverable from beat content and the one carrying the craft. **Do not tag mode or motion** — mode rides in the phrasing; motion is a live choice defaulted by temperature (hot→dilate, cold→compress); both live in the Legend as concepts, not runway labels. For a beat whose mode is deliberately open (a choice that could be thought *or* acted), phrase it mode-neutral and let temperature + content carry it (the "her choice — let him drown" case).

### Scene vs. sequel — pick the template by contour position
Per [[KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework]], every scene is one of two shapes, **selected from its place on the contour**:
- **Scene (proactive)** — `goal → conflict → disaster`. A peak; beats ratchet to a worse-than-it-started turn.
- **Sequel (reactive)** — `reaction → dilemma → decision`. The modulation beat *after* a peak — absorb, process, a new goal crystallizes; its closing **decision** closes an escape and fires the next scene (the staircase).

Right after a high point, run a **sequel** (the reader's numb; the floor needs resetting). Don't stack peaks (plateau fatigue) or sequels (slack) — the contour says which comes next. **Want vs. resistance is the but/therefore engine:** the *but* is the resistance, the *therefore* the cost it exacts; a sagging beat means soft resistance — strengthen the obstacle or deepen the want.

### Temperature is derived from the contour — proposed, not imposed
Default **cold**. Mark **warm/hot** at the scene's intensity peaks, derived from the sequence envelope's escalation range + the chapter/scene's place in it (scene-intensity can't run pre-draft, so this is the *planned* contour). Open each scene with a one-line **contour header**. CRE overrides any beat's temperature live — the runway is a roadmap, not a cage; this only removes the *forced* pause, never the freedom.

### Every present character is an agent — no decor
Build from the scene's **roster** (the chapter envelope lists who's present + each one's carried state, read from `arcs.md` / prior `continuity.md` / the **working-canon overlay**). **Every present character with a live arc gets their own *but/therefore* thread** — their struggle, successes, failures — interleaved with the POV character's. A present character given no thread is **decor**, the character-level UNDRAMATIZED failure — flag it. (The hound on the storm-trek is not set dressing: he entered overriding his fear with the doll in his maw, so he drops it, she says "leave it," he retrieves it — she delivers the boy, he delivers the doll.)

### Form
```
SCENE — <name>   POV: <who>   present: <roster + carried state>   contour: <one line>
goal — <character goal>  /  <story goal>
──────────────────────────────────────────────
[cold]  <in-mode beat prompt>                  → BUT <complication>
[cold]  <in-mode beat prompt>                  → THEREFORE <consequence>
   └ <sub-beat choreographing the moment>
   └ <sub-beat>
[cold]  <another present character's thread>   → THEREFORE <what it costs / the parallel>
[HOT]   <in-mode beat prompt>
★ <one write-in-full, only if the brief specifies a line/image CRE already hears>
[SEALED] <what to enact-and-withhold, per the seal schedule>
```

This supersedes Step 2's 3–5-keyword output on the dictation route; the `→` forward-pointers, the Conditions block + receipts Close (Step 4), and never-overwrite + weight-scaling (Step 5) are unchanged. The temperature-only-surface rationale lives in [[KNOWLEDGE/STYLE/REGISTER LEGEND]] ("How this wires into the system").

## Files this workflow does NOT touch
`draft.md`, `envelope.md`, `dictation/`, `slate/`, `revisions/`, `open-loops.md`, `continuity.md`, `notes.md`, `_status.md`, and `brief.md` itself (read-only). It writes one file — `runway.md` — and produces no prose.

## Logging
DIR-003 applies. Append a session line to `<chapter>/changelog.md` and the vault `_CHANGELOG.md` (newest-first, file-tool top-insert per DIR-005). File notable fragilities to `_OBSERVATIONS.md`.

## Pipeline relationship
**brief.md (confirmed) → runway-builder (this) → CRE dictates from runway.md → dictation-preflight → transcoder.** The runway is the dictation *input habit* scaffold; the envelope is the Transcoder's cut-test. They are independent prep passes off the same chapter — neither consumes the other.
