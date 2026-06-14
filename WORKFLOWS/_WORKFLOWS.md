---
type: workflows-anchor
purpose: The automations book — built workflows, the skills built from them, and an intake for raw automation ideas.
status: active
last_updated: 2026-06-14
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

## Rules
- An idea is not a workflow until it graduates — keep raw ideas in Intake, built automations as their own docs.
- File-tools write rule (`^obs-020`).
