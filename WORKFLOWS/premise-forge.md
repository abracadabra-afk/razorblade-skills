---
type: workflow
name: premise-forge
status: spec — run by hand/in chat; graduates to a packed skill after 2–3 live runs
triggers: ["forge the premises", "run the premise forge", "fill the bag", "build the premise bag", "size this idea", "what does this want to be"]
lane: 5 (writing-ops) + 1 (fiction)
created: 2026-08-09
---

# premise-forge

The **premise developer** — an attended, feeling-first instrument with two jobs: (1) keep the WIW `CANDIDATES/` bag stocked with gut-ratified, short-form-contained story premises, so a weekend creative slot always presents work instead of demanding origination (the founding mission; the upstream-most tool in the episode route, formalizing S0); and (2) **size any story idea CRE brings** against the format spectrum — short / novella / novel / series — honing it toward the container it actually wants (the format-aware extension, CRE-ruled 2026-08-09 same session). One tool, one measurement, different buckets.

**The problem it exists to kill:** when no work is presented, CRE spends his highest-creative-level time *creating* work rather than *executing* it — the executive-dysfunction / decision-overwhelm tax. premise-forge time-shifts premise origination into a deliberate session so the mic never waits on a blank page.

> **Design provenance (CRE-ruled 2026-08-09, premise-forge design session):** the original three-skill concept (market-trend runner → premise developer → pre-dictation scaffold) was collapsed to this one skill. The market layer was deleted on CRE's ruling — *"I won't be interested in the story at all if I'm trying to check the box for a 'market'"* — trend-chasing is a trap he named from experience. The pre-dictation scaffold already exists as the episode route (episode-init → episode-runway). What remained is this: feeling-first premise development, gut-gated, banked.
>
> **Format-aware amendment (CRE-ruled 2026-08-09, same session):** generalized from shorts-only to the format spectrum — same measurement, different buckets. Three modes (FILL / DECLARED / OPEN), format verdict in Step 6 (world-load axis added), larger formats bank to `WRITING/SEEDS/` (sized, never scheduled), the bag stays shorts-pure, and the generation carve-out stays FILL-mode-only.

## Modes (declared at session open)

The tool **always measures**; the mode only sets the target format and what happens on a mismatch:

| Mode | CRE says | Target | On a larger/mismatched verdict |
|---|---|---|---|
| **FILL** | "fill the bag" / "forge the premises" / "I need shorts" | short-form, locked | **Size, bank to SEEDS, park — never develop in-session.** The session returns to shorts. |
| **DECLARED** | "here's an idea for a series/novel/novella" | CRE's declaration | Honing shapes toward the target; if the measurement contradicts it ("you said novella; this measures like a series"), surface with a one-line basis — **CRE rules.** A genuine format fork (novella vs. duology) hands to decision-helper. |
| **OPEN** | "here's an idea — I don't know what it wants to be" | none | The format verdict converges *through* the honing conversation; it lands when the premise stops moving. |

**The mode boundary is a guard, not a convenience.** In FILL mode a shiny larger idea is the executive-dysfunction failure wearing a productivity costume — the known gravity is that everything blows into a novel, and a Saturday fill session must not wander off following one. Two minutes to size and bank it; then back to shorts. No trigger stated → default by opener: "fill the bag"-family → FILL; "here's an idea…" → DECLARED or OPEN per whether he names a format.

## The sanctioned-generation boundary

Every gate in this vault carries the organic-process guard: *never invents story options.* premise-forge is the one deliberate exception, and the carve-out is narrow:

- **Generation is sanctioned at the what-if layer only, and only in FILL mode**, per CRE's own standing instruction in [[WRITING/SHORTS/PREMISES]] — a document that literally instructs an AI to produce *short-form* premises in his format. This workflow formalizes that existing, CRE-ruled practice. **In DECLARED and OPEN modes the tool generates nothing**: CRE brings the idea; the tool sizes, challenges, and hones his material — cleanly inside the guard, no carve-out needed. "Brainstorm me novel premises" would be a new ruling, made explicitly, never inherited from this one.
- **Authorship lives in CRE's selection and honing.** Nothing enters the bag without his felt yes; his language always supersedes proposed phrasing.
- **Everything downstream stays guarded.** Beats, scenes, dialogue, prose — the guard holds in full. This skill never writes a word of story.

