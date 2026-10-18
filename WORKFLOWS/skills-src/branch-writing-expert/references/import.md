# Import mode — prose → board, verbatim; structure proposed, ruled, then landed

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

## 2. Structure: propose, rule, land

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

Show them to him as one ruling list, grouped, one line each with the reason ("Scene around 4 blocks after the first break ·
begins 'The river…'"). He rules in one pass ("all", "all but 3 and 7", "2: the speaker is Mara"). Approved items go into one
ops file (copy each item's `op`, edit only what he changed; never copy a `pov` item whose value he left empty — an open POV
is no write) → `apply`. Rejected and unanswered items are not written and not re-asked. After the wraps land, run
`propose` once more: the POV slots now exist, and that list is what you show him if he wants to name POVs. Book and Part
cards: only if he asks for them (`add-card` by his title).

## 3. Close

Change list: the import line (cards, blocks, sources untouched) and the structure lines. "Undo the last run" after the
structure run restores the plain import; a second undo removes the board file (the import whole); redo brings either back.
Summaries, beat groupings and intensity values stay blank or arrive later as tagging-mode offers.

Never: edit the source note or the chapter drafts; reword or drop a block; invent a speaker, a scene title or a POV; export
back into `draft.md`; decide which copy is canon.
