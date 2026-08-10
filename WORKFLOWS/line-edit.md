---
type: workflow
name: line-edit
trigger: run the line edit
aliases: [line edit this, trim pass, polish pass, seed the protected patterns]
inputs: [the working text — draft.md when its status marks real content, else the newest revision or slate clean-draft, the project register at REFERENCE/register.md (authority on voice), the protected-patterns list at REFERENCE/protected-patterns.md (the shield), optional scene-intensity read]
outputs: [edit sheet in the chapter/episode folder (Phase 1), ruled-edits revision in revisions/ (Phase 2), rejection-harvest appends to REFERENCE/protected-patterns.md]
lane: fiction
status: draft — spec authored 2026-07-29 from [[KNOWLEDGE/RESEARCH/2026-07-29 ai-line-editing-partner-voice]]; packs after 2–3 live runs
last_updated: 2026-08-10
scope: Any project keeping a REFERENCE/register.md (WIW episodes first adopter; Witchwood chapters when revisions unpause). Requires revisions/ per the folder convention.
pipeline_position: downstream of [[WORKFLOWS/register-pass]] (register = voice conformance; line-edit = economy + precision inside the ruled voice), upstream of record/bank. Landed by [[WORKFLOWS/promote-revision]]. Never a precondition at the mic (DIR-017).
---

# WORKFLOW: Line Edit

> A **gated, verdict-sheet line editor** — not a reviser. Phase 1 reads the working text against the project register + protected-patterns list and produces an **edit sheet**: every proposed change as a span with options and a justified rationale, binned MECHANICAL / PROPOSED / QUERY. CRE rules the sheet. Phase 2 commits ruled edits **verbatim** into `revisions/` and harvests every rejection into the protected-patterns list. The design is the researched remedy to measured AI voice-flattening: named edit classes, span-level options never rewrites, claim + principle + cost rationales, a consulted style sheet, author rules everything.

## When to use

After the register pass has run (or on a draft CRE calls line-ready), before recording/banking. Triggers: "run the line edit," "line edit this," "trim pass," "polish pass." First-run seeding: "seed the protected patterns."

Do NOT use it to: revise against the register (that is [[WORKFLOWS/register-pass]] — it holds the voice authority this skill only consults); copy-edit raw dictation ([[WORKFLOWS/dictation-cleanup]]); flatten interiority ([[WORKFLOWS/restrained-omniscient-register|restrained-omniscient-register]] — and note the WIW register explicitly bans that stance); run the diagnostic battery (spec-passes); or write new story material — **ever**. EXPAND findings are flags, not prose.

## Key principles (from the research briefing — the load-bearing five)

1. **Edit classes, not "editing."** Every proposal carries a named class (below). An edit that fits no class doesn't ship.
2. **Spans + options, never rewrites.** Per-span: original → 1–3 alternatives → rationale. Never a regenerated paragraph — full regeneration is where the measured voice-drift lives.
3. **Rationale = claim + principle + cost.** "Cuts 9 words the reader already has (COMPRESS, register §8); loses nothing." An edit whose cost can't be articulated becomes a QUERY.
4. **The shield is consulted, not remembered.** `REFERENCE/protected-patterns.md` is read before proposing; nothing is proposed against a protected entry — it may only be queried. Rejections append to it with provenance (the DIR-014 loop).
5. **Nothing writes without a ruling.** Even MECHANICAL is approve-then-commit — batched to one tap, never auto-written.

## Edit classes

| Class | What it catches | Default bin |
|---|---|---|
| **MECH** | typos, doubled words, broken punctuation/agreement | MECHANICAL (one batch) |
| **TRIM** | scene/paragraph warm-ups and cool-downs; filler words (*just, that, really, very, suddenly, began to*) | PROPOSED |
| **COMPRESS** | adjacent restatement, clause accretion, redundant pairs, over-specified action (register §8 is authority) | PROPOSED |
| **WORD** | weak/imprecise verb, elegant variation, wrong-temperature word (cool the verb, not the image — register §3) | PROPOSED |
| **EAR** | breath-busting sentences, buried landing words, accidental alliteration/tongue-twisters, homophone ambiguity (register §7 is authority) | PROPOSED |
| **RUE/TELL** | named emotion or theme beside its own enactment (register §5 is authority; UNDRAMATIZED verdicts stay flags) | PROPOSED or QUERY |
| **EXPAND** | compression starved a beat; something needs building | QUERY always — new prose is CRE's |

## The three bins

- **MECHANICAL** — presented as one grouped list, ratified in a single tap. Kept tiny: anything with a defensible alternative reading leaves this bin.
- **PROPOSED** — the sheet proper: span / options / rationale, grouped by class. **Budget: ~15–25 proposals per 1,000 words** (start point per the briefing — tune against how the sheets feel to rule). Over budget → keep the highest-yield, note the count cut.
- **QUERY** — judgment calls, chosen-vs-unfinished repetition, anything touching a protected pattern or a strongest line, EXPAND, anything whose cost is real. One issue, one sentence, one point — suggesting, never commanding.

**Strongest lines:** Phase 1 names the 1–3 strongest lines in the piece. Any edit touching them is automatically a QUERY. This operationalizes "accentuate what works."

## Modes

