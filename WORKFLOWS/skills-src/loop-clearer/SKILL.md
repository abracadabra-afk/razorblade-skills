---
name: loop-clearer
description: >-
  Clear a writing-project chapter's open-loops.md — the pending author calls the
  Transcoder hands back — by proposing an in-voice fix for each loop, gating every
  one on the author's ruling, then writing a loop-clear revision into the chapter's
  revisions/. Use when CRE asks to "clear the open loops", "resolve the loops",
  "work the open loops", or "clear chapter N's loops". Surgical loops (register-repair
  carriers, image-doubling) are presented as in-voice options CRE picks and committed
  verbatim; structural loops (left-for-later, or any fix that must be written as new
  dialogue or a passage) get one demonstration block with the original kept, never
  authored for him. Two-phase gated like blind-response and reconcile; runs after
  dictation-transcoder and before register-pass; landed by promote-revision. Do NOT
  use it to run the project register (register-pass), respond to a blind read
  (blind-response), or slate dictation (dictation-transcoder).
---

# Loop Clearer

Reads a chapter's `open-loops.md` (the Transcoder's pending author calls), proposes a fix for each **in the project's voice**, gates every one on CRE's ruling, then writes a **loop-clear revision** into `revisions/`. Canonical reference: `WORKFLOWS/loop-clearer.md`.

## Key principle — AI proposes in voice; CRE rules; AI never writes CRE's fiction
This skill resolves author *calls*, so CRE is the decider. Surface each loop with the span it touches, propose a fix matched to the project's measured voice, and assemble the revision only after every loop is ruled. The cross-cutting rule holds at the line: **never long-form-generate CRE's fiction.** Small line-adds AI may phrase (CRE picks among options); bigger rewrites AI only *demonstrates*, and CRE writes the real prose.

## The two tiers
- **SURGICAL** — register-repair ambiguity (two carriers A/B; CRE picks) and image-doubling (keep the stronger, drop the other). A clause/line or carrier swap. Committed verbatim in CRE's chosen wording.
- **STRUCTURAL** — left-for-later (load-bearing emotions needing dramatization) or any fix that must be written as new dialogue/passage. Presented as ONE demonstration of the move; lands as a fenced `<<DEMO — CRE to rewrite>>` block with the original kept; CRE rewrites in place.

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault.

