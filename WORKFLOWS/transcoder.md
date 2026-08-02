---
type: workflow
name: transcoder
trigger: slate this dictation
aliases: [transcode this, run the slate, transcoder v5, slate it]
inputs: [raw dictation text from speech-to-text, perceptual envelope (POV + conditions + state), the floor register canon at KNOWLEDGE/PROSE FRAMEWORK/narrator-rules.md, the contamination checklist at REFERENCE/contamination-checklist.md (optional)]
outputs: [floor-draft prose (cold register), cut log, synthesis ledger (incl. floor ledger + heat bank), leaves-left audit]
lane: fiction
status: active
last_updated: 2026-08-01
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). First adopter — Witchwood. v5.1 adds standalone/episode mode (envelope derivable from ruled canon with provenance) — first adopter WRITING/SHORTS/EPISODES.
pipeline_position: upstream of [[WORKFLOWS/prose-expansion]] (via the spine-review gate) and [[WORKFLOWS/dictation-cleanup]]
---

# WORKFLOW: Dictation Transcoder (v6)

> Generative pass that converts raw dictation into a clean rough-draft slate. **Rewrite-allowed.** Pairs with [[WORKFLOWS/dictation-cleanup]] downstream, which is the protective copy-edit pass the v5 spec refers to as the "separate, protective pass… later."

## v6 changelog (2026-08-01 — the cold-floor recalibration, CRE-ratified)

Source: `SYSTEM/reports/2026-08-01-transcoder-v6-proposal.md` (all five rulings taken at recommended defaults). The problem fixed: register breaches native to dictation (hedges, editorial descriptors, filters, glossing) passed the perceptual cut, survived synthesis, and were verdicted `left-for-later` — riding the slate into revision and making register-pass the heavy repair stage. v6 normalizes register at the one stage already licensed to rewrite. **Repack + Save-skill pending (DIR-009); pilot on next fresh Witchwood dictation before repack.**

1. **Operation 3 — Normalize to floor.** New third operation after Cut and Synthesize: enforce the [[KNOWLEDGE/PROSE FRAMEWORK/narrator-rules]] deny-lists over the whole draft. Every normalization lands in the **floor ledger**.
2. **`left-for-later` retired for register breaches.** A named load-bearing emotion or narrator editorial in the floor is a defect, not a deferral (see amended verdict set below).
3. **Heat bank.** Dictated warm/hot language stripped by floor normalization is banked per beat, verbatim, in the synthesis ledger. Expansion step 7 re-selects from CRE's own words; the machine flags gaps, never invents heat.
4. **Spine-review gate.** The floor draft + ledgers + developmental-seam flags are presented to CRE before any expansion pass runs (see section below).
5. **Narrator baseline: rules-within-ruled-POV.** The floor honors each project's ruled POV (Witchwood: close third); the deny-lists are POV-agnostic and apply within it.
6. **Slate contract unchanged.** Same four files; `clean-draft.md` is now the floor draft; floor ledger + heat bank are sections of the synthesis ledger.

Expansion (framework steps 4–7) lives downstream in [[WORKFLOWS/prose-expansion]] — POV tags and temperature tags are machine passes; sentence restructure and temperature word choice are **CRE's** (ownership CRE-ruled 2026-08-01).

## v5.1 changelog (2026-07-22 — amended off the EP 01 DOOMSCROLLER live test)

Live test: two passes on `WRITING/SHORTS/EPISODES/EP 01 - DOOMSCROLLER` (slate/2026-07-22-01 and -02). Six amendments, all live in `skills-src/dictation-transcoder/SKILL.md` (repack + Save-skill pending, DIR-009):

