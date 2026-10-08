---
type: schema
title: Branch Writing card marker schema
schema_version: 1
plugin: branch-writing
plugin_version: 0.9.0
created: '2026-10-07'
last_updated: '2026-10-08'
---

# Branch Writing — card marker schema, v1

This is the contract for anything that reads or writes a Branch Writing board with plain file tools. That includes the plugin, the future AI tagger, dev-edit's network walk, and scene-intensity. A board is **one ordinary Markdown file**. The plugin needs nothing beyond what is written here.

## 1. A card in the file

```
%%bw {"v":1,"kind":"beat","depth":3,"type":"dialogue","speaker":"Mara"}%% ^k3x9a2

The card body: plain Markdown, exactly as written.

%%/bw%%
```

- **Begin marker:** a line that starts with `%%bw `, then one JSON object, then `%%`, then a space and the card's **block ID** (`^k3x9a2`). It is one line. The JSON never contains a `%` character, because writers escape it as `%`. That means the first `%%` after `%%bw ` always closes the marker.
- **Body:** everything between the begin-marker line and the end-marker line. Writers put one blank line on each side of the body. Readers strip one leading blank line and any trailing blank lines.
- **End marker:** a line that is exactly `%%/bw%%`.
- One blank line separates cards. The file ends with a newline.
- **Preamble:** anything before the first begin marker (frontmatter, for example) belongs to no card and is kept byte-for-byte.

**Why `%%`:** checked live in Obsidian 1.14.4 on 2026-10-07. Obsidian comments are hidden in reading view and collapse to zero height. They keep the trailing `^id` as a real block ID, and wikilinks inside them land in Obsidian's link index and graph. HTML comments (`<!-- -->`) fail on the last two counts: no block ID and no link indexing.

## 2. Order and tree

- Cards appear in **story order**. This is pre-order: a card, then everything under it, then its next sibling. Reading the file top to bottom reads the story.
- `depth` builds the tree. The Project card is 0, its children are 1, and so on. A card's parent is the nearest card above it with a smaller depth.
- If a hand edit jumps depth (for example 1 → 3), the card is treated as a child of the card above it. The plugin rewrites the corrected depth only when it next edits that card.
- A move always moves a card together with every card under it, as one contiguous block.

## 3. Card ID

- The ID is the Obsidian block ID after the marker (`^k3x9a2`): letters, digits and `-`, unique within the file. The plugin generates six lowercase base-36 characters. Any valid block ID works.
- The ID is **not** repeated inside the JSON.
- Link to a card with Obsidian's own syntax: `[[File name#^k3x9a2]]`, or `[[#^k3x9a2]]` within the same file. These links resolve in Obsidian, show in the graph and backlinks, and survive file renames, because Obsidian's link updater rewrites them.
- A marker without an ID gets one the next time the plugin writes that card.

## 4. Marker fields (v1)

| Field | Type | Meaning |
|---|---|---|
| `v` | integer | Schema version. Currently `1`. |
| `kind` | string | A **level key** from the project's `levels` (default `project`, `sequence`, `scene`, `beat`, `micro`), a **custom type key** from `customTypes` (e.g. `flashback`), or a non-structural kind: `note`, `side` (side-note), `variant`, `research`. The last level in `levels` is the prose level; every level above it is a container. In the default template `beat` is a container (type + summary) and `micro` (Micro-beat) holds the prose. Boards made with plugin 0.1 use four levels with `beat` as the prose level; their Project card says so and they keep working. |
| `depth` | integer ≥ 0 | Tree depth (section 2). |
| `type` | string | The card's type, from its level's list: `levels[].types` for container levels (default Beat: `conversation`, `action`), `beatTypes` for the prose level (default `action`, `reaction`, `dialogue`, `interiority`, `description`). Any string is kept. |
| `speaker` | string | Who speaks a `dialogue` card. Used by dialogue export and by `char:` walks. |
| `color` | string | A swatch `id` from the project's `swatches`. Present only when the card was coloured **by hand**; type colours are defaults looked up from settings (§5), never stamped onto cards. |
| `tags` | array of objects | `{"tag":"thread:river","by":"cre"}`. `tag` is free-form. Starter prefixes: `thread:`, `char:`, `seed:`, `payoff:`. `by` is `"cre"` (set by hand in the plugin) or `"ai"` (set by an AI pass). A bare string entry is read as `{"tag":…,"by":"cre"}`. |
| `links` | array of objects | `{"to":"[[File#^id]]","by":"ai","rel":"echoes"}`. `to` is an Obsidian block link. `by` works as in `tags`. `rel` (the relation label) is optional and free-form. |
| `fields` | object | Structural fields, keyed by the names in that level's `fields` template, for example `{"summary":"Bob talks to Steve about the party.","chapter":"18","pov":"Mara"}`. `summary` is the one-sentence line shown under a container's title. Values are strings when set by the plugin. Other value types are kept but are read-only in the plugin. A value whose name is no longer in the template is kept, never deleted. |
| `of` | string | On a `variant`: the ID of the card it is an alternative to. |
| `settings` | object | **Project card only.** The project's settings (section 5). |

