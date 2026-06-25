---
type: workflow
name: dev-promote
trigger: promote the dev
aliases: [cross the dev into canon, promote dev entry, dev promote, promote to reference]
inputs: [a DEV entry CRE selects — a scenes/, sequences/, or registry/ note from a project's DEV/ tree]
outputs: [gated REFERENCE deltas to bible.md / arcs.md / threads.md (PLANNED), each on CRE's per-fact ruling; provenance (DEV <entry> <date>); superseded facts archived to a History line; optionally a cleared _LEDGER line; a _CHANGELOG entry]
lane: fiction
status: proposed
last_updated: 2026-06-24
revision_note: scoped 2026-06-24 (CRE-attended, ^backlog-dev-promote-crossing). Rulings — write targets = bible + arcs + threads-as-PLANNED; provisional-canon rule = prose wins (chapter-derived supersedes dev-promoted). Build deferred to its own session.
---

# WORKFLOW: dev-promote

> **status: proposed.** This doc is the scoped design, not a built skill. It records the CRE-ruled shape so the build session has a fixed target. Nothing here runs until the skill is built + packaged.

## When to use
CRE has developed a piece of the story in the `DEV/` tree — a scene, a sequence read, a character/lore/location registry entry — far enough that some of it has become **trusted**, and he wants that material to cross **up** into the project's `REFERENCE` canon (`bible.md` / `arcs.md` / `threads.md`) where the drafting pipeline actually trusts it. This is the **one gated crossing** named (but deliberately not built) in [[WORKFLOWS/dev-capture]] § *The one gated crossing*. It is the `promote-revision` discipline applied to development: a deliberate, gated move up — never an automatic sync.

It is **not** capture (that's [[WORKFLOWS/dev-capture]], which routes talk *into* DEV) and it is **not** the draft-derived canon pass (that's [[WORKFLOWS/canon-sync]], which derives REFERENCE *from a landed `draft.md`*). dev-promote sits between them: it lets pre-draft DEV material seed REFERENCE *before* the prose exists, under a hard gate.

## The governing principle — why this is the only rigor seam
The dev layer is permissive and ungated **precisely because nothing crosses into trusted canon silently.** dev-promote is that crossing, so it is where the rigor lives: it **proposes, CRE rules, then it writes** — the canon-sync / reconcile / blind-response gating shape. The marble does not fall here; every fact is a deliberate, ruled commitment. A wrong promotion is expensive (downstream chapters will trust it), so unlike capture, this act gates every fact.

## What it reads / what it writes
- **Reads:** the one DEV entry CRE selects (`scenes/SC NN`, `sequences/SEQ NN`, `registry/<...>`), plus the current `REFERENCE/bible.md` / `arcs.md` / `threads.md` (to diff against). It **never edits the DEV entry** — authority flows up; the DEV note stays the source (the canon-sync "reads draft, never writes it" rule, one storey taller).
- **Writes (only on per-fact approval):** three REFERENCE targets (CRE-ruled 2026-06-24):
  1. **`bible.md`** — durable world/entity facts (a character's canon traits, a lore rule, a place fact).
  2. **`arcs.md`** — character arc maps (entry → waypoints → exit), promoted as **PLANNED** arc intent.
  3. **`threads.md`** — reader-promises, promoted as **PLANNED** only (see the thread lifecycle below). DEV is upstream of planting, so dev-promote may *seed* a promise but never mark it planted/advanced/paid — those states are earned in the prose and remain canon-sync's to write.
- **Never writes:** `story-so-far.md` or a chapter's `continuity.md` — those are draft-derived narrative state, not development intent. dev-promote has no business there.

### The thread lifecycle (why threads-as-PLANNED is safe)
```
PLANNED        (dev-promote — intent: a promise CRE means to plant)
  └─ planted   (canon-sync — the setup appears in a landed draft)
       └─ advanced  (canon-sync)
            └─ paid  (canon-sync)
```
dev-promote owns only the **PLANNED** rung. When the dramatizing chapter lands, canon-sync transitions the promise PLANNED → planted from the prose (prose wins — see below). A PLANNED promise that never gets planted is a visible, harmless to-do, not a continuity wound.

## Provenance + the provisional-canon rule (prose wins)
Every promoted fact carries dev provenance: **`(DEV <entry> <date>)`** — e.g. `(DEV scenes/SC 12 2026-06-24)`. This makes a promoted fact **provisional canon** and keeps re-promotion idempotent (re-promoting an entry replaces exactly its own `(DEV ...)` facts, the canon-sync provenance discipline).

**Prose wins (CRE-ruled 2026-06-24).** When the chapter that dramatizes a promoted fact later **lands**, canon-sync derives the same fact from the prose with `(CH<N> rev<M>)` provenance. The chapter-derived fact is **authority**: canon-sync **supersedes** the `(DEV ...)` line and archives it to the fact's History line (never a silent delete). The result is a single source of truth — REFERENCE never carries a stale dev-intent fact next to the as-written one.

> **Build dependency:** this rule requires a small `canon-sync` extension — it must recognize a `(DEV ...)`-provenanced fact as **supersedable** and archive it when it writes the matching chapter-derived fact. Note in the build: canon-sync currently only replaces its own `(CH<N> rev<M>)` facts; teach it to also retire a superseded `(DEV ...)` provisional fact for the same entity/claim. Until that extension ships, a landed chapter would leave the `(DEV ...)` line in place (visible, not wrong — just not yet auto-retired).

## The gating shape (two-phase, the canon-sync / reconcile pattern)
**Phase 1 — propose.** Read the selected DEV entry; derive a **delta sheet** of candidate REFERENCE facts. Tag each:
- **ADD** — new to REFERENCE.
- **CHANGE** — refines an existing REFERENCE fact (non-contradicting).
- **CONTRADICTION** — collides with an existing REFERENCE fact (a continuity fork).

Each candidate shows its target file, the proposed line with `(DEV <entry> <date>)` provenance, and (for CHANGE/CONTRADICTION) the existing line it touches.

**Phase 2 — CRE rules each, then write.** CRE rules every candidate (approve-add / approve-change / defer / reject). Only approved facts are written (file tools, DIR-005; serialized frontmatter if any, DIR-004). A CONTRADICTION is **never** auto-overwritten — on approval the superseded fact archives to a History line. Nothing writes without an explicit ruling.

**Preserve-the-kind carries up.** A claim CRE left open in DEV ("maybe she knows") is **not promotable as settled canon**. The router surfaces it as a question to resolve first, never silently hardens it. (The dev-capture preserve-the-kind discipline, enforced at the crossing.)

## Steps
1. **Sentinel + load.** Confirm `_DIRECTIVES.md` frontmatter (`^obs-004`). Resolve the project; load the selected DEV entry + current `REFERENCE/bible.md` / `arcs.md` / `threads.md`.
2. **Derive candidates.** From the DEV entry, extract durable facts (→ bible), arc waypoints (→ arcs, PLANNED), and intended promises (→ threads, PLANNED). Skip CRE-left-open questions (preserve-the-kind).
3. **Diff + classify.** Against current REFERENCE, tag each candidate ADD / CHANGE / CONTRADICTION; attach `(DEV <entry> <date>)` provenance.
4. **Gate (Phase 1 → CRE).** Present the delta sheet. CRE rules each.
5. **Write approved (Phase 2).** Write ruled facts to their targets; archive any superseded fact to a History line. File tools only; never touch the DEV entry.
6. **Ledger (optional).** If a `_intake/_LEDGER.md` collision is what surfaced this promotion, clear/annotate that line when the promotion resolves it (the ledger ↔ promotion pairing named in `^backlog-dev-promote-crossing`).
7. **Log.** Append a `_CHANGELOG` entry (fiction lane); report the promoted facts + any deferred/rejected.

## Scope guards (must-not)
- No prose drafting; no edits to the DEV entry (read-only on DEV).
- No writes to `story-so-far.md` / `continuity.md` (draft-derived, not dev-derived).
- No auto-cross — every fact gates; nothing writes without a ruling.
- No resolving a CRE-left-open question; no marking a thread planted/advanced/paid (those are prose-earned, canon-sync's).
- No `patch_vault_file` / whole-file MCP rewrite of REFERENCE docs (DIR-005); file-tool targeted edits, re-read to verify.

## Relationship to the pipeline
- **Upstream:** [[WORKFLOWS/dev-capture]] fills the DEV tree; dev-promote is the gated exit *up* from it.
- **Sibling:** [[WORKFLOWS/canon-sync]] derives the same REFERENCE files from a landed `draft.md`. dev-promote is the *pre-draft* path into the same canon; the prose-wins rule keeps them from fighting (canon-sync supersedes dev-promoted facts on land).
- **Pattern parents:** [[WORKFLOWS/promote-revision]] (the gated deliberate move up) + [[WORKFLOWS/canon-sync]] (the derive-classify-gate shape). dev-promote holds no new gating philosophy — it reuses theirs at a new seam.

## Build order (smallest proving loop first)
1. **bible-only proving loop:** one registry entry (a lore rule or a character's durable traits) → `bible.md`, full two-phase gate, `(DEV ...)` provenance, History-archive on contradiction. Prove the gate + provenance where the fact shape is simplest.
2. **arcs (PLANNED):** promote a character's arc waypoints from a `sequences/`/`scenes/` read into `arcs.md` as PLANNED intent.
3. **threads (PLANNED) + the lifecycle:** seed PLANNED promises into `threads.md`; spec the canon-sync PLANNED → planted transition.
4. **canon-sync supersession extension:** teach canon-sync to retire a superseded `(DEV ...)` provisional fact on land (the prose-wins build dependency above).
5. **_LEDGER pairing (optional):** consume/clear a ledger collision line when a promotion resolves it.
Package as **one skill** mirroring `canon-sync` (it shares the sentinel + gating shape). Add the trigger row to [[_SKILLS MAP]] at build time (deferred now to avoid touching the truncation-prone canon doc pre-build — the `^backlog-chapter-pipeline-skillsmap` precaution).

## Stop conditions
- No DEV entry selected / entry empty → "nothing to promote," stop.
- No `REFERENCE/` tree for the project → halt (REFERENCE is the write target; don't scaffold it here).
- Every candidate is a CRE-left-open question → stop; surface the questions, promote nothing.
- A secret/credential in the DEV entry → never promote; flag + advise rotate (DIR-001).

## Logging
On completion, append a `_CHANGELOG` entry under the `fiction` lane; file any genuinely new build surprise to [[_OBSERVATIONS]] with a `^obs-NNN` anchor; add follow-up build tasks to [[_BACKLOG]].
