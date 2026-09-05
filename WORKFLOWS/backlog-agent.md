---
type: workflow
name: backlog-agent
trigger: work the backlog
aliases: [work the backlog with me, run the backlog agent, pick up a backlog plan]
inputs: [SYSTEM/backlog-queue/_served/ session plans (composed by backlog-supervisor), the reference files each plan names]
outputs: [the artifacts a plan's completion conditions name, a completion log .md beside the plan in SYSTEM/backlog-queue/_review/, an unconditional run receipt in SYSTEM/reports/backlog-agent-runs.md]
lane: meta
status: draft
version: 2
created: 2026-09-04
last_updated: 2026-09-04
---

# WORKFLOW: backlog-agent

## When to use

Two modes, two triggers, and they are deliberately different phrases rather than one phrase with a modifier — attended sessions are CRE-called and a modifier is easy to fire by accident.

- **Unattended** — **"work the backlog"**, or the `backlog-agent` scheduled task. Polls `SYSTEM/backlog-queue/_served/` for a plan marked `mode: unattended`, executes it, and writes a completion log detailed enough for [[WORKFLOWS/backlog-supervisor]] to audit without re-doing the work.
- **Attended** — **"work the backlog with me"**, CRE present. Reads **`SYSTEM/backlog-queue/_attended/`** (a separate folder as of 2026-09-04, outside the unattended pipeline and its cap), shows him the prepared sittings with their ages, and works the one he picks — moving it straight to `_working/`. **Never self-started.** The scheduled task never runs this mode, an unattended run never reads that folder, and CRE can always name a plan outright: *"work the backlog with me on `^anchor`."*

This is the **executing half** of the supervised backlog loop. The planning and reviewing half is [[WORKFLOWS/backlog-supervisor]].

## The one rule that matters most

**This skill never chooses its own work.** It does not read `_BACKLOG.md` to find something to do, does not rank, and does not decide an item is worth doing. It executes a plan the supervisor wrote.

That is not a limitation, it is the fix. `vault-backlog-agent` (v1, deleted 2026-08-03) self-selected from `_BACKLOG` and reported *"auto-run surface exhausted"* on its third run ([[SYSTEM/reports/2026-06-16-vault-backlog-agent-dispatch-exhausted]]), because backlog items are written for a human and are not directly executable. An agent handed a plan finishes; an agent handed a backlog is right to refuse.

If `_served/` is empty, the correct behavior is to stand down, not to go looking.

## Write surface — the hard floor a plan cannot widen

Every plan names a **Write surface for this plan**. This skill writes what that section names **and nothing else**. Everything else defers back to the supervisor with a reason (DIR-012 cl. 1: safe ops write, judgment defers, and in doubt a report beats a mutation).

Two layers, and the outer one is not negotiable.

**Always allowed, in every mode:**

- `SYSTEM/backlog-queue/**` — its own completion logs and the plan's folder position.
- `SYSTEM/reports/**` — its run receipt, and any report a plan asks for.

**Allowed only when the plan's write surface names the exact path:**

- `WORKFLOWS/*.md` canon docs and `WORKFLOWS/skills-src/**` sources — **including authoring a new doc or source unattended when the plan names the exact path and specifies the content** (v2, 2026-09-04). The pack/install that follows is never attempted here (DIR-007/009); the plan's completion log names it as the desktop trip owed, and the supervisor queues it on the weekly sheet. Until packed the doc runs from the trigger index, which is the degraded mode already in place.
- `SYSTEM/**` outside the two folders above.
- `_BACKLOG.md` — **only** the single item the plan names, and only the edit the plan's completion conditions describe. Its own DIR-003 log lines are separate and always allowed. **Reach that item by the shared slice-read protocol** — `WORKFLOWS/backlog-supervisor.md` § Candidate source: measure with a metadata call, `Grep -n` with an explicit path to find the line, `Read` by offset for the slice, edit anchored on that slice, re-read the same slice — **never by pulling the file** (added 2026-09-04): `_BACKLOG.md` measured **288.6 KB**, past the ~256 KB point where the file tools return a prefix without saying so, and a targeted read is both correct and cheaper. If the item cannot be located that way, defer the plan rather than editing against a partial — an edit anchored on text you only half-read is a destructive write waiting to happen. Same rule for `_CHANGELOG.md` (252.6 KB) and `_OBSERVATIONS.md` (235.8 KB); full policy at `WORKFLOWS/log-rotate.md` § The hard line above the bands.

**The auto-ratify class, from the agent's side (v2, 2026-09-04).** DIR-012 clause 6 (proposed at `SYSTEM/reports/2026-09-04-dir012-auto-ratify-proposal.md`; armed on CRE's word) makes a **reversible** write — stamp · move · archive verbatim · rewrite-down · fold, never delete — on `SYSTEM/**`, `_BACKLOG.md` + shards, `_OBSERVATIONS.md` (stamps + own DIR-003 lines), `WORKFLOWS/*.md`, `WORKFLOWS/skills-src/**` his standing yes. **What that changes here:** a plan may name such a path without carrying a per-item CRE ruling, and the agent executes it. **What it does not change:** the plan still has to name the path — the class widens what a plan *may* name, never what the agent does on its own — and the never-written list below is untouched by it, armed or not. The agent does not check whether the class is armed; the supervisor does, before serving.

