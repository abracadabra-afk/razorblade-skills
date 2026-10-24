# The ops file — every board write

`node scripts/board_tool.mjs apply <ops.json> [--dry]`. One file per run; one run per instruction batch (one undo step).
The ops file's `"board"` is the board written. A `--board` that names a different file is refused, `--dry` included
(`^obs-474`: a "scratch" test once wrote the live board). For a scratch test, write an ops file whose `board` is the copy.

```json
{"board": "WRITING/PROJECTS/.../Practice board.md",
 "label": "his words for what this run does",
 "ops": [
   {"op": "add-cast", "name": "Mara", "aliases": ["Mar"], "profile": {"want": "his words", "flaw": "his words"}},
   {"op": "add-era", "name": "1985", "label": "the drought years"},
   {"op": "add-tag", "card": "title:The Bridge", "tag": "thread:river"}
 ]}
```

Every element carries `"op"` and that op's fields. Ops run in order within one file, so an op may refer to what an
earlier one made by name (a cast member, an era) — not by id, which the real run draws fresh (ids printed by `--dry`
are provisional). Cast profile answers are keyed by the character's profile field names: the starter list is role,
tagline, want, need, flaw, wound, personality, voice, appearance, notes (schema §5b); a project's templates may add
more, and `read` shows each character's `fields`. Eras are added in time order (the list order is the timeline;
`parent` nests a sub-era).

The tool runs the version check, reads the board, applies the ops through the plugin's own core, verifies that every card
outside the run is byte-identical, writes the log entry (before-text of every touched card), then the board, then parse-gates
the file. It prints one `made:` line per write (the change list) and one `NOT DONE:` line per refusal. Exit 2 = refused,
nothing written; 3 = written with NOT DONE lines.

References: a card by `^id` or `title:Exact title` (containers only; unique), or `beat:<scene ref>:<n>` — the scene's n-th
Beat, 0-based (Beats a run has just made have no unique title); cast, world entries, eras and relation types by name (any
case; aliases resolve). Values are CRE's words. `--dry` shows the change list and writes nothing.

