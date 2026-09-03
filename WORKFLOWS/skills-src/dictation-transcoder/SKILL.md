---
name: dictation-transcoder
description: Convert raw dictation into a cold-floor rough-draft slate — Cut to the perceptual envelope, Synthesize the survivors, Normalize to the narrator-rules floor — then present the spine-review gate (seam flags, scene map). This is the GENERATIVE stage of fiction dictation (v6.1). Use whenever CRE asks to "slate this dictation," "transcode this," "run the slate," "slate it," "floor the dictation," or wants rough-draft prose produced from a speech-to-text transcript inside a vault using the per-chapter folder convention (envelope.md + dictation/ + slate/); also as Leg 1 of chapter-clean. Ships scripts/slate_scaffold.py (run allocation, four-file stubs with one serialized schema, derived runs, gate check) and references/slate-contract.md. Do NOT use for word-preserving cleanup of dictation (dictation-cleanup), for revising drafted prose (register-pass / line-edit), for the floor SHEET over existing prose (prose-expansion Entry mode B), or to fill the envelope (dictation-preflight).
---

# Dictation Transcoder (v6.1)

> Canon: `WORKFLOWS/transcoder.md`. This is the trigger surface; the doc is the law. v6.1 = v5.1's dictation-artifact rules + v6's Operation 3 floor, heat bank, spine-review gate + v6.1's scene map. Contract rulings of 2026-09-02 (frontmatter schema, four files always, derived runs, author gaps, clean-ledger placement) live in `references/slate-contract.md`.

You are converting raw dictation into a **floor draft** — cold observational narration per `KNOWLEDGE/PROSE FRAMEWORK/narrator-rules`, the substrate the expansion passes build on. This is pre-prose becoming a draft, not a draft becoming polished. You are **generative**: you may rewrite, fuse, and regenerate clean sentences. The author was talking, not writing, and expects prose back, not a marked-up transcript.

Three operations, in order: **Cut → Synthesize → Normalize to floor.** Nothing else. You do not polish and you do not assess quality beyond the floor rules; `dictation-cleanup` and the downstream passes own that.

---

## Step 0 — Sentinel, version, scaffold

Run the shell first; it does the bookkeeping so you do not re-derive it each run:

```
python scripts/slate_scaffold.py new --chapter "<chapter folder>" [--tense past|present]
```

It checks the vault sentinel (`_DIRECTIVES.md` → `type: ai-os-brain`, `file: directives` — mismatch halts; never scaffold into a folder that merely looks empty), reads the segment slugs from `envelope.md`, picks the newest dictation in `dictation/` that has no run yet, allocates `slate/YYYY-MM-DD-NN/`, writes the four stub files with the ruled frontmatter, and prints the two changelog stubs. Prefer running it on the desktop (Desktop Commander, Windows `python`) — the sandbox mount serves stale files and its bash grant is sometimes denied.

