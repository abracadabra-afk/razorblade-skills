---
type: workflow
name: dictation-runner
lane: fiction / os
status: active
trigger: scheduled task `dictation-runner` (polls _DICTATION INBOX/) + manual "run the dictation runner"
created: 2026-06-14
updated: 2026-06-14
purpose: Remote, phone-first VOICE pipeline. Drop ANY audio in _DICTATION INBOX/ from anywhere - a chapter you're dictating or a random thought/task/list. A scheduled Cowork task transcribes it, then forks it: fiction goes to the chapter-draft pipeline (reconcile -> cleanup -> _drafts/), everything else goes to your INBOX for the inbox-router to file. One drop zone, no toggling.
---

# dictation-runner

> **The problem this kills:** the old flow was record -> Buzz (manual desktop transcribe) -> copy-paste into Cowork -> trigger cleanup/transcode. Four hand-offs, all desktop-bound. This collapses it to: **drop audio in one folder; a polling task does the rest.** As of 2026-06-14 that one folder takes *every* kind of voice note, not just chapter dictation - the runner decides at transcription time whether a clip is fiction or a second-brain note, so you never pick a folder.

## What changed (2026-06-14): one folder, two destinations

You used to need a separate path for "dictate a chapter" vs "capture a stray thought." Now both land in `_DICTATION INBOX/`. The separation of concerns moved out of *which folder you drop into* and into a **classifier** the runner runs after transcription. The runner makes exactly one decision - **fiction, or not** - and each branch hands off to an already-built, mature pipeline:

- **fiction** -> the existing reconcile + cleanup path (unchanged).
- **not fiction** -> your **[[INBOX]]**, where the existing **[[WORKFLOWS/inbox-router|inbox-router]]** does all the domain sorting.

**Guardrail:** the runner NEVER writes a domain bucket directly. Per the vault's connector discipline ([[_VAULT MAP]]), the inbox-router is the *sole* write-path into Vibes/Tasks/Life/Knowledge/Business/Workflows. A non-fiction clip is dropped into INBOX (the universal front door) with the spoken intent preserved as a hint; the router files it from there.

## Architecture - one polling loop, transcribe-then-fork

```
phone (record audio) --Dropbox app--> _DICTATION INBOX/<clip>.m4a
                                              |
              scheduled task "dictation-runner" wakes (~every 30 min)
                                              |
  STAGE A . deterministic (runner.py, no LLM)
   * faster-whisper-small (vendored, offline) transcribes the audio
   * classify_route(): decide fiction vs inbox (see "The fork" below)
   |
   |-- FICTION:
   |     * canon name-reconcile (garbled proper nouns vs Codex + bible + _LEXICON.md)
   |     * writes _reconciled/<clip>.md  (reconciled text + corrections + raw audit)
   |
   |-- INBOX (everything else):
   |     * writes _inbox/<clip>.md  (verbatim transcript body + intent hint + confidence)
   |
   * moves the audio to processed/
                                              |
  STAGE B . the skills (this Cowork session)
   |-- for each new _reconciled/*.md:  dictation-cleanup -> _drafts/<clip>-clean.md
   |                                    -> move note to _reconciled/done/
   |-- for each new _inbox/*.md:        append body to INBOX (with intent-hint comment)
   |                                    -> move note to _inbox/done/
   * logs one consolidated line per clip to _CHANGELOG
                                              |
  (decoupled) the inbox-router - on its own schedule or "sort the inbox" -
  files the new INBOX items into the domain books, honoring the intent hint.
```

**Why polling, not triggers:** every "who fires whom" hand-off was the brittle part and impossible to drive from a phone. A single scheduled task watching one folder removes them all. **Transport is Dropbox:** the vault lives in Dropbox, so a file the phone drops into `_DICTATION INBOX/` is already visible to the runner's sandbox mount.

## The fork (classify_route, Stage A detail)

The runner decides fiction-vs-inbox in this order. The whole thing is biased so that **uncertainty resolves to INBOX** - both branches are non-destructive staging (a holding draft in `_drafts/` vs. text in INBOX), the inbox-router can segment a mixed clip and review-bin anything ambiguous, and the fiction branch never commits to a chapter on its own. So a wrong guess is always cheap and recoverable; a stray thought never lands silently inside a chapter.

1. **Explicit spoken directive at the head of the clip (highest priority).** A keyword *or* a natural-language instruction in the first clause, honored deterministically:
   - **Fiction markers:** `fiction`, `chapter`, `scene`, `dictation`, `slate`, `prose`, `manuscript`, `draft`, `narration`, or a **project name** (`Witchwood`, `Godsrift`, `Ghost River`, `Darkbloom`). A spoken project name also overrides the filename's project.
   - **Inbox markers:** `inbox`, `task`, `to-do`, `reminder` / `remind me`, `note to self`, `idea`, `vibe`, `capture`, `thought`, `list`, `file under ...`, `add to ...`, `put in ...`, `business`, `marketing`, `knowledge`, `workflow`, `backlog`.
   - The runner peels the directive clause off the body at the first separator (`:` `,` `-`) and keeps it as a **routing hint** for the inbox-router. Recommended phrasing: *say the directive, a slight pause/comma/colon, then the note.* Without a separator the directive stays in the body (harmless) and routing still works.
