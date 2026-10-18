---
type: workflow
name: interlock-plotter
lane: Fiction (Lane 1) — structure, administrative
status: packed 2026-10-17 (DIR-009, bytes verified); installed 2026-10-17 (uploaded through claude.ai Settings → Capabilities → Skills; confirmed enabled in the skills list, full description); proven on test boards at 1 and 5 leads (three iterations, final 16/16 and 18/18)
triggers: '"interlock the arcs" · "build the interlock board" · "check the interlock"'
skill_source: WORKFLOWS/skills-src/interlock-plotter/
intent: "[[WORKFLOWS/intents/interlocking-arc-model-branch-writing]]"
model: "[[WORKFLOWS/interlocking-arc-model]]"
created: 2026-10-17
last_updated: 2026-10-17
---

# interlock-plotter

**What it does.** CRE plots his book against the [[WORKFLOWS/interlocking-arc-model|Interlocking Arc Model]] in chat; the skill writes his answers into a plan, builds a Branch Writing board from the plan once he approves it, then reports collisions, switch locks and open blanks as observations. It is an administrative tool: it never writes prose, never invents a beat, premise or character, and never makes a story decision the plan doesn't hold (CRE ruling 2026-10-17; schema §4).

**Triggers.**

| Phrase | Runs |
|---|---|
| "interlock the arcs" | the full run: target → cast and roles → K1–K6 → beat walk (seven rounds of five beats) → optional placement → plan → "approve the plan" → build → check |
| "build the interlock board" | build + check, from an approved plan |
| "check the interlock" | the check report only, on any board (read-only) |

**Where things land.**
- Plans: `WRITING/BOARD PLANS/<board> - arc plan.md` (test runs: `SYSTEM/skill-tests/branch-writing/_work-*`). The ```` ```json ```` block is the record; the summary and beat table above it are regenerated from it by `scripts/plan_tool.py`, never hand-edited. Format: [[SYSTEM/reports/2026-10-17-interlocking-arc-model-proposal]] §5.
- Boards: a **new** file, or a **copy** of an existing board. The builder refuses an existing path.
- Check reports: `SYSTEM/reports/YYYY-MM-DD-<board>-interlock-check.md`.

**Tools.**
- `scripts/plan_tool.py` (in the skill): `new`, `set`, `beat`, `walk`, `render`, `approve`, `status`. Every plan write goes through it, so the JSON stays valid and a change after approval takes the approval off. `approve` accepts only CRE's phrase "approve the plan".
- `tools/build-plan.mjs` (plugin dev folder, node, outside Obsidian): plan → board; refuses an unapproved plan, an existing path, a target in `REFERENCE/`, and templates made from a different version of the model than the plan names. Parse-gates what it wrote.
- `tools/check-board.mjs` (same folder): the check report from `iamObservations`, the plugin's one pure check function (F5).
- `tools/make-iam-templates.mjs`: regenerates the 13 IAM arc templates from the model (F7).

**Guardrails, with reasons.**
- *CRE plots; it builds.* Every value written is his words from the session or the plan; a suggestion on the page would anchor him (CDIR-001, CDIR-003). It may say what a rule asks of a beat (the model's words, shown in the walk sheet), never the answer.
- *A blank is a valid state.* An unfilled beat stays an open, labelled blank, and the check lists blanks so nothing is lost, never as a fault.
- *Observations, never verdicts.* Whether the structure is locked is his call (CDIR-004). The report never says ready, locked or complete.
- *One question per decision, default open.* Switches and story calls stay open until he picks; folders, names and question order are the skill's.
- *Never a live board.* New board or copy only. "check the interlock" reads a live board and writes nothing to it.
- *Degraded mode.* The plan is written on every answer. If he stops mid-walk, nothing is lost and the next run resumes at the first unwalked group (`plan_tool.py status`).
- *Attended only.* Never scheduled.

**Not for:** prose; premises; character ideas; editing the model (CRE's text, CDIR-002); `audit the arcs` (arc-audit reads a draft); `shape the part`; boards CRE is working in; `REFERENCE/` or StoryLine's Codex.

**Proof runs.** [[SYSTEM/reports/2026-10-17-interlock-plotter-proof]] — fresh test boards at one lead and at five, each beat slot filled or an open labelled blank, the check report listing every conflict as an observation.

## Run log

- 2026-10-17 — authored; proof runs at 1 and 5 leads on test boards (see the proof report).
