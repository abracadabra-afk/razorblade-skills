---
name: dev-draft-audit
description: Reconcile a fiction part's DEV/ reads against CRE's rendered rough drafts (which live OUTSIDE the vault, in Google Drive) — the published-draft reconciliation sibling of dev-capture. Use whenever CRE points at a draft folder and asks to "run the draft audit," "audit the drafts," "audit the rough drafts," or "draft-audit part N." It maps chapter-to-sequence from internal evidence, then bins every finding MISSING / SUPERSEDED / CONTESTED / GRAIN for CRE to rule — recovering dropped chapters (SEQ 23B and 33B were both found this way), harvesting his real titles from behind router-derived working names, and banking rendered grain (coinages, inscriptions, inheritance beats) the dev notes skimmed past. Drafts are EVIDENCE, never authority — read-only through the report; it writes only after CRE rules, and never into REFERENCE canon. Do NOT use it to route new dev talk (dev-capture), lint capture integrity (dev-capture-audit), judge readiness (dev-readiness), or revise prose (never).
---

# dev-draft-audit

You are reconciling a part's **DEV/ reads** against the **rendered rough drafts** CRE actually wrote. His dev notes are dictated *from skimmed memory of* those drafts, and the drafts live outside the vault — so the fan silently drops chapters, keeps working names over his real titles, and strands load-bearing grain on pages the notes never carried. You close that gap.

Canonical reference: `WORKFLOWS/dev-draft-audit.md`. This is the AI-trigger surface; that doc is the in-vault canon.

---

## The governing principle

**Drafts are evidence, never authority.** The DEV tree stays canonical-at-its-layer; a draft can only (a) fill a hole or (b) surface a conflict for CRE to rule. Two supersession defaults resolve most calls before he has to:

1. **Newer dev outranks older drafts on STRUCTURE.** Later dictation/rulings supersede draft-era staging, mechanics, and architecture. Today's gut outranks last month's page.
2. **Drafts outrank the fan on RENDERED GRAIN.** In-voice dialogue, imagery, coinages, inscriptions — the material dev notes skim past — is the audit's treasure, adopted as grain and pointers, not as structure.

The two defaults ARE the trivia-filter: they exist so CRE rules only on genuine forks.

---

## Step 0 — Vault sentinel + scope
Read `_DIRECTIVES.md` from the mounted root; confirm `type: ai-os-brain` + `file: directives` (`^obs-004`). Mismatch/missing → halt and ask which folder is the vault. CRE names the part and points at the draft folder. Load the part's `DEV/sequences/` reads (or the `project.md` act-table rows) and note which sequence titles are **router-derived working names** pending CRE — those are harvest targets.

## Step 1 — Read everything
Read **all** drafts in the folder. They are short chapters; a partial read misses exactly the gaps this audit exists to find. Note file-ordinal vs chapter-header numbering (header typos happen — ordinals are usually authoritative) and modified dates (vintage decides supersession).

## Step 2 — Map draft ↔ read
Build the mapping from **internal evidence, not titles or CRE's memory** — 23B's placement contradicted the stated recollection and the prose settled it; wounds, props, and callbacks date a chapter precisely. One draft may span several reads; several drafts may share one read; a draft may map to **nothing** (→ MISSING) and a read may have no draft (→ usually a newer dev invention; confirm it stands).

## Step 3 — Bin the findings
- **MISSING** — draft material absent from the fan. Recovery candidate.
- **SUPERSEDED** — draft contradicts a newer ruling/dictation. Listed, defaulted dead (recoverable via floor). Flag **loudly** when it collides with a same-day ruling (the FALL-father case) instead of silently applying the default.
- **CONTESTED** — a genuine fork no ruling settles (staging, titles, thematic beats). CRE rules; never decided for him.
- **GRAIN** — rendered material worth banking: coinages, named beats, inheritance lines, corroborations of rulings.

## Step 4 — Report; CRE rules
One punch list: the mapping table, then the bins, each item with a lead-with-the-pick recommendation. **Write nothing until he rules.**

## Step 5 — Apply the rulings
- **Recoveries:** floor the draft **verbatim** as `_intake/_audit/DATE-PART-draft-ref-NAME.md` (frontmatter: status, routed_to, supersession flags for dead beats/obsolete residue inside it); write the read as a **letter-suffix sequence** (`SEQ NNB`) — no renumbering mid-flow (`^ww-seq23b-renumber` collects the deferred consolidation); update neighbors' prev/next links + the act table.
- **Titles:** harvested names are CRE-named — rename files (create + delete) with a **Grep-verified wikilink sweep**; mind cloud-only files Grep cannot see (check likely referencers via the file tools). Close the naming backlog items.
- **Grain:** targeted additions to the touched registry entries/reads (`^poe-005` shape) + a **Drive pointer on every mapped read** (`Rendered draft: FOLDER, CH NN`). **Pointers over mirroring** — floor a whole draft only when it is a recovery's source or ruled true-history (the interlude case). Drive stays source of truth.
- **Obsolete residue:** when a draft carries retired prior-architecture artifacts (the foundling lines), flag them in the floor's frontmatter so no future pass harvests them.

## Step 6 — Micro-capture + close loops
Record every ruling verbatim-in-spirit on the session's micro-capture floor (`^poe-004` shape). Close the backlog items the audit resolves; open items for what it surfaces (title collisions, deferred renumbers).

## Step 7 — Log
`_CHANGELOG` entry under the fiction lane (file tools — DIR-005): mapping verdict + rulings + grain. Bump `^poe-012` (the draft-audit mode noticing) with the sighting. Ledger per the standard rule — drafts vs **landed** prose only (`^poe-006`); forward-flow parts stay dormant.

---

## Files this skill writes — and must not
**Writes (only after CRE rules):** `_intake/_audit/` floors, recovered sequence reads, targeted registry/read additions + Drive pointers, renamed files, the micro-capture floor, `_CHANGELOG` / `_POETICS` / backlog entries.
**Must NOT write:** anything into `REFERENCE/` canon (this is DEV-layer work); any prose; anything at all during Steps 0–4.

## Guards
- **Read-only until CRE rules** (Steps 0–4 write nothing).
- **Never canon** — nothing crosses into REFERENCE.
- **Preserve the kind** — a question a draft leaves open stays open; a mystery adopted stays a mystery.
- **No prose generation** — the audit summarizes and mirrors; it never writes CRE's fiction.
- DIR-001 (secrets), DIR-004 (serialized frontmatter where derived), DIR-005 write hygiene (file tools, verify by re-read).

## Stop conditions
- Sentinel fails → halt.
- No draft folder resolvable / empty → "nothing to audit," stop.
- The part has no DEV reads yet → wrong tool; run `dev-capture` on the material first.
- A finding would resolve an ambiguity CRE left open → surface it, never settle it.

## What this skill is NOT
- Not `dev-capture` (never routes new dev talk).
- Not `dev-capture-audit` (that lints structure; this reconciles content).
- Not `dev-readiness` (that finds gaps against the descent; this finds them against drafts).
- Never a reviser. A draft is evidence, not a place to edit.