2. **No explicit directive -> heuristic classifier.** Two deterministic signals:
   - **canon-density** (the strongest signal, and one Stage A is uniquely good at): how many high-confidence canon names per 100 words. A clip dense in Witchwood/Godsrift vocabulary in narration is almost certainly prose.
   - **register**: third-person + past tense + quoted dialogue lean fiction; first-person + to-do/imperative cues (`remember to`, `need to`, `call`, `email`, `renew`, lists) lean inbox.
3. **Low signal either way -> INBOX, flagged `uncertain`.** Defaulted there for the router (and its Needs-review) to handle.

**v1 is heuristic by design.** The explicit directive is the primary control; the classifier is just the fallback for when you forget. Tunable knobs live at the top of `runner.py` (`CANON_STRONG`, `FICTION_SCORE`, `INBOX_SCORE`). Upgrade path: swap the heuristic for an LLM classify step in Stage B (see `_BACKLOG`); the fork interface stays the same.

## Scope boundary (still true)

- **Automated:** transcribe -> fork -> (fiction) holding draft in `_drafts/` or (inbox) item in `INBOX`. Both are safe, non-destructive staging.
- **Stays a desk action:** the **transcoder/slate** into a specific `CHAPTER N/` `draft.md`. It needs an `envelope.md` (perceptual POV) and a chapter target - not on-the-go inputs. At the desk you route a holding draft into a chapter and run `slate this dictation` as usual.

## The name-reconcile (Stage A, fiction branch only)

Lives in `WORKFLOWS/dictation-runner/lexicon.py` + `runner.py`. Deterministic, stdlib + `jellyfish`. (The same lexicon machinery also powers `canon_density()`, which the fork uses as a fiction signal - scored for *presence* of canon, not repair of it.)

- **Lexicon source (derived + curated):** StoryLine Codex filenames (`WRITING/STORYLINE/<Project>/Codex/**`); `### ` entity headers in `REFERENCE/bible.md`; a curated seed `REFERENCE/_LEXICON.md` for world/lore terms not in the Codex (e.g. *Witchwood*, *Godsrift*) and known mishears (`winch wood => Witchwood`).
- **Matching:** double-metaphone phonetic key + Jaro-Winkler on the surface form, best-of-window over 1-4 word spans.
- **Confidence tiers:** >=0.92 -> auto-correct; 0.86-0.92 -> flag inline `[AUTHOR: heard -> Canonical?]`; <0.86 -> left alone. Common words guarded out.
- **Project selection:** default **Witchwood**; override by filename (`godsrift_...m4a`) or by a spoken project name at the head of the clip.

## Dependencies (self-bootstrapped by `runner.py`)

`runner.py` now owns its own deps via an **import-first guard** (`_ensure_deps()`, top of file): it tries to import `faster_whisper`, `jellyfish`, `yaml`; if they already resolve (vendored, or a reuse dir already on the path) it does nothing; else it adds ONE deterministic reuse dir (`$DICTATION_DEPS`, default `/tmp/pydeps`) to `sys.path`; only as a last resort does it `pip install --no-cache-dir --target <that one dir>`. The explicit `pip install` step below is therefore **optional** — kept only as a fallback. This replaces the old blind per-run `pip install --break-system-packages …`, which scattered fresh ~481 MB copies into new dirs every run and, on an ~10 GB sandbox already carrying the 6 GB vault mount, eventually failed with *No space left on device* (^obs: sandbox-disk-pressure). Note those scattered copies end up owned by a privileged boot identity (`nobody`), so a normal task run cannot delete them — only a boot-time `/tmp` sweep can. **Fix lives above the task: the sandbox image should clear leftover `/tmp/{site,pylibs,pydeps,pipcache}` on session start.**

```
# fallback only — runner.py self-bootstraps; prefer letting it
pip install --no-cache-dir --target /tmp/pydeps faster-whisper jellyfish pyyaml
```
`pyyaml` is required by the staging-note writer (DIR-004: derived frontmatter is serialized via `yaml.safe_dump` and parse-gated, never hand-formatted). The model is **vendored** at `_models/faster-whisper-small` (offline). To (re)vendor or swap size, run on a machine with HF access:
```
huggingface-cli download Systran/faster-whisper-small --local-dir "<vault>\_models\faster-whisper-small"
```

## The scheduled task prompt (Stage A + B)

