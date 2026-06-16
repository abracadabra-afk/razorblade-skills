---
type: workflow
name: vault-boot
trigger: mount the vault
aliases: [boot the vault, boot my OS, load my OS, load my workspace, spin up the vault, start a vault session]
inputs: [none — reads the four loading-order anchors from the vault]
outputs: [a confirmed bootstrap (brief summary of each anchor), then awaits a task]
lane: meta / os
status: active
last_updated: 2026-06-15
---

# WORKFLOW: Vault Boot (the manual mount)

> The on-demand equivalent of the `mount-the-vault` scheduled task. CRE wanted a way to load the AI-OS workspace at the start of any Cowork chat without opening the schedule UI and clicking "run now" — a short phrase instead. This is that phrase. It reads the loading-order anchors, confirms what loaded, and stops; it never starts work on its own.

## When to use

CRE says **"mount the vault"** (or "boot the vault" / "boot my OS" / "load my OS" / "load my workspace" / "spin up the vault" / "start a vault session") at the top of a fresh Cowork session. Use it any time the bootstrap hasn't run and the next thing CRE wants is the OS loaded and ready.

## Inputs

None. The workflow reads four files from the vault via the Obsidian MCP (or the file tools).

## Outputs

A short bootstrap confirmation (one line per anchor on what loaded), then the agent awaits a trigger. No notes are written on a boot-only run.

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (Folded into Step 1's read of `_DIRECTIVES` — don't double-read.)

### Step 1 — Read the loading order, in order (DIR-002)
Read these four, in sequence, before anything else:
1. `_ME.md` — who Chad is, how he works, current focus
2. `_VAULT MAP.md` — top-level bucket index + routing rules
3. `_SKILLS MAP.md` — lanes, protocols, named workflows
4. `_DIRECTIVES.md` — non-negotiable rules

Do not preload deeper notes — open them only when a task requires it.

### Step 2 — Confirm + await
Confirm the bootstrap loaded (a brief per-anchor summary), then **stop and await a task**. Do not dispatch the backlog, run a workflow, or edit any note until CRE gives a trigger.

## Trigger phrases the boot hands off to (post-mount)
- "dispatch" / "what's next" → read `_BACKLOG`, propose top 1–3 items by priority, await pick.
- Any workflow trigger phrase (see `_SKILLS MAP`) → load the matching `WORKFLOWS/<name>.md` and execute its steps.

## Stop conditions
- Vault sentinel fails (Step 0) → halt, ask which folder is the vault.
- After Step 2 → always stop; this workflow never proceeds into work unprompted.

## Logging
A boot-only run with no task attached is **trivial — do not log it** (DIR-003 applies to non-trivial sessions). Whatever task the boot hands off to does its own logging.

## Relationship to the scheduled task
`mount-the-vault` (scheduled task, manual-only) and this workflow share the same body — the scheduled task is for unattended runs; this is the on-demand chat path. Keep both. (See `task-control.md` for the task roster.)
