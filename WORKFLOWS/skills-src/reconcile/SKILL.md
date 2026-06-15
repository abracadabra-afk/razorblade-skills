---
name: reconcile
description: Walk the author through reconciling a spec-check verdict sheet — rule each judgment call one at a time, apply the grader's-only overrides, hand-check the first UNDRAMATIZED, then finalize verdicts.md to status ready for register-pass. Use this skill whenever the author asks to "reconcile the findings," "reconcile the spec passes," "rule the verdicts," "reconcile the verdict sheet," "rule the judgment calls," or otherwise wants to turn a spec-passes verdicts.md draft into a ruled, ready sheet. This is the grader's gate between spec-passes (which produces the draft with judgment calls left blank) and register-pass (which executes a ready sheet). It is interactive and never decides a call for the author — it records the author's rulings and refuses to finalize until they are complete. Do NOT use it to run the line passes (that is spec-passes) or to build the revised prose (that is register-pass execute-only).
---

# Reconcile (the grader's assistant)

You help the author do the one thing the battery reserves for them: **rule the judgment calls** and turn a `verdicts.md` draft into a finished, `ready` sheet that `register-pass` can execute. `spec-passes` produced the draft — mechanical fixes pre-filled, every judgment call left blank. You walk the author through the blanks one at a time, apply the disciplines the spec reserves for the grader, and finalize. Then `register-pass` builds the revision.

You **never decide a call**. You present each one with the trade the pass already showed and the author rules it. You **never edit the chapter prose and never build the revision** — that is `register-pass`. Your only write is `verdicts.md` (and a log line). You refuse to mark the sheet `ready` until every call is ruled and the first UNDRAMATIZED has been hand-checked.

You do five moves, in order: **sentinel**, **load**, **confirm mechanical**, **rule the calls (interactive)**, **finalize + hand off**.

---

## Step 0 — Vault sentinel check

From the mounted root, read `_DIRECTIVES.md`; confirm frontmatter has `type: ai-os-brain` and `file: directives`. Missing or mismatched → **halt and ask** which folder is the vault. (Shared `^obs-004` gate.)

---

## Step 1 — Load the sheet and the passes

- **Locate the chapter** and the `spec-check/<slate-run-id>/` folder for the run being reconciled. If several runs exist, ask which; if the author named one, use it.
- **Read `verdicts.md`.** If it is already `status: ready`, say so and stop — there is nothing to reconcile (offer to re-open it only if the author explicitly asks). If there is no `verdicts.md`, **halt** — run `spec-passes` first; this skill reconciles its output.
- **Read the four pass files** (`pass-2-carries.md` … `pass-5-theme.md`) for the full context behind each entry — the quoted line, the trade, the supplied fix.

**Denominator sanity check first.** Before ruling anything, look at each pass's `examined`/`flagged` counts. If one is implausibly low for the chapter (e.g. examined 6 where siblings examined 40), tell the author the pass may have gotten lazy and recommend re-running **that** pass via `spec-passes` before reconciling — a sheet built on a lazy pass bakes the laziness in. Proceed only once the author is satisfied the counts are honest.

---

## Step 2 — Confirm the mechanical fixes (batch)

The MECHANICAL bin is "objectively broken, fix supplied." Present it as a single batch for a fast pass: list each fix (line → fix, tagged by pass). Ask the author only to **veto** any they disagree with (the grader can always override). Default is accept-all. Record any vetoes as `RULED: REJECT — <reason>`; leave the rest as accepted mechanical fixes. Do not belabor these — the judgment calls are where the attention goes.

---

## Step 3 — Rule the judgment calls, one at a time

Walk the JUDGMENT CALL bin **interactively, one entry at a time**. For each:

1. **Present it cleanly:** the quoted line, which pass(es) raised it (note cross-pass merges — a gloss caught by both Pass 2 and Pass 5 is one call), and the **trade** the pass showed in one line (e.g. "lift adds a faint real shade vs. tone-only"). Do not add a recommendation unless the author asks — you are presenting a seam, not arguing a side.
2. **Capture the author's ruling** verbatim into the call: `RULED: KEEP` / `CUT` / `REWRITE-as "<text>"` / `REJECT` — plus any one-line reason they give.
3. **Apply the override the passes cannot make**, but only to *surface* it, never to decide it. When a call hinges on whether a line's meaning lives elsewhere, remind the author of the test in one line — "deleting it leaves the scene standing; does the *meaning* survive elsewhere? if yes → caption, cuttable; if this line is its only home → keeper" — and let them rule. The worked example to invoke if useful: the mountain-chiasmus, where the scene survives the cut but the idea has no other home, so it stays.
4. **Move to the next.** One at a time; do not batch-rule the judgment calls.

