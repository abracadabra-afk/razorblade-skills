---
name: skill-test
description: 'Outcome-level verdict on one installed vault skill from CRE seat before it touches live work, plus a ready fix prompt when it falls short. Use whenever CRE says "test skill N", "test the skill", "run the skill test", "does skill N actually work", or asks whether a Cowork skill delivers its goal. Reads the INSTALLED copy with the file tools, states the goal in one line, asks CRE what must be true for the goal to count as met (optional test case), runs it in three isolated subagents on one case, then an auditor takes CRE seat (from _ME plus the stated goal) and rules PASS, PASS-WITH-NOTES, or FAIL. Writes one report to SYSTEM/reports/ and, short of PASS, a skill-creator handoff block plus one _BACKLOG item. Writer skills run against a scratch copy under SYSTEM/skill-tests/, never live canon. Never edits, packs, or installs. Do NOT use to build or edit a skill (skill-creator), diagnose drift (skill-audit), review design (skill-review), or audit task prompts (task-audit). One skill per run, attended only.'
---

# skill-test

You are producing a verdict CRE can trust before a skill touches live material: does the installed
skill deliver its outcome, judged from his seat, on a case he supplied or accepted. Three isolated
runs on the same case expose variance; an auditor carrying his stated goal and his working profile
rules on what came back. Anything short of PASS ends in a fix prompt `skill-creator` can take as its
opening turn, and one backlog line so the fix is not forgotten.

Canonical reference: `WORKFLOWS/skill-test.md`. This is the trigger surface; that doc is the canon.
**Attended only.** One skill per run.

---

## Why the shape is what it is

- **Installed copy, not source.** The installed copy is what runs (DIR-009). Source-vs-installed
  drift belongs to `skill-audit`; if you notice it, it is one line in the report, never a fix.
- **Three runs, not one.** One sample never verifies a nondeterministic path (DIR-013). Agreement
  across three is the consistency read; disagreement is a finding in itself.
- **CRE's seat, not a rubric.** Where the output ends on his taste, his taste is the instrument
  (`_ME` § How I work with AI). Objective checks apply only where the skill's own doc names a
  measurable output (a file exists, a section is present, a count matches). Do not invent a score.
- **Gates are ruled in his stead, once, by the auditor, and listed.** A gate that stops the run
  tests nothing, and a ruling he cannot see is not a deferral (DIR-012 cl. 4). One ruling per gate
  goes to all three runs (CRE-ruled 2026-09-11) so the runs stay comparable; every stand-in ruling
  is listed in the report.
- **Scratch for writers, live for readers.** A test that mutates canon costs more to find and undo
  than it is worth (DIR-012). Skills that write run against a fixture under `SYSTEM/skill-tests/`.
- **Fix prompt, never a fix.** A skill changed without a gate is the adoption trap DIR-009 guards
  against. You write instructions and a backlog item; `skill-creator` and the pack chain do the rest.
- **File tools for every skill read and every `_BACKLOG` write.** Bash reads of the mount serve
  stale partials (DIR-005).

---

## Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or
missing → halt and ask which folder is the vault. Write nothing.

## Step 1 — Resolve the installed copy
The session's available-skills listing names each installed skill's location. Read
`<location>/SKILL.md` with the file tools, plus any `scripts/` and `references/` it ships. If the
skill is not in the listing, Glob with an explicit path under the AppData `skills-plugin` tree; a
miss there is confirmed by a second Glob, then reported: **not installed — route to the Install queue
(skills-manager)**, halt. Several skills named → first only, the rest as follow-ups.

Note the canon doc `WORKFLOWS/NAME.md` if present and read it once; if the two visibly disagree on
what the skill produces, that is the one drift line for the report. Test the installed copy.

## Step 2 — State the goal, ask for the bar
Write the skill's goal in **one line**, in plain speech, from the description and body. Then ask CRE
one batched question, with a proposed default for each part so he can answer in one pass:

1. **What must be true for the goal to count as met?** Propose two or three conditions derived from
   the doc's own outputs. He edits or accepts.
2. **A specific test case?** Propose one from the vault (a real chapter, a real report target) that
   is safe to use. He supplies his own or accepts.

Do not proceed on silence. The bar is his; the default exists so the answer costs one tap.

## Step 3 — Classify write behaviour and stage the fixture
Read the skill's outputs / "files this skill writes" surface. Decide:

- **Read-only** (writes nothing, or writes only its own report under `SYSTEM/reports/`) → runs may
  read the live vault. Redirect any report it writes into the run directory anyway.
