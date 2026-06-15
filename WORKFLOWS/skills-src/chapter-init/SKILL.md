---
name: chapter-init
description: Scaffold a brand-new chapter folder in a writing project that uses the per-chapter folder convention — create CHAPTERS/CHAPTER N - TITLE with every convention file (brief, envelope, changelog, draft, open-loops, continuity, notes, _status, plus dictation/slate/revisions dirs), each stamped with the CORRECT chapter frontmatter, and seed brief.md's payoffs from REFERENCE/threads.md. Use whenever the author asks to "scaffold chapter N," "start a new chapter," "init chapter N," "set up the folder for chapter N," or names a chapter that doesn't exist yet and wants to work in it. This is pipeline step S1 — before the brief fill (S2), dictation (S3), and "prep the envelope." It exists because hand-copying a sibling chapter ships stale chapter frontmatter (the obs-005 trap). Do NOT use it to fill the envelope (dictation-preflight), slate dictation (dictation-transcoder), or repair an existing chapter folder — it only creates folders that don't exist and never writes prose.
---

# Chapter Init

You are scaffolding a **new chapter folder** — pipeline step **S1**. The job is structural and deliberately boring: create the folder, write every convention file from canonical templates with the correct `chapter:` stamp, seed the brief's thread inventory, and log it. You write **no prose** and **no intent** — the brief's creative content is S2, and that belongs to the author.

Why this skill exists: chapters used to be scaffolded by copying a sibling chapter's files, which shipped frontmatter still claiming the *old* chapter (`^obs-005` — CH2/CH3 carried `chapter: CHAPTER 1 - KNOTS` for days, confusing every downstream skill that trusts frontmatter as truth). The fix is never to copy a sibling: the bundled script writes from templates and refuses to leave a placeholder unsubstituted.

Four moves, in order: **gate**, **scaffold**, **seed**, **log**.

---

## Step 0 — Vault sentinel check

Before doing anything else, verify you are pointed at the right vault — the same gate every skill in this family shares (`^obs-004`).

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. If `_DIRECTIVES.md` is missing or the frontmatter doesn't match, **halt and ask** which folder is the intended vault. Do NOT scaffold a bootstrap and do NOT write anywhere.

(The script re-checks this — belt and suspenders — but check it yourself first so the failure is conversational, not a stack trace.)

## Step 1 — Gate

Collect three things; halt on whichever is missing rather than guessing:

- **Project root** — the folder containing `CHAPTERS/` and `REFERENCE/`. If exactly one project in the vault qualifies, use it and say so. If several, ask.
- **Chapter number N** — if the author didn't give one, the default is (highest existing chapter + 1); confirm it in your reply.
- **TITLE** — never invent a title. If the author hasn't named the chapter, ask. Titles are stored uppercase (matching `CHAPTER 1 - KNOTS`, `CHAPTER 2 - SO BROKEN`).

Hard gates (the script enforces these too):
- A `CHAPTER N - *` folder already exists for that N → **halt**. This skill never overwrites and never back-fills an existing chapter — repairing a half-built folder is a different, manual conversation.
- N skips a number (not highest+1) → surface it and get the author's explicit OK before re-running with `--allow-gap`.

## Step 2 — Scaffold (run the script)

Run the bundled script — do not hand-create the files, and **never copy files from a sibling chapter**:

```bash
python3 <skill>/scripts/scaffold.py --project "<project-root>" --number <N> --title "<TITLE>"
```

It creates `CHAPTERS/CHAPTER N - <TITLE>/` with: `brief.md` (status `unfilled`, `spec_material: true`), `envelope.md`, `changelog.md` (init entry included), `draft.md` (`status: scaffold`), `open-loops.md`, `continuity.md`, `notes.md`, `_status.md` (header only — segment rows appear when the envelope is authored), and `dictation/`, `slate/`, `revisions/` each with their README. Every file is stamped `chapter: CHAPTER N - <TITLE>` and today's date. `spec-check/` is deliberately **not** created — the spec-check battery creates it per run.

Use `--dry-run` first if anything about the inputs felt uncertain. If the script exits with a `GATE:` message, that's a stop condition — relay it, don't work around it.

## Step 3 — Seed brief.md (inventory, not intent)

Read `REFERENCE/threads.md`. For each thread that is still open (not PAID/closed), replace the `{{THREAD-SEED}}` comment in the new `brief.md` under **Payoffs / advances due** with one line per thread:

```
- **T<NN> <name>** — open since CH<M>; <one-line current state>. <<PROPOSED — CRE to rule: pays / advances / dormant>>
```

This is a harvest of what already exists, so the author starts S2 with the ledger in front of them — it is **not** a proposal about what the chapter should do. Leave every other brief section untouched and `status: unfilled`. Then set the changelog init entry's open-loops line to mention how many threads were seeded.

If `REFERENCE/threads.md` doesn't exist, delete the seed comment, note the skip, and move on — don't fabricate threads.

## Step 4 — Log

- The chapter's `changelog.md` already carries the script's init entry — extend it with the seed count if you seeded.
- **Project pipeline board** (`PIPELINE.md` at the project root), if present: add/update the chapter's row — S1 done today, S2 next (owner CRE+AI). Recording the ruling in the same gesture as the artifact is the `^obs-012` rule.
- **Vault `_CHANGELOG.md`**: one session entry, newest at top — `## YYYY-MM-DD — [fiction] chapter-init: CHAPTER N - <TITLE>` with **Ran / Shipped / Open loops** lines.

---

## Files this skill writes — and the ones it must not

**Writes:** the new chapter folder and its 11 files (via the script); the new `brief.md` §Payoffs seed lines; a row on `PIPELINE.md` if the board exists; an entry in vault `_CHANGELOG.md` (and `_OBSERVATIONS.md` if something fragile surfaced).

**Must NOT write or alter:** any existing chapter folder, any `REFERENCE/` file (threads.md is read-only here), any sibling chapter's files, and the brief's Job/Beats/Setups/Seal sections (those are the author's, at S2).

## Stop conditions

- Vault sentinel fails → halt, ask which folder is the vault.
- No TITLE given → ask; never invent one.
- `CHAPTER N - *` already exists → halt; never overwrite or back-fill.
- N is not highest+1 and the author hasn't confirmed the gap → ask first.
- Project has no `CHAPTERS/` or no `REFERENCE/` → convention not adopted; ask before fabricating structure.

## What this skill is NOT

- Not the brief author. The seed is an inventory of open threads; the chapter's job, beats, setups, and seal schedule are written **with the author** at S2.
- Not the envelope author — that is `dictation-preflight` ("prep the envelope").
- Not a migrator or repairer of existing chapters. If a chapter folder exists but is malformed, surface what's wrong and let the author decide.
