---
name: log-rotate
description: Threshold-gated size-maintenance pass that keeps the append-only brain docs (_CHANGELOG, _OBSERVATIONS, _BACKLOG) from growing past the size where the editing tools stop being safe — the size sibling of backlog-sweep (content) and link-audit (references). Use when CRE asks to "rotate the logs," "run the log doctor," "vault health," "check the brain-doc sizes," or "rotate the changelog," and on the weekly vault-health scheduled task. Measures each file with the file tools (never bash wc -c — the mount serves stale partials that understate size), bands it GREEN/WARN/ROTATE, and acts per the house "safe ops write; risky ops gate" rule: _CHANGELOG rotation is delegated to the desktop carve (rotate-changelog.ps1); _OBSERVATIONS and _BACKLOG are gated, never auto-moved (anchors cross-linked / items live). Do NOT use to archive closed backlog items (backlog-sweep), fix broken links (link-audit), or rewrite these logs via patch_vault_file or an MCP whole-file write.
---

# log-rotate

You are running a **threshold-gated size-maintenance pass** over the append-only brain docs. It keeps each live file small enough that a file-tool **top-insert stays safe** — which is what lets the newest-first convention survive. The size sibling of `backlog-sweep` (content) and `link-audit` (references): a measure-then-act pass with the house **"safe ops write; risky ops gate"** discipline. It exists because `_CHANGELOG.md` crossed ~260K chars (2026-06-15), at which point MCP whole-file rewrites and `patch_vault_file` misfire (`^obs-020` / `^obs-081`) and even a newest-first top-insert gets risky — so entries started landing at the foot, inverting the convention (`^obs-082`).

Canonical reference: `WORKFLOWS/log-rotate.md`. This is the AI-trigger surface; that doc is the in-vault canon.

---

## The hard line — file tools only, safe ops write, risky ops gate
- **Measure and carve from the file tools only** (Read / Write / Edit on the mounted vault). **Never** bash `wc -c` and **never** a bash read of these files: on a large file the bash mount serves a stale, truncated partial that understates size and would corrupt any carve range (`^obs-014` / `^obs-084`: on the first live run it understated `_CHANGELOG` by ~16K and ended mid-entry).
- **Never** `patch_vault_file` and **never** the Obsidian MCP whole-file rewrite for these files (`^obs-020` / `^obs-081`) — both dump cruft or truncate at size.
- New/newest entries go in at the **top** via a targeted `Edit` (anchor on the `# CHANGELOG\n\n\n` → first-entry boundary), not appended at the foot. Rotation is what keeps that top-insert safe; restoring newest-first is part of the point.
- After every write, **re-read the touched region with the file tools** to confirm it landed (`^obs-014`); do not trust a bash read alone.
- Safe ops write; risky ops gate. Archiving is reversible, data loss is not.

---

## Step 0 — Vault sentinel (^obs-004)
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). If it fails, **halt and report** — do not edit.