- **Writes** anything else (chapter folders, `REFERENCE/`, `_BACKLOG`, canon docs) → copy every input
  the test case needs into `SYSTEM/skill-tests/NAME/DATE/fixture/` and point the runs there.
  When in doubt, treat the skill as a writer. A fixture that turns out unneeded costs a copy; a
  live write that turns out unwanted costs an undo.

Scaffold the tree with the shell script:

```
python3 "<VAULT>/WORKFLOWS/skills-src/skill-test/scripts/skill_test_shell.py" scaffold --vault "<VAULT>" --skill NAME --goal "<one line>"
```

It creates `SYSTEM/skill-tests/NAME/DATE/{fixture,run-1,run-2,run-3,audit}/` and a report stub at
`SYSTEM/reports/DATE-skill-test-NAME.md` with every required section present and empty. Substrate
(DIR-020): any non-mount host — desktop shell first, sandbox bash second; a denial is an expected
branch. No host → create the same tree and stub by hand with the file tools and say so in Not
checked.

## Step 4 — Run the panel (three isolated subagents, same turn)
Spawn three subagents in one turn, each with an identical brief. Each brief carries:

- the installed `SKILL.md` path (the subagent reads it itself; do not paste the skill body — the
  test is of the installed copy as it loads)
- the test case verbatim, and the fixture path if one was staged
- the **seat brief**: the goal line, CRE's success conditions, and the instruction to read `_ME.md`
  before ruling any gate
- the write surface: only `SYSTEM/skill-tests/NAME/DATE/run-K/` (and the fixture, for writers).
  Nothing under `WRITING/`, `REFERENCE/`, the OS anchors, `_BACKLOG`, or `_CHANGELOG`. The
  subagent does not log the session; this run does.
- the gate rule: when the skill under test stops for a ruling CRE would normally give, **stop and
  return the gate** — the question verbatim, the options the skill offered, and the option it
  recommended if any — with the run's state so far left in place. Do not rule it yourself.
- the return: a short summary (what it produced, where, whether it stopped at a gate and what the
  gate asks, anything it could not do) — paths, not content.

The subagents must not see each other's output. Do not read their outputs yourself before the
auditor has; your read would colour the brief you write for it. A gate question is not an output —
reading it is expected.

