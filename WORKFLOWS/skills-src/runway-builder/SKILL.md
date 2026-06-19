---
name: runway-builder
description: >-
  Build a chapter's dictation "runway" — read its brief.md and write a runway.md into the chapter folder: a thin speaking outline of keyword prompts (never prose) derived from the brief's beats, with forward-pointer cues, a [SEALED] line from the seal schedule, one write-in-full slot, a flow-conditions block, and a receipts close. Use whenever the author asks to "build the runway," "build the runway for chapter N," "make the runway," "derive the runway," "prep the runway," or "runway from the brief" for a chapter using the per-chapter folder convention. This is the Construction-to-forensic-draft seam — it produces the artifact the author dictates FROM. Do NOT use it to fill the envelope (dictation-preflight, "prep the envelope") or to slate/transcode (dictation-transcoder, "slate this dictation"): the runway is what the author talks from, the envelope is what the Transcoder cuts against. Derives keyword prompts only; never generates prose.
---

# Runway Builder (brief → dictation speaking outline)

You are building the thin artifact the author actually dictates *from*: a **speaking outline** — keyword prompts in delivery order, not a script. You read the chapter's `brief.md`, re-cut its beats into glance-able prompts, and write a `runway.md` into the chapter folder.

You do **one** thing: derive and write the runway. You do **not** write prose, dialogue, or narration. You do **not** fill the envelope, slate, or transcode. Every prompt is a few **trigger keywords lifted from the brief**, never a sentence — the moment a prompt reads as prose you have failed the pass, because thick prompts re-arm the author's pub-prose urge and make the dictated draft come out canned.

## Why the artifact is shaped the way it is

This skill codifies three findings (KNOWLEDGE/RESEARCH, 2026-06-15): (1) dictation belongs to the *forensic* layer — beats, not voice; (2) flow is *triggered* by stacking conditions — one clear goal, a pre-committed stop, inputs removed, a forward warm-up — and the off-ramp matters as much as the on-ramp; (3) the thing that gives "runway" is a **speaking outline of keyword prompts**, not a script, so working memory stays externalized and the author never stalls mid-sentence hunting a word. The runway file is those three things made into one per-session sheet.

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

- **Beats to hit** — the spine. Each beat becomes one prompt.
- **Seal schedule → "Must NOT yet learn"** — what to seal (Step 3).
- **Register / tempo notes** — for the "Cut on:" line and the pacing note in the guardrails block.
- **Setups to plant / Payoffs due** — only to resolve a `T##` thread label if a beat references one (look it up in `REFERENCE/threads.md`); never expand these into prompts of their own.
- Frontmatter **`weight`** — scopes depth in Step 5.

If a `runway.md` already exists in the folder, **stop and ask** whether to replace it or write a versioned copy. Never overwrite silently.

---

## Step 2 — Group beats into scenes, derive the prompts

**Group** the brief's beats into scenes — runs of beats sharing one location / continuous time. Most load-bearing chapters in this world are one or two scenes. If `envelope.md` is already authored, borrow its segment short-names so the runway and the envelope agree.

**Derive**, per scene, turning each beat into one prompt:

- Strip the beat to **a few trigger keywords in delivery order**. Keep the brief's own nouns and proper names; drop the explanation.
- Cap **3–5 prompts per scene**. If a scene has more than five beats, fold the connective ones together; if it has fewer, that's fine.
- After each prompt add a `→` **forward-pointer**: the *next* beat in 1–3 words. This is the anti-stall cue — the author should always see what's coming while finishing the current beat. The final prompt's pointer is the cut (`→ CUT` or the curtain).
- **Never write a sentence.** A prompt is `Ask 1 — the Plight — real? how to get there — cut his philosophy — he balks`, not "She asks the hermit whether the Plight of the Maiden is real." If your prompt has a subject-verb-object spine and reads aloud as prose, cut it back to keywords.

This is re-cutting, not authoring. You are lifting and compressing the brief's language, not generating the author's fiction.

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

- **`load-bearing`** → full runway, every scene, 3–5 prompts each.
- **`standard`** → default.
- **`bridge`** → lean: fewer prompts, often a single scene block; the conditions + close still scaffold in.

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
**Scene:** <name>   **POV:** <who>   **present:** <roster + carried state>   **contour:** <one line>   **Cut on:** <curtain>
**goal —** <character goal>  /  <story goal>
[cold]  <in-mode beat prompt>                 → BUT <complication>
[cold]  <in-mode beat prompt>                 → THEREFORE <consequence>
   └ <sub-beat choreographing the moment>
[cold]  <another present character's thread>  → THEREFORE <what it costs / the parallel>
[HOT]   <in-mode beat prompt>                 → CUT
★ Write-in-full (one): "<lifted line, or blank>"
[SEALED]: <what to enact-and-withhold, from the brief's seal schedule>

