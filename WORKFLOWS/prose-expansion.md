---
type: workflow
name: prose-expansion
trigger: expand the prose
aliases: [run the expansion, tag the spine, expansion passes, floor the draft, run the floor sheet]
inputs: [a CRE-gated floor draft (transcoder v6 slate, spine-review gate cleared), the synthesis ledger's heat bank, the chapter envelope/runway tension curve, KNOWLEDGE/PROSE FRAMEWORK/ canon (sentence-structure.md + temperature.md + narrator-rules.md)]
outputs: [POV-tagged spine, repetition census, temperature-tag proposal sheet, CRE's restructured/heated draft]
lane: fiction
status: draft — 2 live runs (EP 01 2026-08-01, WITCHWOOD CH12 2026-08-03); packs after 3
last_updated: 2026-08-10
scope: Any project on the per-chapter folder convention with a transcoder v6 floor. Framework steps 4-7 (see KNOWLEDGE/PROSE FRAMEWORK/framework.md).
pipeline_position: downstream of [[WORKFLOWS/transcoder]] (v6, behind the spine-review gate); upstream of [[WORKFLOWS/register-pass]]
---

# WORKFLOW: Prose Expansion (framework steps 4–7)

> The expansion stage of the prose-building framework: the machine tags, **CRE writes**. Machine prose generation stopped at the transcoder's floor — nothing in this workflow authors a sentence of CRE's fiction except the gated step-5 assist, and that only proposes. Ownership CRE-ruled 2026-08-01 (`SYSTEM/reports/2026-08-01-transcoder-v6-proposal.md`).

## Hard preconditions

- The floor draft has **cleared the spine-review gate**. Never run any pass here on an ungated floor.
- DIR-017 untouched: everything here is downstream of the mic. No expansion rule ever gates dictation.

## Entry mode B — existing piece (revision route, first run: EP 01, 2026-08-01)

For a landed draft that predates the v6 floor (its spine and beats exist; register drifted): **do not regenerate a floor** — that discards ratified line work — and do not enter at step 4, which would conflate restructure with re-registering. Instead:

1. **Floor sheet.** Run transcoder Operation 3 *diagnostically* over the existing draft: sweep against the project's floor rules, output a gated verdict sheet in the piece's folder (`floor-sheet-YYYY-MM-DD.md`) — span → breach class → floored option → heat-bank note. `protected_patterns` and prior rulings are excluded or presented as resolved-confirm (DIR-011), never re-flagged. **draft.md is never touched by the sheet.**
2. **CRE rules the sheet** per item (floor it / keep it / his own line). "Keep — performance" is a legitimate verdict with provenance; picks commit verbatim to a revision.
3. **Gate + steps 4–7** proceed on the ruled text as normal.

The sheet doubles as the spine-review surface for existing work — the cold diff exposes the same developmental seams the floor draft would.

**One-sweep runner (CRE-ratified 2026-08-03):** [[WORKFLOWS/chapter-clean]] **mode B** wraps this route into two sittings — floor sheet binned via [[WORKFLOWS/clean-mode]] with the mode-B bias (LEAN-default, the machine never auto-floors finished prose; close calls keep) → Gate A residue → autonomous stretch (steps 4–7 + register) → Gate B + ledger veto.

**Reference implementations.** Two, deliberately different in scale — reach for whichever matches the piece in front of you.

- **Short / Entry mode B — EP 01 *Happening Near You*, 2026-08-01.** Full traversal in one day: floor sheet (F1–F10) → landed draft 4 → POV tags → assist walk under the non-regression gate (W1–W4) → landed draft 5 → motion-seam check (M1/M2 graduated to protected_patterns) → temperature dial ratified. Its `expansion/` folder is the worked example for every artifact this workflow produces.
- **Novel chapter / entry at step 4 — WITCHWOOD CH12 *Where It Puts You*, 2026-08-03.** First novel-chapter run and the first `protected_patterns` surface in that project. Steps 4→5 in one session on a gate-cleared v6 floor: POV + transition tags over 158¶ → motion-seam check → assist walk (W1–W8, all ruled in one pass) → `revisions/…-rev1.md`, temperature held for after the restructure. Use this one for **scale mechanics** — how the census, the visible skip list, and the diff exit gate behave on a chapter rather than a 2,600-word short — and for the shape of a `protected_patterns` block carrying five ruled keeps with their readings.

**One structural difference worth knowing before you pick an order.** EP 01 ran temperature *after* the restructure landed, and CH12 repeated that deliberately (CRE-ruled at the top of the run): **heat placement moves when sentences move**, so a dial map built on the pre-restructure text is partly invalidated by step 5. Default to holding step 6 until step 5 lands, and say so when proposing scope.

## Step 4 — POV tagging (machine, annotation only)

Tag every spine sentence/cluster against the [[KNOWLEDGE/PROSE FRAMEWORK/sentence-structure]] taxonomy: **SENSING** / **DOING** / **THINKING-FEELING** / **SPEAKING**. Output is a tagged copy of the floor (inline tags or a margin map — whichever CRE ruled for the project; default inline `[S]/[D]/[T]/[SP]` markers). No prose is touched. Ambiguous spans get a dual tag + one-line note, never a guess presented as a ruling.

**Transition tags (Motion Laws, CRE-ratified 2026-08-01).** Every envelope/beat boundary additionally gets **[TR-jarring]** or **[TR-flowing]** from the envelope delta — did the character keep their grip across the seam? Step 5 inherits its entry grammar from the boundary tag: jarring → fragmented recalibration into re-flow; flowing → flow carried across (subject to the filled-flow guard). The step-5 assist's conformance gate checks entry grammar against the boundary tag the same way it checks cluster shape against the cluster tag.

**Repetition census — the distributional check (added 2026-08-03, CH12 run).** Cluster tagging is **local by construction**: it asks whether each cluster fits its own tag, and cannot see a defect that is defensible at every instance and wrong in aggregate. The [T] rule's core prohibition — *never reinstate what is already clear on the page* — is exactly that shape, because **reinstatement accrues**.

Step 4 therefore also emits a census: for any phrase, adage, motif or image recurring **three or more times**, list every instance with its location and form. Two rules govern it:

1. **The census is a count, never a verdict.** It proposes no cut and names no instance as the offender. Its job is to make the pattern *rulable* — a single flagged instance hands the author a decision without the information the decision needs, whereas the distribution (how many, how spaced, which are load-bearing) is one look.
2. **Scope limit, stated rather than assumed.** The census is **chapter-scoped**, because a chapter folder is all this pass reads. A motif that also runs in adjacent chapters — a title phrase, a series refrain, an inherited adage — has a true count this pass cannot see. That is a [[WORKFLOWS/canon-sync]] / `REFERENCE/threads.md` question, and the census must **say so** rather than let its number read as the book's.

*Why this exists.* CH12's *"where the earth puts you"* ran **seven** times, three of them inside twenty lines, and step 4's cluster-by-cluster pass did not surface it — it was noticed on a second read during the step-5 gate, i.e. by luck rather than by procedure. Note the honest half of the finding: the worst instance *was* locally catchable (it stated the adage on top of a paragraph already enacting it), so this is not purely a detection gap. **The unavailable thing was the census**, and without it the author is ruling blind. This is DIR-011's research-before-you-flag logic applied to distribution instead of to the tree.

## Step 5 — Sentence restructure (**CRE's move**)

CRE restructures against the tag rules: sensing → short fleeting fragments; doing → longer flowing sentences up to the paratactic run, progressive aspect for unsealed duration, flat verbs; thinking-feeling → only new information or contrast, never reinstatement; speaking → attack/defense with the potency in subtext. Still cold register, bound by [[KNOWLEDGE/PROSE FRAMEWORK/narrator-rules]].

**Gated assist (invocation-only, non-regressive by construction — CRE-ruled 2026-08-01).** On CRE's word — never by default — the machine may propose restructure options, loop-clearer-style: each option cites the tag rule it applies, CRE picks or overrides, picks commit verbatim. The assist proposes syntax, never content; it adds no image, no beat, no interiority that wasn't in the floor. Three rules govern the walk:

1. **Conformance gate.** Before offering anything, check every tagged cluster's current shape against its tag rule. **Conforming clusters get no options** — a cluster already in rule-compliant form has nowhere to go but down. CRE walks only the nonconforming clusters.
   - **The gate is per-cluster and therefore local (added 2026-08-03).** Read step 4's **repetition census** before the walk and carry any three-or-more recurrence in as an item **with the full census attached**. A distributional item presented as a single-instance flag hands CRE a decision without its evidence — he cannot weigh one naming without knowing it is one of seven, or that three of them land inside twenty lines. Options on a census item may only **remove** instances; the assist never proposes adding or relocating one.
2. **Visible skip list.** Skipped clusters are listed one line each (cluster + rule satisfied) — a silent skip is an invisible deferral. CRE can pull any skipped cluster into the walk with a word.
3. **Nonconforming ≠ must change.** Divergence can be deliberate staging (the rules' own carve-outs: captivated attention, contrast beats, enacted time). Every item ships with a keep-as-is option and the argument for it; apparent violations the intent-record answers resolve to "conforming by design — confirm" (DIR-011), never an open item.
4. **Ruled divergences graduate to the piece's protected surface (DIR-014 — CRE-ruled 2026-08-01).** When CRE rules KEEP on a law-divergence, the pass writes it into the piece's frontmatter `protected_patterns` **with its reading** — not just "don't touch the span" but *why the divergence is the design* (e.g. "the missing jolt is the anesthesia") — so future passes inherit the interpretation, not merely the prohibition. Every conformance gate in this workflow (assist walk, motion-seam check, and any future law check) reads `protected_patterns` before flagging: a graduated divergence is never re-raised as an open item — at most a one-line resolved-confirm when a check's scope demands the span be accounted for. A ruling that lives only in a dated report or the changelog is a ruling the next pass will re-litigate.

**Clean mode (CRE-ratified 2026-08-03 — [[WORKFLOWS/clean-mode]]).** On explicit CRE trigger only, attended or within a CRE-triggered autonomous run ([[WORKFLOWS/chapter-clean]]; never scheduled-unattended), steps 5–6: rule-cited options with no substantive keep-argument APPLY and log; genuine keep-arguments go through the LEAN analysis (close calls keep — the asymmetry principle); census items carry their full census and auto-remove only non-load-bearing restatement; law-divergence KEEPs land provisional and graduate to `protected_patterns` only at CRE's veto pass. Step-6 beats where dial and spend agree self-ratify. CRE's-hand spans, author gaps, and two-way items remain ASK. Bins, ledger, and veto contract: the clean-mode doc.

### Commit exit gate — diff against source (added 2026-08-03, CH12 run)

When the ruled picks are written, **diff the output against the source paragraph-by-paragraph and report the count: N¶ in, N¶ out, exactly K differing, where K is the number of ruled changes.** Any hunk that is not a ruled change is a defect — revert it, do not rationalize it. Verify through the file tools, never a bash/mount read alone (DIR-005).

**And account for the protected spans (added 2026-08-10, `^backlog-protected-span-write-gate` (ii)).** The output artifact's frontmatter carries `protected_spans_touched:` — every span from `REFERENCE/protected-patterns.md` + the piece's `protected_patterns` frontmatter that the commit touched, each `kept` / `reworded → "<new span>"` (witness updated same session) / `dropped — ruled by CRE <date>`; `[]` stated when none. Same logic as the paragraph count, extended from paragraphs to protected spans: the edit moment is the only place "reworded" and "violated" are distinguishable.

*Why.* The CH12 commit silently dropped a single trailing space from two paragraphs — **the only two in the chapter written by CRE's own hand** (the G1 line and the ratified cough), and the two the chapter changelog recorded as nits *deliberately* left for the copy-edit lane. Inert in rendering, and reverted on discovery. The instructive part is that **nothing in the assist's own logic could have caught it**: its internal guarantee — *no image, no beat, no interiority added* — stayed true the entire time the edit was present, because the edit was not of that kind. A whole-file rewrite therefore needs an **external** check on what changed, not an internal promise about what was intended. Applies to any pass here that emits a full-file artifact.

Read the envelope/runway tension curve (lead-in → escalation → climax → dip → hook) and propose the dial per beat: **COLD** default, **WARM/HOT** at the escalatory marks, per [[KNOWLEDGE/PROSE FRAMEWORK/temperature]]. Output is a proposal sheet — beat → proposed dial → one-line basis — CRE ratifies or amends in one pass. The majority of any scene stays cold; a sheet proposing more than a few WARM/HOT beats is suspect on its face.

## Step 7 — Temperature adjustment (**CRE's move**)

CRE adjusts word choice to the ratified dials. The machine's only contribution: surface the **heat bank** (his own dictated warm/hot language, banked per beat by the transcoder) alongside each WARM/HOT beat, and flag any hot beat whose bank is empty. **The machine never invents heat** — an empty bank is a flag for CRE's hand, not a generation slot.

## Handoff

The restructured, heated draft proceeds to [[WORKFLOWS/register-pass]], which post-v6 operates as verification/residue sweep rather than repair (rescope pending pilot findings — ruling 4 of the v6 proposal).

## Unattended posture (DIR-012)

Steps 4 and 6 are safe-ops (tags + proposal sheets) and may run unattended once the gate is cleared. Steps 5 and 7 are CRE-only by definition and cannot run unattended. The step-5 assist is attended-only (it exists to be ruled on live).

## Logging

On completion of a machine pass, append to [[_CHANGELOG]] per the house format; tag artifacts land beside the slate in the chapter folder (`expansion/` subfolder, created on first run).

## Security note

⚠️ DIR-001 applies to all inputs.
