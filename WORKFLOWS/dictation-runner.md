---
type: workflow
name: dictation-runner
lane: fiction / os
status: active
trigger: scheduled task `dictation-runner` (polls _DICTATION INBOX/) + manual "run the dictation runner"
created: 2026-06-14
updated: 2026-06-22
purpose: Remote, phone-first DICTATION pipeline. Drop ANY audio OR a dropped .txt/.md transcript in _DICTATION INBOX/ from anywhere - a chapter you're dictating, a long-form dev session, or a random thought/task/list. A scheduled Cowork task transcribes audio (text is read directly), then forks it: fiction -> reconcile -> dictation-cleanup -> _drafts/; dev -> reconcile -> MECHANICAL cleanup -> DEV/_intake; everything else -> INBOX for the inbox-router. Nothing reaches a project or the dev intake un-cleaned, but each destination gets the right depth of cleanup. One drop zone, no toggling.
---

# dictation-runner

> **The problem this kills:** the old flow was record -> Buzz (manual desktop transcribe) -> copy-paste into Cowork -> trigger cleanup/transcode. Four hand-offs, all desktop-bound. This collapses it to: **drop audio in one folder; a polling task does the rest.** As of 2026-06-14 that one folder takes *every* kind of voice note, not just chapter dictation - the runner decides at transcription time whether a clip is fiction or a second-brain note, so you never pick a folder.

## What changed (2026-06-14): one folder, two destinations

You used to need a separate path for "dictate a chapter" vs "capture a stray thought." Now both land in `_DICTATION INBOX/`. The separation of concerns moved out of *which folder you drop into* and into a **classifier** the runner runs after transcription. The runner forks each clip to one of **three** destinations, then each branch hands off to an already-built pipeline:

- **dev** (a `dev note` / `dev capture note` / `capture the dev` marker at or near the head, preamble-tolerant) -> `<PROJECT>/DEV/_intake/`, where **[[WORKFLOWS/dev-capture|dev-capture]]** ("capture the dev") segments + routes it. *(Added 2026-06-21 — `^backlog-dictation-runner-dev-fork`; preamble-tolerance 2026-06-23 — `^backlog-dictation-runner-preamble-tolerance`.)*
- **fiction** -> the existing reconcile + cleanup path (unchanged).
- **not fiction** -> your **[[INBOX]]**, where the existing **[[WORKFLOWS/inbox-router|inbox-router]]** does all the domain sorting.

**Guardrail:** the runner NEVER writes a domain bucket or a `DEV/` content file directly. Per the vault's connector discipline ([[_VAULT MAP]]), the inbox-router is the *sole* write-path into Vibes/Tasks/Life/Knowledge/Business/Workflows, and dev-capture is the *sole* write-path into `DEV/scenes|sequences|registry`. The runner only **stages**: a non-fiction clip drops into INBOX, a dev clip into the `_dev/` pre-clean queue (and after Stage-B cleanup into `DEV/_intake/`), each with the spoken intent preserved as a hint; the downstream router files it from there.

## What changed (2026-06-22): text transcripts in, and clean-before-routing

Two folds, both consolidations rather than new machinery:

