---
type: workflow
name: brainstorm-walker
status: draft — source authored 2026-09-06 off the ratified intent; packaging pending (desktop pack-skills.ps1, DIR-009); graduates after 2–3 live runs
triggers: ["build the walker", "prep the brainstorm"]
lane: 5 (writing-ops) + 1 (fiction)
intent: "[[WORKFLOWS/intents/brainstorm-walker]]"
created: 2026-09-06
last_updated: 2026-09-06
revision_note: "v1 — built 2026-09-06 from WORKFLOWS/intents/brainstorm-walker.md (ratified same day). Companion edits landed in the same build: brainstorm Inputs name the walker's typed notes as a second input; episode-harden step 7 offers 'build the walker' at the stamp; pipeline S2 row names the walker as what CRE carries to the mic; _SKILLS MAP trigger row."
---

# brainstorm-walker

The **coverage document CRE carries into the S2 dream-catching brainstorm** on a Writing Is War episode. It runs after `episode-harden` stamps `shape.md` and before the brainstorm, reads the ratified shape, the blueprint, the gated premise, the candidate's arc chain and the shared `SHORTS/DEV/registry/` read-only, asks him nothing, and derives one file into the episode folder: `walker.md`. The file opens with a one-screen refresher of the story's mechanics lifted verbatim, then four episode-level cues left blank (the opening line or image, the closing line or image, the reader's experience during and after), then one block per shape entry — the committed line as the reminder, seven lens questions (dialogue, imagery, action, reflection, setting, character, feel) headed in the S2 cue grammar, and an empty notes slot — walk, then cast, then setting, agenda last. He speaks to it at the mic or types into it at the desk; typed notes become a second input to `brainstorm`.

**The problem it exists to kill:** when CRE rambles at the mic he follows no checklist, and when he comes back to a story after time away he has lost its mechanics. Harden commits the spine; the brainstorm is where he spends himself on the aesthetic layer. Without a guiding document the brainstorm covers whatever he happened to remember. With it, he knows when he finishes that he had the opportunity to review the entire story, whether he addressed every portion or not.

**A derive, never a second spine.** The walker mirrors the ratified shape (DIR-019 §1). It never reopens a ruling, never proposes a beat, and nothing downstream grades the brainstorm against it — skipping a cue is legal (DIR-017 §2). Collisions between what the mic moves and the ratified shape stay with `episode-feedback`.

## Pipeline position — inside S2 of the episode route

```
S1.75 HARDEN              episode-harden → shape.md, status: ratified; offers "build the walker" at the stamp
      WALKER              ← this workflow — walker.md, carried to the mic or the desk
S2    dream-catching      brainstorm (transcript + walker notes) → dev-capture into WRITING/SHORTS/DEV/
S3    synthesis + REGEN   episode-feedback, then episode-blueprint run 2 reads shape.md
```

The walker adds no route step. Trigger-called; harden offers it in one line at the stamp (CRE says yes or not).

## When to use

CRE says **"build the walker"** or **"prep the brainstorm"** on a WIW episode whose `shape.md` is ratified and whose S2 brainstorm has not run. Also on a re-ratified shape (regeneration carries his notes). Do NOT use it to synthesize the brainstorm (`brainstorm`), to carve the runway (`episode-runway`, S4), to ask or commit a pillar, cast fact or setting fact (`episode-harden`), to plan budgets or rule GO (`episode-blueprint`), to surface collisions (`episode-feedback`), to punch-list a DEV tree (`dev-readiness`), or to tally which cues were touched (not in v1 — a watch item after two live runs).

## Inputs (all read-only)

- `shape.md`, `status: ratified` — **required**; missing → route to `episode-harden`; draft → stop, the spine is not committed. Every tagged entry (want, MoT, ending, rungs and their sub-lines, flaw, cast, setting), the knot, the anchor, the curve, the agenda.
- `premise.md` — frontmatter tier / container / POV; § The premise, verbatim.
- `blueprint.md` — frontmatter curve; § Incident and § Choice; **never below the `## Your notes` rule**.
- The source candidate's `triage.md` `## Arc chain` (path from `premise.md` `source_candidate`) — the Choice and Mirror lines; absent → recorded in `sources_read`.
- `WRITING/SHORTS/DEV/registry/` — names and first lines only: the recurring characters, places and lore already banked across episodes.
- **Never `draft.md`** (plan-only, CRE-ruled 2026-09-03). **Never `WRITING/SHORTS/DEV/scenes/`** — this episode's S2 has not run and other episodes' scenes are noise here.

## Output — `walker.md`

Serialized frontmatter (DIR-004): `type: brainstorm-walker`, `episode`, `shape_ratified`, `shape_fingerprint` (the regenerate trigger — a hash of the shape, not a status field, per DIR-010), `status` (`current` | `superseded`), `superseded_by`, `block_count`, `sources_read` (with the not-read line), `generated`, `tool`, `note`. Body, in order:

```
# EP NN - TITLE · walker
## Refresher                 knot · anchor · curve · gate line · the premise (folded, verbatim) ·
                             mechanics (Choice, Incident, Mirror, want, MoT scopes, ending, flaw) ·
                             cast one-liners · setting · the shape's agenda · banked in the registry
## Episode-level cues        4 slots — scene — the opening · scene — the closing ·
                             project level — the reader, during · project level — the reader, after
## The walk                  one block per entry in the shape's walk order: want, MoT, ending, rungs
                             from the anchor down (sub-lines ride with their rung), flaw
## Cast                      one block per member (sub-lines ride with the member)
## Setting                   one block per setting line
## Brainstorm agenda         LAST — carried whole, one notes slot per line; the ⚑ open blocks listed once
---
## Your notes                the catch-all; CRE's; carried verbatim on every regeneration
```

**A block:**

```
### E3  [⚑ open if any line is NOT NAMED — CRE]

- <the shape's E3 line, verbatim, tag included>
- <E3's sub-lines, verbatim>

- **scene — E3** · dialogue — <question>
- **scene — E3** · imagery — <question>
- **scene — E3** · action — <question>
- **character — E3** · reflection — <question>
- **place — E3** · setting — <question>
- **character — E3** · character — <question>
- **what I love about this — E3** · feel — <question>

**Your notes:**
```

The bold head is the spoken cue (`WRITING/SHORTS/DEV/_DEV_MAP.md` cue table); he says it before he answers and `dev-capture`'s deterministic layer routes on it. Heads are fixed per lens so the same lens always speaks the same head. Questions are fixed templates parameterised only by the entry's own label; the script carries no story material. A block holding a `[NOT NAMED — CRE]` line is flagged `⚑ open` and switches to the open-hole templates — those are the holes S2 exists to fill.

## Steps

1. **Sentinel** (`^obs-004`), then **`_CREATIVE DIRECTIVES`** before any episode file (DIR-002 creative-lane load). Attended or unattended alike — generation asks nothing and rules nothing.
2. **Locate + preconditions** — the episode folder; `shape.md` present and ratified; S2 not banked (the script probes `DEV/_intake/_audit/` for a brainstorm floor naming the episode — never `scenes/`); an existing walker whose fingerprint matches the shape → nothing moved, stop.
3. **Derive** — `python scripts/walker.py derive --root <vault> --episode "EP NN - TITLE"`. Existing `walker.md` → regeneration: every filled notes slot carried verbatim by block key, the tail carried, orphans (a renamed shape line) to `## Carried notes`, never dropped; an orphan goes home if its block returns.
4. **Check** — `python scripts/walker.py check <walker.md> --shape <shape.md>`: frontmatter parses; section order with the agenda last before the rule; four episode-level slots; seven lenses per block with cue-grammar heads in question form; a notes slot per block; no quoted speech in a question; **no word in a question that is not template vocabulary or already on the block's reminder lines** (the no-proposed-content floor); every tagged shape entry and agenda line present verbatim. The `not checked:` line names the remainder (DIR-018): whether a question is really a question or a beat wearing a question mark, whether a lifted line is still what the shape says today, whether a carried note is complete.
5. **Re-read through the file tools** (DIR-005), then present in one plain sentence: what he is carrying, where it is, the open flags.
6. **Lifecycle** — regenerate when `shape.md` is re-ratified; `supersede --by <sheet>` once the brainstorm sheet ratifies (stamps status + `superseded_by`, body untouched); never rule on the walker.
7. **Log** — `_CHANGELOG` top-insert; `_OBSERVATIONS` for tool surprises; `_CREATIVE OBSERVATIONS` (`^cobs`) for craft observations, automatically (DIR-003).

## Sharpening a question — only under the floor

The templates are generic on purpose: they cannot author. A question may be sharpened toward its committed line **only** with words already on that line, and `check` re-run — a sharpened question that introduces a noun, verb or image the reminder does not carry is a proposed beat, and the checker fails it. In doubt, keep the template.

## Stop conditions

Sentinel fails · no episode folder or ambiguous · no `shape.md` (route to `episode-harden`) · `shape.md` not ratified · S2 already banked for this episode (offer `supersede`) · the walker already mirrors the current shape (nothing moved) · a secret in any read file (DIR-001).

## Guards (each with its reason)

- **Reads the sources read-only and asks CRE nothing during generation** — the spine is committed; the walker mirrors it rather than reopening it (DIR-019 §1, CDIR-009).
- **Never reads `draft.md`** — the plan-only rule stops prose being mined into plans (CRE, 2026-09-03). **Never reads `SHORTS/DEV/scenes/`** — S2 has not run and other episodes' scenes are noise.
- **Every prompt is a question about a committed entry, never a beat, image, line or option** — a proposed one authors the story (CDIR-003). The opening, closing and reader-experience slots are asked and left blank.
- **Reminder lines lifted verbatim in the carve register, tags included** — craft content is his (CDIR-002) and a paraphrase drifts.
- **Coverage, never obligation** — nothing downstream grades the brainstorm against it and skipping a cue is legal, because a runway is a flow-kickstarter and divergence is a win (DIR-017 §2), and because a checklist that assigns obligation before arrival is the failure CRE ruled out on 2026-08-26 ([[DECISIONS/2026-08-26 witchwood-dev-authority-layers|dec-030]], the discarded must-arrive/available classing).
- **Heads in the S2 cue grammar** (`_DEV_MAP` cue table), fixed per lens — `dev-capture`'s deterministic layer keys on those heads and a spoken cue that matches routes without inference.
- **Every `[NOT NAMED — CRE]` entry carried as a cue flagged open; the shape's agenda carried whole** — those are the holes S2 exists to fill (DIR-018 shape).
- **Notes slots empty at generation, carried verbatim on regeneration, orphans never dropped** — the notes are his material and a clobbering regenerate costs him the session.
- **Regenerate on re-ratify; stamp `superseded_by:` when the sheet ratifies; never rule on the walker** — it is a derived artifact (DIR-019 §1). The regenerate trigger is a fingerprint of the shape, not a status field (DIR-010 §5).
- **Writes only `walker.md`** — `WRITING/SHORTS/DEV/` is `dev-capture`'s; `shape.md`, `blueprint.md`, `premise.md` are other tools' outputs.
- **Serialized, parse-gated frontmatter; file-tool writes; re-read after** (DIR-004, DIR-005).

## Evals

Objective parts only (`WORKFLOWS/skills-src/brainstorm-walker/evals/`): every tagged shape entry has a block carrying it verbatim; each block has the seven lenses with cue-grammar heads and an empty notes slot; the four episode-level slots present; frontmatter parses; regeneration preserves filled notes slots on a fixture; the fixture vault's `draft.md` and `DEV/scenes/` sentinel tokens never appear; the blueprint's below-the-rule line never appears. Run: `python scripts/walker.py check <fixture> --shape <fixture shape>` — `pass-*` exit 0, `fail-*` exit 1. Whether a prompt is a question or a beat is CRE's gate and is deliberately not eval'd. Fixtures are synthetic (EP 95 - FIXTURE LANTERN), not CRE material.

## Relationship to the rest of the OS

- **Upstream:** [[WORKFLOWS/episode-harden]] (S1.75 — `shape.md`, ratified; offers this at the stamp) ← [[WORKFLOWS/episode-blueprint]] run 1 ← [[WORKFLOWS/episode-init]] ← [[WORKFLOWS/premise-forge]] DEEPEN (the arc chain read here).
- **Downstream:** [[WORKFLOWS/brainstorm]] (S2 — the transcript **and the walker's typed notes** are its inputs) → [[WORKFLOWS/dev-capture]] (routes the ratified sheet into `WRITING/SHORTS/DEV/`; the walker's cue heads are its vocabulary) → [[WORKFLOWS/episode-feedback]] (S3 — the collision seam) → [[WORKFLOWS/episode-blueprint]] run 2.
- **Cue grammar:** `WRITING/SHORTS/DEV/_DEV_MAP.md`.
- **Route:** [[WORKFLOWS/pipeline]] episode route v4, S2 row; [[WORKFLOWS/intents/wiw-route-v4]].
- **Intent:** [[WORKFLOWS/intents/brainstorm-walker]] (ratified 2026-09-06). Open items it carries: first live target (EP 04 if its S2 has not run when the skill installs, else EP 05); chaining from the harden stamp stays trigger-called.
- **Siblings / not this:** `episode-harden` (commits the spine; this reads it) · `brainstorm` + `dev-capture` (synthesis and routing, downstream) · `episode-runway` (S4 drafting carve) · `episode-blueprint` (budgets, verdict, both runs) · `episode-feedback` (collision seam) · `dev-readiness` (gap punch list over a DEV tree, read side) · `interview-me` (not called; generation asks nothing).

## Run log

**2026-09-06 — built.** Source at `WORKFLOWS/skills-src/brainstorm-walker/` (SKILL.md + `scripts/walker.py` derive / check / supersede + evals with a synthetic fixture vault and four fixtures). Verified in the sandbox against a copy of EP 04 (18 blocks: 9 walk · 4 cast · 5 setting; `check --shape` PASS; regeneration carried notes, tail and orphans across two shape moves and returned an orphan home). The live EP 04 folder was not written. Packaging is CRE's, on the desktop (`pack-skills.ps1` → sha-verify → Save-skill, DIR-009); the session's skill list is snapshotted at boot, so the first run needs a fresh session. Description 992 chars, quoted, no angle brackets.
