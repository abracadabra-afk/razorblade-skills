---
type: workflow
name: backlog-supervisor
trigger: supervise the backlog
aliases: [serve the backlog, run the backlog supervisor, audit the backlog work, close out the backlog, run the close-out, run the evening close-out]
inputs: [_BACKLOG.md § Standing queue (backlog-sweep's ranking — consumed, never recomputed), _BACKLOG.md lane items + project shards, SYSTEM/backlog-queue/_review/ completion logs, SYSTEM/backlog-queue/_intake/ routed findings, _CHANGELOG.md, SYSTEM/reports/, SYSTEM/backlog-queue/_closed/, every surface in § Intake (the sweepers' bins and reports, the drift ledger, SCRATCHPAD/, the run-receipt logs)]
outputs: [session plan .md files in SYSTEM/backlog-queue/_served/ and _attended/, audit verdicts moving plans to _closed/ or fix prompts back to _served/, re-probe records beside closed plans, routed findings in SYSTEM/backlog-queue/_intake/, rulings-sheet lines in SYSTEM/backlog-queue/_rulings/pending.md, the weekly rulings sheet SYSTEM/backlog-queue/_rulings/<sunday>-rulings.md, the weekly briefing SYSTEM/reports/<sunday>-vault-briefing.md + its TASKS.md seed, an unconditional run receipt in SYSTEM/reports/backlog-supervisor-runs.md]
lane: meta
status: draft
version: 2
created: 2026-09-04
last_updated: 2026-09-04
---

# WORKFLOW: backlog-supervisor

## When to use

CRE says **"supervise the backlog"** / **"serve the backlog"** / **"run the backlog supervisor"** (the morning fire), or **"close out the backlog"** / **"run the close-out"** (the evening fire), or either scheduled task fires. It is the **planning and reviewing half** of the supervised backlog loop; [[WORKFLOWS/backlog-agent]] is the executing half. **Since v2 (2026-09-04) it is also the vault's one reader of every system gate and bin** — see § Intake. Nothing a sweeper emits is meant to reach CRE unresearched; this skill reads it, resolves what the tree answers, executes what the auto-ratify class covers, plans what the agent can do, and puts the rest on one weekly sheet.

**Two fires, two modes — never folded into one run.** Plan/serve and audit/close are different jobs; folded together the morning run gets slow and the close-out gets skipped (CRE-ruled 2026-09-04).

- **Morning fire, `mode: morning` — plan/serve** (`backlog-supervisor`, daily 08:20). Two jobs, in this order every run:
  1. **Audit** — any completion log sitting in `SYSTEM/backlog-queue/_review/` gets read against its plan's completion conditions. Pass moves it to `_closed/` awaiting its re-probe; fail comes back as a fix prompt naming the specific mistakes.
  2. **Serve** — for each eligible backlog item and each routed finding in `_intake/`, compose a **session plan**: the instructions to work the item, the references the work needs, the **observable** the close-out will re-probe, and the completion conditions, written so a cold agent with no memory of this session can finish it without asking a question.
- **Evening fire, `mode: close-out` — audit the day, close what is finished, keep the bins current** (`backlog-supervisor-close`, daily 20:20). It re-probes yesterday's closed plans against their observables before an item is closed in `_BACKLOG`; walks every intake surface for what the day's runs emitted; closes superseded and finished items; retires phantom findings; routes the rest to `_intake/` (agent) or `_rulings/pending.md` (CRE). **On Sundays** it also compiles the weekly rulings sheet and the weekly briefing and seeds the sheet onto `TASKS.md` (§ The weekly sheet and the briefing). Close-out mode **never serves a plan** and never reads § Standing queue for candidates — that is the morning's job.

Audits run first in the morning because a stuck item that never gets reviewed is worse than an item that never gets served, and because the cheap-check-first rule (DIR-008 cl. 2) requires the early-exit to account for **pending queue state**, not just new arrivals (`^obs-166`).

## Why this skill exists — the v1 failure it is built around

`vault-backlog-agent` (2026-06 → deleted 2026-08-03) self-selected items straight out of `_BACKLOG` and executed them. On its third run it reported *"auto-run surface exhausted"* and stopped finding work ([[SYSTEM/reports/2026-06-16-vault-backlog-agent-dispatch-exhausted]]). The diagnosis in that report is the whole design brief for this skill: **backlog items are written for a human and are not directly executable.** An item says *"land the gate clause into the remaining pass docs"* — a person knows what that means; an agent with no plan does not, and correctly refuses.

The translation step from *human-readable item* to *executable session* did not exist. That is this skill. The agent never reads `_BACKLOG` to choose work; it reads a plan this skill wrote.

`backlog-sweep.md` § Step 4c pre-authorized exactly this route: *"If an unattended executor is ever wanted again, that is a CRE decision to author a fresh doc-backed task with its own routing — never a revival of this taxonomy or the retired prompt."* This is that fresh doc. It revives nothing.

## Why v2 exists — the second dispersal (2026-09-04)

The admin pass ([[WORKFLOWS/sysadmin]]) was built because CRE had to remember to open five artifacts and opened none. It fixed the *reading* — one list — and left the *ruling* where it was: every judgment call from every sweeper still ended as a line he had to tap, and DIR-012 clause 1's *never auto-rule* meant a run could not close an item it had already proved closed. The supervisor's first live run made the cost measurable: **nine of eleven candidates ruled ATTENDED**, most needing nothing from him but a yes to a stamp, a check-off, or a rewrite-down the run had already researched. Two attended channels then existed for the same deferrals — the Monday admin pass and the supervisor's gate bin — which is the dispersal again, one layer up.

CRE ruled the fix (the self-management handoff, 2026-09-04): unless a call directly impacts the outcome of his work he accepts the system's recommendation anyway, so a defined class of recommendations is his **standing yes** (§ The auto-ratify class); every gate and bin routes **through this skill** rather than into his field of view (§ Intake); the admin pass merges into **one weekly sheet** this skill compiles and `sysadmin` walks, cleared every week rather than capped; a second daily fire closes out the day; and every closed item carries a **re-probed observable** before it is closed. Provenance: [[TASKS/PROJECTS/vault-self-management]].

## Intake — every gate-emitting surface and its route

**The rule:** sweepers keep writing where they write today. **This skill consumes.** No sweeper writes a bin CRE is expected to open unaided, because this table is the documented route for each one, and the close-out fire walks it every evening. A surface missing from this table is a bin with no server — the DIR-021 clause 4 shape — and adding the row is the fix, never a new attended channel.

