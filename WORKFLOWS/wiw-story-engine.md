---
type: workflow
name: wiw-story-engine
status: "draft — source authored 2026-09-12 off the ratified intent; mechanical-shell evals pass on fixtures; packaging pending (desktop pack-skills.ps1, DIR-009); graduates after 2–3 live runs. Supersedes premise-forge (WIW modes), episode-harden and episode-blueprint ON THE WIW ROUTE ONLY — their installs stay until this has run live"
triggers: ["forge the story", "run the story engine", "fill the bag", "engine step 2", "engine step 3", "re-run the spine"]
lane: 5 (writing-ops) + 1 (fiction)
intent: "[[WORKFLOWS/intents/wiw-story-engine]]"
created: 2026-09-12
last_updated: 2026-09-12
revision_note: "v1.1 — 2026-09-12 (later, same day), off skill-test PASS-WITH-NOTES (SYSTEM/skill-tests/wiw-story-engine/2026-09-12/). Seven fixes, no contract change. (A) scaffold-spine no longer writes `placing facts — none needed` — a scaffold default in a Step 2 slot was tool text where SKILL.md promises none; now [NOT NAMED — CRE] like every other slot. (B) check-spine counts a [NOT NAMED — CRE] placing-facts line as a hole (11 on the test spines, was 10 plus a false FLAG). (C) SKILL.md: 'none needed' is CRE's answer, never a default. (D) new `budget` subcommand — fixed template over the band midpoint, rounded to 50, deterministic; three runs had produced three splits. (E) the stamp gate leads with a recommended path (draft when a Step 2 hole stands, stamp-over-holes when only denies/subtracts stand — default pending CRE's ruling) and a holed draft must list every hole on the Checks `stamp —` line; check-spine fails without it. (F) a one-sentence Inescapable is recorded verbatim on the half its wording answers, the other half a hole, never split or paraphrased. (G) shape taken silently from the triage with a `resolved against triage § Shape` Checks line (default pending CRE's ruling). Fixtures untouched; all four still behave; the three test spines still PASS unchanged. Re-pack owed (DIR-009). v1 — 2026-09-12, built from WORKFLOWS/intents/wiw-story-engine.md (ratified same day). One tool replaces three on the WIW route: Step 1 Forge (premise-forge FILL/BRING, want-first, no knot), Step 2 Want vs Inescapability (episode-harden's slot), Step 3 Escalations (episode-blueprint's slot, trigger → Therefore → But → Penalty). Per-piece file is spine.md, replacing shape.md + blueprint.md. dec-036 carried as the promise mapping only; its flaw-discovered-in-response clause is obsolete for short form. ^backlog-blueprint-harden-want-first is discharged by this build."
---

# wiw-story-engine

The **WIW story engine** — one attended tool that takes a Writing Is War short from a feeling or a what-if to a stamped, in-band escalation plan, the promise carried from sentence one. It runs CRE's three-step model from `SCRATCHPAD/WiW Workflow rev1.md`: **Step 1 Forge** (premise = a single witnessed instance, promise = the dread compact, a declared shape) banks to the candidate's `triage.md`; **Step 2 Want vs Inescapability** and **Step 3 Escalations** write one per-piece file, `spine.md`, in the episode folder. Each step builds the next.

**The problem it exists to kill:** the three-skill chain it replaces (`premise-forge` → `episode-harden` → `episode-blueprint`) was built flaw-first for long form. A 2,500-word piece cannot pay for the lead-up a flaw needs, so the chain produced literary pieces and over-band plans, and made CRE originate cold at three separate sittings. The short-form spine is the **wound shown through action**: one witnessed instance, a want shown in the first physical move, an Inescapable that refuses it, and escalations that subtract until the cut. No flaw, no backstory, one tool.

**The behavior is the installed skill's `SKILL.md`** at `WORKFLOWS/skills-src/wiw-story-engine/` — this doc is the canon record: position, provenance, guards, what moved. Where they disagree the source wins and this doc is stale (DIR-009 announce-the-gap rule).

