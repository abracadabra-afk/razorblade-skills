---
type: workflow
name: backlog-supervisor
trigger: supervise the backlog
aliases: [serve the backlog, run the backlog supervisor, audit the backlog work]
inputs: [_BACKLOG.md § Standing queue (backlog-sweep's ranking — consumed, never recomputed), _BACKLOG.md lane items + project shards, SYSTEM/backlog-queue/_review/ completion logs, _CHANGELOG.md, SYSTEM/reports/, SYSTEM/backlog-queue/_closed/]
outputs: [session plan .md files in SYSTEM/backlog-queue/_served/, audit verdicts moving plans to _closed/ or fix prompts back to _served/, a "## Needs CRE ruling (backlog-supervisor DATE)" bin in _BACKLOG.md for escalations, an unconditional run receipt in SYSTEM/reports/backlog-supervisor-runs.md]
lane: meta
status: draft
created: 2026-09-04
last_updated: 2026-09-04
---

# WORKFLOW: backlog-supervisor

## When to use

CRE says **"supervise the backlog"** / **"serve the backlog"** / **"run the backlog supervisor"**, or the `backlog-supervisor` scheduled task fires. It is the **planning and reviewing half** of the supervised backlog loop; [[WORKFLOWS/backlog-agent]] is the executing half.

Two jobs, in this order every run:

1. **Audit** — any completion log sitting in `SYSTEM/backlog-queue/_review/` gets read against its plan's completion conditions. Pass closes it; fail comes back as a fix prompt naming the specific mistakes.
2. **Serve** — for each eligible backlog item, compose a **session plan**: the instructions to work the item, the references the work needs, and the completion conditions, written so a cold agent with no memory of this session can finish it without asking a question.

Audits run first because a stuck item that never gets reviewed is worse than an item that never gets served, and because the cheap-check-first rule (DIR-008 cl. 2) requires the early-exit to account for **pending queue state**, not just new arrivals (`^obs-166`).

## Why this skill exists — the v1 failure it is built around

`vault-backlog-agent` (2026-06 → deleted 2026-08-03) self-selected items straight out of `_BACKLOG` and executed them. On its third run it reported *"auto-run surface exhausted"* and stopped finding work ([[SYSTEM/reports/2026-06-16-vault-backlog-agent-dispatch-exhausted]]). The diagnosis in that report is the whole design brief for this skill: **backlog items are written for a human and are not directly executable.** An item says *"land the gate clause into the remaining pass docs"* — a person knows what that means; an agent with no plan does not, and correctly refuses.

The translation step from *human-readable item* to *executable session* did not exist. That is this skill. The agent never reads `_BACKLOG` to choose work; it reads a plan this skill wrote.

`backlog-sweep.md` § Step 4c pre-authorized exactly this route: *"If an unattended executor is ever wanted again, that is a CRE decision to author a fresh doc-backed task with its own routing — never a revival of this taxonomy or the retired prompt."* This is that fresh doc. It revives nothing.

## Candidate source — consume the Standing queue, never re-rank

**This skill computes no ranking of its own.** Two rankers over one backlog will disagree and neither will be trusted.

Read `_BACKLOG.md` § **Standing queue (backlog-sweep YYYY-MM-DD)** and take its candidates in the order that block already states:

1. the **Ranked-3 attended serving**, in its order;
2. then the block's **"skipped, not served"** list, in the order it already ranks them (it states its own ordering rule and dates).

That is ~9 candidates without a single independent judgment about priority. If a run needs candidates past the end of that list, it applies **backlog-sweep's own recorded rule** — priority band `#p1`→`#p2`→`#p3`→untagged, oldest first within band by the item's anchor date, `#blocked`/`#waiting` excluded — and says so in the receipt as *extending the sweep's stated ordering*, never as a new ranking.

**Freshness gate.** If § Standing queue is missing, or is older than `backlog-sweep`'s last recorded fire, **stand down and report**. Do not compute a ranking to fill the gap — that is the second-ranker failure this rule exists to prevent.

**The counts are approximate and this skill never repeats them as fact.** The block itself carries a DIR-018 note that its item count has no stable matcher across runs (`^obs-254`, `^backlog-queuetag-derivation` open). Cite the block, never re-derive a lane count, and never publish one.

## Eligibility — ruled per item, per run, reason recorded, and never written back as a tag

**This skill does not read queue tags to decide eligibility.** `^obs-250` deleted `#unattended` / `#unattended-confirm` after a string match reported six agent-lane items when two were real — four matched the tag string inside their *prose*, three of those in sentences recording the tag's own removal. `_BACKLOG.md` § Conventions forbids the revival by name, and the surviving `#desktop` tag is still inflatable the same way. So eligibility is ruled from the **item's content** — its recorded next action and what that action touches — read directly, per item, per run.

Note the corollary: `#gated` is the *default for an untagged item*, which means it records the **absence** of a ruling rather than a ruling. It is not a veto. Where CRE has genuinely ruled an item his — the item says so in words — that reads as ATTENDED below.

Every candidate gets exactly one disposition, with a one-clause reason, recorded in the run receipt and (for served items) in the plan:

| Disposition | Meaning |
|---|---|
| **UNATTENDED** | A cold agent can finish it in one session using only safe ops inside the write surface below. Plan served, agent-pickup allowed. |
| **ATTENDED** | Real work exists and can be planned, but finishing it needs CRE — a ruling, a creative call, his voice, a schedule change, or a desktop-only action. Plan served, marked `mode: attended`, **never** auto-picked-up. |
| **NOT-ELIGIBLE** | No plan this run. Reason recorded. |

**The ruling lives in the run receipt and the plan file only. Nothing is ever written back into `_BACKLOG.md` as a tag, a lane, or a status field.** That is both the `^obs-250` guard and the DIR-010 §5 guard in one.

### The tests, in order

Run these against each candidate; the first one that fires decides.

- **E1 — Is there a recorded next action?** `_BACKLOG` § Conventions requires an item to be *current state + next action + pointers*. No single recorded next action → **NOT-ELIGIBLE** (*"no recorded next action; needs CRE to name one"*). This is the same rule the sweep's serving uses when it skips an item, and it is the commonest skip.
- **E2 — Has it already been addressed?** Run the already-addressed check below. Already done → **NOT-ELIGIBLE** (*"already addressed, evidence: …"*), and add one line to the gate bin proposing the item be closed — proposing, never closing it (that is a `backlog-sweep` judgment call).
- **E3 — Is it blocked or waiting?** Read the item and decide from its text, not a grep. Genuinely blocked on an external clock or an unmet precondition → **NOT-ELIGIBLE** (*"blocked on …"*).
- **E4 — Does finishing it require a fork ruling?** An unruled choice inside the item — which of two designs, whether to keep or cut, where a rule should live → **ATTENDED**, and name `decision-helper` as the route in the plan. Neither skill in this pair ever rules a fork.
- **E5 — Is it fiction execution?** Chapter drafting, prose generation, a register or canon pass, anything that authors CRE's words → **ATTENDED**, plan-and-defer only. AI executes; CRE creates.
- **E6 — Does the next action land outside the agent's write surface?** Desktop-only (pack / Save-skill / install / git write-op / StoryLine UI / "Run now"), a scheduled-task prompt edit, `_DIRECTIVES`, an OS anchor, `DECISIONS/`, `TASKS/TODAY.md`, the week plan → **ATTENDED**.
- **E7 — Otherwise → UNATTENDED.** Compose the plan.

**An E6 sharpening from the pilot.** An item with one in-surface leg and one out-of-surface leg is only splittable when the legs are genuinely **independent**. Where DIR-016 binds them — a canon doc *and* its live task prompt must change in the same session — serving the doc half alone would ship a route updated on one surface of two, which DIR-016 names the most expensive failure shape available, because the record then says it works. Rule the whole item ATTENDED instead. (`^backlog-taskaudit-gatebin` is the worked example: leg (b) is a clean `WORKFLOWS/task-audit.md` edit, and it is still not servable.)

An item can be ATTENDED on one run and UNATTENDED on a later one — a fork ruled, a desktop trip made — which is precisely why the ruling is per run and lives nowhere durable.

### The already-addressed check (E2)

All three surfaces, because a single surface has repeatedly been wrong here:

1. **`_CHANGELOG.md`** — entries since the item's anchor date, **read in full**. Summaries lie; `backlog-sweep` § Step 3b established reading before counting.
2. **`SYSTEM/reports/`** — any dated report naming the item's anchor or its deliverable.
3. **`SYSTEM/backlog-queue/_closed/`** — a prior closed plan for the same anchor, and its verdict.

Then the **wording-vs-state check** (`backlog-sweep` § Step 4b check 3): where the item names a checkable artifact — a file, a doc section, a skill, a task — read the artifact and test the item's own wording against it. An item that says "packaging pending" is a snapshot nothing re-checks.

Two hard constraints on a negative:

- **Read the artifact to EOF before concluding a claimed edit did not land** (`^obs-247`). A partial write looks exactly like a non-write from the middle of a file. Anything less reports *"state unconfirmed — partial read,"* never a confident negative.
- **A `Glob` miss is never evidence of absence** (DIR-005). Confirm every load-bearing negative with a pathed `Grep` or a direct `Read`. Every `Glob`/`Grep` against vault content passes an explicit `path` — unpathed, they search the Cowork outputs scratch and return a clean "No files found" with no warning.

## Composing a session plan — the artifact that makes this work

A plan is written for a **cold agent with no memory of this session and no access to CRE**. The test it must pass: *could a stranger finish this without asking a question?* If not, it is not a plan yet — either research it further or rule the item ATTENDED.

Write it to `SYSTEM/backlog-queue/_served/<YYYY-MM-DD>-<anchor-slug>.md`, frontmatter serialized (DIR-004):

```yaml
---
type: backlog-session-plan
anchor: backlog-approval-gated-openers
item_file: _BACKLOG.md
mode: unattended        # or attended
round: 1                # 1 = initial; 2 and 3 are the two fix rounds
served: 2026-09-04
served_by: backlog-supervisor
eligibility_reason: "next action is a read-and-report sweep landing in SYSTEM/reports/; no fork, no fiction, no desktop step"
---
```

Body, these sections, all of them:

- **## The item** — the anchor, and the item's current state in the supervisor's own words. Not a copy-paste: the plan is the translation.
- **## The job** — what this session must accomplish, stated whole and upfront, in plain instruction. One session's worth. If it does not fit one session, split it and serve only the first part, saying so.
- **## Why** — the reason the work matters, one or two sentences. A cold agent that knows why makes better calls at the edges than one following steps.
- **## References** — every file the work needs, by full path, each with one line on what it carries and why it is here. Anything the agent would otherwise have to go find. Include the directives that bind this particular job, by number. **Name the substrate a reference needs when it is not the file tools** — `C:\Users\Chad\Claude\Scheduled\` is unreachable by `Read` and needs the host route, a fact the pilot plan omitted and the agent had to discover.
- **## Steps** — the ordered work. Name the substrate for any mechanical step (§ Substrate below).
- **## Write surface for this plan** — the exact paths this session may write, and nothing else. Everything not named here defers.
- **## Completion conditions** — objective, checkable statements. *"`SYSTEM/reports/2026-09-04-approval-gated-openers.md` exists and lists every one of the 14 registered task prompts with a flag or a clear."* Not *"the sweep is done."* These are what the audit reads; a vague condition makes the audit a judgment call, which is the one thing this loop cannot afford. **Check the conditions against this plan's own Defer section before serving** — a condition that forbids what the Defer rule authorizes is a self-contradicting plan, and the agent will be right whichever way it goes.
- **## Defer instead of guessing** — the named cases where this job should stop and defer rather than proceed, each with what to write in the completion log.
- **## Out of scope** — the adjacent work this session must not do.

For `mode: attended`, the same shape, addressed to a session with CRE present: the research already done, the specific question or ruling he needs to give, and the options laid out. An attended plan's job is to make his sitting short.

**Serve at most 3 plans per run**, and never let `_served/` + `_working/` + `_review/` exceed **5 open plans** in total. Bounded output is house discipline (`backlog-sweep` caps graduations at 5, `sysadmin` at 12, `day-launch` at 7): an unbounded queue is one nobody works.

## Auditing a completion log

For each `SYSTEM/backlog-queue/_review/<...>.log-rN.md`, read the log **and the artifacts it claims**, then rule:

- **PASS** — every completion condition is met, verified against the artifact itself rather than the log's claim about it (DIR-018: a check that passes on a proxy has not verified the thing). Move the plan and all its logs to `_closed/`. Update the `_BACKLOG` item: check it off if the plan discharged the whole item, otherwise rewrite its **Next:** down to what remains (amend by replacement, § Conventions). Both edits are file-tool, verified by re-read.
- **PARTIAL / FAIL** — write a **fix prompt** to `_served/<date>-<anchor>.md` at `round: N+1`, naming the specific mistakes and missteps: which condition is unmet, what the log claimed versus what the artifact shows, what to do differently. A fix prompt that says "try again" is not a fix prompt. Move the plan and logs back to `_served/` alongside it.
**Reconcile duplicates first.** If the same anchor appears in more than one queue folder, the agent's seat had no delete primitive and copied forward instead of moving (the 2026-09-04 pilot's finding). Resolve to the **furthest-along copy** in `_served/` → `_working/` → `_review/` → `_closed/` order, audit that one, and clear the stale copies with the host route. This is a safe op, not a finding to gate.

**When a completion condition and the plan's own Defer rule conflict, the plan is the defect, not the agent.** The pilot's condition 3 demanded one of three verdicts for every task while its Defer section authorized a fourth (`UNREAD`) for unreadable inputs; the agent followed the Defer rule and said so. That is correct behavior and audits to a pass — record the plan defect so the next plan does not repeat it, and never fail an agent for obeying an instruction the plan gave it.

- **DEFERRED-BY-AGENT** — the log says the agent stopped and deferred with a reason. Not a failure. Either re-plan around the obstacle (a new round 1, if the obstacle is something the plan should have covered) or rule the item ATTENDED and route the reason to the gate bin.

**Cap the loop at two fix rounds.** Round 1 is the initial plan; rounds 2 and 3 are the two fixes. A fail at round 3 **escalates**: move everything to `_closed/` with a terminal `ESCALATED` note, rewrite the `_BACKLOG` item's **Next:** to name both logs by path, and add a line to the gate bin. The item goes back to CRE having been worked, with the record of what was tried attached.

## Escalation and deferral — one channel, the one he already opens

Every deferral, escalation, and NOT-ELIGIBLE-worth-knowing goes to a **`## Needs CRE ruling (backlog-supervisor YYYY-MM-DD)` bin in `_BACKLOG.md`** — the same surface `backlog-sweep`, `log-rotate`, and `task-audit` write, and the surface [[WORKFLOWS/sysadmin]] already aggregates on the attended admin pass. One line each: the item, the proposed action, the one-clause reason.

This is deliberate and it is the whole of DIR-012 clause 4 and clause 5. A deferral CRE cannot see is not a deferral, and a new parallel channel would be a sixth artifact he has to remember to open — which is the dispersal failure `sysadmin` exists to fix. If a prior run's bin has unruled lines, **fold them in rather than stacking a second bin.**

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`) with the file tools. Mismatch → halt, write the receipt, report (`^obs-004`).

### Step 1 — Cheapest work-check first (DIR-008 cl. 2)
Before reading anything expensive, enumerate the four queue folders and get four counts: `_review/`, `_served/`, `_working/`, `_closed/`. Branch:

- **`_review/` non-empty** → there are audits to run. Continue (audits come first, always).
- **`_review/` empty and `_served/` + `_working/` at the 5-plan cap** → nothing to audit, no room to serve. **Stand down**: write the receipt, end the run. No `_BACKLOG` read, no plan composition.
- **Otherwise** → continue to serving.

The early-exit accounts for pending queue state, not just new arrivals — a served-but-unworked plan is work in flight, and treating an empty `_review/` as "nothing to do" would strand the queue (`^obs-166`, the file-inbox bug).

### Step 2 — Audit everything in `_review/`
Per § Auditing above. Move plans, write fix prompts, update `_BACKLOG` items for passes. Do this before serving so a fix prompt is in `_served/` for the same day's agent run.

### Step 3 — Load candidates
Read `_BACKLOG.md` § Standing queue. Apply the freshness gate. Take candidates in the order the block states (§ Candidate source). Read each candidate item in full from `_BACKLOG.md` or its project shard.

### Step 4 — Rule eligibility per candidate
Run E1–E7 in order. Record every disposition and reason. Stop once 3 plans are composed or the working set hits the cap.

### Step 5 — Compose and serve
Write each plan to `_served/`. Re-read each written plan through the file tools and confirm the frontmatter parses and every required section is present (DIR-004, DIR-005).

### Step 6 — Gate bin
Fold forward any unruled lines from a prior `backlog-supervisor` bin, add this run's escalations and deferrals, write the bin to `_BACKLOG.md` with a targeted file-tool edit, re-read to confirm.

### Step 7 — Receipt, unconditionally
Append one line (newest-first) to `SYSTEM/reports/backlog-supervisor-runs.md` **every fire, including a stand-down and including a halt**: date, mode, counts audited / passed / failed / escalated / served, dispositions ruled, and any substrate fallback taken. Create the file if absent.

This is not optional and not conditional. `^backlog-scheduler-liveness-check` is open precisely because every task writes a receipt when it runs and nothing writes anything when it doesn't, so six days of scheduler silence (2026-08-26 → 09-01) produced no signal at all. A stand-down line is the most valuable line this file carries.

### Step 8 — Log (DIR-003)
A run that changed the vault gets a `_CHANGELOG.md` top-insert (meta lane). New fragility → `_OBSERVATIONS.md` with a `^obs-NNN` anchor, re-scanning for the highest anchor immediately before the write and re-reading the heading after (`^obs-236`). Follow-ups → `_BACKLOG.md`. A stand-down run is trivial: receipt only, no changelog entry.

## Substrate (DIR-020)

The only mechanical step is enumerating the queue folders and reading files. **This workflow never requires `bash`.**

1. **Preferred — the host route**: `mcp__Desktop_Commander__list_directory` / `move_file` (or `windows-cli`) against the real Dropbox folder. Better, not degraded: it reads the actual folder, so the mount-staleness caveat DIR-005 exists for does not apply, and it is the only route with a true atomic move. It is also the **only** route that can read a scheduled-task prompt — `C:\Users\Chad\Claude\Scheduled\` sits outside the file tools' connected folders. `mcp__workspace__bash` is currently denied on scheduled seats (`^obs-281`, `^obs-284`) and has already halted `skills-sweep` outright.
2. **Fallback — the file tools**: `Glob` with an explicit `path`, and **every empty result confirmed by a direct `Read` of that folder's `README.md`** before it is treated as an empty folder. A `Glob` miss is not evidence of absence.

A denial on route 1 is an expected branch, not an error: fall through, and name the fallback in the receipt. Never reach for `bash` at any tier.

## Stop conditions

- **Vault sentinel fails** → halt, receipt, report. Never edit.
- **§ Standing queue missing or stale** → stand down, receipt, report. Never compute a ranking to fill the gap.
- **The file tools cannot write `_BACKLOG.md`** → halt, receipt, report. Never fall back to `patch_vault_file` or a whole-file MCP rewrite; both have silently truncated canon here (DIR-005).
- **Working set at cap with an empty `_review/`** → stand down (this is normal, not a fault).
- **`bash` is the only route left for a mechanical step** → this workflow is bash-blocked by declaration: report the step as unrun rather than attempting it.
- **No candidate is eligible** → that is a valid, informative run. Receipt it with the dispositions, and if several runs in a row rule everything ATTENDED, say so plainly in the gate bin: it means the backlog's remaining debt is genuinely CRE's, which is a finding, not a failure. (v1 hit this state and called it "surface exhausted"; the difference is that this run can say *why*, item by item.)

## Logging

Receipt every fire (Step 7). `_CHANGELOG` / `_OBSERVATIONS` / `_BACKLOG` per DIR-003 on any run that changed the vault. All OS-doc edits via targeted file-tool edits, each verified by re-reading through the file tools (DIR-005) — never `patch_vault_file`, never a bash read to verify.

## What this is NOT

- **Not `backlog-sweep`.** The sweep owns maintenance, archival, dedupe, observation graduation, and the Standing queue computation. This skill never archives, never dedupes, never graduates an observation, and never computes the ranking — it consumes it.
- **Not a re-ranker.** It has no ordering of its own and refuses to invent one.
- **Not `sysadmin`.** That pass is the attended consumer of sweeper deferrals and the place rulings get made. This skill *feeds* it; it never rules a deferral.
- **Not `decision-helper`.** A fork inside an item routes there or to CRE. Neither skill in this pair rules one.
- **Not `day-launch` or `week-shape`.** It never writes `TASKS/TODAY.md` or the week plan.
- **Not `task-control`.** It never pauses, resumes, creates, or edits a scheduled task.
- **Not a fiction executor.** No chapter drafting, no prose generation, no register or canon pass. Fiction items are plan-and-defer only.
- **Not a scheduler liveness monitor.** It writes the receipts that make liveness checkable, but it cannot detect its own absence and must never be relied on for that — the monitor for `^backlog-scheduler-liveness-check` has to be something that does not depend on the process it watches, which this does.

## Packaging

Source at `WORKFLOWS/skills-src/backlog-supervisor/`. Per DIR-009: author via the file tools → pack on the **desktop** with `WORKFLOWS/git-bridge/pack-skills.ps1` → sha-verify packaged bytes against source → Save-skill. Never sandbox packaging (`^obs-156`). The description is single-quoted: it contains `#` and `: `, and an unquoted `#` opens a YAML comment that the installer silently truncates at (`^obs-299`).