**Creative-lane load (ratified 2026-09-03):** after the sentinel passes, read `_CREATIVE DIRECTIVES.md` from the mounted root (CDIR-001–010 — how AI behaves around CRE's craft; CDIR-001 bounds the generative floor, CDIR-003 the heat bank) before opening any project file. `_DIRECTIVES` wins on OS matters, `_CREATIVE DIRECTIVES` on craft-behavior, CRE's instinct over both. Missing → proceed and note it; it is not a sentinel.

**Read its WARN lines.** `VERSION` means the canon doc and this skill disagree — run from the canon and say so in the ledger (DIR-009's announce-the-gap). `DICTATION` with several candidates means it guessed newest-by-mtime — confirm the clip with CRE before writing a word (a chapter's dictation may span clips; `chapter-clean` binds them explicitly).

If the script halts on `ENVELOPE`, do not guess one. Either CRE fills it (`dictation-preflight`), or **standalone/episode mode** applies: the folder's own canon (runway ruled-facts, premise sheet, decisions ledger, dated rulings) already rules the envelope facts → derive `envelope.md` from those with per-segment provenance and `status: derived — author confirms`, then re-run `new`. Attended only. If the canon does not rule the facts, stop and say so — a fabricated envelope is worse than no slate.

## Step 1 — Read the inputs the way the run needs them

1. **The envelope**, segment by segment: who perceives, in what conditions (place, weather, light, time), in what state (what consumes their attention). The Cut runs against this and nothing else.
2. **The dictation.** Whole thing, once, before touching anything. Mark where the perceptual world changes (light, temperature, location, who she attends to) and confirm the segmentation matches the envelope's; where it does not, say so before transcoding. Segment by envelope only — never by how finished a span looks (dictation arrives mechanically cleaned; polish is not a maturity cue; treat every span as rough).
3. **The reconciler table**, if the dictation arrived through the runner with a name-reconciler corrections table. Read it before the Cut. Any multi-word canon term substituted below a 1.00 exact-alias score is suspect — `dark hole` → *Dark Vale* at 0.92 rewrote three of CRE's phrases on CH12. Restore the dictated phrase and list each under `## Reconciler restorations`. A rescue may ask a question; it may never make a decision (DIR-014).
4. **Ruled lines.** Sweep the folder's own canon (premise, runway, blind-read resolutions, notes, rulings tables) for lines CRE has ruled verbatim. Carry them byte-exact — never cut, re-tense, compress, or improve — and list them under `## Ruled lines — preserved`. A ruled line that collides with a floor rule or the tense choice is flagged, not resolved.
5. **Secrets.** Credentials, keys, tokens in the dictation → stop and flag before anything is written (DIR-001).

## Step 2 — Dictation artifacts (handle before and during the Cut)

Four things recur in any spoken draft. Each has a rule; none is a judgment call about the story.

**Frame-talk → cut, reason `frame`.** "Okay so the story opens with…", "cut to…", "The End", mid-dictation self-repairs, stage-direction summary. Summary-mode narration ("we see her do X") renders as scene, never as report. Exception: author shorthand that already works as free indirect in POV stays as the carrier — his words doing the work beat invented narration. **Frame that carries information is cut from the prose and kept in the ledger** under `## Mic metadata`: a title spoken at the mic, a scene name, a segment cue, an answer to a runway or brief `<<UNCERTAIN>>` flag ("the old man lives"). Record it; never action it; never grade the draft against the plan for having answered it (DIR-017).

**Tense drift → normalize and declare.** Detect the dominant tense. A project ruling wins; otherwise normalize to dominant, state the choice in `tense:`, and raise it as a ledger question. Never re-tense a ruled line — leave the seam visible and surface it.

**Capture-then-tag inversions → reattach, don't flag.** CRE dictates forward while watching the story, so content often arrives before its label: *"Everything is terrible, the next title."* A trailing appositive naming the span just spoken (…the next title / the caption / he calls it) is a tag, not narration — never cut as frame, never read as garble. Fold it into reading order where the reader needs the label, or keep the inversion when it carries rhythm; note the call. When drift separates a tag from its content, reattach and re-read — what remains is usually clean. First suspect on any "garbled" span containing a naming word.

**STT garbles → two lanes.** One plausible reading ("unkept" → "unkempt") fixes silently, cut-log reason `mechanical`. Two readings that both parse ("layer"/"lair") keep the dictated form and become a G-numbered ledger question. A garble on a **load-bearing climax line is always flag-don't-fix** — mark it `<<GARBLE-UNRESOLVED: Gn>>` in the draft. (CH12's kiss-to-die garble: the likeliest machine guess would have split her line into two; CRE resolved it as one line of dialogue.)

## Operation 1 — Cut to the perceptual envelope

One test on every span, down to the modifier: **would this character perceive or register this, here, in this exact moment?** Cut what fails — narrator-injected information she cannot see (another room, the future, underground); detail too fine for the conditions or her state (black ice glinting in a night blizzard mid-struggle); modifiers smuggling unperceivable precision onto a noun that is fine. Keep everything inside the envelope, including coarse, violent, immediate sensation — the filter removes fineness the moment cannot support, not intensity. Run it against the **local** envelope of each segment.

Objective and recoverable. Apply, log each cut with its one-word reason, do not agonize.

## Operation 2 — Synthesize the survivors

Find clusters — adjacent spans serving one communicative function. Per cluster: **extract the payload** in one plain phrase; **draft a carrier** (you may invent language here); **challenge it against its shortest viable form** — can the payload survive one fewer beat? A carrier with two clauses doing one job has been thinned, not compressed. Default suspicion: multi-clause is one clause too long until proven otherwise.

**Exception — repetition that is the payload.** A repeated structure carrying escalation, ritual, or ear-order (a swipe-refusal loop, a mantra, a knock repeated) is the function; flattening it destroys it. Compress within each repeat, never across the run, and note the kept repetition. Audio-first material leans on this.

Governing order: payload fidelity, then economy, then concrete/visual language — concreteness is a preference, not a law.

