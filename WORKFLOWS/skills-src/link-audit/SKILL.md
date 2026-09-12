---
name: link-audit
description: 'Audit an Obsidian vault for broken references - dangling [[wikilinks]], ![[embeds]] and [md](links), plus broken #headings and ^block-anchors - and print a categorized punch list. Use when CRE asks to "run the link doctor", "check for broken links", "audit the links", "find dangling links/references", "are there broken wikilinks", or after a restructure/move to verify nothing dangles. Read-only apart from its report and the DIR-003 brain-log lines - it diagnoses and hands CRE a fix list, never edits a content note. Sibling of skill-audit (audits skills) and backlog-sweep. Do NOT use it to FIX links (manual/separate pass), to audit skills (skill-audit), or to sweep the backlog (backlog-sweep).'
---

# Link Audit (the link doctor)

Read-only reference-integrity audit of an Obsidian vault. The script resolves every
link and does the classification; you read its arithmetic, check the tree, and hand
CRE a short actionable list. Canonical doc: `WORKFLOWS/link-audit.md`.

**The deliverable is the net actionable count, not the raw finding count.** Three
isolated runs on 2026-09-11 produced byte-identical resolver output and net counts
of ~15 / ~40 / ~1,430, because each improvised its own classifier over 1,672 raw
findings. The classification now lives in the script. Do not re-derive it by hand.

## What it reports

**Actionable** — the only tier that goes in front of CRE:
- **DANGLING** — target file not found anywhere.
- **BROKEN-ANCHOR** — file resolves, but the `^block-id` is missing in it.
- **BROKEN-HEADING** — file resolves, but the `#heading` is missing in it.
- **INTEGRITY** — a scanned note's own bytes carry NUL/control/trailing-pad bytes.
- **SUSPECT-STALE** — a target read back truncated, so its anchor set is untrustworthy;
  any BROKEN-* off it is downgraded to this advisory and the run prints a
  "MOUNT MAY BE STALE" banner (the `^obs-073` guard).

**Benign, suppressed by default** (`--benign` to list, always counted in the header):
FOLDER-LINK · HOUSE-PREFIX · CLIPPING · TEMPLATE · AMBIGUOUS. Each is a real
unresolved link that is not breakage. Named in `link_audit.py`'s docstring.

## Step 1 — Vault sentinel
Read `_DIRECTIVES.md` from the mounted vault root and confirm its frontmatter has
`type: ai-os-brain` and `file: directives` (the `^obs-004` guard). Missing or
mismatched → halt and ask which folder is the vault. Write nothing.

## Step 2 — Run the resolver
`python3 link_audit.py --vault <VAULT>` (bundled alongside this SKILL.md).
Flags: `--all` (quarantined zones), `--benign` (the benign classes), `--ambiguous`,
`--json`.

Per DIR-020 the first call is a **live entitlement probe**. If bash is denied, this
skill is **bash-blocked** — say so and stop. There is no file-tool fallback: the
resolver's whole value is that it is deterministic, and a hand-walk of ~2,000 links
is exactly the improvisation this skill exists to remove.

Path resolution runs four layers in Obsidian's order — root-relative, source-relative,
unique path suffix, then shortest-path-among-several → AMBIGUOUS. A link at a
directory resolves to FOLDER-LINK. Before 2026-09-11 only layer one existed, and its
absence generated ~95% of this skill's lifetime output (`^obs-287`).

## Step 3 — Freshness guard (`^obs-014` / `^obs-073`)
The bash/Dropbox mount serves **stale or truncated** views of files written, moved,
or deleted this session, and a file-tools write does not heal the bash view. Truncated
targets self-flag as `SUSPECT-STALE` behind a banner. **Run in a FRESH session**, and
confirm any surprising DANGLING through the **file tools** before reporting it real —
never with bash, which reads the same mount (DIR-005).

> There is no live-view mitigation. The old `--rest-base` / `--rest-key` path is
> **gone** — flags removed from the script, plugin removed from the vault 2026-07-13
> under DIR-001 (its `data.json` held a full-access apiKey and a TLS private key).
> **Never pass those flags, never set `OBSIDIAN_REST_BASE`/`OBSIDIAN_API_KEY`, and
> never go looking for that key** — retrieving it re-introduces the exact secret
> DIR-001 had removed. Treat mount staleness as present and unmitigated.