- **Long-form text transcripts now use the same door.** Drop a `.txt`/`.md` transcript (e.g. a long dev session you ran through Buzz, or any prose dictation captured as text) straight into `_DICTATION INBOX/`. Stage A skips Whisper for text and reads it directly (`read_input`); the *identical* fork, reconcile, cleanup and staging run from there. There is no separate transcript inbox — the "long-form vs short-form" split dissolved into one length-agnostic intake. The README and any `_`/`.`-prefixed file are ignored by the scan, so the drop-zone's own files are never eaten.
- **Cleanup moved ahead of the routing move, tiered per destination.** The principle (CRE ruling): nothing reaches a project, a chapter draft, or the dev intake un-cleaned — but cleanup is *tiered to the destination*. **Fiction** → the full fiction `dictation-cleanup`. **Dev** → **mechanical cleanup only** (Pass 1, optionally Pass 2): dev talk is loose, note-like development thinking, not prose, so the fiction-specific dialogue/scene passes are the wrong tool. **Inbox** → **verbatim** (the inbox-router's contract is to file raw). To honor "clean before the move," the dev branch no longer writes `DEV/_intake/` directly — Stage A reconciles it and stages it to a new `_dev/` **pre-clean queue**, and Stage B cleans it before it lands in `DEV/_intake/`. The dev branch is now name-reconciled too (dev talk carries garbled canon names just like prose).

## What changed (2026-07-11): gateway sidecar transcription (voice-gateway P3)

Stage A's transcription quality jumped from `faster-whisper-small` to **`large-v3-turbo` on the aegis-moon GPU** without re-plumbing anything, via a sidecar relay ([[SYSTEM/voice-gateway]] P3):

- **Desktop relay** — scheduled task `voice-gateway-transcribe` (`SYSTEM/maintenance/gateway-transcribe.ps1`, every 5 min, idle-≥30s guard, atomic tmp→rename, log `gateway-transcribe.log`): POSTs each new audio clip at the inbox root to the voice-gateway (`:8446`, profile guessed from the filename stem) and saves the response as a **`<clip>.gateway.json` sidecar** beside it. A FAIL just logs — the next 5-min pass retries while the sidecar is absent.
- **Runner** — `read_input()` consumes the sidecar's **pre-reconcile `raw_text`** when present (the relay's profile is only a filename guess; the runner's own classify→reconcile with the CLASSIFIED project's lexicon stays the single canonical correction path) and tags the staging note `model: voice-gateway/whisper-large-v3-turbo`. **No/unreadable sidecar → the vendored `small` fallback, automatically** — the relay or server being down is a quality downgrade, never a stall. The sidecar rides along to `processed/` with its clip.
- **Why a relay:** the Cowork sandbox running Stage A cannot reach the tailnet, and the desktop has no python — so the desktop does the POST (same scheduled-task family as `vault-transport-sweep`), and the runner just reads a file. Text drops (`.txt`/`.md`) are unaffected (read directly, no relay involvement).

## Architecture - one polling loop, read-then-fork-then-clean

```
phone/desktop --Dropbox--> _DICTATION INBOX/<clip>.{m4a | txt,md}
                                              |
              scheduled task "dictation-runner" wakes (~every 30 min)
                                              |
  STAGE A . deterministic (runner.py, no LLM)
   * AUDIO -> faster-whisper-small (vendored, offline) transcribes
     TEXT (.txt/.md) -> read directly, no transcription (read_input)
   * classify_route(): decide dev vs fiction vs inbox (see "The fork" below)
   |
   |-- DEV ("dev note" / "capture the dev" at head):
   |     * canon name-reconcile (dev talk carries canon names too)
   |     * writes _dev/<clip>.md  PRE-CLEAN queue (reconciled + raw audit + dest)
   |     * (no DEV/ tree for that project -> falls back to INBOX, verbatim)
   |
   |-- FICTION:
   |     * canon name-reconcile (garbled proper nouns vs Codex + bible + _LEXICON.md)
   |     * writes _reconciled/<clip>.md  (reconciled text + corrections + raw audit)
   |
   |-- INBOX (everything else):
   |     * writes _inbox/<clip>.md  (verbatim transcript body + intent hint + confidence)
   |
   * moves the source clip to processed/
                                              |
  STAGE B . the skills (this Cowork session) -- CLEAN, THEN LAND
   |-- for each new _reconciled/*.md:  dictation-cleanup (full) -> _drafts/<clip>-clean.md
   |                                    -> move note to _reconciled/done/
   |-- for each new _dev/*.md:          MECHANICAL cleanup only -> <PROJECT>/DEV/_intake/<clip>.md
   |                                    -> move note to _dev/done/  (then "capture the dev" routes)
   |-- for each new _inbox/*.md:        append body VERBATIM to INBOX (with intent-hint comment)
   |                                    -> move note to _inbox/done/
   * logs one consolidated line per clip to _CHANGELOG (noting route: dev/fiction/inbox)
                                              |
  (decoupled) the inbox-router files new INBOX items ("sort the inbox"); dev-capture
  files DEV/_intake/ notes ("capture the dev") - each on its own trigger.
```

