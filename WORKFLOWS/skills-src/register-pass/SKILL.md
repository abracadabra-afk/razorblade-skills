---
name: register-pass
description: Revise a chapter's newest slate clean-draft against the project's own register — a project-specific revision prompt kept at REFERENCE/register.md — and write the revised passage plus the register's editorial note into the chapter's revisions/ folder. Use this skill whenever the author asks to "run the register," "revise with the register," "do a register pass," "run the reviser," or otherwise wants a finished slate run through the project register inside a vault that uses the per-chapter folder convention (slate/ + revisions/). This is the DOWNSTREAM revision stage out of the Transcoder — it consumes a slate clean-draft and promotes a revised version into revisions/ (a one-way door). Do NOT use it to produce a slate from dictation (that is dictation-transcoder, "slate this dictation") or to author an envelope (that is dictation-preflight, "prep the envelope"). If the author asks to slate or transcode, route there instead.
---

# Register Pass

You are running a chapter's **slate clean-draft** through the **project register** and promoting the result into the chapter's `revisions/` folder. The slate is the rough draft the Transcoder produced; the register is a project-specific revision prompt that says how this world's prose should be strengthened. Your output is the revised passage plus the register's own editorial note.

You hold **no revision philosophy of your own.** The register changes project to project — Witchwood's fuses a child's fairy-tale register with adult material reality; another world's will be something else entirely. Your job is orchestration: find the right register, find the right slate, run the register's instructions faithfully against the slate, route the two outputs to the right files, and log. *How* to revise is the register's call, not yours. Do not import rules from any other skill's revision stance, and do not soften, extend, or "improve on" the register — execute it.

You perform four moves, in order: **locate**, **run**, **route**, **log**. Nothing else.

---

## Step 0 — Vault sentinel check

Before doing anything else, verify you are pointed at the right vault. The risk: a mounted folder that *looks* empty silently reads as "fresh start-up" and you write a revision into the wrong directory tree.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. If `_DIRECTIVES.md` is missing, or the frontmatter doesn't match, **halt and ask** which folder is the intended vault. Do NOT scaffold a bootstrap and do NOT write anywhere.

This is a hard gate. Pass it before locating anything.

---

## Required inputs

You cannot run without all three. If any is missing, stop and ask before doing anything else.

**1. The chapter folder.** A folder following the per-chapter convention:

```
<chapter>/
├── envelope.md       (read-only context, if you need POV/conditions)
├── draft.md          (you do NOT write here)
├── slate/            YOUR INPUT lives here — the newest run's clean-draft.md
│   └── YYYY-MM-DD-NN/
│       ├── clean-draft.md       <- the passage you revise
│       ├── synthesis-ledger.md  <- prior-pass context (read-only)
│       └── leaves-left.md       <- prior-pass context (read-only)
├── revisions/        YOUR OUTPUT goes here (one-way door)
├── changelog.md      chapter-level history (you append a log line)
├── open-loops.md / continuity.md / notes.md / _status.md   (you do NOT write here)
└── dictation/        (not used by this skill)
```

If the author gave a chapter name without a path, search the vault for a folder matching it that contains a `slate/` directory. If several match, ask. If none follow the convention (no `slate/`, no `revisions/`), do not fabricate one — tell the author the project hasn't adopted the per-chapter folder convention and stop.

**2. The project register.** Walk up from the chapter folder to the **project root** — the folder whose `CHAPTERS/` directory contains this chapter — and read `<project>/REFERENCE/register.md`. (For Witchwood: `WRITING/PROJECTS/WITCHWOOD/REFERENCE/register.md`.) If it is not there, search upward for the nearest ancestor with a `REFERENCE/register.md`. If you find exactly one, use it and name its path in your output. If you find none, **halt and ask** — the register is project-specific and you must never invent one, substitute another project's register, or fall back to a generic revision prompt. If you find more than one plausible register, ask which.

