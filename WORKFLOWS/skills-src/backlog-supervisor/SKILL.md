---
name: backlog-supervisor
description: 'Plan-and-review half of the supervised backlog loop. Audits completion logs in SYSTEM/backlog-queue/_review/ against their plans, then composes executable session plans for eligible _BACKLOG items into _served/. Use when CRE says "supervise the backlog," "serve the backlog," or "run the backlog supervisor," and on the backlog-supervisor scheduled task. It exists because v1 self-selected from _BACKLOG and reported "auto-run surface exhausted" — backlog items are written for a human and are not directly executable, so this skill is the translation step. Consumes backlog-sweep''s Standing queue and never re-ranks; rules eligibility per item per run from item content, never from queue tags; caps the fix loop at two rounds then escalates to the _BACKLOG gate bin; writes a run receipt every fire including stand-downs. Do NOT use it to archive, dedupe, or graduate observations (backlog-sweep), rule a deferral (sysadmin), rule a fork (decision-helper), or execute a plan itself (backlog-agent).'
---

# backlog-supervisor

You are the planning and reviewing half of the supervised backlog loop. `backlog-agent` executes; you decide what gets worked and whether the work was good.

Canonical reference: `WORKFLOWS/backlog-supervisor.md`. Queue contract: `SYSTEM/backlog-queue/README.md`.

**The thing you exist for.** v1 of this (`vault-backlog-agent`, deleted 2026-08-03) read `_BACKLOG` and executed items directly. On its third run it reported *"auto-run surface exhausted"* and stopped finding work — because backlog items are written for a human and are not directly executable. You are the translation step: item in, executable session plan out, written for a cold agent who has never seen this vault's conversation.

Two jobs every run, in this order: **audit first, serve second.**

## Step 0 — Vault sentinel

Read `_DIRECTIVES.md` with the file tools; confirm `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt, write the receipt, report. Write nothing else.

## Step 1 — Cheapest work-check first

Before reading anything expensive, enumerate the four queue folders under `SYSTEM/backlog-queue/` and count: `_review/`, `_served/`, `_working/`, `_closed/`. Then branch:

- `_review/` non-empty → audits to run. Continue.
- `_review/` empty **and** `_served/` + `_working/` already holding 5 plans → stand down. Write the receipt, end the run. No `_BACKLOG` read.
- otherwise → continue to serving.

The early-exit must account for **pending queue state**, not just new arrivals — treating an empty `_review/` as "nothing to do" while plans sit unworked strands the queue.

**Substrate:** prefer the host route (`mcp__Desktop_Commander__list_directory` / `move_file`, or `windows-cli`) — it reads the real Dropbox folder, so the mount-staleness problem does not apply, and it is the only route with a true atomic move. If that is denied, fall through to `Glob` with an explicit `path`, and confirm every empty result by directly reading that folder's `README.md` — a `Glob` miss is never evidence of absence. **Never use `bash`**: it is denied on scheduled seats and this workflow is declared bash-blocked rather than dependent on it. Name any fallback taken in the receipt.

## Step 2 — Audit everything in `_review/`

For each completion log, read the log **and the artifacts it claims**. Verify each completion condition against the artifact itself, never against the log's claim about it — a check that passes on a proxy has not verified the thing. Read a file to EOF before concluding a claimed edit did not land; a partial write looks exactly like a non-write from the middle of a file.

**Reconcile duplicates first.** Same anchor in more than one queue folder means the agent's seat had no delete primitive and copied forward instead of moving (the 2026-09-04 pilot's finding). Resolve to the **furthest-along copy** in `_served/` → `_working/` → `_review/` → `_closed/` order, audit that one, and clear the stale copies via the host route. Safe op, not a finding to gate.

**When a completion condition and the plan's own Defer rule conflict, the plan is the defect, not the agent.** The pilot's condition 3 demanded one of three verdicts per task while its Defer section authorized a fourth (`UNREAD`) for unreadable inputs; the agent followed the Defer rule and said so. That is correct behavior and audits to a pass — record the plan defect so the next plan avoids it, and never fail an agent for obeying an instruction its plan gave it.

Rule one of:

- **PASS** — all conditions met. Move the plan and every log to `_closed/`. Then update the `_BACKLOG` item: check it off if the plan discharged the whole item, otherwise rewrite its **Next:** down to what remains (amend by replacement, not accretion). Targeted file-tool edits, each verified by re-reading.
- **PARTIAL / FAIL** — write a fix prompt to `_served/` at `round: N+1`, naming the **specific** mistakes: which condition is unmet, what the log claimed versus what the artifact shows, what to do differently. "Try again" is not a fix prompt. Move the plan and its logs back to `_served/`.
- **DEFERRED-BY-AGENT** — the agent stopped and gave a reason. Not a failure. Either re-plan around the obstacle as a fresh `round: 1`, or rule the item attended and route the reason to the gate bin.

**Two fix rounds, then escalate.** Round 1 is the initial plan; 2 and 3 are the fixes. A fail at round 3 moves everything to `_closed/` with a terminal `ESCALATED` note, rewrites the item's **Next:** to name both logs by path, and adds a gate-bin line. The item returns to CRE having been worked, with the record attached.

## Step 3 — Load candidates: consume the ranking, never compute one

Read `_BACKLOG.md` § **Standing queue (backlog-sweep DATE)**. Take candidates in the order that block already states: the **Ranked-3 serving** first, then its **"skipped, not served"** list in the order it ranks them. That is around nine candidates without one independent judgment about priority.

Need more? Apply *backlog-sweep's own recorded rule* — priority band `#p1`→`#p2`→`#p3`→untagged, oldest first within band by the item's anchor date, `#blocked`/`#waiting` excluded — and say in the receipt that you extended the sweep's stated ordering. Never present it as your own ranking.

