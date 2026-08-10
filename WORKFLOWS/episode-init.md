---
type: workflow
name: episode-init
status: spec — run by hand/in chat; graduates to a packed skill after 2–3 live runs
triggers: ["build episode N", "init the episode", "scaffold the episode", "start a new episode", "episode builder"]
lane: 5 (writing-ops) + 1 (fiction)
created: 2026-07-23
---

# episode-init

The **Writing Is War episode builder** — takes a feeling, a candidate, or a premise line through the Pass-1 gate and scaffolds the episode folder (convention v2). The shorts sibling of [[WORKFLOWS/chapter-init]], with the gate folded in: one trigger takes an idea from "this interests me" to a gated, scaffolded folder ready for the sit-with-it period.

> **CRE-ruled position (2026-07-23):** the gate lives *here*, not in episode-runway. episode-runway keeps the runway carve (S4) and the Pass-3 check; this workflow owns conception → folder.

## Pipeline position — the episode route v2

```
S0  FEELING CAPTURE   CANDIDATES/<title>/triage.md · PREMISES.md · felt-source dictation
S1  GATE + SCAFFOLD   ← this workflow
S2  SIT               CRE's notes accumulate in notes.md — no tooling, just time
S3  SYNTHESIS         episode-feedback ("reconcile my notes")
S4  RUNWAY CARVE      episode-runway v2 Pass 2 — lightweight, post-synthesis
S5  DRAFTING ENGINE   mic → dictation-runner → dictation-cleanup → transcoder →
                      scene-intensity on the slate → expansion/compression (CRE) → land draft.md
S6  FINISH ARC (v3)   dev-edit (blind dev panel → informed walk → roadmap) → CRE's AUTHOR PASS →
                      panel-read (the pre-publication gate) → panel-response → line passes → record prep
S7  PRODUCTION        episode-runway Pass 3 — TOS re-check → routing re-call · Short cut · production.md
```

Ratified provenance for this order: transcoder ruled **in** the route (CRE, 2026-07-23 — "critical; it turns my telling the story to myself into prose"); scene-intensity sequential after the transcoder (built 2026-07-22, run live on EP 01's pass-2 slate); blind read moved **post-slate** so the one-shot cold reader is spent on prose, not on the raw telling (EP 01's blind read burned flags on STT garbles and cleaner artifacts the transcoder removes).

> **S0 + SIT amendment (2026-08-09, CRE-ruled — premise-forge design session).** S0 is now formalized by [[WORKFLOWS/premise-forge]] (attended, feeling-first premise developer → `CANDIDATES/<title>/triage.md`, pre-answering this workflow's Pass-1 gate — confirm, don't re-derive). And **the SIT is repositioned**: it lives **between rough draft and author pass** (the S5→S6 seam), not between gate and dictation. Bag → gate → runway → mic **same-day is sanctioned**; the sit happens on banked rough drafts, which the steady drafting cadence keeps supplied. The S2 row in the diagram above is superseded accordingly.

> **Route v3 amendment (2026-08-09, CRE-ruled — EP 01 post-mortem).** S6 restructured: [[WORKFLOWS/dev-edit]] (blind dev panel + informed flag-keyed walk) is the first instrument after the drafting engine, producing the roadmap for **CRE's author pass**; the reader panel ([[WORKFLOWS/panel-read]]) moves to the **pre-publication gate** and is never convened on pre-author-pass material. Governing category ruling: CONTENT flags (a beat does no new work) are cured only by the author pass; EXECUTION machinery (choreographer, line queues, panel-response) never runs on a section carrying an open CONTENT flag. Evidence: EP 01's video-2-escalation choreo session died whole with the sorority sequence; CRE's own author-flags D2b predated the panel's C1 by two days. Full provenance in dev-edit.md. `blind-read` stays available as a cheap single cold probe at CRE's call.

## When to use

CRE brings an episode idea in any form — a feeling he wants to explore, a `CANDIDATES/` triage, a `PREMISES.md` entry, a felt-source dictation — and wants it gated and stood up as a folder. Runs before the sit (S2). Do NOT use it to carve the runway (episode-runway), reconcile notes (episode-feedback), or repair an existing episode folder — like chapter-init, it only creates folders that don't exist.

## Inputs

- **The idea** — anything: a premise line, a fragment, a triage note, a dictation. If it's a `CANDIDATES/` entry, its `triage.md` pre-answers most of the gate; confirm rather than re-derive.
- **Episode number** — **CRE's scheduling call, always.** Candidates stay unnumbered until he assigns a slot. If N is not (highest existing episode + 1), surface and confirm.
- **Working title** — from CRE; never invent one.

## Steps

### Step 1 — Vault sentinel (`^obs-004`)
Verify `_DIRECTIVES.md` frontmatter (`type: ai-os-brain`, `file: directives`). Fail → halt.

### Step 2 — Gates (structural)
- Folder `EP NN - *` already exists → **halt**; never overwrite, never fill gaps in an existing episode.
- No number or title from CRE → ask; don't proceed on placeholders.

### Step 3 — THE GATE (Pass 1, moved here from episode-runway v1)

Run the four checks in order, per the canonical constraint set in [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]]:

**a. Premise integrity** — knot · scenario-challenges-knot · tensional constraint · **topical peg** (no peg, no title/thumbnail/algorithm surface — a premise without a peg is not ready).

**b. TOS band** — free-tier safe / age-restricted / never. Read the *intended* content against the line; Pass 3 re-checks the draft for drift.

