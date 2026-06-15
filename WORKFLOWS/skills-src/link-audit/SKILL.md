---
name: link-audit
description: Audit an Obsidian vault for broken references - dangling [[wikilinks]], ![[embeds]] and [md](links), plus broken #headings and ^block-anchors - and print a categorized punch list. Use when CRE asks to "run the link doctor", "check for broken links", "audit the links", "find dangling links/references", "are there broken wikilinks", or after a restructure/move to verify nothing dangles. Read-only - it diagnoses and hands CRE a fix list, never edits a note. Sibling of skill-audit (audits skills) and backlog-sweep. Do NOT use it to FIX links (manual/separate pass), to audit skills (skill-audit), or to sweep the backlog (backlog-sweep).
---

# Link Audit (the link doctor)

Read-only reference-integrity audit of an Obsidian vault. You scan every note's links and resolve them against the real file index, then hand CRE a categorized punch list of what's broken. You write nothing except the report (and optional brain-log entries). Canonical doc: `WORKFLOWS/link-audit.md`.

## What it reports
- **DANGLING** - target file not found anywhere.
- **BROKEN-ANCHOR** - file resolves, but the `^block-id` is missing in it.
- **BROKEN-HEADING** - file resolves, but the `#heading` is missing in it.
- **AMBIGUOUS** (info, `--ambiguous` to show) - basename matches >1 file and none in the same folder; Obsidian still resolves to the shortest path, so low-priority.
- **SUSPECT-STALE** - a target file read back **truncated** (NUL bytes / partial), so its anchor/heading set is untrustworthy; the audit downgrades any `BROKEN-ANCHOR`/`BROKEN-HEADING` off it to this advisory instead of a confident false finding, and prints a top-level "MOUNT MAY BE STALE" banner (the `^obs-073` guard).

## Step 1 - Vault sentinel
From the mounted vault root, read `_DIRECTIVES.md` and confirm its frontmatter has `type: ai-os-brain` and `file: directives` (the `^obs-004` guard). Missing/mismatched -> halt and ask which folder is the vault. Write nothing.

## Step 2 - Run the resolver
`python3 link_audit.py --vault <VAULT>`  (bundled alongside this SKILL.md).
Flags: `--all` (include quarantined zones), `--ambiguous` (show the info tier), `--json` (machine output).
It matches Obsidian's resolution: basename with **folder-proximity tie-break**, path links, case-insensitive, and it **ignores links inside code spans/fences** so doc examples like `` `[[wikilinks]]` `` don't false-flag.

## Step 3 - OBS-014 GUARD (mandatory)
A flagged-missing file can be a **stale-mount artifact** - the in-session bash mount serves **stale or truncated** views of files written/moved/deleted that session (`^obs-014`/`^obs-073`). Strongest mitigation: pass `--rest-base http://127.0.0.1:27123 --rest-key <Local REST API key>` (or env `OBSIDIAN_REST_BASE`/`OBSIDIAN_API_KEY`) so every target is read from Obsidian's **live in-memory view**, immune to the mount (falls back to disk per-file on any API error). Without the API, truncated reads self-flag as `SUSPECT-STALE`; still **run in a FRESH session** and confirm any surprising DANGLING via the file tools before reporting it as real.

## Step 4 - Categorize, don't dump
Split the list into: (a) genuine breakage to fix; (b) the vault's **folder-link convention** - links pointing at a folder rather than a note (e.g. `[[KNOWLEDGE/STYLE]]`); these show as unresolved but are pre-existing navigational style, not breakage; (c) heading-fragment near-misses (low stakes - click lands at file top). Present the actionable list first. The quarantined zones (`GRAVEYARD/`, `evals/`, `_CHANGELOG`, `_OBSERVATIONS`, migration plan, backups) are reported separately and usually ignorable.

## Step 5 - Hand off
Fixes are manual or a separate pass. Never edit a note. If run as a real session, append a one-line `_CHANGELOG` entry (meta lane) with the finding count + file new fragility to `_OBSERVATIONS`.
