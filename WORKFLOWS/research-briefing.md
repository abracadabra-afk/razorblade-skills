---
type: workflow
name: research-briefing
trigger: run the research
aliases: [do the research, research this, run the researcher, research dispatch, what research is pending, dispatch research]
inputs: [unchecked "Research ..." task(s) in TASKS/TASKS.md]
outputs: [a concise Markdown briefing in KNOWLEDGE/RESEARCH/, the source task checked off + moved to Done with a link, a run report]
lane: knowledge
status: active
last_updated: 2026-06-15
---

# WORKFLOW: research-briefing

## When to use
CRE has a research project parked in [[TASKS/TASKS|Tasks]] (e.g. *"Research dictation practice methods for fiction"*) and wants it run into a reviewable briefing. Triggers: **"run the research"**, "do the research", "research this", or the daily scheduled runner. This is the AI half of CRE's research lane — he names *what* to look into (via the inbox/task list); this workflow does the disciplined gathering, verifies it, and hands back a tight briefing filed in [[KNOWLEDGE/RESEARCH/_RESEARCH|KNOWLEDGE/RESEARCH]] for his review.

## Core discipline
- **CRE creates the question; AI executes the legwork.** This is admin around the thinking, not the thinking. Findings are *for his review* — never treated as settled, never auto-folded into craft or canon.
- **Lens before length.** Every briefing is filtered through CRE's ADHD learning style (concise, externalized, time-boxed, completion-visible). The *type* of research decides how heavy that lens is (see Step 2). **Concise always; never pad.** If a point can be cut and the briefing still lands, cut it.
- **Verify before you report.** No single-source claims on anything load-bearing. Corroborate across ≥2 independent sources; flag contested or thin claims rather than smoothing them over. Cite every source.
- **One queue, oldest first, no guessing.** The researcher works whatever is *awaiting research* in Tasks. Urgent items CRE runs manually; the daily runner takes the rest. It does not invent research topics.
- File-tools write rule (`^obs-020`); verify writes by reading the file back via the file tools, not a bash read (`^obs-014`). On this vault do **not** use `patch_vault_file` heading/JSON targets to edit tables or sections (`^obs-081`) — read → edit → write whole file, or append. DIR-001: never store a secret found mid-research into a note.

## Modes
- **On-demand (default trigger).** Run the oldest pending research task now. If CRE names a specific one ("research X"), run that — and if it isn't already in Tasks, add it under ⚡ Inbox first so the queue stays the source of truth.
- **Dispatch ("what research is pending" / "research dispatch").** Don't research yet — list the pending `Research …` tasks, recommend the top one (oldest), await CRE's pick. Mirrors the `_BACKLOG` "dispatch" pattern.
- **Scheduled (the `research-runner` task).** Unattended: process exactly **one** item — the oldest pending non-urgent research task — then stop. No item pending → no-op, log nothing noisy.

## Detection (what counts as a research task)
A task in [[TASKS/TASKS]] is a research item when its text **begins with "Research"** (case-insensitive — "Research…", "Research:", "Research on…"), **regardless of how the line is bulleted or checkboxed.**

- **Match on the "Research" lead, not on a well-formed checkbox.** A line that begins with "Research" but has a **missing or malformed checkbox glyph** — a bare `- Research …`, a `Research …` with no bullet at all, an odd glyph — is still a pending research item. (The inbox-router / voice-note path sometimes drops a task without a proper `- [ ]`.) Treat it as **pending**, process it, and **normalize it to `- [x]` on close-out** (Step 5).
- **Skip only the clearly-done.** A line that is genuinely checked (`- [x]`) is finished — skip it.
- The queue is every pending such line across ⚡ Inbox and Active, **oldest first** (top-to-bottom within Inbox, then Active). Urgent items CRE runs manually, so the scheduled runner simply takes the oldest pending one; there is no urgency tag to parse.
- **Upstream note:** a glyph-less "Research" line usually means whatever filed it didn't use a proper `- [ ]` checkbox. Normalizing it on close is the fix here; flag it in the run report if it recurs, since the real fix is at the source (the inbox-router).

## Steps

### Step 1 — Vault sentinel + load + pick
Confirm `_DIRECTIVES.md` frontmatter is present (the `^obs-004` guard). Read [[TASKS/TASKS]] and select the target task per the active mode and the Detection rules above (a missing/malformed checkbox does not disqualify a "Research" line). Read [[KNOWLEDGE/RESEARCH/_RESEARCH]] (briefing index + filename convention). If the queue is empty, report "nothing awaiting research" and stop.

### Step 2 — Classify the research type (sets the lens)
Decide which of two types the task is. Default to **auto-classifying** from the task text; only ask CRE if it is genuinely ambiguous *and* he is present.

