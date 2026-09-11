---
type: workflow
name: episode-harden
status: draft — source authored 2026-09-05 off the ratified intent; packaging pending (desktop pack-skills.ps1, DIR-009); graduates after 2–3 live runs
triggers: ["harden the episode"]
lane: 5 (writing-ops) + 1 (fiction)
intent: "[[WORKFLOWS/intents/episode-harden]]"
created: 2026-09-05
last_updated: 2026-09-11
revision_note: "2026-09-11 — PROVISIONAL banner added (dec-036): the short-form spine is the want the character has no agency to satisfy, with the flaw discovered in the response rather than established before it, so the rung-walk DOWN to the flaw is provisional. The `## Want` field already asks the right question and is unchanged. Banner only — no step, field or script changed. Full rework deferred by CRE behind a state trigger (the premise floor is producing in-band pieces), tracked at `^backlog-blueprint-harden-want-first`. Prior: 2026-09-06 — step 7 offers 'build the walker' at the stamp (brainstorm-walker build; installed skill inherits at repack, DIR-009). v1 — built 2026-09-05 from WORKFLOWS/intents/episode-harden.md (ratified same day). Companion edits landed in the same build: episode-blueprint Inputs name shape.md as run 2's structural source (premise wins on overlap, shape next, DEV additive for the aesthetic layer — CRE widened the 'nowhere else' clause 2026-09-05); pipeline S1.75 row; _SKILLS MAP trigger row."
---

# episode-harden

The **structural commitment session** on a Writing Is War episode — the step between `episode-blueprint` run 1 and the S2 dream-catching brainstorm. It reads the blueprint, the gated premise, and the candidate's deepened `## Arc chain` as known, then interviews CRE from the reader's point of view and writes the answers to `shape.md` in the episode folder: what the character wants in her heart of hearts, the scope of the question she is building to and of the answer she gets, the ending, each rung walked down from the anchor to the flaw with one line per rung naming what her intentions, obfuscations, and flaw are running against, and from that shape the cast and setting as derived defaults he ratifies. He carries the ratified `shape.md` into the brainstorm; `episode-blueprint` run 2 reconciles against it at S3.

**The problem it exists to kill:** when CRE rambles at the mic he follows no checklist, and the pieces a reader needs — the want, the question, the answer's scope, who these people have to be — get left to chance and then derived at the keyboard while he is shaping prose. Harden commits the spine and the placing facts on paper first, so the brainstorm spends itself on the aesthetic layer (conversation, looks, feel, vibe) over a locked spine, and he drafts without deriving structure at the mic.

**Layers, not rivals (CRE-ruled 2026-09-05, `^obs-322`).** DEEPEN captures the arc chain at pick time; the blueprint measures variance and budget; harden commits the reader's pillars and the cast; the brainstorm is aesthetic. Four tools touch one field at four layers. None re-asks another's ruled item.

## Pipeline position — S1.75 of the episode route

```
S0    feeling capture        premise-forge (DEEPEN optional) → CANDIDATES/TITLE/triage.md
S1    gate + scaffold        episode-init  → EP NN folder, gated premise.md, GO
S1.5  blueprint run 1        episode-blueprint → blueprint.md, [ANGLE MISSING — CRE] hand-backs
S1.75 HARDEN                 ← this workflow — shape.md, ratified, carried into S2
S2    dream-catching         brainstorm → dev-capture into WRITING/SHORTS/DEV/ (aesthetic layer)
S3    synthesis + REGEN      episode-feedback, then episode-blueprint run 2 reads shape.md — MANDATORY
S4    runway carve           episode-runway Pass 2 — OPTIONAL, mic route only
S5    drafting engine        mic or desk → S6 dev-edit → S7 CRE's author pass → …
```

Run 2 stays at S3 — the regeneration follows the last thing that moves the premise (route v4 ruling). Harden adds one step and moves none.

## When to use

