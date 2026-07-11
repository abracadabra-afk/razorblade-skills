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
| doc-deferring | "Read `WORKFLOWS/<name>.md` and follow it", thin body | resistant | `CLEAN` |
| inline-behavior | procedure baked into the body | **prone** (both hits) | `REVIEW` (or `DRIFT-*` if a signal/stamp fires) |
| runner-staged | logic in `runner.py` staged each run | cosmetic | `INFO` |

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
6. **Report** — table + punch list + plain next-actions; for every mappable inline task, surface the
   option-(a) doc-deferral recommendation.
7. **Log** (explicit session only) — `_CHANGELOG` (meta, top-insert), `_OBSERVATIONS` for new
   fragility.

## Verdicts
`CLEAN` · `DRIFT-MECH` (lint signal — certain) · `DRIFT-EXACT` (stamp sha ≠ doc sha) · `REVIEW`
(inline, no stamp — semantic read) · `BROKEN-REF` (loader doc missing) · `NO-DOC` (inline, unmapped)
· `INFO` (runner-staged cosmetic).

## The provenance stamp (heuristic → exact)
A one-line comment on an inline prompt:
```
<!-- tracks: WORKFLOWS/research-briefing.md sha:<first-12-of-doc-sha> · stamped YYYY-MM-DD -->
```
lets `task_audit.py` compare the stamped sha to the doc's current sha for an exact verdict instead of
a "go read it" `REVIEW` (mirrors `skill-audit`'s optional `source_sha`). Re-stamp whenever a prompt is
deliberately re-synced. CRE ruled the stamp in (2026-06-29).

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
