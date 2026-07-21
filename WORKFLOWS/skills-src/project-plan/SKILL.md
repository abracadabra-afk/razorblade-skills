---
name: project-plan
description: Turn a goal or a portfolio project into a runway — value-done, 3-7 receipt-carrying milestones, and the CURRENT milestone chunked into one-session steps each with a physical first action — then write TASKS/PROJECTS/slug.md, seed those chunks into TASKS.md, and fill the project's Next milestone slot in PORTFOLIO.md. Use when CRE says "plan the project," "break this down," "chunk this," "plan this out," "replan X," or "close out X." It is the rung between PORTFOLIO (quarterly, which projects matter) and week-shape (weekly). Ops and life lanes ONLY — fiction keeps brief-runway-beats and this never writes into a chapter folder. Gated — it proposes, CRE rules in one pass, then it writes. Replan and close are MODES, not separate skills. Do NOT use it to plan the week (week-shape), serve the day (day-launch), tag loose tasks (triage-the-tasks), rule a fork (decision-helper), or push reminders.
---

# project-plan

The project layer. Canon: `WORKFLOWS/project-plan.md`. Convention: `TASKS/PROJECT-SCHEMA.md`. Design: `SYSTEM/reports/2026-07-20-project-layer-proposal.md`.

## Step 0 — sentinel

Confirm `_DIRECTIVES.md` opens with `type: ai-os-brain` + `file: directives`. Mismatch → halt, ask which folder is the vault. File tools only; verify every write by re-read (DIR-005).

## Scope gate

**Ops and life lanes only.** Fiction projects (Witchwood, Ghost River, Godsrift) already have a project manager — `brief → runway → beats`, `WORKFLOWS/pipeline`, the per-chapter folder convention. If CRE asks to plan fiction work, say so and route to the pipeline. A fiction milestone may appear inside an ops/life plan as one line whose receipt the pipeline produces; never chunk it, never write into a chapter folder.

## Modes

- **create** (default) — new plan
- **replan** — re-cut an existing plan; propose a diff, not a fresh spine; append one line to its Replan log
- **close** — retro → `landed` or `abandoned`; both valid outcomes

## Steps

1. **Prior-ruling check first.** Sweep `DECISIONS/`, `TASKS/PORTFOLIO.md`, `_BACKLOG.md`, and the project's own domain folder. If already ruled or planned, **lead with that** — *"you ruled this on <date>; here is what you ruled"* — and re-open only if CRE says it's stale (DIR-010 vault-content corollary). "I've been meaning to do this forever" is a retrieval trigger, not a planning trigger.

2. **Elicit `done looks like`** — one falsifiable sentence in CRE's words. If he can't state it, **the project isn't ready to plan.** Say so and stop. Do not paper over a fuzzy goal with a tidy milestone list.

3. **Propose the spine — 3–7 milestones, each with a named receipt.** Derived from vault material, never invented. A milestone whose proving artifact can't be named is wrong — re-cut before showing.

4. **Chunk milestone 1 ONLY.** Each chunk = one work session in the project's `win:` window + a **physical first action** ("open Substack, type three candidate names," not "decide on branding"). Stamp `chunk:<ID>` (form `INITIALS-milestone.n`) and any `needs:<ID>`. Two sessions = two chunks. Later milestones stay one line.

5. **Reality check BEFORE the gate.** Chunks remaining ÷ recent per-lane rate, from `chunk:` receipts in `TODAY.md`. If under ~3–4 weeks of history, report **"insufficient history to project"** — do not manufacture a date (DIR-013 cl. 2). Otherwise state it flat: *"target 09-15, derived 10-12, gap +27d."* Never ship a plan the model calls fiction without saying so. No commentary on CRE (DIR-015 cl. 5).

6. **Gate.** One screen, one pass. He edits, ratifies, or kills it.

7. **Write.** `TASKS/PROJECTS/<slug>.md` per PROJECT-SCHEMA (frontmatter via `yaml.safe_dump`, parse-gated — DIR-004) → seed milestone 1's chunks into `TASKS.md` `## Active`, schema-tagged, stamped `<!-- project-plan YYYY-MM-DD -->` → fill that project's `**Next milestone:**` slot in `PORTFOLIO.md`. Verify each by re-read.

8. **Stop.**

## Hard caps

20 minutes · 7 milestones · one milestone chunked · one screen at the gate.

## Never

- Chunk beyond the current milestone
- Plan fiction work or write into a chapter folder
- Invent a project or set its PORTFOLIO rank
- Push to Odysseus (CRE-ruled 2026-07-20 — day-launch owns accountability) or create calendar events (dec-007 — router is the sole connector write-path)
- Estimate effort, compute percent-complete, or draw a chart
- Comment on CRE's performance — receipts are numbers, never affective
