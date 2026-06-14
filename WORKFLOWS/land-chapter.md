---
type: workflow
name: land-chapter
trigger: land the chapter
aliases: [land the revision, promote and land, promote and sync, land it, full landing, land chapter N]
inputs: [the chapter's newest revisions/…-rev<N>.md (the thing being promoted), the chapter's draft.md, REFERENCE/ (canon target), the target StoryLine project under WRITING/STORYLINE/<Project>/ if one exists]
outputs: [draft.md landed from the newest revision, derived REFERENCE state (story-so-far/bible/threads + chapter continuity end-state), a StoryLine scene+codex mirror (when a StoryLine project exists), a single end-to-end landing report]
lane: fiction
status: active
last_updated: 2026-06-12
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]) that keep a REFERENCE/ folder. StoryLine mirroring runs only when the project has a WRITING/STORYLINE/<Project>/ target; otherwise that leg no-ops. First intended adopter — Witchwood.
pipeline_position: A thin orchestrator over the back half of the pipeline. It sequences three existing skills unchanged — [[WORKFLOWS/promote-revision]] → [[WORKFLOWS/canon-sync]] → [[WORKFLOWS/storyline-sync]] — so a single trigger takes a finished revision all the way to landed — draft updated, canon current, StoryLine mirrored. Modeled on [[WORKFLOWS/book-ingest]], which already chains canon-sync + storyline-sync after it lands an ingested chapter. Holds no logic of its own.
---

# WORKFLOW: Land the Chapter (promote → canon-sync → storyline-sync)

