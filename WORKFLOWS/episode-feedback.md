---
type: workflow
name: episode-feedback
status: spec — run by hand/in chat; graduates to a packed skill after 2–3 live runs
triggers: ["reconcile my notes", "sharpen the episode", "run the author feedback", "feedback pass"]
lane: 5 (writing-ops) + 1 (fiction)
created: 2026-07-16
---

# episode-feedback

The **author's-feedback reconciliation pass** for the Writing Is War episode battery. Takes CRE's notes file in the episode folder (`chad's notes.md` or `notes.md`), reconciles it against the gated `premise.md` + `runway.md`, and — **after CRE rules** — writes the sharpened artifacts back with provenance. Concepts in, concrete storytelling out; the episodic shape exits tight.

**Position: Pass 2.5** — between the runway build (Pass 2) and dictation. Architecturally it is the episode-lane sibling of `blind-response` (two-phase gated response pass) crossed with `reconcile` (the ruling walk). It exists because CRE's thinking keeps developing after the artifacts land: without a sanctioned pass, his notes either sit unreconciled (the runway drifts stale) or get folded in silently (ratified rulings overwritten without anyone noticing). This pass makes every collision explicit and the sharpening cheap.

## The authority rule (the design principle)

> **CRE's notes are authority over the AI-derived structure — but not silently over his own prior rulings.** When a note collides with something he ratified at the gate (the knot, TOS band, tier, container, the turn), the pass surfaces both states and asks for an explicit re-ruling. No note, however clear, silently overwrites a Pass-1 verdict.

## Inputs

- The episode folder's notes file (any of: `chad's notes.md`, `notes.md`)
- `premise.md` — Pass-1 gate output, carrying the ratified rulings
- `runway.md` — Pass-2 output
- [[WORKFLOWS/episode-runway]] + [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]] — the channel constraints (TOS band, container two-band rule, ear-first block)

## Phase 1 — CLASSIFY & PROPOSE (read-only)

Segment the notes. Route every item into one of three bins:

1. **REFINEMENT** — sharpens a beat, flow condition, or register flag without touching a ratified ruling. → Proposed amendment with a one-line basis; one-tap confirm.
2. **GATE COLLISION** — contradicts or amends something ruled at Pass 1 or fixed in the runway (the knot, TOS band, tier routing, container, the turn, an established flow condition). → Never silently applied. Presented as an explicit re-ruling showing both states: *"ruled X on DATE; the note implies Y — confirm the amendment or keep the ruling."*
3. **DECISION TREE** — branches CRE articulated in the notes ("help me decide" items). → Presented for ruling with a recommendation + one-line basis, decision-helper style. **Never invents branches** (organic-process guard); it measures only the options CRE wrote.

**DIR-011 applies in full:** research every item against the tree (premise, runway, strategy doc, prior rulings) before presenting it. A note the artifacts already carry presents as *"resolved against [[premise]] §x — confirm,"* never as an open flag.

**Phase-1 deliverable: the ruling sheet** — every item binned, a recommendation per item, and the downstream impact stated (container word-budget pressure, TOS drift, ear-first cost). Chat-first; nothing written yet.

## Phase 2 — CRE RULES, THEN WRITE

- CRE rules each item — the ratify-or-dig-in surface. **Hard gate: no artifact write before the ruling.**
- Apply ruled amendments to `premise.md` and/or `runway.md` via the file tools: **targeted edits**, provenance stamps in frontmatter (`amended: <date> — per author notes, CRE-ruled`) and inline where a ruling changed a ratified line.
- Append a **rulings block** to the notes file (or `feedback-log.md` if the notes run long): each item, the ruling, one-line basis, date. The notes file stays CRE's; the block is appended below a rule, never interleaved into his text.
- **Re-state the container + TOS verdicts post-amendment.** If the reshape breaches the 2,000–2,800 band or drifts the TOS band, that is a **routing re-call flag** per the gate table — never a trim-to-fit, never ignored.

## Guards

- **Never writes CRE's prose.** Amendments are structure, constraints, and rulings — not the anomaly line, not a beat's sentence, not "here's how that could go."
- **Never invents options.** Decision trees are measured exactly as articulated.
- **Ratified gates move only by explicit re-ruling.** See the authority rule above.
- **Diagnostic honesty.** If a ruled amendment breaks the container or TOS band, say so plainly and route per the gate table.
- **The notes file is CRE's document.** Read it, quote it, append the rulings block below a divider — never edit his words.

## Relationship to the rest of the OS

- **Upstream:** [[WORKFLOWS/episode-runway]] Passes 1–2 (the artifacts this amends)
- **Downstream:** dictation → [[WORKFLOWS/dictation-cleanup]] → episode-runway Pass 3
- **Siblings (same two-phase gated architecture):** [[WORKFLOWS/spec-check]] (`blind-response`, `reconcile`) · [[WORKFLOWS/loop-clearer]]
- **Not this:** `episode-runway` (builds the artifacts; this sharpens them) · `decision-helper` (general ledger — this pass's rulings live in the episode folder) · `workshop-chapter` (novel lane, read-only)

## Run log

- **2026-07-16 — live run 1 (EP 01 - DOOMSCROLLER):** first execution, in-chat. Notes carried 3 insight points + 2 decision trees; collisions with the ruled knot and the ruled turn surfaced and re-ruled. (1 of 2–3 runs before packing.)
- **2026-07-17 — live run 2 (EP 01 - DOOMSCROLLER):** stamping run — source was a same-day decision-helper session (dec-017 five forks + serving-mechanics quick ruling) rather than a fresh notes pass, so every item presented as resolved-against-ledger (DIR-011), zero gate collisions, zero open flags. 7 items applied to `runway.md` (POV, setting, butcher, silent, victims' feeds, serving mechanics, opener candidate captured with provenance). Container + TOS re-verdicts unchanged. Pattern worth carrying into the pack: the pass has two natural input modes — raw author notes (run 1) and a ratified decision ledger (run 2); the ruling sheet collapses to confirmations in mode 2. (2 of 2–3 runs before packing.)
