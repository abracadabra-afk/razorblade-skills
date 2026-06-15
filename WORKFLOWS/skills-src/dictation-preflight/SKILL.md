---
name: dictation-preflight
description: >-
  Pre-flight for the Transcoder — read the queued dictation for a chapter and fill in that chapter's envelope.md (POV + conditions + state, segmented by perceptual envelope) BEFORE any slate is run. Use this skill whenever the author asks to "prep the envelope," "preflight this chapter," "fill the envelope," "ready the envelope for the transcoder," "set up the envelope," "envelope prep," or otherwise wants a chapter's envelope authored from its dictation so the Transcoder won't trip the empty-envelope gate. This is the UPSTREAM preparation step: it produces the envelope the Transcoder requires. Do NOT use it to transcode, slate, or generate prose — that is dictation-transcoder ("slate this dictation"), which runs after this. If the author asks to slate, transcode, or run the slate, route there instead.
---

# Dictation Pre-Flight (envelope prep)

You are preparing a chapter for the Transcoder. The Transcoder needs a filled `envelope.md` and **halts** when it finds an empty or placeholder one. Your job is to read the queued dictation, derive the perceptual envelope(s) it was recorded against, and write them into `envelope.md` so the slate can run cleanly.

You do **one** thing: author the envelope. You do not transcode, cut, synthesize, or write any prose. You do not touch the slate. When you are done, the chapter is ready for "slate this dictation," not finished.

The envelope states, per segment:

- **Who** is perceiving (the POV character)
- **In what conditions** (place, weather, light, time of day)
- **In what state** (what they're doing, carrying, suffering — what consumes their attention)

These are the tests the Transcoder's Cut operation runs against. Getting them right here is the whole point of the pass.

---

## Step 0 — Vault sentinel check

Before doing anything else, verify you are pointed at the right vault. The risk: a mounted folder that *looks* empty reads as "fresh start-up" and you write an envelope into the wrong directory tree.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. If `_DIRECTIVES.md` is missing or the frontmatter doesn't match, **halt and ask** which folder is the intended vault. Do NOT scaffold a bootstrap and do NOT write anywhere.

This is a hard gate. Pass it before reading any chapter.

---

## Required inputs

You cannot run without these. If either is missing, stop and ask.

**1. The chapter folder.** A folder following the per-chapter convention:

```
<chapter>/
├── envelope.md       <- YOU write here (the only substantive output)
├── changelog.md      chapter-level history (you append a log line)
├── _status.md        per-segment phase tracker (you fill segment names only)
├── draft.md          (you do NOT write here)
├── open-loops.md     (you do NOT write here)
├── continuity.md     (you do NOT write here)
├── notes.md          chapter-scoped research (read-only, for context)
├── brief.md          forward intent (read-only — intent context when present)
├── dictation/        raw transcripts — read the newest unslated one
├── slate/            Transcoder output (read-only, to find the newest *unslated* dictation)
└── revisions/        one-way door — never read, never write
```

If the author gave a chapter name without a path, search the vault for a folder matching it that contains `envelope.md`. If several match, ask. If none follow the convention (no `envelope.md`, no `dictation/`), do not fabricate one — tell the author the project hasn't adopted the per-chapter folder convention and stop.

**2. The queued dictation.** From `<chapter>/dictation/`, pick the **newest file by mtime** that does not already have a matching `<chapter>/slate/YYYY-MM-DD-NN/` produced from it (ignore `README.md`). Name the file you picked in your output so a misfire is visible. If the dictation file's own header/frontmatter pins an `envelope-segment`, respect that pointer — you are filling the envelope for that segment.

---

## Step 1 — Read the envelope as it stands and classify it

Read `<chapter>/envelope.md`. Decide, field by field, what is real and what is scaffold. Treat a field as **unfilled** if any of these is true:

- It is an angle-bracket placeholder (`<short name>`, `<character>`, `<place, weather, light, time of day>`, …).
- It is a bare ellipsis (`…`) or empty.
- The frontmatter `chapter:` does not match this chapter's folder name — a tell that the file is a **verbatim template copy** carried over from another chapter (the `^obs-005` failure: a new chapter's envelope is the blank CHAPTER 1 template, frontmatter still reading `chapter: CHAPTER 1 - KNOTS`, every field a placeholder). When the frontmatter is stale, distrust the whole file and treat all segment fields as unfilled until proven otherwise, and correct `chapter:` and `last_updated` when you write.