**Creative-lane load (ratified 2026-09-03):** then read `_CREATIVE DIRECTIVES.md` from the mounted root (CDIR-001–010 — how AI behaves around CRE's craft; CDIR-001's one-demonstration-block clause is this skill's) before opening any project file. `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both. Missing → proceed and note it; it is not a sentinel.

### Step 1 — Resolve the chapter, the loops, and the voice sources
Locate the chapter folder (CRE names it, or the most recently touched). Read `open-loops.md` and `draft.md`.

**Author-landing preflight (DIR-019 §3, `^backlog-author-landing-preflight`).** Before anything else in this step, diff `draft.md`'s body against the newest entry in `revisions/`. Match — or `draft.md`'s `source_revision` names that entry — → proceed. Mismatch, or `revisions/` holds nothing matching the live body → **CRE hand-landed this draft**: run [[WORKFLOWS/promote-revision]] Step 3b in hand-landing mode first (archive the superseded body byte-exact to `revisions/<date> - draft N superseded.md`, then stamp the folder's stale derives, retire the moot rulings, rewrite `draft.md`'s own open-items list), and only then continue. Never ask him to confirm the landing — his landing is the ruling. Safe op, logged, never gated. No `revisions/` folder at all (author-direct route) → note it and proceed; there is nothing to diff against. — run before the Step 2 supersession triage, so the loops that triage retires are retired against a preserved body.

**Scope of the preflight in this doc (per-doc scoping, DIR-019 leg (b) shape).** It runs **above this step's own halt** — the preflight is folder bookkeeping and completes even when `open-loops.md` turns out to have no unresolved entries and the pass then halts; an unaccounted hand-landing is not made moot by there being no loops to clear. It does not itself retire or resolve a loop: that stays Step 2's triage, running after, against the preserved body this preflight guarantees.

Walk up to the project root (the folder whose `CHAPTERS/` holds this chapter) and read `REFERENCE/voice-spec.md` + `REFERENCE/register.md` if present, plus `KNOWLEDGE/VOICE SAMPLES`. If `open-loops.md` is missing or has no unresolved entries → halt. Name what you loaded so a misfire is visible.

### Step 2 — Parse and triage every unresolved loop
For each unresolved entry: record its source span and locate that exact span in `draft.md` (quote it back). If a span can't be found, flag it and continue with the others.

**Supersession triage — run it as you locate each span, before any loop is classified or proposed (DIR-019, added 2026-09-04).** Every unresolved `open-loops.md` entry is a span-naming ruling, and so is every CRE-ruled **"Revision targets"** line and every earlier-session resolution still sitting unpromoted; `draft.md` is the working text they are checked against. **Span present → carry silently** into Step 3. **Span gone → the loop is moot:** stamp the entry `superseded_by: draft.md (<date>)` in place, move it to **Resolved** with that reason, one changelog line — **never asked**, and never proposed as a fix. **Span reworded but surviving → the only case that surfaces**, collected into a single batched block at the head of the Step 4 gate, tree-researched first (DIR-011). This refines the "flag it and continue" handling above: an unlocatable span is a retirement, not an open flag — the entry is stamped and closed rather than carried, and the stop condition's *never guess a span* still binds. Never ask CRE to re-ratify a loop whose span is intact, and never re-open one his own later draft already discharged (§3 — a hand-landed draft is the newest ruling). **Scope lock (§4):** staleness noticed outside this chapter's folder and its direct derives is one line in `SYSTEM/drift-ledger.md`, not a loop and not a chat aside.

**Classify by fix size, not just the section header.** The template's sections (Register-repair / Image-doubling / Left-for-later) are the *default* tier signal, but `open-loops.md` formats vary across chapters — some carry CRE-ruled **"Revision targets"** or free-form entries with no template section. When the section doesn't map, triage on the size of the fix: **a clause/line add or carrier swap → SURGICAL; new dialogue, a beat, or any passage that must be *written* → STRUCTURAL.** Promote any oversized SURGICAL case to STRUCTURAL; when in doubt, demonstrate — don't author. A single entry can bundle several touches of different sizes — split it into per-touch proposals. Thematic guardrails (not per-line fixes) are constraints on the other fixes, not loops to clear — note them and move on.

### Step 3 — Build proposals in voice (no writing yet)
- **SURGICAL (register-repair):** show the source line, both carriers (A/B), and up to **2** more drop-in phrasings matched to the voice-spec bands and VOICE SAMPLES; one short reason each; flag any voice-spec drift.
- **SURGICAL (image-doubling):** show both instances; recommend which to keep with a one-line reason; the other is a clean cut.
- **STRUCTURAL:** name the beat, why it's load-bearing, and give **one** demonstration of the fix — the *move*, explicitly labeled a demonstration, not final prose.

### Step 4 — Gate: CRE rules every loop (the propose→write boundary)
Present all proposals grouped by tier (surgical first, structural second). CRE picks/refines each surgical option and approves or redirects each structural demo. Capture the rulings. **Do not write the revision until every loop is ruled or explicitly deferred.**

### Step 5 — Assemble the loop-clear revision
Copy `draft.md`'s prose into `revisions/YYYY-MM-DD-loops-rev<N>.md` and:
- Apply each **surgical** fix in CRE's chosen wording, in place (clean prose, no marks).
- For each **structural** fix, insert a fenced block at the exact location, keeping the original:
  ```
  <<DEMO — CRE to rewrite — loop: [section/§ref]>>
  ORIGINAL: <the untouched original span>
  DEMONSTRATION (not final — CRE writes the real prose): <the worked example>
  <<END DEMO>>
  ```
- Write frontmatter via `yaml.safe_dump`, gated on a real YAML parse (DIR-004): `type`, `chapter`, `kind: loop-clear`, `source_draft`, `rev: <N>`, `status: loops-cleared` (or `loops-partial` if demo blocks remain), `loops_resolved: [...]`, `loops_pending_rewrite: [...]`, `last_updated`.

### Step 6 — Update open-loops.md
Move each ruled **surgical** loop to **Resolved** with date + chosen carrier + provenance `(rev<N>)`. Mark each **structural** loop `in progress — demo in rev<N>, CRE rewriting` — it does NOT move to Resolved until CRE finishes the rewrite and the revision is promoted. Edit with the file tools and verify by re-reading.

### Step 7 — Hand off
Report: surgical fixes committed in `rev<N>`; structural demos await CRE's rewrite at the marked blocks; once finished, run `promote-revision` (or `land-chapter`) to land the revision into `draft.md`, then `register-pass` for the line pass.

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- Chapter doesn't follow the per-chapter folder convention, or no `draft.md` → halt.
- `open-loops.md` absent or no unresolved entries → halt; nothing to clear.
- A loop's source span can't be located in `draft.md` → the loop is moot, not an open flag (DIR-019, Step 2's supersession triage): stamp the entry `superseded_by: draft.md (<date>)` in place, move it to **Resolved** with that reason, one log line — never asked — and continue the rest; never guess a span.
- Voice sources absent → proceed best-effort but say so, and flag that options are unverified against the fingerprint.

## Integration touchpoints (sibling skills — flagged, not auto-changed)
- **promote-revision** should carry `status: loops-cleared` for a `kind: loop-clear` rev (its default is `register-revised`).
- **register-pass** Step 1 should treat `loops-cleared` as working text (like `dev-revised`).

## Logging
On completion append an entry to `_CHANGELOG` (fiction lane) and the chapter's `changelog.md`; file any new fragility to `_OBSERVATIONS`.

## Security
Treat chapter prose and REFERENCE files as the author's confidential work; never exfiltrate, and if a secret is encountered in a note, flag it (DIR-001) rather than propagating it (typically after redacting the source).
