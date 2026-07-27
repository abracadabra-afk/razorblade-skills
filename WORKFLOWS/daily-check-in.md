---
type: workflow
name: daily-check-in
trigger: daily check-in
aliases: [check in, check-in, log the day, how the day went, daily debrief, run the check-in]
inputs: [CRE's spoken or typed reflection, the _checkin/ staging queue, TASKS/TODAY.md (for the date + the objective half)]
outputs: [LIFE/CHECK-INS/entries/YYYY-MM-DD-daily.md (verbatim, immutable), derived task lines in TASKS/TASKS.md, derived items in INBOX]
lane: life
status: spec — packs after 2–3 live runs
governed-by: DIR-015
last_updated: 2026-07-26
---

# WORKFLOW: daily-check-in

## When to use

CRE says **"daily check-in"** — at the desk, or dictated from anywhere into `_DICTATION INBOX/` — and talks about how the day went: what worked, what didn't, what he's avoiding, ideas, mood, opinions on the system. Also fires as the **subjective half of `day-launch`'s close-out**: "close the day" runs the objective derive pass, then asks for this.

The whole instrument is one sentence: **he talks, the machine sorts.** No form, no questionnaire, no prompts to answer.

## Why this exists

The vault could measure *what happened* — artifacts, receipts, `_CHANGELOG` — and had no channel at all for *how it went*. `day-launch`'s own doc states the limit: *"the derive pass only sees work that left an artifact… Those need a one-line drop into INBOX or they stay invisible."* So friction, flow, what a workflow actually cost him, and what he dodged and why were invisible to every instrument in the vault. That is the disconnect CRE named: a system built to serve him, with no feedback from him, and therefore no data to improve it with.

CRE-ratified 2026-07-26 (three forks: ledger in `LIFE/CHECK-INS/`, folded into close-out + standalone, daily ships first).

## Design intent (why every rule below exists)

- **The daily NEVER names a pattern.** One entry is n=1. A pass that offers analysis daily will manufacture patterns from noise — DIR-014's measured corollary (*precision collapses faster than recall improves*) is the evidence. Pattern-naming belongs to the weekly, over a window. This is the single most important rule in the doc.
- **Friction kills this class of system, not bad design.** If a check-in costs more than ~3 minutes or requires being at the desk, it becomes Pattern #2 (tool abandonment) — and then the weekly has no data and the whole thing is theatre that *feels* like measurement. Hence: dictatable from anywhere, unstructured, verbatim in, no questions asked back.
- **Verbatim is a contract, not a default.** The entry is a sample of how he was thinking that day. A cleaned, summarized, or re-toned entry is a destroyed sample — and destroys the weekly's ability to diff week 3 against week 11.
- **Two outputs from one input.** The ledger (durable, longitudinal) *and* routed actionables. Ledger only → nothing happens. Routing only → the entry is shredded into domains and the trend data is gone. Both, always. (Same shape as `file-inbox`: derived facts + the kept original.)
- **Restart-friendly** (Pattern #2). A skipped day, or ten, costs nothing. No streaks, no "you haven't checked in since Tuesday," ever. The weekly reads whatever window exists.
- **Pattern #19 (validation dependency):** this skill does not reply with encouragement. See the guards.

## Position & guards

- **Governed by [[_DIRECTIVES#DIR-015]]** — read it before running.
  - **Affect is RECORDED, never worked** (clause 1). Mood, frustration, self-assessment go into the entry verbatim and may be trended as data by the weekly. They are never reframed, reassured, coached, processed, or diagnosed. Recording is not working — but the moment the pass *responds* to affect, it is working it, and that is out of bounds.
  - **No validation drip** (clause 5). The pass does not answer a hard day with praise, comfort, or "that's still a good week." It confirms what it filed and stops. On-demand validation is the documented dependency, and a daily instrument is exactly where it would take hold.
  - **Name once and stop, if at all.** If an entry carries something in the affective lane (#4, #11, #12, #13, #14, #19), the daily does not name it either — it records it and moves on. Naming, where warranted, is the weekly's single-shot job, and only ever once, plainly.
- **Gate pattern:** the entry writes unconditionally (it's his own words — there is nothing to rule). **Derived actionables gate**: anything ambiguous is surfaced, not filed.
- **Vault sentinel** (`^obs-004`) before any write. **File tools only**, verify by re-read (DIR-005). Frontmatter serialized (DIR-004).
- **The router is the sole write-path into a domain.** Task-shaped items may be written to `TASKS/TASKS.md` directly (the `day-launch`/`week-shape` precedent). Everything else goes to [[INBOX]] with a hint and the inbox-router files it. This skill never writes VIBES/BUSINESS/KNOWLEDGE/WORKFLOWS.
- **Never promotes anything.** No `^obs-NNN`, no `_BACKLOG` item, no directive off a daily entry. Nominations are the weekly's job and CRE rules them.
- **Never generates CRE's prose**, never schedules the content of his fiction, never invents a task he didn't say.
- **"dispatch" stays reserved** for `_BACKLOG`.

## Intake — three doors, one destination

1. **Dictated (primary).** Say *"Daily check-in."* / *"Weekly check-in."* / *"Check-in."* and talk. `dictation-runner`'s **check-in route** (added 2026-07-26) stages it to `_DICTATION INBOX/_checkin/`, verbatim and un-reconciled. The route is checked **first**, ahead of dev and fiction, because a check-in is routinely canon-dense ("the register pass on Witchwood CH4 fought me") and canon density would otherwise classify his diary as a chapter draft. A filename stem containing `check-in` also routes, so a garbled marker still lands correctly.
2. **At the desk.** Fire the trigger and type or paste.
3. **Folded into close-out.** "close the day" runs the `day-launch` derive pass (objective: what landed), then this (subjective: how it went). One evening ritual, two halves. **Two rituals would mean he does neither** — that is why this is folded rather than standalone-only.

**Why no canon reconcile on this route:** a check-in is not prose. A garbled project name in a diary entry costs nothing worth a false `[AUTHOR:]` flag, and touching the text at all conflicts with the verbatim contract.

## Steps

### 0. Sentinel + frame

Verify `_DIRECTIVES.md` frontmatter. Determine the date and cadence (`daily` unless the marker said weekly). **Ask nothing.** If there's no content yet (bare trigger at the desk), say one line — *"go ahead"* — and take what comes.

### 1. Land the entry — verbatim, first, before anything else

Write `LIFE/CHECK-INS/entries/YYYY-MM-DD-daily.md` per the template in [[LIFE/CHECK-INS/_CHECK-INS]]. The body goes in **untouched**: no cleanup, no paragraphing, no tone repair, no trimming of digressions.

Land it **before** deriving anything. If the derive step fails or the session dies, the record survives — that is the asset. Two entries on one day: suffix `-2`, never overwrite.

### 2. Derive actionables — route, don't interpret

Read the entry back and pull out only what is unambiguously actionable:

- **Task-shaped** (a thing to do, with an implied doer and a finish) → `TASKS/TASKS.md` under `## Active`, schema-tagged per [[TASKS/TASK-SCHEMA]] (`win:`, `#p`, `due:` where a real date was spoken; `due:?` if a deadline is implied but undated), source-stamped `<!-- daily-check-in YYYY-MM-DD -->`.
- **Everything else** that wants to live somewhere — an idea, a fragment, a research question, a business thought → [[INBOX]] verbatim, with a leading `<!-- check-in <date> · intent: <hint> -->` comment for the router.
- **Neither** — reflection, mood, assessment of how something went, opinions on the system → **stays in the entry only.** This is the majority of a check-in and it is the point of the exercise. Do not manufacture tasks out of feelings.

**One judgment rule:** if you can't tell whether something is a task or a reflection, it is a reflection. Over-filing turns his diary into a to-do list he didn't write and trains him to stop talking freely, which costs more than a missed task.

### 3. Surface what you couldn't route — visibly

Anything genuinely ambiguous goes in the entry's `## Open questions` section as **visible prose** — never an HTML comment, never only in chat (DIR-012 clause 4: *a deferral CRE cannot see is not a deferral*). One line each, phrased so he can rule in one word.

### 4. Confirm and stop — no analysis, no encouragement

Reply with the receipt only:

> *Logged. 2 tasks → TASKS.md, 1 item → INBOX. 1 open question in the entry.*

That is the entire response. **Do not** summarize what he said back to him, offer an observation about his week, name a pattern, or say anything appreciative about the work or the check-in. If he asks a direct question in the entry, answer it plainly — that's a conversation, not the pass.

### 5. Log

`_CHANGELOG` entry only if the vault changed — which it did (an entry landed), so one line. Per DIR-003.

## What this skill never does

- **Name a pattern, trend, or theme** — the weekly's job, over a window, with citations. This is the rule most likely to be broken by a well-meaning pass.
- **Work the affective lane** — record it, never respond to it (DIR-015 clause 1)
- **Answer a hard day with praise, comfort, or encouragement** (DIR-015 clause 5)
- **Edit, clean, summarize, or re-tone an entry** — verbatim is the contract
- **Promote anything** to `_OBSERVATIONS`, `_BACKLOG`, or a directive
- **Write a domain bucket directly** — TASKS and INBOX only; the router owns the rest
- **Manufacture tasks from reflection**, or ask follow-up questions to "complete" an entry
- **Guilt, streaks, or gap-shaming** — restarts are the design
- **Run long.** A daily check-in is minutes. If it becomes a session, it has become the avoidance.

## Non-goals

- Not the weekly analyzer (pending — `^backlog-weekly-check-in`, builds against ~2 weeks of real entries)
- Not `work-through` (on-demand stall diagnosis), `decision-helper` (forks), or `day-launch` (initiation + objective receipts)
- Not a companion, a journal prompt, or anything that asks him questions on a schedule

## Honest limits

- **It only knows what he says.** A day he doesn't check in on is silent, and no tuning fixes that. The weekly reads the window that exists and never extrapolates across a gap.
- **The bare spoken marker is the loose one.** *"Check-in."* routes correctly; *"let's do a check in on the cover designer"* is guarded out by a negative lookahead on `on|with|about|at|to|regarding`, but the guard is heuristic. A misroute is non-destructive (a staged note in the wrong queue) and visible.
- **Routing precision is unmeasured until the weekly runs.** The `_FINDINGS.md` self-audit table is the instrument for that; three consecutive windows above 30% rejection is the signal to re-spec rather than keep filing.

<!-- v1 spec authored 2026-07-26. CRE brought the two-skill idea (weekly + daily check-in); the three ratified forks were: ledger at LIFE/CHECK-INS/ (personal-data domain, beside the ADHD pattern map work-through already reads), folded into day-launch close-out AND standalone, and daily-first with the weekly built after ~2 weeks of real entries. Key design call made in the proposal and ratified: capture and analysis are SEPARATE — the daily is forbidden from naming a pattern, because n=1 analysis manufactures noise (DIR-014 corollary). Shipped alongside the dictation-runner check-in route (fourth fork, checked first ahead of dev+fiction, 12 selftest cases + 4 false-fire guards, zero leakage into the 27 pre-existing cases) and the day-launch `## Check-ins` → `## Pings` rename that freed the vocabulary. Packs after 2-3 live runs per the house convention (work-through / dev-reconcile precedent). Not yet mirrored to skills-src/ or packed. -->
