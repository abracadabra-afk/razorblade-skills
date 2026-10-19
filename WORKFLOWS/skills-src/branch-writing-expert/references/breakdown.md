# Breakdown mode — the administrative levels above his prose

CRE (2026-10-19): "the prose level (microbeats) are my words - those are hands off. But the levels above it are
administrative." And: "this is a plotting and planning tool, separation and identification of the chains is what i built
it for so I can identify what is missing, write the draft text for each piece, and export those pieces into a working draft
that I can then format and modify as I like (knowing everything is inside)." With ADHD, pieces identified on the board beat
scanning a block of text for what is there.

So this mode reads his prose and **writes the structure above it directly** — no ruling list first, every run logged and
undoable — one chapter (a Sequence) at a time, **piloting the first chapter** and letting him read it on the board before
the rest. His words are the forbidden zone: never changed, added, dropped or reordered. Paragraphing is not protected (the
export is his working draft).

## What a chapter ends up as

```
Sequence (the chapter)   title (his folder name, kept) · summary · goal holder · chain ENTRY → BUT/THEREFORE → EXIT
 └ Scene                 title · summary · goal holder · chain: ONE LINE PER BEAT · linked to the chapter's line(s)
    └ Beat               type (setup/hook · escalation · scene-climax · valley · outcome/hook) · title · summary
       │                 linked to its scene line · NO chain of its own (unless he gives it one)
       └ micro-beat      his words, one beat each, typed (action · reaction · epiphany · interiority · sensory/setting ·
                         transition · dialogue)
```

- **Depth (CRE, 2026-10-19): chains stop at the Scene.** A Beat is the contract he fills — type, title, summary, its
  micro-beats under it. "Beat to microbeat is a drill too far." A beat he wants choreographed (a fight, each back and forth
  a BUT / THEREFORE) gets a chain from the beat's **+** in the plugin, on his click; only then are its micro-beats placed in
  slots (`place-in-bloc`), and only on his word.
- **The chapter's chain → its scenes:** each present-day scene carries a run of the chapter's lines (`link-from`, e.g.
  ENTRY + BUT → scene 2, THEREFORE + EXIT → scene 3). One line feeds one scene, so a scene's ending lives on the chapter's
  last line of its run — write it there.
- **A flashback interlude** (an italic memory opening a chapter) is its own Scene with an era **on the scene** ("only here",
  the chapter keeps the present). It stands beside the chapter's chain, not linked into it. Its era is a story call: resolve
  it against his own timeline events first ("resolved against your 'baby in fire' event — winter 2.1, confirm") and leave the
  rest for him to name. A chapter's own present-day era goes on the **chapter**, and carries forward to the next chapters.
- **The scene's chain → its beats:** write the scene's chain with exactly one line per beat (ENTRY = the first beat, EXIT
  = the last, BUT / THEREFORE between), then link each beat to its line. A step the scene is missing then shows as a line
  with nothing under it — the reason he built the tool.

## The runs (each one undoable on its own)

1. **Read.** `board_tool.mjs read <board> --full`; dump the chapter's micro-beats with ids and types. Re-hash the board and
   compare with the last run's after-hash (`log`): if they differ he edited it — read again.
2. **Split** — one micro-beat per beat it fires, at the sentence where the type changes (his example: "Snow fell … It
   cried." sensory/setting → "Cried and cried … into the fire." action → "It screamed there …" reaction). Sentence breaks
   only; a quote with its own tag ("…," she said and stood up.) stays one dialogue piece. Spec → `scripts/split_plan.mjs` →
   ops; `scripts/words.mjs` before and after — they must match.
3. **Type** every untyped micro-beat (`set-type`; the tools refuse `dialogue` on a card with no opening quote).
4. **Group and carry up** — one plan per chapter → `scripts/admin_plan.mjs` → one ops file: `regroup-beats` per scene
   (runs of micro-beats, in order, all covered, each Beat typed, titled, summarized), scene title / summary / goal holder /
   chain with `linkBeats: true`, the chapter's summary / goal holder / chain and `links` (scenes → chapter lines). Titles,
   summaries and chain lines are yours, plain, and say what the prose already does — never what it should do.
5. **Prove it.** Words hash unchanged; the board round-trips; read the chains back through the plugin (`chainLines`,
   `pointRun`) and say so in one line. On a new op or a big run: a scratch copy first (`--log-dir` in the scratchpad), with
   export and undo byte-identity checked.
6. **Hand it over.** Tell him to reopen the board tab (an open tab can miss outside writes). Show the change list. Pilot
   chapter: ask whether it reads right before the next chapters — his read is the gate, not a measure of yours.

## Eras on a scene-sourced board (plugin 0.64)

On his word, a board's eras come from its scenes (`set-era-source`): a present scene's era carries forward; a
**flashback** scene (`set-flashback`) keeps its era to itself; Books, Parts and Sequences show the rolled-up span. **Before
switching a board over, mark every interlude a flashback** — an unmarked interlude would count as the present and drag the
timeline into the past. A line that remembers rather than thinks is a micro-beat of type `memory` (`add-beat-type` once,
then `set-type`), with `set-remembers` naming its era when known: a broad bucket (Childhood, Teenage) for an unplotted
memory, a season for one tied to a plotted event. Interiority stays present-tense thought. Which lines are memories is
administrative; which era a memory remembers, and which scenes are flashbacks, are story calls — resolve against his
timeline and list them for him.

## Still his

POV, eras he hasn't placed on his timeline, cast entries, speakers, merging dialogue into conversations (his click in the
plugin: Shift-select a run, right-click, Merge — action lines and named tags come in), Complete marks, a beat's own chain,
and any call he says is his.

## Plan shapes

`splits.json` — `{ "<card id>": [["<type>", "<the piece's opening words>"], …] }`

`chapter-plan.json` — `{ "sequence": {"id", "summary", "goalHolder", "chain": {"entry", "turns": [{"k", "text",
"outcome"?}], "exit": {"k", "text", "outcome"?}}, "links": [{"scene", "lines": [a, b]}]}, "scenes": [{"id", "title",
"summary", "goalHolder", "chain", "linkBeats": true, "beats": [{"type", "title", "summary", "cards": [ids]}],
"micro": {"<id>": "<type>"}}] }`