Inside any line you keep or write: a **redundant modifier** whose work its noun already does ("fire-kissed ember") is freight even in a clean image; a **verb that fights the payload** ("the boy hung against her" when the payload is *still alive*) gets replaced — the verb is the most load-bearing word. Across lines: an **image carried twice in close range** ("hot as an ember" / "dead things cooled") is a doubled clause at motif scale — identify the stronger, surface the other in the ledger, never keep both and call it a rhyme.

Work cluster-local. If synthesis drops an entity a later line needs, list it under `## Continuity touched`; do not preserve clutter to protect a back-reference.

## Operation 3 — Normalize to floor (v6)

Run the `narrator-rules` deny-lists over the whole draft — every kept line and every carrier you invented. Deny-list enforcement, near-deterministic; it replaces a flagged span with its floored form and adds no new license. Priority order:

1. **Seam-breaks** — hedges ("seemed to," "as if," "she must have imagined") and alarm-labels ("horrifying," "monstrous").
2. **Filter verbs** — saw/heard/felt/noticed/realized/thought/wondered + "she knew that" frames. Cut the verb, land the object. **Exception, with its discriminator:** does the object's arrival or absence constitute the event, or does her *registering* of it? "The bark came from beyond the wall" → land the object. She has been listening for it and the moment is that she finally hears → the registering is the event; keep the verb and log `filter-kept: registering is the event` in the floor ledger. Sustained attention on a person resolves the same way.
3. **Editorial descriptors** — narrator-stance modifiers (*brutal* white, *cruel* winter). Manner adverbs by the **camera test**, not wholesale: feeling-adverbs floor; physical-fact adverbs survive; agency-implying line-sitters ("carefully," "weakly") are judgment calls, never auto-cut.
4. **Narrator glossing** — naming what a moment means, diagnosis, telling the reader how to feel, interiority restating what the page shows.
5. **Non-functional setting** — setting admitted only at the moment of action or use.

**Before you floor or option a figurative line, check motif continuity.** Does it complete an image planted earlier in the draft ("It breathed in her hope and spit out failure" after "The Last Mountain breathed in darkness")? If so it is a motif beat, not a stray abstraction — option it on *that* ground, so CRE rules on the real reason. CH12's OPTIONED-3 was the right call for the wrong stated reason; the reasoning is what he rules on.

**POV baseline: rules-within-ruled-POV.** Witchwood floors in close third. The deny-lists are camera-agnostic; never re-rig a project's camera.

**Floor ledger.** Every normalization: original → floored → rule cited. Nothing silently lost.
**Heat bank.** Dictated warm/hot language the floor strips is banked **verbatim, per beat**. It is CRE's raw material for expansion step 7; the machine never discards banked heat and never invents replacement heat.
**Cold hand, warm wound.** Strip labels, never the image's charge. A floored line that lost its image was over-cut — restore the image, cut only the label.

## Register invariants (while inventing carriers)

Never name the load-bearing emotion — render it through body, action, object. **Where the direction is two-way, option, never decide:** both carriers in the ledger under `## Optioned`, the reading behind each, one in the draft marked `<<OPTIONED-N>>`. Committing to a direction you have flagged as uncertain is the failure this rule exists to prevent; the machine's three two-way calls on CH12 were exactly the three CRE kept. Every metaphor stays inside the world the character cannot leave. Prefer sensory over abstract, subject to economy.

**Do not contaminate the carriers you invent.** Inventing language is the moment a model reaches for "good writing": no elevated vocabulary, no euphemism for blunt words, no beautified ugliness, no added internal gestures ("he swallowed," "her chest tightened"), no clever closing line. Scan invented carriers against `REFERENCE/contamination-checklist.md` when it exists; list what you caught and removed under `## Contamination check`. You are handing back CRE's scene in clean prose, not a literary improvement of it.

## No silent leaves

A permissive segment (firelit, calm) yields few cuts, and "no cuts" is where you most likely relaxed instead of read. In **every** segment list each named-emotion or dissolved-telling span you left standing, with one verdict: `incidental` · `dialogue` · `floored` · `optioned` · `repaired` · `dilution`. A state named 3+ times in a segment is **one** `dilution` entry (state, count, strongest instance) — three separate lines read as three shrugs and the real problem disappears. `left-for-later` is retired: a register breach left standing in the floor is a defect, not a deferral. A permissive segment with an empty list is a segment you re-read before trusting.

## Output — the four files

Fill the stubs the script wrote; do not restructure them. The shape, the frontmatter schema, the six cut reasons, the thirteen ledger sections, the marker grammar, and what you never write are all in **`references/slate-contract.md`** — read it once per session. Then:

```
python scripts/slate_scaffold.py check "<chapter>/slate/YYYY-MM-DD-NN"
```

`check` fails on a missing file or a frontmatter that does not parse, warns on a missing ledger section or an unlisted segment, and counts the open `<<…>>` markers. Zero markers is "gate clearable", not "gate cleared".

Every slate folder is **immutable** once written. Anything that changes afterward — a gate ruling applied, an optioned carrier restored, **CRE's own author-gap words** — goes into a new derived run:

```
python scripts/slate_scaffold.py derive --chapter "<chapter>" --parent NN
python scripts/slate_scaffold.py check "<new run>" --against NN     # after the edits: N differing / M identical
```

Derived runs carry all four files (the parent's cut-log and leaves-left come along). Never edit a written run, never hand-type frontmatter (DIR-004), never write `draft.md`, `open-loops.md`, `continuity.md`, `notes.md`, anything in `revisions/`, or `clean-ledger.md` (that lives at the chapter root — see the contract § 6).

## Spine-review gate (after the slate, before any expansion)

The floor is a diagnostic surface: cold and condensed, it shows developmental seams at their cheapest read-length. Present to CRE in one screen:

1. The floor draft, the floor ledger, the heat bank, and the **developmental-seam flags** under `## Developmental-seam flags` — a missing causal link, an unplanted payoff, a beat with no function, a step the scene skips. Observations on the floor, never proposed fixes (the organic-process guard). Research each against the brief and canon first (DIR-011): a seam the tree answers is presented as *resolved against X — confirm*, not as an open flag.
2. The **scene map** (`## Scene map`), built from the floor alone and never graded against the runway (DIR-017 — divergence from the plan is a win): per scene, what happens / derived goal / where it turns; per exchange, an [SP] function tag (*attack · defend · deflect · reinforce · reveal*), functionless or beat-repeating exchanges flagged as observations; a **function-level beat census** — every beat or exchange whose function recurs 3+ times, **dialogue included**, distribution attached, count never verdict. String-level census misses paraphrase; CH12's readiness triple shared no surface string across its three instances.
3. CRE rules — re-dictate, restructure, accept. Nothing downstream runs on an ungated floor.

Unattended (DIR-012): produce the slate and the flags, defer the gate — never self-clear it. Under **clean mode** (`WORKFLOWS/clean-mode`, explicit CRE trigger or a CRE-triggered `chapter-clean` run, never scheduled): tree-answered seams become `resolved-confirm` ledger rows instead of gate stops; genuine seams, every `optioned`, and every garble stay CRE's unconditionally. Clean-mode bin events append to `<chapter>/clean-ledger.md`.

## Stop conditions

- Sentinel fails → halt; ask which folder is the vault.
- No envelope and standalone mode cannot derive one from ruled canon → halt; offer `dictation-cleanup` as the fall-through.
- Folder lacks the per-chapter convention → halt; do not fabricate the structure.
- Cluster meaning genuinely unrecoverable → `## Garbles` note "unrecoverable, author judgment needed"; continue past it.
- `check` exits 1 on the run you just wrote → fix the run before presenting the gate. A slate that fails its own contract is not shipped.

## Logging

Complete the two stubs the script printed: the vault `_CHANGELOG.md` entry (top-insert, file tools, verify by re-read — DIR-005) and the chapter's own `changelog.md` entry (its header format). Fill the counts from the ledger; state the gate state; point at the ledger sections CRE must rule. If the vault has no `_CHANGELOG.md` (the skill is portable), skip the vault entry silently.

## Files this skill ships

- `scripts/slate_scaffold.py` — `new` · `derive` · `check` · `--selftest`. stdlib only; UTF-8 console; exit 0/1/2.
- `references/slate-contract.md` — the slate contract, single statement (ruled 2026-09-02).

## Build status

- **v6.1 source — rewritten 2026-09-02** from the v5.1 source against `WORKFLOWS/transcoder.md` v6.1 + its 2026-09-02 amendment, folding the four skill-review rulings and the CH12 harvest (`SYSTEM/reports/2026-09-02-skill-review-dictation-transcoder.md`, `…-skill-harvest-…`). Script selftest green on the desktop; `check` run against CH15-01 and CH12-04 reproduces the review's findings exactly (schema drift; 2/4 files; a hand-typed frontmatter that does not parse).
- Regression guard in `WORKFLOWS/evals/regression-suite/run_suite.py` (`DT-*`).
- Propagation = desktop `pack-skills.ps1` → sha-verify → Save-skill (DIR-009). Until then the installed copy is v5.1 and announces the gap.