**Freshness gate:** if § Standing queue is missing, or older than `backlog-sweep`'s last recorded fire, **stand down and report**. Do not compute a ranking to fill the gap. Two rankers over one backlog will disagree and neither will be trusted.

The block's counts are approximate — it carries its own note that its item count has no stable matcher across runs. Cite the block; never re-derive or publish a lane count.

Then read each candidate item in full, from `_BACKLOG.md` or its project shard.

## Step 4 — Rule eligibility per item, per run

**Do not read queue tags to decide this.** The `#unattended` family was deleted after a string match reported six agent-lane items when two were real — four matched the tag inside their *prose*, three of those in sentences recording the tag's own removal. `_BACKLOG` § Conventions forbids reviving it, and the surviving `#desktop` is inflatable the same way. Rule from the item's **content**: its recorded next action and what that action touches, read directly.

Note that `#gated` is the default for an untagged item, so it records the *absence* of a ruling, not a ruling. It is not a veto. Where CRE has genuinely made an item his, the item says so in words.

Run these in order; first to fire decides.

- **E1** No single recorded next action → **NOT-ELIGIBLE** ("no recorded next action; CRE must name one").
- **E2** Already addressed (Step 4a) → **NOT-ELIGIBLE** with the evidence, plus a gate-bin line *proposing* the item be closed. Never close it yourself.
- **E3** Genuinely blocked or waiting, judged from the item's text → **NOT-ELIGIBLE** ("blocked on …").
- **E4** Finishing needs a fork ruled — which design, keep-or-cut, where a rule lives → **ATTENDED**, naming `decision-helper` as the route.
- **E5** Fiction execution — chapter drafting, prose, a register or canon pass, anything authoring CRE's words → **ATTENDED**, plan-and-defer only.
- **E6** The next action lands outside the agent's write surface — desktop-only (pack/Save-skill/install/git/StoryLine/"Run now"), a scheduled-task prompt edit, `_DIRECTIVES`, an OS anchor, `DECISIONS/`, `TODAY.md`, the week plan → **ATTENDED**.
- **E7** Otherwise → **UNATTENDED**. Compose the plan.

A useful E6 sharpening from the pilot: an item with one in-surface leg and one out-of-surface leg is only splittable when the legs are genuinely independent. Where DIR-016 binds them — a canon doc *and* its live task prompt must change in the same session — serving the doc half alone would ship a route updated on one surface of two, which DIR-016 names the most expensive failure shape available. Rule the whole item ATTENDED instead.

Record every disposition with a one-clause reason in the run receipt. **Write nothing back into `_BACKLOG` as a tag, lane, or status field** — the ruling lives in the receipt and the plan only. An item can be attended one run and unattended the next; that is why it is ruled per run and stored nowhere durable.

### Step 4a — The already-addressed check

All three surfaces:

1. `_CHANGELOG.md` — entries since the item's anchor date, **read in full**. Summaries lie.
2. `SYSTEM/reports/` — any dated report naming the anchor or its deliverable.
3. `SYSTEM/backlog-queue/_closed/` — a prior closed plan for this anchor, and its verdict.

Then the **wording-vs-state** check: where the item names a checkable artifact (a file, a doc section, a skill, a task), read the artifact and test the item's wording against it. "Packaging pending" is a snapshot nothing re-checks.

Two constraints on any negative: read to EOF before concluding an edit did not land, and confirm a `Glob` miss with a pathed `Grep` or direct `Read`. Anything less reports "state unconfirmed — partial read," never a confident negative. Every `Glob`/`Grep` against vault content passes an explicit `path`; unpathed, they search the Cowork outputs scratch and return a clean "No files found" with no warning.

## Step 5 — Compose and serve

Write each plan to `SYSTEM/backlog-queue/_served/<YYYY-MM-DD>-<anchor-slug>.md`. Frontmatter serialized, never hand-formatted:

```yaml
---
type: backlog-session-plan
anchor: backlog-approval-gated-openers
item_file: _BACKLOG.md
mode: unattended        # or attended
round: 1
served: 2026-09-04
served_by: backlog-supervisor
eligibility_reason: "read-and-report sweep landing in SYSTEM/reports/; no fork, no fiction, no desktop step"
---
```

