---
name: spec-passes
description: Run spec-check Passes 2–5 (the spec-aware line passes) as a single fan-out — one isolated subagent per pass — and collect their findings into a verdict-sheet scaffold for the author to reconcile. Use this skill whenever the author asks to "run the line passes," "run passes 2–5," "run the spec passes," "spec passes," or otherwise wants the four spec-aware diagnostic passes executed after the blind read and developmental pass. Each pass runs in its own fresh subagent context with only its single prompt + the working text, so the passes stay isolated (no blending, honest examined-counts) while the author issues one command. Do NOT use this for Pass 1 (that is the clean-room blind-read skill) or the developmental rewrite (that is blind-response) — this runner deliberately excludes both. It diagnoses only; it never edits the chapter and never decides judgment calls.
---

# Spec-Passes Runner (Passes 2–5 fan-out)

You orchestrate the four spec-aware diagnostic passes of the spec-check battery — Pass 2 (carries vs asserts), Pass 3 (descriptor), Pass 4 (dialogue punctuation stance), Pass 5 (narrator naming theme) — by dispatching **each pass to its own isolated subagent** and collecting the results. Each subagent gets a fresh context with one pass-prompt and the chapter text, so the passes do not blend and each reports an honest examined-count, while the author runs one command instead of four.

You **diagnose only**. You never edit the chapter, never run Pass 1 (blind) or the developmental pass, and never *decide* a judgment call — you assemble the candidates into a `verdicts.md` scaffold and hand the rulings to the author.

You do five moves, in order: **sentinel**, **resolve**, **load the prompts**, **fan out**, **assemble**.

---

## Step 0 — Vault sentinel check

From the mounted root, read `_DIRECTIVES.md` and confirm its frontmatter has both `type: ai-os-brain` and `file: directives`. If missing or mismatched, **halt and ask** which folder is the vault. (Shared `^obs-004` gate.)

---

## Step 1 — Resolve the chapter, the working text, and the run id

- **Chapter folder** (per-chapter convention). If given a name without a path, find the matching folder containing `slate/`. Several → ask; none → say the project hasn't adopted the convention and stop.
- **Working text** — the text every pass reads. Prefer `<chapter>/draft.md` when its frontmatter `status` marks real content (e.g. `dev-revised` — the developmental pass has run); otherwise fall back to the newest slate `clean-draft.md`. Name which you picked. (This is the same working-text rule register-pass uses, so the passes and the register audit the same text.)
- **Slate-run-id** — the slate run this cycle is keyed to: a populated `draft.md`'s `source_slate` names it; a raw slate is its own folder name (e.g. `2026-06-03-01`). Output goes to `<chapter>/spec-check/<slate-run-id>/`.

If there is no working text at all (no populated draft, no slate), halt — there's nothing to diagnose; run the Transcoder (and ideally blind-read + blind-response) first.

---

## Step 2 — Load the pass prompts from the canonical battery doc

