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

**Creative-lane load (ratified 2026-09-03):** then read `_CREATIVE DIRECTIVES.md` from the mounted root (CDIR-001–010 — how AI behaves around CRE's craft; CDIR-004 governs the passes) before opening any project file. The orchestrator reads it; the per-pass subagents stay isolated with only their prompt + the working text. `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both. Missing → proceed and note it; it is not a sentinel.

---

## Step 1 — Resolve the chapter, the working text, and the run id

- **Chapter folder** (per-chapter convention). If given a name without a path, find the matching folder containing `slate/`. Several → ask; none → say the project hasn't adopted the convention and stop.
- **Working text** — the text every pass reads. Prefer `<chapter>/draft.md` when its frontmatter `status` marks real content (e.g. `dev-revised` — the developmental pass has run); otherwise fall back to the newest slate `clean-draft.md`. Name which you picked. (This is the same working-text rule register-pass uses, so the passes and the register audit the same text.)
- **Slate-run-id** — the slate run this cycle is keyed to: a populated `draft.md`'s `source_slate` names it; a raw slate is its own folder name (e.g. `2026-06-03-01`). Output goes to `<chapter>/spec-check/<slate-run-id>/`.

If there is no working text at all (no populated draft, no slate), halt — there's nothing to diagnose; run the Transcoder (and ideally blind-read + blind-response) first.

**Author-landing preflight (DIR-019 §3, `^backlog-author-landing-preflight`).** Before anything else in this step, diff `draft.md`'s body against the newest entry in `revisions/`. Match — or `draft.md`'s `source_revision` names that entry — → proceed. Mismatch, or `revisions/` holds nothing matching the live body → **CRE hand-landed this draft**: run [[WORKFLOWS/promote-revision]] Step 3b in hand-landing mode first (archive the superseded body byte-exact to `revisions/<date> - draft N superseded.md`, then stamp the folder's stale derives, retire the moot rulings, rewrite `draft.md`'s own open-items list), and only then continue. Never ask him to confirm the landing — his landing is the ruling. Safe op, logged, never gated. No `revisions/` folder at all (author-direct route) → note it and proceed; there is nothing to diff against. — this is item 0 of `WORKFLOWS/spec-check.md` § Running order and rules, ported into this runner because the running order is the line passes' to hold; the supersession triage below assumes the developmental pass moved the text, and this covers the case where CRE moved it.

**Scope of the preflight in this doc (per-source scoping, DIR-019 leg (b) shape).** It runs **in the orchestrator's context alone, and its result never reaches a pass subagent in any form** — not pasted, not summarised, not named in a Step 3 prompt, not implied by an instruction to read `revisions/`. Like `panel-read`, it is folder bookkeeping done before the battery reads anything, and a check a pass would have to open `revisions/` to run is the check in the wrong place; Step 3's fan-out isolation is untouched by it, and Pass 1 — which this runner never runs — stays a clean room regardless. It runs **below this step's own halt**, unlike `loop-clearer`'s, which runs above its: that halt fires when there is no working text at all, and a diff against a draft that does not exist has nothing to preserve. It does not itself retire or resolve a ruling — that stays the supersession triage below, running after, against the body this preflight guarantees is preserved.

**Supersession triage — before Passes 2–5 read the working text (DIR-019, added 2026-09-04).** The developmental pass revises `draft.md` between Pass 1 and the line passes, so everything Pass 1 and its grading produced is a dated claim about text that has since moved. Check every span-naming ruling the battery carries forward — `pass-1-blind.md`'s quoted lines, the `brief.md` **Grading record** rulings, a Workshop-2 ruling set on the dictation route, and any earlier `verdicts.md` for this chapter — against the working text the passes are about to read: **span present → carry silently; span gone → moot, stamp the row `superseded_by: <working text> (<date>)` in place, one log line, never asked; span reworded but surviving → the only case that surfaces**, one batched block carried into the reconciliation, tree-researched first (DIR-011). A pass never re-flags a span its own developmental revision already fixed, and never re-opens a ruling CRE's later draft discharged (§3 — a hand-landed draft is the newest ruling). This also keeps the Step 3 denominator guard honest: a pass counting a span that no longer exists is measuring the old draft. **Scope lock (§4):** staleness outside this chapter's folder and its direct derives is one line in `SYSTEM/drift-ledger.md`, not a pass finding.

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

*One exception, created by Step 1's supersession triage (DIR-019):* a moot row in `pass-1-blind.md`, in the `brief.md` **Grading record**, or in an earlier `verdicts.md` may take a `superseded_by: <working text> (<date>)` **stamp** — a stamp added beside the row, never a rewrite of it and never a deletion. The prohibition above is otherwise unchanged, and the chapter prose is untouchable regardless.

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
