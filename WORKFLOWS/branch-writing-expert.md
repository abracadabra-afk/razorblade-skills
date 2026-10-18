---
type: workflow
name: branch-writing-expert
lane: Meta (vault tooling for the fiction lane) — structure, administrative
status: authored 2026-10-18 through skill-creator from the ratified intent; proven on scratch copies by scripted stand-ins (proof report below); packed per DIR-009; install (Save-skill) and CRE's own run on the Practice board pending
triggers: '"work the board" · "board: …" · "import to the board" · "tag the board" · "interlock the arcs" · "build the interlock board" · "check the interlock"'
skill_source: WORKFLOWS/skills-src/branch-writing-expert/
intent: "[[WORKFLOWS/intents/branch-writing-expert]]"
schema: "[[WORKFLOWS/branch-writing-schema]]"
absorbs: "[[WORKFLOWS/interlock-plotter]] (plotting mode) · ^backlog-branch-writing-tagger-intent (tagging mode)"
created: 2026-10-18
last_updated: 2026-10-18
---

# branch-writing-expert

**What it does.** The single front door to Branch Writing, CRE's Obsidian plugin for plotting and writing his novels. He
feeds it information at any level — structure, cast, eras, relationships, systems, items, tags, a dump of story ideas — and
it executes on the board he names or is working in, live boards included. It executes his ideas, never changes them, never
writes prose, and shows a short change list after each run. Every write is logged per board so it can undo and redo its
own work byte-for-byte. It reads the board fresh every run and checks the installed plugin and the schema against its
calibration record at every launch (CRE rulings (a)–(h), 2026-10-18; the intent).

**Modes.**

| CRE says | Mode | What happens |
|---|---|---|
| "work the board" / "board: …" / any instruction about a board | Work the board | direct instructions execute (cast, eras, relationships, world entries, tags, links, containers, fields, plotting switch, leads, exits); inferences are a ruling list he approves first |
| "here is a dump of my story ideas" → "match them to beats" | Idea dump → placement | ideas filed verbatim in the board's inbox, typed; one placement proposal per idea with its reason; approved ideas move to their card's tray, the rest stay in the inbox |
| "import to the board" | Import (prose → board) | the plugin's convert rule, word for word, into a new board (a short story note, or one board per book from `CHAPTERS/*/draft.md`, marked a working copy); scenes, chapters, dialogue speakers, cast and POV proposed and ruled; sources never changed |
| "interlock the arcs" · "build the interlock board" · "check the interlock" | Plotting (the former `interlock-plotter`) | plan in his words → his approval → a new board or a copy via the plugin's node builder → the story-bible setup → the check report, observations only |
| "tag the board" | Tagging (the former "AI tagger") | tags and links as `by: ai` entries; beat types, speakers, summaries, wants, states and a chain summary under the `ai` marker key; intensity to the board's sidecar; route A (rule first) or route B (write as offers) |
| after a build, or "set up the bible" | Story-bible setup | a placeholder era when none is named, every unplaced step filed in it; roles and the relationships the model's roles state, proposed and ruled; nothing invented |
| "undo the last run" / "redo" | Undo / redo | the touched cards restored or re-applied byte-for-byte from the board's change log; a hand-edited card is named and left alone |

**Where things land.**
- The board he names (live or new). Change logs: `SYSTEM/board-logs/<board>.md` (his default; out of his sight — the chat change list is what he sees).
- Plans: `WRITING/BOARD PLANS/<board> - arc plan.md`; check reports: `SYSTEM/reports/YYYY-MM-DD-<board>-interlock-check.md`; intensity offers: `<board>.measure.json` beside the board (schema §6a).
- Calibration record: `WORKFLOWS/skills-src/branch-writing-expert/calibration.json` (the plugin version, the schema doc's version and hash, the node core's hash it was calibrated to). The tool reads the vault copy first, so a recalibration lands in the source and ships at the next pack.
- Test runs: `SYSTEM/skill-tests/branch-writing/_work-*`.

