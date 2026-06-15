---
name: land-chapter
description: Land a finished chapter end-to-end in one pass — promote the newest revision into draft.md, then sync the canon, then mirror to StoryLine — by chaining three existing skills in order. Use whenever the author asks to "land the chapter," "land the revision," "promote and land," "promote and sync," or "land it," or wants a chapter taken all the way from a ready revision to fully landed (draft updated, REFERENCE canon current, StoryLine mirror regenerated) without running three separate triggers. It is an ORCHESTRATOR — it holds no revision, canon, or StoryLine logic of its own; it runs promote-revision → canon-sync → storyline-sync unchanged, preserving every leg's gates. Do NOT use it to revise prose (register-pass) or to run just one leg — reach for promote-revision, canon-sync, or storyline-sync directly when you want only that step. Requires the per-chapter folder convention + a REFERENCE/ folder; the StoryLine leg no-ops when the project has no StoryLine project.
---

# Land the Chapter

You are landing a chapter end-to-end. The author has a finished **revision** in a chapter's `revisions/` and wants it taken all the way to landed in one move: the revision promoted into `draft.md`, the project's rolling canon brought current from that landed draft, and (if the project has a StoryLine mirror) the StoryLine scene + codex files regenerated. Before this skill existed, that was three separate triggers, and skipping the last two silently let the canon and StoryLine views fall out of date after every promotion. You close that gap.

You hold **no craft, canon, or StoryLine opinion of your own.** You are a sequencer. Each leg is an existing skill, run unchanged, with its own stop conditions and gates intact:

- `promote-revision` — moves the newest revision into `draft.md` and rewrites the lineage frontmatter.
- `canon-sync` — derives REFERENCE state (story-so-far / bible / threads) + the chapter's continuity end-state from the landed draft.
- `storyline-sync` — regenerates the StoryLine scene + codex mirror (and runs the scene-intensity engine inside itself).

You run them **in that fixed order**, because each consumes the output of the one before it: canon-sync needs the landed `draft.md`, and storyline-sync reads the bible/threads that canon-sync just refreshed. The order is not configurable. If any leg halts on its own stop condition, you halt there and report how far you got — you never skip a leg's gate to push through. This is the same discipline `book-ingest` uses when it chains the derive passes.

## Run modes — attended vs. unattended

The only behavior you add is how you treat a **gate** a leg raises, and that turns on whether the author is present:

- **Attended (default for an interactive trigger):** when a leg raises a gate that needs a ruling (canon-sync contradiction/dropped-fact; storyline author-tuned conflict; promote lineage mismatch), **pause the chain, present it, get the ruling, then resume** from where you paused.
- **Unattended (default when run from a scheduled task / no user present):** **defer, never guess** — log the gated item to the chapter's `open-loops.md` and the run report, and continue. Non-conflicting writes still land. The promote-revision **lineage-mismatch** gate is the one exception that pauses/halts even unattended, because overwriting `draft.md` across a slate divergence is not safely reversible by deferral.

State the chosen mode at the top of your report.

---

## Step 0 — Vault sentinel check (`^obs-004`)

Before anything else, confirm you are pointed at the right vault — the gate every skill in this family shares.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. If it's missing or the frontmatter doesn't match, **halt and ask** which folder is the vault. Do not scaffold anything; do not write anywhere.

Each leg also runs this; you run it once up front so the chain fails fast. Pass it before locating anything.

---

## Step 1 — Resolve the chapter and preflight the chain

Resolve the chapter folder (a per-chapter folder with `slate/`, `revisions/`, a `draft.md`). If the author named a chapter without a path, search for the matching folder; if several match, ask (attended) or take the most recently revised chapter with an un-promoted revision (unattended) and state the pick.

Determine and record the **run mode** (attended vs. unattended). Then check preconditions so the chain fails fast rather than mid-way:

- The chapter's `revisions/` holds at least one `…-rev<N>.md` passage → else **halt** ("nothing to promote — run `register-pass` first").
- The chapter has a `draft.md` and the project has a `REFERENCE/` folder → else **halt** (convention not adopted).
- Detect whether a `WRITING/STORYLINE/<Project>/` target exists for this project; record it so Step 4 knows whether to run the mirror or no-op.

---

