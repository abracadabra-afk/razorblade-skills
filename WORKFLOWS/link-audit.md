---
type: workflow
name: link-audit
trigger: run the link doctor
aliases: [check for broken links, audit the links, find dangling links, find broken references, link audit, reference doctor]
inputs: [the mounted vault root]
outputs: [a categorized punch list of dangling links / broken anchors / broken headings; optional brain-log entries]
lane: meta
status: active
last_updated: 2026-06-14
---

# WORKFLOW: link-audit (the link doctor)

## When to use
CRE says **"run the link doctor"** / "check for broken links" / "find dangling references," or wants the vault swept for reference rot — especially **after a restructure or a batch of moves**. The reference sibling of `skill-audit` (skills) and `backlog-sweep` (the backlog): **read-only**, it diagnoses and hands CRE a fix list; it never edits a note.

## What it checks
Scans every note for `[[wikilinks]]`, `![[embeds]]`, and `[md](links)` and resolves each against the real file index, plus heading/block-anchor indices. Reports four kinds:
- **DANGLING** — target file not found anywhere.
- **BROKEN-ANCHOR** — file resolves, but the `^block-id` doesn't exist in it.
- **BROKEN-HEADING** — file resolves, but the `#heading` doesn't exist in it.
- **AMBIGUOUS** (info, off by default) — a basename matches >1 file and none in the same folder; Obsidian still resolves to the shortest path, so this is low-priority.

## Resolution rules (matches Obsidian)
- Bare `[[Note]]` resolves by **basename**, with a **folder-proximity tie-break** (a same-folder match wins — so `[[open-loops]]` resolves to the sibling, not a random chapter's).
- `[[folder/Note]]` resolves by path. Case-insensitive (matches the Dropbox/Windows filesystem).
- Links inside inline code or fenced code blocks are **ignored** (so `` `[[wikilinks]]` `` examples in docs don't false-flag).
- `#heading` / `#^block` fragments are checked only when the target file is readable.

## Steps
1. **Vault sentinel** — confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`); the `^obs-004` guard. Write nothing.
2. **Run** the bundled resolver: `python3 link_audit.py --vault <VAULT>` (add `--all` to include the quarantined zones, `--ambiguous` to show the info tier, `--json` for machine output).
3. **Apply the `^obs-014` guard** — a flagged-missing file can be a stale-mount artifact. **Run in a FRESH session**, and confirm any surprising DANGLING via the file tools (or the Obsidian MCP) before reporting it as real. The in-session bash mount serves stale views of files moved/deleted that session.
4. **Categorize, don't dump.** Separate the punch list into: genuine breakage (fix), the vault's **folder-link convention** (links pointing at folders rather than notes — pre-existing style, not breakage), and resolver-soft cases (heading-fragment near-misses). Present the actionable list; quarantine GRAVEYARD / `evals/` / `_CHANGELOG` / `_OBSERVATIONS` noise.
5. **Hand off.** Fixes are manual or a separate pass — this skill never edits a note.

## Quarantine (reported separately, `--all` to show)
`GRAVEYARD/`, `WORKFLOWS/evals/`, `_CHANGELOG.md`, `_OBSERVATIONS.md`, the migration plan, and backup files — dangling references there are expected (cold storage / historical record).

## Stop conditions
- Sentinel fails → halt, ask which folder is the vault.
- Zero findings → report "no broken references," stop.

## Logging
If run as a real session (not an incidental check), append a one-line `_CHANGELOG` entry (meta lane) noting the finding count; file any new fragility to `_OBSERVATIONS`.
