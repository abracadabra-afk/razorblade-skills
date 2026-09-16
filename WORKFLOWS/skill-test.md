---
type: workflow
name: skill-test
trigger: test skill N
aliases: [test the skill, run the skill test, does skill N actually work]
inputs: [one installed skill name; CRE's success conditions (asked, with defaults); an optional test case]
outputs: [SYSTEM/reports/YYYY-MM-DD-skill-test-NAME.md (verdict first); SYSTEM/skill-tests/NAME/DATE/ evidence tree; on FAIL or PASS-WITH-NOTES one _BACKLOG item under OS / Meta carrying a skill-creator handoff pointer; a _CHANGELOG entry; NO edit to any skill]
lane: meta
status: draft
last_updated: 2026-09-15
revision_note: v1 authored 2026-09-11 from WORKFLOWS/intents (CRE-dictated brief). Shell script built + selftested; evals written for the shell only. Gate handling CRE-ruled same day (auditor rules once, runs resume). Not yet run live; first target is CRE's pick. Packaging pending (DIR-009 desktop chain).
---

# WORKFLOW: skill-test

## When to use
CRE has a vault of Cowork skills and no way to know whether one delivers its outcome except by
running it on live work and noticing later. This gives him a verdict from his own seat **before** a
skill touches live material, and a fix prompt `skill-creator` can open with when it falls short.
Trigger on "test skill N," "test the skill," "run the skill test," or any ask of the form *does this
skill actually work*.

## The axis it owns (and its neighbors)

| Skill | Question it answers |
|---|---|
| `skill-audit` | Does the installed copy match its source? (drift) |
| `skill-review` | Is the skill shaped right, scripted where it should be, cheap to load? (design) |
| `skill-creator` | Author or change a skill; run evals; tune a description |
| `task-audit` | Do scheduled-task prompts match their canon docs? |
| **`skill-test`** | **Does the installed skill deliver its outcome, judged from CRE's seat, on a case he set?** |

Same folder, different questions. `skill-test` never authors, packs, installs, diagnoses drift, or
reviews design.

## Governing principle — verdict from CRE's seat, fix as a prompt
Three isolated runs on one case expose variance (DIR-013: one sample never verifies a
nondeterministic path). An auditor carrying `_ME` and CRE's stated goal rules on what came back.
Where the output ends on his taste, his taste is the instrument; objective checks apply only where
the skill's own doc names a measurable output. Anything short of PASS ends in a `skill-creator`
handoff block and one backlog line — never an edit to the skill (DIR-009's adoption trap).

## Guardrails, with reasons
1. **Writer skills run against a fixture under `SYSTEM/skill-tests/NAME/DATE/`; only read-only
   skills touch the live vault.** A test that mutates canon costs more to find and undo than it is
   worth (DIR-012). When in doubt, treat the skill as a writer.
2. **Gates are ruled in CRE's stead, once, by the auditor, and every ruling is listed.** A gate that
   stops the run tests nothing, and a ruling he cannot see is not a deferral (DIR-012 cl. 4). Runs
   stop at a gate and return it; the auditor rules once from `_ME` + the goal; the same ruling goes
   to all three runs, which resume (CRE-ruled 2026-09-11, `DECISIONS/_QUICK LOG`). Three
   independent rulings would turn a ruling divergence into a false skill divergence.
3. **Fix instructions and a backlog item, never an edit to the skill.** DIR-009.
4. **Test the installed copy, not `skills-src/`.** The installed copy is what runs (DIR-009). Drift
   noticed is one report line, routed to `skill-audit`.
5. **Judge from CRE's seat, not an invented rubric.** `_ME` § How I work with AI: ask whose call it
   already is; where a step ends on taste, hand it over.
6. **Report lands in `SYSTEM/reports/`.** Agent output elsewhere disrupts the domain roots.
7. **File tools for every skill read and every `_BACKLOG` write.** Bash reads of the mount serve
   stale partials (DIR-005).

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm `type: ai-os-brain` + `file: directives`. Mismatch → halt.

### Step 1 — Resolve the installed copy
Read `<installed location>/SKILL.md` (from the session's skill listing; else a pathed Glob under
the AppData `skills-plugin` tree, negative confirmed twice — DIR-005) plus any shipped `scripts/`
and `references/`. Not installed → report, route to the Install queue (`skills-manager`), halt.
Read `WORKFLOWS/NAME.md` once; a visible disagreement on what the skill produces is the drift line.

### Step 2 — Goal line + the bar (CRE-gated)
State the goal in one line. Ask one batched question with defaults: what must be true for the goal
to count as met (two or three conditions proposed from the doc's outputs), and an optional test case
(one proposed from the vault). Do not run on silence.

### Step 3 — Write class + fixture
Classify read-only vs writer from the doc's outputs surface. Writer → copy the test case's inputs
into `SYSTEM/skill-tests/NAME/DATE/fixture/`. Scaffold with
`scripts/skill_test_shell.py scaffold` (tree + report stub with every section). Substrate: any
non-mount host (DIR-020); no host → build the tree by hand, say so in Not checked.

### Step 4 — Panel of three (one turn, isolated)
Three subagents, identical brief: installed `SKILL.md` path (they read it; never pasted), the test
case, the fixture path, the seat brief (goal, conditions, read `_ME` before ruling a gate), the
write surface (`run-K/` only), the gate rule (stop at a gate and return it verbatim with the
skill's own recommendation; never rule it), and a paths-only return. The orchestrator does not read
run outputs before the auditor does; a returned gate question is not an output.

**Gate loop.** Runs returned at a gate → auditor in gate mode rules each gate once (`_ME` + goal,
the skill's recommendation unless `_ME` argues against it) → `audit/stand-in-rulings.md` → the
same ruling to all three runs via `SendMessage` → resume. If `SendMessage` is unavailable, resume
each run as a fresh agent against its `run-K/` directory plus `audit/stand-in-rulings.md`, and
record the fallback under Not checked. Repeat until all three finish.

### Step 5 — Auditor (one subagent, CRE's seat)
Reads `_ME` in full, the goal, the conditions, the case, the installed `SKILL.md` (for measurable
outputs only), the three run dirs and `audit/stand-in-rulings.md`. Answers sound / usable /
consistent, lists every stand-in ruling with basis (naming any taste call CRE should re-rule), rules `PASS` / `PASS-WITH-NOTES` / `FAIL`, and on the latter two writes
the `skill-creator` handoff block (skill + installed path · goal · what the test showed with
evidence paths · the change wanted as instructions with reasons · what must be true after · what
not to change). Taste questions the evidence does not settle → `PASS-WITH-NOTES` with the question
named, never a threshold.

### Step 6 — Report
`SYSTEM/reports/YYYY-MM-DD-skill-test-NAME.md`, verdict first, path second, detail after. Sections
in order: Verdict line · Goal and bar · Runs (RUN 1/2/3) · Stand-in rulings · Consistency · Verdict
detail · skill-creator handoff (or `None — PASS`) · Drift noticed · Not checked (DIR-018). Then
`skill_test_shell.py check` — exit 0 clean · 1 findings · 2 unreadable; confirm findings by
file-tools re-read.

### Step 7 — Backlog item (FAIL / PASS-WITH-NOTES)
Top of `## OS / Meta` in `_BACKLOG.md`, file tools, verified by re-read:
`- [ ] **skill-test NAME — VERDICT DATE.** <what fell short>. Fix prompt ready in
[[SYSTEM/reports/DATE-skill-test-NAME]] § skill-creator handoff — open skill-creator with it, then
the DIR-009 desktop pack chain. #p2 #gated ^backlog-skilltest-NAME-DATE`. Re-run `check`.

### Step 8 — Chat + log
Chat: verdict, path, at most three lines. `_CHANGELOG` (meta, top-insert, file tools, re-read);
testing surprises → `_OBSERVATIONS`. Evidence tree stays.

## Stop conditions
- Sentinel fails → halt.
- Skill not installed → report + route, halt.
- Bar not stated → ask once with defaults, wait.
- Asked to fix, repack, or install → refuse; hand over the handoff block.
- Several skills named → first only.
- Asked to schedule → decline; attended only.
- A run writes outside its run dir → that run is FAIL on that ground; say so.

## Unruled defaults in force (v1)

| Question | Default |
|---|---|
| Read-only skill on live canon? | Allowed; any report it writes redirects to its run dir. |
| Fixture scope? | Only what the case needs, copied, never moved. |
| Cleanup of `SYSTEM/skill-tests/`? | Never here; evidence stays. `log-rotate` or CRE decides. |

## Logging
Meta lane. One `_CHANGELOG` entry per run naming the verdict and report path.

## Calibration (first live run)
Target: CRE's pick — a read-only skill first (`link-audit` or `task-audit`) so the fixture leg is
not the variable. Expected: three runs agree, PASS or PASS-WITH-NOTES, zero stand-in rulings. Any
FAIL on a read-only sweeper on the first run → re-read the auditor brief before the verdict is
trusted; the brief, not the skill, is the more likely defect on run one.

## Packaging
Source `WORKFLOWS/skills-src/skill-test/` (SKILL.md · `scripts/skill_test_shell.py` ·
`evals/evals.json`). Pack on the desktop (`pack-skills.ps1`), sha-verify, Save-skill (DIR-009).
Add `skill_test_shell.py --selftest` to the regression suite when packed. Not installed as of
2026-09-11.

## What this is NOT
- Not `skill-creator` — never authors or edits a skill; writes its opening prompt.
- Not `skill-audit` — no drift diagnosis.
- Not `skill-review` — no design or script review.
- Not `task-audit` — scheduled-task prompts out of scope.
- Not the trigger-accuracy harness (`^autoresearch-trigger-harness`, `^obs-030` loop #1).
- Not scheduled. Not more than one skill per run.
