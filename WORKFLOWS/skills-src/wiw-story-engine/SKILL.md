---
name: wiw-story-engine
description: "Take a Writing Is War short from a feeling or a what-if to a stamped, in-band escalation plan in one tool, promise carried from sentence one. CRE's three-step WIW model. Step 1 Forge - FILL forges premise plus promise sentences for his gut (SPARK / REWORK / KILL), BRING tests his own - banks to WRITING/SHORTS/CANDIDATES/TITLE/triage.md. Step 2 Want vs Inescapability and Step 3 Escalations ask and record his want, rationale, Inescapable (force and truth), Story (must / or else), setting, then per beat trigger, Therefore, But, Penalty, plus Climax, Cut, Pay-off and budgets, into EPISODES/EP NN/spine.md, replacing shape.md and blueprint.md. Use when CRE says forge the story, run the story engine, fill the bag, engine step 2, engine step 3, or wants a WIW premise, spine or escalation plan. Generates only at Step 1 FILL; never proposes a slot; flags never veto; attended only; never reads draft.md or SHORTS/DEV. Not episode-init, the S2 brainstorm, episode-feedback, the runway, or long-form sizing."
---

# wiw-story-engine

One tool for the pre-draft half of a Writing Is War short: a felt yes on a premise, the want and the thing that refuses it, the escalations that strip the character down to the cut. It replaces `premise-forge`, `episode-harden` and `episode-blueprint` on the WIW route. Its job is to get CRE from a feeling to a plan he can dictate from without making him originate cold, and without the tool writing a word of his story.

The model is his: `SCRATCHPAD/WiW Workflow rev1.md`. This skill is the mechanical shell around it. `references/model.md` maps every slot to his definition; `references/checks.md` explains each check and what it cannot see. Read them when a slot's meaning or a check's verdict is in doubt.

## Why the shape is what it is

A horror/narration audience returns for a recognizable promise: dread, a fresh wound, a cut at the peak, inside 2,000–2,800 words, in any sub-genre. A novel can afford a lead-up that establishes a flaw; a short cannot. So the entry point here is the **wound shown through action** — one witnessed instance — and the character's **response to each denial** is what tells the reader who they are. There is no flaw in this spine and no backstory anywhere. The novel/Witchwood route stays flaw-first and this tool never touches it.

Every slot is CRE's words verbatim or `[NOT NAMED — CRE]`. The tool generates in exactly one place — Step 1 FILL, the what-if layer his `PREMISES.md` already instructs an AI to produce — because the felt yes is the only admission to the bag and the tool stocks the bag, it does not author (CDIR-001, CDIR-003). Everywhere else it asks and records. A want, a rationale, an Inescapable, an escalation, a climax, a cut, a pay-off proposed by the tool would be the tool writing his story (CDIR-003, CDIR-009).

## Boot, every run

1. Sentinel (`^obs-004`): `_DIRECTIVES.md` frontmatter `type: ai-os-brain`, `file: directives`; mismatch → halt, ask which folder is the vault.
2. Read `_CREATIVE DIRECTIVES.md` after `_DIRECTIVES` and before any `WRITING/` file (DIR-002 creative-lane load). CDIR-001, 003, 009 are the boundary this tool carries.
3. Attended only. Every step ends on CRE's taste; an unattended run would defer all of it (DIR-012). Not attended → stop and say so.
4. Never read `draft.md` or `WRITING/SHORTS/DEV/`. The plan precedes the prose and must not grade it (DIR-017, DIR-019). If S2 has already banked DEV material for this episode, Step 3 still does not read it; CRE carries what moved in his own words (the re-run below).
5. Write only `triage.md` (Step 1) and `spine.md` (Steps 2–3). Everything else is a report or a chat line.

## Declare the step

CRE's trigger sets it; otherwise infer from the opener and say which step you took in one line.

| CRE says | Step | Mode |
|---|---|---|
| "forge the story" · "fill the bag" · "I need shorts" · a feeling | **1** | FILL — the tool forges |
| "here's a premise …" · a what-if of his own | **1** | BRING — the tool tests and banks his |
| "engine step 2" · "want and inescapable for EP NN" | **2** | ask + record |
| "engine step 3" · "escalate EP NN" · "re-run the spine" | **3** | ask + record; re-run carries notes |
| "deepen", a novel/series idea, "what does this want to be" | — | not this tool: say "not a WIW short" for a long-form idea and stop; `premise-forge` DEEPEN and long-form sizing are out of scope here |

