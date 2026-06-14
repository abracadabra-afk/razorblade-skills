---
type: workflow
name: skill-audit
trigger: audit the skills
aliases: [check skill drift, are my skills in sync, run the skill doctor, which skills need reinstalling, skill audit, skill doctor]
inputs: [the mounted vault root, the installed skills directory (.claude/skills / skills-plugin), WORKFLOWS/*.md (canonical docs), the WORKFLOWS/skills/*.skill packages, the bundled skill_audit.py]
outputs: [a drift + structural-integrity report across all skills, a rebuild/reinstall punch list, optional _CHANGELOG/_OBSERVATIONS entries on a real audit session]
lane: meta
status: draft
last_updated: 2026-06-10
scope: Any vault that keeps skill sources (WORKFLOWS/*.md and/or WORKFLOWS/skills/*.skill packages) and installs them into Cowork. Read-only — never writes the installed cache or a skill's content.
pipeline_position: The verification half of the skill pipeline; skill-creator is the build half. Runs on demand to reconcile the three layers a Cowork skill exists in.
---

# WORKFLOW: Skill Audit (the skill doctor)

> A read-only reconciliation of every Cowork skill across its three layers — canonical doc, build artifact, installed copy — that reports drift and structural integrity and hands CRE a rebuild/reinstall punch list. It writes nothing but the report (and optional brain-log entries). Established 2026-06-10 after a `storyline-sync.skill` shipped truncated (`^obs-018`) and then ran stale because the install lagged the rebuild.

## Why this exists

A skill that launches in Cowork loads from the **installed app-data cache, NOT from the vault.** The vault holds only the *source* (`WORKFLOWS/<name>.md`) and a *build artifact* (`<name>.skill` in the vault's `WORKFLOWS/skills/` build dir). Getting a vault edit to actually run is a two-hop manual chain — edit the doc → rebuild the `.skill` via skill-creator → install the `.skill` (Save skill button) — and drift can appear silently at each hop. Nothing today enforces that the running copy matches the current source. This workflow makes the drift visible.

## The three layers

1. **Canonical doc** — `WORKFLOWS/<name>.md`. Human-edited source of truth. Matched to a skill by frontmatter `name:`.
2. **Build artifact** — `<vault>/WORKFLOWS/skills/<name>.skill`. Zip of `<name>/SKILL.md`, built from the doc via skill-creator. (The auditor searches `WORKFLOWS/skills/` first; the vault root is a fallback for stray/legacy builds.)
3. **Installed copy** — `<installed>/<name>/SKILL.md`. The file that actually RUNS — app data, outside the vault, read-only.

This workflow cannot fix layers 2 or 3: rebuilding is skill-creator's job; installing is CRE's (Save skill / Settings → Capabilities). It only diagnoses.

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault.

### Step 1 — Resolve the three roots
From the system prompt's "Shell access" mapping, identify `VAULT` (mounted vault root), `INSTALLED` (the `.claude/skills` / `skills-plugin` dir), and `WORKFLOWS` (defaults to `VAULT/WORKFLOWS`). If `INSTALLED` is unclear, ask rather than auditing the wrong tree.

### Step 2 — Run the script
`python skill_audit.py --vault <VAULT> --installed <INSTALLED>`. It matches the three layers by frontmatter `name:` and checks, per skill: structural integrity (frontmatter parses; trailing newline present — a missing one is the `^obs-018` truncation signature; last line not a bare mid-word cut), installed==package (SHA + missing-sections list), and doc-vs-package (mtime heuristic, or exact if the package carries a `source_sha`). Verdicts: `OK` · `REINSTALL` · `REBUILD` · `UNBUILT` · `EXTERNAL` (not vault-managed) · `BROKEN-PKG`.

### Step 3 — Coherence guard (`^obs-014`) — MANDATORY confirmation
The bash mount of the Dropbox-synced tree, and even the installed-cache mount, can serve **stale or incoherent copies**. The read-twice guard in the script catches *flickering* reads but NOT a *consistently stale* one. Therefore: for any skill flagged `REINSTALL`/`REBUILD` on **installed-side integrity**, re-read that installed `SKILL.md` through the file tools (live store) and trust that over the shell read before reporting. In the 2026-06-10 pilot this distinguished three bash-flagged "truncated" installs — two were false (storyline-sync, canon-sync read complete live) and one was real (register-pass genuinely ends mid-sentence). Never report an installed-side defect from a shell read alone.

### Step 4 — Report
Present the table + punch list, then translate to plain actions: `REINSTALL` → "running copy stale/broken — reinstall `<name>.skill`"; `REBUILD` → "doc changed after last build — rebuild via skill-creator, then reinstall"; `UNBUILT` → "doc exists, never packaged (or the package isn't kept in the vault)." Never claim to have fixed anything.

### Step 5 — Log (real audit sessions only)
On a deliberate audit session, append a one-line `_CHANGELOG.md` (meta lane) entry naming flagged skills, and file new fragilities to `_OBSERVATIONS.md`. A quick check stays fully read-only.

## Notes

- **Vault package coverage is itself a finding.** If a skill is installed and has a doc but no `<name>.skill` in `WORKFLOWS/skills/`, its build artifact was one-off (e.g. session outputs) and isn't kept in the vault — so there's no durable artifact to diff or rebuild from. Surfacing those is half the value.
- **Optional `source_sha` stamp.** A future build can stamp the doc's sha into the package frontmatter as `source_sha:`; the script then does an exact doc↔package check instead of the mtime heuristic. Honored if present, ignored if absent.
- Keep this separate from skill-creator: this holds no build logic and never writes a skill's content.