## Pipeline position

```
premise-forge (S0)  →  bag: CANDIDATES/<title>/triage.md
                          ↓  CRE picks (weekend slot / next-up)
episode-init (S1)   →  gate confirms triage pre-answers → scaffold
episode-runway      →  runway carve
mic → drafting engine → rough draft banked
                          ↓  THE SIT (between rough draft and author pass — CRE-ruled 2026-08-09)
dev-edit → AUTHOR PASS → panel-read → line passes → record prep
```

**The sit ruling.** The sit-with-it phase lives **between rough draft and author pass**, not between gate and dictation. Bag → gate → runway → mic *same day* is sanctioned. A steady cadence of banked rough drafts means the author pass always has aged material waiting — the sit happens on drafts, not on premises.

**The two-buffer economy.** This workflow maintains buffer 1 (premise bag → feeds the mic); the drafting engine maintains buffer 2 (rough-draft bank → feeds the author pass). A weekend slot draws from either by energy: generative → pick and dictate; editorial → author-pass a banked draft. Both refill from normal operation; work is always presented, never originated cold.

## When to use

CRE says "forge the premises" / "fill the bag" (FILL mode), brings a story idea with a named format ("here's a series idea" — DECLARED), or brings an idea he can't size ("I don't know what it wants to be" — OPEN). Also fires when the bag hits its min-fill floor. **Attended, never scheduled** — the gut gate is the load-bearing mechanism and cannot run unattended (DIR-012 clause 1 would strip the whole point). Do NOT use it to gate/scaffold an episode (episode-init), synthesize a dictated talk-through (brainstorm), route dev talk (dev-capture), or **develop** larger-format material — this tool sizes and banks seeds; developing one is dev-layer work behind a portfolio decision.

## Inputs

- **A feeling / human condition** — from CRE ("loneliness," "jealousy," "self-worth," "resignation"), OR offered by the variety scan (Step 3) when he arrives without one. CRE may also point at a [[VIBES/_VIBES|VIBES]] capture fragment as the seed — *at his pointer only; never mine VIBES (or any LIFE surface — DIR-015) automatically.*
- **The premise grammar** — [[WRITING/SHORTS/PREMISES]]: knot · scenario-that-challenges-the-knot · tensional constraint · topical peg, in the one-sentence "What if…" form.
- **The corpus for variety** — `EPISODES/*/premise.md` + `CANDIDATES/*/triage.md` (knots, conditions, subgenres, constraint shapes already used).
- **Container bands** — [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]] §3b: standard ~2,000–2,800 words ≈ 15–20 min.

## Outputs

- Banked short-form candidates: `WRITING/SHORTS/CANDIDATES/<WORKING TITLE>/triage.md`, each pre-answering the episode-init Pass-1 gate.
- Banked larger-format seeds: `WRITING/SEEDS/<WORKING TITLE>/triage.md` with `format:` + the measurement that produced the verdict — sized, never scheduled.
- A ranked **next-up** (CRE-ratified, FILL mode) so the next creative slot presents one story, not a menu.

## Steps

