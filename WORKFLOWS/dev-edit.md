---
type: workflow
name: dev-edit
trigger: run the dev edit
aliases: [dev edit, convene the dev panel, dev-edit walk, walk the piece]
inputs: [the landed post-transcode draft (draft.md, register rev acceptable), CRE's harvested flags (captured before any seat reads), the corpus surfaces for the informed layer (register, voice samples, premise/brief, prior rulings)]
outputs: [3 blind dev-seat reports + an isolated synthesis in a dev-edit/ run folder, the flag-keyed walk sheet (REINFORCES/CONTRADICTS/NEW), the author-pass roadmap with the affirmed-sections map, EXECUTION-class deferrals staged on the line passes' input surface]
lane: fiction (+ writing-ops for WIW episodes)
status: spec — packs after 2–3 live runs
governed-by: DIR-011 (resolve before flag), DIR-012 (gates attended), DIR-014 (rulings land on tool-read surfaces), DIR-015 (executional lane only), DIR-017 (never gates the mic)
pipeline_position: episode route v3 S6a — first instrument after the drafting engine (post-transcode/register rev), BEFORE CRE's author pass. panel-read moves downstream to the pre-publication gate. Naming note — NOT part of the DEV/-tree family (dev-capture/dev-readiness/dev-reconcile, which live upstream of the brief); this is a developmental edit of drafted prose.
created: 2026-08-09
last_updated: 2026-08-09
---

# WORKFLOW: dev-edit

The **developmental edit for first-draft material** — a two-layer instrument that runs where EP 01 proved the reader panel should not: after the transcoder, before CRE's author pass. Layer one is a **blind dev panel** (three isolated developmental seats with different attention assignments, findings only, never fixes). Layer two is the **informed dev-editor walk** (spec-aware, corpus-versed) that triages the synthesis against the tree, keys every finding to CRE's own harvested flags, and walks the piece with him to a ruled roadmap for his author pass.

**What this instrument is for (founding reframe, CRE-ruled 2026-08-09):** it is a **deliberation terminator, not a defect detector.** CRE trusts his gut on the story more than any output; where he loses hours-to-days is debating whether the gut call is right or an ADHD artifact. The product is *weight* — evidence-based convergence that reinforces or pushes against his instinct so he can rule once and move. Success metric: he ruled in one sitting. Not: findings were found.

## Provenance — the EP 01 post-mortem (2026-08-09, CRE-ruled)

The full reader panel + response machinery ran on EP 01 **before** the author pass. Costs, verified against the tree:

- CRE's own `author-flags-2026-07-27` carried D2b ("video 2 is where the rule clicks") **two days before** the panel's C1 flagged the same scene — the panel confirmed an instinct already on paper.
- The `video-2-escalation` choreographer session (six ratified beats, two desk-ruled slots, gap dictation) died whole when CRE's author pass replaced the sorority sequence with Bum Beatdown (draft 6, 08-05). The map is flagged stale in draft.md's own frontmatter.
- Three protected spans retired 08-05; sorority-sequence line rulings discarded; three panel convenings where the route needed one.

**The category ruling that governs this workflow:** the 07-29 C1 was a **CONTENT** verdict ("a repeated beat, not an escalation… only geography advanced" — the beat does no new story work); the 08-05 C1 on the rewritten scene was an **EXECUTION** verdict ("summary-telling… right where the scene most needed us to feel two humans agreeing" — right content, told not shown), cured by a same-day tighten. The EP 01 waste was executing against a CONTENT flag with EXECUTION machinery. **Execution rulings never run on a section carrying an open content flag.**

## Finding taxonomy (every finding gets both tags)

1. **CONTENT** — the beat does no new work; engine/premise-level; "I skimmed to get to the violence." Only CRE's author pass can cure it. These findings ARE the roadmap.
2. **EXECUTION** — summary vs. dramatized, runs long, over-itemizes, ear-level. Cheap and stable to fix, but only once the content underneath is author-affirmed. **Deferred downstream** to a surface the line passes and the pre-publication panel read (DIR-014) — never worked here.

## Steps

### Step 0 — Sentinel + flag harvest (the non-negotiable first move)

Verify `_DIRECTIVES.md` frontmatter (`^obs-004`). Then **capture CRE's read first, verbatim** — his flags, hunches, "something's off in the second scene" — before any seat reports exist (the author-flags pattern). If an `author-flags` file already exists for the piece, it serves. The blind seats never see these; independence is what makes the convergence evidential.

### Step 1 — Blind dev panel (3 isolated seats, simultaneous)

Clean-room contract inherited whole from [[WORKFLOWS/panel-read]]: each seat is a fresh isolated subagent holding ONLY its seat prompt + the prose. No spec, no register, no premise, no CRE flags. Common report rules also inherited (quote per finding, denominator, strengths mandatory — this is a walk of *strength and weakness*, not a defect hunt). **Findings only, never fixes** — a seat names the weakness; it never authors the solution (organic-process guard).

> ⚠️ **Strip the frontmatter, and hand each seat TEXT rather than a path (`^obs-269` — inherited with the contract, but restated here because this pass fails worse than a panel does).** This pass reads `draft.md` by name, and this doc records elsewhere that `draft.md`'s own frontmatter carries live rulings. That header typically holds an `open_flags` list naming **CRE's live unruled craft worries by name** — which is to say, a substantial overlap with the very Step-0 flags the seats are forbidden to see. A panel that reads the header returns a contaminated read. **This pass returns something worse: manufactured convergence.** Its whole product is the keying at Step 2 — REINFORCES means *"your gut, independently confirmed by N seats."* A seat that read the flags off the header confirms nothing, the desk cannot tell the difference, and the walk sheet banks the false agreement as a ruling that no later pass re-raises. So: the orchestrator extracts the body (everything below the closing `---`) once, before any seat launches, and passes that text. **A seat handed a path, or disclosing that it saw frontmatter, is void — re-run it.**

The three seats differ by **developmental axis** — differentiation is what keeps 3-from-one-model convergence from being an echo:

- **STRUCTURE** `dev-structure.md` — does each beat/scene do new story work; escalation and progression logic; repetition vs. advancement; where the spine sags or steps down. The C1-content class is this seat's home turf.
- **ENGINE / CHARACTER** `dev-engine.md` — does the protagonist's want/flaw drive every scene; is the premise's promise being spent or hoarded; whose decision moves each beat; where the character is carried by the plot instead of driving it.
- **AUDIENCE / PROMISE** `dev-promise.md` — what the opening teaches a reader to expect; setup vs. payoff ledger; genre contract; what was planted and what pays; where the piece over- or under-delivers on its own promises.

### Step 2 — Synthesis (one isolated subagent), then the desk keying

The synthesizer receives the three reports + the prose (nothing else) and bins by convergence, panel-read style: CONSENSUS (all 3) / CORROBORATED (2, with independent reasons) / SINGLETON (weighted by home turf) / STRENGTHS. It never averages disagreement and never prescribes.

The **desk** (orchestrator, spec-aware) then produces the walk sheet by keying every synthesis finding to CRE's Step-0 flags:

- **REINFORCES** — convergence lands where his gut already was. No debate owed: presented as "your flag, confirmed by N seats — rule and move."
- **CONTRADICTS** — the evidence pushes against a flag or an intended move. Presented **once**, with the seats' reasons, then CRE rules. His ruling is terminal.
- **NEW** — nothing he'd flagged. The genuine blind-spot catch, and the only bin that earns fresh deliberation.

Every item also carries its CONTENT/EXECUTION tag. EXECUTION items route straight to the deferral list — they appear on the walk sheet for visibility, never for ruling here.

### Step 3 — The informed walk (attended; this is the instrument)

The dev-editor layer is **corpus-versed by requirement**: before the walk it loads the piece's spec surface (premise/brief + rulings blocks), the project register, and enough of CRE's corpus ([[KNOWLEDGE/STYLE]], [[KNOWLEDGE/VOICE SAMPLES]], prior finished pieces as needed) to know his tendencies and deliberate moves. **DIR-011 first:** any finding the tree already answers — a ruled register choice, a ratified premise amendment, a protected pattern — presents as *"resolved against [[X]] — confirm,"* never as an open flag. A blind seat flagging CRE's deliberate restraint is noise the walk absorbs, not a question he answers twice.

Then walk the piece top to bottom with CRE, tree-silent items only, in text order. Per item he rules: **agree / disagree**, and on agree: **compress / expand / rework / affirmed-as-is**. The dev-editor frames, supplies the evidence, and may advise; **CRE rules, and his instinct overrides the evidence without argument** — an overruled CONTRADICTS is recorded with his one-line why and never re-raised by any seat, pass, or later session (the anti-rumination payload: the record does the re-arguing so his head doesn't).

**The choreographer offer (CRE-ruled 2026-08-09).** When a walk item is choreography-class — the weakness lives in *event mechanics* (staging, reveal order, blocking, action/dialogue dramaturgy), not in whether the beat belongs — and the event's content is ruled (affirmed, or a rework where CRE has settled *what happens* and staging is the open question), the dev-editor **offers** [[WORKFLOWS/choreographer]]: *"this is a staging question — want a beat map before your pass?"* **CRE triggers it or it doesn't run** — never automatic, never a standing leg. A resulting ratified map exits as an **optional flow-kickstarter** for his author pass under DIR-017 clause 2 (density scales to re-load burden; divergence is a win; nothing grades the pass against the map). The gate's teeth: EP 01's climax-inversion map (content-affirmed) survived; its video-2-escalation map (content-contested) died whole. A pre-author-pass map is a bet the pass won't move the content under it — CRE places that bet, not the instrument.

### Step 4 — Roadmap out

Deliverables, all safe-op writes to the run folder (frontmatter serialized per DIR-004):

1. **`walk-sheet.md`** — every finding, its bins (REINFORCES/CONTRADICTS/NEW × CONTENT/EXECUTION), CRE's ruling, dated. The episode's ruling surface for this tier; downstream passes and future doubt spirals meet "ruled 2026-MM-DD, here's the evidence ruled on."
2. **`roadmap.md`** — the author-pass plan in his ruled terms: sections binned rework / compress / expand / **affirmed**, in suggested write order. The **affirmed-sections map is the write-gate for downstream machinery**: choreographer, line queues, and panel-response run only on affirmed sections; a section binned rework gets nothing until CRE's pass lands.
3. **EXECUTION deferrals** staged on the surface the line passes read (DIR-014) — a deferral living only in the walk sheet will be re-litigated.

Exit: the mic/desk is CRE's. This workflow never schedules, grades, or follows up on the author pass (DIR-017 — the pass is his flow, not a spec compliance run).

## Route v3 placement

```
transcoder → register rev → DEV-EDIT (this workflow) → CRE's author pass →
panel-read (the pre-publication gate) → panel-response → line passes → record prep
```

Replaces the route-v2 S6 shape (blind read → dev fixes → register → CRE's passes) for episodes. `blind-read` remains available as a cheap single cold probe at CRE's call; the reader panel is **never** convened on pre-author-pass material — that is this instrument's slot. First pilot: next episode (EP 02).

## Guards

- **Never authors CRE's prose, options, beats, or solutions.** Seats name weaknesses; the walk frames rulings; the roadmap records them. Nothing here writes fiction.
- **Gut-authority clause.** The evidence is weight, not verdict. CRE overruling convergence is a valid, expected outcome, logged without argument and closed permanently.
- **Honest limits, stated in every synthesis:** three seats from one model share blind spots three humans would not. Differentiated attention assignments mitigate; they do not eliminate. This instrument protects against *one prompt's* taste profile, not the model's. The pre-publication reader panel remains the stronger convergence instrument — which is why it guards the gate.
- **Attended only.** The walk is the point. Unattended, a run may at most fan out Steps 1–2 and stage the un-keyed synthesis to `SYSTEM/reports/` (DIR-012); flag harvest and walk wait for CRE.
- **Affective boundary (DIR-015).** If the session drifts from "is this scene right" to "why can't I finish anything," that is `work-through`'s lane, named once, never worked here.

## Stop conditions

- No landed post-transcode draft → nothing to edit; this is not a runway or dev-capture instrument.
- CRE's flags not yet harvested → stop; Step 0 is not skippable (a synthesis keyed to nothing is a verdict sheet, which is the instrument this replaces).
- Any seat prompt found to contain spec material or CRE's flags → that seat's read is void; rebuild and re-run.
- Any seat handed a **file path** rather than extracted prose text, or disclosing that it saw the draft's frontmatter → that seat's read is void (`^obs-269`); extract the body and re-run. **If a voided seat's findings already reached a walk sheet, re-key that sheet** — a REINFORCES banked off a contaminated seat is the failure this pass cannot self-detect.
- A section carrying an open CONTENT flag being routed to choreographer/line machinery → stop; that is the EP 01 category error this workflow exists to prevent.

## Not this

- **`panel-read`** — reader personas, pre-publication gate. Readers read finished work; dev editors read first drafts.
- **`blind-response` / `panel-response`** — revision passes; this pass revises nothing.
- **`workshop-chapter`** — the novel-side sibling (intent-first, informed, read-only); dev-edit adds the blind convergence layer and the flag-keyed ruling mechanics for the episode route.
- **`dev-capture` / `dev-readiness` / `dev-reconcile`** — the upstream DEV/-tree family, below the brief. Different tier entirely; the shared word is an accident of vocabulary.
- **`choreographer`** — not a leg of this workflow; callable from the walk by CRE only, on content-ruled events (see the choreographer offer, Step 3). Its default home stays post-author-pass, nested in panel-response.
- **`line-edit` / `register-pass`** — EXECUTION machinery, downstream of the author pass.

## Logging

Per DIR-003: a run that writes the walk sheet/roadmap logs one `_CHANGELOG` entry (unit, finding counts by bin, rulings by class, roadmap section count). Fragilities (a seat performing its axis, convergence-as-echo suspicion, a walk that ran long) file to `_OBSERVATIONS`.

---

_Canonical doc, authored 2026-08-09 from the EP 01 workflow post-mortem (CRE-ruled same session). Fills the standing finding from episode-feedback run 3 (2026-07-21): "shorts have no DEV layer." Procedure changes land here first; packs after 2–3 live runs (house pattern)._
