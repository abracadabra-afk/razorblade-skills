---
type: workflow
name: episode-runway
status: spec — run by hand/in chat; graduates to a packed skill after 2–3 live runs
triggers: ["workshop this episode", "run the episode gate", "build the episode runway", "gate this premise"]
lane: 5 (writing-ops) + 1 (fiction)
created: 2026-07-13
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

## Episode folder convention

```
WRITING/SHORTS/EPISODES/EP NN - <TITLE>/
├── premise.md      Pass-1 output — knot · constraint · topical peg · TOS band · tier routing
├── runway.md       Pass-2 output — the speaking outline CRE dictates from
├── draft.md        CRE's dictated prose (cleaned via dictation-cleanup; NEVER authored here)
└── production.md   Pass-3 output — title · thumbnail line · description + content advisories · tier · publish slot · Short-cut spec · series/playlist slot · paid author's-note flag
```

---

## Pass 1 — THE GATE (idea stage, *before* a word is drafted)

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

## Pass 2 — THE RUNWAY (the artifact CRE dictates from)

Structure only. **Zero prose.** Same discipline as `runway-builder`: each beat is a plain action line plus GOAL → BUT → THEREFORE. If a line could be read aloud in the finished story, it does not belong in the runway.

`runway.md` carries:

- **Flow conditions block** — POV, tense, the narrating voice, who's in the room, what the reader is allowed to know and when.
- **The anomaly-line slot** — the cold open is CRE's sentence. The runway holds `[ANOMALY LINE — CRE]` and states the **wrong fact** the line must land, flat, in sentence one. **The gate does not write the line.** It can restate the premise's own wrong fact back to CRE (his words, from `PREMISES.md`) as the thing the line must carry.
- **Logic beats** — the forensic spine, GOAL → BUT → THEREFORE, front to back.
- **The ear-first constraints, as flow conditions** (see below).
- **The turn** — the beat where the knot breaks or holds.
- **Word budget per movement** — so the 2,000–2,800 container is hit by dictating, not by cutting afterward. (At CRE's 5,000+/hr dictation pace, the runway *is* the container control — the budget lines carry the whole discipline.)

### The ear-first constraint block (the thing a normal workshop never checks)

The story is **narrated solo by its author**, with little to no dialogue. So the runway flags, up front:

- **Name collision** — characters whose names sound alike are indistinguishable to the ear. Flag before drafting, not in the booth.
- **Dialogue attribution** — with no character voices, a he-said/she-said ping-pong turns to mush aloud. Keep exchanges short, attributed, and rare. **Prefer reported speech to staged exchange.**
- **Breath** — sentences must be sayable in one breath, or built to break. A gorgeous 60-word sentence is a lung failure on mic.
- **Punctuation doing visual work** — em-dash cascades, parentheticals, italics-as-emphasis: the ear hears none of it. If a beat depends on how it *looks*, it dies in audio.
- **The reread problem** — a reader can go back a line. A listener cannot. Any beat that only lands on reread is a beat that doesn't land. Flag it.

---

## Pass 3 — THE CHECK (after CRE dictates)

Runs on `draft.md` **after** dictation (and after `dictation-cleanup`, which is word-preserving). Diagnostic only — **it flags, CRE fixes.**

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

- **Upstream:** [[WRITING/SHORTS/PREMISES]] (the feed) · [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]] (the constraints)
- **Sibling:** [[WORKFLOWS/runway-builder]] (chapters) — same architecture, novel-scale
- **Downstream:** [[WORKFLOWS/dictation-cleanup]] (word-preserving polish of the dictated draft)
- **Not this:** `workshop-chapter` (novel chapters, read-only) · `dictation-transcoder` (generative slate — **deliberately not in this route**; CRE's episode prose is dictated, cleaned, and published as his)
