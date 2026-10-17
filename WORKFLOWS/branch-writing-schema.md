---
type: schema
title: Branch Writing card marker schema
schema_version: 1
plugin: branch-writing
plugin_version: 0.56.0
created: '2026-10-07'
last_updated: '2026-10-17'
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
| `kind` | string | A **level key** from the project's `levels` (default `project`, `sequence`, `scene`, `beat`, `micro`), a **custom type key** from `customTypes` (e.g. `flashback`), or a non-structural kind: `note`, `side` (side-note), `variant`, `research`, `idea` (§5a), `cast` (§5b), `arcbeat` (§5c), `world` (§5h). The last level in `levels` is the prose level; every level above it is a container. In the default template `beat` is a container (type + summary) and `micro` (Micro-beat) holds the prose. Boards made with plugin 0.1 use four levels with `beat` as the prose level; their Project card says so and they keep working. |
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

**Rule for AI writers (CRE ruling 2026-10-17).** Branch Writing is an administrative tool. An AI writer may **build structure from a plan CRE approved**: cast cards, arcs and arc steps, plot arcs and their steps, beats, links, the containers the plan names (Book, Part, Sequence, Scene cards, by title), placements, and the model and plotting settings the plan holds. It builds **only onto a new board or a copy, never a board CRE is working in.** Every value it writes is CRE's words from that plan. Whatever the plan leaves open stays blank: a step keeps its template label and an empty body. It never writes prose (a prose-level body, a conversation, subtext). It never makes a story decision the plan doesn't hold. It never sets what the sections below keep as CRE's own: key-beat and line marks, the Complete mark, chain lines, the idea inbox. Outside a build: set `"by":"ai"` on every tag and link you add, never change or remove an entry whose `by` is `"cre"`, and never touch a card body.

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
  "kindColors": {"side":"stone","note":"stone","research":"stone","variant":"wheat","idea":"amber"},
  "ideaTypes": ["dialogue","beat","scene","twist","image","question"],
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
- `ideaTypes`: the type list for `idea` cards (the Idea panel's sort chips). Missing on older boards → the default list.
- `tagPrefixes`: quick-add prefixes in the Tags dialog, and the order the tag filter groups by. Any prefix is valid in `tags`; these are just offered.
- `levels[].fields[].asTag`: the field's value also answers as the tag `<field>:<value>` (e.g. `setting:the house`) for filtering and walking. **Derived, never written to `tags`.**
- `levels[].optional` (0.32): the level may be skipped — a card may sit directly under the level above it with no nesting warning (Book and Part also count as optional by key; §5l).
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
    - **The default template includes an Item tracker (plugin 0.31):** `{"key":"item","name":"Item","like":"side","color":"wheat","tracks":"item","holder":"holder","types":["gained","lost","spent","given","used"],"effects":{"gained":"gain","lost":"lose","spent":"lose","given":"transfer","used":"use"},"fields":[{"name":"item","desc":"What is tracked","onCard":true},{"name":"holder","desc":"Who has it after this","onCard":true,"cast":true,"who":"any"}]}`. Boards made earlier keep their own setup; the Items tab offers **Add the Item tracker type** (it appends this type to the stored `customTypes`, touching nothing else), or use Import from…. A holder field created by "Tracks a thing" carries `cast: true, who: "any"` (0.31), so it is picked from the cast and the world on the card as in the panel.
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

## 5a. Ideas (plugin 0.10, 2026-10-10)

An **idea** is a card with `kind: "idea"`, kept in the board's own file (one inbox per board, CRE-ruled 2026-10-10). Body = the idea text; `type` from `ideaTypes`; `tags` as on any card.

```
%%bw {"v":1,"kind":"idea","depth":1,"type":"twist","tags":[{"tag":"seed:knife","by":"cre"}]}%% ^k8d2qa

The knife was hers all along.

%%/bw%%
```

- **Where it is decides its state — no extra field.** Directly under the Project card (or at depth 0 on a board without one) = **in the inbox**. As a child of any other card = **placed** on that card ("in the sequence, not yet in a scene"). Placing is an ordinary move; a placed idea stays with its card when cards are added under that card.
- **Never in the columns.** An idea with no children shows in the Idea panel (inbox) or in its card's idea tray (placed), never as a column card. An idea that has cards under it (only possible by hand) shows normally, so nothing is hidden.
- **Side kind:** never exports, not on the main line, not in rollups. Inbox ideas are skipped by the seed check, the walk and the toolbar tag list; placed ideas count in the seed check.
- **Becoming a card** ("Make it a…") changes `kind` to a level (or a custom type acting like one) in place: a container takes the text as `fields.summary` and an empty body; the prose level keeps the body. `type` is dropped unless the new kind's list has it. Tags carry over. Position: on the level above → stays put; on the same level → next sibling after that card; deeper → after the branch it was in; no parent of the right level → the plugin asks for one.
- A custom type with key `idea` (suggested as a side type in 0.3) is read as this built-in kind.
- **AI writers:** may add `by:"ai"` tags to ideas like any card; never create, move, retype or rewrite an idea — the inbox is CRE's.

## 5b. Cast and character profiles (plugin 0.11, 2026-10-10)

A **cast member** is a card with `kind: "cast"` directly under the Project card, one per character, never shown in the columns (the Character panel holds them), never exported, off the main line.

```
%%bw {"v":1,"kind":"cast","depth":1,"name":"Ashley Vane","aliases":["Ash"],"profile":[{"name":"role","options":["protagonist","main","supporting","antagonist"]},{"name":"flaw"},{"name":"personality","long":true}],"fields":{"role":"protagonist","flaw":"won't ask for help"}}%% ^c4st01

%%/bw%%
```

- `name` (string) and `aliases` (array of strings, "nicknames" in the panel) are fixed parts of a character, not profile fields.
- `profile`: **this character's own field list**, same shape as `levels[].fields` plus `long: true` (a bigger text box). Each character can differ. Missing → the starter list (role, tagline, want, need, flaw, wound, personality, voice, appearance, notes).
- `fields`: the answers, keyed by profile field name. A value whose field was removed from `profile` is kept until cleared.
- **Names resolve case- and space-insensitively across name + aliases.** A dialogue `speaker` typed in the plugin takes the cast's spelling of that name or nickname (a nickname stays a nickname, since export prints it). A Character card's who-field (`arc.key`) takes the full `name`.
- **Character card from a profile:** the new arc-type card (Character) gets `fields[arc.key] = name` plus every card-type field whose name matches a profile field (case-insensitive) with a value; carry-forward then fills the rest. Nothing is synced afterwards — the card is a scene snapshot.
- **Rename:** Character cards whose who-field equals the old full name follow; dialogue speakers equal to the old full name follow only when CRE chooses; nicknames are never rewritten.
- **Profile templates** are plain notes in `<templates folder>/Characters/` (default `WRITING/BOARD TEMPLATES/Characters/`), shared by every board: frontmatter `type: bw-profile-template` (a fixed literal), a readable field list, and a ```` ```json ```` block `{"v":1,"fields":[…]}` that the plugin reads. A template holds the **field shape only, never a character's answers**. They contain no `%%bw` marker, so they are never listed as board templates. "Apply template" adds missing fields to a character and removes nothing.
- The cast is planning that happens before the draft. It is separate from StoryLine's Codex and `REFERENCE/` canon, which derive from landed drafts. The plugin never reads or writes either.
- **AI writers:** may create cast cards (name, aliases, the profile answers in the plan) during a build (§4). Otherwise never create, edit or delete cast cards. Never create or edit profile templates.

## 5c. Arcs and arc steps (plugin 0.12, 2026-10-10)

A character's arcs live on its cast card: `arcs: [{"id":"arc-k2x9q","name":"Revenge","fields":[{"name":"lie believed"},{"name":"cost","long":true}]}]`. `fields` is the field list **every step of that arc** carries, shaped by CRE.

An **arc step** is a card with `kind: "arcbeat"` that floats like an idea (§5a): under the Project card = unplaced (shown only in the Character panel); under any other card = placed, shown in that card's tray.

```
%%bw {"v":1,"kind":"arcbeat","depth":3,"cast":"c4st01","arc":"arc-k2x9q","step":2,"label":"Vow","hint":"the promise they make","arcFields":{"lie believed":"I can do it alone"}}%% ^st3p02

Ash swears it at the river.

%%/bw%%
```

- `cast` = the cast card's block ID; `arc` = the arc's `id`; `step` = position in the arc (1…n, renumbered on every reorder/removal); `label` = the step name ("Vow"); `hint` = optional prompt from a template; body = this character's text for the step; `arcFields` = the step's values. These are kept out of `fields`, so they never collide with a level's fields.
- **Make it a…** works as for ideas (§5a). The card keeps `cast`/`arc`/`step`/`label`/`arcFields`, so the planner still shows "became Beat in …". A step with no text becomes its label.
- **Order observation (never a verdict):** a placed step that sits earlier in story order than a lower-numbered placed step is flagged "comes before step N in the story".
- **Removing an arc** removes its unplaced steps. Placed and converted ones stay as they are, with `cast`/`arc`/`step` cleared. Deleting a character removes its arcs the same way.
- **Arc templates** are notes in `<templates folder>/Arcs/` (default `WRITING/BOARD TEMPLATES/Arcs/`): frontmatter `type: bw-arc-template` (fixed literal), a readable list, and ```` ```json ```` `{"v":1,"fields":[…],"steps":[{"label","hint"?}]}`. They hold the **structure only** (step labels, hints and the step field list), never a character's text or values. They are independent of character templates (§5b): a character takes a profile template and any number of arcs from arc templates.
- **Sub-steps (plugin 0.13):** a step can be broken into smaller steps that get from its entry to its exit, to any depth. A sub-step is an ordinary `arcbeat` card with `parentStep` = its step's block ID, and its `step` numbers it among its siblings only. `arcSteps` lists top-level steps (no `parentStep`); numbering reads "2.1", "2.2.1". Sub-steps carry the arc's step fields and are placed, moved, unplaced and promoted independently of their step. **Observation:** a placed sub-step outside the card its parent step is on (or became) is flagged "outside Sequence: …, where step 2 is". Sibling story order is flagged as for steps. Deleting a step removes its unplaced sub-steps and unlinks placed ones (`cast`/`arc`/`step`/`parentStep` cleared). Arc templates nest: `{"label","hint"?,"steps"?:[…]}`.
- **AI writers:** may create arcs, their steps and sub-steps, from an arc template or the plan, during a build (§4), with CRE's words as step text. May write arc templates generated verbatim from a CRE spec, on CRE's word. Otherwise never create, edit, move or delete arc steps, arcs or arc templates.

- **Links (0.34):** a step card may also be a step of other arcs through `links: [{cast, arc, step, label?}]`; every arc listing reads both, and a step's number is read per arc. Beats, the form that makes them, and the rest live in §5n.
- **Moving between levels (0.53, lean profile §n1):** a step moves to any level or parent in its own arc by drag (onto a row's middle = its last sub-step; its top or bottom quarter = before or after it, at its level) or by ← (up a level: next after its parent step) and → (down a level: last sub-step of the step above it). No new key: the move sets, changes or removes `parentStep` on the moved step and renumbers `step` in the list it left and the list it joined, in one undo step. Its sub-steps go with it (they name it); its `parent` (where it is placed) and `plotLine` don't change, and it doesn't move in the file. Refused: a move into itself or its own sub-steps, a move to another arc, and a level change for a step in this arc only through a link. A step that gains a sub-step becomes a category (§5q), one that loses its last a one-off.
- **Arc identity (0.54, lean profile §n2):** every arc chip on the board (line chips, shelf chips, Needs and checklist rows) is tinted with its character's colour and reads "◇ label · Arc N.N". The colour is the cast card's `color` (a swatch id, the key every card's colour uses), written only when CRE picks one on the character's **Colour** row in the Characters panel; Auto removes it. Without one the colour is **derived, never stored** (§6). ◇ = a character arc; ◆ is reserved for a plot arc, which no card can hold today. The toolbar's **Arc legend** lists the characters with steps on the board, their colours and arcs, and the icons in use.
- **AI writers (0.53–0.54):** a build gives each step the level the plan's tree has. Never move a step between levels on an existing board. Never set or clear a cast card's `color`.

## 5d. Eras and life stages (plugin 0.15 stages, 0.16 eras, 2026-10-10)

**Eras** are the story's periods, in time order (CRE-ruled 2026-10-10: story-level eras, with each character's stages mapped to them, so everyone in a scene is consistent). They live on the Project card: `eras: [{"id":"era-k2x9q","name":"1985","label":"the drought years"}, {"id":"era-p4m1z","name":"Present"}]`. Names are unique (any case); `label` is optional free text.

- **A card's era:** any card in the story may carry `"era":"<era id>"`.
  - On a **top-level card** (a Sequence, directly under the Project card) it **carries forward**: later sequences are in that era until one sets another.
  - On anything **deeper** (a scene, a beat: a flashback, a memory) it applies to **that card and its subtree only**; the next card is back in the running era with no return marker.
  - **Era at a card** = the nearest era set on the card or an ancestor, else the last era set on a preceding top-level card, else the **first era** in the list. A board with no eras has no era anywhere.
- **Aging means a new era** (CRE, 2026-10-10): a character's stage can't change partway through an era; split the era and everyone moves into the new one together.
- Renaming an era changes only `eras[].name` (cards and characters refer to its id). Deleting one clears `era` from the cards that set it (they fall back to the era around them) and drops characters' mappings to it.
- **Tags (derived, never stored):** a card that sets an era answers to `era:<name>` as its own tag, so the walk stops there. Every story card answers to its era in force in the filter, so filtering `era:1985` lights the whole period, flashbacks included.

**Sub-eras (plugin 0.27, 2026-10-11; CRE's design: a life period holds its units — the seasons of the teenage years).** An era may carry `"parent":"<era id>"`: it sits inside that era. One list, one kind of thing; a season is an era with an id, so everything that keys on era ids works unchanged.
- **Order:** the list stays in time order and is read as a tree: an era is followed by the eras inside it, then the next era at its level (`eras: [Teenage years, Summer 1985 (parent: Teenage), Winter 1986 (parent: Teenage), Present]`). The plugin keeps that order on every write; a hand edit that breaks it is read back in tree order. Any depth; names stay unique across the whole list (so "Summer 1985", not "Summer" twice).
- **A card in a sub-era is in the eras above it too.** The filter tag `era:teenage years` lights every season's cards; `era:winter 1986` only that season's; a card that sets a season answers to the parent's walk tag as well. A card set to the parent alone means "somewhere in those years".
- **Spans.** Every before/after/during check uses an era's span: itself and everything inside it. A death in Summer 1985 has happened by Present and by Winter 1986; a character born in Winter 1986 is "not born yet" in Summer 1985 but never in Teenage years itself; a relationship link `to` (until) a parent holds through its last sub-era, as does an event's `until`; a card in the parent and a card in one of its seasons are never before or after each other (only positions in the file order them, as within one era). Character-card carry-forward reads earlier cards in the same era or one nested in it.
- **Stages carry down:** a season with no `eraStages` mapping takes the nearest earlier mapping in list order, which is its parent's unless an earlier season set one. World entries' `byEra` changes and relationship ranges follow the same list order.
- **History** on a parent makes every era inside it history; the story starts at the first era that isn't.
- **Editing:** "inside" on the add row and a "sits inside" select on each era (Eras tab); an era can't sit inside itself or its own sub-era. Moving earlier/later stays among the eras at the same level and takes the block along; re-parenting moves the block to the end of the new parent (or, to the top level, after the era it was in). Deleting a parent moves the eras inside it up a level and keeps them; cards set to them are untouched.
- **Display only:** the Eras tab indents sub-eras and numbers them 2.1, 2.2; the timeline draws them as shorter bands; the card chip, Arc tracking's dividers and the walk read "Winter 1986 · Teenage years".
- **AI writers:** never create, re-parent, move or delete eras.

**The Visuals pane (plugin 0.28, 2026-10-11; CRE's call: drawings below the board, inputs in the side panel).** One pane under the board, four tabs: **Timeline** (eras, sub-eras, events), **Family tree**, **Arc tracking** (the resistance chart and the per-character chains) and **Intensity** (the former Intensity graph view, which still opens if a saved workspace has one and offers the way over). The Characters panel keeps every input — era rows, events, stages, cast, links, types — and each tab that used to draw there now carries an "Open Visuals" row instead; the Arc tracking tab keeps the chains without the chart. Links run both ways: a timeline band opens that era's row, a tree name opens that character, a chart dot jumps to its card; the pane follows the board you're on and redraws on changes and on resize. Toolbar button (the pulse icon) and commands "Visuals pane", "Timeline", "Family tree", "Intensity graph". View only; nothing in the file.

**Structures (plugin 0.29, 2026-10-11; CRE's design: a system or an organisation as a hierarchy, roles held by characters, changing over time).**
- **Kinds inside kinds.** A world kind may carry `within: ["faction","religion","polity"]`: the kinds its entries can sit inside besides their own (`tree` still means "inside its own kind"). An entry's `parent` may then point at an entry of any allowed kind, in the base and per era as before. A parent of a kind not allowed is flagged, never moved. The tree a kind's tab draws is that kind's entries with everything inside them, of any kind, each entry under its own kind's colour and badge; an entry also lists on its own kind's tab, as a root. Tags: an ancestor answers under its own prefix (`faction:the crown` on a card linked to a role in it). Nesting is set in Project settings → World kinds ("sits inside"); a newly added kind can be picked once saved.
- **Built-in Role.** `{"key":"role","name":"Role","plural":"Roles","color":"ember","prefix":"role:","group":"systems","within":["faction","religion","polity"],"fields":[{"name":"held by","onCard":true,"cast":true},{"name":"duties","long":true},{"name":"notes","long":true}]}`. Boards saved before 0.29 gain it like any built-in (switch it off in Project settings if unwanted).
- **Holder fields.** A profile field with `cast: true` names someone: the value is stored as the name and changes by era through `byEra` like any field. **0.30:** `who` says what it may name — `"cast"` (characters, the default), `"world"` (any world entry: a house, a guild), `"any"` (either; characters resolve first) — and `many: true` allows several, stored comma-separated (`"held by": "Bram, House Vane"`; a name can't contain a comma). The panel draws a single-name field as a picker and a `many` field as chips with an add list; an era row with no list of its own shows the carried names greyed, and the first add starts from them. Each name is resolved like any character or entry name (nicknames and era names included); a name that resolves to nothing, or to someone not born / not built yet or dead / destroyed in that era, is flagged on the entry. **Holds** appears under a character and (0.30) under a world entry: every entry whose holder field names them, with the eras as runs ("1985 → Present"). The built-in Role's "held by" is `who: "any", many: true`; any kind's field may be a holder field (a Place's "steward", a Spell's "taught by").
- **Visuals → Structures.** The chart of a kind's entries (a faction, a magic system) with what sits inside, as of an era: boxes by depth, children centred under their parent, the holders of a holder field named in the box ("vacant" when none; an unresolved name marked "?"). Click a box for the entry, a name for the first holder. Display only.
- **AI writers:** never set `within`, `cast`, `who`, `many`, a `parent`, or a holder field's value.

**An event's era (0.28):** the open event row has an **in** select beside **until** (sub-eras indented in both). Picking another era moves the event there, keeping its place among that era's events last; an event pinned to a card whose era isn't the new one comes **unpinned** (it stays off the page in the new era). Dragging onto a card still pins it and sets its era to the card's.

**Life stages** live on the cast card, in the order CRE lists them: `stages: [{"id":"stg-k2x9q","name":"Child","label":"9","aliases":["Ashie"],"fields":{"appearance":"skinned knees","flaw":"afraid of the water"}}, {"id":"stg-p4m1z","name":"Adult"}]`.

- `name` = the stage ("Child"); `label` = optional free-text age; `aliases` = nicknames used in that period; `fields` = **only the profile values that change in this stage**, keyed by profile field name.
- **Stages by era:** `eraStages: {"<era id>": "<stage id>"}` on the cast card. An era with no mapping **carries the stage of the nearest earlier era that has one**; before any mapping (or on a board with no eras) the character is on the base profile. Deleting a stage drops the eras mapped to it.
- **0.15 start points:** a stage's `at` ("start" or a block ID) from plugin 0.15 is ignored since 0.16 and kept untouched, like any unknown field.
- **Values cascade in list order:** base profile `fields`, then each stage's `fields` up to the one in force. A change persists until a later stage changes it again. The base profile is never rewritten by a stage.
- **Character card from a profile (§5b)** fills from the profile **as of the stage for the target card's era**. A card-type field named `stage` (if CRE adds one) gets the stage's name.
- **Carry-forward (§ Character cards)** only reads earlier cards **in the same era**, so the scene after a flashback picks up where the present left off. With no eras, it is unchanged.
- **Names:** stage `aliases` resolve to the character exactly like profile `aliases` (speaker spelling, Character card who-field, walks, Arc tracking). They are not merged into the profile's own `aliases`.
- **Renaming a profile field** moves its value in every stage too.
- **Display only, never stored:** the "⏳ 1985" chip on a card that sets an era ("· only here" below top level), Arc tracking's "1985 — Child · 9" dividers, the dashed era-change lines on the resistance chart, and one scale line per era.
- **Profile templates (§5b)** may carry `"stages":["Child","Adult"]` in their JSON block: stage names only, never values, ages, nicknames or era mappings. A character made from the template, or given it with "Apply template", gets any of those stages it lacks (matched by name, any case), empty.
- **AI writers:** never create, edit or delete eras, a card's era, stages or era mappings.

## 5e. Events (plugin 0.17, 2026-10-10)

Phase 2 of eras → events → relationships (CRE-ruled 2026-10-10). Events live on the Project card: `events: [{"id":"evt-k2x9q","type":"born","era":"<era id>","who":["<cast id>"],"parents":["<cast id>","<cast id>"],"at":"sce042","note":"in the flood year"}]`.

- **Types:** four built-ins, fixed: **born** and **died** (one person), **married** and **separated** (two people). CRE's own types live in `eventTypes: [{"name":"turned","people":1,"begins":"vampire"}, {"name":"cured","people":1,"ends":"vampire"}]`. Names are unique (any case, built-ins included). Renaming a type moves its events; a type in use can't be removed.
- **Where an event sits:** every event belongs to an era (`era`). Without `at` it is **off the page**. With `at` (a block ID) it is **pinned** to the card where it happens, and pinning sets `era` to that card's era. Within an era, events keep their list order.
- **parents** (births only): up to two cast ids. Phase 3 derives parent/child links from these.
- **Existence (derived):** a character with a `born` event exists from that point on, and one with `died` until that point. With neither, they exist in every era. Between eras the comparison is by era order. Inside one era it is by **file order**, and only when both sides are pinned to cards; otherwise "same era" counts as alive. Known limit: a same-era flashback placed later in the board than a pinned death reads as after it. Splitting the era resolves it.
- **States (derived):** a type's `begins`/`ends` turns a named state on and off for the people in it, walking eras in order (like the Ledger's gained/lost).
- **Observations (never verdicts):** a type that doesn't exist; someone no longer in the cast; too few people for the type; a pinned card that was deleted or now sits in another era; born or died more than once; dies before being born; someone in a non-birth event who isn't born yet or has died by then; a birth whose parent isn't born yet, died before it, or is the child; ending a state they aren't in. Arc tracking flags a Character card for someone not born yet or already dead at that card.
- **Removals:** deleting a character removes events they're in and drops them from births' `parents`. Deleting an era removes its events.
- **Display only, never stored:** the "✦ Wren born" chip on a pinned card, Life events under each character, the Eras tab's event lines, and "(not born yet)" / "(died)" beside names.
- **AI writers:** never create, edit, pin or delete events or event types.

## 5f. Relationships (plugin 0.18, 2026-10-10)

Phase 3 of eras → events → relationships. **One cast per board** (default taken 2026-10-10 because CRE hadn't ruled on it; a cast shared across boards for multi-book lineage would be its own build).

- **Kinship is derived, never stored:**
  - A `born` event's `parents` (§5e) make parent/child.
  - A shared parent makes siblings, and **half-siblings** when they share exactly one and either has another known parent.
  - Grandparents and grandchildren follow from parents.
  - Only a character's first `born` event counts.
- **Marriages** come from `married` events. One ends at a later `separated` event between the same two people (any order of names), and reads as **former spouse** from then on.
- **Hand-made links** live on the Project card: `relations: [{"id":"rel-k2x9q","type":"mentor","a":"<cast id>","b":"<cast id>","from":"<era id>","to":"<era id>","note":"after the fire"}]`. They read "**a** is **b**'s *type*" (Bram is Wren's mentor). `from`/`to` bound the eras it holds in, inclusive; absent means from the start / to the end. A link needs two different cast members.
- **Types:** `relationTypes: [{"name":"mentor","inverse":"student"}, {"name":"rival"}]`, written only once CRE edits the starter list (friend, rival, lover, enemy, mentor→student, guardian→ward). `inverse` is what the other side is called; absent means the same both ways. Names are unique. Renaming a type moves its links; a type in use can't be removed.
- **At a card** (the Relationships tab follows the board selection):
  - characters not born yet or already dead (§5e) are listed separately;
  - a child, grandchild or sibling counts once born;
  - a marriage counts from the wedding (before it, nothing; after a separation, former spouse);
  - a link counts inside its eras;
  - a dead relative is marked "died".
  - **Whole story** shows every tie with its eras ("married in 1960, separated in Present", "from 1985").
- **Family tree (derived):**
  - generation = one more than the deepest known parent; a spouse with no known parents sits in their partner's generation;
  - rows place spouses side by side and children under their parents;
  - a separated couple's line is dashed, and † marks someone with a `died` event;
  - cast members with no family ties are listed as "Not in the tree".
- **Observations (never verdicts):** someone their own ancestor; a link with an unknown type, a missing person, the same person twice, a deleted era, or an end before its start; two linked people who both appear on the board (Character cards or dialogue) but never in the same scene.
- **Removals:** deleting a character removes their links. Deleting an era clears it from any link's `from`/`to` (that side becomes open).
- **AI writers:** never create, edit or delete relationship links or types.

## 5g. Books (plugin 0.19, 2026-10-10)

CRE's design (2026-10-10): a **Book** level above Sequence, so one board holds a whole series and every book shares the one Project card's cast, eras, events and relationships. This replaced the queued "cast shared across boards".

- **The level:** `{"key":"book","name":"Book","fields":[summary],"export":"nothing","heading":1,"color":"amber"}`, inserted at `levels[1]` of the Project card's settings. Levels become Project → Book → Sequence → Scene → Beat → Micro-beat. A board gets it once, from **Add Book level…** in the toolbar's Project menu (on the Project card itself before 0.26). It moves every story card directly under the Project card (not cast, ideas or side cards) into a new Book card titled "Book 1", in order, and leaves the text and the clean export unchanged. A Book is an ordinary structural card (`kind: "book"`); a card added below one is another Book.
- **A book's name:** its first line, else its summary, else "Book N" by position.
- **Chapters restart per book.** A chapter is identified as `"<book name> · <chapter>"` (the Chapter filter reads "The Return · Chapter 1"). Group by chapter keeps books apart, and export starts each book's chapter count afresh.
- **Eras (§5d) carry from every level above Scene:** an era set on a Book or a Sequence carries forward in story order until a later Book or Sequence sets another. One set on a Scene or below applies only there. The era at a card is its own era, else the nearest scene-level era above it, else the latest Book/Sequence era before it, else the first era. On a board without books this is the 0.16 rule unchanged.
- **Tags (derived):** a Book card answers to `book:<name>`, so the walk stops at books, and every card answers to its book's tag in the filter.
- **Showing one book** is a view setting (the toolbar's Book selector), never stored. It hides the other books' cards; off-board cards stay. Arc tracking (its scene axis and rows), the intensity graph and Copy/Export clean follow it. An export of one book is written as `<board> - <book> (clean).md`. Selecting a card in a hidden book (walk, link, panel jump) switches to its book.
- **Scale (measured 2026-10-10, Windows):** a full-prose trilogy (4,350 cards, 1.5 MB) parses, serializes, resolves eras and exports in milliseconds. Drawing the board is the cost: about 2 s per redraw with all books shown, about 0.7 s with one book. A planning-depth trilogy (about 900 cards) redraws in about 0.5 s with all books, 0.3 s with one.
- **AI writers:** never add the Book level, or create, retitle, move or delete Book cards, except that a build (§4) may create the Book cards its plan names, on its new board.
- **The Project card has no column (plugin 0.26, 2026-10-11; CRE's call).** View only, nothing in the file changes: while the Project card is the only card at depth 0, the board starts at the first level under it, and the toolbar carries the project's name (its body's first line; click to rename, the rest of the body is kept), the whole-board rollup, and a **Project menu** on the gear (Rename project…, Project settings…, Save as template…, Import from…, Add Book level…). A board with other depth-0 cards (hand-edited) still draws column 0 with the card in it. The card can't be the selection while hidden: a new board opens on the first story card, left-arrow from a top-level card stays put.

## 5l. Parts (plugin 0.32, 2026-10-12)

CRE's call (2026-10-12): the level between Book and Sequence was missing — the container his dev pipeline already calls a **part** (`shape-the-part`: parts/sequences → scenes, chapters cut last). Built the way Books were: optional, one click, nothing in the file format changes.

- **The level:** `{"key":"part","name":"Part","fields":[summary],"export":"heading","heading":1,"color":"rust","optional":true}`, inserted directly above Sequence — below Book when the board has books. A board gets it once, from **Add Part level…** in the toolbar's Project menu. It moves every story card under the Project card (or under each Book) that belongs below the new level into a new Part card titled "Part 1", in order; side cards, ideas and the cast stay. An empty board gets an empty Part 1 to build under, so nine parts can be laid down before any sequence. A Part is an ordinary structural card (`kind: "part"`); a card added below one is another Part. Rename the level ("Act") in Project settings.
- **A part's name:** its first line, else its summary, else "Part N" by position among the parts beside it.
- **A Part owns nothing of its own.** Chapters run straight through the parts (they restart per book, §5g); there is no one-part view and no `part:` tag (the Kind filter lights every Part). What it carries is what every level above Scene carries: an **era** set on it runs forward until a later Part or Sequence sets another (§5d), its **rollup** counts what is under it and lists its sequences, and it **exports as a heading** by default — "Part One" above its chapter headings; set Export: nothing on the level to keep parts out of the manuscript.
- **`optional` on a level (new, any level):** a card may sit directly under the level above an optional one, skipping it, with no nesting warning. Book and Part count as optional by key as well, so a board that added its Book level before 0.32 behaves the same. That is where a **prologue or epilogue** lives: a Sequence straight under the Project (or Book), above Part 1 or after the last part — Ctrl/Cmd+← pulls one out of Part 1. Skipping Sequence or Scene still warns.
- **Prologue and Epilogue card types** (`customTypes`, keys `prologue` / `epilogue`, `like: "sequence"`, `export: "heading"`, colour olive) are added to the board's settings with the Part level when it lacks them. A titleless one exports headed by its type name ("# Prologue"); a titled one by its title.
- **Project settings (0.32):** each level row has Move up / Move down arrows (the structure can be reordered; cards keep their kind) and a **may be skipped** toggle (`optional`). Before this, "Add level above the prose level" was the only way in and it always landed the new level directly above Micro-beat.
- **AI writers:** never add the Part level, or create, retitle, move or delete Part cards, except that a build (§4) may create the Part cards its plan names, on its new board.

## 5m. The board mark and board names (plugin 0.33, 2026-10-12)

CRE's finding (2026-10-12): renaming the project left the tab reading "Untitled board 12", and nothing in the file explorer told a board from a note. Two small changes, one to the file.

- **The board mark:** one frontmatter line, `board: branch-writing`. The plugin writes it when a board is **created** (in front of the markers) or a note is **converted** (into the note's frontmatter, as its last line, else a new block in front), and on request for boards made earlier: the command **Mark boards for the explorer** adds it to every board in the vault that lacks it and reports the count (a board open in a card view is changed through its view, so its undo and unsaved edits survive). **Opening never adds it:** a board without the line still opens as a board and saves byte-identical until it is edited. The parser treats the line as preamble, like any frontmatter (§1); nothing else reads it. It is the one thing Obsidian's own metadata cache can see, so Dataview, search and any other tool can tell boards apart too.
- **The explorer icon:** the file explorer shows the board icon (the same columns icon as the tab) beside every note whose cached frontmatter carries the mark, and beside any board opened, created or marked this session (a set the plugin keeps, not stored). Plugin setting **Board icon in the file explorer** (on by default) switches it off. Decoration only — rows get a class and a span, nothing is written.
- **Board names:** New board (ribbon, command, folder menu, from a template) asks for a name first; it becomes the **file name** (Obsidian's forbidden characters dropped, a taken name numbered) and the **Project card's first line** as typed. Empty, or the API without a name, gives "Untitled board N" as before. **Rename project…** now renames the file to follow: at once when the file was named for the old title or still "Untitled board N", after asking when the file had been renamed by hand; a name already in use leaves the file alone and says so. Links follow (Obsidian's own rename). The tab reads the file name, so the two now agree.
- **Prompts** (0.33): every text prompt has a Cancel beside Save; Escape still cancels.
- **AI writers:** may create the new board a build targets (its name from the plan, with the `board:` mark), or a copy of an existing board. Never rename, mark or remove an existing board.

## 5n. Beats — the spine before the scenes (plugin 0.34, 2026-10-12)

CRE's design (2026-10-12, worked through in chat): eras (time), sequences (plot) and character arcs (journey) felt like three systems that met only on the board, too late. The join is one object, a **beat**, with three faces: *when* it happens and whether it is a fact in the world; *whose* arc it advances and as which step; *where* in the plot it lands and, later, the card it becomes. A beat is made in one form and lives in all three views before any scene exists; the Spine view (next) reads these.

- **A beat is an arc-step card** (`kind: "arcbeat"`, §5c) — it waits under the Project card, drags onto a sequence or scene, keeps its data, and "Make it a…" turns it into a Scene or Beat. New on the card, all optional: `who: [castId…]` (the people it is about; its arcs' owners count too); `links: [{cast, arc, step, label?}]` (further arcs it is a step of — an ensemble beat is one card in several arcs); `era` (its own era, §5d; absent = the era of wherever it is placed, and unplaced = not in time yet); `world: [placeId]` + `fields.setting` (its place, §5h). Its **fact** is an event (§5e) pinned to it (`at: <card id>`): one record, in the Timeline and on the beat.
- **A free beat** has no `cast`/`arc`/`step`: a storm, a war, a moment that is nobody's step. One with no era either is listed first on the Eras tab as "not in any era yet" so it is never lost.
- **Arc links** (§5c amended): every listing of an arc's steps reads a card's own `cast`/`arc`/`step` **and** its `links`; a step's number and label are read "as seen from" an arc (`stepIn`, `stepLabelIn`); reorder and rename carry an arc context so moving a linked beat in one arc leaves its number in the other alone; deleting it closes the gap in every arc; removing an arc only drops the link on beats that belong to another arc. Sub-steps belong to the card's own arc only.
- **The form** (New beat…: the Eras tab under an open era, each arc on the Arcs tab, or the command): what happens; who, ticked, each with "advances: new step of <arc>… / an existing unplaced step"; where (a Place); when (an era, or where it's placed — the story's first era by default so a free beat is findable); also a fact? (an event type; a name for one about nobody). Taking an existing step makes the beat **that** card (its text filled, nothing else lost); in a second arc an unplaced, childless step is absorbed (removed, its number kept on the link). Nothing opens on the board; the beat waits in the panel until dragged.
- **Where beats show:** the Eras tab lists each era's beats (placed ones by their card's era, unplaced by their own) with who, fact and where, draggable to the board, ⋯ for the step menu; the Visuals Timeline draws them under the events as squares (hollow while unplaced); the Arcs tab shows a linked beat as the step of every arc it serves; the board's tray chip badges a free beat by its people.
- **Make it a…:** the card keeps its era, place, world link and fact; its `who` become `char:` tags; text becomes a container's summary or a prose card's body (§5a). Chapter is never on the form: the beat takes its chapter from the scene it ends in.
- **AI writers:** may read beats. During a build (§4) may create, link and place beats as the plan holds them. Never promote one (Make it a…). Never touch beats on an existing board.

## 5o. The Spine (plugin 0.35, 2026-10-12) — derived, never stored

The roadmap CRE asked for after the beat (§5n): "a story spine can be built in full before scenes and beats and microbeats hit the board … once a spine is built, a roadmap, I have all of the information needed to drill down." The Spine is the first tab of the Visuals pane and is **read from the board every redraw** — it adds nothing to the file.

- **Columns** are the cards at the spine level — the intensity graph's *outer* level, Sequence unless renamed (`settings.intensity.levels.outer`) — in story order, inside the book shown when one is. Off-board and side cards are never columns.
- **Groups** above the columns: runs of columns in the same Part (§5l); with no parts, the same Book (§5g); neither → no group row. A column outside every part reads "no part".
- **The era band:** each column's era (§5d, `eraIdAt` of the sequence), equal neighbours merged into one cell.
- **Facts:** events (§5e) whose `at` card is the sequence or anything under it.
- **A row per character** who has any beat: cards that are arc steps or beats (`kind: "arcbeat"`), or the cards those became (they keep `cast`/`arc`/`step`, `who`, `links`), where `beatWho` (§5n) names the character. A chip lands in the column of the card it sits on (placed) or is (became); unplaced ones fill the row's first cell; one placed outside every column is counted, not shown. A chip reads the step number *as seen from that character's arc* (`stepIn`), its text (`beatText`), and a flag per pinned fact. The row head counts placed/total.
- **Nobody's row:** beats with no `who` at all.
- **Seeds:** `seed:<name>` / `payoff:<name>` tags on cards inside a column, by column, with the Seed check's statuses (paid / open / backwards / orphan — paid means a payoff at or after the first seed's column); the view draws a line from each seed chip to each payoff chip.
- **Interaction (view only):** a chip drags onto any column cell or sequence heading → `placeIdeaOn` (the same move as dragging onto the board); a placed chip's click opens the step menu; a card chip's click shows the card; a sequence or part heading selects it on the board; an era cell or a fact opens the Eras tab; a character name opens them; New beat… opens the form (§5n).
- **AI writers:** read-only; a described spine is a description of these derived rows, never a thing to write back.

## 5p. The drill (plugin 0.36, 2026-10-12)

Release three of the braid (beat §5n → Spine §5o → drill): the step from the roadmap down to the board's levels, and the one stored change — an arc's order.

- **Drilling a column** (view state only, never stored): a sequence heading on the Spine carries a chevron; open, the column splits into one sub-column per scene under it (`SpineColumn.scenes`: the scene-level cards — the intensity graph's *inner* level — anywhere under the sequence, in order) plus "in the sequence" for beats placed on the sequence itself. A chip's `scene` is the index of the scene it sits in or is (through any beat in between), -1 on the sequence; `factScenes` the same for facts. Dropping a chip on a scene sub-column, a scene heading, or "in the sequence" is the same move as on the board (`placeIdeaOn`).
- **Make it a card here:** a placed chip offers one click that turns the beat into the kind its host holds (`childKind`: a scene in a sequence, a Beat in a scene) — §5n's Make it a… with the kind chosen for you; era, place, fact and who-as-tags carry as before.
- **`arcs[].order`** (stored on the cast card, §5c): `"time"` for a backstory told in flashbacks; absent = story order. The planner's out-of-order observation then compares the **eras** the steps sit in (`eraIdAt` of each step's host, `eraCompare` with sub-eras) instead of file order: a later step in an earlier era reads "comes before step N in time"; steps in the same era say nothing. Arcs tab: "in story order / in time order" beside the arc's name.
- **AI writers:** may read `order`; never set it, never drill or promote.

## 5q. Plotting mode (plugin 0.37, 2026-10-13)

The Statement Plotting Method v12 through CRE's ratified lean profile ([[WORKFLOWS/statement-plotting/Statement-Plotting-Method_v12-lean-profile]], dec-037). **Opt-in per board.** A board without `settings.plotting.on` reads, writes and exports exactly as before; nothing below exists on it.

**Switching it on** (Project settings → Plotting mode) is one additive, undoable change. Fields are appended to a level's template only when the template lacks a field of that name (case-insensitive), so a scene's existing `pov`, `setting`, `goal` and `outcome` are reused. Every added field carries `"plot": true`; the plugin keeps those out of the field-rename rows and out of the plain editor when plotting is off. Switching off sets `settings.plotting.on` to `false` and changes nothing else.

- `settings.plotting`: `{"on": true, "leads"?: [castId…], "world"?: true, "exits"?: {castId: cardId}}`. `leads` is the POV-lead roster in order, stored only once there are two or more; `world` switches world tracking on; `exits` is the lead-exit marker (#267), the unit after which a lead leaves the rotation, the carry and the Closure offers.
- `settings.structuralRoles`: the E5 role list this book uses. Absent = the novella preset.
- `plotArcs` (on the Project card's marker, beside `events` and `relations`): `[{"id":"parc-…","label"?,"goal_holder"?: castId,"action_type"?,"slots"?:{…},"span"?,"goal"?,"stakes"?,"opposition"?,"conflict"?,"planned_outcome"?,"outcome_detail"?,"planned_change"?,"resolved_in"?: cardId,"main"?: true,"leadArc"?: true}]`. `action_type` is an E2 name (Travel … Prepare; "AC5" also reads); `planned_outcome` an E3 label. `main` is stored only when picked by hand.
- **The Character Arc** is an arc on the cast card (§5c) flagged `"plot": true`, with `beliefStart`, `beliefEnd`, `direction` (Positive / Negative / Flat) and one step field, `belief`. Its waypoints are its arc steps: `label` = the E5 role, `arcFields.belief` = the planned belief.
- **Cast profile fields** added: `emotional start`, `physical start` (text, not the 0–10 intensity lane), `pronoun`, `pronoun (subject)`, `pronoun (possessive)`. A character's belief start is the Character Arc's `beliefStart`, shown on the character, stored once.
- **Book fields** (Project card; each Book card on a series board): `story start`, `world start`, `world end`.
- **Sequence fields:** `shape` (Scene / Sequel / Event / Closure; absent = Scene), `serves arc` (a `plotArcs` id), `goal holder`, `leads` (the rotation list: names, comma-separated, repeats allowed), `opposition`, `action`, the E2 slots (`origin`, `destination`, `target`, `threat`, `opponent`, `information`, `secret`, `object`, `holder`, `ward`, `truth`, `ordeal`, `plan`, `coming event`), `goal`, `outcome`, `outcome detail`, `story from`, `story to`, `world from`, `world to`, `span`, `stakes`, `conflict`, `role`, and the statement fields of the other shapes (`character`, `reacts to`, `reacts to (short)`, `setting prep`, `setting`, `option a`, `option b`, `costs`, `decision`, `sets goal`, `agent`, `event action`, `effect`, `closes arcs`).
- **Scene fields:** `goal holder`, `serves arc`, `action` and the slots, `setting prep`, `setting`, `goal`, `stakes`, `opposition`, `conflict`, `outcome`, `outcome detail`, `resolved in` (a card id), `story from`, `story to`, `world from`, `world to`, `role`, `questions opened`, `pov`.
- **Card types** (`customTypes`, `like: "scene"`, `plot: true`): `sequel` (character, reacts to, reacts to (short), setting prep, setting, option a, option b, costs, decision, sets goal, role), `event` (agent, event action, setting prep, setting, effect, story/world from/to, role — a story unit, not a §5e event), `closure` (character, reacts to, reacts to (short), setting prep, setting, closes arcs, option a, option b, decision, role).
- **Beat-level fields** (the Beat **level**, one exchange inside a unit — not the §5n arc-step beat): `actor`, `action`, `responder`, `reaction`, `direction` (Toward / Away), `what changed`, `cost` (`"true"`), `functions`, `form`, `read against`. A Beat card counts as a plotted beat only once one of these is filled (or it is an FL4 placeholder): a Beat used as a container of micro-beats is not one.
- **Ledger rows** are Character cards (the arc type, §5) directly under a unit. `char` names the character; `entry state` / `exit state` are the emotional pair. Added: `wants`, `outcome`, `outcome detail`, `dimensions` (`physical`, `belief`, comma-separated — emotional is on by default; a filled pair also switches its dimension on), `physical from`, `physical to`, `belief from`, `belief to`, `physical signal`, `emotional signal`, `belief signal`.
- **Value forms:** cast references on cards are names (any name or nickname); in `plotArcs` and the roster they are cast block IDs. `reacts to` and `resolved in` are card block IDs (a range is `id..id`). `closes arcs` is `plotArcs` ids, comma-separated. `outcome` is an E3 label, set by the outcome questions. `setting prep` is blank for "in" (the template's default); `-`, `—` or `none` means no preposition on purpose. Labelled tracks: `label: value; label: value`.
- `plotComplete: true` on a unit or sequence marks it Complete (the author's mark; refused below Outlined or while a required field is blank).
- **The flows' stored keys (0.38).** The flows store nothing derived. A few marks record what the tool made or what the author ruled:
  - `plotStub: true` on a sequel (or a sequel-shape sequence) the FL4 pass created. It is withdrawn only while untouched: nothing but its tool-written `reacts to`.
  - `plotNoStub: true` on a unit whose stub the author deleted, so it is never raised again.
  - `plotFl4` is a queue answer (`"beat"` / `"sequel"`) on a queued unit or sequence. On a Beat card it is instead the id of the unit whose reaction it is: the FL4 placeholder, flagged until its `what changed` is filled.
  - `plotReviewed: true` on a sequel whose sets-goal prefill was accepted (FL5).
  - `plotLedgerPlan: {name: {dimension: [from, to]}}` on a sequence: a ledger plan accepted from the FL3 rollup, or typed.
  - `plotOffer: true` on a Closure added from a per-lead offer (0.39).
  - Two blank-only fills are also written when a card is created: a new scene's `goal holder` from its sequence's rotation list, and a placeholder beat's `actor`.
- **Visibility (0.39, b9), optional:**
  - `vis: {"<field>": {"v": "Concealed" | "Misdirected" | "Shown, unread", "shown"?: "<what the reader sees>", "revealed_in"?: cardId | "never"}}` on a unit. This is the per-field map the profile suggests; an unset field is Shown.
  - `visUnit: cardId` is one revealed in for every hidden field of the unit; a field's own wins.
  - A unit whose pov is `Offscreen` treats its filled fields as Concealed.
- **Statement blocks (0.41, lean profile §j).** A Scene unit and a Scene-shape sequence are drawn as a GOAL line above a CHAIN (ENTRY → BUT / THEREFORE turns → EXIT); a plotting beat as one sentence. Nothing below is written to a board until the author first uses it, in the same undo step; a board opened and saved without an edit is byte-identical. Every key is new only where no field existed (profile §j5, the mapping marked UNCONFIRMED there):
  - ENTRY's words are `story from`; EXIT's words (a BUT or plain EXIT) are `story to`; EXIT's ending is the unit's own `outcome` / `outcome detail`.
  - A THEREFORE EXIT: `decision` holds what they decide (no leading "to"); `character` holds who, only when typed (blank = the goal holder). `sets goal` is not written.
  - `plotChain: {"exit"?: "but" | "therefore", "turns"?: [{"id": "t…", "k": "but" | "therefore", "text"?, "outcome"?, "detail"?}]}` on the unit's marker: the EXIT's flavor (absent = plain) and the middle turns in order. A turn's id is unique within the card. Absent = no turns and a plain EXIT. `outcome` on a turn is an E3 label (Disruption included).
  - `plotFrom: "<parent card id>:<point>"` on a drilled child (point = `entry`, `exit` or a turn id): the one link from a child to the chain point it was drilled from. The point keeps no link back; its child is found by this key. The child stores no outcome: its EXIT's ending is its point's ending, written there.
  - `with` (a field): companions on a unit, names comma-separated ("with The Hound and John"). The goal holder stays one character.
  - **Disruption** is a sixth E3 label (`outcome`, a turn's `outcome`), picked from the list, never set by the outcome questions; "resolved in" is not asked for it.
  - Condition blocks write the existing `vis` map (0.39, b9): hidden until → `Concealed`, misdirected until → `Misdirected`, revealed in → `Shown, unread`; the unit named is that field's `revealed_in`.
  - **Reading the outcome.** On a card with a chain or a `plotFrom`, every reader of `outcome` / `outcome detail` (status, stubs, rules, views, statements) goes through the chain: the EXIT's ending (on a child, its point's), else the last turn that has one. A THEREFORE EXIT has no ending, so a stored outcome under it is kept but not read until the EXIT is BUT or plain again. A card with neither key reads its fields exactly as before.
  - **FL4 with a chain.** A THEREFORE EXIT raises no stub and no queue question; a BUT EXIT always puts the unit (or sequence) on the queue ("beat or sequel?") unless a stub is raised; a plain EXIT runs FL4 as before. A unit with `plotNoStub` is never given a stub by a queue answer either (the 0.40 path re-raised one in the edit that deleted it), and its queue row offers Beat only.
  - **V2 and status.** On a chain unit or sequence, a BUT turn with words (or a BUT EXIT's words) counts opposition and conflict as filled for V2 and for the Sketch / Outlined tiers; the fields themselves still render in the statement.
  - A Beat card with `plotFrom` is a plotting beat from the moment it exists.
- **AI writers (0.41):** may read `plotChain`, `plotFrom` and `with` to describe a plot; never add, move or remove a turn, set a flavor, drill, or write a chain line.
- **Free-text cards (0.42, lean profile §k).** Every plotting unit (Scene, Reaction, Event, Aftermath — stored kinds `scene`, `sequel`, `event`, `closure`, unchanged), every sequence, every plotting beat and every Arc is drawn as a title plus its typed chain. 0.41's storage carries the chain unchanged; the keys below are new and are written only the first time the author uses the thing, in the same undo step. A board opened and saved without an edit is byte-identical; no stored key is renamed, moved or deleted, and old slot values are never converted.
  - **Title:** the card's body (its first line), as every structural card's title already is. A beat's one typed line is its title.
  - **A THEREFORE EXIT's words** are `story to`, like any EXIT. A 0.41 card whose THEREFORE EXIT kept its words in `decision` (and `character`) shows them as "X decides to Y" until that line is edited; the edit writes `story to` and clears that `decision` / `character` on a Scene (never on a Reaction or Aftermath, where they are slot values).
  - **A leading "but" / "therefore"** typed on a turn or EXIT sets its flavor (`plotChain` `k` / `exit`) and is not stored in the words.
  - `plotPins: {"entry" | "exit" | "<turn id>": "<world entry id>"}` on a unit or sequence: a chain line's accepted place pin. Absent = no pins; a line without one is at the place of the line before (ENTRY: the previous same-level card's EXIT place).
  - `plotUntag: ["<cast card id>" | "<world entry id>", …]`: tags the author removed from a card. The name-matcher never re-adds them; a drop by hand lifts the mark.
  - **A character tagged by drop:** the card's existing `tags` (`{"tag": "char:<name>", "by": "cre"}`). A place, item or other entry dropped is the existing `world` id list (the kind's field, such as `setting`, is **not** filled on a typed card, so it stays typed).
  - **A run:** the child's existing `plotFrom`, written `"<parent id>:<first line>..<last line>"` for a bundled run of consecutive lines (`".."` never occurs in a line id); a single line stays `"<parent id>:<line>"`. The parent holds no key. A line belongs to at most one child; the child's outcome is the run's last line that has an ending (else the last that can carry one), read and written there.
  - `plotArcs[i].chain: {"entry"?, "exit"?, "exit_k"?: "but" | "therefore", "turns"?: [{"id", "k", "text"?, "outcome"?, "detail"?}]}`: an Arc's chain. Its title is the existing `label`; its EXIT's ending is the existing `planned_outcome` / `outcome_detail`. A sequence drilled from an Arc line holds `plotFrom: "<arc id>:<line>"` (or a run).
  - **Done:** `plotComplete: true`, set and cleared from the card menu with no gate on a typed card.
  - **Who accepted:** the shape's existing who field — `goal holder` (Scene, sequence), `character` (Reaction, Aftermath), `agent` (Event), `actor` (beat).
  - **A chain line's condition:** the existing `vis` map, keyed `story from` (ENTRY), `story to` (EXIT) or `chain:<turn id>` (a turn).
  - **A character's state on a unit,** edited in the Characters panel, writes their existing ledger row (a Character card under the unit, added the first time); a place typed there is the row's new `place` field.
  - **Typed vs slot-built:** a card holding none of its shape's slot fields (Scene: action and its E2 slots, goal, stakes, opposition, conflict, setting, span, `with`; Reaction: reacts to (and short), option a / b, costs, decision, sets goal; Event: event action, effect; Aftermath: reacts to (and short), closes arcs, option a / b, decision; beat: action, responder, reaction, what changed) is a typed card. A slot-built card shows those values behind its + as one plain line.
- **AI writers (0.42):** may read every key above; may suggest tags, pins, positions and states only as offers the author accepts (the planned tagger, `^backlog-branch-writing-tagger-intent`), marked `by: ai`; never write a chain line, a title, a run, a pin or `plotUntag`.
- **Beat chains and micro-beat blocs (0.43, lean profile §l).** A beat's chain is stored as a unit's is; one new key links a micro-beat to the chain point it keeps. Written only the first time the author uses the thing, in the same undo step. A board opened and saved without an edit is byte-identical; no stored key is renamed, moved or deleted.
  - **A beat's chain:** `story from` (ENTRY) and `story to` (EXIT) in the beat's `fields`, `plotChain` (turns, EXIT flavor) on its marker, EXIT's ending in the beat's `outcome` / `outcome detail`, a turn's ending on the turn. The Beat level's template is not changed: the two fields are written into `fields` on first use and are drawn as the chain, never as fields.
  - **A plotting beat** (above) is now also a beat holding `plotChain`, `story from` or `story to`. A beat used only as a container of micro-beats is still not one, until it is given a chain (card menu → "Give this beat a chain…").
  - `plotBloc: "entry" | "exit" | "<turn id>"` on a micro-beat (a direct child of the beat, at the prose level): the chain point whose bloc it is in. Absent, or naming a line the beat no longer has, = unplaced. Moving a micro-beat to another bloc rewrites it; moving it under another card removes it (unplaced there); removing a turn removes it from that turn's micro-beats.
  - **The order rule:** under a beat with a chain, the file holds its micro-beats in bloc order — ENTRY's, each turn's in chain order, EXIT's, then unplaced. Every plugin write that places, moves or re-orders keeps it, in the same undo step; other cards under the beat (notes, side cards, variants) keep their positions. A hand edit that breaks the order is read as it stands, and settled only when that beat is next edited.
  - `beatTypes` default: `exposition` is in the built-in list for new boards (colour `wheat`). A board that stores its own list keeps it; Project settings → the prose level offers "Add exposition".
- **AI writers (0.43):** may read `plotBloc` and a beat's chain; never place, move or unplace a micro-beat, write a beat's chain line, or settle the order.
- **Conversations (0.44, fix list 2026-10-16 item 2).** One dialogue micro-beat can hold a whole conversation. It stays `kind` = the prose level and `type: "dialogue"` (so a bloc's type mix counts it once); its **body holds the lines, one paragraph each, exactly as written** (word counts, search and reading view see every line). One new key on its marker: `convo: {"with": [names], "who": [the speaker of each line, by position], "end"?: "natural" | "interrupted" | "walked out" | "cut away", "endText"?: string}`. Participants are names (cast names, or any name). A paragraph with no `who` entry (typed in Markdown) takes the next participant after the line before. `speaker` is not used on a conversation (a merge moves it into `who`). Clean export writes each line as a dialogue card of its own would be written (same quotes, same tag rule), so a merge leaves the export byte-identical. Nothing is ever merged by itself: "Merge into one conversation" (card menu) joins a run of neighbouring dialogue micro-beats in the same bloc into the first card, in one undo step; a card with other marker keys (a colour, fields, an era), children, a body of more than one paragraph, or something linking to its block id stays out of the run.
- **AI writers (0.44):** may read `convo`; never write it or merge cards.
- **Card types onto the chain, release 1 (0.45, lean profile §m1): quiet retirements, UI only.** Nothing is stored, added, renamed or deleted; a board's settings are not changed. On a board with `settings.plotting.on`:
  - **"Add card"** (the card menu's Add other) leaves out the Character card type (the custom type keyed `character`, else the board's first arc type) and "Character from the cast…". Card kind still lists it; the Characters panel's "Add to selected card" stays.
  - **The Beat level's position types** (`setup/hook`, `escalation`, `scene-climax`, `valley`, `outcome/hook` on `levels[beat].types`, the Story Framework's list) are not offered in its type picker (the card menu's Type list, the `t` key); any other type on that list (the plotting fixtures' `conversation`, `action`) still is. A list of positions only leaves no picker, and `t` does nothing. A custom type `like: "beat"` without its own `types` is treated the same. The list stays in the settings; Project settings still edits it.
  - **Stored values read as before:** a Beat's stored `type` still draws on its card and answers the Type filter (`allTypes` is unchanged); stored Character cards keep feeding the Characters panel, the ledger, the carry and Arc tracking. `typesFor` itself is unchanged, so every reader that clears or checks a type against the level's list (an idea made into a card) behaves as before.
  - Reaction, Event and Aftermath slot fields were already only behind + (0.42 §k1); unchanged.
  - Plotting off: every list as before. Subtext stays offered until release 6.
- **Card types onto the chain, release 2 (0.46, lean profile §m2): line marks and key-beat marks.** Written only the first time CRE sets a mark, in the same undo step; a board opened and saved without an edit is byte-identical, and no stored key is renamed, moved or deleted.
  - `plotMarks: {"entry" | "exit" | "<turn id>": {"beat"?: "<mark>"}}` on a unit, sequence or plotting beat: what is marked on each chain line. `beat` is the key-beat mark, one per line. Later releases add their own keys beside `beat` (event, closes, item effect). A line with nothing left drops out; an empty object drops the key.
  - `plotArcs[i].chain.marks`: the same object for an Arc's lines. An Arc that has no `chain` yet gains one holding only `marks`.
  - **Following the line:** a turn's id never changes, so a move or a flip carries its marks with nothing written. Removing a turn deletes its entry in the same edit (Undo restores both). A mark naming a line the chain doesn't have is not drawn and stays in the file.
  - **Offers:** scene and beat chains offer `climax`, `valley`, `hook`, then `settings.plotting.keyBeats`; sequence and Arc chains offer the story-beat list (`settings.structuralRoles`, else the novella preset). A unit-level `role` still reads as before.
  - `settings.plotting.keyBeats: [names]`: CRE's own key-beat entries, written only from **New key beat…** in a line's ⋯ menu (added and set on that line in one undo step).
  - The beat-position types stay retired from the picker (release 1); a stored Beat `type` still reads.
- **AI writers (0.46):** may read `plotMarks`, an Arc's `chain.marks` and `keyBeats`; never set, suggest, move or clear a mark (lean profile §m: marks are CRE's).
- **Card types onto the chain, release 3 (0.47, lean profile §m3): shape views.** Nothing is stored, added, renamed or deleted. The views are derived from the keys above (§6 "Shape views").
- **Card types onto the chain, release 4 (0.48, lean profile §m4): event, closes and fact on the line; no new stubs.** Each key is written only the first time CRE sets it, in the same undo step; a board opened and saved without an edit is byte-identical, and no stored key is renamed, moved or deleted.
  - `plotMarks[line].event: {"agent"?: "<name>"}` on a unit, sequence or plotting beat: the line is an event, caused by someone other than the goal holder. `agent` is a name (any cast name or nickname, or any name typed); absent = no one's doing (the world, the weather). The effect is the line's ending, read, never stored. An Arc's `chain.marks` takes no event mark.
  - `plotMarks[line].closes: ["<plotArcs id>", …]` on a unit, sequence or plotting beat: the Arcs that resolve on that line. The per-lead Aftermath offers count an Arc closed when any existing line's closes mark names it, else when an Aftermath's `closes arcs` does. V19 and the Aftermath "changes" check read a closes mark on the unit's own chain as they read `closes arcs`.
  - `events[i].line: "entry" | "exit" | "<turn id>"` on a §5e event pinned to a card: the line of that card it happens on. `at` is unchanged and still the pin every reader (Spine, Timeline, the card chip) uses. Re-pinning or unpinning the fact drops `line` in the same edit; a removed turn drops `line` on every fact on it. A `line` naming a line the card doesn't have is not drawn and stays in the file.
  - All three follow their line as the key-beat mark does (a move or a flip writes nothing; a removed turn takes them, Undo restores them).
  - **FL4 stubs retired (CRE-ruled 2026-10-16):** the post-edit pass raises no `plotStub` card and withdraws none. Stored stubs, `plotStub` and `plotNoStub` stay exactly as they are. A queue answer of Sequel (the legacy face) and "Also a sequel for {lead}" on an existing stub still add one, as the author's own clicks.
- **AI writers (0.48):** may read the event and closes marks and a fact's `line`; never set, move or clear one.
- **Card types onto the chain, release 5 (0.49, lean profile §m5): Character "turned at".** Written only the first time CRE points a to-value at a line, in the same undo step; a board opened and saved without an edit is byte-identical, and no stored key is renamed, moved or deleted.
  - `plotTurnedAt: {"emotional" | "physical" | "belief": "entry" | "exit" | "<turn id>"}` on a ledger row (a Character card directly under a unit): the line of that unit's chain that turned the character on that dimension. Absent for a dimension = "by the end of the unit", as every row before 0.49. Set and cleared only from the Characters panel; clearing the to-value drops its entry in the same edit. An empty object drops the key.
  - **Following the line:** a move or a flip writes nothing; removing a turn drops every entry naming it on the unit's rows in the same edit (Undo restores). An entry naming a line the unit doesn't have reads as no line and stays in the file.
  - **The 0.8 Character fields** (`role`, `flaw`, `challenge`, `coping`, `resistance`) are not offered on a plotting board where no Character card holds a value in any of them: the editor leaves them out and a new row doesn't copy them from the profile. Nothing stored changes, the Character type's `fields` list is untouched, and a stored `resistance` still draws in Arc tracking.
- **AI writers (0.49):** may read `plotTurnedAt`; never set, move or clear it.
- **Card types onto the chain, release 6 (0.50, lean profile §m6): subtext on the conversation card.** Written only the first time CRE types one, in the same undo step; a conversation with no subtext stores exactly what it stored before, and no stored key is renamed, moved or deleted.
  - `convo.beneath: "<words>"` on a conversation micro-beat: what is under the whole conversation. Absent when empty.
  - `convo.sub: ["<note>" | "", …]`: an optional subtext note per spoken line, by position, as `convo.who`. Rewritten with `who` whenever lines move, are added or removed, so a note stays with its line. Absent when every note is empty.
  - **Never exported:** the export reads a conversation's speakers and words only.
  - **The Subtext type** (the custom type keyed `subtext`) leaves the card menu's Add other on a plotting board; Card kind still lists it, a stored Subtext card reads as before, and plotting off it is offered as before.
- **AI writers (0.50):** may read `beneath` and `sub`; never write them (they are CRE's words).
- **Card types onto the chain, release 7 (0.51, lean profile §m7): floaters onto the chain.** Each key is written only the first time CRE uses it, in the same undo step; a board opened and saved without an edit is byte-identical, and no stored key is renamed, moved or deleted.
  - `plotLine: "entry" | "exit" | "<turn id>"` on an idea (`kind: "idea"`) or an arc step (`kind: "arcbeat"`) placed on a card: the line of that card's chain it belongs to. Absent, or naming a line the card doesn't have, = unplaced (the card's shelf). No order rule: the floater's place in the file doesn't change. A removed turn, a move to another card, a return to the inbox or "Make it a…" drops it in the same edit.
  - **Make it a line:** an idea becomes a new turn (`plotChain`) after the chosen line, its words the turn's text; the idea card is removed in the same edit (Undo restores it).
  - `plotMarks[line].items: [{"item": "<name>", "change": "<tracker change>", "holder"?: "<name>"}]` on a unit, sequence or plotting beat: things changing hands on that line. The Ledger reads them with the old tracker cards, in story order.
- **AI writers (0.51):** may read `plotLine` and `items`; never place, move, unplace, insert or mark (floaters wait on purpose, and the marks are CRE's).
- **Arc needs (0.55–0.56, lean profile §n3–§n4).** Read from what the board already stores; one new key, written only the first time CRE uses it, in the same undo step. A board opened and saved without an edit is byte-identical; no stored key is renamed, moved or deleted.
  - **A need (0.55, derived):** an arc step placed on a typed sequence or scene-level unit (Scene, Reaction, Event, Aftermath) on no line (`plotLine` absent or naming a line the card doesn't have). It is drawn in the card's **Needs** list, not on its shelf. On a beat (on or off its lines) or on a line of a scene or beat chain, a step is a beat. Ideas keep the shelf.
  - **An inherited need (0.56, derived):** a card drilled from a sequence's line or run (`plotFrom`) has as needs the arc steps on those lines of that sequence (`plotLine`), drawn "↳ from Sequence 2 · BUT". Nothing is written on the child; off the line, it is gone from the child.
  - **A category (0.56, derived):** an arc step with at least one sub-step (`parentStep` naming it). One with none is a one-off, placed once.
  - `plotNeeds: ["<step id>", …]` (0.56) on a typed sequence or scene-level unit: the categories that are also needs on this card beyond the card each is placed on. The step card is never copied or moved by it. Added by dropping a category that is placed elsewhere from the Characters panel or the Spine onto the card (off its lines); taken off by the row's **Not needed here**; moved with the row's drag to another card. The last one off drops the key. An entry naming a card that is gone, isn't an arc step or has no sub-steps is not drawn and stays in the file.
  - **The checklist (0.56, derived):** a category's direct sub-steps under its row: ✓ with where on a beat card or a line of a scene or beat chain; "→ where" placed as a need; "○ open" when unplaced. Never a count or a warning.
- **AI writers (0.55–0.56):** may read needs, `plotNeeds` and checklists to describe a plan; never place, add, move or take off a need, an appearance or a way.
- **AI writers:** may read every key here. During a build (§4) may set what the plan holds: the plotting switch, the roster, lead exits, `plotArcs` goal holders and the plan's words. Never write a chain line, a mark, a statement, the Complete mark or an outcome. The statements are the author's words in v12's templates. Nothing here is generated.

## 5h. World entries (plugin 0.21, 2026-10-10)

The story world beside the cast, on one model: places first (0.21), items and system kinds (0.24), CRE's own kinds (0.25). A **world entry** is a card with `kind: "world"` directly under the Project card, never in the columns (the World panel holds it), never exported, off the main line.

```
%%bw {"v":1,"kind":"world","depth":1,"wkind":"place","name":"The Mill","aliases":["the old wheel"],"parent":"w0harr","profile":[{"name":"type","onCard":true},{"name":"description","long":true}],"fields":{"type":"mill"},"byEra":{"era-p4m1z":{"name":"The Burnt Mill","fields":{"type":"ruin"},"parent":""}}}%% ^w0mill

%%/bw%%
```

- `wkind`: the entry's kind, a key from the board's world kinds (§5k): `place`, `item`, `faction`, `religion`, `polity`, `magic`, or one of CRE's own.
- `name` and `aliases`: fixed parts of the entry, as for a cast member (§5b). `profile` and `fields`: its own field list and values, same shape as a cast profile; missing `profile` → the kind's starter fields.
- **Changes by era, keyed straight to the story's eras:** `byEra: {"<era id>": {"name"?, "aliases"?, "fields"?: {…}, "parent"?}}` holds, per era, only what changes. **Values cascade in era order:** base, then each era's changes up to the era asked about; an era with no entry carries. The base is never rewritten by an era. (Characters keep their life stages mapped to eras, §5d; this is the same idea without the named stage in between.)
- **Nesting** (kinds with `tree: true`, places): `parent` is the entry it sits in at the base; a `byEra[...].parent` overrides it from that era on, `""` meaning "nothing from here on" (top level). What a place sits in can therefore change by era. Loops are observed (`worldFlags`), never broken.
- **Links from cards:** a story card links to entries by id, `world: ["w0mill"]`. Dropping an entry on a card adds the id and, when the kind names a `field` the card's level has, fills that field with the entry's **name as of the card's era** (a place fills a scene's `setting`; an item fills a tracker card's `item`). A card whose kind-field already names an entry (any of its names) counts as **linked by name**, so older boards and hand-typed settings show up without a rewrite; such a link draws as a dotted chip.
- **Tags (derived, never stored):** a linked card's own tag is `<prefix><base name>` (`place:the mill`), so the walk stops where the entry is set. In the filter it also answers to every name the entry has had and to everything it sits in as of the card's era (`place:harrow`), carried down to the cards underneath; the Tag filter offers the ancestors too.
- **Renaming** an entry (base or era name) renames the kind-field on cards linked by id whose field held the old name; a field that only matched by name is left alone. **Deleting** an entry drops its links (clearing a field that named it), lifts entries nested in it to the top level, and takes its own events and ties (§5i, §5j).
- **Templates** per kind are notes in `<templates folder>/<Plural>/` (`WRITING/BOARD TEMPLATES/Places/`): frontmatter `type: bw-world-template` + `kind: <key>`, a readable field list, and ```` ```json ```` `{"v":1,"kind":"place","fields":[…]}`. Field shape only, never an entry's values.
- **Display only:** the "📍 The Old Mill (The Mill)" chip (base name in brackets when the era renames it), its tooltip's "in Harrow › Vermont", the tree per era, Through the story grouped by era, and every observation (a parent that is gone or loops; a card in a place that isn't built yet or is destroyed by then, §5i).
- **AI writers:** never create, edit, move, rename or delete world entries, their changes by era, their nesting or their links on cards.

## 5i. Lore events and history-only eras (plugin 0.22, 2026-10-10)

Events (§5e) become world history: about any entries, or nobody; spanning eras; mentioned by cards.

- **Subjects:** `who` may hold cast ids, world entry ids, or nothing. Built-in types: **born**, **died**, **married**, **separated** (characters) and, new, **built** and **destroyed** (places and things). CRE's own types take `people: 0 | 1 | 2` (0 = a war, a flood: nobody in particular) and are about anything. A character in a place-type event, or a place in a people-type event, is an observation, never refused.
- **Existence** is derived for any entry: born/built = exists from there on, died/destroyed = gone after. A card in a place that isn't built yet or is destroyed by then carries the observation ("The Mill is destroyed by here (destroyed in 1985)") on its chip and in Through the story.
- **Lore:** `name` ("The Flood War") is shown instead of "<who> <type>". `until` (an era id) makes the event span its era through that one inclusive; a state a spanning event begins holds while it runs and lets go after its last era. Ending before starting is an observation.
- **Mentions:** a card lists events it refers to without them happening there: `events: ["evt-k2x9q"]` on the card (card menu → Mentions). Pinned stays `at` on the event (§5e). Each event lists the cards that mention it; a mentioned event draws as a dashed "↗" chip.
- **History-only eras:** `history: true` on an era (§5d). The story starts in the **first era that isn't history**; cards with no era of their own default to it, and the Eras tab marks "the story starts here". A history era is reached only by setting it on a card (a myth, a flashback).
- **Removals:** deleting an entry removes the unnamed events it is in (as before for characters) and only drops it as a subject from a named lore event. Deleting an era removes events starting in it, opens the end of events running until it, and drops world entries' changes keyed to it.
- **Display only:** the Eras tab's timeline (one band per era, history hatched; marks per event, bars for spans), "… The Flood War (since 1870)" under later eras, the "↗" chips, existence notes.
- **AI writers:** never create, edit, pin, mention or delete events, nor mark an era history.

## 5j. Ties between any entries (plugin 0.23, 2026-10-10)

Hand-made links (§5f `relations`) join any two entries: `a` and `b` may be cast ids or world entry ids. Same fields (`type`, `from`, `to`, `note`), same reading ("a is <type> of b"; world types read plainly: "Bram rules Harrow", "Harrow borders Vermont").

- **Types:** the starter list gains, for places and systems, `borders`, `rules → ruled by`, `member of → has member`, `holds → held by`, `allied with`, `at war with`, each marked `"for": "world"`. A `for: "world"` type is offered once a world entry is on either side; two characters see the people types only. CRE's own types take the mark too (the "places & systems" switch).
- **At a card:** a tie counts inside its eras, as before; a world entry's row sits after the people's. A tie whose side isn't built yet or is destroyed by then is held back like an unborn or dead character's.
- **Reading (plugin 0.31, display only):** in the Relationships tab a tie of a `for: "world"` type is phrased from the row's own side — Dee's row reads "member of Guild", Town's "ruled by Council", Council's "rules Town" — while people ties keep the other's role ("Bram · mentor"). Nothing in `relations` changes.
- **Observations:** unknown type, a side no longer on the board, the same one twice, an era gone, ending before starting. "Never share a scene" is checked for two characters only.
- Deleting an entry removes the ties it is in. Kinship and the family tree stay about characters.
- **AI writers:** never create, edit or delete ties or tie types.

## 5k. Items, system kinds and CRE's own kinds (plugin 0.24–0.25, 2026-10-10)

The **world kinds** a board uses live in its settings: `worldKinds: [{key, name, plural?, color?, prefix?, field?, tree?, ledger?, group?, icon?, fields?, builtin?}]`, read as *what is stored, plus any built-in kind the board doesn't name unless it is listed in `worldKindsOff`*. So a board saved before a new built-in shipped still gets it, and switching a built-in off sticks.

- **Built-ins:** `place` (prefix `place:`, fills `setting`, nests), `item` (`item:`, fills `item`, `ledger: true`), and the system kinds `faction`, `religion`, `polity`, `magic` (`faction:` … `magic:`, `group: "systems"` — one shared tab). Starter field lists are short (type, description, notes) and each entry's fields are its own afterwards.
- **Items and the Ledger:** an item entry's Through the story also shows, by name, the Ledger rows (§5 tracker types) whose thing matches any of its names: lore above (the profile), possession history below. Dropping an item on a tracker card fills its `item` field; on a scene it links by id. Both answer to `item:<name>` as the Ledger already did.
- **Systems** carry their weight in ties (§5j): who is member of what, who rules which place, from which era until which.
- **Own kinds (0.25):** Project settings → World kinds: name, plural, colour, tag prefix (`ship:`), the card field a drop fills, a group, nests, ledger, starter fields; `key` is set once from the name and never changes. A kind with entries on the board can't be removed; removing a built-in adds it to `worldKindsOff`. Import from… adds the source's own kinds this board lacks (never replaces one). Templates per kind follow the plural (`WRITING/BOARD TEMPLATES/Ships/`).
- **AI writers:** never add, edit or remove world kinds.

## 6. Derived values (never stored)

Word counts, beat-type mix, threads touched, section numbers (1.2.4), soft nesting warnings, and seed-check statuses are all computed when displayed. **Never write a rollup into a marker.** A stored count goes stale the moment a beat changes.

- **Rollup:** words and prose-card count under a container, the prose type mix, threads touched, and the list of its direct container children with their types (e.g. a scene's beats: conversation, action).
- **Eras and life stages (§5d):** the era at a card, `era:` tags, the stage for an era, the cascaded profile, the era chips and the Arc tracking dividers are computed when displayed.
- **Events (§5e):** existence, states, observations and the event chips are computed when displayed.
- **Relationships (§5f):** kinship, marriages, ties at a card, the family tree and its generations are computed when displayed.
- **Books (§5g):** a card's book, book-qualified chapters, `book:` tags and the one-book view are computed when displayed.
- **World (§5h–§5k):** an entry as of an era (the cascade), the tree per era, links by name, `place:` / `item:` / `faction:` … tags and the ancestors a card answers to, Through the story, an item's possession history, existence notes on chips, the timeline, spans and "still running" lines, ties at a card, and every world observation are computed when displayed.
- **Main line:** every card except custom side types (`like: "side"`) and `note` / `side` / `variant` / `research` / `idea` / `cast` / `arcbeat` / `world` cards and everything under them.
- **0.31 (display only, never stored):** a story card (any level) whose parent is a side kind other than `variant` carries the soft warning "… under a Character (off the main line: not counted, not exported)" — the beat typed while a dropped Character card was still selected; a book or sequence with no `era` of its own shows the era in force as a greyed chip; a card whose own era differs from the era around it names that era in its chip's tooltip; a container's rollup counts its direct children by kind ("3 scenes · 1 beat"); the type-mix strip waits for a typed micro-beat; an empty board draws a first-card placeholder in its first column; the drop zones are labelled above / below / child while dragging.
- **Statement blocks (0.41):** the GOAL sentence and every chain line as drawn; the unit outcome (the last ending in the chain) and its note; the hook and its notes; the ENTRY ghost (the previous unit's EXIT at the same level, "X decides to Y" for a THEREFORE); the THEREFORE carry (a decision as the decider's next unit's ghost goal, same level, story order); a THEREFORE EXIT's who when blank (the goal holder); a drilled child's "⤴ from" line, its who / actor prefill and a drilled beat's Away / Toward; the Tagged line and the underlined names inside words; which slots sit behind the card's +. Selections, opened slots and the palette's state are view state. Never written; a ghost is written only when the author accepts it (Enter), and then as their value.
- **Free-text cards (0.42):** every tag chip (names and nicknames of cast and world entries matched in typed words, minus `plotUntag`, plus the accepted who and what was placed by hand); the who offer (the first character named); each line's pin offer (the first place named that isn't its pin); each line's place (pinned, or carried from the line before; ENTRY from the previous same-level card's EXIT, within a lane — a flashback card with its own era is its own lane); the ENTRY offer (a drilled child's run's first line, else the previous card's EXIT words); who the words leave behind ("leaving X behind", "left X behind", "without X", "X stays / remains"); every character's position per unit (start, end, the line they were left at; left behind on the ENTRY line = they stay where they were) and the continuity notes ("X starts Scene 4 at the Cottage, last at the Ridge, no travel shown", same era only); Where is everyone; the child's shape suggestion (a run ending on a BUT → Scene, a lone THEREFORE → Reaction) and → next's (BUT exit → Reaction, else Scene); the run brackets; a slot-built card's plain slot line; Leads' who (accepted, else first named); the Book outline of Arc chains, Progress (lines not split, cards done, next cards still to make) and the outline beat sheet; which rules go quiet on a typed card. Edit state (the line being typed, a draft, the picked run, an opened slot line, a fresh child's shape offer) is view state. Never written; a suggestion is written only when accepted, and then as the author's value.
- **Beat chains and blocs (0.43):** a beat's blocs (its micro-beats grouped by `plotBloc`, in chain order) and the unplaced group; each bloc's type mix (counts by `type`, "untyped" when none) and its words ("2 dialogue · 1 action"); whether a beat has a chain (ENTRY or EXIT words, a turn or an EXIT flavor); the prose column's bloc labels (ENTRY, BUT, THEREFORE, EXIT · flavor, UNPLACED). Which blocs are open is view state. Never written.
- **Card types onto the chain, release 1 (0.45):** which kinds "add card" offers and whether a level's type picker shows are read from `settings.plotting.on` on every menu, never stored.
- **Key-beat marks (0.46):** each line's mark chip, the list a line's ⋯ offers, and the two observations ("two lines marked climax", "the line marked climax has no ending") are read from `plotMarks` / `chain.marks` on every redraw. Never written; no mark is ever derived.
- **Shape views (0.47, lean profile §m3):** read only from CRE's key-beat marks (`plotMarks`, an Arc's `chain.marks`), the chains, `plotFrom` and the hand-set intensity fields, when Visuals → Plot → Shape is open: whether the Shape tab is offered (any mark in the book); where each climax lands (line n of N, per chain, across a sequence's scenes and the Arc chains); the rhythm around each climax (the lines before it, the line after, the next valley in the chain or the next unit); nesting (the parent line a marked chain was drilled from, and its mark); marks against intensity (each lane's highest value against the climax scene or sequence, the gap's size and distance); the mark chips in Book and Beat sheet. Never written; nothing is derived in place of a mark, and an unmarked chain contributes nothing.
- **Event, closes and fact chips (0.48, lean profile §m4):** each line's "⚡ event · agent" chip with the line's ending as its effect, its "⊘ closes A1" chip, its "✦ Wren born" fact chip, the agents an Event menu offers (the card's tagged characters minus its goal holder), the facts a line's menu offers (those pinned to the card), and which Arcs count as closed for the per-lead Aftermath offers are read on every redraw. Never written.
- **Floaters on the chain, read (0.51, lean profile §m7):** which floaters sit on which line (a `plotLine` naming a line the card has) and which are on the shelf; the shelf itself (no count); each line's floater and item chips; the lines Put on a line and Make it a line offer; the Ledger's merged events and their order. Read on every redraw, never written.
- **Arc needs, read (0.53–0.56, lean profile §n):** the drop zones and which ←/→ a step row offers; each character's auto colour (the board's swatches, assigned per cast card ID: hand-picked ones first, then by ID order, each at a fixed hash of its ID or the next free swatch); every arc chip's tint, icon and "Arc N.N"; the Arc legend's rows; a chain card's Needs (its own, its `plotNeeds` appearances and, on a card drilled from a sequence line, the steps on that line); each need's sub-step landings and a category's checklist (✓ on a beat or a scene or beat line, → as a need, ○ open); whether a step is a category. Read on every redraw through per-model indexes, never written.
- **Turned at, read (0.49, lean profile §m5):** the turned-at picker's lines; a drilled beat's reading of each pointed to-value against its own line (before, "turns here", after); a Character card's place inside its scene's slot on Arc tracking's chart; "at BUT" and the line order of belief changes in Plot → Arc track; whether a board offers the five 0.8 Character fields (any Character card holding one). Read on every redraw, never written.
- **Plotting rules and views (0.39):**
  - every observation (V1–V35, read per lead in an ensemble), and which ones stop the Complete mark;
  - the Progress view's counts; the lead-spacing view; the sequence lead lines; the lead outcome clauses; the per-lead Closure offers; the waypoint notes;
  - the reader statement; the reveal chain and V14–V16; the Ensemble view, Beat sheet and Arc track.

  Never written.
- **Plotting flows (0.38):**
  - every prefilled or carried value a blank field answers: FL1 goal holder, pov, opposition and serves arc (the single-Arc auto-link; a lead's own Arc); FL2 story, world and per-character from-values (blank pairs pass through, labels carry each); FL5 sets goal; the rotation list prefill; the routed goal; the routed row wants or offer;
  - the derived row wants and outcome; belief on and belief to at a waypoint or resolved in; a lead Arc's span; beat 1's actor and the responder;
  - the virtual required rows; FL3 Arc outcomes and sequence rollups; the FL4 queue and where a placeholder goes.
  
  Never written.
- **Plotting (0.37):** every statement (Sketch and full per shape, Book, Arc (subplots), ledger row, beat line), each card's status (below Sketch / Sketch / Outlined; Complete only with the author's mark), what each tier still needs, a sequence's drafting-ready flag, the main Arc when not picked (the only Arc; in an ensemble the first lead's), the effective roster (one lead, the main Arc's goal holder, in a single-POV book), POV mode (single / ensemble, from the roster's length), an Arc's label when blank (its goal holder's name) and code (A1, A2 … by position), and turning points. Never written.
- **Chapter:** a card's chapter is the nearest `fields.chapter` on itself or an ancestor.
- **Seed check:** pairs `seed:NAME` and `payoff:NAME` tags by NAME (case-insensitive), in story order.
  - `paid`: a payoff comes after the first seed.
  - `open`: a seed with no payoff.
  - `backwards`: every payoff comes before the first seed.
  - `orphan`: a payoff with no seed.
- **Thread walk:** the cards carrying a tag, in story order. A `char:NAME` walk also includes `dialogue` cards whose `speaker` matches NAME.

## 6a. Intensity alignment — design spec (CRE-ratified 2026-10-09, NOT YET BUILT)

The intensity graph today plots hand-set values at two levels and compares endpoints. This section specifies the walk across all levels and the check against the prose. Nothing here changes sections 1–4; every value below is derived or lives in a sidecar, so schema stays v1.

**Principle.** Planned values that agree with each other prove nothing about the prose. Each beat carries three numbers per lane: **target** (planned), **measured** (from the prose), **gap**. Hand-setting is kept to sequence and scene endpoints; beats derive. (Fractal Envelope Model: materialize the upper rungs, check the lower ones.)

**1. Walk up / walk down between set levels (sequence ↔ scene).**
- *Endpoint check:* first child's start vs the parent's start; last child's end vs the parent's end.
- *Seam check:* each child's end vs the next child's start. With continuous seams the children's changes sum exactly to the parent's change, so any misalignment is located at a seam or an endpoint.
- Shown as gap **magnitudes**, never pass/fail. A discontinuity at a scene cut may be deliberate; that is CRE's call. Each lane is checked independently.

**Re-key (CRE-ruled 2026-10-16, card types onto the chain, lean profile §m2).** Step 2 below is re-keyed from beat *types* to CRE's **key-beat marks on chain lines**: a scene's peak target sits on the line marked climax. The beat-position types (setup/hook, escalation, scene-climax, valley, outcome/hook) are retired from the picker on plotting boards (0.45, §5q); setup/hook is ENTRY, escalation the BUT/THEREFORE turns, outcome/hook EXIT. What follows is UNCONFIRMED — card types 2026-10-16, and is settled when step 2 is built (after release 2 ships the marks): the scene's start target sits on ENTRY and its end on EXIT; its peak (the higher-magnitude endpoint, or a hand value) on the line marked climax; a dip on a line marked valley; other lines interpolate by line order; a beat's target is read from the line of its scene its `plotFrom` names (a run: its last line), and a beat chain's own marks place targets inside the beat the same way. A scene with no climax mark gets no peak target (nothing is derived in its place, §m "marks are CRE's"); its lines interpolate between ENTRY and EXIT. `settings.intensity.beatShapes` then maps mark names, not beat types, to shapes. A stored beat `type` is still read for a beat that is not drilled from a chain line, until CRE rules otherwise. The original step 2 text is kept below as provenance.

**2. Derived beat targets (walk down).** A beat's target is interpolated from its scene's start/end by beat type: `setup/hook` = scene start · `escalation` = rising between · `scene-climax` = the scene's peak (the higher-magnitude endpoint, or a hand value) · `valley` = a dip below the surrounding beats · `outcome/hook` = scene end. Beats of unlisted type interpolate linearly by position. An optional hand override on a beat is stored as ordinary `fields` (`intensity start/end`, `physical start/end` added to the Beat level) and is drawn as an override. The type-to-shape map lives in `settings.intensity.beatShapes` so a template can change it.

**3. Measured values (the silent-failure fix).** A beat's prose is its micro-beats joined in story order.
- *Physical lane:* computed live in the plugin from the scene-intensity rubric's mechanizable dimensions (D5 somatic load, D6 narration-only pacing surface), rescaled to 0…10. **Does not check:** stakes, proximity or turns. The tooltip says so (DIR-018).
- *Emotional lane:* an AI pass extending `scene-intensity` to beat scope: magnitude from D1/D2/D4, sign as a new judged call. Evidence-gated as the rubric already requires.
- *Storage:* never in markers (§6). A sidecar `<board>.measure.json` keyed by card ID, each entry holding the values, the rubric version and a **hash of the prose it read**. Hash mismatch → the measured line draws hollow (stale), never as a current value.

**4. Gap markers.** Planned vs measured is drawn as a ghost line beside the planned line, with a marker where they differ. The tool never edits either side.

**Governing rule (DIR-017 amendment, 2026-10-09).** Revision stage only, never at dictation or as a dictation precondition. A mirror, not a grade: show the gap's size, never pass/fail. On a gap the default is to **move the plan to the prose**; changing the prose is CRE's call alone.

**Build order:** `^backlog-bw-align-walk` → `^backlog-bw-align-beat-targets` → `^backlog-bw-align-measure` → `^backlog-bw-align-gap-markers`.

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
