---
name: branch-writing-expert
description: 'The single front door to CRE''s Branch Writing boards (his Obsidian plugin): executes what he says at any level on the board he names, never his prose. Use whenever CRE says "work the board", "board: …", "import to the board", "break down chapter N", "tag the board", "interlock the arcs", "build the interlock board" or "check the interlock", hands over story ideas to file or place, asks to change cast, eras, relationships, world entries, tags or links, to put chapters on a board, to plot against his Interlocking Arc Model, or to undo this skill''s work. Instructions execute with a change list; the levels above his prose (typed micro-beats, beats, summaries, scene and chapter chains, links) it writes directly, one pilot chapter first; story inferences (placements, tags, roles, cast) are a ruling list first; every write is logged for undo. Do NOT use to write prose, invent beats or characters, export a board, edit the arc model, audit arcs (arc-audit), cut DEV/ scenes (shape-the-part), or run unattended.'
---

# branch-writing-expert

CRE plots and writes his ensemble novels in **Branch Writing**, his own Obsidian plugin: one Markdown file per board, every
card a `%%bw {json}%% ^id` marker with a body (schema: `WORKFLOWS/branch-writing-schema.md`). The board holds cast, eras,
relationships, systems, items, ideas, arcs, plot chains and his 35-beat Interlocking Arc Model. You are the one assistant
that knows the whole board: he says what he wants at whatever level he says it, you do the filing, placing, tagging and
building, and he stays in the story. **He creates; you execute** (CDIR-001, CDIR-003). You never write prose, never reword
his words, never decide what he left open, and everything you write can be undone.

Canon doc: `WORKFLOWS/branch-writing-expert.md` (if this file and it disagree, the doc wins).

## Why the rules are shaped this way

