# The revision contract (v2 — ruled 2026-09-02, dec-033)

This is the single statement of what a register-pass run writes into `<chapter>/revisions/`. `scripts/register_scaffold.py` enforces it (`new` writes the stubs, `check` verifies a finished pair); the canon `WORKFLOWS/register-pass.md` and `promote-revision` point here. If this file and a run disagree, the run is wrong.

Why one file: between 2026-06 and 2026-08 five register runs shipped four different frontmatter schemas. `source_slate` went out as a path (`slate/2026-06-03-01/clean-draft.md`) and as a bare run id (`2026-08-05-01`) — the one key `promote-revision` compares to decide whether a promotion is a lineage mismatch. The note's pairing key drifted `explains:` → `pairs_with:`. One run produced a note with no passage that no doc defined. Every consumer that reads a revision reads *this* shape.

---

## 1. Files and names

```
<chapter>/revisions/
├── YYYY-MM-DD-<slug>-rev<N>.md          the revised passage        (full / execute-only)
├── YYYY-MM-DD-<slug>-rev<N>-note.md     the editorial note         (full / execute-only)
└── YYYY-MM-DD-<slug>-sweep<N>-note.md   the note alone             (sweep — no passage)
```

- `<slug>` — the slate's `envelope_segments` joined with `+` (`waking-hearth+the-hunt`). When the working text is `draft.md` and no segment list is reachable, `full-chapter` (the form every 2026-08 run used).
- `<N>` — next integer for that slug in `revisions/`, starting at 1. `rev` and `sweep` count separately; a sweep never consumes a `rev<N>` (RP-Q2), so `land-chapter`'s "at least one rev" probe stays honest.
- The script allocates both. Never hand-name a revision.

## 2. Modes

| mode | when | writes |
|---|---|---|
| `full` | no ready verdict sheet for this slate run | rev + note |
| `execute-only` | `<chapter>/spec-check/<run>/verdicts.md` exists, `status: ready`, `slate_run` matches the working text's run | rev + note; the sheet's rulings win on every span they cover |
| `sweep` | the register ran as a verification sweep and earned no edit (`chapter-clean` Leg 7: "rev only if edits earned") | note only |

A `verdicts.md` whose `slate_run` does not match is treated as absent, and the mismatch is named in the note.

## 3. Working text — which prose the register runs on

Prefer `<chapter>/draft.md` when it carries real content; otherwise the newest `slate/YYYY-MM-DD-NN/clean-draft.md` (latest date, then highest NN), unless CRE names a run.

`draft.md` is **scaffold** when its `status` starts with `not-yet-migrated`, or its body is empty / only the placeholder blockquote. Anything else is real content — `dev-revised`, `loops-cleared`, `expansion-revised`, `register-revised`, `author-cut …`, `line-pass-ready`, and whatever the next pass names. The test is *is there prose here*, not a status whitelist, because the status vocabulary has grown with every new pass and a whitelist goes stale the day one is added.

When the working text is `draft.md`, `source_slate` comes from its frontmatter (normalized to the bare form). The slate ledgers (`synthesis-ledger.md`, `leaves-left.md`) still belong to that run and are read as prior-pass context only.

## 4. Rev frontmatter (the passage file)

```yaml
---
type: chapter-revision
chapter: CHAPTER 13 - THE UMBRAL PRECIPICE
project: WITCHWOOD
rev: 2
kind: register
source_slate: 2026-08-05-01
working_text: draft.md
register: REFERENCE/register.md
register_title: Braided-Register Literary Fantasy (v3)
mode: execute-only
verdicts: spec-check/2026-08-05-01/verdicts.md
maturity_gear: POLISHED
generated: '2026-09-02 15:10'
---
```

