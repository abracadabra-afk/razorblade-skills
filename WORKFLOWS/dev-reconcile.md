---
type: workflow
name: dev-reconcile
trigger: reconcile the layer
aliases: [run the dev reconcile, dev reconcile, run the layer audit, reconcile the parts layer, reconcile the sequence layer]
inputs: [project + the completed DEV layer CRE names (parts/acts spine · sequences · scenes)]
outputs: [a binned seam sheet (SYSTEM/reports/ if CRE wants it durable); ruled in-place fixes to DEV entries; DECISIONS entries for structural forks (via decision-helper); parked flags visible to dev-readiness; a descent verdict; _CHANGELOG entry]
lane: fiction
status: draft
last_updated: 2026-07-14
revision_note: spec authored 2026-07-14 per dec-008 (CRE-ratified option C). Runs ATTENDED + manual until 2-3 live runs prove the bins; packages after (the episode-runway discipline). Pilot target = the Witchwood Parts/Acts layer, ^backlog-dev-reconcile-pilot.
---

# WORKFLOW: dev-reconcile

> **status: spec.** Ratified design (dec-008), not yet a packaged skill. Run it attended from this doc; refine the bins from the live walks; pack after 2–3 runs.

## When to use

CRE has completed a **layer milestone** in a project's top-down dev descent — e.g. the parts/acts spine + sequence reads are captured — and wants the layer's seams corrected **before** descending to the next layer, so nothing wrong gets baked into everything below it. Trigger: "reconcile the layer," "reconcile the parts layer," "run the dev reconcile."

This is the dev-stack lift of the prose pipeline's own architecture (blind-read → blind-response *before* the line passes): fix structure at the altitude where a beat moves in one edit, not across hundreds of placed scenes.

## Position in the pipeline

```
dev-capture (fills the layer)
   └─ dev-capture-audit      mechanical integrity (optional pre-filter, read-only)
        └─ DEV-RECONCILE     ← this pass: content seams, binned + ruled
             ├─ decision-helper   structural forks (triangulate lane)
             ├─ dev-promote       gated crossing when a ruling hardens canon-worthy material
             └─ dev-readiness     the exit gate: descent verdict + blind-spot caveat
                  └─ descend to the next layer (sequence → scene)
```

- **Not dev-capture-audit** — that lints capture *structure* (anchors, floors, frontmatter); this pass judges capture *content* (seams, contradictions, redundancy, continuity).
- **Not dev-readiness** — that surfaces forward gaps (what's missing before descent); this pass corrects backward seams (what's wrong in what exists). They meet at the exit gate.
- **Not dev-promote** — nothing here writes REFERENCE. A ruling that hardens trusted canon queues a dev-promote candidate; the crossing stays gated and separate.
- **Not decision-helper** — this pass is the *feeder*: it surfaces and bins; decision-helper measures the structural forks one at a time.

## The three bins (the triage gate)

Every finding gets exactly one bin, proposed by the pass, ruled by CRE:

| Bin | Test | Handling |
|---|---|---|
| **QUICK** | One obvious fix, fully sourced to CRE's own captured material (normalize a term, dedupe a repeated beat, pick which entry holds a fact) | Walked reconcile-style — one at a time, CRE rules in seconds, committed verbatim |
| **STRUCTURAL** | A genuine fork: which act holds the reveal, whether two sequences merge, a contradiction with story-shape consequences | Handed to **decision-helper** (triangulate lane: Chad-likes / story-prefers / reader-experience). Options = CRE's articulated branches + recombinations of his own captured dev (dec-001 recombination boundary) — never invented substance |
| **PARK** | Not decidable until a lower layer fills in | Held flag on the touched entries (`^poe-010` shape) + a parked DECISIONS entry with a `parked-until` **condition** when fork-shaped. Visible to dev-readiness by definition |

CRE can rebin anything; his rebins are ledger data.

## Steps

