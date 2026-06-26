---
name: research-briefing
description: Run a research task parked in TASKS/TASKS into a concise, verified Markdown briefing in KNOWLEDGE/RESEARCH/. Use when CRE says "run the research," "do the research," "research this," "research dispatch," or "what research is pending," and on the daily research-runner scheduled task. CRE names the topic; this skill does the disciplined gathering, corroborates every load-bearing claim across 2+ independent sources (citing all, flagging thin/contested points), and hands back a tight briefing for his review — never auto-folding findings into craft or canon. Classifies each task SKILL-BUILD (heavy ADHD lens: an actionable, time-boxed protocol) vs GENERAL (light lens: answer-first, scannable). Three modes: on-demand (oldest pending or a named topic), dispatch (list pending, CRE picks), scheduled (one oldest item, silent no-op when empty). Do NOT use to invent research topics, graduate findings into durable canon, or fetch around a blocked source.
---

# research-briefing

You are running CRE's **research lane**: he names *what* to look into (via the inbox / Tasks list); you do the disciplined gathering, verify it, and hand back a tight, reviewable briefing filed in `KNOWLEDGE/RESEARCH/`. This is **admin around the thinking, not the thinking** — findings are for his review, never treated as settled and never auto-folded into craft or canon.

Canonical reference: `WORKFLOWS/research-briefing.md`. This is the AI-trigger surface; that doc is the in-vault canon.

---

## Core discipline
- **CRE creates the question; AI executes the legwork.** Findings are *for review* — never settled, never auto-folded into craft or canon.
- **Lens before length.** Every briefing is filtered through CRE's ADHD learning style (concise, externalized, time-boxed, completion-visible). The *type* of research sets how heavy that lens is (Step 2). **Concise always; never pad** — if a point can be cut and the briefing still lands, cut it.
- **Verify before you report.** No single-source claims on anything load-bearing — corroborate across **≥2 independent sources**; flag contested or thin claims rather than smoothing them over. **Cite every source.**
- **One queue, oldest first, no guessing.** Work whatever is *awaiting research* in Tasks; never invent topics. Urgent items CRE runs manually; the daily runner takes the rest.
- File-tools writes only (`^obs-020`); verify writes by reading back via the file tools, not a bash read (`^obs-014`). Do **not** use `patch_vault_file` heading/JSON targets on this vault (`^obs-081`) — read → edit → write whole file, or append. DIR-001: never store a secret found mid-research into a note.

## Step 0 — Vault sentinel (^obs-004)
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). If it fails, **halt and report** — do not write.

## Modes
- **On-demand (default trigger).** Run the oldest pending research task now. If CRE names one ("research X") and it isn't already in Tasks, add it under ⚡ Inbox first so the queue stays the source of truth, then run it.
- **Dispatch ("what research is pending" / "research dispatch").** Don't research yet — list the pending `Research …` tasks, recommend the top one (oldest), await CRE's pick. Mirrors the `_BACKLOG` dispatch pattern.
- **Scheduled (the `research-runner` task).** Unattended: process exactly **one** item — the oldest pending non-urgent research task — then stop. No item pending → silent no-op, log nothing noisy.

## Detection — what counts as a research task
A line in `TASKS/TASKS.md` is a research item when its text **begins with "Research"** (case-insensitive — "Research…", "Research:", "Research on…"), **regardless of how it is bulleted or checkboxed.**
- **Match on the "Research" lead, not on a well-formed checkbox.** A bare `- Research …`, a `Research …` with no bullet, or an odd glyph is still **pending** (the inbox-router / voice path sometimes drops the `- [ ]`). Process it, and **normalize it to `- [x]` on close-out** (Step 5).
- **Skip only the clearly-done** (`- [x]`).
- The queue is every pending such line across ⚡ Inbox then Active, **oldest first** (top-to-bottom). No urgency tag to parse — the runner just takes the oldest pending.
- If a glyph-less "Research" line **recurs**, flag it in the report — the real fix is upstream (the inbox-router).

## Step 1 — Load + pick
Read `TASKS/TASKS.md` and select the target per the active mode + the Detection rules (a missing/malformed checkbox does not disqualify a "Research" line). Read `KNOWLEDGE/RESEARCH/_RESEARCH.md` (index + filename convention). Queue empty → report "nothing awaiting research" and stop.

## Step 2 — Classify the type (sets the lens)
Auto-classify from the task text; only ask CRE if genuinely ambiguous *and* he is present.
- **SKILL-BUILD** — research meant to *improve CRE's own ability to do something* (a practice, technique, habit, process, tool-use). Tells: "how to", "techniques/methods/practice for", "get better at", "improve my…", anything about *his* doing. → **Heavy ADHD lens.** Organize as an actionable, ADHD-compatible protocol, explicitly filtered through `LIFE/MENTAL HEALTH/ADHD Patterns` + `LIFE/MENTAL HEALTH/ADHD Writing Process`: externalize working memory, time-box, make completion visible, insert friction where avoidance / perfectionism / restart-loops hit, default to short formats, build in artificial validation points. Findings that fight his wiring get flagged with the adaptation, not parroted.
- **GENERAL** — research for a book project, world, market, or topic of interest *not* about improving his own practice. → **Light lens.** Broader and more open, but still ADHD-favorable: lead with the answer, concise and scannable, externalized structure (clear sections, one-line takeaway up top), no filler.

