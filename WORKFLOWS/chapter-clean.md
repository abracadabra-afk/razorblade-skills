---
type: workflow
name: chapter-clean
trigger: clean the chapter
aliases: [run the chapter clean, one-sweep the chapter, run the chapter chain, chapter clean, clean it mode B]
inputs: [queued dictation for the chapter (dictation entry) OR an existing draft.md (mode B — existing work), the per-chapter folder, the project REFERENCE/ canon (register, narrator-rules, voice-spec, contamination-checklist), KNOWLEDGE/PROSE FRAMEWORK/ canon]
outputs: [near-finished draft.md (status register-swept or register-revised), the chapter clean-ledger.md, one consolidated Gate B ruling sheet, one consolidated changelog entry]
lane: fiction
status: draft — CRE-ratified 2026-08-03 (incl. the autonomous posture); pilot on WITCHWOOD CH13; packs after 2–3 live runs
last_updated: 2026-08-03
scope: Projects on the per-chapter folder convention running the v6/slate route (transcoder → expansion → register). First adopter — Witchwood. The dictation-route sibling is [[WORKFLOWS/chapter-pipeline]], which never runs the Transcoder; the two orchestrators stay separate.
pipeline_position: The v6-route orchestrator — wraps transcoder v6.1 → spine gate → prose-expansion 4–7 → register-pass into one trigger with exactly two CRE sittings. Tier-1 runner in [[WORKFLOWS/pipeline]] § QA tiers.
---

# WORKFLOW: Chapter Clean (the v6-route one-sweep orchestrator)

> One trigger takes a chapter from queued dictation to near-finished draft with **two CRE sittings**: the author gate (rule and walk away) and the end gate (remaining rulings + ledger veto, folded into the line pass CRE makes before landing anyway). Everything between runs autonomously in [[WORKFLOWS/clean-mode]] under its **CRE-triggered autonomous posture** (posture 2, ratified 2026-08-03). Born from the CH12 measurement: five manually-prompted gate sessions, ~25 rulings, ~4 changed sentences — and CRE sitting there prompting each next step.

## ORCHESTRATOR ONLY — the iron rule

This doc holds **no craft, register, expansion, or QA logic of its own.** It sequences existing legs, preserves every leg's gates and exit checks unchanged, and inherits procedure changes by only ever *calling* the legs (the [[WORKFLOWS/land-chapter]] pattern). A procedure change belongs in the leg doc, never here — `skill-audit` flags the drift otherwise.

## The shape

```
TRIGGER  "clean the chapter <N>"                        [CRE — sitting 1 begins]
  └─ Leg 0  dictation-preflight    envelope.md authored from the queued dictation (skipped if present)
  └─ Leg 1  transcoder v6.1        slate: floor + ledgers + heat bank + scene map + seam flags
GATE A — the author gate           seams · optioned calls · garbles · author gaps · scene-map ASKs
                                    [CRE rules, ~minutes after trigger — sitting 1 ends; he walks]
  └─ AUTONOMOUS STRETCH (clean mode, posture 2 — each leg a fresh subagent, strictly sequential)
     Leg 2  prose-expansion 4      POV/transition tags + two-layer census        (safe-op)
     Leg 3  prose-expansion 5      assist walk, clean bins; APPLY commit + diff gate
     Leg 4  promote-revision       expansion rev → draft.md (expansion-revised)
     Leg 5  prose-expansion 6      temperature dial, self-ratifying where dial=spend
     Leg 6  prose-expansion 7      no-op or flag — machine never writes heat; text-change needs → Gate B
     Leg 7  register-pass          verification sweep, clean bins; rev only if edits earned
     Leg 8  promote-revision       register rev → draft.md (only if Leg 7 wrote one)
GATE B — the end gate              remaining ASKs + step-7 hand items + clean-ledger veto
                                    [CRE — sitting 2, folded into his line pass; served by land-chapter]
```

## Entry mode B — existing work (CRE-ratified 2026-08-03)

The same two-sitting shape for a piece that already has prose — the orchestrated form of [[WORKFLOWS/prose-expansion]]'s Entry mode B (EP 01 *Happening Near You*, 2026-08-01, is the reference traversal; it took the multi-sitting manual form this mode retires). This is the uniform **back-catalog upgrade instrument**: pre-v6 Witchwood chapters, Ghost River 2e chapters, WIW episodes.

