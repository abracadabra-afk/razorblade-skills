---
type: workflows-anchor
purpose: The automations book — built workflows, the skills built from them, and an intake for raw automation ideas.
status: active
last_updated: 2026-07-29
---

# WORKFLOWS

> **The automations book.** Everything the system can *do* on command: the named multi-step workflows and the Cowork skills built from them. (Formerly branded "DoBook" — the brand was retired in the 2026-06-14 restructure; this bucket is now just **WORKFLOWS**, plain and direct.)

> Routing: the [[WORKFLOWS/inbox-router|Inbox router]] sends *automation ideas* ("we should have a skill that…", "automate the X step") to the **Intake** below. A built/active automation is a full workflow doc in this folder (`<name>.md`), registered in [[_SKILLS MAP]].

---

## Layout
- `WORKFLOWS/<name>.md` — the canonical source doc for each automation.
- `WORKFLOWS/skills/` — the packaged `.skill` build artifacts + `REGISTRY.md` + `_skill-patches/` (moved here from the old root `SKILLS/` in the 2026-06-14 restructure).
- `WORKFLOWS/prompts/` — reusable standalone prompt assets (incl. the migrated DICTATION PROMPTS).

## Built automations (live)
The workflow docs in this folder are the canonical source for each automation; [[_SKILLS MAP]] is the trigger-phrase index, and installed `.skill` packages are the auto-trigger surface. See [[_SKILLS MAP]] → "Named workflows" + "Cowork skills" for the full registry.

## ⚡ Intake — automation ideas (raw)

> CRE (or the router) drops half-formed "wouldn't it be useful if…" automation ideas here. When one is real, it graduates into its own `WORKFLOWS/<name>.md` (use [[WORKFLOWS/_TEMPLATE]]) and gets registered in `_SKILLS MAP`.

<!-- idea: <one line> — why / what it would do -->

- idea: Build an auto researcher skill/trigger <!-- routed from INBOX 2026-06-15 -->
- idea: Build a "Closing Ritual" skill — end-of-day check-in where CRE reports accomplishments (words dictated, scenes edited, project progress, what worked / what didn't, what to remember for tomorrow); creates a daily log of productivity/progress/methodology reinforcement + positive reinforcement, tracking running metrics (word counts, streaks) writers like to watch grow <!-- routed from INBOX 2026-06-15 -->
- idea: Beat-based dictation runway from the briefing files — after a chapter is scaffolded through the workshop, derive an ADHD-friendly, light-touch "breadcrumb" runway from its brief: just the notes/key beats to keep in mind so the story can breathe while still hitting the beats already decided. Not heavy-handed with instruction <!-- routed from INBOX 2026-06-15 -->
- ✅ graduated 2026-07-28 → **day-launch v2.7** (lane quotas + the growth split, CRE-ratified live: Creative 1–2 · Growth 1–2 · Admin 0–2 · Personal 1–2, cap 7; `#growth` marker added to [[TASKS/TASK-SCHEMA]]; growth serves before admin in the afternoon window — a fourth *time* window was considered and declined, lanes are board sections not clock blocks). Original idea kept below for provenance.
- idea *(graduated, see above)*: Restructure day-launch's TODAY brief into distinct lanes rather than one flat 3–5 list — CRE's own words: "I do think the today brief needs some adjustment, as [Witchwood] wasn't even on there as the first project that should have been completed as I did. Perhaps breaking the day into different lanes: the creative lane, my morning, where my creative energy is at its highest and I'd rather do writing and deep work; then an operational lane for marketing and projects that are related to the acquisition of readers and branding etc; and then a personal lane where I have my appointments and projects that need to be done on a personal level. I know we're limiting the total list to five or so, but I think having two or three in each lane is good. That way I can work through multiple tasks if they are available to me." Note: day-launch v2 already has energy-mapped windows (win:morning/ops/personal) with a hard cap of 5 total — this proposes going further, a per-lane sub-cap (2–3 each) rather than one global 5-item cap. <!-- routed from INBOX 2026-07-28; from 2026-07-27 check-in, intent: workflow / day-launch lane restructuring -->

- idea: Line-edit / editing skills — CRE's own words: "I also do need to develop editing skills for line edits. I'm thinking highly specialized skills especially around trimming compression, which are make-and-break type skills. Line edits of course, so I can have a well-edited piece when I post it. Episode 1 has my target for that — next, get some editing skills. Perhaps research first before building them so they are built effectively to serve my voice and vision while offering quality edits." Note: embeds a "research first" steer — build to serve CRE's voice/vision; Episode 1 (WIW) is the target piece. <!-- routed from INBOX 2026-07-29; from 2026-07-28 check-in, intent: skill idea — editing/line-edit skill -->
- idea: Choreographer skill + dialogue-choreography skill — CRE's own words: "The other skills I've had on my mind lately are a choreographer skill. This would allow me, while I'm dictating, to move over events that require choreography such as fight scenes, action — that way as I dictate I can make note with the outcome of the action, with a note to follow up with the choreographer to really make the action shine. I think this would be a very valuable skill. Normally I could choreograph fight scenes, action scenes, horror scenes, murder scenes, even sex scenes. Similar to choreographer, I'm also thinking of dialogue as a way to choreograph conversations — the attacking and defending that makes compelling dialogue so pertinent." Note: pairs with DIR-017 (dictation is protected forward-flow) — the choreographer is a "move-over-and-flag-for-later" mechanism so action beats don't stall the mic. <!-- routed from INBOX 2026-07-29; from 2026-07-28 check-in, intent: skill idea — choreographer skill + dialogue choreography -->

- ✅ graduated 2026-06-15 → [[WORKFLOWS/vault-boot]] (trigger "mount the vault"). The "mount vault" bootstrap is now a built workflow + Cowork skill, not a `prompts/` asset — the on-demand sibling of the `mount-the-vault` scheduled task. The verbatim prompt lives in the workflow doc + `skills-src/vault-boot/SKILL.md`.

## Rules
- An idea is not a workflow until it graduates — keep raw ideas in Intake, built automations as their own docs.
- File-tools write rule (`^obs-020`).
