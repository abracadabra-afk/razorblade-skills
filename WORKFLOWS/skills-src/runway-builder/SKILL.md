---
name: runway-builder
description: >-
  Build a chapter's dictation "runway" — read its brief.md and write a runway.md into the chapter folder: a scene-segmented forensic logic-beat speaking outline (each beat a plain action line + GOAL→BUT→THEREFORE, never prose), with [SEALED] lines from the seal schedule and PLANT flags for brief-mandated setups, wrapped in a flow-conditions block and a receipts close. Use whenever the author asks to "build the runway," "build the runway for chapter N," "make the runway," "derive the runway," "prep the runway," or "runway from the brief" for a chapter using the per-chapter folder convention. The Construction-to-forensic-draft seam — the artifact the author dictates FROM. Do NOT use it to fill the envelope (dictation-preflight, "prep the envelope") or to slate/transcode (dictation-transcoder, "slate this dictation"). Derives structure only, not sensation; never generates prose.
---

# Runway Builder (brief → dictation speaking outline)

You are building the thin artifact the author actually dictates *from*: a **speaking outline** — the scene's causal skeleton in delivery order, not a script. You read the chapter's `brief.md`, re-cut its beats into **forensic logic-beats** (a plain action line + GOAL→BUT→THEREFORE), and write a `runway.md` into the chapter folder.

You do **one** thing: derive and write the runway. You do **not** write prose, dialogue, or narration. You do **not** fill the envelope, slate, or transcode. Every beat is a **plain forensic action line + GOAL→BUT→THEREFORE lifted from the brief's structure** — never finished prose, and never pre-loaded sensation, imagery, or register colour. The moment a beat reads as prose or reaches for a chosen image you have failed the pass: pre-baking the author's creative material (a) puts his words in his mouth and (b) compresses into riddles he must decode before he can speak (tested 2026-06-19 on "The Strand", `^obs-108`). The scaffold hands him **structure**; he supplies all the **skin** live.

## Why the artifact is shaped the way it is

