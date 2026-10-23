# Stage the beats — "stage the beats for <scene>": a finalized scene's map, as one beat brief

When CRE finalizes a scene he wants each beat's job in one place at the moment he writes it: what happens, what it does for
which arc, what comes in, who arrives in what state, what to land, plant or pay off, and which of his own lines are
waiting. The board already holds all of that, but it is spread across panels and side files. This mode gathers it and
writes one page per scene, so none of it has to be held in his head (`_ME`: never make him the mechanism; ADHD Patterns
#8). (Intent: `WORKFLOWS/intents/branch-writing-stage-the-beats.md`. First subject and worked example: Witchwood Interlock,
Ch 48 "Bad Hounds Bite".)

Triggers: "stage the beats for <scene>", "stage scene X", "brief the beats", "restage <scene>". One scene per trigger.

## Why the rules are shaped this way

- **Every line has a source on the map, or it isn't written.** The brief carries authority only because each line is a
  call he already made: a step, a tag, a thread line, a DEV line, a marker, an idea. An invented need is the hardest error
  for him to spot (CDIR-003). If you want to write a line and can't cite it, it is a gap (Open), not an instruction.
- **Say what a beat must do, never how it is worded.** "Land his readiness to bite the glass", not a sentence of prose.
  His words are the forbidden zone, and the brief must never become a draft (CDIR-001).
- **A quote is not a summary.** Summarize plainly. Quote him only where the line *is* the story object (a vow, an adage, a
  quoted plant, a motto), and keep its context ("the hermit's Widowsbane, 'Put it into his mouth…' (T09)"). `verify`
  refuses a quoted span that is not his words on the board, in the DEV note or in `threads.md`. The one exception: when he
  rules a gap in chat, write the ruling on a line that opens `**Ruled (CRE, <date>):**`, quoted as he said it. Log it
  in `_CHANGELOG` too (and in `_CREATIVE OBSERVATIONS` when it is about the story), because the brief is regenerated.
  Rulings on that line are not checked. A ruling is never re-asked at a restage: carry the line over.
- **Steps sort onto beats mechanically; ideas sort by his ruling.** A step's chain line (`plotLine`) and a beat's
  `plotFrom` (a single line or his bundled run) already say where the step belongs, so the script places it and you never
  re-place it. Where an idea that sits on the scene belongs is a story call: a ruling list first, then `place-idea`
  (CDIR-009: an approved placement is never re-asked).
- **His grouping is the ruling.** A beat he bundled over several lines (`plotFrom "<scene>:<a>..<b>"`) is one brief with
  exchange rows. Never bundle or split lines yourself, never drill, never move a step (plotting mode, his board moves).
