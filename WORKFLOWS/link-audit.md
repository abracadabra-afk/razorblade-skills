---
type: workflow
name: link-audit
trigger: run the link doctor
aliases: [check for broken links, audit the links, find dangling links, find broken references, link audit, reference doctor]
inputs: [the mounted vault root]
outputs: [SYSTEM/reports/<date>-link-audit.md - a categorized punch list of dangling links / broken anchors / broken headings; the DIR-003 brain-log lines]
lane: meta
status: active
last_updated: 2026-09-11
---

# WORKFLOW: link-audit (the link doctor)

## When to use
CRE says **"run the link doctor"** / "check for broken links" / "find dangling references," or wants the vault swept for reference rot — especially **after a restructure or a batch of moves**. The reference sibling of `skill-audit` (skills) and `backlog-sweep` (the backlog): **read-only apart from its report and the DIR-003 brain-log lines** (§ Write surface), it diagnoses and hands CRE a fix list; it never edits a content note.

## What it checks
Scans every note for `[[wikilinks]]`, `![[embeds]]`, and `[md](links)` and resolves each against the real file index, plus heading/block-anchor indices.

**Actionable** — the only tier that reaches CRE: `DANGLING` · `BROKEN-ANCHOR` · `BROKEN-HEADING` · `INTEGRITY` (a scanned note's own bytes carry NUL/control/trailing-pad) · `SUSPECT-STALE`.

**Benign, suppressed by default** (`--benign` lists them; always counted in the header line): `FOLDER-LINK` · `HOUSE-PREFIX` · `CLIPPING` · `TEMPLATE` · `AMBIGUOUS`. Each is a genuinely unresolved link that is not breakage. Full definitions in `link_audit.py`'s docstring — that is the record, this is the pointer.

The actionable kinds:
- **DANGLING** — target file not found anywhere.
- **BROKEN-ANCHOR** — file resolves, but the `^block-id` doesn't exist in it.
- **BROKEN-HEADING** — file resolves, but the `#heading` doesn't exist in it.
- **AMBIGUOUS** (info, off by default) — a basename matches >1 file and none in the same folder; Obsidian still resolves to the shortest path, so this is low-priority.
- **SUSPECT-STALE** — a target file read back **truncated** (NUL bytes / partial), so its anchor/heading index can't be trusted; any `BROKEN-ANCHOR`/`BROKEN-HEADING` off it is downgraded to this advisory instead of a confident false finding, and the run prints a top-level "MOUNT MAY BE STALE" banner. The `^obs-073` guard.

## Resolution rules (matches Obsidian)
- Bare `[[Note]]` resolves by **basename**, with a **folder-proximity tie-break** (a same-folder match wins — so `[[open-loops]]` resolves to the sibling, not a random chapter's).
- **`[[folder/Note]]` runs four layers, in Obsidian's order** (rebuilt 2026-09-11, `^obs-287` / `^backlog-linkaudit-path-resolution` — **closed**): (1) vault-root-relative, (2) **source-relative** to the linking note's folder, (3) **unique path suffix** (Obsidian's shortest-path-when-possible rule), (4) suffix matching several files → `AMBIGUOUS`, resolved to the shortest, never `DANGLING`. A target that is a **directory** → `FOLDER-LINK`, the vault's navigation convention, not breakage. Case-insensitive throughout — the source path is lowered before the layer-2 join, and forgetting that is worse than skipping the layer: the link falls through to layer 3 and matches the *wrong project's* file, so the heading check then runs against a file the author never linked (327 phantom BROKEN-HEADINGs, caught by the closing self-check on its first run).
- Wikilink targets are **unescaped (`\|` → `|`) before the alias split** — 99 links live inside markdown tables, where the pipe must be escaped, and splitting the raw text left a trailing backslash on every one.
- Links inside inline code or fenced code blocks are **ignored** (so `` `[[wikilinks]]` `` examples in docs don't false-flag).
- `#heading` / `#^block` fragments are checked only when the target file is readable, and matched on the **full heading text**. A heading's trailing **provenance stamp** (`## Sanctuaries along the trail *(CRE, 2026-06-29)*`) is **not** stripped: tried 2026-09-11 and reverted, because Obsidian anchors on the full text, so a cite omitting the stamp genuinely will not navigate — and the 2026-09-06 run already ruled exactly those two cites real (`^backlog-linkaudit-fixlist-2026-09-06`). The 08-19 prefix ruling is scoped to `_DIRECTIVES` / `_SKILLS MAP` and does not reach a DEV lore note.

## Ratified house conventions — NOT findings (CRE-ruled 2026-08-19, Monday gate-bin pass)

> **Enforced in the resolver since 2026-09-11.** These were prose-only, so they came back as findings on every run — all three 09-11 test runs re-reported all 32, two of them recommending the exact find-and-replace CRE ruled against. The script now emits them as the benign class `HOUSE-PREFIX` (suppressed by default, `--benign` to list). `^backlog-linkaudit-prefix-accept` **closed**. The prose below stays because the *reason* has to travel with the rule — an agent that sees only the rule will be tempted to re-litigate it.

- **Heading-PREFIX cites on the OS anchors are house style.** `[[_DIRECTIVES#DIR-005]]`, `[[_DIRECTIVES#DIR-015]]`, `[[_SKILLS MAP#Fiction]]`, `[[_SKILLS MAP#Cowork skills]]`, `[[_SKILLS MAP#Cross-cutting rules]]` and their kin cite a heading by its **stable identifier prefix**, not its full text. They render fine; only exact-heading navigation fails. **Do not report them.** Basis for the ruling: the full heading text is long and *gets amended* — DIR-005's heading has been amended four times — so pinning 32 cites to full heading text guarantees they break again on the next amendment. This is DIR-014's own logic (widen the **exact** layer, never chase the drift). Accept a prefix match on `_DIRECTIVES` and `_SKILLS MAP` targets. Closed as `^backlog-heading-prefix-cites`; resolver change tracked at `^backlog-linkaudit-prefix-accept`.
- **Bare `[[items#…]]` is retired.** All 48 instances were rewritten 2026-08-19 to the vault-root-relative form `[[WRITING/PROJECTS/<PROJECT>/DEV/registry/items#Heading|Heading]]`. A bare `[[items#…]]` is now a **real** finding again — report it.

## Steps
1. **Vault sentinel** — confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`); the `^obs-004` guard. Write nothing.
2. **Run** the bundled resolver: `python3 link_audit.py --vault <VAULT>` (add `--all` for the quarantined zones, `--benign` for the benign classes, `--ambiguous` for the info tier, `--json` for machine output). Per DIR-020 this first bash call is a **live entitlement probe**, not an assumption — a denial is an expected branch, see Stop conditions.

   > ⚠️ **The `--rest-base` / `--rest-key` path is RETIRED (corrected 2026-08-03).** This step used to recommend reading targets through Obsidian's Local REST API for freshness. **That plugin was removed from the vault on 2026-07-13** under DIR-001 — its `data.json` held a 64-char `apiKey` granting full read/write over the vault plus a TLS private key, and removal (not rotation) was the ruled fix, since `CLAUDE.md` makes the file tools the default read path. **Do not pass `--rest-base`/`--rest-key`, do not set `OBSIDIAN_REST_BASE`/`OBSIDIAN_API_KEY`, and never go looking for that key** — retrieving it would re-introduce the exact secret DIR-001 had removed. **The flags were removed from the script 2026-08-10** (`^backlog-linkaudit-dead-rest-flags`) — passing them is now an argparse error, not a silent no-op.
   >
   > **The freshness mitigation is therefore Step 3 alone**: `SUSPECT-STALE` self-flagging, a fresh session, and file-tool confirmation of any surprising DANGLING before it is reported as real. Treat mount staleness as *present and unmitigated*, not solved.
3. **Apply the `^obs-014`/`^obs-073` guard** — a flagged-missing file can be a stale-mount artifact, and a recently-written file can read back **truncated** (the bash mount serves stale/partial views of files written/moved/deleted that session; a file-tools write does not heal it). **There is no live-view mitigation** — the `--rest-base` path named above is retired and its flags no longer exist in the script. What remains: truncated reads self-flag as `SUSPECT-STALE` behind a banner; **run in a FRESH session**; and confirm any surprising DANGLING through the **file tools** before reporting it real — never with bash, which reads the same mount (DIR-005).
3b. **Never infer a missed upstream run from absent artifacts — probe the scheduler first (added 2026-08-10, `^obs-246` / `^backlog-vaulthealth-silent-noop`).** This pass runs LAST in the Sunday window and is tempted to reason about the passes before it (esp. `vault-health`, whose rotation changes what this pass sees). An absent report or `_CHANGELOG` entry is **not** evidence a pass didn't run — the 2026-08-09 run inferred exactly that about `vault-health`, reasonably and wrongly, and downgraded its own findings to provisional while `vault-health` had fired and exited silently. Before asserting anything about an upstream pass: (i) probe `lastRunAt` via `list_scheduled_tasks`; (ii) check its receipt surface — `vault-health` writes `SYSTEM/reports/vault-health-runs.md` every run, including no-ops. A populated `lastRunAt` with no receipt means **the run failed**, which is a finding to report, not a reason to downgrade your own.
4. **Read the arithmetic; do not re-derive it.** The categorization *is* the deliverable, and improvising it fresh each run is where 100% of the run-to-run inconsistency lived — three isolated runs on 2026-09-11 produced byte-identical resolver output and net actionable counts of **~15 / ~40 / ~1,430**. It is executable now. The script prints one line:

   ```
   net ACTIONABLE: 17   (benign suppressed: {...} | quarantined: 156 |
                         ambiguous-fragment: 307 | self-check caught: 0)
   ```

   That line is the suppression arithmetic in full: resolver-limitation hits suppressed, ratified house-convention headings dropped, folder-link / clipping / template classes subtracted, net reported. **Lead with the net, never the raw count.** `self-check caught: N > 0` is a **defect in this script**, not a finding — those items are pulled from the actionable section automatically; report the count and reason, never as breakage. **Never move an item between bins by hand** — a misclassification is a script change, so the next run inherits it. **Sanity band:** the vault has sat near ~19 net since 2026-09-06; a run returning hundreds has a resolver regression, not a link crisis.
5. **Check the tree before the write-up** (DIR-011, and `_ME`'s *a settled call stays settled*). For each principal finding, search `_BACKLOG` and `_OBSERVATIONS` for an existing anchor **before** it reaches CRE. Tree-answered → present as *"resolved against `^anchor` — confirm"*, one tap, never as a fresh open question. The presenting pass owns that research; never assume an earlier pass did it. (The 2026-09-06 run diagnosed this gap in itself; the 09-11 test confirmed it.)
6. **Hand off.** Fixes are manual or a separate pass — this skill **never edits a content note**.

## Quarantine (reported separately, `--all` to show)
`GRAVEYARD/`, `WORKFLOWS/evals/`, `SYSTEM/history/`, `SYSTEM/skill-tests/`, `_CHANGELOG.md`, `_OBSERVATIONS.md`, the migration plan, and backup files — dangling references there are expected (cold storage / historical record / test fixtures).

`SYSTEM/skill-tests/` added 2026-09-11: `skill-test` copies real notes into per-run fixture trees, so their links double-count ones already scanned at the real path — and the net moves whenever a test runs, which is the one thing a baseline must not do.

## Stop conditions
- Sentinel fails → halt, ask which folder is the vault.
- **Bash denied → bash-blocked; report and stop** (DIR-020). There is no file-tool fallback: the resolver's whole value is determinism, and a hand-walk of ~2,000 links is the improvisation this skill exists to remove.
- Resolver exits 2 (scanned <50% of the vault) → report the refusal, never a verdict. A "clean" result off an empty scan is worse than a crash (`^obs-245`).
- Zero actionable → report "no broken references," name the benign counts, stop.

## Write surface (exhaustive) — the one bounded exception to read-only
The write-up goes to **`SYSTEM/reports/<date>-link-audit.md`** (the SYSTEM convention: agents write reports there, never to the vault root). Plus the DIR-003 brain-log lines — a one-line `_CHANGELOG` entry (meta lane, top-insert) with the **net** count, and any new fragility to `_OBSERVATIONS` (`^obs-NNN`; re-scan max anchor before write, re-read after).

Those two logs are the **only** exception to "never edits a note," and it is named here because DIR-003 requires them of every non-trivial session — leaving the contradiction unresolved is why the 2026-09-11 test's no-outside-writes condition held only on a brief that overrode this step. **Nothing else is writable.** No content note, no fix, ever.

## What a run does NOT check (DIR-018)
State these in the report rather than letting the net count imply more than it proves: **Obsidian's live resolution** (the four layers match its documented rules and the vault's landed record; no Obsidian instance verified them) · **the benign classes member-by-member** (suppressed by rule, not audited — re-run with `--benign` after a restructure) · **AMBIGUOUS and `ambiguous-fragment`** (counted, never resolved; a link matching several files may still land somewhere unintended) · **quarantined zones** (`--all` to see them; expected to dangle by design).
