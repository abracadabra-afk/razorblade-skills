---
type: workflow
name: runway-builder
trigger: build the runway
aliases: [build the runway for chapter N, make the runway, derive the runway, prep the runway, runway from the brief, build the dictation runway, runway this chapter]
inputs: [a chapter folder using the per-chapter convention with a filled brief.md]
outputs: [a runway.md written into the chapter folder — the v3 chronological-spine speaking outline: entry state, per-scene "what happens" + story goal + plain chronological beats shaped to the tension curve, set & lore, dialogue bank, register reminders, and a notes space that makes the doc CRE's workspace]
lane: fiction
status: draft
last_updated: 2026-07-28
consumes: [the chapter's brief.md (Beats to hit + Seal schedule + goal + weight), envelope.md (segment names + POV + roster, when present), the PRIOR chapter's continuity.md + open-loops.md (entry state), REFERENCE/threads.md, REFERENCE/bible.md + the project DEV tree (set & lore + dialogue bank — tree-sourced only)]
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). First adopter — Witchwood.
pipeline_position: Construction (confirmed brief.md) → THIS → Phase 3 dictation; parallel-upstream sibling of [[WORKFLOWS/dictation-preflight]]
sources: KNOWLEDGE/RESEARCH 2026-06-15 — [[KNOWLEDGE/RESEARCH/2026-06-15 dictation-practice-fiction]] · [[KNOWLEDGE/RESEARCH/2026-06-15 flow-state-writing-dictation]] · [[KNOWLEDGE/RESEARCH/2026-06-15 outlines-adhd-dictation-flow]] · check-ins [[LIFE/CHECK-INS/entries/2026-07-26-daily]] + [[LIFE/CHECK-INS/entries/2026-07-27-daily]] (the v3 evidence) · CRE format ruling 2026-07-28
---

# WORKFLOW: Runway Builder (brief → dictation speaking outline, v3 chronological spine)

> Derivation pass that reads a chapter's `brief.md` and writes a `runway.md` into the chapter folder — the speaking outline CRE dictates from **and annotates as his own**. v3 (CRE-ruled 2026-07-28) replaces the forensic GOAL→BUT→THEREFORE surface with a **chronological spine**: plain sentences stating what happens and why, in order, shaped to CRE's tension curve. The runway is both a starting stone for dictation and a workspace CRE marks up as he sees opportunities to enhance the story. Sits at the **Construction → dictation seam**: after the brief is confirmed, before CRE records.

## When to use

When a chapter using the per-chapter folder convention has a `brief.md` with **Beats to hit**, and CRE wants the dictation runway for it. Trigger phrases: "build the runway," "build the runway for chapter N," "make the runway," "derive the runway," "runway from the brief." Do NOT use it to fill the envelope (that is [[WORKFLOWS/dictation-preflight]]) or to slate dictation (that is [[WORKFLOWS/transcoder]]). The runway is what CRE dictates **from**; the envelope is what the Transcoder cuts **against** — different artifacts, different passes.

## Inputs

- **The chapter folder** (per-chapter convention).
- **`<chapter>/brief.md`** — the source of truth for this pass. Read **Beats to hit**, **Seal schedule**, **Register / tempo notes**, and the `weight` field.
- **The prior chapter's `continuity.md` + `open-loops.md`** — for the Entry state (where the story stands, carried loops worth flagging).
- **`<chapter>/envelope.md`** (optional) — segment short-names + roster, when already authored.
- **`REFERENCE/threads.md`** — to resolve `T##` thread labels and source dialogue-bank / set-piece entries.
- **`REFERENCE/bible.md` + the project DEV tree** (as needed) — the only permitted sources for Set & lore and Recommended-tier dialogue entries. **Tree-sourced only; never invented.**

## Outputs

- **`<chapter>/runway.md`** — the v3 chronological-spine outline (see "The v3 form" below).
- A short **derivation note** in the reply: which brief beats mapped where, anything tagged `<<UNCERTAIN>>`, and any divergence from the brief worth CRE's eye.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Load and classify the brief
Read `<chapter>/brief.md`. If it has no **Beats to hit** (status `unfilled`), halt — nothing to derive; tell CRE to fill the brief first (workshop / pipeline S2). If `status` is `drafted` (not `confirmed`), proceed but note the runway inherits unconfirmed intent. Read `weight` — it scopes depth (Step 6).

### Step 2 — Entry state
From the prior chapter's `continuity.md` + `open-loops.md`: 2–4 lines on where the story stands entering this chapter — position, who carries what, the operative emotional state, and any carried loop worth a ⚠️ flag (a thread gone dark, a state left implicit that this chapter inherits). This is orientation, not recap — only what CRE needs to hold to start talking.

