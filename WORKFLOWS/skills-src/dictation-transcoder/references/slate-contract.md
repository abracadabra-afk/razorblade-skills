# The slate contract (v6.1 — ruled 2026-09-02)

This is the single statement of what a transcoder run writes. `scripts/slate_scaffold.py` enforces it (`new` writes it, `check` verifies it); the canon `WORKFLOWS/transcoder.md` and `chapter-init`'s slate-README point here. If this file and a run disagree, the run is wrong.

Why one file: between 2026-06 and 2026-08 five runs shipped five different frontmatter schemas, one run shipped two of the four files, and a key rename (`envelope_segments` → `segments`) silently broke `register-pass`'s slug derivation. Every consumer that reads a slate reads *this* shape.

---

## 1. Folder

```
<chapter>/slate/YYYY-MM-DD-NN/
├── clean-draft.md
├── cut-log.md
├── synthesis-ledger.md
└── leaves-left.md
```

- `YYYY-MM-DD` is the run date; `NN` is two digits, first free number for that date starting at `01`. The script allocates it.
- **Exactly four files, every run** — including derived runs (§ 5). `register-pass` reads `leaves-left.md` "if present" and cannot tell *absent* from *empty*; a missing file lies to it.
- **Immutable once written.** No run is ever edited after its `generated` stamp. Changes go into a new derived run (§ 5). The one file that may legitimately appear beside the four is `clean-ledger.md` — and it should not be here either (§ 6).

## 2. Frontmatter — identical block in all four files

```yaml
---
source_dictation: dictation/<filename>.md
envelope_segments: [seg-one, seg-two, seg-three]
generated: '2026-09-02 14:05'
transcoder_version: v6.1
tense: past
status: floor-draft
---
```

Optional keys, present only when true:

```yaml
supersedes: slate/2026-09-02-01
derived_from: slate/2026-09-02-01
```

| key | type | who reads it |
|---|---|---|
| `source_dictation` | string, path relative to the chapter folder | the script's dictation pick (a dictation with a run is not re-picked); audit |
| `envelope_segments` | **list** of segment slugs, in order | `register-pass` — joins them with `+` for its revision slug; `chapter-clean` Gate A |
| `generated` | quoted `'YYYY-MM-DD HH:MM'` | `check` — a `clean-draft.md` modified long after this stamp was edited in place (§ 5) |
| `transcoder_version` | `vN.N`, read from the canon doc head, not typed | `skill-audit`; the version-announce guard |
| `tense` | `past` / `present` (+ ` — seam kept` when a ruled line differs) | expansion, register-pass |
| `status` | `floor-draft` · `gate-pending` · `gated` · `derived` | `chapter-clean` (gate state), `promote-revision` |
| `supersedes` | run path | audit trail |
| `derived_from` | run path | § 5; `check` |

Retired — never write these: `segments` (any form), `type`, `chapter`, `file`, `run` (all redundant with the path), `word_count`, `coverage`, `register`, `floor`, `generated_by`, `transcoder`, `last_updated`. Anything else worth saying goes in the ledger body, not the frontmatter.

Frontmatter is **serialized, never hand-typed** (DIR-004). The script emits it and parse-gates it; a run whose block fails to parse fails `check`.

## 3. The four files

### `clean-draft.md`
The floor draft — prose in the floor register (`KNOWLEDGE/PROSE FRAMEWORK/narrator-rules`), nothing else. One `# Floor draft — <chapter> (slate YYYY-MM-DD-NN)` heading, then the prose.

Inline markers — the only text in the draft that is not prose:

| marker | meaning | cleared by |
|---|---|---|
| `<<GARBLE-UNRESOLVED: G1>>` | a meaning-splitting STT garble on a line the machine may not guess | CRE's words |
| `<<OPTIONED-N>>` | two-way register call; both carriers in the ledger | CRE picks; a derived run applies it |
| `<<REGISTER-AMBIGUOUS: see synthesis-ledger.md#cluster-N>>` | register-repair whose direction the text does not settle | CRE picks |
| `<<AUTHOR-GAP: label>>` | a hole only CRE's words fill (a climax line, a planted beat that never arrived) | CRE's words, in a derived run |

**The gate is open while any marker remains.** `check` counts them; zero markers is a machine-readable "gate clearable", not "gate cleared" — the seam flags and scene map are CRE's regardless.

### `cut-log.md`
One line per cut span: `- "the span" — reason`. Six reasons, no others:

`unperceived` · `too-fine` · `narrator-injection` · `modifier` · `frame` · `mechanical`

`frame` = dictation meta-narration ("the story opens with", "cut to", self-repairs). `mechanical` = a single-reading STT fix ("unkept" → "unkempt"), logged so nothing is silently changed. Terse — this file exists so CRE can re-add anything load-bearing on the next dictation.

### `synthesis-ledger.md`
The audit trail and the gate surface. Fixed section order; a section with nothing in it is present with one line saying so (an absent heading reads as "not checked").