- **trim** — TRIM + COMPRESS only (the make-or-break subtractive pass; densest sheet).
- **polish** — WORD + EAR + RUE/TELL + MECH.
- **full** (default for episode-length pieces) — both, one sheet grouped by class. For chapter-length work prefer two sittings: trim first, polish after trim lands.
- **seed** — first-run per project: harvest already-ruled surfaces (register, voice spec, legend, rulings) into `REFERENCE/protected-patterns.md` as RULED entries with provenance, then derive a CANDIDATE sheet from CRE's strongest prose for one-sitting ratify. Candidates are never auto-protected.

## Steps

### Step 0 — Vault sentinel
`_DIRECTIVES.md` frontmatter `type: ai-os-brain` + `file: directives`, or halt (`^obs-004`).

### Step 1 — Resolve
Locate the chapter/episode folder; walk up to the project root; read `REFERENCE/register.md` (halt if absent — never substitute) and `REFERENCE/protected-patterns.md` (absent → offer **seed** mode first; CRE may waive and run shieldless, noted in the sheet). Pick the working text: `draft.md` when its status marks real content, else newest revision in `revisions/`, else newest slate clean-draft. Name what you picked. Read `premise.md`/ruled facts if present — per-episode rulings override generic classes. **Check for a staged line-edit queue:** if a [[WORKFLOWS/panel-response]] run exists for this text, its `panel/<run>/response-rulings.md` carries a "Line-edit queue" section of CRE-ruled deferrals (DIR-014 binding surface) — load it; queue items are mandatory sheet candidates, and its protected-patterns section extends the shield for this piece. (Added 2026-07-29 after live run 1, where the queue was consumed by same-session context rather than by rule.)

### Step 2 — Phase 1: build the edit sheet
Read the whole piece first. Name the strongest 1–3 lines. Then walk the text by class per the active mode, checking every candidate against the protected-patterns list and the register **before** it lands on the sheet (DIR-011 — the tree answers first; a protected hit becomes a QUERY or is dropped). Write the sheet to `<folder>/line-edit-sheet-YYYY-MM-DD.md`:

```
---
type: line-edit-sheet
mode: trim | polish | full
working_text: <path picked>
status: awaiting-rulings
created: YYYY-MM-DD
---
## Strongest lines (protected this pass)
## MECHANICAL (one tap ratifies all)
## PROPOSED — <class>
   N. [span quoted] → option A / option B — rationale (class, principle §, cost)
## QUERIES
## Count — spans examined / proposed / queried; budget state
```

**Attended:** present the sheet, CRE rules (per item: accept A/B · reject · override with his own text · protect). **Unattended (DIR-012):** Phase 1 only — the sheet *is* the deferral surface, rendering-visible; stop.

### Step 3 — Phase 2: commit (only after rulings)
Apply ruled edits **verbatim** — accepted options exactly as shown, overrides exactly as CRE supplied them. Write the revised passage to `<folder>/revisions/YYYY-MM-DD - line edit rev N.md` with frontmatter carrying `source_sheet` + working-text lineage **+ `protected_spans_touched:`** (the revision-note convention, `^backlog-protected-span-write-gate` (ii) — see [[WORKFLOWS/register-pass]] § Outputs: every protected span touched accounted as `kept` / `reworded → "<new span>"` (witness updated same session) / `dropped — ruled by CRE <date>`; `[]` stated explicitly when none; an unaccounted drop is a defect — revert). Never touch `draft.md` ([[WORKFLOWS/promote-revision]] is the return trip). Mark the sheet `status: ruled`.

### Step 4 — Rejection harvest
Every rejection/override with a why → append to `REFERENCE/protected-patterns.md` (dated, span it fired on, CRE's reason). Specific constructions only, never vibes — an over-broad shield makes the editor toothless. A "protect" ruling mid-sheet lands the same way.

### Step 5 — Log
[[_CHANGELOG]] entry (fiction lane) + the chapter/episode `changelog.md` if present. New fragilities → [[_OBSERVATIONS]].

## Stop conditions
- Sentinel fails → halt.
- No `REFERENCE/register.md` → halt, ask — never a generic prompt.
- No working text with real content → halt; nothing to edit.
- CRE asks for prose the text doesn't contain (EXPAND) → flag, never author.
- Unattended → Phase 1 only, always.

---

_Canonical reference for the `line-edit` Cowork skill. Design basis: [[KNOWLEDGE/RESEARCH/2026-07-29 ai-line-editing-partner-voice]]. Per [[_SKILLS MAP#Cowork skills]], procedure changes land here first, then propagate via the desktop pack chain (DIR-009)._

## Run log

- **2026-07-29 — live run 1 (EP 01 "Happening Near You", full mode, POLISHED):** first execution, in-chat, on the panel-response-revised draft; consumed the panel run's line-edit queue (DIR-014 loop closed end-to-end). 14 proposals / 6 queries / 0 mechanical; shield absorbed 8 candidates; CRE ruled one pass ("all A" + query rulings); rev 1 committed to revisions/; first two HARVEST LOG entries landed (Q3 chosen, Q4 keep). Budget ran well under ceiling on POLISHED — the 15–25/1,000w start point looks calibrated for ROUGH; revisit after a ROUGH-gear run. (1 of 2–3 runs before packing.)
