---
name: blind-response
description: Run the developmental pass that responds to a chapter's blind read (spec-check Pass 1) — triage the first-reader's findings with the author, then revise the draft to fix the ones the author rules real. Use this skill whenever the author asks to "respond to the blind read," "address the blind read," "run the developmental pass," "do the dev pass," or otherwise wants the reader-experience problems a blind read surfaced (drift, a fear/seal that leaked, underbuilt planting, told-not-shown) fixed BEFORE the line-level spec passes run. This is the DEVELOPMENTAL stage — it sits after blind-read (Pass 1) and before spec-check Passes 2–5, and it writes the revised text to the chapter's draft.md. It is two-phase and gated — it proposes, the author rules and approves, then it writes. Do NOT use it to produce a blind read (that is blind-read), to run the line passes, or to execute the register (that is register-pass). It fixes structure and reader experience, never line/voice — that is the register's job.
---

# Blind Response (developmental pass)

You are running the **developmental pass** of the spec-check battery: you take the chapter's blind read (Pass 1) and use it to fix the **reader-experience** problems it surfaced — drift, a fear or theme that landed too early or too late, planting too thin for the ending to reach, emotion told instead of shown at the macro level — **before** the line-level passes (2–5) audit the text. You revise structure and experience; you never touch line/voice. That is the register's job, downstream.

You cannot grade the blind read yourself, and you must not try. The blind read's value is whether its cold findings match what the author *intended* — and you never saw the chapter blind, so a finding like "the reader understood the fear at the bath scene" might be a leak **or** the method working exactly as designed. Only the author knows. So this skill is **two-phase and gated**: you propose, the author rules and approves, then you write.

You do four moves, in strict order: **locate**, **triage (gate 1)**, **propose fixes (gate 2)**, **write**. You never write before both gates are passed.

---

## Step 0 — Vault sentinel check

Before anything else, from the mounted root read `_DIRECTIVES.md` and confirm its frontmatter has both `type: ai-os-brain` and `file: directives`. If missing or mismatched, **halt and ask** which folder is the vault. Do not scaffold, do not write. (Shared `^obs-004` gate.)

---

## Required inputs

You cannot run without all three. If any is missing, stop and ask.

**1. The chapter folder** (per-chapter convention), containing `slate/`, `draft.md`, and ideally `spec-check/<slate-run>/pass-1-blind.md`. If given only a chapter name, search the vault for a matching folder that contains `slate/`. If several match, ask; if none follow the convention, say so and stop.

**2. The blind read** — `<chapter>/spec-check/<slate-run-id>/pass-1-blind.md`, produced by the `blind-read` skill against a specific slate run. If the author pasted the blind read into the conversation instead, use that and note it. If there is no blind read at all, **halt** — this pass *responds* to one; run `blind-read` first.

**3. The work the blind read read** — the same slate `clean-draft.md` the blind read was run against (its `slate_run`/`source` frontmatter names it). You revise *that text*. You are now spec-aware (post-blind), so you may also read the project register (`REFERENCE/register.md`), the chapter's `brief.md` (the written spec — including any Grading record the author filled after Pass 1), `REFERENCE/threads.md`, the chapter `envelope.md`, `continuity.md`, and `notes.md` for context — the clean-room rule was Pass 1's, not yours.

---

## Phase 1 — Triage (GATE 1: the author rules)

Read the blind read and the work side by side. For **every** finding the blind read reported (drift point, the fear/knowledge moment, the prediction, the earned/asserted pair — all of it), do this and show your work:

1. **Quote the blind-read finding** and the line it cited.
2. **Locate it in the work** — quote the actual passage the reader was reacting to.
3. **Propose a triage, with reasoning, in one of three buckets:**
   - **PROBLEM** — this reads as a genuine reader-experience failure (attention lost, a thread underbuilt, emotion asserted not shown). Say what's broken.
   - **WORKING-AS-INTENDED** — this looks like the method succeeding, not failing. The classic case: fear understood through a character's *contradicted action* (showing, not naming) is the technique working; flagging it would "fix" the design. Say why you read it as intended.
   - **AUTHOR-CALL** — genuinely depends on intent you can't recover (e.g. was the fear *meant* to land here or three scenes later?). Frame the question precisely.
When the chapter has a `brief.md`, cite it in each proposal: a finding that contradicts the brief's stated intent (a seal the schedule says must hold, a beat the job required) is presumptively **PROBLEM**; one the brief planned (a deliberate seal, intended foreshadowing, a thread meant to stay quiet) is presumptively **WORKING-AS-INTENDED**. If the author already filled the brief's Grading record after Pass 1, treat those notes as rulings-in-progress and say so. The brief informs your proposal — the ruling still belongs to the author.

4. **Never decide.** Your triage is a *proposal with reasoning*. The author rules every finding. This is the spec-comparison the model structurally cannot make — you never saw the spec blind.

Present the full triage table and **stop. Await the author's rulings** (PROBLEM / INTENDED / and the answers to AUTHOR-CALLs). Do not propose fixes yet. Do not write anything.

If the author rules everything INTENDED, say so plainly and stop — the chapter answered its blind read; nothing to revise. Route them straight to Passes 2–5.

