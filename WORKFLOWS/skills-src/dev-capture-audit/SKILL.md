---
name: dev-capture-audit
description: Audit a project's DEV/ tree for capture INTEGRITY — the read-only QA sibling of dev-capture. Use when CRE asks to "audit the dev capture," "audit the dev tree," "run the dev-capture doctor," or "check the dev capture," or wants a dev-capture run/batch checked for structural defects. Runs a deterministic linter (scripts/audit_dev.py) flagging duplicate ^poe anchors, broken _POETICS↔_DEV_MAP graduation parity, a routed transcript left in _intake/, missing floors, placeholder leaks, bad frontmatter, missing boundary tags, dangling DEV wikilinks, and thin stubs, then reports a severity-ranked punch list. READ-ONLY — never edits the tree; fixes stay gated and manual. Do NOT use to route/write entries (dev-capture), judge content readiness (dev-readiness), audit installed-skill drift (skill-audit), or as the vault-wide link authority (link-audit; this is a DEV-scoped pre-filter).
---

# dev-capture-audit

You are running **capture-integrity QA** on a project's `DEV/` tree — the read-only sibling of `dev-capture`. You verify the *bookkeeping the capture pipeline is responsible for*, never whether the story is good (that is judgment) or developed enough (that is `dev-readiness`). **You never edit the tree.** Every fix is a gated, manual act you recommend, not apply.

Canonical reference: `WORKFLOWS/dev-capture-audit.md`. This is the AI-trigger surface; that doc is the in-vault canon.

---

## Step 0 — Vault sentinel (^obs-004)
Read `_DIRECTIVES.md` from the mounted root; confirm `type: ai-os-brain` + `file: directives`. Mismatch/missing → halt and ask which folder is the vault. Write nothing.

## Step 1 — Resolve the project
The target is the folder with `CHAPTERS/` and/or `REFERENCE/` and a `DEV/` sibling. If CRE names one, use it; if exactly one qualifies, use it and say so; else ask. If the project has no `DEV/` tree → halt (this skill audits, it does not scaffold).

## Step 2 — Run the deterministic linter
```
python3 <skill>/scripts/audit_dev.py --project "<project-root>"
```
(run in the sandbox or locally; `--json` for machine output, `--strict` to fail on WARN). It emits a severity-ranked punch list and exits `0` clean · `1` ERROR findings · `2` gate failure.

**Freshness (^obs-122 / ^obs-123):** the script reads the filesystem it is given. Prefer running it where the files are **local and current** (the desktop install). A Cowork/Dropbox **sandbox mount can serve stale AND truncated** copies of recently-written files — both data and the script itself — so an in-sandbox run is **candidate-only**: confirm every finding (anchors, graduation parity, floors, footers, ledger) via the **file tools** (cloud-latest), not the bash mount, before reporting.

## Step 3 — (Optional) judgment pass — v2, opt-in
Only when CRE asks for the deeper read: fan a subagent over the routed entries for the judgment checks the script cannot do — **preserve-the-kind** (entries committing what CRE left open), **taste-drift** against `_DEV.md`, **routing sanity** (right bucket?). Report **candidates to verify**, never verdicts. **Know `^poe-007`:** draft-derived "settled" content (CRE directed harvesting a near-canon landed chapter) is legitimate — flag it to verify against the draft, not as a violation.

## Step 4 — Report
Present the punch list grouped by severity, **ERRORs first**, each with the file and a one-line recommended fix. Recommend; do not apply. Note which findings are likely intentional (e.g. a dangling `[[Witchwood]]` is a future-entry candidate, not a defect).

## Step 5 — Log
Append a dated `_CHANGELOG` entry under the `fiction` lane (file tools — DIR-005). File any genuinely new build surprise to `_OBSERVATIONS` (assign `^obs-NNN` by scanning the *whole* file via the file tools for the max + 1 — collision-safe, `^obs-122`).

---

## Files this skill writes — and must not
**Writes:** nothing in the `DEV/` tree. Only a `_CHANGELOG` note (+ optional `_OBSERVATIONS`/`_BACKLOG` follow-ups). The punch list is reported, not filed into the tree.
**Must NOT write:** any `DEV/` entry, floor, ledger, or poetics line; any auto-fix of a finding. Fixes are gated and manual.

## Build status
- **v1 (deterministic linter) — built:** `scripts/audit_dev.py` (stdlib only; sentinel-gated; exit 0/1/2). Checks: anchor uniqueness, graduation parity, intake invariant, floor pointers, frontmatter/DIR-004, placeholder leak, boundary tags, ledger form, project consistency, DEV-scoped dangling links, thin stubs, provenance footer.
- **v2 (judgment pass) — specced, not built:** the subagent fan-out for preserve-the-kind / taste-drift / routing sanity (Step 3).
- Propagation to the installed skill = desktop `pack-skills.ps1` + Save-skill repack (source-ahead).

## Stop conditions
- Sentinel fails → halt, ask which folder is the vault.
- No `DEV/` tree → halt; audit does not scaffold.
- Asked to FIX a finding → report + recommend; never auto-edit the tree.

## What this skill is NOT
- Not `dev-capture` (never routes or writes entries).
- Not `dev-readiness` (capture integrity, not content readiness).
- Not `link-audit` (DEV-scoped pre-filter, not the vault-wide authority).
- Not `skill-audit` (no installed-skill drift check).