This skill codifies three findings (KNOWLEDGE/RESEARCH, 2026-06-15): (1) dictation belongs to the *forensic* layer — beats, not voice; (2) flow is *triggered* by stacking conditions — one clear goal, a pre-committed stop, inputs removed, a forward warm-up — and the off-ramp matters as much as the on-ramp; (3) the thing that gives "runway" is a **speaking outline of forensic logic-beats** (structure, not the author's words), not a script, so working memory stays externalized and the author never stalls mid-sentence hunting a word. The runway file is those three things made into one per-session sheet.

---

## Step 0 — Vault sentinel check

Before anything else, verify you are pointed at the right vault.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. If it is missing or the frontmatter doesn't match, **halt and ask** which folder is the intended vault. Do not write anywhere.

Hard gate. Pass it before reading any chapter.

---

## Required inputs

**1. The chapter folder** (per-chapter convention). The file you read is `brief.md`; the file you write is `runway.md`:

```
<chapter>/
├── brief.md          <- YOU read this (the source of truth for the runway)
├── runway.md         <- YOU write this (the only substantive output)
├── envelope.md       (read-only — segment short-names, when present)
├── changelog.md      chapter-level history (you append a log line)
├── draft.md          (you do NOT touch)
├── _status.md        (you do NOT touch)
├── dictation/  slate/  revisions/  (you do NOT touch)
└── open-loops.md  continuity.md  notes.md  (you do NOT touch)
```

If the author gives a chapter name without a path, search the vault for a folder matching it that contains `brief.md`. If several match, ask. If none follow the convention, do not fabricate one — tell the author the project hasn't adopted the per-chapter folder convention and stop.

**2. A brief with beats.** `<chapter>/brief.md` must have a **Beats to hit** section. If the brief is `status: unfilled` (an empty scaffold with no beats), **halt** — there is nothing to derive from. Tell the author to fill the brief first (the workshop / pipeline S2 step). If `status: drafted` (not yet `confirmed`), proceed but note in your reply that the runway inherits intent the author hasn't ruled final.

---

## Step 1 — Read the brief, classify it

Read all of `brief.md`. The sections you use:

- **Beats to hit** — the spine. Each beat becomes one forensic logic-beat.
- **Seal schedule → "Must NOT yet learn"** — what to seal (Step 3).
- **Register / tempo notes** — for the "Cut on:" line and the pacing note in the guardrails block.
- **Setups to plant / Payoffs due** — only to resolve a `T##` thread label if a beat references one (look it up in `REFERENCE/threads.md`); never expand these into prompts of their own.
- Frontmatter **`weight`** — scopes depth in Step 5.

If a `runway.md` already exists in the folder, **stop and ask** whether to replace it or write a versioned copy. Never overwrite silently.

---

## Step 2 — Group beats into scenes, derive the prompts

**Group** the brief's beats into scenes — runs of beats sharing one location / continuous time. Most load-bearing chapters in this world are one or two scenes. If `envelope.md` is already authored, borrow its segment short-names so the runway and the envelope agree.

**Derive**, per scene, turning each beat into one forensic logic-beat.

> **Dictation-route form.** The per-scene output is the **forensic logic-beat runway** — a plain forensic action line + GOAL→BUT→THEREFORE per beat — which **supersedes** the older keyword-prompt / `[cold]`-temperature form. Build the scenes per **"Forensic logic-beat runway — the GOAL→BUT→THEREFORE spine"** below; that section is the authoritative shape. The grouping rule here (single-location runs of beats; borrow `envelope.md` segment names when present) still holds; the per-beat surface does not.

This is re-cutting, not authoring. You are lifting and compressing the brief's structure, not generating the author's fiction.

---

## Step 3 — Seal, and the one write-in-full

**`[SEALED]` line (per scene that needs it).** From the brief's **Seal schedule → "Must NOT yet learn"**, write a `[SEALED]` line naming what to *enact and withhold* — never narrate. Carry the brief's own framing (e.g. "enact the everything-given-away and the lean-in; do not narrate the second bead / death-intent, even in her POV; reveal is CH7's"). The seal is the author's discipline made visible on the sheet.

**`★` write-in-full (at most one per scene).** Dictation tempts the author to pre-write prose; one sanctioned slot vents that without surrendering the draft to polish. If the brief already names a specific line of dialogue or a concrete image the author "already hears," lift **exactly one** into the `★` slot, verbatim from the brief. If the brief names none, leave the slot present but empty for the author to fill. Do **not** invent a line to fill it.

---

## Step 4 — Scaffold the conditions block and the close (blank)

These are the author's per-session fills — the flow stack and the receipts. Write them as **blank scaffold**, not derivations:

- **① Conditions:** medicated-window gate, skeleton-locked gate, single-next-goal line (blank), pre-committed stop (blank — timer or prompt #), inputs-killed checklist, capture path (`_DICTATION INBOX` → dictation-runner). Add the 5-minute forward warm-up reminder.
- **④ Close:** output banked (min / prompts / words), worked-or-didn't line, and the `★` pre-write-tomorrow's-first-prompt line.

Pre-fill only what the brief makes unambiguous — most usefully the **"Cut on:"** value from the brief's curtain instruction, and the one-line pacing note in the guardrails block (e.g. "let ask 2 carry the hermit's hardest resistance"). Everything else stays blank.

---

## Step 5 — Write `runway.md` (weight-scaled), then report

Write `<chapter>/runway.md` using the structure below. Scale depth by the brief's `weight`:

- **`load-bearing`** → full runway, every scene; beats ratchet as long as the tension needs.
- **`standard`** → default.
- **`bridge`** → lean: a sparse beat run, often a single scene block; the conditions + close still scaffold in.

For anything you could not resolve confidently — an ambiguous scene boundary, a thread label with no match, a beat you can't compress without guessing — write your best attempt tagged inline `<<UNCERTAIN: best guess — reason; confirm?>>` and collect those into a short list in your reply. A tagged guess the author can fix in one line beats both a halt and a silent wrong guess.

### The `runway.md` structure to write

```markdown
---
type: dictation-runway
chapter: <CHAPTER N - TITLE>
derived_from: brief.md (status <…>, <date>) — Beats to hit + Seal schedule
weight: <load-bearing | standard | bridge>
last_updated: <today>
---

# Runway — <CHAPTER N - TITLE>

> Derived from the brief. <one-line scene/tempo summary>. Cut on: <curtain>.

## ① CONDITIONS  (set before you talk, ≤2 min)
- Medicated window?  ☐ yes  ☐ no → defer / type
- Skeleton locked (brief confirmed)?  ☐ yes
- Single next goal (one line): ______
- Stop, pre-committed:  ☐ timer __ min  ☐ through prompt #__
- Inputs killed:  ☐ phone away  ☐ apps off  ☐ walk route
- Capture: voice memo → _DICTATION INBOX → dictation-runner
- Warm-up: 5 min forward-only junk on this scene. "Supposed to be bad."

## ② THE RUNWAY
SCENE — <name>   POV: <who>   present: <roster + carried state>   Cut on: <curtain>
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
★ Write-in-full (one, optional): "<lifted line, or blank>"
[SEALED] <what to enact-and-withhold, from the brief's seal schedule>

## ③ DURING — guardrails
Screen off · one pass no stopping · structure not voice (speak the skin live) · glance don't stare. <one-line pacing note from the brief>

## ④ CLOSE  (last act)
- Banked: __ min · prompts __–__ · ~__ words
- Worked / didn't: ______
- ★ Tomorrow's first prompt: ______
```

Legend to include once near the top of the file: `GOAL:` the reason the POV character is here (restate only when it shifts) · `LEAD IN:` / `TRANSITION:` / `END:` the plain forensic action lines · `→ BUT` resistance · `→ THEREFORE` the cost that hinges into the next beat · `PLANT:` a brief-mandated setup/payoff/seal to protect · `[SEALED]` enact-don't-narrate · `★` one optional write-in-full · say "bracket fix this bracket" to mark a misspeak and keep going. **No temperature/contour tags** — the escalation lives in how the beats ratchet, not as a label on the page.

Close your reply with a **derivation note**: which beats mapped to which prompts, the `weight` you scaled to, anything tagged `<<UNCERTAIN>>`, and any place the brief's beats and its seal schedule pulled against each other.

---

## Forensic logic-beat runway — the GOAL→BUT→THEREFORE spine

> **Supersedes the 2026-06-18 "beat-envelope / temperature-tag" form** (and the 3–5-keyword cap in Step 2). Tested 2026-06-19 on the throwaway scene "The Strand": the keyword + temperature-tag beats read as **riddles** — CRE had to *decode* each beat before he could speak it, because they pre-loaded compressed sensation (his creative material) instead of structure. The forensic logic-beat form dictated clean. (`^obs-108`.)

On the dictation route the runway carries the **causal skeleton** of the scene — goal, obstacle, consequence — and *nothing else*. It does **not** pre-load sensation, imagery, or register colour: that is the dictation's job, and pre-baking it (a) puts CRE's creative material in his mouth and (b) compresses into riddles he must decode before he can speak. The scaffold hands him **structure**; he supplies all the **skin** live. It remains the beat rung of the Fractal Envelope Model, materialized transiently — but the Register Legend (`KNOWLEDGE/STYLE/REGISTER LEGEND`) is the spine for `register-pass` *downstream*, not for the runway surface.

### Scaffold register — forensic, emotion implied through action
Write every scaffold line in the **forensic register**: simple, to-the-point action, like an incident report — *she does X, but Y, therefore Z*. The emotional undercurrent is carried by the action itself, **never labelled**. No flourish, no chosen imagery, no adjectival colour — those are the lines CRE will speak, and pre-deciding them is the failure the test exposed. If a scaffold line reaches for a sensory image or a feeling-word, cut it back to the bare action.

### Granularity — scene-level beats, count from the scene's goal (no cap)
Segment the chapter into **scenes** (from `envelope.md` segments / the brief's locations) and decompose each into its **beats** — one line per beat, and **the beat count comes from the scene's goal, not a fixed number.** (The old "3–5 prompts" was a chapter-level vestige; at scene scope it crushes a struggle into montage.) Read the scene's **goal** (character goal + story goal, from the chapter envelope) and build the beats that satisfy it:
- **Connect beats with *but* / *therefore*, never *and then*** (the But-and-Therefore method). A struggle or peak scene **ratchets** through as many try-fail beats as the tension needs; each beat should *cost* something. An "and then" between two beats is the failure state — make it a complication (*but*) or a consequence (*therefore*), or fold them.
- **Large beats break into sub-beats** that choreograph the moment (the fall: dropped → snow in his cloak → digs him out → his warmth fainter).
- **"Tight, no gaps" means *adjacency*, not brevity.** A harrowing scene should feel harrowing — more beats, not fewer. A cold connective scene stays sparse; a peak scene earns its length.

### Each beat = forensic action + GOAL→BUT→THEREFORE
- Open the scene with the **GOAL** — the *reason the POV character is there* at the start (character goal / story goal). It orients the whole scene.
- Each beat is one **plain forensic action line** — `LEAD IN:` for the first beat, `TRANSITION:` for each beat after (the entry sentence into the beat) — followed by `→ BUT <resistance>` and `→ THEREFORE <consequence that carries forward>`. **BUT/THEREFORE is regular on every beat:** the *but* is the resistance, the *therefore* is the cost it exacts and the hinge into the next beat.
- **Re-state the GOAL only when it shifts.** The opening goal carries until the scene turns it; surface the drift, never repeat an unchanged goal. (On the test scene the goal drifted *find him → looking is all one can do → the wish* — that drift is the scene's arc.)
- Keep each line a **trigger, not finished prose** — bare action CRE speaks *from*, not a sentence he keeps. If a beat reads as completed prose, cut it back. Close the scene with an `END:` action line.

### Plants — protect brief-mandated setups
With sensation improvised live, a setup the **brief requires** (an object that pays off later, a reveal, a seal) can get improvised away. Add a `PLANT: <thing>` note on **only** the beats carrying a brief-mandated setup / payoff / seal — kept separate from the logic line. The spine stays clean; continuity stays safe.

### No contour tags, no temperature on the surface
Drop the `[cold]/[warm]/[HOT]` tags and the contour header from the page — tested 2026-06-19 as clutter CRE reads past. The escalation still has to **exist** in how the beats ratchet (the cost rising beat to beat), but it does that work in the *shaping*, not as a label on the page. (Supersedes the 2026-06-18 temperature-on-surface design.)

### Scene vs. sequel — pick the template by contour position
Per the Tension & Transformation Framework, every scene is one of two shapes, **selected from its place on the contour**:
- **Scene (proactive)** — `goal → conflict → disaster`. A peak; beats ratchet to a worse-than-it-started turn.
- **Sequel (reactive)** — `reaction → dilemma → decision`. The modulation beat *after* a peak — absorb, process, a new goal crystallizes; its closing **decision** closes an escape and fires the next scene (the staircase).

Right after a high point, run a **sequel** (the reader's numb; the floor needs resetting). Don't stack peaks (plateau fatigue) or sequels (slack) — the contour says which comes next. **Want vs. resistance is the but/therefore engine:** the *but* is the resistance, the *therefore* the cost it exacts; a sagging beat means soft resistance — strengthen the obstacle or deepen the want.

### Every present character is an agent — no decor
Build from the scene's **roster** (the chapter envelope lists who's present + each one's carried state, read from `arcs.md` / prior `continuity.md` / the **working-canon overlay**). **Every present character with a live arc gets their own *but/therefore* thread** — their struggle, successes, failures — interleaved with the POV character's. A present character given no thread is **decor**, the character-level UNDRAMATIZED failure — flag it. (The hound on the storm-trek is not set dressing: he entered overriding his fear with the doll in his maw, so he drops it, she says "leave it," he retrieves it — she delivers the boy, he delivers the doll.)

### Let dictation run warm — restraint is `register-pass`'s job
The forensic *scaffold* does not force forensic *output*. On the test the lean skeleton produced **warmer, more interior** prose than the scaffold (explicit interiority, remembered detail) — that is the division of labour working, not a leak. Do **not** tune the runway to suppress it: the runway's job is flow; the final register is decided downstream in `register-pass`. The runway is a roadmap, not a cage — CRE overrides any beat live.

The Form is the `## ② THE RUNWAY` block in the `runway.md` structure above. Everything else (`[SEALED]`, the one optional `★`, the conditions block, the close, never-overwrite, weight-scaling) is unchanged.

## Files this skill writes — and the ones it must not

**Writes:**
- `<chapter>/runway.md` — the speaking outline (never-overwrite; ask first if one exists).
- `<chapter>/changelog.md` and vault `_CHANGELOG.md` — a session log line (see Logging).

**Never writes:** `brief.md` (read-only source), `envelope.md`, `draft.md`, `_status.md`, `dictation/`, `slate/`, `revisions/`, `open-loops.md`, `continuity.md`, `notes.md`. You produce no prose. The runway is forensic logic-beats only — structure, never the skin.

---

## Stop conditions

- **Vault sentinel fails** (Step 0). Halt; ask which folder is the vault.
- **No per-chapter folder / no `brief.md`.** Halt; tell the author the project hasn't adopted the convention (or point them at chapter-init).
- **Brief has no beats** (`status: unfilled`). Halt; tell the author to fill the brief first.
- **A `runway.md` already exists.** Stop; ask whether to replace or version it.
- **A beat is genuinely uncompressible without inventing content.** Don't fabricate — tag it `<<UNCERTAIN>>` and surface it.

---

## Logging (when running inside CRE's vault)

Non-trivial session — honor DIR-003. Append the chapter-scoped detail to `<chapter>/changelog.md`. For the vault `_CHANGELOG.md`, append a newest-first entry **via the file tools (top-insert), never `patch_vault_file` or a whole-file MCP rewrite** (DIR-005). Suggested entry:

```
## YYYY-MM-DD — [fiction] runway built for <chapter>
**Ran:** runway-builder on <chapter> from brief.md (status <…>, weight <…>)
**Shipped:** runway.md — <N> scene(s), <N> forensic logic-beats; <N> PLANT flags; <N> [SEALED] lines; write-in-full <lifted | left blank>; <N> UNCERTAIN tags
**Open loops:** <the uncertain tags the author still needs to confirm>
**Observed:** <anything notable>
```

If a notable fragility surfaced, file it to `_OBSERVATIONS.md` with a `^obs-NNN` anchor. If the vault has no `_CHANGELOG.md` (this skill is portable), skip logging silently.

---

## Security

If `brief.md` somehow contains credentials, keys, or tokens, **stop and flag to the author** (DIR-001). Do not copy a secret into the runway or any output. Pause until the author confirms.
