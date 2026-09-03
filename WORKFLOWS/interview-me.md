---
type: workflow
name: interview-me
trigger: interview me
aliases: [interview me about X, ask me what you need to know, what do you need from me, surface the unknowns, help me think through what I want]
inputs: [a goal in chat, a dictation transcript, or a vault note; optional caller frame (the fields another skill needs filled)]
outputs: [an answer sheet in chat (Known / Ruled / Defaulted / Still open); optionally saved to SYSTEM/reports/YYYY-MM-DD-interview-SLUG.md on request]
lane: meta
status: draft
last_updated: 2026-09-03
revision_note: v1 — authored 2026-09-03 alongside intent-capture from the two 2026-09 Claude 5 prompting clippings. Not yet packaged or run live.
---

# WORKFLOW: interview-me

## When to use
CRE has a task, tool, feature, or idea partly in his head and wants the unknowns pulled out before anything gets built or run. Standalone on "interview me about X." Called by `intent-capture` (its Step 3), and available to `decision-helper`, `project-plan`, and `premise-forge` wherever they currently improvise a "what do I still need to know" step.

Source: Anthropic's internal practice of running an interview skill before handing a Claude 5 model an end-to-end task (rule 2 of the seven, `Clippings/Anthropic Just Revealed 7 New Rules for Prompting Claude 5 Models`) and the discovery phase of the AI-native SDLC playbook (`Clippings/Claude Codes New INTENT.MD, What is It`).

## The axis it owns (and its neighbors)

| Skill | Question it answers |
|---|---|
| **`interview-me`** | What has CRE **not said** that would change the outcome? |
| `intent-capture` | What does he **want**, written down and prompt-ready? |
| `decision-helper` | Which **branch** he already named should he take? |
| `project-plan` | What are the **milestones** and the first chunk? |
| `brainstorm` / `premise-forge` | Fiction development capture; generation only in FILL mode |

It asks; the others write. It never generates options or content.

## Governing principle — batched, defaulted, bounded
Built for the ADHD profile: 5 to 7 questions per round, each with a proposed default so one reply ratifies the lot; max 3 rounds; never asks what the input or the tree already answers (DIR-011); trivia is defaulted, not asked (`_ME`: don't make him rule on trivia). Stops on "enough" or "just write it" and takes defaults.

## Steps
0. Sentinel (`^obs-004`).
1. Take the input (chat / dictation / note) + the caller frame (or the default six-field frame: job, why, guardrails, done, output style, non-goals). Secrets on sight (DIR-006).
2. Extract what is already answered; check the tree (`_ME`, `DECISIONS/`, `TASKS/PORTFOLIO.md`, the named project or skill folder, prior `WORKFLOWS/intents/`). Bin the rest load-bearing vs trivia.
3. Round 1: the batch, each question tagged with its field, a few words on why it matters, and a default.
4. Rounds 2 and 3 only if his answers opened a new load-bearing unknown. Early stop on his word.
5. The answer sheet: Known / Ruled / Defaulted / Still open. Offer once to save standalone; a caller owns the write.

Full behavior in `WORKFLOWS/skills-src/interview-me/SKILL.md`.

## Stop conditions
- Sentinel fails → halt.
- A question would require proposing story, premise, product, or option content he has not articulated → ask it with no default ("your call").
- Stall mid-interview → DIR-015: executional pattern named once at most, defaults taken, end in the sheet.

## Logging
Standalone with a saved sheet → one `_CHANGELOG` line (meta). Chat-only or invoked by a skill → the caller logs.

## Packaging
Source `WORKFLOWS/skills-src/interview-me/` (SKILL.md only, no scripts). Pack on the desktop (`pack-skills.ps1`), sha-verify, Save-skill (DIR-009). Not packaged as of 2026-09-03; tracked at `^backlog-intent-pair-pack`.

## What this is NOT
- Not `intent-capture` — writes nothing to `WORKFLOWS/intents/`.
- Not `decision-helper` — no recommendation, no ledger entry.
- Not skill-creator's own intake interview — that runs after a brief exists; this runs before and feeds it.
