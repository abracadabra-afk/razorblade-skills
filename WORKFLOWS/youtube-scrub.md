---
type: workflow
name: youtube-scrub
status: spec — run by hand/in chat; graduates to a packed skill after 2–3 live runs (DIR-009)
triggers: ["scrub for youtube", "run the youtube scrub", "youtube-safe cut", "scrub for the channel"]
inputs: [any dark prose CRE intends to narrate on YouTube — a landed WIW episode draft, a novel excerpt, or a pasted/standalone piece; plus intended title/thumbnail/description if drafted]
outputs: [a gated scrub map → a derived youtube cut (one-way), a clean metadata sheet, a visual-discipline checklist]
lane: 5 (writing-ops) + 1 (fiction)
scope: general-purpose — the flag engine is project-agnostic; WIW/shorts is the primary application, not the boundary
created: 2026-07-27
provenance: dec-023 (split-band ruling + the WIW penalty-inversion sharpening) + KNOWLEDGE/RESEARCH/2026-07-27 youtube-horror-narration-graphic-content-monetization
---

# youtube-scrub

The **YouTube discovery-cut pass.** Takes any dark prose CRE intends to **narrate on YouTube** and produces the **YouTube-safe cut** — a derived version scrubbed across YouTube's known enforcement flags — plus a clean metadata sheet and a visual-discipline checklist. The original stays the canonical/uncut; this is the discovery layer.

> **General-purpose engine.** The flag taxonomy is project-agnostic: it runs on a WIW episode, a narrated Witchwood/Godsrift excerpt, or a standalone piece. WIW/shorts is the primary consumer (and the only place with a folder convention + a metadata liturgy), but nothing in the core is WIW-specific.

> **Derived, one-way, gated — like the storyline mirror and the §F two-cut design.** It never edits the **source** prose (that is the uncut canon). It **proposes** softenings and CRE **authors** the final wording — the house rule holds: AI does not write CRE's prose, it proposes swaps and CRE rules. Two-phase, like `blind-response` / `reconcile` / `loop-clearer`.

## Why this exists

dec-023 ruled the split-band pattern: uncut → the paid/dark surface (Substack), a scrubbed discovery cut → YouTube. That cut is a **standing, repeatable need** — for every WIW episode and for any other dark prose CRE ever narrates on the channel — so it gets a defined pass instead of a per-piece scramble. The enforcement flags are known, narrow, and mechanical to *scan* for; what they can't be is *auto-decided* (the swaps touch voice), so the skill flags-and-proposes and CRE rules.

**The one hard target (dec-023 sharpening): stay out of the 18+ age-gate.** YouTube's job in CRE's model is *discovery, not revenue* (strategy §10), so **age-restriction is the only real hit** (autoplay off, weak recs, no signed-out/underage surfacing = kills discovery) and **demonetization is a near-non-cost** (a demonetized video still autoplays/recommends — reach survives). So Tier-A flags below are must-fix; Tier-B (profanity/metadata → demonetization) is cheap polish, not required for the cut to do its job.

Canonical strategy: [[BUSINESS/SUBSTACK/WRITINGISWAR - YOUTUBE CHANNEL STRATEGY]]. Evidence base (refresh when policy moves): [[KNOWLEDGE/RESEARCH/2026-07-27 youtube-horror-narration-graphic-content-monetization]].

## Position in the pipeline

- **WIW episode:** runs at **Pass 3 / production**, after the uncut `draft.md` has landed (`promote-revision` / `land`). Sibling to the episode's production notes.
- **Any other prose:** on demand, whenever CRE points it at a piece he intends to narrate.

It consumes finished prose; it never runs upstream of a landed draft and never feeds back into one.

## Inputs

- The **source prose** — a landed WIW episode `draft.md`, a novel excerpt, or a pasted/standalone piece.
- The intended **title** and any drafted **thumbnail/description** text, if they exist yet (for the metadata scan).

## Outputs

1. **Scrub map** (chat / gated) — every flagged instance, its tier, and a proposed in-voice softening *slot* for CRE to fill or rule.
2. **The derived cut** — the approved cut, written one-way, `derived: from <source>`. For a WIW episode → `youtube-cut.md` in the episode folder; for standalone prose → a sibling `<name> - youtube-cut.md` next to the source (or the outputs scratch if the source is a paste). The source is never touched.
3. **Metadata sheet** — clean title/thumbnail/description + an advisory line. WIW episodes use the liturgy content-advisory template ([[WRITING/SHORTS/REFERENCE/liturgy]]); other prose uses the same discipline without the fixed liturgy wording.
4. **Visual-discipline checklist** — the non-prose production reminders (the strongest age-gate lever is imagery, which no prose edit touches).

## The flag taxonomy (the core — project-agnostic)

Evidence-grounded in the briefing; ranked by what actually bites. **Thresholds are classifier-driven, opaque, and shift without notice** (`<<UNCERTAIN>>`) — so scan conservatively and prefer flagging a borderline instance over missing it.

### Tier A — age-gate risk (must-fix; these kill discovery)

