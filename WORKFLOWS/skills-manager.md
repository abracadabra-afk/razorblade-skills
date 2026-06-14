---
type: workflow
name: skills-manager
trigger: manage the skills
aliases: [run the skills manager, skills manager, what skills need work, refresh the skill registry, skills sweep]
inputs: [WORKFLOWS/*.md (canonical docs), SKILLS/*.skill (build artifacts), the installed skills cache, SKILLS/REGISTRY.md (the ledger), skill-audit (scanner), skill-creator (builder)]
outputs: [a refreshed SKILLS/REGISTRY.md, an Install queue (the only manual surface left for CRE), rebuilt .skill packages where the doc moved ahead, _CHANGELOG/_OBSERVATIONS/_BACKLOG entries]
lane: meta
status: active
last_updated: 2026-06-14
scope: Any vault that keeps skill sources (WORKFLOWS/*.md) + build artifacts (SKILLS/*.skill) and installs them into Cowork. Orchestration-only — holds no scan or build logic of its own; it sequences skill-audit and skill-creator and persists the result.
pipeline_position: The management layer ABOVE the two existing skill skills. skill-audit is the scanner (diagnose), skill-creator is the builder (fix); skills-manager sequences them, persists state in a registry, and surfaces the one irreducibly-manual step (install) as a queue.
---

# WORKFLOW: Skills Manager (the skill control tower)

> **Recommended path (lead):** Don't build a new engine — you already own ~80% of it. `skill-audit` (scanner) and `skill-creator` (builder) exist and work. The actual pain you named — *"hard to know what to do with so many elements to touch"* — is a **state-tracking gap, not a tooling gap**. Fix it with one new persistent artifact (`SKILLS/REGISTRY.md`) and a thin orchestrator that runs audit → updates the registry → rebuilds where the doc moved ahead → hands you a one-line **Install queue**. Run it on a schedule so drift never silently accumulates. That's the whole system.

---

## Why this exists

A Cowork skill lives in **three layers** that drift independently:

1. **Doc** — `WORKFLOWS/<name>.md` (human-edited source of truth)
2. **Package** — `SKILLS/<name>.skill` (built from the doc via skill-creator)
3. **Installed** — app-data cache, **what actually runs**, read-only

Getting an edit to actually run is a three-hop manual chain: **edit doc → rebuild package → install (Save skill)**. Drift appears silently at each hop, and today the *state of that drift is scattered* — across `^backlog-*-rebuild` lines, `_CHANGELOG` entries, and `_OBSERVATIONS`. The result is exactly what you described: a pile of elements to touch with no single place that says *what's done, what's pending, and whose move it is.*

Worse, the scatter goes stale. The 2026-06-13 audit (`^obs-055`, `^obs-054`, `^obs-050`) found multiple backlog items marked "rebuild needed" when the rebuild was **already done** and only the install remained — a done deliverable masquerading as open work. Without a single derived ledger, every dispatch risks re-doing finished work or jumping a gate.

## The design (four parts, one new)

### 1. The Registry — `SKILLS/REGISTRY.md` *(new — the keystone)*
One row per skill, **derived not hand-maintained**: lane, doc status, package present?, installed verdict (`OK` / `REINSTALL` / `REBUILD` / `UNBUILT` / `EXTERNAL`), last audited, **pending action**, and **whose move** (🤖 automatable vs 🧑 CRE-only). This is the single source of truth that replaces the scattered `^backlog-*-rebuild` lines. You glance at one table and know the state of every skill.

### 2. The Scanner — `skill-audit` *(exists; one extension)*
Already does the read-only three-layer reconciliation and prints a punch list. **Extension:** have it **write** its verdicts into the Registry instead of only printing them, and add the `^obs-054` check (flag any `WORKFLOWS/<name>.md` shorter than its packaged `SKILL.md` — a truncated doc that would ship a truncated skill if rebuilt). Keep its `^obs-014` mandatory file-tool confirmation of installed-side flags.

### 3. The Builder — `skill-creator` *(exists; the handoff target)*
When the Registry shows `REBUILD`, the manager hands the doc to skill-creator, rebuilds the `.skill` **bash-side on one filesystem** (`^obs-018` discipline), re-audits to confirm the package is now current, and flips the row `REBUILD → REINSTALL`.

### 4. The Install Queue — *(new — the human handoff)*
Install (Save skill) is the **only** step that must be CRE's — it's the trust boundary; nothing automates it. So the manager surfaces a dead-simple queue: *these N `.skill` files need Save-skill, nothing else.* That list is your entire manual surface area. Everything above it is automated.

## Steps (the orchestrator)

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md`; confirm `type: ai-os-brain` + `file: directives`. Mismatch → halt and ask which folder is the vault.

### Step 1 — Scan
Run `skill-audit` across all three layers. Honor its `^obs-014` guard (confirm any installed-side flag via the file tools, never a bash read alone) and its `^obs-054` doc-truncation check.

**Doc-vs-package staleness — content-based, never mtime (`^obs-060` #1).** The mtime heuristic gives false OKs in *both* directions: the 2026-06-14 scan reported `chapter-init` and `register-pass` as OK when a content grep of their packaged `SKILL.md` proved both stale (missing `weight`/Character-state and `voice-spec`/`Step 2.5`/`contamination` respectively). So a package is **never** ruled current on timestamps. Decide staleness by content, in this order:

1. **Preferred — `source_sha`.** If the package `SKILL.md` frontmatter carries `source_sha: <sha256>`, compare it to `sha256(WORKFLOWS/<name>.md)`. Equal → not stale. Differ → **REBUILD**. (Every rebuild in Step 3 stamps this, so packages become deterministically checkable over time.)
2. **Fallback — content probe (no `source_sha` yet).** Extract the doc's distinctive current sections/tokens (recent step names, new field names, new section headers — e.g. for register-pass: `Step 2.5`, `voice-spec`, `contamination`; for chapter-init: `weight: standard`, `Character state @ end`) and confirm each appears in the packaged `SKILL.md` (and bundled scripts/templates where the doc puts the behavior). Any expected token missing → **REBUILD**. Emit OK only after a positive content check — never from mtime alone.

**Package corruption — distinguish NUL-pad from real truncation (`^obs-060` #2).** Scan every file in each package for a **trailing run of NUL bytes** or a missing terminal newline on otherwise-complete text (the `^obs-018` atomic-write artifact: `land-chapter`/`workshop-chapter` carried 108/361 trailing NULs while their text ended cleanly on the final section). Flag these `NUL-PAD` — a safe 🤖 auto-clean (Step 3), **not** a doc problem. Reserve `BROKEN-PKG`/`DOC-REPAIR` (🧑) for text that ends **mid-word/mid-sentence** (genuine truncation). Report a NUL run explicitly as "obs-018 NUL padding (content complete; rebuild to clean)", never as "trailing whitespace."

### Step 2 — Refresh the Registry
Write the audit verdicts into `SKILLS/REGISTRY.md` — one row per skill, with pending action + whose-move. Derived fields overwrite; any CRE-authored note column is preserved (fill-gaps-only).

### Step 3 — Auto-fix what's automatable (🤖)
Three classes auto-fix; each ends by re-verifying the package and flipping the row to `REINSTALL` so it lands in the Step-4 queue. All build work is bash-side **on one filesystem** (`^obs-018`), and every write is verified *immediately* while still materialized (`^obs-062` — see below).

**(a) `NUL-PAD` — mechanical clean (no doc change).** Strip the trailing NUL run / normalize to a single terminal newline, repackage deterministically (ZIP, temp dir), confirm 0 NUL bytes and the text is byte-identical to the de-NUL'd original. This is the safest fix — the instruction text is already correct.

**(b) `REBUILD` — doc moved ahead, doc intact.** The packaged `SKILL.md` is **not** a copy of the doc; it's the authored skill surface. So rebuilding = **propagate the doc's current behavior into the package**, surgically:
  1. Read the canonical `WORKFLOWS/<name>.md` and the packaged `SKILL.md` (+ bundled `scripts/`,`templates/`).
  2. Identify exactly what the doc now specifies that the package lacks (the Step-1 content-probe tokens name it), and add/edit only those — sections in `SKILL.md`, and any script/template the doc puts behavior in (e.g. chapter-init's `templates/brief.md` weight field, `templates/continuity.md` Character-state section). Drop stray files that don't belong (e.g. a leftover `head.txt`).
  3. Where the doc describes a runnable artifact (scaffold script, etc.), exercise it (dry-run + a throwaway real run) to confirm it still works with the change.

**(c) `UNBUILT` doc that should be packaged** — first-time package via skill-creator.

**Stamp + verify-or-revert (hard gate, every rebuild).** After building, stamp `source_sha: sha256(WORKFLOWS/<name>.md)` into the package `SKILL.md` frontmatter (serialized per DIR-004). Then run the **ship gate** — refuse to copy the package into `SKILLS/` unless ALL pass: every Step-1 expected token now present · 0 NUL bytes in every package file · single terminal newline · frontmatter parses (real YAML load) · the de-NUL'd `SKILL.md` is not **shorter** than the prior package's by more than a small tolerance (a truncation guard — a shrinking rebuild is the `^obs-018`/`^obs-054` signature). Any failure → **do not ship**; keep the old package, leave the row at `REBUILD`/`BROKEN-PKG`, and hand it to CRE in Step 5. A bad unattended rebuild must never overwrite a working package.

**Skip** any row whose **doc** is truncated/incomplete (`^obs-054`) — that's a content repair (Step 5), not a rebuild.

### Step 4 — Emit the Install queue (🧑)
List exactly the `.skill` files now at `REINSTALL`. One line each: *"Save-skill `<name>.skill` — \<one-clause reason\>."* Nothing more. This is CRE's whole job.

### Step 5 — Hand back the CRE-only content work
Anything that requires authoring or ruling — a **truncated/incomplete doc** (`^obs-054`, e.g. storyline-sync.md), a **description/trigger-text** change (route to the `^obs-030` eval harness; rulings are CRE's), a **new skill from scratch** — is summarized as a handoff, never auto-edited. (Mirrors the `_ME` "AI executes; CRE creates" line: the manager moves bytes and runs builds, it doesn't author canonical procedure or creative content.)

### Step 6 — Log
On a real management run, refresh the Registry's `last_run`, append a one-line `_CHANGELOG` entry naming what was rebuilt and what's queued for install, and file any new fragility to `_OBSERVATIONS`. A quick status check stays read-only.

## Automation boundaries (what stays manual, and why)

| Step | Automatable? | Owner |
|---|---|---|
| Scan / diagnose (audit) | ✅ fully | 🤖 |
| Update the registry | ✅ fully | 🤖 |
| Rebuild a package from an **intact** doc | ✅ fully | 🤖 |
| Clean a `NUL-PAD` package (strip NULs, repackage) | ✅ fully | 🤖 |
| **Ship a rebuild that fails the verify gate** | ❌ never auto-ship | 🧑 CRE |
| **Install (Save skill)** | ❌ trust boundary | 🧑 CRE |
| **Repair a truncated/incomplete doc** | ❌ canonical content | 🧑 CRE |
| **Description/trigger-text tuning** | ⚙️ semi (eval harness proposes) | 🧑 CRE rules |
| **Author a brand-new skill** | ❌ creative procedure | 🧑 CRE + skill-creator |

The design deliberately automates everything up to two hard lines — the **install trust boundary** and the **content-authoring boundary** — and stops there.

## Cadence (so drift stops accumulating)

Add a scheduled task (e.g. weekly **"skills sweep"**, or piggyback an existing runner) that runs this manager unattended: re-scan, refresh the Registry, rebuild the automatable rows, and report the Install queue. This is what kills the `^obs-055` stale-open class — the Registry is always current, so a backlog line can never quietly claim "rebuild needed" after the rebuild already shipped. The backlog stops carrying per-skill `^*-rebuild` lines at all; it carries only *"CRE: clear the Install queue"* when the queue is non-empty.

## What this is NOT

- **Not a new scanner or builder.** It holds no audit or build logic; it sequences `skill-audit` and `skill-creator` unchanged (the `land-chapter` orchestration discipline — duplicating their logic would make skill-audit flag the drift).
- **Not an installer.** It can never click Save-skill; it only makes the queue trivially short.
- **Not a doc/skill author.** Truncation repair and new-skill authoring are handed back to CRE.

## Rulings (CRE, 2026-06-13)

All four open calls ruled — workflow flipped `status: active`:

1. **Registry IS the source of truth.** `SKILLS/REGISTRY.md` owns skill state; the standing `^backlog-*-rebuild` lines collapse into Registry rows. The backlog keeps only "clear the Install queue" when non-empty.
2. **The manager writes the Registry; `skill-audit` stays a pure read-only scanner.** The manager runs audit, then persists the verdicts (single-responsibility, the `land-chapter` discipline).
3. **Weekly cadence.** Scheduled task `skills-sweep` (Mondays) runs this workflow unattended: re-scan → refresh Registry → rebuild automatable rows → report the Install queue.
4. **DIR-004 graduated** — serialized derived-YAML is now a directive (`_DIRECTIVES#DIR-004`), retiring `^cand-dir-004-yaml`.

## Hardening (2026-06-14, `^obs-060` / `^obs-062`)

The first real auto-rebuild pass (4 packages, 2026-06-14) exposed why the previously-wired Step 3 had never fired and what makes unattended rebuilds safe:

- **The scanner, not the rebuilder, was the gap.** Step 3 already said "rebuild REBUILD rows," but the mtime check mis-verdicted the stale packages as OK, so Step 3 never saw them. Fix is in Step 1: **content/`source_sha`-based staleness, never mtime.** A rebuild step is worthless if the scan won't flag what's stale.
- **NUL-pad ≠ truncation.** Trailing-NUL packages still *run* (text complete) so they'd been logged "OK (runs)" and skipped. They are now their own auto-clean class (Step 3a) — `land-chapter`/`workshop-chapter` were exactly this.
- **`source_sha` is the durable backbone.** Once stamped, doc-vs-package is an exact comparison; the content-probe fallback only covers not-yet-stamped packages and retires itself as each is rebuilt.
- **Verify-or-revert is the safety that lets this run unattended.** Auto-authoring a package from an intact doc is in-bounds (CRE's boundaries table), but only because the ship gate refuses to overwrite a working package with one that lost a token, gained NULs, failed to parse, or shrank. The install Save remains CRE's review point.
- **`^obs-062` de-hydration discipline (Dropbox).** Writing `.skill` files into `SKILLS/` puts the whole folder into a sync state — the just-written files stay visible, the rest revert to cloud-only placeholders that bash AND the Obsidian API briefly can't read. So: verify each write the instant it lands (before de-hydration), keep a non-Dropbox temp copy of anything to re-read this run, and treat a post-write missing sibling as sync-lag, not loss. Build in a temp dir, copy the finished `.skill` into `SKILLS/`, verify, move on.
