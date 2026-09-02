---
type: workflow
name: skill-review
trigger: review skill N
aliases: [shape skill N, run the skill review, is skill N optimized, harvest the session for skill N, harvest skill N]
inputs: [one skill's source dir WORKFLOWS/skills-src/NAME/ (+ its canon doc if present); harvest mode adds a run transcript or excerpt]
outputs: [SYSTEM/reports/YYYY-MM-DD-skill-review-NAME.md (or -skill-harvest-) — verdict line + MECHANICAL / PROPOSED / QUERY bins + Not-checked; a _CHANGELOG entry; NO edits to the skill]
lane: meta
status: draft
last_updated: 2026-09-02
revision_note: v1 scaffold — deterministic linter (scripts/lint_skill.py) built; reasoning pass + harvest mode specced. Not yet run live; first target dictation-transcoder, report-only, after the CH13 chapter-clean pilot lands.
---

# WORKFLOW: skill-review

## When to use
When CRE wants one skill's **design** judged: is it one unit or two, is its mechanical shell a script or forty lines of prose the model re-derives every run, does its description fire on the right phrases, does it load more than it needs to, and what would break downstream if it changed. Also after a skill run that needed hand corrections — **harvest** mode sorts those into one-time vs forever so the forever ones reach the skill instead of dying with the chat.

Source: the 2026-09-02 review of the *How Anthropic Engineers Prompt Claude Code* clipping (`Clippings/`), mapped onto the vault: skills over prompts, the tools layer is the leverage, composable over monolithic, scripts inside skills, invocation flags, and the compounding loop. Three of those six were already house practice; this skill makes the other three (description precision, invocation control, harvest) recur and adds the two checks the vault needs that the video does not mention — **split cost** and **contract surface**.

## The axis it owns (and its neighbors)

| Skill | Question it answers |
|---|---|
| `skill-audit` | Does the **installed copy match its source**? (drift across canon → .skill → installed) |
| `skill-creator` | **Author** or change a skill; run evals; tune a description |
| `skills-manager` | **Orchestrate** the build: scan, package, queue installs |
| **`skill-review`** | Is the skill **shaped right, scripted where it should be, and cheap to load** — and who depends on its contract? |

Same folder, different questions. `skill-review` never authors, never packages, never installs, never resolves drift.

## Governing principle — read-only, one skill, one seam
**Diagnose, never fix.** It writes a report and a changelog line. Every fix routes to `skill-creator` (content) or the desktop pack chain (`pack-skills.ps1` → Save-skill, DIR-009). One skill per run — a portfolio mode is a later decision, not a default.

The work splits at the deterministic / judgment seam:
- **Deterministic (built):** `scripts/lint_skill.py` — frontmatter, description limits, size band, referenced paths, scripts, shell-candidate lines, gate phrases, sibling overlap, consumers, canon pairing, invocation flags. Exit 0/1/2, `--json`, `--selftest`. stdlib only.
- **Judgment (specced):** the reasoning pass — split vs merge, what clusters into a script, what is reference material vs procedure, which contract spans are protected. Produces binned proposals, never verdicts on CRE's craft.

## Anti-rules (why a naive pass gets this vault wrong)
1. **Never split at a gate.** The two-phase propose → rule → write skills are one unit by design.
2. **Never split where the second half needs the first half's working context** (transcoder Cut → Synthesize). A split there adds a serialization boundary and paraphrase risk — the failure `chapter-clean` guards against by passing paths, never content.
3. **Every split has a cost here:** a `_SKILLS MAP` row, a canon doc, a pack, an install, a manifest row. Name it on the item.
4. **Script the shell, never the craft.** Sentinel, input gates, YAML scaffolds, census, exit status, changelog stubs — yes. Floor deny-lists, register invariants, anything semantic — no (DIR-014 corollary, DIR-018).
5. **Legs called by path gain little from description tuning.** Weight F1 by whether the skill is an entry point.
6. **Never hide a leg CRE also runs standalone** behind `user-invocable: false`.
7. **Freeze chain legs mid-pilot.** A leg edit = repack + reinstall + wider installed-vs-canon gap, inherited untested by the chain. Report-only until the pilot lands.
8. **Contract spans are protected.** File names, `status` values, frontmatter keys a caller reads — any item touching one is QUERY, never MECHANICAL, and names the caller.

## Steps (review mode)

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm `type: ai-os-brain` + `file: directives`. Mismatch → halt.

### Step 1 — Resolve the target
`WORKFLOWS/skills-src/NAME/` via the file tools; canon `WORKFLOWS/NAME.md` alongside if present. No source dir → halt, report the orphan. Several named → first only, rest as follow-ups.

### Step 2 — Freeze check
Grep `WORKFLOWS/*.md` for orchestrators listing the skill as a leg. If one names a pilot chapter, **probe the pilot chapter's `draft.md` status / `changelog.md` head — never the orchestrator's own status line** (DIR-010). Landed → no freeze; a stale status line goes to `SYSTEM/drift-ledger.md`. Unlanded pilot → **FROZEN (report-only)**, every item stamped *apply after pilot lands*. (Amended 2026-09-02 after the first run froze on a month-stale "pilots CH13".)

### Step 3 — Deterministic linter
`python3 SKILLDIR/scripts/lint_skill.py --skills-src WORKFLOWS/skills-src --workflows WORKFLOWS --skill NAME`. Confirm every ERROR/WARN by file-tools re-read before it enters the report (`^obs-122`/`^obs-123`). Bash denied on the seat (`^obs-281`) → hand-run FM / DESC / SIZE / REF-PATHS from the file-tools read; state that OVERLAP and CONSUMERS were not machine-scanned.

### Step 4 — Reasoning pass
F1 description · F2 invocation control · F3 shape (split vs merge, both signals) · F4 load cost (progressive disclosure to `references/`) · F5 scripts (shell clusters, each with its constraint set: stdlib, ships in the `.skill`, golden test in `WORKFLOWS/evals/regression-suite/`) · F6 contract surface (protected spans from CONSUMERS) · F7 canon pairing (pointer to `skill-audit`). Anti-rules bind throughout. Full check text lives in the skill's `SKILL.md`.

### Step 5 — Report
`SYSTEM/reports/YYYY-MM-DD-skill-review-NAME.md`: verdict line (`SHAPE OK` / `RESHAPE` / `FROZEN`) → MECHANICAL (batch-ratify) → PROPOSED (evidence, change, cost, route) → QUERY (tree-researched first, DIR-011) → Not checked (DIR-018) → Follow-ups. Chat gets the verdict line and bin counts only.

### Step 6 — Log
`_CHANGELOG` (meta lane, top-insert, file tools, verify by re-read — DIR-005). New surprise → `_OBSERVATIONS`. Unserved rulings → `## Needs CRE ruling (skill-review DATE)` in `_BACKLOG` (DIR-012 clause 5).

## Steps (harvest mode)
1. Read the run's back-and-forth (current session, pasted excerpt, or a file). Secrets on sight (DIR-006).
2. Extract every correction, friction, re-ask, hand fix — short verbatim quotes.
3. Classify `ONE-TIME` vs `FOREVER`.
4. Route FOREVER → `description` / `instructions` / `tools` / `canon doc`. CRE's craft language → QUERY.
5. Report as `…-skill-harvest-NAME.md` in the Step 5 shape; ONE-TIME listed once under Not-applied. Log.

## Stop conditions
- Sentinel fails → halt.
- No `skills-src/NAME/` → halt, report the orphan.
- Linter exit 2 → report the gate failure; no reasoning pass on unparseable frontmatter.
- Asked to fix → report + route; never edit.
- Several skills named → first only.

## Logging
Meta lane. One `_CHANGELOG` entry per run naming the verdict line and bin counts; the report carries the detail.

## Calibration (first live run)
Target `dictation-transcoder`, report-only, after CH13 lands. Expected: one shell script proposed, zero splits, a shorter SKILL.md via `references/`. Any other result → tighten the anti-rules before the skill touches another chain leg.

## Packaging
Source `WORKFLOWS/skills-src/skill-review/` (SKILL.md + scripts/lint_skill.py). Pack on the desktop (`pack-skills.ps1`), sha-verify, Save-skill (DIR-009). Add `lint_skill.py --selftest` to the regression suite when packed. Not installed as of 2026-09-02.

## What this is NOT
- Not `skill-audit` — no drift check.
- Not `skill-creator` — never authors, never rewrites a description, never runs evals.
- Not `task-audit` — scheduled-task prompts are out of scope.
- Not `link-audit` — paths inside one skill dir only.
- Not a portfolio review — one skill per run.