- **Weight is read off, never judged.** "Lean into character or action" is what is slotted: count character-arc steps
  against plot steps (CRE 2026-10-22: "i'm not sure lean into a character here is subjective if their are arc beats
  slotted in the beat").
- **A need nobody placed is a gap, and its beat is his call.** "Needs a plant before Ch 60; no beat holds it yet." Research
  the tree first (DIR-011), then name it. Never pick the beat.
- **The brief is derived; it goes stale and is rebuilt, never ruled on** (DIR-019 §1). Its fingerprint covers the scene's
  chain and fields, its beats, the steps on it, the ideas' placement and the prose's words. When any of these moves, the
  brief is stale. Rebuild it on his word.
- **The checklist is what the map holds, not a test he is graded on.** Divergence while drafting is a win, and the map
  follows the prose at revision (DIR-017 §2). On a beat with prose, show map-vs-prose gaps; never grade or touch the prose.
- **The brief lives in its own file, linked from the scene.** A beat's summary says what the prose already does, never
  what it should do (CRE 2026-10-19), so nothing from the brief goes into a summary.
- **N POV leads, several spine sets.** Name each step by its arc and role (the Woodsgirl spine is its own set, the boy is a
  deuteragonist against Death), never as if there were one lead (memory: ensemble POV books).

## The run

1. **Load.** Boot per SKILL.md, read `_CREATIVE DIRECTIVES.md`, run the version check and `read` the board. Hash the
   board, then run `words.mjs <board> --ideas`. Keep both lines; they must match at the end. Keep a copy in the scratchpad.
2. **Gather** (read-only, a few seconds):
   `node <skill>/scripts/stage_scene.mjs gather <board> --scene <^id | title:… | "Ch 48"> --out <scratchpad>/stage`
   It writes `facts.md` (readable, in chain order), `facts.json` (what `verify` checks against), `ideas.json` (the scene's
   ideas on no line) and `README.md` (what it did not check). It names the brief's path:
   `WRITING/BOARD BRIEFS/<board name>/Ch NN - <chapter title>.md` (the scene title when the chapter has several scenes).
   It checks names against the World tab *and* the cast: a name with no World entry may be a cast member (the
   Trailkeeper is cast), so never call a thing missing from the board until both are checked. Word "not linked"
   the way he sees it. The scene card draws a chip for every cast or World name in its chain lines (by words, nothing
   stored) beside the entries linked by hand, and since plugin 0.66.2 every such World chip is a link: it reaches the
   entry's Through the story (schema §5h, "Linked by words"; CRE 2026-10-22: "shouldn't all chips provide links?").
   So a name with a chip is linked. The facts mark it "(chip from the words)"; never offer to link it by hand or call
   it untracked. "Not linked" is only for a name the facts list as NOT LINKED: named outside the chain lines (a summary
   or a field), or a chip he took off with ×. Say which, plainly: "the darkness is named in the beat's summary, not
   its lines, so its World entry doesn't list this scene" (CRE 2026-10-22: "confused lots of tags on the scene?").
   If the scene is already staged, run `check` first: *fresh* means say so and stop unless he said "restage".
3. **Read the sources it names.** These are the DEV note (the scene's `seq` field), the threads it lists, the trace reports
   that cite the scene, a `choreo/` folder if one exists, and the measure side file. The script's thread and trace hits are
   candidates matched by name. Read them before citing them; use only the lines that bear on a beat. `REFERENCE/` and DEV
   are read-only, always (DIR-012).
4. **The ruling list: ideas onto beats.** Only if `ideas.json` is not empty. Make one numbered line per proposal, grouped
   by run of consecutive ideas ("ideas 2–21 (Day 30 → 'She backed away') → beat 1 'The mad sire': the pen barred, the mad
   sire"). Each reason is the idea's own words beside the beat's line. Ask once: "approve all, or name the ones to
   change". If he waves it off, the ideas stay on the scene. That is a valid state, and the brief says so under My material.
   Approved runs become `place-idea` ops (`on` = the beat). Dry run, then apply, under the change log.
5. **Write the brief** (the shape below), into the scratchpad first. Then run, in order:
   - `python <skill>/scripts/stage_front.py <facts.json> <brief.md>`: the frontmatter (DIR-004: `yaml.safe_dump`,
     parse-gated). Re-gather first if you placed ideas, so the fingerprint is the board's current one.
   - `node <skill>/scripts/stage_scene.mjs verify <brief.md> --facts <facts.json>`. It checks that there is one section per
     beat, each citing its beat, that every step on the scene appears under exactly its own beat, that a run has an
     exchange row per line, that every quote is found, that every section has a Sources line, and that the fingerprint
     matches. Fix every PROBLEM line; never patch `facts.json`.
   - Spot-read 10 checklist lines against the cards and files they cite. This is the check the script can't make: that
     each line says what its source says.
6. **Land it.** Copy the brief to its path in the vault. Then ask him to close the board's tab (`^obs-457`), re-hash, and
   write the stamp:
   `node <skill>/scripts/stage_scene.mjs stamp-ops <board> --scene <ref> --brief "<vault path>" --out <ops.json>`, then
   `board_tool.mjs apply <ops.json> --dry`, then `apply`. That writes `staged = <date> · fp <hash> · <path>` on the scene
   (a structural field; the fingerprint ignores it) and a `by: ai` link to the brief (rel "beat brief").
   Then `words.mjs --ideas` again: both lines must equal step 1's. Then `check`: it must say *fresh*.
7. **Close.** Use the chat shape below, then the `_CHANGELOG` entry (SKILL.md Close).

**Staleness on demand.** "Is the Ch 48 brief current?" → `stage_scene.mjs check <board> --scene <ref>`. *Stale* names
what moved (chain, beats, steps, ideas, prose). Tell him in one line and offer the rebuild ("restage Bad Hounds Bite").
Never rebuild unasked.

## The brief's shape

Frontmatter (written by `stage_front.py`): type, board, scene, chapter, title, built, fingerprint, fingerprint_parts, mode,
sources.

**Header.** A one-line note that this page is derived, not a spec, and how to rebuild it. Then **Where it sits** (part ·
chapter · scene · DEV SEQ · era, or "dual" with both timelines named) · **Setting** · **Goal holder** · **Summary** (plain,
from the scene's) · **Story from → to** · **What the scene accomplishes** (the DEV note's "what this is doing", plain, his
key line quoted) · **Scene-level open** (the unwritten half, ideas waiting on placement, entries named but not linked (outside the chain lines, or taken off with ×),
entries missing from World, no intensity score, DEV markers, steps off any beat, needs inherited from the sequence).

**One section per beat, in chain order** (`## N. "<beat title>" · <type> · <line kind> · <timeline>`):
- **What happens:** one or two plain lines from the beat's summary and line.
- **What it accomplishes:** one bullet per arc step on the beat. Give the arc and its role (and the arc's goal, with its
  motto quoted), the step's number and model beat, the step as a plain line, and "The step before it (Ch N): …" from the
  facts. Add the DEV note's line for the beat where it says what the beat is for.
- **Coming in:** the previous beat, then the previous beat in the same timeline (dual scenes), then "The reader knows",
  which is each plant and earlier step this beat relies on, with chapter or thread and his line quoted.
- **States:** from → to per character in play, from the steps' words, the DEV line and any ledger rows or offers. A state
  the map doesn't give is "(not stated on the map)", never guessed.
- **Checklist,** each line typed and sourced:
  `Land` (an arc step) · `Plant` · `Pay off` (full or partial, naming the thread) · `Foreshadow` · `Move` (a state, from →
  to) · `Show` (his DEV words for the beat, quoted) · `Weight` (character-arc steps vs plot steps, counted; markers
  listed apart) · `Use` (his ideas and dictated lines, cited by id or range) · `Open` (held and audit markers, quoted, and
  gaps).
- **My material:** his ideas and prose for the beat, or "nothing yet".
- **Open:** gaps found while building, and map-vs-prose gaps on a beat with prose.
- **Sources:** one line: beat id · line id · step ids · marker ids · DEV sections · threads · world entries · idea ids.

**A bundled beat** (`run: true` in the facts) keeps the same section, with the run laid out first:
- **The run:** purpose, stakes and outcome. The outcome is the run's last line that has an ending (else its last line).
- **The exchange table:** `| # | Line | What happens | Upper hand | Carries out |`, one row per line with the line id in
  it. "Upper hand" and "carries out" come from the line and its steps' words; where they don't say, write "—".
- **Steps by row**, then **carried state** run down the rows (wounds, weapons, ground, light, who holds what), each from
  a line, a step or a ledger row.
- **Finer layer:** the beat's own chain (`ownChain`) and its blocs, if he wrote one. Each bloc shows what prose covers it.
- **Choreography:** a beat map in the chapter's `choreo/` folder, pulled in where one exists. Otherwise write "a run with
  no blocking yet — choreograph it?". Designing it is the choreographer's job, with him.

About one screen per beat. Short lines and checklists, no essays. Match the Ch 48 brief
(`WRITING/BOARD BRIEFS/Witchwood - Interlock/Ch 48 - Bad Hounds Bite.md`) and the appendix example in the intent.

## Talking to CRE, for this mode

Lead with the outcome ("The Ch 48 brief is ready: 9 beats, every arc step placed. The present half is unwritten.").
Then give the ruling list if there is one, with the ready-to-type reply. Then the change list (the stamp, the link, any
placed ideas) and the brief's path as a link. The brief's usefulness is his call; ask once whether it takes the load off,
and log what he says.

## What this mode never does

Write prose, beat content, a chain line or a beat's own chain; reword an idea; bundle, split, drill or move anything;
place an idea before he rules; design an event; grade prose; write into a summary; write `REFERENCE/` or DEV; stage more
than the scene he named; run unattended. Siblings it doesn't overlap: runway-builder (the dictation route's `brief.md` →
runway), brainstorm-walker (the WIW lens walker), choreographer, workshop-chapter, dev-readiness, and this skill's own
audit and trace modes.