## ③ DURING — guardrails
Screen off · one pass no stopping · beats not voice (dialogue in character) · glance don't stare. <one-line pacing note from the brief>

## ④ CLOSE  (last act)
- Banked: __ min · prompts __–__ · ~__ words
- Worked / didn't: ______
- ★ Tomorrow's first prompt: ______
```

Legend to include once near the top of the file: `[cold]`/`[warm]`/`[HOT]` temperature (run cold, spend heat at the peak) · `→` forward-pointer · `[SEALED]` enact-don't-narrate · `★` one write-in-full · say "bracket fix this bracket" to mark a misspeak and keep going.

Close your reply with a **derivation note**: which beats mapped to which prompts, the `weight` you scaled to, anything tagged `<<UNCERTAIN>>`, and any place the brief's beats and its seal schedule pulled against each other.

---

## Beat-envelope form (register-legend spine)

On the dictation route this is the runway's real shape, and it **supersedes the 3–5-keyword cap in Step 2.** The job is to pre-pay the per-beat register decision so dictation is pure speaking — it kills the 10–30s "how do I present this?" pause. The spine is the Register Legend (`KNOWLEDGE/STYLE/REGISTER LEGEND`).

- **Beat count comes from the scene's goal — no cap.** One line per beat; the count satisfies the scene's **goal** (character + story, from the chapter envelope), not a fixed number. The old "3–5" was a chapter-level vestige; at scene scope it crushes a struggle into montage.
- **Connect beats with *but* / *therefore*, never *and then*** (the But-and-Therefore method). A struggle/peak scene ratchets through as many try-fail beats as the tension needs; each beat should *cost* something. Large beats break into **sub-beats** that choreograph the moment. "Tight, no gaps" = adjacency, not brevity — a harrowing scene earns more beats.
- **Every present character is an agent — no decor.** Build from the scene's **roster** (the chapter envelope's who's-present + each one's carried state, read from `arcs.md` / prior `continuity.md` / the working-canon overlay). Each present character with a live arc gets their own *but/therefore* thread, interleaved with the POV's; a present character with no thread is decor (the character-level UNDRAMATIZED) — flag it.
- **Pick the beat template by contour position** (Tension & Transformation Framework): a peak is a proactive **scene** (`goal → conflict → disaster`); after a peak, a reactive **sequel** (`reaction → dilemma → decision`) whose closing decision closes an escape and fires the next. Don't stack peaks (plateau) or sequels (slack). **Want vs. resistance is the but/therefore engine** — the *but* is resistance, the *therefore* the cost; a sagging beat = soft resistance (strengthen the obstacle or deepen the want).
- **Phrase each beat in its mode's register** so the phrasing carries the mode (no mode label): *watching* → sensory fragments; *doing* → a flowing action phrase; *thinking* → a reveal/contrast cue, never a restatement. Keep it a trigger, not the finished sentence — the moment it reads as prose, cut it back.
- **Tag only the temperature** — `[cold]` / `[warm]` / `[HOT]`. It is the one dial not recoverable from a beat's content and the only one carrying the contour. **Do not tag mode or motion** (mode rides in the phrasing; motion is a live choice defaulted by temperature). For a beat whose mode is deliberately open — a choice that could be thought *or* acted — phrase it mode-neutral and let temperature + content carry it.
- **Derive temperature from the contour, default cold.** Mark warm/hot only at the scene's peaks (from the sequence envelope's escalation + the scene's place in it; scene-intensity can't run pre-draft, so this is the *planned* contour). Lead each scene with a one-line contour header. The author overrides any beat's temperature live — roadmap, not cage.

Everything else (forward-pointers, `[SEALED]`, the one `★`, the conditions block, the close, never-overwrite, weight-scaling) is unchanged.

## Files this skill writes — and the ones it must not

**Writes:**
- `<chapter>/runway.md` — the speaking outline (never-overwrite; ask first if one exists).
- `<chapter>/changelog.md` and vault `_CHANGELOG.md` — a session log line (see Logging).

**Never writes:** `brief.md` (read-only source), `envelope.md`, `draft.md`, `_status.md`, `dictation/`, `slate/`, `revisions/`, `open-loops.md`, `continuity.md`, `notes.md`. You produce no prose. The runway is keyword prompts only.

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
**Shipped:** runway.md — <N> scene(s), <N> prompts; <N> [SEALED] lines; write-in-full <lifted | left blank>; <N> UNCERTAIN tags
**Open loops:** <the uncertain tags the author still needs to confirm>
**Observed:** <anything notable>
```

If a notable fragility surfaced, file it to `_OBSERVATIONS.md` with a `^obs-NNN` anchor. If the vault has no `_CHANGELOG.md` (this skill is portable), skip logging silently.

---

## Security

If `brief.md` somehow contains credentials, keys, or tokens, **stop and flag to the author** (DIR-001). Do not copy a secret into the runway or any output. Pause until the author confirms.