---

## Phase 2 — Propose fixes (GATE 2: the author approves)

For the findings the author ruled **PROBLEM** (and only those), propose concrete fixes. Stay inside this scope hard:

- **Pass-1 findings only.** You address what the blind read surfaced and the author ruled a problem. You do **not** go hunting new issues, and you do not line-edit. If you notice something the blind read didn't, note it in one line at the end for the author — do not fix it.
- **Structural / reader-experience only.** Your moves are: cut or compress a passage that caused drift; build out an underbuilt plant so the ending can reach it (this is the *build, don't cut* move — invent the scene-beat the thread needs); convert a macro told-not-shown into an enacted beat; relocate a reveal the author ruled mistimed. You do **not** adjust diction, fix descriptors, repunctuate dialogue, or polish voice — those are Passes 3–4 and the register, on stable text.
- **Show each fix as a before → after**, name the blind-read finding it answers, and name the move (compress / build / enact / relocate). For a *build*, show the new beat you'd add and what in the text it hooks to.

Present all proposed fixes and **stop. Await the author's approval** (per fix: approve / revise / drop). Do not write before approval.

---

## Write — the revised draft to `draft.md`

Only after Gate 2, apply the approved fixes to the work and write the result to `<chapter>/draft.md`. This is the chapter's "current assembled rough draft," which the Transcoder deliberately leaves for exactly this promotion — so writing here is correct, and the **slate stays untouched** (immutable audit trail; never write to `slate/`).

Set the frontmatter so downstream (Passes 2–5, register-pass) knows this draft now carries real, developmentally-revised content — and **stamp the correct chapter name** (some scaffolds carry a stale `chapter:` from a copied template):

```yaml
---
type: chapter-draft
chapter: <THIS chapter's folder name>
status: dev-revised
source_slate: slate/<slate-run-id>/clean-draft.md
blind_read: spec-check/<slate-run-id>/pass-1-blind.md
last_updated: YYYY-MM-DD
---
```

Below the frontmatter, write the revised prose (carry forward any `<<...>>` Transcoder placeholder slots the work still had — leave them for the register; don't invent resolutions). Then write a short audit note to `<chapter>/spec-check/<slate-run-id>/dev-pass-note.md`: the triage rulings, the approved fixes applied (before → after, move), and any one-line "noticed but out of scope" items for the author.

When you finish, tell the author plainly: the developmental draft is in `draft.md`; **Passes 2–5 and the register will now read `draft.md`, not the slate** (the slate remains the pre-developmental audit trail); and the door to Passes 2–5 is open.

---

## Files this skill writes — and the ones it must not

**Writes:**
- `<chapter>/draft.md` — the developmentally-revised draft (only after both gates).
- `<chapter>/spec-check/<slate-run-id>/dev-pass-note.md` — the audit note.
- `<chapter>/changelog.md` and vault `_CHANGELOG.md` — a session log line.

**Never writes:**
- `<chapter>/slate/**` — immutable. Read-only here.
- `<chapter>/spec-check/<run>/pass-1-blind.md` or any pass output — read-only inputs.
- `REFERENCE/register.md`, `envelope.md`, dictation — inputs/author-owned.
- Anything at all before **both** gates have been passed.

---

## Stop conditions

- **Vault sentinel fails** (Step 0). Halt; ask which folder is the vault.
- **No blind read** for the chapter/slate. Halt; run `blind-read` first — this pass responds to one.
- **No slate `clean-draft.md`** the blind read points to. Halt; the work is missing.
- **Gate not passed.** If asked to write before the author has ruled triage (Gate 1) and approved fixes (Gate 2), decline and return to the open gate. The gates are the whole point.
- **Author ruled everything INTENDED.** Stop; nothing to revise — route to Passes 2–5.
- **A fix would require line/voice work** (diction, descriptor, punctuation, register). Out of scope — note it for the register, don't do it here.

---

## Logging (when running inside CRE's vault)

Non-trivial session — honor DIR-003. If `_CHANGELOG.md` has frontmatter `type: ai-os-brain, file: changelog`, append (newest first):

```
## YYYY-MM-DD — [fiction] developmental pass on <chapter>
**Ran:** blind-response on <chapter> against spec-check/<slate-run>/pass-1-blind.md (slate/<run>/clean-draft.md)
**Shipped:** draft.md (status: dev-revised); <N> findings triaged → <N> ruled PROBLEM; <N> fixes approved & applied (<compress/build/enact/relocate counts>); dev-pass-note.md
**Open loops:** <AUTHOR-CALLs still open, out-of-scope items noted for the register, remaining <<placeholders>>>
**Observed:** <anything notable — e.g. stale draft.md frontmatter corrected (^obs-005 class)>
```

Append chapter-scoped detail to `<chapter>/changelog.md`. File any new fragility to `_OBSERVATIONS.md` with a `^obs-NNN` anchor. If the vault has no `_CHANGELOG.md`, skip logging silently.

---

## Security

If the work, blind read, or register contains credentials, API keys, or tokens, **stop and flag to the author** (DIR-001). Do not copy the secret into `draft.md`, the note, the changelog, or any output. Pause until the author confirms (typically after redacting the source