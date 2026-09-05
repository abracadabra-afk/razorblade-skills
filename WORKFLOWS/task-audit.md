---
type: workflow
name: task-audit
trigger: audit the task prompts
aliases: [check task-prompt drift, are my scheduled tasks in sync, run the task doctor, which task prompts are stale, task prompt audit]
inputs: [the live scheduled-task SKILL.md prompts (via list_scheduled_tasks), WORKFLOWS/[name].md canon docs]
outputs: [a read-only drift report (chat or SYSTEM/reports/), a punch list of prompts to re-sync]
lane: meta
status: draft
last_updated: 2026-06-29
---

# WORKFLOW: task-audit

## When to use
A scheduled task runs a prompt at `C:\Users\Chad\Claude\Scheduled\<task>\SKILL.md` — a
hand-maintained surface that can silently lag its `WORKFLOWS/<name>.md` doc. `skill-audit` watches
the *Cowork-skill* chain (doc → `.skill` → installed); **nothing** watched the *scheduled-task*
chain until this. Triggers: **"audit the task prompts"**, "check task-prompt drift", "run the task
doctor", "which task prompts are stale". The detector half of `^backlog-task-prompt-drift`;
`^backlog-taskprompt-doc-drift` is the propagate half.

## Core discipline
- **Read-only.** Diagnoses drift; never edits a task prompt. Fixes stay CRE-attended via the
  `scheduled-tasks` `update_scheduled_task` API — **body-only, no frontmatter (`^obs-138`)** — and
  verified by re-reading the host `SKILL.md`.
- **Deterministic where it can be, human where it must be.** A bundled `task_audit.py` does the
  mechanical work (shape classification + convention lint + stamp-sha compare); the fuzzy
  "does this inline prompt still match its doc" call is a gated semantic read (Stage B), never
  automated.
- **The lint is the load-bearing value.** Both 2026-06-24 hits were mechanically detectable
  (`STALE-BOOK-NAME`, `CHANGELOG-FOOT-APPEND`); the `--selftest` proves the catch.
- File-tools only for any vault write; verify by re-reading (`^obs-020`/`^obs-014`). Stage the
  script + prompts off the mount before running (`^obs-103`/`^obs-084`).

## The three prompt shapes (`^obs-124`)
| Shape | Marker | Drift risk | Verdict path |
|---|---|---|---|
| doc-deferring | "Read `WORKFLOWS/<name>.md` and follow it", thin body | resistant | `CLEAN` — **unless it carries a summary block, see below** |
| inline-behavior | procedure baked into the body | **prone** (both hits) | `REVIEW` (or `DRIFT-*` if a signal/stamp fires) |
| runner-staged | logic in `runner.py` staged each run | cosmetic | `INFO` |

> ### ⚠️ `CLEAN` is a SHAPE verdict, not a CONTENT verdict (added 2026-08-03)
> A doc-deferring prompt is *supposed* to be a bare loader. In practice every one of them ships an
> **"In brief:" / "Summary of what to do:" / "the outline below"** block for orientation — and that
> block goes stale silently while the shape verdict stays `CLEAN`, so it never reaches the Step-5
> semantic pass. **The audit's one deterministically-clean row is the one nothing ever reads.**
>
> Live instance: the 2026-08-03 audit passed `vault-health` `CLEAN`. Its summary's Step 3 was
> instructing an **in-sandbox `_CHANGELOG` carve** — precisely what `log-rotate.md` forbids
> (`^obs-083`/`^obs-084`, carve is desktop-owned) — and its Step 1 omitted the
> `brain-doc-sizes.json` measurement path the doc names as preferred. That night's run got it right
> only by correctly preferring the doc over its own summary; an agent leaning on the summary would
> have performed the forbidden operation. The guardrail was holding on judgment, not instruction.
>
> **Rule:** a doc-deferring prompt with a summary block and **no `tracks:` stamp** routes to
> `REVIEW`. A stamp clears it, because the stamp converts doc movement into an exact `DRIFT-EXACT`
> signal — which is the entire purpose of stamping. Three ways to close such a row: add the stamp,
> delete the summary (the true loader shape), or rule it CLEAN at Stage B.

