# World walk — "finish the bible" / "walk the world": a built board's side panels, at his approvals

A built board has its structure full and its bible empty. On Witchwood that meant no tags, an empty seed check, world
entries no card links to, a cast holding only roles, and interludes with no era. So the World tab, Through the story, the
place and item filters, the seed check and the timeline showed him nothing, while the material sat in his DEV registry and
his thread list. This mode carries that material onto the board, stage by stage, so the panels tell him concisely and
clearly what is in his story and he can see what is missing for the redraft. (Intent:
`WORKFLOWS/intents/branch-writing-world-walk.md`; first subject and worked example: the Witchwood Interlock board and
`SYSTEM/reports/2026-10-22-witchwood-interlock-gap-walk.md`.)

## Why the rules are shaped this way

- **One approval list per stage, and the next stage only after he has ruled it.** Later stages build on earlier ones: links
  and tags find an entry only once it exists. He skips a long list by its length (`_ME`: report the true size of a pile),
  so eight short lists, each ruled in one pass, beat one long sheet.
- **His words stay exactly as they are**: micro-beats and idea cards are the only forbidden zone (CRE 2026-10-19 and
  2026-10-22; CDIR-001). `scripts/words.mjs <board> --ideas` runs before and after every writing run. Both lines must
  match; a run that moved them is undone at once and reported.
- **Side-panel text is information for him, in plain words drawn from his.** A description, a profile answer or an event
  note tells him what a thing is, and he won't use it in the work (CRE 2026-10-22: "the administrative goal is conveying
  information to me concisely and with clarity"). Write it plain. Keep his original lines in the entry's `notes` with the
  source path, because "if a quote is key, it should stay as my words, but its context needs inclusion". A line that *is*
  the story object (an adage, a vow, a refrain) is named plainly and quoted. Match the four entries the clarity walk
  already described (Dark Vale, the darkness, darkshine, the men of the deep woods). Their shape is a plain description,
  then `notes` = his key lines in quotation marks, the source, then "Description in his words: …".
- **Story content only from his sources:** the board's words, the project's DEV registry, `REFERENCE/threads.md`, and the
  approved arc plan. When none of them answers, the gap stays an open line. An invented place, item, era or relationship is
  the hardest error for him to spot (CDIR-003).
- **Story inferences are proposals; admin writes directly.** He rules each of these: which entries exist, which kind a
  lore entry becomes, which registry character is which cast member, a scene's era, a flashback call, a seed or payoff
  placement, a profile answer, and an event's pin. These you write directly, logged and undoable, with a change list
  after: the links that follow from an approved entry, idea types, `by: ai` tags, and byte-identical duplicate ideas. That
  is the expert's split everywhere (SKILL.md).
- **The registry is dev material, never landed canon.** Each entry calls itself "developing understanding, not committed
  canon", so it is a source for proposals and nothing lands from it unruled. `REFERENCE/` is read-only, as always.
- **Leave what he made as he made it.** His own entries, eras, tags and kinds are never renamed or removed (on Witchwood:
  the generic "Magic" and "Religion" entries and the unused `summer - 4` era). List them once in the report as his to
  rename or remove. A needed new world kind is a Project setting he owns (schema §5k): report it NOT DONE with the setting
  named, and propose the nearest existing kind beside it.
- **Every stage is built for N POV leads and several spine sets.** Never assume one lead or one timeline (memory:
  ensemble POV books). Witchwood has five leads and a second full spine for the Woodsgirl in its own seasons.

## The run

**Before any stage:**
1. Run the version check and read the board (SKILL.md Load). Read `_CREATIVE DIRECTIVES.md`.
2. Check the spec-material guard: `threads.md` is spec material. If the board is one a blind-read or dev-edit panel will
   read, skip stage 4 and say why. A plotting board such as the Interlock board is fine.
3. Ask him to close the board's tab (`^obs-457`). Hash the board (`sha256sum`), and run `words.mjs <board> --ideas`.
   Keep a copy in the scratchpad.

