---
type: workflow
name: dev-reconcile
trigger: reconcile the layer
aliases: [run the dev reconcile, dev reconcile, run the layer audit, reconcile the parts layer, reconcile the sequence layer]
inputs: [project + the completed DEV layer CRE names (parts/acts spine · sequences · scenes)]
outputs: [a binned seam sheet (SYSTEM/reports/ if CRE wants it durable); ruled in-place fixes to DEV entries; DECISIONS entries for structural forks (via decision-helper); parked flags visible to dev-readiness; a descent verdict; _CHANGELOG entry]
lane: fiction
status: draft
last_updated: 2026-07-15
revision_note: v1.2 — ripe-fork handoff added (CRE-ratified 2026-07-15, same session as run 1): parked-until wake convention (decision-helper (ripe) / CRE-articulation / milestone:<name>) + every run ends by naming the ripe decision calls; dev-readiness carries the matching triage. v1.1 folded run-1 process notes. Packages after run 2-3 per dec-008. ^backlog-dev-reconcile-pilot.
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
| **PARK** | Not decidable until a lower layer fills in | Held flag on the touched entries (`^poe-010` shape) + a parked DECISIONS entry with a `parked-until` **condition** when fork-shaped — written in the **wake convention** (Step 6) so the handoff is machine-triageable. Visible to dev-readiness by definition |

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

**Implementation recipe (proved in run 1, 2026-07-15 — a 75-read layer in one pass):**
- **Seed deterministically first:** one grep over the layer's reads for the flag vocabulary (`⚑` · `pending CRE` · `CRE to confirm` · `CRE to rule` · `[AUTHOR` · `held` / `Held —` · `router-unresolved`) harvests sources 1–2 cheaply before any semantic reading.
- **Fan the cross-read to parallel read-only subagents** by act block (run 1: three agents over SEQ 01–22 / 23–45 / 46–75). Each agent reports: (a) a **traveling-item ledger** (who holds which instrument at range entry/exit + every hand-off, with SEQ numbers — items are the likeliest collision carriers), (b) **knowledge states** (who knows what, where it changes), (c) candidate contradictions with verbatim quotes + both file names, (d) stranded setups, (e) duplicated function, (f) taste drift. Cap each report (~600–700 words); the orchestrator stitches at the part boundaries the agents can't see across.
- **Tell the agents what's already on the sheet** so they don't re-report the grep harvest.
- Run-1 yield: the recipe found real seams no single reader had (bead-location drift, destroyed-vs-abandoned, coinage anachronism, a possession gap) and certified the load-bearing continuity clean (the Widowsbane count reconciles end-to-end through the SEQ 57 number test).
- **A stale-flag class exists beyond the three bins:** flags whose ruling already exists elsewhere (a titles ruling in `project.md`, the doll-name ruling in `items.md`) but was never synced into the read — and stale pointers the other direction. Pure sync, safe-ops; batch them with the mechanical writes, don't spend walk items on them.
- **Resolve-before-bin (`^obs-188`, CRE-directed 2026-07-15):** every sweep finding gets a **resolution-research pass against the tree** (registry entries, `_audit/` floors, `DECISIONS/`, ruled terms) before it is binned. Tree-answered → present with the sourced resolution ATTACHED (a one-tap "confirm the sourced fix," or the stale-sync batch), never as an open QUICK the walk must deliberate. Only tree-silent findings cost walk items. *(The Nameless/Last Mountain flag survived this pass unresearched and reached the exit gate as a phantom blocker — the rule exists so a sweep never exports a question the tree already answers.)*

### Step 4 — Rule (the walk)
Present QUICK findings one at a time, reconcile-style — ratify / rebin / skip, seconds each. Then STRUCTURAL findings one decision at a time through decision-helper (its surface, its ledger, its exits). PARK findings get their condition stated and logged. Nothing writes until ruled.

**Batch the rubber-stamps (run-1 pattern — load-bearing for the ADHD profile):** "one at a time" is for genuine calls, not for confirmations. Group same-class items into **en-bloc ratify batches with a pull-out option** ("ratify all / ratify with exceptions / walk them individually"): run 1 moved ~20 items in three questions — the `^poe-010` "CRE to confirm the beat holds" closures as one batch, the router-resolved `[AUTHOR:]` normalizations as one, the stale-flag syncs + mechanical punch list as one. Reserve individual walk items for seams where CRE's answer changes content. Genuinely-open `[AUTHOR:]` words still go one per question, **with the transcript context quoted** — he's ruling on a sentence, not a word list.

**Expect live rebins — the bins must bend:** run 1 had a QUICK escalate to STRUCTURAL mid-walk (the moonstone knowledge-state: CRE answered "this needs a help me decide" and articulated the substance). Record the substance he gives verbatim into the parked entry; that's ledger data, not a failed QUICK.

**Redundancy findings need evidence before they're rulable:** naming a pair ("SEQ 20↔22 same function") got "I need more information"; quoting each read's own *What this sequence is doing* line side by side got instant rulings. Present redundancies with the reads' self-descriptions — half of them dissolve on contact (run 1: two "duplications" were plant→payoff pairs, one was a self-aware designed rhyme). Real pacing risks (the triple rock-bottom) resolve as **motif + a standing scene-intensity flag at drafting**, not as dev-layer restructuring.

### Step 5 — Write ruled fixes
File tools only (DIR-005), serialized YAML if frontmatter is touched (DIR-004). Ruled fixes apply **in place** to the DEV entries (sculptor-not-historian: the `_audit/` floor stays the recoverable history). Close resolved held flags per `^poe-010`; clear/annotate resolved `_LEDGER` lines. Canon-worthy hardenings → queue as dev-promote candidates, not written here. **Structural resolutions requiring new story substance are CRE's to author** — record his ruling verbatim; never draft it.

