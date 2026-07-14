---
type: workflow
name: triage-the-tasks
trigger: triage the tasks
aliases: [triage my tasks, triage tasks, run the task triage, tag my tasks]
inputs: [TASKS/TASKS.md open items missing tags or carrying due:?, TASKS/TASK-SCHEMA.md (the convention)]
outputs: [TASKS/TASKS.md open items tagged with #p / win: / due: per the schema; a one-line summary of what was inferred vs. asked]
lane: life
status: draft
last_updated: 2026-07-14
---

# WORKFLOW: triage-the-tasks

## When to use

CRE says **"triage the tasks"** (or a fresh pile of untagged items has landed in TASKS.md and he wants them made spine-ready). The triage step is the **enrichment layer** of the task-scheduling substrate ([[SYSTEM/reports/2026-07-14-task-scheduling-layer-proposal]], ratified 2026-07-14): it walks the open items that are missing schema tags — or carry a `due:?` placeholder — and fills in priority, window, and (where load-bearing) a real deadline, so `week-shape` and `day-launch` can order and surface them correctly. The convention it writes to is frozen in [[TASKS/TASK-SCHEMA]].

It is the **attended, asking** sibling of the router's unattended enrichment: `inbox-router` stamps what it can infer and flags `due:?`; this skill is where CRE's answers actually land.

## Design intent (the pattern map is the spec)

- **Pattern #3 (planning-as-procrastination): this is a fast menu, not a planning session.** Soft cap ~5 minutes. Infer aggressively; stop CRE only where a missing answer changes *when a task gets served*.
- **Pattern #15 (time blindness):** the whole point. A deadline that lives only in prose never feels urgent until it's a crisis; a `due:` date lets the system feel it for him and surface it in range.
- **Pattern #8 (working memory):** priority/date/window live on the line, never in his head.
- **Pattern #2 (abandonment):** restart-friendly. A skipped triage costs nothing — untriaged items keep their inferred defaults (`#p3`, domain-inferred `win:`), stay served, and wait for the next run. No streaks, no backlog-of-shame.

## Position & guards

- **Gate pattern:** proposes tags, CRE rules, then writes. The asks are batched into ONE pass — never item-by-item interrogation.
- **Vault sentinel** (`^obs-004`): confirm `_DIRECTIVES.md` frontmatter before any write.
- **File tools only**; verify every write by re-read (DIR-005). Tags are inline body text (not frontmatter) — no YAML concern, but keep them exactly to the schema shape.
- **Never invents tasks**, never schedules the content of CRE's fiction, never sets a **hard `due:` date** without CRE (an inferred date is always `due:?` until he confirms it), never guilt/streaks.
- **Reads the schema as authority** ([[TASKS/TASK-SCHEMA]]) — if the convention changes, this skill follows it; it does not hard-code tag rules that could drift.

## What counts as "needs triage"

An open `- [ ]` item is a triage candidate if **any** of:
- it has no `win:` tag, or
- it has no `#p` tag, or
- it carries `due:?` (a known-but-undated deadline), or
- CRE explicitly points at it.

Done (`- [x]`) items are never triaged.

## Steps

1. **Sentinel + load.** Confirm the vault sentinel. Read [[TASKS/TASK-SCHEMA]] (the convention) and TASKS.md's open items. Collect the triage candidates.
2. **Infer silently (no ask).**
   - **Window** from domain/content: fiction drafting → `win:morning`; business / marketing / site / Substack / KDP / ads / admin-cancellations → `win:ops`; family, health, food, personal appointments/admin → `win:personal`. (Emoji is a strong hint: 🌲→morning; 👻📈📰🌐💸→ops; 🏠 and family/health language→personal.)
   - **Priority** default `#p3`; bump to `#p2` only on clear signal (a flagship item, a money leak, a blocker); `#p1` only for a genuine near-term deadline.
3. **Detect deadlines → the ONLY thing worth asking.** Scan each candidate for deadline language ("before X", "by Friday", "next week", "starts", "due", "expires", "renewal", a bare date). For every hit **without a real date**, add it to the ask list. Everything else takes its inferred defaults and is not raised. Also detect **recurrence** language ("every Monday", "weekly", "each month", "recurring") → propose an `every:<cadence>` tag (e.g. `every:mon`), which **replaces** `due:` (a task is one-shot or recurring, not both — [[TASKS/TASK-SCHEMA]]).
4. **Ask once (batched).** Present the ask list as one compact block — each item + its inferred window/priority + the question "deadline? what date?" CRE answers in one pass (a date, "no deadline," or a priority correction). If nothing is date-bearing, skip the ask entirely and go to write.
5. **Write + verify.** Apply the tags to each open line per the schema order (`- [ ] #pN win:<window> [due:…] <text>`), file tools, re-read to verify. A confirmed date becomes `due:YYYY-MM-DD`; a deadline CRE couldn't date stays `due:?` (never silently dropped). Stamp a light provenance note in the line's trailing `<!-- … ; triaged YYYY-MM-DD -->` comment.
6. **Summarize.** One line: N items tagged, M inferred silently, K dates set (or still `due:?`). No ceremony.

## Relationship to the other layers

- **Upstream:** `inbox-router` files raw tasks and pre-stamps inferred `win:` + `due:?` — this skill resolves those flags.
- **Peers:** `week-shape` reads the tags to place items in the week; `day-launch` reads `due:` + `#p` to surface and order the day. Neither invents a tag value — triage (or CRE) is the author of dates.
- **Downstream, later:** the `project-breaker` helper (AI Helper Targets #3, unbuilt) will emit already-tagged sub-steps into this same schema.

## What this skill never does

- Invent tasks or task content; schedule the content of CRE's fiction
- Set a hard `due:` date on its own — an unconfirmed date is always `due:?`
- Interrogate item-by-item, or run longer than a few minutes (Pattern #3)
- Guilt, streaks, or "you still haven't dated this" framing
- Answer "dispatch" (that's `_BACKLOG`) or make residency/priority-order calls (PORTFOLIO + decision-helper)

<!-- v1 authored 2026-07-14 as Step 2 of ^backlog-task-scheduling-layer (proposal ratified same day). Canon doc; skill source at WORKFLOWS/skills-src/triage-the-tasks/SKILL.md. Desktop pack-skills.ps1 + Save-skill pending (DIR-009). -->
