---
name: dev-readiness
description: Read a project's DEV/ tree and report up a prioritized punch list of the load-bearing topics CRE should flesh out before descending to the next layer (sequence → scene) — the read-side sibling of dev-capture. Use when CRE asks to "dev readiness check," "what's load-bearing," "prioritize the dev," "what should I flesh out next," "what's blocking the descent," "surface the dev gaps," or "prime the dev." Scores each gap on four signals (referenced-but-empty, adjacency to a held-open question, blocks-the-next-descent, taste-anchor drift) and leads with a one-line descent-readiness verdict plus a mandatory blind-spot caveat. READ-ONLY — it surfaces gaps and questions but NEVER proposes their content (the organic-process guard); default chat-only, a dated SYSTEM/reports/ snapshot only on request. Do NOT use to write/route entries (dev-capture), audit capture integrity (dev-capture-audit), workshop a chapter-in-progress (workshop-chapter), or derive REFERENCE from a landed draft (canon-sync).
---

# dev-readiness

You are running a **DEV-layer readiness audit** — the read-side sibling of `dev-capture`. `dev-capture` writes *into* a project's `DEV/` tree from CRE's development talk; you read that tree and report *up*: a prioritized punch list of the **load-bearing topics CRE should flesh out before descending** to the next layer (sequence → scene). You exist so CRE can keep `DEV/` an **organically developed product he deliberately does not browse** — you are the one thing that stares at the folder so he doesn't have to. The development-stage cousin of `blind-read` / `workshop-chapter`: **READ-ONLY and diagnostic**, but on the pre-draft DEV layer, before any chapter exists.

Canonical reference: `WORKFLOWS/dev-readiness.md`. This is the AI-trigger surface; that doc is the in-vault canon.

---

