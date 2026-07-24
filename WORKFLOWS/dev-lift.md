---
type: workflow
name: dev-lift
trigger: lift the dev
aliases: [run the dev lift, lift part N, lift the narration, dev lift]
inputs: [a cleaned dev transcript (a DEV/_intake staging note, or its swept copy on the _intake/_audit floor) whose body is predominantly narrated story]
outputs: [per-sequence proto-draft files in DEV/proto/ (derived, regenerable); a stream-split map + flag counts in the run report; the editorial stream left for dev-capture (pointer only — this pass never routes dev notes)]
lane: fiction
status: spec — packs after 2-3 live runs
last_updated: 2026-07-23
revision_note: born 2026-07-23 from the Part 9 ruling — CRE's dev captures are narration told to himself as audience, not aboutness; the dictation runner's repeated prose-route signal on Witchwood dev clips was correct. Pilot lift (SEQ 70-71) same day.
---

# WORKFLOW: dev-lift

## When to use
CRE's dev capture for a part/sequence is **the story told** — near-prose in the wrong tense, wrapped in a thin editorial frame ("The next sequence is…", "This sequence highlights…") — and he wants the narration lifted into a workshoppable rough draft **without waiting for the descent to chapters**. The output is a **proto-draft**: his words, tense-normalized, editorial frame stripped, thin spots flagged. It enters the battery at workshop/blind-read instead of at a blank page.

Do NOT use it to:
- route dev notes into the DEV tree — that is [[WORKFLOWS/dev-capture]] (the editorial stream is *its* material; this pass only lifts the narration stream);
- generate prose from genuine aboutness — if a transcript is mostly planning talk with no narration, there is nothing to lift (stop condition below);
- compress dictation against a perceptual envelope — that is the Transcoder, which needs a chapter folder + envelope.md and does a different job;
- revise or polish existing prose — register-pass / dictation-cleanup own that.

## The authorship line (governing principle)
**You-spoke-it vs machine-invents-it** — that is the only line, and it is not dev-vs-chapter (the 2026-07-23 ruling; see `^obs` entry of that date). When the dev capture is narration, lifting it is **dictation-cleanup-class work**: word-preserving transformation of CRE's own telling. The pass may *delete frame* and *shift tense*; it may **never add narrative content**. Every gap, every summary patch, every ambiguity survives as a flag, not a fill. The moment a lift dramatizes a summary sentence or bridges a gap, it has crossed into authorship — hard stop, cardinal sin.

## Position in the pipeline
A **sibling pass to dev-capture over the same transcript**, not a replacement and not a stage of it:

- **dev-capture** consumes the *editorial stream* (frames, taste, structure talk) → DEV entries. It owns the transcript's `_intake/` lifecycle (sweep to floor, removal).
- **dev-lift** consumes the *narration stream* → `DEV/proto/`. It reads the transcript wherever it lives (`_intake/` or the `_audit/` floor) and **never moves, edits, or removes it**.

**Run order: capture first, lift second** (amended 2026-07-23, run 1). The reads are where rulings land — normalized garbles, ruled terms, canon corrections, CRE confirmations from dev-reconcile. A lift that runs before (or ignorant of) the capture ships flags the tree already answers: on Part 9, four of the lift's six `[AUTHOR:]` flags and one adage error were already CRE-ruled in the sequence reads, and the protos had to be corrected after the fact (`^poe-015`). Same-session back-to-back is still the natural shape — capture leg first. The proto layer is **derived and regenerable** — nothing downstream trusts it until the descent seeds it (see *Descent wiring*), so a lift is a safe-op write, cheap to discard and re-run.

## The two streams (split rules)
Segment the transcript line-by-line into:

1. **Editorial stream** — structural frames ("The next sequence is…", "This act picks up…", "That is the final part…"), analysis/taste ("This sequence highlights…", "It demonstrates that…", "This is the braid itself"), process talk ("Okay, let's do a dev note capture for…"). → excluded from the lift; listed in the split map; dev-capture's material.
2. **Narration stream** — story told: events, imagery, verbatim dialogue, interiority CRE actually spoke. → lifted.

**Boundary calls:** a sentence that *frames then narrates* ("The next sequence is just that: a dangerous and deadly game of…") is split at the colon — frame out, narration in. An analysis sentence carrying story facts ("It demonstrates that she has embraced *when in dark places, become delight*") is **not** silently converted to scene: it goes to the lift as a `[SUMMARY]` block (below). When in doubt, keep it in the lift as `[SUMMARY]` rather than dropping content on the floor.

