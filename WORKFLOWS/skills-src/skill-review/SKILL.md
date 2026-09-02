---
name: skill-review
description: Review ONE vault skill's design quality — is it shaped right (composable vs monolithic, split or merge), is its mechanical shell scripted where a script would normalize results, is its description precise, is its load cost justified, and what contract do its callers depend on. Use when CRE asks to "review skill N," "shape skill N," "run the skill review," "is skill N optimized," or "harvest the session for skill N" (the second mode: mine a just-finished run's back-and-forth for one-time vs forever fixes). Runs a deterministic linter (scripts/lint_skill.py) then a reasoning pass, and writes a binned MECHANICAL / PROPOSED / QUERY punch list to SYSTEM/reports/. READ-ONLY — never edits a skill; fixes route to skill-creator, packaging to pack-skills.ps1. Do NOT use to check source-vs-build-vs-installed drift (skill-audit), to author or fix a skill (skill-creator), to audit scheduled-task prompts (task-audit), or to review more than one skill per run.
---

# skill-review

You are reviewing the **design** of one vault skill — the fourth leg of the skills family. `skill-audit` asks *is the installed copy current*; `skill-creator` *authors*; `skills-manager` *orchestrates the build*. You ask **is this skill shaped right, scripted where it should be, and cheap enough to load** — and you hand back a punch list. **You never edit the skill.** Every fix is a gated, manual act routed to `skill-creator` (content) or the desktop pack chain (`pack-skills.ps1` → Save-skill).

Canonical reference: `WORKFLOWS/skill-review.md`. This is the AI-trigger surface; that doc is the in-vault canon.

Two modes. **Review** (default) reads the skill's source. **Harvest** reads a run's back-and-forth and sorts the corrections into one-time vs forever. Both end in the same report shape.

---

## Step 0 — Vault sentinel (^obs-004)
Read `_DIRECTIVES.md` from the mounted root; confirm `type: ai-os-brain` + `file: directives`. Mismatch/missing → halt and ask which folder is the vault. Write nothing.