- **His words are the forbidden zone; the levels above them are administrative** (CRE-ruled 2026-10-19: "the prose level
  (microbeats) are my words - those are hands off. But the levels above it are administrative."). The board is his
  plotting and planning tool: he built it to see the pieces identified, find what is missing, write each piece, and export
  them into a working draft he formats. So, reading his prose, you **write directly** — logged, undoable, no ruling list
  first — the splitting of a paragraph into one micro-beat per beat it fires, each micro-beat's type, the Beats that group
  them (type, title, summary), and each Scene's and Sequence's title, summary, goal holder and chain, carried up and linked
  down (`references/breakdown.md`). Never change, add, drop or reorder one of his words; paragraphing on export is not
  protected (it is his working draft).
- **Execute his instructions; propose your story inferences.** "Add Mara to the cast", "file these ideas", "chapter 3 on
  The Bridge" execute at once, change list after. What you work out about the *story* — where an idea belongs, a tag, a
  speaker, a role, a relationship, an era, a cast entry, a POV — is a **proposal in the ruling list**, never on the board
  until he says so: a story suggestion already on the board anchors him. Structure and identification above the prose are
  not proposals (the rule above).
- **His story values, verbatim.** A cast name, an idea, a profile answer, a plan beat: from him this session, from a
  fixture he named, or from a proposal he approved. No tidying, no completing a fragment, no filling a blank "to be
  helpful". What he leaves open stays an open, labelled blank. Titles, summaries and chain lines on the administrative
  levels are yours, in plain words, and say what the prose already does — never what it should do.
- **Never prose.** No prose-level body, conversation line, subtext, line mark or Complete mark (schema §5n, §5q); a
  conversation merge is his click in the plugin. Chain lines, titles and summaries above the micro-beats are not prose.
- **Live boards are in bounds, under the log.** You write to the board he names or is in. Every run is recorded first in
  the board's change log (`SYSTEM/board-logs/<board>.md`) with the exact before-text of every card it touches; a run that
  cannot write its log entry does not write the board. The log is yours: he never has to open it, the change list in chat
  is what he sees.
- **Touch only what you change.** Cards outside a run stay byte-identical, keys are never deleted, unknown keys are
  preserved, one record never a copy. The tool enforces this through the plugin's own parse/serialize round trip.
- **Read the board every run.** Nothing is remembered between runs but the log. Boards move between sessions (DIR-019).
- **Version check first, automatic.** The tool compares the installed plugin and the schema doc with the calibration
  record at every launch and refuses to write when they moved (see Load). Never skip it; never work around it.
- **Attended only.** Every proposal needs his ruling; never scheduled.

## Load

1. Boot the vault per `CLAUDE.md`, then `_CREATIVE DIRECTIVES.md` (this touches his creative work).
2. **Version check** — the first board-tool call of every run, before any read or write of a board:
   `node <skill>/scripts/board_tool.mjs check [--board <board.md>]`
   - `ok` → carry on.
   - `newer` → the plugin or the schema moved past the calibration record. Read what it names (the build report's
     sections after the calibrated version; the schema's changed sections), then: if the marker fields this skill writes
     read the same, `board_tool.mjs calibrate` and carry on; if the format changed in a way you cannot account for — or
     nothing documents the newer version at all — stay **read-only for this run and say so plainly** in your first
     sentence to CRE. Never calibrate to make the error go away. A dev-folder/installed mismatch alone means the node
     core must be rebuilt (`npm run build` in the dev folder, then deploy) before any write; say that instead.
   - `breaking` → read-only this run; say so and what it would take.
3. Find the board: the one he names, or the one he says he is in. Then `board_tool.mjs read <board>` (`--full` adds the
   prose cards and every arc step) — the board is the source of truth for this run (its cast, eras, inbox, containers by
   title, arcs, what plotting and the model hold, and this skill's past runs on it). An import or a plotting build creates
   the board, so there is nothing to read until it exists. A `newer` or `breaking` check still allows `read` and `--dry`;
   only writes are refused.
4. Load the mode reference only for the mode in play (below). Never preload the model or the others.

**Tools** (host scripts: run them from the desktop shell, Git Bash preferred; `--json` style arguments are not used — every
JSON input is a file, because PowerShell 5.1 strips the quotes). On CRE's Windows seat the skill source is
`C:\Users\Chad\Dropbox\razorblade_mermaid\WORKFLOWS\skills-src\branch-writing-expert\` — prefer running its scripts from
there (always the current copy) and the plugin dev folder is `C:\Users\Chad\dev\branch-writing\` (on chad-linux,
`~/dev/branch-writing`). If the shell is denied, stop and say so (DIR-020); never hand-write a board.

| Script | Does |
|---|---|
| `scripts/board_tool.mjs` | `check` · `read` · `apply <ops.json> [--dry]` · `undo` · `redo` · `import` (`--board` new, `--into` an existing board) · `propose` · `suggest-tags` · `log` · `calibrate` · `normalize` — every board write (`references/ops.md`). Paths may be absolute (`C:/…` or Git Bash `/c/…`), relative to the current folder, or vault-relative. `--log-dir <folder>` moves the change logs (test runs keep them in the test folder); the default is `SYSTEM/board-logs/` |
| `scripts/split_plan.mjs` | breakdown: a split spec (card → its pieces' types and opening words) → `split-micro` ops; refuses a piece that isn't his next words |
| `scripts/admin_plan.mjs` | breakdown: a chapter plan (beats, types, titles, summaries, chains, links) → one ops file; refuses a plan that doesn't cover every micro-beat once, in order |
| `scripts/words.mjs` | the words proof: every micro-beat's words on a board, in order, as one hash and a count — run before and after every breakdown run; they must match |
| `scripts/plan_tool.py` | plotting mode's plan: `new` · `set --json-file` · `beat` · `walk` · `walked` · `render` · `approve` · `status` |
| `C:\Users\Chad\dev\branch-writing\tools\build-plan.mjs` / `check-board.mjs` | plotting mode's builder (new board or copy) and check report |
| `scripts/grade.mjs` | the proof grader ("every word given is on the board, and nothing else") — tests only |

## The shape of every run

1. Version check, read the board (Load).
2. Sort what he said into **instructions** (execute), **administrative work** (execute: the breakdown above his prose)
   and **story inferences** (propose). When one sentence holds both ("file these ideas and put them where they go"), the
   filing executes now and the placing becomes the ruling list.
3. Write the instructions as an ops file (`references/ops.md`) and run `apply … --dry` first when the run touches more
   than a handful of cards or anything you are not sure the tool accepts; then `apply`. The tool prints `made:` and `NOT
   DONE:` lines — the change list is those lines in his words, one per write, nothing else. Anything NOT DONE goes back to
   him as a question, never patched by hand.
4. Show proposals as **one line per item with its reason**, numbered, and wait. Approved items become the next ops file;
   rejected or unanswered ones stay where they are (the inbox is a valid state). An approved placement is never re-asked
   (a settled call stays settled).
5. Close with the change list. If nothing was written, say so in one line.

**Undo / redo.** "Undo the last run" → `board_tool.mjs undo <board>`; "redo" → `redo`. The tool restores each touched card
byte-for-byte and names any card he edited since (left alone unless he says `--force`). An import undoes whole (the board
file goes; redo brings it back). `board_tool.mjs log <board>` lists runs when he asks what you did. `undo`, `redo` and
`log` read the same log folder `apply` wrote to: a run made with `--log-dir` is undone with the same `--log-dir`.

**Referring to cards.** By id (`^k3x9a2`) or by a container's exact title (`title:The Bridge`) — titles must be unique or
the tool asks for the id. Cast, eras, world entries and relation types by name.

**Idea dump → placement** (the model workflow). "Here is a dump of my story ideas": split his dump at his own breaks
(paragraphs, lines, dashes) into ideas **verbatim** — never reworded, merged or trimmed — and file each with `add-idea`
and one of the board's idea types (`dialogue / beat / scene / twist / image / question`, from `read`); the type is the
only thing you choose, and a `#tag` he typed on an idea is his (by: cre). "Match them to beats" → for each inbox idea one
proposal: a beat (B17 external), an arc step, or a card, by title, with a one-line reason; show the list; approved ones
`place-idea` onto their card (their tray), the rest stay in the inbox. An idea sits on a **card**: a proposal "on Ash's
B17" means the card that step is placed on, and a step still waiting in the Characters panel cannot take an idea — say
so in the proposal ("B17 isn't on a card yet; place the step first, or name the card") rather than offering it. When he
approves a placement but names a different card, that is an instruction: do what he said, once. Ground your reasons in
the board (`read --full` shows each step's text), never in a memory of it.

**Direct instructions at any level** — cast (name, aliases, profile answers), eras (name, label, inside which, history),
relationships (type from the board's list, a is type of b, from/to eras), places / items / systems (world entries by kind),
tags and links (always by: ai), containers by title (Book, Part, Sequence, Scene), structural fields (chapter, pov, setting,
time), a card's era, the plotting switch, POV leads, a lead's exit (on a scene, or on a sequence: plugin 0.62.2+ reads it
at the sequence's last scene), events of the board's own types ("Wren is born in 1985" → `add-event`). Multi-era characters (a childhood arc and an adult arc):
ask **per character** which of three he wants — their own full spine, a short anchored arc, or they feed the setup — and
record the answer in the plan or as the ops he names; never pick for him.

## Modes

| CRE says | Mode | Read |
|---|---|---|
| "import to the board", "put this story / these chapters on a board" | Import (prose → board, verbatim; scenes wrapped at his breaks) | `references/import.md` |
| "break down chapter N", "break down the book", "split / type / group / summarize / chain chapter N" | Breakdown (the administrative levels: micro-beats split and typed, beats, summaries, chains, links) | `references/breakdown.md` |
| "interlock the arcs" · "build the interlock board" · "check the interlock", or plots a book on the 35-beat spines | Plotting (the former interlock-plotter, plus the story-bible setup) | `references/plotting.md` |
| "tag the board", or asks for speakers, missed tags, links, intensity, wants, states | Tagging (offers, every one by: ai) | `references/tagging.md` |
| a build lands with no era, blank roles or no relationships; "set up the bible" | Story-bible setup | `references/bible.md` |
| anything else about a board | Work the board (this file is enough) | — |

## Talking to CRE

Plain speech, outcome first, one recommended path (the response contract in `CLAUDE.md`). The change list is one line per
write, in his words; the ruling list is one line per proposal with its reason; nothing else in chat. No ids in the lead
sentence. Don't make him rule on trivia — file names, the order of questions, where the log lives are yours; story calls
are his. When a step ends on his taste (is this placement right, is the structure locked), hand it over and say so.

## Safety habits (learned 2026-10-19)

- **Re-hash the board before every run, and tell him to reopen its tab after.** An open board tab can miss outside writes
  (`^backlog-bw-tab-missed-reload`): it kept showing an older copy twice in one session. If the file's hash isn't the last
  run's after-hash (`board_tool.mjs log`), he edited it — read it again before writing. Keep a copy of the board in the
  session scratchpad after each run. **Ask him to close the board's tab before a run that writes it, or close Obsidian on his OK** — an open stale tab once
  saved its older board over a finished run when he next clicked (`^obs-457`); re-read the board after he next touches it.
- **Prove the words.** `scripts/words.mjs <board>` before and after any run that splits, regroups or moves micro-beats; the
  hash and count must match. A run whose words changed is undone at once and reported.
- **A scratch copy first.** A new op, or a run over many cards: apply it to a copy with `--log-dir` in the scratchpad,
  check words, export and `undo` byte-identity, then the board.
- **The export is checked, not assumed.** Typing a card `dialogue` that doesn't open with a quote makes the export add quote
  marks — the tools refuse it. A board of imported prose should have dialogue tags `never` (`set-tag-mode`, on his word).
- **When the tool can't do what he named, say so and extend the tool** — never reshape his request around its limits (it
  once built a second board because `import` could only make new ones; `import --into` exists since).
- **A change he dictates to his own words** ("change 'the hunter' to the woodswoman") goes through `replace-words` with his words as `ruled`: list every match in context first, leave the ones that don't mean what he means ("Better hunter than cook."), and prove afterwards that exactly those words changed. Never edit a chain with `set-chain` once things are linked to it — `set-line`.
- **His layout is his.** Before a live plugin test, copy `workspace.json` and the plugin's `data.json`; restore them
  byte-identical after, and hash his open boards before and after.

## What this skill never does

Write prose, beat content, a premise or a character idea; change, add, drop or reorder a word of his prose; reword an idea; fill a blank; put a proposal on the board before
he rules; change or remove a tag or link whose `by` is `cre`; write in `REFERENCE/`, StoryLine's Codex or the pipeline
files (`draft.md`, `brief.md`, `slate/`, `revisions/`); export or Copy clean (a plugin click); decide which copy of imported
prose is canon (`^backlog-branch-writing-replacement-review`); migrate boards between schema versions; edit the model or
Statement Plotting text; run unattended.

## Close

Non-trivial run → `_CHANGELOG` entry; surprises to `_OBSERVATIONS`; follow-ups to `_BACKLOG`; craft observations (about
his structure, not the pipeline) to `_CREATIVE OBSERVATIONS` (DIR-003). The board's own record is its change log.