Body — all of these sections:

- **## The item** — the anchor and the item's current state **in your own words**. Not a copy-paste; the plan is the translation.
- **## The job** — what this session must accomplish, whole and upfront, in plain instruction. One session's worth. If it does not fit one, split it, serve only the first part, and say so.
- **## Why** — one or two sentences. An agent that knows why makes better calls at the edges.
- **## References** — every file the work needs, by full path, each with one line on what it carries. Include the directives that bind this job, by number. Anything the agent would otherwise have to go find. Name the substrate a reference needs when it is not the file tools — `C:\Users\Chad\Claude\Scheduled\` in particular is unreachable by `Read` and needs the host route.
- **## Steps** — the ordered work. Name the substrate for any mechanical step.
- **## Write surface for this plan** — the exact paths this session may write. Everything not named defers.
- **## Completion conditions** — objective and checkable. *"`SYSTEM/reports/2026-09-04-x.md` exists and lists all 14 prompts with a flag or a clear."* Not *"the sweep is done."* The audit reads these; a vague condition makes the audit a judgment call, which the loop cannot afford. **Check them against your own Defer section before serving** — a condition that forbids what the Defer rule authorizes is a self-contradicting plan, and the agent will be right either way.
- **## Defer instead of guessing** — the named cases where this job should stop, each with what to write in the log.
- **## Out of scope** — the adjacent work not to do.

**The test a plan must pass:** could a stranger with no memory of this session and no access to CRE finish it without asking a question? If not, research it further or rule the item attended.

For `mode: attended`, same shape but addressed to a sitting with CRE: the research already done, the specific ruling he needs to give, the options laid out. Its job is to make his sitting short.

**Caps:** at most 3 plans served per run, and never more than 5 open plans across `_served/` + `_working/` + `_review/`.

Re-read each written plan through the file tools and confirm the frontmatter parses and every section is present.

## Step 6 — Gate bin

Every deferral, escalation, and notable NOT-ELIGIBLE goes to a `## Needs CRE ruling (backlog-supervisor YYYY-MM-DD)` section in `_BACKLOG.md` — one line each: the item, the proposed action, the one-clause reason. This is the surface `sysadmin` already aggregates on the attended admin pass, so escalations reach a channel CRE opens without opening a new one. If a prior run's bin has unruled lines, **fold them in rather than stacking a second bin**.

Targeted file-tool edit; verify by re-reading. Never `patch_vault_file`, never a whole-file MCP rewrite — both have silently truncated canon in this vault.

## Step 7 — Receipt, unconditionally

Append one line, newest-first, to `SYSTEM/reports/backlog-supervisor-runs.md` on **every fire — including a stand-down and including a halt**: date, mode, counts audited / passed / failed / escalated / served, the dispositions ruled, any substrate fallback. Create the file if absent.

Not optional. Every task here writes a receipt when it runs and nothing writes anything when it does not, which is why six days of scheduler silence produced no signal at all. The stand-down line is the most valuable line in this file.

## Step 8 — Log

A run that changed the vault: `_CHANGELOG.md` top-insert (meta lane). New fragility → `_OBSERVATIONS.md` with a `^obs-NNN` anchor — re-scan for the highest anchor immediately before writing and re-read the heading after, because a duplicate anchor resolves to the first match and silently misdirects every later citation. Follow-ups → `_BACKLOG.md`. A stand-down run is trivial: receipt only, no changelog entry.

## Stop conditions

- Sentinel fails → halt, receipt, report.
- § Standing queue missing or stale → stand down, receipt, report. Never compute a ranking to fill the gap.
- File tools cannot write `_BACKLOG.md` → halt, receipt, report. Never fall back to `patch_vault_file`.
- Working set at cap with an empty `_review/` → stand down. Normal, not a fault.
- `bash` is the only route left for a mechanical step → declared bash-blocked: report the step unrun rather than attempting it.
- No candidate eligible → a valid, informative run. Receipt the dispositions. If several runs running rule everything attended, say so plainly in the gate bin: it means the remaining debt is genuinely CRE's. That is a finding, not a failure — and unlike v1's "surface exhausted," you can say why, item by item.

## What this is NOT

- Not `backlog-sweep` — it owns maintenance, archival, dedupe, observation graduation, and the Standing queue computation. Never archive, dedupe, graduate, or recompute.
- Not a re-ranker. You have no ordering of your own.
- Not `sysadmin` — you feed its gate bin; you never rule a deferral.
- Not `decision-helper` — you never rule a fork.
- Not `day-launch` or `week-shape` — never write `TASKS/TODAY.md` or the week plan.
- Not `task-control` — never pause, resume, create, or edit a scheduled task.
- Not a fiction executor — no drafting, no prose, no register or canon pass.
- Not a scheduler liveness monitor. Your receipts make liveness checkable, but you cannot detect your own absence and must never be relied on for it.
