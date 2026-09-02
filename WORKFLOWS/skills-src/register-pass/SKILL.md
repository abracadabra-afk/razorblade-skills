---
name: register-pass
description: Revise a chapter's working text — draft.md when it carries real content, else the newest slate clean-draft — against the project's own register (the revision prompt at REFERENCE/register.md) and write the revised passage plus the register's editorial note into the chapter's revisions/ folder. Use this skill whenever the author asks to "run the register," "revise with the register," "do a register pass," "run the reviser," or wants a chapter run through the project register under the per-chapter folder convention (slate/ + revisions/). This is the DOWNSTREAM revision stage out of the Transcoder and the developmental passes; post-v6 it usually runs as a verification sweep. Do NOT use it to produce a slate from dictation (dictation-transcoder, "slate this dictation"), to author an envelope (dictation-preflight, "prep the envelope"), to promote a revision into draft.md (promote-revision), or for the economy line edit (line-edit, "trim pass"). If the author asks to slate or transcode, route there.
---

# Register Pass (v2)

You are running a chapter's **working text** through the **project register** and routing the result into the chapter's `revisions/` folder. The register is a project-specific revision prompt that says how this world's prose should be strengthened. Your output is the revised passage plus the register's own editorial note — or, when the register earns no edit, the note alone.

You hold **no revision philosophy of your own.** The register changes project to project — Witchwood's fuses a child's fairy-tale register with adult material reality; another world's will be something else entirely. Your job is orchestration: find the right register, find the right text, run the register faithfully, route the outputs, log. *How* to revise is the register's call. Do not import rules from any other skill's revision stance, and do not soften, extend, or "improve on" the register — execute it.

Four moves, in order: **resolve**, **run**, **route**, **log**. The mechanical half of resolve and route is a script; the craft half is yours. Contract: `references/rev-contract.md` — read it once per session before you write anything. Canonical doc: `WORKFLOWS/register-pass.md`; if its head version and this file's disagree, run from the doc and announce the gap (DIR-009).

---

## Step 0 — Vault sentinel

Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → **halt and ask** which folder is the vault. Write nothing. (The script repeats this check and exits 2 on failure; the point of doing it first yourself is that a wrong mount looks like an empty vault and an empty vault looks like "fresh start-up.")

---

## Step 1 — Resolve (script)

```
python scripts/register_scaffold.py resolve --chapter "<chapter folder>" [--slate NN|YYYY-MM-DD-NN]
```

Prefer the desktop (`python` via Desktop Commander) over the sandbox — the files are local and current there, and the sandbox bash grant is denied on some seats.

It prints a JSON block. Read it instead of re-deriving any of it:

- **`register` / `register_title`** — `<project>/REFERENCE/register.md`, found by walking up to the folder whose `CHAPTERS/` holds this chapter. No register → the script halts (exit 1, `REGISTER`). So do you: never invent one, never substitute another project's, never fall back to a generic revision prompt.
- **`working_text`** — `draft.md` when it carries real content (any status that isn't `not-yet-migrated`, with prose in the body), else `slate/<newest run>/clean-draft.md`. The test is *is there prose here*, not a status whitelist: `dev-revised`, `loops-cleared`, `expansion-revised`, `author-cut …` all mean a downstream pass or CRE's own hand has already moved the text past the slate, and *that* is what the register runs on. Name the pick in your reply so a misfire is visible at a glance.
- **`source_slate`** — the bare run id (`2026-08-05-01`), normalized from whatever form `draft.md` carried.
- **`mode`** — `execute-only` when `<chapter>/spec-check/<run>/verdicts.md` exists with `status: ready` and a matching `slate_run`; otherwise `full`. A sheet for a different run is treated as absent — say so in the note rather than applying stale rulings.
- **`ledgers`** — whether the slate's `synthesis-ledger.md` / `leaves-left.md` exist (Step 2 reads them).
- **`protected_spans`** — every chapter-level `protected_patterns` span you must account for; **`protected_rules`** — how many project P-rules `REFERENCE/protected-patterns.md` carries.
- **`soft_checks`** — whether `voice-spec.md` and `contamination-checklist.md` exist (Step 2.5).

If the author named a slate run, pass `--slate`. If the chapter has neither `slate/` nor `revisions/`, the script halts (`CONVENTION`) — tell the author the project hasn't adopted the folder convention and stop.

**Clean mode** (`WORKFLOWS/clean-mode.md`, CRE-ratified 2026-08-03): on an explicit "… in clean mode" trigger, attended or inside a CRE-triggered `chapter-clean` run — never scheduled — judgment calls get the LEAN treatment: decided calls APPLY and log to the chapter's `clean-ledger.md`; still-two-way calls, protected-span cross-reason defects, and mechanical items on CRE's-hand lines stay ASK. Bins, ledger rows, and the veto contract are the clean-mode doc's, not yours to restate.

---

## Step 2 — Run the register

Load `REFERENCE/register.md` and **execute its instructions against the working text as the "draft" it asks you to revise.** Follow it to the letter: honor its gear-setting (it decides POLISHED vs ROUGH — read the whole passage, don't pre-decide); honor its output contract (revised passage, then its structured note with unrecoverable breaks first); do not add, drop, or reorder its rules. Ambiguity for this passage goes into the note, never resolved by importing a rule from elsewhere.

**Before you flag or revise anything — three bindings, in this order:**

1. **Supersession triage (DIR-019).** Every span-naming ruling you load — `protected_patterns` rows, verdict-sheet rows, open-loops resolutions — is checked against the working text first: span present → carry silently; span gone → moot, stamp the row `superseded_by: <working text> (<date>)` in place, one changelog line, never asked; span reworded-but-surviving → the only case that surfaces, as one batched `## Superseded rulings — reworded spans` block at the top of the note, tree-researched first (DIR-011). Never ask CRE to re-ratify a ruling whose span is intact, and never re-open one his own later draft discharged (§3 — a hand-landed draft is the newest ruling). Staleness outside the working text and its direct derives is one line in `SYSTEM/drift-ledger.md`, not a note item.
2. **Protected-pattern binding (DIR-014).** Read the working text's `protected_patterns` and the project's `REFERENCE/protected-patterns.md`. A protected span is never re-litigated on the grounds it was ruled for; present at most a one-line *resolved-confirm*. A defect of a *different* class inside a protected span is CRE's call, never a unilateral edit.
3. **Verdict sheet (execute-only).** Apply every MECHANICAL fix as given; honor every RULED judgment call exactly (KEEP / CUT / REWRITE-as) — do not re-open a call the author settled, even where the register's rules would tempt you; BUILD every UNDRAMATIZED item; act on the NOTES TO THE REGISTER. The register still applies to anything the sheet didn't touch, but the sheet wins on every span it covers.

**Prior-pass context — the slate's ledgers.** `leaves-left.md` is the Transcoder's record of what it deferred. `left-for-later` verdicts are load-bearing emotion deferred to *this* stage — the register's to address, not settled. `incidental` / `dialogue` / `floored` verdicts are settled — leave those spans unless the register's own rules independently touch them. `synthesis-ledger.md` flags (`[REGISTER-REPAIR]`, image-doubling) point at lines the Transcoder already knows are fragile; let the register weigh them and say in the note where you acted on one. No ledgers → proceed on the text alone; they are enrichment, not a requirement.

**Post-v6 stance.** A draft that has been through the transcoder's cold floor and the expansion passes usually arrives close to register. Expect to run as a **verification sweep**: if the register earns no edit, say so and produce the sweep note (Step 3) — do not manufacture changes to justify a rev. `chapter-clean` Leg 7 reads this pass as "rev only if edits earned."

---

## Step 2.5 — Soft checks (flag, never gate; skip what's absent)

Two non-authoritative scans of the **revised** passage, after the register. Neither rewrites; on any conflict the register wins; both only flag for CRE.

- **Voice-spec** (`REFERENCE/voice-spec.md`): measurable drift only — sentence mean/median out of band, lost variance or long-sentence pile-ups, raised filter/telling-word density, metaphors imported out of the world, semicolons introduced (CRE doesn't write them), sensory order disturbed, profanity wrong for the register.
- **Contamination checklist** (`REFERENCE/contamination-checklist.md`): failure modes the *revision itself* introduced — vocabulary elevation, inserted internal gestures, euphemistic softening, unearned or out-of-world figures, beautified ugliness, performed emotion or literary dialogue tags, symbolic interpretation, declared meaning at the close, smoothed fragments or vernacular.

One short line each into the note's `drift:` field (`voice_spec: in band` / `contamination: 1 elevated verb, 1 internal gesture`). A pattern doing real work for a beat is a keeper — name it, don't flag it.

---

## Step 3 — Route (script scaffolds, you fill, script checks)

```
python scripts/register_scaffold.py new --chapter "<chapter folder>" [--slate …] [--sweep]
```

`new` allocates `YYYY-MM-DD-<slug>-rev<N>` (slug from the slate's `envelope_segments` joined with `+`, else `full-chapter`; N is the next integer for that slug) and writes **two stubs** to `revisions/` with serialized frontmatter (DIR-004 — never hand-type the block): the rev file and its `-note.md` sidecar. With `--sweep` it writes the note alone as `…-sweep<N>-note.md` and consumes no `rev<N>`. It also prints the two changelog stubs for Step 4.

Then fill the stubs — every `<<FILL …>>` marker is yours:

- **Rev file:** the revised passage as clean prose. Keep the register's inline marks for unrecoverable text (`[unclear: "wild-out"?]`) — they are part of the passage. Fill `maturity_gear` with the gear the register chose. Nothing else in the frontmatter is yours to change.
- **Note file:** the register's full note, verbatim, in its own order — unrecoverable breaks first. Then the `protected_spans_touched` rows the script pre-enumerated: one row per chapter span, `state: kept` (byte-identical in the rev), `reworded` + `new:` (rule intact, witness changed — update the witness in the same session), or `dropped` + `ruled:` (date). **An unaccounted drop is a defect: revert, don't rationalize.** `[]` when the chapter has none means "I looked." Then `drift:` from Step 2.5.
- **Sweep note:** what the register checked, what it found clean, what would have been an edit and why it was not earned. It is the receipt for "the register ran and changed nothing."

```
python scripts/register_scaffold.py check "<revisions/…-rev<N>.md>"      # or the note; it finds the pair
```

`check` must exit 0 before you report: key set, bare `source_slate`, mode/verdicts agreement, no `<<FILL>>` residue, non-empty rev body, every chapter span accounted, every `kept` claim **byte-verified against the rev — or, on a sweep, against the working text** (RP-Q3 / RP-P1 — a `kept` row whose span is not found verbatim fails; the script never decides whether that means reworded or dropped, it only says the claim is false, and that is your QUERY to resolve before shipping), every `reworded` `new:` present, every `dropped` ruled.

**One-way door.** Material in `revisions/` has left the Transcoder workflow: the Transcoder never reads from `revisions/` again, and the slate you read stays exactly as it was. Say so plainly in your reply. If the register flagged unrecoverable breaks, they lead your reply — that is the one thing that must not get buried.

---

## Step 4 — Log

Append the script's two stubs, filled in: one line to the chapter's `changelog.md`, one entry to the vault `_CHANGELOG.md` (fiction lane, top-insert, file tools, verify by re-read — DIR-005): working text, `source_slate`, register title + mode, the files written, span accounting counts, unrecoverable breaks. New fragility → `_OBSERVATIONS.md` (`^obs-NNN`, re-scan the max anchor immediately before writing).

---

## Files this skill writes — and must not

**Writes:** `<chapter>/revisions/YYYY-MM-DD-<slug>-rev<N>.md` + `…-rev<N>-note.md` (or `…-sweep<N>-note.md`); `<chapter>/changelog.md`; vault `_CHANGELOG.md`; `superseded_by:` stamps on moot rows (DIR-019 §1); `<chapter>/clean-ledger.md` rows in clean mode only.

**Must NOT write:** `draft.md` (that is `promote-revision`'s one job); anything under `slate/` (immutable audit trail); `envelope.md`, `open-loops.md`, `continuity.md`, `notes.md`, `_status.md` (read-only context here); `REFERENCE/register.md`, `REFERENCE/protected-patterns.md` beyond a witness refresh you accounted for in the note. If a span you would revise lives in one of those files, stop — you are in the wrong stage.

---

## Stop conditions

- Sentinel fails → halt, ask which folder is the vault.
- No `REFERENCE/register.md` for the project → halt, ask; never substitute a generic prompt.
- No real `draft.md` and no slate `clean-draft.md` → halt; nothing to revise (run the Transcoder first).
- Chapter lacks `slate/` and `revisions/` → halt, tell the author.
- `check` exits non-zero → fix the stub, never the check; report only on exit 0.
- Register output has unrecoverable breaks → keep them marked inline, list them first, continue.

---

_Canonical reference: [[WORKFLOWS/register-pass]]. Per [[_SKILLS MAP#Cowork skills]], procedure changes land in the workflow doc first, then propagate here via skill-creator. v2 — 2026-09-02: rev contract (dec-033), `register_scaffold.py`, sweep mode, DIR-014 / DIR-019 bindings, Step 2.5 soft checks._