**Why polling, not triggers:** every "who fires whom" hand-off was the brittle part and impossible to drive from a phone. A single scheduled task watching one folder removes them all. **Transport CUTOVER 2026-07-10 (`^backlog-server-transport`): phone capture now rides Nextcloud, not the Dropbox app.** Phone drops go to `VAULT TRANSPORT/_DICTATION INBOX` (Nextcloud app → aegis-moon → desktop Nextcloud client), and the desktop scheduled task **`vault-transport-sweep`** (`SYSTEM/maintenance/sweep-transport.ps1`, every 5 min, idle-≥60s guard, moves logged to `transport-sweep.log`) moves them into the vault's `_DICTATION INBOX/` — where this runner picks them up exactly as before. Drop zone, runner.py, and the scheduled-task prompt are all UNCHANGED (the sweep lives desktop-side because the Cowork sandbox can't see the Nextcloud folder). Dropbox remains the vault's own sync, and desktop drops straight into `_DICTATION INBOX/` still work.

## The fork (classify_route, Stage A detail)

The runner decides dev-vs-fiction-vs-inbox in this order. The whole thing is biased so that **uncertainty resolves to INBOX** - all branches are non-destructive staging (a holding draft in `_drafts/`, a dev note in the `_dev/` pre-clean queue, or text in INBOX), the downstream routers can segment a mixed clip and review-bin anything ambiguous, and the fiction branch never commits to a chapter on its own. So a wrong guess is always cheap and recoverable; a stray thought never lands silently inside a chapter.

0. **Explicit dev directive at/near the head (highest priority, wins over fiction).** A dev marker — **`dev note`**, **`dev capture note`**, or **`capture the dev`** — at the head *or after a short discourse lead-in* routes to `dev`. **Preamble-tolerance (2026-06-23, `^backlog-dictation-runner-preamble-tolerance`):** the marker is detected in a short flattened lead-in window (first ~20 words, punctuation neutralized), so a run-up like *"Okay, let's do a dev note…"* no longer defeats it — the prior `^`-anchored check missed all four 2026-06-23 Witchwood notes; the marker set also now covers the spoken **"dev capture note"** form, not just "dev note"/"capture the dev". A spoken project name (searched a little wider, into sentence 1–2) resolves *which* project's DEV tree (e.g. `"…dev capture note for Witchwood…"`); omit it and the project defaults to Witchwood, flagged `uncertain`. A sub-cue keyword (`scene`, `sequence`, `character`, `place`, `location`, `world`, `lore`, `item`/`object`, `project`, plurals OK) is preserved as a `subcue_hint` for dev-capture. If the resolved project has no `DEV/` tree, the clip falls back to INBOX, verbatim (no silent scaffold). The marker stays narrow + multi-word by design so it never fires mid-prose (guarded against "develop", a "dev camp" mention, and a filler lead-in with no marker). The dev clip is canon-reconciled and staged to the `_dev/` pre-clean queue; **Stage B then runs mechanical cleanup only** (not the full fiction cleanup — dev talk isn't prose) before it lands in `DEV/_intake/`, after which you run "capture the dev" to route it.
1. **Explicit spoken directive at the head of the clip.** A keyword *or* a natural-language instruction in the first clause, honored deterministically:
   - **Fiction markers:** `fiction`, `chapter`, `scene`, `dictation`, `slate`, `prose`, `manuscript`, `draft`, `narration`, or a **project name** (`Witchwood`, `Godsrift`, `Ghost River`, `Darkbloom`). A spoken project name also overrides the filename's project. *(A leading `dev note` overrides these — see 0.)*
   - **Inbox markers:** `inbox`, `task`, `to-do`, `reminder` / `remind me`, `note to self`, `idea`, `vibe`, `capture`, `thought`, `list`, `file under ...`, `add to ...`, `put in ...`, `business`, `marketing`, `knowledge`, `workflow`, `backlog`.
   - The runner peels the directive clause off the body at the first separator (`:` `,` `-`) and keeps it as a **routing hint** for the inbox-router. Recommended phrasing: *say the directive, a slight pause/comma/colon, then the note.* Without a separator the directive stays in the body (harmless) and routing still works.
2. **No explicit directive -> heuristic classifier.** Two deterministic signals:
   - **canon-density** (the strongest signal, and one Stage A is uniquely good at): how many high-confidence canon names per 100 words. A clip dense in Witchwood/Godsrift vocabulary in narration is almost certainly prose.
   - **register**: third-person + past tense + quoted dialogue lean fiction; first-person + to-do/imperative cues (`remember to`, `need to`, `call`, `email`, `renew`, lists) lean inbox.
3. **Low signal either way -> INBOX, flagged `uncertain`.** Defaulted there for the router (and its Needs-review) to handle.

