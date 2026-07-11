---
name: vault-boot
description: >-
  Boot Chad's Obsidian vault OS — read the canonical boot doc and the
  loading-order anchors, confirm bootstrap, then await a task. Use whenever CRE
  says "mount the vault", "boot the vault", "boot my OS", "load my OS", "load my
  workspace", "spin up the vault", "start a vault session", or otherwise wants
  the AI-OS workspace loaded at the start of a Cowork session. This is the
  manual, on-demand equivalent of the `mount-the-vault` scheduled task. It boots
  from CLAUDE.md at the vault root (the canonical boot doc), reads _ME → _VAULT
  MAP → _SKILLS MAP → _DIRECTIVES in order with the file tools, confirms what
  loaded, and stops. It does NOT run a workflow, dispatch the backlog, or edit
  any note on its own — after booting, it waits for a trigger phrase
  ("dispatch", a workflow trigger, etc.).
---

# Vault Boot

You are a Claude agent working out of Chad's (CRE's) Obsidian vault.

## The canonical boot doc

**Read `CLAUDE.md` at the vault root with the file tools and follow it exactly** — the Step-0 sentinel (`_DIRECTIVES.md` frontmatter `type: ai-os-brain` + `file: directives`; mismatch or missing → halt and ask which folder is the vault), the loading order (`_ME` → `_VAULT MAP` → `_SKILLS MAP` → `_DIRECTIVES`), the directives, the server/unattended posture, and the session-end logging rules all live there. This skill deliberately holds no boot behavior of its own (doc-deferring, `^obs-124`/`^obs-160`): if this file and `CLAUDE.md` ever disagree, `CLAUDE.md` wins.

## Read path

The **file tools on the mounted vault folder are the default** for all reads and writes (DIR-005). The Obsidian MCP is an optional read-only alternative and is frequently unavailable — never block on it, and never substitute bash reads for OS docs (the mount serves stale partials).

## OUTPUT

After the sentinel check and the four anchor reads, confirm the bootstrap loaded (one line per anchor), then await a task. Do not start work, dispatch the backlog, or edit any note until CRE gives a trigger. A boot-only run with no task attached is trivial — do not log it.