CRE says **"harden the episode"** on a gated WIW episode that has a `blueprint.md` (run 1, ruled GO), before the S2 brainstorm has run. Attended only. Do NOT use it to plan budgets, variance, or the GO/RESHAPE call (`episode-blueprint`), to capture the arc chain at pick time (`premise-forge` DEEPEN — stays optional; read its chain when one exists), to run or route the dream-catching session (`brainstorm` + `dev-capture`), to reconcile notes against the premise (`episode-feedback`), to carve the runway or check production (`episode-runway`), or to weigh a fork (`decision-helper` — a fork found here is recorded `[NOT NAMED — CRE]`, never weighed).

> **PROVISIONAL — the short-form axis is want-first (dec-036, CRE-ruled 2026-09-11).** This doc walks every rung DOWN to the flaw, treating the flaw as the floor the ladder rests on. dec-036 makes the short-form spine the **want the character has no agency to satisfy in that moment**, legible in the opening move, with the flaw discovered in the response rather than established before it — because the lead-up a flaw-first ladder needs is what pushes a piece past 2,500 words. The `## Want` field already carries the right question; the rung-walk below it is the provisional part. **The rework is deferred by CRE**, trigger: *the premise floor is producing in-band pieces* — not date-bound.

## Inputs

- `blueprint.md` (run 1, `ruling` stamped) — **required**; missing → not blueprinted → route to `episode-blueprint`. Read: Cast roles, Flaw, Escalations with angles and failure modes, Moment of Truth, Climax, Outcome mode, frontmatter `curve`, and every `[… — CRE]` hand-back (the agenda seed).
- `premise.md` — the gate output: knot, constraint, cast as stated, rulings block. **Premise wins on overlap** with the blueprint and the chain.
- The source candidate's `triage.md` `## Arc chain` (path in `premise.md` frontmatter `source_candidate`; absent → record the absence in `sources_read`). Choice, mirror, escalations, Moment of Truth, ending stance in CRE's words. Additive where the premise is silent.
- `DECISIONS/_QUICK LOG.md` rows naming the episode — rulings never re-asked (CDIR-009).
- The craft, **by path at run time** (CDIR-002): `KNOWLEDGE/PROCESS/CRAFT BELIEFS` ("Structure," "Character Arcs," "Endings" — the chain is the spine, Endings carries the stance) and `KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework` (want vs resistance — resistance sets the slope; the shape; the staircase; the curve vocabulary). This is where the interview's vocabulary comes from; the tool carries no craft of its own.
- **Never `draft.md`** (plan-only, CRE-ruled 2026-09-03). **Never `WRITING/SHORTS/DEV/`** — S2 has not run yet, and if it has, this tool is out of position.

> **Read as known; ask only what they leave open.** A field the blueprint, premise, or arc chain already answers is presented as *"resolved against blueprint § Moment of Truth — confirm"* (one tap, `[ruled]`), never re-asked (DIR-011, CDIR-009). Re-asking a ruled field costs CRE what the deepening and the blueprint already bought.

## Output — `shape.md`

Serialized frontmatter (DIR-004): `type: episode-shape`, `episode`, `anchor_rung`, `rung_count`, `curve` (as read from the blueprint, never ruled here), `status` (`draft` | `ratified`), `ratified` (`CRE, YYYY-MM-DD` when stamped), `blueprint_run_read`, `sources_read`, `generated`, `tool`. Body, one screen, in the blueprint's carve register — one-sentence lines, no prose, no quoted speech — pillars top-down in **walk order**, then cast, setting, agenda:

```
# EP NN - TITLE · shape
**Knot:** his phrase from premise § a
**Anchor rung:** E3 — his phrase                                              [ruled]
## Want                      what she wants in her heart of hearts             [ruled | NOT NAMED — CRE]
## Moment of Truth
- **Question** — the scope of what she is building to ask                     [tag]
- **Answer** — the scope of what she gets                                      [tag]
## Ending
- **Gained** — one sentence · **Lost** — one sentence · **Mode** — stated | inferred   [tag each]
## Rungs                     walked DOWN from the anchor to E1
- **E4** — the rung · runs against: what her intentions, obfuscations, flaw meet here   [tag]
- **E3** — …  ·  - **E2** — …  ·  - **E1** — …
## Flaw                      one sentence                                      [tag]
## Cast
- **Role / name** — age · social status · personality · living conditions · mental state   [tag]
- **The instrument** — job: one sentence · arc: one sentence                   [tag]
## Setting
- **Era** · **Region** · **Class** · **Living conditions** — one line each     [tag each]
## Brainstorm agenda         LAST — what is still open + the blueprint's [ANGLE MISSING — CRE] hand-backs
```

**Tags — every entry carries exactly one, never a silent fill (DIR-018 shape):**

| tag | meaning |
|---|---|
| `[ruled]` | CRE's words — from the blueprint, premise, arc chain, or this session |
| `[recommended]` | a derived default proposed, **not yet ratified** — legal only while `status: draft` |
| `[recommended → ratified]` | a derived default CRE accepted as offered |
| `[NOT NAMED — CRE]` | asked and not answered, or a fork he did not rule — a hole, visible to S2 and run 2 |

One tag per line. A cast or setting detail whose status differs from its line's gets its own line, so each detail is tagged. His phrasing replaces a default → the tag flips to `[ruled]`.

**Section order** is the walk order, which is the Character Arcs chain read **backwards**: the reader's pillars are named from the top (what is at stake at the Moment of Truth) so every rung below is built in relation to it. The blueprint and the arc chain run the chain forwards; the shape is the same chain seen from the summit. Neither re-derives the other.

## The interview — three rounds via `interview-me`

Batched, defaulted where a default is derivable, **blank where the answer would be content**. Three rounds is `interview-me`'s cap and this tool's exact shape; anything a round opens that does not fit the next round lands as `[NOT NAMED — CRE]` on the agenda, never a fourth round.

**Round 1 — the summit (anchor, want, question, answer, ending).** Opens with the anchor: *which rung is the all-in?* — proposal: the blueprint's Moment of Truth line (`[recommended]`), because the blueprint's MoT and the rung he feels as all-in can differ (EP 04: the interruption at hour 24 vs the big question at hour 16). His pick sets where the walk starts. Then, **no defaults**: the want in her heart of hearts; the scope of the question she is building to; the scope of the answer she gets; the ending as gained / lost / mode. Where the arc chain's Moment of Truth or ending stance already answers one, present it resolved — confirm.

**Round 2 — the walk down.** From the anchor rung to E1, one question per rung, **no defaults**: the rung as the blueprint states it (resolved — confirm), and *what are her intentions, obfuscations, and flaw running against here?* — the resistance line. The walk is checked against the curve the blueprint carries (oscillating, spike, slow burn …) and against the T&T shape (each rung tracks the original refusal; closes an escape; relates to the anchor) — as **questions to him**, never as corrections. The flaw closes the round: resolved against blueprint § Flaw — confirm. If two rungs' resistance lines read as one to you, ask once, plainly; his answer is the ruling.

**Round 3 — who they must be, and where.** From the shape he has now stated, propose **derived defaults** for ratification, one pass: for each cast member — age, name, social status, personality, living conditions, mental state; for the instrument or obstacle — its job in the story and its arc alongside hers; for the setting — era, region, class, living conditions. Each carries a one-clause basis (*"38 — old enough for a decade of distance, young enough that the bill is hers"*). He ratifies, replaces, or leaves blank. **Texture stays at the mic**: no conversation, no appearance beyond what the shape fixes, no feel, no vibe (CRE-ruled 2026-09-05).

## Steps

