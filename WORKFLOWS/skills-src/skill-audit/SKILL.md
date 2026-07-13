---
name: skill-audit
description: Reconcile a vault's skill SOURCES against the INSTALLED skill cache and report drift + structural integrity. Use whenever CRE asks to "audit the skills," "check skill drift," "are my skills in sync," "run the skill doctor," "which skills need reinstalling/rebuilding," or wants to know whether a Cowork skill that is running matches the current vault source. It diagnoses the three-layer chain — canonical doc (WORKFLOWS/[name].md) then build artifact ([name].skill in the vault's skills/ build dir) then installed copy (what actually runs, in app data outside the vault) — flags truncation/staleness, and prints a rebuild/reinstall punch list. Do NOT use it to author or fix a skill's content (that is skill-creator), to package a skill, or to install one — it never writes the installed cache (read-only, behind the install trust boundary) and never edits a workflow doc; fixes stay manual.
---

# Skill Audit (the skill doctor)

You are running a read-only reconciliation of every Cowork skill across its three layers, reporting drift and structural integrity so CRE knows exactly which skills to **rebuild** and which to **reinstall**. You write nothing except the report (and, if asked, the brain-log entries).

**Why this skill exists.** A skill that launches in Cowork loads from the **installed app-data cache**, NOT from the vault. The vault holds only the *source* (`WORKFLOWS/<name>.md`) and a *build artifact* (`<name>.skill` in the vault's `WORKFLOWS/skills/` build dir). Getting a vault edit to actually run is a two-hop manual chain — edit the doc → rebuild the `.skill` via skill-creator → install the `.skill` — and drift can silently appear at each hop. This was proven the hard way: a `storyline-sync.skill` shipped truncated (bad build, `^obs-018`) and then ran stale for 22 minutes because the install lagged the rebuild. This skill makes that drift visible.

## The three layers (what gets compared)

1. **Canonical doc** — `WORKFLOWS/<name>.md`. Human-edited source of truth for the procedure. Matched to a skill by its frontmatter `name:`.
2. **Build artifact** — `<vault>/WORKFLOWS/skills/<name>.skill`. A zip containing `<name>/SKILL.md`, built from the doc via skill-creator. (Searched in `WORKFLOWS/skills/` first; the vault root is a fallback for stray/legacy builds.)
3. **Installed copy** — `<installed>/<name>/SKILL.md`. The file that actually RUNS. Lives in Claude's app data, OUTSIDE the vault, and is read-only.

You **cannot** fix layers 2 or 3 from here: rebuilding is skill-creator's job, and installing is CRE's action via the **Save skill** button (Settings → Capabilities). This skill only tells CRE what's stale.

## Step 0 — Vault sentinel check

The gate every skill in this family shares (`^obs-004`). From the mounted vault root, read `_DIRECTIVES.md` and confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`. Missing or mismatched → halt and ask which folder is the intended vault. Write nothing.

## Step 1 — Resolve the three roots — and DO NOT read the installed cache through a mount

- `VAULT` — the mounted vault root (the Dropbox-synced folder). Reading this via bash is fine for *discovery*.
- `INSTALLED` — the installed skills directory. **This must be a REAL, LOCAL path, not a sandbox mount.** On CRE's machine it is the AppData path: `C:\Users\Chad\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\<a>\<b>\skills`.
- `WORKFLOWS` — defaults to `VAULT/WORKFLOWS`.

**The hard rule (`^obs-183`).** The sandbox bash mount of the installed cache (`/sessions/<id>/mnt/.claude/skills/`) serves **stale partials** — it has reported an old `SKILL.md` alongside a freshly-installed `references/` file *in the same directory*, and produced two false "stale install" findings that a desktop probe disproved minutes later. **Never justify a drift verdict from a mounted read.** The script enforces this: it **hard-fails (exit 2)** on a mounted `--installed` path. Run it on the **desktop** — via `windows-cli` (`mcp__windows-cli__execute_command`) or a local python — pointed at the real AppData path.

`--allow-mount` exists as an escape hatch and downgrades **every** drift verdict to `UNCERTAIN`, because that is all a mounted read can honestly support.

> **Why the old `^obs-014` double-read guard did not save us.** It read each file twice and compared size + line count — which detects a **torn** read, not a **stale** one. A stale read is perfectly self-consistent: read it twice, get the same wrong bytes, report "coherent" with total confidence. That guard is retired; the mount refusal replaces it.

## Step 2 — Run the audit script (on the desktop)

```
python skill_audit.py --vault <VAULT> --installed <INSTALLED> [--workflows <WORKFLOWS>] [--json] [--allow-mount]
```

The bundled `skill_audit.py` enumerates all three layers, matches them by frontmatter `name:`, and for each skill checks:

- **Structural integrity** of the installed copy and the package: frontmatter parses (name + description present); the file ends with a trailing newline (a missing one = mid-write truncation, the `^obs-018` signature); last line isn't a bare mid-word cut. A package or installed copy failing this is BROKEN.
- **installed == package, across the WHOLE TREE** (`^obs-183`) — not just `SKILL.md`. Both sides are enumerated in full (the installed dir walked recursively; every zip entry read) and compared three ways: files **packaged but never installed**, files **installed but not packaged** (stale leftovers), and files present on both sides whose **shas diverge**. Any of these ⇒ **REINSTALL**, with the offending paths named. This is the check that was missing: the old audit compared only `SKILL.md`, so a skill whose `references/` or `scripts/` never reached the cache read as **OK**.
- **doc vs package** (heuristic): if the doc was edited after the package was last built ⇒ **REBUILD** candidate. Exact if the package frontmatter carries a `source_sha` of the doc; otherwise mtime-based and labelled a heuristic.

Verdicts: `OK` · `REINSTALL` (rebuild fine, install stale/broken/incomplete) · `REBUILD` (doc newer than build, or package broken) · `UNBUILT` (doc but no `.skill`) · `UNCERTAIN` (mounted read — advisory only) · `EXTERNAL` (installed but no vault source — not vault-managed; **also how the DIR-009 raw-doc install bypass shows up**) · `BROKEN-PKG`.

## Step 3 — The failure mode no file check can see

**A Save-skill is not live until the Cowork session restarts.** The skill list is snapshotted at boot, so a *correct* install still runs the *old* copy in the session that performed it — which reads exactly like "the fix didn't work." Whenever the report contains an install action, say this out loud. It is the third independent reason an install looks unfixed (the other two: the lying mount, and genuine drift).

## Step 4 — Report

Present the script's table and punch list verbatim, then translate the punch list into plain next-actions for CRE, e.g.:

- `REINSTALL <name>` → "the running copy is stale/broken — reinstall `<name>.skill` (Save skill button)."
- `REBUILD <name>` → "`WORKFLOWS/<name>.md` changed after the last build — rebuild `<name>.skill` via skill-creator, then reinstall."
- `UNBUILT <name>` → "doc exists but was never packaged — build it via skill-creator."

Never claim to have fixed anything: this skill only diagnoses. If everything is in sync, say so plainly.

## Step 5 — Log (only on an explicit audit session, not a quick check)

If CRE ran this as a real session (not an incidental check), append a one-line entry to the vault `_CHANGELOG.md` (meta lane) noting which skills were flagged, and file any new fragility to `_OBSERVATIONS.md`. Otherwise stay read-only.

## Notes

- **Optional `source_sha` stamp.** If a future build stamps the doc's sha into the package SKILL.md frontmatter as `source_sha:`, this script uses it for an exact doc↔package check instead of the mtime heuristic. It is honored if present and ignored if absent — no requirement to add it.
- This skill is the verification half of the skill pipeline; skill-creator is the build half. Keep them separate: this one holds no build logic and never writes a skill's content.
