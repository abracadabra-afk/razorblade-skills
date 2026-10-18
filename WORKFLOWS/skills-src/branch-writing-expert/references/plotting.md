# Plotting mode — the Interlocking Arc Model (the former interlock-plotter)

CRE structures his ensemble novels (1 to N POV leads; his first book has five) with the **Interlocking Arc Model** — three
35-beat spines (lead internal, antagonist, external plot), failed-mains exits X1–X4, a deuteragonist, switches K1–K8,
anchor maps AM1–AM7 and collision rules CR1–CR4. The model text is his, verbatim: `WORKFLOWS/interlocking-arc-model.md` —
read it now (only now), never edit it. Your job is the administrative assembly: his story information into a plan, beat by
beat, in his words; the board built from the plan once he approves it; collisions and locks reported as facts.

Extra rules for this mode, beyond the skill's:
- **Observations, never verdicts** (CDIR-004). Collisions, K-R1 locks and blanks are facts; whether the structure is locked
  enough to write against is his call. Never write "ready", "complete", "passes" or "fails" about a board.
- **One question per decision, with "open" as the default.** Never default a story call to an option you made up.
- **The plan is the record.** Every write to it goes through `scripts/plan_tool.py`, which keeps the JSON valid and
  regenerates the readable table. Save after every round: if he stops anywhere, the next run resumes at the first unwalked
  group (`plan_tool.py status`).
- **The builder writes a new board or a copy, never an existing file** (its own refusal). Plotting a live board means
  building a copy beside it and telling him so; the rest of the expert's modes then work on whichever he keeps.

Tools (Git Bash on the desktop):
- `python -I scripts/plan_tool.py …` — new / set --json-file / beat / walk / walked / render / approve / status.
- `node C:\Users\Chad\dev\branch-writing\tools\build-plan.mjs <plan.md> [--dry]` — plan → board, outside Obsidian.
- `node C:\Users\Chad\dev\branch-writing\tools\check-board.mjs <board.md> --out <report.md>` — the check report.
- `node C:\Users\Chad\dev\branch-writing\tools\make-iam-templates.mjs --check` — the 13 IAM templates match the model.

Plans: `WRITING/BOARD PLANS/<board> - arc plan.md` (test runs keep plan, board and check together in their test folder under
`SYSTEM/skill-tests/branch-writing/_work-*`). Check reports: `SYSTEM/reports/YYYY-MM-DD-<board>-interlock-check.md`.

## "interlock the arcs" — the full run

**1. Target.** Ask once: a new board (name, folder) or a copy of an existing board (which; the copy gets a new name). Then
`plan_tool.py new <plan> --board-path … --title … [--copy-of …]`.

**2. Cast and roles.** Take the names he gives (aliases, any profile answers — want, flaw, need — in his words). Ask **one
role per character**, every roster lead included: lead, antagonist, deuteragonist (and who they face, D1), an exit X1–X4,
an anchor AM1–AM5, or none. A non-character antagonist (K4 force) is a cast entry named for the force. Ask whether
Statement Plotting is on and who the POV leads are; the model lead is the first roster lead. Record with
`plan_tool.py set --json-file part.json` — write the JSON to a file first:

```json
{"cast": [{"key": "ash", "name": "Ashley Vane", "aliases": ["Ash"], "profile": {"flaw": "his words"}}],
 "roles": [{"cast": "ash", "role": "lead"}, {"cast": "kit", "role": "deuteragonist", "against": "mara"},
           {"cast": "wen", "role": "AM1", "beats": {"resolves": 31}}],
 "plotting": {"on": true, "leads": ["ash", "bo", "wen"]},
 "switches": {"K2": "V2"},
 "structure": [{"kind": "sequence", "title": "The Bridge", "under": null}]}
```

Roles: `lead`, `antagonist`, `deuteragonist` (+ `against`), `X1`–`X4`, `AM1`–`AM5`. `set` replaces a list key whole (`cast`,
`roles`, `structure`); `switches` and `plotting` merge. At 5 leads every lead needs a role; say plainly which still have none.