1. **Standalone/episode mode.** The convention gate halted on a valid target (an episode folder with the envelope fully ruled in runway §A + dec-017). New rule: if the folder's own canon rules the envelope facts, derive `envelope.md` with per-segment provenance + `status: derived — author confirms`, create `slate/`, proceed (attended only). DIR-011 applied to a gate: a halt the tree can answer is noise. Never fabricate unruled envelope facts.
2. **`frame` cut reason + summary-mode conversion.** The v5 reason set (unperceived/too-fine/narrator-injection/modifier) named almost nothing that actually needed cutting on real dictation — the artifacts were frame-talk ("the story opens with," "In this video," "The End"), which had no reason code. Added `frame` + the rule: summary-mode dictation renders as scene, not report. Exception: author shorthand that works as free indirect ("same cycle") stays as the carrier.
3. **Tense normalization, declared.** Dictation drifts tense; v5 was silent. Detect dominant tense; conform to a project ruling if one exists, else normalize to dominant and surface the choice as an open ledger question. Never re-tense a ruled line; leave the seam visible.
4. **Ruled-line guard (DIR-014).** Sweep folder canon for author-ruled verbatim lines before synthesis; carry byte-exact; ledger-list under "Ruled lines — preserved"; collisions flag, never fix. (Pass 1 re-tensed a ruled blind-read line — caught in evaluation; the guard exists so it can't recur.)
5. **Two-lane garble policy.** Mechanical single-reading STT errors (`unkept`→`unkempt`) fix silently, reason `mechanical`; meaning-splitting garbles (`layer`/`lair`) keep the dictated form and ask. A rescue may ask a question; it may never make a decision.
6. **Intentional-repetition exception** to the shortest-form challenge: a repeated structure that carries escalation/ritual/ear-order (the swipe-refusal loop) is payload — compress within each repeat, never across the run. Load-bearing for audio-first shorts.
7. **Capture-then-tag inversions (added same day, from CRE's own account of his mic process).** Forward-only dictation invents content first and labels it after — *"Everything is terrible, the next title"* ("I see it in real time, I capture and tag"). A trailing appositive naming the just-spoken span is a tag, not narration: never cut as frame, never read as garble; fold into reading order or keep the inversion where it carries rhythm; reattach a drift-separated tag to its content before flagging anything as garbled. First suspect on any garbled span containing a naming word (title/caption/called/tagged) — the EP 01 "It's titled, still, avoiding…" span was exactly this.

## When to use

When CRE provides raw dictation for a chapter that is using the per-chapter folder convention (envelope.md present). Trigger phrases: "slate this dictation," "transcode this," "run the slate." Do NOT trigger this on a project that hasn't adopted the folder structure — fall back to [[WORKFLOWS/dictation-cleanup]] in that case.

**Banked prose does not come through the mic (`^obs-221`, CRE-nominated 2026-07-26).** Dictation is a forward-only generative motion for producing *new* material. Prose CRE has already written (e.g. the ~30 banked/ingested Witchwood chapters) must be routed through the **revision pipeline** — not re-dictated from or hand-edited at the mic. Re-dictating existing material invites editing-during-dictation, which CRE has ruled a mistake that runs *lengthier* than just hand-editing the work directly. If the input is dictation *against* already-written prose rather than fresh generation, that is not a slate job. **Two sanctioned revision routes for existing prose (v6, 2026-08-01):** (a) `register-pass` against the project register, the standing route; (b) the **floor sheet** — this workflow's Operation 3 run *diagnostically* over the existing draft, gated per-item — via [[WORKFLOWS/prose-expansion]] **Entry mode B** ("floor the draft"), when the goal is conformance to the cold floor. Neither ever comes back through the mic.

## Inputs

- Raw dictation text.
- **The perceptual envelope.** Pulled from the chapter's `envelope.md`. States: who is perceiving (POV), in what conditions (place, weather, light, time), in what state (what they're doing/carrying/suffering — what consumes their attention). **If missing, stop and ask before doing anything else.**

## Outputs (four files per run, immutable)

| Section            | Destination                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------------|
| Clean draft        | `<chapter>/slate/YYYY-MM-DD-NN/clean-draft.md`                                                       |
| Cut log            | `<chapter>/slate/YYYY-MM-DD-NN/cut-log.md`                                                           |
| Synthesis ledger   | `<chapter>/slate/YYYY-MM-DD-NN/synthesis-ledger.md`                                                  |
| Leaves left        | `<chapter>/slate/YYYY-MM-DD-NN/leaves-left.md`                                                       |

Ambiguous register-repair calls and image-doubling questions go to `<chapter>/open-loops.md`. Anything synthesis dropped that a later section will need goes to `<chapter>/continuity.md`. Accepted clean-draft text gets stitched into `<chapter>/draft.md`.

---

## What this pass is doing

You are converting raw dictation into a clean first draft of close third-person prose. This is **pre-prose becoming a draft**, not a draft becoming polished. You are **generative**: you may rewrite, fuse, and regenerate clean sentences. You are not protecting the author's wording — the author was talking, not writing, and expects to receive prose, not their transcript marked up.

You perform exactly three operations, in this order: **Cut**, then **Synthesize**, then **Normalize to floor**. Nothing else. You do not assess quality beyond the floor register rules, and you do not polish. The protective pass ([[WORKFLOWS/dictation-cleanup]]) does that later. Your only job is to hand back a registrally and directionally correct **floor draft** — cold observational narration per [[KNOWLEDGE/PROSE FRAMEWORK/narrator-rules]], the substrate the expansion passes build on.

## Maturity is fixed — do not classify it

Everything submitted to you is rough by definition. This tool is used only during the rough-draft phase; once material crosses into revision (`<chapter>/revisions/`), it leaves this workflow entirely and never returns here. Therefore:

- Treat the entire input as rough. Never decide a span is "finished" and skip it.
- Never infer draftedness from surface signals. Clean punctuation, complete sentences, and quotation marks do not mean a span is done — dictation arrives mechanically cleaned, so these signals are meaningless as maturity cues.
- The only thing that survives untouched is a line that passes the checks below, not a line that looks polished.

The one segmentation you do perform is by **perceptual envelope** (below). Maturity is not recoverable from the text, so you never guess it.

## Whole scenes and chapters: segment by envelope

A long passage usually crosses more than one perceptual envelope — e.g. an exterior storm-trek (cold, dark, wind, attention on staying upright) gives way to a hut interior (firelit, warm, still, attention on a second person):

1. Read the whole passage and mark where the perceptual world changes — light, temperature, location, who the character is attending to.
2. Propose envelope boundaries and the envelope for each segment, and state them before transcoding. The author confirms or corrects them once.
3. Run Cut against the **local** envelope for each segment. A detail unperceivable in the storm may be perfectly perceivable by firelight; the test is always "could she register this **here**," not "anywhere in the scene."

Do not segment by maturity — only by envelope. Every segment is equally rough.

---

## Operation 1 — Cut to the perceptual envelope

Run one test on every span, down to the modifier level: **would this character perceive or register this detail, here, in this exact moment?**

Cut anything that fails:

- Narrator-injected information the character cannot see or would not think about.
- Detail too fine for the conditions or their state (e.g. black ice glinting during a night blizzard while struggling).
- Modifiers that smuggle in unperceivable precision even when the noun is fine.

Keep anything inside the envelope, including coarse, violent, or immediate sensation — the filter removes fineness the moment can't support, not intensity.

This operation is objective and recoverable. Apply the test and report what fell.

## Operation 2 — Synthesize the survivors

Work on what remains after the cut. Find clusters — runs of adjacent spans serving one communicative function. For each cluster:

1. **Extract the payload.** What is this trying to tell the reader? State it in one plain phrase ("movement is brutally obstructed"; "the boy is fragile but still alive.").
2. **Draft a carrier** — one image or sentence delivering that payload. You may invent language.
3. **Challenge it against its shortest viable form.** Can this payload survive one fewer beat? If two clauses do the same job, it has not been compressed — it has been thinned. Cut to the single sharpest instance and keep cutting until removing one more beat would lose payload. Default suspicion: a multi-clause carrier is one clause too long until proven otherwise.

**Governing value, in order:** payload-fidelity first, economy second, concrete/visual language third. Concreteness is a preference, not a law — if an abstract gauge ("a hundred times harder") carries the payload more economically than a literal image, take it.

### Two checks inside any line you keep or write

- **Redundant modifier.** A modifier whose work its own noun already does ("fire-kissed ember" — ember carries fire; "rotted boughs" mid-struggle) is freight. Cut it even inside an otherwise-clean image.
- **Verb against payload.** If the payload is "still alive," a slack verb ("the boy hung against her") contradicts it; pick a verb that carries the life ("pressed," "burned," "shivered"). The verb is the most load-bearing word.

### Image-level redundancy (across lines)

Also catch an image carried twice in close range across separate lines you'd otherwise both keep — e.g. "hot as an ember" and "dead things cooled" two clauses later are the same temperature image twice. **Do not keep both and note that they rhyme.** Identify the stronger instance, and surface the other for the author to drop: "ember and dead-things-cooling are one image twice; keep which?" → into `open-loops.md`.

Leave a span untouched if it already stands alone as a clean, single-payload sentence and survives both checks. Synthesis is for collapsing redundancy, not for rewriting non-redundant lines — but a kept line still loses its dead modifiers.

**Do not look ahead for dependencies.** Work cluster-local. If synthesis drops an entity a later line needed, that is acceptable — log to `continuity.md` so the author can re-dictate. Do not preserve clutter to protect a back-reference.

---

## Operation 3 — Normalize to floor (v6)

Run the [[KNOWLEDGE/PROSE FRAMEWORK/narrator-rules]] deny-lists over the full draft — every kept line and every invented carrier. This is deny-list enforcement, near-deterministic; it adds no new generative license beyond replacing the flagged span with its floored form.

**The deny-lists, in priority order:**

1. **Seam-breaks** — narrator hedges ("seemed to," "as if," "she must have imagined") and alarm-labels ("horrifying," "grotesque," "monstrous"). Highest priority.
2. **Filter verbs** — saw/heard/felt/noticed/watched/realized/thought/wondered + "she knew that / he decided that" frames. Cut the verb, land the object. Exception: keep when the perceiving *is* the event.
3. **Editorial descriptors** — narrator-stance modifiers (*brutal* white, *cruel* winter, *noble* gaze). **Adverb Law refinement (2026-08-01):** manner adverbs are cut by the **camera test**, not wholesale — feeling-adverbs ("angrily") floor automatically; physical-fact adverbs ("dryly") are compressed sensing and SURVIVE; agency-implying line-sitters ("carefully," "weakly") flag as judgment calls, never auto-cut. Full law in the narrator-rules doc.
4. **Narrator glossing** — naming what a moment means, clinical/therapeutic diagnosis, telling the reader how to feel, interiority that reinstates what the page already shows.
5. **Non-functional setting** — setting admitted only at the moment of action or use.

**POV baseline (CRE-ruled 2026-08-01): rules-within-ruled-POV.** The floor honors the project's ruled POV — Witchwood floors in close third. The deny-lists are POV-agnostic and apply within whatever camera the project has ruled. Never re-rig a project's camera.

**Floor ledger.** Every normalization is logged in the synthesis ledger: original span → floored span → rule cited. Nothing is silently lost.

**Heat bank.** When floor normalization strips dictated warm/hot language (an editorializing verb, a hot descriptor, a named-feeling line that carried real charge), bank the original **verbatim, per beat**, in a `## Heat bank` section of the synthesis ledger. This is CRE's raw material for expansion step 7 — his heat survives; only its placement in the floor is deferred. The machine never discards banked heat and never invents replacement heat.

**Cold hand, warm wound.** Floor normalization strips the narrator's *labels*, never the image's charge. Statement imagery stays hot; only naming and interpretation are withheld. Do not flatten affect — a floored line that lost its image has been over-cut; restore the image, cut only the label.

---

## Register invariants (apply during generation, not as a separate pass)

> v6 note: these invariants apply *while inventing carriers* in Operation 2; Operation 3 then enforces the full Narrator Rules over everything. They overlap by design — cheaper to generate clean than to repair after.

- **Never name the load-bearing emotion.** Render fear, grief, love, hope structurally — through the body, the action, the object — never by stating the feeling.
  - **Register-repair resolves to options, not output, when direction is ambiguous.** If the original could plausibly point in more than one direction, give both carriers, name the reading behind each, and let the author choose via `open-loops.md`. Committing to a direction you've flagged as uncertain is the exact failure to avoid. Only resolve it yourself when the surrounding action makes the direction unambiguous.
- **Keep every metaphor inside the world the character cannot leave:** its animals, weather, plants, labor, bodies. No technology, modern idiom, clinical or literacy terms — nothing they could not have touched.
- **Prefer direct sensory language over abstraction**, subject to the economy ranking above.
- **Don't contaminate the carriers you invent.** Drafting a carrier (Operation 2) is the moment AI reaches for "good writing." When you invent language, do not elevate the vocabulary, soften blunt/crude words into euphemism, beautify ugliness, add internal gestures ("he swallowed," "her chest tightened"), or close on a clever/meaning line. This is not a separate quality pass — it's the rule that you hand back *CRE's scene in clean prose*, not a literary improvement of it. If `<project>/REFERENCE/contamination-checklist.md` exists, scan your invented carriers (especially register-repair lines) against its patterns and note any you caught and removed in the synthesis ledger. Checklist absent → apply the rule from memory; it's the same enemy either way.

These — plus not contaminating the carriers you invent — are the only quality constraints you apply. Everything else is [[WORKFLOWS/dictation-cleanup]]'s job.

## No silent leaves — prove you read the permissive segments

A comfortable envelope (firelit, calm, daylit) produces few perceptual cuts. That is correct — but a segment reporting "no cuts" is the place you are most likely to have relaxed rather than read closely. Guard against it directly.

In every segment, including ones with no perceptual cuts, locate each span that names an emotion or dissolves telling into a descriptive clause. List each one you chose to leave, with a one-word verdict:

- **incidental** — minor color, not load-bearing; naming is harmless.
- **dialogue** — spoken by a character; out of your scope.
- **floored** — normalized in Operation 3 (appears in the floor ledger; heat banked if it carried charge).
- **optioned** — direction genuinely ambiguous; both carriers given, author chooses via `open-loops.md`.
- **repaired** — you rendered it structurally (then appears in the synthesis ledger).

> **v6: `left-for-later` is retired for register breaches.** A load-bearing named emotion or narrator editorial left standing in the floor is a defect, not a deferral — floor it (Operation 3) or option it. Deferring register to downstream passes is the exact friction v6 exists to remove.

**Group a repeated named state.** If the same interior state is named 3+ times in a segment, do not list its instances separately — that hides the real problem. Collapse into one entry: name the state, count, strongest instance, verdict `dilution — keep [strongest], the other namings thin it`.

A permissive segment with zero named-emotion spans listed is a segment you must re-read before trusting.

---

## Output format

1. **Floor draft** (`clean-draft.md`, name kept for convention continuity) — transcoded prose in the floor register, nothing else in this section.
2. **Cut log** — each cut span + one-word reason (`unperceived`, `too-fine`, `narrator-injection`, `modifier`).
3. **Synthesis ledger** — for each collapsed cluster: payload extracted → carrier written. Surface interpretation. If a beat fell to the shortest-form challenge, note what and why. If a dead modifier was cut or a verb changed, note it. If an image was carried twice across lines, present both and ask which to keep. **Register-repair lines get their own flag** — any carrier inventing prose to render an unnamed emotion is the riskiest output. Mark explicitly. If direction was ambiguous, give both carriers and leave a clearly-marked slot in the clean draft pointing to `open-loops.md`. **If a contamination pattern was caught and removed from an invented carrier** (elevation, euphemism, internal gesture, beautified ugliness, clever close — see `REFERENCE/contamination-checklist.md`), note it here in one line.
4. **Leaves left** — per segment, every named-emotion or dissolved-telling span you chose not to touch, each with its verdict. Must be present for every segment. A 3+-instance state appears as one grouped entry.

The synthesis ledger additionally carries (v6): a **`## Floor ledger`** section (original span → floored span → rule cited, one line each) and a **`## Heat bank`** section (dictated warm/hot language banked verbatim, per beat).

## Spine-review gate (v6 — after the slate, before any expansion)

The floor draft is a diagnostic surface: cold and condensed, it exposes developmental seams at their cheapest read-length. On completing the slate:

1. Present CRE the floor draft, the floor ledger, the heat bank, and any **developmental-seam flags** — a missing causal link, an unplanted payoff, a beat with no function, a spine that skips a step the scene needs. Flags are observations on the floor, never proposed fixes (the organic-process guard); research each against the chapter's brief/canon before raising it (DIR-011).
2. CRE rules the seams — re-dictate, restructure, or accept.
3. Only after CRE clears the gate do the expansion passes ([[WORKFLOWS/prose-expansion]], framework steps 4–7) run. **No expansion pass ever runs on an ungated floor.**

Unattended runs (DIR-012): produce the slate + flags, defer the gate to CRE — never self-clear it.

## Stop conditions

- **No envelope provided.** Halt. Ask for one.
- **Chapter folder doesn't exist / not adopted.** Fall through to [[WORKFLOWS/dictation-cleanup]] (the existing project-agnostic workflow) and note the routing miss.
- **Cluster meaning is genuinely unrecoverable.** Don't guess — surface to `open-loops.md` and continue past it.

## Logging

On completion, append to [[_CHANGELOG]]:

```
## YYYY-MM-DD — [fiction] transcoder run on <chapter>
**Ran:** Transcoder v5 on <chapter>/<segment(s)>
**Shipped:** slate/<YYYY-MM-DD-NN>/ (4 files); draft.md stitched; <N> open-loops added; <N> continuity entries
**Open loops:** <pointers>
```

## Security note

⚠️ DIR-001: If raw dictation contains credentials, API keys, or tokens, STOP and flag to CRE before proceeding.