> One trigger that takes a chapter from "revision is ready" to **fully landed**. It runs [[WORKFLOWS/promote-revision]] (move the newest revision into `draft.md`), then [[WORKFLOWS/canon-sync]] (update REFERENCE + the chapter's continuity end-state from the landed draft), then [[WORKFLOWS/storyline-sync]] (regenerate the StoryLine scene + codex mirror) — in that order, because each consumes the output of the one before it. This closes the gap CRE hit: promoting a revision did **not** auto-trigger the two downstream syncs, so the canon and StoryLine views silently fell out of date after every promotion.

## Key principle — orchestration only, gates preserved

This workflow **holds no revision, canon, or StoryLine logic of its own.** It is a sequencer. Each leg is the existing skill, run unchanged, with its own stop conditions and gates intact:

- `promote-revision`'s lineage-mismatch gate (revision `source_slate` ≠ draft `source_slate`) still pauses the chain.
- `canon-sync`'s contradiction + dropped-fact gates still fire (handling depends on run mode — see below).
- `storyline-sync`'s author-tuned-conflict gate and its mandatory scene-intensity engine run (Step 3b) still apply.

If any leg halts on its own stop condition, the chain halts there and reports how far it got — it never skips a leg's gate to "push through." This is the same discipline as [[WORKFLOWS/book-ingest]], which chains the derive passes unchanged after scaffolding.

## Run modes — attended vs. unattended

The only behavior this orchestrator adds is how it treats a **gate** raised by a leg, and that turns on whether CRE is present:

- **Attended (default for an interactive trigger):** when a leg raises a gate that needs CRE's ruling (canon-sync contradiction/drop; storyline author-tuned conflict; promote lineage mismatch), **pause the chain and present it** for a ruling, then resume from where it paused.
- **Unattended (default when run from a scheduled task / no user present):** **defer, never guess** — log the gated item to the chapter's `open-loops.md` and the run report, and continue the chain. Non-conflicting writes still land. This matches the scheduled-task "produce a report" convention and book-ingest's unattended rule (principle 4 there). The lineage-mismatch gate in promote-revision is the one exception that **always** pauses/halts even unattended, because overwriting `draft.md` across a slate divergence is not safely reversible by deferral.

State the chosen mode at the top of the run report.

## Inputs

- **The chapter** — the per-chapter folder to land. If not named, ask (attended) or take the most recently revised chapter with an un-promoted revision (unattended), and state the pick.
- Everything else (the newest revision, REFERENCE state, the StoryLine target) is resolved by the individual legs.

## Outputs

| What | Destination | Produced by |
|---|---|---|
| Landed prose + rewritten lineage frontmatter (`status: register-revised`) | `<chapter>/draft.md` | promote-revision |
| Updated rolling canon + chapter end-state | `REFERENCE/story-so-far.md`, `bible.md`, `threads.md`, `<chapter>/continuity.md` | canon-sync |
| Regenerated scene + codex mirror (if a StoryLine project exists) | `WRITING/STORYLINE/<Project>/Scenes/`, `/Codex/…` | storyline-sync |
| Deferred gates (unattended) / ruled gates (attended) | `<chapter>/open-loops.md` + run report | this orchestrator |

## Steps

### Step 0 — Vault sentinel (`^obs-004`)
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (Each leg also runs this; the orchestrator runs it once up front so the chain fails fast.)

### Step 1 — Resolve chapter + preflight the chain
Resolve the chapter folder. Determine the run mode (attended vs. unattended) and record it. Quick preconditions before doing any work, so the chain fails fast rather than mid-way:
- The chapter has a `revisions/` with at least one `…-rev<N>.md` → else halt ("nothing to promote — run `register-pass` first").
- The chapter has a `draft.md` and the project has a `REFERENCE/` → else halt (convention not adopted).
- Detect whether a `WRITING/STORYLINE/<Project>/` target exists for this project; record it so Step 4 knows whether to run or no-op.

### Step 2 — promote-revision
Run [[WORKFLOWS/promote-revision]] for the chapter. On success, `draft.md` body = the newest revision's prose and frontmatter is rewritten (`status: register-revised`, keep `source_slate`, add `source_revision`). **If its lineage-mismatch gate fires, stop the chain here** and surface both slates (this gate pauses in every mode). Capture the promoted rev path/`source_revision` to carry into the report.

### Step 3 — canon-sync
Run [[WORKFLOWS/canon-sync]] against the just-landed `draft.md`, treating the promoted `source_revision` as the provenance tag (`CH<N> rev<M>`). Additions write automatically; the diff-based dropped-fact check and contradiction check run as normal. **Gate handling per run mode** (attended → pause for ruling; unattended → defer to `open-loops.md` + report, continue). Carry canon-sync's added/updated/deferred counts into the report.

### Step 4 — storyline-sync (conditional)
If Step 1 found a `WRITING/STORYLINE/<Project>/` target, run [[WORKFLOWS/storyline-sync]] against the landed `draft.md` (it reads the now-current `REFERENCE/bible.md`/`threads.md` from Step 3, which is exactly why it runs last). It segments scenes on hard breaks, **actually runs the scene-intensity engine** (Step 3b there — never eyeball `si_*`), writes scene files + Codex entries, and its author-tuned-conflict gate follows the run mode. If **no** StoryLine project exists, **skip this leg and say so in the report** ("no StoryLine project for <Project> — mirror step skipped"); skipping is not a failure.

### Step 5 — Verify (roll up each leg's self-test)
The orchestrator does not invent a new check — it confirms each leg reported success:
- promote-revision: `draft.md` `status: register-revised`, body matches the promoted rev, `source_revision` set.
- canon-sync: facts written carry the `(CH<N> rev<M>)` provenance; any contradictions/drops were ruled (attended) or deferred to `open-loops.md` (unattended), none silently dropped.
- storyline-sync (if run): its Step 6 self-test passed — all scene/codex YAML parses, wikilinks resolve, `sequence` unique, and every scene's `intensity == round(si_local/10)` with the `si_*` block present (proof the engine actually ran).

Confirm via the **file tools, not a bash read** (`^obs-014`). Any leg's self-test FAIL → halt, leave the chapter flagged in the report, do **not** log it as fully landed.

### Step 6 — Log
Write **one** consolidated landing entry (not three) to the chapter `changelog.md` and the vault [[_CHANGELOG]] (fiction lane): chapter landed, rev promoted, canon facts added/updated, conflicts ruled or deferred, StoryLine scenes/codex written (or skipped). File deferred gates to the chapter `open-loops.md`. File any new fragility to [[_OBSERVATIONS]]; add follow-ups to [[_BACKLOG]] if warranted. (DIR-003.)

### Step 7 — Report
Emit one end-to-end landing report: run mode; chapter + rev promoted; canon adds/updates and any deferred/ruled conflicts; StoryLine scenes + codex written (or "skipped — no project"); the verify PASS/FAIL roll-up; and an explicit list of anything left for CRE to rule. If a leg halted the chain, the report says which leg, why, and what state the chapter is in.

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- No `…-rev<N>.md` in `revisions/`, or no `draft.md`/`REFERENCE/` → halt before promoting (nothing to land / convention not adopted).
- promote-revision lineage mismatch → halt the chain, surface both slates (pauses in every mode).
- Any leg's own self-test FAILs → halt at that leg, report the partial state, do not mark the chapter landed.

## Logging
On completion append a single consolidated entry to [[_CHANGELOG]] (fiction lane) and the chapter's `changelog.md`; deferred gates to `open-loops.md`; fragilities to [[_OBSERVATIONS]]. (DIR-003.)

---

## Notes

- **Why this order is fixed.** canon-sync derives from the *landed* `draft.md`, so promote must run first. storyline-sync reads `REFERENCE/bible.md`/`threads.md` for its Codex + plotline tags, so it must run *after* canon-sync has refreshed them. The sequence is not configurable.
- **No new logic, by design.** Procedure changes belong in the three leg docs, not here. If a leg's behavior changes, this orchestrator inherits it automatically because it only ever *calls* the leg. (Same relationship book-ingest has to canon-sync/storyline-sync.)
- **Trigger ownership (ruled 2026-06-12).** `"land the chapter"` belongs to `land-chapter` — the full bundle is the truer owner of the phrase (canon-sync alone lands only the *canon*, not the draft or StoryLine). The alias was removed from [[WORKFLOWS/canon-sync]], which keeps `"sync the canon"`, `"canon sync"`, `"update the story so far"`, `"update the bible"`, `"sync chapter N"`. Note: the installed `canon-sync.skill` must be rebuilt + re-installed for its auto-trigger description to drop the phrase too (see packaging note).

## Skill packaging
Bundled as `SKILLS/land-chapter.skill` per the [[_SKILLS MAP#Cowork skills]] convention. The skill is **orchestration-only** — it carries the run-mode logic and the call sequence and shells out to the three existing skills; it must NOT duplicate their procedures (skill-audit would flag the drift). Install via "Save skill". `canon-sync.skill` was also rebuilt to drop the `"land the chapter"` trigger from its description; both need re-installing for the trigger surface to fully settle.
