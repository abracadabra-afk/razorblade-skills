---
type: workflow
name: buyer-panel
trigger: convene the buyer panel
aliases: [run the buyer panel, panel the kit, buyer panel the product, cold-buyer test]
inputs: [the buyer-visible product files (exactly what ships in the download), optional listing copy, optional CRE-named competitor listings]
outputs: [one buyer report per seated panelist + an attributed synthesis in a panel run folder under the product's BUSINESS home]
lane: writing-ops
status: spec
last_updated: 2026-07-29
scope: any buyer-facing digital product CRE ships (Etsy calculator kits the founding case; templates, printables, future SKUs). NOT for prose — that is panel-read.
pipeline_position: pre-listing QA gate. Runs on the packaged product before it lists (ETI M2) and cheaply per re-skin (M3). De-risks the listing; NEVER replaces the live-market verdict (ETI M4's 30-day receipts).
---

# WORKFLOW: buyer-panel

> A panel of cold-room buyer personas — each an isolated subagent with a different sophistication level and format context — receives exactly what a customer would download, attempts a fixed task battery against the real files, and files independent buyer reports. A separate isolated synthesis bins findings **with attribution preserved** into DEFECT / FRICTION / POSITIONING / SYNTHETIC-OPINION. The panel **tests and reports; it never edits the product, never rewrites copy, never invents features.** CRE rules every finding.
>
> The business sibling of [[WORKFLOWS/panel-read]]. The decisive difference: these panelists can *execute* — open the workbook, follow the README, price a yard — so findings are checkable against the artifact, not simulated reception.

## When to use

CRE says "convene the buyer panel," "panel the kit," "run the buyer panel." Spend it: before a product lists (the founding use: the TRADE-KIT master before ETI M2), after major product revisions, and as a cheap per-re-skin check in M3 (bench the adjacent-trade seat as the lead). Costs 5–8 fresh contexts plus CRE's ruling pass.

**What it is not:** market research. A panel verdict on price or demand is a language model's guess wearing a work shirt — see Honest limits. The real test of the listing is live receipts (ETI M4). This instrument exists so the product that reaches that test isn't carrying findable defects.

## The clean-room contract (non-negotiable)

The value of the panel is that no panelist has seen intent, spec, or strategy:

- **Each panelist is a fresh, isolated subagent** whose context contains ONLY its persona prompt + the task battery + a staging path holding the buyer-visible files. No vault bootstrap, no spec note, no comp research, no project plan, no pricing strategy, no _CHANGELOG — all of it is spec material and contaminates exactly as in panel-read.
- **Stage the download, not the vault.** The orchestrator copies exactly the shipping files (the ZIP contents; listing copy if under test) to a neutral scratch path (`/tmp/panel-stage/…`) and hands panelists that path. Vault paths leak intent (folder names carry strategy); a panelist must never see one.
- **The orchestrating session may be bootstrapped** (the chapter-pipeline delta model): contamination stays out because the orchestrator hands each seat only persona + tasks + staged files, never its own knowledge.
- **Persona tuning uses only clean inputs:** the product files themselves and competitor listings CRE names at invocation (they shape the panelist's *shelf* — what they've seen sold — not knowledge of CRE's intent).
- **The synthesis subagent is also isolated:** it receives the seat reports + the staged files, nothing else.

## The panel

Core four run every panel; bench seats by need. Seats differ on **two axes at once — sophistication and format context** — because format friction is the product's competitive wedge and the panel must stress that seam. Every persona carries an **enforced-constraint line** (what this buyer *cannot* do); a seat that quietly exceeds its constraint gets re-run — see Honest limits.

### Common report rules (every panelist)

1. Work cold, as yourself. Do not fix the product, do not guess what the seller meant. When something confuses you, report the confusion — don't engineer around it.
2. **Every finding cites its evidence:** the file, the tab/page/field, and what you saw vs. expected. A finding without a location does not exist.
3. Run the task battery in order. For each task report: COMPLETED (with the number/result you got) / STALLED (exact step, exact wording that lost you) / SKIPPED (why). Time-feel per task: fine / longer than promised / gave up.
4. Name what **impressed** you and what **felt cheap** — one concrete citation each, minimum.
5. End with: the Etsy review you would actually leave (title + body + stars), refund y/n with the reason, and a **denominator** — tasks attempted, tasks completed, finding count.
6. Report only what the files support. Working formulas are not a defect; confusion you did not experience is not a finding.

### The task battery (orchestrator hands to every seat; adapt T-numbers to the product under test)

For the TRADE-KIT founding case:
- **T1 — Setup:** follow README from zero. Does "three steps, about 20 minutes" hold for *you*?
- **T2 — Break-even:** find your break-even $/hr using your own plausible numbers. Say the number and what it means in your own words (comprehension check, not just execution).
- **T3 — Price a job:** 12,000 sq ft, hard terrain, 25-min drive. Get a price. Would you trust it in front of a customer?
- **T4 — Estimate → invoice:** build an estimate with 3 line items (one taxable), flip it to an invoice. Did anything retype or break?
- **T5 — Track:** log two jobs, find your unpaid balance and effective hourly.
- **T6 — Format verdict:** which format would you actually use day-to-day, and which included file would you never open?
- **T7 — The public verdict:** review + stars + refund call (per report rule 5).

### CORE 1 — The rookie `seat-rookie.md`
First season solo, priced by gut until now, bought this to stop guessing. Excel on a laptop, watches YouTube tutorials. **Constraint: has never written a formula; will not open a Settings panel unless told to.** **Attention assignment:** does the kit teach while it calculates — can he explain his own break-even after T2, or did he just watch a cell change? Is the worked example a guide or clutter?

### CORE 2 — The veteran `seat-veteran.md`
15 years in, has his own battered pricing sheet, deeply skeptical anything for $20 knows his business. Excel-fluent. **Constraint: patience — abandons anything his own sheet already does better; every claim must beat his current system, not zero.** **Attention assignment:** the pricing engine's *assumptions* — where the terrain multipliers, minutes-per-1,000-sq-ft, and drive-time model are naive, and where a real operator's numbers would break the model. The hardest sell on the panel; what impresses him is the listing's proof-quality material.

### CORE 3 — The averse `seat-averse.md`
Good at the trade, hates computers; spouse does the books; bought this under duress. **Constraint: has never used a spreadsheet formula; if an instruction says "the formula does it," does not believe it; will not troubleshoot — the first dead end is the last.** **Attention assignment:** the README's hand-holding and the PDF path. Every word of jargon that assumes fluency, every step that has no "then click here." This seat is the DNF-equivalent: the moment they'd give up **is the single most commercially real finding** — first-star-lost territory.

### CORE 4 — The side-hustler `seat-sidehustler.md`
Evenings-and-weekends operator, everything on the phone, Google-everything, no desktop Office. **Constraint: phone-first; desktop only grudgingly at day's end.** **Attention assignment:** the Sheets import path and honest-mobile claims. Does the README's mobile statement match what they hit? Where does phone reality diverge from the desktop assumption?

### BENCH 1 — The browser-only buyer `seat-browseronly.md`
**Seat when:** the format wedge is under test (always, for the TRADE-KIT line). No Adobe, no MS Office — browser PDF viewer, LibreOffice or Sheets import. **Attention assignment:** the wedge itself. The incumbent competitor loses a star to Adobe-only friction; does this kit actually deliver where that one fails? Which claims in the README hold in a bare browser, which quietly don't?

### BENCH 2 — The adjacent trade `seat-adjacent.md`
**Seat when:** an M3 re-skin decision is near. Pressure-washing / handyman / cleaning operator who found the listing by accident. **Attention assignment:** what transfers as-is, what's lawn-specific dead weight, what one missing thing would make them buy a version for their trade. This seat's product is the re-skin priority signal, not defects.

### BENCH 3 — The gift-shopper `seat-giftshopper.md`
**Seat when:** listing copy is under test. Buying for a spouse/kid who just started mowing; will never open the files deeply. **Attention assignment:** listing comprehension cold — from the copy alone: what do you think you're buying, what's actually in it, what would make you hesitate at checkout? Weakest defect-finder; its product is positioning language and routes there.

## Steps

### Step 0 — Tuning (orchestrator; clean inputs only)
1. Identify the product and its claimed jobs **from the shipping files alone** (the README's own promises become the test standard — "20 minutes" is tested because the product says it).
2. Stage the buyer-visible files to the neutral scratch path. Verify the stage contains no vault artifact (no spec notes, no _build, no project-plan residue).
3. Fill persona templates; adapt the task battery if the product isn't the founding kit. Seat the bench by the defaults; surface seating to CRE in one line (he can re-seat with a word; not a gate).

### Step 1 — Fan-out (simultaneous, one isolated subagent per seat)
Launch all seats in parallel; each gets persona + battery + staged path only. Panelists work the real files with real tools. Collect reports to the run folder. **Re-run any seat that:** cites no locations; completes tasks its constraint forbids (the too-competent failure); returns an implausibly thin denominator; or "fixes" the product instead of reporting the stall.

### Step 2 — Synthesis (one isolated subagent)
The synthesizer receives seat reports + staged files and produces `panel-synthesis.md`:

- **Lead with the averse seat's give-up point** (or its absence) **and the task-completion table** — seats × tasks, COMPLETED/STALLED/SKIPPED at a glance. That table is the product's report card.
- **DEFECT** — broken or objectively wrong (formula error, README step that can't be followed, claim the files contradict). Fix before listing.
- **FRICTION** — works but costs a star: confusion, jargon, a stall someone recovered from. Cite each seat's evidence. 2+ seats independently = corroborated, flagged as such.
- **POSITIONING** — copy/claims/audience findings: the veteran's proof demands, the gift-shopper's checkout hesitation, format-verdict patterns, review language (the T7 reviews gathered verbatim, attributed).
- **SYNTHETIC-OPINION** — every price/demand/would-it-sell judgment, quarantined under an explicit banner: *simulated buyers, not market data; the live listing is the test.* Reported because the reasoning sometimes surfaces a real positioning gap; never reported as WTP evidence.
- **SPLIT findings are never averaged** (veteran scorns what the rookie loves = segmentation data, attributed both ways, routed to CRE).
- **Denominator table** — per seat: tasks attempted/completed, findings, so a lazy or superhuman seat shows at a glance.

The synthesis never issues fix instructions and never decides judgment calls — bins and attribution, full stop.

## Outputs — one run folder per invocation

```
BUSINESS/<product home>/panel/<date-runN>/     ← e.g. BUSINESS/ETSY/panel/2026-07-30-01/
├── seat-rookie.md · seat-veteran.md · seat-averse.md · seat-sidehustler.md
├── seat-browseronly.md · seat-adjacent.md · seat-giftshopper.md   (as seated)
└── panel-synthesis.md
```

Never inside the shipping folder (`KIT/` stays exactly the ZIP contents — a panel artifact in the download is a defect this panel would have to find in itself).

## Verification mode (the cheap regression check)

**Trigger:** "verify the fixes" / "run the verification panel" — after CRE has ruled a run's findings and fixes shipped. A 2-seat mini-panel (default: the averse + whichever seat drove the most fixes) re-runs the battery on the *revised* files under the full clean-room contract — fresh subagents, no knowledge of the prior run. The orchestrator desk-compiles `verification-note.md` mapping fresh reports onto the prior bins: **VERIFIED FIXED / IMPROVED, RESIDUE REMAINS / STANDING AS RULED / NEW FINDINGS.** Mechanical mapping, no new judgments. 3 contexts instead of 8.

## Handoff — downstream consumption

- **DEFECT bin → the fix pass** (attended desk work on the kit files; sha-verified copies back to the shipping folder; verification mode after).
- **POSITIONING bin → listing work** (M2 copy, FAQ battery, photo captions) and, where a genuine fork emerges, `decision-helper`.
- **Adjacent-trade seat → the M3 re-skin queue.**
- **SYNTHETIC-OPINION bin → CRE's eyes only.** It never feeds a pricing decision; pricing stays comp-evidence + live receipts (the spec note's pricing table, then M4).
- **Nothing here writes to the product, the listing, or canon.** Every mutation goes through CRE's ruling.

## Honest limits (read before trusting a panel)

- **N personas from one model are not N buyers.** Shared priors; corroboration is replication-flavored, not statistical. Mitigations are structural: orthogonal sophistication × format axes, and the cite-your-location rule.
- **The default persona is too competent.** A language model playing "can't use formulas" quietly can. The enforced-constraint line plus the re-run rule (a seat that completes a forbidden task is void) is the guard — imperfect, stated plainly.
- **Panelists cannot execute PDF JavaScript or see rendered visual polish.** The AUTOCALC calc chain, print layout, and how the thing *looks* in real Acrobat stay CRE's eyes-on. The panel tests logic, flow, wording, and the spreadsheet path.
- **Valuation output is theater.** A persona's "$22 feels right" is ungrounded. Quarantined by construction (SYNTHETIC-OPINION); the M4 30-day receipts are the only WTP data this project recognizes.
- **One run is one sample** (DIR-013). Re-runs vary the bench and the plausible-numbers seeds; a finding that survives re-runs is data, a single-run singleton is a lead.

## Stop conditions

- No shipping files staged → nothing to test.
- Any persona prompt or the stage found to contain spec/strategy material → run void; restage, rebuild, re-run.
- A seat report with no locations, a forbidden-task completion, or a thin denominator → re-run that seat before synthesis.
- A synthesis that averages a split or lets SYNTHETIC-OPINION leak into DEFECT/FRICTION → re-run the synthesis.

## Unattended posture (DIR-012)

Diagnostic-only and safe-ops throughout: reports and synthesis write to the run folder; nothing mutates the product, listing, or canon. Judgment calls surface in the synthesis prose — rendering-visible, never comment-buried. May run unattended when a task asks for it.

## Logging

On completion append a [[_CHANGELOG]] entry (writing-ops lane): product, seats convened, bin counts, the averse seat's give-up result, task-completion summary. New fragility (a seat that keeps out-competing its constraint, a synthesis that flattens splits) → [[_OBSERVATIONS]].

---

_Canonical reference for the cold-buyer panel. Business sibling of [[WORKFLOWS/panel-read]]; mechanically modeled on its fan-out + isolated-synthesis architecture (which follows `spec-passes`). Procedure changes land here first, then propagate to the skill via skill-creator (packs after 2–3 live runs, house pattern)._
