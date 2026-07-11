---
name: task-audit
description: Reconcile each scheduled task's live SKILL.md prompt against its WORKFLOWS/[name].md canon doc and report drift — the sibling of skill-audit for the scheduled-task spine. Use whenever CRE asks to "audit the task prompts," "check task-prompt drift," "are my scheduled tasks in sync with their docs," "run the task doctor," or "which task prompts are stale." It classifies each task prompt's SHAPE (doc-deferring / inline-behavior / runner-staged per ^obs-124), runs a deterministic convention lint that catches mechanical drift (stale book names, _CHANGELOG foot-append, wrong scheduler path), and compares an optional tracks: provenance stamp to the doc's current sha for exact drift. READ-ONLY — it never edits a task prompt; fixes stay CRE-attended via update_scheduled_task (body-only, ^obs-138). Do NOT use it to reconcile the Cowork-skill chain doc->.skill->installed (that is skill-audit), to author or fix a prompt's content (skill-creator / a manual edit), or to package/install a skill.
---

# Task Audit (the scheduled-task prompt doctor)

You run a **read-only** reconciliation of every scheduled task's live `SKILL.md` prompt against
its `WORKFLOWS/<name>.md` canon doc, reporting drift so CRE knows which prompts to re-sync. You
write nothing except the report (and, if asked, the brain-log entries).

**Why this skill exists.** `skill-audit` reconciles the *Cowork-skill* chain
(`WORKFLOWS/<name>.md` → `<name>.skill` build → installed copy). A **scheduled task** runs a
different surface: a prompt stored at `C:\Users\Chad\Claude\Scheduled\<task>\SKILL.md`, a
hand-maintained file that can silently lag its `WORKFLOWS/<name>.md` doc. Nothing else reconciles
those two — a task ran stale for weeks (`^obs-113`), and the 2026-06-24 audit found two live hits
(`books-daily-ingest-weave` stale book paths, `research-runner` `_CHANGELOG` foot-append). This
skill is the catch.

**The three prompt shapes (`^obs-124`) — what predicts drift:**

- **doc-deferring** — "Read `WORKFLOWS/<name>.md` and follow it"; logic read at runtime. **Drift-resistant.**
- **inline-behavior** — procedure baked into the `SKILL.md` body. **Drift-prone** (both real hits).
- **runner-staged** — logic in a `runner.py` staged each run; prompt drift **cosmetic**.

## Step 0 — Vault sentinel (`^obs-004`)

From the mounted vault root, read `_DIRECTIVES.md` and confirm its frontmatter is
`type: ai-os-brain` + `file: directives`. Missing/mismatched → halt and ask which folder is the
vault. Write nothing.

## Step 1 — Gather the live task prompts (the scheduler dir is host-side)

The scheduler dir is on the Windows host and **not reachable from sandbox bash**. So:

1. Call `list_scheduled_tasks` (the authoritative registry) to get every task's `taskId`, its
   `path` (`C:\Users\Chad\Claude\Scheduled\<task>\SKILL.md`), and `enabled` state.
2. **Read each `path` via the file tools** (cloud-authoritative) and **write a copy to the session
   outputs scratch** as `prompts/<taskId>.md`. This is the `^obs-103` "stage off the host, read a
   clean copy" discipline — the script reads the scratch, never the host path.

## Step 2 — Stage the script off the mount, then run it (`^obs-103` / `^obs-084`)

NEVER run `task_audit.py` directly off the vault mount: the Dropbox mount can serve a truncated or
NUL-padded copy that crashes python (`source code string cannot contain null bytes`) — a corrupt
*script* is wrong behavior, not just wrong data. Instead:

1. Read `WORKFLOWS/skills-src/task-audit/task_audit.py` **via the file tools** and write it to the
   outputs scratch (or `bash cp` it to `/tmp`); `py_compile` it — if it won't compile, re-read via
   the file tools and re-stage. Do the same for `task_doc_map.json`.
2. Run:

   ```
   python3 task_audit.py --prompts-dir <scratch>/prompts \
       --workflows <VAULT>/WORKFLOWS --map <scratch>/task_doc_map.json
   ```

