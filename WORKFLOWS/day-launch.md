---
type: workflow
name: day-launch
trigger: launch the day
aliases: [launch my day, start my day, plan my day, what's my three, day launch, close the day, wrap the day]
inputs: [TASKS/TASKS.md open items, yesterday's TASKS/TODAY.md, _ME.md current focus]
outputs: [TASKS/TODAY.md (the day plan + receipts), Odysseus check-in nudges + timed-item reminders (attended), checked-off source lines in TASKS.md at close-out]
lane: life
status: draft
last_updated: 2026-07-10
---

# WORKFLOW: day-launch

## When to use

Every working morning, in the medicated window (~7:00–7:30). CRE says **"launch the day"** (or the `day-launch-runner` scheduled task fires) → the helper reads [[TASKS/TASKS]] + yesterday's `TODAY.md`, proposes **3–5 items** for today with a **first domino**, CRE ratifies in one pass, the plan lands in `TASKS/TODAY.md`, and the accountability layer (Odysseus check-in nudges + timed-item reminders) goes live. At day's end (or next morning), **"close the day"** records receipts and carries the rest forward without ceremony.

Built off the ratified 2026-07-10 decision (`DECISIONS/_QUICK LOG.md`, `^backlog-task-initiation-helper`): task **initiation** is the strongest-evidence AI-assist mechanism with no vault coverage ([[KNOWLEDGE/RESEARCH/2026-07-10 neurodivergent-ai-helpers-measurable-outcomes]]). The EF-offload layer already exists; this is the layer that gets the day *started*.

## Design intent (why every rule below exists)

CRE's pattern map ([[LIFE/MENTAL HEALTH/ADHD Patterns]]) is the spec:

- **Initiation is the stall** (Patterns #3, #5, #10): the plan must end in a *first physical action*, not a list. Hence the first domino + the 5-minute rule.
- **Working memory can't hold the plan** (#8): the plan lives in ONE visible file, never in his head. `TODAY.md` is the external working memory.
- **Time blindness eats the day** (#15–17): fixed check-in nudges ("what am I doing right now?") arrive from outside, via Odysseus, because markdown can't tap him on the shoulder.
- **Tools get abandoned** (#2): the system is built for **restarts, not streaks**. A stale `TODAY.md` is never a failure state — the next morning run just starts fresh and notes a neutral receipt. No streak counters, no guilt language, ever.
- **Validation must be built in** (#19): visible `- [x]` receipts, a small win in every day's list, and a one-line "you did X of Y — and Y was sized for a day" at close-out.
- **His day, his call**: the helper proposes the 3–5; CRE rules. It never invents tasks, never schedules his fiction's content (a *writing block* is an item; the prose is his), and never moralizes about what got done.

## Position & guards

- **Gate pattern:** proposes, CRE rules. The morning proposal is `status: proposed` until he ratifies (chat "go" / edits / his own hand-edit of the file).
- **Vault sentinel** (`^obs-004`) before any write.
- **File tools only** for `TASKS.md` + `TODAY.md` edits, verify by re-read (DIR-005 / `^obs-014`). Frontmatter kept to flat scalars (DIR-004 posture).
- **Dual-writer split:** the unattended morning run owns the fresh `TODAY.md` proposal; daytime edits are CRE's; close-out is attended. Never rewrite a `TODAY.md` CRE has touched today — append/mark only.
- **Odysseus discipline inherited from [[WORKFLOWS/odysseus-tasks]]:** pushes are attended by default; the ONLY unattended push allowed is the fixed pair of standard check-in nudges (CRE opted in 2026-07-10). Item-level timed reminders wait for his morning ratify. Idempotent via `<!-- ody: … -->` stamps; secrets never in titles (DIR-001).
- **"dispatch" stays reserved** for `_BACKLOG` proposals — day-launch never answers it.

## The file: `TASKS/TODAY.md`

One rolling file — rewritten each morning (proposal section), appended during the day (check-ins), closed at night (receipts). Template:

```markdown
---
type: day-plan
date: 2026-07-10
status: proposed
---

# TODAY — Friday 2026-07-10

**First domino:** <the smallest-start item — do 5 minutes of it before anything else, badly is fine>

- [ ] <item 1>  ← first domino
- [ ] <item 2> (2:00 pm) <!-- ody: abc123 -->
- [ ] <item 3 — the small win>

## Check-ins
<!-- stamped when CRE answers a nudge: HH:MM — what he was doing. Data, not judgment. -->

## Receipts (rolling, last 14 days)
- 2026-07-09 — 2/3 · carried: AC filters
```

`status:` moves `proposed → launched → closed`. Receipts older than 14 days are pruned on write (the file stays small forever; long-term evidence lives in the fortnight review, below).

## Steps — morning run ("launch the day" / scheduled)

1. **Sentinel + staleness check.** Verify `_DIRECTIVES.md` frontmatter. If `TODAY.md` exists with an older date and `status != closed`, run the close-out first (neutral receipts, carry-overs collected) — a missed day costs one line, not a lecture.
2. **Gather candidates.** Open `- [ ]` items from `TASKS/TASKS.md` (⚡ Inbox + Active), yesterday's carry-overs, anything CRE said this morning. Read `_ME.md` "Current focus" as the tiebreak lens. Never invent an item.
3. **Propose 3–5.** Hard cap 5. Selection: (a) anything time-bearing today, (b) carry-overs before new, (c) one item advancing Current focus, (d) always include one **small win** (finishable <30 min — the validation point), (e) designate the **first domino**: the item with the lowest activation energy, stated as a physical first action ("open X and read the last paragraph"), never as an outcome.
4. **Gate.** Attended: show the list + first domino + any parsed times; CRE ratifies/edits in one pass. Unattended (scheduled run): write the proposal to `TODAY.md` tagged `status: proposed` and stop — the plan is ready when he sits down; ratifying it IS the initiation ritual.
5. **Write + verify.** `TODAY.md` per template, file tools, re-read to verify.
6. **Arm the accountability layer.** (a) Unattended-allowed: the two standard check-in nudges → Odysseus (`POST /api/codex/todos`, titles "Check: what am I doing right now? → TODAY.md", due ~10:30 and ~14:30; skip if already stamped today). (b) Attended-only: one Odysseus reminder per timed item CRE ratified, verbatim time phrase as `due_date`, stamp the `TODAY.md` line `<!-- ody: <id> -->` (the odysseus-tasks Step-4 mechanics exactly). (c) **Odysseus unreachable** (env unset, 403, connection refused): never fabricate a push, never block the launch — flag the un-armed nudges in one line (chat if attended, an HTML comment in `TODAY.md` if not) and move on; no `ody:` stamp without a real returned id. (d) **Windows call mechanics (proven live 2026-07-10, aegis-moon instance):** never pass a JSON body to `odysseus_api.py` through PowerShell args — PS 5.1 mangles embedded quotes into invalid JSON (sometimes silently). Use `Invoke-RestMethod` with a `ConvertTo-Json` body. Add: `action=add, title, due_date` (verbatim natural-language phrase — "in 10 minutes" parsed live). Delete: `action=delete, id` (NOT `note_id`). User-scope env vars may be stale in a long-running shell host — read via `[Environment]::GetEnvironmentVariable(...,'User')`.

## During the day

A nudge fires → whenever CRE next talks to the vault (or just edits the file himself), stamp one line under `## Check-ins`: time + what he was doing. If it was avoidance (scroll/game — Patterns #16/#17), the stamp names it neutrally ("11:40 — YouTube; redirected to first domino"). Recognition, not confession. Any item done → check it off; small dopamine, visible receipt.

## Steps — close-out ("close the day" / auto next morning)

1. Count `- [x]` vs total; append the receipts line: `YYYY-MM-DD — X/Y · carried: <items>`.
2. **Check off completed source lines in `TASKS/TASKS.md`** (file-tool edit + verify) so the master list stays true.
3. Carry-overs return to the candidate pool — silently, no "again?!" framing (Pattern #11).
4. One line of grounded validation, sized honestly: what got done, and that the list was a day's worth. If 0/Y: "the plan survives a zero day — same time tomorrow." Then `status: closed`.

## Fortnight review (the evidence loop)

Every ~2 weeks, or when CRE asks "how's day-launch working": read the receipts + check-in stamps, surface ONE pattern as a proposal he ratifies ("first dominos that start with 'open' get done; ones that start with 'figure out' don't"), and log a ratified finding to `DECISIONS/_WEIGHTS.md`-style memory in this doc's changelog block. This is briefing Do-this #6: the field can't measure; this helper measures itself.

## What this skill never does

- Invent tasks, generate CRE's prose, or schedule the *content* of his fiction
- Guilt, streaks, "you said you would," or any shame framing — restarts are the design, not the failure
- Push item-level Odysseus reminders unattended (the fixed check-in pair is the sole opt-in exception)
- Answer "dispatch" (that's `_BACKLOG`) or triage decisions (that's `decision-helper`)
- Exceed 5 items, ever — an overfull list is an unstarted list

## Non-goals (increments)

- Two-way Odysseus completion sync (rides `^backlog-odysseus-bridge-increments` (a))
- A body-double "work with me" live session mode — v2 candidate once the morning loop is proven
- Auto-ingesting `_BACKLOG` items — TASKS is the boundary; the router owns crossings

<!-- v1 authored 2026-07-10 per ^backlog-task-initiation-helper (ratified decision, DECISIONS/_QUICK LOG.md 2026-07-10). Anchor time 7:00–7:30 + Odysseus check-in opt-in ruled by CRE 2026-07-10. -->