## Step 1 — Measure
**Preferred (byte-exact):** read `SYSTEM/reports/brain-doc-sizes.json` — the size stamp the desktop Git Bridge sync (`seed-repo.ps1`, daily ~12:00) writes with authoritative filesystem access (`^backlog-logrotate-exact-size` / `^obs-090`). Use it when its `generated` timestamp is ≤ 36 h old; bytes ≥ chars, so banding on bytes errs toward rotating early (safe). If missing or stale, **fall back**: measure each of `_CHANGELOG.md`, `_OBSERVATIONS.md`, `_BACKLOG.md` with the **file tools** (read to EOF / file-size), treating an at-threshold call as ambiguous (report, don't act). **Do not size with bash `wc -c`** (`^obs-084`). Record each file's band + which measurement path was used:

| Band | Size | Action |
|---|---|---|
| GREEN | < 150K | report only |
| WARN | 150K–200K | report + recommend rotation next run |
| ROTATE | ≥ 200K | act per the per-file policy below |

Defaults chosen 2026-06-15; tune in this table, not in the scheduled task.

## Step 2 — Report
Emit a one-table report: file · size · band · recommended action. If all GREEN, say so and **stop here** (read-only run).

## Step 3 — Rotate `_CHANGELOG` if ROTATE (delegate to the desktop)
`_CHANGELOG.md` is append-only and almost never back-referenced by anchor, so moving old entries is non-destructive — **but the carve is a desktop-owned write** (`^obs-083`): the Cowork sandbox sees a stale, truncated partial of this large file (`^obs-084`), so it can neither size nor carve it safely. Do **not** carve from the sandbox. Report that `_CHANGELOG` is in the ROTATE band and recommend running **`WORKFLOWS/git-bridge/rotate-changelog.ps1`** on the desktop (preview first, then `-Execute`), then `seed-repo.ps1` to commit. That script keeps the most-recent N distinct dates live (default 2), carves older entries **verbatim** into `SYSTEM/history/_CHANGELOG-<bucket>.md`, normalizes the live file to clean newest-first (fixing any foot-append inversion), leaves a foot pointer, bumps `last_updated`, and asserts entry-conservation before writing. Only on a clean, non-sandbox environment with authoritative file access should an agent carve directly — and then only entirely from file-tool reads, verifying both files after.

## Step 4 — Gate the rest (never auto-move)
- **`_OBSERVATIONS.md` — GATE.** Its `^obs-NNN` anchors are cross-linked vault-wide (`[[_OBSERVATIONS#^obs-NNN]]`); moving a block breaks every citation (`^obs-079` — never repoint blind). Past WARN/ROTATE, do **not** move content. Emit a gated recommendation: a **citation-safe split** — carve only observations whose anchors have **zero inbound references** vault-wide (verify with a search) into `SYSTEM/history/_OBSERVATIONS-<period>.md`, leaving a redirect stub for any that are cited. List the candidates; let CRE rule.
- **`_BACKLOG.md` — GATE (defer to `backlog-sweep`).** Growth here is open items; the right tool is `backlog-sweep` (archives closed items, dedupes), not rotation. Past WARN, recommend running `backlog-sweep` and/or a CRE working session; do not rotate.

For either past WARN, assemble a `## Needs CRE ruling (log-rotate YYYY-MM-DD)` bin (append to `_BACKLOG.md`, or surface inline on an attended run) with the proposed split / sweep recommendation + reason. Never move their content automatically.

## Step 5 — Report + log
Append a dated entry to `_CHANGELOG.md` (meta lane) — **via the file tools, newest-first at the top** (post-rotation the file is lean, so this is safe). Counts: files measured / bands / rotated / archived-to / gated. File any new fragility to `_OBSERVATIONS.md` (`^obs-NNN`, top-insert). Add follow-ups to `_BACKLOG.md`.

---

## Stop conditions
- Vault sentinel fails (Step 0) → halt, report.
- The file tools can't write a target → halt, report; **never** fall back to `patch_vault_file` or an MCP whole-file rewrite.
- A `_CHANGELOG` rotation would split mid-entry, or the cutoff is ambiguous → carve on a clean `## ` entry boundary only; if none is safe, gate it.
- More than the recent-keep window is unclear → keep more, not less; archiving is reversible, data loss is not.

## Files this skill writes — and must not
**Writes (file tools only):** a measured size report (chat or `SYSTEM/reports/`); on a clean non-sandbox run, a lean newest-first `_CHANGELOG.md` + dated `SYSTEM/history/_CHANGELOG-<bucket>.md` archives; a gated `## Needs CRE ruling` bin appended to `_BACKLOG.md`; the closing `_CHANGELOG` / `_OBSERVATIONS` / `_BACKLOG` log entries.
**Must NOT write:** any move of `_OBSERVATIONS` / `_BACKLOG` content (gated only); any `_CHANGELOG` carve from inside the sandbox; any edit via `patch_vault_file` or an MCP whole-file rewrite. Apply all active `_DIRECTIVES` (DIR-001 secrets, DIR-002 loading order, DIR-003 log every session, DIR-004 serialized YAML, DIR-005 file-tools-only on the OS docs).

## What this skill is NOT
- Not `backlog-sweep` (archives closed backlog items + dedupes content; this measures size and gates `_BACKLOG` to it).
- Not `link-audit` (broken-reference sweep; this is the size sibling, not the reference one).
- Not a content editor — it never rewrites an entry; it carves verbatim (desktop) or gates.

## Build status
- Canon doc shipped 2026-06-15 at `WORKFLOWS/log-rotate.md` (status: active, `^obs-082`); the desktop carve lives at `WORKFLOWS/git-bridge/rotate-changelog.ps1`.
- This source authored from that doc (source-ahead of any install).
- Propagation to the installed skill = desktop `pack-skills.ps1` + Save-skill (`^backlog-log-rotate-skill-package`). The `_SKILLS MAP` trigger row is already present (the "rotate the logs" / "vault health" row). Until packaged, the workflow runs via the bootstrap trigger index + the weekly `vault-health` scheduled task (both already live).
