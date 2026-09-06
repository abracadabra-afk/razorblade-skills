---
name: brainstorm-walker
description: "Derive walker.md, the coverage document CRE carries into the S2 dream-catching brainstorm on a Writing Is War episode whose shape.md is ratified and whose brainstorm has not run. Reads shape.md, blueprint.md, premise.md, the candidate's arc chain and the shared SHORTS/DEV registry read-only, asks nothing, and writes one file: a one-screen refresher lifted verbatim (knot, want, MoT question and answer scope, ending, cast, setting, agenda, banked registry), four blank episode-level slots (opening line or image, closing line or image, reader experience during and after), then one block per shape entry with the committed line, seven lens questions (dialogue, imagery, action, reflection, setting, character, feel) headed in the S2 cue grammar, and an empty notes slot. Coverage, never obligation; regenerates on re-ratify carrying typed notes verbatim. Use when CRE says build the walker or prep the brainstorm. Not the brainstorm synthesis, the runway carve, harden, or a coverage tally."
---

# Brainstorm Walker

You are building the **coverage document CRE carries into his dream-catching brainstorm** on a Writing Is War episode. When he rambles at the mic he follows no checklist, and when he comes back to a story after time away he has lost its mechanics. `episode-harden` has already committed the spine to `shape.md`; the brainstorm is where he spends himself on the aesthetic layer — conversation, looks, feel, vibe — over that locked spine. The walker puts the story back in front of him and hands him a cue for every part of it, so when he finishes he knows he had the chance to review the whole story, whether he addressed every portion or not. He speaks to it at the mic or types into it at the desk; typed notes become a second input to `brainstorm`.

Three things shape everything below:

- **The walker mirrors the shape; it never reopens it (DIR-019 §1, CDIR-009).** Every reminder line is lifted verbatim, with its tag. You ask CRE nothing during generation. A derived artifact is regenerated, never ruled on.
- **Every prompt is a question about a committed entry, never a beat, image, line, or option (CDIR-003).** A proposed one authors the story. The script's templates are fixed and carry no story material; the opening, closing, and reader-experience slots are asked and left blank.
- **Coverage, never obligation (DIR-017 §2; CRE, 2026-08-26).** Nothing downstream grades the brainstorm against the walker. Skipping a cue is legal. A checklist that assigns obligation before arrival is the failure he ruled out.

Canonical doc: `WORKFLOWS/brainstorm-walker.md`. Intent: `WORKFLOWS/intents/brainstorm-walker.md`. Route canon: `WORKFLOWS/pipeline.md` episode route v4, row S2.

---

## Position — inside S2, between harden's stamp and the mic

```
S1.75 HARDEN              episode-harden → shape.md, status: ratified
      WALKER              ← this skill — walker.md, carried to the mic or the desk
S2    dream-catching      brainstorm (transcript + walker notes) → dev-capture into WRITING/SHORTS/DEV/
S3    synthesis + REGEN   episode-feedback, then episode-blueprint run 2
```

The walker adds no route step. `episode-harden` offers it at the stamp; it is trigger-called, never chained automatically.

---

## Step 0 — Sentinel, then the creative-lane load

From the mounted vault root, read `_DIRECTIVES.md` and confirm frontmatter `type: ai-os-brain` + `file: directives`. Missing or mismatched → **halt and ask** which folder is the vault.

Then read `_CREATIVE DIRECTIVES.md` (CDIR-001–010) **before opening any episode file** — Lane 5 + Lane 1 tool (DIR-002 creative-lane load). `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both.

Generation asks nothing and rules nothing, so this skill runs attended or unattended alike. It writes one derived file; there is no gate to defer.

---

## Step 1 — Locate the episode and confirm the preconditions

The episode folder is `WRITING/SHORTS/EPISODES/EP NN - TITLE/`. Named without a path → search there; several matches → ask which.

Check, in order, and stop plainly on the first that fails:

1. `shape.md` exists. Missing → not hardened; route CRE to `episode-harden` and stop.
2. `shape.md` frontmatter `status: ratified`. Draft → the spine is not committed; say so and stop. The walker mirrors a ruling, not a draft.
3. S2 has not banked this episode. The script probes `WRITING/SHORTS/DEV/_intake/_audit/` for a brainstorm floor naming the episode (never `scenes/`). Found → the walker's job is done for this episode; offer `supersede` instead, or `--force` if CRE says the brainstorm is going another round.
4. An existing `walker.md` whose `shape_fingerprint` matches the current `shape.md` → nothing moved; say so and stop. `--force` regenerates anyway.

**Never read `draft.md`** (plan-only, CRE-ruled 2026-09-03 — prose is not mined into plans). **Never read `WRITING/SHORTS/DEV/scenes/`** (this episode's S2 has not run; other episodes' scenes are noise). Never read a blueprint below its `## Your notes` rule. The script honours all three; you honour them too when you look at the folder.

