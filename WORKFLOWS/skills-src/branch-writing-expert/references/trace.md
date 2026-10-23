# Trace mode — "trace X": follow one thread through every source, report what he can rule from

CRE writes ensemble books across several projects, and a thread's material — a character, an object, a relationship, a
force, a piece of lore — is scattered across his board, his development notes, his landed chapters, older drafts and
archives, often in versions that disagree. A trace follows **one** thread through all of it, in story order, and hands him
one report: how the thread runs, where its sources disagree, what is still his to rule, and a subplot step table so the
thread can go onto the board. (Intent: `WORKFLOWS/intents/branch-writing-trace-thread.md`; the audit mode is the sibling
that reads every thread at once.)

**Read-only, and a report.** A trace never writes the board, the plan, DEV, REFERENCE or the chapters; it writes its
scratch notes and one report in `SYSTEM/reports/`. The step table goes onto the board only on his "send it", as a separate
run through the normal write path (below). It runs attended — the calls need his judgment. A version check of `newer` or
`breaking` does not stop it (reads are allowed); say so in one line and carry on.

## Why the trace is shaped this way

- **Sources differ by project, so read the map, never a layout from memory.** Each project keeps a source map at
  `WRITING/PROJECTS/<PROJECT>/trace-sources.md`: its source families, its POV strands, whose words each family holds, and
  its source rank. If a project has none, build one from its folder tree (same shape as Witchwood's), show it to him in a
  few lines and have him confirm it once before the first trace; then save it. Trace every family on the map — the pilot
  that skipped a family missed the line that settled the call.
- **His words, exactly, with file and line.** A paraphrase put in his mouth is the failure `^obs-463` measured. Know whose
  words a quote is — the map says per family: his prose, his dictation floors, his rulings and his idea cards are **his**;
  DEV's capture of a floor, a board summary, a REFERENCE line are **a file's** words. Quote either, but label it, and confirm
  a load-bearing DEV line against the floor it came from.
- **Every strand before "missing".** A relationship or a beat can live in another lead's strand: the bond trace called "no
  mother-and-son version" when the hound's strand carried it (`^obs-465`). Before the report says a thread is absent
  anywhere, search every POV strand on the map — design for N leads, never one or two.
- **Resolve before you ask** (DIR-011, DIR-019; working rule 3). Check every would-be call against his rulings and the
  newer drafts first. One the tree settles is shown once as *"resolved against X — confirm"*; one he already ruled is not
  re-asked. The newer draft wins.
- **Story questions in plain words.** Never a model code ("K2", "B17 external") — ask what the story has to answer
  (memory: "IAM switches in plain words"). Never offer story options of your own (CDIR-003): where only he can answer, ask
  plainly and offer "decide at the redraft".
- **His words are the forbidden zone** (CDIR-001). In the step table, every step carries his exact words as its proof; the
  step line around them is a plain line of what happens there, drawn from his words (SKILL.md, "A quote is not a summary").
  Anything the thread needs that he has not written — a gap, a held question, a span the redraft must fill — goes on as a
  **labelled redraft marker** (`<thread> —`, like `body —`, `bond —`, `held —`), never as a step.
- **His markers are his placeholders.** A `held —`, `body —`, `bond —`, `adage —`, `hermit —` or `audit —` marker already
  on the board marks something he knows; cite it, don't re-raise it. A keep-dark marker (`held — hold the mystery: …`) is
  a design choice, never a gap.

## The run

1. **Version check and the board.** `board_tool.mjs check --board <board>` (Load). Hash the board, the plan and the source
   map (`sha256sum`) before and after: they must match, and the report says so.
2. **The map.** Read `WRITING/PROJECTS/<PROJECT>/trace-sources.md` (missing → build, confirm, save, as above). Note its POV
   strands and its source rank.
3. **His record first.** Pull the ruled list the readers resolve against: earlier reports on this thread or its neighbours
   in `SYSTEM/reports/` (their "Ruled", "Your calls" and "Resolved against" sections), the project's `DECISIONS/`, the
   author flags, the plan's `ruled` notes. One line per ruling with where it lives. A thread traced before gets a fresh
   report (`-2`) that starts from the old one's rulings.
4. **Search terms.** The thread's names and its variants across the project: aliases, the lexicon's ruled term, older
   names in the archive, the object's or place's other spellings (grep the map's families for each; a thread under an old
   name is still the thread).
5. **Readers, in parallel.** One read-only subagent per family on the map, about 6 at most — merge small families as the
   map's reader split says. Hand each: its family's paths, the search terms, the POV strands, the ruled list, and this
   file's "Why the trace is shaped this way". Each returns **entries**, in story order where it can tell:
   `where (CH / SEQ / card id / part) · event, one plain line · exact quote · file:line · whose words (his / a file's) ·
   date of the file when it is an archive or Drive source`. Readers report what they find; they never judge a call.
6. **Verify.** A reader's entry is a lead, not a fact. Before anything goes in the report: every quote is on its cited
   line word for word (grep it — watch curly quotes, `^obs-468`); a "missing" claim was searched in every strand; two
   entries for one moment merge, with the newer source first.
7. **Assemble** in story order (the report shape below): the throughline, the table, the core every source agrees on, the
   disagreements ranked, the gaps against the grid, his calls (resolved ones as "confirm"), stale notes, the step table,
   what wasn't checked.
8. **Hash again** and write the report. A live board can move under a trace (another session's run, his own edit): if
   a hash changed, `board_tool.mjs log` names the run; say so in the report's `hashes` line, re-check every cited card
   and quote against the board as it now is, and carry on — the trace itself wrote nothing.
9. **Chat** (Talking to CRE, below). Offer the step table for the board in one line. Nothing written to the board.

## The report

`SYSTEM/reports/YYYY-MM-DD-<project>-trace-<thread slug>.md` (`-2` if one exists). Match the bond trace, the failing-body
trace and the Death trace in `SYSTEM/reports/`: plain speech, his words quoted with source, tables where they help. A
thread may add a section where it earns one (the bond's pacts and topic table; Death's rulings layer and its
past/present bridge) — never a filler section.

```
---
type: report
topic: Thread trace — <thread> (<Project>)
date: YYYY-MM-DD
mode: trace a thread (branch-writing-expert, read-only; ends in a subplot step table)
thread: "<the thread as he named it>"
source_map: "WRITING/PROJECTS/<PROJECT>/trace-sources.md"
sources: <one line per family read, with what was read in it>
hashes: "board <before> = <after> · plan <before> = <after>"
---
# Thread trace — <thread>

Read-only. Quotes are CRE's words or a file's, marked, with source. Nothing here says what the thread should be.

## The throughline
<a few sentences on how the thread runs, start to end, in plain speech; then, where it helps, one bullet per stretch>

## Story order
| Where | Event | Words | Source |
<one row per moment, in story order: CH / SEQ / board card; a plain line; the exact quote (his, or labelled); file:line>

## The stable core
<what every source agrees on — the parts that are settled>

## Where the sources disagree
<ranked: what touches the current book first, then later books, then the archive's dead ends; each with both quotes and
which is newer>

## Gaps against the grid
<the beats or spans where the thread should be working and nothing carries it — searched in every strand; each one
becomes a redraft marker in the step table>

## Your calls
<numbered; only what the tree can't settle; each one plain question, with the evidence, and "decide at the redraft" where
that is an honest answer>

Resolved against your rulings — confirm:
<one line each: the would-be call, the ruling or newer draft that settles it, where it lives>

## Stale, for canon-sync (no action now)
<REFERENCE / DEV lines the newer material has overtaken>

## Step table — <label>
Proposed label **"<label>"** (<from his words, where>); goal holder <who>; goal <his line, quoted, with source>. Label,
goal and goal holder are his call.

| # | Step | His words | Lands at |
<a plain line of what happens; his exact words; card id (^id) / CH / SEQ — "board Ch N (^id)" when it is on the board>

**Redraft markers** (working text, labelled "<thread> —", not his prose):
| # | Marker | Lands at |

<one line: which steps are on the board now, which wait for a part or an import>

## What this trace did not check
<families skipped or listed only, prose ranges that don't exist yet, candidates dropped unverified>
```

## The step table onto the board — only on his "send it"

The table is shaped as a plan subplot (`references/plotting.md` § Subplots): label, goal holder, goal, and steps with
`text` (the plain line), `quote` (his words) and `src` / `cards` / `parts` (where it lands), markers as steps whose text
keeps its `<thread> —` prefix. When he says "send it" (or "put it on the board"), that is a new run, not part of the
trace: his rulings on label and goal are applied, the subplot is added to the plan with `plan_tool.py set --json-file`
(subplots only, so the grid's approval stands), then `subplot_build.mjs … --key <k> --out <ops>`, `apply --dry`, his tab
closed, `apply` — the usual change list after. Steps whose part isn't on the board yet wait unplaced, with their reason.

## Talking to CRE, for this mode

Lead with what the thread is, in two or three plain sentences. Then his calls, one recommended answer each — and where the
answer is his taste, say so and offer "decide at the redraft". Then the report link and one line: "Want the step table on
the board? Say 'send it'." No ids, paths or model codes in the lead. His answers are rulings: they land where he says (the
plan, a marker, a DEV note — a separate run), and the next trace reads them as part of his record.
