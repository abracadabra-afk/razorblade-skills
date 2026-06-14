---
type: workflow
name: dictation-runner
lane: fiction / os
status: active
trigger: scheduled task `dictation-runner` (polls _DICTATION INBOX/) + manual "run the dictation runner"
created: 2026-06-14
purpose: Remote, phone-first dictation pipeline. Drop audio in _DICTATION INBOX/ from anywhere; a scheduled Cowork task transcribes it offline, reconciles garbled proper nouns against project canon, runs dictation-cleanup, and leaves a finished first draft waiting — no desktop orchestration, no Buzz, no copy-paste.
---

# dictation-runner

> **The problem this kills:** the old flow was record → Buzz (manual desktop transcribe) → copy-paste into Cowork → trigger cleanup/transcode. Four hand-offs, all desktop-bound. This collapses it to: **drop audio in one folder; a polling task does the rest.** The orchestrator is a scheduled Cowork task (the same mechanism as `mount-the-vault`), so there are no cross-app event triggers to wire.

## Architecture — one polling loop, two stages

```
phone (record audio) ──Dropbox app──▶ _DICTATION INBOX/<clip>.m4a
                                              │
              scheduled task "dictation-runner" wakes (~every 15 min)
                                              │
  STAGE A · deterministic (runner.py, no LLM)
   • faster-whisper-small (vendored, offline) transcribes the audio
   • canon name-reconcile: garbled proper nouns matched vs the project's
     StoryLine Codex + REFERENCE/bible.md + REFERENCE/_LEXICON.md
   • writes _reconciled/<clip>.md  (reconciled text + corrections + raw audit)
   • moves the audio to processed/
                                              │
  STAGE B · the skills (this Cowork session)
   • runs dictation-cleanup on the reconciled transcript (non-destructive copy-edit)
   • writes _drafts/<clip>-clean.md   ← finished first draft, waiting
   • moves the reconciled note to _reconciled/done/
   • logs the run to _CHANGELOG
```

**Why polling, not triggers:** every "who fires whom" hand-off (Buzz→save→Cowork) was the brittle part and impossible to drive from a phone. A single scheduled task that watches one folder removes all of them. You don't need real-time — dictate on a walk, the draft is built by the time you're back.

**Transport is Dropbox:** the vault lives in Dropbox, so a file the phone drops into `_DICTATION INBOX/` is already visible to the runner's sandbox mount. No Google Drive / Supabase plumbing for transport.

## Scope boundary (v1)

- **Automated:** transcribe → reconcile → cleanup → holding draft in `_DICTATION INBOX/_drafts/`. Safe: `dictation-cleanup` is the protective, word-preserving copy-edit and the output never touches a chapter folder.
- **Stays a desk action:** the **transcoder/slate** into a specific `CHAPTER N/` `draft.md`. It needs an `envelope.md` (perceptual POV) and a chapter target — not on-the-go inputs. At the desk you route the holding draft into a chapter and run `slate this dictation` as usual.

## The name-reconcile (Stage A detail)

Lives in `WORKFLOWS/dictation-runner/lexicon.py` + `runner.py`. Deterministic, stdlib + `jellyfish`.

- **Lexicon source (derived + curated, no hand-maintenance of the bulk):**
  - StoryLine Codex filenames (`WRITING/STORYLINE/<Project>/Codex/**`) — characters, items, locations, lore.
  - `### ` entity headers in `REFERENCE/bible.md`.
  - A curated seed `REFERENCE/_LEXICON.md` for **world/lore terms not in the Codex** (e.g. *Witchwood*, *Godsrift*) and **known mishears** (`winch wood => Witchwood`). This is the one file you hand-grow.
- **Matching:** double-metaphone phonetic key + Jaro-Winkler on the surface form, best-of-window over 1–4 word spans, span-aligned, article-dedup.
- **Confidence tiers:** ≥0.92 → auto-correct; 0.86–0.92 → flag inline `[AUTHOR: heard → Canonical?]` (your existing review convention); <0.86 → left alone. Common words (the boy, the river, wind, water) are guarded out to avoid false positives.
- **Why this beats a bigger model:** `large-v3` has never heard of *Godsrift* either. Only your canon knows your invented vocabulary, so a lexicon pass is the correct fix — and it's free and offline.
- **Project selection:** default **Witchwood**; override by putting the project in the filename (`godsrift_...m4a`).