## Step 1 — Forge

**Reads:** `WRITING/SHORTS/PREMISES.md` (his grammar and standing generation instruction), `CANDIDATES/*/triage.md` and `EPISODES/*/premise.md` frontmatter (variety — his corpus, never a market), `SCRATCHPAD/New WiW Story Model.md` §shapes when the shape list is needed. Bag census first: `python scripts/engine.py bag WRITING/SHORTS/CANDIDATES` — live count, ages, 90-day re-gut flags, cap and min-fill. At cap (~12) lead with hygiene before forging; below min-fill (4) surface "forge the story" as a task to `TASKS/TASKS.md` so week-shape serves it. Legacy triages (knot/what-if shape) are read as they are; the engine never rewrites a banked candidate.

**FILL.** Take the condition he brings, or offer 2–3 under-worked ones from his corpus (he picks; the scan never picks). Forge ~5–8 premise + promise pairs in his grammar: premise = one witnessed instance, the reader in the room the first time it happens, no "keeps", no "always"; promise = the dread compact, the wrongness the reader is now waiting for. Sub-genre free under the horror promise. Present flat — no ranking, no advocacy, no shape yet.

**BRING.** Take his sentence(s) as written. If it needs a taught mechanism, several spines, a span that stretches, or a cast beyond a protagonist and two, it is not a WIW short: say so in one line and stop. Do not size it, do not develop it.

**The gut gate.** Per candidate, CRE rules SPARK / REWORK / KILL. Kills are free; never argue for a corpse. REWORK: he names what is off; re-forge that one and return it to the gate with no default. Expect most of a batch to die.

