# The ops file — every board write

`node scripts/board_tool.mjs apply <ops.json> [--dry]`. One file per run; one run per instruction batch (one undo step).

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
| `add-world` | `kind` (place/item/faction/religion/polity/magic/role/own), `name`, `aliases?`, `fields?` | never invented |
| `set-world` | `entry`, `field`, `value` | |
| `add-idea` | `text` (verbatim) or `from: {source, block \| quote}`, `type?` (from the board's ideaTypes), `tags?`, `by?`, `on?` | tags default by: ai; `by: "cre"` only for a `#tag` he typed. `from` takes the words from a file — the n-th block (the plugin's block split, frontmatter skipped) or a `quote` that must occur in it word for word — so his words are never retyped; `on` places the new idea on a card in the same op (a card made earlier in the run, by title or `beat:<scene>:<n>`) |
| `place-prose` | `under` (a Beat or Scene), `source` (file), `blocks: [a, b]`, `skip?: [n…]` | his prose from a source file as micro-beats appended under the container, block for block; the ops name the file and range, never the words; `skip` leaves a heading line or `***` break off (named in the change list); the run logs the file's hash and re-checks it before writing (2026-10-20, the Witchwood board build) |
| `place-idea` | `idea` (^id), `on` (card, or a placed arc step: the card it sits on) | approved placement → the card's tray; refused on a step that isn't on a card yet |
| `place-on-line` | `step` (^id), `via` (the Beat that carries it, or a micro-beat under it) — or `on` + `line` (0 = ENTRY) | CRE 2026-10-21: arc steps sit at line level — the step goes on the scene chain line its Beat is linked to (the first line of a run), through the plugin's `putFloatOnLine` (`plotLine`), moving it to that scene first if it sits elsewhere; a step on a line is drawn as a beat, not a Need. Build the ops from the plan's citations with `scripts/step_lines.mjs` |
| `add-plot-arc` | `label`, `goalHolder?` (cast), `fields?` (goal, stakes, opposition, conflict, planned_outcome, outcome_detail, planned_change, span, action_type) | a subplot (CRE 2026-10-21): a plot Arc (§5q `plotArcs`) with **no model role** — only the external spine carries one. Label and fields in his words; a working label he rules is marked as such in the plan |
| `add-plot-step` | `arc` (label or id), `label`, `text` or `from: {source, quote}`, then `via` (its Beat's line) / `parts: [{text, via}]` (sub-steps, one per scene) / neither + `unplaced` (the reason it waits) | a subplot step (an arcbeat with `plotArc`) placed by the same rules as the spines' steps: line-level by citation, sub-steps when it spans scenes; refused on an arc that carries a model role. Build the ops from the plan with `scripts/subplot_build.mjs` |
| `split-step` | `step` (^id), `parts: [{text, via}]` (≥ 2; `via` = the Beat that carries that piece), `unplace?` | CRE 2026-10-21 ("yes, sub steps"): a step whose plan cell cites more than one scene becomes a parent with one sub-step per cited scene, through the plugin's own sub-step mechanism (`addSubStep` / `addPlotArcStep` + `parentStep`). Each part's `text` must be a verbatim span of the step's own words, in order — his clause for that piece, never new wording; each sub-step goes on its Beat's line. With `unplace` the parent comes off the board and lives in the Characters panel as a category (its checklist shows each landed sub-step). A cell whose clauses don't split cleanly by its citations goes to his ruling list instead |
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
| `replace-arc-words` | `arc` (label or id), `field` (goal / stakes / planned_outcome / outcome_detail / planned_change / opposition / conflict / span), `from`, `to`, `count`, `ruled` | 2026-10-22: `replace-words` for a plot Arc's own text fields — only on his explicit word naming the change; any other count refuses |
| `move-step` | `step` (^id), `dir` (-1 up, 1 down) | 2026-10-22, on his word: a step one place up or down among its siblings, through the plugin's own Plot-tab move (`moveStep` / `movePlotStep`), which renumbers the list; words untouched |
| `set-line` | `card`, `line` (position, 0 = ENTRY), `text` | one chain line's words in place — its id, flavor, ending and the links to it stay (rewriting a whole chain with `set-chain` gives turns new ids and breaks the links of what was drilled from them) |
| `split-micro` | `card`, `pieces: [{text, type?}]` | breakdown: one micro-beat per beat it fires. The pieces, in order, re-joined with the whitespace between them, must read back as the card's words byte for byte, split at whitespace; a paragraph wrapped whole in `*…*` is split inside the markers and each piece re-wrapped. Never `dialogue` on a piece without an opening quote. Build the ops with `scripts/split_plan.mjs` |
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
| `set-arc-role` | `cast`, `arc` (name or id), `role` (a model role, or `null` to clear), `set?` (a spine set key), `against?` | the model role an arc he already has carries (0.65.1). Only on his word or his ruling: which of his arcs is which spine is a story call. On a copy build, an arc holding a role in a set blocks that set's template arc (the builder holds the beats), so clearing or moving the role is how his ruling lands |
| `add-lead` | `cast` | POV roster |
| `set-lead-exit` | `cast`, `unit` (a Scene-level card, or a Sequence/Part/Book; `""` = stays) | on a container (plugin 0.62.2+) the exit reads at its last scene, named in the `made:` line; a container with no scene yet is stored and reported NOT DONE (reads "stays to the end" until one is added) |
| `add-event` | `type`, `who` (name or list), `era` (name, id or exact label), `parents?`, `at?` (the card it happens on), `name?`, `until?` (era) | on CRE's word only (schema §5e/§5i): "Wren is born in 1985" → `{"op": "add-event", "type": "born", "who": "Wren", "era": "1985"}`. Type must be on the board (born, died, married, separated, built, destroyed, or his own); era must exist (add it only on his word); subjects match the type's count and kind; parents only on born; `at` needs a card in an era, and the same era if both are given. Everything is checked before anything is written |
| `mark-working-copy` | `source` | frontmatter: the drafts stay the authority until the replacement review |

Never available, by design: body text on any card, `plotChain` / `plotMarks` / `plotComplete` / `convo` / `vis`, moving a
step between arc levels, deleting a key, renaming or removing a board, Book/Part level insertion (a Project-settings change
the plugin owns), world kinds, new event types (an event of an existing type is `add-event`).

Other commands: `read <board> [--full]` (the board as JSON: counts, cast, eras, relations, world, inbox, placed ideas, arc
steps, containers, plotting/model, this skill's runs) · `undo <board> [--run id] [--force]` · `redo <board>` · `log <board>` ·
`import --source <note> --board <new>` / `import --book <project dir> --board <new>` · `propose <board> [--out f.json]` ·
`suggest-tags <board> [--out f.json]` · `check [--board]` · `calibrate` · `normalize <board>` (a hand-edited file that does
not round-trip: a logged whole-file run, only when `apply` refuses for that reason and CRE agrees).
