---
type: workflow
name: canon-sync
trigger: sync the canon
aliases: [canon sync, update the canon, update the story so far, update the bible, sync chapter N]
inputs: [the chapter's landed draft.md, REFERENCE/story-so-far.md, REFERENCE/bible.md, REFERENCE/threads.md, REFERENCE/arcs.md, the chapter's continuity.md, the chapter's brief.md (read-only, intent cross-check), the run's pass-1-blind.md (read-only, Prediction harvest)]
outputs: [updated REFERENCE/story-so-far.md, updated REFERENCE/bible.md, updated REFERENCE/threads.md (thread events + blind-read pickup), updated REFERENCE/arcs.md (entry/waypoint/exit character state), filled end-state sections + the Character state @ end of chapter block in the chapter's continuity.md, a conflict block for CRE to rule when the draft contradicts existing canon]
lane: fiction
status: active
last_updated: 2026-06-13
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]) that keep a REFERENCE/ folder. First adopter — Witchwood.
pipeline_position: downstream of [[WORKFLOWS/promote-revision]] — runs when a chapter's draft.md has landed. Its outputs feed the NEXT chapter's [[WORKFLOWS/dictation-preflight]] (which reads REFERENCE first, back-walks only as fallback).
---

# WORKFLOW: Canon Sync

> Derivation pass that runs when a chapter **lands** — i.e. after [[WORKFLOWS/promote-revision]] has made `draft.md` canonical. It reads the landed draft and updates the project's rolling state: `REFERENCE/story-so-far.md`, `REFERENCE/bible.md`, `REFERENCE/threads.md`, `REFERENCE/arcs.md`, and the chapter's own `continuity.md` end-state + character-state sections. It closes the context loop: each landed chapter updates project state, and that state primes the next chapter's pre-flight. This is the fix for [[_OBSERVATIONS#^obs-010]] — `continuity.md`'s end-state sections were dead template that no skill owned, and chapter-spanning canon pointed at archived docs.
>
> **Continuity model (added 2026-06-13, `^obs-048`).** Canon-sync also tracks **character state over time**, ported from the parked Inkwell orchestrator's `character_arc_maps` (entry → waypoints → exit) and `character_progression_timeline` (per-scene physical/mental/relationship/decision/arc-position). `bible.md` answers *what is true about X*; `arcs.md` + the per-chapter character-state block answer *where X is on their journey, and how their physical/mental/relationship state changes chapter to chapter.* The per-chapter state blocks are the data; `arcs.md` is the roll-up (entry state seeded once, waypoints at flagged turns, exit state = the rolling latest).

## When to use

After promoting a revision (or whenever `draft.md` meaningfully changed and the project state is stale). Trigger phrases: "sync the canon," "update the story so far," "update the bible." (The full promote→canon→storyline bundle is [[WORKFLOWS/land-chapter]], which now owns "land the chapter" and calls this skill as its canon leg.) Do NOT use it to revise prose (that is [[WORKFLOWS/register-pass]]), to move a revision into the draft (that is [[WORKFLOWS/promote-revision]]), or to fill an envelope (that is [[WORKFLOWS/dictation-preflight]]). It derives state from finished prose; it never changes a word of any draft.

## Key principles

