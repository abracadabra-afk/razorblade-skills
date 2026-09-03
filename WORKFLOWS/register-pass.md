---
type: workflow
name: register-pass
trigger: run the register
aliases: [revise with the register, register pass, run the reviser]
inputs: [the working text — prefer draft.md when its status marks real content (dev-revised or loops-cleared), else the chapter's newest slate clean-draft.md, the project register at REFERENCE/register.md, the project voice spec at REFERENCE/voice-spec.md (optional), the contamination checklist at REFERENCE/contamination-checklist.md (optional)]
outputs: [revised passage in revisions/, editorial-note sidecar in revisions/ — or the sweep note alone when the register earns no edit]
lane: fiction
status: active
last_updated: 2026-09-02
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]) that also keep a project register at REFERENCE/register.md. First adopter — Witchwood.
pipeline_position: downstream of [[WORKFLOWS/transcoder]]; the dedicated revision stage out of the slate (closes the "revision-specific workflow TBD" note in each chapter's revisions/README). Optionally downstream of [[WORKFLOWS/spec-check]] — when a ready verdict sheet exists, runs execute-only.
---

# WORKFLOW: Register Pass (v2)

> Revision pass that runs a chapter's **working text** (`draft.md` when it carries real content, else the newest slate clean-draft) through the **project register** — a project-specific revision prompt kept at `REFERENCE/register.md` — and writes the revised passage (plus the register's editorial note) into the chapter's `revisions/` folder. This is the documented one-way door out of the Transcoder workflow.