**3. Switches.** K1–K6 one at a time, each **open** until he picks (the model's options exactly; the tool refuses others).
As soon as both sides of a lock are set, name it as a fact, quoting the model (K-R1; the V × PH cell). K7/K8 are derived.

**4. Beat walk.** One model group (5 beats) per round, seven rounds: Setup 1–5, Incident 6–10, Trials 11–15, Pinch 1 16–20,
Mid-Point 21–25, Pinch 2 26–30, Final Showdown 31–35. Each round: `plan_tool.py walk --beats a-b`, show him the sheet (the
three spine labels, the role slots that land there, under each "asks: …" in the model's words), take his words:
`plan_tool.py beat --n 17 --spine external --text "<his words>" [--who keys] [--src "chat <date>"]`.
`--spine` is `external`, `lead` or `antagonist`; for any other role the role code with the character's key (`--spine X2
--cast bo`, `--spine deuteragonist --cast kit`, `--spine AM1 --cast wen`).
- His words go in **verbatim**. A fragment he chose stays a fragment.
- Someone his words name who isn't cast: ask once whether to add them and to the beat's `who`. Never add a person yourself.
- "Skip", silence or "later" → **no call**; a beat the plan doesn't list is an open, labelled blank. Don't ask twice.
- After each round `plan_tool.py walked --beats a-b`; tell him where the walk stands in one line.
- A beat number means what the builder reads: the step at that beat; else the compressed step whose rows span it; else the
  one step carrying that beat. Compressed steps hold a range: ask once for the step, not once per beat.
- An anchor's open beat ("29 lost, or 31 if they survive") is his pick → the role's `beats` (`{"resolves": 31}`) via `set`.
- K2 V2/V3: the lead's B34 has 34a and 34b (`--n 34 --spine lead --sub a` / `--sub b`); the deuteragonist's Moment of Truth
  at 34b is its own B34 (`--n 34 --spine deuteragonist --sub b`).

**5. Placement (optional).** Only onto containers he names: `structure` via `set` (`{"kind": "sequence", "title": "The
Bridge", "under": null}`, `{"kind": "scene", "title": "The far bank", "under": "The Bridge"}` — a scene names the sequence
it sits under), then `beat --n … --spine … --at "seq:<title>"` or `--at "scene:<title>"` (the prefix is a reminder; the
builder matches the title). No default structure; an unplaced step waits in the Characters panel. **Lead exits (known gap, plugin
0.62):** the plugin honours a lead's exit only on a **unit** (a Scene-level card); the builder writes the exit onto
whatever container holds the exit step, so an exit step placed on a Sequence reads "stays to the end" in the Plot tab.
Until the fix lands, place an exit lead's exit step on a **Scene** (name it under its sequence in `structure`) or tell him
after the build that the exit needs a scene; never patch the board by hand.

**6. Plan → approval.** `render`, show a one-screen summary (cast and roles, switches, filled/open counts, the
`build-plan.mjs <plan> --dry` preview — anything "NOT DONE" goes to him now). Wait for **"approve the plan"**; only then
`plan_tool.py approve --phrase "<his exact words>"`. Any later change takes the approval off.

**7. Build.** `node …/build-plan.mjs <plan.md>` writes the new file (or copy), parse-gates it, prints what it made and
anything it could not do. Report that list plainly; "NOT DONE" goes back to him as a question.

**8. Story-bible setup.** `references/bible.md`: the placeholder era + beats filed in it land now (one ops run); roles and
relationships go to him as the ruling list.

**9. Check.** `node …/check-board.mjs <board.md> --out <report>`. Tell him the counts by kind (locks, collisions, order,
notes, open blanks) and the one or two that might change a decision. Never call the board locked, done or ready. On the
board itself the Visuals pane's **Interlock** tab (0.62+) draws the same grid; point him there.

## "build the interlock board" — steps 7–9 from an approved plan (if it isn't approved, say so and stop).
## "check the interlock" — step 9 only, on the board he names (read-only; a live board is fine).