**Unknown fields are preserved untouched.** That applies at the top level of the marker, inside `fields`, inside `settings`, and inside each tag or link object. A writer that adds a field must keep every key it doesn't own. The plugin only rewrites a marker it is changing. It keeps existing key order and appends new keys. A marker whose JSON doesn't parse is never rewritten: the plugin flags the card and refuses to edit that card's metadata or move it until the JSON is fixed by hand.

**Rule for AI writers:** set `"by":"ai"` on every tag and link you add. Never change or remove an entry whose `by` is `"cre"`. Never touch a card body.

## 5. Project card settings (`settings`)

The first card, `kind: "project"`, depth 0, holds the project's settings so they travel with the file. Any missing key falls back to the default shown here.

```json
{
  "levels": [
    {"key":"project","name":"Project","fields":[],"export":"nothing","heading":1},
    {"key":"sequence","name":"Sequence","fields":[{"name":"summary","desc":"One sentence: what happens here.","onCard":true},{"name":"intensity start","onCard":true},{"name":"intensity end","onCard":true},{"name":"physical start","onCard":true},{"name":"physical end","onCard":true},{"name":"job"},{"name":"question"}],"export":"nothing","heading":2,"color":"heather"},
    {"key":"scene","name":"Scene","fields":[{"name":"summary","desc":"One sentence: what happens here.","onCard":true},{"name":"intensity start","onCard":true},{"name":"intensity end","onCard":true},{"name":"physical start","onCard":true},{"name":"physical end","onCard":true},{"name":"chapter"},{"name":"pov","asTag":true},{"name":"setting","asTag":true},{"name":"time"},{"name":"goal"},{"name":"turn"},{"name":"outcome"}],"export":"break","heading":3,"color":"tide"},
    {"key":"beat","name":"Beat","fields":[{"name":"summary","desc":"One sentence: what happens here.","onCard":true}],"types":["conversation","action"],"export":"nothing","heading":4,"color":"sage"},
    {"key":"micro","name":"Micro-beat","fields":[],"export":"prose"}
  ],
  "beatTypes": ["action","reaction","dialogue","interiority","description"],
  "customTypes": [{"key":"character","name":"Character","like":"side","color":"rose","fields":[{"name":"char","desc":"Name","onCard":true,"asTag":true},{"name":"role","desc":"protagonist / main / supporting / antagonist","onCard":true,"asTag":true,"carry":true,"options":["protagonist","main","supporting","antagonist"]},{"name":"flaw","desc":"Internal flaw","carry":true},{"name":"challenge","desc":"Scene-level challenge"},{"name":"coping","desc":"Coping mechanism / behavior","carry":true},{"name":"resistance","desc":"Resistance to change (0–10)","onCard":true,"scale":true,"min":0,"max":10,"carry":true},{"name":"entry state","onCard":true},{"name":"exit state","onCard":true}],"arc":{"key":"char","scale":"resistance","entry":"entry state","exit":"exit state","role":"role"}}],
  "kindColors": {"side":"stone","note":"stone","research":"stone","variant":"wheat"},
  "typeColors": {"action":"rust","reaction":"amber","dialogue":"tide","interiority":"heather","description":"sage"},
  "colorByType": false,
  "tagPrefixes": ["thread:","char:","seed:","payoff:","item:"],
  "intensity": {"min":-10,"max":10,"start":"intensity start","end":"intensity end","splitBy":"pov","step":4,"levels":{"outer":"sequence","inner":"scene"},"phys":{"start":"physical start","end":"physical end","min":0,"max":10},"markers":{"flat":true,"cross":true,"step":true,"against":true,"high":true,"low":true,"mismatch":true,"both":true,"diverge":true}},
  "dialogue": {"tag":"{speaker} said.","mode":"first","quotes":"curly"},
  "swatches": [{"id":"ember","name":"Ember","color":"#D08A7A"}, "… 12 Lamplight swatches …"],
  "export": {"chapterHeading":"# Chapter {chapter}","sceneBreak":"* * *"},
  "layout": {"cardWidth":340,"spacing":10,"tagsOnCard":false}
}
```

