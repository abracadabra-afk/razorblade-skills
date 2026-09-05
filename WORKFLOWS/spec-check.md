---
type: workflow
name: spec-check
trigger: run the spec-check battery
aliases: [spec check this chapter, run the battery, spec-check battery]
inputs: [a chapter's newest slate clean-draft.md]
outputs: [five pass results + a reconciled verdicts.md in spec-check/<slate-run>/]
lane: fiction
status: active
last_updated: 2026-09-04
scope: Witchwood (and any per-chapter-folder project with a project register). Selective QA gate — run on chapters that matter, not every slate.
pipeline_position: diagnostic tier between [[WORKFLOWS/transcoder]] (slate) and [[WORKFLOWS/register-pass]] (execution). Pass 1 runs in a clean room via the `blind-read` skill; Passes 2–5 are spec-aware pasteable prompts.
---

# WORKFLOW: Witchwood Spec-Check Prompt Battery

> Five narrow diagnostic passes, each one operation deep. The battery **diagnoses and sorts**; it never rewrites. Every pass hands **you** two bins — mechanical failures (objectively broken, fix supplied) and judgment calls (defensible either way, trade shown, no verdict) — and you are the grader. The reconciled rulings become `verdicts.md`, which [[WORKFLOWS/register-pass]] then executes as settled input.

## Where this sits

```
transcoder (slate, generative)
  → Pass 1 BLIND READ (blind-read skill, clean room)
  → DEVELOPMENTAL PASS (blind-response skill — triage w/ CRE, revise → draft.md)   [optional]
  → Passes 2–5 (spec-aware) on the working text → CRE rules → verdicts.md
  → register-pass (execute settled verdicts + build UNDRAMATIZED + rewrite)
```

**The working text.** After Pass 1, the developmental pass (`blind-response`) may revise the chapter from the blind read into `draft.md`. From that point on, **every downstream stage reads `draft.md`** when its `status` marks real content (`dev-revised`), and falls back to the newest slate `clean-draft.md` when it doesn't. So Passes 2–5 and the register run on the developmentally-revised text when there is one, and on the raw slate when the developmental pass was skipped. The slate stays immutable either way.

This is the diagnostic tier the register's closing clause was written for: *"If this reviser runs downstream of a separate diagnostic pass that has already ruled on flagged candidates, do not re-litigate those rulings — take the human's verdicts as settled input."* The battery is **optional** and **selective**: when `verdicts.md` exists for a slate run, `register-pass` runs execute-only; when it doesn't, `register-pass` runs full discover-and-revise. Use the battery on chapters worth the cost (five fresh contexts + your grading), not on every slate.

### Scope by chapter weight
"Chapters worth the cost" is set, not guessed, by the chapter's **weight** (see [[WORKFLOWS/chapter-weight]] — read `brief.md` `weight:`, else `_status.md`, else default `standard`):

- **`load-bearing`** → run the **full battery**: blind-read → (developmental pass as needed) → all four spec-passes → reconcile.
- **`standard`** *(default)* → the ordinary selective battery (the running order below).
- **`bridge`** → run **lean**: Pass 2 (CARRIES vs ASSERTS) only, or skip the battery entirely and go straight to `register-pass`. Blind-read optional.

Depth scales; the quality bar does not — every weight still gets the register downstream. If a `bridge` chapter trips heavy flags on the one pass it gets, stop and recommend re-weighting it rather than waving it through.

## Inputs

- The chapter's **newest slate `clean-draft.md`** (or a slate run you name). This is the chapter text every pass reads.

## Outputs — one folder per slate run, written to `spec-check/`

Keyed to the slate run it diagnosed, kept **out** of the immutable `slate/` tree:

```
<chapter>/spec-check/<slate-run-id>/      e.g. spec-check/2026-06-03-01/
├── pass-1-blind.md        (written by the `blind-read` clean-room skill)
├── pass-2-carries.md
├── pass-3-descriptor.md
├── pass-4-dialogue.md
├── pass-5-theme.md
└── verdicts.md            YOUR reconciled rulings — the file register-pass consumes
```

`<slate-run-id>` is the slate folder name (e.g. `2026-06-03-01`), so a verdict sheet is always traceable to the exact draft it judged.

**No slate leg? Mint a dated run id (added 2026-08-24).** On the episode route — and any folder whose `slate/` is N/A-stubbed — there is no slate folder to key against, and the target text is `draft.md`. Use `YYYY-MM-DD-NN` (today's date, `NN` from `01`) as the run id, record `slate_run: none — no slate leg`, and name the real file in `source:`. **Never invent a slate path that does not exist.** Where the pass supersedes draft text, snapshot the pre-pass body into the run folder first — on a no-slate project `draft.md` is both source and target, so nothing else preserves the audit trail the `slate/` tree normally provides.

---

## Running order and rules

1. **Run Pass 1 (Blind) FIRST, on a clean context, before any other pass touches the chapter.** Do not paste the spec, the cheat sheet, the chapter's `brief.md`, `REFERENCE/threads.md`, or any other prompt into that context — the brief and the threads ledger are spec material and contaminate a blind read exactly like the register does. Once a context has seen a spec-aware pass, its blind reading is contaminated forever — so Pass 1 gets its own fresh thread. In this vault, **use the `blind-read` skill** ("blind read chapter N"), which deliberately skips the project bootstrap and reads only the chapter prose. Do **not** run Pass 1 inside a normal bootstrapped session — the bootstrap loads `_SKILLS MAP` and the register, which contaminates the blind read.
2. **Developmental pass (optional, between Pass 1 and Passes 2–5).** Run the `blind-response` skill ("respond to the blind read") to fix the reader-experience problems Pass 1 surfaced — drift, a mistimed reveal, underbuilt planting, macro told-not-shown — *before* the line passes look at the text. It is two-phase and gated: it proposes a triage (problem vs. working-as-intended), **you rule**, it proposes fixes, **you approve**, then it writes the revised chapter to `draft.md`. When the chapter has a `brief.md`, the triage cites it — a finding that contradicts the brief's stated intent is presumptively PROBLEM; one the brief planned (a deliberate seal, intended foreshadowing) is presumptively INTENDED; the brief informs the proposal, the ruling stays yours. Skip it only if the blind read was clean. Run it because line-editing text you're about to restructure is wasted work — fix structure first, then audit stable text.
3. **Passes 2–5 are spec-aware.** Run them after the developmental pass (or after Pass 1 if you skipped it), **on the working text** (`draft.md` if `status: dev-revised`, else the slate `clean-draft.md`). Two ways to run them:
   - **One command (recommended):** the `spec-passes` skill ("run the line passes") fans the four passes out to **one isolated subagent each** — every pass gets a fresh context with only its prompt + the working text, so they stay isolated (no blending, honest examined-counts) while you issue a single command. It reads the four prompts below as its source of truth, writes the four `pass-N-*.md` files, and assembles a `verdicts.md` **draft** with the judgment calls left blank for you. It excludes Pass 1 and the dev pass by design.
   - **By hand:** paste each prompt below into its own fresh context (or at least its own clean message), one at a time — front-load the interpretive Pass 2, run the mechanical lookups (Passes 3–4) last — and save each result to the matching `pass-N-*.md`. Maximum control; the runner exists to spare you the four manual pastes without losing the isolation.
4. **You are the grader.** Every pass ends by handing you two bins — mechanical failures (fix supplied) and judgment calls (trade shown, no verdict). The judgment-call bin is yours to rule on. Never let a pass decide those for you.
5. **Watch the denominator.** Every pass reports how many sentences/lines it examined, not just how many it flagged. A pass that flags 2 of 6 and one that flags 2 of 40 are telling you different things. If the count looks implausibly low, the pass got lazy — run it again. After the amendments, recurring seams (dog banter, the "good and loyal" epithet, the captions) should resolve inside the passes rather than landing on your desk — so a healthy post-amendment chapter shows fewer flags on a **steady** examined-count. Flags down + count steady = the instrument learned; flags down + count also down = the pass got lazy. Watch the ratio, not the flag total.
6. **Every pass de-duplicates.** If several flags share one underlying cause or turn on one unresolved decision, the pass groups them and names the single decision, rather than listing one recurring move as N independent findings. (Chapter 1's Pass 4 returned seven "judgment calls" that were one decision made seven times — that is the failure this prevents.)

**Supersession triage — before Passes 2–5 read the working text (DIR-019, added 2026-09-04).** The developmental pass revises `draft.md` between Pass 1 and the line passes, so everything Pass 1 and its grading produced is a dated claim about text that has since moved. Check every span-naming ruling the battery carries forward — `pass-1-blind.md`'s quoted lines, the `brief.md` **Grading record** rulings, a Workshop-2 ruling set on the dictation route, and any earlier `verdicts.md` for this chapter — against the working text the passes are about to read: **span present → carry silently; span gone → moot, stamp the row `superseded_by: <working text> (<date>)` in place, one log line, never asked; span reworded but surviving → the only case that surfaces**, one batched block carried into the reconciliation, tree-researched first (DIR-011). A pass never re-flags a span its own developmental revision already fixed, and never re-opens a ruling CRE's later draft discharged (§3 — a hand-landed draft is the newest ruling). This also keeps rule 5's denominator honest: a pass counting a span that no longer exists is measuring the old draft. **Scope lock (§4):** staleness outside this chapter's folder and its direct derives is one line in `SYSTEM/drift-ledger.md`, not a pass finding.

**Chapter 1 note:** Pass 5 (narrator naming theme / confirming a parallel) may find little or nothing, because the keystone legend and its parallels arrive later. Run it anyway — a clean result on a chapter that shouldn't trip it is a calibration check on the prompt itself.

---

## PASS 1 — BLIND READ (Tier 1, run first, no spec)

> Run via the `blind-read` skill. Paste this with the piece's **prose body** and NOTHING else.

> ⚠️ **Strip the frontmatter before you paste (`^obs-269`, added 2026-08-24).** A mature `draft.md` opens with YAML carrying the POV ruling, the register version, a pointer to a numbered premise/brief ruling, cut rationales, and an `open_flags` list naming your **live, unruled craft worries by name**. Paste from the first line of prose — everything below the closing `---`. The dispatcher owns this strip; handing the reader a *path* re-opens the hole, because it must then open the file itself and meets the header on the way to the prose. On EP 02 the reader obeyed every filename prohibition and was contaminated anyway: the header named the two worries that came back as the read's two load-bearing findings, so their independence could not be established. A guard that checks *"did the reader open the spec files?"* without checking *"did the spec reach the reader?"* has passed on a proxy (DIR-018).

You are reading a piece — a novel chapter or a standalone episode — cold, as a first-time reader. Do not edit. Do not guess at the author's intentions or themes. Answer only from what is on the page, and quote a specific line for every answer.

**Cast mapping — do this first, in one line each.** Questions 2, 3 and 5 turn on two figures. Name them **from the text alone**, before answering: the **central figure** (whoever the narration sits with) and the **significant secondary figure** (whoever applies the most pressure to them). If the piece has no such figure, say so plainly rather than forcing a fit. Never infer these from a title, a filename, or a folder name.

1. **Drift.** Mark the first place, if any, where your attention slipped or you started skimming. Quote the line you were on. If you never drifted, say so.
2. **The central figure's deepest fear.** At what point — if any — did you understand what they are most afraid of? Quote the earliest line that gave it to you, and state in one sentence what you think that fear is. If you never formed a clear sense of it, say that plainly.
3. **Narrator vs. character knowledge.** Is there any point where the narration seems to understand the central figure more deeply than they understand themselves — where the narrator's knowledge outruns the character's? Quote the earliest such line and say what the narrator seems to know that they don't.
4. **Prediction.** At the end, what do you expect to happen next? What is the central figure carrying, planning, or hiding that the piece has set up? List what you can infer and quote what planted it.
5. **The secondary figure.** Who are they to you, on this evidence alone? What is their relationship to the central figure — who is taking care of whom?
6. **Earned or asserted.** Name one moment that landed emotionally, and one that felt told-to-you rather than shown. Quote both.

Report only what the text supports. Where it supports nothing, say nothing was there.

> **Role-phrased since 2026-08-24.** Questions 2/3/5 previously read "the mother" and "the boy" — correct for the Witchwood chapter they were written against, wrong everywhere else. On EP 02 (a mother, a daughter, no boy) the hardcoding forced a hand-mapping by the dispatcher, which is itself a channel for the dispatcher's assumptions to reach a supposedly blind reader. Witchwood behavior is unchanged; the pass is now portable.

*Grading (private, against the spec): if the model named the central figure's deepest fear from early narration, or the narrator's knowledge outran theirs anywhere before the intended point, your seal leaked there. If its prediction can't reach what you planted, the planting is underbuilt. **Check the sheet's `contaminated:` stamp before you grade — a `partial` read's findings on any primed question carry no evidentiary weight.***

---

## PASS 2 — CARRIES vs. ASSERTS (Tier 2, interpretive, adversarial)

> The core pass. Folds three issues — ornate verbs for plain actions, narrator gloss, and told-not-shown emotion — into one operation, because they are one principle: meaning should be carried by image, action, and character-interior, not asserted by diction or by the narrator.

You are a prosecuting line-editor for a folk-tale novel written in a deliberately plain register: humble, common words for ordinary actions; strangeness reserved for images, beasts, and the characters' inner worlds. The narrator never names what a moment means — the scene and the characters' interior carry it. Assume violations exist and hunt them; do not reassure.

Examine every sentence. For each, decide whether its meaning is CARRIED (by a concrete image, a physical action, or a character's own thought in their own voice) or ASSERTED (by an ornate word standing in for a plain act, or by the narrator stepping outside the scene to state significance, diagnosis, or how to feel).

For every ASSERTED sentence, run this and show your work:

1. Quote the sentence.
2. Name the assertion type: (a) ornate verb/phrase for a plain action, (b) narrator naming meaning/emotion/theme, or (c) emotion stated rather than shown.
3. Write the rendered version — the plainest counterpart for (a); the line with the gloss deleted for (b); the gesture/action that would show it for (c).
4. Measure the delta: does the original carry meaning the rendered version loses, or only tone/grandeur?
   - Only tone → flag: cuttable.
   - For type (a), also check metaphor accuracy: does the fancy word's buried image match the literal action? If it over-claims (e.g. *unseal* for eyes merely closed a moment), flag even if it sounds good.
   - **The two-part deletion test** (run it for every type-(b) gloss). Delete the line, then check two separate things: (i) does the surrounding scene still stand? and (ii) does the line's specific meaning survive elsewhere in the scene — can you point to the exact image, action, or line that carries it? A scene can survive while its meaning does not. If the meaning is enacted nearby → the gloss only captions it → cuttable. If the scene survives but the meaning lives only in this sentence → the line IS the meaning, not a caption on it → do NOT flag; this is a keeper. (Worked example: "the mountain had spent her entire life in kind" — deleting it leaves the chores intact, but the chores dramatize weariness, not the mountain consuming her; that idea has no other home, so the line stays.)
   - **UNDRAMATIZED is the dangerous verdict, not the rare one.** Before you call any gloss "cuttable," you must actually locate the enactment — quote the image or action that carries the meaning. If you cannot point to it, do not default to cuttable because the line "feels redundant"; classify it UNDRAMATIZED and name what the scene would need to dramatize it. UNDRAMATIZED means the fix is building a scene, not cutting a line — flag it loudly, because it is the failure that quietly hollows a book.

Then sort all flags into two bins:

- **MECHANICAL FAILURES** — objectively breaks the rule (ornate verb that misdescribes the action; narrator naming an emotion no character is feeling; undramatized assertion). Supply the fix.
- **JUDGMENT CALLS** — defensible either way (a lift that adds a faint real shade; a gloss whose scene almost carries it). Show the trade in one line. Do NOT decide these; present the seam and stop.

End with a count: sentences examined, sentences flagged, split by bin. Protect, do not flag: strange imagery, unusual ideas, fragmented syntax, and any character's inner voice — these are intended features. When in doubt whether something is earned ornament or tone-only, classify it as a judgment call, not a mechanical failure. If several flags are the same recurring move (e.g. the narrator captioning what a scene just performed), group them under one heading and name the single habit, rather than listing them as independent findings.

---

## PASS 3 — DESCRIPTOR (Tier 2, mechanical, run alone)

> Near-pure lookup. Cheap, reliable, keep it separate so it doesn't dilute Pass 2.

You are checking a folk-tale novel for two descriptor faults. Examine every adjective and adverb. Assume violations exist.

Before flagging anything, hold this distinction: affectionate close-third coloring and atmospheric folk register are not verdicts. "Greedy" on a slobbering dog, "lonely" on a folk-tale cottage — these are voice, not editorial judgment on significance. The cut-rule targets the narrator's verdict on a thing's meaning or moral weight (brutal, cruel, noble), never warmth, mood, or register-coloring. Folk tales are made of lonely cottages and dark woods; that coloring is the register, not an intrusion.

**(A) Editorial descriptors — CUT without replacement.** Words that supply the narrator's verdict on significance or moral quality rather than an observable fact: brutal, cruel, noble, savage, merciless, gentle (as verdict), and any modifier that tells the reader how to weigh a thing. For each: quote it, and confirm the sentence still stands with it simply removed.

**(B) Wrong-register specificity — SUBSTITUTE.** Words reaching for real physical specificity in language that breaks the plain/folk register: clinical or modern-psychological terms (neutral skin, mutinous fingers, malformed, massaged, migration, anything therapeutic, naturalist, or technical). The descriptor was trying to be specific — so do not just delete it; write one or two in-register replacements that keep the specificity (e.g. *neutral skin* → brown / sallow / sun-cured; *mutinous fingers* → fingers that wouldn't mind him). Prefer a replacement that pre-echoes nearby imagery where one exists (e.g. *malformed legs* → gnarled legs, which rhymes with a following root-simile). For each: quote it, name what specific thing it reached for, supply the replacement(s).

Output three lists: (A) CUTS, (B) SUBSTITUTIONS, and JUDGMENT CALLS — any flagged descriptor that is plausibly affectionate coloring or folk register rather than a verdict on significance. For judgment calls, show the trade in one line (verdict reading vs. voice reading) and do NOT decide; present the seam and stop. If a descriptor is borderline between (A) and JUDGMENT, it goes in JUDGMENT, not (A). End with a count: modifiers examined, flagged in each list. Do not flag earned thematic imagery (chrysalis, knot, cairn) or any descriptor that is observable physical fact rather than judgment. If one descriptor recurs (e.g. a repeated epithet), name it once as a habit rather than listing each instance separately.

---

## PASS 4 — DIALOGUE PUNCTUATION STANCE (Tier 2, mechanical, run alone)

> A classification operation, unrelated to Pass 2. Its own pass.

You are checking dialogue punctuation in a folk-tale novel. The rule tracks the speaker's stance in the moment, not the character, and not the addressee. Quotation marks are always kept. Examine every line of dialogue.

For each line, classify the stance:

- **FLAT** (no ? or !): pronouncement, aphorism, fatalism; a rhetorical question wanting no answer; a line of authority, resignation, or judgment. (e.g. *A dying beast is a dangerous one.*)
- **MARKED** (? or ! retained): a genuine question wanting an answer; a real exclamation of emotion (a child's upset, a mother's alarm); warm address where the mark lets the warmth land.

**Critical rule for the hunter speaking to her hound** (this is most of the chatter and the place this pass most often goes wrong): "warm address keeps the mark" is the PRIMARY test, not a tiebreaker. A companionable question to the dog ("Friends of yours?", "Have you got it, old man?") keeps its mark even though the dog cannot answer — the warmth is the point and the mark is how it lands. Do not flag these as rhetorical-and-therefore-flat. Stance, not addressee, decides: a warm line to the dog stays MARKED; a fatalistic line that happens to be aimed at the dog (e.g. a grim reflection over a kill) goes FLAT. A line that is self-directed (about the speaker, not addressed to the dog at all) is judged on its own stance — resignation goes flat regardless of the question-word.

Flag any line whose punctuation contradicts its stance — a genuine question or warm address written flat, or a pronouncement/resignation carrying a needless mark. For each flag: quote the line, name the stance you read, name the mismatch, supply the corrected punctuation.

Two bins: MECHANICAL (clear stance/mark mismatch) and JUDGMENT CALL (lines that could be read in either stance — show both readings, do not decide). De-duplicate: if multiple lines turn on a single unresolved decision (e.g. how to punctuate all warm dog-address), do NOT list them as separate judgment calls — name the one decision and list the lines it governs underneath it. End with a count: dialogue lines examined, flagged by bin.

---

## PASS 5 — NARRATOR NAMING THEME / CONFIRMING PARALLEL (Tier 2, run alone, adversarial)

> High-stakes single check. The narrator must never state the book's themes or confirm a thematic parallel that should land in the reader or in a character's mouth — recognition lives in the silence after a character speaks, never in narration.

You are prosecuting a folk-tale novel for one fault: the narrator stating a theme, or confirming a thematic parallel, that should be left for the reader to derive or for a character to speak. The book's method is that meaning arrives through action, image, and character speech; the narrator never closes the loop by naming it. Assume violations exist.

Examine the narration (not dialogue). Flag any sentence where the narrator:

- names what the story or a scene means;
- confirms a parallel or symbolic equivalence (X is Y, in the narrator's voice);
- delivers a thesis-statement or moral coda;
- tells the reader the significance of an image instead of letting the image carry it.

For each: quote it; state the theme/parallel it names; run the two-part deletion test. Delete the line, then check two separate things: (i) does the surrounding scene still stand? and (ii) does the line's specific meaning survive elsewhere — can you quote the exact image, action, or character line that carries it? If the meaning is enacted nearby → the line only labels it → flag cuttable. If the scene survives but the meaning lives only in this sentence → the line IS the meaning, not a gloss on it → do NOT flag; it is a keeper (a chiastic epigram whose idea has no other home is the classic example — keep it). If you cannot locate the enactment at all → do not default to cuttable; flag UNDRAMATIZED and name what the scene would need to carry it. UNDRAMATIZED is the dangerous verdict — the fix is building, not cutting — so flag it loudly rather than letting it hide as a "redundant" cut.

**Special handling — load-bearing utterances.** Some potent phrases are legitimate in a character's mouth and forbidden in the narrator's. If you find such a phrase, report which voice it currently sits in. Flag it only where it sits in the narrator's voice; note where it is correctly in a character's mouth. Also distinguish a narrator line that completes a folk cadence (maxim-and-confirmation, tale-voice rhythm) from one that diagnoses — the former can be legitimate even when terse; treat it as a judgment call, not a mechanical failure.

Two bins: MECHANICAL (narrator clearly naming theme/parallel) and JUDGMENT CALL (a line that hovers between rendering and gloss — show the trade, do not decide). De-duplicate recurring moves into a single named habit. Before flagging, also audit the lines where the method works (image carrying a parallel unnamed) and frame the flags as deviations from that discipline. End with a count: narration sentences examined, flagged by bin.

---

## The verdict sheet — `spec-check/<slate-run>/verdicts.md`

After the passes, **you reconcile** into `verdicts.md`. This is the only file `register-pass` reads back; the five `pass-*.md` files stay as the audit trail. Structure it so the register can execute it without re-deciding anything:

```markdown
---
slate_run: <slate-run-id>           # e.g. 2026-06-03-01
source_slate: slate/<run>/clean-draft.md
reconciled: YYYY-MM-DD
status: ready            # ready = register-pass may execute; draft = still grading
---

## MECHANICAL — apply as given
(objectively broken; fix supplied by the pass; register applies verbatim)
- [pass 3] "neutral skin" → "sun-cured" — wrong-register specificity
- [pass 2] "<line>" → "<plain counterpart>" — ornate verb misdescribes action
...

## RULED JUDGMENT CALLS — your verdicts (settled; do not re-litigate)
(every judgment call any pass surfaced, with YOUR ruling: KEEP / CUT / REWRITE-as)
- [pass 2] "<line>" — RULED: KEEP (the line is the meaning's only home)
- [pass 4] warm dog-address punctuation — RULED: all MARKED
...

## UNDRAMATIZED — build, don't cut
(the dangerous verdict; you hand-check the FIRST one personally)
- [pass 5] "<glossed theme line>" — build: <what the scene must show to carry it>
...

## NOTES TO THE REGISTER
- Anything the register should know running execute-only (e.g. "blind read says the
  central figure's fear leaked at line X — tighten the interior there").
```

`register-pass` keys off `slate_run`/`status: ready`: when it finds a ready sheet for the slate it's about to revise, it runs the register **execute-only** (applies MECHANICAL, honors RULED calls, builds UNDRAMATIZED, never re-opens settled rulings).

---

## After the passes — your reconciliation

Run the **`reconcile` skill** ("reconcile the findings") to do this with help: it loads the `verdicts.md` draft + the four pass files, batch-confirms the mechanical fixes (you veto any), then walks the judgment calls **one at a time** — each with its trade and which passes raised it — recording your ruling and refusing to finalize until every call is ruled. It enforces the first-UNDRAMATIZED hand-check and the denominator sanity check below, and writes `verdicts.md` to `status: ready`. It never rules for you and never builds prose; when the sheet is ready you run `register-pass`. (You can also reconcile by hand by editing `verdicts.md` directly — the skill just structures the same work.)

**Supersession triage — at ruling time, not authoring time (DIR-019, added 2026-09-04).** A verdict sheet is a dated claim about a draft, and drafts move between the passes writing the sheet and you ruling it. Before the sheet is presented, re-check every row that quotes a span — MECHANICAL fixes, RULED JUDGMENT CALLS carried from an earlier sheet, UNDRAMATIZED items, NOTES TO THE REGISTER — against the current working text: **span present → carry silently; span gone → moot, stamp the row `superseded_by: <working text> (<date>)` in place, one log line, never put to CRE; span reworded but surviving → the only case that surfaces**, batched into one block at the head of the walk, tree-researched first (DIR-011). Carry a dated `cleared_against:` stamp on the sheet; a sheet older than ~48h re-clears before presentation, and the MECHANICAL bin gets the same clearance as the rest — a stale sheet produces mechanical-*looking* rows, which is exactly the class that gets batch-ratified without close reading (DIR-014). This does **not** loosen `## RULED JUDGMENT CALLS — your verdicts (settled; do not re-litigate)`; it pushes the same way. That rule forbids re-opening a settled *ruling*; this one asks only whether the *span* the ruling names still exists. A settled call whose span survives carries untouched, one whose span is gone is retired by stamp rather than re-litigated, and only the reworded case reaches you — once. **Scope lock (§4):** staleness outside this chapter's folder and its direct derives is one line in `SYSTEM/drift-ledger.md`, not a verdict row.

The passes hand you sorted candidates, not verdicts. Four things only you can do:

- **Rule on every judgment call.** The "is this lift worth the faint seam" decisions are yours. Record each in `verdicts.md`.
- **Apply the override the passes can't.** Cut a gloss when its meaning is enacted elsewhere; keep it when the line is the meaning's only home. The deletion test can mislead — a scene often survives a cut while the idea in the cut line does not (the mountain-chiasmus is the worked example). The passes now check for this, but you make the final call.
- **Hand-check the first UNDRAMATIZED.** That branch stayed silent on Chapter 1 because the chapter was too well-built to contain a hollow scene — so it is still unproven. The first time any pass returns UNDRAMATIZED on a real chapter, check it by hand, hard: it is the only verdict that tells you to build rather than cut, and it catches the failure that actually sinks books.
- **Grade Pass 1 against the spec privately.** The blind read's value is entirely in whether its cold findings match what you intended the chapter to do. The written spec is the chapter's `brief.md` (when one exists): check the Prediction section against "Setups to plant," and check every answer against the seal schedule — anything from "must NOT yet learn" that the blind reader named is a leak. Record the comparison in the brief's **Grading record** section so blind-response triage cites a ruling, not a memory. The model never sees that comparison; you make it. Where the blind read and a spec-aware pass disagree on extent (Ch. 1: the lies-cluster), treat the disagreement as a signal that your interior voice isn't marked clearly enough to read as interior — not as a tie to break.
- **Watch the denominators across passes.** If one chapter trips far more or far fewer flags than its neighbors on the same pass, that's a signal about the chapter, or about the pass drifting under volume. Re-run anything whose count looks wrong before trusting its silence. Remember the post-amendment ratio: fewer flags on a steady examined-count means the instrument learned; fewer flags on a dropping count means it got lazy.

## Stop conditions

- No slate `clean-draft.md` for the chapter → nothing to diagnose; run the Transcoder first.
- Pass 1 about to run in a spec-aware context → stop; run it via the `blind-read` skill instead.
- A pass returns a flag count implausibly low for the chapter → re-run it before trusting the silence.

## Logging

On completion append an entry to [[_CHANGELOG]] (fiction lane) noting which slate run was graded and the bin counts; file any new fragility to [[_OBSERVATIONS]].

---

## Dictation route (chapter-pipeline) deltas

This battery was written for the **slate route** and still runs it unchanged. When invoked by [[WORKFLOWS/chapter-pipeline]] (the **dictation route**), four things change; the five pass prompts, the verdict sheet, and `reconcile` are identical.

1. **Working text = the cleaned `draft.md`.** There is no slate on the dictation route — the chapter is dictated, run through `dictation-cleanup`, then developmentally revised. Every pass reads `draft.md`, and the `spec-check/<run-id>/` folder is keyed to a date/run tag instead of a slate-run id. The "no slate `clean-draft`" stop condition does not apply; the gate is "no cleaned `draft.md`." Passes 2–5 still run on the **structurally-settled** draft (after the developmental + loop revisions are promoted — chapter-pipeline Phase 4), then feed `register-pass` execute-only.

2. **Pass 1 runs as a subagent, and its triage moves to Workshop-2.** `blind-read` is invoked as an isolated clean-room **subagent** whose `pass-1-blind.md` is handed to [[WORKFLOWS/workshop-chapter]] **Workshop-2**, which reconciles the cold read against the warm project-fluent read and captures CRE's PROBLEM / WORKING-AS-INTENDED rulings (the brief still informs the call). So the developmental **triage** (running-order step 2) is performed in Workshop-2, not by `blind-response`. `blind-read`'s own logic is unchanged — only its invocation (subagent) and the destination of its findings.

3. **`blind-response` runs execute-only.** Because Workshop-2 already produced the ruled triage, `blind-response` **skips its own phase-1 triage** and executes the ruled structural fixes into `draft.md` (`status: dev-revised`) — the same use-if-present coupling `register-pass` has to a ready `verdicts.md`. Standalone "respond to the blind read" still runs the full two-phase triage; **execute-only fires only when a Workshop-2 ruling set is present.**

4. **No weight-scoping.** Every chapter is load-bearing (CRE-ruled 2026-06-18), so the full battery runs on every chapter; the [[WORKFLOWS/chapter-weight]] lean/bridge branch ("Scope by chapter weight") is not applied on this route.

> **Build note (desktop-gated):** these deltas are specified here (canonical) and in [[WORKFLOWS/workshop-chapter]]. Propagating them to the running skills requires editing `skills-src/blind-response/SKILL.md` (add the execute-only mode **and** repair the `^obs-094` truncation — append the missing `).` to its `## Security` tail) and `skills-src/blind-read/SKILL.md` (note the subagent invocation), then `pack-skills.ps1` rebuild + Save-skill reinstall. Tracked at `^backlog-chapter-pipeline-build`.

---

_Canonical reference for the Witchwood spec-check battery. Pass 1 is delivered as the `blind-read` Cowork skill; Passes 2–5 are pasteable prompts run in fresh contexts. Procedure changes land here first, then propagate to the skills via skill-creator._
