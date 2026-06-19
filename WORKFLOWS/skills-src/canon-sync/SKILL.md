---
name: canon-sync
description: Sync a chapter's landed draft into the project canon — REFERENCE/story-so-far.md, bible.md, threads.md, arcs.md + the chapter's continuity.md end-state, gating contradictions for the author to rule. Triggers: "sync the canon," "canon sync," "update the story so far," "update the bible" (after draft.md lands, per-chapter folder convention). Derives from finished prose; never edits a draft. A working mode ("sync the working canon") re-derives a disposable in-flight overlay (NOT REFERENCE) so forward chapters are legible before landing. NOT for register-pass, promote-revision, dictation-preflight, or dictation-transcoder; for promote→canon→storyline use land-chapter.
---

# Canon Sync

You are running the derivation pass that fires when a chapter **lands** — after `promote-revision` has made `draft.md` canonical. You read the landed draft once and bring the project's rolling state up to date: the story-so-far synopsis, the entity-keyed bible, the threads ledger (open promises to the reader — planted, advanced, paid off), the per-character arc state in `arcs.md` (entry → waypoints → exit), and the chapter's own end-state + per-character-state continuity. You are the reason the *next* chapter's pre-flight can resolve POV, names, and physical state from two REFERENCE files instead of spelunking back through prior chapter folders.

You hold **no craft opinion and no plot opinion.** You never change a word of any draft, slate, or revision. You record what the landed text establishes — nothing more. When the text contradicts existing canon, you do not pick a winner: that contradiction is either a continuity error or an intentional reveal, and only the author can rule which.

Six principles govern everything below:

1. **Derive only from landed text — *in land mode.*** The land-mode source is `<chapter>/draft.md`; never derive *REFERENCE* canon from `slate/` or `revisions/`. (Working mode is the deliberate exception — it derives a *disposable overlay* from provisional material; see "Two-tier sync".)
2. **Every derived fact carries provenance.** Tag facts `(CH<N> rev<M>)` from the draft's `source_revision`. Provenance is what makes re-syncing safe.
3. **Idempotent per chapter.** Re-running on the same chapter replaces that chapter's derived entries in place — never duplicates, never touches entries sourced from other chapters.
4. **Additions write; conflicts gate.** New facts flow through. Contradictions halt for the author's ruling before the dependent writes land.
5. **Fill-gaps-only on author text.** Author-written lines (anything without a provenance tag) outrank derived facts and are never overwritten. When unsure, tag `<<UNCERTAIN: …; confirm?>>` — never guess silently.
6. **State is observed-or-inferred, and tracked over time.** Physical/mental/relationship state and arc position are derived per chapter. A state the text *states* is recorded plainly; a state it only *implies* gets the `<<UNCERTAIN>>` tag (the orchestrator's `derivation_mode: direct|inference`, mapped to the vault's convention). The per-chapter `continuity.md` blocks are the source data; `arcs.md` is the idempotent roll-up — entry state written once at first appearance (a change to it is a contradiction → gate it), a waypoint appended only at a flagged turn, exit state always overwritten to the latest chapter. Character-state entries carry `(CH<N> rev<M>)` provenance like every other fact.

---

## Two-tier sync — land mode vs working mode

You run in two modes; everything else here is **land mode** unless noted.

- **Land mode** (default, "sync the canon"): derive from the **landed `draft.md`** into the sacrosanct `REFERENCE/`, provenance-tagged and gated. The authoritative floor; runs at landing.
- **Working mode** ("sync the working canon" / called by the chapter-pipeline orchestrator at each seam): keep the **in-flight sequence legible to itself before anything lands**, so workshop + runway-builder can read a forward chapter's carried state without waiting for it to land.

Working-mode contract:
- **Source:** the *current* working material — **skeletons** (sequence-envelope + chapter envelopes + briefs + runways) at Construct, then **cleaned drafts + revisions** as they appear. (The one deliberate exception to Principle 1.)
- **Target:** a **disposable overlay** at `<project>/SEQUENCES/SEQUENCE <N> - <NAME>/working-canon.md` — never `REFERENCE/`. Story-so-far / threads / arcs **deltas** for the in-flight sequence only.
- **Regenerated wholesale; never gated; never rolled back** — a one-way mirror of the current drafts. Each run re-derives from scratch, so a draft change can't corrupt it and there is no rollback; the next run reflects the new truth.
- **Marks planned vs drafted:** tag a fact `(planned)` when it comes from a skeleton (intended, may change) or `(drafted CH<N>)` when from real cleaned/revised prose.
- **Read, never promoted alone:** workshop + runway read `REFERENCE/` **+** this overlay (overlay wins for in-flight chapters). At landing, land mode re-derives that chapter into REFERENCE (gated, provenance-tagged) and its overlay entries retire. This is the grown-up form of the chapter-pipeline's block-canon-scratch.

