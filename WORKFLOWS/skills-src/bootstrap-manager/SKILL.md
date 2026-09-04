---
name: bootstrap-manager
description: 'Review the five files every vault session loads — CLAUDE.md plus the loading-order anchors _ME, _VAULT MAP, _SKILLS MAP, _DIRECTIVES — and propose evidence-graded fixes so the bootstrap carries instructions a cold agent can act on rather than generalities it must rediscover. Use when CRE says "review the bootstrap," "audit the anchors," "tune the boot doc," or "run the bootstrap manager." Mines the vault record (_OBSERVATIONS, DECISIONS/, SYSTEM/reports/, LIFE/MENTAL HEALTH/) for repeated patterns in how CRE thinks, rules and collaborates, then writes a three-bin punch list (BATCH-RATIFY / PROPOSED / QUERY) with quoted replacement text to SYSTEM/reports/. Every PROPOSED item cites two independent instances; cuts are graded on the same bar. Proposes everything, writes only what CRE rules. Attended only, never scheduled. Do NOT use for skill drift (skill-audit), prompt drift (task-audit), broken links (link-audit), file size (log-rotate), skill design (skill-review), or to author a directive.'
---

# bootstrap-manager

You are reviewing the **content** of the five files every session in this vault loads before it does
anything else: `CLAUDE.md` and the four loading-order anchors `_ME`, `_VAULT MAP`, `_SKILLS MAP`,
`_DIRECTIVES`. Everything downstream is capped by how concretely those five describe how CRE
actually works.

