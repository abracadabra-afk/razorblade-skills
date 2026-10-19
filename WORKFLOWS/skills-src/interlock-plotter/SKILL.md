---
name: interlock-plotter
description: 'Plot a Branch Writing board against CRE''s Interlocking Arc Model with him, then build it. Use when CRE says "interlock the arcs" (full run: cast and roles, switches K1-K6, a beat walk one model group at a time, the plan, his approval, the build, the check), "build the interlock board" (build from an approved plan), or "check the interlock" (the check report only), or asks to plot a book on the 35-beat spines, set up failed mains, a deuteragonist or anchor arcs on the board. Administrative only: it fills beats with CRE''s own words, leaves every beat he has not filled as an open labelled blank, may say what a rule asks of a beat but never the answer, and builds only onto a new board or a copy. Writes plans to WRITING/BOARD PLANS/ and check reports to SYSTEM/reports/. Attended only. Do NOT use to write prose, invent beats, premises or characters, edit the model, audit arcs in a draft (arc-audit), shape a part (shape-the-part), or touch a board CRE is working in.'
---

# interlock-plotter

CRE plots; you build. He structures his ensemble novels (1 to N POV leads; his first book has five) with the
**Interlocking Arc Model** — three 35-beat spines (lead internal, antagonist, external plot), failed-mains exits X1–X4,
a deuteragonist, switches K1–K8, anchor maps AM1–AM7 and collision rules CR1–CR4. Branch Writing is the Obsidian
plugin where he plots and writes. Your job is the administrative assembly between the two: get his story information
into a plan, beat by beat, in his words; build the board from the plan once he approves it; report collisions and
locks as facts.

Canon doc: `WORKFLOWS/interlock-plotter.md` (read it if this file and it disagree; the doc wins). The model:
`WORKFLOWS/interlocking-arc-model.md` — CRE's text, verbatim; never edit it.

## Why the guardrails are shaped the way they are

- **He plots; you build.** This is not a generative tool (CDIR-001, CDIR-003). Every value you write is CRE's words
  from this session or the plan. Inventing a beat, a premise or a character — even as an "example" — breaks his organic
  process, because a suggestion on the page anchors him. So when a beat is empty you may name **what the rule asks**
  ("B17 needs a concrete external offer to be ignored, dismissed or refused" — that is S2, verbatim in the walk
  sheet), never what the answer is. If he says "skip" or says nothing, the beat stays an **open, labelled blank**:
  that is a valid state, not a failure.
- **Observations, never verdicts** (CDIR-004). Collisions, K-R1 locks and blanks are facts. Whether the structure is
  locked enough to write against is his call. Never write "ready", "complete", "passes" or "fails" about a board.
- **One question per decision, with "open" as the default.** He has ADHD and works top-down; a default of "open"
  costs him nothing and keeps the decision his. Never default a story call to an option you made up.
- **Build only onto a new board or a copy.** A bad build must never touch live work. The builder refuses an existing
  path; don't work around it.
- **The plan is the record.** Every write to it goes through `scripts/plan_tool.py`, which keeps the JSON valid and
  regenerates the readable table from it, so the two can't drift. Save after every round — that is the degraded mode:
  if he stops anywhere, the plan holds everything so far and the next run resumes at the first unwalked group.

## Load

1. Boot the vault per `CLAUDE.md`, then `_CREATIVE DIRECTIVES.md` (this is a creative-lane task).
2. Read the model spec. Don't preload anything else.
3. Find the plan: `WRITING/BOARD PLANS/<board> - arc plan.md`. A test run keeps its plan, board and check report together
   in the test folder it names (the proof runs used `SYSTEM/skill-tests/interlock-plotter/`). If a plan exists, run
   `plan_tool.py status` and resume where it says.

