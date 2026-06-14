---
type: workflow
name: transcoder
trigger: slate this dictation
aliases: [transcode this, run the slate, transcoder v5, slate it]
inputs: [raw dictation text from speech-to-text, perceptual envelope (POV + conditions + state), the contamination checklist at REFERENCE/contamination-checklist.md (optional)]
outputs: [clean rough-draft prose, cut log, synthesis ledger, leaves-left audit]
lane: fiction
status: active
last_updated: 2026-06-13
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]). First adopter — Witchwood.
pipeline_position: upstream of [[WORKFLOWS/dictation-cleanup]]
---

# WORKFLOW: Dictation Transcoder (v5)

> Generative pass that converts raw dictation into a clean rough-draft slate. **Rewrite-allowed.** Pairs with [[WORKFLOWS/dictation-cleanup]] downstream, which is the protective copy-edit pass the v5 spec refers to as the "separate, protective pass… later."

## When to use

When CRE provides raw dictation for a chapter that is using the per-chapter folder convention (envelope.md present). Trigger phrases: "slate this dictation," "transcode this," "run the slate." Do NOT trigger this on a project that hasn't adopted the folder structure — fall back to [[WORKFLOWS/dictation-cleanup]] in that case.

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

You perform exactly two operations, in this order: **Cut**, then **Synthesize**. Nothing else. You do not assess quality, hunt for telling beyond the one register invariant below, or polish. The protective pass ([[WORKFLOWS/dictation-cleanup]]) does that later. Your only job is to hand back a clean, registrally and directionally correct slate.

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

## Register invariants (apply during generation, not as a separate pass)

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
- **left-for-later** — load-bearing named emotion, but rewriting is the protective pass's job.
- **repaired** — you rendered it structurally (then appears in the synthesis ledger).

**Group a repeated named state.** If the same interior state is named 3+ times in a segment, do not list its instances separately — that hides the real problem. Collapse into one entry: name the state, count, strongest instance, verdict `dilution — keep [strongest], the other namings thin it`.

A permissive segment with zero named-emotion spans listed is a segment you must re-read before trusting.

---

## Output format

1. **Clean draft** — transcoded prose, nothing else in this section.
2. **Cut log** — each cut span + one-word reason (`unperceived`, `too-fine`, `narrator-injection`, `modifier`).
3. **Synthesis ledger** — for each collapsed cluster: payload extracted → carrier written. Surface interpretation. If a beat fell to the shortest-form challenge, note what and why. If a dead modifier was cut or a verb changed, note it. If an image was carried twice across lines, present both and ask which to keep. **Register-repair lines get their own flag** — any carrier inventing prose to render an unnamed emotion is the riskiest output. Mark explicitly. If direction was ambiguous, give both carriers and leave a clearly-marked slot in the clean draft pointing to `open-loops.md`. **If a contamination pattern was caught and removed from an invented carrier** (elevation, euphemism, internal gesture, beautified ugliness, clever close — see `REFERENCE/contamination-checklist.md`), note it here in one line.
4. **Leaves left** — per segment, every named-emotion or dissolved-telling span you chose not to touch, each with its verdict. Must be present for every segment. A 3+-instance state appears as one grouped entry.

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
