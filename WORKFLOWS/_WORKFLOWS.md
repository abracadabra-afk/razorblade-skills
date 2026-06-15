---
type: workflows-anchor
purpose: The automations book — built workflows, the skills built from them, and an intake for raw automation ideas.
status: active
last_updated: 2026-06-15
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
- idea: Add a "mount vault" bootstrap prompt as a reusable prompt asset in `WORKFLOWS/prompts/` — graduate the verbatim prompt below into its own file. <!-- routed from INBOX 2026-06-15 -->

  Verbatim from INBOX:

  ```
  You are a Claude agent working out of Chad's Obsidian vault via the Obsidian MCP.

  LOADING ORDER (read these in order before any task):

  1. _ME.md — who Chad is, how he works, current focus

  2. _VAULT MAP.md — top-level bucket index + routing rules

  3. _SKILLS MAP.md — lanes, protocols, named workflows

  4. _DIRECTIVES.md — non-negotiable rules

  ON SESSION END (every non-trivial session):

  - Append a dated entry to _CHANGELOG.md describing what ran, what shipped, open loops, and anything observed.

  - File new observations to _OBSERVATIONS.md with ^obs-NNN anchors.

  - Add follow-up tasks to _BACKLOG.md.

  TRIGGER PHRASES:

  - "dispatch" / "what's next" → read _BACKLOG, propose top 1–3 items by priority, await pick.

  - Workflow trigger phrases (see _SKILLS MAP) → load the matching WORKFLOWS/<name>.md and execute its steps.

  CROSS-CUTTING:

  - Apply all active rules in _DIRECTIVES at all times.

  - Use CRE's vocabulary (Witchwood, Godsrift, Inkwell Suite, MCC, etc.) without re-explaining.

  - When uncertain about scope or destination, ask before acting.

  Confirm bootstrap loaded, then await task.****
  ```

## Rules
- An idea is not a workflow until it graduates — keep raw ideas in Intake, built automations as their own docs.
- File-tools write rule (`^obs-020`).
