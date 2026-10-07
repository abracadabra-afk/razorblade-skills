---
type: workflow
name: reminders
trigger: push my reminders
aliases: [remind me, send this as a reminder, push the reminders, sync my reminders, nudge me]
inputs: [time-bearing open tasks in TASKS/TASKS.md (a date/time or "remind me")]
outputs: [scheduled ntfy push notifications on CRE's phone, the source vault line stamped `<!-- nudge: <id> -->`, a short run report]
lane: os
status: active
created: 2026-10-06
supersedes: WORKFLOWS/odysseus-tasks.md
---

# WORKFLOW: reminders

## When to use
CRE has **time-bearing** to-dos in [[TASKS/TASKS|Tasks]] — anything that should tap him on the shoulder ("call the dentist Tuesday 5pm"). Markdown can't notify; ntfy can. Triggers: **"push my reminders"** (batch) or **"remind me …"** / "send this as a reminder" (single). day-launch uses the same helper for its standard nudges (see [[WORKFLOWS/day-launch]] step 6).

**Why ntfy (CRE-ruled 2026-10-06, `DECISIONS/_QUICK LOG.md`):** Odysseus was retired — CRE didn't use it, and its reminder layer had silently not armed since 2026-09-07 (`^obs-335`). ntfy already runs on aegis-moon, already delivers the aegis-health alerts to CRE's phone, and is watched by the health probe. Calendar *events* are not reminders: they live in Nextcloud Calendar per dec-007.

## The helper — `WORKFLOWS/reminders/nudge.py`
```
nudge send --at "tomorrow 5pm" --id dentist-2026-10-07 --title "Dentist" "Call to confirm the cleaning"
nudge list
nudge cancel dentist-2026-10-07
```
- **Topic `cre-reminders`** on `https://aegis-moon.taild6b761.ts.net:8445` — tailnet-only, no auth, no credential anywhere (DIR-001). CRE's phone subscribes once in the ntfy app.
- **Time is parsed locally** (GNU `date -d`, the seat's timezone) into a unix timestamp. Never hand the server a natural-language time — it would parse in the container's timezone, which is how Odysseus fired reminders 7 h early (2026-07-22, DIR-013 cl. 1).
- **`--id` = ntfy sequence id → idempotent.** Re-sending an id *replaces* the scheduled message (verified 2026-10-06: the server holds one message, not two). This is what the old `<!-- ody: … -->` stamp did.
- **≤ 3 days ahead** (ntfy's hold limit). Further-out items stay in Tasks and are armed on the day (day-launch's morning pass does this).
- **Push-only.** ntfy has no done state — completion evidence stays in the vault (checked lines, `_CHANGELOG`).
- **No click link by default.** An `obsidian://` default was tried 2026-10-06 and on CRE's phone the tap landed on an unrelated third-party site (cloudstreamlink.com) instead of Obsidian — cause not diagnosed. Tapping now just opens ntfy; `--click` only with a plain `https://` URL CRE has asked for.
- Substrate: `python3` + GNU `date`. Native on chad-linux (`~/.local/bin/nudge`); on the Windows seat run from git-bash, never PowerShell.

## Core discipline
- **Dateless to-dos stay vault-only.** Only items with a real time signal get a reminder.
- **Creating reminders is outward → attended by default.** Show CRE the batch with the *parsed* times and get a go. The only unattended pushes are day-launch's three standard nudges (CRE opt-in 2026-07-10).
- **Ambiguous time → never guess.** "soon", "this week" → `<<NEEDS A TIME>>` in the batch; CRE supplies one or skips.
- **Guards:** vault sentinel before any write (`^obs-004`); file-tool edits to `TASKS.md`, verified by re-read (DIR-005); never a secret in a title (DIR-001).

## Steps
1. **Sentinel + reachability.** Verify `_DIRECTIVES.md` frontmatter; `nudge list` (fails loudly if ntfy is unreachable → stop with "is Tailscale up?").
2. **Collect eligible items.** Open `- [ ]` lines in `TASKS/TASKS.md` with a time signal (date, weekday, clock time, relative phrase, `remind me`, `due:`) and no `<!-- nudge: … -->` stamp. Legacy `<!-- ody: … -->` stamps point at a dead system: treat the line as unstamped.
3. **Present the batch (gate).** Title · parsed local time · section · `<<NEEDS A TIME>>` / `>3 days — armed on the day` flags. Await CRE's go (Single mode with an unambiguous item: one-line confirm).
4. **Push + stamp.** `nudge send --at "<phrase>" --id <slug>-<YYYY-MM-DD> --title "<short>" "<task text>"`; on the printed `scheduled … id=…` line, file-tool Edit the `TASKS.md` line to append ` <!-- nudge: <id> -->` (replacing any `ody:` stamp); re-read to verify.
5. **Report.** N scheduled with their times; items left for CRE; any failure. Nothing eligible → one line, stop.

## Non-goals
- Two-way completion (ntfy can't carry it).
- Calendar events (Nextcloud Calendar, dec-007).
- Unattended batch pushes beyond day-launch's standard nudges.