| Source | Surface it writes (unchanged) | Read by | Route |
|---|---|---|---|
| `backlog-sweep` (Sun 14:38) | `_BACKLOG.md` § Standing queue | morning | candidates, in the block's own order (§ Candidate source) |
| `backlog-sweep` | `_BACKLOG.md` § Needs CRE ruling (backlog-sweep …) — consolidations, stale drops, re-prioritizations, compressions, derive-closures, up to 5 graduation proposals | close-out (Sun) | research each (DIR-011) → **AUTO** where in class (a compression the sweep drafted, a derive-closure with decisive evidence, a stale drop whose target is provably gone → execute, stamp the bin line `✅ auto-ratified <date>`) · **RULE** for re-prioritizations, graduations (a directive is never in class), consolidations that change scope → sheet · **PHANTOM** dropped with the mechanism named |
| `task-audit` (Sun 13:53) | `SYSTEM/reports/<date>-task-audit.md` punch list | close-out (Sun) | doc-side drift (canon doc behind a prompt that is right) → **AGENT** plan via `_intake/` · prompt-side drift → **RULE** as a **desktop trip** line with the drafted body in a report (DIR-005: prompt edits stay attended) · false positives → **PHANTOM**, counted per source. Absorbs `^backlog-taskaudit-gatebin` — the report is the bin now, and this row is its server |
| `link-audit` (Sun 16:21) | `SYSTEM/reports/<date>-link-audit.md` | close-out (Sun) | a dangling ref whose target a direct `Read` finds → **PHANTOM** (`^obs-198`) · a rename/move fix inside the class surface → **AGENT** plan · anything in `WRITING/**` or `REFERENCE/` → **RULE** (fiction-side, thin) |
| `skills-sweep` (Sun 13:05) | `SYSTEM/reports/<date>-skills-sweep.md` install queue / repackage handoff / STALE rows | close-out (Sun) | every pack / Save-skill / install → **RULE** as one **desktop-trip checklist** line on the sheet (never attempted unattended, DIR-007/009) · a SOURCE-AHEAD row whose source edit is in class → **AGENT** if the doc side needs finishing, else the same desktop line |
| `vault-health` / `log-rotate` (Sun 15:39) | `_BACKLOG.md` § Needs CRE ruling (log-rotate …) + `SYSTEM/reports/brain-doc-sizes.json` + `vault-health-runs.md` | close-out (Sun) | `_CHANGELOG` carve → **RULE** desktop line · `_OBSERVATIONS` / `_BACKLOG` band findings → **RULE** with the size stated (the count argument is unreliable, the byte measurement is not) · a bin whose recommendation live state has since satisfied → **AUTO**: stamp `superseded_by:` in place |
| `bootstrap-manager` (attended only) | `SYSTEM/reports/<date>-bootstrap-review.md` three-bin punch list | close-out | BATCH-RATIFY bin → **RULE** as one block line (anchors are never in class) · PROPOSED / QUERY → **RULE** individually. Consumed only; never re-run |
| this skill, morning fire | `SYSTEM/backlog-queue/_closed/` plans awaiting re-probe · `_attended/` ages | close-out | § Re-probe · aging line to `pending.md` |
| `backlog-agent` | `SYSTEM/backlog-queue/_review/` completion logs · `backlog-agent-runs.md` | morning (audit) · close-out (receipt liveness) | § Auditing · a missing receipt for an expected fire → **RULE** line *"expected fire absent — evidence, not a monitor"* |
| any session (DIR-019 §4 / DIR-021) | `SYSTEM/drift-ledger.md` § OPEN | close-out | each line re-probed; a derive whose stamp predates its source → **AUTO** retire-in-place (`superseded_by:`), move the line to § CLOSED with the ruling *auto-ratified* · channel/project **law** → **RULE** · already fixed → **PHANTOM** |
| any session (DIR-003) | `_OBSERVATIONS.md` entries with no triage stamp · `_BACKLOG.md` new items | close-out | **read only for the day's new entries** — stamping is `backlog-sweep`'s Step 4b and graduation is CRE's; the close-out folds nothing here. A new `_BACKLOG` item with no recorded next action → one `pending.md` line asking CRE to name one (E1 is never invented) |
| `DECISIONS/` | dated entries whose `review-date` has passed · `_WEIGHTS.md` proposals | close-out (Sun) | **RULE**, always — the ledger is never in class. One line per overdue review, age stated |
| `SCRATCHPAD/` (hand-drop, unrouted) | files, by name and mtime | close-out | **list, never open** — DIR-006 secret-scanning is the reading session's duty and this run does not read. Report count + oldest age in the receipt; a drop older than 7 days → one `pending.md` line *"route to INBOX or GRAVEYARD — your call"* (`_VAULT MAP`: stale notes route on CRE's call). Absorbs the *no server* half of `^backlog-scratchpad-no-server`; the Friday-prompt option stays his |
| every scheduled task | `SYSTEM/reports/<task>-runs.md` receipt logs | close-out (Sun) | per sweeper, one **evidence line** in the briefing § Health: receipt post-dates the window / does not / no receipt file. **Not a liveness monitor** — this is a scheduled task reading other scheduled tasks; `^backlog-scheduler-liveness-check` stays its own build |