Treat a field as **author-filled** (and never overwrite it) if it contains real content the author wrote. **Fill-gaps-only is the law of this pass:** you replace placeholders, ellipses, empties, and stale frontmatter; you never touch a field the author already authored. If the entire envelope is already filled with real content and the frontmatter matches, say so and stop — there is nothing to prep.

---

## Step 2 — Segment the dictation by perceptual envelope

Read the whole queued dictation. A chapter's dictation usually crosses more than one perceptual envelope — e.g. an exterior storm-trek (cold, dark, wind, attention on staying upright) gives way to a hut interior (firelit, warm, still, attention on a second person). Mark where the perceptual world changes:

- **Light** (night blizzard → firelight → dawn)
- **Temperature** (frozen trek → hearth-warmth)
- **Location** (ridge → cottage → memory/dream)
- **Who the POV is attending to** (the dog → the sick boy → the wolves)

For each segment you find, derive the four envelope fields from the text:

- **Short name** — a 1–3 word handle (`waking-hearth`, `storm-trek`, `hovel-diagnosis`, `spring-memory`).
- **Boundaries** — first beat → last beat, anchored by short quoted phrases so the boundary is checkable (`"a braid of smoke twisted…" → "…closed his eyes."`).
- **POV** — who is perceiving.
- **Conditions** — place, weather, light, time of day.
- **State** — what the POV is doing/carrying/suffering; what consumes their attention.

Segment **only** on perceptual world, never on maturity or plot. If the dictation pins a single `envelope-segment`, fill that one segment and leave the others as the author left them.

---

## Step 3 — Confidence, and context resolution (REFERENCE first, walk-back fallback)

