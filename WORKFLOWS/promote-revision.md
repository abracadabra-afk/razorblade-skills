---
type: workflow
name: promote-revision
trigger: promote the revision
aliases: [promote rev, make the revision the live draft, bring the revision into draft, update the working draft, account the landing]
inputs: [the chapter's newest revisions/YYYY-MM-DD-<slug>-rev<N>.md, the chapter's current draft.md]
outputs: [draft.md body replaced with the promoted revision + rewritten lineage frontmatter, supersession stamps on the folder's stale derives + moot rulings (Step 3b)]
lane: fiction
status: active
last_updated: 2026-09-01
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

Frontmatter mapping — **the status names where the live text came from** (general rule folded back from the installed skill 2026-08-10, `^backlog-promote-revision-expansion-route` (a) — the doc had branch cases only, and an expansion rev promoted under the default would have claimed the register already ran): read the rev's `kind`/stage and set status to **that stage**. Named cases: `loop-clear → loops-cleared` · **`expansion → expansion-revised`** (a `prose-expansion` output — the register has NOT run on it; register-pass is downstream of expansion in the v6 route) · a register-pass rev (or no `kind`) → `register-revised`. Any future stage: set status to that stage — never default a foreign rev to `register-revised`.

Then **keep** `source_slate` (deep provenance); **add** `source_revision` (immediate parent = the promoted rev path); **carry `protected_patterns` forward explicitly** (added 2026-08-10, (b) — it is a DIR-014 surface consulted by the next gate and must never ride the implicit "preserve fields not mentioned" catch-all; if the rev's note carries `protected_spans_touched:` with `reworded` entries, confirm the witnesses were updated in the same session before promoting); carry `register`/`register_title`/`mode` from the rev when present (a loop-clear rev may carry none — omit what's absent rather than inventing it); keep `blind_read` and other prior pointers; bump `last_updated`. `slate/`, `revisions/`, and `spec-check/` are never touched.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Locate chapter + revision
Resolve the chapter folder; pick the newest `…-rev<N>.md` passage (or the named one). No revision present → halt (run `register-pass` first). Name the rev picked.

### Step 2 — Verify lineage
Compare the revision's `source_slate` to `draft.md`'s. **Normalize both sides to the bare run id first** (dec-033, 2026-09-02): strip a leading `slate/` and a trailing `/clean-draft.md`, so `slate/2026-08-05-01/clean-draft.md` and `2026-08-05-01` compare equal — the pre-ruling chapters (CH1/CH2 revs carry the path form; CH12–CH17 the bare form) must never false-trip this ask. The bare form is the ruled canonical; write it on the promoted `draft.md`. Match (or draft is a scaffold) → proceed. Mismatch → surface both slates and ask before overwriting — a real divergence should never be buried silently.

**Fallback when a side lacks `source_slate` (added 2026-08-10, (c) — the v6/expansion route stitched CH12's draft with `provenance:` instead, so this check could not run as written):** verify lineage on `provenance:` (or the rev note's stated source) by confirming both sides name the **same slate run**; on a match, **normalize the draft onto `source_slate`** in the same promotion so the check runs as written next time. Neither field present on one side → treat as a mismatch: surface and ask. Every route that emits a promotable rev should write `source_slate`; a route that can't yet is the defect to file, not a case to wave through.

### Step 3 — Promote
Replace `draft.md`'s body with the revision's prose (keep any `[unclear: …]` marks); rewrite the frontmatter per the mapping (read the rev's `kind`/stage first — the status names where the live text came from: `loop-clear → loops-cleared`, `expansion → expansion-revised`, register-pass/default → `register-revised`). Optionally bump `_status.md` `last_updated`.

### Step 3b — Supersession accounting (DIR-019, added 2026-09-01) — safe-op, logged, never asked
A promotion is a staleness event for everything that described the previous draft. In the same session, mechanically:

1. **Stamp the derives.** Every derived artifact in the folder whose stamp predates this promotion — `record-script.md`, `performance-notes.md`, `runway.md`, `choreo/*.md`, any `*-sheet` — gets `superseded_by: draft.md (<date>, <rev>)` in frontmatter, **in place, never moved** (pointers and trails survive). Deterministic derives the route needs downstream (StoryLine) regenerate via their own skill; don't hand-edit them here.
2. **Triage the rulings.** Every span-naming ruling that points at this draft — `open-loops.md` resolutions, `premise.md` amendments, `REFERENCE/protected-patterns.md` rows, board chunks in `TASKS/` naming the chapter — checked by span presence in the promoted text: **present → carry; gone → stamp moot (`superseded_by` + date), one changelog line; reworded-but-surviving → list, one batch, for the next pass that binds them** (not a question for CRE now — the next gated pass surfaces the batch once).
3. **Update the landed file's own list.** `draft.md`'s `status` / open-items field is rewritten to describe **this** landing — the previous landing's "still open" list dies with the previous draft (`^obs-279`'s recurrence).
4. **Archive byte-exact.** The superseded `draft.md` body is already preserved by the revision chain in the normal case; on a **hand-landing** (below) write it to `revisions/<date> - draft N superseded.md` first, before anything else touches the folder.

**Hand-landing mode — trigger "account the landing" (DIR-019 §3).** When CRE has landed a draft himself (no rev in `revisions/`, `draft.md` already carries the new prose), Steps 1–2 don't apply: **his landing is the ruling.** Run Step 3b alone — archive first (item 4), then items 1–3. Never ask him to confirm a change he made, never re-open an item his rewrite discharged. Report what was stamped and what was retired, in one block; the reworded batch (if any) travels to the next pass. This closes the gap `^backlog-author-landing-preflight` names: the hand-landing had no accounting step and no archive.

**Scope lock (§4).** Staleness outside this chapter's folder and its `REFERENCE/` rows — a channel-law worked example, another episode's pointer — is one line in `SYSTEM/drift-ledger.md`, not a finding in this session.

### Step 4 — Log
Append to the chapter `changelog.md` and vault [[_CHANGELOG]] (fiction lane); file fragilities to [[_OBSERVATIONS]].

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- Chapter has no `revisions/` or no `draft.md` → halt, tell CRE (convention not adopted).
- No `…-rev<N>.md` passage in `revisions/` → halt; nothing to promote — **unless** the trigger was "account the landing," in which case run Step 3b alone (hand-landing mode).
- Revision `source_slate` ≠ draft `source_slate` (and draft isn't a scaffold) → pause, surface, ask.

## Logging
On completion append an entry to [[_CHANGELOG]] (fiction lane) and the chapter's `changelog.md`; file any new fragility to [[_OBSERVATIONS]]. See the skill for the exact log format.

---

_Canonical reference for the `promote-revision` Cowork skill. Per [[_SKILLS MAP#Cowork skills]], procedure changes land here first, then propagate to the skill via skill-creator._
