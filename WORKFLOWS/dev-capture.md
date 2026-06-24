---
type: workflow
name: dev-capture
trigger: capture the dev
aliases: [route the dev intake, sort the dev transcript, develop this, file the development, run the dev router]
inputs: [a cleaned dictation transcript (Buzz-local for long sessions, or dictation-runner for short voice notes), targeted at a project's DEV/ layer]
outputs: [segments routed into DEV/scenes, DEV/sequences, DEV/registry, DEV/_DEV.md; held items in DEV/_intake; a deferred contradiction line in _LEDGER.md; an observed-pattern noticing in _POETICS.md; a routing log]
lane: fiction
status: draft
last_updated: 2026-06-22
revision_note: layer two hardened 2026-06-21 — cue-or-reason router across all buckets + deferred ledger + poetics graduation loop proven (sandbox); gated REFERENCE crossing remains separate. 2026-06-22 — added cleanup discipline (intake-removal invariant + scoped/guarded .tmp orphan sweep, Steps 4/8)
---

# WORKFLOW: dev-capture

## When to use
CRE has talked himself through a piece of the story — at any level, project down to scene — and wants that messy, non-linear development talk **captured and organized**, not drafted. This is the **upstream-of-the-brief** layer: the molten "what is this about, what do I love about it, what has to happen here" thinking that *produces* the brief, the threads, the bible — long before any of that is settled. It is **not** drafting prose (that's the dictation route → transcoder) and it is **not** the runway (that's [[WORKFLOWS/runway-builder]], which derives a forensic outline *from* an already-filled brief). This sits below even the brief.

> **Naming guard (DIR-005 hygiene):** do **not** call any of this "runway." There is already a `runway.md` and a `runway-builder`. This layer is the *richer source* a future runway inherits from. Call the tree `DEV/`, call the act *capture* / *develop*.

## The governing principle
**The work moves as it moves; the system follows CRE's flow rather than making CRE follow its structure.** Every design decision below serves that. Capture is permissive and ungated. The single act of rigor lives at exactly one *space* seam (the crossing from DEV into trusted REFERENCE canon, which gates) and one *time* seam (contradictions with already-banked manuscript material, which defer silently to the editing pass). Everywhere else, the marble falls — a wrong routing call is cheap to reverse because **nothing downstream trusts this layer yet.**

## The DEV/ tree (per project, sibling to CHAPTERS / REFERENCE / STORYLINE)
```
WRITING/PROJECTS/<PROJECT>/DEV/
├── _DEV.md              project-level taste anchor: "what I love / what I know so far"
├── project.md           the macro read (logline, what it's about, tone targets) — DERIVED from sequences
├── sequences/
│   └── SEQ NN - <name>.md     one evolving entry per sequence — DERIVED running-read of its scenes
├── scenes/
│   └── SC NN - <name>.md      one evolving entry per scene — THE GRANULAR UNIT (scene = truth)
├── registry/            the wiki — each entry its own note, wikilinked
│   ├── characters/<name>.md
│   ├── locations/<name>.md
│   ├── lore/<topic>.md
│   └── items.md
├── _intake/             holding pen — UNROUTED only: raw transcript lands here, held/ambiguous segments wait here; a routed transcript is removed once swept to _audit/ (the floor is canonical)
│   ├── _LEDGER.md        the deferred contradiction ledger (silent capture, editing-seam resolution)
│   └── _audit/           the transcript floor — swept source transcripts land here; the recovery point a scene's one-line pointer aims at
├── _POETICS.md          observed patterns in HOW CRE develops (capture-permissive, promote-gated)
└── _DEV_MAP.md          this project's cue table + routing rules (the local index)
```

### Three strata, separated by what they model and how they gate
1. **Content** — `scenes/`, `sequences/`, `project.md`, `registry/`. Ungated. **Scene is truth and the evolving unit.** Authority flows *up* (scene → sequence read → project read); the taste anchor propagates *down* (every scene measured against `_DEV.md`). Sharpening **overwrites in place** (sculptor, not historian) — the swept source transcript in `_intake/_audit/` is the floor a superseded take is recoverable from; the entry keeps only a one-line pointer to the dig site, never the old prose. **Down-propagation is surface, not seize:** when the taste anchor sharpens, the router *flags* any `scenes/` entry whose taste has drifted from it — it never rewrites the scene, only surfaces the drift for CRE to rule.
2. **Contradiction ledger** — `_intake/_LEDGER.md`. Silent capture, **deferred** resolution. Logs every ripple that collides with already-banked manuscript material; surfaces **only** when CRE leaves the creative seat and asks. Never interrupts mid-flow.
3. **Poetics log** — `_POETICS.md`. Observes CRE's *process* (routing reality, cue vocabulary, habitual order, braiding), never his *content*. Capture-permissive, promote-gated, slow to generalize. The `OBSERVATIONS → DIRECTIVES` discipline pointed at CRE's creative cognition.

## Two transport paths, one router
Transport and routing are **separate concerns** — the router keys off a *text transcript + a cue*, never off audio.
- **Path A — short voice notes (≤5 min):** ✅ **WIRED (2026-06-21).** [[WORKFLOWS/dictation-runner]] transcribes, then its `classify_route()` forks a clip headed with **"dev note"** (or **"capture the dev"**) into `<PROJECT>/DEV/_intake/`. The `dev` marker **wins over the fiction markers** — a spoken project name still picks *which* project's DEV tree, but no longer forces the fiction branch (CRE ruling). Say the project to target it (`"dev note, Witchwood — the scene where…"`); omit it and it defaults to Witchwood flagged `uncertain`. A sub-cue ("scene…", "character…") is preserved as a routing hint. If the named project has no `DEV/` tree, the clip falls back to INBOX rather than scaffolding silently. As of 2026-06-22 the runner also **canon-reconciles** the dev clip and runs **mechanical cleanup** on it (the mechanical pass of `dictation-cleanup`, Pass 1–2 only — *not* the full fiction copy-edit; dev talk is loose notes, not prose) before the note lands in `DEV/_intake/`, so the transcript this router segments is always clean. The runner only **stages** that cleaned note; you then run **"capture the dev"** to segment + route it (the runner never writes `DEV/scenes|sequences|registry` directly). Marker set is intentionally the narrow phrase "dev note" so it never fires mid-prose.
- **Path B — long development sessions (the deep work):** CRE records long-form and gets a text transcript (Buzz locally, or any STT). This is the *more* important path, and as of 2026-06-22 there are two ways in, both ending clean: **(1) automated** — drop the `.txt`/`.md` transcript into [[WORKFLOWS/dictation-runner|_DICTATION INBOX]] headed `dev note`; the runner reads it directly (no chunking ceiling), reconciles it, runs **mechanical cleanup**, and lands it in `DEV/_intake/` ready for this router. **(2) manual** — run **mechanical** [[WORKFLOWS/dictation-cleanup]] (Pass 1–2 only — *not* the full fiction copy-edit; dev talk is loose notes, not prose) on the transcript yourself, then drop it where this router reads it. Either way the chain is **transcript → mechanical cleanup → dev-capture router (this doc) → segments land in `DEV/`** — this router is only the last link, and it now always receives a cleaned transcript.

## The cue table (the verbal cues that route)
| CRE says (head of a segment) | Routes to | Builds / updates |
|---|---|---|
| "project level…" / "what I love about this book…" | `_DEV.md` (+ `project.md`) | the taste anchor + macro read |
| "sequence — the part where…" | `sequences/SEQ NN.md` | evolving sequence entry |
| "scene — …" / "the moment when…" | `scenes/SC NN.md` | evolving scene entry (granular unit) |
| "character — everything about…" / arc/transformation talk | `registry/characters/<name>.md` | character registry entry |
| "world / lore — …" / "the magic works like…" | `registry/lore/<topic>.md` | lore entry |
| "place — …" | `registry/locations/<name>.md` | location entry |
| (no cue, project-bound) | inferred per the segmentation contract below | best-guess or held |

## Core discipline — the segmentation contract
A long transcript carries material for several files at several scopes, so the router **segments then routes** (the [[WORKFLOWS/inbox-router]] shape), with a graceful-degradation hierarchy because **the input will never be clean and shouldn't have to be:**

1. **Explicit cue wins, always.** A spoken cue is a hard boundary *and* a hard destination — no inference, no second-guessing. The deterministic floor.
2. **Missed cue → infer from content, with confidence, and TAG the boundary as inferred.** Sustained focus on a character's traits/flaws/arc → registry. A GOAL→BUT→THEREFORE chain → sequence. A concrete moment with sensory detail + a stumbled line of dialogue → scene. An inferred segment is visually distinct from a cued one in the result.
3. **Below the confidence bar → HOLD in `_intake/`, never force-file.** A confident misfile is more annoying to undo than an unrouted fragment. This is the one place the router *declines to act* — the Needs-review bin applied here.

**Recognized braid (graduated poetics pattern):** when a segment legitimately feeds two buckets — e.g. CRE braids character transformation with plot intensity — route to **both**, wikilinked, rather than force-choosing one or holding as "ambiguous." Dual-destination is a *recognized shape*, not a failure, once the pattern has graduated in `_POETICS.md`.

**Preserve the kind.** Never resolve ambiguity the author left open. "Maybe she knows" stays a question, not "she knows" — manufacturing canon CRE never committed to is the cardinal sin (the transcoder's open-loops discipline, applied at the dev layer). A stumbled line of dialogue is captured as a **target to reach toward**, flagged un-pressure-tested — never as committed prose. Development is *reaching-toward*; drafting is *committing*; the registers stay distinct even though the medium (voice) is identical.

**Taste is a first-class field, not exhaust.** "How much I like it / what interests me / what feels right" is the steering signal of the whole project — captured, propagated down the spine, never discarded as meta-commentary.

## Steps

### Step 1 — Vault sentinel + load
Confirm `_DIRECTIVES.md` frontmatter (`^obs-004` guard). Identify the target project and read its `DEV/_DEV_MAP.md` (cue table + any graduated `_POETICS` patterns) and `_DEV.md` (the taste anchor, so it can measure drift and propagate it).

### Step 2 — Segment
Split the cleaned transcript into discrete segments: on explicit cues first (hard boundaries), then on topic shifts. One developed thought = one segment. Don't merge unrelated talk; don't split a single continuous thought.

### Step 3 — Classify (cue → reason → hold)
Per segment, apply the segmentation contract: cue wins; else infer-and-tag on the confidence bar; else hold. Apply graduated braid patterns from `_POETICS` (dual-route recognized braids). Watch for: a segment that resolves an ambiguity CRE left open (preserve the question instead); a stumbled dialogue line (capture as target, flag un-tested); a secret (DIR-001 — never file, flag).

### Step 4 — Route (confident + cued segments)
Write each into its destination, **scene-level overwriting in place** (sculptor): the entry becomes the current sharpest version; sweep the source transcript to the floor at `_intake/_audit/` and leave a one-line pointer (`superseded prior take: see _audit/<date>`) — no old prose retained. **Once the transcript is fully processed** (every segment routed or captured as its own HOLD file in Step 5), **remove it from `_intake/`** — the `_audit/` floor is the canonical verbatim copy and `_intake/` holds only *unrouted* material. Registry entries are wikilinked (basename form — `[[Entry]]` / `[[items#Heading]]`, per the `_DEV_MAP` wikilink convention) so Obsidian's graph *is* the connection map. Re-derive the sequence read above any changed scene, and note if the project read may have shifted (silent, no ceremony — authority flows up).

### Step 5 — Hold the rest
Below-bar / unsplittable segments stay in `DEV/_intake/` with the candidate destinations + one line on why held. Never auto-file these.

### Step 6 — Ledger (deferred contradictions)
If a scene discovery rolls up and collides with **already-banked manuscript material** (a landed `draft.md`, a sealed thread, a paid-off plant), log a line to `_intake/_LEDGER.md` — silently. **Do not surface it now.** It becomes an agenda item for the developmental editing pass, when the finished work can actually judge whether the change earned its disruption or is a true continuity wound. (Resolving the ledger is a separate, future editing workflow — out of scope here.)

> **Configurable surface-trigger (forward-compat — see Scaling profiles).** The ledger's *surface trigger* must be a setting, not a hard-coded "defer to editing." For a novel it surfaces at the **editing seat** (the work can still be revised whole). For **serial fiction** it must surface at the **ship boundary** — before the next installment publishes — because once an installment ships it can't be revised and the contradiction cost becomes permanent. Same ledger, same silent capture; only the surfacing moment moves. Build the ledger with this trigger configurable from day one — it is cheap to honor now and expensive to retrofit.

### Step 7 — Poetics (observe the process, slowly)
File any repeated routing reality as a `^poe-NNN` noticing in `_POETICS.md` (dated, with a **sighting count**). **Assign `^poe-NNN` collision-safe:** scan the *whole* `_POETICS.md` for the highest existing anchor and take max+1 — never reuse a number a concurrent run or manual edit may already hold (the `^obs-122` duplicate-`^poe-002` class). A noticing does nothing binding and **does not surface for CRE's ruling until it has recurred** (slow to generalize — one session is an anecdote). The log models *process only*, never story content: where things go, what cues mean, what order CRE thinks in. It learns the shape of the hand, never holds the brush.

### Step 8 — Log + report
Early-trust mode: leave a short routing log showing the router's reasoning (`segment 3 → characters/Halloran.md (inferred: sustained character focus, no cue); segment 7 → _intake, held (sequence beat or scene?)`) so CRE can see where its calls match his intent. Mute on request once trust is established. Report a compact *segment → destination* table + the held list. Append a dated entry to [[_CHANGELOG]] under the `fiction` lane. **Leave the floor clean (cleanup):** after your file-tool writes finish, sweep atomic-write orphans *you* created — for each file you wrote (DEV entries, `_CHANGELOG`), delete only a `<basename>.tmp.<pid>.<hex>` sibling **whose real target exists and is non-empty**, matched by exact basename. Never a blind `*.tmp` wipe; never touch a temp whose target is missing (it may be another process's in-flight write). A vault-wide orphan sweep is the janitor pass's job, not this one.

## The one gated crossing (stated, not built here)
Promoting DEV material into trusted **REFERENCE** canon (bible / threads / arcs) is a **separate, deliberate, gated act** — the `promote-revision` discipline applied to development. The dev layer's permissiveness is *safe precisely because* nothing crosses into canon silently. That gate is named here for completeness but is a downstream workflow, not part of capture.

## Scaling profiles (forward-looking — editions, not re-scopes)
**The engine is scale-free; only the spine and the registry location flex.** The three strata, the cue-or-reason router, scene-is-truth, sculptor-overwrite, the transcript floor, the ledger, and the poetics log scale untouched — they operate on the granular unit and never depend on the macro shape. The poetics log even *crosses* projects (it learns CRE, not the project). So every form below is an additive edition; **none reaches into this workflow and changes it.** Two commitments keep that door open and both are already honored: **(a)** the router routes the granular unit and never hard-codes the macro shape; **(b)** registry entries are standalone wikilinked notes, so they can be lifted *upward* without a migration.

The scaffold skill (separate) picks a **spine profile by form**:
- **Short story** — collapse to `scenes/` + `registry/` + `_DEV.md` (the taste anchor *is* the macro read at this size). No `sequences/`, no `project.md`.
- **Novella** — `scenes/` + an optional lighter `movements/` rung + registry + taste anchor.
- **Novel** — the full tree above (all rungs).

Planned later editions (defer until proof-of-concept; **no re-scope required**):
- **Series** — a shared `registry/` + `arcs/` + `_SERIES_DEV.md` layer *above* the books; per-book DEV trees reference *up* into it (authority-flows-up, one storey taller — the canon-sync derivation discipline applied a level up). New layer, additive; the standalone-registry commitment (b) is what makes lifting `registry/` up to series level a *move*, not a rebuild.
- **Serial fiction** — reuses the short/novella profile; its one real difference is the ledger's surface-trigger flips from editing-seat to **ship-boundary** (see Step 6). A constraint change, not a structural one.
- **Substack** — mostly *not* a dev-layer concern: the *publication/channel* is the existing BUSINESS/SUBSTACK lane; the *fiction* is a short-story or serial-profile DEV tree. The only new piece is a fiction→post **hand-off** skill at the seam; the dev layer doesn't need to know Substack exists.

## Stop conditions
- No transcript / empty input → "nothing to capture," stop.
- No target project resolvable (no project named, no cue implying one) → hold the whole transcript in the most likely project's `_intake/` only if confident; else surface to CRE which project. Don't scatter across projects.
- Secret/credential detected → never file; flag + advise rotate (DIR-001).
- A `DEV/` tree doesn't exist yet for the project → halt and run the `DEV/` scaffold first (the `chapter-init`-style deterministic scaffolder — separate skill).
- The router is about to resolve an ambiguity CRE left open, or graduate a poetics pattern on first sighting → stop; preserve the question / wait for recurrence.

## Build order (smallest proving loop first)
1. The `DEV/` scaffold for Witchwood (deterministic, every file stamped — mirrors `chapter-init`, no template-copy drift).
2. **Scene-capture path only:** spoken/Buzz scene → evolving `scenes/` entry, sharpen-in-place, transcript to the floor, pointer left behind. Prove the granular unit where most discovery happens.
3. The taste anchor `_DEV.md` + its downward propagation (the anti-drift payoff; cheap).
4. *Then* layer two: sequences, full registry, the cue-or-reason router across all buckets, the deferred ledger, the poetics log — **BUILT + hardened 2026-06-21** (router proven end-to-end across every bucket against a sandbox copy of the Witchwood `DEV/` tree; the poetics graduation loop is concrete in SKILL.md Step 7 + the `_DEV_MAP` graduated-patterns binding format). **Still separate:** the gated REFERENCE-promotion crossing (its own downstream workflow — see *The one gated crossing* above). Propagation to the installed skill = the desktop `pack-skills.ps1` + Save-skill repack (source-ahead).
5. *Later editions (no re-scope — see Scaling profiles):* the scaffold's form-profile switch (short story / novella / novel), then series (shared registry + arcs layer), serial (ledger ship-boundary trigger), and the Substack fiction→post hand-off. Build each after proof-of-concept; the foundation does not move for any of them.

## Logging
On completion, append an entry to [[_CHANGELOG]] under the `fiction` lane; file any genuinely new build surprise to [[_OBSERVATIONS]] with a `^obs-NNN` anchor; add follow-up build tasks to [[_BACKLOG]].
