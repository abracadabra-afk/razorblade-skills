---
type: workflow
name: book-ingest
trigger: ingest the book
aliases: [ingest chapter N, ingest this book, book ingest, ingest the next chapter, ingest published book]
inputs: [a published book's per-chapter prose files (the ingest source), the target project root under WRITING/PROJECTS/<PROJECT>/, REFERENCE/ (created on first chapter), the scene-intensity engine, the target StoryLine project under WRITING/STORYLINE/<Project>/]
outputs: [a per-chapter folder (ingested-published variant) with draft.md = published prose (status: ingested), derived REFERENCE state, the chapter continuity end-state, a StoryLine scene+codex mirror, an ingest-run report]
lane: fiction
status: active
last_updated: 2026-06-29
scope: Published, already-finished books that were NOT produced through the dictation pipeline, being brought into the per-chapter folder convention so the continuity/canon and StoryLine workflows can run on them. First adopter — GHOST RIVER (First Edition).
pipeline_position: A front-door variant of [[WORKFLOWS/chapter-init]]. chapter-init scaffolds an EMPTY chapter for dictation; book-ingest scaffolds a chapter whose draft.md is the finished published prose, entering at the LANDED stage. After scaffolding it chains the existing derive passes — [[WORKFLOWS/canon-sync]] then [[WORKFLOWS/storyline-sync]] — unchanged. The `^obs-023` finding: a published book needs only a new scaffolder; the derive passes already accept `status: ingested` as a landed state.
---

# WORKFLOW: book-ingest (ingest a published book)

> Brings an **already-published, non-dictated** book into the vault's per-chapter pipeline AND its StoryLine mirror, one chapter at a time. The book has no dictation → slate → revision lineage, so each chapter enters at the **landed** stage: the published prose drops straight into `draft.md` with a terminal `status: ingested`, and the dictation-side files are marked N/A. From there the existing derive passes run unchanged.

## When to use

A finished, published (or otherwise final, non-dictated) manuscript needs to be usable by canon-sync / storyline-sync / continuity. Trigger phrases: "ingest the book," "ingest chapter N," "ingest the next chapter." Do NOT use it to scaffold a new chapter for dictation (that is [[WORKFLOWS/chapter-init]]), to slate dictation ([[WORKFLOWS/transcoder]]), or to revise prose ([[WORKFLOWS/register-pass]]). It never writes or alters prose — it copies the published text verbatim and derives state from it.

## Key principles

1. **The published prose is canonical and immutable.** `draft.md` is the published text copied byte-for-byte from the ingest source. Never rewrite, clean, or "improve" it.
2. **Never reverse-derive authorial intent.** `brief.md` (forward intent) and `envelope.md` (perceptual envelope) do not exist for a published work and are left as **N/A stubs**. Inferring a brief from finished prose is AI-authored intent, which violates "AI executes, CRE creates." (CRE may author a brief by hand later to enable spec-check on a chapter.)
3. **Provenance is `(CH<N> ingested)`** — not `(CH<N> rev<M>)`, since there is no revision lineage. Re-running on a chapter replaces exactly that chapter's `ingested`-tagged facts (idempotent, same as canon-sync).
4. **Additions write; contradictions gate — and when unattended, defer, never guess.** canon-sync writes non-conflicting facts automatically. A contradiction with already-ingested canon is logged to the chapter's `open-loops.md` and the run report for CRE to rule later; the run continues. (Matches the scheduled-task "produce a report" convention.)
5. **One chapter per run** is the default cadence (smallest blast radius, each run self-tests via Step 6). A run does exactly one chapter unless told otherwise.

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch/missing → halt and ask which folder is the vault.

### Step 1 — Resolve project + select the next chapter
- **Project**: the target project root under `WRITING/PROJECTS/<PROJECT>/` (e.g. `GHOST RIVER`). If ambiguous, ask.
- **Ingest source**: the project's published per-chapter prose (for GHOST RIVER: `WRITING/PROJECTS/GHOST RIVER (FIRST ED)/Chapters/Chapter <N>.md` — **First Edition only**, per CRE 2026-06-10; the Second-Ed/Series materials are NOT ingested).
- **Next chapter** = the lowest-numbered source chapter that does NOT yet have a `CHAPTERS/CHAPTER <N>/` folder with a landed `draft.md`. If every source chapter is ingested → **report "ingest complete"** and stop (the scheduled runner uses this to self-terminate).
- **On-entry temp sweep (`^obs-027` / `^ingest-selftest-harden`):** once the project resolves and its `REFERENCE/` exists, sweep and delete any stranded atomic-write orphans matching the temp glob `REFERENCE/*.tmp.*` **via the Obsidian/vault API** — never bash `rm`, which a Dropbox file-lock blocks (`^obs-027`). These accrete from interrupted canon-sync / storyline-sync atomic writes; left in place they litter the project root and can confound the Step 5 parse / word-count checks. Scope the delete **strictly** to the interrupted-write pattern (`*.tmp.<digits>.*`) — never a live `.md` source-of-truth file; if a candidate does not match that pattern, leave it and flag it in the run report rather than guessing.

### Step 2 — Scaffold the chapter folder (ingested-published variant)
Create `CHAPTERS/CHAPTER <N>/` with the full convention, every file stamped `chapter: CHAPTER <N>`, `project: <PROJECT>`:
- `draft.md` — frontmatter (`type: chapter-draft`, `status: ingested`, `source:` pointing at the ingest file, an `ingest_note`, `last_updated`) followed by the published prose **verbatim** (assemble as frontmatter + raw source bytes; do not reflow).
- `brief.md`, `envelope.md` — **N/A stubs** (`status: not-applicable`).
- `dictation/README.md`, `slate/README.md`, `revisions/README.md` — N/A notes.
- `_status.md`, `changelog.md`, `notes.md`, `open-loops.md`, `continuity.md` — scaffolds (continuity end-state filled in Step 3).
- **First chapter only:** create `REFERENCE/bible.md`, `REFERENCE/threads.md`, `REFERENCE/story-so-far.md` scaffolds, `REFERENCE/intensity_config.json` (engine defaults; flag uncalibrated), and a project `README.md` documenting the ingested-published variant + the `(CH<N> ingested)` convention + an ingest-status table.
- Never overwrite an existing `CHAPTER <N>/` (halt if present). Use the bundled `scaffold_ingest.py` for determinism where available.
- **Valid-YAML guard (`^obs-026`):** the `draft.md` frontmatter must parse as YAML. Any value containing `: ` (colon-space) or backticks — notably `ingest_note`, which mentions `` `status: ingested` `` — MUST be double-quoted, or the whole frontmatter is invalid and downstream YAML parsers choke. The bundled script now emits frontmatter via `yaml.safe_dump`; a hand-written frontmatter must quote those values. **Write `draft.md` atomically and confirm via the file tools (not a bash read) that it ends at the last prose line with no trailing NUL bytes** — the prior CH2 run left NUL-padded truncation (`^obs-027`).

### Step 3 — canon-sync (provenance `CH<N> ingested`)
Run [[WORKFLOWS/canon-sync]] against the landed `draft.md`, treating `status: ingested` as a landed state. Derive `REFERENCE/bible.md` (entities/facts), `REFERENCE/threads.md` (open promises), `REFERENCE/story-so-far.md` (this chapter's synopsis section), and the chapter's `continuity.md` end-state. Tag every derived fact `(CH<N> ingested)`. Additions write; **contradictions and `<<UNCERTAIN>>` items are deferred to `open-loops.md` + the run report — never guessed** (unattended rule, principle 4). Diff against this chapter's prior `ingested`-tagged facts on re-runs (drop stranded facts — the `^obs-015` discipline).

### Step 4 — storyline-sync
Run [[WORKFLOWS/storyline-sync]] into `WRITING/STORYLINE/<Project>/`. Segment scenes on hard scene-breaks (`***`); **actually run the scene-intensity engine** (never eyeball `si_*`) using `REFERENCE/intensity_config.json`; write one scene file per scene (native `intensity = round(si_local/10)` + `arc_valence` + the `si_*` block, all flagged inferred) and create/update Codex entries (Characters, Locations, Items, Lore) from `bible.md`, idempotent and spoiler-clean. StoryLine self-manages Plotlines / Codex categories / Plot Grid — write none of them (`^obs-017`).

### Step 5 — Verify (the self-test)
**Read every file under test through the file tools / a fresh handle — never the bash mount (`^obs-014` / `^obs-027`).** The Dropbox-synced bash mount serves stale partials mid-sync: on the CH2 run it both *missed* a real NUL-padded `draft.md` truncation and *hallucinated* a phantom truncation in unrelated meta — so a mount read of the just-written files is not a valid self-test (and is the same stale-partial class DIR-005 bans for the brain docs). Re-open each written file via the file tools (or a fresh handle that bypasses any cached mount view), then programmatically parse its YAML and confirm: all frontmatter loads; every scene `characters`/`location` wikilink resolves to a real codex file; `sequence` numbers unique; `intensity == round(si_local/10)` and the `si_*` block is present; **`draft.md` ends at the last prose line with no trailing NUL bytes** and its word count matches the source. Report a PASS/FAIL table. FAIL → halt that chapter, leave it flagged in the report, do not log it as done.

### Step 6 — Log
Append to: the chapter `changelog.md`; the project `README.md` ingest-status table (mark CH<N> done across all three columns); the vault [[_CHANGELOG]] (fiction lane). File any deferred conflicts/UNCERTAINs to the chapter `open-loops.md` and surface them in the run report. File fragilities to [[_OBSERVATIONS]]; add follow-ups to [[_BACKLOG]] if warranted.

### Step 7 — Report (and self-terminate signal)
Emit a one-chapter run report: which chapter ingested, scenes + codex written, intensity contour, verify result, and any deferred conflicts/UNCERTAINs for CRE. If Step 1 found no remaining chapters, the report says **"ingest complete — all chapters done"**, which the scheduled runner treats as its stop signal.

---

## Notes

- **GHOST RIVER specifics:** ingest source = First Edition `Chapters/Chapter <N>.md` (20 chapters, untitled → numeric folder names `CHAPTER <N>`). Second-Ed/Series materials are not ingested. `intensity_config.json` is uncalibrated (engine defaults; GR's horror register likely runs hotter than the Witchwood calibration — see `^obs-024`).
- **StoryLine display:** the Items + Lore Codex categories must be enabled in StoryLine's global Codex settings (`data.json codexEnabledCategories`) for those entries to show; this workflow verifies-and-warns, never writes that global setting.
- **Relationship to chapter-init:** this is its published-book sibling. If a chapter is to be *revised* after ingest, that work lands in `revisions/` and flips `draft.md` off `status: ingested` — at which point it rejoins the normal pipeline.
