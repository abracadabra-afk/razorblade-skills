---
type: workflow
name: dev-draft-audit
trigger: run the draft audit
aliases: [audit the drafts, draft-audit part N, dev draft audit, audit the rough drafts]
inputs: [a folder of CRE's rendered rough-draft chapters (Google Drive or elsewhere), the target part's DEV/sequences reads + project.md act table]
outputs: [a binned punch list (MISSING / SUPERSEDED / CONTESTED / GRAIN) for CRE to rule; on ruling — recovered sequence reads (letter-suffix), verbatim draft-ref floors, harvested titles, targeted registry grain, Drive pointers on reads, micro-captured rulings, closed naming/backlog loops]
lane: fiction (dev-capture family)
status: draft
last_updated: 2026-07-08
revision_note: canon doc authored 2026-07-08 after the pattern proved 3× in one session (Part 3; Parts 5/6 interludes + cut backstory; Part 4) — see ^poe-012. .skill packaging pending a Parts-1/2 pilot + the desktop pack-skills.ps1 + Save-skill pass.
---

# WORKFLOW: dev-draft-audit

## When to use
CRE's dev notes are dictated *from skimmed memory of* rendered rough drafts that live **outside the vault** (Google Drive). That gap can silently drop a whole chapter from the dev fan (SEQ 23B and SEQ 33B were both found this way — roughly one per multi-chapter part), leave CRE's real titles unharvested behind router-derived working names, and strand load-bearing grain (in-story coinages, inscriptions, inheritance beats) on pages the notes never carried. Use this workflow whenever CRE points at a draft folder and asks to **audit the drafts** against a part's DEV reads. It is the **published-draft reconciliation sibling of `dev-capture`** — it audits what the capture layer derived against what the drafts actually hold.

**Do NOT use it** to route new dev talk (`dev-capture`), to lint capture integrity (`dev-capture-audit`), to judge readiness (`dev-readiness`), or to revise prose (never). It never treats a draft as canon.

## The governing principle
**Drafts are evidence, never authority.** The DEV tree stays canonical-at-its-layer; a draft can only (a) fill a hole or (b) surface a conflict for CRE to rule. Two supersession defaults resolve most calls before CRE has to:

1. **Newer dev outranks older drafts on STRUCTURE.** CRE's later dictation/rulings supersede draft-era staging, mechanics, and architecture (e.g. the venom's delivery, the interlude delivery-vehicle, retired subplots). Today's gut outranks last month's page.
2. **Drafts outrank the fan on RENDERED GRAIN.** In-voice dialogue, imagery, coinages, inscriptions — the material dev notes skim past — is the audit's treasure, adopted as grain and pointers, not as structure.

Everything else follows the house shape: **read-only until CRE rules;** external source of truth, the vault derives; preserve the kind; the organic-process guard (surface, never author).

## Steps

### Step 0 — Vault sentinel + scope
Confirm `_DIRECTIVES.md` frontmatter (`^obs-004`). CRE names the part and points at the draft folder. Load the part's `DEV/sequences/` reads (or their `project.md` act-table rows) and note which sequence titles are **router-derived working names** (pending CRE) — these are harvest targets.

### Step 1 — Read everything
Read **all** drafts in the folder (they are short chapters; partial reads miss the gaps this audit exists to find). Note file-ordinal vs chapter-header numbering (header typos happen; ordinals are usually authoritative) and modified dates (vintage matters for supersession).

### Step 2 — Map draft ↔ read
Build the chapter-to-sequence mapping from **internal evidence, not titles or CRE's memory** (23B's placement contradicted the stated recollection; the prose settled it — wounds, props, and callbacks date a chapter precisely). One draft may span several reads; several drafts may share one read; a draft may map to **nothing** (→ MISSING) and a read may have no draft (→ usually a newer dev invention; confirm it stands).

### Step 3 — Bin the findings
- **MISSING** — draft material absent from the fan. Recovery candidate.
- **SUPERSEDED** — draft contradicts a newer ruling/dictation. Listed, defaulted dead (recoverable via floor); flag loudly if it collides with a **same-day ruling** (the FALL-father case) rather than silently applying the default.
- **CONTESTED** — a genuine fork no ruling settles (staging, titles, thematic beats). CRE rules; never decided for him.
- **GRAIN** — rendered material worth banking: coinages, named beats, inheritance lines, corroborations of rulings. Adopt via targeted additions + pointers.

### Step 4 — Report; CRE rules
One punch list: the mapping table, then the bins with a recommendation per item (lead with the pick; don't make him rule trivia — the two defaults ARE the trivia-filter). **Write nothing until he rules.**

### Step 5 — Apply the rulings
- **Recoveries:** floor the draft **verbatim** as `_intake/_audit/<date>-<part>-draft-ref-<name>.md` (frontmatter: status, routed_to, supersession flags for dead beats/obsolete residue inside it); write the read as a **letter-suffix sequence** (`SEQ NNB`) — no renumbering mid-flow (`^ww-seq23b-renumber` collects the deferred consolidation); update neighbors' prev/next links + the act table.
- **Titles:** harvested names are CRE-named — rename files (create + delete) with a **Grep-verified wikilink sweep** (mind cloud-only files Grep can't see: check likely referencers via MCP). Close the naming backlog items.
- **Grain:** targeted additions to the touched registry entries/reads (`^poe-005` shape); **Drive pointers on every mapped read** (`Rendered draft: <folder>, CH NN`) — **pointers over mirroring**: floor whole drafts only when they are a recovery's source or ruled true-history (the interlude case); Drive stays source of truth.
- **Obsolete residue:** when a draft carries prior-architecture artifacts CRE has retired (the foundling lines), flag them in the floor's frontmatter so no future pass harvests them.

### Step 6 — Micro-capture + close loops
Record every ruling verbatim-in-spirit on the session's micro-capture floor (`^poe-004` shape), close the backlog items the audit resolves, open items for what it surfaces (title collisions, deferred renumbers).

### Step 7 — Log
`_CHANGELOG` entry under the fiction lane (mapping verdict + rulings + grain). Bump `^poe-012` (the draft-audit mode noticing) with the sighting. Ledger per the standard rule — drafts vs **landed** prose only (`^poe-006`); forward-flow parts stay dormant.

## Guards
- **Read-only until CRE rules** (Steps 0–4 write nothing).
- **Never canon** — nothing crosses into REFERENCE; this is DEV-layer work.
- **Preserve the kind** — a question a draft leaves open stays open; a mystery adopted stays a mystery.
- **No prose generation** — the audit summarizes and mirrors; it never writes CRE's fiction.
- DIR-001 (secrets), DIR-004 (serialized frontmatter where derived), DIR-005 write hygiene (file tools, verify by re-read).

## Stop conditions
- Sentinel fails → halt.
- No draft folder resolvable / empty → "nothing to audit," stop.
- The part has no DEV reads yet → wrong tool; run `dev-capture` on the material first.
- A finding would resolve an ambiguity CRE left open → surface it, never settle it.

## Relationships
`dev-capture` (the upstream router this audits) · `dev-capture-audit` (structural integrity linter — this is the *content* reconciler) · `dev-readiness` (gap-surfacing — this finds gaps *against drafts*, not against the descent) · partially absorbs `^backlog-dev-workshop` (the CONTESTED bin is the comparison surface that item sketched). Proof runs: 2026-07-08 ×3 (`^poe-012`).

## Logging
On completion: `_CHANGELOG` (fiction lane); `_POETICS` sighting bump; follow-ups to `WITCHWOOD/backlog` / `_BACKLOG`.
