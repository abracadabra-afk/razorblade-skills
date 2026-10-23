# Audit mode — "audit the board": read the whole book, report what strains

CRE plots ensemble books on these boards and needs the problems that only show when you read across the whole book: a
payoff with nothing planted, a wound that heals too fast, a thread that goes quiet for twenty sequences, the same beat
twice. A thread trace finds them one thread at a time; the audit finds them across every thread at once, so he fixes them
in the redraft instead of discovering them in the draft. (Intent: `WORKFLOWS/intents/branch-writing-board-audit.md`.)

**Read-only, and a report.** The audit never writes the board, the plan, DEV, REFERENCE or the chapters; the only
things it writes are its scratch work folder and one report in `SYSTEM/reports/`. Every fix is his to rule, so it runs
attended, never on a schedule. A version check of `newer` or `breaking` does not stop it (reads are allowed); say so in
one line and carry on.

## Why the findings are shaped this way

- **A story problem is a question for him, never a fix.** A story suggestion anchors him (CDIR-003, CDIR-004): say what
  strains and where, show the evidence, ask the question his redraft has to answer, and stop. "Should the SEQ 34 rockslide
  cost her something the reader sees later?" is the shape. "Have her limp in SEQ 36" is not.
- **A non-story problem gets its mechanical fix.** A stale summary, a step on the wrong line, a plan cell citing a gone
  card, a marker the board has answered: name the fix, because an administrative fix saves him a step (he asked that every
  critique come with one). The fix is the audit's to *name*; carrying it out is a later "work the board" run on his word.
- **His words, exactly, with card ids.** Quote the card, never paraphrase into his mouth (`^obs-463`). Know whose words a
  quote is: micro-beats, his idea cards and the plan's step cells are **his**; beat titles, beat and scene summaries and
  chain lines were written by this skill's breakdown and are **board summaries**. A finding that rests only on a board
  summary is confirmed against his words (the micro-beats, DEV, the landed chapters) before it is reported, or reported
  as "rests on a summary" — never quoted as if he wrote it.
- **His markers are his placeholders.** `held —`, `body —`, `bond —`, `adage —` and `hermit —` mark gaps he already
  knows about; never re-report one. `audit —` markers (the "Audit Rulings" carrier) hold an earlier audit's rulings,
  his words, for the redraft: never re-report the problem one settles; report it only when the board now does what it
  asks (housekeeping: retire the marker). A keep-dark marker (`held — hold the mystery: …`) is a design choice, never a finding.
  What the audit does report is a marker the board has **since answered**: a held gap the board now fills is a housekeeping
  item (retire the marker), and a keep-dark question the board now answers is a **leaked mystery** — a question for him.
- **Every strand before "missing".** A relationship or a payoff can live in another lead's strand (the bond trace said "no
  mother-and-son version" when the hound's strand carried it, `^obs-465`). Before calling anything absent, search every
  POV lead's scenes, the prose files and the arcs. Design for N leads; never assume one or two.
- **Resolve before you flag** (DIR-011). A finding his record already answers is either dropped (he ruled it) or shown
  once as *"resolved against [ruling] — confirm"*, never as an open question. A settled call stays settled.
- **The structure is not yours.** Beat order across the spines, collisions and open model blanks belong to the Interlock
  check (`check-board.mjs`); cite its report, never redo it.

## The run

1. **Version check and board.** `board_tool.mjs check --board <board>` (Load). The plan is
   `WRITING/BOARD PLANS/<board name> - arc plan.md` when it exists. Hash the board (`sha256sum`) before and after: the
   two must match, and the report says so.
