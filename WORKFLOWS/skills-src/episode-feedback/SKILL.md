---
name: episode-feedback
description: Run the Writing Is War author's-feedback reconciliation pass (episode route S3) — reconcile CRE's notes in an episode folder against the gated premise.md, surface every collision with a prior ruling explicitly, and write ruled amendments back with provenance. Use whenever the author asks to "reconcile my notes," "sharpen the episode," "run the author feedback," or "feedback pass" on a WIW episode (WRITING/SHORTS/EPISODES). Two-phase and gated - Phase 1 classifies every note item REFINEMENT / GATE COLLISION / DECISION TREE and proposes; the author rules; only then does Phase 2 write. Two input modes - raw author notes, or a ratified decision ledger (items present as resolved-against-ledger confirmations). Runs pre-runway in route v2, so the primary write target is premise.md. Do NOT use it to gate or scaffold an episode (episode-init), carve the runway (episode-runway), revise prose (register pass), or respond to a blind read. It never writes CRE's prose and never invents options.
---

# Episode Feedback

You are running the **author's-feedback reconciliation pass** for the Writing Is War episode battery — **S3 of the episode route v2**: after the sit-with-it period (the author's notes accumulating in the episode folder), before the runway carve (S4). The author's thinking keeps developing after the gate; without this pass his notes either sit unreconciled or get folded in silently, overwriting ratified rulings without anyone noticing. You make every collision explicit and the sharpening cheap.

**The authority rule (the design principle):** the author's notes are authority over AI-derived structure — **but not silently over his own prior rulings.** When a note collides with something he ratified at the gate (the knot, TOS band, tier, container, the turn), surface both states and ask for an explicit re-ruling. No note, however clear, silently overwrites a gate verdict.

Canonical doc: `WORKFLOWS/episode-feedback.md`. Channel constraints: `BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY.md`.

---

## Step 0 — Vault sentinel check

From the mounted folder root, read `_DIRECTIVES.md` and confirm frontmatter `type: ai-os-brain` + `file: directives`. Missing or mismatched → **halt and ask** which folder is the vault. Hard gate; never scaffold a bootstrap.

---

## Step 1 — Locate the episode and the inputs

The episode folder lives at `WRITING/SHORTS/EPISODES/EP NN - TITLE/`. If the author named an episode without a path, search there; several matches → ask.

Gather:

- **The notes file** — any of `notes.md`, `chad's notes.md` in the folder. No notes file, or nothing new below the last rulings block → say so and stop; there is nothing to reconcile.
- **`premise.md`** — the gate output carrying the ratified rulings (knot, TOS band, tier, container, amendments). Missing → the episode was never gated; route the author to episode-init and stop.
- **`runway.md`** — only if it exists with real content. In route v2 this pass runs **pre-runway**, so the normal case is premise-only; a built runway means this is a re-run after the carve, and runway lines become part of the collision surface.
- **The decision ledger, when pointed at one** — `DECISIONS/_QUICK LOG.md` or a dated entry. This is **input mode 2** (live-run-2 finding): when the source is a ratified ledger rather than fresh notes, every item presents as *resolved against the ledger — confirm* and the ruling sheet collapses to confirmations.

---

## Step 2 — Phase 1: CLASSIFY & PROPOSE (read-only)

Segment the new note material. Route every item into exactly one bin:

1. **REFINEMENT** — sharpens the premise (or an existing runway line) without touching a ratified ruling. → Proposed amendment + one-line basis; one-tap confirm.
2. **GATE COLLISION** — contradicts or amends something ruled at the gate or in prior feedback runs. → **Never silently applied.** Present both states: *"ruled X on DATE; the note implies Y — confirm the amendment or keep the ruling."*
3. **DECISION TREE** — branches the author articulated ("help me decide" items). → Present for ruling with a recommendation + one-line basis, decision-helper style. **Measure only the options he wrote — never invent branches** (organic-process guard). A heavy fork can be handed to the decision-helper skill; its dec-NNN ruling returns as input mode 2.

**DIR-011 applies in full:** research every item against the tree — premise, runway, the strategy doc, prior rulings blocks, `DECISIONS/` — before presenting it. An item the artifacts already carry presents as *"resolved against premise section X — confirm,"* never as an open flag.

**Phase-1 deliverable — the ruling sheet, chat-first, nothing written:** every item binned, a recommendation per item, and the downstream impact stated (container word-budget pressure, TOS drift, ear-first cost).

---

## Step 3 — The gate: the author rules

The author rules each item (ratify-or-dig-in). **Hard gate: no artifact write before the ruling.** Unattended runs never rule — they defer the whole sheet (DIR-012).

---

## Step 4 — Phase 2: WRITE (ruled items only)

- Apply ruled amendments to `premise.md` (and `runway.md` if it exists) via the file tools: **targeted edits**, provenance stamps in frontmatter (`amended: DATE — episode-feedback run N, CRE-ruled`) and inline where a ruling changed a ratified line.
- Append a **rulings block** to the notes file below a divider: each item, bin, ruling, one-line basis, date. **The notes file is the author's document** — append below the rule, never interleave into or edit his text.
- **Re-state the container + TOS verdicts post-amendment.** A reshape that breaches the 2,000–2,800 band or drifts the TOS band is a **routing re-call flag** per the gate table — never a trim-to-fit, never ignored.
- Verify every write by re-reading through the file tools (DIR-005).

---

## Step 5 — Log

Vault `_CHANGELOG.md`, one entry, newest at top: `## YYYY-MM-DD — [fiction/writing-ops] episode-feedback run N (EP NN - TITLE)` with items binned / rulings applied / container + TOS re-verdicts. Anything fragile → `_OBSERVATIONS.md` with a `^obs-NNN` anchor.

---

## Guards

- **Never writes the author's prose.** Amendments are structure, constraints, and rulings — not the anomaly line, not a beat's sentence, not "here's how that could go."
- **Never invents options.** Decision trees are measured exactly as articulated.
- **Ratified gates move only by explicit re-ruling** (the authority rule).
- **Diagnostic honesty.** If a ruled amendment breaks the container or TOS band, say so plainly and route per the gate table.

## Stop conditions

Sentinel fails · no episode folder / ambiguous · no premise.md (not gated — route to episode-init) · no new note material · author unavailable to rule (Phase 1 sheet delivered, Phase 2 deferred).

## What this skill is NOT

- Not the gate or the scaffold — that is episode-init.
- Not the runway carve or the production check — that is episode-runway (S4 / Pass 3).
- Not a prose reviser — that is the register pass, downstream, post-slate.
- Not the general decision ledger — heavy forks go to decision-helper; this pass's rulings live in the episode folder.

---

_Canonical reference lives at [[WORKFLOWS/episode-feedback]]. Procedure changes land in the workflow doc first, then propagate here._
