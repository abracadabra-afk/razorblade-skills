# Prompt rules for the handoff block

The `## Handoff prompt` section of every `intent.md` is checked against this list before the file is written. Source: Anthropic's Claude 5 prompting guidance as reported in the two 2026-09 clippings (`Clippings/Anthropic Just Revealed 7 New Rules for Prompting Claude 5 Models`, `Clippings/Claude Codes New INTENT.MD, What is It`), mapped onto house practice. Where a rule and a house directive touch, the directive is named.

## The seven

1. **Give the whole job upfront.** One prompt carrying the complete task, not a step-1-then-step-2 drip. Claude 5 models are trained to run end-to-end; over-specifying the method makes them worse, not safer. The handoff block describes the task, the guardrails, and the exit criteria, then stops. Method is the model's.

2. **Interview before you send.** Unknowns that would change the outcome get surfaced before the run, not discovered three iterations in. That is what `interview-me` is for; the intent file records what was asked, what was defaulted, and what is still open, so the run can see its own blind spots (DIR-018 shape).

3. **Say why, not just what.** The model will hit decisions the prompt did not pre-specify. It makes those better when it knows who the output is for and what it enables. Template: *I'm working on [larger task] for [who]. They need [what the output enables]. With that in mind, [request].* The `## Why` section becomes this line.

4. **Define done.** Long-running models do too much, not too little. Exit criteria and output style are the brake. Every handoff block names what finished looks like, how to check it, the shape and length of the output, and where it lands. Point at an example when one exists (a sibling skill, a prior report) rather than describing the shape from scratch.

5. **Reasons instead of hard rules.** "Never do X" becomes "do Y, because Z." The model follows an instruction it understands the cost of more reliably than a prohibition. Guardrails in the intent file are written as instruction + reason from the start, so the handoff block inherits the form. Where a house directive is the reason, cite it by number ("file tools only for OS docs, DIR-005, because MCP whole-file writes have truncated canon here").

6. **Do not ask it to double-check.** No "verify your work," "review before answering," "think step by step," "explain your reasoning," and no all-caps emphasis. Claude 5 models verify autonomously; instructing it adds a redundant pass and can over-trigger. If a check matters, make it an exit criterion under Done (rule 4), which the model then owns.

7. **Fix the voice once.** Verbosity and jargon are a known failure. State the output register once, in the prompt, plainly: for this vault it is the `CLAUDE.md` response contract (lead with the outcome, one recommended path, detail only if load-bearing, plain speech). Do not repeat it per section.

## House additions

- **AI executes; CRE creates.** Any handoff whose target touches fiction or public-facing copy in CRE's name carries the guard explicitly: revision, analysis, formatting, structure yes; long-form generation of his prose no. (`_ME`, cross-cutting rules; CDIR family for Lane 1/5.)
- **Name the tree.** Pointers to the notes the run should read (`_ME`, the canon doc, a sibling skill, `DECISIONS/` entries) go in the block by path. The run starts cold; the pointers are its context.
- **Name the lane.** Fiction / writing-ops / life / meta. The lane sets which directives and which sibling skills the run must not overlap.
- **For target `skill-creator`,** the block also pre-answers skill-creator's own four intake questions in house terms: what the skill enables, the trigger phrases (the `_SKILLS MAP` row), the output format, and whether evals apply (objective outputs yes, subjective no). Plus the house shape: sibling skills it must not overlap and a Do-NOT-use clause for each; the canon doc `WORKFLOWS/<name>.md` it pairs with; description under 1,024 characters, no angle brackets, quoted if it contains a `#` or a `: ` (`^obs-299`).

## Self-check before writing the block

Read the drafted block once as a colleague with no context would. If they would be confused, so will the model. Then confirm:

- one job, stated whole
- a why line naming who and what-it-enables
- every guardrail carries a reason
- done + output style + landing path present
- no verify / step-by-step / caps
- voice stated once
- lane and tree pointers present
- for skill-creator targets: the four intake answers + siblings + canon doc