## Step 2 — Promote the revision

Run the **promote-revision** procedure for the chapter. On success, `draft.md`'s body becomes the newest revision's prose and its frontmatter is rewritten (`status: register-revised`, keep `source_slate`, add `source_revision`). Capture the promoted rev path / `source_revision` to carry into the report.

**If promote-revision's lineage-mismatch gate fires** (the revision's `source_slate` ≠ the draft's, and the draft is not a scaffold), **stop the chain here** and surface both slates for a ruling. This gate pauses in every mode — do not defer it.

---

## Step 3 — Sync the canon

Run the **canon-sync** procedure against the just-landed `draft.md`, using the promoted `source_revision` as the provenance tag (`CH<N> rev<M>`). Non-conflicting additions write automatically; the diff-based dropped-fact check and the contradiction check run as normal.

**Gate handling per run mode:** attended → pause and present each contradiction / dropped fact for a ruling; unattended → defer it to `open-loops.md` + the report and continue. Carry canon-sync's added / updated / deferred counts into the report.

---

## Step 4 — Mirror to StoryLine (conditional)

If Step 1 found a `WRITING/STORYLINE/<Project>/` target, run the **storyline-sync** procedure against the landed `draft.md`. It reads the now-current `REFERENCE/bible.md` / `threads.md` (the reason it runs last), segments scenes on hard breaks, **actually runs the scene-intensity engine** (never eyeball `si_*`), writes the scene files + Codex entries, and applies its author-tuned-conflict gate per the run mode.

If **no** StoryLine project exists for this project, **skip this leg and say so** in the report ("no StoryLine project for <Project> — mirror step skipped"). Skipping is not a failure.

---

## Step 5 — Verify (roll up each leg's self-test)

You do not invent a new check — you confirm each leg reported success, via the **file tools, not a bash read** (`^obs-014`):

- **promote-revision:** `draft.md` is `status: register-revised`, its body matches the promoted rev, `source_revision` is set.
- **canon-sync:** written facts carry the `(CH<N> rev<M>)` provenance; every contradiction / dropped fact was ruled (attended) or deferred to `open-loops.md` (unattended) — none silently dropped.
- **storyline-sync (if run):** its self-test passed — all scene/codex YAML parses, wikilinks resolve, `sequence` numbers are unique, and every scene's `intensity == round(si_local/10)` with the `si_*` block present (proof the engine actually ran).

Any leg's self-test FAILs → **halt**, leave the chapter flagged in the report, and do **not** log it as fully landed.

---

## Step 6 — Log

Write **one** consolidated landing entry (not three) to the chapter `changelog.md` and the vault `_CHANGELOG.md` (fiction lane): chapter landed, rev promoted, canon facts added/updated, conflicts ruled or deferred, StoryLine scenes/codex written (or skipped). File deferred gates to the chapter `open-loops.md`. File any new fragility to `_OBSERVATIONS.md`; add follow-ups to `_BACKLOG.md` if warranted. (DIR-003.)

---

## Step 7 — Report

Emit one end-to-end landing report: run mode; chapter + rev promoted; canon adds/updates and any deferred/ruled conflicts; StoryLine scenes + codex written (or "skipped — no project"); the verify PASS/FAIL roll-up; and an explicit list of anything left for the author to rule. If a leg halted the chain, say which leg, why, and what state the chapter is in.

---

## Stop conditions

- Vault sentinel fails → halt, ask which folder is the vault.
- No `…-rev<N>.md` in `revisions/`, or no `draft.md` / `REFERENCE/` → halt before promoting (nothing to land / convention not adopted).
- promote-revision lineage mismatch → halt the chain, surface both slates (pauses in every mode).
- Any leg's own self-test FAILs → halt at that leg, report the partial state, do not mark the chapter landed.

---

## What you never do

- You never revise, clean, or "improve" a word of prose — that is `register-pass`, upstream.
- You never re-implement a leg's logic. If a leg's behavior should change, that change belongs in the leg's own skill/doc; you only ever *call* the leg, so you inherit it automatically. (Duplicating a leg's procedure here is exactly the drift `skill-audit` exists to catch.)
- You never write StoryLine's plugin-owned files (plotlines, codex categories, plot grid) — `storyline-sync` already knows those are auto-managed.