---

## Step 2 — Derive

```
python scripts/walker.py derive --root "<vault root>" --episode "EP NN - TITLE"
```

The script reads, read-only: `shape.md` (every tagged entry, the knot, the anchor, the curve, the agenda), `premise.md` (frontmatter tier / container / POV and § The premise verbatim), `blueprint.md` (frontmatter curve; § Incident and § Choice; nothing below the rule), the candidate's `triage.md` `## Arc chain` (Choice and Mirror lines, path from `premise.md` `source_candidate`), and `WRITING/SHORTS/DEV/registry/` (names and first lines only — the recurring characters, places and lore already banked across episodes). It writes `walker.md` with serialized, parse-gated frontmatter (DIR-004):

```
type: brainstorm-walker · episode · shape_ratified · shape_fingerprint · status: current | superseded
superseded_by · block_count · sources_read (with the not-read line) · generated · tool · note
```

Body, in this order:

1. **Refresher** — one screen. Knot and anchor as the shape carries them; curve; the gate line (tier, container, POV); the premise verbatim in a folded callout; mechanics (Choice, Incident, Mirror, want, MoT question and answer scope, ending, flaw); cast one-liners; setting lines; the shape's agenda; what is banked in the registry.
2. **Episode-level cues** — four slots, each a head, a question, and an empty notes slot: `scene — the opening`, `scene — the closing`, `project level — the reader, during`, `project level — the reader, after`.
3. **The walk** — one block per shape entry in the shape's walk order: want, Moment of Truth, ending, each rung from the anchor down (a rung's sub-lines such as *E3, the flip* ride in its block), flaw.
4. **Cast** — one block per cast member; a member's sub-lines (*Dana, status*, *Dana, personality*) ride in the member's block.
5. **Setting** — one block per setting line.
6. **Brainstorm agenda** — last. Every agenda line carried whole, each with a notes slot; the blocks flagged `⚑ open` listed once.
7. A `---` rule, then **`## Your notes`** — the catch-all, CRE's, carried verbatim on every regeneration.

Each block is: the committed line(s) lifted verbatim with their tags → seven lens lines → `**Your notes:**` with nothing under it. A lens line is `- **<cue head> <target>** · <lens> — <question>`; the bold head is what he says aloud before answering, so `dev-capture`'s deterministic layer routes it without inference. The heads are fixed per lens — dialogue, imagery, action → `scene —`; reflection, character → `character —`; setting → `place —`; feel → `what I love about this —`. Blocks holding a `[NOT NAMED — CRE]` line carry `⚑ open` in the heading and switch to the open-hole templates; those are the holes S2 exists to fill.

**Regeneration.** If `walker.md` exists and the shape has moved, the script carries every filled notes slot forward verbatim by block key, and the tail under `## Your notes`. A note whose block no longer exists (a renamed shape line) lands under `## Carried notes` with its old heading — never dropped — and goes home if the block comes back. The report line tells you how many slots were carried and how many orphaned.

---

## Step 3 — Check, re-read, present

```
python scripts/walker.py check "<episode>/walker.md" --shape "<episode>/shape.md"
```

Fix every FAIL. The checker confirms: frontmatter parses; sections in order with the agenda last before the rule; the four episode-level slots; every block carries the seven lenses with cue-grammar heads in question form and a notes slot; no quoted speech in a question; **no word in a question that is not template vocabulary or already on the block's reminder lines** (the no-proposed-content floor — a beat wearing a question mark usually brings a new noun with it); with `--shape`, every tagged shape entry and agenda line appears verbatim. The `not checked:` line names what it cannot see — whether a question is really a question about the committed entry, whether a lifted line is still what the shape says today, whether a carried note is complete. That remainder is CRE's, at the mic and the desk (DIR-018).

**Re-read the written file through the file tools** (DIR-005) before presenting.

Present in response-contract voice: one plain sentence on what he is carrying ("Walker built for EP 04 — 18 blocks, none open; the agenda is the shape's five lines. Read the refresher, then talk."), where the file is, and the open flags if any. Nothing else. Do not summarise the questions back to him.