## Dependencies (installed at runtime by the scheduled task)

```
pip install --break-system-packages faster-whisper jellyfish
```
The model is **vendored** at `_models/faster-whisper-small` (the sandbox is firewalled from Hugging Face, so it loads from the vault — offline, ~3 s). To (re)vendor or swap size, run on a machine with HF access:
```
huggingface-cli download Systran/faster-whisper-small --local-dir "<vault>\_models\faster-whisper-small"
```

## The scheduled task prompt (Stage A + B)

> Bootstrap is NOT required for this task. Do exactly this:
> 1. `pip install --break-system-packages faster-whisper jellyfish` in the sandbox.
> 2. Run `python3 "<vault>/WORKFLOWS/dictation-runner/runner.py"`. It prints JSON of what it processed. If `processed: 0`, stop — nothing to do, no log entry.
> 3. For each new `_DICTATION INBOX/_reconciled/*.md` not yet in `_reconciled/done/`: run the **dictation-cleanup** skill on its "Reconciled transcript" section; carry the `[AUTHOR:]` flags through; **suppress cleanup's own `_CHANGELOG` self-log** (Step 4 owns the single line); on a noisy transcript that would trip cleanup's pause/HALT, write `_drafts/<stem>-NEEDS-REVIEW.md` with a note and continue (never stall — no author present); else write `_drafts/<stem>-clean.md`; move the reconciled note to `_reconciled/done/`.
> 4. Append ONE consolidated line per processed clip to `_CHANGELOG.md`.
> 5. Leave any `[AUTHOR:]` name flags in place — CRE rules them at the desk.

## Interaction with dictation-cleanup

Stage B calls the `dictation-cleanup` skill, so its contract matters. Verified 2026-06-14 against the installed skill:

- **Compatible (no change):** the reconciled transcript is still *raw dictation* (corrected proper nouns + flags), so it satisfies cleanup's guard "input is ALWAYS raw dictation, never an already-drafted chapter." Cleanup preserves "every remaining `[AUTHOR:]` flag," so the reconcile pass's `[AUTHOR: heard → Canonical?]` flags survive. It returns only clean Pass-4 prose and is vault-portable.
- **Adjusted (two):** (1) cleanup **self-logs** a `[fiction] dictation cleanup` entry to `_CHANGELOG` when the brain files are present → the scheduled task suppresses that and keeps one consolidated runner line, avoiding double entries per clip. (2) cleanup's **human-in-the-loop stop conditions** (>15 `[AUTHOR:]` flags → pause; possible-rewrite → HALT) assume a present author; unattended, the task writes `<stem>-NEEDS-REVIEW.md` and continues instead of stalling. If `dictation-cleanup`'s flag format or output protocol changes again, re-check these two points.

## Run modes

- **Unattended (scheduled):** empty inbox = silent no-op. Never blocks on a gate; name flags ride through in the draft for later.
- **Manual:** "run the dictation runner" — same steps, on demand.

## Known v1 limits (tracked)

- Multi-word mishears whose phonetics diverge (e.g. *widows pain* → flags *widows → Widowsbane?* and leaves *pain*). The flag still catches it; tighten via `_LEXICON.md` alias.
- Transcription accuracy = `small` model; reconcile fixes proper nouns, not general mishears. Upgrade path: the Supabase→Groq `whisper-large-v3` backend leg (see `_BACKLOG`), which replaces only Stage A.
- Scheduled Cowork tasks run on the desktop's uptime: "unattended" = you don't orchestrate it, not "desktop off." Server-side transcription (the Groq leg) is the answer if desktop-off processing is ever needed.

## Files

- `WORKFLOWS/dictation-runner/runner.py` — Stage A orchestrator (self-locating).
- `WORKFLOWS/dictation-runner/lexicon.py` — lexicon compile + reconcile.
- `_DICTATION INBOX/` — drop zone (`README.md`, `_reconciled/`, `_reconciled/done/`, `_drafts/`, `processed/`).
- `WRITING/PROJECTS/<PROJECT>/REFERENCE/_LEXICON.md` — curated seed (per project).
- `_models/faster-whisper-small/` — vendored model.