> Bootstrap is NOT required for this task. Do exactly this:
> 1. Deps are self-bootstrapped by `runner.py` (import-first guard, reuses `/tmp/pydeps`, installs `--no-cache-dir` to one fixed dir only if missing) — no separate `pip install` step needed. If you must install by hand, use `pip install --no-cache-dir --target /tmp/pydeps faster-whisper jellyfish pyyaml` (never `--break-system-packages` into the shared sandbox — that's what filled the disk).
> 2. Run `python3 "<vault>/WORKFLOWS/dictation-runner/runner.py"`. It prints JSON of what it processed; each result carries a `route` (`fiction` or `inbox`). If `processed: 0`, stop - nothing to do, no log entry.
> 3. **Fiction branch** - for each new `_DICTATION INBOX/_reconciled/*.md` not yet in `_reconciled/done/`: run the **dictation-cleanup** skill on its "Reconciled transcript" section; carry the `[AUTHOR:]` flags through; **suppress cleanup's own `_CHANGELOG` self-log** (Step 5 owns the single line); on a noisy transcript that would trip cleanup's pause/HALT, write `_drafts/<stem>-NEEDS-REVIEW.md` with a note and continue (never stall - no author present); else write `_drafts/<stem>-clean.md`; move the reconciled note to `_reconciled/done/`.
> 4. **Inbox branch** - for each new `_DICTATION INBOX/_inbox/*.md` not yet in `_inbox/done/`: read its frontmatter (`intent_hint`, `confidence`) and its "## Body (verbatim transcript)" section. Append the body **verbatim** to `INBOX.md` under the `## ⚡ Inbox` heading as a new item. If `intent_hint` is non-empty OR `confidence` is `uncertain`, prepend an HTML-comment hint on its own line immediately above the item: `<!-- voice-note <date> . intent: <intent_hint> . confidence: <confidence> -->` (the comment is a steer for the inbox-router; it is NOT part of the captured text). Do NOT classify into a domain here - that is the inbox-router's job. Move the staging note to `_inbox/done/`. Use the file tools to edit `INBOX.md`, not patch-by-heading.
> 5. Append ONE consolidated line per processed clip to `_CHANGELOG.md`, noting the route, e.g. `- dictation-runner: <stem> [fiction] (<project>, <s>s, <N> corrections) -> _drafts/<stem>-clean.md` or `- dictation-runner: <stem> [inbox] (<s>s, <confidence>) -> INBOX`.
> 6. Leave any `[AUTHOR:]` name flags in place - CRE rules them at the desk. Never bind a clip to a chapter (that is a desk action).

## Interaction with the inbox-router

The inbox branch is **decoupled**: the runner only deposits items into INBOX. The inbox-router files them on its own schedule (the `books-daily-ingest-weave` task) or when CRE says "sort the inbox." The router reads the leading `<!-- voice-note ... -->` comment as a strong steer but still files the body verbatim and parks anything ambiguous in its own Needs-review (see [[WORKFLOWS/inbox-router]]).

## Interaction with dictation-cleanup (fiction branch)

Unchanged. Stage B calls `dictation-cleanup` on the reconciled transcript (still raw dictation + flags, so it satisfies cleanup's input guard). Two adjustments persist: suppress cleanup's own `_CHANGELOG` self-log (the runner owns one consolidated line), and on cleanup's human-in-the-loop pause/HALT conditions write `<stem>-NEEDS-REVIEW.md` and continue rather than stall.

## Run modes

- **Unattended (scheduled):** empty inbox = silent no-op. Never blocks on a gate.
- **Manual:** "run the dictation runner" - same steps, on demand.

## Known v1 limits (tracked)

- The fiction/inbox **classifier is heuristic** (canon-density + register). Explicit spoken directives are the reliable control; the classifier is the forget-proofing fallback, and it defaults to INBOX when unsure. Upgrade path: LLM classify in Stage B.
- A first-person fiction passage with no canon names and no spoken directive can misroute to INBOX. Recoverable (it's just staged text); lead with "fiction" to be sure.
- Multi-word mishears whose phonetics diverge still rely on the `[AUTHOR:]` flag; tighten via `_LEXICON.md` aliases.
- Transcription accuracy = `small` model. Upgrade path: Supabase->Groq `whisper-large-v3` for Stage A only.

## Files

- `WORKFLOWS/dictation-runner/runner.py` - Stage A orchestrator: transcribe, `classify_route()` fork, `write_reconciled()` (fiction), `write_inbox_note()` (inbox). Self-locating.
- `WORKFLOWS/dictation-runner/lexicon.py` - lexicon compile + `reconcile()` + `canon_density()` (the fork's fiction signal).
- `_DICTATION INBOX/` - drop zone (`README.md`, `_reconciled/` + `done/`, `_inbox/` + `done/`, `_drafts/`, `processed/`).
- `WRITING/PROJECTS/<PROJECT>/REFERENCE/_LEXICON.md` - curated seed (per project).
- `_models/faster-whisper-small/` - vendored model.
