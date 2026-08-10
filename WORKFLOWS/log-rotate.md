---
type: workflow
name: log-rotate
trigger: rotate the logs
aliases: [log rotate, run the log doctor, vault health, check the brain-doc sizes, rotate the changelog]
inputs: [_CHANGELOG.md, _OBSERVATIONS.md, _BACKLOG.md, project backlog shards (WRITING/PROJECTS/*/backlog.md)]
outputs: [a measured size report, a per-run receipt line in SYSTEM/reports/vault-health-runs.md (every run, incl. no-ops), a rotated lean _CHANGELOG.md, dated archive files under SYSTEM/history/, a gated "Needs CRE ruling" bin for risky rotations]
lane: meta
status: active
last_updated: 2026-08-10
---

# WORKFLOW: log-rotate

## When to use

A threshold-gated maintenance pass that keeps the **append-only brain docs** from growing past the size where the editing tools stop being safe. Triggered by **"rotate the logs"** / **"run the log doctor"** / **"vault health"** / **"check the brain-doc sizes"**, and by the weekly `vault-health` scheduled task (Mondays, **after** `backlog-sweep`, so it measures the log *after* that run has archived closed items into it).

This is the size sibling of `backlog-sweep` (content) and `link-audit` (references): a measure-then-act pass with the house **"safe ops write; risky ops gate"** discipline. It exists because `_CHANGELOG.md` crossed ~260K chars (2026-06-15), at which point MCP whole-file rewrites and `patch_vault_file` misfire (`^obs-020` / `^obs-081`) and even a newest-first top-insert gets risky — so entries started landing at the foot, inverting the convention (`^obs-082`).

## The problem it solves

Three files grow without bound: `_CHANGELOG.md` (one entry/session), `_OBSERVATIONS.md` (one+ per non-trivial session), `_BACKLOG.md` (drained by `backlog-sweep`, but open items accrete) — **plus the per-project backlog shards** (`WRITING/PROJECTS/*/backlog.md`, carved 2026-06-29), added to the measured set for completeness though they stay append-light and should band GREEN. Past a size threshold:
- whole-file rewrites via the Obsidian MCP truncate or fail (`^obs-060`);
- `patch_vault_file` heading/json targets dump cruft instead of inserting (`^obs-020` / `^obs-081`);
- the safe path narrows to **file-tool targeted Edits** (`^obs-014`).

Rotation keeps each live file small enough that a file-tool **top-insert stays safe** — which is what lets the newest-first convention survive.

## Thresholds (chars)

| Band | Size | Action |
|---|---|---|
| GREEN | < 150K | report only |
| WARN | 150K–200K | report + recommend rotation next run |
| ROTATE | ≥ 200K | act per the per-file policy below |

Measure from the desktop-written `SYSTEM/reports/brain-doc-sizes.json` stamp when fresh (byte-exact — see Step 1), else with the **file tools** (read to EOF), **never** bash `wc -c` — on a large file the bash mount can serve a stale, truncated partial that understates size and would corrupt any carve range (`^obs-014` / `^obs-084`). Defaults chosen 2026-06-15; tune in this table, not in the scheduled task.

## Per-file policy (the core of this workflow)

**`_CHANGELOG.md` — ROTATE via the DESKTOP carve (not the sandbox).**
It is append-only and almost never back-referenced by anchor, so moving old entries is non-destructive — but the **carve is a desktop-owned write** (`^obs-083`): the Cowork sandbox sees a stale, truncated partial of this large file (`^obs-084`), so it can neither size nor carve it safely. The carve therefore runs as **`WORKFLOWS/git-bridge/rotate-changelog.ps1`** on the desktop (clean Dropbox access; the Git Bridge `razorblade-os` repo is the byte-exact restore floor). That script: keeps the most-recent N distinct dates live (default 2), carves older entries **verbatim** into `SYSTEM/history/_CHANGELOG-<bucket>.md`, **normalizes the live file to clean newest-first** (also fixing any foot-append inversion), leaves a foot pointer, bumps `last_updated`, and asserts entry-conservation before writing. It is **dry-run by default** (`-Execute` to apply). When this workflow runs in the sandbox and finds `_CHANGELOG` in the ROTATE band, it does **not** carve — it reports and recommends running `rotate-changelog.ps1 -Execute` on the desktop.

**`_OBSERVATIONS.md` — GATE (never auto-move).**
Its `^obs-NNN` anchors are cross-linked across the vault (`[[_OBSERVATIONS#^obs-NNN]]`); moving a block breaks every citation (`^obs-079` — never repoint blind). Past WARN/ROTATE, do **not** move content. Instead emit a gated recommendation: a **citation-safe split** — carve only observations whose anchors have **zero inbound references** vault-wide (verify with a search) into `SYSTEM/history/_OBSERVATIONS-<period>.md`, leaving a redirect stub for any that are cited. List the candidates; let CRE rule.

**`_BACKLOG.md` — GATE (defer to `backlog-sweep`).**
Growth here is open items; the right tool is `backlog-sweep` (archives closed items, dedupes), not rotation. Past WARN, recommend running `backlog-sweep` and/or a CRE working session; do not rotate.

## Tooling discipline (non-negotiable)

- **File tools only** (Read / Write / Edit) on the mounted vault. **Never** `patch_vault_file` and **never** the Obsidian MCP whole-file rewrite for these files (`^obs-020` / `^obs-014` / `^obs-081`).
- New/newest entries go in at the **top** via a targeted `Edit` (anchor on the `# CHANGELOG\n\n\n` → first-entry boundary), not appended at the foot. Rotation is what keeps that top-insert safe; restoring newest-first is part of the point.
- After every write, **re-read the touched region with the file tools** to confirm it landed (`^obs-014`); do not trust a bash read alone.
- **Size and carve from the file tools only** — never bash `wc -c` or a bash read of these files; the bash mount can serve a stale/truncated partial that understates size and would corrupt the carve (`^obs-084`).

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). If it fails, **halt and report** — do not edit (`^obs-004`).

### Step 1 — Measure
**Preferred (byte-exact): read `SYSTEM/reports/brain-doc-sizes.json`** — a size stamp written by the desktop Git Bridge sync (`seed-repo.ps1`, daily ~12:00) with authoritative filesystem access; it carries byte lengths for every brain doc + the project backlog shards (`^backlog-logrotate-exact-size` / `^obs-090`). Use it when its `generated` timestamp is **≤ 36 h old**; bytes ≥ chars, so banding on bytes errs toward rotating early (safe).

> **⚠️ The age window is necessary but NOT sufficient — a fresh stamp can still be wrong (added 2026-08-03).** The ≤ 36 h rule was written for a once-daily desktop sync, and it cannot see **writes made after the stamp**. These three files are the most-written docs in the vault: every non-trivial session appends to `_CHANGELOG` (DIR-003), observations and backlog items land beside it, and the intake pollers add lines all day. Live instance: the 2026-08-03 `vault-health` run measured off a stamp **43 minutes old** — comfortably inside the window, fully compliant — that was already **~13.5 K short** on `_CHANGELOG`, ~3.8 K on `_OBSERVATIONS` and ~7.7 K on `_BACKLOG`, because one session had written to all three in the interim. The banding survived that time; it need not next time, and `_BACKLOG` was left reading ~178 K (comfortably WARN) when it was nearer ~186 K and closing on the 200 K ROTATE line.
>
> **So the age check is the FIRST gate, not the only one.** Before trusting the stamp, ask whether anything has written to a measured file since `generated`:
> - **Your own run counts.** If this session has already appended to `_CHANGELOG` / `_OBSERVATIONS` / `_BACKLOG` — or is about to, per DIR-003 — the stamp is behind by at least that much. Add the known delta, or fall back to the file tools.
> - **Check `_CHANGELOG`'s newest entry date against `generated`.** An entry stamped after it is proof the file has moved; treat the stamp as stale regardless of age.
> - **Anything within ~10 K of a band boundary is ambiguous when measured off a stamp** — re-measure that file with the file tools before acting on the band, don't act on the stamp alone.
>
> Record which path was used **and** whether the intra-window write check passed, so the next run can tell a verified band call from an inherited one.

If the stamp is missing, stale, or fails the write check above, **fall back** to the file-tools token→char proxy: measure each file with the **file tools** (read to EOF / file-size) on `_CHANGELOG.md`, `_OBSERVATIONS.md`, `_BACKLOG.md`, and treat a band call that sits right at a threshold as ambiguous (report, don't act). **Never size with bash `wc -c`** — on a large file the bash mount may return a truncated partial (`^obs-084`: on the first live run it understated `_CHANGELOG` by ~16K and ended mid-entry). Record each file's band + which measurement path was used.

### Step 2 — Report + receipt (EVERY run, including a no-op)
Emit a one-table report: file · size · band · recommended action.

**Then write the run receipt — unconditionally, before any early exit (added 2026-08-10, `^obs-246` / `^backlog-vaulthealth-silent-noop`).** Top-insert one line into `SYSTEM/reports/vault-health-runs.md` (create it with a `# vault-health run receipts` heading if absent):

```
- YYYY-MM-DD HH:MM (attended|scheduled) — bands: CHANGELOG <band> <size> · OBS <band> <size> · BACKLOG <band> <size> · shards <band> — path: <stamp(<generated>, write-check pass|fail)|file-tools> — action: <no-op, all GREEN | gated recommendations | ROTATE delegated to desktop>
```

Verify the insert by re-reading the top of the file (DIR-005). **Why:** the 2026-08-09 scheduled run exited with zero artifacts while `_CHANGELOG` sat past the ROTATE line, and the next pass in the window wrongly inferred it hadn't run. A silent exit was spec-compliant under the old Step 2. The receipt makes every completed run leave evidence; a missing receipt beside a populated `lastRunAt` now unambiguously means **the run failed**, not "nothing to do."

If all GREEN: write the receipt, say so, and stop. **The receipt is the artifact of record for a no-op run — it replaces the `_CHANGELOG` entry** (DIR-003's trivial carve-out applies to the log, not the receipt), so weekly no-ops don't grow the very file this pass exists to keep small.

### Step 3 — Rotate `_CHANGELOG` if ROTATE (delegate to the desktop)
Do **not** carve from the sandbox — the mount is stale (`^obs-084`) and the carve is desktop-owned (`^obs-083`). Report that `_CHANGELOG` is in the ROTATE band and recommend running **`WORKFLOWS/git-bridge/rotate-changelog.ps1`** on the desktop (preview first, then `-Execute`), then `seed-repo.ps1` to commit. Only on a clean, non-sandbox environment with authoritative file access should an agent carve directly — and then only entirely from file-tool reads, verifying both files after.

### Step 4 — Gate the rest
For `_OBSERVATIONS` / `_BACKLOG` past WARN, assemble a `## Needs CRE ruling (log-rotate YYYY-MM-DD)` bin (append to `_BACKLOG.md`, or surface inline on an attended run): the proposed citation-safe split / backlog-sweep recommendation + reason. Never move their content automatically.

### Step 5 — Report + log
**On any run that acted or gated** (non-GREEN band, rotation recommended, bin emitted): append a dated entry to `_CHANGELOG.md` (meta lane) — **via the file tools, newest-first at the top** (post-rotation the file is lean, so this is safe). Counts: files measured / bands / rotated / archived-to / gated. File any new fragility to `_OBSERVATIONS.md` (`^obs-NNN`, top-insert). Add follow-ups to `_BACKLOG.md`. An all-GREEN run already left its receipt at Step 2 and logs nothing here.

## Stop conditions

- Vault sentinel fails (Step 0) → halt, report.
- The file tools can't write a target → halt, report; **never** fall back to `patch_vault_file` or MCP whole-file rewrite.
- A `_CHANGELOG` rotation would split mid-entry, or the cutoff is ambiguous → carve on a clean `## ` entry boundary only; if none is safe, gate it.
- More than the recent-keep window is unclear → keep more, not less; archiving is reversible, data loss is not.

## Logging

On completion, append to `_CHANGELOG.md` (meta lane), newest-first via the file tools. Unattended runs follow the scheduled-task close discipline (changelog + observations + any follow-ups). Apply all active `_DIRECTIVES` (esp. DIR-001 secrets, DIR-002 loading order, DIR-003 log every session, DIR-004 serialized YAML for any derived frontmatter).