**Tools** (in the skill's `scripts/`; host scripts run from the desktop shell, Git Bash — every JSON input is a file, never a shell argument, `^obs-444`).
- `board_tool.mjs` — the one writer, over the plugin's own pure core (`C:\Users\Chad\dev\branch-writing\test\core.mjs`, built by `npm run build`): `check` (version check) · `read` · `apply <ops.json> [--dry]` · `undo` · `redo` · `import` · `propose` · `suggest-tags` · `log` · `calibrate` · `normalize`. Ops shapes: `references/ops.md`. It refuses to write when the version check is not `ok`, when the board doesn't round-trip through the plugin's serializer, when a field is the author's (summary, statements, outcomes, chain, marks, Complete), when a lead exit is put on a Sequence (the plugin honours units only), and when a value would reword or invent.
- `plan_tool.py` — the plotting plan (carried over from interlock-plotter, plus `set --json-file`).
- `grade.mjs` — the proof grader: every string given is on the board and nothing else, untouched cards byte-identical, undo/redo byte-exact, and the mode-specific criteria.
- Plugin dev folder: `tools/build-plan.mjs` (new board or copy from an approved plan), `tools/check-board.mjs`.

**Guardrails, with reasons** (full statements in the intent).
- *Execute his instructions; propose his inferences* — a suggestion on the board anchors him (CDIR-003); an executed guess is his to find and undo.
- *His words, verbatim; never prose* — the organic process breaks the moment the tool writes story (CDIR-001). Open slots stay open, labelled blanks.
- *Live boards under the log* — the log entry is written before the board; a run that cannot log doesn't write. Undo restores byte-for-byte; a card he edited since is left alone and named.
- *Touch only what you change* — the plugin's parse/serialize round trip is the gate; keys hidden never deleted; unknown keys preserved.
- *Version check first, automatic* — a tool working from a stale picture of the format is the one way it can damage a board; a check he has to remember doesn't happen. `newer` → read the build report's later sections and the schema's changed sections, then `calibrate`; a change it can't account for → read-only, said plainly.
- *Tagging reads ruled terms, writes none* — vocabulary from `REFERENCE/_LEXICON.md` and `_DEV_MAP` read-only (DIR-014); a `by: cre` entry is never touched; dev-edit's blind seats never see the network.
- *Story-bible setup never invents* — a placeholder era (BW U13), roles from the model role, relationships only where roles state them; no Place, Item or System the plan doesn't hold.
- *Ensembles, 1..N leads* — proven at one lead and at five.
- *No clicks in his window; attended only.*

**Known gap (plugin 0.62, probed 2026-10-18).** A lead exit written onto a Sequence is ignored by the plugin (unit ids only: `plottab.ts:241`, `flows.ts:84`); the builder writes the exit onto whatever container holds the exit step. Not fixed in this build (the dev folder's last commit is 0.62.0). The skill writes exits only where the plugin honours them: `set-lead-exit` refuses a Sequence, and plotting mode places an exit lead's exit step on a Scene (the five-lead proof does). Fix tracked at `^backlog-bw-lead-exit-unit`.

**Not for:** prose, premises, character ideas, rewording an idea; export / Copy clean (a plugin click); the pipeline files, `REFERENCE/`, StoryLine's Codex; editing the model or Statement Plotting text (CDIR-002); migrating boards between schema versions; deciding which copy of imported prose is canon (`^backlog-branch-writing-replacement-review`); scheduled runs.

**Retirement of `interlock-plotter`.** The intent retires the standalone skill once the expert passes the same one-lead and five-lead proof. The proof report records the result; the uninstall (claude.ai Settings → Skills) and the removal of its `.skill` are CRE's clicks, after his own Practice-board run.

**Proof.** [[SYSTEM/reports/2026-10-18-branch-writing-expert-proof]] — eight scripted stand-in runs on scratch copies (direct instructions with undo/redo, idea dump → placement, tagging on a 313-card board, a short-story import, a three-chapter book import, the version flip, plotting at one and at five leads with the bible setup), graded by `grade.mjs`.

## Run log

- 2026-10-18 — authored through skill-creator from the ratified intent; schema §4 and every "AI writers" line amended; nine stand-in runs on scratch copies (direct 12/12, ideas 12/12, tagging 9/9 + bulk 9/9, story import 11/12 → fixed → 12/12, book import 15/15, version flip 3/3, plotting 25/25 at one lead and 27/27 at five); packed per DIR-009. Install and the Practice-board run are CRE's.
