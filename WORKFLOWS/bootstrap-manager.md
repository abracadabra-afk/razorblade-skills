---
type: workflow
name: bootstrap-manager
trigger: review the bootstrap
aliases: [audit the anchors, tune the boot doc, run the bootstrap manager, bootstrap review, tighten the bootstrap]
inputs: [CLAUDE.md + the four loading-order anchors (_ME, _VAULT MAP, _SKILLS MAP, _DIRECTIVES); the vault's own record — _CHANGELOG, _OBSERVATIONS, _CREATIVE OBSERVATIONS, DECISIONS/, SYSTEM/reports/, LIFE/MENTAL HEALTH/; the prior bootstrap review if one exists]
outputs: [SYSTEM/reports/YYYY-MM-DD-bootstrap-review.md — verdict line + BATCH-RATIFY / PROPOSED / QUERY bins with quoted replacement text + rejected-carry-forward + Not-checked; after CRE rules, targeted file-tool edits into the five files, each verified by re-read; a named regeneration list for any derived boot surface a ratified CLAUDE.md edit affects]
lane: meta
status: draft
last_updated: 2026-09-04
revision_note: v1 authored 2026-09-04. First live run same day — report at SYSTEM/reports/2026-09-04-bootstrap-review.md. Attended only, never scheduled.
---

# WORKFLOW: bootstrap-manager

## When to use

Every session in this vault opens the same five files — `CLAUDE.md` and the four loading-order
anchors — and everything downstream inherits how concretely those five describe how CRE actually
works. Right now they describe him in generalities a cold agent cannot act on, so each session
rediscovers his collaboration and decision patterns or fails to and he corrects it by hand.

The gap this exists to close, stated concretely: `_ME` says *"top-down"* and *"ADHD"* and stops,
while a 19-pattern map of how CRE stalls, decides and restarts sits in
`LIFE/MENTAL HEALTH/ADHD Patterns.md` and never reaches the file every session loads.
`LIFE/MENTAL HEALTH/AI Helper Targets.md` shows the target form — it cites patterns *by number
against a concrete behavior* (#3 planning-as-procrastination, #8 working memory, #15 time
blindness). That is the specificity level the anchors are missing.

**Triggers:** "review the bootstrap" · "audit the anchors" · "tune the boot doc" ·
"run the bootstrap manager".

**Cadence:** attended, every couple of months, or after a stretch of sessions that went sideways.
**Never scheduled** — every item on the report is a judgment call about a file that binds every
future session, and DIR-012 puts that class behind CRE.

## The axis it owns (and its neighbors)

| Skill | Question it answers |
|---|---|
| `skill-audit` | Does the installed skill copy match its source? (doc → `.skill` → installed drift) |
| `task-audit` | Does a scheduled-task prompt still match its canon doc? |
| `link-audit` | Do the vault's references resolve? |
| `log-rotate` | Are the brain docs past the size where the tools stop being safe? |
| `skill-review` | Is one skill shaped right, scripted where it should be, cheap to load? |
| **`bootstrap-manager`** | Do the five files every session loads say things a cold agent can **act on** — and does each line still earn its place? |

Same neighbourhood, different question. This one reads **content**, not drift, not references, not
bytes. It is the only pass that treats the boot surface as a product with a user.

## Governing principle — propose everything, write only what CRE ruled

DIR-002 makes these five files the loading order every session obeys. A wrong line here is applied
silently in every future run before anyone notices — the most expensive failure surface in the
vault. So the pass is two-phase without exception: **report → CRE rules → apply**. There is no
mode in which it edits an anchor on its own judgment, and no bin whose contents are written
without a ruling.

The ratified-write step lives **inside** this skill rather than routing to a separate landing pass:
once CRE has ruled an item, applying it is mechanical, and a second trip costs him a second sitting
for nothing.

## The evidence bar (the rule that makes this pass worth running)

**Two independent instances, each cited by anchor or path, or the item is not PROPOSED.**

- One correction is an anecdote, not a pattern. DIR-010 §3 requires a recommendation's
  highest-weighted criterion be traced to vault evidence before it ships.
- "Independent" means two different sessions, decisions, or observations — not the same event
  recorded on two surfaces. A `_CHANGELOG` entry and the `^obs-NNN` it filed are **one** instance.
- Anything that cannot cite twice goes to **QUERY**, never PROPOSED. QUERY is not a rejection bin;
  it is where a real-looking pattern waits for its second instance.
- **Every citation is re-verified by direct read before it enters the report** (DIR-005: a `Glob`
  or `Grep` hit is a pointer, and the mount lies about freshness). A wrong citation is worse than
  a missing one, because it converts a review into a fabrication CRE has to police.

### Cuts are graded on the same bar

These five files load in full every session and DIR-002 forbids preloading, so a generality that
has never changed an outcome is pure cost. **A pass that only adds makes the bootstrap worse over
time.** A proposed cut therefore carries the same two instances — of the line failing to bind, of
the same instruction living somewhere else that does bind, or of a documented session where the
line was present and the outcome went the way the line forbids. A cut that cannot cite twice is a
QUERY like any other.

## Anti-rules (why a naive pass gets this vault wrong)

1. **The affective lane never becomes an instruction.** DIR-015 splits the pattern map hard.
   Executional patterns — restart loop (#1), tool abandonment (#2), planning-as-procrastination
   (#3), avoidance (#5), working memory (#8), time blindness (#15) — are in bounds and become
   named collaboration instructions. Affective patterns (#4, #11, #12, #13, #14, #19) are named
   once and **never turned into an instruction to work them**. The anchors are a standing
   instruction set; a standing instruction to process shame is exactly what DIR-015 forbids.
   No proposed anchor line may direct a session to reassure, reframe, validate, or process.
2. **Never author a directive.** `_DIRECTIVES` is the binding rulebook and entries land only after
   CRE reviews the source observation. A rule this pass believes in goes to `_OBSERVATIONS` as a
   `^obs-NNN` with a candidate-directive line and a recurrence condition — the existing graduation
   path — and the report says so. Editing `_DIRECTIVES` here means adding a *pointer or a scope
   line CRE ruled*, never a new DIR.
3. **Report drift in the derived boot surfaces; never edit them.** `^obs-160` makes `CLAUDE.md`
   canonical and the rest regenerated installs of it. DIR-016 binds after that: a ratified
   `CLAUDE.md` edit ends with a **named regeneration list**, not a silent divergence.
4. **Never propose text that steers what CRE creates.** AI executes and CRE creates. This pass
   reads `_CREATIVE DIRECTIVES` and `_CREATIVE OBSERVATIONS` as *evidence of his working patterns*
   and never proposes a line about his fiction voice, register, or craft judgment.
5. **Do not restructure the OS.** Line-level changes to five files. Nothing about the domain roots,
   the routing table, or the loading order itself beyond what the evidence names.
6. **A fork inside a proposal is not ruled here.** Two defensible wordings, or a real trade-off,
   goes to CRE as one question — or to `decision-helper` if it needs weighing. This pass measures;
   it does not rule.
7. **The BATCH-RATIFY bin is the least-scrutinized bin on the sheet.** `^obs-297` is the specimen:
   a mechanical-looking item got batch-ratified against CRE's own newer ruling. Nothing enters
   BATCH-RATIFY unless it is a factual correction with no behavioral consequence — a wrong count,
   a stale cross-reference, a duplicated line. Anything that changes what a session *does* is
   PROPOSED, individually, with its evidence visible.

## Substrate (DIR-020)

Every read and every write in this workflow runs on the **file tools** against the vault folder —
that is the substrate, and it is not optional, because DIR-005 puts the five target files in the
file-tools-only class.

The one mechanical step, `scripts/lint_bootstrap.py`, names its substrate as **any non-mount
host**: the desktop shell (Desktop Commander `start_process` or `windows-cli`) is the preferred
route because it reads the real Dropbox folder; sandbox `bash` is an acceptable second. A run's
first bash call is a **live entitlement probe, never an assumption** — a denial is an expected
branch (`^obs-281`, `^obs-284`), not an error.

**This workflow is not bash-blocked.** If no host will run the script, the linter's checks are
performed by hand from the file-tools read and the report's Not-checked line says which ones were
hand-run. The script normalizes the evidence-bar arithmetic; it never decides an item.

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or
missing → **halt** and ask which folder is the vault. Write nothing.

### Step 1 — Read the boot surface in full
`CLAUDE.md`, `_ME.md`, `_VAULT MAP.md`, `_SKILLS MAP.md`, `_DIRECTIVES.md` — all five, end to end,
through the file tools. Record each file's size and the boot total; the budget is the reason cuts
matter (`^obs-275`: boot cost was cut from ~33k to ~4k tokens once, deliberately).

### Step 2 — Carry the prior review forward
Glob `SYSTEM/reports/*bootstrap-review*`. If one exists, read the most recent and build the
**rejected/retired list**: every item CRE declined, and every line an earlier run cut. Nothing on
that list may be re-proposed unless this run has a *new* instance dated after the prior review —
and the item then says so explicitly. Re-proposing a closed call is the friction CRE names by
name (`^obs-280`: *"Every one had the same answer … and every one was presented as a decision."*).
No prior review → say so on the report; the list is empty, not skipped.

### Step 3 — Mine the record for demonstrated patterns
Read for **repeated, demonstrated patterns in how CRE thinks, rules and collaborates** — never for
vault mechanics, which the sibling audits own. Surfaces, in order of density:

| Surface | What it yields |
|---|---|
| `_OBSERVATIONS.md` | how he corrects, what he catches that instruments don't, what he refuses to re-rule |
| `DECISIONS/` (`_QUICK LOG`, `_WEIGHTS`, dated entries) | his ruling criteria, his override direction, how he parks |
| `_CHANGELOG.md` | ruling throughput, batch behaviour, what a session actually asked him |
| `_CREATIVE OBSERVATIONS.md` + `_CREATIVE DIRECTIVES.md` | working patterns only — evidence, never a craft proposal (anti-rule 4) |
| `SYSTEM/reports/` | what past passes deferred to him and how that landed |
| `LIFE/MENTAL HEALTH/` (Patterns, AI Helper Targets, ADHD Writing Process, ADHD Story Contruction) | the executional pattern set, by number, with interventions |
| Session transcripts | live correction shape — *where a transcript tool is reachable* |

**Transcripts (default in force, unruled):** read them where a transcript tool is reachable; where
it is not, state the covered range and the gap on the report rather than skipping the surface
silently.

Fan-out is allowed and encouraged — one isolated subagent per surface, each returning
*pattern + citations + verbatim quote*, is cheaper and less blending-prone than one pass over
everything. Every returned citation is re-verified by direct read (the evidence bar) before it
reaches the report.

### Step 4 — Draft proposals in both directions
For each surviving pattern, write the **actual replacement text**, quoted, in the voice of the
target file. Two directions, both required:

- **Additions** — a line that *would have changed a past outcome*. The item names the outcome.
- **Cuts** — a line that has never changed one. The item names what carries the instruction
  instead, or the sessions where the line was loaded and ignored.

Every item states: the target file · the exact anchor text it replaces or the section it lands in ·
the proposed text verbatim · two citations · the outcome it would have changed. **The test:** the
proposed text reads as something a cold session could apply without asking a question. A line that
requires interpretation is not finished — rewrite it or move it to QUERY.

### Step 5 — Derived-surface check (report only)
For every item targeting `CLAUDE.md`, name the derived installs that would need regenerating
(DIR-016). The current set, per `^obs-160`:

1. the `mount-the-vault` scheduled-task `SKILL.md` prompt
2. the `vault-boot` skill (`WORKFLOWS/skills-src/vault-boot/SKILL.md` + `WORKFLOWS/vault-boot.md`)
3. the Cowork `userPreferences` block
4. `_SESSION START.md`

Read each to confirm it is still a derived install and record whether it currently agrees with
`CLAUDE.md`. **Never edit one here** — the regeneration is its own attended act, and this pass
hands over the list.

### Step 6 — Run the linter
```
python3 SKILLDIR/scripts/lint_bootstrap.py --vault "<VAULT>" --report "SYSTEM/reports/YYYY-MM-DD-bootstrap-review.md" [--json]
```
Checks: boot-surface size census · every PROPOSED item carries ≥2 distinct citations · no item with
<2 citations sits outside QUERY · every item names a target file and quotes replacement text ·
a Not-checked section exists and states a date range · a regeneration list exists if any item
targets `CLAUDE.md`. Exit `0` clean · `1` findings · `2` gate failure. `--selftest` proves the
catches. Confirm every finding by file-tools re-read before acting on it.

### Step 7 — Write the report
`SYSTEM/reports/YYYY-MM-DD-bootstrap-review.md`, severity-ranked, in this shape:

1. **Verdict line** — one sentence: the boot surface's state, the bin counts, the single biggest gap.
2. **BATCH-RATIFY** — factual corrections with no behavioral consequence. Batch-ratify as one.
3. **PROPOSED** — the real changes, each with target · quoted replacement text · two citations ·
   the outcome it would have changed · direction (ADD / CUT).
4. **QUERY** — under the two-instance bar, or a fork, or a protected surface. Each tree-researched
   first (DIR-011) and presented as *resolved against X — confirm* wherever the tree answers it.
5. **Directive candidates** — routed to the `_OBSERVATIONS` → CRE-review graduation path, never
   written. Each with its recurrence condition.
6. **Derived-surface regeneration list** — from Step 5.
7. **Rejected / retired, carried forward** — from Step 2.
8. **Not checked (DIR-018)** — the surfaces that were unreachable (transcripts especially), the
   date range actually covered, and what the linter did not run. A review that passed on partial
   evidence has not reviewed the thing, and its blind spot belongs where CRE will see it.

Chat gets the verdict line and the bin counts. The report carries the detail.

### Step 8 — CRE rules
Present the bins. He ratifies, amends, declines, or parks per item; BATCH-RATIFY goes as one tap.
Nothing is written before this. An item he declines joins the rejected list for the next run.

### Step 9 — Apply the ratified items
Targeted **file-tool edits only** — never `patch_vault_file`, never a whole-file MCP rewrite; both
have silently truncated canon here (DIR-005). Then **re-read every edited file through the file
tools** and confirm the new text is present and the surrounding text is intact. Bump each edited
file's `last_updated`. A ratified `CLAUDE.md` edit closes by restating the regeneration list as an
open item — the edit is not shipped until every executing surface knows it (DIR-016).

### Step 10 — Log
`_CHANGELOG` entry, meta lane, top-insert, file tools, verified by re-read. New surprises →
`_OBSERVATIONS` (`^obs-NNN`, scan the file for the live max first). Directive candidates and any
unserved ruling → `_BACKLOG` under `## Needs CRE ruling (bootstrap-manager DATE)`
(DIR-012 clause 5). Creative-lane craft observations are not this pass's output — it is meta lane.

## Stop conditions

- Sentinel fails → halt, ask which folder is the vault.
- Any of the five files unreadable → halt; a partial boot surface cannot be reviewed.
- Asked to apply an item CRE has not ruled → refuse and report; there is no unattended mode.
- Asked to write a directive → route to the `_OBSERVATIONS` graduation path, never author.
- Asked to fix a derived boot surface → report the drift and hand over the regeneration list.
- Asked to run this on a schedule → decline; attended only.
- No host will run the linter → **not blocked**; hand-run the checks and say so in Not-checked.

## Logging

Meta lane. One `_CHANGELOG` entry per run naming the verdict line, the bin counts, and which items
were ratified and applied. The report carries the detail; the changelog does not repeat it.

## Unruled defaults in force (v1)

| Question | Default | Where it is recorded |
|---|---|---|
| May the run read Cowork session transcripts, and by what route? | Read where a transcript tool is reachable; state the covered range and the gap on the report when it is not. | Step 3 |
| Ratified write inside this skill, or a separate landing pass? | Inside — the write is mechanical once he has ruled. | Governing principle, Step 9 |
| Does it also propose changes to `_CREATIVE DIRECTIVES` (the conditional sixth surface)? | No for v1 — **flag only**, as a QUERY item. | Anti-rule 4 |
| How does a later run avoid re-proposing something an earlier run cut? | It reads the prior review first and carries a rejected/retired list forward. | Step 2 |

Each is a default, not a ruling. CRE overrides any of them in a sentence.

## Packaging

Source `WORKFLOWS/skills-src/bootstrap-manager/` (SKILL.md + `scripts/lint_bootstrap.py`). Pack on
the desktop with `pack-skills.ps1`, sha-verify packaged vs source bytes, Save-skill (DIR-009).
Description is single-quoted in the frontmatter — an unquoted `#` opens a YAML comment and the
installer silently truncates the description (`^obs-299`).

## What this is NOT

- Not `skill-audit` — no source-vs-build-vs-installed drift; do not use it for skill packaging state.
- Not `task-audit` — do not use it to reconcile scheduled-task prompts against their canon docs.
- Not `link-audit` — do not use it as a link checker.
- Not `log-rotate` — do not use it for file size bands (it reads size only as budget context).
- Not `skill-review` — do not use it to review a skill's design or load cost.
- Not `decision-helper` — a fork inside a proposal goes to CRE or there, never ruled here.
- Not a directive author. Not an OS restructure. Not craft or fiction work of any kind.
- Not scheduled, ever.