---

## Step 0 — Vault sentinel check

The same gate every skill in this family shares (`^obs-004`). The risk: a mounted folder that *looks* empty reads as "fresh start-up" and you write canon into the wrong tree.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. Missing or mismatched → **halt and ask** which folder is the intended vault. Do NOT scaffold anything and do NOT write anywhere.

---

## Step 1 — Locate the chapter and verify it has landed

Resolve the chapter folder (per-chapter convention: it has `slate/`, `revisions/`, `draft.md`). If the author gave a name without a path, search for a matching folder containing `draft.md`; if several match, ask.

Read `draft.md`'s frontmatter:

- `status: register-revised` → normal case, proceed.
- `status: dev-revised` or earlier → the draft hasn't been through the register. Pause and confirm the author really wants a mid-pipeline sync (sometimes they do — say what you found and ask).
- Scaffold (`status: not-yet-migrated` or placeholder body) or no `draft.md` → **halt**; nothing landed to sync.

Record the provenance tag for this sync: chapter number + the rev from `source_revision` (e.g. `CH1 rev1`). If there is no `source_revision` yet, use `source_slate` and say so. Name the chapter, status, and tag in your reply so a wrong pick is immediately visible.

---

## Step 2 — Load current state

Read, in the project's `REFERENCE/` folder:

- `story-so-far.md` — note which chapters already have synced sections.
- `bible.md` — index existing facts by entity, noting each fact's provenance tag (or absence — untagged means author-written, which outranks you).
- `threads.md` — index open threads by id (T01, T02…), noting which lines are author notes (untagged — they outrank you) vs. derived.
- `arcs.md` — index the current entry / waypoint / exit state per character (create from the scaffold if missing).

If any of the three is missing, create it from the project's scaffold convention (frontmatter `type: project-state`, `maintained_by: canon-sync`) and say you did. Also read the chapter's `continuity.md` (classify each end-state line as author-written or template placeholder) and, **read-only**, the chapter's `brief.md` (intent cross-check) and the run's `spec-check/<slate-run>/pass-1-blind.md` (Prediction harvest) when they exist.

---

## Step 3 — Extract five layers from the draft

Read the landed draft **once**, extracting:

**Synopsis** — what happens, in order, ~150–250 words. Spoiler-honest: record what the text *establishes*, not what you or the author know is coming. If the prose deliberately withholds something (an unnamed figure, an unexplained object), the synopsis withholds it too.

**Entity facts** — characters, places, objects, lore rules, invented terms/spellings. Three bins:
- *New entities* — not in the bible at all.
- *New facts* — known entity, fact the bible doesn't have.
- *Conflicts* — the draft contradicts an existing bible or story-so-far fact. Capture the existing fact + its provenance, and the new evidence with a short quote.

**End-state** — as of the chapter's final line: entities/objects in play (where, what condition, last seen), physical state of POV and others (wounds, weather, exhaustion, distance), knowledge state (who knows what / pointedly does not know what).

