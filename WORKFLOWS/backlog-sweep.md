---
type: workflow
name: backlog-sweep
trigger: sweep the backlog
aliases: [clean the backlog, tidy the backlog, backlog maintenance, dedupe the backlog]
inputs: [_BACKLOG.md, project backlog shards (WRITING/PROJECTS/*/backlog.md), TASKS/TASKS.md (open items — changelog-derive), _CHANGELOG.md (derive evidence)]
outputs: [a tidied _BACKLOG.md, a dated SYSTEM/history/_BACKLOG-archive file (+ pointer in _CHANGELOG), derived task closures in TASKS/TASKS.md (decisive evidence only), a sweep report, a gated "Needs CRE ruling" bin, observation-graduation candidates (max 5/sweep), observation triage stamps, a Standing queue block in _BACKLOG.md (lane counts + ranked-3 attended serving + agent-toggle recommendation), one replaced serving seed in TASKS/TASKS.md]
lane: writing-ops
status: active
last_updated: 2026-08-03
---

# WORKFLOW: backlog-sweep

## When to use

Maintenance pass over `_BACKLOG.md` to keep it lean and trustworthy. Triggered by **"sweep the backlog"** / **"clean the backlog"** / **"tidy the backlog"**, and by the weekly `backlog-sweep` scheduled task (Mondays, after `skills-sweep`). It removes accumulated cruft — completed items left checked in place, exact duplicates, malformed entries, drifted priority tags — and consolidates near-duplicate items, **gating every judgment call for CRE** rather than guessing.

This is the backlog sibling of `skills-manager` (skills) and `canon-sync` (canon): a derive-and-tidy pass with the house **"additions/safe-ops write; contradictions/judgment-calls gate"** discipline. It runs *after* `skills-sweep` on Mondays because `skills-sweep` appends follow-ups to `_BACKLOG.md`; the sweep then absorbs and normalizes them.

**Since 2026-07-17 the sweep also carries the changelog-derive over the open task list** (Step 3b): day-launch's derive pass only audits items *proposed into TODAY.md*, and week-shape derives only at re-shape, so work done outside a day plan never got its task checked off. The 07-17 ad-hoc sweep caught **5 stale-open items** this way (dec-002, og:image, two umbrellas, the WIW line). This step closes that gap on a weekly cadence.

## Inputs

`_BACKLOG.md` (the whole file). **Plus the per-project backlog shards** listed under `_BACKLOG.md` § Project pointers — `WRITING/PROJECTS/<PROJECT>/backlog.md` (Witchwood, Ghost River, Godsrift): sweep each shard with the identical safe-op/gate rules (carved 2026-06-29 backlog segmentation). Cross-references: `_CHANGELOG.md` (archive destination), `_OBSERVATIONS.md` (for `^obs-NNN` / `^anchor` validity), and `_SKILLS MAP.md` (to confirm a referenced workflow still exists before keeping a task that points at it).

## Outputs

1. A tidied `_BACKLOG.md` with safe ops applied.
2. Completed (`- [x]`) and canceled (`- [-]`) items archived **verbatim** to a dated `SYSTEM/history/_BACKLOG-archive-<date>.md`, with a one-line pointer in `_CHANGELOG.md` — full narratives no longer paste into the live changelog (2026-07-10 hygiene rule, [[SYSTEM/reports/2026-07-10-os-audit-improvements]]).
3. A **"Needs CRE ruling"** bin appended at the end of `_BACKLOG.md` listing every gated judgment call, one line each with the proposed action + reason.
4. A short sweep report (counts: archived / deduped / reformatted / gated / graduation candidates) appended to `_CHANGELOG.md`.
5. **Observation-graduation candidates** (Step 4b) — proposed directive text for CRE to ratify; never auto-written to `_DIRECTIVES`.
6. A **Standing queue** block near the top of `_BACKLOG.md` (Step 4c) — lane counts, a ranked serving of 3 attended items, and the `vault-backlog-agent` toggle recommendation — plus **one** replaced serving seed in `TASKS/TASKS.md` so the serving reaches a surface CRE actually opens.

## Write-mode policy (the core of this workflow)

**AUTO-APPLY (safe ops) — do these without asking:**

- **Archive closed items.** Move every `- [x]` (done) and `- [-]` (canceled) line out of `_BACKLOG.md` into `SYSTEM/history/_BACKLOG-archive-<date>.md` (create it, or append if this date's archive exists), preserving the item's text, anchor, and any "done YYYY-MM-DD" note **verbatim**; leave a one-line pointer in the sweep's `_CHANGELOG.md` entry. Do NOT archive open `- [ ]` items.
- **Merge exact duplicates.** When two `- [ ]` items are textually identical (or identical modulo whitespace/punctuation), keep one, delete the rest. Preserve the surviving line's anchor(s); if duplicates carried different anchors, keep all anchors on the survivor.
- **Normalize formatting.** Fix checkbox glyphs (`[ ]`/`[x]`/`[-]`), collapse stray blank lines, repair obviously mojibaked characters, and ensure each item sits under the correct lane heading (OS/Meta · Fiction · Writing Ops). Move a clearly-misfiled item to its right lane.
- **Fix priority-tag drift.** De-duplicate repeated tags on one line (e.g. `#p1 #p1` → `#p1`). Do NOT invent or change a priority that isn't there.
- **Derived task closures (Step 3b, decisive evidence only).** Check off an open `TASKS/TASKS.md` or `_BACKLOG.md` item when `_CHANGELOG.md` records its deliverable shipped/ruled **with named artifacts** (a commit, a file, a decision entry, a verified deploy). Append the evidence + a `closed via backlog-sweep changelog-derive` provenance comment to the closed line. This mirrors day-launch's derive-pass precedent — artifact-backed closures are safe-ops even unattended.
- **Refresh frontmatter** `last_updated`.
- **Regenerate the Standing queue block (Step 4c).** Counts and the ranked serving are *derived* — they lose no author intent and are fully reversible, so they write. **Replace the existing block; never append a second one.** The block *recommends* the `vault-backlog-agent` toggle and never performs it (a schedule change is `#gated` by this file's own Conventions).
- **Apply observation triage stamps (Step 4b).** Stamp `PARKED` / `NOT A RULE` on `_OBSERVATIONS.md` entries the sweep has considered and is not proposing. These record *that the sweep looked*, not a CRE ruling, so they are safe. `GRADUATED` stamps are NOT safe — they follow a CRE ruling and land in the same attended edit that writes the directive.

**GATE (judgment calls) — never apply; list in the "Needs CRE ruling" bin:**

- Merging **non-identical but overlapping** items (consolidation that changes wording or scope).
- **Dropping / canceling an open item** that looks stale, obsolete, or superseded (e.g. its `^obs` is graduated to a directive, its workflow shipped, its referenced file is gone). Propose; let CRE rule `[x]`/`[-]`.
- **Re-prioritizing** (adding/raising/lowering `#p1`/`#p2`/`#p3`).
- Splitting one overloaded item into several, or rewriting an item for clarity.
- **Compressing an oversized item** (over ~150 words — the 2026-07-10 *state + next action + pointers* format rule): propose the compressed text in the bin; CRE ratifies before it replaces the original.
- **Graduating an observation into a directive** (Step 4b output): always a proposal; `_DIRECTIVES.md` is never written by the sweep.
- **A derive closure that requires judgment** (Step 3b): the evidence is partial, the item would close as *superseded* rather than *done*, the completion is an off-vault hand action with no artifact, or an umbrella has open legs. Propose in the bin with the evidence cited; never guess a completion.
- Anything that touches a `#blocked`/`#waiting` item's meaning.

Rule of thumb: if the operation is reversible and loses no author intent, auto-apply it; if it requires judging whether CRE still wants something, gate it.

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). If it fails, **halt and report** — do not edit (`^obs-004`).

### Step 1 — Inventory
Read `_BACKLOG.md` in full. Build a list of every item with: lane, checkbox state, text, anchors, tags. Count open/done/canceled per lane.

### Step 2 — Classify each item
Tag each as: ARCHIVE (closed) · EXACT-DUP · REFORMAT · STALE? (open but possibly obsolete — verify against `_OBSERVATIONS`/`_SKILLS MAP`/filesystem) · CONSOLIDATE? (overlaps another) · KEEP.

### Step 3 — Apply safe ops
Execute every AUTO-APPLY operation from the policy above. Edit `_BACKLOG.md` with the **file tools (Read/Write/Edit), not `patch_vault_file`** (`^obs-020`/`^obs-014`). Move archived items into a single dated `_CHANGELOG.md` entry.

### Step 3b — Changelog-derive over the open task list (added 2026-07-17, CRE-ratified)
Read every `_CHANGELOG.md` entry dated since the last sweep **in full** (the day-launch 07-14 hardening: read before counting — summaries lie). Cross-reference each entry's shipped artifacts against every open `- [ ]` item in `TASKS/TASKS.md` (all sections) and `_BACKLOG.md`:

- **DECISIVE** (the changelog names the item's deliverable as shipped/ruled, with artifacts) → check off with provenance (safe-op, per the policy above).
- **PARTIAL / SUPERSEDED / JUDGMENT** (open legs remain, closure-as-superseded, off-vault hand action with no artifact) → one line in the gate bin with the evidence cited.
- **No evidence** → leave untouched; never infer completion from silence or plausibility.

Scope note: this derives *closures only* — it never edits an open item's text, priority, or scope (those remain Step 2/4 territory), and it never touches `TASKS/TODAY.md` (day-launch owns it).

### Step 4 — Assemble the gate bin
Append a `## Needs CRE ruling (backlog-sweep YYYY-MM-DD)` section to the bottom of `_BACKLOG.md`. One line per gated call: the item, the proposed action, and the one-clause reason. If a prior sweep's gate bin still has unruled lines, fold them in rather than stacking a second bin.

### Step 4b — Observation-graduation candidates (the learning-loop cadence, 2026-07-10; hardened 2026-07-19)

**This is the promotion pass. It runs here, weekly, on a cadence — not on request.** Read `_OBSERVATIONS.md` entries newer than the last sweep, **plus every entry carrying no triage stamp** (see below). For each viable candidate, add a proposal line to the gate bin: drafted directive text + scope + source `^obs` anchor. Also surface here: `DECISIONS/` entries whose `review-date` has passed, and pending `_WEIGHTS.md` proposals. **Never write `_DIRECTIVES.md`** — graduation is CRE's manual ruling (the `_OBSERVATIONS` header rule); on ratify, the directive lands in a follow-up attended edit. Replaces the retired `_SESSION START` §5 brain-curation prompt ([[SYSTEM/reports/2026-07-10-os-audit-improvements]], item 4).

**Triage stamps — the binding surface (added 2026-07-19, DIR-014).** The pass was previously unbounded and therefore skippable: "any older entry whose Candidate directive remains unactioned" is not computable without re-reading 600+ lines, so in practice only the since-last-sweep window got read, and older entries aged out silently. `^obs-014` sat ungraduated for **seven weeks** while `^obs-183` and `^obs-187` independently rediscovered the same finding. Every entry the sweep considers now gets one machine-visible stamp as its own last line, making "unactioned" a grep, not a judgment:

- `**GRADUATED <date> (CRE-ruled):** landed as DIR-NNN …` — promoted; never re-proposed.
- `**PARKED <date> — <recurrence condition>**` — deliberately not promoted, with the condition that would change that ("graduate if this recurs a third time", "graduate once the Phase 3 operator is live"). Most "none yet" candidate fields are really this.
- `**NOT A RULE <date> — <reason>**` — a method note, per-draft cleanup item, or code-level fix that will never be a directive.
- *no stamp* — never triaged; **always in scope for the next sweep.**

Apply stamps as a **safe op** (they record that the sweep looked, not what CRE ruled). Only `GRADUATED` requires a CRE ruling first.

**Two checks a single-window read cannot make** — run both against the *whole* file, not just the new entries:

1. **Recurrence check.** For each `PARKED` entry, test whether any newer observation satisfies its stated condition. If yes, it is no longer parked — propose it, and cite the recurrence. (`^obs-189` was a textbook recurrence of `^obs-185` and would have been caught this way.)
2. **Cluster check.** Test whether two or more untriaged entries describe the **same underlying failure**, however differently worded. A cluster is far stronger evidence than any single entry and should be proposed as one directive with all sources named. (`^obs-183` + `^obs-187` + `^obs-014` were one finding across seven weeks; `^obs-132` + `^obs-136` + `^obs-137` were one rule that no entry owned, two of them deferring to it as "already covered" — **that phrase is itself a cluster signal: it means the rule is unwritten.**)
3. **Wording-vs-state check (added 2026-08-03, CRE-ruled — DIR-009's announce-the-gap clause, `^obs-230`).** An open item's own worded state ("packaging pending", "install remaining", "blocked on X") is a snapshot nothing re-checks. Where the item names a checkable artifact — a `.skill` in the manifest, an installed skill, a scheduled task, a file — test the wording against the disk/manifest state and flag every contradiction as its own report line: *"item says X, disk says Y."* Six instances of this class were closed in one attended sweep (2026-08-03) after accumulating silently; the flag makes the class visible weekly instead.

**Bounded output.** Propose at most **5** directives per sweep, ranked by evidence strength (cluster or recurrence first, single-instance last), and state how many untriaged entries remain. An unbounded proposal list is one CRE will not read — which is how this step failed the first time.

### Step 4c — Standing queue + serving block (added 2026-08-03, CRE-ratified)

**Why this step exists.** The queue taxonomy in `_BACKLOG.md` § Conventions (`#unattended` / `#unattended-confirm` / `#gated` / `#desktop`, with `#gated` as the default for an untagged item) has always been *computable* — nobody ever computed it. So no surface ever told CRE what workload was waiting for which writer, and the standing question *"is it worth switching the unattended agent on?"* stayed a manual guess. This step answers both from tags that already exist. **It adds no new tagging burden.**

**Compute (open `- [ ]` items only, this file + every project shard):**

| Lane | Definition |
|---|---|
| **Agent** | `#unattended` + `#unattended-confirm` |
| **Attended** | everything else — explicit `#gated` **plus untagged items** (the stated default) |
| **Desktop** | `#desktop` — a **sub-count of Attended**, not a third lane; report it inside the attended figure, never added alongside it |

Do not double-count: `#desktop` items frequently also carry `#gated`.

**Rank the attended bucket by `(priority, age)`.** `#p1` → `#p2` → `#p3` → untagged; within each band, **oldest first**, using the `, YYYY-MM-DD` date carried in the item's anchor parenthetical. Age needs no new tag — it is already in every item. This exists because priority alone has stopped discriminating: at the 2026-08-03 measurement `#p2` held **63 of 131** open items against **4** `#p1`, so a serving ranked on `#p` alone is effectively unordered. **Exclude `#blocked` / `#waiting` items from the serving** (they are not actionable), but keep them in the counts.

**Serve exactly 3.** Not the ranked list — three items, each as: anchor · one-line what-it-is · **the next physical action already recorded in the item**. Never invent a next action; if an item's next action is missing, skip to the next candidate and note the gap. Three is the cap for the same reason day-launch caps its board — an unbounded serving is one CRE will not work.

**Emit the agent-lane line (rewired 2026-08-03 — `vault-backlog-agent` retired, CRE-ruled `^backlog-vaultbacklogagent-nodoc`).** There is currently **no unattended backlog executor**: the task was deleted 2026-08-03 (superseded; this sweep owns the maintenance half). Report the Agent-lane count as information only — *"Agent lane: N items tagged `#unattended`/`#unattended-confirm`; no executor exists."* If the lane grows enough to matter, flag it as a CRE decision (re-introduce an executor as a doc-backed task authored fresh — never resurrect the retired prompt). Do not recommend enabling a task that does not exist; probe live task state before writing any toggle line (DIR-010).

**Write it to two places:**

1. A `## Standing queue (backlog-sweep YYYY-MM-DD)` section in `_BACKLOG.md`, placed **immediately below § Project pointers** so it reads before the lane headings. **Replace** the prior block wholesale — never stack.
2. **One** seed item in `TASKS/TASKS.md`: `- [ ] Walk the backlog serving — 3 attended picks + N agent-lane ready (see _BACKLOG § Standing queue) win:ops #p2`. **Replace the existing seed if one is present; never append a second.** This is the surfacing half — a block only in `_BACKLOG` is a deferral onto a channel CRE does not routinely open (DIR-012 clause 4).

**Placement in the maintenance window (CRE-ruled 2026-08-03 — the wrinkle is closed).** The window moved from Monday to **Sunday afternoon** precisely so this serving lands *upstream* of the planning surfaces instead of a day late. Live order:

`skills-sweep` 13:05 → `task-audit` 13:53 → **`backlog-sweep` 14:38** → `vault-health` 15:39 → `link-audit` 16:21 → *(`week-shape-runner` 18:00)* → *(Monday `day-launch` 07:08)*

So the Standing queue block and its `TASKS.md` seed are both written **before** `week-shape-runner` composes the week proposal and well before Monday's `day-launch` builds the board — the serving reaches CRE on the surfaces he already opens, on the same cycle it was computed. **Two dependencies this ordering creates:** the sweep must still run *after* `skills-sweep` (it absorbs the follow-ups that run appends), and *before* `vault-health` (which rotates the brain docs this sweep reads). Do not re-time this task unattended — a schedule change is `#gated`; if the window has drifted, report it rather than fixing it.

### Step 5 — Report + log
Append a one-line dated entry to `_CHANGELOG.md` under writing-ops: counts archived / deduped / reformatted / gated, **plus the Step 4c lane counts and the three served anchors**, plus anything notable. File any new fragility to `_OBSERVATIONS.md` with a `^obs-NNN` anchor. If nothing changed since the last sweep, say so in one line and keep the run read-only.

## Stop conditions

- Vault sentinel fails (Step 0) → halt, report.
- The file tools can't write `_BACKLOG.md` → halt, report; never fall back to `patch_vault_file`.
- More than ~⅓ of open items would land in the gate bin → apply safe ops only, then surface that the backlog likely needs a CRE working session rather than a routine sweep.

## Logging

On completion, append to `_CHANGELOG.md` (writing-ops lane). Unattended runs follow the scheduled-task close discipline (changelog + observations + any follow-ups). Apply all active `_DIRECTIVES` (esp. DIR-001 secrets, DIR-002 loading order, DIR-003 log every session).
