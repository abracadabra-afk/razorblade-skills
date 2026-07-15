---
type: workflow
name: dev-readiness
trigger: dev readiness check
aliases: [what's load-bearing, prioritize the dev, what should I flesh out next, what's blocking the descent, surface the dev gaps, prime the dev]
lane: fiction — upstream-of-the-brief (DEV/ layer)
profile: project-agnostic (any project with a DEV/ tree)
status: draft
last_updated: 2026-07-15
revision_note: parked-fork triage added 2026-07-15 (CRE-ratified, dev-reconcile v1.2 companion) — reads DECISIONS/ parked entries for the target project and classifies them by the parked-until wake convention; ripe forks lead the punch list. 2026-06-23 — referenced-only blind-spot caveat + start-gate vs late-beat blocker split
---

# dev-readiness — DEV-layer readiness audit (read-only)

> **What this is:** the **read-side sibling of `dev-capture`.** `dev-capture` writes *into* a project's `DEV/` tree from CRE's development talk; `dev-readiness` reads that tree and reports *up* — a prioritized punch list of the **load-bearing topics CRE should flesh out before descending** to the next layer (sequence → scene). It exists so CRE can keep the `DEV/` folder an **organically developed product he deliberately does not browse** — the skill is the one thing that stares at the folder, so he doesn't have to.
>
> **The development-stage cousin of `blind-read` / `workshop-chapter`:** like them it is **READ-ONLY** and diagnostic. Unlike `workshop-chapter` (which is chapter-scoped, downstream of a draft) this runs on the **pre-draft DEV layer**, before any chapter exists.

---

