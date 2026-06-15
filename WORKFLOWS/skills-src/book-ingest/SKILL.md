---
name: book-ingest
description: Ingest an already-published, non-dictated book into the per-chapter folder convention AND its StoryLine mirror, one chapter at a time — drop the published prose verbatim into draft.md (status: ingested), N/A-stub the dictation-side files, then chain canon-sync and storyline-sync. Use when the author asks to "ingest the book," "ingest chapter N," "ingest the next chapter," or to bring a finished/published manuscript (e.g. Ghost River First Edition) into the vault so the continuity/canon and StoryLine workflows can run on it. It is the published-book sibling of chapter-init (which scaffolds an EMPTY chapter for dictation): book-ingest scaffolds a chapter whose draft.md is the finished prose, entering at the LANDED stage with (CH N ingested) provenance. Do NOT use it to scaffold a new chapter for dictation (chapter-init), slate dictation (dictation-transcoder), revise prose (register-pass), or to rewrite/clean/reverse-derive the published text — it copies prose verbatim and only derives state from it.
---

# Book Ingest

Bring an **already-published, non-dictated** book into the vault's per-chapter pipeline and its StoryLine mirror, **one chapter per invocation**. The book has no dictation → slate → revision lineage, so each chapter enters at the **landed** stage: the published prose drops straight into `draft.md` with a terminal `status: ingested`, the dictation-side files are marked N/A, and the existing derive passes (canon-sync, storyline-sync) run unchanged. Canonical procedure: `WORKFLOWS/book-ingest.md`.

Five moves, in order: **gate → select → scaffold → derive → verify+log**.

## Key rules (load-bearing)

1. **Published prose is canonical and immutable.** `draft.md` is the published text copied byte-for-byte. Never rewrite, clean, reflow, or "improve" it.
2. **Never reverse-derive intent.** `brief.md` / `envelope.md` are **N/A stubs** — inferring authorial intent from finished prose violates "AI executes, CRE creates." (CRE may author a brief by hand later to enable spec-check.)
3. **Provenance is `(CH<N> ingested)`** — no revision lineage. Re-running a chapter replaces exactly that chapter's `ingested`-tagged facts (idempotent).
4. **Additions write; contradictions gate.** When unattended, a contradiction with existing canon (or any `<<UNCERTAIN>>`) is **deferred** to the chapter's `open-loops.md` + the run report — never guessed.
5. **One chapter per invocation** by default.

## Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch/missing → halt and ask which folder is the vault.

## Step 1 — Resolve project + select the next chapter
Project root is `WRITING/PROJECTS/<PROJECT>/` (ask if ambiguous). The ingest source is the published per-chapter prose (for GHOST RIVER: `GHOST RIVER (FIRST ED)/Chapters/Chapter <N>.md` — **First Edition only**; Second-Ed/Series materials are NOT ingested). The **next chapter** is the lowest-numbered source chapter without a `CHAPTERS/CHAPTER <N>/draft.md`. If all are ingested → report "ingest complete" and stop.

## Step 2 — Scaffold (use the bundled script)
Run `scripts/scaffold_ingest.py --project-root "<PROJECT_ROOT>" --n <N> --source "<CHAPTER_MD>"`. It writes `draft.md` (frontmatter + verbatim prose, `status: ingested`), N/A stubs for brief/envelope/dictation/slate/revisions, scaffolds the meta files, and — on the first chapter only — creates `REFERENCE/` (bible/threads/story-so-far + intensity_config.json) and the project `README.md` ingest table. It refuses to overwrite an existing chapter folder.

## Step 3 — Derive (chain the existing skills)
- **canon-sync** against the landed `draft.md`, provenance `(CH<N> ingested)` → `REFERENCE/bible.md` + `threads.md` + `story-so-far.md` + the chapter `continuity.md` end-state. Additions write; conflicts/UNCERTAINs defer to `open-loops.md` + report.
- **storyline-sync** into `WRITING/STORYLINE/<Project>/` → segment scenes on `***`, **actually run the scene-intensity engine** (config `REFERENCE/intensity_config.json`; never eyeball `si_*`), write scene files + Codex (Characters/Locations/Items/Lore). StoryLine self-manages Plotlines / Codex categories / Plot Grid — write none.

## Step 4 — Verify (self-test)
Parse all written YAML; confirm every scene `characters`/`location` wikilink resolves, `sequence` numbers are unique, `intensity == round(si_local/10)` with the `si_*` block present, and `draft.md` word count matches the source. FAIL → halt that chapter, flag it in the report, do not log it done.

## Step 5 — Log + report
Append to the chapter `changelog.md`, the project `README.md` ingest table, and the vault `_CHANGELOG.md` (fiction lane). File fragilities to `_OBSERVATIONS.md`. Report: chapter ingested, scene + codex counts, intensity contour, verify result, deferred conflicts/UNCERTAINs.

## Notes
- GHOST RIVER: First-Ed only; untitled chapters → numeric folder names `CHAPTER <N>`; `intensity_config.json` uncalibrated (engine defaults; horror register likely runs hotter — `^obs-024`).
- StoryLine display: Items + Lore Codex categories must be enabled in StoryLine's global `data.json codexEnabledCategories`; this skill verifies-and-warns, never writes that global setting (`^obs-017`).
- Edit with the file tools, not `patch_vault_file`; verify writes with the file tools (`^obs-020`/`^obs-014`).