1. **Sentinel** (`^obs-004`), then **`_CREATIVE DIRECTIVES`** before any episode or craft file (DIR-002 creative-lane load). **Attended only** — not attended → stop (DIR-012).
2. **Locate + gather** — the episode folder; `blueprint.md` (missing → route to `episode-blueprint`); `premise.md`; the triage `## Arc chain`; DECISIONS rows. Never `draft.md`, never `SHORTS/DEV/`. A `shape.md` already present → this is an **amendment sitting**: read it, ask only what he wants to change, keep every ruled tag; there is no regeneration — a ratified shape is a ruling, not a derive.
3. **Read the craft by path.**
4. **Pre-fill** — every field the three sources answer, tagged `[ruled]` with the resolving section noted for the confirm line. Run `python scripts/shape.py handbacks <blueprint.md>` to seed the agenda with the blueprint's hand-backs. List what is left open; that list is the interview.
5. **Round 1 → Round 2 → Round 3**, per the section above, in `interview-me`'s form (field tag, why it matters, default or *your call*). Present each round in response-contract voice: one line on what is resolved, then the batch.
6. **Scaffold → fill → check → re-read** — `scripts/shape.py scaffold` with `--rungs N` and `--anchor`; file-tool fills in his words; `scripts/shape.py check` (frontmatter parses, sections present in walk order, rungs descending and contiguous to E1, one resistance token per rung or the hand-back tag, every entry tagged, no bare `[recommended]` when `status: ratified`, no quoted speech / multi-sentence / 45+-word lines, no placeholders, agenda last); re-read through the file tools (DIR-005). The check names what it did not check (DIR-018): whether a line is his material or an invented beat, whether a resistance line is really different from its neighbour, whether a default was derived from the shape or from imagination.
7. **The stamp** — present the shape; CRE rules `status: ratified` (frontmatter `ratified: "CRE, YYYY-MM-DD"`). Every `[recommended]` he did not touch becomes `[recommended → ratified]` on his word; one he declines becomes `[NOT NAMED — CRE]`. Not stamped → `status: draft` is the visible deferral (DIR-012 §4). Close by naming the agenda in one line — that is what he aims the mic at — **and offer the walker in one line: "build the walker?"** ([[WORKFLOWS/brainstorm-walker]], 2026-09-06). On his yes, run it in the same sitting; on anything else, leave it — trigger-called, never chained silently. Only on a ratified stamp; a draft shape gets no walker.
8. **Log** — `_CHANGELOG` top-insert; `_OBSERVATIONS` for tool surprises; `_CREATIVE OBSERVATIONS` (`^cobs`) for craft observations about the shape, automatically (DIR-003).

## Stop conditions

Sentinel fails · not attended · no folder / ambiguous · no `blueprint.md` (route to `episode-blueprint`) · S2 brainstorm already banked into `SHORTS/DEV/` for this episode (out of position — say so; `episode-feedback` and run 2 own the reconciliation now, and the shape would be a second spine) · CRE answers nothing in round 1 (a shape of `[NOT NAMED — CRE]` is noise; write nothing).

## Guards (each with its reason)

