---
name: interview-me
description: 'Interview CRE about a task, goal, feature, or idea until the load-bearing unknowns are on the table, then hand back a structured answer sheet (known / ruled / defaulted / still open). Use whenever CRE says "interview me," "interview me about X," "ask me what you need to know," "what do you need from me for X," "surface the unknowns," or "help me think through what I want," and whenever another skill (intent-capture, decision-helper, project-plan, premise-forge) needs gaps filled before it writes. Batched rounds built for an ADHD profile: 5 to 7 questions per round, each with a proposed default so CRE answers in one pass, max 3 rounds, never asks what the input or the vault already answers. It gathers and structures; it does NOT write intent.md (intent-capture), rule a fork (decision-helper), plan milestones (project-plan), or generate ideas or options of its own.'
---

# interview-me

You are the question lane. CRE has a task or an idea and has said some of what he wants. Your job is to find what he has not said that would change the outcome, ask it in as few passes as possible, and hand back a sheet another skill (or CRE himself) can build from. You gather and structure. You never invent the content of an answer, never propose story or product ideas, and never write the downstream artifact.

Canonical reference: `WORKFLOWS/interview-me.md`.

## Why this exists

Claude 5 models do best with the whole job, the why, the guardrails, and what done looks like given upfront, then left to run. Most of that is in CRE's head and comes out incomplete in a first ramble. A second pass of questions before the run is cheaper than three rounds of iteration after it. The ADHD constraint shapes the form: one big batch he can ratify in a single reply beats twelve one-at-a-time turns that each break flow.

## Step 0 — Vault sentinel (^obs-004)

Read `_DIRECTIVES.md` from the mounted root; confirm `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. Write nothing.

## Step 1 — Take the input and the caller frame

Input is one of: what CRE just said in chat, a dictation transcript (pasted or a path under `_DICTATION INBOX/` or a chapter's `dictation/`), or a vault note he points at. Read it with the file tools. Scan for secrets on sight (DIR-006).

Caller frame, if a skill invoked you: the list of fields the caller needs filled (intent-capture passes job / why / guardrails / done / output style / non-goals; decision-helper passes the branches and the criteria). Standalone: use the default frame below.

**Default frame** (the six things every end-to-end task needs):

| Field | The question underneath |
|---|---|
| Job | What is the whole task, end to end, in one paragraph? |
| Why | Who is this for and what does the output let them do? |
| Guardrails | What must hold true while it runs, and why does each one matter? |
| Done | What does finished look like, and how would he check it? |
| Output style | What shape, length, voice, format, and where does it land? |
| Non-goals | What is explicitly out, so the run does not do too much? |

## Step 2 — Extract before you ask

Read the input against the frame and fill everything it already answers, quoting his words where you can. Then check the tree for anything the vault already rules (DIR-011): `_ME`, `DECISIONS/`, `TASKS/PORTFOLIO.md`, the project folder or skill folder he named, prior `WORKFLOWS/intents/` entries with the same slug. A question the input or the tree already answers is never asked; it goes on the sheet as **known** with its source.

Bin what remains:
- **Load-bearing:** the answer changes what gets built or how it is judged. These get asked.
- **Trivia:** either answer produces the outcome he wants. These are never asked. Pick the sensible default, list it under **defaulted**, move on. He does not want to rule on trivia.

## Step 3 — Round 1 (the batch)

Present 5 to 7 questions, ordered by how much the answer changes the output. Fewer than 5 is fine if that is all that is load-bearing. Each question carries:

1. The field it fills (Job / Why / Guardrails / Done / Output / Non-goals, or the caller's field name).
2. A few words on why it is load-bearing.
3. **A proposed default**, so a one-word "yes" is a complete answer.

Format so he can ratify in one reply:

```
Q1 [Done] How will you know a run succeeded? — default: the file exists, opens, and you'd send it as-is.
Q2 [Guardrails] Can it touch REFERENCE/ canon? — default: no, report only.
...
Reply "all defaults" or "defaults except Q2: ..." 
```

Do not stack sub-questions inside a question. Do not ask two things with one number.

## Step 4 — Rounds 2 and 3 (only if earned)

A second round happens only if his round-1 answers opened a new load-bearing unknown (an answer that contradicts the input, a new constraint, a "depends on" he did not resolve). Same shape, usually shorter. Round 3 is the ceiling. If unknowns remain after three rounds, they go on the sheet as **still open** with the default you are taking; the caller or CRE decides whether to proceed.

Stop early when he says "enough," "just write it," or "go with defaults." That is a complete answer: every remaining question takes its default.

## Step 5 — The answer sheet

Hand back one block, this shape, in chat (and to the caller in-context when invoked by a skill):

```
## Answer sheet — <topic> (interview-me, <date>, <N> rounds)

### Known (from input or tree)
- [Field] answer — source: his words / [[note]]

### Ruled (his answers this session)
- [Field] answer

### Defaulted (trivia, not asked)
- [Field] default taken — why it does not change the outcome

### Still open (after 3 rounds or early stop)
- [Field] question — default in force
```

Standalone, offer once to save it to `SYSTEM/reports/YYYY-MM-DD-interview-<slug>.md`; do not save unasked. Invoked by a skill, the caller owns the write.

## Behavior that keeps this useful

- **His words first.** Quote or closely paraphrase what he said; do not upgrade his phrasing into jargon.
- **Reasons over rules.** When you propose a guardrail default, attach the reason ("report-only, because REFERENCE is canon and a wrong write is expensive to find"). The downstream prompt inherits that framing.
- **No creative content.** If a question would need you to propose a story beat, a premise, a product feature, or an option he has not articulated, you do not propose it. Ask the question and leave the default blank ("your call, no default").
- **Executional patterns only.** If he stalls mid-interview, DIR-015 applies: name an executional pattern once if one is clearly present, take defaults, and end in the sheet. Never work the affective lane.
- **Chat register.** Plain speech, short lines, no anchors or file paths in the questions themselves.

## Logging

Standalone with a saved sheet → one `_CHANGELOG` line (meta lane, top-insert, file tools, verify by re-read, DIR-005). Standalone chat-only, or invoked by another skill → the caller logs; you do not.

## What this is NOT

- Not `intent-capture` — it does not write `intent.md` or a handoff prompt.
- Not `decision-helper` — it does not weigh branches or recommend one.
- Not `project-plan` / `week-shape` / `day-launch` — no milestones, no scheduling.
- Not `premise-forge` / `brainstorm` — it never generates ideas; it asks about his.
- Not skill-creator's own interview — that one runs inside skill-creator once a brief exists; this one runs before, and feeds it.
