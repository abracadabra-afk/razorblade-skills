---
name: day-launch
description: Launch CRE's working day — the task-initiation and accountability helper built for his ADHD profile. Reads TASKS/TASKS.md plus yesterday's TODAY.md, proposes 3–5 items for the medicated morning window (hard cap 5) with a designated "first domino" stated as a physical first action, gates on CRE's one-pass ratify, writes the plan to TASKS/TODAY.md, and arms the accountability layer — Odysseus check-in nudges plus attended timed-item reminders. Use whenever CRE says "launch the day," "launch my day," "start my day," "plan my day," "what's my three," "close the day," or "wrap the day," and on the day-launch-runner scheduled task. Restart-friendly by design — no streaks, no guilt; a stale plan closes neutrally and the next morning starts fresh. Do NOT use it to dispatch the _BACKLOG ("dispatch" is reserved), triage a decision (decision-helper), or push arbitrary reminders (odysseus-tasks) — it proposes from existing tasks only, never invents work, never writes CRE's prose.
---

# Day Launch

Task initiation is the stall ADHD hits hardest; this skill is the external scaffolding that gets CRE's day *started*. One morning pass: read his task surface, propose 3–5 for the medicated window, hand him a first domino, gate on his ratify, then let outside nudges hold the thread he can't hold in working memory. The machine plans and pings; CRE rules and works.

