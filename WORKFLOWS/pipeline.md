---
type: workflow-reference
name: pipeline
purpose: The canonical description of how the fiction workflows chain — the pipeline-relationship canon carved out of _SKILLS MAP (2026-07-10 slim) so the boot payload stays lean. Load when doing fiction pipeline work.
lane: fiction + writing-ops (episode route added 2026-07-23)
status: active
last_updated: 2026-07-23
---

# The pipeline (how the fiction workflows chain)

> Carved verbatim from [[_SKILLS MAP]] on 2026-07-10 (the boot-cost slim, [[SYSTEM/reports/2026-07-10-os-audit-improvements]]). The pre-slim map is archived at `SYSTEM/history/_SKILLS MAP-2026-07-10-pre-slim.md`. This doc is the single home for the pipeline-relationship canon; the map holds only the trigger index.

## Pipeline relationship

dictation-preflight is the upstream prep (queued dictation → filled `envelope.md`, authoring the Transcoder's required input — the `^obs-005` fix). Transcoder is next (raw dictation + envelope → clean rough-draft slate, **generative**). spec-check is an **optional, selective diagnostic tier** between the slate and the register: Pass 1 (`blind-read` skill) runs cold in a clean room; the **developmental pass** (`blind-response` skill) then optionally revises the chapter from the blind read into `draft.md` (two-phase gated — CRE rules the triage and approves the fixes; Pass-1 findings + structure only, never line/voice); Passes 2–5 are spec-aware and run on the **working text** (`draft.md` if `status: dev-revised`, else the slate clean-draft) — either via the `spec-passes` runner (one isolated subagent per pass, recommended) or pasted by hand — and CRE reconciles the bins into `spec-check/<slate-run>/verdicts.md` — by hand or via the `reconcile` skill, which walks the judgment calls one at a time, enforces the first-UNDRAMATIZED hand-check, and finalizes the sheet to `status: ready` for `register-pass`. register-pass is the revision/execution stage out of the slate (newest slate `clean-draft.md` → revised passage + editorial note in `revisions/`, running the **project-specific** register at `REFERENCE/register.md` — the dedicated workflow the chapter `revisions/README` files previously called "TBD"). register-pass is **coupled to spec-check use-if-present**: when a ready `verdicts.md` exists for the slate run it runs *execute-only* (honors CRE's settled rulings, builds UNDRAMATIZED, never re-litigates); otherwise it runs *full* discover-and-revise. **promote-revision** closes the loop: because register-pass writes only into `revisions/` and never touches `draft.md`, promote-revision is the return trip that moves the newest revision back into the live `draft.md` (carrying `source_slate` + a new `source_revision`, `status: register-revised`) — keeping `draft.md` a mirror of the newest promoted revision. **canon-sync** runs when the chapter has *landed* (post-promote): it derives project state from the landed `draft.md` — `REFERENCE/story-so-far.md` + `REFERENCE/bible.md` + `REFERENCE/threads.md` (open reader-promises: planted → advanced → paid, with blind-read pickup harvested from the run's `pass-1-blind.md` — the `^obs-011` fix) (per-fact provenance `(CH<N> rev<M>)`, idempotent per chapter) and the chapter's `continuity.md` end-state sections (the previously unowned template — `^obs-010`); additions write, contradictions gate for CRE's ruling. The forward half of `^obs-011` is the per-chapter **`brief.md`** (intent: job, beats, setups, payoffs due, seal schedule) — written before dictation, graded against after Pass 1; spec material the blind read never loads. Its outputs feed the **next** chapter's dictation-preflight, which now resolves implicit POV/place/state from REFERENCE first and back-walks prior chapters only as fallback. dictation-cleanup is the protective copy-edit (slate or any prose → polished copy-edit, **non-destructive**). They chain on projects that have adopted the per-chapter folder convention; register-pass additionally requires a project register; on projects that haven't adopted the convention, only dictation-cleanup applies. See [[_OBSERVATIONS#^obs-003]] for the rationale.

## Conventions (referenced, not triggered)

- [[WORKFLOWS/chapter-weight]] — a one-field tag (`weight: load-bearing | standard | bridge` in `brief.md`, default `standard`) that scopes QA effort: load-bearing chapters get the full spec-check battery + full scene-intensity; bridge chapters get a lean pass (Pass 2 only or straight to the register); the register runs on all of them. **Depth scales, the quality bar never does.** Read by spec-check, scene-intensity, workshop-chapter; seeded by chapter-init. From the archive's scope-based-excellence salvage (`^obs-053`). **status: active** — built 2026-06-13.

## Three REFERENCE checks for the revision lane (per project, archive salvage `^obs-053`)

`register.md` = how to revise (authority) · `voice-spec.md` = the empirical voice fingerprint the prose should match (measured target) · `contamination-checklist.md` = the named AI failure modes to scan for at the generative steps (guard). voice-spec + contamination run as soft checks in register-pass Step 2.5 and the transcoder; both flag for CRE, neither overrides the register.

---

## The episode route (Writing Is War shorts) — v2, compiled 2026-07-23

> The shorts sibling of the chapter pipeline above, compiled from the EP 01 DOOMSCROLLER live run. Canon per stage lives in [[WORKFLOWS/episode-init]] / [[WORKFLOWS/episode-feedback]] / [[WORKFLOWS/episode-runway]]; this table is the **what-do-I-say-and-when** reference. Register: `WRITING/SHORTS/REFERENCE/register.md`. What the route deliberately drops from the novel lane: brief/envelope-preflight, canon-sync, storyline-sync, promote-revision, reconcile — a short carries no continuity debt, which is also why **divergence from the runway is a win and nothing grades the draft against it.**

| Stage | You say | What runs | What you get back |
|---|---|---|---|
| **S0 — feeling capture** | *(no trigger — dictate the feeling, or drop prose/ideas)* | `dictation-runner` files it; candidates land in `WRITING/SHORTS/CANDIDATES/<title>/triage.md`; premise lines in `PREMISES.md` | A felt-source transcript or a triaged candidate |
| **S1 — gate + scaffold** | **"build episode N"** / "episode builder" | `episode-init` — the Pass-1 gate (knot·peg·TOS·tier·container) + folder scaffold. At the gate it can hand a fork to **"help me decide"** (decision-helper) or a stall to **"help me work through"** (work-through) | `EP NN` folder with gated `premise.md`; GO / RESHAPE / NOT-AN-EPISODE |
| **S2 — sit** | *(nothing — time)* | You, in `notes.md` | Your notes, untouched by anything |
| **S3 — synthesis** | **"reconcile my notes"** / "sharpen the episode" | `episode-feedback` — two-phase gated; collisions with your own gate rulings surfaced, never silently folded | Sharpened `premise.md` + rulings block |
| **S4 — runway carve** | **"build the episode runway"** | `episode-runway` Pass 2 — the lightweight carve (one-line movements + word budgets + your banked opener) | Portable `runway.md` you dictate from |
| **S5 — drafting engine** | mic → drop the audio; then **"clean up this dictation"** → **"slate this dictation"** → **"score scene intensity"** | runner → `dictation-cleanup` (the telling, word-preserving) → `dictation-transcoder` v5.1 episode mode (telling → close-third prose) → `scene-intensity` on the slate | Slate + intensity contour; you rule expansion/compression; ratified slate **lands as `draft.md`** (telling retires to `dictation/` — no live fork) |
| **S6 — finish arc** | **"blind read"** (once, only ever on prose) → rule its flags → **"run the register"** → your passes | `blind-read` clean-room → CRE-ruled fixes → register pass against the WIW register → your read-aloud/edit passes | Revision in `revisions/` + editorial note; **you** land it into `draft.md` |
| **S7 — production** | "run Pass 3" / "production check" | `episode-runway` Pass 3 — cold-open test, ear read, container, **TOS re-check → routing re-call**, Short-cut spec | `production.md` — title, advisories, tier, publish slot, Short cut |

**Iron rules that ride the whole route:** the AI never writes your prose (anomaly line, beats, expansion — all yours) · tier/TOS/container move by your ruling, never by edit · the blind read is one-shot per story — spend it after the transcoder · `draft.md` is the sole editable copy once a slate lands · every pass reconciles against the draft, never the runway.