- **Reads blueprint, premise, and arc chain as known; asks only what they leave open** — a ruled field re-asked costs him the deepening (DIR-011, CDIR-009).
- **The anchor is his, offered as the blueprint's MoT** — the MoT and the all-in rung can differ, and the walk changes with the anchor.
- **Defaults only for derived details** (ages, names, socioeconomic status, personality, living conditions, mental state, setting placing facts, the instrument's job and arc) — those follow from the shape he stated. **Never a default for the want, the question, the answer, a rung, a resistance, or the ending** — a proposed one authors the story (CDIR-003); those are asked *your call*.
- **Placing facts, not texture** — era, region, class, living conditions are asked; conversation, appearance beyond the shape, feel, vibe are the brainstorm's and this tool must not spend them (CRE-ruled 2026-09-05).
- **Every entry tagged, never a silent fill** — S2 and run 2 need to see what is committed and what is a hole (DIR-018).
- **Structure only, one-sentence lines, no quoted speech** — AI executes, CRE creates (CDIR-001); a shape that reads like story pre-spends the mic. Names are in scope here as ratified defaults — the one place the carve register admits them, because casting is the job.
- **Never reads `draft.md`** — the plan-only rule (CRE, 2026-09-03).
- **Reads craft by path every run** — the craft is his and a copy drifts (CDIR-002).
- **Attended only** — every field ends on his taste (DIR-012).
- **Questions run through `interview-me`** — one batch he ratifies in a reply beats twelve turns that break flow.
- **A ratified shape is a ruling the brainstorm may wander from; collisions surface through `episode-feedback`'s GATE COLLISION class.** No collision machinery here (the seam has an owner; the mic stays free, DIR-017).
- **A fork is recorded, not weighed** — `[NOT NAMED — CRE]` on the agenda; `decision-helper` if he wants it measured.
- **Writes only `shape.md`** — never `WRITING/SHORTS/DEV/` (dev-capture's, downstream), never `premise.md` or `blueprint.md`.
- **Serialized, parse-gated frontmatter; file-tool writes; re-read** (DIR-004, DIR-005).

## Evals

Objective parts only (`WORKFLOWS/skills-src/episode-harden/evals/`): every pillar present in walk order, rungs descending to E1 with a resistance token each, no untagged entry, no bare `[recommended]` on a ratified shape, agenda last, no quoted speech or multi-sentence lines, no placeholders. Run: `python scripts/shape.py check <fixture>` — `pass-*` exit 0, `fail-*` exit 1. Craft judgments (is the resistance line real, is the default derived or imagined, is the anchor right) are CRE's gate and are deliberately not eval'd.

## Relationship to the rest of the OS

- **Upstream:** [[WORKFLOWS/premise-forge]] DEEPEN (S0, optional — its `## Arc chain` is read here) → [[WORKFLOWS/episode-init]] (S1) → [[WORKFLOWS/episode-blueprint]] run 1 (S1.5 — its hand-backs seed the agenda).
- **Downstream:** [[WORKFLOWS/brainstorm-walker]] (offered at the stamp — derives `walker.md`, the coverage sheet CRE carries to the mic; reads this shape, never reopens it) → [[WORKFLOWS/brainstorm]] + [[WORKFLOWS/dev-capture]] (S2 — CRE carries `shape.md` and `walker.md` in; the brainstorm is the aesthetic layer) → [[WORKFLOWS/episode-feedback]] (S3 — collisions between what the mic moved and the ratified shape surface as GATE COLLISION) → [[WORKFLOWS/episode-blueprint]] run 2 (S3 — reads `shape.md` as its structural source: premise wins on overlap, shape next, DEV additive for the aesthetic layer; CRE-ruled 2026-09-05).
- **Question lane:** [[WORKFLOWS/interview-me]].
- **Craft read by path:** [[KNOWLEDGE/PROCESS/CRAFT BELIEFS]] · [[KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework]] · index [[KNOWLEDGE/CRAFT CANON]].
- **Intent:** [[WORKFLOWS/intents/episode-harden]] (ratified 2026-09-05). Watch-item it bears on: `^backlog-deepen-vs-brainstorm`.
- **Siblings / not this:** `episode-blueprint` (budgets, variance, verdict, both runs) · `premise-forge` DEEPEN (pick-time chain) · `brainstorm` + `dev-capture` (aesthetic layer and routing) · `episode-feedback` (collision seam) · `episode-runway` (mic carve, production check) · `interview-me` (the lane this calls) · `decision-helper` (forks).

## Run log

**2026-09-05 — built.** Source at `WORKFLOWS/skills-src/episode-harden/` (SKILL.md + `scripts/shape.py` scaffold / check / handbacks + evals with three fixtures). Fixtures are synthetic. First live target per the intent's open question: EP 04 if its S2 brainstorm has not yet run when the skill installs, else EP 05. Packaging is CRE's, on the desktop (`pack-skills.ps1` → sha-verify → Save-skill, DIR-009); the session's skill list is snapshotted at boot, so the first run needs a fresh session.
