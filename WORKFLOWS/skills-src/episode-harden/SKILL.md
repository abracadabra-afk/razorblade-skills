---
name: episode-harden
description: "Run the structural commitment session on a gated Writing Is War episode with a run-1 blueprint and write shape.md into the episode folder. Reads blueprint.md, premise.md and the arc chain as known, then interviews CRE from the reader's side in three batched interview-me rounds: the anchor rung (blueprint MoT proposed), the want in her heart of hearts, the scope of the MoT question and answer, the ending, each rung walked DOWN to the flaw with one line naming what her intentions, obfuscations and flaw run against, then cast and setting as derived defaults he ratifies (ages, names, status, mental state, era, region, class; the instrument's job). Every entry tagged ruled / ratified / NOT NAMED, never a silent fill. Use when CRE says 'harden the episode', after blueprint run 1 and before the S2 brainstorm. Structure only, never prose or texture. Attended only. Not for budgets or verdicts (episode-blueprint), the pick-time arc chain (premise-forge DEEPEN), the brainstorm, or collisions (episode-feedback)."
---

# Episode Harden

You are running the **structural commitment session** CRE takes before his dream-catching brainstorm on a Writing Is War episode. When he rambles at the mic he follows no checklist, and the pieces a reader needs — what she wants in her heart of hearts, the scope of the question she is building to, the scope of the answer she gets, who these people have to be — get left to chance and then derived at the keyboard while he is shaping prose. This session commits the spine and the placing facts to `shape.md` first, so the brainstorm spends itself on the aesthetic layer (conversation, looks, feel, vibe) over a locked spine, and `episode-blueprint` run 2 has a structural source to reconcile against.

Three things shape everything below:

- **AI executes; CRE creates (CDIR-001, CDIR-003).** You ask, record his words, and propose defaults only for details that *follow from the shape he has stated*. You never propose the want, the question, the answer, a rung, a resistance line, or the ending — a proposed one authors the story. Those questions go out with **no default** — *your call*.
- **Read as known; ask only what is open (DIR-011, CDIR-009).** The blueprint, the premise and the deepened arc chain already carry his rulings. A field they answer is presented as *resolved against blueprint § Flaw — confirm*, one tap, never re-asked. Re-asking costs him what the deepening and the blueprint already bought.
- **Layers, not rivals.** DEEPEN captured the chain at pick time; the blueprint measured variance and budget; you commit the reader's pillars and the cast; the brainstorm is aesthetic. Four tools on one field at four layers (`^obs-322`). Do not drift into any of the other three.

**PROVISIONAL — the short-form axis is want-first (dec-036, CRE-ruled 2026-09-11).** This skill walks every rung DOWN to the flaw, treating the flaw as the floor the ladder rests on. dec-036 makes the short-form spine the **want the character has no agency to satisfy in that moment**, legible in the opening move, with the flaw discovered in the response rather than established before it — because the lead-up a flaw-first ladder needs is what pushes a piece past 2,500 words. The `## Want` round already asks the right question and is unaffected; the rung-walk below it is the provisional part, so do not treat a thin flaw as a stall when the want and the denial are named. The rework is deferred by CRE behind a state trigger — *the premise floor is producing in-band pieces* — tracked at `^backlog-blueprint-harden-want-first`.

Canonical doc: `WORKFLOWS/episode-harden.md`. Intent: `WORKFLOWS/intents/episode-harden.md`. Route canon: `WORKFLOWS/pipeline.md` episode route v4, row S1.75.

---

## Position — S1.75, between blueprint run 1 and the brainstorm

```
S1.5  blueprint run 1      episode-blueprint → blueprint.md, GO, [ANGLE MISSING — CRE] hand-backs
S1.75 HARDEN               ← this skill — shape.md, ratified, carried into S2
S2    dream-catching       brainstorm → dev-capture into WRITING/SHORTS/DEV/  (aesthetic layer)
S3    synthesis + REGEN    episode-feedback, then episode-blueprint run 2 reads shape.md — MANDATORY
```