## What it is NOT
- **Not `dev-capture`.** It never writes into the creative layer, never routes a transcript, never sharpens an entry. (`dev-capture` is the write side; this is the read side.)
- **Not a content generator.** It **surfaces gaps and questions; it never fills them.** It says *"the Widowsbane has no origin and it's load-bearing" — it does not propose what the Widowsbane is.* Same discipline as `dev-capture` (reaching-toward, never committing) and `workshop-chapter` (never generates CRE's prose). **This is the guardrail that protects the organic process** — see Standing rules.
- **Not `workshop-chapter`** (chapter-in-progress, post-draft) or `canon-sync` (derives REFERENCE from a *landed* draft). This is strictly the `DEV/` layer.

---

## Trigger phrases
"dev readiness check" · "what's load-bearing" · "prioritize the dev" · "what should I flesh out next" · "what's blocking the descent" · "surface the dev gaps" · "prime the dev"

---

## Inputs (read-only)
The target project's `DEV/` tree:
- `_DEV.md` — taste anchor (esp. **Open questions I'm holding** + **What I know so far**)
- `project.md` — macro read (esp. an empty **Shape** = no sequence layer yet)
- `sequences/` (or `movements/`) and `scenes/` — the descent layers; empty = not yet built
- `registry/` — `characters/`, `locations/`, `lore/`, `items.md` (dangling wikilinks + empty buckets live here)
- `_intake/_LEDGER.md` — banked-material collisions
- `_POETICS.md` — how CRE develops (context only; never a gap)
- `_DEV_MAP.md` — the tree's own profile (short/novella/novel may legitimately lack rungs)
- **`DECISIONS/` parked entries for this project** (`type: decision`, `status: parked`, `project:` matching) — the forks dev-reconcile banked; triaged by the wake convention (see Steps)

---

## The prioritization rubric — what makes a gap "load-bearing"
Four signals. A gap that lights up more signals ranks higher.

1. **Referenced-but-empty** — a `[[wikilink]]` with no entry behind it, or an empty registry bucket that other entries already lean on. Something in the tree already depends on it (e.g. `[[Wishbringer]]` linked from a character, no item entry).
2. **Adjacency to a held-open question** — the gap sits next to one of `_DEV.md`'s **Open questions** or a climax/structural unknown. Fleshing it out might *resolve* that question, not just decorate it. (Highest-leverage signal.)
3. **Blocks-the-next-descent** — the gap must be filled before the next layer down is productive. *You cannot talk the sequence usefully without X.* This is the signal that orders the punch list against CRE's top-down drive.
4. **Taste-anchor drift** — an entry pulling away from `_DEV.md`'s tone targets / molten core. Surface the drift; never rewrite it.

**Object/origins beat physical description.** Origins and properties of weight-bearing objects/places are *generative* (where a thing came from tends to tell you where it must appear and what it pays off) → they rank as descent-blockers. Pure physical description of characters is **drafting texture** (it feeds the perceptual-envelope / Transcoder stage, not the structural one) → it ranks **deferrable** unless an entry explicitly leans on a look.

---

## Steps
1. **Vault sentinel (`^obs-004`).** Read `_DIRECTIVES.md`; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch → halt, ask which folder is the vault. (Project-agnostic: also confirm the target project's `DEV/_DEV_MAP.md` exists; if absent, this project has no DEV tree — say so and stop.)
2. **Read the DEV tree** (Inputs above), read-only. Note the profile from `_DEV_MAP.md` so a legitimately-absent rung (short = no `sequences/`) is not flagged as a gap.
3. **Detect gaps.** Walk every entry: harvest dangling wikilinks, empty buckets, empty `project.md` **Shape**, empty descent layers, and each `_DEV.md` **Open question** still open. Cross-reference the `_LEDGER.md` for any banked-material collision touching a gap. **Detection is referenced-only** — it can only see what the tree already names (dangling links + empty buckets). A load-bearing piece that exists solely in CRE's head and has never been captured or linked is **invisible** to this scan; that is a structural blind spot, reported every run (Standing rules), never silently absent.
3b. **Resolve-before-present (`^obs-188`, CRE-directed 2026-07-15).** Before any detected flag reaches the punch list, **research it against the tree** — registry entries, `_audit/` rulings floors, `DECISIONS/`, the ruled-terms table. A flag the tree decisively answers is **not a gap**: report it under a separate "RESOLVED AGAINST THE TREE — confirm" line (sourced, one tap), never as a blocker, and note the stale flag for a safe-ops sync. Only tree-silent questions rank as gaps. *(Source instance: the Nameless/Last Mountain "slip" presented as a start-gate blocker while both entries sat complete in the registry.)*
4. **Score each gap** against the four-signal rubric. Record which signals fired (that is the *why* shown to CRE).
5. **Triage by descent-readiness.** Sort each gap into one of three tiers (below), ordered by CRE's current top-down position (what's he about to descend into — sequence? scene?). Within BLOCKERS, mark each gap **[start-gate]** (blocks the *opening* of the next descent — you can't begin the outline without it) or **[late-beat]** (blocks a specific *later* beat, not the start). The descent verdict's "gated by" count includes **start-gate blockers only**, so the headline number always matches the start-gate set; late-beat blockers are surfaced but excluded from the gate (a late-beat carrier like a climax object blocks a beat the descent reaches, not the descent's beginning).
5b. **Triage the parked forks (the dev-reconcile handoff, added 2026-07-15).** Read the project's parked `DECISIONS/` entries and classify each by its `parked-until` wake convention: **`decision-helper (ripe)`** → lead the punch list with the literal call (*"run the decision helper on dec-NNN"*); **`CRE-articulation`** → surface as an articulation ask (CRE names branches; not measurable yet); **`milestone: <name>`** → report as sleeping under its named milestone, **never wake it early.** A ripe fork adjacent to a start-gate blocker outranks everything — it is a decision already prepared, waiting only to be run. (Same guard as ever: the skill names the fork, never invents its branches.)
6. **Present the punch list in chat** (Output format below). Lead with the one-line descent-readiness verdict, follow it immediately with the **blind-spot caveat line**, then the tiers. **Never propose the content of any gap.**
7. **(Optional) write a dated report** to `SYSTEM/reports/dev-readiness-<project>-<date>.md` *only if CRE asks* — the default is chat-only, so the `DEV/` folder and CRE's eyes stay clean. The report is a snapshot, never canon, and writes nothing into `DEV/`.

---

## Output format
```
DEV-READINESS — <PROJECT> · <date>
Descent verdict: <ready / not-ready> to drop to <sequence|scene> level — gated by: <the START-GATE blockers only, 1–3 items>
Blind spot: this audit only sees what the tree already references — pieces you've discussed but not yet captured won't appear here. Run dev-capture to enter them before they can rank.

RIPE FORKS (decisions prepared and waiting — run these)
- dec-NNN <one-line fork> — "run the decision helper on dec-NNN"
- dec-NNN <one-line fork> — awaits your candidate branches (articulation ask)
(sleeping: dec-NNN under <milestone> — not woken)

BLOCKERS (flesh out before the descent)
- [start-gate] <gap> — signals: <which fired> · adjacent open question: <id/none> · blocks the OPENING of the descent: <one line>
- [late-beat] <gap> — signals: <…> · blocks a specific later beat, not the outline's start: <one line>

LOAD-BEARING (high value; do soon)
- <gap> — signals: <…> · <one line>

DEFERRABLE (drafting texture; safe to wait)
- <gap> — <one line>
```
Each line names the gap and *why it ranks* — never a proposed answer. The verdict is the headline: it tells CRE in one line whether the next top-down talk will be productive yet, and the start-gate items gating it. The **blind-spot line is mandatory every run** — it stops "absent from the audit" being misread as "unimportant" for a piece that simply hasn't been captured yet.

---

## Standing rules
- **Surface, never fill (the organic-process guard).** The deliverable is *topics and questions*, not content. The moment this skill proposes what a gap *is*, it has contaminated the organic build it exists to protect. Hard line.
- **Read-only.** No write into `DEV/` ever. The only write at all is the optional, CRE-requested `SYSTEM/reports/` snapshot (never the vault root — `^obs-090` convention).
- **Preserve the kind.** A gap that is an open *question* is reported as a question, never re-cast as a missing fact to be settled.
- **Profile-aware.** Honor `_DEV_MAP.md`'s profile — never flag a legitimately-absent rung (short-story has no `sequences/`; the taste anchor *is* the macro read at that size) as a gap.
- **Process, not content, from `_POETICS.md`.** Read it for how CRE develops (e.g. uncued, segmented-by-inference); never treat a poetics noticing as a creative gap.
- **Referenced-only blind spot (report it, every run).** The audit sees only what the tree names — dangling links and empty buckets. A load-bearing piece that lives only in CRE's head, never captured or linked (e.g. an object discussed in chat but not yet in `items.md`), is **invisible** to the scan. Always emit the blind-spot caveat line; never let absence-from-the-audit read as unimportance. The remedy for an uncaptured piece is a `dev-capture` pass to enter it into the tree — *then* this skill can rank it. (First-run shakedown 2026-06-23: the Widowsbane — flagged in conversation as high-leverage — did not surface because nothing in the tree references it.)
- **Start-gate vs late-beat blockers.** Within BLOCKERS, separate gaps that block the *opening* of the next descent (the verdict's gate) from gaps that block a specific *later* beat. The verdict's "gated by" counts **start-gate blockers only** — so the headline count and the start-gate set always agree; a late-beat blocker (e.g. a climax-object carrier) is surfaced but excluded from the gate rather than inflating it.

---

## Pipeline relationship
Sits **upstream of the brief**, on the same `DEV/` layer as `dev-capture` — the two are a read/write pair. `dev-capture` fills the tree from talk; `dev-readiness` reads the tree and points CRE at what to talk about next, so the top-down descent (`_DEV` → `sequences/` → `scenes/` → eventually the per-chapter `brief.md`) is fed in the right order. Hands nothing forward automatically; CRE chooses what to develop, then runs `dev-capture` on the resulting talk.

<!-- status: draft — authored 2026-06-22. .skill packaging is desktop-gated (pack-skills.ps1 + Save-skill), same path as dev-capture (^obs-109). Register the trigger row in _SKILLS MAP via the file tools at the desktop. -->