For every field, ask honestly: **can I read this off the dictation with confidence?** Conditions and state are usually right there in the prose. POV and place names are the fields most often left implicit (the text says "the hunter" or "she," never the name; the cottage is "the stead," never the holding's name).

When a field is unclear from the dictation alone, resolve it in this order before guessing:

**1. Project state first.** Read `REFERENCE/story-so-far.md`, `REFERENCE/bible.md`, and `REFERENCE/threads.md` (maintained by canon-sync) — current state, entity facts, canonical names/spellings, open promises, where things stood at the end of the last landed chapter. This is the cheap, authoritative path. The chapter's own `brief.md` (when present) is intent context — useful for segment naming and for flagging when the dictation visibly diverges from the chapter's stated job (note the divergence in your reply; never block on it).

**2. Back-walk as fallback.** When REFERENCE is missing, empty, or stale relative to the prior chapter (compare its `last_updated` / synced chapters against the newest landed draft), walk back across prior chapters (nearest first): the prior chapter's `envelope.md` (recurring POV names, place names, perceptual vocabulary) → prior `continuity.md`/`draft.md` (who this character is, where they are, what they carry) → this chapter's `notes.md` and the project entry note (world facts, proper nouns). If the back-walk was needed because REFERENCE was stale, say so — that is a signal to run canon-sync.

Re-assess each unclear field after resolution and cite, in your output, which file resolved it ("POV = the hunter; bible.md Characters — carried forward"). Resolution is how you turn an implicit "she" into a confident, consistent POV label instead of inventing one.

---

## Step 4 — Write what you're confident in; ask on what you're not

**Write when confident.** For every field you can read off the dictation or resolve via the walk-back, write it straight into `envelope.md` (fill-gaps-only). Update the frontmatter `chapter:` to match the folder and bump `last_updated` to today.

**Ask with your best guess when you're not.** For any field still uncertain after the walk-back — ambiguous POV, an unnamed place, a segment boundary you can't pin, a dream-vs-memory you can't tell apart — do not silently commit a guess that would feed the Transcoder a wrong test. Instead:

- Write your **best guess** into the field, tagged inline so it cannot pass as confirmed:
  `<<UNCERTAIN: best-guess — one-line reason; confirm?>>`
  e.g. `**POV:** the hunter <<UNCERTAIN: "she" throughout, never named; CH1 calls her "the hunter" — confirm she's the same POV>>`
- Collect every uncertain field into a single **clarification block** in your reply to the author: each field, your best guess, and the one thing you'd need to confirm it.
- Tell the author plainly that the chapter is **not yet slate-ready**: the tagged fields should be confirmed (or corrected) before they run "slate this dictation," because the Transcoder will test against whatever the envelope says.

A field you guessed and tagged is better than a halt (the author can confirm in one line) and far better than a silent wrong guess (which the Transcoder would faithfully cut against). Confident fields go in clean; uncertain ones go in flagged and surfaced.

---

## Step 5 — Sync the status tracker (gaps only)

In `<chapter>/_status.md`, fill the **Envelope** column's `<name from envelope.md>` placeholders with the segment short-names you just wrote, one row per segment. Do not change phases, blockers, or any column the author has set — gaps only. If `_status.md` is absent, skip it silently.

---

## Files this skill writes — and the ones it must not

**Writes:**
- `<chapter>/envelope.md` — the segments (gaps only; stale frontmatter corrected).
- `<chapter>/_status.md` — segment names only (gaps only).
- `<chapter>/changelog.md` and vault `_CHANGELOG.md` — a session log line (see Logging).

**Never writes** (these are the Transcoder's or the author's):
- `<chapter>/draft.md`, `<chapter>/slate/`, `<chapter>/open-loops.md`, `<chapter>/continuity.md`, `<chapter>/notes.md`, `<chapter>/revisions/`.
- The dictation files. If a transcript looks wrong, say so — do not edit it. The author re-dictates.

You author the envelope. You do not produce a single line of prose. The slate is a separate, downstream pass.

---

## Stop conditions

- **Vault sentinel fails** (Step 0). Halt. Ask which folder is the vault.
- **Chapter folder doesn't follow the convention** (no `envelope.md` or no `dictation/`). Halt. Tell the author and ask whether they want to scaffold the folder first.
- **No unslated dictation** in `dictation/`. Halt. Tell the author there's nothing queued to prep against.
- **Envelope already fully filled** with author content and matching frontmatter. Stop — nothing to do; tell the author it's already slate-ready.
- **A segment's perceptual world is genuinely unreadable** from the text even after the walk-back. Don't fabricate it — write your best guess tagged `<<UNCERTAIN>>` and surface it in the clarification block.

---

## Logging (when running inside CRE's vault)

This is a non-trivial session, so honor DIR-003. If `_CHANGELOG.md` at the vault root has frontmatter `type: ai-os-brain, file: changelog`, append a session entry (newest first):

```
## YYYY-MM-DD — [fiction] envelope pre-flight on <chapter>
**Ran:** dictation-preflight on <chapter> against dictation/<filename>
**Shipped:** envelope.md filled — <N> segments (<short-names>); <N> fields tagged UNCERTAIN pending confirm; _status.md segment names synced
**Open loops:** <the uncertain fields the author still needs to confirm before slating>
**Observed:** <anything notable — e.g. stale template copy detected and frontmatter corrected (relates to ^obs-005)>
```

Also append the chapter-scoped detail to `<chapter>/changelog.md` in its own format. If a notable fragility or pattern surfaced, file it to `_OBSERVATIONS.md` with a `^obs-NNN` anchor for CRE to curate. If the vault has no `_CHANGELOG.md` (this skill is portable across vaults), skip logging silently.

---

## Security

If the raw dictation contains credentials, API keys, tokens, or other secrets, **stop and flag to the author before proceeding** (DIR-001). Do not copy the secret into the envelope, the changelog, or any output file. Pause until the author confirms they want to continue (typically after redacting the source).
