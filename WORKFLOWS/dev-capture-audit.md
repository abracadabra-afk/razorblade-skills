---
type: workflow
name: dev-capture-audit
trigger: audit the dev capture
aliases: [audit the dev tree, dev-capture doctor, check the dev capture, dev capture audit, dev capture doctor]
inputs: [a project's DEV/ tree (the dev-capture output), read-only]
outputs: [a severity-ranked punch list of capture-integrity findings (ERROR / WARN / INFO); a dated _CHANGELOG note; NO edits to the DEV tree]
lane: fiction
status: draft
last_updated: 2026-06-24
revision_note: v1 — the deterministic structural linter (scripts/audit_dev.py). Judgment layer (preserve-the-kind / taste-drift / routing sanity) specced as v2, not built.
---

# WORKFLOW: dev-capture-audit

## When to use
After a `dev-capture` run or a batch of them, when you want to know whether the **capture mechanism did its job** — anchors unique, the graduation loop in parity, the intake invariant held, every entry floored, frontmatter valid, links resolving, nothing left half-routed. It is the read-only QA sibling of `dev-capture`. Run it on demand ("audit the dev capture"), as the closing step of a dev batch, or on a schedule.

It exists because the `DEV/` tree is something CRE **deliberately does not browse** (the same reason `dev-readiness` exists). That is exactly the condition under which silent, compounding defects breed — a duplicate `^poe` anchor sat invisibly until a manual review caught it (`^obs-122`). This skill is the thing that stares at the folder so CRE doesn't have to.

## The axis it owns (and its neighbors)
Three skills read the `DEV/` layer; keep them distinct.

| Skill | Question it answers | Layer |
|---|---|---|
| `dev-readiness` | Is the **content developed enough** to descend a layer? (what to flesh out) | content readiness |
| **`dev-capture-audit`** | Did the **capture mechanism stay structurally sound**? (links, anchors, floors, invariants, frontmatter) | capture integrity |
| `skill-audit` | Does the **installed skill match its source**? (cache drift) | skill currency |

Same folder, different questions. This skill never judges whether the story is good or developed — only whether the *bookkeeping the capture pipeline is responsible for* is intact.

## Governing principle — read-only, two seams
**Diagnose, never fix.** It writes nothing into the `DEV/` tree. It emits a punch list and a `_CHANGELOG` note; every fix (renumber an anchor, pull up a hedge, restore a floor) stays a gated, manual act — the `skill-audit` philosophy. A linter that auto-edits canon is a liability.

The work splits at exactly one seam — **deterministic vs. judgment** — the same seam as the blind-read clean room vs. the spec passes:

- **Deterministic layer (v1 — built):** everything a script can decide exactly. Fast, cheap, no LLM, runs every time. `scripts/audit_dev.py`. This is ~90% of the value at near-zero cost.
- **Judgment layer (v2 — specced, opt-in):** everything that needs a reader — preserve-the-kind, taste-drift against `_DEV.md`, routing sanity. An LLM/subagent pass. It can only ever produce **candidates to verify**, never verdicts, so it is opt-in and token-priced.

## The deterministic check catalog (v1)
`scripts/audit_dev.py` runs these against a project's `DEV/` tree:

| # | Check | Verifies | Severity |
|---|---|---|---|
| 1 | **Anchor uniqueness** | no two `### ^poe-NNN` share a number in `_POETICS.md` | ERROR |
| 2 | **Graduation parity** | every `promoted → _DEV_MAP` poetics entry has a matching `- ^poe-NNN` binding line in `_DEV_MAP` § Graduated patterns, and vice versa | ERROR |
| 3 | **Intake invariant** | `_intake/` holds only `README.md`, `_LEDGER.md`, `_audit/`, and `HOLD-*.md` — a stray transcript means a routed note was never swept/removed | ERROR |
| 4 | **Floor pointer** | every standard entry's `[[_intake/_audit/…]]` footer link resolves to a real audit file | ERROR |
| 5 | **Frontmatter / DIR-004** | every entry's frontmatter parses and carries `type:` + `project:` | ERROR |
| 6 | **Placeholder leak** | no `{{…}}` token survived routing | ERROR |
| 7 | **Boundary tag** | each standard entry declares `boundary: cued|inferred` (bucket files: `per-entry`) | WARN |
| 8 | **Ledger form** | `_LEDGER.md` has `surface_trigger`; each collision line carries a `[source:…]` pointer | WARN |
| 9 | **Project consistency** | each entry's `project:` matches the tree's project | WARN |
| 10 | **Dangling wikilink** | every `[[target]]` resolves to a DEV basename, a registry heading, or a declared alias (some misses are intentional future-entry candidates) | WARN |
| 11 | **Thin stub** | no standard entry is suspiciously short (a sign of a fabricated/empty entry or missing taste) | WARN |
| 12 | **Provenance footer** | each standard entry ends with a `Routed (…)` footer | INFO |

Exit codes: `0` clean · `1` ERROR findings (or WARN under `--strict`) · `2` gate failure (sentinel / no DEV tree).

## The judgment layer (v2 — specced, not built)
An opt-in LLM pass (a subagent fan-out, as run in the 2026-06-24 review) over the routed entries:
- **Preserve-the-kind:** entries that commit plot CRE left open. Reported as *candidates*, with the original line quoted.
- **Taste-drift:** entries whose taste reads off from `_DEV.md`'s anchor — surfaced for CRE, never rewritten.
- **Routing sanity:** did a segment land in the right bucket (character vs. sequence vs. lore).

## Two rules baked in from the field
1. **Anchor checks must read cloud-latest via the file tools, not the bash mount.** On a Dropbox vault the disk view trails the cloud; in the 2026-06-24 session a `grep` reported a stale max anchor while the file-tool read showed the true one (`^obs-122`). The script reports the freshness caveat in its header; the agent should ensure the tree is synced (or cross-check anchors via the file tools) before trusting anchor/graduation findings.
2. **The judgment layer must know `^poe-007`.** "Settled" back-half content that is **draft-derived** (CRE directing dev-capture to harvest a near-canon landed chapter) is legitimate — not a preserve-the-kind violation. The v2 pass reports such content as a candidate to *verify against the draft*, not as a defect, or it will false-positive exactly where the first review did.

## Composition — don't duplicate
The vault-wide broken-link authority is `link-audit`; this skill's dangling-link check is a fast **DEV-scoped** pre-filter, not a replacement — defer to `link-audit` for a full-vault pass. It does not re-audit skill-cache currency (`skill-audit`) or content readiness (`dev-readiness`).

## Steps
1. **Vault sentinel + resolve project.** Confirm `_DIRECTIVES.md` (`^obs-004`). Resolve the target project (a `CHAPTERS/`/`REFERENCE/` folder with a `DEV/` sibling); if none/many, ask.
2. **Run the deterministic linter** against a **synced, local** tree — the desktop where the Dropbox folder is current, *not* a lagging cloud/sandbox mount (which can serve stale **and truncated** copies of files written seconds earlier, producing false positives): `python3 <skill>/scripts/audit_dev.py --project "<project-root>"`. Capture the punch list. If you must run it in-sandbox, treat every finding as a **candidate** and confirm it via the file tools (cloud-latest) before reporting.
3. **(Optional) judgment pass.** On request, fan a subagent over the routed entries for the v2 checks; collect candidates (never verdicts).
4. **Report.** Present the punch list grouped by severity, ERRORs first, each with file + one-line fix. Recommend fixes; do not apply them.
5. **Log.** Append a dated `_CHANGELOG` note under the `fiction` lane (file tools — DIR-005). File any genuinely new build surprise to `_OBSERVATIONS`.

## Build order
1. **v1 — the deterministic linter** (`scripts/audit_dev.py`) — the smallest proving loop; run it against the live Witchwood tree first. **(built)**
2. **v2 — the judgment pass** — the subagent fan-out for preserve-the-kind / taste-drift / routing sanity, gated and opt-in. (specced)
3. Later: read the check rule-set from `_DEV_MAP` where possible so the linter doesn't rot as the convention moves.

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- No `DEV/` tree for the project → halt; this skill audits, it does not scaffold (run `dev-capture`'s scaffolder).
- It is asked to FIX a finding → report it, recommend the fix, and leave it for a gated manual edit. Never auto-edit the tree.

## What this skill is NOT
- Not `dev-capture` (it never routes or writes entries).
- Not `dev-readiness` (it judges capture integrity, not content readiness).
- Not `link-audit` (its link check is a DEV-scoped pre-filter; the vault-wide authority is `link-audit`).
- Not `skill-audit` (it does not check installed-skill drift).

## Logging
On completion, append an entry to [[_CHANGELOG]] under the `fiction` lane; file any new build surprise to [[_OBSERVATIONS]] with a `^obs-NNN` anchor (scan the whole file for the max + 1, via the file tools); add follow-up build tasks to [[_BACKLOG]].