1. `## Mic metadata` — frame-talk that carried information rather than story: a title spoken at the mic, scene/segment cues, any runway or brief `<<UNCERTAIN>>` flag the dictation answered. Recorded, never actioned. (Reports what the mic said; never grades the draft against the plan — DIR-017.)
2. `## Reconciler restorations` — when the dictation arrived with a name-reconciler corrections table: every multi-word-term hit below 1.00 the run judged wrong and restored to the dictated phrase. Nothing here = table read, nothing restored.
3. `## Ruled lines — preserved` — author-ruled verbatim lines carried byte-exact (DIR-014).
4. `## Clusters collapsed` — per cluster: payload → carrier → notes (dropped beat, dead modifier, verb change, image doubled across lines with both shown).
5. `## Floor ledger` — Operation 3, one line each: original span → floored span → rule cited. `filter-kept: registering is the event` rows live here too.
6. `## Heat bank` — dictated warm/hot language the floor stripped, **verbatim, per beat**. Never discarded, never invented.
7. `## Optioned` — every two-way call: both carriers, the reading behind each, which is in the draft.
8. `## Register repair` — every carrier that rendered an unnamed emotion structurally (`[REGISTER-REPAIR]`), the riskiest output.
9. `## Contamination check` — patterns caught and removed from invented carriers (`REFERENCE/contamination-checklist.md`).
10. `## Garbles` — G-numbered; the meaning-splitting ones left as markers, the mechanical ones summarized.
11. `## Developmental-seam flags` — the spine-review gate's observations, each tree-researched first (DIR-011).
12. `## Scene map` — v6.1: per scene (what happens · derived goal · turn), per exchange ([SP] function tag), function-level beat census with dialogue included. Observations and counts, never verdicts.
13. `## Continuity touched` — entities synthesis dropped that a later section may need; CRE's to log.

### `leaves-left.md`
Per segment, every named-emotion or dissolved-telling span left standing, each with one verdict. Present for **every** segment, including ones with no cuts — an empty segment is a re-read signal, not a clean bill.

Verdicts, exactly these: `incidental` · `dialogue` · `floored` · `optioned` · `repaired` · `dilution`

`dilution` is the grouped verdict: a state named 3+ times in a segment is one entry — state, count, strongest instance, `dilution — keep [strongest], the other namings thin it`. `left-for-later` is retired (v6): a register breach left standing is a defect, not a deferral.

## 4. Gate states

`floor-draft` (written, gate not yet presented) → `gate-pending` (presented to CRE) → `gated` (every seam, optioned call, and garble ruled; markers may still stand as AUTHOR-GAP until a derived run fills them). The status lives in the frontmatter of the run that carries it; a later derived run carries the new state.

## 5. Derived runs (ruled 2026-09-02)

A derived run is how anything changes after a run is written: applying gate rulings, restoring an optioned carrier, **and CRE's own author-gap words**. Never edit an existing run — not for a ruling, not for a one-word fix, not for the author's hand. Every slate folder is a frozen witness.

`scripts/slate_scaffold.py derive --parent NN`:
- allocates the next run for today, copies **all four files** from the parent (Q3 — the parent's cut-log and leaves-left come along verbatim), sets `derived_from` and `supersedes` to the parent, re-stamps `generated`, sets `status: derived`;
- the edits then happen in the new run's `clean-draft.md` (and ledger, to record what was applied);
- `check --against PARENT` afterwards prints the paragraph diff: *N differing / M identical* — the receipt that says exactly what changed.

Author gaps: CRE writes into the derived run, not into the gated run and not into `draft.md` (`chapter-clean` Step 2 wording updated to match). Stitch to `draft.md` happens from the derived run.

## 6. Files this run does not write

`draft.md` · `open-loops.md` · `continuity.md` · `notes.md` · anything in `revisions/` · **`clean-ledger.md`**.

The clean-ledger (clean-mode bin events, `WORKFLOWS/clean-mode`) lives at **`<chapter>/clean-ledger.md`** — chapter root, appended per leg (ruled 2026-09-02, per `chapter-clean` Step 3). A `clean-ledger.md` inside a slate run is a placement error; `check` reports it as WARN so the Gate A accounting can append it to the root file. It is never moved by a pass.

## 7. Logging stubs

The script prints both; the model completes the counts.

Vault `_CHANGELOG.md` (top-insert):
```
## YYYY-MM-DD — [fiction] transcoder run on <chapter>
**Ran:** Transcoder vN.N on <chapter> · segments: a+b+c · dictation: <file>
**Shipped:** slate/YYYY-MM-DD-NN/ (4 files) · N floor normalizations · N heat-bank entries · N optioned · N garbles open
**Gate:** <open: N markers, N seam flags> | <cleared>
**Open loops:** <pointers into the synthesis ledger>
```

Chapter `changelog.md` (that file's own format, newest at top):
```
## YYYY-MM-DD — transcoder vN.N — slate run NN
**Ran:** <segments>
**Slate run:** `slate/YYYY-MM-DD-NN/`
**Open loops:** <pointers>
**Notes:**
```
