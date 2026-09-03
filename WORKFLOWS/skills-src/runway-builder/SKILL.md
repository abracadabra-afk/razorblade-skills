---
name: runway-builder
description: >-
  Build a chapter's dictation runway — read its brief.md and write a runway.md into the chapter folder: the v3 chronological-spine speaking outline. Entry state, then per scene a one-line what-happens, a story goal, and plain chronological beats shaped to the tension curve (lead-in, escalation, climax, dip, hook — no BUT/THEREFORE labels), with PLANT and [SEALED] flags, SET & LORE one-liners, a DIALOGUE BANK (conversations, never lines — Critical and tree-sourced Recommended), slim register reminders, and a Your-notes section: the doc is the author's workspace to annotate and rearrange. Use whenever the author asks to "build the runway," "make the runway," "derive the runway," "prep the runway," or "runway from the brief" on the per-chapter folder convention. Do NOT use it to fill the envelope (dictation-preflight) or to slate/transcode (dictation-transcoder). Structure only; never generates prose.
---

# Runway Builder (brief → dictation speaking outline, v3 chronological spine)

You are building the artifact the author dictates *from* — and annotates as **his own**. You read the chapter's `brief.md`, re-cut its beats into a **chronological spine** (plain sentences stating what happens and why, in order), and write a `runway.md` into the chapter folder.

You do **one** thing: derive and write the runway. You do **not** write prose, dialogue lines, or narration. You do **not** fill the envelope, slate, or transcode. Beats are plain declarative sentences lifted from the brief's structure — **no flourish, no chosen imagery, no adjectival colour, no pre-baked sensation**: emotion is carried by the action, never labelled. The skin is the author's, spoken live. But unlike older forms, a beat may plainly state what is happening *and why* — keyword compression that makes the author decipher his own story at the mic is the failure state this form replaced (CRE-ruled 2026-07-28).

## Why v3 is shaped this way

The v2 forensic form (GOAL→BUT→THEREFORE per beat) validated on a test scene but failed at live chapter scale — task-initiation impasses, "deciphering on the fly," no ownership. The author's own wins came from plain chronological bullets he annotates and rearranges: *"I go in there and add my notes and arrange it the way I want to — that creates an ownership."* v3 merges that plainness with the survivors of the old form (entry state, story goal, plants, seals) plus two new sections (set & lore, dialogue bank). The but/therefore causal logic survives as **your shaping discipline** — it never appears as notation on the page. The doc has two co-equal jobs: a starting stone for dictation, and a workspace the author marks up as he sees opportunities to enhance the story.

---

## Step 0 — Vault sentinel check

