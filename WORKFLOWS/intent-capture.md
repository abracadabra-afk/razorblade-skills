---
type: workflow
name: intent-capture
trigger: capture the intent
aliases: [write the intent, intent for X, build me a prompt for X, prep a prompt for skill-creator, turn this into a brief, interview me and write it up]
inputs: [a ramble in chat, a dictation transcript, or a vault note describing a skill / tool / feature / task CRE wants]
outputs: [WORKFLOWS/intents/SLUG.md — six source sections + a derived handoff prompt block; status draft until CRE ratifies; a _CHANGELOG entry]
lane: meta
status: draft
last_updated: 2026-09-03
revision_note: v1 — authored 2026-09-03 with interview-me from the two 2026-09 Claude 5 prompting clippings. First intent written with it is its own (WORKFLOWS/intents/intent-capture.md). Not yet packaged or run live on a second target.
---

# WORKFLOW: intent-capture

## When to use
CRE wants something built or done and it is still mostly in his head: a new vault skill, a change to a workflow, a tool, a one-shot end-to-end run. He rambles, dictates, or points at a note; this writes the intent down as the first link of the artifact chain (**intent → spec → plan → build**) and derives the prompt the next link runs on. The main consumer is `skill-creator`; `project-plan` and a bare Claude 5 run are the other two targets.

Source: the AI-native SDLC playbook's `intent.md` discovery phase (originator brainstorms with the agent, the agent writes it down, the originator reviews) and the seven Claude 5 prompting rules, both from the 2026-09 clippings in `Clippings/`. Mapped onto the vault: one file per intent, the originator gate, and the house prompt rules in `skills-src/intent-capture/references/prompt-rules.md`.

## The artifact
`WORKFLOWS/intents/<slug>.md`, from `skills-src/intent-capture/assets/intent-template.md`:

| Section | Holds |
|---|---|
| Job | the whole task, one paragraph, his words |
| Why | who it is for, what the output enables (rule 3 template) |
| Guardrails | instruction + reason, positive form, directives cited |
| Done looks like | exit criteria, output style, landing path, example to match |
| Non-goals | what the run must not widen into |
| Known context | tree pointers that settle things (DIR-011) |
| Open questions | unresolved after the interview, default in force |
| Interview record | rounds, defaults accepted, still open |
| **Handoff prompt** | **derived** from the above; regenerated, never hand-edited (DIR-019 §1) |

The sections are the source; the block is the mirror. When a skill ships from an intent, its canon doc links back to the intent file.

## Governing principle — capture, never widen
It writes down what CRE wants. Mechanical defaults (a landing path, a format) are taken and stated; creative or scope defaults are never taken (organic-process guard). It never builds the target and never invents a goal. The originator ratifies before the status moves.

## Steps
0. Sentinel (`^obs-004`); creative-lane load if the lane is fiction or writing-ops (DIR-002).
1. Take the input; settle slug / target / lane (defaults from the language; ask only if unclear). Existing slug → amend, status back to `draft`.
2. Extract into the template in his words; tree check for siblings, prior rulings, tracking backlog items → Known context. For target `skill-creator`, also pre-extract skill-creator's four intake answers + siblings + lane directives.
3. Invoke `interview-me` with the empty fields as the caller frame; merge the answer sheet. "Just write it" → defaults + Open questions.
4. Rewrite guardrails as instruction + reason.
5. Derive the handoff block; self-check against `references/prompt-rules.md`.
6. Write the file (file tools), re-read, confirm frontmatter + sections (DIR-005).
7. Originator gate: show job / done / guardrails / open questions in chat; ratify or correct; regenerate the block on any correction.
8. Hand off: path + the one next action for the target; offer a `_BACKLOG` item.

Full behavior in `WORKFLOWS/skills-src/intent-capture/SKILL.md`.

## Stop conditions
- Sentinel fails → halt.
- No goal in the input → one question, then proceed.
- Asked to build → write the intent, route to the target, stop.
- Secret in the input → DIR-006.
- Unattended → file stays `draft`; review lands as a `## Needs CRE ruling (intent-capture DATE)` line in `_BACKLOG` (DIR-012).

## Logging
One `_CHANGELOG` entry in the intent's lane: slug, target, rounds, open-question count, status. Surprises → `_OBSERVATIONS`; craft observations from fiction / writing-ops intents → `_CREATIVE OBSERVATIONS` (DIR-003).

## Packaging
Source `WORKFLOWS/skills-src/intent-capture/` (SKILL.md + `references/prompt-rules.md` + `assets/intent-template.md`). Pack on the desktop (`pack-skills.ps1`), sha-verify, Save-skill (DIR-009). Both referenced paths must ship in the `.skill`. Not packaged as of 2026-09-03; tracked at `^backlog-intent-pair-pack`.

## Calibration (first live run)
The first intent written was this skill pair's own, `WORKFLOWS/intents/intent-capture.md`, authored in-session from the clippings and CRE's three rulings (scope any task, batched interview, `WORKFLOWS/intents/` location). Second run should be a real new-skill request end to end, then "harvest the session for skill intent-capture" (`skill-review` harvest mode) to sort the one-time vs forever corrections.

## What this is NOT
- Not `skill-creator` — never writes a SKILL.md, runs evals, or tunes a description.
- Not `interview-me` — that asks; this writes.
- Not `project-plan` / `decision-helper` — no milestones, no fork weighing.
- Not `brainstorm` / `premise-forge` / `dev-capture` — fiction development has its own capture lane.
- Not the spec or the plan — those are built by the target from this file.