### Step 3 — Scenes: summary, story goal, chronological beats
Group the brief's beats into scenes (single-location runs; cross-reference `envelope.md` segments when present). Per scene:

- **Header:** scene name · POV · present (roster + carried state, kept to one line).
- **What happens:** one plain sentence — the whole scene in a glance.
- **Story goal:** what the **story** needs this scene to accomplish — the arc moved, the reversal landed, the plant set. Not the POV character's want (that lives in the beats themselves).
- **Beats:** plain declarative sentences, **chronological**, stating what happens and why. Shaped to the tension curve (below), with the escalation living in the *shaping*, never in labels. `PLANT:` and `[SEALED]` ride inline on the beats that carry them (Step 4).

### Step 4 — Plants + seals
From the brief's **Seal schedule**, write a `[SEALED]` line where it applies: name what to enact-and-withhold, never narrate. Add `PLANT:` only on beats carrying a brief-mandated setup / payoff / seal. These are the continuity protections that survive from every prior form — with sensation improvised live, a required setup can get improvised away; the flags keep it safe.

### Step 5 — Set & lore, dialogue bank, register reminders
- **SET & LORE** — one line per setting / set piece: what it is and why it matters to the story. No description paragraphs. Sourced from the brief, bible, threads, and DEV tree only.
- **DIALOGUE BANK** — conversations, **never lines**. Each entry: who · about what · what must change hands. Two tiers:
  - **Critical** — key emotional moments between characters that push arcs forward. Derived from the brief's mandated beats and the thread schedule.
  - **Recommended** — flavor, character, worldbuilding. **Tree-sourced only** (threads, DEV entries, prior continuity — e.g. a thread checkpoint due for revival). If the tree is silent, the tier stays empty for CRE's own notes. The builder never invents a conversation the tree doesn't name (organic-process guard, CRE-ruled 2026-07-28).
- **REGISTER REMINDERS** — a short glance-then-ignore list: only the **elective-restraint commitments** for this chapter (seal discipline, POV interiority limits, the register commitment the chapter specifically tests). Never mechanical fixes `register-pass` will catch downstream — those are its job, not the mic's.

### Step 6 — Write `runway.md` (never-overwrite; weight-scaled)
Close the doc with a **Your notes** section and the standing invitation ("mark this file up — arrange, annotate, cut, add; this file is yours"). Write `<chapter>/runway.md`. **Never overwrite** an existing `runway.md` — if one exists, stop and ask whether to replace or version it. Scale depth by `weight`: `load-bearing` → full treatment, every scene; `bridge` → lean (may collapse to one scene block, bank + lore optional); `standard` → default. Tag anything unresolvable `<<UNCERTAIN: best guess — reason; confirm?>>` and surface it in the reply rather than guessing silently.

## The v3 form — chronological spine (CRE-ruled 2026-07-28)

> **Supersedes the 2026-06-19 forensic GOAL→BUT→THEREFORE form** (and, transitively, the 2026-06-18 beat-envelope/temperature form). Evidence: the 07-23 CH9 impasse on the forensic arm, the 07-26/07-27 check-ins (`^backlog-runway-format-friction` — wins on plain chronological bullets across Witchwood dev-sequencing, Doomscroller, and a Godsrift chapter; losses on both system runways), and the two-arm CH9 comparison (forensic `runway.md` vs `runway-bare.md`). CRE's ruling is a **merge**, not a swap: bare's chronological plainness and ownership posture + the current form's entry state, scene summary, story goal, plants, and seals — plus two new sections (set & lore, dialogue bank).

### Beat register — plain statement, emotion through action
Beats are **short plain sentences in chronological order that state what happens and why**. The old "triggers, never sentences" rule is dead: keyword compression made CRE *decipher his own story* at the mic (the named friction — "too much unnecessary information… necessary information presented in a fragmented fashion"). Sometimes it is important to plainly state what is happening and why, so he can hold it in his head and move beat to beat. What survives from the forensic register: **no flourish, no chosen imagery, no adjectival colour, no pre-baked sensation** — emotion is carried by the action, never labelled. The skin is still his, spoken live.

### The tension curve — shape, never label
Each scene's beats are shaped to CRE's named curve: **lead-in (current state) → beats of escalating tension → climax → dip for reflection or decision → hook.** No BUT/THEREFORE labels, no LEAD IN/TRANSITION/END scaffolding, no contour or temperature tags on the page (the 2026-06-19 clutter ruling stands). The escalation must *exist* in how the beats ratchet — cost rising beat to beat, the dip doing its sequel work (absorb → decide → the decision fires the hook) — but it does that work in the shaping, invisibly. A sagging run of beats means soft resistance: strengthen the obstacle in the *content* of the beats, not with a label.

