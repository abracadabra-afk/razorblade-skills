---
type: workflow
name: backlog-sweep
trigger: sweep the backlog
aliases: [clean the backlog, tidy the backlog, backlog maintenance, dedupe the backlog]
inputs: [_BACKLOG.md]
outputs: [a tidied _BACKLOG.md, archived-completed entries in _CHANGELOG.md, a sweep report, a gated "Needs CRE ruling" bin]
lane: writing-ops
status: active
last_updated: 2026-06-14
---

# WORKFLOW: backlog-sweep

## When to use

Maintenance pass over `_BACKLOG.md` to keep it lean and trustworthy. Triggered by **"sweep the backlog"** / **"clean the backlog"** / **"tidy the backlog"**, and by the weekly `backlog-sweep` scheduled task (Mondays, after `skills-sweep`). It removes accumulated cruft — completed items left checked in place, exact duplicates, malformed entries, drifted priority tags — and consolidates near-duplicate items, **gating every judgment call for CRE** rather than guessing.

This is the backlog sibling of `skills-manager` (skills) and `canon-sync` (canon): a derive-and-tidy pass with the house **"additions/safe-ops write; contradictions/judgment-calls gate"** discipline. It runs *after* `skills-sweep` on Mondays because `skills-sweep` appends follow-ups to `_BACKLOG.md`; the sweep then absorbs and normalizes them.

## Inputs

`_BACKLOG.md` (the whole file). Cross-references: `_CHANGELOG.md` (archive destination), `_OBSERVATIONS.md` (for `^obs-NNN` / `^anchor` validity), and `_SKILLS MAP.md` (to confirm a referenced workflow still exists before keeping a task that points at it).

## Outputs

1. A tidied `_BACKLOG.md` with safe ops applied.
2. Completed (`- [x]`) and canceled (`- [-]`) items moved to `_CHANGELOG.md` (honoring the backlog convention: *"When completing a task, move it to _CHANGELOG instead of leaving it checked here."*).
3. A **"Needs CRE ruling"** bin appended at the end of `_BACKLOG.md` listing every gated judgment call, one line each with the proposed action + reason.
4. A short sweep report (counts: archived / deduped / reformatted / gated) appended to `_CHANGELOG.md`.

## Write-mode policy (the core of this workflow)

**AUTO-APPLY (safe ops) — do these without asking:**

- **Archive closed items.** Move every `- [x]` (done) and `- [-]` (canceled) line out of `_BACKLOG.md` into a dated `_CHANGELOG.md` entry. Preserve the item's text, anchor, and any "done YYYY-MM-DD" note verbatim. Do NOT archive open `- [ ]` items.
- **Merge exact duplicates.** When two `- [ ]` items are textually identical (or identical modulo whitespace/punctuation), keep one, delete the rest. Preserve the surviving line's anchor(s); if duplicates carried different anchors, keep all anchors on the survivor.
- **Normalize formatting.** Fix checkbox glyphs (`[ ]`/`[x]`/`[-]`), collapse stray blank lines, repair obviously mojibaked characters, and ensure each item sits under the correct lane heading (OS/Meta · Fiction · Writing Ops). Move a clearly-misfiled item to its right lane.
- **Fix priority-tag drift.** De-duplicate repeated tags on one line (e.g. `#p1 #p1` → `#p1`). Do NOT invent or change a priority that isn't there.
- **Refresh frontmatter** `last_updated`.

**GATE (judgment calls) — never apply; list in the "Needs CRE ruling" bin:**

- Merging **non-identical but overlapping** items (consolidation that changes wording or scope).
- **Dropping / canceling an open item** that looks stale, obsolete, or superseded (e.g. its `^obs` is graduated to a directive, its workflow shipped, its referenced file is gone). Propose; let CRE rule `[x]`/`[-]`.
- **Re-prioritizing** (adding/raising/lowering `#p1`/`#p2`/`#p3`).
- Splitting one overloaded item into several, or rewriting an item for clarity.
- Anything that touches a `#blocked`/`#waiting` item's meaning.

Rule of thumb: if the operation is reversible and loses no author intent, auto-apply it; if it requires judging whether CRE still wants something, gate it.

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). If it fails, **halt and report** — do not edit (`^obs-004`).

### Step 1 — Inventory
Read `_BACKLOG.md` in full. Build a list of every item with: lane, checkbox state, text, anchors, tags. Count open/done/canceled per lane.

### Step 2 — Classify each item
Tag each as: ARCHIVE (closed) · EXACT-DUP · REFORMAT · STALE? (open but possibly obsolete — verify against `_OBSERVATIONS`/`_SKILLS MAP`/filesystem) · CONSOLIDATE? (overlaps another) · KEEP.

### Step 3 — Apply safe ops
Execute every AUTO-APPLY operation from the policy above. Edit `_BACKLOG.md` with the **file tools (Read/Write/Edit), not `patch_vault_file`** (`^obs-020`/`^obs-014`). Move archived items into a single dated `_CHANGELOG.md` entry.

### Step 4 — Assemble the gate bin
Append a `## Needs CRE ruling (backlog-sweep YYYY-MM-DD)` section to the bottom of `_BACKLOG.md`. One line per gated call: the item, the proposed action, and the one-clause reason. If a prior sweep's gate bin still has unruled lines, fold them in rather than stacking a second bin.

### Step 5 — Report + log
Append a one-line dated entry to `_CHANGELOG.md` under writing-ops: counts archived / deduped / reformatted / gated, plus anything notable. File any new fragility to `_OBSERVATIONS.md` with a `^obs-NNN` anchor. If nothing changed since the last sweep, say so in one line and keep the run read-only.

## Stop conditions

- Vault sentinel fails (Step 0) → halt, report.
- The file tools can't write `_BACKLOG.md` → halt, report; never fall back to `patch_vault_file`.
- More than ~⅓ of open items would land in the gate bin → apply safe ops only, then surface that the backlog likely needs a CRE working session rather than a routine sweep.

## Logging

On completion, append to `_CHANGELOG.md` (writing-ops lane). Unattended runs follow the scheduled-task close discipline (changelog + observations + any follow-ups). Apply all active `_DIRECTIVES` (esp. DIR-001 secrets, DIR-002 loading order, DIR-003 log every session).
