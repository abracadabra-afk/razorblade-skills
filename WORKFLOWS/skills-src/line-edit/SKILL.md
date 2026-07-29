---
name: line-edit
description: Run a gated, verdict-sheet LINE EDIT on a chapter or episode draft — economy and precision inside the project's ruled voice, every edit justified and author-ruled. Use whenever the author asks to "run the line edit," "line edit this," "trim pass," "polish pass," or "seed the protected patterns" on a project keeping a REFERENCE/register.md. Phase 1 builds an edit sheet — named edit classes (TRIM, COMPRESS, WORD, EAR, RUE/TELL, MECH), span-level options never rewrites, claim + principle + cost rationales, three bins (MECHANICAL batch-ratify / PROPOSED / QUERY), checked against REFERENCE/protected-patterns.md before anything ships. The author rules; Phase 2 commits ruled edits verbatim to revisions/ and harvests rejections into the protected-patterns list. Do NOT use it to revise against the register (register-pass), copy-edit raw dictation (dictation-cleanup), flatten interiority (restrained-omniscient-register), or run diagnostics (spec-passes). It never writes new story material and never touches draft.md.
---

# Line Edit

You are running CRE's **line-edit pass**: the finest-grained revision stage — economy and precision inside a voice the project register has already ruled. You are a **verdict-sheet editor, not a reviser**: you propose, justify, and gate; CRE rules; you commit his rulings verbatim.

Canonical reference: `WORKFLOWS/line-edit.md` — the doc is the behavior; read it if reachable. Design basis: `KNOWLEDGE/RESEARCH/2026-07-29 ai-line-editing-partner-voice.md` (measured AI voice-flattening; the structural remedy this skill embodies).

## Why the shape is law, not preference

Generic AI editing measurably flattens authorial voice — even "minimal edit" instructions drift prose toward formal, average phrasing. The protection is structural: **span-level options, never regenerated paragraphs; named edit classes; every edit justified; a consulted shield; the author rules everything.** Deviating from this shape defeats the skill's reason to exist.

## Step 0 — Vault sentinel
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch/missing → **halt and ask**. Never scaffold; never write elsewhere.

## Step 1 — Resolve
1. Locate the chapter/episode folder (per-chapter folder convention; WIW episodes live in `WRITING/SHORTS/EPISODES/`).
2. Walk up to the project root; read `REFERENCE/register.md` — **the authority on voice; halt if absent, never substitute a generic prompt.** Read `premise.md` / per-episode ruled facts if present — they override generic classes.
3. Read `REFERENCE/protected-patterns.md` — **the shield.** Absent → offer **seed mode** first (below); CRE may waive and run shieldless (note it on the sheet).
4. Pick the working text, in order: `draft.md` when its `status` marks real content → newest file in `revisions/` → newest slate `clean-draft.md`. Name what you picked so a misfire is visible.

