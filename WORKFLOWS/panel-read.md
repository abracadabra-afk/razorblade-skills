---
type: workflow
name: panel-read
trigger: run the panel read
aliases: [panel read chapter N, convene the panel, reader panel, panel this]
inputs: [the working text (chapter draft, WIW episode, or short), optional CRE-named comps, optional bench-seat picks]
outputs: [one reader report per seated panelist + an attributed synthesis (the Pass-1-tier artifact) in a panel/ run folder]
lane: fiction
status: spec
last_updated: 2026-07-29
scope: any prose unit — Witchwood/Godsrift chapters, WIW episodes, shorts. Generalizes blind-read; the single cold read stays the cheap default for routine chapters.
pipeline_position: Pass-1 tier (clean room), sibling of blind-read. Upstream of Workshop-2 / blind-response triage. Fan-out mechanics per spec-passes; subagent invocation per the chapter-pipeline Pass-1 delta.
---

# WORKFLOW: panel-read

> A panel of clean-room reader personas — each an isolated subagent with a different critical lens — read the work simultaneously and file independent reader reports, which a separate synthesis pass bins into consensus, split, and singleton findings **with attribution preserved**. The panel **diagnoses and reports; it never edits, never rewrites, never writes CRE's prose.** CRE grades the synthesis against `brief.md` privately, exactly as with a single blind read.

## When to use

CRE says "run the panel read," "convene the panel," "panel read chapter N." Use when a single cold read isn't enough coverage: load-bearing chapters, openings, WIW episodes pre-production, marketing-serving reads (e.g. Ghost River 2e). For routine chapters, **`blind-read` remains the default Pass 1** — the panel costs 5–8 fresh contexts plus CRE's grading; spend it where it pays.

**Relationship to blind-read:** panel-read does not replace it. `blind-read` is the spec-check battery's canonical Pass 1; panel-read is the expanded instrument CRE invokes deliberately. When a panel run exists for a text, its synthesis **serves as** the Pass-1 artifact downstream (see Handoff).

## Verification mode (the cheap regression check)

**Trigger:** "run the verification read" / "verify the fixes" — after a revision cycle (panel-response, line-edit) has consumed a prior panel run's findings. **What it is:** a 2-seat mini-panel (default: GENERAL + EAR, or the seats whose findings drove the revision) reads the *revised* draft under the full clean-room contract — fresh isolated subagents, prose only, no knowledge of the prior run or the fixes. The orchestrator then desk-compiles a **verification note** (`panel/<date-runN>/verification-note.md`) mapping the fresh reports onto the prior run's bins: **VERIFIED FIXED** (not re-flagged by a fresh reader) / **IMPROVED, RESIDUE REMAINS** / **STANDING AS RULED** (replicated — data, not defect) / **NEW FINDINGS**. The mapping is mechanical, no new judgments; the two seat reports sit beside it as evidence.

Costs 3 fresh contexts instead of 7–8 — spend it to confirm a revision landed before record/bank, not as a substitute for a full panel on new text. A finding a fresh reader *replicates against a ruling* stays standing-as-ruled; it never reopens the ruling by itself. First live use: EP 01 run 2026-07-29-02 (verified the panel-response + line-edit cycle; caught one fix-relocation residue and the surviving tap-timing instant).

## The clean-room contract (non-negotiable)

The entire value of a cold read is that the reader has not seen intent. Every panelist inherits blind-read's isolation, enforced by construction:

- **Each panelist is a fresh, isolated subagent** whose context contains ONLY its persona prompt + the prose. No vault bootstrap, no register, no `brief.md`, no runway, no envelope, no `REFERENCE/*`, no threads, no DEV material — all of it is spec material and contaminates exactly like the register does.
- **The orchestrating session may be bootstrapped** (this is the chapter-pipeline Pass-1 delta model): contamination stays out because the orchestrator hands each subagent only prose + persona prompt, never its own knowledge.
- **Persona tuning uses only clean inputs** (Step 0): the prose itself, and comps CRE names at invocation. CRE-named comps are safe — they shape the panelist's *shelf*, not its knowledge of his *intent*. A persona built from spec material is a contaminated reader wearing a costume; that run is void.
- **The synthesis subagent is also isolated**: it receives the panelist reports + the prose, nothing else. A spec-aware synthesizer would discount findings that contradict intent — which is precisely the signal CRE grades for.

## The panel

Core four seats run every panel. Bench seats are seated by need (Step 0 defaults; CRE can override at invocation). Every persona shares the **common report rules** below; each differs in its **attention assignment** — what it is asked to attend to — not merely its voice. Genuinely different attention assignments are what make overlap meaningful (see Honest limits).

### Common report rules (every panelist)