**Each stage:**
1. **Facts.** `node <skill>/scripts/world_walk.mjs <board> --out <scratchpad>/world-walk --stage <stage>`. The script is
   read-only and takes about 3 seconds on a 6,800-card board. It writes `<stage>.md` (readable, story order) and
   `<stage>.json` (for building ops), plus a `README.md` listing what it did not check. Re-run it at the start of every
   stage, because the board has moved. Its rows are candidates and evidence, never findings: read the cited words before
   proposing.
2. **The list.** Totals first, then one numbered line per proposal with its reason, grouped by kind. The reason is the
   evidence: the registry path, the card's words, or the plan cell. Ask with plain questions, never by code. He may
   answer "all", "all but 3, 7", or line by line.
3. **The write.** Build one ops file from what he approved plus the stage's admin (`references/ops.md`). Run
   `apply --dry` first; the first use of a new op (`link-world`, `pin-event`) and any run over ~50 cards go to a scratch
   copy first (SKILL.md Safety habits). Re-hash before writing: if the hash isn't the last run's after-hash, read again.
   Then `apply`, then `words.mjs --ideas` again.
4. **Close the stage.** Give the change list (the tool's `made:` lines, counted per kind), the NOT DONE lines as
   questions, and one line of what this stage did not check (the script's README line plus anything you skipped). Append
   the stage's section to the report. Wait for him before the next stage.

## The stages

| # | Stage | Script gives | Proposed (his ruling) | Written directly (admin) | Ops |
|---|---|---|---|---|---|
| 1 | **The registry** | each registry place, item, lore entry and character, with mentions in his words, its blurb and "What it is", the names the registry's own links use for it, and the board entry or cast member it may already be | each missing entry: kind, name, aliases, description, notes · each lore entry's kind · which registry character is which cast member, or a new cast member | nothing | `add-world` (`fields: {description, notes}`, `sources: [registry path]`), `add-cast` (name, aliases), `add-aliases` |
| 2 | **Links** | per world entry, the scenes whose micro-beats or ideas name it, split into *direct* (a proper name, mostly capitalised in his text) and *ask* (a name that is also an ordinary word: "the darkness", "Cottage", "Magic") | per *ask* entry, one line: link every mention / only where it means the entry (name the scenes) / none | every *direct* scene link for an approved entry: one link per scene, and the cards inside carry it. A link never fills `setting`: a scene naming a place is not set there (the boy wishes for the Moon Sea in the cottage); where a scene happens is his call (`fill: true` only on his word) | `link-world` |
| 3 | **Era walk** | flashbacks with no era, interludes neither marked nor given an era, unplaced arc steps with no era, and eras no card uses, each with its opening words and beats | each flashback's era · each interlude's flashback call and era · each unplaced step's era, only from its own words or the plan | nothing; placed steps inherit their scene's era and are never stamped | `set-era`, `set-flashback` |
| 4 | **Seeds** | each thread's Planted quotes (and a Settled thread's paid quote) matched by span: *present* (the card), *reworded?* (the nearest card, its words now), *gone*, or *no quote* | each present seed or payoff as `seed:<tag>` / `payoff:<tag>` on its card | nothing | `add-tag` |
| 5 | **Tag the board** | — (`suggest-tags`) | tagging mode as it stands: `references/tagging.md`, route A or B on his word (default B on a board this size) | | `add-tag`, `offer` |
| 6 | **Events** | each unpinned event and the scenes whose words name it, its subjects ranked, same era first | each pin, quoting the card's words; a card in another era only with his ruling that the event's era moves | nothing | `pin-event` (`moveEra: true` only on that ruling) |
| 7 | **Profiles** | each cast member's empty fields beside the matched registry entry's Who / Flaw and wound / Want / Transformation | each answer as a plain line, his lines kept in `notes` | nothing | `set-cast` |
| 8 | **Idea admin** | ideas typed by their form (an opening quote → dialogue, a closing ? → question), the rest to read, twins in one scene, and the same words in different scenes | nothing (placement stays the idea-placement proposal) | every retype, every twin removed, and the stage-5 `by: ai` tags on ideas | `set-type`, `remove-duplicate-idea`, `add-tag` |

| 9 | **Settings** (added 2026-10-22, on his ask) | per scene, an evidence block (his prose, or his ideas where there's no prose; era; the places his words name; the tool's titles and summary marked as tool-written) in chunks of 20 for parallel readers | each scene's setting: a board place, a place in his words that isn't an entry yet (proposed with its own add-world), or "not shown". A scene that moves takes its main action's place unless he says otherwise | nothing | `set-field` (`setting`), `add-world` for a new place he approves |

**9. Settings.** A setting is where the action happens, read from the scene's own words, never the first place named: the boy wishes for the Moon Sea in the cottage, so that scene's setting is the cottage. Readers return `^id · place · board/new · a quote under 15 words · note`. Validate every chunk's id set before use. The list leads with the counts (clear / not shown / new places), then the new places to approve, then the moving scenes; the routine ones go as one approve-all block grouped by place. An empty slot (no prose of his) is read from its ideas, which is weaker evidence: say so on its line.

### Stage notes

**1. The registry.** Read each row's "⚑ his ruling in the entry" lines first: a ruling further down an entry outranks its opening section. On Witchwood, the Carved Wolf's own entry already carried "the hare should replace the wolf", which an opening-section read missed. Write each description from the entry's "What it is", blurb and "What it feels like / means". Say
what the thing is in one to three plain sentences, not what happens to it across the book. Notes get his key lines in
quotation marks, then `Source: <registry path> (DEV registry — developing, not canon)`; the tool refuses a quoted span
that is not in the notes, the board or a `sources` file. Aliases come only from names he uses for the thing on the board
or in the registry's links ("Petyr" for Petyr the Brave, "the hole" for the Witch Hole). Never take a description
("charm", "fever", "his own doctrine") or a possessive. Lore kinds: propose the nearest of the board's kinds with a
one-line reason (a curse, power or rite → `magic`; a tale or song → `own` if the board has it, else NOT DONE: "a `lore`
or `tale` kind, Project settings → World kinds"). **Characters:** which registry character is which cast member is always
his ruling, even on an exact name. On Witchwood the registry's "Hunter" is the woodswoman, the board's "the hunter" is
another man, and the registry's "lurker" links point at the Witch. A registry character the board already holds as a
world entry (the men of the deep woods, a faction) stays where it is unless he says otherwise. Ask: "Is the registry's
Hunter the woodswoman? (the registry calls her the mother of the Boy; the board's 'the hunter' died in fall - 1)".

**2. Links.** The script's *ask* rule (the capital-letter share) is a screen, not the list: his prose writes his own
coined names lowercase ("the moonscarred trail", "the heartbox", "the nameless mountain"), so it flags far more than the
real risks. Read each flagged entry's matches in `links.md`. Where every match means the entry, it goes direct. Where a
lone match means something else ("the nexus of a clearing"), drop that scene. Ask him only about the entries whose name
is an ordinary word with other meanings in his prose (on Witchwood: "the darkness", "Cottage", the generic "Magic", and
"The Knots", which is also rope). His answer for one entry covers every scene; never ask per scene. A scene already linked is skipped.
Linking the Scene is enough: its Beats and micro-beats sit inside it.

**3. Era walk.** Besides the interludes, the script lists *past scenes not marked a flashback*: present-looking scenes where names that live in the past ("the woodsgirl") outnumber every other cast name. On Witchwood these were the Woodsgirl's midpoint chapters, which alternate with the present (Ch 40–46) and say nothing of "interlude". Read the chapters on either side of a flagged run, because a past scene that names no one (Ch 40, Ch 59) slips the screen. On a scene-sourced board (`eraSource: scene`) the era goes on the scene; a flashback's era applies to it
only, while a present scene's carries forward. That makes marking a scene a flashback a story call, because it stops the
scene carrying the present. Evidence for a proposal: the scene's own words first ("her father the night before he left
with the trapper" → summer - 1), then its DEV sequence note, then the arc plan. A season the words don't name is an open
line, never a guess. **Witchwood:** the present is `spring 3 - present` from Part 2 to the end (ruled 2026-10-22: it never
reaches summer), so propose no season turn there. List the Woodsgirl seasons no scene uses (fall - 1, summer - 2, …) as
facts for the report, not as gaps to fill.

**4. Seeds.** The tag is `seed:<id>-<name words>` (`seed:t09-widowsbane`), the same name for the payoff, so the seed check
pairs them. The span rule (DIR-019): *present* → propose. *Gone* → no tag, and one line in the report. *Reworded?* → one
batched question for the whole stage, each with the old quote, the card's words now, and "tag it here?". A thread whose
Planted line holds no quote ("devilkin dream-story, segment 1") is an open line, and so is a Settled thread with no paid
quote. Never pick a card for either by reading. An abandoned thread gets no tag. A thread with more than one quote takes
its first in story order.

**6. Events.** `pin-event` takes the card's era. The script ranks candidates in the event's own era first. A candidate in
another era means either the event's era is wrong or the scene's is. Usually stage 3 has just answered that, so re-run
the script after stage 3 lands. Propose a pin only where the card's words show the event; otherwise it stays unpinned as an
open line.

**7. Profiles.** Use the stage-1 mapping rulings, never the script's guess. A field that already has an answer is his: leave
it. An empty `notes` field gets his lines and the registry path; one with text keeps every word, and the new lines go
below it (`set-cast` writes the whole value, so build it as old + "\n\n" + new). A field the registry doesn't answer stays
empty.

**8. Idea admin.** The form-typed ideas need no reading. For the rest (995 on Witchwood), read in chunks of about 150,
using parallel subagents on a big board. Each gets its chunk from `ideas.json` `read` and the board's idea types, and
returns `{id, type}` from the words alone; when unsure it keeps `beat`. Twins in one scene are removed; the twin keeps his
words. The same words in different scenes are left alone and listed: an idea placed twice is not clutter. The `--ideas`
proof line must match before and after, because a retype changes no text and a removed twin leaves the distinct set as it
was.

## The report

`SYSTEM/reports/YYYY-MM-DD-<board slug>-world-walk.md`. Create it at stage 1 and add one section per stage as it closes, so
it reads as a whole run.

```
---
type: report
topic: World walk — <board>
date: YYYY-MM-DD
mode: branch-writing-expert, "finish the bible" (world walk)
board: "<board path>"
sources: board · <registry path> · <threads path> · <plan path>
runs: <the change-log run ids, one per stage>
words: "<before> = <after>"  (micro-beats and ideas)
---
# World walk — <board>

**Where the panels stand now.** <two to four plain sentences: what the World tab, seed check, timeline and cast now show,
and the biggest open gap>

## Stage N — <name>
<counts per kind written · his rulings in one line each · NOT DONE lines · open lines (no source answers) · the span-rule
log (gone quotes) · what this stage did not check>

## Still his
<his own entries, eras, tags and kinds left as he made them, to rename or remove: one line each>

## What this run did not check
<the script README lines, plus stages skipped and why>
```

## Talking to CRE, for this mode

Each list leads with the outcome and the count ("27 places, items and lore entries to add, 6 cast questions"). Then come
the lines, then one plain question: "approve all, or name the ones to change". Ask story calls as story questions ("Is
the registry's Hunter the woodswoman?"), never by field or code. Don't make him rule on the admin stages line by line: say
what will be written and its count, write it, and give the change list. Close each stage in one line naming what comes
next ("Next: linking the 63 scenes that name a place or item — say go"). Never start the next stage unasked.

## What this mode never does

Write, reword or reorder prose or an idea's words; place arc steps (plotting mode) or ideas (idea placement); add, rename or
remove a world kind, an era or an entry he made; write `REFERENCE/`, DEV, StoryLine or the chapter files; rewrite text
already on the board for clarity (the clarity walk did that, r62–r63); run unattended.