The script classifies each prompt's shape, runs the **convention lint** (stale book names, wrong
scheduler path, `_CHANGELOG` foot-append, missing NUL-guard — extend the `LINT` list as new retired
conventions appear), and, when a prompt carries a `<!-- tracks: WORKFLOWS/<doc> sha:… -->` stamp,
compares it to the doc's current sha for an **exact** verdict. Run `--selftest` first if you've
touched the script.

**Verdicts:** `CLEAN` · `DRIFT-MECH` (a lint signal fired — mechanical, certain) · `DRIFT-EXACT`
(stamp sha ≠ doc sha) · `REVIEW` (inline, no stamp — needs a semantic read) · `BROKEN-REF` (loader
points at a missing doc) · `NO-DOC` (inline, no mapped doc) · `INFO` (runner-staged, cosmetic).

## Step 3 — Coherence guard (`^obs-014` / `^obs-084`)

If a staged copy looks truncated or NUL-padded, that's the stale mount, not the file — re-read the
host `SKILL.md` (or the script) through the **file tools** (cloud-authoritative) and trust that
over a bash read before reporting. Shell reads are for discovery, not for justifying a conclusion.

## Step 4 — Semantic pass on the REVIEW rows (the Stage-B judgment)

The script's shape label is best-effort — the `doc-deferring`/`inline` boundary is genuinely fuzzy
for hybrid prompts (e.g. `research-runner` carries a loader *and* inline steps). For each `REVIEW`
(and any `DRIFT-EXACT`), load the task prompt **and** its mapped doc(s) and judge whether the inline
behavior still faithfully matches the doc's current procedure — the call a script can't make.
Report HIT (with the specific divergence) or CLEAN. This is the only non-deterministic step; keep it
honest and specific.

## Step 5 — Report

Present the script's table + punch list, then translate into plain next-actions:

- `DRIFT-MECH <task>` → "the prompt carries a retired convention (`<signal>`) — re-sync it to the
  current house pattern."
- `DRIFT-EXACT <task>` → "`WORKFLOWS/<doc>` changed since this prompt was last synced — re-read the
  doc and update the prompt, then re-stamp."
- `REVIEW <task>` → the Step-4 finding.
- For every `inline-behavior` task that maps to a doc, surface the **option-(a)** recommendation:
  collapse the prompt to the doc-deferring loader (the shape that keeps `skills-sweep` /
  `backlog-sweep` / `vault-health` permanently clean). Pilot = `research-runner` (its Step 2 already
  reads its doc).

Never claim to have fixed anything — this skill only diagnoses.

## Step 6 — Applying a fix (only when CRE asks; always CRE-attended)

Task-prompt edits are behavior-changing and go through the `scheduled-tasks`
`update_scheduled_task` API (the file is outside connected folders, so a direct Edit fails). **Per
`^obs-138`, pass the prompt BODY ONLY — no `---` frontmatter block — or the scheduler doubles the
frontmatter.** Set `description` via its own field. Verify by re-reading the host `SKILL.md`. When
you sync a prompt to its doc, refresh (or add) its `<!-- tracks: WORKFLOWS/<doc> sha:<first-12> -->`
stamp so the next audit is exact, not heuristic.

## Step 7 — Log (only on an explicit audit session)

If CRE ran this as a real session, append a one-line entry to `_CHANGELOG.md` (meta lane, top-insert
via the file tools, `^obs-084` guard) noting which tasks were flagged, and file any new fragility to
`_OBSERVATIONS.md`. Otherwise stay read-only.

## Notes

- **`task_doc_map.json`** is the committed task→doc map (not every task is 1:1; some compose two
  docs; `vault-backlog-agent` has none). Keep it current when tasks are added/renamed — a new task
  with no map entry shows up as `NO-DOC`, which is the prompt to map it.
- **The lint is the deterministic value; the shape label and REVIEW are advisory.** The two real
  2026-06-24 hits were both mechanically detectable (the `--selftest` proves it).
- Sibling of `skill-audit` (Cowork-skill chain) and `link-audit` (references); same read-only,
  report-only, file-tools-only posture. This one never crosses the install trust boundary because
  it never touches a skill build — its write surface is the scheduler, and that stays CRE-attended.