- **Detection at trigger:** no queued/bound dictation + `draft.md` carrying real content → mode B (or CRE says "clean it, mode B"). Both a queued clip *and* a live draft → ask, never guess.
- **Leg 0-B (envelope):** where `envelope.md` is absent/unfilled, derive it from the draft + ruled canon (the transcoder v5.1 standalone derivation rule — per-segment provenance, `status: derived — author confirms` at Gate A; never fabricate unruled facts).
- **Leg 1-B (floor sheet, replaces the slate):** transcoder Operation 3 run *diagnostically* — a verdict sheet in the piece's folder, `draft.md` untouched. `protected_patterns` + prior rulings excluded or presented resolved-confirm (DIR-011), per the mode-B law in the prose-expansion doc.
- **The sheet is binned, not walked — with the mode-B bias: LEAN-default, never APPLY-direct.** The machine never auto-floors a line of finished work, even a clean deny-list hit: every floor item runs the LEAN analysis; decided edits apply and log, close calls **keep** and log (the asymmetry principle, weighted harder here — an existing work has already passed CRE's eye, and *"keep — performance"* is a live verdict far more often than on raw dictation); genuine two-ways reach Gate A. Loosen this bias only from pilot receipts, never from theory.
- **Gate A-B holds the residue:** two-way floor items, developmental seams the cold diff exposes, the derived envelope confirm.
- **From there the stretch is identical:** ruled/decided picks commit as a floor revision → promote (`status: floor-revised` — the status names where the text came from) → expansion 4–7 → register sweep → Gate B + ledger. DIR-017 is untouched — mode B never goes near the mic.

## Why two gates, not one

The chain has a hard ordering constraint: **no expansion pass ever runs on an ungated floor** (transcoder law), and author gaps are CRE's words — the census, the dial, and the register cannot do honest work around a hole where a climax line goes. So the ASK items split by *when they block*: Gate A holds what blocks the stretch (and it is the gate that earned its cost on every CH12 item — G1, the cough seat, the carrier choice, the optioned calls at 3/3); Gate B holds everything clean mode routed to ASK downstream, plus the ledger veto. Gate A cannot be deferred; Gate B cannot be brought forward without re-serializing CRE into every leg. Two is the honest minimum.

## Steps

### Step 0 — Vault sentinel + posture declaration
Read `_DIRECTIVES.md`; confirm `type: ai-os-brain` + `file: directives`; mismatch → halt. Declare at the top of the run report: **CRE-triggered autonomous (clean-mode posture 2)** — this run was fired by CRE this session; it is not a scheduled task and must never be one (posture 3 forbids clean mode). Verify the installed-skill version gap per DIR-009's announce-the-gap clause: each leg runs from its canon `WORKFLOWS/<name>.md` where the installed skill lags.

### Step 1 — Legs 0–1: bind, envelope, slate
**Binding (at trigger).** The [[WORKFLOWS/dictation-runner]] never binds a clip to a chapter (its scope rule); this orchestrator does. Pick-up point: **`_DICTATION INBOX/_reconciled/done/`** — the name-reconciled transcript, *not* the `_drafts/<clip>-clean.md` cleanup copy (cleanup is the dictation route's instrument; the transcoder consumes reconciled-raw and handles the mechanical layer itself — CH12 precedent, its changelog verbatim: *"dictation landed to `dictation/` from `_DICTATION INBOX/_reconciled/done/`"*). Copy byte-verified into `<chapter>/dictation/`, archive original kept. **Clip↔chapter match is confirmed with CRE at trigger, never guessed** — name the clip(s) being bound in the Gate A screen; a chapter's dictation may span multiple clips.
**Leg 0:** if the chapter has no `envelope.md` (or it is unfilled), run [[WORKFLOWS/dictation-preflight]] to author it from the bound dictation — ungated machine work; the segmentation is presented for confirmation at Gate A (CH12 precedent: 4 segments where CRE spoke 3, collapse-if-unwanted noted). **Leg 1:** run [[WORKFLOWS/transcoder]] on it. Output: the four-file slate run incl. floor ledger, heat bank, scene map. If the chapter already has a **gated** floor, skip to the stretch.

### Step 2 — Gate A (the author gate; same sitting as the trigger)
Present in one screen: developmental-seam flags (tree-answered ones already `resolved-confirm`, per the transcoder's clean-mode block), optioned register calls, garbles, author gaps, and the scene map's ASK-class items (plausibly-deliberate repetition, functionless exchanges). CRE rules; author gaps get his words — **written into a new derived slate run** (`slate_scaffold.py derive --parent NN`, CRE-ruled 2026-09-02: every written run stays immutable; the gated run is never edited and `draft.md` is not the gap surface), then verbatim-stitched from that run. The clean-ledger rows for this leg append to `<chapter>/clean-ledger.md`, chapter root. **The stretch does not start until Gate A is fully ruled** — a partially ruled gate halts here and says so. If CRE calls a choreographer session off a Gate A item, the run pauses for it (choreographer stays pull-only, tier 2).

### Step 3 — The autonomous stretch (legs 2–8)
Each leg runs in a **fresh subagent** with only: its canon doc, the chapter folder paths, the project REFERENCE surfaces its doc names, and the clean-ledger. Strictly sequential — the ordering is load-bearing (the dial reads the restructured text; the register reads the promoted draft). Every leg runs its own exit checks unchanged (diff gates, DIR-004 parse gates, DIR-005 file-tool verification); every clean-mode bin event appends to `<chapter>/clean-ledger.md`. The orchestrator passes file paths and statuses between legs, never content it might paraphrase.

**Leg-4/8 note (promote):** [[WORKFLOWS/promote-revision]] predates the expansion route (`^backlog-promote-revision-expansion-route`) — until that lands, the orchestrator applies the installed skill's general rule explicitly: *the status names where the live text came from* (`expansion-revised`, then `register-revised` only if Leg 7 wrote a rev), carries `protected_patterns` forward explicitly, and normalizes lineage onto `source_slate`.

### Step 4 — Gate B (the end gate)
Compile one sheet: every ASK item the stretch collected (register judgment calls, close-call LEANs, step-7 text-change needs with their heat banks) + the clean-ledger for veto. Present it as the front matter of CRE's line pass. Gate B is **served** (DIR-012 clause 5): `land-chapter`'s stop condition — an unreviewed clean-ledger blocks promote — is the standing mechanism; no new task needed.

**Post-ruling re-runs are machine work:** if a Gate B ruling invalidates upstream output (a census cut changes a scored beat; a register ruling moves a temp), the affected leg re-runs mechanically and the ledger annotates. CRE never re-rules what a re-run merely re-derives.

## Stop conditions
- Vault sentinel fails → halt.
- Run was initiated by a scheduled task or any non-CRE trigger → **refuse** (posture 3; clean mode forbidden).
- Gate A not fully ruled → halt at Gate A; report what waits.
- Any leg's own self-test or exit gate FAILs → halt at that leg, report partial state; never improvise past a leg failure.
- A promote leg's lineage mismatch → halt the chain.
- Chapter lacks the per-chapter convention or the project lacks `REFERENCE/register.md` → halt (the legs' own preconditions).

## Logging
One consolidated entry to the chapter `changelog.md` + the vault [[_CHANGELOG]] (fiction lane) covering the whole run — legs run, Gate A rulings, ledger counts (APPLY-edit / APPLY-keep / resolved-confirm / LEAN→APPLY / ASK), Gate B contents. Deferred items live in the Gate B sheet + `open-loops.md`; fragilities to [[_OBSERVATIONS]]; follow-ups to [[_BACKLOG]] (DIR-003).

## Pilot — WITCHWOOD CH13 (shared with clean-mode + v6.1)
CH13 runs this orchestrator as its route, which pilots all three ratified 2026-08-03 designs in one receipt: clean mode's bins, the v6.1 scene map, and the two-sitting shape. Exit questions add to clean-mode's list: (e) did Gate A hold everything that actually blocked the stretch, or did a mid-stretch halt surface a mis-binned item; (f) wall-clock of the autonomous stretch; (g) did the two-sitting rhythm hold, or did CRE get pulled back in between. Packs after 2–3 live runs (DIR-009 chain); until then it runs from this doc via the trigger index.

---

_Canonical reference. Orchestration-only; procedure changes land in the leg docs. Per [[_SKILLS MAP#Cowork skills]], changes here propagate to the skill via skill-creator once packaged._
