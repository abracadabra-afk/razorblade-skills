---
type: workflow
name: link-audit
trigger: run the link doctor
aliases: [check for broken links, audit the links, find dangling links, find broken references, link audit, reference doctor]
inputs: [the mounted vault root]
outputs: [a categorized punch list of dangling links / broken anchors / broken headings; optional brain-log entries]
lane: meta
status: active
last_updated: 2026-08-10
---

# WORKFLOW: link-audit (the link doctor)

## When to use
CRE says **"run the link doctor"** / "check for broken links" / "find dangling references," or wants the vault swept for reference rot — especially **after a restructure or a batch of moves**. The reference sibling of `skill-audit` (skills) and `backlog-sweep` (the backlog): **read-only**, it diagnoses and hands CRE a fix list; it never edits a note.

## What it checks
Scans every note for `[[wikilinks]]`, `![[embeds]]`, and `[md](links)` and resolves each against the real file index, plus heading/block-anchor indices. Reports five kinds:
- **DANGLING** — target file not found anywhere.
- **BROKEN-ANCHOR** — file resolves, but the `^block-id` doesn't exist in it.
- **BROKEN-HEADING** — file resolves, but the `#heading` doesn't exist in it.
- **AMBIGUOUS** (info, off by default) — a basename matches >1 file and none in the same folder; Obsidian still resolves to the shortest path, so this is low-priority.
- **SUSPECT-STALE** — a target file read back **truncated** (NUL bytes / partial), so its anchor/heading index can't be trusted; any `BROKEN-ANCHOR`/`BROKEN-HEADING` off it is downgraded to this advisory instead of a confident false finding, and the run prints a top-level "MOUNT MAY BE STALE" banner. The `^obs-073` guard.

## Resolution rules (matches Obsidian)
- Bare `[[Note]]` resolves by **basename**, with a **folder-proximity tie-break** (a same-folder match wins — so `[[open-loops]]` resolves to the sibling, not a random chapter's).
- `[[folder/Note]]` resolves by path. Case-insensitive (matches the Dropbox/Windows filesystem).
- Links inside inline code or fenced code blocks are **ignored** (so `` `[[wikilinks]]` `` examples in docs don't false-flag).
- `#heading` / `#^block` fragments are checked only when the target file is readable.

## Steps
1. **Vault sentinel** — confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`); the `^obs-004` guard. Write nothing.
2. **Run** the bundled resolver: `python3 link_audit.py --vault <VAULT>` (add `--all` to include the quarantined zones, `--ambiguous` to show the info tier, `--json` for machine output).

   > ⚠️ **The `--rest-base` / `--rest-key` path is RETIRED (corrected 2026-08-03).** This step used to recommend reading targets through Obsidian's Local REST API for freshness. **That plugin was removed from the vault on 2026-07-13** under DIR-001 — its `data.json` held a 64-char `apiKey` granting full read/write over the vault plus a TLS private key, and removal (not rotation) was the ruled fix, since `CLAUDE.md` makes the file tools the default read path. **Do not pass `--rest-base`/`--rest-key`, do not set `OBSIDIAN_REST_BASE`/`OBSIDIAN_API_KEY`, and never go looking for that key** — retrieving it would re-introduce the exact secret DIR-001 had removed. The flags remain in the script for a future sanctioned freshness source; they have no live backend today.
   >
   > **The freshness mitigation is therefore Step 3 alone**: `SUSPECT-STALE` self-flagging, a fresh session, and file-tool confirmation of any surprising DANGLING before it is reported as real. Treat mount staleness as *present and unmitigated*, not solved.
3. **Apply the `^obs-014`/`^obs-073` guard** — a flagged-missing file can be a stale-mount artifact, and a recently-written file can read back **truncated** (the bash mount serves stale/partial views of files written/moved/deleted that session; a file-tools write does not heal it). Mitigations: prefer `--rest-base` (Step 2); truncated reads self-flag as `SUSPECT-STALE` + a banner; still **run in a FRESH session** and confirm any surprising DANGLING via the file tools before reporting it as real.
3b. **Never infer a missed upstream run from absent artifacts — probe the scheduler first (added 2026-08-10, `^obs-246` / `^backlog-vaulthealth-silent-noop`).** This pass runs LAST in the Sunday window and is tempted to reason about the passes before it (esp. `vault-health`, whose rotation changes what this pass sees). An absent report or `_CHANGELOG` entry is **not** evidence a pass didn't run — the 2026-08-09 run inferred exactly that about `vault-health`, reasonably and wrongly, and downgraded its own findings to provisional while `vault-health` had fired and exited silently. Before asserting anything about an upstream pass: (i) probe `lastRunAt` via `list_scheduled_tasks`; (ii) check its receipt surface — `vault-health` writes `SYSTEM/reports/vault-health-runs.md` every run, including no-ops. A populated `lastRunAt` with no receipt means **the run failed**, which is a finding to report, not a reason to downgrade your own.
4. **Categorize, don't dump.** Separate the punch list into: genuine breakage (fix), the vault's **folder-link convention** (links pointing at folders rather than notes — pre-existing style, not breakage), and resolver-soft cases (heading-fragment near-misses). Present the actionable list; quarantine GRAVEYARD / `evals/` / `_CHANGELOG` / `_OBSERVATIONS` noise.
5. **Hand off.** Fixes are manual or a separate pass — this skill never edits a note.

## Quarantine (reported separately, `--all` to show)
`GRAVEYARD/`, `WORKFLOWS/evals/`, `_CHANGELOG.md`, `_OBSERVATIONS.md`, the migration plan, and backup files — dangling references there are expected (cold storage / historical record).

## Stop conditions
- Sentinel fails → halt, ask which folder is the vault.
- Zero findings → report "no broken references," stop.

## Logging
If run as a real session (not an incidental check), append a one-line `_CHANGELOG` entry (meta lane) noting the finding count; file any new fragility to `_OBSERVATIONS`.
