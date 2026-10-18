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

References: a card by `^id` or `title:Exact title` (containers only; unique); cast, world entries, eras and relation types by
name (any case; aliases resolve). Values are CRE's words. `--dry` shows the change list and writes nothing.

| op | fields | notes |
|---|---|---|
| `add-cast` | `name`, `aliases?`, `profile?: {field: value}` | refuses a name already in the cast |
| `set-cast` | `cast`, `field`, `value` | a profile answer (`""` clears) |
| `add-era` | `name`, `label?`, `parent?` (era name), `history?` | eras are story-level; a lone era is not the story's start (BW U13) |
| `set-era` | `card`, `era` (name; `""` clears) | on a Sequence it carries forward; deeper, that subtree only |
| `file-beats-in-era` | `era` | every unplaced arc step without an era gets this one (bible setup) |
| `add-relation-type` | `name`, `inverse?`, `forWorld?` | only on CRE's word |
| `add-relation` | `type`, `a`, `b`, `from?`, `to?`, `note?` | "a is type of b"; the type must be on the board |
| `add-world` | `kind` (place/item/faction/religion/polity/magic/role/own), `name`, `aliases?`, `fields?` | never invented |
| `set-world` | `entry`, `field`, `value` | |
| `add-idea` | `text` (verbatim), `type?` (from the board's ideaTypes), `tags?`, `by?` | tags default by: ai; `by: "cre"` only for a `#tag` he typed |
| `place-idea` | `idea` (^id), `on` (card, or a placed arc step: the card it sits on) | approved placement → the card's tray; refused on a step that isn't on a card yet |
| `unplace-idea` | `idea` | back to the inbox |
| `add-tag` / `remove-tag` | `card`, `tag` | always by: ai; a cre tag is never removed |
| `add-link` / `remove-link` | `card`, `to` (`^id`, a title, or `[[File#^id]]`), `rel?` | always by: ai |
| `set-field` | `card`, `field`, `value` | structural fields only: chapter, pov, setting, time, job, question…; never summary, goal, outcome, statements (offer them) |
| `set-type` | `card`, `type`, `speaker?` | a direct instruction ("these are dialogue, Mara speaks"); inferred types are offers |
| `add-card` | `kind` (a container level), `under` or `after`, `title?`, `fields?` | Book, Part, Sequence, Scene, Beat containers by his title; never a prose card |
| `wrap` | `cards: [^id…]`, `kind`, `title?`, `fields?` | a container around sibling cards (import: a Scene around a run) |
| `offer` | `card`, `offer: {type?, speaker?, summary?, wants?, states?, chain?}` | tagging mode: written under the marker key `ai` (by: ai, dated), never into his fields |
| `offer-intensity` | `card`, `emotional?: [start, end]`, `physical?: [start, end]`, `rubric?`, `note?` | §6a: to the sidecar `<board>.measure.json`, never a marker |
| `set-plotting` | `on` | Statement Plotting on/off (his instruction) |
| `add-lead` | `cast` | POV roster |
| `set-lead-exit` | `cast`, `unit` (a Scene-level card; `""` = stays) | refused on a Sequence: the plugin honours exits on units only |
| `mark-working-copy` | `source` | frontmatter: the drafts stay the authority until the replacement review |

Never available, by design: body text on any card, `plotChain` / `plotMarks` / `plotComplete` / `convo` / `vis`, moving a
step between arc levels, deleting a key, renaming or removing a board, Book/Part level insertion (a Project-settings change
the plugin owns), world kinds, events (no op yet: name it as NOT DONE and route it to `_BACKLOG`).

Other commands: `read <board> [--full]` (the board as JSON: counts, cast, eras, relations, world, inbox, placed ideas, arc
steps, containers, plotting/model, this skill's runs) · `undo <board> [--run id] [--force]` · `redo <board>` · `log <board>` ·
`import --source <note> --board <new>` / `import --book <project dir> --board <new>` · `propose <board> [--out f.json]` ·
`suggest-tags <board> [--out f.json]` · `check [--board]` · `calibrate` · `normalize <board>` (a hand-edited file that does
not round-trip: a logged whole-file run, only when `apply` refuses for that reason and CRE agrees).