**c. Tier routing** — FULL / SAFE-CUT / TEASE, ruled **now, at conception, never after drafting**. Recommendation with a one-line basis; **CRE rules.** The ~6–7 FULL + 1–2 TEASE monthly rhythm depends on this call happening here.

**d. Container** — two-band gate (strategy §3b): standard ~2,000–2,800 words ≈ 15–20 min, or route out at conception (two-parter / TEASE long-form / SHORTS proper).

**Callable sub-skills at the gate — never reimplemented:**
- A fork CRE has articulated (which spine, which setting, this reveal or that) → hand to **decision-helper** ("help me decide"); its ruling comes back as gate input with a `dec-NNN` pointer. (EP 01 precedent: dec-017's five at-the-mic forks.)
- A stall or shapeless feeling → hand to **work-through** ("help me work through"); executional lane only, DIR-015 governs.
- The gate itself never invents story options (organic-process guard) and never smooths a broken premise into shape — it names what's missing and hands it back.

**Gate verdict: GO / RESHAPE / NOT-AN-EPISODE.** CRE rules. Only GO proceeds to Step 4.

### Step 4 — Scaffold (convention v2)

```
WRITING/SHORTS/EPISODES/EP NN - <TITLE>/
├── premise.md        Pass-1 output — knot · constraint · peg · TOS band · tier · container verdict
├── notes.md          CRE's sit-with-it surface (seeded empty; his document — appended below a rule only, never interleaved)
├── runway.md         stub, status: awaiting synthesis (episode-runway v2 carves it at S4)
├── envelope.md       stub, status: derives at slate time (from the carved runway + rulings; transcoder v5.1 episode mode)
├── draft.md          status: scaffold — becomes the single editable source of truth once the ratified slate lands
├── production.md     stub (Pass-3 output — title · advisories · tier · Short-cut spec · publish slot)
├── dictation/        raw + cleaned tellings (the runner's outputs)
└── slate/            transcoder outputs (immutable audit trail)
```

Every file stamped `episode: EP NN - <TITLE>` + `last_updated: <today>` — no body ever copied from a sibling episode (the `^obs-005` template-copy trap, killed here the same way chapter-init kills it). Frontmatter serialized per DIR-004.

**What is deliberately NOT scaffolded** (vs the novel convention): `brief.md` (the premise is the brief at this scale) · `open-loops.md` / `continuity.md` / `_status.md` (a short carries no continuity debt — the reason divergence is a win) · `revisions/` (CRE's passes edit `draft.md` in place; the slate is the audit trail).

### Step 5 — Landing rules recorded in the scaffold

Three rules stamped into `draft.md`'s scaffold frontmatter so no future session re-derives them:
1. **The ratified slate lands as `draft.md`; from that moment `draft.md` is the only editable copy.**
2. **Landing retires the source transcript** (stub it in `dictation/` with a pointer) — closes the live-fork foot-gun filed off EP 01 (2026-07-22, `chad's notes.md` §E).
3. **The derived-artifact inventory includes rule and canon surfaces (added 2026-08-10, `^backlog-protected-span-write-gate` (iii) / `^obs-235` / DIR-010 inventory clause).** Any pass that supersedes draft text and stamps a "these derived artifacts are stale" note must enumerate **every** derived surface — not just the obvious outputs (`record-script.md`, `performance-notes.md`, `choreo/*`, `production.md`) but the **rules files derived from the same text**: the project `REFERENCE/protected-patterns.md` witnesses and any register-sourced per-episode rows. A rules file reads as authority rather than output, which is exactly why it gets omitted — EP 01's frontmatter flagged `record-script` + `performance-notes` as stale while the protected-patterns witnesses, stale from the same rewrite by the same cause, went unlisted. That omission class is the one this rule exists to kill.

### Step 6 — Log
- Vault `_CHANGELOG.md`: one session entry (gate verdict + scaffold).
- If the idea came from `CANDIDATES/`, stamp the triage note `status: promoted → EP NN` — the candidate is spent, not deleted.

## Stop conditions

Sentinel fails · folder exists · no number/title · gate verdict is RESHAPE or NOT-AN-EPISODE (nothing scaffolds on a non-GO) · CRE hasn't ruled tier.

## Guards

- **Never writes CRE's prose** — not the anomaly line, not a beat. Gate + structure only.
- **Never invents story options.** Forks go to decision-helper exactly as CRE articulated them.
- **Tier routing is CRE's ruling.** Recommend with a one-line basis; he rules.
- **Numbering is CRE's scheduling call.** Candidates are promoted, never auto-numbered.

## Relationship to the rest of the OS

- **Upstream:** [[WRITING/SHORTS/PREMISES]] · `WRITING/SHORTS/CANDIDATES/` (triage convention, 2026-07-22) · felt-source dictations via [[WORKFLOWS/dictation-runner]]
- **Downstream:** [[WORKFLOWS/episode-feedback]] (S3) → [[WORKFLOWS/episode-runway]] v2 (S4 carve + S7 Pass 3)
- **Callable:** [[WORKFLOWS/decision-helper]] · [[WORKFLOWS/work-through]]
- **Sibling:** [[WORKFLOWS/chapter-init]] (novel scale; keeps brief/continuity apparatus this deliberately drops)
- **Not this:** the runway carve · notes synthesis · the drafting engine · the finish arc

## Run log

*(none yet — first live run should be EP 02, off a ruled candidate or fresh feeling)*