> **Mode routing:** FILL runs all steps. DECLARED and OPEN skip the FILL machinery — no bag census, no batch generation, no gut gate on admission (CRE's own idea needs no admission) — entering at **Step 6** (measure) and iterating with **Step 7** (hone + bank); Step 8 runs only if the session also touched the bag.

### Step 1 — Vault sentinel (`^obs-004`)
Verify `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). Fail → halt.

### Step 2 — Bag census
Read `CANDIDATES/` (a `Glob` miss is never evidence of absence — confirm any negative with a direct read, DIR-005). Report: live candidates, their conditions/knots, ages, and any **stale flags** (Step 8). If the bag is at cap (~10–12 live), lead with hygiene (Step 8) before forging more — an overfull bag reintroduces the decision overwhelm this exists to kill.

### Step 3 — Condition intake + variety scan
Two entries:

- **CRE brings the condition** → run the variety scan as a freshness check only ("you've worked isolation twice — still game, or angle it differently?"). His condition wins regardless; the scan informs, never vetoes.
- **CRE arrives open** → run the scan as the offer: conditions/knot-families already worked vs. untouched ("worked: isolation ×2, dread ×3; untouched: envy, self-worth, grief-adjacent shame"). Offer 2–3 untouched or under-worked conditions. **He picks; the scan never picks for him.**

The scan reads the corpus (Inputs) — never the market. Variety comes from CRE's own body of work.

### Step 4 — Forge (the sanctioned what-if layer)
Generate what-if premises around the chosen condition, **batch of ~5–10, one condition per batch**, each in the full PREMISES grammar:

1. **Knot first, always.** Start from the character flaw/condition ("paranoid," "isolated and resigned"). The knot is the premise's spine — never reverse-engineer a knot onto a scenario.
2. **Scenario that directly challenges the knot.** The situation must detonate the flaw, not merely coexist with it.
3. **Tensional constraint.** A clock, a countdown, a closing door — and prefer constraints that do *containment* work (a 20-minute clock is also a container; see Step 6).
4. **Peg from the condition, never from a market.** The peg is the contemporary costume the timeless condition wears — ask *"what does this condition look like right now?"* (isolation → doomscrolling; hypervigilance → baby monitors; parasocial hunger → the feed). Worked example: HAPPENING NEAR YOU — condition: isolation/resignation, *"easier to stay inside"*; peg: algorithms as substitute for touching grass. The condition produced the peg. A premise whose peg has no condition under it is a box-check, not a story.

Present the batch flat — no advocacy, no ranking at this stage.

### Step 5 — Gut gate (CRE rules every candidate)
CRE's felt response is the only gate. Per candidate:

- **SPARK** — the gut kicked in → proceeds to Step 6.
- **REWORK** — something's there but the angle is off → CRE names what; re-forge that one.
- **KILL** — discard freely, zero sunk cost, no defense of the corpse. Expect most of a batch to die; that is the instrument working, not failing.

**Never argue for a killed premise. Never smooth a broken one into shape uninvited** — name what's missing and hand it back (the episode-init gate's own rule). A bag of market-optimal premises CRE is lukewarm on is worse than an empty bag: he won't dictate them, and the bag teaches him to distrust it.

### Step 6 — Scope measurement (the format verdict)
CRE's named weakness runs opposite to most: an under-contained story **blows up into a novel**, and paring down costs him more than expanding. Catch the sizing at conception — the cheapest point. Each SPARK (FILL mode) or brought idea (DECLARED/OPEN) is measured on the containment dimensions:

- **Knots** — one flaw under pressure, or a knot ensemble?
- **Escalation spines** — one line of pressure rising to one detonation, or braided/sequential spines?
- **The constraint's temporal span** — a clock that bounds the story's world (20 minutes, one blackout, one battery bar) vs. one that stretches ("over the following weeks…" is a novel leak; generational span is series gravity).
- **Cast** — protagonist + ≤2 load-bearing others, or an ensemble?
- **World-load** — does the premise demand a world with its own rules, economies, and history (Godsrift-shaped), or does it run on the reader's own world plus one intrusion (WIW-shaped)? High world-load is the strongest series signal.
- **Container bands** — natural telling in ~2,000–2,800 words? (Two-band gate, strategy §3b.)

**Verdict per premise — the format spectrum:** **SHORT-FORM · NOVELLA · NOVEL · SERIES**, recommendation with a one-line basis, measured dimensions named. **CRE rules.** None of these verdicts is a failure. Then by mode:

- **FILL:** SHORT-FORM proceeds to Step 7 (bag). Anything larger → sized and banked to SEEDS (Step 7), parked, session returns to shorts.
- **DECLARED:** verdict matches the declaration → hone toward it. Contradiction → surface it; CRE rules the format (a real fork hands to decision-helper). Then Step 7 banks per the ruled format.
- **OPEN:** the verdict converges through honing; when the premise stops moving, it lands, and Step 7 banks per the landed format.

### Step 7 — Hone + bank (two destinations, by format)
Conversationally sharpen each survivor with CRE — tighten the what-if sentence, sharpen the constraint, confirm the peg. **His phrasing always supersedes proposed phrasing.** Then bank by format verdict:

**SHORT-FORM → the bag:** `WRITING/SHORTS/CANDIDATES/<WORKING TITLE>/triage.md`. The bag stays **shorts-pure, always** — that purity is what makes the weekend slot decision-free.

**NOVELLA / NOVEL / SERIES → the seedbed:** `WRITING/SEEDS/<WORKING TITLE>/triage.md`, same triage convention plus a `format:` frontmatter field and a `## Format measurement` section recording the dimensions that produced the verdict. **A seed is sized, not scheduled:** the seedbed is a parking lot with good labels, never a queue. A seed entering actual development is a **portfolio-residency decision** — decision-helper + CRE, outside this tool entirely (week-shape's guard: story residency is never reordered by an instrument).

Both destinations: working title from CRE (never invent one he hasn't at least shrugged at), frontmatter serialized per DIR-004, following the existing candidate-triage convention:

```
---
type: candidate-triage
working_title: <TITLE>
author: Chad Ryan
source: premise-forge session YYYY-MM-DD
condition: <the feeling/human condition>
format: short-form   # seeds carry novella | novel | series
triaged: YYYY-MM-DD
status: banked premise — awaiting CRE pick + episode-init gate   # seeds: "seed — sized, not scheduled; development is a portfolio decision"
---
# <TITLE> — forged premise
## The what-if        (the honed one-sentence premise, verbatim as CRE ratified it)
## Character knot     (the flaw + the condition under it)
## Tensional constraint (and the containment work it does)
## Peg                (the contemporary costume — and its condition source)
## Container          (band verdict + why it holds short)
## TOS band / tier    (best pre-read: free-tier / age-restricted / never → FULL / SAFE-CUT / TEASE rec — episode-init re-rules at gate)
## Variety note       (what this adds against the worked corpus)
## Format measurement (the Step-6 verdict + the dimensions that produced it; shorts: the containing elements named)
```

The triage pre-answers the episode-init Pass-1 gate so init **confirms rather than re-derives**. Candidates stay **unnumbered** — episode numbering is CRE's scheduling call, always (episode-init's rule).

### Step 8 — Bag hygiene + next-up
- **Cap:** ~10–12 live candidates. At cap, forge nothing new until CRE retires or promotes.
- **Min-fill floor:** below **4** live candidates → surface "fill the bag" as a task to `TASKS/TASKS.md` so it rides week-shape/day-launch onto the board (DIR-012 clause 5's logic: a floor nobody serves is a dead letter).
- **Staleness:** a candidate's **peg is a dated claim** (DIR-010). At ~90 days, or when a peg's moment has visibly passed, flag for **re-gut**: CRE re-rules SPARK (peg refresh if needed) or KILL. Never auto-retire — the checker flags; CRE rules (DIR-014's matcher lesson: the distinguishing fact isn't in the text).
- **Next-up:** close every session by proposing a ranked next-up from the live bag (recency of gut-yes, peg freshness, variety vs. the last published episode). **CRE ratifies or reorders.** The weekend slot then presents one story, zero decisions.

## Stop conditions

- Sentinel fails → halt.
- CRE's gut isn't firing on anything in a batch → **stop forging, don't brute-force volume.** Offer a different condition or end the session; a forced bag is a distrusted bag.
- Any pull toward drafting beats, scenes, or prose → out of scope; that's the mic's job (DIR-017 protects the forward flow) and the route's.

## Guards (summary)

- **Attended, never scheduled.** The gut gate is the mechanism.
- **Generation sanctioned at the what-if layer only, FILL mode only** (PREMISES.md carve-out); DECLARED/OPEN work CRE's own material; never a word of story prose, beats, or scene work in any mode.
- **Knot-first, peg-from-condition, never market-first.** No trend research, no market scans — CRE ruled the market layer out entirely.
- **CRE's felt yes is the only admission to the bag; kills are free.**
- **The mode boundary holds in FILL mode:** larger ideas are sized and banked in minutes, never developed — the session returns to shorts.
- **The bag stays shorts-pure; larger formats bank to `WRITING/SEEDS/` — sized, never scheduled.** A seed entering development is a portfolio-residency decision (decision-helper + CRE), never this tool's move.
- **Episode numbers are CRE's; working titles are CRE's.**
- **DIR-015:** if a session opens a vein about CRE's own state rather than a story condition, the affective lane is named, never worked.

## What this does NOT fix

The bag guarantees **presented work, not flow**. A stall in front of a stocked bag is `work-through` territory (executional lane, DIR-015 governs), not a bag defect — the bag can't help and shouldn't try.

## Logging

Non-trivial sessions (anything that banked, retired, or re-ruled candidates) log per DIR-003. Boot-and-browse with no bag mutation is chat, not history.