### Ownership — the runway is CRE's workspace
The doc's second job (co-equal with dictation): a surface CRE **modifies and makes notes on** as he sees opportunities to enhance the story. Plain markdown bullets he can reorder, cut, and annotate; a Your-notes section; the standing mark-this-file-up invitation. The arranging *is* the ownership step — the machine deliberately does not finish the doc for him.

### Every present character acts
Build from the scene's roster. Every present character with a live arc **does something** in the beats — a present character given no action is decor, the character-level UNDRAMATIZED failure. (No per-character logic-thread notation anymore; their actions simply appear in the chronology.)

### Dropped from prior forms
- **Conditions block** — dead. Session mechanics live in CRE's own habits, not the runway.
- **Close / receipts block** — dead. The daily check-ins own worked/didn't-work capture.
- **`★` write-in-full slot** — dead (default, 2026-07-28: unclaimed in the format ruling; the dialogue bank covers its job).
- **Forensic labels** (GOAL/BUT/THEREFORE, LEAD IN/TRANSITION/END) — dead on the runway surface. The but/therefore causal logic remains a *shaping discipline* for the builder, never notation on the page.

### Let dictation run warm — restraint is `register-pass`'s job
Unchanged, and now DIR-017 law. The runway's job is flow; the final register is decided downstream. The runway is a roadmap, not a cage — CRE overrides any beat live, and **divergence from the runway is a win**; no downstream pass grades the draft against the plan. **No editing during dictation** (`^obs-221` / DIR-017 clause 1): the mic is forward-only; if a beat is friction he can't move past, that is a runway-format signal, not a cue to edit at the mic. Density scales to how much CRE must re-load, not to the work's importance (DIR-017 clause 2).

### Form
```
# Runway — <CHAPTER>

> <one-line orientation: scenes + the cut>
> Mark this file up — arrange, annotate, cut, add. This file is yours.

## ENTRY STATE  (from CH<N-1> continuity)
- <where the story stands — 2–4 lines>
- ⚠️ <carried loop worth flagging, if any>

## SCENE <n> — <name>   POV: <who>   present: <roster + carried state>
**What happens:** <one plain sentence>
**Story goal:** <what the story needs this scene to do>

- <plain chronological beat — what happens, and why when it matters>
- <beat>
   - PLANT: <only if the brief mandates a setup/payoff/seal here>
- <climax beat>
- <dip beat — reflection / decision>
- <hook beat> *(hook → next scene)*
- [SEALED] <what to enact-and-withhold, per the seal schedule>

## SET & LORE
- <setting / set piece> — <why it matters to the story>

## DIALOGUE BANK  (conversations, never lines)
- **Critical** — <who + about what>. What changes hands: <the arc movement>.
- **Recommended** — <who + about what — tree-sourced (thread/dev/continuity ref)>.

## REGISTER REMINDERS  (glance before you start, then ignore)
- <elective-restraint commitment for this chapter>

## Your notes
<!-- arrange, annotate, cut, add — this file is yours -->
```

## History

- **v1 (2026-06-18)** — beat-envelope / temperature tags. Superseded same week: read as riddles (`^obs-108`).
- **v2 (2026-06-19)** — forensic logic-beats, GOAL→BUT→THEREFORE. Dictated clean on the test scene, but live chapter use (CH9, Doomscroller) hit task-initiation impasses: fragmented presentation, deciphering-on-the-fly, no ownership (`^backlog-runway-format-friction`, check-ins 2026-07-26/27). Pre-slim copy of the v2 spec: git history of this doc.
- **v3 (2026-07-28)** — chronological spine, CRE-ruled from the two-arm CH9 comparison + his section-by-section format review. The causal but/therefore logic survives as builder discipline; the page shows plain chronology.

## Files this workflow does NOT touch
`draft.md`, `envelope.md`, `dictation/`, `slate/`, `revisions/`, `open-loops.md`, `continuity.md`, `notes.md`, `_status.md`, and `brief.md` itself (read-only). It writes one file — `runway.md` — and produces no prose.

## Logging
DIR-003 applies. Append a session line to `<chapter>/changelog.md` and the vault `_CHANGELOG.md` (newest-first, file-tool top-insert per DIR-005). File notable fragilities to `_OBSERVATIONS.md`.

## Pipeline relationship
**brief.md (confirmed) → runway-builder (this) → CRE annotates + dictates from runway.md → dictation-preflight → transcoder.** The runway is the dictation *input habit* scaffold; the envelope is the Transcoder's cut-test. They are independent prep passes off the same chapter — neither consumes the other.