**3. The working text — `draft.md` if it carries real content, else the newest slate clean-draft.** Decide which text you revise in this order:

   - **Prefer `<chapter>/draft.md`** when its frontmatter `status` marks real content (e.g. `dev-revised`) rather than scaffold (`not-yet-migrated`, or a body that is only the placeholder blockquote). A populated `draft.md` means the developmental pass (`blind-response`) has already revised the chapter from the slate; that revised text — not the raw slate — is what the register should run on.
   - **Otherwise fall back to the newest slate `clean-draft.md`** — from `<chapter>/slate/`, the latest `YYYY-MM-DD` then highest `NN`. This is the normal path when no developmental pass has run.

   If the author named a specific slate run, use that. Name the working text you picked (draft.md vs. which slate run) in your output so a misfire is immediately visible. When you read from a slate run, also read its `synthesis-ledger.md` and `leaves-left.md` if present — **prior-pass context only** (see below), never the thing you revise. (When working from a populated `draft.md`, the slate ledgers still belong to the slate run named in its `source_slate` frontmatter.)

---

## Prior-pass context — how to treat the slate's ledgers

The register may include a clause about running downstream of an earlier pass. The Transcoder's `leaves-left.md` is exactly that earlier pass's record. Use it as input, with this discipline:

- **`left-for-later`** verdicts are load-bearing emotion the Transcoder deliberately deferred to the revision stage. **That stage is you.** These are the register's to address — do not treat them as settled.
- **`incidental`** and **`dialogue`** verdicts are settled rulings. Do not re-litigate them; leave those spans unless the register's own rules independently touch them.
- **`synthesis-ledger.md`** flags (`[REGISTER-REPAIR]`, image-doubling questions) point to lines the Transcoder already knows are fragile. Let the register weigh them; surface in your note where you acted on one.

If the slate has no ledgers (older or partial runs), proceed on the clean-draft alone — the ledgers are enrichment, not a requirement.

---

## Check for a spec-check verdict sheet — pick the mode

Before running the register, look for `<chapter>/spec-check/<slate-run-id>/verdicts.md`, where `<slate-run-id>` is the slate run you selected (e.g. `2026-06-03-01`). This is the optional output of the spec-check battery (`WORKFLOWS/spec-check.md`), in which the author has already diagnosed the chapter and **ruled** the judgment calls. Two modes:

- **Execute-only mode** — a `verdicts.md` exists for this slate run with frontmatter `status: ready`. The diagnostic work is done and the rulings are settled. Run the register in its downstream stance (the register's own closing clause): **do not re-litigate** the author's rulings. Specifically:
  - Apply every **MECHANICAL** fix as given.
  - Honor every **RULED JUDGMENT CALL** exactly (KEEP / CUT / REWRITE-as) — do not re-open a call the author has settled, even if the register's rules would tempt you to.
  - **Build** every **UNDRAMATIZED** item (this is the register's §-style "build, don't cut" work).
  - Read the **NOTES TO THE REGISTER** and act on them.
  - Otherwise still apply the register's rules to anything the verdict sheet didn't touch, but the sheet's rulings win on every span it covers.
- **Full mode** — no `verdicts.md` (or `status:` is not `ready`). Run the register normally: discover and revise from scratch, as the register's own instructions direct. (This is the default; the battery is optional and selective.)

Name which mode you used and (in execute-only) the verdict sheet path in your output, so it's auditable. If a `verdicts.md` exists but its `slate_run` doesn't match the slate you're revising, treat it as **not present** (it belongs to a different draft) and note the mismatch rather than applying stale rulings.

---

## Run the register

Load `REFERENCE/register.md` and **execute its instructions against the clean-draft as the "draft" it asks you to revise.** Follow it to the letter:

- **Honor its gear-setting.** If the register sets a maturity gear (e.g. POLISHED vs ROUGH), let *it* decide — read the whole passage and set the gear by its rules. Do not pre-decide. (Note that slate output is rough by construction, but the register's own step decides how to treat it.)
- **Honor its output contract.** The register specifies exactly what to return — typically the revised passage followed by a structured note (diagnosis, craft changes, mechanical corrections, changes-considered-and-rejected, counts, and unrecoverable breaks listed first). Produce all of it; you will split it across two files in the next move.
- **Do not add, drop, or reorder the register's rules.** If something in the register is ambiguous for this passage, surface the ambiguity in the note rather than resolving it by importing a rule from elsewhere.

The register is the authority on craft. You are the authority only on *which* register, *which* slate, and *where the outputs go.*

---

## Route the outputs — write two files to `revisions/`

The register returns one combined response (revised passage + note). Split it into two files in `<chapter>/revisions/`.

**Naming.** Per the chapter's `revisions/README.md`, revision files are `YYYY-MM-DD-<slug>-rev<N>.md`.

- `<slug>` — derive from the slate clean-draft's `envelope_segments` frontmatter: join the segment short-names with `+` (e.g. `waking-hearth+the-hunt`). If there is no usable segment list, fall back to a short chapter slug.
- `<N>` — scan `revisions/` for existing files with the same `<slug>`; use the next integer (start at `1`).

**File 1 — the revised passage** → `revisions/YYYY-MM-DD-<slug>-rev<N>.md`

Clean revised prose only. Keep any inline marks the register left for unrecoverable text (e.g. `[unclear: "wild-out"?]`) — those are part of the passage, not commentary. Front it with:

```yaml
---
source_slate: slate/YYYY-MM-DD-NN/clean-draft.md
register: REFERENCE/register.md
register_title: <the register's own title/version line, e.g. "Braided-Register Literary Fantasy (v3)">
mode: full | execute-only
verdicts: spec-check/<slate-run-id>/verdicts.md   # omit in full mode
maturity_gear: <the gear the register chose>
generated: YYYY-MM-DD HH:MM
---
```

**File 2 — the editorial note** → `revisions/YYYY-MM-DD-<slug>-rev<N>-note.md`

The register's full note, verbatim, in its specified order. Front it with a one-line back-reference to the rev file it explains and the slate it came from. If the register flagged **unrecoverable breaks**, they appear at the top of this note *and* you surface them at the top of your reply to the author — those are the one thing that must not get buried.

**One-way door.** Material in `revisions/` has left the Transcoder workflow: per the chapter's `revisions/README.md`, the Transcoder never reads from `revisions/` again. The slate you read stays exactly as it was — it remains the immutable audit trail. Do not modify, delete, or "promote out" the slate. In your reply, tell the author plainly that this chapter material has crossed the one-way door.

---

## Files this skill writes — and the ones it must not

**Writes:**
- `<chapter>/revisions/YYYY-MM-DD-<slug>-rev<N>.md` — revised passage.
- `<chapter>/revisions/YYYY-MM-DD-<slug>-rev<N>-note.md` — editorial note.
- `<chapter>/changelog.md` and vault `_CHANGELOG.md` — a session log line (fiction lane): which slate run was revised, which register + mode, the `rev<N>` files written, and any unrecoverable breaks.

**Must NOT write:**
- `draft.md` — promoting a revision into the live working draft is `promote-revision`'s job, not this skill's. You write only into `revisions/`.
- `slate/` (any file) — the slate is the immutable audit trail. Never modify, delete, or "promote out" of it.
- `envelope.md`, `open-loops.md`, `continuity.md`, `notes.md`, `_status.md` — read-only context here.
- `REFERENCE/register.md` — you execute the register; you never edit it.

If a span you would revise lives in one of those files, stop — you are in the wrong stage.

---

## Logging

On completion, append a one-line entry to the chapter's `changelog.md` and to the vault `_CHANGELOG.md` (fiction lane): the slate run revised, the register title + mode (`full` / `execute-only`), the `rev<N>` files written, and any unrecoverable breaks (surfaced first, never buried). File any new fragility to `_OBSERVATIONS.md`.

---

## Stop conditions

- Vault sentinel fails → halt, ask which folder is the vault.
- No `REFERENCE/register.md` for the project → halt, ask; never substitute a generic prompt.
- No slate `clean-draft.md` in the chapter → halt; nothing to revise (run the Transcoder first).
- Chapter doesn't follow the per-chapter folder convention (no `slate/`, no `revisions/`) → halt, tell the author.
- Register output has unrecoverable breaks → keep them marked inline, list them first, continue.

---

_Canonical reference for this skill lives at [[WORKFLOWS/register-pass]]. Per [[_SKILLS MAP#Cowork skills]], procedure changes land in the workflow doc first, then propagate here via skill-creator._