| key | type | who reads it |
|---|---|---|
| `type` | `chapter-revision` | every revisions/ reader; distinguishes this from loop-clear / expansion / author revs |
| `chapter` | folder name | `promote-revision` (stamp check) |
| `project` | project folder name | audit |
| `rev` | integer, same as `<N>` in the filename | `promote-revision` (newest pick) |
| `kind` | `register` | `promote-revision` — maps to `status: register-revised` on promotion (loop-clear → `loops-cleared`, expansion → `expansion-revised`) |
| `source_slate` | **bare run id** `YYYY-MM-DD-NN` (dec-033) | `promote-revision` — compared to `draft.md`'s; both sides are normalized (strip `slate/` and `/clean-draft.md`) so pre-ruling chapters never false-trip |
| `working_text` | `draft.md` or `slate/<run>/clean-draft.md` | audit — a misfire is visible at a glance |
| `register` | project-relative path | `promote-revision` (carried forward) |
| `register_title` | the register's own `# ` title line, verbatim | `promote-revision` (carried forward) |
| `mode` | `full` / `execute-only` (never `sweep` on a rev file) | `promote-revision` (carried forward); `chapter-clean` |
| `verdicts` | sheet path — **execute-only only**; absent otherwise | audit |
| `maturity_gear` | the gear the register chose | audit |
| `generated` | quoted `'YYYY-MM-DD HH:MM'` | audit |

Retired — never write these on a register rev: `status` (the rev has no lifecycle; `draft.md` does), `source` (free-text provenance — use the keyed fields), `rulings` (belongs in the note body), `sheet` / `ledger` (expansion and clean-mode surfaces; cite them in the note body), `explains` (was the note's pairing key; now `pairs_with`).

## 5. Note frontmatter (the sidecar)

```yaml
---
type: revision-note
pairs_with: revisions/2026-09-02-full-chapter-rev2.md
protected_spans_touched:
- span: she thought of choices
  state: kept
- span: the pillow of her tongue
  state: reworded
  new: the wet pillow of her tongue
- span: Been through worse, haven't we?
  state: dropped
  ruled: '2026-09-02'
drift:
  voice_spec: in band
  contamination: none
---
```

| key | type | who reads it |
|---|---|---|
| `type` | `revision-note` | revisions/ readers |
| `pairs_with` | the rev file this note explains; for a sweep, the working text + `(sweep — no passage produced)` | `promote-revision` (finds the note), `line-edit` |
| `protected_spans_touched` | list, one row per **chapter-level** `protected_patterns` span (from the working text's frontmatter); `[]` explicitly when the chapter has none | the write gate (`^backlog-protected-span-write-gate` ii), `line-edit`, `record-script` |
| `drift` | mapping: `voice_spec`, `contamination` — one short line each, or `n/a — <file> absent` when the project keeps no such reference | CRE; the note body repeats nothing |

**`protected_spans_touched` rows.** `state` is one of three:

- `kept` — the span is in the rev body **byte-identical** (on a sweep: in the working text the note names). The script verifies this (RP-Q3; sweep path RP-P1, 2026-09-02); a `kept` row whose span is not found verbatim fails `check` and goes to the reasoning stage as a QUERY. The script never decides what happened — only that the claim is false.
- `reworded` — rule intact, witness changed. `new:` is required and must appear verbatim in the rev body. Update the witness in `REFERENCE/protected-patterns.md` / the chapter frontmatter in the same session.
- `dropped` — `ruled:` (date) is required. A drop without a ruling is a defect: revert, don't rationalize.

The rows come pre-enumerated in the stub with `state: <<FILL: kept|reworded|dropped>>`; a note that still carries a `<<FILL` marker fails `check`. The empty list is a statement ("touched none, and I looked"), never an omission.

**What the script does NOT verify (DIR-018):** the project-wide P-rules in `REFERENCE/protected-patterns.md` are constructions, not spans — the reasoning stage consults them before every proposal and the script only reports their count. Whether a rewording preserved the *rule* is a reading, never a match.

## 6. Bodies

- **Rev body** — clean revised prose only. The register's inline unrecoverable marks (`[unclear: "wild-out"?]`) stay; they are part of the passage. No headings, no commentary. `check` fails an empty body.
- **Note body** — the register's full editorial note, verbatim, in the register's own order: unrecoverable breaks **first**, then diagnosis, craft changes, mechanical corrections, changes-considered-and-rejected, counts. Then any execute-only accounting (which verdict rows were applied), any `leaves-left` `left-for-later` items addressed, and any `[REGISTER-REPAIR]` flags acted on.
- **Sweep note body** — what was checked, what was found clean, what would have been an edit and why it was not earned. It is the receipt for "the register ran and changed nothing."

## 7. Never

- Never write into `slate/` — the audit trail is immutable.
- Never write `draft.md` — that is `promote-revision`'s one job.
- Never hand-type the frontmatter — the script emits it and parse-gates it (DIR-004).
- Never revise a span the verdict sheet ruled, and never re-litigate a `protected_patterns` row on the grounds it was ruled for (DIR-014).
