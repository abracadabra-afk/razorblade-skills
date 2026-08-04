---
type: workflow
name: clean-mode
trigger: in clean mode
aliases: [clean mode, ratify by exception, run it clean]
inputs: [any gated pass this convention names (transcoder spine-review gate, prose-expansion, register-pass), the pass's own evidence surfaces (register, protected_patterns, prior rulings, ruled terms, the census)]
outputs: [the pass's normal outputs, plus one consolidated clean-ledger.md per chapter]
lane: fiction
status: ratified — CRE 2026-08-03; pilot on WITCHWOOD CH13 (runs from this doc until propagation completes)
last_updated: 2026-08-03
scope: A mode MODIFIER, not a standalone workflow. Applies only to the passes whose deltas appear below. Never a default; never unattended.
pipeline_position: orthogonal — modifies the gate behavior of [[WORKFLOWS/transcoder]] (spine-review gate), [[WORKFLOWS/prose-expansion]], and [[WORKFLOWS/register-pass]]
---

# Clean mode — ratify-by-exception

> A gate-behavior modifier for the cleaning phase of the chapter pipeline. In clean mode, a gated pass applies its evidence-bound leanings itself, logs every one to a visible per-chapter ledger, and surfaces to CRE **only** the calls that are genuinely his — two-way flags, his own words, protected-span questions, developmental seams. Ratification moves from *pre-write gate* to *post-write veto during the line pass CRE was already going to make.*

## Why this exists (the CH12 measurement, 2026-08-03)

CH12 WHERE IT PUTS YOU cost CRE ~25 discrete rulings across 5 gate sessions for a net of ~4 changed sentences (step 5: 4 edits · step 7: no-op · register sweep: 0 edits). The rulings split cleanly:

- **Rule-application calls carrying a leaning** — the 31-beat temp dial, M1/M2, most of the W1–W8 walk — CRE accepted at ~100%. Pure decision fatigue, no signal.
- **Author-content / two-way calls** — G1 (the machine's likely guess would have split his line wrong), the cough seat (his placement beat the map's sketch), S1's carrier choice, and the three optioned register calls he ruled back — **which were exactly the three the machine had flagged two-way, 3/3.**

The passes already distinguish decidable from undecidable; they just gate on both. Clean mode routes on that distinction. It is **class-based, never threshold-based** — DIR-014's corollary measured confidence thresholds failing in both directions; the classifier here is the pass's own evidence structure, i.e. the reasoning stage, which is where DIR-014 says the problem belongs.

**The risk bound that makes this safe:** clean mode is licensed only for the cleaning phase, upstream of CRE's own line-by-line pass before `land-chapter`. A wrong auto-apply costs one reversion in a pass he was making anyway; the sweep-mode design charges ~25 interrupts to prevent it. Chapters CRE will NOT line-pass before landing must not run clean mode.

## Invocation

- **Explicit at trigger, every time:** "run the register **in clean mode**," "expansion steps 4–5 **clean**." No trigger phrase, no clean mode.
- **Sweep mode (the current, fully gated behavior) stays the default** for every pass, every project.
- **Three postures, not two (amended 2026-08-03, CRE-ratified — the autonomous posture):**
  1. **Attended-interactive** — CRE present, ruling live. Clean mode runs.
  2. **CRE-triggered autonomous** — CRE fired the run (e.g. [[WORKFLOWS/chapter-clean]]), ruled the author gate, and walked away; the clean-mode stretch executes without him **because the safety was never his presence during APPLY — it is the hard-ASK list plus the served veto gate.** Requires all three: an explicit CRE trigger this session, the author gate ruled, and Gate B + the clean-ledger armed with the `land-chapter` stop condition serving them. Clean mode runs.
  3. **Scheduled-unattended** — pollers, scheduled tasks, anything nobody fired. Clean mode is **forbidden**; the full DIR-012 posture holds: safe ops write, judgment defers, never self-clear a gate.

  The original "attended sessions only" rule was mis-aimed at presence; the binding conditions were always the ASK list and the veto. Posture 2 makes that explicit. What separates 2 from 3 is the human trigger and the armed, served exit gate — not the wall-clock attendance in between.

## The three bins

Every item a pass would previously have gated now lands in exactly one:

### APPLY — evidence-bound, applied and logged
The leaning cites a **binding surface** — a register section, `protected_patterns`, a prior dated ruling, the ruled-terms table, canon (`threads.md`/`bible.md`), or the pass's own census — **and** the pass generated no substantive craft counter-argument. Applied immediately; one ledger line. This is DIR-011 extended a notch: tree-answered currently means "resolve and present as one-tap confirm"; in clean mode it means "apply and log."

### LEAN — analyzed, then routed
A leaning exists but so does a counter-argument. Run the [[WORKFLOWS/decision-helper]] **backend** (Step 3 — options assembled, evidence weighed, one-line basis) inline, without the DECISIONS/ ledger ceremony — the analysis logs to the chapter's clean-ledger instead (micro-calls don't belong in the life ledger). If the evidence decides it → **APPLY**, with the analysis line. If it stays two-way → **ASK**.

### ASK — CRE's, always
Reaches him, and only these classes (see the hard list below). Collected and presented in the fewest gate moments the chain's ordering allows — items that don't block a downstream step batch to a single end-of-chain gate; items that do (e.g. a step-5 structural call step 6 must read) gate in place.

## The asymmetry principle — auto-KEEP is cheaper than auto-EDIT

A wrong keep leaves CRE's text standing, and his line pass reads that line regardless. A wrong edit alters text. So when a LEAN analysis is close, **default to keep-and-log, not edit** — the protective bias the register already encodes ("the sentence stays unless an edit is earned"), applied to the mode. Corollary: a KEEP auto-ruled by the machine is **provisional** — it lands in the ledger as `APPLY-keep (machine)`, and graduates to `protected_patterns` only when CRE's veto pass ratifies it (see Ledger). Machine keeps never write to a DIR-014 binding surface directly; `protected_patterns` stays a CRE-ruled surface.

## Hard-ASK list — never auto-ruled, in any mode

1. **CRE's desk-authored spans** — lines recorded as his hand in the chapter changelog (CH12: the G1 line, the cough). Any alteration, **including mechanical** (the trailing-space incident happened twice in one day; a standing deliberate ruling outranks "mechanical fixes are free").
2. **Author gaps (G#)** — his words only, ever.
3. **Two-way flags** — anything the pass itself frames with substantive arguments both ways after the LEAN analysis, and every transcoder `optioned` verdict by definition.
4. **Protected-span cross-reason defects** — a defect of type B inside a span protected for reason A (the JC1 class). The protection's reading does not transfer; CRE rules whether it covers.
5. **Developmental seams requiring a choice** — re-dictate / restructure / carrier A-vs-B. The organic-process guard is not mode-sensitive.
6. **Anything canon-contradicting** — clean mode does not extend to `canon-sync` contradictions or any pass outside the deltas below.

And one absolute that is not an ASK because it is a **never**: clean mode adds no generative license. No new image, beat, interiority, or heat, in any bin — APPLY commits only edit classes the pass was already licensed to propose (deletion of flagged spans, floored forms, joins/splits, ruled-option syntax). The "AI executes, CRE creates" law is untouched by this mode.

## The clean-ledger — one per chapter, the veto surface

`<chapter>/clean-ledger.md`, created on the chapter's first clean-mode pass, **appended** by each subsequent one. Rendering-visible prose/table, never HTML comments (DIR-012 clause 4). One row per bin event:

```
| # | pass | span/item | action | basis | veto |
```

- `action` ∈ `APPLY-edit` · `APPLY-keep` · `resolved-confirm` (DIR-011 class) · `LEAN→APPLY (analysis: …)` — plus the pass's ASK items listed at the foot with their eventual rulings, so the chapter's whole decision history reads in one place.
- `basis` names the binding surface or analysis in one line. A row with no citable basis is a row that belonged in ASK — that is the audit test.
- `veto` — ☐, flipped by CRE during his line pass. A vetoed `APPLY-edit` reverts via a normal revision event; a vetoed `APPLY-keep` re-opens as an ASK item.

**The veto pass is served, not hoped for (DIR-012 clause 5):** `land-chapter` treats an unreviewed clean-ledger as a stop condition — before promote, CRE either says "ledger reviewed" or rules the outstanding rows. His line pass and the veto pass are the same pass; the attestation is one line.

**Diff exit gate applies to every clean-mode commit** — N¶ in, N¶ out, exactly K differing where K = ledger `APPLY-edit` rows for that commit; any unledgered hunk is a defect, revert it (the prose-expansion exit gate, made mode-law).

---

## Per-workflow deltas

### [[WORKFLOWS/transcoder]] — spine-review gate (delta: modest, the gate mostly earns its cost)

| Item class | Sweep (today) | Clean mode |
|---|---|---|
| Floor normalizations (deny-list) | already ungated | unchanged |
| Seam flags the tree/brief answers | presented resolved-confirm | **APPLY** (`resolved-confirm` ledger row, no gate stop) |
| Genuine developmental seams | gate | **ASK** (hard list #5) |
| `optioned` register calls | gate | **ASK** (hard list #3 — v6's optioned verdict hit 3/3 on CH12; do not touch what works) |
| Garbles (G#) | open-loops | **ASK** (hard list #2) |

CH12 restated: the gate would have carried 5 items instead of 7. The gate survives clean mode — it is the one gate whose calls are mostly real.

### [[WORKFLOWS/prose-expansion]] — steps 4–7 (delta: the big win)

- **Step 4** (tags + census): unchanged — annotation safe-op.
- **Step 5 assist walk:**
  - Nonconforming item, option cites the tag rule, no substantive keep-argument (the W1 missing-*as* class, the W3 redundant-tag class) → **APPLY-edit**.
  - Item with a genuine keep-argument → **LEAN** → analysis → APPLY or ASK. Close calls keep (asymmetry principle).
  - Motion-seam / law-divergence KEEP recommendations with readings (the M1/M2 class) → **APPLY-keep (machine)**, provisional, graduates on veto-pass ratify.
  - **Census items** → **LEAN** with the full census attached; an instance auto-removes only when the analysis shows it is non-load-bearing restatement under the [T] reinstatement rule (the W8 three-in-twenty-lines class); options remain remove-only; anything load-bearing or close → ASK.
  - Visible skip list: unchanged.
- **Step 6 temps:** beats where dial and current spend agree (28/31 on CH12) → **APPLY** (self-ratifying map). Judgment items whose lean is *leave heat out / move dial to meet text* → **LEAN**, and these decide easily (two of CH12's three were arguments for doing nothing). Any beat whose ratified dial would require **text change** → that is step 7, CRE's move by definition — ASK/his hand, unchanged.
- **Step 7:** CRE-only, unchanged. Empty-bank-at-HOT stays a flag for his hand.

CH12 restated: steps 4–7 would have surfaced ~2–3 items instead of ~13 (8 walk + 2 seams + 3 temps).

### [[WORKFLOWS/register-pass]] — post-v6 verification sweep (delta: judgment calls get the LEAN treatment)

- Settled-set matching (prior rulings, no re-litigate) → unchanged, now also a `resolved-confirm` ledger row each.
- **Judgment calls** → **LEAN** each: analysis inline; decided → APPLY (keeps cost nothing — asymmetry principle); still two-way → ASK. On CH12's four: JC2/JC3 likely LEAN→APPLY-keep or a ruled minimal cut, JC4 is a recalibration note not a text call (APPLY as a voice-spec annotation), **JC1 is hard-ASK #4** — protected-span cross-reason, structurally CRE's.
- Mechanical items on CRE's-hand lines → **ASK** (hard list #1), codifying this run's override of "mechanical fixes are free."
- **Bundled fix (`^backlog-protected-patterns-binding`, #p1):** register-pass reads the working text's `protected_patterns` frontmatter (and `REFERENCE/protected-patterns.md` where a project keeps one) **before flagging**, in both modes. CH12's five ruled spans were protected only by the register's own no-re-litigate clause — `^obs-177`'s exact shape, one week after DIR-014. This lands with clean mode because it is the same seam: rulings must sit on surfaces the pass actually reads, or the machine cannot be trusted to apply them.

---

## What clean mode never does

- Never runs from a scheduled task or any run CRE didn't fire this session (posture 3), never by default, never on a chapter CRE won't line-pass before landing.
- Never generates prose, heat, images, beats, or interiority — no new license in any bin.
- Never touches CRE's desk-authored spans or author gaps.
- Never writes a machine ruling to `protected_patterns` or any DIR-014 binding surface — provisional keeps wait for the veto pass.
- Never extends past the three deltas above without its own ruled delta here first.
- Never substitutes for the register, the narrator rules, or any craft authority — it changes who ratifies, not what the rules are.

## Propagation checklist (DIR-016 — on CRE's ratify of this doc)

A mode spanning three workflows is a change on every executing surface. On ratify:

1. ~~This doc → `status: ratified`~~ (the ratify itself).
2. `WORKFLOWS/transcoder.md` — one short "Clean mode" pointer block in the spine-review-gate section.
3. `WORKFLOWS/prose-expansion.md` — pointer block under the step-5 assist rules + step 6.
4. `WORKFLOWS/register-pass.md` — pointer block + the `protected_patterns` binding fix (its doc is `last_updated: 2026-06-19` and needs it regardless).
5. `_SKILLS MAP` — one trigger row ("… in clean mode" → this doc).
6. Installed skills — announce-the-gap applies (DIR-009): until repack, any skill-routed run of these passes leads with "canon carries clean mode; installed copy predates it" and runs from the doc when attended.

Until all six land, clean mode runs **from this doc, attended, by explicit trigger only** — which is also the pilot posture.

## Pilot — WITCHWOOD CH13

First chapter through the dictation route after ratify runs steps in clean mode by CRE's per-pass trigger. Exit questions, answered from the receipt not from theory: (a) how many items reached ASK vs the sweep-mode counterfactual; (b) did any APPLY get vetoed at the line pass — every veto is a misrouted class, tighten the class, not a threshold; (c) did the clean-ledger read well as a veto surface inside his line pass, or does it want a different shape; (d) total ratification minutes vs CH12's hours. 2–3 chapter runs before any skill packs (house rule).

---

_Canonical reference. Per [[_SKILLS MAP#Cowork skills]], procedure changes land here first, then propagate per the DIR-016 checklist above._