Canonical doc: `WORKFLOWS/day-launch.md`. Evidence base: `KNOWLEDGE/RESEARCH/2026-07-10 neurodivergent-ai-helpers-measurable-outcomes.md` + `LIFE/MENTAL HEALTH/ADHD Patterns.md` (the spec: Patterns #2 tool-abandonment, #3/#5/#10 initiation, #8 working memory, #15–17 time blindness, #19 validation).

## Position & guards

- **Gate pattern (house rule):** proposes, CRE rules. The morning list is `status: proposed` until he ratifies — in chat, by edit, or by hand.
- **Vault sentinel:** confirm `_DIRECTIVES.md` frontmatter reads `type: ai-os-brain` + `file: directives` before any write; mismatch → halt and ask.
- **File tools only** for `TASKS.md`/`TODAY.md` edits; verify every write by re-reading through the file tools (never a bash/mount read). Frontmatter stays flat scalars.
- **Dual-writer split:** an unattended morning run owns only the fresh proposal; daytime edits are CRE's; close-out is attended. Never rewrite a `TODAY.md` CRE touched today — append or mark only.
- **Close-out never skips the derive pass, and the derive pass never skips `_CHANGELOG.md`.** Even when every item is pre-checked by hand, read today's `_CHANGELOG.md` entries in full first — it is the authoritative record of completions and unplanned work (DIR-003). Trusting the hand-checks and skipping the scan is the 2026-07-14 failure this exists to prevent.
- **Odysseus pushes are attended by default** (inherit `WORKFLOWS/odysseus-tasks.md` mechanics + guards). Sole unattended exceptions, CRE-ruled 2026-07-10: the three fixed nudges — two check-ins (~10:30/~14:30) + the evening close reminder (~21:00; reminds-to-close, never auto-closes). Idempotent via `ody:` HTML-comment stamps; no secrets in titles.
- **Restart rule (Pattern #2):** a stale or zero day is a data point, not a failure. No streaks, no guilt language, ever. The system is built for restarts.
- **"dispatch" is not yours** — that trigger reads `_BACKLOG`. Never answer it.

## The file: `TASKS/TODAY.md`

One rolling file. Rewritten each morning (proposal), appended during the day (check-ins), closed at night (receipts). Exact template:

```markdown
---
type: day-plan
date: 2026-07-10
status: proposed
---

# TODAY — Friday 2026-07-10

**First domino:** the smallest-start item — do 5 minutes of it before anything else; badly is fine

- [ ] item 1  ← first domino
- [ ] item 2 (2:00 pm) <!-- ody: abc123 -->
- [ ] item 3 — the small win

## ⚠️ Lane gaps & open rulings
<!-- v2.3: only when a window is empty/underfed or a ruling is pending — visible prose, never an HTML comment -->

## Check-ins
<!-- HH:MM — what CRE was doing. Data, not judgment. -->

## Receipts (rolling, last 14 days)
- 2026-07-09 — 2/3 · carried: AC filters
```

`status:` moves proposed → launched → closed. Prune receipts older than 14 days on write so the file stays permanently small.

## Morning run ("launch the day" / scheduled)

1. **Sentinel + staleness.** If `TODAY.md` carries an older date and isn't `closed`, run close-out first — neutral receipts, carry-overs collected. A missed day costs one line, not a lecture.
2. **Gather candidates.** Read `TASKS/PORTFOLIO.md` first (v2 — the strategy layer: resident story, ops-lane theme, energy map, rules R1/R2). Then open `- [ ]` items from `TASKS/TASKS.md` (⚡ Inbox + Active), yesterday's carry-overs, anything CRE said this morning. `_ME.md` "Current focus" is the tiebreak lens. Never invent an item; never pull from `_BACKLOG`.
3. **Propose 3–5 (hard cap 5), three-windowed (v2/v3).** **Morning window (`win:morning`) = the resident story, always** (Portfolio rule R1 — never propose a story-switch, never let admin colonize the peak); **afternoon window (`win:ops`) = ops items** (the week's flagship theme + admin batch); **personal window (`win:personal`, late afternoon/early evening) = life-domain tasks** (family, health, personal admin, appointments) — a distinct slot so personal work stays visible and never competes with the flagship. Order of claim: (a) time-bearing today; (b) carry-overs before new; (c) one item advancing Current focus; (d) always one **small win** finishable inside 30 minutes — the built-in validation point. The morning item's **first domino derives from the chapter's own state** — the Daily Close "tomorrow starts at:" line, else the runway/pipeline position ("open the runway, read beat 12, hit record") — never "work on X"; it carries a **pre-committed stop** (time or beat-count — the flow-vs-hyperfocus brake). Rule R2: never propose a backward-edit/revision item unless the pipeline stage says revision — fix-it urges route to `open-loops.md`. Other dominos stay physical first actions ("figure out X" is how a domino dies). **READ THE TASK TAGS (v3, `TASKS/TASK-SCHEMA.md`):** route each candidate to its window by `win:`; order within a window by `#p` (`#p1` > `#p2` > `#p3`). Treat `due:` as the time-bearing signal in (a): surface an item into its window as its deadline nears — `#p1` at 4 days out, `#p2` at 3, `#p3` at 2 — and on/after the date it sits top of its window. A `due:?` item (deadline real, date missing) is a flag to run `triage-the-tasks`, not a scheduling input. An `every:<cadence>` item surfaces into its window on its cadence day (e.g. `every:mon` on Mondays), ordered by `#p` like anything else — it is standing, never archived (see close-out). Hard cap 5 across all three windows. **VISIBLE LANE GAPS (v2.3):** an empty or underfed window is NEVER flagged silently. Write a visible `## ⚠️ Lane gaps & open rulings` section into `TODAY.md` (between the item list and Check-ins) with one block per gap: (a) why the lane is empty, (b) every candidate considered-and-excluded with its reason (paused-by-ruling · gated/attended-only · `_BACKLOG`-resident · due-date not reached), and (c) the ruling that would fill it, stated as options. Naming a `_BACKLOG`-resident candidate there is a pointer, not ingestion — the TASKS boundary stands; CRE's ruling is the only crossing. HTML comments in `TODAY.md` carry machine stamps only (`ody:`, `derived:`, arming state) — never reasoning CRE needs to see (2026-07-15 miss: the empty morning lane's why + options went into an invisible comment and the flagship gap never reached the file CRE reads).
4. **Gate.** Attended: show list + domino + parsed times; CRE ratifies or edits in one pass — never item-by-item interrogation. Unattended: write the proposal (`status: proposed`) and stop; the plan is waiting when he sits down, and ratifying it is itself the initiation ritual.
5. **Write + verify.** `TODAY.md` per template; re-read to confirm.
6. **Arm accountability.** (a) Unattended-allowed: the three standard nudges → Odysseus todos — the two check-ins titled "Check: what am I doing right now? → TODAY.md" (due ~10:30 and ~14:30) plus the evening close reminder "Close: run day-launch close-out → TODAY.md" (due ~21:00); each skipped if already created today. (a2) **FULL-LIST PUSH (v2.2):** at ratify, push EVERY ratified item as an Odysseus todo (due only if timed) and stamp each `TODAY.md` line `<!-- ody: id -->` — the Odysseus tasks UI on CRE's phone is the live day-plan view where he checks things off. If ratify happened by hand-edit with no session, the next session that finds `status: launched` lines unstamped pushes them late. Idempotent: never re-push a stamped line. (b) Attended-only: one reminder per ratified timed item — verbatim time phrase as `due_date`, capture the returned id, stamp the `TODAY.md` line with the `ody:` comment. (c) **Odysseus unreachable** (env unset, 403, connection refused): never fabricate a push and never block the launch on it — the plan stands on its own; flag the un-armed nudges in one line (chat if attended, an HTML comment in `TODAY.md` if not) and move on. No `ody:` stamps without a real returned id. (d) **Windows call mechanics (proven live 2026-07-10):** from a Windows session, do NOT pass a JSON body to the python helper through PowerShell args — PS 5.1 strips the embedded quotes and the request dies as invalid JSON (silently, in the worst case). Push via `Invoke-RestMethod` (`POST $env:ODYSSEUS_URL/api/codex/todos`, Bearer header, `ConvertTo-Json` body). Add shape: `action=add, title, due_date` (natural-language due phrase, backend parses); delete shape uses `id` (not `note_id`). Env vars live at User scope — child shells of a long-running MCP may carry a stale env; read them via `[Environment]::GetEnvironmentVariable(...,'User')` when in doubt.

## During the day

When a nudge fires and CRE next surfaces (or he edits the file directly), stamp one line under `## Check-ins`: time + what he was doing. Avoidance (scrolling, gaming) gets named neutrally — "11:40 — YouTube; redirected to first domino." Recognition, not confession. Completed items get checked immediately: visible receipt, small dopamine, working memory relieved.

## Close-out ("close the day" / auto next morning)

0. **DERIVE PASS (v2.1 — CRE never reports completions; artifacts do).** **MANDATORY and non-skippable — runs in full even when every item is already checked by hand (attended close-out included). Pre-checked items are exactly when this gets skipped and off-list work goes uncredited (2026-07-14 miss: hand-checks trusted, `_CHANGELOG.md` never opened, a new dev skill + four other unplanned wins fell off the receipt). A hand-checked list is never a substitute for the scan.** Before counting, reconcile every open item — today's list AND the week's `TASKS.md` Active seeds — against ground truth. **`_CHANGELOG.md` is the PRIMARY source and the first thing to read: open it and read every entry dated today, start to finish, before counting — close-out is not complete until you have. Every non-trivial session logs there (DIR-003), so it is the single richest record of both completions and unplanned work; most off-list wins surface here and nowhere else.** Evidence order: **(0) Odysseus todo state (v2.2)** for every `ody:`-stamped line — `GET /api/codex/todos?format=json` twice (`archived=false` pending, `archived=true` completed); `done: true` → derived check `<!-- derived: odysseus id, date -->`; **absent from both lists = deleted ≠ done** (falls through to artifacts); endpoint unreachable → skip silently → **`_CHANGELOG.md` today's entries (REQUIRED — read in full, per above)** → project artifacts (new files/mtimes in `dictation/`, `DEV/_intake/`, `slate/`, `revisions/`; `draft.md`/`_status.md` frontmatter; chapter changelog) → project backlogs → `DECISIONS/_QUICK LOG.md`. Verifiable done → check it off with a provenance stamp `<!-- derived: artifact, date -->` (safe-op). Ambiguous → ONE Needs-confirm line in `TODAY.md`; never guess done, never nag twice. Artifacts moved that no item covers → an `unplanned:` receipt line — off-list work earns visible credit.
1. Count checked vs total (derived checks count); append the receipts line: `YYYY-MM-DD — X/Y · carried: items · unplanned: items|none`.
2. Check off completed source lines in `TASKS/TASKS.md` (file-tool edit + verify) so the master list stays true. **Recurrence carve (`TASK-SCHEMA`):** an `every:<cadence>` item is standing — do NOT check it off or archive it; record its completion as a dated receipt in `TODAY.md` and stamp `<!-- last-done: YYYY-MM-DD -->` on the source line, leaving it open to re-arm on the next cadence day.
3. Carry-overs return to the candidate pool silently — no "again?" framing.
4. **CASCADE (v2.1).** If the derive pass emptied a lane ahead of schedule, pull the next open item in that lane from the week's `## This week` order / `TASKS.md` Active into tomorrow's candidate pool and note it in the close line. Seeds all spent → say so; the next week-shape re-shapes. Close-out never invents scope; residency switches stay decision-helper's.
5. One line of grounded validation, honestly sized: what got done, and that the list was a day's worth. On a zero day: "the plan survives a zero day — same time tomorrow." Set `status: closed`.

## Fortnight review (the evidence loop)

Every ~2 weeks, or on "how's day-launch working": read receipts + check-in stamps, surface ONE pattern as a proposal CRE ratifies ("dominos phrased as 'open…' get done; 'figure out…' don't"). Ratified findings append to the canon doc's changelog block. The literature can't measure this stuff; this helper measures itself.

## What this skill never does

- Invent tasks, write CRE's prose, or schedule the content of his fiction — a writing block is an item; the writing is his
- Use guilt, streaks, or "you said you would" — restarts are the design
- Push item-level reminders unattended (the fixed check-in pair is the only exception)
- Answer "dispatch" (that's `_BACKLOG`) or weigh decisions (that's `decision-helper`)
- Exceed 5 items — an overfull list is an unstarted list
