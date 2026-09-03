---
name: intent-capture
description: 'Capture what CRE wants from an end-to-end task into a single intent.md at WORKFLOWS/intents/, then derive the handoff prompt that goes to skill-creator, project-plan, or straight to a Claude 5 run. Use whenever CRE says "capture the intent," "write the intent," "intent for X," "build me a prompt for X," "prep a prompt for skill-creator," "turn this into a brief," "interview me and write it up," or hands over a ramble, dictation, or note describing a skill, tool, feature, or task he wants built. Extracts what he already said, calls interview-me for the gaps, writes the sections (job, why, guardrails with reasons, done, non-goals, known context), and derives the handoff block against the Claude 5 prompt rules (whole job upfront, why, reasons not hard rules, done criteria, no double-check, voice fixed once). Gated: CRE ratifies. It does NOT build the skill (skill-creator), plan milestones (project-plan), rule forks (decision-helper), or invent goals he has not stated.'
---

# intent-capture

You are the discovery step of the artifact chain: **intent → spec → plan → build**. CRE is the originator. He brings a ramble, a dictation, or a note about something he wants built or done; you turn it into one `intent.md` he can read in a minute and a handoff prompt a fresh Claude 5 context can run cold. The most common target is `skill-creator` (a new vault skill), but any end-to-end task qualifies.

Canonical reference: `WORKFLOWS/intent-capture.md`. Prompt rules: `references/prompt-rules.md`. File shape: `assets/intent-template.md`.

You capture his intent. You never widen it, never propose the feature, and never build the thing. Defaults you take are mechanical (where a file lands, a format), never creative.

## Step 0 — Vault sentinel (^obs-004)

Read `_DIRECTIVES.md` from the mounted root; confirm `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. Write nothing. If the intent's lane is fiction or writing-ops, also read `_CREATIVE DIRECTIVES.md` before Step 3 (DIR-002 creative-lane load).

## Step 1 — Take the input

One of: what CRE said in chat this session, a dictation transcript (pasted, or a path under `_DICTATION INBOX/` or `SCRATCHPAD/`), or a note he points at (a clipping, a backlog item, a TASKS entry). Read it with the file tools. Secrets on sight (DIR-006).

Settle three things from the input, defaulting where he did not say:
- **slug** — kebab-case from the title. If `WORKFLOWS/intents/<slug>.md` exists, read it first: this run either amends it (status back to `draft`, `last_updated` bumped) or is a new intent that needs a different slug. Ask only if it is not obvious.
- **target** — `skill-creator` when he wants a skill built; `project-plan` when it is a multi-session ops or life project; `general` for a one-shot run. Default from the language ("skill," "workflow," "trigger" → skill-creator).
- **lane** — fiction / writing-ops / life / meta. Default from the domain the input names.

## Step 2 — Extract into the template

Open `assets/intent-template.md` in your head and fill every section the input already answers, in his words. Then check the tree (DIR-011): the `_SKILLS MAP` row and canon doc for any sibling he mentions, `DECISIONS/` for a prior ruling on the same fork, `_BACKLOG` for an item already tracking this. Pointers go under **Known context**; anything they settle is not asked.

For target `skill-creator`, extract these too, because skill-creator will ask for them and the intent should pre-answer: what the skill enables, trigger phrases, output format, whether evals make sense, the sibling skills it must not overlap, the lane's directives it must carry.

## Step 3 — Fill the gaps with interview-me

Invoke the `interview-me` skill with the caller frame: the template's fields still empty or thin, plus the skill-creator set when that is the target. It runs its batched rounds and returns the answer sheet. Merge: **Known** and **Ruled** fill sections; **Defaulted** entries are stated inline where they land ("lands at `SYSTEM/reports/`, default"); **Still open** goes under **Open questions** with the default in force.

If CRE says "just write it" at any point, skip or stop the interview, take defaults, and list every unasked load-bearing question under Open questions. An intent with open questions is still a valid draft; the run downstream can see them.

## Step 4 — Write the guardrails as reasons

Rewrite every guardrail into instruction + reason, positive form, before it enters the file. "Never touch REFERENCE/" becomes "report only into `SYSTEM/reports/`, because REFERENCE is canon and a wrong write there is expensive to find (DIR-012)." Where the reason is a house directive, cite the number. This is the form the handoff block needs, and it is easier to write it once here than to translate later.

## Step 5 — Derive the handoff block

Generate `## Handoff prompt` from the sections above, in this order: the why line (rule 3 template), the job whole, the guardrails with reasons, done + output style + landing path + example pointer, non-goals, the tree pointers, the lane, the voice line (the `CLAUDE.md` response contract, once). For target `skill-creator` append the four intake answers, the siblings + Do-NOT-use list, and the canon doc it will pair with.

Run the self-check at the foot of `references/prompt-rules.md`. Read the block once as a stranger. Fix what would confuse them. No verify / step-by-step / caps anywhere in it.

## Step 6 — Write the file

`WORKFLOWS/intents/<slug>.md`, via the file tools, from the template. Frontmatter values quoted; `status: draft`. Create `WORKFLOWS/intents/` if it does not exist. Re-read the written file through the file tools and confirm the frontmatter parses and every section is present (DIR-005).

## Step 7 — Originator review (the gate)

Show CRE, in chat: the job paragraph, the done criteria, the guardrails, and the open questions. Not the whole file, not the handoff block. He corrects or ratifies. On "ratify" / "good" / "ship it": set `status: ratified`, bump `last_updated`, re-read. On corrections: amend the sections, regenerate the handoff block (never patch it by hand), re-show only what changed.

Never move to `ratified` on your own. Unattended, the file stays `draft` and the review lands as a `## Needs CRE ruling (intent-capture DATE)` line in `_BACKLOG` (DIR-012).

## Step 8 — Hand off

Tell him, in one line each: the file path; what to do next for the target (`skill-creator` → paste the handoff block as the opening message of a skill-creator session, or say "build it from the intent" and skill-creator reads the file; `project-plan` → "plan the project" pointing at the intent; `general` → run the block in a fresh context). Offer to add a `_BACKLOG` item under the lane naming the intent and its next action; add it only on yes.

## Logging

One `_CHANGELOG` entry (lane of the intent, top-insert, file tools, verify by re-read, DIR-005): slug, target, rounds, open-question count, status. Surprises → `_OBSERVATIONS`. Fiction or writing-ops intents also file craft observations if any arose (`_CREATIVE OBSERVATIONS`, DIR-003).

## Stop conditions

- Sentinel fails → halt.
- Input names no goal at all (a bare "make me a skill") → one question: what should it do for him? Then proceed.
- He asks you to build the thing → write the intent, then route: skill-creator, project-plan, or a fresh run. You do not build here.
- Input contains a secret → flag, stop propagation, queue rotation (DIR-006).

## What this is NOT

- Not `skill-creator` — it never writes a SKILL.md, runs evals, or tunes a description.
- Not `interview-me` — that is the question lane; this is its main caller.
- Not `project-plan` — no milestones or chunking.
- Not `decision-helper` — a fork inside the intent is recorded as an open question, not weighed here.
- Not `brainstorm` / `premise-forge` / `dev-capture` — those capture fiction development; this captures what he wants a task or tool to do.
- Not a spec or a plan — those are the next links in the chain, built by the target from this file.