2. **Crawl.** `node <skill>/scripts/audit_crawl.mjs <board> --out <scratchpad>/audit-<board> --plan <plan>` — under a
   second on a 6,600-card board. Read its `README.md` first: counts, the files, and what the crawl did not check. The files
   are facts, never findings: a silence can be design, a repeat a refrain, an inversion a flashback.
   | File | Use it for |
   |---|---|
   | `outline-P<n>.md` | the spine in story order: sequences, scenes, beats, summaries, goal holders, outcomes, with every arc step (◆) and marker (⚑) where it sits — read every part, it is what the checks walk |
   | `prose-P<n>.md` | his words, one micro-beat a line with `sc NNN · ^id` — grep it to confirm a fact or find a quote |
   | `arcs.md` | each arc's steps in step order, where they sit, unplaced steps, order inversions, silences |
   | `markers.md` | every marker by class (keep-dark, sources-disagree, held, body, bond, adage, hermit) |
   | `alignment.md` | the plan against the board |
   | `names.md` | each cast member and world entry: mentions, first and last scene, longest silences |
   | `repeats.md` | repeated phrases in his words, near-twin beat summaries, shared beat titles |
   | `bible.md` | the side panels the world walk filled, all ruled by him: the timeline (each scene's era, flashback mark, setting), place changes between consecutive present scenes, where the present's era turns, the seed check (open = a candidate dangling plant), pinned events (⚠ where an event's era and its card's era disagree), cast profiles, world entries; plus the tagging pass's offered state changes and wants per character (`‹ai offer›`, not his). The outlines show each scene's era, setting and links; the prose file shows each card's offers after his words |
3. **The structure report.** Find the newest `SYSTEM/reports/*-<board>-interlock-check*.md`. If the board's change log
   (`board_tool.mjs log`) shows a run after it, write a fresh one: `node <dev>/tools/check-board.mjs <board> --out
   SYSTEM/reports/<date>-<board>-interlock-check.md` (it refuses an existing file; add `-2`). Cite it; don't restate it.
4. **His record, before any check.** Build the ruled list the checks resolve against: the board's earlier reports in
   `SYSTEM/reports/` (thread traces, ledgers, sweeps: their "Ruled", "Your calls" and "Resolved against" sections), the
   project's `DECISIONS/` entries, `DEV/_DEV_MAP.md` ruled terms and `REFERENCE/_LEXICON.md` (read-only), and the plan's own
   `ruled` notes. One line per ruling with where it lives.
5. **The five checks.** Whole board, every part. On a big board, run them as five parallel subagents (one per check),
   each handed the work folder, the ruled list, this file's section for its check and "Why the findings are shaped this
   way"; each returns candidates in the shape below. On a small board, do them in sequence yourself.
6. **Verify every candidate** before it goes in the report — a subagent's candidate is a lead, not a finding:
   - the quote is on the cited card word for word (grep the prose and outline files), and labelled his or a summary;
   - it is not a marker, a keep-dark item, or something on the ruled list (then drop it or "resolved against — confirm");
   - a "missing" claim was searched across every lead's strand, the prose, the arcs, and — where the board has no prose
     for that part — DEV, REFERENCE and the landed chapters (read only to confirm or rule out, never as the subject);
   - two candidates about one problem merge into one finding with both card sets.
7. **Rank and write** the report (shape below). Hash the board again.
8. **Chat** (Talking to CRE): the three findings that matter most in plain speech, the report link, one recommended
   path (usually: read the top three and answer their questions). Nothing written to the board.

**Candidate shape** (subagents return this, one per candidate): check · cards (`^id` list, with `sc NNN`) · evidence
(exact quotes, each marked *his* or *summary*, with its card) · what strains, in one plain sentence · story or
housekeeping · for story: the question for him · for housekeeping: the mechanical fix.

## The checks

**Continuity** — facts that disagree between scenes: an object (who holds it, where it is, whether it still exists), a
wound or a body's state, a count (beads, days, hounds), time of day and elapsed time, distance and direction, weather and
light, who knows what and when. Walk the outlines in order keeping a running ledger for the facts the book tracks (the
items and world entries in `names.md` are the start, not the limit); grep the prose to confirm each change. A change the
story causes is not a finding; a change nothing causes is. Facts a held "sources disagree" marker already names are
known — skip them. From `bible.md`: walk the place changes (is each move on the page, or meant to be off it?), the
era turns, and the events whose era disagrees with their card. Read each character's offered states in order for a state
that reverses with nothing between. The offers are leads from a reader, not his words: confirm every one in the prose before it
becomes a finding.

**Beat mapping** — the arcs on the board doing their job: each arc step sits where its words happen (the step's text
matches what the card it sits on does), sub-steps follow their parent's scenes, nothing is unplaced that the board could
now place, and **plants have payoffs and payoffs have plants** — an object, a promise, a skill, a rule, a line that comes
back. `arcs.md` gives the order inversions and unplaced steps; an inversion is a finding only when it isn't a flashback or
an interlude in another era (the Woodsgirl interludes run in their own time). For plants and payoffs, read the outlines
for setups that never return and returns with nothing set up, then confirm in the prose. The seed check in `bible.md`
is where to start: each open thread is a plant with no payoff tagged. Search the prose after its seed before calling it
dangling: the payoff may be on the page but not tagged yet, which is a housekeeping fix (tag it), not a story finding.

**Alignment** — the plan, the spines and the subplots agreeing with the board. `alignment.md` lists the mechanical
drift: plan words no step carries, steps in another scene than the card their cell cites, cells citing a gone card,
subplots on one side only, board step words not in the plan. Then the reading part: each subplot's goal, stakes and
planned outcome (in `arcs.md`) against what its steps on the board actually do — does the last step deliver the planned
outcome; does the goal holder ever act on the goal. Plan-vs-board drift is housekeeping (which side moves is his call:
the plan to the board by default, DIR-017); a subplot whose steps don't deliver its outcome is a story question.

**Meaning issues around plotting** — a turn that doesn't land because its setup is missing; a rule of the world broken
without cost (the magic, the venom, the moon, Death's patience); a thread gone silent where it should be alive (an arc
silence or a name silence across stretches where the story needs that thread working); a choice with no consequence; a
character who knows something they couldn't. Use `arcs.md` silences and `names.md` silences as the map, then read those
stretches of the outline to judge whether the silence costs the reader. Many silences are right (a character offstage on
purpose); report only the ones that strain. Test what characters do against their profiles in `bible.md` (want, need,
flaw, wound). An action against the profile with no turn to earn it is a candidate, and so is a want the offered wants drop
without a payoff. A profile is his ruling; an offer is not.

**Repetition** — the same beat, image, line or move used again without meaning to. `repeats.md` gives the phrase
repeats in his words and near-twin summaries; read each in place. A refrain, the adage, a callback, a ritual (the
morning care, the knots) or a deliberate mirror (the B1/B35 bookends) is design — skip it, or name it as kept-well when it
works. A repeated *move* (the same rescue twice, the same argument beat for beat, two scenes doing one job) won't show in
the phrase list: watch for it while reading the outlines for the other checks.

## Ranking: how much it would strain a reader

Rank the story findings by what a reader would feel, highest first; this is your estimate, and his to reorder.

1. **Breaks belief** — a contradiction or a rule broken without cost that a reader would catch.
2. **A turn that doesn't land** — a payoff with no plant, a climax resting on a setup the board doesn't have.
3. **A thread gone quiet** where the story needs it alive, so its return feels unearned.
4. **A dangling plant** — set up and never paid (unless a marker or ruling holds it).
5. **Repetition** that dulls a moment.

Within a tier, weight by reach: the main spine and the leads over a subplot, a long span over a short one, a scene the
book turns on over a passing one. Housekeeping is not ranked against story: it is its own list.

## The report

`SYSTEM/reports/YYYY-MM-DD-<board slug>-audit.md` (`-2` if one exists). Match the body ledger and the bond trace: plain
speech, his words quoted with source, tables only where they help.

```
---
type: report
topic: Board audit — <board>
date: YYYY-MM-DD
mode: read-only audit (branch-writing-expert, "audit the board")
board: "<board path>"
plan: "<plan path> (approved <date>)"
structure: "<the interlock-check report cited>"
sources: board · plan · <what was read to confirm: DEV / REFERENCE / landed chapters / earlier reports>
board_sha256: "<before> = <after>"
---
# Board audit — <board>

Read-only. The board was not changed. Quotes are his words or a board summary, marked, with card ids.

**Bottom line.** <two to four sentences: where the book strains most, in plain speech>

## The three that matter most
<the top three findings, written out: what strains, the evidence, the question for him>

## Where it strains — ranked
<every story finding, numbered, grouped by part where that reads better: **N. headline.** (check · cards) what strains,
evidence in quotes with ^ids, then *Your call:* the question>

## Board housekeeping
<numbered: what is off, the cards, the mechanical fix — "say 'work the board: …' to apply">

## Markers the board has since answered
<marker ^id, its text, the card that now answers it; keep-dark ones are leaked mysteries and also appear above>

## Resolved against your rulings — confirm
<one line each: the would-be finding, the ruling that settles it, where the ruling lives>

## Kept well
<a few things the board does right across the book: a plant paid, a thread that never drops — evidence, not praise>

## What this run did not check
<the crawl README's list, plus this run's own gaps: parts read from summaries only, checks skipped, candidates dropped
unverified>
```

## Talking to CRE, for this mode

Lead with the three findings that matter most, each in a sentence, then the report link and one path. No ids in the
lead. Don't ask him to rule on housekeeping one item at a time: offer it as one "work the board" run he can approve
whole. His answers to the story questions are rulings: when he gives them, they land where he says (a marker, a
change on the board, a DEV note — a separate run), and a later audit reads them as part of his record.

**When it runs.** On request. And after each part lands on the live board (an import or a build into a live board),
offer it once, in one line: "Part N is on the board — want me to audit the board?" Never run it unasked.