## Step 3b — Probe the scheduler before blaming an upstream pass (`^obs-246`)
This pass runs last in the Sunday window and is tempted to reason about the passes
before it. **An absent report or `_CHANGELOG` entry is not evidence a pass didn't
run** — the 2026-08-09 run inferred exactly that about `vault-health`, reasonably and
wrongly, and downgraded its own findings while `vault-health` had fired and exited
silently. Before asserting anything: probe `lastRunAt` via `list_scheduled_tasks`, and
check the receipt surface (`SYSTEM/reports/vault-health-runs.md`, written every run
including no-ops). A populated `lastRunAt` with no receipt means the run **failed** —
a finding to report, not a reason to downgrade your own.

## Step 4 — Read the arithmetic; do not re-derive it
The script prints one line:

```
net ACTIONABLE: 17   (benign suppressed: {...} | quarantined: 156 |
                      ambiguous-fragment: 307 | self-check caught: 0)
```

That **is** the triage — suppress resolver-limitation hits, drop ratified
house-convention headings, subtract the folder-link / clipping / template classes,
report the net. Your job is to read it, not to redo it.

- **Report the net as the headline.** Never lead with the raw finding count.
- **`self-check caught: N` where N > 0 is a defect in this script**, not a finding.
  Those items are pulled from section A automatically. Report the count and the
  reason; do not list them as breakage and do not hand CRE fixes for them.
- **Do not move an item between bins by hand.** A misclassification is a script
  change, so that the next run inherits it. Hand-suppression is how the ~15/~40/~1,430
  spread happened.
- **Sanity band.** The vault has sat near ~19 net actionable since 2026-09-06. A run
  returning hundreds has a resolver regression, not a link crisis — say so and stop.

## Step 5 — Check the tree before writing anything up (DIR-011 / `_ME`)
For each principal finding, search `_BACKLOG.md` and `_OBSERVATIONS.md` for an
existing anchor **before** putting it in front of CRE. A settled call stays settled:
a tree-answered item is presented as *"resolved against `^anchor` — confirm"*, one
tap, never as a fresh open question. The presenting pass owns this research; never
assume an earlier pass did it.

## Step 6 — Hand off
Write-up goes to **`SYSTEM/reports/<date>-link-audit.md`** (the SYSTEM convention —
agents write reports there, never to the vault root). Shape it outcome-first: the net
count, the actionable list, the benign classes named with their counts, and one
recommended path. That shape was right in all three test runs — keep it.

**Write surface, exhaustively:** that report, plus the DIR-003 brain-log lines — a
one-line `_CHANGELOG` entry (meta lane, top-insert) and any new fragility to
`_OBSERVATIONS` (`^obs-NNN`, re-scan max anchor before write, re-read after). Those
two logs are the **one bounded exception** to read-only, because DIR-003 requires them
of every non-trivial session. **Nothing else** — no content note, no fix, ever. Fixes
are manual or a separate pass.

## Stop conditions
- Sentinel fails → halt, ask which folder is the vault.
- Bash denied → **bash-blocked**; report and stop (DIR-020).
- Resolver exits 2 (scanned <50% of the vault) → report the refusal, not a verdict.
  A "clean" result off an empty scan is worse than a crash (`^obs-245`).
- Zero actionable → report "no broken references," name the benign counts, stop.

## What this run did NOT check (DIR-018)
State these in the report rather than letting the net count imply more than it proves:
- **Obsidian's live resolution.** The four layers match Obsidian's documented rules
  and the vault's landed record; no Obsidian instance verified them.
- **The benign classes member-by-member.** They are suppressed by rule, not audited.
  After a restructure, re-run with `--benign` before trusting them.
- **AMBIGUOUS and `ambiguous-fragment`.** Counted, never resolved. A link matching
  several files may still land somewhere the author did not intend.
- **Quarantined zones.** `--all` to see them; expected to dangle by design.
