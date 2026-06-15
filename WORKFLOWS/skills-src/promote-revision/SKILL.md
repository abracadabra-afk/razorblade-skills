---
name: promote-revision
description: Promote a chapter's newest revision (the register-pass output in revisions/) into the live draft.md, carrying the metadata forward so the lineage stays intact. Use this skill whenever the author asks to "promote the revision," "promote rev N," "make the revision the live draft," "bring the revision into draft," "update the working draft," or otherwise wants the latest revised passage in revisions/ to become the chapter's working draft.md inside a vault that uses the per-chapter folder convention (slate/ + revisions/ + draft.md). This is the RETURN TRIP out of revisions/ — register-pass deliberately never writes draft.md, so this is the skill that closes that gap. It copies prose and rewrites frontmatter only; it never revises, edits, or re-runs the register. Do NOT use it to revise against the register (that is register-pass, "run the register") or to produce a slate (that is dictation-transcoder). If the author asks to run the register or slate, route there instead.
---

# Promote Revision

You are promoting a chapter's newest **revision** — the passage `register-pass` wrote into `revisions/` — into the chapter's live **`draft.md`**, and carrying its metadata forward so the lineage is never lost. `register-pass` deliberately refuses to write `draft.md` (it keeps `revisions/` a clean one-way door). That refusal leaves a gap: something has to move the revised text back into the working draft. You are that something.

You hold **no craft opinion.** You do not revise a single word, re-run the register, fix prose, or re-open any ruling. Promotion is a faithful copy of the revision's prose plus a deterministic rewrite of `draft.md`'s frontmatter. If the prose looks like it could be improved, that is not your call — that is a fresh `register-pass`, not a promotion.

Hold one invariant in mind, because it makes the whole operation safe and reversible:

> **`draft.md` is a working mirror of the newest *promoted* revision.** The immutable copies live in `revisions/` (and the slate behind them). Promotion just re-points the mirror. So overwriting `draft.md` loses nothing recoverable — re-promoting an earlier rev restores any prior state, and the revision you promote stays untouched in `revisions/` as the source of truth.

You perform four moves, in order: **locate**, **verify**, **promote**, **log**. Nothing else.

---

## Step 0 — Vault sentinel check

Before doing anything else, verify you are pointed at the right vault — the same gate every skill in this family shares (`^obs-004`). The risk: a mounted folder that *looks* empty reads as "fresh start-up" and you write into the wrong tree.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. If `_DIRECTIVES.md` is missing, or the frontmatter doesn't match, **halt and ask** which folder is the intended vault. Do NOT scaffold a bootstrap and do NOT write anywhere.

This is a hard gate. Pass it before locating anything.

---

## Step 1 — Locate the chapter and the revision to promote

**The chapter folder.** A folder following the per-chapter convention (it has `slate/`, `revisions/`, and a `draft.md`). If the author gave a chapter name without a path, search the vault for a matching folder that contains a `revisions/` directory. If several match, ask. If the folder has no `revisions/` or no `draft.md`, it hasn't adopted the convention — tell the author and stop; do not fabricate the structure.

**The revision.** In `<chapter>/revisions/`, revision passages are named `YYYY-MM-DD-<slug>-rev<N>.md`, each with a sibling `…-rev<N>-note.md` (the editorial note — you do **not** promote the note; it stays as the rationale record).

- Default: pick the **newest** revision passage — latest `YYYY-MM-DD`, then highest `<N>`. Exclude the `-note.md` sidecars.
- If the author named a specific rev (e.g. "promote rev1" or a filename), use that one.
- If `revisions/` holds no `…-rev<N>.md` passage, **halt** — there is nothing to promote (run `register-pass` first).

Name the revision file you picked in your reply, so a wrong pick is immediately visible.

---

## Step 2 — Verify the lineage before you overwrite

`draft.md` is the live working copy. Before replacing its body, run two cheap sanity checks so a promotion can't silently scramble the chapter's history:

1. **Read the revision's frontmatter.** It carries `source_slate` (and, from `register-pass`, `register` / `register_title` / `mode` / `verdicts` / `maturity_gear`). You will carry these forward.
2. **Read `draft.md`'s current frontmatter.** Compare its `source_slate` to the revision's `source_slate`.
   - **Match** → normal case. The revision was built from the same slate lineage the draft already tracks. Proceed.
   - **Mismatch** → the revision descends from a *different* slate than the current draft claims. This is not necessarily wrong (the author may be re-baselining), but it is exactly the kind of thing that should never happen silently. **Surface it and ask** before overwriting: name both slates and let the author confirm.
   - **Draft is still a scaffold** (`status: not-yet-migrated`, or its body is only the placeholder blockquote) → there is no real content to lose; proceed and say so.

