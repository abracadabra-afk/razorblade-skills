---
type: workflow
name: promote-revision
trigger: promote the revision
aliases: [promote rev, make the revision the live draft, bring the revision into draft, update the working draft]
inputs: [the chapter's newest revisions/YYYY-MM-DD-<slug>-rev<N>.md, the chapter's current draft.md]
outputs: [draft.md body replaced with the promoted revision + rewritten lineage frontmatter]
lane: fiction
status: active
last_updated: 2026-06-16
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). Any project with a revisions/ + draft.md — no register required (the register already ran upstream).
pipeline_position: the return trip out of [[WORKFLOWS/register-pass]]. register-pass writes revisions/ and deliberately never touches draft.md; this workflow moves the newest revision back into the live draft, closing that gap.
---

# WORKFLOW: Promote Revision

> Moves a chapter's newest **revision** (the `register-pass` output in `revisions/`) into the live **`draft.md`**, carrying the metadata forward so the lineage stays intact. This is the documented return trip out of the `revisions/` one-way door.

## When to use

When CRE has a revision in a chapter's `revisions/` and wants it to become the working draft. Trigger phrases: "promote the revision," "promote rev N," "make the revision the live draft," "bring the revision into draft," "update the working draft." Runs **after** [[WORKFLOWS/register-pass]] (which produces the revision but never writes `draft.md`).

Do NOT trigger this to revise against the register (that is [[WORKFLOWS/register-pass]]) or to produce a slate (that is [[WORKFLOWS/transcoder]]). It moves text and rewrites frontmatter; it never changes a word of prose.

## Key principle — the draft is a mirror, so promotion is safe

`draft.md` is a working **mirror of the newest promoted revision**. The immutable copies live in `revisions/` (and the slate behind them). So overwriting `draft.md` loses nothing recoverable — re-promoting an earlier rev restores any prior state, and the promoted revision stays untouched in `revisions/`. That invariant is what lets the skill overwrite `draft.md` without a heavy approval gate in the normal case.

## Inputs

- **The revision** — newest `<chapter>/revisions/YYYY-MM-DD-<slug>-rev<N>.md` (latest date, then highest N), unless CRE names a specific rev. The `-note.md` sidecar is read for lineage but never promoted.
- **The current `draft.md`** — its frontmatter is read to compare lineage and to preserve earlier-stage pointers (`blind_read`, etc.).

## Outputs (one file rewritten)

| What | Destination |
|---|---|
| Promoted prose (byte-for-byte from the revision) + rewritten frontmatter | `<chapter>/draft.md` |

Frontmatter mapping: `status: register-revised` — **except** when the promoted rev carries `kind: loop-clear` (a `loop-clearer` output), in which case map `status: loops-cleared`. Read the rev's `kind` and branch: `loop-clear → loops-cleared`, default (no `kind`, or any register-pass rev) → `register-revised`. Then **keep** `source_slate` (deep provenance); **add** `source_revision` (immediate parent = the promoted rev path); carry `register`/`register_title`/`mode` from the rev when present (a loop-clear rev may carry none — omit what's absent rather than inventing it); keep `blind_read` and other prior pointers; bump `last_updated`. `slate/`, `revisions/`, and `spec-check/` are never touched.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Locate chapter + revision
Resolve the chapter folder; pick the newest `…-rev<N>.md` passage (or the named one). No revision present → halt (run `register-pass` first). Name the rev picked.

### Step 2 — Verify lineage
Compare the revision's `source_slate` to `draft.md`'s. Match (or draft is a scaffold) → proceed. Mismatch → surface both slates and ask before overwriting — a real divergence should never be buried silently.

### Step 3 — Promote
Replace `draft.md`'s body with the revision's prose (keep any `[unclear: …]` marks); rewrite the frontmatter per the mapping (read the rev's `kind` first — `loop-clear` lands `status: loops-cleared`, otherwise `register-revised`). Optionally bump `_status.md` `last_updated`.

### Step 4 — Log
Append to the chapter `changelog.md` and vault [[_CHANGELOG]] (fiction lane); file fragilities to [[_OBSERVATIONS]].

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- Chapter has no `revisions/` or no `draft.md` → halt, tell CRE (convention not adopted).
- No `…-rev<N>.md` passage in `revisions/` → halt; nothing to promote.
- Revision `source_slate` ≠ draft `source_slate` (and draft isn't a scaffold) → pause, surface, ask.

## Logging
On completion append an entry to [[_CHANGELOG]] (fiction lane) and the chapter's `changelog.md`; file any new fragility to [[_OBSERVATIONS]]. See the skill for the exact log format.

---

_Canonical reference for the `promote-revision` Cowork skill. Per [[_SKILLS MAP#Cowork skills]], procedure changes land here first, then propagate to the skill via skill-creator._