When uncertain, prefer SKILL-BUILD only if the task is clearly about *his* doing; else GENERAL. Record the choice in the briefing frontmatter (`research_type:`).

## Step 3 — Research + verify
Gather with web search + fetch (or connected sources):
- Pull from multiple independent, credible sources; prefer primary / practitioner / expert sources over content farms.
- **Corroborate load-bearing claims across ≥2 sources.** Where sources disagree or a claim is thin/anecdotal, say so plainly.
- Keep a running source list with URLs as you go.
- Scope to depth: a SKILL-BUILD protocol needs enough to be *actionable*; a GENERAL brief needs enough to be *accurate and oriented*, not exhaustive. Don't boil the ocean.

## Step 4 — Synthesize the briefing (apply the lens)
Write the briefing in Markdown to the format in `KNOWLEDGE/RESEARCH/_RESEARCH.md`. Always:
- **TL;DR first** — 1–3 sentences answering the question, before anything else.
- Tight sections with descriptive headers; short paragraphs or compact lists, never walls of text.
- **SKILL-BUILD:** a **"Do this" protocol** (concrete, sequenced, time-boxed where possible) + an **"ADHD fit"** note on each major technique (how to make it stick / where it'll fight his wiring). Minimal theory — enough to justify the action.
- **GENERAL:** lead with the takeaway, then substance in scannable sections; a short "So what / how it could be used" close where relevant.
- A **Sources** section at the foot (titles + URLs).
- Flag any contested/thin/uncertain point inline with `<<UNCERTAIN>>` rather than hiding it.

**Briefing frontmatter** (serialize cleanly per DIR-004 — no hand-wrapped quotes):
```yaml
---
type: research-briefing
title: <task title, cleaned>
research_type: skill-build | general
source_task: <verbatim task text>
status: for-review
created: YYYY-MM-DD
---
```

## Step 5 — File + close out
- Write the briefing to `KNOWLEDGE/RESEARCH/<YYYY-MM-DD> <slug>.md` and **verify by reading it back** via the file tools.
- Append a one-line entry to the `KNOWLEDGE/RESEARCH/_RESEARCH.md` index.
- In `TASKS/TASKS.md`: check the source task off (`- [x]`), append ` → [[KNOWLEDGE/RESEARCH/<file>|briefing]] (ready for review)`, and move it to the **## Done** section (newest first). **If the source line had a missing/malformed checkbox, normalize it to a proper `- [x]` as part of this move.** The completion receipt is deliberate — it serves the validation / working-memory patterns.

## Step 6 — Report
Tell CRE: which task ran, the type/lens applied, the TL;DR, and a link to the briefing. Note any checkbox normalization. Keep it to a few lines — the briefing is the deliverable, not the chat.

## Stop conditions
- Queue empty → "nothing awaiting research", stop (scheduled mode: silent no-op).
- A source can't be retrieved / a topic is unsearchable → report what's missing and offer alternatives; **do not fabricate or work around fetch restrictions.**
- A secret/credential surfaces mid-research (DIR-001) → do not store it; flag and move on.
- Genuinely ambiguous type *and* CRE present → ask once; if unattended, default per Step 2 and note the assumption in the briefing.

## Files this skill writes — and must not
**Writes (file tools only):** a briefing at `KNOWLEDGE/RESEARCH/<date> <slug>.md`; a one-line index entry in `KNOWLEDGE/RESEARCH/_RESEARCH.md`; the close-out edit in `TASKS/TASKS.md`; the closing `_CHANGELOG` entry (knowledge lane).
**Must NOT write:** anything into craft/canon (`KNOWLEDGE` method notes, project REFERENCE, the bible/threads) — briefings are a review surface, graduation is CRE's separate call; any secret (DIR-001). Apply all active `_DIRECTIVES` (DIR-001 secrets, DIR-002 loading order, DIR-003 log every session, DIR-004 serialized YAML, DIR-005 file-tools-only on OS docs).

## What this skill is NOT
- Not a topic generator — it works the existing Tasks queue, never invents research.
- Not canon — a briefing is the draft for CRE's review, not a settled KNOWLEDGE/method note or project fact; graduation is a separate, deliberate step CRE makes.
- Not a scraper / restriction-bypass — when a source is blocked it reports the gap, never works around it.

## Build status
- Canon doc shipped 2026-06-15 at `WORKFLOWS/research-briefing.md` (status: active, `^obs-075`); the daily `research-runner` scheduled task fires ~07:53 (just after `books-daily-ingest-weave` sorts the INBOX into Tasks).
- This source authored from that doc (source-ahead of any install).
- Propagation to the installed skill = desktop `pack-skills.ps1` + Save-skill (`^backlog-research-skill-package`). The `_SKILLS MAP` "run the research" trigger row is already present. Until packaged, the workflow runs via the bootstrap trigger index + the live `research-runner` scheduled task.
