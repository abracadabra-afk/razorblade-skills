---
type: workflow
name: brainstorm
trigger: synthesize the brainstorm
aliases: [brainstorm this transcript, run the brainstorm, summarize the brainstorm, brainstorm synthesis]
inputs: [a dictation transcript of CRE talking a project/sequence/scene through with himself — raw or cleaned; pasted, pointed-at, or staged in DEV/_intake/]
outputs: [a CRE-ratified decision sheet in DEV/_intake/ (cue-headed, ready for dev-capture), the source transcript swept to DEV/_intake/_audit/, open questions preserved as questions]
lane: fiction
status: spec
last_updated: 2026-07-26
revision_note: v2 same day as v1 — input mode corrected per CRE. v1 was built chat-first (live back-and-forth with the AI); CRE's actual flow is a solo dictated talk-through presented for synthesis. Transcript-first now; live mode demoted to optional Mode B. Packs after 2–3 live runs.
---

# WORKFLOW: brainstorm

## When to use
CRE has **talked a piece of the story through with himself** at the mic — exploratory, messy, non-linear, full of musings, reversals, and discarded options — and hands over the transcript for **synthesis**: capture the ideas, pull out the decisions he made, summarize the major takeaways, surface anything that needs a ruling. The output is a distilled decision sheet he ratifies once, which then feeds dev-capture. Use on "synthesize the brainstorm," "brainstorm this transcript," "run the brainstorm."

**How it differs from dev-capture** (the seam that matters): dev-capture routes a transcript of **designed elements** — segments stated as story truth, filed as-is into the DEV tree. A brainstorm transcript is **upstream of design**: CRE argues with himself, tries an option and abandons it, decides something at minute 40 that contradicts minute 5. Routing that raw would file the debris alongside the decisions. Brainstorm is the distillation pass between the mic and the router — synthesis first, CRE's ratify, *then* commit.

It is **not**:
- dev-capture (that routes designed elements; this distills exploration *into* routable decisions);
- dictation-cleanup (no copy-edit output; the transcript is source material, not prose);
- the transcoder or any drafting instrument (never produces prose);
- decision-helper (it may *hand off* an articulated fork to it, never triage one itself).

**Route position (the simplified dictation route):** **brainstorm → commit (dev-capture) → speak (runway → dictate) → land.** The runway leg is under active template testing (`^backlog-runway-format-friction`) — this doc deliberately does not specify it.

## The governing principle — the organic-process guard
**CRE creates; the skill distills.** Everything in the sheet must trace to something CRE actually said. The extraction contract:

- **A decision is something he stated as a call** — "it's X," "she does Y," "I'm going with Z." Sustained musing is not a decision, however detailed.
- **The last position wins, with provenance.** When he reverses himself, the sheet carries the *final* position as the decision and notes the reversal in one line ("supersedes the earlier 'X' take") — never both as live, never the skill's pick of which was better.
- **Preserve the kind.** "Maybe she knows" stays a question. A stumbled line of dialogue is a target, flagged un-pressure-tested, never committed prose. Never resolve an ambiguity he left open — manufacturing a decision he didn't make is the cardinal sin here.
- **Taste is content.** "What I love about this / what interests me" statements are first-class captures, not exhaust.
- **Uncertain → Open questions, never Decisions.** When it's unclear whether he decided or mused, it goes down as a question. The gate exists so he can promote it with one word; a false decision costs far more than a demoted one.
- **Forbidden:** adding story content (plot, names, images, dialogue, worldbuilding), filling gaps, "completing" a thought he abandoned, writing prose of any kind.

## The exit artifact — the decision sheet
One file per transcript: `DEV/_intake/<YYYY-MM-DD> brainstorm - <topic>.md`. Frontmatter serialized per DIR-004 (`yaml.safe_dump`, parse-gated):

```yaml
type: brainstorm-sheet
project: <PROJECT>
topic: <topic>
date: <YYYY-MM-DD>
ratified: pending   # flips to yes at the gate
source_log: _audit/<YYYY-MM-DD>-brainstorm-<topic>.md
```

Body sections:

1. **Decisions** — each as a **cue-headed segment** using the project's `_DEV_MAP` cue table (`scene — …`, `sequence — …`, `character — …`, `lore — …`, `place — …`, `project level — …`). Deliberate: cue-headed segments hit dev-capture's deterministic layer (cue wins, always — no inference on ratified material). Compression in CRE's own vocabulary, ruled spellings from `_DEV_MAP`; supersession notes inline where he reversed himself.
2. **Takeaways** — the major through-lines of the session that aren't discrete filed decisions (3–7 lines, no padding).
3. **Open questions** — everything left open, preserved as questions; dialogue targets flagged as targets.
4. **Rulings needed** — forks he articulated but didn't close, each with *his* stated branches only. Candidates for decision-helper.