**Never written unattended, whatever a plan says.** A plan that asks for one of these is itself the defect: stop, defer, and say so in the completion log.

- `_DIRECTIVES.md` and `SYSTEM/directives-reference.md` — canon; graduation is CRE's ruling alone.
- `_ME.md`, `_VAULT MAP.md`, `_SKILLS MAP.md`, `CLAUDE.md` — the OS anchors and the boot doc.
- `_CHANGELOG.md` / `_OBSERVATIONS.md` beyond this session's own DIR-003 entries — the brain logs' *curation* is desktop-owned under the dual-writer split.
- `WRITING/**` — every chapter `draft.md`, `brief.md`, `revisions/`, `REFERENCE/` canon, register, and DEV tree. The desktop owns active drafting. No prose, no register pass, no canon pass, ever.
- `DECISIONS/` — `decision-helper` owns the ledger.
- `TASKS/TODAY.md` (day-launch owns it) and `TASKS/TASKS.md` § This week (week-shape owns it).
- Scheduled-task `SKILL.md` prompts — that surface has no version control and no backup, so the failure is total (DIR-005); `task-control` and attended sittings own it.
- Anything requiring a fork to be ruled, a priority to be set, or an item to be dropped as stale.

Attended mode relaxes only what CRE relaxes in the moment, out loud. It does not inherit a wider surface by default.

## Executing a plan

### Claim by moving, not by marking

On pickup, **move the plan file from `_served/` to `_working/`**. That move *is* the claim — there is no `status:` field to set, because a status line is written once by the session that created the thing and is exactly the surface nobody updates when that thing finishes (DIR-010 §5). Folder position is the state, and it cannot go stale because moving is the same act as changing state.

`SYSTEM/backlog-queue/_served/` → `_working/` → `_review/` → `_closed/`. This skill performs the first two moves; the supervisor performs the last.

### One plan per unattended run

Take the oldest `mode: unattended` plan, by the date in its filename, preferring a higher `round` (a fix prompt is a plan someone is already waiting on). One plan, then stop. A run that finishes early does not go looking for a second — the working-set cap is the supervisor's to manage.

### Work it

Follow the plan's Steps. Read every file in its References before starting; a plan that named a file expects it to be read. Where a plan names a directive by number, that directive binds this session.

Defer rather than guess. The plan's **Defer instead of guessing** section names the expected cases; the general rule covers the rest. Defer when:

- a completion condition turns out to need a decision the plan did not make;
- a reference file is missing, or its content contradicts what the plan assumed;
- finishing would require writing outside the plan's write surface;
- the work turns out to be larger than one session;
- a secret is found on any surface read (DIR-006: flag on sight, never propagate, never file it).

A deferral is a **successful outcome**, not a failure, and the completion log says so. The one genuinely bad outcome is a guess written into the vault.

### Verify before claiming

Every write is a targeted file-tool edit, **re-read through the file tools afterward** to confirm it landed (DIR-005). Never `patch_vault_file`, never a whole-file MCP rewrite, never a bash read to verify a write. Read a file to EOF before concluding an edit did not land — a partial write looks exactly like a non-write from the middle of a file (`^obs-247`). A `Glob` miss is never evidence of absence; confirm a load-bearing negative with a pathed `Grep` or a direct `Read`.

Derived frontmatter is serialized via `yaml.safe_dump` and parse-gated, never hand-formatted (DIR-004).

## The completion log