## Pipeline position — the WIW route, collapsed

```
S0    FORGE          wiw-story-engine Step 1 → CANDIDATES/<TITLE>/triage.md   (was premise-forge)
S1    gate + scaffold episode-init → EP NN folder, gated premise.md, GO        (unchanged)
S1.5  SPINE step 2   wiw-story-engine Step 2 → spine.md (want, rationale, Inescapable, Story, setting)   (was harden)
S1.75 SPINE step 3   wiw-story-engine Step 3 → spine.md (escalations, climax, cut, pay-off, budgets, stamp)   (was blueprint run 1)
S2    dream-catching  brainstorm-walker (reads the stamped spine) → brainstorm → dev-capture   (unchanged)
S3    synthesis       episode-feedback, then wiw-story-engine Step 3 RE-RUN carrying ## Your notes   (was blueprint run 2)
S4+   runway (optional, mic route) → drafting → dev-edit → author pass → …   (unchanged)
```

`episode-init` stays separate between Step 1 and Step 2. The S3 regeneration survives as a re-run of Step 3. The novel/Witchwood route is untouched: `runway-builder`, `brief.md`, the Craft Beliefs arc chain, all flaw-first, all outside this tool.

## The three steps, in one screen

| Step | Asks / forges | Writes | Checks (pass / FLAG, never veto) |
|---|---|---|---|
| **1 Forge** | FILL: forges ~5–8 premise + promise pairs for his gut (SPARK / REWORK / KILL). BRING: tests his own. After the gut, on SPARKs only: shape from his list, working title. | `CANDIDATES/<TITLE>/triage.md` — `type: candidate-triage`, `## Premise`, `## Promise`, `## Shape`, `## Container`, `## TOS band / tier`, `## Promise read`, `## Variety note` | premise is one witnessed instance (no "keeps", no "always"); shape on the list; promise mapping (dread · fresh wound · destruction · compelled · no agency) |
| **2 Want vs Inescapability** | want as the first physical move · rationale · Inescapable as **force** + **truth** · Story as **must** / **or else** · setting 3–4 off-details each tied force or truth, no era/region/class unless the premise needs them | `EPISODES/EP NN/spine.md` § Step 2, `step: 2`, `status: draft` | Inescapable names both halves; setting 3–4 each tied; want not a declaration |
| **3 Escalations** | per beat: trigger → Therefore → But (`denies:` the assumption) → Penalty (`subtracts:` the loss) · Climax as the ultimate Therefore · the Cut · the Pay-off · budgets per section | same file § Step 3 + § Checks + § Stamp, `step: 3`; CRE stamps `status: stamped` | promise mapping re-read against the filled slots; each Penalty subtracts something new; budgets sum inside 2,000–2,800 (IN-BAND / UNDER / OVER); Cut short; Pay-off `(~0)` |

Every slot is CRE's words verbatim or `[NOT NAMED — CRE]`. The tool generates in one place only — Step 1 FILL, the what-if layer `PREMISES.md` already sanctions. Slot definitions in his words: `skills-src/wiw-story-engine/references/model.md`. Each check with its reason and its blind spot: `references/checks.md`.

## Output — `spine.md`