Before anything else, verify you are pointed at the right vault.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. If it is missing or the frontmatter doesn't match, **halt and ask** which folder is the intended vault. Do not write anywhere.
4. **Creative-lane load (ratified 2026-09-03):** read `_CREATIVE DIRECTIVES.md` from the mounted root (CDIR-001–010 — how AI behaves around CRE's craft) before opening any project file. `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both. Missing → proceed and note it; it is not a sentinel.

Hard gate. Pass it before reading any chapter.

---

## Required inputs

**1. The chapter folder** (per-chapter convention). You read `brief.md`; you write `runway.md`:

```
<chapter>/
├── brief.md          <- YOU read this (the source of truth)
├── runway.md         <- YOU write this (the only substantive output)
├── envelope.md       (read-only — segment names + roster, when present)
├── changelog.md      chapter-level history (you append a log line)
├── draft.md  _status.md  dictation/  slate/  revisions/   (you do NOT touch)
└── open-loops.md  continuity.md  notes.md                 (you do NOT touch)
```

If the author gives a chapter name without a path, search the vault for a folder matching it that contains `brief.md`. If several match, ask. If none follow the convention, do not fabricate one — say so and stop.

**2. A brief with beats.** `brief.md` must have a **Beats to hit** section. `status: unfilled` → **halt**; tell the author to fill the brief first (workshop / pipeline S2). `status: drafted` (not `confirmed`) → proceed, but note the runway inherits unconfirmed intent.

**3. The prior chapter's `continuity.md` + `open-loops.md`** — for the Entry state.

**4. Reference material as needed:** `REFERENCE/threads.md` (thread labels, dialogue-bank sourcing), `REFERENCE/bible.md` + the project DEV tree (set & lore, Recommended dialogue — **tree-sourced only**).

---

## Step 1 — Read the brief, classify it

Sections you use: **Beats to hit** (the spine), **Seal schedule → "Must NOT yet learn"** (seals), **Setups to plant / Payoffs due** (PLANT flags + thread lookups), **Register / tempo notes** (the register reminders + the cut), frontmatter **`weight`** (depth scaling, Step 6).

If a `runway.md` already exists, **stop and ask** whether to replace or version it. Never overwrite silently.

---

## Step 2 — Entry state

From the prior chapter's `continuity.md` + `open-loops.md`: 2–4 lines on where the story stands entering this chapter — position, who carries what, the operative emotional state, and any carried loop worth a warning flag (a thread gone dark, a state the previous chapter left implicit that this one inherits). Orientation, not recap — only what the author needs to hold to start talking.

---

## Step 3 — Scenes: what happens, story goal, chronological beats

**Group** the brief's beats into scenes (single-location / continuous-time runs; borrow `envelope.md` segment names when present). Per scene:

- **Header:** scene name · POV · present (roster + carried state, one line).
- **What happens:** one plain sentence — the whole scene at a glance.
- **Story goal:** what the **story** needs this scene to accomplish — the arc moved, the reversal landed, the plant set. Not the POV character's want; that lives inside the beats.
- **Beats:** plain declarative sentences, **chronological**, stating what happens and why when the why matters. Shape them to the tension curve: **lead-in (current state) → escalating beats → climax → dip for reflection or decision → hook.** The escalation lives in the shaping — cost rising beat to beat, the dip doing its work (absorb → decide → the decision fires the hook) — **never** as labels, contour tags, or temperature marks on the page. A sagging run means soft resistance: strengthen the obstacle in the beats' content.
- **Every present character acts.** A present character with a live arc who does nothing is decor — the character-level UNDRAMATIZED failure. Their actions appear in the chronology; no per-character notation.
- Beat count comes from the scene's job, not a fixed number. A harrowing scene earns more beats; a connective scene stays sparse. Large beats may break into sub-beats that choreograph the moment.

This is re-cutting, not authoring. You lift and shape the brief's structure; you never generate the author's fiction.

---

## Step 4 — Plants + seals

From the brief's **Seal schedule**, write a `[SEALED]` line where it applies: name what to *enact and withhold* — never narrate. Carry the brief's own framing. Add `PLANT:` only on beats carrying a brief-mandated setup / payoff / seal, indented under the beat. With sensation improvised live, a required setup can get improvised away — these flags keep continuity safe while the spine stays clean.

---

## Step 5 — Set & lore, dialogue bank, register reminders

- **SET & LORE** — one line per setting / set piece: what it is and why it matters to the story. No description paragraphs. Sourced from the brief, bible, threads, and DEV tree only.
- **DIALOGUE BANK** — conversations, **never lines**. Each entry: who · about what · what must change hands. Two tiers:
  - **Critical** — key emotional moments between characters that push arcs forward. Derived from the brief's mandated beats and the thread schedule.
  - **Recommended** — flavor, character, worldbuilding. **Tree-sourced only** (threads, DEV entries, prior continuity — e.g. a thread checkpoint due for revival). If the tree is silent, leave the tier empty for the author's own notes. **Never invent a conversation the tree doesn't name** (organic-process guard, CRE-ruled 2026-07-28).
- **REGISTER REMINDERS** — a short glance-then-ignore list: only the **elective-restraint commitments** this chapter specifically tests (seal discipline, POV interiority limits — e.g. "stay inside her fog; the narrator may not outrun her"). Never mechanical fixes register-pass will catch downstream.

---

## Step 6 — Write `runway.md` (weight-scaled), then report

Close the doc with a **Your notes** section and the standing invitation (mark this file up — arrange, annotate, cut, add; this file is yours). Scale depth by the brief's `weight`:

- **`load-bearing`** → full treatment, every scene.
- **`standard`** → default.
- **`bridge`** → lean: may collapse to one scene block; set & lore + dialogue bank optional.

For anything you could not resolve confidently, write your best attempt tagged inline `<<UNCERTAIN: best guess — reason; confirm?>>` and collect those into a short list in your reply. A tagged guess the author can fix in one line beats both a halt and a silent wrong guess.

### The `runway.md` structure to write

```markdown
---
type: dictation-runway
form: v3-chronological-spine
chapter: <CHAPTER N - TITLE>
derived_from: brief.md (status <…>, <date>) — Beats to hit + Setups + Seal schedule; entry state from CH<N-1> continuity.md
weight: <load-bearing | standard | bridge>
last_updated: <today>
---

# Runway — <CHAPTER N - TITLE>

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
- <hook beat> *(hook → next scene / the cut)*
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

Close your reply with a **derivation note**: which brief beats mapped to which scenes, the `weight` you scaled to, anything tagged `<<UNCERTAIN>>`, dialogue-bank sources cited, and any place the brief's beats and its seal schedule pulled against each other.

---

## Dictation is protected — DIR-17 posture

- **The runway is a flow-kickstarter, not a spec.** Density scales to how much the author must re-load (a novel chapter re-loads canon; a short holds in working memory), never to the work's importance. Craft rules never gate dictation as preconditions.
- **Divergence from the runway is a win.** No downstream pass grades the finished draft against the plan.
- **No editing during dictation.** The mic is forward-only; if a beat is friction the author can't move past, that is a runway-format signal, not a cue to edit at the mic.
- **Let dictation run warm.** A plain scaffold producing warm, interior prose is the division of labour working. The final register is decided downstream in register-pass — do not tune the runway to suppress warmth.

---

## Files this skill writes — and the ones it must not

**Writes:** `<chapter>/runway.md` (never-overwrite; ask first), `<chapter>/changelog.md` + vault `_CHANGELOG.md` (session log line).

**Never writes:** `brief.md` (read-only source), `envelope.md`, `draft.md`, `_status.md`, `dictation/`, `slate/`, `revisions/`, `open-loops.md`, `continuity.md`, `notes.md`. You produce no prose and no dialogue lines.

---

## Stop conditions

- **Vault sentinel fails** (Step 0). Halt; ask which folder is the vault.
- **No per-chapter folder / no `brief.md`.** Halt; point at chapter-init.
- **Brief has no beats** (`status: unfilled`). Halt; the brief fills first.
- **A `runway.md` already exists.** Stop; ask replace-or-version.
- **A beat, set-piece, or dialogue entry cannot be derived without inventing story content.** Don't fabricate — tag `<<UNCERTAIN>>` or leave the slot empty and surface it.

---

## Logging (when running inside CRE's vault)

Non-trivial session — honor DIR-003. Append the chapter-scoped detail to `<chapter>/changelog.md`. For the vault `_CHANGELOG.md`, append a newest-first entry **via the file tools (top-insert), never `patch_vault_file` or a whole-file MCP rewrite** (DIR-005). Suggested entry:

```
## YYYY-MM-DD — [fiction] runway built for <chapter> (v3)
**Ran:** runway-builder on <chapter> from brief.md (status <…>, weight <…>)
**Shipped:** runway.md — <N> scene(s), <N> beats; <N> PLANT flags; <N> [SEALED] lines; <N> dialogue-bank entries (sources cited); <N> UNCERTAIN tags
**Open loops:** <the uncertain tags the author still needs to confirm>
**Observed:** <anything notable>
```

If a notable fragility surfaced, file it to `_OBSERVATIONS.md` with a `^obs-NNN` anchor. If the vault has no `_CHANGELOG.md` (this skill is portable), skip logging silently.

---

## Security

If `brief.md` somehow contains credentials, keys, or tokens, **stop and flag to the author** (DIR-001). Do not copy a secret into the runway or any output. Pause until the author confirms.