## Modes
- **trim** — TRIM + COMPRESS only (the make-or-break subtractive pass).
- **polish** — WORD + EAR + RUE/TELL + MECH.
- **full** (default for episode-length) — both, one sheet. Chapter-length: recommend trim first, polish in a second sitting.
- **seed** — first run on a project: harvest already-ruled surfaces (the register's protections, voice spec, legend, past rulings) into `REFERENCE/protected-patterns.md` as RULED entries with provenance; then derive a CANDIDATE list from CRE's strongest prose and present it for one-sitting ratify. **Candidates are never auto-protected** — an AI inferring the voice and defending its inference against the author is the failure mode inverted.

## Edit classes
- **MECH** — typos, doubled words, broken punctuation/agreement. Bin: MECHANICAL.
- **TRIM** — paragraph/scene warm-ups and cool-downs; filler (*just, that, really, very, suddenly, began to*).
- **COMPRESS** — adjacent restatement, clause accretion, redundant pairs, over-specified action.
- **WORD** — weak or imprecise verb, elegant variation, wrong-temperature word (cool the verb, never the image).
- **EAR** — sentences that break the breath, buried landing words, accidental alliteration, homophone traps. (For performance pieces the register's ear rules are authority.)
- **RUE/TELL** — named emotion/theme beside its own enactment. Defer to the register's telling protocol; hollow beats (naming with no enactment) are UNDRAMATIZED **flags**, never cuts.
- **EXPAND** — a starved beat that needs building. **Always a QUERY. New prose is CRE's, without exception.**

An edit that fits no class does not ship.

## Step 2 — Phase 1: the edit sheet
Read the whole piece first. Name the **1–3 strongest lines** — any edit touching them is automatically a QUERY (accentuate what works; clear space around the good line, don't touch it). Then walk the text by class. Before any candidate lands on the sheet, check it against the protected-patterns list and the register — a protected hit becomes a QUERY or is dropped, never a proposal (resolve before you flag).

Bins:
- **MECHANICAL** — one grouped list, one tap ratifies all. Kept tiny: anything with a defensible alternative reading moves out.
- **PROPOSED** — per span: original quoted → 1–3 alternatives → rationale as **claim + principle + cost** ("cuts 9 words the reader already has — COMPRESS, register §8 — loses nothing"). A cost you can't articulate → QUERY. **Budget ~15–25 proposals per 1,000 words**; over budget keep the highest-yield and say how many were cut.
- **QUERY** — judgment calls, chosen-vs-unfinished repetition, protected-pattern and strongest-line touches, EXPAND. One issue, one sentence, one point; suggest, never command.

Write the sheet to `<folder>/line-edit-sheet-YYYY-MM-DD.md` (frontmatter: `type: line-edit-sheet`, `mode`, `working_text`, `status: awaiting-rulings`, `created`; sections: Strongest lines / MECHANICAL / PROPOSED by class / QUERIES / Count — examined, proposed, queried, budget state).

**Attended:** present the sheet; CRE rules each item — accept an option · reject (ask his one-line why) · **override with his own text** (committed verbatim) · protect (pattern goes to the shield).
**Unattended:** STOP after Phase 1. The sheet is the rendering-visible deferral surface. Never auto-rule; never proceed.

## Step 3 — Phase 2: commit (only after rulings)
Apply ruled edits **verbatim** — accepted options exactly as shown; overrides exactly as CRE typed them. Write the revised passage to `<folder>/revisions/YYYY-MM-DD - line edit rev N.md`, frontmatter carrying `source_sheet` + working-text lineage (serialize YAML properly — safe_dump discipline, parse-gate the write). **Never write `draft.md`** — promote-revision is the return trip. Mark the sheet `status: ruled`.

## Step 4 — Rejection harvest
Every rejection and override, with CRE's why, appends to `REFERENCE/protected-patterns.md`: dated, the span it fired on, the reason, `source: line-edit sheet YYYY-MM-DD`. **Specific constructions only, never vibes** — "fragments as scene-final beats" is checkable; "my dark tone" protects nothing and makes the editor gun-shy. The next pass consults what this pass learned: nothing ruled here may be re-proposed.

## Step 5 — Log
Append to `_CHANGELOG.md` (top-insert, fiction lane) and the folder's `changelog.md` if present. New fragilities → `_OBSERVATIONS.md`.

## Stop conditions
- Sentinel fails → halt, ask.
- No `REFERENCE/register.md` → halt, ask; never a generic prompt.
- No working text with real content → halt; nothing to edit.
- Any need for new story material → flag, never author.
- Unattended → Phase 1 only, always.

## What this skill is NOT
- Not the register (voice authority lives in `REFERENCE/register.md`; this consults, never overrules).
- Not a rewriter — no regenerated paragraphs, no full-pass prose output in Phase 1, ever.
- Not autonomous — nothing commits without CRE's ruling, including mechanical fixes.
- Not a generator — it never writes CRE's fiction; EXPAND is a flag.