1. Read cold, as yourself (the persona). Do not edit, do not rewrite, do not guess at the author's intentions.
2. **Quote a specific line for every finding.** A finding without a quote does not exist.
3. Report your **drift point** (first place attention slipped; quote the line) and, if you stopped reading, exactly where and why.
4. Name what **landed** and what **fell flat** — one quote each minimum.
5. End with your persona-verdict (in your own terms) and a **denominator**: how much of the text you actually examined, and your finding count. An implausibly thin denominator gets the seat re-run.
6. Report only what the text supports. Where it supports nothing, say nothing was there.

### CORE 1 — The slush reader / acquiring editor `panel-slush.md`

**Lens:** market. **Attention assignment:** commercial viability — pacing against professional standards, hook strength, whether the piece earns its length, reasons for acceptance/rejection, constructive notes through a publisher's eyes.

**Unit-sensitive brief (Step 0 sets it):**
- **Opening chapter / short / WIW episode → true slush:** you read submissions for a professional {GENRE} market whose recent list resembles {COMPS}. Would you pass this up the chain? Name the acceptance case and the rejection case honestly — including where in the stack you'd have stopped reading. Market-appetite read: what's selling in this space, and where does this sit.
- **Mid-book chapter → acquiring editor:** you bought this book; this chapter has crossed your desk. Does it earn its place? Would a paying reader keep turning pages? Where does it sag against the chapter's implied job? (Acceptance/rejection is a malformed question mid-book; do not ask it.)

### CORE 2 — The genre superfan `panel-superfan.md`

**Lens:** saturation and novelty. **Attention assignment:** you have read everything in {GENRE} — including {COMPS} and everything they imitate — and you are always hunting the next great one. What's fresh here, what's been done, which moves push the boundary of what you love. Expressive in both directions: name what you *loved*, loudly, and where you found room for improvement.

**Two guards written into the persona prompt:**
- Every cliché-flag must name the prior art — where you've seen this move before (a named work, or the trope's standard form). An unnamed "this is cliché" is a performed reaction, not a finding.
- **A familiar move executed well is not a defect.** Say explicitly when a trope is earned. Your credibility is that you can tell the difference.

### CORE 3 — The general reader `panel-general.md`

**Lens:** comprehension and engagement. **Attention assignment:** the current blind-read core, project-agnostic: drift point; clarity of stakes (what does the protagonist want/fear, quote the earliest line that gave it to you); whether narration outruns character knowledge; prediction (what happens next, what was planted, quote what planted it); who the characters are to each other on this evidence alone; one moment that landed vs. one told-not-shown. No genre background, no expectations — just likes good stories.

(The Witchwood-specific Pass-1 prompt in [[WORKFLOWS/spec-check]] stays canonical for that battery; this seat is its generalized form.)

### CORE 4 — The DNF reader `panel-dnf.md`

**Lens:** attrition. **Attention assignment:** read only as long as you'd genuinely keep reading. The moment you'd put it down, **stop** — and report the exact quit line and the reason in plain reader terms (bored / confused / repelled / lost trust / stopped caring), not craft vocabulary. If you'd finish, say so honestly — a false DNF is worse than none — and instead report the two nearest-miss moments where you *almost* put it down. This seat measures momentum; nobody else on the panel does, because the others finish out of duty.

### BENCH 1 — The ear reader `panel-ear.md`

**Seat when:** the work will be narrated (WIW episodes near-mandatory; any audio-bound prose). **Attention assignment:** experience the text as audio. Flag dialogue-attribution confusion (who's speaking, aloud, without the eye's backtrack), tongue-trippers and unpronounceable names, homophone ambiguity, sentences that die when spoken, rhythm flatlines. Quote each.

### BENCH 2 — The genre skeptic `panel-skeptic.md`

**Seat when:** dark content is doing heavy lifting, or a crossover question is live. **Attention assignment:** you read widely and well, but {GENRE} is not your home — it has to *earn* its effects from you rather than draw on genre goodwill. Where did the work assume goodwill it hadn't earned? On dark content specifically: mark where violation reads as **earned** (dread, consequence, weight) vs. **gratuitous** (repellent without payoff) — quote the line where it tips. End with a crossover verdict: would you hand this to a reader outside the genre.

### BENCH 3 — The reviewer `panel-reviewer.md`

**Seat when:** the read serves marketing/positioning decisions. **Attention assignment:** react in public-facing terms — the five-star pull-quote you'd write, the one-star complaint someone will write, your actual star rating with rationale, and who you'd recommend it to. Weakest defect-finder on the panel (overlaps the superfan); its product is positioning language, and the synthesis routes it there.

## Steps

### Step 0 — Tuning (orchestrator; clean inputs only)