1. **Derive only from landed text.** The source is `<chapter>/draft.md`. Never derive canon from `slate/` or `revisions/` — those are intermediate. If `draft.md` is a scaffold or `status` shows pre-register work, warn and ask before syncing.
2. **Every derived fact carries provenance.** Each bible fact and story-so-far section is tagged with its source (`CH<N> rev<M>` from the draft's `source_revision`). Provenance is what makes re-syncing safe: when a chapter is re-promoted, the re-run replaces exactly the facts sourced from that chapter and nothing else.
3. **Idempotent per chapter.** Re-running canon-sync on the same chapter replaces that chapter's derived entries in place. It never duplicates and never touches entries sourced from other chapters.
4. **Additions write; conflicts gate.** New entities, new facts, and the chapter synopsis write automatically. Anything that **contradicts** existing canon (bible says blue eyes, draft says brown; story-so-far has him in the vale, draft opens him on the ridge) halts for CRE's ruling — it is either a continuity error or an intentional reveal, and only CRE can rule which. Deferred rulings are logged to the chapter's `open-loops.md`.
5. **Fill-gaps-only on author text.** In `continuity.md` and the bible, author-written lines are never overwritten. Uncertain derivations are tagged `<<UNCERTAIN: …; confirm?>>`, never guessed silently (same discipline as pre-flight).
6. **State is observed-or-inferred, and tracked over time.** Physical/mental/relationship state and arc position are derived per chapter. A state the text *states* is recorded plainly; a state the text only *implies* is tagged `<<UNCERTAIN: …; confirm?>>` (the orchestrator's `derivation_mode: direct|inference` discipline, mapped to the vault's existing UNCERTAIN convention). The per-chapter `continuity.md` blocks are the source data; `arcs.md` is the idempotent roll-up — entry state written once at a character's first appearance, a waypoint appended at each chapter CRE (or an obvious turn) flags, exit state always overwritten to the latest chapter's state. Like every other derived fact, character-state entries carry `(CH<N> rev<M>)` provenance and re-sync replaces only this chapter's.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Locate chapter + verify it has landed
Resolve the chapter folder; read `draft.md` frontmatter. Expect `status: register-revised` (or `dev-revised` if CRE explicitly syncs mid-pipeline). Record `source_revision` (or `source_slate` if no revision yet) as this sync's provenance tag. Scaffold or missing draft → halt.

### Step 2 — Load current state
Read `REFERENCE/story-so-far.md`, `REFERENCE/bible.md`, `REFERENCE/threads.md`, and `REFERENCE/arcs.md` (create any from the scaffold templates if missing) and the chapter's `continuity.md`. Index existing bible facts by entity and provenance, open threads by id, and the current entry/waypoint/exit state per character in `arcs.md`. **The set of bible facts and thread events already provenance-tagged to THIS chapter (`(CH<N> rev<M>)`) is the prior extraction — treat it as the baseline to diff the new draft against (see Step 3).** Also read, read-only: the chapter's `brief.md` (if present) and the run's `spec-check/<slate-run>/pass-1-blind.md` (if present).

### Step 3 — Extract (diff-based, not a spot-read)
> **This is a DIFF, not a fresh read.** A re-sync's job is to find the *delta* between the chapter's prior extraction (the CH-tagged facts from Step 2) and the current landed draft. Reading only the new draft for "what's there" silently misses **removed** facts — text that was cut in a revision but whose derived canon still asserts it (the `^obs-015` failure: a hand-revision cut the hunter's-mother paragraph and the opening establishing paragraph, but canon-sync spot-read the new draft and left the stranded bible/codex facts in place across three rounds). Walk every CH-tagged fact and confirm the current draft still supports it; if it doesn't, that fact is **dropped** and must be surfaced, not ignored.

Read the landed draft and extract four layers:
- **Synopsis** — what happens in this chapter, in order, ~150–250 words, spoiler-honest (what the text establishes, not what CRE knows is coming).
- **Entity facts** — characters, places, objects, lore rules, invented terms: new entities, new facts about known entities, and **contradictions** with existing bible facts.
- **Dropped facts** — every bible fact / thread event tagged to this chapter (Step 2 baseline) that the current draft **no longer supports** because a revision cut or rewrote the text. Absence is not contradiction; it gates as its own class — archive to History / keep as author-intended / defer (Step 4). Check entity entries, place grounds, lore/season details, terms, and thread plantings — not just the spot the change seems to touch.
- **End-state** — as of the chapter's last line: entities/objects in play (where, condition), physical state of POV + others (wounds, weather, distance), knowledge state (who knows what / doesn't know).
- **Character state & arc** — for each character meaningfully on stage in this chapter: `physical` (body, wounds, exhaustion), `mental` (emotional/psychological state, what they want or fear now), `relationships` (notable shifts in how they stand toward another character this chapter — `X ↔ Y: <shift>`), `key decision` (any choice that moves them), and `arc_position` (where they sit on their journey — e.g. `setup / rising / midpoint / crisis / climax / falling / resolution`; use the project's own arc vocabulary if it has one). Then, at the arc level: a character appearing for the **first time** gets an **entry state**; a chapter that is an obvious turning point (or one the brief flags) gets a **waypoint**; every tracked character's **exit state** advances to this chapter. Anything the text only implies (not states) is flagged `<<UNCERTAIN>>` per principle 6.
- **Thread events** — new promises planted (each becomes a `threads.md` entry), advances to open threads, and payoffs/abandonments (these move the thread to **Settled** with a History line — settling a thread is a state change, so gate it like a conflict if the brief or an author note says it should still be open). Cross-check against the chapter's `brief.md` "Setups to plant" — a setup the brief intended that the landed text doesn't carry gets surfaced to CRE, not silently skipped. If `pass-1-blind.md` exists for this run, record its Prediction pickups per planted thread (predicted / not surfaced).

### Step 4 — Gate conflicts and drops
Two classes gate before writing **anything that depends on the ruling**:
- **Contradictions** — the draft asserts something different from existing canon. Present the existing fact + provenance, the new evidence + quote, and a recommendation (error vs. intentional change). CRE rules: update canon / keep canon and flag the draft line / defer.
- **Dropped facts** (from the Step 3 diff) — a CH-tagged fact the revised draft no longer supports. Present the stranded fact + where it lives (bible entry, place grounds, lore/season, term, thread planting) and a recommendation. CRE rules: archive to History / keep as author-intended / defer (→ `open-loops.md`).
Present **all** dropped facts found in the diff in a single batch, not one at a time as they surface — incremental discovery is the `^obs-015` failure mode. Non-conflicting, non-dropped writes proceed regardless.

A **state contradiction** gates like any other: if the new character state can't follow from the prior chapter's exit state without an unexplained jump (a character recorded gravely wounded last chapter now acting unhurt; a character recorded dead now on stage and alive), present the prior state + provenance, the new evidence + quote, and a recommendation (continuity error vs. intentional reveal vs. an off-page beat to note). CRE rules. Routine progression (wounds healing over time, an arc advancing) is **not** a contradiction — it just writes.

### Step 5 — Write
- `REFERENCE/story-so-far.md` — replace/insert this chapter's section (provenance-commented), keep chapters in reading order, bump `last_updated`.
- `REFERENCE/bible.md` — add new entities/facts with `(CH<N> rev<M>)` tags; replace facts previously sourced from this chapter; apply ruled conflict updates AND ruled dropped-fact archivals (the superseded or cut fact moves to the entry's `History` line, never silently deleted); bump `last_updated`.
- `REFERENCE/threads.md` — add planted threads with provenance; append advances to open threads; move paid/abandoned threads to **Settled** (History line, never deleted); fill the **Blind-read pickup** line per planted thread. Author-note lines are never overwritten.
- `<chapter>/continuity.md` — fill the **Entities / objects in play**, **Physical state**, **Knowledge state**, and **Time / place** sections with the end-state, gaps-only (author lines stay). Then fill the **Character state @ end of chapter** section (create it if the scaffold predates this section) with one entry per on-stage character — `physical` / `mental` / `arc_position` / `relationships` / `key decision`, inferred values tagged `<<UNCERTAIN>>`. Leave **Dropped-by-synthesis** strictly alone — that section belongs to the Transcoder. Bump `last_updated`.
- `REFERENCE/arcs.md` — for each tracked character: write the **entry state** once (at first appearance; never overwrite it on re-sync); append a **waypoint** for this chapter only if it's a flagged turn (don't append a waypoint every chapter — that's what the per-chapter `continuity.md` blocks are for); always overwrite the **exit state (current)** to this chapter's end-state. Each line carries `(CH<N> rev<M>)` provenance; re-syncing this chapter replaces only its own entries. Create `arcs.md` from the scaffold template if missing. Bump `last_updated`.

> **Idempotency for character state.** Like bible facts, every `arcs.md` waypoint/exit line and every `continuity.md` character-state entry is provenance-tagged to its chapter. Re-running canon-sync on chapter N replaces N's waypoint and rewrites the exit state from N forward; it never touches another chapter's entry state or waypoints. Entry state is write-once — a re-sync confirms it, never rewrites it (an entry-state change is a contradiction → gate it).

---

### Step 6 — Log

Append (newest at top), matching the house format:

- **`<chapter>/changelog.md`** — chapter synced, provenance tag, counts: facts added / replaced, threads touched, **character-state entries written, arcs.md entry/waypoint/exit updates**, conflicts ruled / deferred.
- **vault `_CHANGELOG.md`** — `## YYYY-MM-DD — [fiction] canon-sync on <chapter>` with **Ran / Shipped / Open loops** lines.

File anything fragile (a state contradiction suggesting drift, a bible or arcs section getting unwieldy, a stale REFERENCE doc you had to rebuild) to `_OBSERVATIONS.md` with a `^obs-NNN` anchor.

---

## Files this skill writes — and the ones it must not

**Writes:**
- `REFERENCE/story-so-far.md`, `REFERENCE/bible.md`, `REFERENCE/threads.md`, `REFERENCE/arcs.md` — the rolling project state.
- `<chapter>/continuity.md` — end-state + **Character state @ end of chapter** sections, gaps-only.
- `<chapter>/open-loops.md` — deferred conflict rulings only.
- `<chapter>/changelog.md`, vault `_CHANGELOG.md`, `_OBSERVATIONS.md` — logs.

**Must NOT write or alter:**
- `draft.md`, anything in `slate/`, `revisions/`, or `spec-check/` — you derive from them, never into them.
- `envelope.md`, `brief.md`, `_status.md`, the dictation files, `REFERENCE/register.md`, `REFERENCE/spec-check.md`.

---

## Stop conditions

- Vault sentinel fails → halt, ask which folder is the vault.
- No `draft.md`, or the draft is a scaffold → halt; nothing landed to sync.
- Draft status is pre-register and the author didn't ask for a mid-pipeline sync → pause, confirm.
- A conflict ruling is pending (fact, dropped fact, or **state contradiction**) → hold the dependent writes; everything non-conflicting still lands.

---

## What this skill is NOT

- Not a reviser. It records what the text establishes; improving the text is `register-pass`.
- Not a promoter. Moving a revision into `draft.md` is `promote-revision` — this runs *after* that.
- Not the Transcoder's continuity log. `Dropped-by-synthesis` entries belong to the slate run that dropped them.
- Not a planner. It records the arc the prose *realizes*, chapter by chapter; it does not design or prescribe a character's arc ahead of the writing.
- Not a judge. Conflicts between draft and canon — including state contradictions — are the author's to rule, always.

---

_Canonical reference for this skill lives at [[WORKFLOWS/canon-sync]]. Per [[_SKILLS MAP#Cowork skills]], procedure changes land in the workflow doc first, then propagate to `SKILLS/canon-sync.skill` via skill-creator._