| op | fields | notes |
|---|---|---|
| `add-cast` | `name`, `aliases?`, `profile?: {field: value}` | refuses a name already in the cast |
| `set-cast` | `cast`, `field`, `value` | a profile answer (`""` clears) |
| `rename-spine-set` | `key`, `name` | his instruction (2026-10-22, "rename it"): a spine set's display name in the board's model; its pill tag follows the name (`setTag`), the key never changes; arcs already named after the old set name keep their names |
| `add-aliases` | `cast`, `aliases: [names]` | his instruction: more names for an existing cast member (2026-10-21) — appended, existing kept, duplicates and the main name skipped; his names only, no epithets he didn't give |
| `add-era` | `name`, `label?`, `parent?` (era name), `history?` | eras are story-level; a lone era is not the story's start (BW U13) |
| `set-era` | `card`, `era` (name; `""` clears) | on a Sequence it carries forward; deeper, that subtree only |
| `file-beats-in-era` | `era` | every unplaced arc step without an era gets this one (bible setup) |
| `add-relation-type` | `name`, `inverse?`, `forWorld?` | only on CRE's word |
| `add-relation` | `type`, `a`, `b`, `from?`, `to?`, `note?` | "a is type of b"; the type must be on the board |
| `add-world` | `kind` (place/item/faction/religion/polity/magic/role/own), `name`, `aliases?`, `fields?` (`description`, `notes`, …), `sources?` (files) | never invented; from his word or an approved proposal (world walk: a DEV registry entry). A `description` is a plain line drawn from his words; any span it puts in quotation marks must be in the entry's `notes`, his words on the board or a `sources` file, or the op refuses |
| `set-world` | `entry`, `field`, `value`, `sources?` | a `description` gets the same quote check |
| `link-world` | `card` (a Scene or other container), `entry`, `fill?` | world walk (2026-10-22): the card links the entry through the plugin's `linkWorld` (its `world` list); the kind's field (a place → `setting`) is left as it was — a scene naming a place is not set there — unless the op says `fill: true` on his word (then an empty field fills, a field he filled with another name is kept). Admin once the entry is approved; one link per scene, and the cards inside carry it |
| `unlink-world` | `card`, `entry` | the reverse, through the plugin's `unlinkWorld` |
| `add-idea` | `text` (verbatim) or `from: {source, block \| quote}`, `type?` (from the board's ideaTypes), `tags?`, `by?`, `on?` | tags default by: ai; `by: "cre"` only for a `#tag` he typed. `from` takes the words from a file — the n-th block (the plugin's block split, frontmatter skipped) or a `quote` that must occur in it word for word — so his words are never retyped; `on` places the new idea on a card in the same op (a card made earlier in the run, by title or `beat:<scene>:<n>`) |
| `place-prose` | `under` (a Beat or Scene), `source` (file), `blocks: [a, b]`, `skip?: [n…]` | his prose from a source file as micro-beats appended under the container, block for block; the ops name the file and range, never the words; `skip` leaves a heading line or `***` break off (named in the change list); the run logs the file's hash and re-checks it before writing (2026-10-20, the Witchwood board build) |
| `place-idea` | `idea` (^id), `on` (card, or a placed arc step: the card it sits on) | approved placement → the card's tray; refused on a step that isn't on a card yet |
| `place-on-line` | `step` (^id), `via` (the Beat that carries it, or a micro-beat under it) — or `on` + `line` (0 = ENTRY) | CRE 2026-10-21: arc steps sit at line level — the step goes on the scene chain line its Beat is linked to (the first line of a run), through the plugin's `putFloatOnLine` (`plotLine`), moving it to that scene first if it sits elsewhere; a step on a line is drawn as a beat, not a Need. Build the ops from the plan's citations with `scripts/step_lines.mjs` |
| `add-plot-arc` | `label`, `goalHolder?` (cast), `fields?` (goal, stakes, opposition, conflict, planned_outcome, outcome_detail, planned_change, span, action_type) | a subplot (CRE 2026-10-21): a plot Arc (§5q `plotArcs`) with **no model role** — only the external spine carries one. Label and fields in his words; a working label he rules is marked as such in the plan |
| `add-plot-step` | `arc` (label or id), `label`, `text` or `from: {source, quote}` (both: the quote is checked in its source, the step carries `text`), then `via` (its Beat's line) / `parts: [{text, via}]` (sub-steps, one per scene) / neither + `unplaced` (the reason it waits); `before?` (^id of a top-level step of the same arc: the new step goes just ahead of it, story order, renumbered by the plugin's own move) | a subplot step (an arcbeat with `plotArc`) placed by the same rules as the spines' steps: line-level by citation, sub-steps when it spans scenes; refused on an arc that carries a model role. Build the ops from the plan with `scripts/subplot_build.mjs` |
| `split-step` | `step` (^id), `parts: [{text, via}]` (≥ 2; `via` = the Beat that carries that piece), `unplace?` | CRE 2026-10-21 ("yes, sub steps"): a step whose plan cell cites more than one scene becomes a parent with one sub-step per cited scene, through the plugin's own sub-step mechanism (`addSubStep` / `addPlotArcStep` + `parentStep`). Each part's `text` must be a verbatim span of the step's own words, in order — his clause for that piece, never new wording; each sub-step goes on its Beat's line. With `unplace` the parent comes off the board and lives in the Characters panel as a category (its checklist shows each landed sub-step). A cell whose clauses don't split cleanly by its citations goes to his ruling list instead. The split proves the citation; then `set-step-text` makes each sub-step a whole line for its scene (2026-10-22), in the same run |
| `unplace-idea` | `idea` | back to the inbox |
| `add-tag` / `remove-tag` | `card`, `tag` | always by: ai; a cre tag is never removed |
| `add-link` / `remove-link` | `card`, `to` (`^id`, a title, or `[[File#^id]]`), `rel?` | always by: ai |
| `set-field` | `card`, `field`, `value` | structural fields only: chapter, pov, setting, time, job, question…; never summary, goal, outcome, statements (offer them) |
| `set-type` | `card`, `type`, `speaker?` | a direct instruction ("these are dialogue, Mara speaks"); inferred types are offers |
| `add-card` | `kind` (a container level), `under` or `after`, `title?`, `fields?` | Book, Part, Sequence, Scene, Beat containers by his title; never a prose card |
| `wrap` | `cards: [^id…]`, `kind`, `title?`, `fields?` | a container around sibling cards (import: a Scene around a run) |
| `offer` | `card`, `offer: {type?, speaker?, summary?, wants?, states?, chain?}` | tagging mode: written under the marker key `ai` (by: ai, dated), never into his fields |
| `offer-intensity` | `card`, `emotional?: [start, end]`, `physical?: [start, end]`, `rubric?`, `note?` | §6a: to the sidecar `<board>.measure.json`, never a marker |
| `replace-words` | `card`, `from`, `to`, `count`, `ruled` (his words) | **only on his explicit instruction naming the change** ("please change to the woodswoman"): an exact phrase swapped on the cards he means; any other count refuses. The one op that touches his words — never on your own initiative; prove afterwards that only those words changed |
| `fill-step` | `step` (^id), `from: {source: <plan.md>, n, spine, set?, sub?}` | 2026-10-22 (board audit): an **empty** arc step takes its words from his approved plan's cell — the words come from the plan record, never from the op, and the step's beat number must be the cell's. A step with any text is refused (changing his words is `replace-words`) |
| `set-step-text` | `step` (^id), `was` (its current text), `text`, `sources?` (files) | administrative (CRE 2026-10-22, "a summary is better than a quote"): an arc step's or sub-step's text as a plain line of what happens there. `was` must match the board (a moved board refuses); any span in quotation marks must be his words on the board (prose, ideas, arc fields) or in a `sources` file; redraft markers are refused. His old words go to the plan cell's `quote` in the same session |
| `set-arc-text` | `arc`, `field` (goal / stakes / planned_outcome / outcome_detail / planned_change / opposition / conflict), `was`, `text` | administrative (CRE 2026-10-22): a plot Arc's field as a plain line; a goal written as a line of his becomes `<plain goal> · motto: "<his line>"`. Quoted spans must be his words on the board (the old value counts). `set-step-text` also takes `marker: true` for a ruling marker (its prefix up to the first colon is kept; its quotes may come from its old text) |
| `replace-arc-words` | `arc` (label or id), `field` (goal / stakes / planned_outcome / outcome_detail / planned_change / opposition / conflict / span), `from`, `to`, `count`, `ruled` | 2026-10-22: `replace-words` for a plot Arc's own text fields — only on his explicit word naming the change; any other count refuses |
| `move-step` | `step` (^id), `dir` (-1 up, 1 down) | 2026-10-22, on his word: a step one place up or down among its siblings, through the plugin's own Plot-tab move (`moveStep` / `movePlotStep`), which renumbers the list; words untouched |
| `set-mark-label` | `card`, `line` (position, 0 = ENTRY), `label` ("" = the model's name back), optional `was` (its current label; a moved board refuses) | plugin 0.74+: a key beat placed on a line, renamed for this story ("Rituals on the Mountain") while it keeps its beat. Admin (CRE 2026-10-19); writes `plotMarks[line].label` only, never the beat. Refused unless the label shares a word with the line's text or the card's title, summary or full summary (drawn from his words), and on a line with no key beat |
| `set-line` | `card`, `line` (position, 0 = ENTRY), `text` | one chain line's words in place — its id, flavor, ending and the links to it stay (rewriting a whole chain with `set-chain` gives turns new ids and breaks the links of what was drilled from them) |
| `split-micro` | `card`, `pieces: [{text, type?}]` | breakdown: one micro-beat per beat it fires. The pieces, in order, re-joined with the whitespace between them, must read back as the card's words byte for byte, split at whitespace; a paragraph wrapped whole in `*…*` is split inside the markers and each piece re-wrapped. Never `dialogue` on a piece with no quote marks at all (0.71.3: its own marks anywhere are enough). Build the ops with `scripts/split_plan.mjs` |
| `link-from` | `card` (or `beat:<scene ref>:<n>`, the scene's n-th Beat, 0-based), `parent`, `lines: n` or `[a, b]` (positions in the parent's chain, 0 = ENTRY) | a child linked to the line, or run of lines, it carries (`plotFrom`). One line feeds one child; the child's ending is read from its run's last line, so put the ending there |
| `place-in-bloc` | `card` (a micro-beat), `line` (its beat's chain position) | only for a beat he has given a chain (a choreographed fight): the micro-beat into that slot through the plugin's own move. Not part of the default breakdown (chains stop at the Scene) |
| `regroup-beats` | `scene`, `groups: [{cards: [^id…], type?, title?, summary?}]` | administrative (2026-10-19): dissolves the scene's container Beats and wraps each run of micro-beats in a new Beat; the groups must cover every micro-beat once, in order |
| `set-title` / `set-summary` | `card`, `text` | a Beat, Scene or Sequence (never a prose card) |
| `set-chain` | `card`, `entry`, `turns: [{k: but/therefore, text, outcome?, detail?}]`, `exit: {k: ""/but/therefore, text, outcome?, detail?}` | replaces the card's turns; outcomes are the E3 labels |
| `remove-empty-card` | `card` (a Beat or Scene; `beat:<scene>:<n>` works) | on his word: a container with nothing under it and nothing linking to it comes off the board (2026-10-21: a Beat built from a stale DEV beat its neighbour carries). Refused if any card sits under it or points at it; undo restores it. Re-chain and re-link the scene after |
| `remove-break-card` | `card` | on his word: a card whose whole body is a break mark (`***`), nothing else on it; the Scenes around it export their own break |
| `remove-duplicate-idea` | `idea`, `twin` (both ^ids) | on his word (2026-10-22, "remove dulpicates - no clutter"): an idea card whose text is byte-identical (trimmed) to a twin idea in the same scene comes off; the twin keeps his words. Refused if the words differ at all, the two sit in different scenes, or the idea carries a card, tag or link the twin doesn't; undo restores it |
| `set-era-source` | `on` | on his word (plugin 0.64): the board's eras come from its scenes — a present scene's era carries forward, a flashback's applies to it only, and Books / Parts / Sequences show the rolled-up span (a sequence's own era is its planned start) |
| `set-flashback` | `card` (a scene), `on?` | a story call: on his word or an approved proposal |
| `set-remembers` | `card` (a micro-beat typed `memory`), `era` (`""` = not known) | the era a memory remembers — a broad bucket (Childhood, Teenage) for an unplotted memory, a season for one tied to a plotted event; the scene keeps its own era |
| `add-beat-type` | `name` | a micro-beat type added to the board's list (`memory`), on his word |
| `set-tag-mode` | `mode` (`never` / `first` / `every`) | on his word: how the export adds dialogue tags; `never` for prose written with its own tags (plugin 0.63; a new-board import starts there) |
| `set-plotting` | `on` | Statement Plotting on/off (his instruction) |
| `add-book-level` | `title?` | the plugin's "Add Book level…": every story card under the Project card moves into one new Book card, in order (text and export unchanged); once per board, on his word only (CRE 2026-10-23: series → books → parts) |
| `set-arc-role` | `cast`, `arc` (name or id), `role` (a model role, or `null` to clear), `set?` (a spine set key), `against?` | the model role an arc he already has carries (0.65.1). Only on his word or his ruling: which of his arcs is which spine is a story call. On a copy build, an arc holding a role in a set blocks that set's template arc (the builder holds the beats), so clearing or moving the role is how his ruling lands |
| `add-lead` | `cast` | POV roster |
| `set-lead-exit` | `cast`, `unit` (a Scene-level card, or a Sequence/Part/Book; `""` = stays) | on a container (plugin 0.62.2+) the exit reads at its last scene, named in the `made:` line; a container with no scene yet is stored and reported NOT DONE (reads "stays to the end" until one is added) |
| `add-event` | `type`, `who` (name or list), `era` (name, id or exact label), `parents?`, `at?` (the card it happens on), `name?`, `until?` (era) | on CRE's word only (schema §5e/§5i): "Wren is born in 1985" → `{"op": "add-event", "type": "born", "who": "Wren", "era": "1985"}`. Type must be on the board (born, died, married, separated, built, destroyed, or his own); era must exist (add it only on his word); subjects match the type's count and kind; parents only on born; `at` needs a card in an era, and the same era if both are given. Everything is checked before anything is written |
| `pin-event` | `event` (evt-id, or its exact label), `on` (the card it happens on) | world walk (2026-10-22): an existing event pinned through the plugin's `pinEvent` — a story call, on his ruling. Pinning makes the event's era the card's era: a card in another era is refused unless the ruling says the era moves (`moveEra: true`) |
| `unpin-event` | `event` (evt-id) | the pin comes off; the event stays in its era |
| `mark-working-copy` | `source` | frontmatter: the drafts stay the authority until the replacement review |

Never available, by design: body text on any card, `plotChain` / `plotMarks` / `plotComplete` / `convo` / `vis`, moving a
step between arc levels, deleting a key, renaming or removing a board, Book/Part level insertion (a Project-settings change
the plugin owns), world kinds, new event types (an event of an existing type is `add-event`).

Other commands: `read <board> [--full]` (the board as JSON: counts, cast, eras, relations, world, inbox, placed ideas, arc
steps, containers, plotting/model, this skill's runs) · `undo <board> [--run id] [--force]` · `redo <board>` · `log <board>` ·
`import --source <note> --board <new>` / `import --book <project dir> --board <new>` · `propose <board> [--out f.json]` ·
`suggest-tags <board> [--out f.json]` · `check [--board]` · `calibrate` · `normalize <board>` (a hand-edited file that does
not round-trip: a logged whole-file run, only when `apply` refuses for that reason and CRE agrees).
