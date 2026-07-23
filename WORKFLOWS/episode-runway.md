---
type: workflow
name: episode-runway
status: spec — run by hand/in chat; graduates to a packed skill after 2–3 live runs
triggers: ["workshop this episode", "run the episode gate", "build the episode runway", "gate this premise"]
lane: 5 (writing-ops) + 1 (fiction)
created: 2026-07-13
amended: 2026-07-23 — v2, CRE-ruled off the EP 01 live run. Pass 1 (the gate) moved to [[WORKFLOWS/episode-init]] at conception; Pass 2 repositioned post-synthesis and re-specced to the lightweight carve (design principle D, EP 01 chad's notes §D); transcoder + scene-intensity ruled INTO the route (overturning v1's exclusion); blind read moved post-slate. Folder convention v2 lives in episode-init.
---

# episode-runway

The **Writing Is War episode gate + dictation runway.** Takes a raw story idea, pressure-tests it against the five channel constraints, routes it to a tier, and hands back a **speaking outline CRE dictates from** — logic beats, never prose.

> **It is `runway-builder`'s short-form sibling.** Same architecture, same guard: it derives *structure*, not sensation. **It never writes CRE's prose, ever.** The gate reasons; CRE dictates. That is not a promise the skill makes — it is the shape of the artifact it produces.

## Why this exists

A normal short-story workshop holds craft. This holds five things a craft workshop doesn't, and that CRE should not have to carry in working memory while an idea is still forming:

1. **Cold open** — the Anomaly Line (strategy §9b)
2. **Ear-first** — the story is *narrated solo*, with little to no dialogue
3. **YouTube TOS band** — free-tier safe vs. age-restricted (age restriction kills reach + monetization)
4. **Tier routing** — full episode · YouTube-safe cut · paywall-only tease
5. **Container** — 2,000–2,800 words ≈ 15–20 min at ~130–140 wpm (two-band rule, re-ruled 2026-07-15 — strategy §3b; 4,000+ routes out at conception)

Canonical strategy: [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]]. Premise source: [[WRITING/SHORTS/PREMISES]].

## Episode folder convention — v2 (moved)

**The convention is now owned by [[WORKFLOWS/episode-init]]** (convention v2: adds `notes.md`, `envelope.md`, `dictation/`, `slate/` — the transcoder-route surfaces EP 01 grew organically). This doc's passes write into that folder; they no longer define it.

## Pipeline position — the episode route v2

```
S0 feeling capture → S1 episode-init (gate + scaffold) → S2 sit (notes.md) →
S3 episode-feedback → S4 RUNWAY CARVE (this doc, Pass 2) →
S5 drafting engine: mic → runner → cleanup → transcoder → scene-intensity → land draft.md →
S6 finish arc: blind read → dev fixes → register pass → CRE's passes →
S7 PASS 3 (this doc) → production.md
```

---

## Pass 1 — THE GATE *(moved to episode-init, v2)*

> **v2 (2026-07-23):** the gate now runs inside [[WORKFLOWS/episode-init]] at conception — one trigger takes an idea from feeling to gated, scaffolded folder. **The tables below remain the canonical constraint reference** the builder executes; they are kept here, not duplicated there.

**Input:** CRE talks the idea. Anything — a premise line, a fragment, an image, a `PREMISES.md` entry.

**The gate asks, in order:**

**a. Premise integrity.** Does it carry all three of the `PREMISES.md` requirements?
- a character **knot** (the flaw the story will press on)
- a scenario that **directly challenges** that knot
- a **tensional constraint** (the clock, the closing door)
- and the field usually left blank: the **topical contemporary human experience** — *this is the discovery peg.* No peg, no title, no thumbnail, no algorithm surface. **A premise without a peg is not ready.**

**b. TOS band.** Read the intended content against the line:
- **Free-tier safe** — implied/dramatized violence, psychological horror, dread, aftermath (Jackson/King register)
- **Age-restricted** — lingering gore, graphic torture, detailed brutal deaths → *kills reach and monetization*
- **Never** — shock for its own sake, real violence, explicit sexual content, hate/self-harm

**c. TIER ROUTING — the decision this whole gate exists to force.** Made **now**, at conception, never after drafting:

| Route | When | What gets made |
|---|---|---|
| **FULL** | The story sits inside the free-tier band as conceived | One story, one record, three platforms. The default. |
| **SAFE-CUT** | It crosses the line, but a YouTube version exists **that doesn't gut it** | The uncut version is the Substack paid post; the safe cut is the video. **The gate must state honestly whether the cut guts the story — if it does, this is not a SAFE-CUT, it's a TEASE.** |
| **TEASE** | It crosses the line and cannot be cut without ruining it | Paywall-only. The video that week is an essay/announce: *"the story for this one isn't YouTube-friendly — it's on the Substack."* Trains the audience that Substack = the unfiltered work. |

> **The rhythm this protects:** ~6–7 FULL + 1–2 TEASE per month. That rhythm is only executable if routing happens **before** drafting. Routing after the fact is how a schedule becomes a hope. It is also how the **paid tier gets deliberately fed** rather than fed by accident.

**d. Container — the two-band gate (re-ruled 2026-07-15, strategy §3b).** Does this idea fit the **standard band, ~2,000–2,800 words ≈ 15–20 min**? A premise that needs **4,000+** is not a weekly episode — say so at conception, and route it: two-parter, TEASE/paywall long-form, or SHORTS proper / Substack long-form. Like tier routing, this call is made **now**, never after drafting.

**Pass-1 output:** `premise.md` + a **GO / RESHAPE / NOT-AN-EPISODE** call. CRE rules. **The gate never smooths a premise into shape by writing it — it names what's missing and hands it back.**

---

## Pass 2 — THE RUNWAY CARVE (v2: runs at S4, *after* the sit + episode-feedback synthesis)

> **Timing re-ruled (v2):** v1 built the runway immediately after the gate; EP 01 proved that's too early — CRE's thinking kept developing through the sit and three feedback runs, and the heavy runway had to be carved down to speaking shape afterward. v2 builds it **once, late, lightweight**, from the settled premise.

**Format: the carve (design principle D — EP 01 `chad's notes.md` §D, CRE-ruled 2026-07-21).** The runway is a **flow kickstarter, not a spec**:

- **One-line summary** of the story at the top (the settled spine, from the amended premise).
- **Movements, not beat trees** — `m1…mN`, each **one memorizable sentence** + a word budget `(~450)`. Portable: CRE must be able to read a beat on a walk and work it in his head. GOAL → BUT → THEREFORE is derivation discipline, not shipped format — if it can't collapse into the one sentence, the movement isn't settled yet.
- **Word budget per movement** — the 2,000–2,800 container is hit by dictating, not by cutting afterward. At CRE's 5,000+/hr pace, the budget lines carry the whole container discipline.
- **The opener slot** — the anomaly line is CRE's sentence; the runway banks his candidate verbatim if one exists (`Opener you banked: "…"`), else holds `[ANOMALY LINE — CRE]` + the wrong fact it must land.
- **Ear-first flags** (block below) — carried as flags on the relevant movements, not as a wall of instructions. Embedded instruction is implicit distrust and costs flow.
- **Zero prose, still.** If a line could be read aloud in the finished story, it does not belong in the runway.

**The runway is spent the moment dictation starts.** Divergence is a win; **nothing downstream may grade the draft against the runway** — every later pass reconciles against the draft. The one thing that should survive divergence is the *feeling*, and CRE notices that at the mic, not a pass.

### The ear-first constraint block (the thing a normal workshop never checks)

The story is **narrated solo by its author**, with little to no dialogue. So the runway flags, up front:

- **Name collision** — characters whose names sound alike are indistinguishable to the ear. Flag before drafting, not in the booth.
- **Dialogue attribution** — with no character voices, a he-said/she-said ping-pong turns to mush aloud. Keep exchanges short, attributed, and rare. **Prefer reported speech to staged exchange.**
- **Breath** — sentences must be sayable in one breath, or built to break. A gorgeous 60-word sentence is a lung failure on mic.
- **Punctuation doing visual work** — em-dash cascades, parentheticals, italics-as-emphasis: the ear hears none of it. If a beat depends on how it *looks*, it dies in audio.
- **The reread problem** — a reader can go back a line. A listener cannot. Any beat that only lands on reread is a beat that doesn't land. Flag it.