- `levels[].fields` is the level's field template, in display order. Each entry is `{"name", "desc"?, "onCard"?}`:
  - `desc` is a one-line meaning, shown as the input hint and on hover.
  - `onCard: true` shows the field on the collapsed card. Other fields appear only when the card is expanded or being edited.
  - A plain string entry (the 0.1 format) is read as `{"name": …}`.
- `levels[].types` is the type list for a container level. The prose level uses `beatTypes`.
- `levels[].color`: the default swatch for every card of that level.
- `kindColors`: default swatches for the built-in side kinds, e.g. `{"side":"stone","note":"stone","research":"stone","variant":"wheat"}`.
- `colorByType` and `typeColors`: when `colorByType` is true, prose-level cards take the swatch mapped to their `type` (default map action → rust, reaction → amber, dialogue → tide, interiority → heather, description → sage).
- **Colour a card shows**, first match wins: its own `color` → its type's colour (prose level, only when `colorByType` is on) → its card type's colour (`levels[].color`, `customTypes[].color` or `kindColors`) → none. Changing a type colour therefore recolours every card of that type that wasn't coloured by hand.
- `intensity`: the intensity graph's settings.
  - Values live in ordinary `fields` named by `start` and `end` (default `"intensity start"`, `"intensity end"`), as signed numbers from `min` to `max`. Default −10 to +10: 0 is neutral, + is positive charge, − is negative, and the size is the intensity. Stored as strings like `"-3"` (a JSON number is also read); out-of-range values clamp, and `−` is read as minus.
  - `levels.outer` / `levels.inner` name the two plotted levels (custom types acting like them count).
  - **Two lanes.** `start`/`end` are the **emotional** lane: signed `min`…`max`, default −10…+10. `phys.start`/`phys.end` are the **physical** lane: unsigned `phys.min`…`phys.max`, default 0…10 (calm → violent), fields `"physical start"` / `"physical end"`. Each lane is optional per card and independent. Physical values outside the range clamp; a negative physical value reads as 0.
  - Lane markers:
    - `both`: emotional and physical each rise ≥ 2 within the card.
    - `diverge`: one lane moves ≥ `step` while the other moves ≤ 1.
    - `flat` ("no change") fires only when neither lane with values moves.
    - The physical peak is a `high` marker in the physical lane.
    - `against` and `mismatch` read the emotional lane.
  - `splitBy` names the field whose values give one line each in the inner view (default `pov`). Values are compared case- and space-insensitively.
  - `step` is the jump size that gets a marker; `markers` switches each marker kind.
  - The graph and all its markers (no change, crosses neutral, big step, against its sequence, sequence ≠ its scenes, highest, lowest) are computed for display only and never written. Field renames in the plugin keep `start`/`end` pointing at the renamed fields.