**After the gut, on SPARKs only** (never pre-measured — a shape on a premise the gut has not admitted is a ranking in a measurement's clothes):
- **Shape** — ask from his list: slow burn · single incident · twist/reveal · circular · frame story · epistolary · cat-and-mouse · dread curve · slow burn to sudden shock · kishōtenketsu. A shape he names off the list is recorded as his.
- **Promise mapping** — read the five lines against the two sentences (`references/checks.md`): dread · fresh wound · destruction · compelled to watch · no agency. Record each as his phrase or `thin — [NOT NAMED — CRE]`. Dread reads first. A thin line is a flag on the row; the candidate still banks.
- **Working title** — his. Skipped → bank under `UNTITLED - P<n>/`, `working_title: "[NOT NAMED — CRE]"`, `working_title_placeholder: true`, one gate line asking for a rename. Never a tool-invented noun; never held out of the bag for want of a title.

**Bank.** `python scripts/engine.py scaffold-triage --out "WRITING/SHORTS/CANDIDATES/<TITLE>/triage.md" --title "<TITLE>" --mode FILL --subgenre … --shape …`, fill with the file tools in his words, `python scripts/engine.py check-triage <path>`, re-read through the file tools (DIR-005). The triage keeps `type: candidate-triage` and the Container / TOS band sections so `episode-init` reads it as before; where init used to read the what-if and the knot it now reads `## Premise` + `## Promise`.

**Close.** One reply carries every ratify: the SPARKs' shapes, titles, and a ranked next-up from the live bag (recency of yes, sub-genre and shape variety against the last published episode) that he confirms or reorders. If a REWORK is pending, its second gut ruling rides the same reply. The session closes on his reply; if it cannot, name the outstanding item.

## Between Step 1 and Step 2

`episode-init` — separate, unchanged. It gates the candidate, scaffolds `EP NN/`, writes `premise.md`, stamps the triage `promoted → EP NN`. This tool does not gate and does not scaffold the episode folder. Step 2 needs the folder to exist.

## Step 2 — Want vs Inescapability

**Reads:** `EP NN/premise.md` (the gate's rulings — premise wins on overlap), the source triage, `DECISIONS/_QUICK LOG.md` rows naming the episode. Never `draft.md`, never `SHORTS/DEV/`. Resolve before you ask (DIR-011): a slot the premise or a ruling already answers is presented as *resolved against premise § x — confirm*, one tap.

**Ask** — through `interview-me` as the caller frame, one batch, **no defaults on any of these** because every one is story content:

| Slot | The question |
|---|---|
| **Want** | What is the first physical thing they do? (Not "wants to" — the move: turning off the radio, stacking the chair.) |
| **Rationale** | Why do they act that way — the surface reason that keeps the want in place? |
| **Inescapable · force** | What refuses them, no matter what they try? |
| **Inescapable · truth** | What is that force the shape of — the thing beneath the rationale the story surfaces and never states? |
| **Story · must / or else** | They must ___ or else ___. |
| **Setting** | 3–4 sensory details that are off — each one an early signature of the force or the truth. Era, region, class only if the premise needs them: say which and why. **"none needed" is his answer, never a default** — the `placing facts —` line reads `[NOT NAMED — CRE]` until he says none needed or names them. |

Stop when he says enough. Unanswered is `[NOT NAMED — CRE]`, visible, never filled.

**A one-sentence Inescapable.** He will often answer with one sentence ("His daughter wants to be heard. No matter what he tries to stop it."). Record it verbatim on whichever line its wording answers — `force` if it names what refuses, `truth` if it names what the refusal is the shape of — and leave the other half `[NOT NAMED — CRE]`. Never split one sentence across both lines and never paraphrase the second half out of the first. `## Checks` says which half he answered.

**Shape.** Taken silently from the triage (`--shape` at scaffold); `## Checks` carries one line, `shape — <shape> · resolved against triage § Shape`. Not re-presented for confirm — a settled call stays settled — unless the premise has moved at the gate and `premise.md` says so. (Default in force pending his ruling; reversible on his word.)

**Write.** `python scripts/engine.py scaffold-spine --out "WRITING/SHORTS/EPISODES/EP NN - TITLE/spine.md" --episode "EP NN - TITLE" --candidate "<triage path>" --shape … --subgenre … --escalations 3 --band-low 2000 --band-high 2800` (band numbers from `BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY` §3b, read at run time — the tool carries none). Copy `**Premise:**` and `**Promise:**` from the triage verbatim. Fill Step 2 with the file tools in his words. Run `check-spine`; fix structural FAILs (yours), record FLAGs on the `## Checks` lines (his). Frontmatter `step: 2`, `status: draft`. Re-read.

**Close.** Lead with what is decided and what is open; then "engine step 3 when you're ready." No craft lecture.

## Step 3 — Escalations

**Reads:** `spine.md` (Step 2 as known), `premise.md`, DECISIONS rows. Never `draft.md`, never `SHORTS/DEV/`.

**Ask** — `interview-me`, no defaults. Per beat, in his order: **trigger** (what just happened that they must answer) → **Therefore** (the only logical next move given that denial) → **But** (what the world refuses — and `denies:` the exact assumption they were counting on) → **Penalty** (what it subtracts — `subtracts:` the loss, and it must be a loss the previous beat did not take). Then **Climax** as the ultimate Therefore, the last best hand; the **Cut** — the last line on the page, the peak, before any explanation; the **Pay-off** — what survives off the page. Three beats is the model's shape; he sets the count.

**Budget** — his per-section targets when he gives them. When he gives none, run `python scripts/engine.py budget --escalations N --band-low … --band-high …` and present its split for one-tap ratify; never derive by hand. The template is fixed (Opening 14% · escalations 62%, rising by 50 per beat · Climax 20% · Cut 4% · Pay-off 0, over the band midpoint, rounded to 50, remainder on Climax), so two runs on the same inputs give the same numbers. This is the one place a number may be proposed, because a budget is arithmetic, not story; his numbers replace it whole.

**Checks before the stamp** (`references/checks.md`): promise mapping re-read against the filled slots (destruction from the or-else, compelled from want + rationale, no agency from force + truth); Inescapable names both halves; setting 3–4 each tied; each Penalty subtracts something new; budget in band. `check-spine` runs the mechanical half and prints pass / FLAG; record each on `## Checks`. Flag, never veto.

**The stamp.** Present in response-contract voice: verdict and band in one sentence, then **a recommended path he can overrule in one word**, then the spine, then the batched holes. The recommendation (default in force pending his ruling; reversible): **draft** when a Step 2 hole stands (truth, a setting detail, placing facts — the spine's pillars are not yet his), **stamp over the holes** when only `denies:` / `subtracts:` clauses stand (the beats are his; the clauses are the check's vocabulary and he can fill them at the mic). A gate with no recommendation makes him the mechanism.

CRE stamps → frontmatter `status: stamped`, `stamped: "CRE, YYYY-MM-DD"`, `## Stamp` reads `status: stamped — CRE, YYYY-MM-DD`; the Checks `stamp —` line reads `stamped · holes carried: …` or `stamped · no holes`. A hole he stamps over stays `[NOT NAMED — CRE]` — his call, recorded.

Not stamped → `status: draft` is the visible deferral (DIR-012 §4), and the Checks `stamp —` line **lists every `[NOT NAMED — CRE]` hole by slot** (`stamp — draft · holes: Inescapable truth · Setting details 1–3 · Setting placing facts · E1 denies · E1 subtracts …`). That line is the degraded mode: it is what the next sitting, the walker, and the S3 re-run read so the holes route without CRE remembering them. `check-spine` fails a holed draft without the line and flags a hole the line does not name. Re-read through the file tools.

**Re-run after the S2 dream-catching leg.** `episode-feedback` will have amended `premise.md`; CRE carries what moved in his words. Regenerate above the rule: `run: n+1`, every slot re-asked only where he says it moved (a ruled slot is not re-asked, CDIR-009), and **`## Your notes` carried verbatim**, never interleaved, never summarized. The prior run's text is not kept as a second spine; the stamp resets to `draft` until he re-stamps.

## Hand-back grammar

- `[NOT NAMED — CRE]` — asked and not answered, or a fork he did not rule. A hole, visible to every downstream reader. Never a tool placeholder in its place.
- `thin — [NOT NAMED — CRE]` on a promise-mapping line — the sentences cannot answer it.
- `pass` / `FLAG · reason` on `## Checks` — the tool's read, his to overrule.
- `stamp — draft · holes: …` on `## Checks` — the deferral record; every hole by slot, so nothing waits on him remembering it.
- A fork he articulates is recorded as two lines and a hole, never weighed here (`decision-helper` if he wants it measured).

## Stop conditions

Sentinel fails · not attended · long-form idea (say "not a WIW short", stop) · Step 2/3 with no `EP NN` folder or no `premise.md` (route to `episode-init`) · CRE answers nothing in a step (write nothing — a file of holes is noise) · any pull toward beats-as-prose, dialogue, or a rendered image in a slot (the mic's, DIR-017; offer nothing, record what he said).

## Guards, each with its reason

- **Generate only at Step 1 FILL** — the felt yes is the only admission and the tool stocks the bag, it does not author (CDIR-001, CDIR-003).
- **Ask and record everything in Steps 2–3; never propose** a want, rationale, Inescapable, escalation, climax, cut or pay-off — the character's response to the denial is CRE's instrument (CDIR-003, CDIR-009).
- **Unanswered reads `[NOT NAMED — CRE]`** — a silent fill becomes canon downstream.
- **Promise mapping at Step 1 and again pre-stamp; flag, never veto** — CRE's gut outranks the check; the check catches a dread-less premise before dictation.
- **Inescapable must name force and truth** — force alone is a mechanism, truth alone is literary.
- **Each Penalty subtracts something new** — the only mechanical proof of escalation.
- **Setting 3–4, each tied to force or truth, no era/region/class unless the premise needs it** — texture is filled at the mic (DIR-017 §2).
- **Never `draft.md`, never `SHORTS/DEV/`** — the plan precedes the prose and must not grade it (DIR-017, DIR-019).
- **No flaw in the spine; the novel route untouched** — the wound shown through action is the entry point for short form.
- **Attended only** (DIR-012). **Writes only `triage.md` and `spine.md`.**
- **Serialized, parse-gated frontmatter; file-tool writes; re-read after** (DIR-004, DIR-005). A bash read of the mount is not verification.
- **Band numbers travel as arguments** — §3b is ruled; the tool carries no container numbers.
- **`## Your notes` carried verbatim on every re-run** — the notes are his and the tool never writes below the rule.

## Not this tool

`episode-init` (gate + scaffold, between Step 1 and Step 2) · `brainstorm-walker` / `brainstorm` / `dev-capture` (the S2 dream-catching leg — reads the stamped spine, never reopens it) · `episode-feedback` (notes reconciled against the premise) · `episode-runway` (the mic carve) · `premise-forge` DEEPEN and long-form sizing (out of scope — "not a WIW short", stop) · any drafting or revision pass · an impact score of any kind.

## Log

Non-trivial (anything banked, written, stamped) → `_CHANGELOG` top-insert; tool surprises → `_OBSERVATIONS` (`^obs-NNN`); craft observations about the premise or the spine's shape — prose, not pipeline — → `_CREATIVE OBSERVATIONS` (`^cobs-NNN`), automatically (DIR-003).