Serialized frontmatter (DIR-004): `type: episode-spine`, `episode`, `source_candidate`, `shape`, `subgenre`, `status` (`draft` | `stamped`), `step` (2 | 3), `run`, `band_low`, `band_high`, `band_source`, `budget_total`, `band_verdict`, `escalation_count`, `checks`, `stamped`, `sources_read`, `generated`, `tool`. Body: `**Premise:**` / `**Promise:**` / `**Shape:**` head carried verbatim from the triage, then `## Step 2 — Want vs Inescapability` (### Want · Rationale · Inescapable · Story · Setting), `## Step 3 — Escalations` (### Opening (~N) · E1..En (~N) · Climax (~N) · Cut (~N) · Pay-off (~0)), `## Checks`, `## Stamp`, a rule, `## Your notes` last. Worked example: `evals/fixtures/pass-spine-radio-stamped.md` — CRE's radio/daughter walk-through from rev1, end to end.

`spine.md` replaces `shape.md` and `blueprint.md`. Downstream readers: `brainstorm-walker` derives from the stamped spine (its shape.md read is stale from this build — see follow-ups); `episode-feedback` reconciles notes against `premise.md` as before and the Step 3 re-run picks up what moved.

## Mechanical shell

`scripts/engine.py` — `scaffold-triage` · `scaffold-spine` · `check-triage` · `check-spine` · `budget` · `bag`. Two result classes on purpose: **FAIL** is structural (the file is not the shape the route reads — the tool's to fix, exit 1); **FLAG** is content the check can see but CRE rules (exit 0). The check prints what it did not check (DIR-018). Console-encoding-safe (DIR-020); band numbers are arguments, never constants; no vault path is hard-coded.

## Guards (each with its reason)

- **Generate only at Step 1 FILL** — the felt yes is the only admission; the tool stocks the bag, it does not author (CDIR-001, CDIR-003).
- **Ask and record everything in Steps 2–3; never propose** a want, rationale, Inescapable, escalation, climax, cut or pay-off — the character's response to the denial is CRE's instrument (CDIR-003, CDIR-009). Unanswered reads `[NOT NAMED — CRE]`, never a tool placeholder.
- **Promise mapping at Step 1 and again pre-stamp; flag, never veto** — CRE's gut outranks the check; the check catches a dread-less premise before dictation (dec-036 carried as the mapping only).
- **Inescapable names force and truth** — force alone is a mechanism, truth alone is literary.
- **Each Penalty subtracts something the previous did not** — the only mechanical proof of escalation.
- **Setting 3–4, each tied, no era/region/class unless the premise needs it** — texture is filled at the mic (DIR-017 §2).
- **Never `draft.md`, never `WRITING/SHORTS/DEV/`** — the plan precedes the prose and must not grade it (DIR-017, DIR-019).
- **No flaw in the spine; the novel route untouched.**
- **Attended only** (DIR-012). **Writes only `triage.md` and `spine.md`.**
- **`## Your notes` carried verbatim on every re-run**; the tool never writes below the rule.
- **Long-form ideas get "not a WIW short" and stop** — no sizing, no seedbed, no DEEPEN here.
- **Serialized, parse-gated frontmatter; file-tool writes; re-read after** (DIR-004, DIR-005).

## Stop conditions

Sentinel fails · not attended · long-form idea · Step 2/3 with no `EP NN` folder or `premise.md` (route to `episode-init`) · CRE answers nothing in a step (write nothing) · any pull toward beats-as-prose or dialogue in a slot.

## Evals

Mechanical shell only (`skills-src/wiw-story-engine/evals/`): four fixtures — `pass-triage-radio`, `pass-spine-radio-stamped` (CRE's walk-through, 2,450 IN-BAND, 0 flags), `flag-triage-pattern` (exit 0, flags: "keeps", shape not named, dread thin), `fail-spine-broken` (exit 1: 15 structural, 10 flags). Run: `python scripts/engine.py check-triage|check-spine <fixture>`. **2026-09-12 build run: all four behave as specified.** Premise quality, dread, and whether a slot is CRE's material are never eval'd.

## What this supersedes, and what it does not touch

| Predecessor | On the WIW route | Elsewhere |
|---|---|---|
| [[WORKFLOWS/premise-forge]] | FILL / BRING → Step 1. DEEPEN not carried (no arc chain in the short-form spine). | DECLARED / OPEN long-form sizing and `WRITING/SEEDS/` stay with premise-forge. |
| [[WORKFLOWS/episode-harden]] | → Step 2. The rung-walk down to the flaw is gone; the want, the Inescapable and the Story are the pillars. | none — WIW-only tool |
| [[WORKFLOWS/episode-blueprint]] | → Step 3, both runs. Escalations are trigger → Therefore → But → Penalty, not angle-on-flaw; budgets sum inside the band rather than to a center. | `runway-builder` / `brief.md` carry the novel plan; untouched |

Installs and packages of the three are **not retired by this build** — that follows a live run (intent non-goal). Their canon docs carry a superseded-for-WIW banner. The `_BACKLOG` items targeting them (`^backlog-premise-forge-v22-pack`, `^backlog-premise-forge-step6-refusal-untested`, `^backlog-deepen-vs-brainstorm`, `^backlog-deepen-first-run`, `^backlog-episode-harden-pack`, `^backlog-blueprint-curve-options-and-tag-ceiling`) close or re-home once this tool is live; `^backlog-blueprint-harden-want-first` is discharged by this build.

## Relationship to the rest of the OS

- **Upstream:** `WRITING/SHORTS/PREMISES.md` (his grammar + the FILL sanction) · `SCRATCHPAD/WiW Workflow rev1.md` and `SCRATCHPAD/New WiW Story Model.md` (the model — read by path, never restated as craft of the tool's own, CDIR-002).
- **Between steps:** [[WORKFLOWS/episode-init]] — reads `## Premise` + `## Promise` where it used to read the what-if and the knot.
- **Downstream:** [[WORKFLOWS/brainstorm-walker]] → [[WORKFLOWS/brainstorm]] → [[WORKFLOWS/dev-capture]] (S2, reads the stamped spine) → [[WORKFLOWS/episode-feedback]] → Step 3 re-run → [[WORKFLOWS/episode-runway]] (optional carve).
- **Question lane:** [[WORKFLOWS/interview-me]] — every Step 2/3 slot is story content and carries no default.
- **Rulings carried:** [[DECISIONS/2026-09-04 wiw-throughline-dark-vs-horror|dec-034]] (horror is the promise, sub-genre free — aligned) · [[DECISIONS/2026-09-11 wiw-premise-floor|dec-036]] (the five-clause floor → the promise mapping; the flaw clause dropped for short form by CRE's 2026-09-12 ruling).
- **Intent:** [[WORKFLOWS/intents/wiw-story-engine]].

## Packaging

Source at `WORKFLOWS/skills-src/wiw-story-engine/` — `SKILL.md` (description 1,007 chars, quoted, no angle brackets) + `scripts/engine.py` + `references/model.md`, `references/checks.md` + `evals/`. Pack on the desktop with `pack-skills.ps1`, sha-verify, Save-skill (DIR-009); never sandbox-packaged (`^obs-156`). The session's skill list is snapshotted at boot — first live run needs a fresh session.

## Run log

**2026-09-12 — built.** Off the ratified intent, one session. Shell evals green on four fixtures. First live target: the next candidate CRE picks for EP 05 — Step 1 on a fresh feeling, or BRING on a bag candidate re-stated in the new grammar (legacy triages keep their knot/what-if shape; the engine never rewrites a banked candidate).

## Open taste calls (defaults in force, CRE's to flip)

- **Stamp recommendation** — v1.1 recommends *draft* while a Step 2 hole stands and *stamp over the holes* when only `denies:` / `subtracts:` stand. His ruling replaces the rule.
- **Shape at Step 2** — taken silently from the triage with a Checks record line, not re-presented. If he wants the one-tap confirm, the rule flips.

## Follow-ups (seeded to `_BACKLOG`)

- `brainstorm-walker` reads `shape.md`; on this route it should read `spine.md` — a walker amendment, not this tool's.
- `episode-init` check (a) reads the five-clause floor from the triage's `## Promise read`; confirm on the first live gate that the engine's five lines satisfy it without a wording change.
- Retire the three predecessors' WIW installs after the first live run.
