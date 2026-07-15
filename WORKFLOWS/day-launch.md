---
type: workflow
name: day-launch
trigger: launch the day
aliases: [launch my day, start my day, plan my day, what's my three, day launch, close the day, wrap the day]
inputs: [TASKS/TASKS.md open items, yesterday's TASKS/TODAY.md, _ME.md current focus]
outputs: [TASKS/TODAY.md (the day plan + receipts), Odysseus check-in nudges + timed-item reminders (attended), checked-off source lines in TASKS.md at close-out]
lane: life
status: draft
last_updated: 2026-07-15
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
- **Close-out never skips the derive pass, and the derive pass never skips `_CHANGELOG.md`.** Even when every day item is pre-checked by hand, close-out reads today's `_CHANGELOG.md` entries in full first — it is the authoritative record of completions *and* unplanned work (DIR-003 puts every non-trivial session there). Trusting the hand-checks and skipping the scan is the 2026-07-14 failure the derive pass exists to prevent.
- **Odysseus discipline inherited from [[WORKFLOWS/odysseus-tasks]]:** pushes are attended by default; the ONLY unattended pushes allowed are the fixed set of standard nudges — the two check-ins plus the evening close reminder (CRE opted in to the check-ins 2026-07-10; evening close added 2026-07-10). Item-level timed reminders wait for his morning ratify. Idempotent via `<!-- ody: … -->` stamps; secrets never in titles (DIR-001).
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

## ⚠️ Lane gaps & open rulings
<!-- v2.3: present ONLY when a window is empty/underfed or a ruling is pending — visible prose, never an HTML comment: why the lane is empty, what was excluded and why, the ruling that would fill it -->

## Check-ins
<!-- stamped when CRE answers a nudge: HH:MM — what he was doing. Data, not judgment. -->

## Receipts (rolling, last 14 days)
- 2026-07-09 — 2/3 · carried: AC filters
```

`status:` moves `proposed → launched → closed`. Receipts older than 14 days are pruned on write (the file stays small forever; long-term evidence lives in the fortnight review, below).

## Steps — morning run ("launch the day" / scheduled)

1. **Sentinel + staleness check.** Verify `_DIRECTIVES.md` frontmatter. If `TODAY.md` exists with an older date and `status != closed`, run the close-out first (neutral receipts, carry-overs collected) — a missed day costs one line, not a lecture.
2. **Gather candidates.** Open `- [ ]` items from `TASKS/TASKS.md` (⚡ Inbox + Active), yesterday's carry-overs, anything CRE said this morning. Read `_ME.md` "Current focus" as the tiebreak lens. **v2:** read [[TASKS/PORTFOLIO]] first — resident story, ops-lane theme, energy map (the strategy layer; ratified 2026-07-11). Never invent an item.
3. **Propose 3–5.** Hard cap 5. Selection: (a) anything time-bearing today, (b) carry-overs before new, (c) one item advancing Current focus, (d) always include one **small win** (finishable <30 min — the validation point), (e) designate the **first domino**: the item with the lowest activation energy, stated as a physical first action ("open X and read the last paragraph"), never as an outcome. **v2 — energy-mapped slots (2026-07-11, per the ratified spine):** the list is windowed (three windows, per `PORTFOLIO.md`'s energy map). **Morning window (`win:morning`) = the resident story, always** (per `PORTFOLIO.md` R1 — never propose a story-switch, never let admin colonize the peak); **afternoon window (`win:ops`) = ops items** (the week's flagship theme + admin batch); **personal window (`win:personal`, late afternoon/early evening) = life-domain tasks** (family, health, personal admin, appointments) — a distinct slot so personal work is visible and never has to compete with the flagship. The morning item's **first domino comes from the chapter's own state** — the Daily Close "tomorrow starts at:" line, else the runway/pipeline position ("open the runway, read beat 12, hit record"), never "work on <project>". The morning item carries a **pre-committed stop** (time or beat-count — the flow-vs-hyperfocus guardrail, [[KNOWLEDGE/RESEARCH/2026-06-15 flow-state-writing-dictation]]). Per R2 (forward motion): never propose a backward-edit/revision item unless the pipeline stage says revision — fix-it urges route to `open-loops.md`. **v3 — read the task tags (2026-07-14, task-scheduling layer):** candidate items now carry schema tags ([[TASKS/TASK-SCHEMA]]). Route each to its window by `win:`; order within a window by `#p` (`#p1` > `#p2` > `#p3`). Treat `due:` as the time-bearing signal in (a): surface an item into its window as its deadline nears — **`#p1` at 4 days out, `#p2` at 3, `#p3` at 2** — and on/after the date it sits top of its window. A `due:?` item (deadline real, date missing) is a flag to run `triage-the-tasks`, not a scheduling input. An **`every:<cadence>`** item (recurring, [[TASKS/TASK-SCHEMA]]) surfaces into its window on its cadence day (e.g. `every:mon` on Mondays), ordered by `#p` like anything else — it is standing, never archived (see close-out). Still hard-capped at 5 items across all three windows. **v2.3 — visible lane gaps (2026-07-15, CRE-directed):** an empty or underfed window is NEVER flagged silently. When a window (the morning lane especially — it's the flagship) gets no item, write a visible **`## ⚠️ Lane gaps & open rulings`** section into `TODAY.md` (between the item list and `## Check-ins`) with one block per gap naming: (a) *why* the lane is empty, (b) every candidate considered-and-excluded with its reason (paused-by-ruling · `#gated`/attended-only · `_BACKLOG`-resident · due-date not reached), and (c) the ruling that would fill it, stated as options. Surfacing a `_BACKLOG`-resident candidate here is a **pointer, not ingestion** — the TASKS boundary stands; CRE's ruling is the only crossing. **HTML comments in `TODAY.md` carry machine stamps only** (`ody:`, `derived:`, arming state) — never reasoning CRE needs to see or act on. Root cause: the 2026-07-15 unattended run left the morning lane empty (rule-correctly) but put the entire why + the available options in an HTML comment, invisible in Obsidian's reading view — the flagship gap never reached the one file CRE reads in the morning.
4. **Gate.** Attended: show the list + first domino + any parsed times; CRE ratifies/edits in one pass. Unattended (scheduled run): write the proposal to `TODAY.md` tagged `status: proposed` and stop — the plan is ready when he sits down; ratifying it IS the initiation ritual.
5. **Write + verify.** `TODAY.md` per template, file tools, re-read to verify.
6. **Arm the accountability layer.** (a) Unattended-allowed: the standard nudges → Odysseus (`POST /api/codex/todos`; skip any already stamped today) — the two check-ins (title "Check: what am I doing right now? → TODAY.md", due ~10:30 and ~14:30) plus the evening close reminder (title "Close: run day-launch close-out → TODAY.md", due ~21:00). (a2) **v2.2 — FULL-LIST PUSH (increment (i), 2026-07-11):** at ratify, push EVERY ratified day item as an Odysseus todo (title = the item line, verbatim-ish; due only if timed) and stamp each `TODAY.md` line `<!-- ody: <id> -->` — the Odysseus tasks UI (phone, ntfy-backed) is now the live view of the day plan, where CRE checks things off. Fires whenever ratify happens with a session present; if CRE ratified by hand-edit with no session, the next session that finds `status: launched` lines unstamped pushes them late (idempotent via the stamps — never re-push a stamped line). The close reminder pings CRE to close while he still remembers what he did — it does NOT auto-close (that stays the attended close-out / next-morning staleness sweep); its purpose is to keep the tally accurate. (b) Attended-only: one Odysseus reminder per timed item CRE ratified, verbatim time phrase as `due_date`, stamp the `TODAY.md` line `<!-- ody: <id> -->` (the odysseus-tasks Step-4 mechanics exactly). (c) **Odysseus unreachable** (env unset, 403, connection refused): never fabricate a push, never block the launch — flag the un-armed nudges in one line (chat if attended, an HTML comment in `TODAY.md` if not) and move on; no `ody:` stamp without a real returned id. (d) **Windows call mechanics (proven live 2026-07-10, aegis-moon instance):** never pass a JSON body to `odysseus_api.py` through PowerShell args — PS 5.1 mangles embedded quotes into invalid JSON (sometimes silently). Use `Invoke-RestMethod` with a `ConvertTo-Json` body. Add: `action=add, title, due_date` (verbatim natural-language phrase — "in 10 minutes" parsed live). Delete: `action=delete, id` (NOT `note_id`). User-scope env vars may be stale in a long-running shell host — read via `[Environment]::GetEnvironmentVariable(...,'User')`.

## During the day

A nudge fires → whenever CRE next talks to the vault (or just edits the file himself), stamp one line under `## Check-ins`: time + what he was doing. If it was avoidance (scroll/game — Patterns #16/#17), the stamp names it neutrally ("11:40 — YouTube; redirected to first domino"). Recognition, not confession. Any item done → check it off; small dopamine, visible receipt.

## Steps — close-out ("close the day" / auto next morning)

0. **v2.1 — DERIVE PASS (2026-07-11, per CRE: "I don't want to have to tell the system I completed something").** **MANDATORY and non-skippable — the pass runs in full even when every day item is already checked by hand (attended close-out included). Pre-checked items are the exact condition under which the pass gets skipped and off-list work goes uncredited — 2026-07-14 miss: an attended close-out trusted the hand-checks, never opened `_CHANGELOG.md`, and a whole new dev skill (dev-reconcile) plus four other unplanned wins fell off the receipt. A hand-checked list is never a substitute for the scan.** Before counting anything, reconcile every open item — today's `TODAY.md` list AND the week's `TASKS.md` Active seeds — against **ground truth artifacts**, the same derive-don't-ask rule the pipeline board uses ("the board is a CACHE; artifacts are the truth"). **`_CHANGELOG.md` is the PRIMARY evidence source and the first thing close-out reads: open it and read every entry dated today, start to finish, before counting anything — close-out is not complete until you have. It is the single richest record of both completions and unplanned work, because every non-trivial session logs there (DIR-003); most off-list wins surface here and nowhere else.** Evidence sources, in order: **(0) v2.2 — Odysseus todo state (increment (iii), live 2026-07-11)** for every `<!-- ody: -->`-stamped line — two calls: `GET /api/codex/todos?format=json&archived=false` (pending) + `archived=true` (completed); a todo with `done: true` (archived OR all checklist items checked) → derived check `<!-- derived: odysseus <id>, YYYY-MM-DD -->`; a todo **absent from both lists was deleted — deletion ≠ done** (falls through to the artifact scan; no artifact → carries normally); endpoint unreachable → skip this source silently, artifacts still rule. Then: **`_CHANGELOG.md` session entries dated today (REQUIRED — read in full, per above; the richest and most reliable source of unplanned work)**, the chapter/project artifacts themselves (new files or mtimes in `dictation/`, `DEV/_intake/`, `slate/`, `revisions/`; `draft.md`/`_status.md` frontmatter; chapter `changelog.md`), project backlogs, `DECISIONS/_QUICK LOG.md`. Rules: (a) **verifiable done → check it off** with a provenance stamp `<!-- derived: <artifact>, YYYY-MM-DD -->` — a safe-op write; (b) **ambiguous evidence → one Needs-confirm line** in `TODAY.md`, never guessed done, never nagged twice; (c) **unplanned work found** (artifacts moved that no list item covers) → an `unplanned:` receipt line — off-list work earns receipts too (Pattern #19: the credit must be visible, and CRE never has to report it).
1. Count `- [x]` vs total (derived checks count); append the receipts line: `YYYY-MM-DD — X/Y · carried: <items> · unplanned: <items|none>`.
2. **Check off completed source lines in `TASKS/TASKS.md`** (file-tool edit + verify) so the master list stays true. **Recurrence carve ([[TASKS/TASK-SCHEMA]]):** an `every:<cadence>` item is standing — do NOT check it off or archive it. Record its completion as a dated receipt in `TODAY.md` and stamp `<!-- last-done: YYYY-MM-DD -->` on the source line, leaving it open to re-arm for the next cadence day.
3. Carry-overs return to the candidate pool — silently, no "again?!" framing (Pattern #11).
4. **v2.1 — CASCADE.** If the derive pass emptied a lane ahead of schedule (e.g., the week's morning-lane target verifiably done by Tuesday), pull the **next open item in that lane** from the week's `## This week` order / `TASKS.md` Active into tomorrow's candidate pool, and note it in the close line ("morning lane advanced early → next: <item>"). If the whole week's seeds are spent, say so — the next week-shape run re-shapes; close-out never invents new scope (that stays week-shape's job, and residency switches stay decision-helper's).
5. One line of grounded validation, sized honestly: what got done, and that the list was a day's worth. If 0/Y: "the plan survives a zero day — same time tomorrow." Then `status: closed`.

## Fortnight review (the evidence loop)

Every ~2 weeks, or when CRE asks "how's day-launch working": read the receipts + check-in stamps, surface ONE pattern as a proposal he ratifies ("first dominos that start with 'open' get done; ones that start with 'figure out' don't"), and log a ratified finding to `DECISIONS/_WEIGHTS.md`-style memory in this doc's changelog block. This is briefing Do-this #6: the field can't measure; this helper measures itself.

## What this skill never does

- Invent tasks, generate CRE's prose, or schedule the *content* of his fiction
- Guilt, streaks, "you said you would," or any shame framing — restarts are the design, not the failure
- Push item-level Odysseus reminders unattended (the fixed standard nudges — two check-ins + the evening close reminder — are the sole opt-in exceptions)
- Answer "dispatch" (that's `_BACKLOG`) or triage decisions (that's `decision-helper`)
- Exceed 5 items, ever — an overfull list is an unstarted list

## Non-goals (increments)

- ~~Two-way Odysseus completion sync~~ **SHIPPED into v2.2 (2026-07-11):** endpoint (c) live on aegis-moon (`cre/codex-todos-state`, done-state JSON) → full-list push at ratify (step 6 (a2)) → derive-pass evidence source 0 (close-out Step 0). First live proof rides Monday's plan.
- A body-double "work with me" live session mode — v2 candidate once the morning loop is proven
- Auto-ingesting `_BACKLOG` items — TASKS is the boundary; the router owns crossings

<!-- v1 authored 2026-07-10 per ^backlog-task-initiation-helper (ratified decision, DECISIONS/_QUICK LOG.md 2026-07-10). Anchor time 7:00–7:30 + Odysseus check-in opt-in ruled by CRE 2026-07-10. Evening close reminder (~21:00) added 2026-07-10 per CRE — third unattended-allowed nudge; reminds-to-close, never auto-closes. -->
<!-- v2 2026-07-11 per ^backlog-productivity-spine (spine ratified 2026-07-11): Step 2 reads TASKS/PORTFOLIO.md; Step 3 gains energy-mapped lanes (morning = resident story per R1, afternoon = ops), pipeline-aware first domino (Daily Close "tomorrow starts at" line), pre-committed stop, and the R2 no-backward-edits guard. Feeder fixed upstream by WORKFLOWS/week-shape (seeds TASKS.md weekly). Installed .skill now behind this doc — repack pending (desktop pack-skills.ps1). -->
<!-- v2.1 2026-07-11, CRE-directed same session: close-out gains Step 0 DERIVE PASS (reconcile open items against artifacts — pipeline-board derive-don't-ask extended to the day layer; verifiable→check w/ provenance, ambiguous→one Needs-confirm line, unplanned work→receipt) + Step 4 CASCADE (early-emptied lane pulls the next open item in week order; never invents scope). week-shape Step 1 gained the matching weekly derive. Repack still pending. -->
<!-- v2.2.1 2026-07-14, CRE-directed ("harden the close-out to not skip the change log"): Step 0 DERIVE PASS made MANDATORY/non-skippable even when items are pre-checked, and `_CHANGELOG.md` elevated to the named PRIMARY source read in full before counting (was buried mid-chain in the evidence list). New guard bullet added. Root cause: the 2026-07-14 attended close-out trusted hand-checks, never opened `_CHANGELOG`, and dropped 5 unplanned wins (incl. the dev-reconcile skill build) from the receipt. Skill source mirrored. Installed `.skill` now behind this doc — desktop repack + Save-skill pending (DIR-009), `^backlog-repack-day-launch`. -->
<!-- v2.3 2026-07-15, CRE-directed ("things will fall through the cracks if there is not a presentation of what was not populated"): Step 3 gains the VISIBLE LANE GAPS rule + the template gains the `## ⚠️ Lane gaps & open rulings` section — an empty/underfed window always writes a visible gap block (why empty · excluded candidates + reasons · the ruling that would fill it); HTML comments restricted to machine stamps. Root cause: the 2026-07-15 unattended run flagged the empty morning lane (dev-reconcile pilot in _BACKLOG, CH2 S12 paused) only in an HTML comment — invisible in reading view. Skill source mirrored. Repack rides ^backlog-repack-day-launch (one repack carries v2/v2.1/v2.2.1/v2.3). -->