### Step 1 — Sentinel + scope
Confirm the `_DIRECTIVES.md` sentinel (`^obs-004`). Resolve the project and the layer CRE named. Load `_DEV_MAP.md`, `_DEV.md` (taste anchor), the layer's entries (`project.md` + `sequences/` for the top layer), and `_intake/_LEDGER.md`. **Layer-drained check:** any unrouted note in `_intake/` belonging to this layer → surface and stop (reconciling an undrained layer produces false seams).

### Step 2 — Pre-filter (optional, recommended)
Run the dev-capture-audit linter. Mechanical defects go to its own punch list — they are not seams and must not clutter the sheet.

### Step 3 — Sweep: derive the seam sheet
Sources, in order:
1. `_intake/_LEDGER.md` — contradictions dev-capture already banked against this layer.
2. **Held flags** on the layer's entries (`^poe-010` carry-the-thread) — open questions and dev-internal seams.
3. **Cross-read collisions** — the same beat placed twice, two reads asserting incompatible facts/order, a setup at this altitude with no landing (stranded at layer scope).
4. **Redundancies** — duplicated function (two sequences doing the same story job).
5. **Taste-anchor drift** — an entry pulling against `_DEV.md`'s stated loves (flag only; the ruling is CRE's).

Each finding: one-line seam + entry locations + verbatim evidence quotes + proposed bin. **The sheet describes; it never prescribes story content.** Chat-first; write to `SYSTEM/reports/` only if CRE wants it durable.

### Step 4 — Rule (the walk)
Present QUICK findings one at a time, reconcile-style — ratify / rebin / skip, seconds each. Then STRUCTURAL findings one decision at a time through decision-helper (its surface, its ledger, its exits). PARK findings get their condition stated and logged. Nothing writes until ruled.

### Step 5 — Write ruled fixes
File tools only (DIR-005), serialized YAML if frontmatter is touched (DIR-004). Ruled fixes apply **in place** to the DEV entries (sculptor-not-historian: the `_audit/` floor stays the recoverable history). Close resolved held flags per `^poe-010`; clear/annotate resolved `_LEDGER` lines. Canon-worthy hardenings → queue as dev-promote candidates, not written here. **Structural resolutions requiring new story substance are CRE's to author** — record his ruling verbatim; never draft it.

### Step 6 — Exit gate
Run dev-readiness on the layer: descent verdict + mandatory blind-spot caveat, parked forks surfaced. Descend on a clear verdict or CRE's explicit overrule.

### Step 7 — Log
`_CHANGELOG` entry (fiction lane); observations to `_OBSERVATIONS`; follow-ups to `_BACKLOG`.

## Bounded-gate rule (load-bearing)

The pass is **1–2 sessions per layer, with a defined exit** (the Step-6 verdict). A finding that outgrows the session **parks** — it does not extend the gate. This is the guard that keeps "correct before descending" from becoming "never descend."

## Scope guards (must-not)

- Never invents story options, branches, or content of any kind (organic-process guard; recombination of CRE's own captured dev is the ceiling, with provenance).
- Never writes `REFERENCE/` (dev-promote's crossing) or any draft/prose file.
- Never resolves a held flag from inference alone (`^poe-010`).
- Never runs on an undrained layer (Step 1 check).
- No `patch_vault_file` / whole-file MCP rewrites; file-tool targeted edits, re-read to verify (DIR-005).

## Stop conditions

- Unrouted `_intake/` notes for the layer → stop, surface (drain first).
- No DEV tree / layer entries empty → nothing to reconcile, stop.
- Secret/credential encountered → flag + queue rotation, never propagate (DIR-001/006).
- CRE rules fewer than the sheet holds and the session ends → remaining findings persist as held flags; the pass resumes, it doesn't re-sweep from scratch.

## Packaging plan

Attended manual runs from this doc first. After 2–3 live runs prove the bins and the walk: author `skills-src/dev-reconcile/SKILL.md`, pack via desktop `pack-skills.ps1`, sha-verify, Save-skill (DIR-009). Tracked: `^backlog-dev-reconcile-pilot`.

## Logging

On completion, append a `_CHANGELOG` entry (fiction lane); new patterns to `_OBSERVATIONS`; follow-ups to `_BACKLOG`.