- `levels[].fields[]` / `customTypes[].fields[]` options:
  - `scale: true` (+ `min`, `max`, default 0…10): a number set with a click strip. Stored as a string like `"7"`; out-of-range values clamp.
  - `carry: true`: when a card of a tracker or arc type is filled in, an empty field takes the **most recent value set** for the same key (same character / thing) on an earlier card of that type. A card that left it blank doesn't erase it. Never overwrites a value.
  - `options`: suggested values offered while typing, alongside values already on the board.
- `customTypes[].arc`: `{"key","scale"?,"entry"?,"exit"?,"role"?}` makes the type an **arc type**. `role` names a field (default `role`) whose latest value per character is shown as a badge. The Arc panel can filter by it and orders characters by the role field's `options` order (protagonist → main → supporting → antagonist), then any other roles. `key` names the field that says who (default `char`, which with `asTag` also answers as `char:<name>`), `scale` the plotted field, and `entry`/`exit` the state fields.
  - A new card's empty entry state is filled from that character's previous card's exit state.
  - The **Arc panel** groups cards by key (case-insensitive) in story order on a shared scene axis. It shows entry → exit for each card, the exit → next entry gap between cards, and the scale as one line per character.
  - Observations only: missing entry or exit state, and the scale moving against that character's overall trend.
  - The default template includes **Character** (2026-10-08). Boards made earlier keep their own setup; use Import from… to add it.
