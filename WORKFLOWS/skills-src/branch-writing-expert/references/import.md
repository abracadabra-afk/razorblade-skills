# Import mode — prose → board, verbatim; scenes wrapped at his breaks

Two cases: a **short story** (one note) and a **book** (a project's `CHAPTERS/<folder>/draft.md` files, one board per book).
The board must hold exactly the source text and nothing else; the structure on top is yours to propose and his to rule.

## 1. Verbatim first pass (one logged run, undoes whole)

`node scripts/board_tool.mjs import --source <note.md> --board <new board.md> [--title <his title>]`
`node scripts/board_tool.mjs import --book <project folder> --board <new board.md> [--title <his title>]`

The tool uses the plugin's own convert rule: headings become containers by rank (the heading line stays the card's body,
`#` included, exactly as the plugin's own Convert leaves it), every other block a prose card word for
word; it refuses to write unless every source block is on the board; the source files are read, never changed (their hashes
are in the log). A book board gets one Sequence per chapter folder, titled with the **folder name** (his words) and the
chapter number in `fields.chapter`, the draft's blocks under it; its frontmatter is marked `bw-working-copy: true` with the
source and the authority line (the pipeline's drafts stay canon until `^backlog-branch-writing-replacement-review` rules).
Source frontmatter is metadata, not prose: it is not imported, and the tool says so.

The target is a **new** file; the tool refuses an existing path, `REFERENCE/`, and pipeline paths. Pick the folder he names
(or beside the source); never inside a chapter folder.

**Onto a board he already built** (cast, eras, timeline in place) — `--into` instead of `--board`:
`node scripts/board_tool.mjs import --book <dir> --into <existing board.md> [--source-label "<where the prose lives>"] [--dry]`
(`--source` works the same). The same verbatim convert, appended under the board's Project card after everything already
there, as **one apply-kind run**: every card already on the board stays byte-identical (the tool refuses otherwise), and
"undo" takes out exactly the cards it added, frontmatter too. Prefer it whenever he names a board that exists — never
build a second board beside his and leave him to merge them. His prose kept as loose chapter notes (not
`CHAPTERS/<folder>/draft.md`) is staged first as sha-verified byte copies in folders named for the notes (his words);
`--source-label` then names the real notes in the frontmatter, never the staging path.

## 2. Structure

*Since 2026-10-19 (CRE: the levels above his prose are administrative):* the **scene wraps at his own breaks and the
dialogue types** are administrative — apply them as one run with a change list, no ruling list, then the break cards
themselves (`***`, kept word for word) go with `remove-break-card` once the Scenes export their own break, on his word.
**Cast candidates, speakers and POV stay story calls:** list them for him to rule (the cast candidates are mostly
capitalised words, not people — say so). After the import, the breakdown (`references/breakdown.md`) carries it up.
Before he works the board: dialogue tags `never` (`set-tag-mode`, on his word; a new-board import starts there).

The `propose` output is the source of those ops:

`node scripts/board_tool.mjs propose <board.md> --out <proposals.json>` reads the imported board and lists, each with a
reason and the op that would land it:
- **scenes** — runs of prose cards between scene-break cards (`* * *` and kin) → a Scene card wrapped around each run
  (the break card itself stays, word for word; deleting it is his click);
- **chapters** — a container whose title reads "Chapter N" → `chapter` field;
- **dialogue** — prose cards opening with a quote → type `dialogue`, with the speaker only where a plain "X said" tag names
  one (otherwise the speaker is his call);
- **cast** — names that tag dialogue or recur mid-sentence → cast cards;
- **pov** — every Scene with no pov: listed as open, **never guessed**. On a fresh import there are no Scenes yet, so
  this list is empty until the scene wraps land; if he names POVs, run `propose` again afterwards (or `set-field pov` on
  the Scenes he names). A book import has already set `chapter` from the folder numbers, so the chapters list is
  normally empty too — say so rather than leaving a blank unexplained.
- The speaker tag is read from the common forms ("X said", "said X", asked, called, whispered…); a line with none
  keeps the speaker blank for him.

(Before 2026-10-19 this was a ruling list:) one line each with the reason ("Scene around 4 blocks after the first break ·
begins 'The river…'"). He rules in one pass ("all", "all but 3 and 7", "2: the speaker is Mara"). Approved items go into one
ops file (copy each item's `op`, edit only what he changed; never copy a `pov` item whose value he left empty — an open POV
is no write) → `apply`. Rejected and unanswered items are not written and not re-asked. After the wraps land, run
`propose` once more: the POV slots now exist, and that list is what you show him if he wants to name POVs. Book and Part
cards: only if he asks for them (`add-card` by his title).

## 2b. A part's structure from the DEV tree (added 2026-10-20, the Witchwood board build)

Where the book has no prose yet, the structure comes from the DEV `sequences/` (and `scenes/`) files themselves — never the
crawl digests. Write a part plan (chapters as his containers with the DEV sequences each covers, matched by content and noted
in `fields.seq`; one Scene per DEV sequence or run of its beats; one Beat per DEV beat, each typed, titled, summarized; chains
with one line per Beat) and run `node scripts/dev_import.mjs <plan.json> --out <ops.json> --report <quotes.json>`. It refuses
unless every sequence the plan claims is covered beat for beat, once, and lifts each read's quoted lines, keeping only those
found word for word in the dictation floors the plan names (they become ideas on their Beat, `seq:NN` + `dev dictation`). When
his prose runs the DEV beats in another order, each Beat names the DEV beat it carries (`dev: n`) and the Beats follow the prose.
Prose goes in with `place-prose` per Beat; draft passages kept as source material with `add-idea from`. Example plan and
report: `SYSTEM/reports/2026-10-20-witchwood-part3-pilot*`.

**Arc steps go on lines, not loose on the scene (CRE, 2026-10-21).** A step is placed on the scene chain line of the Beat
that carries it — the first cited Beat when it spans several — so it reads as a beat on that line, not as a Need. In a part
plan each step names its Beat (`{"id", "on": "title:<scene>", "beat": n}`); a step with no Beat to carry it (an interlude
slot with no chain yet) stays on the scene only with a `sceneOnly` reason, otherwise `dev_import.mjs` refuses. On a board
built earlier, `scripts/step_lines.mjs <board> <plan.md>` does the same from each plan cell's cited board cards; a cell
that cites no board card (DEV or chapter cites only) is a placement for his ruling list, never guessed.

**A chapter's chain sits a level above its scenes (CRE, 2026-10-21).** Chapter 1 is the model: four lines for its two
present-day scenes, each scene linked to its run of two. A chapter runs about one line per scene or turn — at most two per
linked scene, three for a single scene with a turn — and its lines are written at chapter grain, never a copy of a
scene's own lines (the Part 3 pilot's single-scene chapters repeated their scene's chain and showed it twice, once as
"from Chapter N" above the scene). Interludes stay beside the chain. `dev_import.mjs` refuses a chapter with too many
lines for its scenes, or a chapter line whose words nearly match a line of a scene it links (measured against the longer
line; naming the same event is not a copy) — the test asks for a rewrite, it never writes one.

**A step that spans scenes becomes sub-steps (CRE, 2026-10-21: "yes, sub steps").** When a plan cell cites more than one
scene (a pinch or a midpoint that runs across scenes or chapters), the step becomes a parent with one sub-step per cited
scene — the plugin's own sub-steps, not markers or a new structure — each on the line of the Beat that carries it. Each
sub-step's words are the cell's own clause for that piece, split by its citations; no new wording. The parent keeps its
whole text and comes off the board as a category (`split-step` with `unplace`). Where the clauses can't be split cleanly
by citation — a cited scene with no clause of its own, one clause covering two scenes, a citation of a whole scene rather
than a Beat — the cell goes to his ruling list instead of a guess. In a part plan: `{"id", "parts": [{"text", "on":
"title:<scene>", "beat": n}, …]}`; on an earlier board, `step_lines.mjs` lists every spanning cell for this split rather
than putting it on one line.

**The neighbour check (CRE, 2026-10-21) — before any sequence's beats are built.** A DEV read can still carry a beat its
neighbour now holds: SEQ 24's beat 1 (back on the trail, the boy wanting to know what happened) was dictated before SEQ 23B
was recovered and slotted in ahead of it; 23B carries that stretch and ends on the cracks where 24 begins, so the pilot built
it twice-over as an empty Beat in the wrong place. The rule:
- Read each sequence's neighbours before building it — the previous and next sequence in the plan **and** the `prev:` /
  `next:` its own read names, even outside the part being built. Look hardest at inserted or recovered "B" sequences and at
  any note saying *slotted between*, *superseded*, *recovered*, *placement* or *this sequence's onset*.
- A beat a neighbour already carries is **never built twice and never dropped silently**: it goes to CRE's ruling list as
  "resolved against SEQ X — confirm", with what decided it.
- Where a landed or Drive draft covers the stretch, **the draft's order decides which sequence owns the beat** (here: Drive
  CH 15 holds the questions and the hike and ends on the cracks; CH 16 opens on the shatter → 23B owns it).
- `dev_import.mjs` enforces it: it flags every seam with a "B" sequence, a note in either read naming the other, or edge beats
  whose words overlap, and refuses until the plan's `seams` resolves each one — `{"between": ["SEQ 23B", "SEQ 24"],
  "carried": [{"seq": "SEQ 24", "beat": 1, "by": "SEQ 23B", "byBeats": "1–4", "decidedBy": "<the draft order, or the
  reason>"}]}`, or `{"between": [...], "clear": "<why nothing repeats>"}`. Whether a beat is really carried is a reading
  call written into the plan; the overlap score only asks, it never decides (DIR-014). A carried beat counts as covered,
  is built nowhere in its own scene, and prints (and writes with `--rulings <file>`) as the ruling list line. Dropping a
  beat without a seam entry, or carrying one without `decidedBy`, is refused.

## 3. Close

Change list: the import line (cards, blocks, sources untouched) and the structure lines. "Undo the last run" after the
structure run restores the plain import; a second undo removes the board file (the import whole); redo brings either back.
Summaries, beat groupings and intensity values stay blank or arrive later as tagging-mode offers.

Never: edit the source note or the chapter drafts; reword or drop a block; invent a speaker, a scene title or a POV; export
back into `draft.md`; decide which copy is canon.