Write `SYSTEM/backlog-queue/_working/<plan-name>.log-r<N>.md` (matching the plan's `round`), then move the plan and the log together into `_review/`.

The log is written **for the audit**, and the audit verifies against artifacts rather than claims — so a log that says "done" without paths is a log that will fail. Sections:

```yaml
---
type: backlog-completion-log
anchor: backlog-approval-gated-openers
plan: 2026-09-04-backlog-approval-gated-openers.md
round: 1
mode: unattended
outcome: complete        # complete | partial | deferred
worked: 2026-09-04
worked_by: backlog-agent
---
```

- **## What I did** — the actual work, in order, plainly.
- **## Completion conditions** — each condition from the plan, quoted, with **met / not met** and the **artifact path plus the specific evidence** that shows it. This is the section the audit reads first.
- **## Observable — first probe** *(v2, 2026-09-04)* — the plan's `## Observable` quoted, then **one probe of it against live state at the end of the run**: the exact reading (a `Grep` count, a line quoted from the artifact, a frontmatter value), the substrate used, the timestamp. This is reading one of three: the morning audit reads it again, and the evening close-out reads it a third time before the `_BACKLOG` item is closed (`backlog-supervisor.md` § Observables). A plan with no `## Observable` is a pre-v2 plan — say so and probe the completion conditions instead. **Never write the probe from the plan's expectation; write what the artifact actually returned.**
- **## Files written** — every path touched, with what changed and confirmation it was re-read.
- **## What I deferred and why** — anything not done, each with the reason and what a next session would need. Empty is a valid answer; vague is not.
- **## Surprises** — anything the plan assumed that turned out otherwise. This is how a bad plan gets fixed rather than repeated.

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`) with the file tools. Mismatch → halt, receipt, report (`^obs-004`). If a plan's job touches `WRITING/` in any read capacity, load `_CREATIVE DIRECTIVES.md` before the work (DIR-002) — and note that touching `WRITING/` to *write* is outside the surface regardless.

### Step 1 — Cheapest work-check first (DIR-008 cl. 2)
Enumerate `_served/` and `_working/`. Branch:

- **A plan already in `_working/`** → a prior run claimed it and did not finish. Do not start a new one: read it, finish or defer it, and note the interrupted claim in the log. Stranded work in flight is the queue state an early-exit must account for (`^obs-166`).
- **`_served/` has no `mode: unattended` plan** → **stand down**: write the receipt, end the run. Nothing else — no `_BACKLOG` read, no bootstrap beyond the sentinel. This is the normal case and it must stay cheap.
- **Otherwise** → claim the oldest eligible plan and continue.

**`_attended/` is never read on an unattended run** — not even to count it. The cheapest-work-check stays an enumeration of `_served/` and `_working/`, and adding a third folder to it would make the common stand-down more expensive for a lane this run cannot touch.

Attended mode skips this branch entirely: it reads **`SYSTEM/backlog-queue/_attended/`**, shows CRE the prepared sittings with their ages, and works the one he picks — or the one he names outright.

### Step 2 — Claim
Move the plan into `_working/` — from `_served/` on an unattended run, **straight from `_attended/`** when CRE picks one in a sitting. Confirm the move by reading the plan at its new path. From `_working/` both lanes follow the same path onward, and the supervisor audits them identically.

### Step 3 — Read in
The plan in full, then every file in its References. Do not begin writing until both are done.

### Step 4 — Execute
Follow the plan's Steps inside the plan's write surface, verifying each write by re-read. Where the plan has the agent author a canon doc or a skill source, use the house workflow-doc shape (frontmatter, When to use, Steps, Stop conditions, Logging, What this is NOT) and `yaml.safe_dump`-serialized frontmatter (DIR-004); a description over 1,024 characters or containing an angle bracket is a defect the pack gate will reject, so check it before handing back.

### Step 5 — Probe, log, hand back
Probe the plan's observable once (§ The completion log); write the completion log; move plan and log to `_review/`; confirm both landed at the new path.

### Step 6 — Receipt, unconditionally
Append one line (newest-first) to `SYSTEM/reports/backlog-agent-runs.md` **every fire, including a stand-down and including a halt**: date, mode, plan worked (or "no eligible plan — stood down"), outcome, files written, any substrate fallback taken. Create the file if absent.

Not optional. `^backlog-scheduler-liveness-check` is open because every task writes a receipt when it runs and nothing writes anything when it does not, so the 2026-08-26 → 09-01 outage produced no signal at all. The stand-down line is the one that makes silence detectable.

### Step 7 — Log (DIR-003)
A run that changed the vault gets a `_CHANGELOG.md` top-insert (meta lane), naming the plan and the anchor. New fragility → `_OBSERVATIONS.md` with a `^obs-NNN` anchor, re-scanning for the highest anchor immediately before the write and re-reading the heading after (`^obs-236`). A stand-down run is trivial: receipt only.

## Substrate (DIR-020)

The mechanical steps are folder enumeration and file moves. **This workflow never requires `bash`.**

1. **Preferred — the host route**: `mcp__Desktop_Commander__list_directory` / `move_file` (or `windows-cli`) against the real Dropbox folder. Better, not degraded — it reads the actual folder rather than a mount that can serve stale partials. `mcp__workspace__bash` is currently denied on scheduled seats (`^obs-281`, `^obs-284`) and has already halted `skills-sweep`.
2. **Fallback — the file tools**: `Glob` with an explicit `path`, every empty result confirmed by a direct `Read` of the folder's `README.md`; a move performed as `Write` to the destination then delete of the source, with **both** ends confirmed by re-read before the source is removed.

**A move needs a delete, and some seats do not have one** (found in the 2026-09-04 pilot: the agent had Read/Write/Edit/Glob/Grep and no delete primitive, so every hop copied forward and one plan sat in three folders at once — folder position stopped being a state). With no delete available: copy forward, leave the source, drop a `.superseded` marker beside it naming the destination, and say so plainly in the completion log. **The furthest-along folder wins**, and the supervisor clears the stale copies on its next audit. Never improvise a delete out of an unrelated connector — a Dropbox-app delete, a Drive trash, or an Obsidian vault delete is a different substrate with a different blast radius.

**Reading a scheduled-task prompt requires the host route.** `C:\Users\Chad\Claude\Scheduled\` sits outside the file tools' connected folders: a `Read` there returns a connected-folders error whose only offered remedy is `request_cowork_directory` — approval-gated, and therefore fatal on an unattended run. Read prompts through Desktop Commander / `windows-cli` instead. This is the plainest case in the vault of DIR-020's point that the host route is *better*, not degraded.

A denial on route 1 is an expected branch, not an error: fall through and name the fallback in the receipt. Never reach for `bash` at any tier. A plan whose own Steps require `bash` is deferred, not attempted — say so in the log so the supervisor can re-plan it for an attended desktop sitting.

## Stop conditions

- **Vault sentinel fails** → halt, receipt, report. Never edit.
- **No eligible plan** → stand down, receipt. This is the normal empty-queue case, not a fault.
- **A plan asks for a write in the never-written list** → do not perform it. Defer the whole plan with that named as the reason; the plan is the defect.
- **A plan's completion conditions are not objectively checkable** → execute what is clear, defer the rest, and say in the log that the conditions were unverifiable. Never self-certify a vague condition as met.
- **A fork appears inside the work** → stop, defer, name it. Neither skill in this pair rules a fork.
- **The file tools cannot write** → halt, receipt, report. Never fall back to `patch_vault_file` or a whole-file MCP rewrite (DIR-005).
- **A secret is found** → flag, never propagate, never file it; queue rotation + relocation in the completion log and stop touching that surface (DIR-001, DIR-006).
- **`bash` is the only route left for a step** → bash-blocked by declaration: defer the step rather than attempting it.

## What this is NOT

- **Not a work-chooser.** It never reads `_BACKLOG` to select an item, never ranks, and never decides something is worth doing. That is `backlog-supervisor`, and the separation is the entire fix for v1.
- **Not `backlog-sweep`.** It never archives, dedupes, reformats, graduates an observation, or computes the Standing queue.
- **Not `sysadmin`.** It never rules a deferral.
- **Not `decision-helper`.** It never rules a fork.
- **Not `day-launch` or `week-shape`.** It never writes `TASKS/TODAY.md` or the week plan.
- **Not `task-control`.** It never pauses, resumes, or edits a scheduled task.
- **Not a fiction executor.** No chapter drafting, no prose generation, no register or canon pass, no writing anywhere under `WRITING/`. AI executes; CRE creates.
- **Not a scheduler liveness monitor.** Its receipts are evidence for one, but it cannot detect its own absence and must never be the thing that watches for it.

## Packaging

Source at `WORKFLOWS/skills-src/backlog-agent/`. Per DIR-009: author via the file tools → pack on the **desktop** with `WORKFLOWS/git-bridge/pack-skills.ps1` → sha-verify packaged bytes against source → Save-skill. Never sandbox packaging (`^obs-156`). The description is single-quoted: it contains `: `, and an unquoted `#` or `: ` breaks the YAML parse that the installer silently truncates on (`^obs-299`).