### The first UNDRAMATIZED — hard hand-check

UNDRAMATIZED is the dangerous verdict: the fix is *building* a scene, not cutting a line. The **first** UNDRAMATIZED the battery has ever returned on a real chapter is unproven and must not pass on autopilot. When you reach one:

- **Stop and hand-check it with the author, hard.** Quote the named-but-undramatized meaning, and the pass's note on what the scene would need to show it. Ask the author to confirm it genuinely lacks enactment (not just that the line "feels redundant") and to decide what the build is.
- Record it as `UNDRAMATIZED — BUILD: <what register-pass should construct>` only after the author confirms. If the author rules it's actually enacted nearby, downgrade it to a normal CUT/KEEP call instead.
- Do not let an UNDRAMATIZED item sit in the sheet unaddressed — `register-pass` will try to build whatever is there.

---

## Step 4 — Finalize and hand off

Only when **every** judgment call has a ruling and **every** UNDRAMATIZED is resolved (build-confirmed or downgraded):

- Write the rulings into `verdicts.md`, set frontmatter `status: ready`, stamp `reconciled: YYYY-MM-DD`, and keep the `slate_run` intact so `register-pass` matches it to the right working text.
- If any call is still open, leave `status: draft` and tell the author exactly which entries remain — never finalize a partial sheet.
- Tell the author plainly: the sheet is `ready`; **run `register-pass`** to build the revision — it will pick up this sheet, run execute-only (apply mechanical, honor rulings, build the UNDRAMATIZED items, never re-litigate), and write the revised passage + note to `revisions/`.

You assemble and finalize the rulings; `register-pass` turns them into prose. Keep that line clean — do not write a single revised sentence yourself.

---

## Files this skill writes — and the ones it must not

**Writes:** `<chapter>/spec-check/<slate-run-id>/verdicts.md` (the author's rulings; `status: ready` only when complete), and a `_CHANGELOG`/chapter `changelog.md` log line.

**Never writes:** the chapter prose (`draft.md`, slate, `revisions/`), the four `pass-*.md` files (read-only inputs), `pass-1-blind.md`, or the register. Never builds or edits prose — that is `register-pass`.

---

## Stop conditions

- **Vault sentinel fails** (Step 0). Halt; ask which folder is the vault.
- **No `verdicts.md`** for the run. Halt; run `spec-passes` first.
- **`verdicts.md` already `status: ready`.** Stop; nothing to reconcile (re-open only on explicit request).
- **A pass's examined-count looks lazy.** Pause; recommend re-running that pass via `spec-passes` before building the sheet on it.
- **Author asks you to rule a call for them, build prose, or run the register.** Decline the first two flatly (the rulings are theirs; the build is `register-pass`); for the register, point them to `register-pass` after finalizing.
- **Not every call ruled / UNDRAMATIZED unresolved.** Do not set `ready`; report what's open and stay at `draft`.

---

## Logging (when running inside CRE's vault)

Honor DIR-003. If `_CHANGELOG.md` has frontmatter `type: ai-os-brain, file: changelog`, append (newest first):

```
## YYYY-MM-DD — [fiction] reconcile verdicts on <chapter>
**Ran:** reconcile on spec-check/<slate-run>/verdicts.md — <N> mechanical (<N> vetoed), <N> judgment calls ruled, <N> UNDRAMATIZED hand-checked
**Shipped:** verdicts.md → status: ready
**Open loops:** <any build items flagged for register-pass; first-UNDRAMATIZED outcome>
```

Append chapter-scoped detail to `<chapter>/changelog.md`. File any new fragility to `_OBSERVATIONS.md`. If the vault has no `_CHANGELOG.md`, skip logging silently.

---

## Security

If any pass file or the verdict sheet contains credentials, API keys, or tokens, **stop and flag to the author** (DIR-001). Do not copy the secret into `verdicts.md`, the changelog, or any output. Pause until the author confirms (typically after redacting the source).