**Write hygiene (run 1, `^obs-187` — both bit):**
- **Insert desk notes ABOVE the read's provenance footer** (`*Captured from [[_intake/_audit/…]]*`), never EOF-append: the dev-capture-audit linter keys footer detection on the file tail, and appended notes demoted six clean reads to "no provenance footer."
- **Do not trust a bash linter re-run immediately after the write batch.** The mount serves stale partials; run 1's post-write `audit_dev.py` reported a phantom broken floor pointer (`_audit/2.md` — a wikilink truncated mid-read) and a phantom missing `[source:]` line. Verify every new flagged line **through the file tools** before treating it as real; repair edits against phantom defects are how a correct pass corrupts a tree.
- **Expect the `^obs-172` per-file delete lock** on any intake-straggler removal — catch it and queue a `#desktop` delete rather than retrying.
- **In-line strikes** (ratify tags, word fixes, table cells) = file-tool Edits. **Uniform one-line notes across many files** may batch via a bash append-only script (pure `'a'` mode, no read-modify-write — DIR-007-safe) — but per the footer rule above, prefer file-tool inserts above the footer now; if batching, verify a sample through the file tools after.
- **Parked STRUCTURAL forks get real `DECISIONS/` entries** (`dec-NNN`, `status: parked`, wake condition in `parked-until`, yaml `safe_dump` + parse-gate), **cross-linked by `dec-NNN` id from every touched read** so dev-readiness sees them. A fork whose branches CRE hasn't articulated yet parks with "awaits CRE's candidate homes" as the wake condition — the entry never invents branches (organic-process guard).
- **Attribute rulings to their true date.** A stale flag synced today was often ruled earlier (run 1: the 33B rename was CRE-ruled 07-08; today's write says so, not "ruled 2026-07-15").

### Step 6 — Exit gate
Run dev-readiness on the layer: descent verdict + mandatory blind-spot caveat, parked forks surfaced. Descend on a clear verdict or CRE's explicit overrule.

**Run-1 note:** when the reconcile session itself just held the whole layer (ledger, flags, forks, item continuity), the exit gate may be delivered **inline in dev-readiness's output shape** — one-line descent verdict + load-bearing gaps + the mandatory blind-spot caveat — rather than re-running the full skill cold. That kept the pass inside the bounded gate. A standalone dev-readiness run stays the right call when time has passed since the walk.

**The ripe-fork handoff (v1.2 — CRE-ratified 2026-07-15; this is how the pass tells the next session what to do).** Every parked DECISIONS entry this pass writes carries `parked-until` in the **wake convention**, one of exactly three shapes:

| `parked-until` | Meaning | Handoff action |
|---|---|---|
| `decision-helper (ripe)` | Branches CRE-articulated; nothing upstream blocks measuring | **Name the literal next call** — *"run the decision helper on dec-NNN"* |
| `CRE-articulation` | Fork is real but CRE hasn't named branches | Surface for branch-naming (best while the source material is hot); **not measurable yet** |
| `milestone: <name>` | Wakes at a named seat/boundary (act revision, a grain descent) | **Do not wake.** The milestone's own session re-triages |

The run's **final output is the handoff**: the ripe calls listed by dec-id, the articulation asks named, the dormant forks left sleeping. The next session starts from the handoff, not from rediscovery in chat. (Run 1's handoff: ripe → `dec-009`; articulation → `dec-010`; dormant → `dec-011`/`dec-012`/`dec-013`.) The same triage is `dev-readiness`'s job when it runs standalone later — see its doc.

### Step 7 — Log
`_CHANGELOG` entry (fiction lane); observations to `_OBSERVATIONS`; follow-ups to `_BACKLOG`. The changelog entry's **Open loops** line repeats the ripe-fork handoff (dec-ids + their wake states) so the pickup brief carries it. **Close with the gloss question** — *"anything you glossed?"* — answers feed `DEV/_AUTHOR FLAGS.md`; inside sessions only, never scheduled (CRE-ratified 2026-07-15).

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

**Run 2 — 2026-07-16, Witchwood Part-2 SCENE layer (the shape-the-part run-1 handoff — the lean "reconcile and rule 2" profile): the bins held on the small shape.** Bounded to SC 01–17 same-session with the descent; arc lens folded in as a sweep source (no separate leg), author-flags cue-harvest only (CRE: nothing glossed), readiness inline. Sheet: **zero QUICK/STRUCTURAL/PARK — one stale-sync batch of 5** (two `^af` carries onto SC 12, two Cleave held-question closures, the Moon Magic dec-010 sync, one held-fork carry to SC 10), ratified en bloc. Verdict READY; the `^af-002` Knots-ladder wake fired and was handed off (before dictation, CRE's discretion). **Profile datum for packaging: a same-day mechanical descent yields a sync-only sheet — the lean profile is right-sized; a cold-context sweep remains the stronger check when time has passed.**

**Run 1 — 2026-07-15, Witchwood Parts/Acts (attended, full seven steps): the bins held.** ~30 findings ruled in one bounded session; QUICK/STRUCTURAL/PARK needed no fourth bin, one live rebin (QUICK→STRUCTURAL) worked as designed; forks parked as `dec-009`–`dec-013`; exit verdict *clear to descend*. What run 2 should prove: the bins on a **different layer shape** (a sequence→scene descent milestone, or another project's first layer) — run 1 was the largest, most flag-rich case the workflow will likely ever see. Everything above tagged "run 1" is candidate SKILL.md content at packaging.

## Logging

On completion, append a `_CHANGELOG` entry (fiction lane); new patterns to `_OBSERVATIONS`; follow-ups to `_BACKLOG`.