- `tagPrefixes`: quick-add prefixes in the Tags dialog, and the order the tag filter groups by. Any prefix is valid in `tags`; these are just offered.
- `levels[].fields[].asTag`: the field's value also answers as the tag `<field>:<value>` (e.g. `setting:the house`) for filtering and walking. **Derived, never written to `tags`.**
- **Derived tags.** These are computed and never stored, and they compare case- and space-insensitively:
  - a dialogue card's `speaker` → `char:<speaker>`
  - an `asTag` field → `<field>:<value>`
  - a tracker card's thing → `<tracks field>:<value>`

  A card's **own** tags (stored plus derived) are the walk's stops. The filter also counts tags **inherited** from the `asTag` fields of cards above it (a scene's setting lights its beats), and things tracked by tracker cards directly under it (the beat where the sword is spent).
- `customTypes`: CRE's own card types, each `{"key","name","like","fields"?,"types"?,"color"?,"export"?,"heading"?}`.
  - `like` is a level key or `"side"`. A level-like type sits at that level's place in the tree: same children, same nesting rules, in rollups, exported with the main line, with `export`/`heading` overriding the level's when present. A heading export with no card title uses the type name ("Interlude").
  - A `"side"` type attaches anywhere and never exports, like a side-note.
  - `types` empty means "use the level's list".
  - `key` is set once from the name ("Flashback" → `flashback`) and never changes.
  - **Tracker types:** `tracks` names the field holding the tracked thing (e.g. `"item"`), `holder` the field naming who has it after the event, and `effects` maps each change (the card's `type`) to `gain`, `lose`, `transfer` (to the holder), `use` or `none`. Starter set: gained → gain, lost → lose, spent → lose, given → transfer, used → use. `types` mirrors the keys of `effects`.
    - The **Ledger** groups each type's cards by thing (case-insensitive) in story order and replays the effects. It ends on held / not held and the holder.
    - Its observations are never verdicts: lose or transfer with nothing held, gain while already held (by the same holder), use while not held, use by someone other than the holder, no change set.
    - Example event: `{"kind":"item","type":"spent","fields":{"item":"Sword","holder":"Bram"}}`, placed as a child of the card where it happens.
  - Removing a type in the plugin converts its cards to the level it acted like (a side type becomes `note`) after a confirm. A card whose kind is unknown to the settings is exported as prose, so nothing is dropped.
- `levels[].export`: `heading` (uses the first line of the card body as the heading text, at `heading` level), `break` (a scene break between that level's cards), or `nothing`. The last level is always `prose`. Summaries and other fields never export.
- `dialogue.mode`: `first` means tag the first line of an exchange, then tag again only when the speaker changes after a break. Every container card (including a Beat) starts a fresh exchange. `every` tags every line. `never` adds no tags.
- `layout.tagsOnCard`: `false` shows a collapsed card's tags and links as a count (e.g. "3 tags").
- The starter fields are CRE's own examples from the intent (sequence: job, question; scene: POV, setting, time, goal, turn, outcome), plus `chapter` and a `summary` on every container. Earlier starters (seal, register, weight and the StoryLine names) were dropped 2026-10-08 as not CRE's vocabulary.
- Renaming a field in Project settings moves existing values to the new name on every card of that level, after asking. A card that already holds a value under the new name keeps both.
- Expanded/collapsed state is view-only and never written to the file.

### Templates

A **template** is an ordinary board file containing only a Project card, kept in the plugin's templates folder (plugin-wide setting; default `WRITING/BOARD TEMPLATES/`, created on first save). Its title is the card body. Its setup is the card's `settings`.
- A new board from a template gets a **copy** of those `settings`, with an empty title and a new ID. Boards never link back to their template.
- "Import from…" merges chosen parts of another board's or template's `settings` into this board's Project card. It is additive:
  - Custom types are added by `key`, and replace an existing one only when explicitly ticked. A type whose `like` level this board lacks is skipped.
  - Fields are only added to levels this board already has.
  - Colours and tag prefixes merge.
  - Dialogue, export, intensity, layout and swatches are replaced only when ticked.
  - Unknown keys survive.

## 6. Derived values (never stored)

Word counts, beat-type mix, threads touched, section numbers (1.2.4), soft nesting warnings, and seed-check statuses are all computed when displayed. **Never write a rollup into a marker.** A stored count goes stale the moment a beat changes.

- **Rollup:** words and prose-card count under a container, the prose type mix, threads touched, and the list of its direct container children with their types (e.g. a scene's beats: conversation, action).
- **Main line:** every card except custom side types (`like: "side"`) and `note` / `side` / `variant` / `research` cards and everything under them.
- **Chapter:** a card's chapter is the nearest `fields.chapter` on itself or an ancestor.
- **Seed check:** pairs `seed:NAME` and `payoff:NAME` tags by NAME (case-insensitive), in story order.
  - `paid`: a payoff comes after the first seed.
  - `open`: a seed with no payoff.
  - `backwards`: every payoff comes before the first seed.
  - `orphan`: a payoff with no seed.
- **Thread walk:** the cards carrying a tag, in story order. A `char:NAME` walk also includes `dialogue` cards whose `speaker` matches NAME.

## 7. Clean export rules

Export covers the main line only, with no markers, no block IDs, no `%%` comments and no structural fields.

- Each structural level renders as set in `export`. A chapter heading (`export.chapterHeading`) starts wherever a card's `fields.chapter` value changes.
- Dialogue cards hold only the line. Export adds `dialogue.quotes`-style quote marks, unless the line already opens with a quote. It adds the tag from `dialogue.tag` per `dialogue.mode`, and joins them with a comma: a final `.` becomes `,`; `?`, `!`, `—` and `…` are kept.
- A quoted line with text after its closing quote is treated as CRE's own tag and exported as written.
- Nothing else in a body is changed.

## 8. Reading a board without the plugin (Python sketch)

```python
import json, re
BEGIN = re.compile(r'^%%bw[ \t]([\s\S]*?)%%[ \t]*(?:\^([A-Za-z0-9-]+))?[ \t]*$', re.M)
def cards(text):
    ms = list(BEGIN.finditer(text))
    for i, m in enumerate(ms):
        end = ms[i+1].start() if i+1 < len(ms) else len(text)
        seg = text[m.end():end]
        body = re.split(r'^%%/bw%%[ \t]*$', seg, maxsplit=1, flags=re.M)[0].strip('\n')
        yield m.group(2), json.loads(m.group(1)), body
```

When writing, replace only the marker line of the card you change. Re-serialize its JSON with `%` escaped as `%`, and keep everything else byte-for-byte.

## 9. Versioning

`v` increments only for a breaking change to sections 1–4. Adding a new optional field is not a breaking change: readers ignore what they don't know, and writers keep it.