You never need the author's permission for the *normal* (matching-lineage) case — promotion is reversible by design (see the invariant above). The ask is reserved for the mismatch, where proceeding blindly would bury a real divergence.

---

## Step 3 — Promote: copy the prose, rewrite the frontmatter

Replace `<chapter>/draft.md` with the revision's prose under a rewritten frontmatter block. Keep the body **byte-for-byte** as it appears in the revision passage (including any `[unclear: …]` inline marks the register left — those are part of the passage, not yours to resolve).

Rewrite `draft.md`'s frontmatter by this mapping. Preserve fields not mentioned; do not drop provenance.

| Field | Value on promotion |
|---|---|
| `type` | keep (`chapter-draft`) |
| `chapter` | keep (the folder name) |
| `status` | set to `register-revised` (the stage the promoted text came from). If you ever promote a revision from a different stage, set `status` to that stage instead — the status names *where the live text came from*. |
| `source_slate` | **keep** — the original provenance, carried unchanged from the revision's frontmatter. |
| `source_revision` | set to the path of the revision you promoted, e.g. `revisions/2026-06-03-<slug>-rev<N>.md` — the live text's *immediate* parent. This is the field that makes the promotion auditable and reversible. |
| `register` / `register_title` / `mode` | carry forward from the revision's frontmatter if present (records which register/mode produced the live text). |
| `blind_read` and any other prior lineage pointers | keep whatever `draft.md` already had — promotion adds to the lineage, it does not erase earlier stages. |
| `last_updated` | today's date (check via the shell if unsure). |

Why both `source_slate` *and* `source_revision`: the slate is the deep provenance (where the words originally came from), the revision is the immediate parent (what was just promoted). Keeping both means anyone can walk the chain in either direction without guessing.

**Do not touch** `slate/`, `revisions/`, the `-note.md` sidecars, or any `spec-check/` file. They are the immutable record; `draft.md` is the only thing this skill writes (besides the logs). If the chapter keeps a `_status.md` phase tracker, you may bump its `last_updated` and note the promotion, but never invent fields it doesn't already have.

---

## Step 4 — Log

Append a short entry to both logs (newest at top), matching the house format used by the sibling skills:

- **`<chapter>/changelog.md`** — a chapter-scoped entry: what was promoted, the status transition, the rev path, and the frontmatter lineage now recorded. Bump the file's `last_updated`.
- **vault `_CHANGELOG.md`** — a one-entry session line under the fiction lane: `## YYYY-MM-DD — [fiction] promote revision on <chapter>` with **Ran / Shipped / Open loops** lines.

If you noticed anything fragile (a lineage mismatch you had to resolve, a missing field, a `_status.md` that didn't match the folder), file it to `_OBSERVATIONS.md` with a `^obs-NNN` anchor.

---

## Files this skill writes — and the ones it must not

**Writes:**
- `<chapter>/draft.md` — body replaced with the promoted revision's prose; frontmatter rewritten per the mapping above.
- `<chapter>/changelog.md` and vault `_CHANGELOG.md` — a log line each.
- optionally `<chapter>/_status.md` (`last_updated` bump only) and `_OBSERVATIONS.md` (if something fragile surfaced).

**Must NOT write or alter:**
- Anything in `slate/`, `revisions/` (including the `-note.md` you read), or `spec-check/`. These are the immutable audit trail; promotion mirrors them into `draft.md`, it never edits them.

---

## Stop conditions

- Vault sentinel fails → halt, ask which folder is the vault.
- Chapter has no `revisions/` or no `draft.md` (convention not adopted) → halt, tell the author.
- `revisions/` holds no `…-rev<N>.md` passage → halt; nothing to promote (run `register-pass` first).
- Revision `source_slate` ≠ draft `source_slate` (and draft is not a scaffold) → pause, surface both, ask before overwriting.

---

## What this skill is NOT

- Not a reviser. It moves text; it never improves it. Improvement is `register-pass`.
- Not a slate or envelope step. Those are `dictation-transcoder` and `dictation-preflight`.
- Not a judge. It does not read or re-open `verdicts.md` rulings — `register-pass` already executed them; promotion just carries the result home.

---

_Canonical reference for the `promote-revision` Cowork skill lives at [[WORKFLOWS/promote-revision]]. Per [[_SKILLS MAP#Cowork skills]], procedure changes land in the workflow doc first, then propagate to the skill via skill-creator._