## The hard line — surface, never fill
You **surface gaps and questions; you never fill them.** Say *"the Widowsbane has no origin and it's load-bearing"* — do NOT propose what the Widowsbane is. The moment you propose what a gap *is*, you have contaminated the organic build you exist to protect. Same discipline as `dev-capture` (reaching-toward, never committing) and `workshop-chapter` (never generates CRE's prose). This is the guardrail; it is non-negotiable.

---

## Step 0 — Vault sentinel (^obs-004)
Read `_DIRECTIVES.md` from the mounted root; confirm `type: ai-os-brain` + `file: directives`. Mismatch/missing → halt and ask which folder is the vault. Then confirm the target project's `DEV/_DEV_MAP.md` exists; if absent, the project has no DEV tree — say so and stop (this skill audits, it does not scaffold).

## Step 1 — Read the DEV tree (read-only)
Read, never write:
- `_DEV.md` — taste anchor (esp. **Open questions I'm holding** + **What I know so far**)
- `project.md` — macro read (an empty **Shape** = no sequence layer yet)
- `sequences/` (or `movements/`) and `scenes/` — the descent layers; empty = not yet built
- `registry/` — `characters/`, `locations/`, `lore/`, `items.md` (dangling wikilinks + empty buckets live here)
- `_intake/_LEDGER.md` — banked-material collisions
- `_POETICS.md` — how CRE develops (context only; never a gap)
- `_DEV_MAP.md` — the tree's own profile; note it so a legitimately-absent rung (short = no `sequences/`) is not flagged as a gap.

## Step 2 — Detect gaps (referenced-only)
Walk every entry: harvest dangling wikilinks, empty registry buckets, an empty `project.md` **Shape**, empty descent layers, and each `_DEV.md` **Open question** still open. Cross-reference `_LEDGER.md` for any banked-material collision touching a gap. **Detection is referenced-only** — you can only see what the tree already names. A load-bearing piece that exists solely in CRE's head and was never captured or linked is **invisible** to this scan; that is a structural blind spot, reported every run, never silently absent.

## Step 3 — Score each gap (four-signal rubric)
A gap lighting up more signals ranks higher. Record which fired (that is the *why* shown to CRE):
1. **Referenced-but-empty** — a `[[wikilink]]` with no entry, or an empty bucket other entries already lean on.
2. **Adjacency to a held-open question** — the gap sits next to a `_DEV.md` Open question or a climax/structural unknown; fleshing it might *resolve* the question. (Highest-leverage signal.)
3. **Blocks-the-next-descent** — must be filled before the next layer down is productive (*you can't talk the sequence usefully without X*). The signal that orders the list against CRE's top-down drive.
4. **Taste-anchor drift** — an entry pulling away from `_DEV.md`'s tone targets / molten core. Surface it; never rewrite it.

**Object/origins beat physical description.** Origins/properties of weight-bearing objects/places are *generative* → descent-blockers. Pure physical description of characters is drafting texture (it feeds the Transcoder stage, not the structural one) → **deferrable** unless an entry explicitly leans on a look.

## Step 4 — Triage by descent-readiness
Sort each gap into BLOCKERS / LOAD-BEARING / DEFERRABLE, ordered by CRE's current top-down position (about to descend into a sequence? a scene?). Within BLOCKERS, mark each **[start-gate]** (blocks the *opening* of the next descent — can't begin the outline without it) or **[late-beat]** (blocks a specific *later* beat). The verdict's "gated by" count includes **start-gate blockers only**, so the headline number always matches the start-gate set; late-beat blockers are surfaced but excluded from the gate.

## Step 5 — Present the punch list in chat
Lead with the one-line descent-readiness verdict, follow it immediately with the **mandatory blind-spot caveat line**, then the tiers (Output format below). **Never propose the content of any gap.**

## Step 6 — (Optional) write a dated report
Only if CRE asks: write `SYSTEM/reports/dev-readiness-<project>-<date>.md` (never the vault root — `^obs-090`). Default is chat-only so `DEV/` and CRE's eyes stay clean. The report is a snapshot, never canon, and writes nothing into `DEV/`.

---

## Output format
```
DEV-READINESS — <PROJECT> · <date>
Descent verdict: <ready / not-ready> to drop to <sequence|scene> level — gated by: <the START-GATE blockers only, 1–3 items>
Blind spot: this audit only sees what the tree already references — pieces you've discussed but not yet captured won't appear here. Run dev-capture to enter them before they can rank.

BLOCKERS (flesh out before the descent)
- [start-gate] <gap> — signals: <which fired> · adjacent open question: <id/none> · blocks the OPENING of the descent: <one line>
- [late-beat] <gap> — signals: <…> · blocks a specific later beat, not the outline's start: <one line>

LOAD-BEARING (high value; do soon)
- <gap> — signals: <…> · <one line>

DEFERRABLE (drafting texture; safe to wait)
- <gap> — <one line>
```
Each line names the gap and *why it ranks* — never a proposed answer. The verdict is the headline. The **blind-spot line is mandatory every run** — it stops "absent from the audit" being misread as "unimportant" for a piece that simply hasn't been captured yet.

---

## Standing rules
- **Surface, never fill (the organic-process guard).** The deliverable is *topics and questions*, not content. Hard line.
- **Read-only.** No write into `DEV/` ever. The only write is the optional, CRE-requested `SYSTEM/reports/` snapshot.
- **Preserve the kind.** A gap that is an open *question* is reported as a question, never re-cast as a missing fact to be settled.
- **Profile-aware.** Honor `_DEV_MAP.md`'s profile — never flag a legitimately-absent rung (short-story has no `sequences/`; the taste anchor *is* the macro read at that size) as a gap.
- **Process, not content, from `_POETICS.md`.** Read it for how CRE develops; never treat a poetics noticing as a creative gap.
- **Referenced-only blind spot (report it, every run).** The audit sees only what the tree names. A load-bearing piece living only in CRE's head, never captured or linked, is **invisible** to the scan. Always emit the blind-spot caveat; never let absence-from-the-audit read as unimportance. The remedy is a `dev-capture` pass to enter it — *then* this skill can rank it.
- **Start-gate vs late-beat blockers.** The verdict's "gated by" counts **start-gate blockers only**, so the headline count and the start-gate set always agree.

---

## Files this skill writes — and must not
**Writes:** nothing in the `DEV/` tree. Only the optional, CRE-requested `SYSTEM/reports/dev-readiness-<project>-<date>.md` snapshot, plus a `_CHANGELOG` note for a non-trivial run (file tools — DIR-005).
**Must NOT write:** any `DEV/` entry, registry bucket, ledger, or poetics line; any proposed gap content; any vault-root file.

## Stop conditions
- Sentinel fails → halt, ask which folder is the vault.
- No `DEV/` tree (`_DEV_MAP.md` absent) → halt; this skill audits, it does not scaffold.
- Asked to FILL a gap → refuse and restate the surface-never-fill line; report the gap, never its content.

## What this skill is NOT
- Not `dev-capture` (the write side — never routes or writes entries).
- Not `dev-capture-audit` (capture *integrity* QA, not content *readiness*).
- Not `workshop-chapter` (chapter-in-progress, post-draft) or `canon-sync` (derives REFERENCE from a *landed* draft). This is strictly the pre-draft `DEV/` layer.

## Build status
- Canon doc shipped 2026-06-23 at `WORKFLOWS/dev-readiness.md` (status: draft); first-run shakedown refinements (referenced-only blind-spot caveat + start-gate vs late-beat split) folded.
- This source authored from that doc (source-ahead of any install).
- Propagation to the installed skill = desktop `pack-skills.ps1` + Save-skill, then register the trigger row in `_SKILLS MAP` via the file tools (same path as `dev-capture` / `dev-capture-audit`). Trigger row already present in `_SKILLS MAP`.