**A1 — Named violent descriptors.** The literal words YouTube's violence policy names: **tortured, dismembered, decapitated**, and framing that is prolonged / zoomed / central. Policy puts *spoken* description in scope (EDSA: context must be in "images or audio"; TTS carries no exemption), so a graphic enough narration is an age-gate candidate on the words alone. *Action:* flag each; propose a softening that keeps the **beat** while dropping the named descriptor — a restrained register does the horror, not the gore word (this is why the swaps are low-cost when the gore isn't load-bearing).

**A2 — Sexual-violence terms.** rape / molest / sexual assault (the "SA" / "grape" / "corn" euphemism cluster exists because these move the systems). *Action:* flag + propose reframe.

**A3 — Suicide / self-harm terms.** suicide / kill yourself / self-harm (the "unalive" cluster). **The sharpest *spoken-word* tripwire in the niche — narrower and harder than gore** (a narrator can describe a graphic killing more freely than say the literal word "suicide"). *Action:* flag every instance + propose reframe. **This is the one to never miss** for any piece that touches self-harm.

**A4 — Visual discipline (non-prose).** The single strongest age-gate trigger is **on-screen imagery**, which no prose scrub touches. *Action:* emit a checklist — talking-head + atmospheric b-roll only, no gore visuals, no lurid thumbnail. If the cut keeps visuals non-graphic, the whole age-gate risk drops to the words.

**Trigger-word handling (A1–A3) — the gate.** For each flagged term the skill offers, and CRE rules, among: **(a) literary reframe** — write around the term, keep the restrained voice (the recommended default; the "unalive"/"SA" euphemism register clashes with a literary channel); **(b) euphemism** — adopt the niche cluster; **(c) audio bleep/mute** — keep the word in the written/canonical version, mask it in the spoken track. The skill never picks for him; it proposes the slot, CRE authors the line.

### Tier B — demonetization risk (should-fix; cheap, but reach survives it)

**B1 — Profanity placement.** Strong profanity in the **title, thumbnail, first ~7–15 seconds, or used throughout** is the pattern that demonetizes; "hell" / "damn" no longer count; bleeping/silencing is rewarded. *Action:* scan title + the opening ~15 s of narration + overall density; flag placement; propose bleep/trim/move.

**B2 — Metadata luridness.** Title / thumbnail text / tags / description are classifier inputs on their own — a gory thumbnail or a "psychotic murderer stalks a girl" description can flag an otherwise-clean video. *Action:* produce a clean, atmospheric metadata sheet; advisories go in the **description**, never the title.

### Tier C — whole-piece check

**C1 — Focal-point / context.** "Content where the focal point is on violence without context" is weaker than the same violence as a *beat* in a story. A narratively-framed piece normally passes this; *Action:* note it only if a piece reads as wall-to-wall cruelty with no frame.

## Steps

### Step 1 — Scan
Read the source prose. Walk it for A1–A3 (prose), then the title/opening/metadata for B1–B2, then the whole-piece C1 check. Build the **scrub map**: each instance with a quote, its flag tier, and a proposed softening slot. Compile the A4 visual checklist and the B2 metadata sheet in the same pass.

### Step 2 — Gate (CRE rules)
Present the scrub map. CRE rules each instance (accept the proposed reframe, supply his own wording, choose euphemism/bleep, or reject). **Nothing is written until he rules.** Tier-A instances are surfaced as must-fix; Tier-B as optional polish flagged as such.

### Step 3 — Write the cut
Apply CRE's ruled swaps into the derived cut file (`derived: from <source>`, one-way). Attach the metadata sheet and the visual checklist. The source prose is untouched.

## Stop conditions

- **No finished source prose** → stop; this runs on landed/finished text only.
- **CRE hasn't ruled the map** → never write the cut; the map defers to the gate (Needs-review), never auto-applied (DIR-012 — safe ops write, judgment defers).
- **A genuinely borderline piece** (heavy A1–A3 the reframes can't fully de-risk) → recommend the empirical **throwaway-channel upload** to confirm before the real publish (DIR-013 clause 2 — check ≥2 samples; enforcement is inconsistent, and a human reviewer can age-gate a high-traffic video the classifier passed). Most pieces stay below the line by design and skip this.

## Guards

- **Never edits the source prose.** The uncut is the canon; the cut is a derived, one-way artifact.
- **Proposes; CRE authors.** AI does not write CRE's prose — it proposes softenings and CRE rules the final wording (house rule; two-phase gate).
- **Sole hard target is the age-gate.** Tier B is cheap polish, not a requirement — demonetization is acceptable under the discovery-first strategy (dec-023).
- **Evidence-grounded and honest about opacity.** Cites the briefing; thresholds shift, so it flags conservatively and never claims certainty. When policy moves, refresh the briefing and this taxonomy.

## Logging

On completion, append an entry to [[_CHANGELOG]] (writing-ops/fiction). Packaging follows DIR-009: after 2–3 live runs, author `skills-src/youtube-scrub/`, desktop-pack, Save-skill; register in [[_SKILLS MAP]].