---

## Pass 3 — THE CHECK (v2: runs at S7, after the finish arc)

Runs on the **finished** `draft.md` — after the drafting engine (mic → runner → cleanup → **transcoder** → **scene-intensity** → expansion/compression → land) and the finish arc (blind read → dev fixes → register pass → CRE's passes). Diagnostic only — **it flags, CRE fixes.** First live run owed: EP 01 (`^backlog-ep01-tos-rerule` is exactly this pass's item 5).

1. **Cold open test** — is sentence one **both flat and wrong**? Flat-but-not-wrong = setting. Wrong-but-not-flat = the narrator is doing the reader's work (register violation).
2. **The never-open-with list** — waking up · weather · a room · name-and-job · backstory.
3. **Ear read** — the constraint block above, checked against the actual prose.
4. **Container** — word count vs. 2,000–2,800; runtime at ~130–140 wpm. A draft that landed 4,000+ triggers a **routing re-call** (two-parter / TEASE / route out), not a trim-to-fit.
5. **TOS re-check** — the draft can drift past the band the gate cleared. Re-read it. If it drifted, the routing call gets re-made, not ignored.
6. **Short cut point** — identify which 30–45 sec stands alone as the anomaly Short (strategy §3c.1): usually the anomaly line + first beat, hard cut mid-fall, loop-friendly. **Diagnostic only — the pass proposes the cut point with a one-line basis; the cut is CRE's call.** The Short must not pre-spend the turn.

**Pass-3 output:** `production.md` — title, thumbnail line, description + **content advisories** (they live in the description, never spoken aloud — reading them out spoils the story and pays a retention cost at the worst possible moment), tier, publish slot, **Short-cut spec** (in/out points + the wrong fact the Short carries), **series/playlist slot** (which playlist + end-screen target, strategy §3c.2), and the **paid author's-note flag** (Substack post carries the below-the-fold note per §3c.4 — the note itself is CRE's, never drafted here).

---

## Guards

- **It never writes CRE's prose.** Not the anomaly line, not a beat, not a "here's how that sentence could go." Structure, constraints, and questions only. (Cross-cutting rule, `_SKILLS MAP`: *AI executes; CRE creates.*)
- **It never smooths a broken premise into a working one.** It names the gap and hands it back.
- **Tier routing is CRE's ruling.** The gate recommends with a one-line basis; CRE rules.
- **It is not a craft workshop.** It holds channel constraints, not craft. CRE's 30 years hold the craft.

## Relationship to the rest of the OS

- **Upstream:** [[WORKFLOWS/episode-init]] (S1 gate + scaffold; owns the folder convention) → the sit → [[WORKFLOWS/episode-feedback]] (S3 synthesis)
- **Constraints canon:** [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]]
- **Sibling:** [[WORKFLOWS/runway-builder]] (chapters) — same derivation discipline, novel-scale; note the episode carve is deliberately lighter (no continuity debt)
- **Downstream (the drafting engine, sequential):** [[WORKFLOWS/dictation-runner]] → [[WORKFLOWS/dictation-cleanup]] (word-preserving; the "telling" preserved) → [[WORKFLOWS/transcoder]] (**ruled INTO the route, CRE 2026-07-23** — "critical; it turns my telling the story to myself into prose"; v5.1 episode mode, envelope derives from the carved runway at slate time) → `scene-intensity` on the slate (expansion/compression contour; re-runnable, so it precedes the one-shot blind read) → land `draft.md` (single editable copy; landing retires the source transcript)
- **Finish arc (post-slate):** `blind-read` (one-shot, spent on prose) → dev fixes (CRE-ruled) → register pass against `WRITING/SHORTS/REFERENCE/register.md` (v1 built 2026-07-23; CRE-ratify pending, `^backlog-wiw-register`) → CRE's passes → back here for Pass 3
- **Not this:** `workshop-chapter` (novel chapters, read-only) · `canon-sync`/`storyline-sync`/`promote-revision`/`reconcile` (novel apparatus a short doesn't carry)