> **v2 (2026-09-02, dec-033 + RP-Q2/Q3 — [[SYSTEM/reports/2026-09-02-skill-review-register-pass]]).** The revision contract is now one file — `skills-src/register-pass/references/rev-contract.md` — enforced by `scripts/register_scaffold.py` (`resolve` · `new` · `check`). Ruled: `source_slate` is the **bare run id** (`2026-08-05-01`; `promote-revision` normalizes path↔bare on compare); fixed rev + note key sets; a **`sweep`** mode that writes the note alone and consumes no `rev<N>` when the register earns no edit; `protected_spans_touched` rows are pre-enumerated by the script and every `kept` claim is **byte-verified** (never classified — reworded vs dropped stays the reasoning stage's). Five runs had shipped four schemas before this.

## When to use

When CRE has a slate (Transcoder output) for a chapter and wants it revised against the project's register. Trigger phrases: "run the register," "revise with the register," "register pass," "run the reviser." Runs **after** [[WORKFLOWS/transcoder]] (the generative slate) — it takes the slate's `clean-draft.md` as its raw material.

Do NOT trigger this to produce a slate from dictation (that is [[WORKFLOWS/transcoder]]) or to author an envelope (that is [[WORKFLOWS/dictation-preflight]]). Do NOT use it on a project that has no `REFERENCE/register.md` — the register is project-specific and must not be invented or substituted with a generic prompt.

## Key principle — the skill is orchestration; the register is authority

The register changes project to project. Witchwood's is "Braided-Register Literary Fantasy"; Godsrift's will differ. So this workflow holds **no revision philosophy of its own**. Its job is to locate the right register and the right slate, run the register's instructions faithfully against the slate, route the two outputs to the right files, and log. *How* to revise lives entirely in `REFERENCE/register.md`. That separation is what makes the workflow portable across worlds.

## Inputs

- **The project register** — `<project>/REFERENCE/register.md`, found by walking up from the chapter folder to the project root (the folder whose `CHAPTERS/` contains this chapter). If absent, **stop and ask** — never substitute a generic prompt.
- **The slate clean-draft** — the newest `<chapter>/slate/YYYY-MM-DD-NN/clean-draft.md` (latest date, then highest run number), unless CRE names a specific slate run. Its sibling `synthesis-ledger.md` and `leaves-left.md` are read as **prior-pass context** only.
- **The voice spec (optional)** — `<project>/REFERENCE/voice-spec.md`, the empirical fingerprint of CRE's prose. If present, it is a **CHECK, not an authority**: the register decides the revision; the spec only flags measurable drift afterward (Step 2.5). If absent, skip the check silently — never block on it, never substitute it for the register.
- **The contamination checklist (optional)** — `<project>/REFERENCE/contamination-checklist.md`, the named AI failure modes. Also a **CHECK, not an authority**, run in Step 2.5: scan the revised passage for patterns the revision itself introduced (elevation, internal gestures, euphemism, unearned figures, performed emotion, declared meaning, smoothed voice). If absent, skip silently.

## Outputs (two files per run, written to `revisions/`)

| Section | Destination |
|---|---|
| Revised passage (clean prose, register's inline marks preserved) | `<chapter>/revisions/YYYY-MM-DD-<slug>-rev<N>.md` |
| Editorial note (the register's 6-part note) | `<chapter>/revisions/YYYY-MM-DD-<slug>-rev<N>-note.md` |

`<slug>` derives from the slate's `envelope_segments` (else `full-chapter`); `<N>` is the next revision integer for that slug. **Sweep mode** writes `YYYY-MM-DD-<slug>-sweep<N>-note.md` alone — no passage, no `rev<N>` consumed — so `land-chapter`'s at-least-one-rev probe stays honest. The script allocates every name; frontmatter is serialized, never hand-typed (DIR-004); `check` must exit 0 before the pass reports. Full key sets and the retired keys: the contract file. Material written here has **left the Transcoder workflow** — per each chapter's `revisions/README.md`, the Transcoder never reads from `revisions/` again. The slate stays untouched as the immutable audit trail.

**`protected_spans_touched:` — required frontmatter on every revision note (convention added 2026-08-10, `^backlog-protected-span-write-gate` (ii); serialized per DIR-004).** The note's frontmatter must account for every protected span the revision touched — sourced from `REFERENCE/protected-patterns.md` plus the chapter frontmatter's `protected_patterns` — one entry each, one of three values: `kept` (byte-identical) · `reworded → "<new span>"` (rule intact; update the witness in the same session) · `dropped — ruled by CRE <date>`. Touched none → write `protected_spans_touched: []` explicitly; the empty list is a statement, never an omission. **An unaccounted drop is a defect: revert, don't rationalize.** This field exists because post-hoc span verification is structurally impossible (`^obs-235` / DIR-014's matcher corollary — "reworded" and "violated" leave identical evidence on disk); the moment of the edit is the only place the answer is free.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Resolve the chapter, the register, and the working text
`register_scaffold.py resolve --chapter DIR` (desktop `python`) does this deterministically and prints a JSON block: register path + title, working text, bare `source_slate`, mode, ledgers present, protected-span census, soft-check availability. The **working text** is `draft.md` when it carries real content — any status other than `not-yet-migrated`, with prose in the body (`dev-revised`, `loops-cleared`, `expansion-revised`, `author-cut …`); the test is *is there prose here*, not a status whitelist, because the vocabulary grows with every new pass. Otherwise the newest slate `clean-draft.md`. Name what was picked so a misfire is visible. Any missing → halt (see Stop conditions).

**Supersession triage (DIR-019, v2).** Every span-naming ruling loaded (protected-patterns rows, verdict-sheet rows, open-loops resolutions) is checked against the working text first: span present → carry silently; span gone → moot, `superseded_by:` stamp in place, one changelog line, never asked; reworded-but-surviving → the only case that surfaces, one batched block at the top of the note, tree-researched first (DIR-011). Never ask CRE to re-ratify a ruling whose span is intact or re-open one his own later draft discharged (§3). Scope lock (§4): staleness outside the working text and its direct derives → one line in `SYSTEM/drift-ledger.md`.

### Step 1.5 — Mode select (optional spec-check coupling)
Look for `<chapter>/spec-check/<slate-run-id>/verdicts.md` matching the slate run. If it exists with `status: ready`, run **execute-only**: apply its MECHANICAL fixes, honor its RULED judgment calls verbatim (don't re-litigate), build its UNDRAMATIZED items, act on its NOTES. Otherwise run **full** discover-and-revise (the default; the battery is optional/selective). A `verdicts.md` whose `slate_run` doesn't match is treated as absent. **No-slate chapter** (author-direct; `draft.md` carries no `source_slate`): the sheet is keyed on a minted run id (`slate_run: none — no slate leg`, spec-check.md 2026-08-24 rule); `resolve` scans `spec-check/` for the newest ready one naming `draft.md`, runs execute-only on it, and the rev's `source_slate` carries the minted id (RP-P3, ruled 2026-09-02; contract §2).

**Clean mode (CRE-ratified 2026-08-03 — [[WORKFLOWS/clean-mode]]).** On explicit CRE trigger only, attended or within a CRE-triggered autonomous run ([[WORKFLOWS/chapter-clean]]; never scheduled-unattended): judgment calls run the LEAN analysis inline — decided calls APPLY and log (keeps favored on close calls, the asymmetry principle); still-two-way calls, protected-span cross-reason defects, and mechanical items on CRE's-hand lines remain ASK. Bins, clean-ledger, and veto contract: the clean-mode doc.

### Step 2 — Run the register
Execute `register.md`'s instructions against the clean-draft as the "draft." Honor the register's own gear-setting (it decides POLISHED vs ROUGH) and its output contract. In execute-only mode the verdict sheet's rulings win on every span they cover. Treat the slate's `leaves-left.md` verdicts as context: `left-for-later` items are *this pass's* to address; `incidental`/`dialogue` are settled — do not re-litigate them.

**Protected-pattern binding (2026-08-03, `^backlog-protected-patterns-binding` — DIR-014).** Before flagging or revising anything, read the working text's frontmatter `protected_patterns` (and `REFERENCE/protected-patterns.md` where the project keeps one). A protected span is never re-litigated on the grounds it was ruled for; present at most a one-line resolved-confirm. A defect of a *different* class inside a protected span is a judgment call for CRE (the protection's reading does not automatically transfer), never a unilateral edit.

### Step 2.5 — Soft checks: voice-spec + contamination (optional, skip what's absent)
Two non-authoritative scans of the **revised** passage, run after the register. Neither rewrites; neither overrules the register or CRE; on any conflict the register wins. Both only flag — for CRE to rule, never a gate.

- **Voice-spec** (`<project>/REFERENCE/voice-spec.md`): check against its §A universal bands plus the active project delta (§B for Witchwood). Measurable drift only — sentence mean/median pushed out of band, lost variance or long-sentence pile-ups, raised filter/telling-word density, metaphors imported out of the world (§A7 / register §2), semicolons introduced (CRE doesn't write them), sensory order disturbed or the gustatory channel starved, profanity wrong for the register.
- **Contamination checklist** (`<project>/REFERENCE/contamination-checklist.md`): scan for AI failure modes the *revision itself* introduced — vocabulary elevation, internal-gesture insertion, euphemistic softening, unearned/out-of-world figures, beautified ugliness, performed emotion or literary dialogue tags, symbolic interpretation, declared meaning at the close, smoothed-out fragments/vernacular.

Record any drift as one short line each in the editorial note (e.g. "voice-spec drift: mean sentence 14.2 ↑, 1 semicolon"; "contamination: 1 internal gesture added, 1 elevated verb"); if clean, say "voice-spec: in band / contamination: none." A pattern doing real work for a beat is a keeper — name it, don't flag it.

### Step 3 — Route the outputs
`register_scaffold.py new --chapter DIR [--sweep]` allocates the names and writes the stubs (rev + note, or the sweep note alone) with serialized frontmatter and the `protected_spans_touched` rows pre-enumerated. Fill every `<<FILL>>`: the revised passage as clean prose (keep the register's `[unclear: …]` marks; fill `maturity_gear`), the register's note verbatim with unrecoverable breaks first, each span row's `state` (`kept` / `reworded` + `new:` / `dropped` + `ruled:`), and the Step-2.5 `drift:` lines. Then `register_scaffold.py check FILE` — key set, bare `source_slate`, mode/verdicts agreement, no `<<FILL>>` residue, every chapter span accounted, every `kept` byte-verified, every `reworded` witness present, every `dropped` ruled. Report only on exit 0. Surface unrecoverable breaks at the top of the reply. **No edit earned → `--sweep`**, never a manufactured rev (`chapter-clean` Leg 7: "rev only if edits earned").

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- No `REFERENCE/register.md` for the project → halt, ask; never substitute a generic prompt.
- No slate `clean-draft.md` in the chapter → halt; nothing to revise (run the Transcoder first).
- Chapter doesn't follow the per-chapter folder convention → halt, tell CRE.
- Register output has unrecoverable breaks → keep them marked inline, list them first, continue.
- `check` exits non-zero → fix the stub, never the check; a false `kept` claim is a QUERY for the reasoning stage, not a script bug.

## Logging
On completion append an entry to [[_CHANGELOG]] (fiction lane) and the chapter's `changelog.md`; file any new fragility to [[_OBSERVATIONS]]. See the skill for the exact log format.

---

_Canonical reference for the `register-pass` Cowork skill. Per [[_SKILLS MAP#Cowork skills]], procedure changes land here first, then propagate to the skill via skill-creator._