- **SKILL-BUILD** — research meant to *improve CRE's own ability to do something* (a practice, technique, habit, process, tool-use). Tells: "how to", "techniques/methods/practice for", "get better at", "improve my…", anything about *his* doing. → **Heavy ADHD lens.** The briefing is organized as an actionable, ADHD-compatible protocol, explicitly filtered through [[LIFE/MENTAL HEALTH/ADHD Patterns]] and [[LIFE/MENTAL HEALTH/ADHD Writing Process]]: externalize working memory, time-box, make completion visible, insert friction where avoidance/perfectionism/restart-loop hit, default to short formats, build in artificial validation points. Findings that fight his wiring get flagged with the ADHD-compatible adaptation, not parroted.
- **GENERAL** — research for a book project, world, market, or any topic of interest that is *not* about improving his own practice. → **Light lens.** Broader and more open, but still presented ADHD-favorably: lead with the answer, keep it concise and scannable, externalize structure (clear sections, a one-line takeaway up top), no filler.

When uncertain, prefer SKILL-BUILD only if the task is clearly about *his* doing; otherwise GENERAL. Note the chosen type in the briefing frontmatter (`research_type:`).

### Step 3 — Research + verify
Gather with web search + fetch (or connected sources). Discipline:
- Pull from multiple independent, credible sources; prefer primary/practitioner/expert sources over content farms.
- **Corroborate load-bearing claims across ≥2 sources.** Where sources disagree or a claim is thin/anecdotal, say so plainly rather than presenting it as fact.
- Keep a running source list with URLs as you go.
- Scope to depth: a SKILL-BUILD protocol needs enough to be *actionable*; a GENERAL brief needs enough to be *accurate and oriented*, not exhaustive. Don't boil the ocean — CRE wants concise and usable.

### Step 4 — Synthesize the briefing (apply the lens)
Write the briefing in Markdown to the format in [[KNOWLEDGE/RESEARCH/_RESEARCH]] (below, for reference). Always:
- **TL;DR first** — 1–3 sentences answering the question, before anything else (working-memory + scan-friendly).
- Tight sections with descriptive headers; short paragraphs or compact lists, never walls of text.
- For SKILL-BUILD: a **"Do this" protocol** (concrete, sequenced, time-boxed where possible) and an **"ADHD fit"** note on each major technique (how to make it stick / where it'll fight his wiring). Keep theory minimal — enough to justify the action, no more.
- For GENERAL: lead with the takeaway, then the substance in scannable sections; a short "So what / how it could be used" close where relevant.
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

### Step 5 — File + close out
- Write the briefing to `KNOWLEDGE/RESEARCH/<YYYY-MM-DD> <slug>.md` and verify the write by reading it back.
- Append a one-line entry to the [[KNOWLEDGE/RESEARCH/_RESEARCH]] index.
- In [[TASKS/TASKS]]: check the source task off (`- [x]`), append ` → [[KNOWLEDGE/RESEARCH/<file>|briefing]] (ready for review)`, and move it to the **## Done** section (newest first). **If the source line had a missing or malformed checkbox glyph, normalize it to a proper `- [x]` checkbox** as part of this move. The completion receipt is deliberate — it serves the validation / working-memory patterns.

### Step 6 — Report
Tell CRE: which task ran, the type/lens applied, the TL;DR, and a link to the briefing. Note if the source line needed checkbox normalization. Keep it to a few lines — the briefing is the deliverable, not the chat.

## Stop conditions
- Queue empty → "nothing awaiting research", stop (scheduled mode: silent no-op).
- A source can't be retrieved / a topic is unsearchable → report what's missing and offer alternatives; do not fabricate or work around fetch restrictions.
- A secret/credential surfaces mid-research (DIR-001) → do not store it; flag and move on.
- Genuinely ambiguous type *and* CRE present → ask once; if unattended, default per Step 2 and note the assumption in the briefing.

## Notes / fragility
- Use the Obsidian file tools for writes; verify by reading back (`^obs-020` / `^obs-014`). Do not use `patch_vault_file` heading/JSON targets on this vault (`^obs-081`).
- The scheduled `research-runner` fires daily ~07:53, just after `books-daily-ingest-weave` (07:06) has sorted the INBOX into Tasks — so freshly-routed research items are present before the runner picks the oldest.
- Briefings are a one-way review surface: CRE reads, then decides what (if anything) graduates into durable KNOWLEDGE craft/method notes or a project. The briefing is the draft, not the canon.

## Logging
On completion, append an entry to [[_CHANGELOG]] under the `knowledge` lane.
