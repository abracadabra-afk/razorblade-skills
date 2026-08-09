---
type: workflow
name: panel-response
trigger: respond to the panel
aliases: [panel response, work the panel findings, run the panel response, panel developmental edit]
inputs: [pass-1-panel.md (the panel synthesis), the working draft, the unit's spec surface (brief.md / premise.md) + prior rulings (DECISIONS/, premise amendments, feedback-log), REFERENCE canon where the unit has one]
outputs: [response-rulings.md (the ruled sheet, in the panel run folder), a choreo handoff list, ratified choreo maps (via the nested choreographer), the approved structural revision written to the working draft with provenance, changelog lines]
lane: fiction (+ writing-ops for WIW episodes)
status: spec — packs after 2–3 live runs
governed-by: DIR-011 (resolve before flag), DIR-012 (gates attended), DIR-014 (rulings land on tool-read surfaces), DIR-017 (banked prose never re-dictated; choreo maps exit to revision)
pipeline_position: Workshop-2 tier — consumes the Pass-1-tier panel synthesis; sits between panel-read and the line passes; nests choreographer between its two phases. Route v3 (2026-08-09) — on episodes this always post-dates CRE's author pass, since panel-read is the pre-publication gate.
last_updated: 2026-08-09
---

# WORKFLOW: panel-response

The **developmental response pass for a panel read** — the panel-tier sibling of `blind-response`. Takes `pass-1-panel.md` (attributed, binned, split-preserving) and turns it into exactly one structural revision of the working draft, through three moves in fixed order: **rule first, design second, revise once.**

It exists because the panel synthesis is deliberately not actionable: it bins and attributes, never prescribes. Between that artifact and a revised draft sat a gap — ruling on premise vs. split, synthesizing ruled findings into structural fixes CRE approves, and routing choreography-class defects through the right instrument before any prose moves. This pass is that gap.

## The design principle — rule first, design second, revise once

The chicken-and-egg question (panel → choreographer → dev edit, in what order?) was ruled 2026-07-29: **the choreographer nests inside this pass, between its phases.** It is not a peer stage.

- **Ruling precedes choreography** because half a panel's output is positioning data, not defect. A choreographer run against unruled findings designs fixes for problems CRE may decline (a 2–2 split ruled toward the praising seats has nothing to fix). The choreographer's own Step 2 dials (stakes, flaws, thematic intent) presuppose settled intent; for a panel-flagged event, the ruling is what settles it. This is the DIR-011/DIR-014 seam applied at pipeline scale.
- **Choreography precedes revision** because otherwise Phase 2 rewrites an event without its beat map and the choreographer forces a second revision of the same stretch. One revision, informed by ratified maps.

## Position

`panel-read` (Pass-1 tier) → **Phase 1: rule & route** → `choreographer` (per choreo-binned event) → **Phase 2: revise** → the line passes (`register-pass` / `line-edit`) as normal.

Siblings in the two-phase gated architecture: [[WORKFLOWS/spec-check]] (`blind-response`, `reconcile`) · [[WORKFLOWS/episode-feedback]] · [[WORKFLOWS/loop-clearer]].

## When to use

CRE says **"respond to the panel"** / **"panel response"** / **"work the panel findings"** — a `panel-read` run has produced `pass-1-panel.md` for a working text (chapter, WIW episode, short) and he wants the findings ruled and the ruled ones built into the draft.

**Not for single blind reads:** when the Pass-1 artifact is `pass-1-blind.md`, `blind-response` remains the canonical route (Witchwood spec-check battery). The two may converge after this pass's live runs prove the shape; until then they stay separate so the battery's canon doesn't churn.

**Not for pre-author-pass material (route v3, CRE-ruled 2026-08-09):** this pass consumes a panel run, and on the episode route the panel is the pre-publication gate — so this machinery only ever meets an authored draft. Hard corollary from the EP 01 post-mortem: **no fix-class routing (choreographer, structural revision, line queue) against a section carrying an open CONTENT flag** — a beat whose story content CRE has not yet affirmed gets his author pass first, per [[WORKFLOWS/dev-edit]]'s affirmed-sections map. EP 01 run 1 executed a full choreo session against exactly such a section (video 2, sorority) and the work died whole with the scene.

## Phase 1 — RULE & ROUTE (read-only)

**Step 0 — sentinel + locate.** Verify `_DIRECTIVES.md` frontmatter (`^obs-004`). Identify the run folder and the draft revision the panel read (the synthesis frontmatter carries `source:`). If the draft has moved since the panel read it, say so before anything else — rulings against a stale read are rulings against a phantom text.

**Step 1 — load.** The synthesis, the draft, the unit's spec surface (`brief.md` / `premise.md`), prior rulings (`DECISIONS/`, premise amendment stamps, `feedback-log.md` / rulings blocks), and REFERENCE canon where the unit has one. **The clean room ended with the panel — this pass is spec-aware by design.** That is what lets it do DIR-011 research the synthesis could not.

**Step 2 — walk the bins, in synthesis order** (DNF → CONSENSUS → CORROBORATED → SPLIT → SINGLETON → PRAISE/POSITIONING). Per finding:

- **DIR-011 first:** research it against the tree before presenting. A finding the spec surface or a prior ruling already answers presents as *"resolved against [[premise]] §x — confirm,"* never as an open flag. A finding that collides with a ratified gate ruling presents as an explicit re-ruling showing both states (the episode-feedback authority rule) — never silently applied either way.
- **CRE rules:** **REAL** (a defect to fix) / **PREMISE** (working as intended — declined, with his one-line why recorded) / **SPLIT-RULED** (an audience call: which seat he sides with, recorded as positioning data) / **DEFER** (parked, with what would unpark it).
- **Weighting guidance, not verdicts:** consensus ≥ corroborated ≥ home-turf singleton; a split is never averaged and never presented as a defect. A split that turns out to be a genuine strategic fork routes to `decision-helper`, not this sheet.

**Step 3 — bin every REAL finding by fix class:**

1. **CHOREO** — the defect lives in event structure: staging, reveal order, blocking, attribution-of-action, mechanics of a climax. → the choreographer handoff list.
2. **STRUCTURAL** — compression, transformation, reordering, cut/keep, runway-length problems, plant/payoff arming. → Phase 2 directly.
3. **LINE** — diction, itemization length, tongue-trippers, stock language. → **deferred downstream, recorded on a surface the line passes read** (the run's verdict/edit sheet the register or line-edit run will consume — DIR-014; a deferral that lives only in this ruling sheet will be re-litigated).

**Step 4 — protect the praise.** Consensus assets (elements 3+ seats independently praised) are recorded in the ruling sheet as **protected patterns** so Phase 2 and the downstream line passes don't sand them off while fixing their neighbors. (Precedent: line-edit's protected-patterns harvest.)

**Phase-1 deliverable: the ruling sheet** — chat-first, every finding ruled, every REAL binned, protected patterns listed, downstream impact stated (for WIW units: container word-budget and TOS-band pressure of the proposed fixes). After CRE rules, the sheet writes to `panel/<run>/response-rulings.md` (safe-op; frontmatter serialized per DIR-004). **Hard gate: no draft write in Phase 1, ever.**

## The choreographer interlude

For each CHOREO-binned event, run [[WORKFLOWS/choreographer]] per its own canon — one session per event, its own two-phase gate intact — with **one exit re-routed:** on banked prose, the ratified map exits to **Phase 2's revision as its spec**, not to the mic. Re-dictating banked material is DIR-017 clause 1's named mistake. The mic exit remains available only where the ruled fix is a **genuinely new, never-written stretch** (a new beat, an added scene) — that is forward flow, and it is CRE's call.

**Phase 2 is blocked until every CHOREO-binned event carries a ratified map.** A stop, not a warning.

## Phase 2 — REVISE (gated)

**Step 5 — propose the revision.** One structural revision covering all ruled-REAL structural fixes, using the choreo maps as the spec for their events. Presented as a change plan (what moves, what compresses, what's cut, what the choreo map re-stages), not as finished prose dumped for rubber-stamping. CRE approves the plan — ratify-or-dig-in, per item or in one pass.

**The boundary:** structural revision means restructuring, compressing, cutting, and reordering **CRE's existing prose**, plus executing the ratified choreo staging. It never touches line/voice (the register's lane — even when a line-class defect sits adjacent to a structural fix, it stays deferred). It never authors new story material: where a ruled fix requires prose that doesn't exist, that is a **demonstration-block moment** — one demonstration maximum, original kept, never committed for him (loop-clearer precedent) — or a gap-fill dictation seed.

**Step 6 — write.** Snapshot the pre-response draft into the run folder (`panel/<run>/pre-response-draft.md`), then apply the approved revision to the working `draft.md` via the file tools, with provenance in frontmatter (`revised: <date> — panel-response run <id>, CRE-ruled`). On the per-chapter convention the chapter `changelog.md` gets one line. For WIW units, **re-state the container + TOS verdicts post-revision** — a breach is a routing re-call flag per the gate table, never a trim-to-fit.

**Step 7 — exit.** Point downstream: line-class deferrals staged for the register/line-edit run; any gap-fill dictation seeds named; any `decision-helper` forks listed. The draft is now the input to the line passes.

## Guards

- **Never writes CRE's prose.** Structural moves on his existing words; one demonstration block maximum where new material is unavoidable, original kept.
- **Never averages a split.** Splits are positioning data; ruled splits are audience decisions, recorded as such.
- **Never invents options, beats, or story turns** (organic-process guard). It measures what the panel found and what CRE ruled.
- **Ratified gate rulings move only by explicit re-ruling** (the episode-feedback authority rule, inherited whole).
- **Rulings land where tools read** (DIR-014): line-class deferrals go to the line passes' input surface; premise declines stamp the spec surface if they amend it; this sheet alone binds nothing.
- **Attended only.** The gates are the skill. An unattended run may at most pre-research the DIR-011 column of the ruling sheet into a `SYSTEM/reports/` draft (DIR-012); it never rules, never writes the draft.

## Stop conditions

- No `pass-1-panel.md` → run `panel-read` first; nothing to respond to.
- The draft has moved past the revision the panel read → surface it; CRE decides re-panel vs. proceed-with-caveat.
- A ruled fix contradicts canon (continuity/threads) → surface for ruling before it enters the plan.
- A CHOREO-binned event without a ratified map at Phase 2 → stop; run the choreographer.
- CRE starts dictating prose mid-session → capture verbatim as his, route through normal intake; never absorb it as the pass's proposal.

## Not this

- **`blind-response`** — the single-blind-read sibling; canonical for the Witchwood spec-check battery. This pass adds attribution-aware ruling, fix-class routing, and the choreographer nest.
- **`reconcile`** — rules the spec-passes (2–5) verdict sheet; different tier.
- **`episode-feedback`** — reconciles CRE's *own notes* against the premise; this reconciles *panel findings* against the draft. Same gated architecture, different input authority.
- **`choreographer`** — nested here per event, never replaced; its canon governs its sessions.
- **`line-edit` / `register-pass`** — downstream; this pass feeds them and never does their job.

## Logging

Per DIR-003: a run that writes the ruling sheet and/or the revision logs one `_CHANGELOG` entry (unit, findings ruled by verdict class, fix-class counts, choreo sessions run, revision applied y/n). Ruling-sheet-only sessions still log (the sheet is a vault write). New fragilities (a bin that keeps mis-classing, a choreo handoff that keeps stalling) file to `_OBSERVATIONS`.

## Run log

- **2026-07-29 — live run 1 (EP 01 "Happening Near You", panel run 2026-07-29-01):** full pipeline in-chat, same day as authoring. 14 findings → 6 REAL (1 CHOREO / 2 STRUCTURAL / 3+batch LINE), 4 PREMISE, 3 SPLIT-RULED, 0 DEFER; CRE ruled one-pass. DIR-011 research resolved/re-classed 4 of 14 against the tree (dec-020, the serving ruling, premise amendment 2, a 4×-motif refrain the flagging seat couldn't see). First live choreographer run nested (climax-inversion, 6 beats, one-pass ratify; second exit door exercised). Revision applied to draft.md (~2,610 words, in band; TOS unchanged); line-edit queue staged in response-rulings.md. Instrument held; one watch item: staged-flip execution left a back-to-back "Travis…Travis" sentence pair, queued for the line pass. (1 of 2–3 runs before packing.)

<!-- v1 spec authored 2026-07-29 from the panel-response design session. Founding ruling (CRE-ratified): the chicken-and-egg between panel-read, choreographer, and the dev edit resolves as rule-first / design-second / revise-once, with the choreographer nested between this pass's phases; on banked prose the choreo map exits to Phase 2, not the mic (DIR-017). Skeleton: blind-response two-phase gate + episode-feedback authority rule + fix-class routing (new). Not yet mirrored to skills-src/ or packed. -->
