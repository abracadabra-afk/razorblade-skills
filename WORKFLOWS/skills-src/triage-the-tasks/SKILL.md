---
name: triage-the-tasks
description: Enrich CRE's TASKS.md open items with the task-scheduling schema — priority (#p1/#p2/#p3), window (win:morning/ops/personal), and deadline (due:) tags — so week-shape and day-launch can order and surface them. Use whenever CRE says "triage the tasks," "triage my tasks," "tag my tasks," or a pile of untagged tasks needs making spine-ready. It walks each open item that is missing a #p/win: tag or carries a due:? placeholder, infers the window from the item's domain and a default #p3 priority, and asks CRE ONLY for load-bearing deadline dates, batched into one pass rather than item-by-item. Gated: it proposes tags, CRE rules, then it writes them back per TASKS/TASK-SCHEMA.md and verifies. An inferred date stays due:? until CRE confirms it. Do NOT use it to invent tasks, schedule fiction content, launch or close a day (day-launch), shape the week (week-shape), break a goal into steps (project-breaker), or dispatch _BACKLOG. Restart-friendly; never guilt or streaks.
---

# Triage The Tasks

The enrichment layer of the task-scheduling substrate (ratified 2026-07-14, `SYSTEM/reports/2026-07-14-task-scheduling-layer-proposal.md`): it fills in the schema tags that `week-shape` and `day-launch` read to order and surface work. The convention is frozen in `TASKS/TASK-SCHEMA.md`. This is the **attended, asking** sibling of `inbox-router`'s unattended enrichment — the router flags `due:?`, this skill resolves it.

Canonical doc: `WORKFLOWS/triage-the-tasks.md`. Spec: `LIFE/MENTAL HEALTH/ADHD Patterns.md` (#3 planning-as-procrastination, #15 time blindness, #8 working memory, #2 abandonment).

## Position & guards

- **Gate pattern:** proposes tags, CRE rules, then writes. Asks are batched into ONE pass — never item-by-item.
- **Vault sentinel:** confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`) before any write; mismatch → halt and ask.
- **File tools only**; verify every write by re-read (DIR-005). Tags are inline body text, kept exactly to the schema shape.
- **Fast menu, not a plan** (Pattern #3): soft ~5-minute cap. Infer aggressively; stop CRE only where a missing answer changes *when a task gets served*.
- **Never** invents tasks, schedules fiction content, sets a hard `due:` date without CRE (inferred date = `due:?` until confirmed), or uses guilt/streak framing.
- **Reads the schema as authority** (`TASKS/TASK-SCHEMA.md`) — follows it, never hard-codes tag rules that could drift.

## What counts as "needs triage"

An open `- [ ]` item where **any** of: no `win:`, no `#p`, carries `due:?`, or CRE points at it. Done (`- [x]`) items are never triaged.

## Steps

1. **Sentinel + load.** Confirm the sentinel. Read `TASKS/TASK-SCHEMA.md` + TASKS.md open items; collect triage candidates.
2. **Infer silently (no ask).** Window from domain: fiction drafting → `win:morning`; business/marketing/site/Substack/KDP/ads/admin-cancellations → `win:ops`; family/health/food/personal appointments+admin → `win:personal` (emoji is a strong hint). Priority default `#p3`; `#p2` only on clear signal (flagship, money leak, blocker); `#p1` only for a genuine near-term deadline.
3. **Detect deadlines — the only thing worth asking.** Scan for deadline language ("before X", "by Friday", "next week", "starts", "due", "expires", "renewal", a bare date). Each hit **without a real date** joins the ask list; everything else takes its inferred defaults, unraised. Also detect **recurrence** ("every Monday", "weekly", "each month") → propose `every:CADENCE` (e.g. `every:mon`), which replaces `due:` (one-shot OR recurring, not both — `TASKS/TASK-SCHEMA.md`).
4. **Ask once (batched).** Present the ask list as one compact block — item + inferred window/priority + "deadline? what date?" CRE answers in one pass (a date, "no deadline," or a priority fix). Nothing date-bearing → skip the ask.
5. **Write + verify.** Apply tags per schema order `- [ ] #pN win:WINDOW [due:DATE] the task text`; file tools; re-read to verify. Confirmed date → `due:YYYY-MM-DD`; undatable deadline stays `due:?` (never dropped). Light provenance in the trailing comment (`; triaged YYYY-MM-DD`).
6. **Summarize.** One line: N tagged, M inferred silently, K dates set / still `due:?`. No ceremony.

## Never

Invent tasks or task content · set a hard `due:` without CRE · interrogate item-by-item · run long (Pattern #3) · guilt or streaks · answer "dispatch" · make residency/priority-order calls (PORTFOLIO + decision-helper).