## Step 1 — Resolve the target (source, never the installed cache)
- Target = `WORKFLOWS/skills-src/NAME/` (SKILL.md + scripts/ + any references/). Read it with the file tools (DIR-005 — the bash mount serves stale partials).
- Also read the canon doc `WORKFLOWS/NAME.md` if it exists. Where canon and source disagree, note it as a pointer to `skill-audit`; do not resolve it here.
- No `skills-src/NAME/` → halt and report (an installed skill with no source is an orphan; onboarding it is CRE's call, tracked in `_BACKLOG`).
- One skill per run. Asked for several → take the first named, list the rest as follow-ups.

## Step 2 — Freeze check (chain legs mid-pilot)
Grep `WORKFLOWS/*.md` for orchestrators that call this skill (`chapter-clean`, `chapter-pipeline`, `land-chapter`, or any doc whose shape block lists it as a leg). If a calling orchestrator names a pilot chapter, **probe the pilot's live state — never its status line** (DIR-010: a recorded status is not a state). Open the pilot chapter's `draft.md` frontmatter and `changelog.md` head: `status: landed` / a LANDED entry → the pilot is over, no freeze. Only an unlanded pilot freezes the run: **REPORT-ONLY, FROZEN**, verdict line says FROZEN, every item stamped *apply after pilot lands*. Editing a leg mid-pilot means repack + reinstall + a wider installed-vs-canon gap, and the chain inherits the change untested. A stale orchestrator status line found this way is one line to `SYSTEM/drift-ledger.md`, not a finding (DIR-019 §4). *Origin: the 2026-09-02 first run froze on `chapter-clean.md`'s "pilots CH13" a month after CH13 landed.*

## Step 3 — Run the deterministic linter
```
python3 SKILLDIR/scripts/lint_skill.py --skills-src "WORKFLOWS/skills-src" --workflows "WORKFLOWS" --skill NAME [--canon DOC] [--json]
```
Prefer the desktop (Desktop Commander `start_process`, Windows `python`) over the sandbox: the files are local and current there, and the sandbox bash grant has been denied on some seats (`^obs-281`). `--canon` names the canon doc when its basename differs from the skill (the transcoder's is `transcoder.md`); without it the script falls back to the one `WORKFLOWS/*.md` that references `skills-src/NAME`.
Exit `0` clean · `1` ERROR findings · `2` gate failure (bad path, unparseable frontmatter). Checks, by id:

| id | what it decides exactly |
|---|---|
| FM-PARSE | frontmatter parses; `name` matches the folder |
| DESC-LEN / DESC-BRACKET / DESC-TRIGGERS / DESC-NEGATIVE | description ≤1024 chars, no angle brackets (DIR-009 pack rule), count of quoted trigger phrases, presence of a Do-NOT-use clause |
| SIZE | SKILL.md bytes / words / lines, ~tokens (bytes÷4), band GREEN ≤8k · WARN ≤16k · HEAVY >16k tokens |
| REF-PATHS | every relative path SKILL.md names (scripts/, templates/, references/) exists in the skill dir — a missing one fails the pack (DIR-009) |
| SCRIPTS | scripts present, count, referenced-from-SKILL.md or dangling |
| SHELL-CANDIDATES | lines that read like the mechanical shell (sentinel, frontmatter/YAML writes, file scaffolds, changelog entry, exit codes) — candidates only, INFO |
| GATES | count of halt / ask / CRE-rules / gated phrases — INFO |
| OVERLAP | normalized lines (≥12 words) shared with sibling SKILL.md files; house boilerplate (sentinel, logging) tallied separately |
| CONSUMERS | every `WORKFLOWS/*.md` and sibling SKILL.md that names this skill, with the lines that name it — the contract surface |
| CANON-PAIR | `WORKFLOWS/NAME.md` exists; its `last_updated` vs the skill's version line — pointer to skill-audit, INFO |
| INVOKE-FLAGS | `user-invocable` / `disable-model-invocation` present in frontmatter — INFO; Cowork support of these flags is UNVERIFIED (DIR-010) |

**Freshness (^obs-122 / ^obs-123):** a sandbox run is candidate-only. Confirm every ERROR/WARN line by re-reading the flagged lines through the file tools before it enters the report. If the bash tool is denied on this seat (`^obs-281`), skip the script, run the FM/DESC/SIZE/REF-PATHS checks by hand from the file-tools read, and state in the report's Not-checked line that OVERLAP and CONSUMERS were not machine-scanned.

## Step 4 — Reasoning pass (the checks a script cannot decide)
Work each check against the source you read. Anti-rules are binding: they exist because a naive pass recommends the wrong thing on this vault.

**F1 Description (trigger precision).** Does it fire on the phrases in the `_SKILLS MAP` row and refuse its siblings' phrases? Overlap with a sibling's description is a finding. Route any rewrite to `skill-creator`'s description-optimization loop — never rewrite here. *Anti-rule:* legs called by path inside an orchestrator gain little from trigger tuning; weight this check by whether the skill is an entry point.

**F2 Invocation control.** Human-only candidates: skills that write canon or promote (`land-chapter`, `promote-revision`, `canon-sync`). Agent-only candidates: utilities CRE never types. *Anti-rule:* never propose hiding a leg CRE also runs standalone (`register-pass`). Every flag proposal is a QUERY until Cowork's support for the flag is confirmed live.

**F3 Shape (composability).** Two signals, opposite directions. *Split signal:* OVERLAP lines shared with siblings, or two procedures inside one SKILL.md with different triggers and different outputs. *Merge signal:* a skill that only ever runs inside one orchestrator and has no standalone trigger. Measure both; recommend only when one dominates. *Anti-rules:* (a) never split at a gate — the two-phase propose/rule/write skills (`blind-response`, `reconcile`, `loop-clearer`) are one unit by design; (b) never split where the second half needs the first half's working context in the same window (the transcoder's Cut → Synthesize: survivors, cut reasons, heat bank) — a split there adds a serialization boundary and paraphrase risk; (c) every split costs a `_SKILLS MAP` row, a canon doc, a pack, an install, a manifest row — name that cost on the item.

**F4 Load cost (progressive disclosure).** SIZE band WARN/HEAVY → which sections are reference material read on demand (examples, templates, long tables) rather than procedure read every run? Propose moving them to `references/` with a one-line pointer. Never propose cutting a rule to save tokens.

**F5 Scripts (the shell, never the craft).** SHELL-CANDIDATES → which cluster into one script: sentinel + input gate + output scaffold with `yaml.safe_dump` frontmatter (DIR-004) + census/exit status + changelog stub. Every script proposal carries its constraint set on the item: stdlib only (DIR-007 — nothing installs on the mount), referenced path ships in the `.skill` (DIR-009), and a golden test lands in `WORKFLOWS/evals/regression-suite/` or the sweep's Step 3.5 never sees it. *Anti-rule:* never script a judgment — floor deny-lists, register invariants, leaves census semantics, anything DIR-014's corollary covers. A regex that "normalizes" a semantic check hides misses (DIR-018).

**F6 Contract surface (consumers).** From CONSUMERS: list every file name, `status` value, frontmatter key, and folder the callers read from this skill (e.g. `expansion-revised`, `source_slate`, `protected_patterns`, the four slate files). These are **protected spans** for this review: any item that touches one is a QUERY, never MECHANICAL, and names the caller that would break.

**F7 Canon pairing.** Source says vX, canon says vY → one INFO line pointing at `skill-audit`. Not your finding to resolve.

## Step 5 — Report
Write `SYSTEM/reports/YYYY-MM-DD-skill-review-NAME.md`. Shape:

1. **Verdict line** — one of `SHAPE OK` / `RESHAPE` / `FROZEN (report-only)`, plus the SIZE band and the script status in one sentence.
2. **MECHANICAL** — items a pack can absorb without a design call: a missing referenced path, description over length, a dangling script. Batch-ratify.
3. **PROPOSED** — the design items with evidence: check id, the lines, the proposed change, the cost (repack? contract touch? new map row?), the route (`skill-creator` / `pack-skills.ps1` / regression suite).
4. **QUERY** — anything touching a protected span (F6), an invocation flag, or a split/merge call. One line of tree research per item first (DIR-011) — if a prior ruling or a `_BACKLOG` anchor already answers it, present *resolved against X — confirm*.
5. **Not checked (DIR-018)** — what the linter did not run, what was hand-checked from a mount read, what the reasoning pass skipped.
6. **Follow-ups** — the other skills named in the trigger, and any sibling the OVERLAP check implicates.

Present the verdict line and the counts per bin in chat. The report carries the detail; chat does not repeat it.

## Step 6 — Log
`_CHANGELOG` entry under the `meta` lane (file tools, top-insert, verify by re-read — DIR-005). New build surprise → `_OBSERVATIONS` (`^obs-NNN`, scan the whole file for max + 1). Items CRE must rule that are not served by an existing gate bin → one `## Needs CRE ruling (skill-review DATE)` block in `_BACKLOG` (DIR-012 clause 5).

---

## Mode 2 — Harvest ("harvest the session for skill N")
The compounding loop: a skill run just finished and the back-and-forth holds corrections. Sort them so the forever ones reach the skill.

1. **Input:** the run's transcript — the current session's exchange after the trigger, a pasted excerpt, or a file CRE points at. Read it in full. Scan for secrets on sight (DIR-006).
2. **Extract** every correction, friction, re-ask, and manual fix CRE made. Quote each verbatim, short.
3. **Classify** each: `ONE-TIME` (chapter-specific, project-specific, this run's data) or `FOREVER` (a rule, an example, an edge case, a trigger miss, a mechanical step done by hand every run).
4. **Route** each FOREVER item to a layer: `description` (it should have fired / should not have) · `instructions` (a rule or edge case) · `tools` (a step done by hand that a script would normalize) · `canon doc` (the WORKFLOWS doc, not the skill). Items in CRE's craft language (register, voice, a story call) are QUERY — they are his to word.
5. **Report** in the Step 5 shape (`SYSTEM/reports/YYYY-MM-DD-skill-harvest-NAME.md`), ONE-TIME items listed once under Not-applied. Then Step 6.

Harvest never edits the skill either. It hands `skill-creator` a sorted list.

---

## Files this skill writes — and must not
**Writes:** `SYSTEM/reports/…-skill-review-NAME.md` or `…-skill-harvest-NAME.md`; a `_CHANGELOG` entry; optional `_OBSERVATIONS` / `_BACKLOG` lines.
**Must NOT write:** anything under `WORKFLOWS/skills-src/`, any `WORKFLOWS/NAME.md` canon doc, any `.skill`, the installed skill cache, `_SKILLS MAP`. No auto-fix of any finding.

## Build status
- **v1 — scaffolded 2026-09-02:** `scripts/lint_skill.py` (stdlib only; exit 0/1/2; `--json`; `--canon DOC` when the canon basename differs from the skill name, e.g. `transcoder`; `--selftest`). Selftest green and a dry linter run on `dictation-transcoder` completed on the desktop 2026-09-02 (sandbox bash was denied on the seat — run it via the desktop, which is also the fresh filesystem). Reasoning pass + harvest mode specced in this doc. **Reasoning pass not yet run live** — first target is `dictation-transcoder`, report-only, after the CH13 `chapter-clean` pilot lands. Calibration test: expected result is one shell script, zero splits, a shorter SKILL.md; a different result means the anti-rules need tightening before this touches another chain leg.
- Propagation to the installed skill = desktop `pack-skills.ps1` + Save-skill (DIR-009).

## Stop conditions
- Sentinel fails → halt, ask which folder is the vault.
- No `skills-src/NAME/` → halt; report the orphan.
- Linter exit 2 → report the gate failure; do not proceed to the reasoning pass on a skill whose frontmatter will not parse.
- Asked to FIX a finding → report + route; never edit.
- Asked to review several skills at once → first one only, rest as follow-ups.

## What this skill is NOT
- Not `skill-audit` (no drift check across source / build / installed).
- Not `skill-creator` (never authors, never rewrites a description, never runs evals).
- Not `task-audit` (scheduled-task prompts are out of scope).
- Not `link-audit` (dangling paths inside one skill dir only, not vault-wide links).