Read `WORKFLOWS/spec-check.md` and extract the four prompt sections verbatim: **PASS 2 — CARRIES vs. ASSERTS**, **PASS 3 — DESCRIPTOR**, **PASS 4 — DIALOGUE PUNCTUATION STANCE**, **PASS 5 — NARRATOR NAMING THEME / CONFIRMING PARALLEL**. The workflow doc is the single source of truth for these prompts — do **not** keep your own copy, so an edit to the battery propagates automatically. If `WORKFLOWS/spec-check.md` is absent (this skill running outside CRE's vault), halt and tell the author the battery doc is required.

---

## Step 3 — Fan out: one isolated subagent per pass

Spawn **four subagents in parallel** (Pass 1 is excluded — it has its own clean-room skill; the dev pass is excluded — it has human gates). Give each subagent exactly:

1. **One pass-prompt**, verbatim, from Step 2.
2. **The working text** — paste its prose (or give the path and tell the subagent to read only that file). Each subagent sees only the chapter text and its single prompt — nothing about the other passes.
3. **These standing instructions:**
   - Run *only* this one pass. Do not perform any other pass's operation.
   - Do not edit any file. Return your findings as text.
   - Honor the prompt's output contract exactly, including the **two bins** (MECHANICAL / JUDGMENT CALL) and the closing **count: examined vs flagged**.
   - De-duplicate within your pass: group a recurring move under one named habit; never list one habit as N findings.

Run them concurrently — they're independent. Each returns its full structured result.

### Denominator guard
When the results come back, sanity-check the examined-counts against each other and the chapter's length. If one pass reports an implausibly low examined-count (e.g. it "examined 6" lines where its siblings examined 40), the pass got lazy, not lucky — **re-dispatch that one pass once** to a fresh subagent before trusting its silence. Note any re-run in your summary.

---

## Step 4 — Assemble the outputs

Write the per-pass results, then a reconciliation scaffold. You assemble; you do not rule.

### Four pass files
Write each subagent's result to `<chapter>/spec-check/<slate-run-id>/`:
`pass-2-carries.md`, `pass-3-descriptor.md`, `pass-4-dialogue.md`, `pass-5-theme.md`. Front each with:

```yaml
---
pass: <2-carries | 3-descriptor | 4-dialogue | 5-theme>
slate_run: <slate-run-id>
working_text: <draft.md | slate/<run>/clean-draft.md>
examined: <N>
flagged: <N>
generated: YYYY-MM-DD HH:MM
---
```

### The verdict-sheet scaffold — `verdicts.md` at `status: draft`
Assemble all four passes' findings into `<chapter>/spec-check/<slate-run-id>/verdicts.md` using the structure in `WORKFLOWS/spec-check.md`, with two rules:

- **Pre-fill MECHANICAL** with every mechanical failure and its supplied fix, tagged by pass.
- **List every JUDGMENT CALL with a blank ruling slot** — `RULED: ____` — for the author to fill. Do **not** decide them.
- **Cross-pass de-dup:** if the same line or decision was flagged by more than one pass (e.g. a narrator gloss caught by both Pass 2 and Pass 5), enter it **once**, noting which passes raised it, rather than twice.
- List any **UNDRAMATIZED** verdicts prominently (the build-don't-cut items).
- Set frontmatter `status: draft` and `slate_run: <slate-run-id>`. It becomes `status: ready` only when the **author** has ruled the judgment calls — and `register-pass` will not run execute-only until then.

End by telling the author: the four passes are done (give the examined/flagged counts per pass and flag any re-run); `verdicts.md` is a **draft awaiting your rulings**; once you flip it to `ready`, run `register-pass`.

---

## Files this skill writes — and the ones it must not

**Writes:** `<chapter>/spec-check/<slate-run-id>/pass-2-carries.md … pass-5-theme.md`, `verdicts.md` (status: draft), and a `_CHANGELOG`/chapter `changelog.md` log line.

**Never writes:** the chapter prose (`draft.md`, slate, anything in `revisions/`), `pass-1-blind.md`, the register, or `verdicts.md` at `status: ready` (only the author promotes it). Never edits the working text — this is a diagnostic, not a revision.

---

## Stop conditions

- **Vault sentinel fails** (Step 0). Halt; ask which folder is the vault.
- **No working text** (no populated `draft.md`, no slate `clean-draft.md`). Halt; nothing to diagnose.
- **`WORKFLOWS/spec-check.md` missing.** Halt; the canonical pass-prompts are required.
- **Asked to run Pass 1 or the developmental rewrite, or to edit the chapter.** Decline — those are `blind-read` / `blind-response` / `register-pass`. This runner is Passes 2–5, diagnostic only.
- **A subagent returns malformed output** (no bins, no count). Re-dispatch that pass once; if it fails again, write what you have and flag the gap to the author rather than fabricating findings.

---

## Logging (when running inside CRE's vault)

Honor DIR-003. If `_CHANGELOG.md` has frontmatter `type: ai-os-brain, file: changelog`, append (newest first):

```
## YYYY-MM-DD — [fiction] spec line passes (2–5) on <chapter>
**Ran:** spec-passes on <chapter> working text <draft.md | slate/<run>> — 4 subagents (passes 2–5)
**Shipped:** spec-check/<slate-run>/ pass-2…pass-5 + verdicts.md (status: draft); counts: P2 <e>/<f>, P3 <e>/<f>, P4 <e>/<f>, P5 <e>/<f>; <N> re-runs for low counts
**Open loops:** verdicts.md awaiting CRE rulings on <N> judgment calls; <N> UNDRAMATIZED to hand-check
```

Append chapter-scoped detail to `<chapter>/changelog.md`. File any new fragility to `_OBSERVATIONS.md`. If the vault has no `_CHANGELOG.md`, skip logging silently.

---

## Security

If the working text contains credentials, API keys, or tokens, **stop and flag to the author** (DIR-001) before dispatching subagents — do not propagate the secret into subagent prompts or any output file. Pause until the author confirms (typically after redacting the source).
