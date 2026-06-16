---
name: vault-boot
description: >-
  Boot Chad's Obsidian vault OS — read the loading-order anchors and confirm
  bootstrap, then await a task. Use whenever CRE says "mount the vault", "boot
  the vault", "boot my OS", "load my OS", "load my workspace", "spin up the
  vault", "start a vault session", or otherwise wants the AI-OS workspace loaded
  at the start of a Cowork session. This is the manual, on-demand equivalent of
  the `mount-the-vault` scheduled task. It reads _ME → _VAULT MAP → _SKILLS MAP →
  _DIRECTIVES in order via the Obsidian MCP, confirms what loaded, and stops. It
  does NOT run a workflow, dispatch the backlog, or edit any note on its own —
  after booting, it waits for a trigger phrase ("dispatch", a workflow trigger,
  etc.).
---

# Vault Boot

You are a Claude agent working out of Chad's Obsidian vault via the Obsidian MCP.

## Step 0 — Vault sentinel (`^obs-004`)

Read `_DIRECTIVES.md` first; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (This read doubles as the first of the loading-order reads below.)

## LOADING ORDER (read these in order before any task)

1. `_ME.md`        — who Chad is, how he works, current focus
2. `_VAULT MAP.md` — top-level bucket index + routing rules
3. `_SKILLS MAP.md`— lanes, protocols, named workflows
4. `_DIRECTIVES.md`— non-negotiable rules

Read all four with the Obsidian MCP (`get_vault_file`) before doing anything else. Do not preload deeper notes — open them only when a task requires it (DIR-002).

## ON SESSION END (every non-trivial session)

- Append a dated entry to `_CHANGELOG.md` describing what ran, what shipped, open loops, and anything observed.
- File new observations to `_OBSERVATIONS.md` with `^obs-NNN` anchors.
- Add follow-up tasks to `_BACKLOG.md`.

(A boot-only run with no task attached is trivial — do not log it.)

## TRIGGER PHRASES

- "dispatch" / "what's next" → read `_BACKLOG`, propose top 1–3 items by priority, await pick.
- Workflow trigger phrases (see `_SKILLS MAP`) → load the matching `WORKFLOWS/<name>.md` and execute its steps.

## CROSS-CUTTING

- Apply all active rules in `_DIRECTIVES` at all times.
- Use CRE's vocabulary (Witchwood, Godsrift, Inkwell Suite, MCC, etc.) without re-explaining.
- Edit structured OS docs and `WORKFLOWS/*.md` with the file tools only — never `patch_vault_file` or a whole-file MCP rewrite (DIR-005).
- When uncertain about scope or destination, ask before acting.

## OUTPUT

After reading all four anchors, confirm the bootstrap loaded (a brief summary of each anchor), then await a task. Do not start work, dispatch the backlog, or edit any note until CRE gives a trigger.