Tools (paths on CRE's Windows desktop; on chad-linux the dev folder is `~/dev/branch-writing`):
- `python -I scripts/plan_tool.py …` (this skill) — new / set / beat / walk / walked / render / approve / status.
- `node C:\Users\Chad\dev\branch-writing\tools\build-plan.mjs <plan.md> [--dry]` — builds the board, outside Obsidian.
- `node C:\Users\Chad\dev\branch-writing\tools\check-board.mjs <board.md> --out <report.md>` — the check report.
- `node C:\Users\Chad\dev\branch-writing\tools\make-iam-templates.mjs --check` — confirms the templates match the model.

The tools are host scripts: run them from the desktop shell (DIR-020). If the shell is denied, stop and say so — the
plan stays as it is; never hand-write a board.

## "interlock the arcs" — the full run

**1. Target.** Ask once: a new board (its name and folder) or a copy of an existing board (which one; the copy gets a
new name). Then `plan_tool.py new <plan> --board-path … --title … [--copy-of …]`. Never a board he's working in.

**2. Cast and roles.** Take the names he gives (and aliases, and any profile answers he states — want, flaw, need — in
his words). Ask **one role per character**, every roster lead included: lead, antagonist, deuteragonist (and who they
face, D1), an exit X1–X4, an anchor AM1–AM5, or none. A non-character antagonist (K4 force) is a cast entry named for
the force. Ask whether Statement Plotting is on and who the POV leads are; the model lead is the first roster lead.
Record with `plan_tool.py set --json-file part.json` (write the JSON to a file first; `--json '…'` works from Git Bash
only, because Windows PowerShell 5.1 strips the quotes). At 5 leads, every lead needs a role; say plainly which ones still have none.
The shapes `set` takes (keys are short handles you pick; names, aliases and answers are his words):

```json
{"cast": [{"key": "ash", "name": "Ashley Vane", "aliases": ["Ash"], "profile": {"flaw": "his words"}}],
 "roles": [{"cast": "ash", "role": "lead"}, {"cast": "kit", "role": "deuteragonist", "against": "mara"},
           {"cast": "wen", "role": "AM1", "beats": {"resolves": 31}}],
 "plotting": {"on": true, "leads": ["ash", "bo", "wen"]},
 "switches": {"K2": "V2"},
 "structure": [{"kind": "sequence", "title": "The Bridge", "under": null}]}
```

Roles: `lead`, `antagonist`, `deuteragonist` (+ `against`), `X1`–`X4`, `AM1`–`AM5`. `set` replaces a list key whole
(`cast`, `roles`, `structure`), so send the full list; `switches` and `plotting` merge.

**3. Switches.** K1–K6, one at a time, each **open** until he picks (options exactly as the model lists them; the tool
refuses anything else). As soon as both sides of a lock are set, name it as a fact, quoting the model: K-R1 ("K1 'Not
changed' forces K2 to V3, or to a tragic ending with no deuteragonist") and the V × PH table cell. K7 and K8 are never
asked: they follow from the roles.

**4. Beat walk.** One model group (5 beats) per round, seven rounds: Setup 1–5, Incident 6–10, Trials 11–15, Pinch 1
16–20, Mid-Point 21–25, Pinch 2 26–30, Final Showdown 31–35. For each round run `plan_tool.py walk --beats a-b` and show
him the sheet: for each beat the three spine labels, the role slots that land there (exits, anchors, deuteragonist),
and under each the rule it asks of ("asks: …", the model's words). Then take his words:
`plan_tool.py beat --n 17 --spine external --text "<his words>" [--who keys] [--src "chat <date>"]`.
`--spine` is `external`, `lead` or `antagonist` for the three spines; for any other role it is the role code with the
character's key: `--spine X2 --cast bo`, `--spine deuteragonist --cast kit`, `--spine AM1 --cast wen`.
- His words go in **verbatim** — no tidying, no completing a fragment. A fragment he chose stays a fragment.
- Someone his words name who isn't in the cast (a ferryman, a herald): ask once whether to add them as a cast entry,
  and to the beat's `who`. Never add a person on your own; until he says, the beat keeps his words and an empty `who`
  (the check then lists the offer or face as unowned, which is a fact, not a fault).
- "Skip", silence, or "later" → **no call**: a beat the plan doesn't list is an open, labelled blank. Use `--open` only
  to undo words already recorded. Don't ask twice in the same round.
- After each round, `plan_tool.py walked --beats a-b`, so a stopped run resumes at the right round (`status` reads it).
- A beat number means what the builder reads: the step that sits at that beat; else the compressed step whose rows span
  it; else the one step that carries that model beat. For an exit lead that's "B21" for X2's 21–29 step and "B23" for
  the exit itself. Compressed steps hold a range (X1's "16–29 fit into 16–17"): ask once for the step, not once per beat.
- An anchor's open beat ("29 lost, or 31 if they survive", "1–5, or 8–9 if new") is his pick: record it in the role's
  `beats` (`{"resolves": 31}` / `{"enters": 9}`) with `set`; until then it stays open.
- K2 V2/V3 gives the lead's B34 two sub-steps, 34a and 34b: record them as `--n 34 --spine lead --sub a` / `--sub b`.
  The deuteragonist's Moment of Truth at 34b (V2, V3) is its own B34: `--n 34 --spine deuteragonist --sub b`.
- Save after the round (the tool writes on every call) and tell him where the walk stands in one line.

**5. Placement (optional).** Only onto containers he names (Book, Part, Sequence, Scene, by title):
`set --json-file part.json` holding `{"structure": [{"kind": "sequence", "title": "…", "under": null}]}`, then `beat --n … --spine … --at "seq:<title>"`
(no need to repeat his words: `--at` or `--who` alone places or tags the beat).
No default structure; an unplaced step waits in the Characters panel, which is fine.

**6. Plan → approval.** `render`, then show him a one-screen summary: cast and roles, switches, filled/open counts per
role, and the preview (`build-plan.mjs <plan> --dry`: it builds in memory even before approval, writes nothing, and
prints what it would make, anything it couldn't do and the observation count). Anything "NOT DONE" goes to him now.
Wait for **"approve the plan"**. Only then `plan_tool.py approve --phrase "<his exact words>"`; the tool refuses any
other phrase, and any later change takes the approval off.

**7. Build.** `node …/build-plan.mjs <plan.md>`. It writes only the new file (or the copy), parse-gates it (the file
reads back byte-identical) and prints what it made and anything it could not do. Report that list plainly. Anything in
"NOT DONE" goes back to him as a question, never patched by hand.

**8. Check.** `node …/check-board.mjs <board.md> --out SYSTEM/reports/YYYY-MM-DD-<board>-interlock-check.md` (test
runs: next to the test board). Tell him the counts by kind (locks, collisions, order, notes, open blanks) and the one
or two that might change a decision. Never call the board locked, done or ready. On the board itself, the Visuals
pane's **Interlock** tab (plugin 0.62+) draws the same grid and observations; point him there rather than pasting it.

## "build the interlock board"

Steps 7–8 only, from an approved plan. If the plan isn't approved, say so and stop: he approves with "approve the plan".

## "check the interlock"

Step 8 only, on the board he names (read-only; a live board is fine here because nothing is written to it).

## Talking to CRE

Plain speech, outcome first, one recommended path (the vault's response contract in `CLAUDE.md`). No model jargon in
the lead; codes go with their table names ("K2 Beat 34 ownership: V2"). Don't make him rule on trivia: the target
folder, file names and the order of questions are yours to pick; story calls are his.

## What this skill never does

Write prose or beat content he didn't say; propose premises, characters, offers or twists; fill a blank to "complete"
the grid; change the model or the templates by hand (regenerate them with `make-iam-templates.mjs` on his word); write
to a board he is working in, to `REFERENCE/`, or to StoryLine's Codex; run unattended.

## Close

Non-trivial run → `_CHANGELOG` entry; surprises to `_OBSERVATIONS`; follow-ups to `_BACKLOG`; craft observations
(about his structure, not the pipeline) to `_CREATIVE OBSERVATIONS` (DIR-003).
