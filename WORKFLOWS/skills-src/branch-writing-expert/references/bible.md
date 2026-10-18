# Story-bible setup — at build time, never invented

A board built from a plan arrives with its side panel bare: no era (every beat "not in any era yet"), profile `role` blank,
no relationships. The setup fills what the plan and the model already state, and nothing more. Run it right after a
plotting-mode build, or when CRE says "set up the bible" on a board.

## What lands as an instruction (his plan or the model states it)

- **A placeholder era when none is named.** `add-era` with name `Placeholder era` and label `no era named yet — rename it`.
  A lone era is not the story's start until a second exists (DECISIONS 2026-10-14 BW U13), so this is safe to add; he
  renames or splits it when he knows the periods. Then `file-beats-in-era` so every unplaced step is in time; placed steps
  take the era of the card they sit on, and a container with no era of its own is in the first era by the plugin's own
  rule (schema §5d), so nothing more is set. Arcs carry no era of their own (design note 2026-10-18).
- **Profile `role` from the model role**, only where the mapping is stated: a model `antagonist` → profile `antagonist`.

## What is proposed (a mapping or a reading you made)

Show these as a ruling list with the model's words as the reason; land only what he approves:
- `role` for the other model roles — the profile's options are protagonist / main / supporting / antagonist, the model's
  are lead / deuteragonist / X1–X4 / AM1–AM5. Default mapping offered: lead → protagonist; deuteragonist and X1–X4 → main;
  AM1–AM5 → supporting. He may answer "all defaults".
- **Relationships only where roles state them**, with the board's relation types: AM1 mentor → `mentor` of the lead
  ("Mentor / steadfast ally"); the antagonist and the lead → `enemy`; a deuteragonist's `against` → `enemy`; AM2
  Relationship (B-story) → the type he names (the model says "Bond", the board has `lover`, `friend`…: ask). Nothing for X1–X4,
  AM3–AM5 unless he says.
- Multi-era characters: per character, own full spine / short anchored arc / feeds the setup (ask once each).

## Never

A Place, Item or System the plan doesn't hold; an era name beyond the placeholder; an event; a stage or era mapping; a
relationship the roles don't state; a profile answer he didn't give. The bible is his to fill, and a plausible invention is
the hardest kind to spot.