Run 2 stays at S3. You add one step and move none. If S2 has already banked material for this episode into `WRITING/SHORTS/DEV/`, you are out of position — stop and say so (the reconciliation is `episode-feedback`'s and run 2's now; a shape written after the brainstorm is a second spine).

---

## Step 0 — Sentinel, then the creative-lane load

From the mounted vault root, read `_DIRECTIVES.md` and confirm frontmatter `type: ai-os-brain` + `file: directives`. Missing or mismatched → **halt and ask** which folder is the vault.

Then read `_CREATIVE DIRECTIVES.md` (CDIR-001–010) **before opening any episode or craft file** — Lane 5 + Lane 1 tool, creative-lane load rule ratified (DIR-002). `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both.

**Attended only.** Not attended (a scheduled run, a batch, a "just do it" from another agent) → stop and say why: every field here ends on his taste, and an unattended run would either stall or fill (DIR-012). There is no unattended mode.

---

## Step 1 — Locate the episode and gather what is already ruled

The episode folder is `WRITING/SHORTS/EPISODES/EP NN - TITLE/`. Named without a path → search there; several matches → ask.

**Read, in this order:**

1. `blueprint.md` — **required.** Missing → not blueprinted; route CRE to `episode-blueprint` and stop. Read: Cast roles, Flaw, Incident, Choice, each Escalation with its angle and failure mode, Moment of Truth, Climax, Outcome mode, frontmatter `curve` and `escalation_count`, the `ruling`. Every `[… — CRE]` hand-back is an agenda seed. Never read below the `---` rule (`## Your notes` is his).
2. `premise.md` — the gate output: knot, constraint, cast as stated, § a, the rulings block. **Premise wins on overlap** with the blueprint and the chain.
3. The source candidate's `triage.md` `## Arc chain` (path in `premise.md` frontmatter `source_candidate`; no key or no section → record the absence in `sources_read`). Choice, mirror, escalations, Moment of Truth, **ending stance** (gained / lost / stated-or-inferred) in his words. Additive where the premise is silent. A `[NOT NAMED — CRE]` there is a hole, not a fill.
4. `DECISIONS/_QUICK LOG.md` rows naming the episode — rulings you never re-ask.
5. **A `shape.md` already in the folder** → this is an **amendment sitting**, not a rerun. Read it; ask only what he wants changed; keep every ruled tag; never regenerate. A ratified shape is a ruling, not a derive (DIR-019 §1 does not apply to it).

**Never read `draft.md`** (plan-only, CRE-ruled 2026-09-03). **Never read `WRITING/SHORTS/DEV/`** — S2 has not run; if it has, see Position.

Then run:

```
python scripts/shape.py handbacks "WRITING/SHORTS/EPISODES/EP NN - TITLE/blueprint.md"
```

It prints the blueprint's hand-backs (agenda seeds) and the curve as the blueprint carries it. **The curve is the blueprint's field.** If it is not named there, it is an agenda item here — never ask it in this session.

**Pre-fill.** Build the list of every field this tool owns and mark each one *answered by* (blueprint § X / premise § a / arc chain field) or *open*. The open list **is** the interview. Say in one line what is already resolved and how many questions are left.

---

## Step 2 — Read the craft by path (never from memory)

CRE's ruled craft; a copy drifts (CDIR-002). Read fresh every run:

- `KNOWLEDGE/PROCESS/CRAFT BELIEFS.md` — **"Structure"** (failure says more), **"Character Arcs"** (the chain Flaw → Incident → Choice → Escalations → Failures → Moment of Truth → Outcome; each escalation attacks the flaw from a different angle), **"Endings"** (something gained, something lost; outcomes are optional; all receipts in the reader's hand). The chain is the spine; Endings carries the stance — read both.
- `KNOWLEDGE/REFERENCES/Methods/Tension and Transformation Framework.md` — **want vs resistance** (resistance sets the slope; external spikes, internal undertow; equal forces oscillate), **the arc** (refusal as the engine; the refusal is credible because it protects something), **the shape** (open the fault line, pressure along it, remove the escapes one by one, gate the climax on the internal choice), **the staircase**, **the curve vocabulary**.

This is your question vocabulary. *Runs against* is the resistance line: at each rung, what are her intentions, her obfuscations, and her flaw pushing on — and what pushes back. Use the docs' words in your questions; do not paraphrase them into a system of your own, and never quote the craft text into `shape.md`.

**The walk order is the chain read backwards.** The blueprint and the arc chain run Flaw → Outcome. The shape starts at the summit — the Moment of Truth and what is at stake there — and walks down, so every rung is built in relation to the anchor. Same chain, seen from the top. You re-derive nothing; you ask the reader's questions about material he has already committed.

---

## Step 3 — The interview: three rounds, through `interview-me`

Run the questions in `interview-me`'s form: 5–7 per round, each tagged with its field, a few words on why it matters, and either a default or **your call**. One reply ratifies a round. Three rounds is `interview-me`'s cap and this tool's exact shape. Anything a round opens that does not fit the next round lands as `[NOT NAMED — CRE]` on the agenda — never a fourth round. He says "enough" or "just write it" → take the defaults you offered, blank everything without one, write.

Present each round in response-contract voice: one line on what is already resolved (with the resolving section), then the batch. No craft lecture.

### Round 1 — the summit: anchor, want, question, answer, ending

1. **Anchor rung** — *Which rung is the all-in?* **Default: the blueprint's Moment of Truth line** (`[recommended]`). The blueprint's MoT and the rung he feels as all-in can differ — on EP 04 the interruption at hour 24 versus the big question at hour 16 — and the walk in round 2 starts wherever he points.
2. **Want** — what she wants in her heart of hearts, underneath the stated goal. **No default — your call.**
3. **MoT question scope** — the scope of the question she is building to ask at the anchor: how big, of whom, what it would cost to ask. **No default.**
4. **MoT answer scope** — the scope of the answer she gets: whole, partial, withheld, wrong. **No default.** (The arc chain's *false victory — the answer is never complete* language often answers this; if so, resolved — confirm.)
5. **Ending** — gained, lost, mode (stated | inferred). The arc chain's *ending stance* and the blueprint's `ending_mode` usually answer this: present resolved — confirm. Where silent, **no default.**

### Round 2 — the walk down

From the anchor rung to E1, one question per rung, batched (four rungs is four questions; six rungs is six — the batch flexes). For each:

- **The rung** as the blueprint states it — resolved against blueprint § Escalations — confirm.
- **Runs against** — *what are her intentions, her obfuscations, and her flaw running against here? What pushes back?* **No default.** This is the line that keeps the straight line to the summit unpredictable.

Ask the shape questions **as questions to him, never as corrections**: does this rung track the original refusal; which escape does it close; how does it sit on the curve the blueprint carries (a rise, a release to a higher floor, the spike). If two resistance lines read as one to you, ask once, plainly, at the end of the round; his answer is the ruling. Rungs above the anchor (when he anchors below the blueprint's top rung) are still walked — the anchor sets where you start, not what is included; walk up from the anchor to the top rung first, then down. **Flaw** closes the round: resolved against blueprint § Flaw — confirm.

### Round 3 — who they must be, and where

Now the shape is stated, and casting follows from it. Propose **derived defaults**, each with a one-clause basis tied to something he ruled, one batch:

- **Each cast member** — age, name, social status, personality, living conditions, mental state. Basis form: *38 — old enough for a decade of distance, young enough that the bill is hers.*
- **The instrument or obstacle** (the caretaker on EP 04; the mirror's person half) — its **job** in the story and its **arc** alongside hers.
- **The setting's placing facts** — era, region, class, living conditions.

He ratifies, replaces with his own words, or leaves blank. A name is a default here — this is the one tool in the route where casting is the job, so the carve register admits names; the blueprint's "a name is prose" rule is the blueprint's.

**Texture stays at the mic (CRE-ruled 2026-09-05):** no conversation, no appearance beyond what the shape fixes, no feel, no vibe, no images, no objects. If a default of yours starts describing how a room looks or how someone talks, it has left this tool's layer — cut it to the placing fact.

### Defaults: where they are legal

| field | default? |
|---|---|
| anchor rung | yes — the blueprint's MoT |
| want · MoT question · MoT answer · ending (gained/lost/mode) | **never** — your call |
| a rung · a resistance line · the flaw | **never** — resolved-confirm or your call |
| cast details · instrument job + arc · setting placing facts | yes — derived, with basis |
| a fork he names but does not rule | record `[NOT NAMED — CRE]` — never weigh it (that is `decision-helper`, if he wants) |

---

## Step 4 — Scaffold, fill, check, re-read

1. Scaffold (serialized frontmatter, DIR-004), with the rung count from the blueprint and the anchor as he named it:

   ```
   python scripts/shape.py scaffold --episode "EP NN - TITLE" \
     --out "WRITING/SHORTS/EPISODES/EP NN - TITLE/shape.md" \
     --rungs 4 --anchor "E3 — his phrase" --curve "oscillating"
   ```

   (`--curve` is copied from the blueprint frontmatter — never a value you chose. The scaffold refuses to overwrite; an amendment sitting edits the existing file by hand.)

2. Fill with the **file tools**, his phrasing primary. Set `sources_read` and `anchor_rung` in the serialized block — never hand-format a new key with an unquoted colon or `#`.

3. **Tag every entry, exactly one tag per line:**

   | tag | when |
   |---|---|
   | `[ruled]` | his words — from the blueprint, premise, arc chain, or this session |
   | `[recommended]` | your derived default, awaiting his word — legal only while `status: draft` |
   | `[recommended → ratified]` | your default, accepted as offered |
   | `[NOT NAMED — CRE]` | asked and not answered, or a fork he did not rule |

   A cast or setting detail whose status differs from the rest of its line gets its own line, so every detail carries its own tag (the second `Lead / Tomas` line in the fixtures is the pattern). His phrasing replaces a default → `[ruled]`. **Never a silent fill.**

4. **The agenda, last.** One line per open item (every `[NOT NAMED — CRE]` above, in plain words), one line per blueprint hand-back carried forward (`blueprint hand-back: [ANGLE MISSING — CRE] on E4`), the curve if the blueprint left it unnamed. Nothing open → the explicit line: `none — the spine is committed; aim the mic at the aesthetic layer`. This is what he aims the brainstorm at, and what run 2 reads as the holes.

5. Check:

   ```
   python scripts/shape.py check "WRITING/SHORTS/EPISODES/EP NN - TITLE/shape.md"
   ```

   Fix every FAIL. The `not checked:` line names what the script cannot see — whether a line is his material or an invented beat, whether two resistance lines are really different, whether a default came from the shape or from imagination, whether the anchor is right. That remainder is yours at the gate (DIR-018).

6. **Re-read the written file through the file tools** (DIR-005) before presenting. One screen: a six-rung shape runs longer than a three-rung one and that is fine; a line that wraps twice or a tag that has become a sentence is not.

### What a line is, and is not

A shape line names *what the pillar is*, not *what happens on the page*:

- Structure (right): `runs against: her story that money was the reason she stayed.`
- Prose (wrong): `"It was never about the money," she said, not looking up.` — quoted speech, a rendered image, a sentence he could dictate.

If a line could survive into the story verbatim it does not belong here. The checker catches quoted speech, speech tags, multi-sentence lines and 45+-word lines; it cannot catch a well-formed sentence that is his beat rendered. The test is *would I be embarrassed to find this in his draft*. Cite the blueprint and the chain without quote marks inside the pillar sections; the **Knot** line is the one place a quoted phrase belongs.

---

## Step 5 — The stamp: CRE rules

Present the shape in chat: one plain sentence on what is committed and what is open ("Spine committed — want, both scopes, the ending, four rungs with resistance. Two holes: E2's resistance line and her mental state. Cast and setting are defaults for you to ratify."), then the shape, then the batched ratify list.

CRE stamps it: frontmatter `status: ratified`, `ratified: "CRE, YYYY-MM-DD"`. On his word every untouched `[recommended]` becomes `[recommended → ratified]`; one he declines becomes `[NOT NAMED — CRE]` and joins the agenda. **His ruling outranks your read and is not re-asked** (CDIR-009). If he steps away first, the file stays `status: draft` — the visible deferral (DIR-012 §4); bare `[recommended]` tags are legal there and the checker allows them.

Close by naming the agenda in one line. That is the seam this tool exists to hand forward.

---

## Step 6 — Log

`_CHANGELOG.md`, top-insert: `## YYYY-MM-DD — [writing-ops/fiction] episode-harden (EP NN - TITLE)` — anchor, rungs walked, tag counts (ruled / ratified / not named), agenda length, status. Tool surprises → `_OBSERVATIONS.md` (`^obs-NNN`, re-scan the max anchor first). A craft observation — about the shape, not the pipeline — → `_CREATIVE OBSERVATIONS.md` (`^cobs-NNN`), automatically (DIR-003).

---

## Guards

- **Reads blueprint, premise and arc chain as known; asks only what they leave open.** A ruled field is confirmed in one tap, never re-asked.
- **The anchor is his**, offered as the blueprint's MoT. The walk changes with it.
- **Defaults only for derived details.** Never for the want, the question, the answer, a rung, a resistance, or the ending.
- **Placing facts, not texture.** Era, region, class, living conditions are asked; conversation, looks, feel, vibe are the brainstorm's.
- **Every entry tagged; never a silent fill.** S2 and run 2 need to see what is committed and what is a hole.
- **Structure only, one sentence per line, no quoted speech.** Names are in scope as ratified defaults; nothing else from the prose layer is.
- **Never reads `draft.md`. Never reads or writes `WRITING/SHORTS/DEV/`.** Writes only `shape.md`; never `premise.md` or `blueprint.md`.
- **Reads craft by path every run.** Never restates the beliefs or T&T as rules of its own; never quotes them into the shape.
- **Attended only.** Every field ends on his taste.
- **Three rounds, through `interview-me`.** No fourth; leftovers are holes on the agenda.
- **A ratified shape is a ruling the brainstorm may wander from.** Collisions surface through `episode-feedback`'s GATE COLLISION class; this tool adds no collision machinery.
- **A fork is recorded, not weighed.** `[NOT NAMED — CRE]`; `decision-helper` if he wants it measured.
- **Amend, never regenerate.** A second sitting edits the ruled file by hand; the scaffold refuses to overwrite.
- **Serialized, parse-gated frontmatter; file-tool writes; re-read after** (DIR-004, DIR-005).

## Stop conditions

Sentinel fails · not attended · no episode folder or ambiguous · no `blueprint.md` (route to `episode-blueprint`) · S2 has already banked this episode into `WRITING/SHORTS/DEV/` (out of position — say so) · CRE answers nothing in round 1 (a shape of `[NOT NAMED — CRE]` is noise; write nothing).

## What this skill is NOT

- Not the budgets, variance, scope verdict, or GO / RESHAPE call, on either run — **episode-blueprint**.
- Not the pick-time arc chain — **premise-forge** DEEPEN (stays optional; you read its chain when one exists).
- Not the dream-catching session or its routing — **brainstorm** + **dev-capture**. You leave the aesthetic layer open on purpose.
- Not the collision seam — **episode-feedback**.
- Not the mic carve or the production check — **episode-runway**.
- Not the question lane itself — **interview-me** (you call it).
- Not a fork-weigher — **decision-helper**.
- Not prose, a runway, a scene list, or a writer into the DEV tree.

---

_Canonical reference lives at [[WORKFLOWS/episode-harden]]. Procedure changes land in the workflow doc first, then propagate here._
