---
type: schema
title: Branch Writing card marker schema
schema_version: 1
plugin: branch-writing
plugin_version: 0.25.0
created: '2026-10-07'
last_updated: '2026-10-10'
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
- **AI writers:** never create, edit or delete cast cards or profile templates.

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
- **AI writers:** never create, edit, move or delete arc steps, arcs or arc templates.

## 5d. Eras and life stages (plugin 0.15 stages, 0.16 eras, 2026-10-10)

**Eras** are the story's periods, in time order (CRE-ruled 2026-10-10: story-level eras, with each character's stages mapped to them, so everyone in a scene is consistent). They live on the Project card: `eras: [{"id":"era-k2x9q","name":"1985","label":"the drought years"}, {"id":"era-p4m1z","name":"Present"}]`. Names are unique (any case); `label` is optional free text.

- **A card's era:** any card in the story may carry `"era":"<era id>"`.
  - On a **top-level card** (a Sequence, directly under the Project card) it **carries forward**: later sequences are in that era until one sets another.
  - On anything **deeper** (a scene, a beat: a flashback, a memory) it applies to **that card and its subtree only**; the next card is back in the running era with no return marker.
  - **Era at a card** = the nearest era set on the card or an ancestor, else the last era set on a preceding top-level card, else the **first era** in the list. A board with no eras has no era anywhere.
- **Aging means a new era** (CRE, 2026-10-10): a character's stage can't change partway through an era; split the era and everyone moves into the new one together.
- Renaming an era changes only `eras[].name` (cards and characters refer to its id). Deleting one clears `era` from the cards that set it (they fall back to the era around them) and drops characters' mappings to it.
- **Tags (derived, never stored):** a card that sets an era answers to `era:<name>` as its own tag, so the walk stops there. Every story card answers to its era in force in the filter, so filtering `era:1985` lights the whole period, flashbacks included.

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

- **The level:** `{"key":"book","name":"Book","fields":[summary],"export":"nothing","heading":1,"color":"amber"}`, inserted at `levels[1]` of the Project card's settings. Levels become Project → Book → Sequence → Scene → Beat → Micro-beat. A board gets it once, from the Project card's **Add Book level…** button. That button moves every story card directly under the Project card (not cast, ideas or side cards) into a new Book card titled "Book 1", in order, and leaves the text and the clean export unchanged. A Book is an ordinary structural card (`kind: "book"`); a card added below one is another Book.
- **A book's name:** its first line, else its summary, else "Book N" by position.
- **Chapters restart per book.** A chapter is identified as `"<book name> · <chapter>"` (the Chapter filter reads "The Return · Chapter 1"). Group by chapter keeps books apart, and export starts each book's chapter count afresh.
- **Eras (§5d) carry from every level above Scene:** an era set on a Book or a Sequence carries forward in story order until a later Book or Sequence sets another. One set on a Scene or below applies only there. The era at a card is its own era, else the nearest scene-level era above it, else the latest Book/Sequence era before it, else the first era. On a board without books this is the 0.16 rule unchanged.
- **Tags (derived):** a Book card answers to `book:<name>`, so the walk stops at books, and every card answers to its book's tag in the filter.
- **Showing one book** is a view setting (the toolbar's Book selector), never stored. It hides the other books' cards; the Project card and off-board cards stay. Arc tracking (its scene axis and rows), the intensity graph and Copy/Export clean follow it. An export of one book is written as `<board> - <book> (clean).md`. Selecting a card in a hidden book (walk, link, panel jump) switches to its book.
- **Scale (measured 2026-10-10, Windows):** a full-prose trilogy (4,350 cards, 1.5 MB) parses, serializes, resolves eras and exports in milliseconds. Drawing the board is the cost: about 2 s per redraw with all books shown, about 0.7 s with one book. A planning-depth trilogy (about 900 cards) redraws in about 0.5 s with all books, 0.3 s with one.
- **AI writers:** never add the Book level, or create, retitle, move or delete Book cards.

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