1. **Identify the unit and genre from the prose alone**, or take them from CRE at invocation. Take comps from CRE if offered ({COMPS}); otherwise derive a genre-typical shelf from the prose's own signals. Never open spec material to tune — see the clean-room contract.
2. **Fill the persona templates** ({GENRE}, {COMPS}, unit-sensitive slush brief).
3. **Seat the bench** by the defaults above; surface the seating to CRE with the run plan (one line — he can re-seat with a word; don't make it a gate on a standard run).

### Step 1 — Fan-out (simultaneous, one isolated subagent per seat)

Launch all seated panelists **in parallel**, each a fresh subagent receiving only its persona prompt + the prose. Collect reports; write each to the run folder. Re-run any seat whose report violates the common rules (no quotes, thin denominator, a DNF that neither quits nor names near-misses).

### Step 2 — Synthesis (one isolated subagent)

The synthesizer receives the panelist reports + the prose (no spec, no vault context) and produces `pass-1-panel.md`:

- **Lead with the DNF result** — quit point (or nearest misses) up top; it is the single most commercially real finding.
- **CONSENSUS** — the same element flagged independently by 3+ seats. Highest-confidence defects. Cite each seat's quote.
- **CORROBORATED** — 2 seats. Strong.
- **SPLIT** — seats explicitly disagree on the same element (superfan loves what slush rejects). **Not averaged, ever.** Attributed both ways and framed as what it is: positioning/audience data that routes to CRE, not to revision.
- **SINGLETON** — one seat only, weighted by home turf: a DNF quit point or an ear-reader attribution trip is home-turf and stands alone; a superfan cliché-flag standing alone is noted as weak.
- **POSITIONING NOTES** — the reviewer's language, the slush market read, and the SPLIT findings' audience implications, gathered separately from the defect list so revision reads defects and marketing reads positioning.
- **Denominator table** — each seat's examined-count and finding count, so CRE can spot a lazy seat at a glance.

The synthesis preserves persona voice via short attributed quotes from the reports. It never issues fix instructions and never decides judgment calls — it bins and attributes, full stop.

## Outputs — one run folder per invocation

On the per-chapter convention, keyed like a spec-check run and kept out of the immutable trees:

```
<chapter>/spec-check/<run-id>/panel/
├── panel-slush.md
├── panel-superfan.md
├── panel-general.md
├── panel-dnf.md
├── panel-ear.md · panel-skeptic.md · panel-reviewer.md   (as seated)
└── pass-1-panel.md        ← the synthesis; the Pass-1-tier artifact
```

For units without the spec-check convention (WIW episodes, shorts): `panel/<date-run>/` beside the working draft, same contents.

## Handoff — downstream consumption

- **Workshop-2 / `blind-response` triage:** when `pass-1-panel.md` exists for the working text, it **is** the Pass-1 artifact — triage consumes it exactly as it would `pass-1-blind.md`, with findings now attributed. The brief still informs the PROBLEM / WORKING-AS-INTENDED call; the ruling stays CRE's.
- **CRE's private grading (unchanged from spec-check):** grade the synthesis against `brief.md` — Prediction vs. "Setups to plant," every answer vs. the seal schedule. **A seal leak found by ANY panelist is a leak** — leak detection is not lens-dependent; one reader naming what must stay sealed means it's on the page. Record the comparison in the brief's Grading record.
- **SPLIT and POSITIONING findings route to CRE directly** (and, where a genuine fork emerges, to `decision-helper`) — they are audience questions, not revision items.

## Honest limits (read before trusting a panel)

- **N personas from one model are not N independent readers.** They share priors; consensus is replication-*flavored*, not statistical replication. The mitigations are structural: genuinely different attention assignments (so overlap means something) and the quote-every-finding rule (so a performed persona reaction can't survive without text behind it).
- **Personas can perform their role** — the superfan generating cliché-flags because spotting them is its job. The prior-art-naming guard and the earned-trope clause exist for exactly this; a superfan report that flags without naming prior art gets the seat re-run.
- **The panel is not a grader.** Nothing here reads the brief; only CRE grades intent. The panel widens the cold read; it does not replace the spec-aware passes (2–5), the register, or CRE's rulings.

## Stop conditions

- No working text → nothing to read.
- Any persona prompt found to contain spec material → the run is void; rebuild the persona from clean inputs and re-run.
- A panelist report with no quotes, or a denominator implausibly thin for the text → re-run that seat before synthesis.
- A synthesis that averages a SPLIT into a verdict → re-run the synthesis; preserved disagreement is the product.

## Unattended posture (DIR-012)

Panel-read is diagnostic-only and safe-ops throughout: reports and synthesis write to the run folder; nothing mutates the draft, canon, or spec. Judgment stays with CRE (grading, SPLIT rulings) and is surfaced in the synthesis prose — rendering-visible, never comment-buried. May run unattended when a task asks for it.

## Logging

On completion append a [[_CHANGELOG]] entry (fiction lane): unit, seats convened, bin counts (consensus/corroborated/split/singleton), DNF result. File any new fragility (a seat that keeps performing, a synthesis that keeps flattening) to [[_OBSERVATIONS]].

---

_Canonical reference for the reader-panel expansion of Pass 1. Sibling of [[WORKFLOWS/spec-check]] (Pass 1 tier) and mechanically modeled on the `spec-passes` fan-out. Procedure changes land here first, then propagate to the skill via skill-creator (packs after 2–3 live runs, house pattern)._
