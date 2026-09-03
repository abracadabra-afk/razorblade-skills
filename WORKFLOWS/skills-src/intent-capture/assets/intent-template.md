---
type: intent
slug: "<slug>"
title: "<short title>"
target: "<skill-creator | project-plan | general>"
lane: "<fiction | writing-ops | life | meta>"
status: draft
originator: CRE
source: "<chat | dictation: path | note: path>"
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
---

# INTENT: <title>

> Originator reviews before status moves to `ratified`. Sections above the handoff block are the source; the handoff block is derived from them and regenerated, never hand-edited (DIR-019 §1).

## Job
One paragraph. The whole task, end to end, in CRE's words where possible.

## Why
I'm working on <larger task> for <who>. They need <what the output enables>.

## Guardrails
Each as instruction + reason. Positive form.
- <do X>, because <reason / DIR-nnn>.

## Done looks like
- Exit criteria: <what finished is, how to check it>
- Output style: <shape, length, voice, format>
- Lands at: <path>
- Example to match: <[[note]] or "none">

## Non-goals
- <explicitly out>

## Known context
- [[note]] — <what it settles>

## Open questions
- <question> — default in force: <default>

## Interview record
interview-me, <date>, <N> rounds. Defaults accepted: <n>. Still open: <n>.

## Handoff prompt
<!-- derived from the sections above; regenerate, never hand-edit -->
```
<the block, per references/prompt-rules.md>
```