## Steps
1. **Sentinel** (`^obs-004`) — `_DIRECTIVES.md` frontmatter, else halt.
2. **Gather** — `list_scheduled_tasks` → read each `path` via the file tools → stage copies to the
   outputs scratch `prompts/<task>.md` (host dir is unreachable from bash).
3. **Stage + run** `task_audit.py --prompts-dir <scratch>/prompts --workflows <VAULT>/WORKFLOWS
   --map task_doc_map.json` (read the script via the file tools, `py_compile`, run from the clean
   copy). `--selftest` first if the script changed.
4. **Coherence guard** (`^obs-014`/`^obs-084`) — re-read any truncated/NUL-padded copy via the file
   tools before trusting it.
5. **Semantic pass** — for each `REVIEW`/`DRIFT-EXACT`, read prompt + mapped doc and rule HIT/CLEAN.
   This now includes doc-deferring rows flagged for an **unstamped summary block** — do not skip
   them because the shape looks right; that is the `^obs-236` hole.
6. **Orphan check** (standing step, CRE-ruled 2026-09-04) — compare `list_scheduled_tasks` against
   a directory listing of `C:\Users\Chad\Claude\Scheduled\`. A prompt dir with no registered task is
   an **orphan**: inert, unrunnable, and it lints as `NO-DOC` forever, recurring on every punch list
   as if it were live. Report each with its dir mtime. Do **not** delete — stage to
   `SYSTEM/_quarantine/<date>-orphan-task-prompts/` (the vault's holding pen; CRE rules disposal).
   The listing is a host-side read — bash cannot reach that dir, use Desktop Commander or the file
   tools. First run 2026-09-04: 19 dirs vs 16 tasks → `ghost-river-ingest`, `vault-backlog-agent`,
   `witchwood-pipeline-advance` quarantined; parity now 16/16.
7. **Report** — table + punch list + plain next-actions; for every mappable inline task, surface the
   option-(a) doc-deferral recommendation.
8. **Log** (explicit session only) — `_CHANGELOG` (meta, top-insert), `_OBSERVATIONS` for new
   fragility.

## Verdicts
`CLEAN` · `DRIFT-MECH` (lint signal — certain) · `DRIFT-EXACT` (stamp sha ≠ doc sha) · `REVIEW`
(inline with no stamp, **or doc-deferring with an unstamped summary block** — semantic read) ·
`BROKEN-REF` (loader doc missing) · `NO-DOC` (inline, unmapped) · `INFO` (runner-staged cosmetic).

## Lint signals
`STALE-BOOK-NAME` (HIGH) · `STALE-SCHED-PATH` (HIGH) · `CHANGELOG-FOOT-APPEND` (MED) ·
**`STALE-SNAPSHOT` (MED)** · `MISSING-NUL-GUARD` (ADVISORY).

**Two of these are negation-aware, and that is load-bearing.** A *corrected* prompt still contains
the forbidden string — "never a foot-append", "do NOT use the old VIBEBOOK/… paths" — so a naive
match flags the fix as the defect. `CHANGELOG-FOOT-APPEND` discounts an occurrence preceded by a
negation (`^obs-143`); `STALE-BOOK-NAME` discounts one on a line that *retires* the name
(`^obs-232`). **When you add a lint, check whether its siblings need the same exception**, and give
every exception a *paired* selftest (must-hit + must-clear) — `STALE-BOOK-NAME` was simultaneously
too broad (fired on the prohibition) and too narrow (case-sensitive, so blind to the real
mixed-case drift), and a one-sided test could not have caught that.

**Negations were discounted; IDENTIFIERS were not (fixed 2026-09-04, CRE-ruled off `^obs-282`).**
Two false positives had been burning a verdict every run since at least 08-09:

- `CHANGELOG-FOOT-APPEND` fired on **its own signal name**, because a prompt documenting the lint
  vocabulary contains the literal string and naming a signal is neither an authorization nor a
  negation. `task-audit`'s own prompt was the live instance.
- `STALE-BOOK-NAME` fired on the **live filename** `WORKFLOWS/weave-vibebook.md` — the current,
  correct doc name — hitting `books-daily-ingest-weave` every run.

**Why this mattered more than weekly noise:** a HIGH/MED lint flips the verdict to `DRIFT-MECH`,
and `DRIFT-MECH` **short-circuits the stamp comparison** in `audit_one` — so a genuinely stale
`tracks:` stamp could hide behind a false positive indefinitely. The fix is the reason, not the
annoyance.

**Both fixes widen the EXACT layer only** (DIR-014's corollary — never widen a fuzzy threshold to
catch a semantic miss). `_LINT_ID_RX` masks the all-caps signal identifiers, case-sensitively,
before the foot-append scan; `_BOOK_FILENAME_STEM` masks a retired name only when it is
hyphen-prefixed *and* inside a token ending `.md`. Slash-rooted retired paths (`VIBEBOOK/CAPTURE.md`)
and underscore-prefixed ones (`_DOBOOK.md`) are deliberately **not** masked and still hit. Three
paired selftests guard it (selftest count 25 → 28).

**`STALE-SNAPSHOT`** fires when a prompt measures or decides off a **dated artifact** — a
`SYSTEM/reports/*.json` stamp, a cached scan — without any freshness notion. Note the bar is
deliberately *both* an age test **and** a has-anything-written-since test: the `vault-health`
instance was fully compliant with its documented ≤ 36 h window and still measured ~13.5 K stale on
`_CHANGELOG`, because one session had written to all three brain docs inside the window. An age
window cannot see intra-window writes. This is DIR-010 at the artifact layer — a stamp is a dated
claim, not a probe.

## The provenance stamp (heuristic → exact)
A one-line comment on an inline prompt:
```
<!-- tracks: WORKFLOWS/research-briefing.md sha:<first-12-of-doc-sha> · stamped YYYY-MM-DD -->
```
lets `task_audit.py` compare the stamped sha to the doc's current sha for an exact verdict instead of
a "go read it" `REVIEW` (mirrors `skill-audit`'s optional `source_sha`). Re-stamp whenever a prompt is
deliberately re-synced. CRE ruled the stamp in (2026-06-29).

**`doc_sha()` resolves `WORKFLOWS/` first, then the VAULT ROOT** (2026-09-04, CRE-ruled). Before
this, a root-level canon doc could not be stamped at all: `mount-the-vault` defers to `CLAUDE.md` —
the canonical boot doc (`^obs-160`), of which `WORKFLOWS/vault-boot.md` is a *derived install* — and
a `tracks: CLAUDE.md` stamp reported "doc not found", so the one row whose prompt was demonstrably
correct was the one row that could never go clean. `task_doc_map.json` now maps `mount-the-vault` →
`CLAUDE.md`. CRE ruled the **resolver fix over an `expect_verdict` escape**: an escape suppresses
the verdict, the resolver makes the correct verdict *reachable* — DIR-018, never pass on a proxy.

## The option-(a) payload (the durable fix, not just the catch)
For every inline task that maps to a doc, recommend collapsing the prompt to the doc-deferring loader
— bootstrap → sentinel → "Read `WORKFLOWS/<name>.md` and follow it in SCHEDULED MODE" → the few
task-local params → log. The three clean tasks (`skills-sweep`/`backlog-sweep`/`vault-health`) are
exactly this shape. **Pilot: `research-runner`** (its Step 2 already reads its doc; Steps 3–9 just
restate it). Limits: `vault-backlog-agent` has no doc (author one first); composing tasks defer to
two docs but still need a thin shell; runner-staged tasks already defer to `runner.py`; a doc-read
that fails must degrade safely (sentinel + "if the doc won't read, stop, don't improvise").

## Bundled assets
- `skills-src/task-audit/task_audit.py` — the deterministic linter (`--selftest` GREEN 11/11, 2026-06-29).
- `skills-src/task-audit/task_doc_map.json` — the committed task→doc map (keep current on task add/rename).

## Status / fragility
- **status: draft** — canon doc + skill source + script + map authored & tested 2026-06-29
  (`^obs-141`). `.skill` packaging + install pending (desktop `pack-skills.ps1` + Save-skill);
  registration row added to `_SKILLS MAP`. Next: the `tracks:`-stamping pass (pilot research-runner),
  then roll option-(a) conversions one task at a time (each prompt edit CRE-attended, `^obs-138`).
- Design draft + rationale: `SYSTEM/reports/2026-06-29-task-prompt-drift-detector-design.md`.