## The lift rules
**Permitted operations (exhaustive):**
- **Tense normalization** to the project's narrative tense (Witchwood: past; check a landed `draft.md`, not the register doc, for ground truth), with only the agreement/pronoun smoothing the tense shift forces.
- **Frame removal** per the split rules.
- **Spoken-syntax repair** where dictation broke grammar (subject/verb tangles, dropped words) — same license as dictation-cleanup Pass 1, minimal-touch.
- **Paragraphing** by beat, mechanical.
- **Flag carry-through** — every `[AUTHOR: …]` flag from the runner's cleanup survives verbatim, in place.

**Forbidden (the authorship guard):**
- No new sentences, images, dialogue, or transitions. No bridging between narrated moments — a jump gets `[GAP: …]` naming what's missing, one line, interrogative not prescriptive.
- **Summary stays summary.** A telling-register patch ("Their reunion is heartfelt and cathartic") is carried inside a flagged block: `> [SUMMARY — dramatize at desk/mic]: <his sentence, tense-lifted>`. Never expanded.
- No register enforcement, no diction "improvement," no epithet changes — the lift targets tense and frame only; register-pass exists downstream, at the chapter layer, on CRE's trigger.
- No resolving of ambiguities CRE left open (the preserve-the-kind rule from dev-capture applies here verbatim). Name discrepancies against the tree (transcript vs `sequences/` spelling) are surfaced in the report as one-tap confirms (DIR-011), never silently normalized in his prose.

## Output convention
One file per sequence, keyed to the existing `DEV/sequences/` naming:

```
WRITING/PROJECTS/<PROJECT>/DEV/proto/
└── SEQ NN - <name> (proto).md
```

Frontmatter (DIR-004: `yaml.safe_dump`-serialized, parse-gated before the write is treated as done): `type: proto-draft`, `project`, `sequence`, `source` (the transcript basename), `lifted` (date), `tense: <from> -> <to>`, `flags: {summary: N, gap: N, author: N}`, `status: lifted | pilot`. Body = the lifted prose with flags inline. **Naming guard:** never call these files `draft.md` and never write into a chapter folder — `draft.md` is chapter-owned, desktop-attended territory.

## Steps
1. **Sentinel + load.** `^obs-004` guard. Resolve project + transcript; read the transcript via the file tools. Read one landed `draft.md` opening for target tense/POV ground truth. Read `DEV/sequences/` names for keys (a `Glob` miss is not absence — DIR-005; confirm with `Grep`/`Read`).
2. **Narration density check.** If the body is mostly aboutness, stop and say so — route to dev-capture alone.
3. **Split.** Build the stream map (per-paragraph: editorial / narration / mixed-split). This map ships in the report.
4. **Map to sequences.** Match narration runs to `DEV/sequences/` entries by the transcript's own frames + content. Unmatchable runs go in one `UNPLACED (proto).md` with a flag — never guess a home.
5. **Lift.** Apply the lift rules per sequence. Count flags.
5b. **Ruling sweep (added 2026-07-23 — DIR-011/DIR-014 at this seam).** Before finalizing, check every would-be flag and every proper noun against the matching `sequences/` reads, `_DEV_MAP`'s ruled-terms table, and the `_intake/_audit/` rulings floors. Tree-answered → **apply with provenance** in the proto's header note ("resolved against [[SEQ NN]], CRE-confirmed <date>"), never left as an open flag; tree-glossed-but-unconfirmed → downgrade to *confirm at desk*; tree-silent → stays open. Then add the reciprocal pointer: each touched sequence read gets a one-line `Proto-draft:` footer link.
6. **Write** proto files (serialize + parse-gate frontmatter). Safe-op; overwrite-in-place on re-run (sculptor — the transcript itself is the floor).
7. **Report.** Split map, sequence map, flag counts, name-discrepancy confirms, and the one-line reminder that the editorial stream still awaits "capture the dev" if it hasn't run. Log per DIR-003.

## Descent wiring (stated, not built here)
When shape-the-part / chapter-init cuts chapters for a lifted part, the chapter's starting `draft.md` may be seeded from the mapped proto files, provenance-stamped (`source_proto:`), entering the battery at workshop/blind-read. That seeding is a **gated, attended act** belonging to the descent skills — dev-lift never writes it. Amendment tracked in `_BACKLOG`.

## Stop conditions
- Transcript not found / empty → stop.
- Narration density below the bar (mostly aboutness) → stop, report, recommend dev-capture only.
- No `DEV/` tree or no `sequences/` entries to key against → stop; scaffold/dev-capture first (an unkeyed lift would invent structure).
- Secret/credential in the transcript → never file; flag + rotate (DIR-001/DIR-006).
- The lift would require inventing a transition, dramatizing a summary, or resolving an open ambiguity to proceed → flag it and move on; if the whole run degenerates into that, stop — the material isn't narration.

## Logging
Per DIR-003: `_CHANGELOG` entry (fiction lane), surprises to `_OBSERVATIONS`, follow-ups to `_BACKLOG`.