### Sharpening a question — only under the floor

The script's questions are templates parameterised by the entry's own label; they are deliberately generic so they cannot author. You may sharpen one toward its committed line **only** by using words already on that line — and then run `check` again; a sharpened question that introduces a noun, verb or image the reminder does not carry is a proposed beat, and the checker will fail it. When in doubt, leave the template. The template is coverage; the sharpening is a nicety.

---

## Step 4 — Lifecycle

- **Regenerate** when `shape.md` is re-ratified (`derive` again; the fingerprint tells the script the shape moved). Notes carry.
- **Supersede** once the brainstorm sheet ratifies: `python scripts/walker.py supersede "<episode>/walker.md" --by "<the ratified sheet path>"`. Stamps `status: superseded` and `superseded_by:`; the body and every note stay where they are for the record.
- **Never rule on the walker.** It is a derived artifact (DIR-019 §1). A collision between what the mic moved and the ratified shape belongs to `episode-feedback`'s GATE COLLISION class, not here.

---

## Step 5 — Log

`_CHANGELOG.md`, top-insert: `## YYYY-MM-DD — [writing-ops/fiction] brainstorm-walker (EP NN - TITLE)` — blocks (walk / cast / setting), open flags, agenda lines, notes carried on a regeneration. Tool surprises → `_OBSERVATIONS.md` (`^obs-NNN`, re-scan the max anchor first). A craft observation about the shape or the brainstorm — prose, not pipeline — → `_CREATIVE OBSERVATIONS.md` (`^cobs-NNN`), automatically (DIR-003).

---

## Guards

- **Reads the sources read-only; asks CRE nothing during generation.** The spine is committed; the walker mirrors it (DIR-019 §1, CDIR-009).
- **Never reads `draft.md`** (plan-only, CRE 2026-09-03). **Never reads `WRITING/SHORTS/DEV/scenes/`.** Never reads a blueprint below its notes rule.
- **Every prompt is a question about a committed entry** — never a beat, an image, a line, or an option (CDIR-003). The opening, closing, and reader-experience slots are asked and left blank.
- **Reminder lines are lifted verbatim in the carve register, tags included** (CDIR-002). A paraphrase drifts.
- **Coverage, never obligation.** No downstream pass grades the brainstorm against the walker; skipping a cue is legal (DIR-017 §2; the 2026-08-26 ruling against assigning obligation before arrival).
- **Heads in the S2 cue grammar** from `WRITING/SHORTS/DEV/_DEV_MAP.md`, fixed per lens, so `dev-capture` routes on them.
- **Every `[NOT NAMED — CRE]` entry is carried as a cue flagged open; the shape's agenda is carried whole.**
- **Notes slots are empty at generation and carried verbatim on regeneration.** Orphans go to `## Carried notes`, never dropped.
- **Regenerate on re-ratify; supersede when the sheet ratifies; never rule on the walker.**
- **Writes only `walker.md`.** Never `WRITING/SHORTS/DEV/` (dev-capture's), never `shape.md`, `blueprint.md`, `premise.md`.
- **Serialized, parse-gated frontmatter; file-tool writes; re-read after** (DIR-004, DIR-005).

## Stop conditions

Sentinel fails · no episode folder or ambiguous · no `shape.md` (route to `episode-harden`) · `shape.md` not ratified · S2 already banked for this episode (offer `supersede`) · walker already mirrors the current shape (nothing moved) · a secret in any read file (DIR-001 — flag, never propagate).

## What this skill is NOT

- Not the brainstorm or its synthesis — **brainstorm** distils the transcript and the walker's typed notes afterward; this only sets the table.
- Not the runway — **episode-runway** is the S4 speaking carve for drafting prose; this is the S2 coverage sheet for brainstorming.
- Not harden — **episode-harden** asks and commits the pillars, cast and setting; this reads them.
- Not the budgets or verdicts, either run — **episode-blueprint**.
- Not the collision seam — **episode-feedback**.
- Not a gap punch list over a DEV tree — **dev-readiness**.
- Not a coverage grader. Which cues were touched is not tallied in v1.
- Not a writer into `WRITING/SHORTS/DEV/`. Notes reach the tree through `brainstorm` then `dev-capture`.
- Not **interview-me** — generation asks nothing.

---

_Canonical reference lives at [[WORKFLOWS/brainstorm-walker]]. Procedure changes land in the workflow doc first, then propagate here._