**Not routed here, on purpose:** `INBOX` and the intake drop zones (`inbox-router` and the runners serve them; the Friday *Clear the intake gates* item is their sitting); `TASKS/TODAY.md` and the week block (`day-launch` / `week-shape`); anything under `WRITING/` (fiction gates defer to `open-loops.md` and the chapter's own pipeline). Routing those through here would make this skill a second router over surfaces that already have one.

**What "consume" means and does not mean.** Read the surface as written; research each finding against the tree; act on it at its bin. **Never re-derive** a sweeper's finding — if a report is missing or a count looks wrong, that is a finding about the sweeper (a `pending.md` line naming it), not a gap to fill by re-running the sweep.

## The auto-ratify class — CRE's standing yes

**Armed on CRE's word, not before.** The class is his ruling (2026-09-04) and it is written into DIR-012 as clause 6 by an attended landing — the proposal is [[SYSTEM/reports/2026-09-04-dir012-auto-ratify-proposal]]. **Degraded mode, stated first:** until `_DIRECTIVES.md` DIR-012 carries clause 6, every AUTO disposition below is written as a *proposed* line in `_rulings/pending.md` instead of executed, tagged `(would auto-ratify)`, so the sheet shows him exactly what the class would have done. The check is one pathed `Grep` for `auto-ratify` on `_DIRECTIVES.md` at the top of every close-out; the receipt says which state the run was in.

A recommendation is **in class** when **both** hold:

1. **Reversible** — the action is a **stamp** (`superseded_by:`, `PARKED`, `NOT A RULE`, a dated provenance or verification stamp), a **move** (file between folders, item between sections, verbatim archive to `SYSTEM/history/`), an **archive** (verbatim), a **rewrite-down** (an item's *Next:* reduced to what remains, or checked off with the evidence cited — replacement, with the original recoverable from `_CHANGELOG` or the dated archive), or a **fold** (bin lines into one bin or one sheet). **Never a delete.** Never a hard delete, never an emptied folder, never a rewrite that loses text no archive holds.
2. **Write surface limited to** `SYSTEM/**` · `_BACKLOG.md` (root + project shards) · `_OBSERVATIONS.md` (stamps and the run's own DIR-003 entries only) · `WORKFLOWS/*.md` canon docs · `WORKFLOWS/skills-src/**` sources.

**Never in class, whatever the recommendation says:** `WRITING/**`, any `REFERENCE/` canon, `_DIRECTIVES.md` / `SYSTEM/directives-reference.md`, `DECISIONS/`, `TASKS/TODAY.md`, any scheduled-task prompt or cadence change (create / enable / disable / re-time), the OS anchors (`_ME`, `_VAULT MAP`, `_SKILLS MAP`, `CLAUDE.md`), and **every fork** — a choice between designs, keep-or-cut, where a rule lives. A fork with an in-class surface is still a fork: sheet.

**How the class changes the eligibility tests.** It does not add a test; it removes a reason. Before v2 an item whose only missing input was CRE's *yes* — close this, stamp that, fold these — had to be ATTENDED because clause 1 forbade the yes. Now: **E2 closes the item itself** (check-off with the evidence, receipted), and **E6 reads "outside the agent's write surface *as widened by the class*."** The E6 list of surfaces stays exactly as it is — those are the never-in-class surfaces — so an item lands ATTENDED for the same reasons it always did, minus *"needs CRE to say yes to a reversible system write."* **Measure it:** every receipt reports `ATTENDED n / ruled m`; the baseline is 9/11 (pilot 1, 2026-09-04); the briefing trends it.

**Every auto-ratified action is visible.** Receipted with the one-clause reason it qualified, and listed on the week's rulings sheet under *Executed without you — reversible, spot check*. Reversible is not the same as invisible (DIR-012 cl. 4). Ten seconds of his eye on the list is the audit; the undo is one move.

## Observables — no observable, the item stays open

**Every served plan names its observable up front** — a `## Observable` section: *the one thing a stranger checks tomorrow, by path, to see the work held.* Not the completion conditions restated; the durable state those conditions were meant to produce. *"`WORKFLOWS/loop-clearer.md` stop condition 4 reads 'retired by stamp' — a pathed Grep returns 1 hit"*, not *"the edit was made."* A plan with no nameable observable is not a plan yet: research it further, split it, or rule it ATTENDED.

**The close-out re-probes it the next day before the item is closed.** The morning audit's PASS moves the plan to `_closed/` and **does not touch the `_BACKLOG` item**; the evening close-out reads the observable **against live state** — DIR-010 §5: a status field is never evidence of state; DIR-018: a check that passes on a proxy has not verified the thing — and only then checks the item off or rewrites it down. A re-probe that fails sends the plan back to `_served/` as the next fix round with the probe result quoted. **Probed, not proxied:** the probe reads the artifact the observable names, never the completion log, never the receipt, never the plan's own claim.

A plan's completion log echoes the observable and the agent's own first probe of it (§ [[WORKFLOWS/backlog-agent]] § The completion log), so the audit has two readings to compare and the close-out has a third.

## Candidate source — consume the Standing queue, never re-rank

**This skill computes no ranking of its own.** Two rankers over one backlog will disagree and neither will be trusted.

**Measure `_BACKLOG.md` before reading it (added 2026-09-04). This paragraph and the two branches below are the vault's shared slice-read protocol for every brain doc past the limit — `backlog-agent`, `sysadmin`, and every close-out step cite it rather than restating it.** The mechanics, once: `Grep -n` with an explicit `path` finds the line (it reads the whole file — 478 lines at 288.6 KB, so the length is in the lines, not the line count); `Read` by `offset` + `limit` pulls the bounded slice; an edit anchors on text from that slice and is verified by re-reading the same slice. Use `mcp__Desktop_Commander__get_file_info` (host route, DIR-020) to measure — a metadata call, never a read, never bash. **At ~256 KB the file tools stop returning the whole file and the truncation does not announce itself:** the call succeeds and returns a prefix. `_BACKLOG.md` measured **298.6 KB on 2026-09-04 — already past it** — and because this file is organized by lane rather than by date, a prefix hands back the conventions, § Standing queue and the gate bins while silently dropping most of the lane items the run is about to rule on. A run that reads whole and proceeds is indistinguishable from a run that worked, which is why an attended session found this and an unattended one would not have.

Over the **OVER-LIMIT** line (≥ 240 KB — `WORKFLOWS/log-rotate.md` § The hard line above the bands), take one of two branches and name it in the receipt:

1. **Slice deliberately.** § Standing queue sits near the top and survives a bounded offset read. Reach **each candidate item by targeted `Grep` plus an offset `Read`, one at a time** — never by pulling the file and hoping. The receipt records that the run worked from slices.
2. **Halt.** Cannot locate a candidate's item text by targeted read, or cannot measure the file at all → stop, write the receipt naming the file and its size, stand down. A halt with a receipt is a good run; a disposition ruled off a prefix is the bad one, and it looks identical to a good one from the outside.

The same rule binds Step 4a's `_CHANGELOG` read — that file measured **252.6 KB the same day**, days from the same wall.

Read `_BACKLOG.md` § **Standing queue (backlog-sweep YYYY-MM-DD)** and take its candidates in the order that block already states:

1. the **Ranked-3 attended serving**, in its order;
2. then the block's **"skipped, not served"** list, in the order it already ranks them (it states its own ordering rule and dates).

That is ~9 candidates without a single independent judgment about priority.

**Extending past the block: enumerate the band, or decline (`^obs-311`, added 2026-09-04).** A run that needs candidates past the end of that list applies **backlog-sweep's own recorded rule** — priority band `#p1`→`#p2`→`#p3`→untagged, oldest first within band by the item's anchor date, `#blocked`/`#waiting` excluded — and says so in the receipt as *extending the sweep's stated ordering*, never as a new ranking. **A forward scan from where the block stopped is not that rule and must not be presented as it.** `_BACKLOG.md` is not in date order, so reading downward from the block and taking the next plausible item cannot honour "oldest first" — pilot 1 did exactly that, took two 2026-08-24 items, and left a 2026-08-10 item of the same band unranked two sections up. Nothing was mis-served, and that is the point: the result looked defensible and was wrong on its own stated criterion, which is DIR-018's shape applied to a ranking rather than a check.

So an extension does one of two things, and the receipt says which:

1. **Enumerate.** Match the band on the item's **trailing tag run**, anchored — `#p2(?: #[a-z-]+)* \^[a-z0-9-]+` and its siblings — never a bare `#p2` string, which overcounts from prose the same way `^obs-250` / `^obs-254` document. Read each hit's anchor date from the item, sort oldest first, and **write the enumerated list into the run receipt** so the next run can check the order rather than re-derive it. Enumerate `_BACKLOG.md` **and the three project shards** § Project pointers names, since the sweep's rule spans all four.
2. **Decline, and say so.** A perfectly good outcome. The measured size is the reason to expect it: a 2026-09-04 probe returned **80-plus `#p2` trailing-tag runs in `_BACKLOG.md` alone**, before the shards, and anchors carry no dates — so a faithful sort is real work, not a line of grep. A run that will not do that work declines to extend, serves only what the block ranks, and records the decline. **What is forbidden is the third thing: extending without enumerating.**

A consequence worth stating in the receipt when it bites: once the block's candidates are all ruled ATTENDED or NOT-ELIGIBLE, a run that declines to extend has nothing to serve. That is a true and useful signal about where the backlog's debt sits, not a fault (§ Stop conditions).

**Freshness gate.** If § Standing queue is missing, or is older than `backlog-sweep`'s last recorded fire, **stand down and report**. Do not compute a ranking to fill the gap — that is the second-ranker failure this rule exists to prevent.

**The counts are approximate and this skill never repeats them as fact.** The block itself carries a DIR-018 note that its item count has no stable matcher across runs (`^obs-254`, `^backlog-queuetag-derivation` open). Cite the block, never re-derive a lane count, and never publish one.

## Eligibility — ruled per item, per run, reason recorded, and never written back as a tag

**This skill does not read queue tags to decide eligibility.** `^obs-250` deleted `#unattended` / `#unattended-confirm` after a string match reported six agent-lane items when two were real — four matched the tag string inside their *prose*, three of those in sentences recording the tag's own removal. `_BACKLOG.md` § Conventions forbids the revival by name, and the surviving `#desktop` tag is still inflatable the same way. So eligibility is ruled from the **item's content** — its recorded next action and what that action touches — read directly, per item, per run.

Note the corollary: `#gated` is the *default for an untagged item*, which means it records the **absence** of a ruling rather than a ruling. It is not a veto. Where CRE has genuinely ruled an item his — the item says so in words — that reads as ATTENDED below.

Every candidate gets exactly one disposition, with a one-clause reason, recorded in the run receipt and (for served items) in the plan:

| Disposition | Meaning |
|---|---|
| **UNATTENDED** | A cold agent can finish it in one session using only safe ops inside the write surface below. Plan served, agent-pickup allowed. |
| **ATTENDED** | Real work exists and can be planned, but finishing it needs CRE — a ruling, a creative call, his voice, a schedule change, or a desktop-only action. **At most one per run** gets a prepared plan, written to `_attended/`, marked `mode: attended`, **never** auto-picked-up (§ The attended lane). The rest get their disposition, their reason, and their rulings line (`_rulings/pending.md`). |
| **NOT-ELIGIBLE** | No plan this run. Reason recorded. |

**The ruling lives in the run receipt and the plan file only. Nothing is ever written back into `_BACKLOG.md` as a tag, a lane, or a status field.** That is both the `^obs-250` guard and the DIR-010 §5 guard in one.

### The tests, in order

Run these against each candidate; the first one that fires decides.

- **E1 — Is there a recorded next action?** `_BACKLOG` § Conventions requires an item to be *current state + next action + pointers*. No single recorded next action → **NOT-ELIGIBLE** (*"no recorded next action; needs CRE to name one"*). This is the same rule the sweep's serving uses when it skips an item, and it is the commonest skip.
- **E2 — Has it already been addressed?** Run the already-addressed check below. Already done → **NOT-ELIGIBLE** (*"already addressed, evidence: …"*), and **close it: check the item off with the evidence cited, in the same edit** — a check-off with evidence is a rewrite-down inside the auto-ratify class (§ The auto-ratify class), receipted, listed on the week's sheet as *executed, reversible — spot check*. Where the evidence is partial, or the closure would be *superseded* rather than *done*, it is not decisive: write the line to `_rulings/pending.md` instead. **Until DIR-012 clause 6 has landed, this stays a proposed line** (the class's degraded mode). *(v1 wording — "proposing, never closing" — superseded 2026-09-04.)*
- **E3 — Is it blocked or waiting?** Read the item and decide from its text, not a grep. Genuinely blocked on an external clock or an unmet precondition → **NOT-ELIGIBLE** (*"blocked on …"*).
- **E4 — Does finishing it require a fork ruling?** An unruled choice inside the item — which of two designs, whether to keep or cut, where a rule should live → **ATTENDED**, and name `decision-helper` as the route in the plan. Neither skill in this pair ever rules a fork. **First in line for the run's one prepared plan.**
- **E5 — Is it fiction execution?** Chapter drafting, prose generation, a register or canon pass, anything that authors CRE's words → **ATTENDED**. AI executes; CRE creates. **Prepared last and thinnest** — assemble context, name what is due, and stop there (§ The attended lane, thin prep).
- **E6 — Does the next action land outside the agent's write surface, as widened by the auto-ratify class?** Desktop-only (pack / Save-skill / install / git write-op / StoryLine UI / "Run now"), a scheduled-task prompt edit or any cadence change, `_DIRECTIVES` / the reference doc, an OS anchor, `DECISIONS/`, `TASKS/TODAY.md`, the week plan, `WRITING/**`, `REFERENCE/` → **ATTENDED**. **Second in line**, where the work is known and only the hands are missing — the plan becomes a checklist. **Not E6 (v2):** an action whose only missing input is CRE's *yes* to a reversible write on a class surface — a stamp, a fold, a rewrite-down, an archive, a canon-doc or `skills-src/` edit the item already specifies. That yes is standing (§ The auto-ratify class); the item goes on to E7. **Authoring a canon doc or a skill source unattended is in surface** when the plan names the exact path and the content is specified by the item — the pack/install that follows is a desktop trip queued on the weekly sheet, and until packed the doc runs from the trigger index (DIR-009), which is the degraded mode already in place.

- **E7 — Otherwise → UNATTENDED.** Compose the plan.

**"ATTENDED" means served, not stopped.** Earlier wording here read "plan-and-defer only" and three runs took it as *do not write a plan*: nine ATTENDED rulings produced zero attended plans, and the agent's attended mode — which was fully built — had nothing to read. Ruling ATTENDED now means *this item's plan goes to `_attended/` rather than `_served/`*, subject to the one-per-run rule and the cap. Deferring is what happens to the items past the first, and it is recorded, not silent.

**An E6 sharpening from the pilot.** An item with one in-surface leg and one out-of-surface leg is only splittable when the legs are genuinely **independent**. Where DIR-016 binds them — a canon doc *and* its live task prompt must change in the same session — serving the doc half alone would ship a route updated on one surface of two, which DIR-016 names the most expensive failure shape available, because the record then says it works. Rule the whole item ATTENDED instead. (`^backlog-taskaudit-gatebin` is the worked example: leg (b) is a clean `WORKFLOWS/task-audit.md` edit, and it is still not servable.)

An item can be ATTENDED on one run and UNATTENDED on a later one — a fork ruled, a desktop trip made — which is precisely why the ruling is per run and lives nowhere durable.

### The already-addressed check (E2)

All three surfaces, because a single surface has repeatedly been wrong here:

1. **`_CHANGELOG.md`** — entries since the item's anchor date, **read in full**. Summaries lie; `backlog-sweep` § Step 3b established reading before counting. **Measure first, though.** At **252.6 KB on 2026-09-04** this file is days from the read limit, past which a whole-file read returns a prefix and says nothing. It is newest-first, so a prefix returns the *recent* entries this check wants — the failure is gentle here, but that is luck about file ordering, not a property anyone verified. Read the date range you need **by explicit offset**, and say so, rather than pulling the file and trusting what comes back.
2. **`SYSTEM/reports/`** — any dated report naming the item's anchor or its deliverable.
3. **`SYSTEM/backlog-queue/_closed/`** — a prior closed plan for the same anchor, and its verdict.

Then the **wording-vs-state check** (`backlog-sweep` § Step 4b check 3): where the item names a checkable artifact — a file, a doc section, a skill, a task — read the artifact and test the item's own wording against it. An item that says "packaging pending" is a snapshot nothing re-checks.

Two hard constraints on a negative:

- **Read the artifact to EOF before concluding a claimed edit did not land** (`^obs-247`). A partial write looks exactly like a non-write from the middle of a file. Anything less reports *"state unconfirmed — partial read,"* never a confident negative.
- **A `Glob` miss is never evidence of absence** (DIR-005). Confirm every load-bearing negative with a pathed `Grep` or a direct `Read`. Every `Glob`/`Grep` against vault content passes an explicit `path` — unpathed, they search the Cowork outputs scratch and return a clean "No files found" with no warning.

## Composing a session plan — the artifact that makes this work

A plan is written for a **cold agent with no memory of this session and no access to CRE**. The test it must pass: *could a stranger finish this without asking a question?* If not, it is not a plan yet — either research it further or rule the item ATTENDED.

### Verify the plan before serving it (`^obs-313`, added 2026-09-04)

Three supervisor/agent rounds produced three defects and **all three were in the plan, never the execution** — each caught only because the agent departed from its instructions and said so. That is not a check; it is a courtesy the loop cannot rely on once the cadence is armed and no one reads a plan before it ships. The root cause is structural: this skill writes the instructions *and* the pass/fail conditions from one research pass, so a misreading propagates into both halves at once and nothing disagrees with it.

Three rules, each from a real defect:

1. **Every claim the plan makes about a target doc's behavior is verified by direct read of that doc** — never carried from the backlog item's summary, and never inferred from the doc's name or its `_SKILLS MAP` row. The worked case: a plan told the agent that a `canon-sync` contradiction with an older `REFERENCE` row *"is a supersession, not a conflict to gate."* Read flat, that overrides principle 4's contradiction gate and principle 7's `binding_surface: true` write-time debt accounting — the latter derived from DIR-010 §4, **which DIR-019's own closing sentence says it does not repeal.** The claim came from the backlog item's one-line framing; two minutes in `canon-sync.md` would have caught it. Where a plan asserts what a doc does, the plan cites the section it read.
2. **The write surface always names the agent's own run receipt**, `SYSTEM/reports/backlog-agent-runs.md`. The agent's skill requires it unconditionally on every fire, so a surface that omits it forces a conflict between the plan and the agent's own contract — and the agent is right either way, which makes the audit a judgment call. This is the same class as the condition-vs-Defer contradiction below: **a plan must not contradict a rule the agent is separately bound by.** Check the surface against the agent's skill, not only against the job.
3. **Mark which claims are transcribed and which are inferred.** A cold agent cannot tell a quoted rule from the supervisor's paraphrase of one, so it treats both as given. Quote what is quoted; where the plan is summarizing or reasoning, say so in the sentence, and the agent knows which claims to check against the source before acting on them.

**The general form:** the existing rule *"check your conditions against your own Defer section"* catches only defects internal to the plan. Defects 2 and 3 were the plan being wrong about something **outside itself** — the agent's contract, and a target doc's live rules. Both directions need checking.

**When a served plan turns out to be wrong, the plan is the defect, not the agent** (§ Auditing a completion log). An agent that follows an instruction its plan gave it audits to a PASS; an agent that spots a bad instruction, scopes around it, and flags the departure audits to a PASS and gets its scoping ruled on. Never fail an agent for either.

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
- **## Write surface for this plan** — the exact paths this session may write, and nothing else. Everything not named here defers. A path inside the auto-ratify class surface may be named here without CRE's per-item yes; a never-in-class path may not be named at all.
- **## Observable** — **required (v2).** The one durable state a stranger checks tomorrow, by path and condition, to see the work held (§ Observables). The agent probes it once at the end of its run and records the reading in the log; the close-out re-probes it the next evening before the `_BACKLOG` item is closed. A plan that cannot name one is not served.
- **## Completion conditions** — objective, checkable statements. *"`SYSTEM/reports/2026-09-04-approval-gated-openers.md` exists and lists every one of the 14 registered task prompts with a flag or a clear."* Not *"the sweep is done."* These are what the audit reads; a vague condition makes the audit a judgment call, which is the one thing this loop cannot afford. **Check the conditions against this plan's own Defer section before serving** — a condition that forbids what the Defer rule authorizes is a self-contradicting plan, and the agent will be right whichever way it goes.
- **## Defer instead of guessing** — the named cases where this job should stop and defer rather than proceed, each with what to write in the completion log.
- **## Out of scope** — the adjacent work this session must not do.

**Serve at most 3 plans per run**, and never let `_served/` + `_working/` + `_review/` exceed **5 open plans** in total. Bounded output is house discipline (`backlog-sweep` caps graduations at 5, `sysadmin` at 12, `day-launch` at 7): an unbounded queue is one nobody works. `_attended/` is **not** counted against that 5 — it carries its own budget below.

## The attended lane (added 2026-09-04, CRE-ruled off `SYSTEM/reports/2026-09-04-attended-lane-spec.md`)

An ATTENDED disposition names an item as CRE's. The **attended plan** is what makes his sitting cheap: the research already done, the specific ruling he owes stated in one sentence, the options laid out. The weekly sheet tells him *which* items are his; the plan is what stops each one costing an hour of re-derivation.

**Where it goes.** `SYSTEM/backlog-queue/_attended/`, never `_served/`. `mode` and folder must agree. `backlog-agent` reads that folder only on **"work the backlog with me"**, shows CRE the list, and moves his pick **straight to `_working/`**, from where it rejoins the normal path and is audited by Step 2 like anything else. An unattended run never reads the folder.

**Budget — separate, because the lanes drain on different clocks.** At most **one** attended plan written per run; at most **3** open in `_attended/`. An unattended plan clears within a day (picked up 12:29, audited 08:22); an attended one clears when CRE sits down, which may be a week. Under one shared cap the slow lane starves the fast one — and a typical run rules nine ATTENDED against one or two UNATTENDED, so a single budget would fill on the first run and stop the cadence doing anything. At cap, ATTENDED items still get their disposition, their reason, and their rulings line (`_rulings/pending.md`): nothing is lost, only unprepared.

**Which one gets prepared.** The one where preparation changes the most. First match wins:

1. **E4, a fork to rule.** Highest return: the plan researches it, states what the tree already answers, and lays out the options so the sitting is a ratify rather than a deliberation (DIR-011, and CRE's standing rule that a settled call stays settled — present a tree-answered item as *"resolved against X — confirm"*).
2. **E6, out-of-surface but fully specified.** A desktop trip or a prompt edit where the work is known and only the hands are missing. The plan becomes a checklist he executes.
3. **E5, fiction — thin prep only (CRE-ruled 2026-09-04).** Assemble the context, name what the chapter is owed, stop. **Never draft, never propose prose, never shape a story decision.** Preparation is administrative; generation is his. The organic-process guard is about generation, which is why thin prep is allowed at all.

**Never prepared:** E1 (no recorded next action — there is nothing to prepare, and inventing one is the organic-process violation), E2 and E3 (already addressed, or blocked). These get a rulings line and nothing else.

**Sections — the unattended shape, re-aimed at a sitting.** Keep `## The item`, `## The job`, `## Why`, `## References`, `## Steps`, `## Out of scope`, and `## Defer instead of guessing` (re-aimed: where the sitting should stop and re-plan rather than push through). Replace and add:

- **## The ruling you need to give** — replaces `## Completion conditions`. The decision in one sentence, in CRE's vocabulary, options with a recommended default. Tree-answered → *"resolved against X — confirm."*
- **## What I already checked** — the research, so the sitting does not re-derive it. Every claim about a doc cited to the section read (§ Verify the plan before serving it).
- **## What happens after you rule** — whether the remainder becomes agent-executable, and therefore gets an unattended plan next run, or stays his end to end. This is the line that keeps an attended sitting from becoming an attended project.
- **## Time** — an honest estimate. A sitting he can size is a sitting he will start.

**Aging, so the folder cannot rot quietly (CRE-ruled 2026-09-04).** Every run reports `_attended/` in its receipt with an age per plan, and folds **one line** into `_rulings/pending.md` — how many wait, and the oldest one's age. Not a per-plan nag. At **21 days** unworked, stop re-preparing that item and write one rulings line proposing CRE drop it or rule it his-only-forever. A prepared sitting nobody works for three weeks is evidence about the item's real priority, and saying so is better than letting the folder fill. This is also the lane's degraded mode stated up front, per CRE's standing rule that a step waiting on him remembering it does not happen: if he never sits down, the lane reports that plainly and stops growing.

## Auditing a completion log

For each `SYSTEM/backlog-queue/_review/<...>.log-rN.md`, read the log **and the artifacts it claims**, then rule:

- **PASS** — every completion condition is met, verified against the artifact itself rather than the log's claim about it (DIR-018: a check that passes on a proxy has not verified the thing). Move the plan and all its logs to `_closed/`. **Do not touch the `_BACKLOG` item yet (v2).** The item is checked off or rewritten down by the **close-out** after it re-probes the plan's observable against live state the next evening (§ Observables) — a PASS is the audit's reading of the artifact on the morning after; the close-out's is a second, later reading, and only then is the item closed. The audit's own probe of the observable goes in the receipt so the close-out has it to compare against. *(v1 closed the item at PASS; superseded 2026-09-04 — no observable, the item stays open.)*
- **PARTIAL / FAIL** — write a **fix prompt** to `_served/<date>-<anchor>.md` at `round: N+1`, naming the specific mistakes and missteps: which condition is unmet, what the log claimed versus what the artifact shows, what to do differently. A fix prompt that says "try again" is not a fix prompt. Move the plan and logs back to `_served/` alongside it.
**Reconcile duplicates first.** If the same anchor appears in more than one queue folder, the agent's seat had no delete primitive and copied forward instead of moving (the 2026-09-04 pilot's finding). Resolve to the **furthest-along copy** in `_served/` → `_working/` → `_review/` → `_closed/` order, audit that one, and clear the stale copies with the host route. This is a safe op, not a finding to gate.

**When a completion condition and the plan's own Defer rule conflict, the plan is the defect, not the agent.** The pilot's condition 3 demanded one of three verdicts for every task while its Defer section authorized a fourth (`UNREAD`) for unreadable inputs; the agent followed the Defer rule and said so. That is correct behavior and audits to a pass — record the plan defect so the next plan does not repeat it, and never fail an agent for obeying an instruction the plan gave it.

- **DEFERRED-BY-AGENT** — the log says the agent stopped and deferred with a reason. Not a failure. Either re-plan around the obstacle (a new round 1, if the obstacle is something the plan should have covered) or rule the item ATTENDED and route the reason to `_rulings/pending.md`.

**Cap the loop at two fix rounds.** Round 1 is the initial plan; rounds 2 and 3 are the two fixes. A fail at round 3 **escalates**: move everything to `_closed/` with a terminal `ESCALATED` note, rewrite the `_BACKLOG` item's **Next:** to name both logs by path, and add a line to `_rulings/pending.md`. The item goes back to CRE having been worked, with the record of what was tried attached.

## Escalation and deferral — one channel, the weekly sheet

**v2 (2026-09-04): this skill no longer writes a `## Needs CRE ruling (backlog-supervisor …)` bin in `_BACKLOG.md`.** Every deferral, escalation, NOT-ELIGIBLE-worth-knowing, and every CRE-only call the intake walk finds goes to **`SYSTEM/backlog-queue/_rulings/pending.md`** — one line each, in the one-tap form: *the item · the proposed action with a recommended default · the one-clause reason · what it costs to defer*. Tree-answered → *"resolved against [[X]] — confirm."* On Sunday the close-out compiles `pending.md` into the week's sheet (§ The weekly sheet and the briefing), which [[WORKFLOWS/sysadmin]] walks and nothing else does.

This is DIR-012 clauses 4 and 5 with one channel instead of two. The v1 bin and the Monday admin pass were two attended channels for the same deferrals, which recreated the dispersal `sysadmin` was built to fix. The surviving `## Needs CRE ruling (backlog-supervisor 2026-09-04)` bin in `_BACKLOG.md` is **folded into the first weekly sheet by the first Sunday close-out** and stamped `superseded_by:` in place; sweepers other than this skill keep writing their own bins, and § Intake is how those bins are read.

## Steps — morning fire (`mode: morning`, plan/serve)

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`) with the file tools. Mismatch → halt, write the receipt, report (`^obs-004`). Then one pathed `Grep` for `auto-ratify` on `_DIRECTIVES.md` — records whether the class is armed (§ The auto-ratify class); the receipt says which.

### Step 1 — Cheapest work-check first (DIR-008 cl. 2)
Before reading anything expensive, enumerate and count the four **pipeline** folders: `_review/`, `_served/`, `_working/`, `_closed/`. **`_attended/` is a fifth folder in this tree and is not part of this count** — it is CRE-paced, sits outside the 5-open cap, and has its own budget (§ The attended lane); the cheapest-work-check must not grow to cover a lane an unattended run cannot serve. Branch:

- **`_review/` non-empty** → there are audits to run. Continue (audits come first, always).
- **`_review/` empty and `_served/` + `_working/` at the 5-plan cap** → nothing to audit, no room to serve. **Stand down**: write the receipt, end the run. No `_BACKLOG` read, no plan composition.
- **Otherwise** → continue to serving.

The early-exit accounts for pending queue state, not just new arrivals — a served-but-unworked plan is work in flight, and treating an empty `_review/` as "nothing to do" would strand the queue (`^obs-166`, the file-inbox bug).

### Step 2 — Audit everything in `_review/`
Per § Auditing above. Move plans, write fix prompts, update `_BACKLOG` items for passes. Do this before serving so a fix prompt is in `_served/` for the same day's agent run.

### Step 3 — Load candidates
**First, `SYSTEM/backlog-queue/_intake/`** — findings the close-out routed as AGENT work, one file each, already researched and carrying a proposed job. These are not `_BACKLOG` items and consuming them is not ranking: they are the sweepers' own findings translated. Take them oldest first; a plan composed from one names the source report in `## The item` and moves the intake file into the plan's folder beside it. Then read `_BACKLOG.md` § Standing queue. Apply the freshness gate. Take candidates in the order the block states (§ Candidate source). Read each candidate item in full from `_BACKLOG.md` or its project shard, **by slice** (§ Candidate source — measure, then `Grep -n` + offset `Read`). **Past the end of the block: enumerate the next band on its anchored trailing tag run and write the sorted list into the receipt, or decline to extend and say so — never a forward scan** (§ Candidate source, `^obs-311`).

### Step 4 — Rule eligibility per candidate
Run E1–E7 in order. Record every disposition and reason. Stop composing **unattended** plans once 3 are written or the 5-open working set is hit; stop composing **attended** plans after the first, or if `_attended/` already holds 3 (§ The attended lane — separate budgets).

### Step 5 — Compose and serve
Write each unattended plan to `_served/` and the run's one attended plan, if any, to `_attended/` (§ The attended lane — selection, sections, cap). **Before serving, run the three verification rules** (§ Verify the plan before serving it): every claim about a target doc's behavior confirmed by direct read of that doc and cited to the section read · the write surface naming `SYSTEM/reports/backlog-agent-runs.md`, the agent's unconditional receipt · transcribed claims marked apart from inferred ones. Then re-read each written plan through the file tools and confirm the frontmatter parses and every required section is present (DIR-004, DIR-005).

### Step 6 — Rulings lines
Append this run's escalations, deferrals, and CRE-only dispositions to `SYSTEM/backlog-queue/_rulings/pending.md` in the one-tap form (§ Escalation and deferral) — targeted file-tool edit, re-read to confirm. Include **one** line for `_attended/` — how many prepared sittings wait and the oldest one's age — plus a line per item that has crossed 21 days, proposing it be dropped or ruled CRE-only-forever. *(v1 wrote a `_BACKLOG` gate bin here; superseded 2026-09-04.)*

### Step 7 — Receipt, unconditionally
Append one line (newest-first) to `SYSTEM/reports/backlog-supervisor-runs.md` **every fire, including a stand-down and including a halt**: date, **mode (`MORNING` / `CLOSE-OUT`)**, counts audited / passed / failed / escalated / served (**unattended and attended counted separately**), dispositions ruled **with the ratio `ATTENDED n / ruled m`**, whether the auto-ratify class was armed, the contents of `_attended/` with an age per plan, the observable each PASS was probed against and the reading, and any substrate fallback taken. Create the file if absent.

This is not optional and not conditional. `^backlog-scheduler-liveness-check` is open precisely because every task writes a receipt when it runs and nothing writes anything when it doesn't, so six days of scheduler silence (2026-08-26 → 09-01) produced no signal at all. A stand-down line is the most valuable line this file carries.

### Step 8 — Log (DIR-003)
A run that changed the vault gets a `_CHANGELOG.md` top-insert (meta lane). New fragility → `_OBSERVATIONS.md` with a `^obs-NNN` anchor, re-scanning for the highest anchor immediately before the write and re-reading the heading after (`^obs-236`). Follow-ups → `_BACKLOG.md`. A stand-down run is trivial: receipt only, no changelog entry.

## Steps — evening fire (`mode: close-out`)

Audit the day's work and activity, close superseded and finished items, keep the bins current, reduce false positives. **Never serves a plan.** Runs at 20:20 so it sits after the agent (12:29) and, on Sundays, after the whole maintenance window (`link-audit` 16:21, `week-shape-runner` 18:00).

### Step C0 — Vault sentinel + class check
As Step 0. Record armed / not armed.

### Step C1 — Cheapest work-check first
Enumerate, via the host route: `_closed/` plans with no `.probe.md` beside them (re-probes owed) · `_review/` (logs that arrived after the morning — audited **tomorrow morning**, never here; counted only) · `_intake/` and `_rulings/pending.md` sizes · the mtime of every § Intake surface against the last close-out receipt's timestamp. **Nothing owed on any of those and it is not Sunday → stand down**, receipt, end. A Sunday always continues to Step C4.

### Step C2 — Re-probe yesterday's closes (§ Observables)
For each `_closed/` plan with no probe record: read the plan's `## Observable`, **probe the named artifact against live state** — file tools for vault paths, host route for anything outside the connected folder — and write `_closed/<plan>.probe.md` recording the reading, the timestamp, and PASS / FAIL. Then:
- **PASS** → now close the `_BACKLOG` item: check it off with the evidence if the plan discharged the whole item, else rewrite its **Next:** down to what remains — targeted file-tool edit on the sliced item, verified by re-read. In class (a rewrite-down), receipted, listed on the sheet.
- **FAIL** → the work did not hold. Write a fix prompt to `_served/` at `round: N+1` quoting the probe (*"observable X read Y at 20:2x; expected Z"*), move the plan and logs back beside it. Round 3 fails escalate as in § Auditing. The item stays open — no observable, no close.
- **Plan has no `## Observable`** (a v1 plan) → probe its completion conditions instead, say so in the probe record, and note the plan as pre-v2 in the receipt. Never close on the log alone.

### Step C3 — Walk the intake table
For every § Intake row whose surface has changed since the last close-out (mtime, or a new dated file), read what is new — by slice on the brain docs — and for each finding research it against the tree (DIR-011: `DECISIONS/`, `_CHANGELOG` since the finding's date by offset, `SYSTEM/reports/`, `_closed/`, the artifact it names read to EOF) and dispose:

- **AUTO** — in class and armed → execute now (stamp, move, archive, rewrite-down, fold), re-read, receipt with the qualifying reason, add to the sheet's *executed — spot check* list. Not armed → write the line to `pending.md` tagged `(would auto-ratify)`.
- **AGENT** — needs a session but no ruling → one file in `_intake/<date>-<slug>.md`: source, finding, research done, proposed job, proposed observable. The morning fire plans it.
- **RULE** — tree-silent and CRE's (a fork, a priority, a graduation, a cadence, a prompt edit, a desktop trip, anything on a never-in-class surface) → one line in `pending.md`, one-tap form, with the research attached so the sitting does not re-derive it.
- **PHANTOM** — the finding is wrong: a dangling link whose target a direct `Read` finds, a drift computed off a stale partial, a "missing" file the mount could not enumerate (`^obs-183`, `^obs-198`). Retire it in place (the sweeper's own line stamped `PHANTOM <date> — <mechanism>`), and **count it per source** — this count is the false-positive observable the briefing trends (U4 in the plan).
- **ALREADY-ADDRESSED** — live state has satisfied it since it was written → stamp `superseded_by:` in place, count it per source alongside PHANTOM.

**Close superseded and finished items** as they are found: an open `_BACKLOG` item whose deliverable `_CHANGELOG` names shipped with artifacts (the sweep's Step 3b DECISIVE rule) closes here on the same evidence bar — decisive only; partial evidence is a `pending.md` line, never a guess. Fold: where two sources report one defect, one line, both cited. Every write in this step is a targeted file-tool edit, re-read.

### Step C4 — Sunday leg: the weekly sheet + the briefing
See § The weekly sheet and the briefing. Skipped on other days.

### Step C5 — Receipt, unconditionally
As Step 7, `mode: CLOSE-OUT`, plus: re-probes run / passed / failed, items closed, AUTO executed (or proposed, if unarmed), AGENT routed, RULE lines written, PHANTOM + ALREADY-ADDRESSED counts **per source**, `pending.md` line count, and on Sunday the sheet and briefing paths.

### Step C6 — Log (DIR-003)
As Step 8. A stand-down is receipt-only.

## The weekly sheet and the briefing — the Sunday close-out leg

**One sitting a week. Cleared, not capped** (CRE-ruled 2026-09-04: a cap creates a snowball; `sysadmin`'s 12-item cap and 20-minute box are superseded. If a week proves overwhelming, a cap is his to add later — the briefing reports the sheet's length so he can see it coming).

**The sheet** — `SYSTEM/backlog-queue/_rulings/<YYYY-MM-DD>-rulings.md`, dated the Sunday it is compiled, frontmatter serialized (DIR-004). Compiled from `pending.md` (then emptied — its lines now live on the sheet), the carried-forward unruled lines of last week's sheet (each **re-probed against its own stated condition** before re-emission, per `backlog-sweep` Step 4b check 4 — a bin line is live state too, and one that fails its probe is dropped with a note), and the Sunday window's fresh findings from Step C3. Sections, in this order:

1. **Confirm in one tap** — the BATCH block: every line resolved against the tree (*"resolved against [[X]] — confirm"*), every AUTO action that was executed this week (*executed, reversible — spot check*: path, what changed, how to undo), and — while the class is unarmed — every `(would auto-ratify)` line. One decision for the block. Count shown.
2. **Rule** — the genuine calls, one at a time, each: the finding · the proposed action **with a recommended default** · the one-clause reason · what it costs to defer · the research (cited to the section read). Forks route to `decision-helper` with the evidence attached and appear here as *"fork — take to decision-helper, or rule inline: A (default) / B."*
3. **Desktop trips** — a checklist, not a list of problems: every pack / Save-skill / install / carve / prompt edit, in the order that shares a trip, each with the drafted body or command and its verification step. A prompt edit line links the report carrying the drafted prompt body (DIR-005: the system drafts, a human lands).
4. **Fiction, thin** — what a chapter or episode is owed, in one line each, context assembled, nothing proposed (E5).
5. **Carried** — anything CRE did not rule last week, with age. The sheet is walked to zero; what he skips carries with its age, and at three weeks a line proposes drop-or-his-forever, same as the `_attended/` rule.

**The briefing** — `SYSTEM/reports/<YYYY-MM-DD>-vault-briefing.md`, plain speech, four sections and nothing else. **System state only — never a word about CRE's patterns, output, or pace** (DIR-015).

- **Working** — what ran this week and held: fires expected / fires receipted per task, plans served / worked / passed / re-probed, items closed, AUTO actions executed.
- **In development** — what the system is building or changing in itself: open `_intake/` work, plans in flight, canon docs authored and awaiting their desktop pack, the milestones of any live meta project.
- **Needs ruling** — the sheet's length by section, the oldest carried line's age, the one call the system would put first if he only rules one.
- **Health** — the trend lines: `ATTENDED n / ruled m` this week against the 9/11 baseline · PHANTOM + ALREADY-ADDRESSED per source (false positives) · brain-doc sizes against the bands · receipts present / absent per scheduled task (evidence, not a monitor) · queue folder counts · whether the behavioral week was met: *his only system-facing sitting was the sheet, every item pre-researched with a one-tap form, every closed item re-probed*.

**The seed** — one line in `TASKS/TASKS.md` § Inbox, **replaced not stacked**, beside the Standing-queue seed (U3 default: beside, one line each): the existing `every:mon` item *Rule the week's system sheet* re-pointed at this week's sheet and briefing paths. The briefing is served, never fetched — a step that waits on him remembering it does not happen. `TASKS.md` § Inbox recurring items are in the class surface for this one edit only; § This week and `TODAY.md` are never touched.

**Who walks it.** [[WORKFLOWS/sysadmin]], attended, Monday — the sheet and nothing else. Ruled lines are executed by that sitting; the sheet moves to `_rulings/closed/` stamped with the date walked; unruled lines carry into next Sunday's sheet with age.

## Substrate (DIR-020)

The mechanical steps are enumerating the queue folders, measuring the brain docs, listing `SCRATCHPAD/`, reading the intake reports, and moving plans. **This workflow never requires `bash`.**

1. **Preferred — the host route**: `mcp__Desktop_Commander__list_directory` / `move_file` (or `windows-cli`) against the real Dropbox folder. Better, not degraded: it reads the actual folder, so the mount-staleness caveat DIR-005 exists for does not apply, and it is the only route with a true atomic move. It is also the **only** route that can read a scheduled-task prompt — `C:\Users\Chad\Claude\Scheduled\` sits outside the file tools' connected folders. `mcp__workspace__bash` is currently denied on scheduled seats (`^obs-281`, `^obs-284`) and has already halted `skills-sweep` outright.
2. **Fallback — the file tools**: `Glob` with an explicit `path`, and **every empty result confirmed by a direct `Read` of that folder's `README.md`** before it is treated as an empty folder. A `Glob` miss is not evidence of absence.

A denial on route 1 is an expected branch, not an error: fall through, and name the fallback in the receipt. Never reach for `bash` at any tier.

## Stop conditions

- **Vault sentinel fails** → halt, receipt, report. Never edit.
- **§ Standing queue missing or stale** → stand down, receipt, report. Never compute a ranking to fill the gap.
- **The file tools cannot write `_BACKLOG.md`** → halt, receipt, report. Never fall back to `patch_vault_file` or a whole-file MCP rewrite; both have silently truncated canon here (DIR-005).
- **`_BACKLOG.md` is over the read limit and a candidate's item text cannot be reached by targeted read** → halt, receipt naming the file and its measured size, stand down. Never rule a disposition off a prefix — the run would look successful and be wrong.
- **No route available to measure a brain doc's size** → halt and say so. Reading blind to find out is the exact failure the gate exists to prevent.
- **Working set at cap with an empty `_review/`** → stand down (this is normal, not a fault).
- **`_attended/` at its cap of 3** → write no attended plan this run; ATTENDED items still get their disposition and their rulings line (`_rulings/pending.md`). Not a fault, and never a reason to skip the unattended lane, which has its own budget.
- **The block is exhausted and this run will not enumerate the next band** → serve nothing beyond the block, record the decline and the reason in the receipt, and stand down if that leaves nothing. Declining is authorized; extending without enumerating is not (§ Candidate source).
- **`bash` is the only route left for a mechanical step** → this workflow is bash-blocked by declaration: report the step as unrun rather than attempting it.
- **No candidate is eligible** → that is a valid, informative run. Receipt it with the dispositions, and if several runs in a row rule everything ATTENDED, say so plainly on the sheet: it means the backlog's remaining debt is genuinely CRE's, which is a finding, not a failure. (v1 hit this state and called it "surface exhausted"; the difference is that this run can say *why*, item by item.)
- **A plan has no nameable observable** → do not serve it. Research further, split, or rule ATTENDED.
- **A re-probe cannot reach the artifact** (host route denied, file unreadable, path outside every reachable substrate) → the item stays open, probe record says `UNREACHABLE` with the route tried, one `pending.md` line. Never close on the log.
- **The auto-ratify class is not armed** (`_DIRECTIVES.md` DIR-012 carries no clause 6) → every AUTO disposition is written as a `(would auto-ratify)` line, nothing executed under the class. Not a fault — the degraded mode, stated in § The auto-ratify class.
- **A close-out finds a fork, a fiction call, a cadence, a prompt, a directive, a decision, or an anchor in its path** → RULE line, never AUTO, whatever the write surface.
- **Close-out on a non-Sunday with nothing owed** → stand down, receipt. Normal.
- **A sweeper's expected report is absent on a Sunday** → do not re-run the sweep; one RULE line *"expected fire absent"*, and the briefing § Health says which. Consume, never re-derive.

## Logging

Receipt every fire (Step 7). `_CHANGELOG` / `_OBSERVATIONS` / `_BACKLOG` per DIR-003 on any run that changed the vault. All OS-doc edits via targeted file-tool edits, each verified by re-reading through the file tools (DIR-005) — never `patch_vault_file`, never a bash read to verify.

## What this is NOT

- **Not `backlog-sweep`.** The sweep owns maintenance, archival, dedupe, observation graduation, and the Standing queue computation. This skill never archives, never dedupes, never graduates an observation, and never computes the ranking — it consumes it.
- **Not a re-ranker.** It has no ordering of its own and refuses to invent one.
- **Not `sysadmin`.** That pass is the attended sitting that walks the weekly sheet and rules what survives the auto-ratify class. This skill *compiles* the sheet; it never rules a line on it.
- **Not the sweepers.** It consumes their reports and bins; it never re-runs a sweep, re-derives a count, re-scans for links, or computes the Standing queue. A missing report is a finding about the sweeper, not a gap to fill.
- **Not a directive editor.** It proposes amendments into `SYSTEM/reports/`; both directive files are never in its write surface, armed or not.
- **Not `decision-helper`.** A fork inside an item routes there or to CRE. Neither skill in this pair rules one.
- **Not `day-launch` or `week-shape`.** It never writes `TASKS/TODAY.md` or the week plan.
- **Not `task-control`.** It never pauses, resumes, creates, or edits a scheduled task.
- **Not a fiction executor.** No chapter drafting, no prose generation, no register or canon pass. Fiction items are plan-and-defer only.
- **Not a scheduler liveness monitor.** It writes the receipts that make liveness checkable, and the Sunday briefing reports receipts present or absent per task as **evidence** — but it cannot detect its own absence and must never be relied on for that. The monitor for `^backlog-scheduler-liveness-check` has to be something that does not depend on the process it watches, which this does.
- **Not a reporter on CRE.** The briefing is the system's assessment of itself. Nothing in it names a pattern, a pace, or a stall of his (DIR-015).

## Packaging

Source at `WORKFLOWS/skills-src/backlog-supervisor/`. Per DIR-009: author via the file tools → pack on the **desktop** with `WORKFLOWS/git-bridge/pack-skills.ps1` → sha-verify packaged bytes against source → Save-skill. Never sandbox packaging (`^obs-156`). The description is single-quoted: it contains `#` and `: `, and an unquoted `#` opens a YAML comment that the installer silently truncates at (`^obs-299`).