**v1 is heuristic by design.** The explicit directive is the primary control; the classifier is just the fallback for when you forget. Tunable knobs live at the top of `runner.py` (`CANON_STRONG`, `FICTION_SCORE`, `INBOX_SCORE`). Upgrade path: swap the heuristic for an LLM classify step in Stage B (see `_BACKLOG`); the fork interface stays the same.

## Scope boundary (still true)

- **Automated:** transcribe audio (or read a dropped `.txt`/`.md` transcript) -> fork -> clean at the right depth -> (fiction) holding draft in `_drafts/`, (dev) cleaned note in `DEV/_intake/`, or (inbox) verbatim item in `INBOX`. All non-destructive staging.
- **Stays a desk action:** the **transcoder/slate** into a specific `CHAPTER N/` `draft.md`. It needs an `envelope.md` (perceptual POV) and a chapter target - not on-the-go inputs. At the desk you route a holding draft into a chapter and run `slate this dictation` as usual.

## The name-reconcile (Stage A, fiction + dev branches)

Lives in `WORKFLOWS/dictation-runner/lexicon.py` + `runner.py`. Deterministic, stdlib + `jellyfish`. Runs on the **fiction and dev** branches (both carry canon names — the dev reconcile was added 2026-06-22); the inbox branch is left verbatim. (The same lexicon machinery also powers `canon_density()`, which the fork uses as a fiction signal - scored for *presence* of canon, not repair of it.)

- **Lexicon source (derived + curated):** StoryLine Codex filenames (`WRITING/STORYLINE/<Project>/Codex/**`); `### ` entity headers in `REFERENCE/bible.md`; a curated seed `REFERENCE/_LEXICON.md` for world/lore terms not in the Codex (e.g. *Witchwood*, *Godsrift*) and known mishears (`winch wood => Witchwood`).
- **Matching:** double-metaphone phonetic key + Jaro-Winkler on the surface form, best-of-window over 1-4 word spans.
- **Confidence tiers:** >=0.92 -> auto-correct; 0.86-0.92 -> flag inline `[AUTHOR: heard -> Canonical?]`; <0.86 -> left alone. **Short (≤1-word) targets need ≥0.95 to auto.** An all-common heard span (everyday words + stopwords — `which`, `the dark`, `moon was`) is **suppressed outright** (kept verbatim, no flag) by the `COMMON_EN`/`STOPWORDS` guard — the deterministic half of flag-noise control (^obs-119, see § below).
- **Project selection:** default **Witchwood**; override by filename (`godsrift_...m4a`) or by a spoken project name at the head of the clip.

## Flag-noise control (two layers)

Canon-dense notes used to drown in false-positive `[AUTHOR:]` flags: short canon names (Witch, Heartbox, Dark Vale, Moon Sea) fuzz-match everyday words (which, hear, dark, moon). One macro dev note (part-two, the-last-mountain) carried ~31 such flags, nearly all reasoned away by context. Two layers now keep the flag stream honest (^obs-119):

1. **Stage A — deterministic `COMMON_EN`/`STOPWORDS` guard (`lexicon.py`, runs every clip).** A non-alias fuzzy match whose heard span is *entirely* common words + stopwords is suppressed at the source — kept verbatim, no flag. A genuine garble always carries a substantive uncommon token (`dark `**`veil`**, **`widow's`**` bane`, `wych`), so it still corrects. Catches single tokens AND all-common multi-word spans the matcher pulls together (`the dark`, `moon was`, `with wood`, `light of the moon`). Crucially this also stops the worst case — an all-common span scoring ≥0.92 was being *silently AUTO-applied* (`moon was` → `The Moon Sea`), not even flagged.

2. **Stage B — context triage pass (the agent, task Step 4c).** Walks the *remaining* flags with sentence context and downgrades the obvious plain-word ones the stoplist deliberately can't — spans carrying an uncommon token (`dark cavern`, `moon runes`, `dark side`). Downgrade-only (never invents/applies), logs every clear to a `## Triage` block, route-aware (aggressive on dev, conservative on fiction prose). The LLM layer the deterministic guard cannot be.

