# Tagging mode — "tag the board": offers, every one by: ai

The pass that reads a board and writes the under-the-hood layer into the card markers: beat types, speakers, tags and links,
intensity, missed tags, per-character state changes, wants, and a chain summary. **Everything it writes is an offer
marked `by: ai`** that becomes CRE's on first touch; it never changes a body and never changes or removes an entry whose
`by` is `cre`.

## Where each offer goes (schema §4, §5q, §6a)

| Offer | Written as | Why there |
|---|---|---|
| a tag the text supports (`char:Mara`, `place:the mill`, `thread:…`, `seed:` / `payoff:`) | `add-tag` → `tags[]` entry `by: ai` | the schema's own by-attributed slot |
| a link between cards (echoes, pays off, mirrors) | `add-link` with `rel` → `links[]` entry `by: ai` | same |
| beat type, speaker, summary, wants, a character's state change, a ✦ chain summary | `offer` → one marker key `ai: {…, by: "ai", offered: date}` | `type`, `speaker` and the fields carry no `by`; writing them directly would be indistinguishable from his hand. The plugin preserves the `ai` key untouched (§4 unknown keys); showing it on a collapsed card is a plugin feature, queued |
| intensity scores (emotional −10…+10, physical 0…10) via the `scene-intensity` rubric | `offer-intensity` → the sidecar `<board>.measure.json`, keyed by card id with the prose hash | §6a: measured values never sit in a marker and go stale when the prose moves; the hash says when |

## The run

1. Version check, `read <board> --full` (prose cards included).
2. **Vocabulary, read-only:** the project's `REFERENCE/_LEXICON.md` and `_DEV_MAP` ruled terms when the board belongs to a
   project that has them, so tags match his dev notes (DIR-014). Nothing is written there, ever. The board's own `tagPrefixes`
   and existing tags are the house style; follow them.
3. `suggest-tags <board> --out <file>` gives the deterministic part: cast and world names found in bodies that aren't tagged
   yet (`plotUntag` honoured). Add your own reading on top — types, speakers from the tag or the exchange, state changes and
   wants from what the text shows, the chain summary of a unit's chain lines in **his** words, intensity from the rubric
   (load the `scene-intensity` skill's rubric only then).
4. Two routes, his choice at the start of the run (default: route A on a board he is working in, route B on a fresh import):
   - **A. Rule first:** show the offers as a ruling list (one line each with the reason), write only approved ones.
   - **B. Write as offers:** write every offer at once (they are all by: ai and in the `ai` key or the sidecar, so nothing of
     his changes), then show the change list; he clears what he doesn't want ("drop the ai offers on ^k3x9a2" → `remove-tag`
     / an `offer` with the key emptied).
5. Change list: one line per card touched, counts per kind.

**Tags the plugin already derives — never write these** (schema §5 "Derived tags", §5d, §5g, §5h): `char:<speaker>` on a
dialogue card; `<field>:<value>` for any `asTag` field (`pov:`, `setting:`, `char:` and `role:` on Character cards);
`era:<name>` where a card sets an era; `book:<name>`; `place:` / `item:` / `faction:` … where a card links a world entry by
id or by name. `read --full` lists each card's `derivedTags` beside its stored `tags`; `suggest-tags` skips both.

**A valid outcome is "the text supports nothing"**: a board whose cards are already typed, whose speakers are set and
whose text names no one gets a change list of zero writes and one line saying why. Never invent an offer, a score
(intensity needs evidence in the prose) or a summary to have something to show. A board that belongs to no project has no
`_LEXICON` or `_DEV_MAP`; say so and use the board's own vocabulary.

Rules that hold either way: never a prose-level body; never a conversation line, subtext, chain line, statement, mark or
Complete mark (§5n, §5q); a `by: cre` tag or link is never touched; dev-edit's blind seats never see the network (don't
run tagging on a board a dev-edit panel is about to read). On a 200+ card board run `apply --dry` first and read the count.