## The collapsed gate
CRE rules **once**, at the sheet. His approval pass (edit / strike / promote-a-question / confirm, one pass) flips `ratified: yes`. Downstream, **dev-capture treats a ratified sheet's Decisions as pre-ruled**: it routes them without re-asking, and re-gates **only** an actual collision — a `_LEDGER` conflict, a ruled-terms contradiction, banked-manuscript friction (DIR-011: the second gate fires when the tree disagrees, not by default). Open questions and Rulings-needed items route to `_intake` holds as usual — ratifying the sheet ratifies the *decisions*, not the questions.

## Getting the transcript in
Any of: paste it in chat; point the session at a file; or drop it through the normal dictation transport and run brainstorm against the staged copy. **No dedicated runner marker exists yet** — a spoken "brainstorm" lead-in currently routes nowhere special (a "dev note" head would send it to dev-capture's queue instead, which is the wrong instrument for exploratory talk). If live runs prove the flow, adding a `brainstorm` marker to [[WORKFLOWS/dictation-runner]] is the follow-up — tracked on `^backlog-pack-brainstorm`, not improvised here (runner-prompt drift is a known trap).

## Steps

### Step 1 — Sentinel + load (retrieve before you read)
Confirm the `^obs-004` sentinel. Identify the target project (named in the transcript head, or asked once); read its `DEV/_DEV_MAP.md` (cue table + ruled terms), `_DEV.md` (taste anchor), `_intake/_LEDGER.md`, and — targeted — the registry/scene/sequence entries the topic touches. DIR-011 applies to the whole pass: a question the tree already answers is resolved with provenance ("resolved against [[Entry]] — confirm"), never surfaced as an open flag.

### Step 2 — Read + extract
Walk the transcript in order under the extraction contract. Track: candidate decisions (with supersessions as later statements override earlier ones), taste statements, tensions with banked material (noted for the sheet, logged to `_LEDGER` if they collide with landed manuscript — silently, per the dev-layer discipline), forks opened, questions left open. Correct obvious STT garbles of *ruled terms* against the `_DEV_MAP` table (exact-alias only — never guess a name the table doesn't hold).

### Step 3 — Distill
Draft the decision sheet per the format above. Compression, not paraphrase-drift: his vocabulary, his terms. Anything uncertain lands in Open questions, never Decisions.

### Step 4 — Gate (the one ruling)
Present the sheet. CRE edits/strikes/promotes/confirms in one pass. Apply his edits verbatim, flip `ratified: yes`, parse-gate the frontmatter.

### Step 5 — Land + hand off
- Write the ratified sheet to `DEV/_intake/`.
- Sweep the source transcript to `DEV/_intake/_audit/<date>-brainstorm-<topic>.md` — the floor, per the transcript-floor convention; the sheet's `source_log` carries the pointer. If the transcript was staged in `_intake/`, remove the staged copy once swept (the floor is canonical; `_intake/` holds only unrouted material).
- Offer the next leg: run **"capture the dev"** now (same session) or leave the sheet queued. Either way dev-capture finds a cue-headed, pre-ruled sheet.
- If Rulings-needed items exist, offer decision-helper per item — never auto-run it.

### Step 6 — Log
DIR-003: vault-mutating session — append a `_CHANGELOG` entry (fiction lane), observations/backlog as warranted.

## Mode B — live back-and-forth (optional, attended)
CRE *may* instead brainstorm in conversation with the AI ("brainstorm with me"). Same contract, same sheet, same gate — the only differences: the AI's turn repertoire is restricted to **ask / mirror / retrieve / name-tension / offer-the-fork** (never pitching story content — a sparring mode would be an explicit CRE ruling, not drift), and the conversation log is what sweeps to the floor. This is the secondary mode; the transcript path above is the designed flow.

## Stop conditions
- No `DEV/` tree for the project → halt; run the DEV scaffold first.
- The transcript is designed-elements talk, not exploration (cue-headed, stated-as-truth throughout) → route to dev-capture directly; don't add a synthesis layer it doesn't need.
- Secret/credential in the transcript or a read file → DIR-001 (flag, never propagate; revoke first, log second).
- Zero decisions extracted → still a valid exit: a sheet of takeaways + open questions is useful; say so rather than manufacturing decisions.
- Mode B drifts into requests for generated story content → name the guard, offer the explicit-mode ruling, don't drift. Affective drift → DIR-015: name once, stop.

## Unattended posture
The **gate is attended, always** — a sheet is never ratified headless. An unattended run may do Steps 1–3 only (synthesis staged, `ratified: pending`) and defer the gate visibly (DIR-012 clause 4).

## Logging
On completion, append an entry to [[_CHANGELOG]] (fiction lane); file surprises to [[_OBSERVATIONS]]; follow-ups to [[_BACKLOG]].