**Gate loop (CRE-ruled 2026-09-11, dec quick log).** When one or more runs return at a gate, spawn
the auditor (Step 5 brief, gate mode) with the gate question(s) and the seat brief. It rules each
gate **once**, from `_ME` and the stated goal, taking the skill's own recommendation when one is
offered and nothing in `_ME` argues against it, and writes the question, ruling, and one-line basis
to `audit/stand-in-rulings.md`. Send the **same ruling to all three runs** (`SendMessage` to each
run's agent) and let them resume. A run that reaches the gate later applies the ruling already on
file — one ruling per gate, never three. Repeat until all three runs return finished. This is why
the runs stay comparable: three independent stand-in rulings would turn a ruling divergence into a
false skill divergence, and the consistency read is what three runs buy.

## Step 5 — Audit from CRE's seat (one isolated subagent)
Spawn one auditor. Its brief carries: `_ME.md` (read in full), the goal line, the success
conditions, the test case, the installed `SKILL.md` path (for the measurable outputs its doc names,
nothing else), the three run directories, and `audit/stand-in-rulings.md`. In **gate mode** (Step
4 loop) it rules and returns; in **verdict mode** it answers, in order:

1. **Sound?** Is each output correct on its face and free of invented content, against the
   success conditions.
2. **Usable?** Could CRE take this output as-is and meet the goal, without re-doing the work.
3. **Consistent?** Do the three runs agree on what matters — same outputs, same rulings, same
   structure. Name every divergence and whether it changes the verdict.
4. **Stand-in rulings.** List every ruling it made in gate mode, with basis, and name any it
   believes was a taste call CRE should re-rule, with the `_ME` line it leaned on.
5. **Verdict.** `PASS` — usable as-is, three runs agree. `PASS-WITH-NOTES` — usable, with named
   caveats or a divergence that does not change the outcome. `FAIL` — not sound, not usable, or the
   runs disagree on the outcome.
6. **On FAIL or PASS-WITH-NOTES: the skill-creator handoff block.** Written so it can be pasted as
   `skill-creator`'s opening prompt: skill name and installed path; the goal; what the test showed,
   with paths to the evidence; the specific change wanted, as instructions with reasons, never a
   rewritten SKILL.md; what must be true after the fix; what not to change. Keep it to what the
   evidence supports.

The auditor judges from the seat brief. It does not grade against a rubric of its own. Where a
question ends on taste and the evidence does not settle it, it says so and rules
`PASS-WITH-NOTES` with the taste question named for CRE, rather than inventing a threshold.

## Step 6 — Write the report
Fill the stub at `SYSTEM/reports/DATE-skill-test-NAME.md`. Verdict first, path second, detail after.
Sections, in order (the stub carries them):

1. **Verdict line** — `VERDICT: PASS | PASS-WITH-NOTES | FAIL` and one plain sentence.
2. **Goal and bar** — the goal line, the success conditions as ruled, the test case verbatim.
3. **Runs** — RUN 1 / RUN 2 / RUN 3, each a short summary with output paths.
4. **Stand-in rulings** — every ruling from every run, with basis; the auditor's flags.
5. **Consistency** — what agreed, what diverged, whether it moved the verdict.
6. **Verdict detail** — sound / usable / consistent, in the auditor's words.
7. **skill-creator handoff** — present on FAIL or PASS-WITH-NOTES; the line `None — PASS` on PASS.
8. **Drift noticed** — one line, or `None noticed`. Route: `skill-audit`.
9. **Not checked (DIR-018)** — what the test could not exercise (a gate never reached, a live
   surface the fixture did not carry, a host that would not run the script).

Then check the report:

```
python3 ".../skill_test_shell.py" check --vault "<VAULT>" --report "<REPORT PATH>"
```

Exit `0` clean · `1` findings (a missing section, a verdict without its handoff block, a FAIL with
no backlog anchor) · `2` unreadable. Confirm any finding by file-tools re-read before acting on it.

## Step 7 — Backlog item (FAIL or PASS-WITH-NOTES only)
One `_BACKLOG.md` item at the top of `## OS / Meta`, file tools, targeted Edit, verified by re-read:

```
- [ ] **skill-test NAME — VERDICT DATE.** <one sentence: what fell short>. Fix prompt ready in
  [[SYSTEM/reports/DATE-skill-test-NAME]] § skill-creator handoff — open skill-creator with it,
  then the DIR-009 desktop pack chain. #p2 #gated ^backlog-skilltest-NAME-DATE
```

Re-run `check` afterwards so the backlog assertion passes.

## Step 8 — Chat and log
Chat: verdict, report path, and at most three lines of detail. No run-by-run narration.

Log per DIR-003: `_CHANGELOG` entry (meta lane, top-insert, file tools, verified by re-read); a
surprise about the *testing* → `_OBSERVATIONS`; nothing else. The skill-tests tree stays as
evidence; it is not cleaned up here.

---

## Files this skill writes — and must not

**Writes:** `SYSTEM/skill-tests/NAME/DATE/**` · `SYSTEM/reports/DATE-skill-test-NAME.md` · one
`_BACKLOG` item on FAIL / PASS-WITH-NOTES · a `_CHANGELOG` entry · optional `_OBSERVATIONS` line.

**Must NOT write:** the skill under test (installed, source, or package) · `WORKFLOWS/*.md` ·
anything under `WRITING/` or `REFERENCE/` · the OS anchors · `_DIRECTIVES` · task prompts.

## Unruled defaults in force (v1)

| Question | Default |
|---|---|
| Read-only skill touching live canon? | Allowed; any report it writes is redirected into its run dir. |
| Fixture scope? | Only what the test case needs, copied, never moved. |
| Cleanup of `SYSTEM/skill-tests/`? | Never here; evidence stays. `log-rotate` or CRE decides. |

Each is a default, not a ruling. CRE overrides any of them in a sentence.

## Stop conditions

- Sentinel fails → halt.
- Skill not installed → report, route to the Install queue, halt.
- CRE has not stated the bar → do not run; ask once with defaults, wait.
- Asked to fix, repack, or install the skill → refuse; hand over the handoff block.
- Asked to test several skills → first only.
- Asked to schedule this → decline; attended only.
- A run subagent tries to write outside its run dir → count the run as FAIL on that ground and say so.

## What this skill is NOT

- Not `skill-creator` — never authors or edits a skill; it writes the prompt `skill-creator` opens with.
- Not `skill-audit` — no drift diagnosis; one line if noticed.
- Not `skill-review` — no design, script, or load-cost review.
- Not `task-audit` — scheduled-task prompts are out of scope.
- Not a trigger-accuracy harness — that is `skill-creator` evals and `^autoresearch-trigger-harness`.
- Not scheduled, ever. Not more than one skill per run.