Net: Stage A removes the bulk of the over-fire deterministically before anything is written; Stage B clears the contextual residue and logs it; only genuinely ambiguous names reach CRE's desk. `lexicon.py --selftest-common` covers the Stage-A guard.

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
> 2. **Stage the runner off the mount, then run it (`^obs-103` structural kill).** NEVER run `runner.py` directly off the Dropbox mount — the mount can serve a stale, TRUNCATED copy of the *script* (the `^obs-073`/`^obs-095` hazard; a truncated script is wrong **behavior**, not just wrong data) that crashes `python3` with a SyntaxError. Instead always run a clean copy read via the **file tools** (cloud-authoritative — they serve the full file): read `runner.py` **and** `lexicon.py` via the file tools and **write both to the session outputs folder** (the Write tool reaches the outputs folder, NOT sandbox `/tmp`; outputs is session scratch — not Dropbox-synced, so never stale-truncated — and bash reads it at `/sessions/*/mnt/outputs/`). Both must land in the same dir (`runner.py` imports `lexicon` as a sibling). Then `OUT=$(ls -d /sessions/*/mnt/outputs|head -1); VAULT_ROOT="<vault>" python3 "$OUT/runner.py"`. `runner.py` reads `VAULT_ROOT` for every vault path (inbox, vendored `_models`, lexicon sources), so all reads/writes land in the **real** vault while the *code* runs from the clean staged copy — the mount copy of the script is never trusted (sanity: `py_compile "$OUT/runner.py"`; if a staged file won't compile, re-read via the file tools, never fall back to the mount; you may instead bash-`cp` the outputs copy into `/tmp` and run there). It prints JSON of what it processed; each result carries a `route` (`dev`, `fiction`, or `inbox`) and a `source` (the clip filename — audio, or a dropped `.txt`/`.md` transcript, which the runner reads directly with no model). If `processed: 0`, stop - nothing to do, no log entry.
> 3. **Fiction branch** - for each new `_DICTATION INBOX/_reconciled/*.md` not yet in `_reconciled/done/`: run the **dictation-cleanup** skill on its "Reconciled transcript" section; carry the `[AUTHOR:]` flags through; **suppress cleanup's own `_CHANGELOG` self-log** (Step 5 owns the single line); on a noisy transcript that would trip cleanup's pause/HALT, write `_drafts/<stem>-NEEDS-REVIEW.md` with a note and continue (never stall - no author present); else write `_drafts/<stem>-clean.md`; move the reconciled note to `_reconciled/done/`.
> 4. **Inbox branch** - for each new `_DICTATION INBOX/_inbox/*.md` not yet in `_inbox/done/`: read its frontmatter (`intent_hint`, `confidence`) and its "## Body (verbatim transcript)" section. Append the body **verbatim** to `INBOX.md` under the `## ⚡ Inbox` heading as a new item. If `intent_hint` is non-empty OR `confidence` is `uncertain`, prepend an HTML-comment hint on its own line immediately above the item: `<!-- voice-note <date> . intent: <intent_hint> . confidence: <confidence> -->` (the comment is a steer for the inbox-router; it is NOT part of the captured text). Do NOT classify into a domain here - that is the inbox-router's job. Move the staging note to `_inbox/done/`. Use the file tools to edit `INBOX.md`, not patch-by-heading.
> 4b. **Dev branch (clean before it lands)** - for each new `_DICTATION INBOX/_dev/*.md` not yet in `_dev/done/`: run **MECHANICAL cleanup only** on its "## Reconciled transcript" section — i.e. `dictation-cleanup` Pass 1 (mechanical: STT-error fixes, punctuation, verbal-cue resolution; prompt `WORKFLOWS/prompts/dictation/1. Dictation Clean Up`) and optionally Pass 2 (paragraphing). **Do NOT run Passes 3–4** (dialogue-tag thinning, scene polish) — dev talk is loose, note-like development thinking, not prose. Carry any `[AUTHOR:]` flags through. Then write the cleaned transcript to the staging note's `dest` (`<PROJECT>/DEV/_intake/<stem>.md`): **carry the staging note's serialized YAML frontmatter block verbatim** (do not re-format it — DIR-004), set `status: cleaned`, and put the cleaned text under a `## Body (cleaned transcript)` heading. On a transcript too noisy to clean cleanly, write the note with the reconciled text + an `[AUTHOR: noisy — review]` flag rather than stalling (no author present). Move the staging note to `_dev/done/`. CRE then runs **"capture the dev"** to segment + route it into the `DEV/` tree — the runner stages, dev-capture stays the sole write-path into `DEV/scenes|sequences|registry`. Do NOT run dev-capture from this unattended task. (Stage A already handled the no-DEV-tree fallback to INBOX, so any `_inbox/` note is processed by Step 4.)
> 4c. **Flag-triage (context pass) — fiction + dev branches, AFTER cleanup, BEFORE the write.** Walk every remaining `[AUTHOR: heard → Canonical?]` flag in the cleaned text and judge it in its sentence. If the heard word is plainly the everyday English word in that grammatical slot (a relative pronoun "which", the verb "hear"/"watch", the adjective "dark", the common noun "moon") and the canon proper noun would not make sense there, **downgrade** it — delete the flag and restore the heard word verbatim. **Rules:** (a) **downgrade-only** — you may only ever drop a flag and keep the author's original word; never invent, apply, or upgrade a substitution; (b) when genuinely ambiguous, **KEEP the flag** (CRE rules it at the desk); (c) log each flag you cleared in a `## Triage` block at the foot of the note (`heard | proposed | kept-as | reason`) so a wrong clear is auditable. **Route-aware aggressiveness:** on **dev** material be aggressive (loose notes CRE re-reads anyway — a missed canon fix is cheap); on **fiction** be conservative — keep any flag you are not certain about, since a wrong silent keep in prose costs more than an extra flag. This is the LLM layer the deterministic Stage-A `COMMON_EN`/`STOPWORDS` guard cannot do: it clears the multi-word residue (`dark cavern → Dark Vale?`, `moon runes → The Moon Sea?`) carrying an uncommon token that the stoplist deliberately leaves. Inbox branch is exempt (it stays verbatim, no flags). See § Flag-noise control.
> 5. Append ONE consolidated line per processed clip to `_CHANGELOG.md`, noting the route, e.g. `- dictation-runner: <stem> [fiction] (<project>, <s>s, <N> corrections) -> _drafts/<stem>-clean.md`, `- dictation-runner: <stem> [inbox] (<s>s, <confidence>) -> INBOX`, or `- dictation-runner: <stem> [dev] (<project>, <s>s, <subcue>) -> DEV/_intake`.
> 6. Leave any **genuinely ambiguous** `[AUTHOR:]` name flags in place (Step 4c clears only the obvious funcword false positives — downgrade-only and logged) - CRE rules the rest at the desk. Never bind a clip to a chapter (that is a desk action).

## Interaction with the inbox-router

The inbox branch is **decoupled**: the runner only deposits items into INBOX. The inbox-router files them on its own schedule (the `books-daily-ingest-weave` task) or when CRE says "sort the inbox." The router reads the leading `<!-- voice-note ... -->` comment as a strong steer but still files the body verbatim and parks anything ambiguous in its own Needs-review (see [[WORKFLOWS/inbox-router]]).

## Interaction with dictation-cleanup (fiction = full, dev = mechanical only)

**Fiction branch — unchanged.** Stage B calls the full `dictation-cleanup` on the reconciled transcript (still raw dictation + flags, so it satisfies cleanup's input guard). Two adjustments persist: suppress cleanup's own `_CHANGELOG` self-log (the runner owns one consolidated line), and on cleanup's human-in-the-loop pause/HALT conditions write `<stem>-NEEDS-REVIEW.md` and continue rather than stall.

**Dev branch — mechanical passes only (added 2026-06-22).** Stage B runs *only* `dictation-cleanup`'s mechanical pass (Pass 1, optionally Pass 2 paragraphing) on the `_dev/` queue item, never Passes 3–4. The reason is the distinction CRE drew: `dictation-cleanup` is a *fiction prose* copy-edit (dialogue formatting, scene polish), and dev notes are loose, note-like development thinking — the prose passes would mangle them. This also tightens the seam with `dev-capture`, whose Path B expects an already-cleaned transcript: the dev intake now only ever sees mechanically-cleaned text, never raw STT. The inbox branch stays verbatim — no fiction cleaner touches it.

**Flag-triage runs after cleanup on both flag-bearing branches (added 2026-06-26).** On the fiction and dev branches, after cleanup and before the write, Step 4c walks the surviving `[AUTHOR:]` flags and downgrades the obvious funcword false positives in context (downgrade-only, logged, aggressive on dev / conservative on fiction). It pairs with the deterministic Stage-A `COMMON_EN`/`STOPWORDS` guard — see § Flag-noise control. Inbox stays verbatim and is exempt.

## Run modes

- **Unattended (scheduled):** empty inbox = silent no-op. Never blocks on a gate.
- **Manual:** "run the dictation runner" - same steps, on demand.

## Known v1 limits (tracked)

- The fiction/inbox **classifier is heuristic** (canon-density + register). Explicit spoken directives are the reliable control; the classifier is the forget-proofing fallback, and it defaults to INBOX when unsure. Upgrade path: LLM classify in Stage B.
- A first-person fiction passage with no canon names and no spoken directive can misroute to INBOX. Recoverable (it's just staged text); lead with "fiction" to be sure.
- Multi-word mishears whose phonetics diverge still rely on the `[AUTHOR:]` flag; tighten via `_LEXICON.md` aliases. **Funcword over-fire** (everyday words mis-flagged as short canon names) is handled by the two-layer flag-noise control (Stage-A `COMMON_EN` guard + Stage-B triage, ^obs-119), not aliases.
- ~~Transcription accuracy = `small` model.~~ **UPGRADED 2026-07-11 (voice-gateway P3):** audio clips are transcribed by `large-v3-turbo` on the aegis-moon GPU via the gateway sidecar relay (see § What changed 2026-07-11); the vendored `small` model remains the automatic fallback when no sidecar exists (relay/server down, or the runner wakes before the 5-min relay pass — recoverable quality downgrade only). The old Supabase→Groq path is superseded.
- **The fork has three destinations — dev, fiction, or INBOX** (the `dev` route added 2026-06-21, `^backlog-dictation-runner-dev-fork`). Sub-cue detection for a dev clip is head-only: a sub-cue after a sentence-ending period (e.g. `"capture the dev. character — …"`) isn't captured as the `subcue_hint`, which is harmless since dev-capture re-segments the full body anyway. The dev marker set is the narrow phrase `dev note` / `capture the dev` by design — broader words like a bare "develop" were dropped (CRE ruling) to avoid firing mid-prose.
- **Text intake (added 2026-06-22):** dropped `.txt`/`.md` transcripts share the one drop zone — Stage A reads them directly (`read_input`), skipping Whisper. The drop-zone's own `README.md` and any `_`/`.`-prefixed file are excluded from the scan so they're never ingested; name a transcript anything else. A text clip reports `language: text`, `audio_seconds: 0.0`.
- **Dev cleanup is mechanical-only (added 2026-06-22):** the dev branch is reconciled + staged to `_dev/`, then Stage B runs only `dictation-cleanup` Passes 1–2 before it lands in `DEV/_intake/` — matching `dev-capture`'s Path B (cleaned-transcript input) without prose-shaping loose notes. If you ever want light cleanup on the *inbox* branch too, that's a separate non-fiction normalizer, not this fiction cleaner (see `_BACKLOG`).

## Files

- `WORKFLOWS/dictation-runner/runner.py` - Stage A orchestrator: `read_input()` (audio→transcribe | text→read), `classify_route()` fork, `write_dev_stage()` (dev pre-clean queue), `write_reconciled()` (fiction), `write_inbox_note()` (inbox). Self-locating.
- `WORKFLOWS/dictation-runner/lexicon.py` - lexicon compile + `reconcile()` + `canon_density()` (the fork's fiction signal).
- `_DICTATION INBOX/` - drop zone, accepts audio + `.txt`/`.md` transcripts (`README.md`, `_reconciled/` + `done/`, `_dev/` + `done/`, `_inbox/` + `done/`, `_drafts/`, `processed/`).
- `WRITING/PROJECTS/<PROJECT>/DEV/_intake/` - dev destination: Stage B writes the **mechanically-cleaned** transcript here (from the `_dev/` queue) for [[WORKFLOWS/dev-capture]] to pick up.
- `WRITING/PROJECTS/<PROJECT>/REFERENCE/_LEXICON.md` - curated seed (per project).
- `_models/faster-whisper-small/` - vendored model (now the FALLBACK; primary transcription is the gateway sidecar).
- `SYSTEM/maintenance/gateway-transcribe.ps1` + scheduled task `voice-gateway-transcribe` (5 min) - the desktop relay that writes `<clip>.gateway.json` sidecars ([[SYSTEM/voice-gateway]] P3).
