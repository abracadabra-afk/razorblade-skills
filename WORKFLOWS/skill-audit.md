---
type: workflow
name: skill-audit
trigger: audit the skills
aliases: [check skill drift, are my skills in sync, run the skill doctor, which skills need reinstalling, skill audit, skill doctor]
inputs: [a race-free clone of razorblade-skills (git), its skills-manifest.json, WORKFLOWS/git-bridge/build.py, the installed skills cache (.claude/skills / skills-plugin), WORKFLOWS/*.md (canonical reference docs)]
outputs: [a current/STALE/not-installed report per skill, a Save-skill punch list, optional _CHANGELOG/_OBSERVATIONS entries on a real audit session]
lane: meta
status: active
last_updated: 2026-06-14
scope: Vaults using the Git Bridge (a versioned razorblade-skills repo + skills-manifest.json). Read-only — never writes the installed cache or a skill's content.
pipeline_position: The verification half of the skill pipeline; skill-creator authors content, build.py packages it. Runs on demand (or under skills-sweep) to reconcile what RUNS against the canonical git package.
git_bridge: Re-scoped onto the Git Bridge 2026-06-14 (see [[WORKFLOWS/git-bridge-proposal]] / `^obs-063`–`^obs-067`). Supersedes the pre-bridge mount+mtime version.
---

# WORKFLOW: Skill Audit (the skill doctor) — Git Bridge edition

> A read-only reconciliation of every Cowork skill against its **canonical git package**: does the copy that actually RUNS match the package in `razorblade-skills`? It reports `current` / `STALE` / `not-installed` and hands CRE a Save-skill punch list. It writes nothing but the report (and optional brain-log entries). Re-scoped 2026-06-14 onto the Git Bridge, which replaced the fragile Dropbox-mount reads that the original version (2026-06-10) had to defend against.

## Why this exists

A skill that launches in Cowork loads from the **installed app-data cache, NOT from the vault** — and getting an edit to actually run is a manual chain (author → package → Save-skill), with silent drift at each hop. The original skill-audit had to read the package side through the Dropbox mount and guess doc-vs-package drift from mtimes, both unreliable (`^obs-014`, `^obs-060`). The Git Bridge removed that whole problem: the canonical packages now live in a **version-controlled, race-free git repo** with a **SHA-256 manifest**, so currency is an exact content-hash comparison, not a guess. This workflow is now the thin reporter over that.

## The layers (post-bridge)

1. **Source** — `WORKFLOWS/skills-src/<name>/SKILL.md` (+ assets). The editable, diffable skill text. Adopted + built by `pack-skills.ps1` (desktop); rides to the repos via `seed-repo.ps1`.
2. **Package** — `WORKFLOWS/skills/<name>.skill`, built from the source by `pack-skills.ps1` (desktop, `^obs-058`-safe) — *not* the sandbox. Its content is what `build.py audit` content-hashes.
3. **Installed** — `<installed>/<name>/SKILL.md` (+ assets). The copy that actually RUNS — app data, outside the vault, read-only.
4. *(reference, not hash-gated)* **Doc** — `WORKFLOWS/<name>.md`. The human workflow spec. Kept consistent with the source editorially (skill-creator's job), not by a hash check — the package `SKILL.md` is an authored surface, not a copy of the doc.

This workflow cannot fix layers 1–3: authoring is skill-creator's job, packaging is `build.py`'s, installing is CRE's (Save skill). It only diagnoses.

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault.

### Step 1 — Pull the canonical packages (race-free)
Clone the public skills repo fresh into a sandbox-local dir (NOT the Dropbox mount — that is the whole point):
```
git clone --depth 1 https://github.com/abracadabra-afk/razorblade-skills.git /tmp/rs
```
This is the `^obs-063` read path: git transport on `github.com` only. The clone is the canonical package side; never audit the package against the Dropbox-mounted `WORKFLOWS/skills/` (the `^obs-014`/`^obs-060` stale-mount class).

### Step 2 — Verify package integrity
`python3 /tmp/rs/WORKFLOWS/git-bridge/build.py verify --root /tmp/rs`. Confirms every `.skill` unzips, `SKILL.md` frontmatter parses, body is non-empty and not mid-word-truncated, and (if present) the zip SHA matches the manifest. A `BODY-MAYBE-TRUNCATED` or `FAIL` here means the canonical package itself is broken — a build/source repair (Step 5 handoff), rare now that builds are race-free.

### Step 3 — Audit installed-vs-package (the currency check)
`python3 /tmp/rs/WORKFLOWS/git-bridge/build.py audit --root /tmp/rs` (auto-detects the installed cache). It content-hashes each package's `SKILL.md`+assets against the installed copy and reports `current` / `STALE` / `SUSPECT-STALE` / `not-installed`. `STALE` = the running copy differs from the canonical package → it needs a Save-skill. **`SUSPECT-STALE`** (added 2026-06-15, `^obs-070`/`^obs-014`) = the mismatch came off a **truncated/NUL installed-side read** (the audit now auto-detects the mount-staleness signature — a NUL/replacement byte or an installed file that is a proper prefix of the package) → it is **not** confirmed stale; the run prints a `MOUNT MAY BE STALE` banner. This is the script doing the first half of Step 4 automatically, so false STALEs stop getting queued.

### Step 4 — Coherence guard (`^obs-014` / `^obs-066`) — MANDATORY for STALE *and* SUSPECT-STALE
The package side is now race-free (git), but the **installed cache is still an app-data mount** that can read stale within a session — and a just-completed Save-skill may not have propagated into the sandbox's view (`^obs-066`: a re-audit right after reinstalling showed false STALE; the file tools confirmed the installs took). `build.py audit` now auto-downgrades the *detectable* truncation/NUL case to `SUSPECT-STALE`, but a mount can also read stale **without** a NUL signature (a complete-but-old copy), so the guard still applies to plain `STALE`. Therefore: for any `STALE` **or** `SUSPECT-STALE` skill, re-read that installed `SKILL.md` through the **file tools** (live store) before reporting it. If the file-tools copy matches the package, it is **current** — the STALE flag was mount lag; say so. Never report an installed-side defect from the audit's mount read alone. When in doubt, a fresh Cowork session gives a new mount snapshot and a clean read.

### Step 5 — Report
Present the result + a plain punch list: `STALE` → "running copy differs from the git package — Save-skill `<name>.skill`"; `not-installed` → "packaged but never installed"; package `FAIL`/`verify` problems → "canonical package broken — rebuild from source (skill-creator + `build.py package`)." Note any `WORKFLOWS/<name>.md` doc that has drifted from its skill source as an *editorial* follow-up (not a currency defect). Never claim to have fixed anything.

### Step 6 — Log (real audit sessions only)
On a deliberate audit session, append a one-line `_CHANGELOG.md` (meta lane) entry naming flagged skills, and file new fragilities to `_OBSERVATIONS.md`. A quick check stays fully read-only.

## What changed from the pre-bridge version (2026-06-10 → 2026-06-14)

- **Package side reads from a git clone, not the Dropbox mount.** Retires the package-side `^obs-014` re-confirm and the `^obs-060` truncation risk on the canonical copy.
- **Currency is a content hash, not an mtime heuristic.** `build.py audit` compares `SKILL.md`+assets byte-for-byte; the `source_sha` stamp the old Notes wished for is realized as the manifest `content_sha256`.
- **The bundled `skill_audit.py` is superseded by `build.py`** (verify + audit). `build.py` is the single mechanical engine; this doc is the procedure around it.
- **Installed-side guard stays.** The one place the old `^obs-014` discipline still bites is the app-data install cache (`^obs-066`) — Step 4 keeps the file-tools confirmation there.

## What this is NOT

- **Not a builder or installer.** It holds no build logic (that's `build.py` + skill-creator) and never clicks Save-skill (CRE's trust boundary).
- **Not a content author.** Keep it separate from skill-creator: it never writes a skill's content, only reports drift.