The gap you exist to close, concretely: `_ME` says *"top-down"* and *"ADHD"* and stops, while a
19-pattern map of how CRE stalls, decides and restarts sits in `LIFE/MENTAL HEALTH/ADHD Patterns.md`
and never reaches the file every session loads. `LIFE/MENTAL HEALTH/AI Helper Targets.md` shows the
target form — it cites patterns *by number against a concrete behavior* (#3
planning-as-procrastination, #8 working memory, #15 time blindness). That is the specificity level
the anchors are missing.

Canonical reference: `WORKFLOWS/bootstrap-manager.md`. This is the AI-trigger surface; that doc is
the in-vault canon. **Attended only — there is no scheduled or unattended mode.**

---

## The one rule that makes this pass worth running

**Two independent instances, each cited by anchor or path, or the item is not PROPOSED.**

- One correction is an anecdote, not a pattern. DIR-010 §3 requires a recommendation's
  highest-weighted criterion be traced to vault evidence before it ships.
- *Independent* means two different sessions, decisions, or observations. A `_CHANGELOG` entry and
  the `^obs-NNN` it filed are **one** instance, not two.
- Under the bar → **QUERY**, never PROPOSED. QUERY is where a real-looking pattern waits for its
  second instance, not a rejection bin.
- **Re-verify every citation by direct file-tools read before it enters the report.** A `Grep` hit
  is a pointer; the mount lies about freshness (DIR-005). A wrong citation converts a review into a
  fabrication CRE has to police, which is worse than a missing item.

**Cuts are graded on the same bar.** These five files load in full every session and DIR-002 forbids
preloading, so a generality that has never changed an outcome is pure cost — and a pass that only
adds makes the bootstrap worse over time. A proposed cut cites two instances of the line failing to
bind, of the same instruction living somewhere that does bind, or of a session where the line was
loaded and the outcome went the way the line forbids.

---

## Anti-rules (a naive pass gets these wrong on this vault)

1. **The affective lane never becomes an instruction (DIR-015).** Executional patterns — restart
   loop (#1), tool abandonment (#2), planning-as-procrastination (#3), avoidance (#5), working
   memory (#8), time blindness (#15) — are in bounds and become named collaboration instructions.
   Affective patterns (#4, #11, #12, #13, #14, #19) are named once and **never turned into an
   instruction to work them**. The anchors are a standing instruction set; a standing instruction to
   process shame is exactly what DIR-015 forbids. No proposed line may direct a session to reassure,
   reframe, validate, or process.
2. **Never author a directive.** `_DIRECTIVES` is the binding rulebook and entries land only after
   CRE reviews the source observation. A rule you believe in goes to `_OBSERVATIONS` as a `^obs-NNN`
   with a candidate-directive line and a recurrence condition — the existing graduation path — and
   the report says so. A `_DIRECTIVES` edit here is a pointer or scope line CRE ruled, never a new DIR.
3. **Report drift in the derived boot surfaces; never edit them.** `^obs-160` makes `CLAUDE.md`
   canonical and the rest regenerated installs. DIR-016 binds after: a ratified `CLAUDE.md` edit
   ends with a **named regeneration list**, not a silent divergence.
4. **Never propose text that steers what CRE creates.** AI executes, CRE creates. Read
   `_CREATIVE DIRECTIVES` and `_CREATIVE OBSERVATIONS` as *evidence of his working patterns*; never
   propose a line about his fiction voice, register, or craft judgment. For v1 the creative pair is
   **flag-only** — a QUERY item, never an edit.
5. **Do not restructure the OS.** Line-level changes to five files. Nothing about the domain roots,
   the routing table, or the loading order itself beyond what evidence names.
6. **A fork inside a proposal is not ruled here.** Two defensible wordings, or a real trade-off,
   goes to CRE as one question — or to `decision-helper`. You measure; you do not rule.
7. **BATCH-RATIFY is the least-scrutinized bin on the sheet.** `^obs-297` is the specimen: a
   mechanical-looking item got batch-ratified against CRE's own newer ruling. Nothing enters
   BATCH-RATIFY unless it is a factual correction with **no behavioral consequence** — a wrong
   count, a stale cross-reference, a duplicated line. Anything that changes what a session *does* is
   PROPOSED, individually, with its evidence visible.

---

## Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or
missing → **halt** and ask which folder is the vault. Write nothing.

## Step 1 — Read the boot surface in full
`CLAUDE.md`, `_ME.md`, `_VAULT MAP.md`, `_SKILLS MAP.md`, `_DIRECTIVES.md` — all five, end to end,
through the file tools. Record each file's size and the boot total. The budget is why cuts matter:
boot cost was deliberately cut from ~33k to ~4k tokens once already (`^obs-275`).

## Step 2 — Carry the prior review forward
Glob `SYSTEM/reports/*bootstrap-review*`. If one exists, read the most recent and build the
**rejected/retired list**: every item CRE declined, every line an earlier run cut. Nothing on that
list is re-proposed unless this run has a *new* instance dated after the prior review — and the item
then says so explicitly. Re-proposing a closed call is the friction CRE names by name (`^obs-280`).
No prior review → say so on the report; the list is empty, not skipped.

## Step 3 — Mine the record for demonstrated patterns
Read for **repeated, demonstrated patterns in how CRE thinks, rules and collaborates** — never for
vault mechanics, which the sibling audits own.

| Surface | What it yields |
|---|---|
| `_OBSERVATIONS.md` | how he corrects, what he catches that instruments do not, what he refuses to re-rule |
| `DECISIONS/` (`_QUICK LOG`, `_WEIGHTS`, dated entries) | his ruling criteria, his override direction, how he parks |
| `_CHANGELOG.md` | ruling throughput, batch behaviour, what a session actually asked him |
| `_CREATIVE OBSERVATIONS.md` + `_CREATIVE DIRECTIVES.md` | working patterns only — evidence, never a craft proposal |
| `SYSTEM/reports/` | what past passes deferred to him, and how that landed |
| `LIFE/MENTAL HEALTH/` (Patterns · AI Helper Targets · ADHD Writing Process · ADHD Story Contruction) | the executional pattern set, by number, with interventions |
| Session transcripts | live correction shape — *where a transcript tool is reachable* |

**Transcripts:** read them where a transcript tool is reachable; where it is not, state the covered
range and the gap on the report rather than skipping the surface silently.

Fan-out is encouraged — one isolated subagent per surface, each returning *pattern + citations +
short verbatim quote*, is cheaper and less blending-prone than one pass over everything. Every
returned citation is re-verified by direct read before it reaches the report.

Signals worth reading for specifically, because they are the ones a cold session gets wrong:
- what he consistently rejects, and the *shape* of his corrections
- how he prefers to be asked — batch size, cap, one recommendation vs a menu
- what makes him stall, and what work he never gets to because it waits on him
- his ruling criteria, and which criterion carries the most weight
- what he has repeatedly had to tell a session that the anchors never told it

## Step 4 — Draft proposals in both directions
For each surviving pattern write the **actual replacement text, quoted, in the voice of the target
file**. Two directions, both required:

- **ADD** — a line that *would have changed a past outcome*. Name the outcome.
- **CUT** — a line that has never changed one. Name what carries the instruction instead.

Every item states: target file · the exact anchor text it replaces or the section it lands in · the
proposed text verbatim · two citations · the outcome it would have changed · direction.

**The behavioral test:** the proposed text reads as something a cold session could apply *without
asking a question*. A line needing interpretation is not finished — rewrite it or move it to QUERY.

## Step 5 — Derived-surface check (report only)
For every item targeting `CLAUDE.md`, name the derived installs needing regeneration (DIR-016).
Current set per `^obs-160`:

1. the `mount-the-vault` scheduled-task `SKILL.md` prompt
2. the `vault-boot` skill (`WORKFLOWS/skills-src/vault-boot/SKILL.md` + `WORKFLOWS/vault-boot.md`)
3. the Cowork `userPreferences` block
4. `_SESSION START.md`

Read each to confirm it is still a derived install and whether it currently agrees with `CLAUDE.md`.
**Never edit one here.**

## Step 6 — Run the linter
```
python3 "<VAULT>/WORKFLOWS/skills-src/bootstrap-manager/scripts/lint_bootstrap.py" --vault "<VAULT>" --report "<REPORT PATH>" [--json]
```
**Run the script from the vault source path above, not from `SKILLDIR/`.** The `.skill` package
ships `scripts/lint_bootstrap.py`, but a Save-skill install of this SKILL.md alone does not carry
it; the vault copy is always present and always current. `SKILLDIR/scripts/lint_bootstrap.py` is a
valid fallback when the installed copy does have it.

Substrate (DIR-020): **any non-mount host.** Prefer the desktop shell (Desktop Commander
`start_process` / `windows-cli`) — it reads the real Dropbox folder; sandbox `bash` is an acceptable
second. The first bash call is a **live entitlement probe, never an assumption** — a denial is an
expected branch (`^obs-281`, `^obs-284`), not an error. **This workflow is not bash-blocked:** if no
host runs it, perform the checks by hand from the file-tools read and say which ones in Not-checked.

Checks: `SIZE` boot-surface census · `CITES` every PROPOSED item carries ≥2 distinct citations ·
`BIN` nothing under the bar sits outside QUERY · `TEXT` every item names a target and quotes
replacement text · `NOTCHECKED` a coverage section exists and states a date range · `REGEN` a
regeneration list exists if any item targets `CLAUDE.md`. Exit `0` clean · `1` findings · `2` gate
failure. `--selftest` proves the catches. Confirm every finding by file-tools re-read.

## Step 7 — Write the report
`SYSTEM/reports/YYYY-MM-DD-bootstrap-review.md`, severity-ranked:

1. **Verdict line** — one sentence: the boot surface's state, bin counts, the single biggest gap.
2. **BATCH-RATIFY** — factual corrections, no behavioral consequence. Ratified as one.
3. **PROPOSED** — target · quoted replacement text · two citations · outcome it would have changed ·
   ADD or CUT.
4. **QUERY** — under the bar, a fork, or a protected surface. Tree-researched first (DIR-011);
   present as *resolved against X — confirm* wherever the tree answers it.
5. **Directive candidates** — routed to the `_OBSERVATIONS` → CRE-review graduation path, never
   written. Each with its recurrence condition.
6. **Derived-surface regeneration list** — from Step 5.
7. **Rejected / retired, carried forward** — from Step 2.
8. **Not checked (DIR-018)** — surfaces unreachable (transcripts especially), the date range
   actually covered, what the linter did not run. A review that passed on partial evidence has not
   reviewed the thing, and its blind spot belongs where CRE will see it.

Chat gets the verdict line and the bin counts, in plain English, no vault jargon in the lead. The
report carries the detail; chat does not repeat it.

## Step 8 — CRE rules
Present the bins. He ratifies, amends, declines, or parks per item; BATCH-RATIFY goes as one tap.
**Nothing is written before this.** A declined item joins the rejected list for the next run.

## Step 9 — Apply the ratified items
Targeted **file-tool edits only** — never `patch_vault_file`, never a whole-file MCP rewrite; both
have silently truncated canon here (DIR-005). Then **re-read every edited file through the file
tools** and confirm the new text is present and the surrounding text intact. Bump each edited file's
`last_updated`. A ratified `CLAUDE.md` edit closes by restating the regeneration list as an open
item — the edit is not shipped until every executing surface knows it (DIR-016).

## Step 10 — Log
`_CHANGELOG` entry, meta lane, top-insert, file tools, verified by re-read. New surprises →
`_OBSERVATIONS` (`^obs-NNN`; scan the file for the live max first). Directive candidates and any
unserved ruling → `_BACKLOG` under `## Needs CRE ruling (bootstrap-manager DATE)` (DIR-012 clause 5).

---

## Files this skill writes — and must not

**Writes:** `SYSTEM/reports/YYYY-MM-DD-bootstrap-review.md`; a `_CHANGELOG` entry; optional
`_OBSERVATIONS` / `_BACKLOG` lines; and — **only after CRE rules each item** — targeted edits to
`CLAUDE.md`, `_ME.md`, `_VAULT MAP.md`, `_SKILLS MAP.md`, `_DIRECTIVES.md`.

**Must NOT write:** any derived boot surface (`_SESSION START.md`, the `mount-the-vault` prompt, the
`vault-boot` skill, the Cowork preferences block) · a new `DIR-NNN` · `_CREATIVE DIRECTIVES` ·
anything under `WRITING/` · any anchor line CRE has not ruled.

## Unruled defaults in force (v1)

| Question | Default |
|---|---|
| Read Cowork session transcripts, and by what route? | Read where a transcript tool is reachable; state the covered range and the gap when it is not. |
| Ratified write inside this skill, or a separate landing pass? | Inside — mechanical once he has ruled. |
| Propose changes to `_CREATIVE DIRECTIVES` (the conditional sixth surface)? | No for v1 — flag only, as a QUERY item. |
| How does a later run avoid re-proposing something an earlier run cut? | Read the prior review first; carry a rejected/retired list forward. |

Each is a default, not a ruling. CRE overrides any of them in a sentence.

## Stop conditions

- Sentinel fails → halt, ask which folder is the vault.
- Any of the five files unreadable → halt; a partial boot surface cannot be reviewed.
- Asked to apply an item CRE has not ruled → refuse and report; there is no unattended mode.
- Asked to write a directive → route to the `_OBSERVATIONS` graduation path, never author.
- Asked to fix a derived boot surface → report the drift, hand over the regeneration list.
- Asked to run this on a schedule → decline; attended only.
- No host will run the linter → **not blocked**; hand-run the checks and say so in Not-checked.

## What this skill is NOT

- Not `skill-audit` — no source-vs-build-vs-installed drift; not for skill packaging state.
- Not `task-audit` — not for reconciling scheduled-task prompts against their canon docs.
- Not `link-audit` — not a link checker.
- Not `log-rotate` — not for file size bands (size is read only as budget context).
- Not `skill-review` — not for one skill's design or load cost.
- Not `decision-helper` — a fork inside a proposal goes to CRE or there, never ruled here.
- Not a directive author. Not an OS restructure. Not craft or fiction work of any kind.
- Not scheduled, ever.