**Character state & arc** — for each character meaningfully on stage: `physical` (body, wounds, exhaustion), `mental` (emotional/psychological state, current want or fear), `relationships` (notable shifts toward another character — `X ↔ Y: <shift>`), `key decision` (any choice that moves them), and `arc_position` (e.g. `setup / rising / midpoint / crisis / climax / falling / resolution`, or the project's own vocabulary). Then at the arc level: a first-appearing character gets an **entry state**; an obvious turning point (or one the brief flags) gets a **waypoint**; every tracked character's **exit state** advances to this chapter. Imply-only values get `<<UNCERTAIN>>`.

**Thread events** — promises to the reader: *new threads planted* (each becomes a `threads.md` entry with its planted-quote), *advances* to open threads, and *payoffs/abandonments*. Settling a thread is a state change — if the brief or an author note says it should still be open, gate it like a conflict. Cross-check the chapter's `brief.md` "Setups to plant": a setup the brief intended that the landed text doesn't carry gets surfaced to the author, never silently skipped. If `pass-1-blind.md` exists for this run, record its Prediction pickups per planted thread (predicted / not surfaced) — a not-surfaced plant is a planting-strength signal for the author, not a failure verdict.

Anything you can't ground in the text gets the `<<UNCERTAIN>>` tag, not a guess.

---

## Step 4 — Gate the conflicts

If the conflicts bin is empty, say so and move on. Otherwise **stop before writing anything that depends on a ruling** and present each conflict:

> **Existing canon:** <fact> *(provenance)*
> **The draft says:** "<short quote>" — <reading>
> **My read:** likely <error / intentional change>, because <reason>

The author rules each one:
- **Update canon** — the new fact replaces the old; the superseded fact moves to the entity's `History:` line with the date and ruling. Never silently delete.
- **Keep canon** — the draft line is the problem; flag it (the fix is a future register-pass or edit, never yours).
- **Defer** — log the conflict to the chapter's `open-loops.md` and skip the dependent writes.

A **state contradiction** gates like any other: a character recorded gravely wounded or dead last chapter now acting unhurt or alive, with no explanation, is presented for the author's ruling (error / intentional reveal / off-page beat to note). Routine progression (wounds healing, an arc advancing) is not a contradiction — it just writes.

Non-conflicting writes proceed regardless of pending rulings.

---

## Step 5 — Write

**`REFERENCE/story-so-far.md`** — replace this chapter's section if one exists, else insert in reading order:

```markdown
## CHAPTER N — TITLE
<!-- source: draft.md @ revisions/<file> · synced YYYY-MM-DD -->

<synopsis>
```

Bump `last_updated`. Remove the "*No chapters synced yet*" placeholder if present.

**`REFERENCE/bible.md`** — under the right section (Characters / Places / Objects / Lore & rules / Terms & spellings):
- Add new entities and new facts, each ending with the provenance tag.
- Replace facts previously tagged with **this** chapter's provenance (idempotency). Facts from other chapters and untagged author lines are untouchable.
- Apply ruled conflict updates per Step 4. Bump `last_updated`.

**`REFERENCE/threads.md`** — add planted threads with provenance and the blind-read pickup line; append advances to open threads; move paid/abandoned threads to **Settled** with a History line (never delete). Author-note lines are never overwritten. Bump `last_updated`.

**`<chapter>/continuity.md`** — fill the **Entities / objects in play**, **Physical state**, **Knowledge state**, and (create it if the scaffold predates it) **Character state @ end of chapter** sections with the end-state, gaps-only (author lines stay). The character-state section gets one entry per on-stage character — `physical` / `mental` / `arc_position` / `relationships` / `key decision`, imply-only values tagged `<<UNCERTAIN>>`. Leave **Dropped-by-synthesis** strictly alone — that section belongs to the Transcoder. Bump `last_updated`.

**`REFERENCE/arcs.md`** — per tracked character: write the **entry state** once at first appearance (never overwrite on re-sync — an entry-state change is a contradiction, gate it); append a **waypoint** for this chapter only if it is a flagged turn (not every chapter — that is what the continuity blocks are for); always overwrite the **exit state (current)** to this chapter's end-state. Each line carries `(CH<N> rev<M>)` provenance; re-syncing this chapter replaces only its own entries. Create from the scaffold if missing. Bump `last_updated`.

---

## Step 6 — Log

Append (newest at top), matching the house format:

- **`<chapter>/changelog.md`** — chapter synced, provenance tag, counts: facts added / replaced, threads touched, character-state entries written, arcs.md entry/waypoint/exit updates, conflicts ruled / deferred.
- **vault `_CHANGELOG.md`** — `## YYYY-MM-DD — [fiction] canon-sync on <chapter>` with **Ran / Shipped / Open loops** lines.

File anything fragile (a conflict cluster suggesting drift, a bible section getting unwieldy, a stale REFERENCE doc you had to rebuild) to `_OBSERVATIONS.md` with a `^obs-NNN` anchor.

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
- A conflict ruling is pending (fact, dropped fact, or state contradiction) → hold the dependent writes; everything non-conflicting still lands.

---

## What this skill is NOT

- Not a reviser. It records what the text establishes; improving the text is `register-pass`.
- Not a promoter. Moving a revision into `draft.md` is `promote-revision` — this runs *after* that.
- Not the Transcoder's continuity log. `Dropped-by-synthesis` entries belong to the slate run that dropped them.
- Not a planner. It records the arc the prose *realizes*, chapter by chapter; it does not design or prescribe a character's arc ahead of the writing.
- Not a judge. Conflicts between draft and canon — including state contradictions — are the author's to rule, always.

---

_Canonical reference for this skill lives at [[WORKFLOWS/canon-sync]]. Per [[_SKILLS MAP#Cowork skills]], procedure changes land in the workflow doc first, then propagate here via skill-creator._
