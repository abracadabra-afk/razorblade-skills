---
type: workflow
name: prose-expansion
trigger: expand the prose
aliases: [run the expansion, tag the spine, expansion passes]
inputs: [a CRE-gated floor draft (transcoder v6 slate, spine-review gate cleared), the synthesis ledger's heat bank, the chapter envelope/runway tension curve, KNOWLEDGE/PROSE FRAMEWORK/ canon (sentence-structure.md + temperature.md + narrator-rules.md)]
outputs: [POV-tagged spine, temperature-tag proposal sheet, CRE's restructured/heated draft]
lane: fiction
status: draft — packs after 2-3 live runs
last_updated: 2026-08-01
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

## Step 4 — POV tagging (machine, annotation only)

Tag every spine sentence/cluster against the [[KNOWLEDGE/PROSE FRAMEWORK/sentence-structure]] taxonomy: **SENSING** / **DOING** / **THINKING-FEELING** / **SPEAKING**. Output is a tagged copy of the floor (inline tags or a margin map — whichever CRE ruled for the project; default inline `[S]/[D]/[T]/[SP]` markers). No prose is touched. Ambiguous spans get a dual tag + one-line note, never a guess presented as a ruling.

## Step 5 — Sentence restructure (**CRE's move**)

CRE restructures against the tag rules: sensing → short fleeting fragments; doing → longer flowing sentences up to the paratactic run, progressive aspect for unsealed duration, flat verbs; thinking-feeling → only new information or contrast, never reinstatement; speaking → attack/defense with the potency in subtext. Still cold register, bound by [[KNOWLEDGE/PROSE FRAMEWORK/narrator-rules]].

**Gated assist (invocation-only, non-regressive by construction — CRE-ruled 2026-08-01).** On CRE's word — never by default — the machine may propose restructure options, loop-clearer-style: each option cites the tag rule it applies, CRE picks or overrides, picks commit verbatim. The assist proposes syntax, never content; it adds no image, no beat, no interiority that wasn't in the floor. Three rules govern the walk:

1. **Conformance gate.** Before offering anything, check every tagged cluster's current shape against its tag rule. **Conforming clusters get no options** — a cluster already in rule-compliant form has nowhere to go but down. CRE walks only the nonconforming clusters.
2. **Visible skip list.** Skipped clusters are listed one line each (cluster + rule satisfied) — a silent skip is an invisible deferral. CRE can pull any skipped cluster into the walk with a word.
3. **Nonconforming ≠ must change.** Divergence can be deliberate staging (the rules' own carve-outs: captivated attention, contrast beats, enacted time). Every item ships with a keep-as-is option and the argument for it; apparent violations the intent-record answers resolve to "conforming by design — confirm" (DIR-011), never an open item.

## Step 6 — Temperature tagging (machine proposes, CRE ratifies one-pass)

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
