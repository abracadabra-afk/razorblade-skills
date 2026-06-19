---
type: workflow
name: loop-clearer
trigger: clear the open loops
aliases: [resolve the loops, work the open loops, clear the loops, clear chapter N's loops, run the loop clearer]
inputs: [the chapter's open-loops.md (unresolved entries), the chapter's draft.md (the prose to revise), the project voice spec at REFERENCE/voice-spec.md (optional), the project register at REFERENCE/register.md (optional), KNOWLEDGE/VOICE SAMPLES + KNOWLEDGE/STYLE (voice reference)]
outputs: [a loop-clear revision in revisions/ carrying the surgical fixes + marked demo blocks for the bigger rewrites, the chapter's open-loops.md with ruled entries moved to Resolved / marked in-progress]
lane: fiction
status: active
last_updated: 2026-06-19
scope: Projects using the per-chapter folder convention (see [[_SKILLS MAP#Fiction]]) that keep an open-loops.md populated by the Transcoder. First adopter — Witchwood.
pipeline_position: downstream of [[WORKFLOWS/transcoder]] (which POPULATES open-loops.md); upstream of [[WORKFLOWS/register-pass]]. Automates the open-loops.md note's own instruction ("Resolve here, then patch draft.md") into a gated, in-voice revision. Its loop-clear revision is landed by [[WORKFLOWS/promote-revision]].
---

# WORKFLOW: Loop Clearer

> Reads a chapter's **open-loops.md** (the pending author calls the Transcoder handed back instead of output), proposes a fix for each **in the project's voice**, gates every one on CRE's ruling, then writes a **loop-clear revision** into `revisions/` — surgical fixes committed in CRE's chosen wording, bigger rewrites left as marked demonstration blocks for CRE to rewrite in place.

## When to use

When a chapter has unresolved entries in `open-loops.md` and CRE wants them worked into the draft. Trigger phrases: "clear the open loops," "resolve the loops," "work the open loops," "clear chapter N's loops." Runs **after** [[WORKFLOWS/transcoder]] (which populates the loops) and **before** [[WORKFLOWS/register-pass]] (the line/voice pass on the cleared draft).

Do NOT use it to run the register (that is [[WORKFLOWS/register-pass]]), to respond to a blind read (that is the `blind-response` developmental pass — it works Pass-1 findings, not open-loops entries), or to slate dictation (that is [[WORKFLOWS/transcoder]]).

## Key principle — AI proposes in voice; CRE rules; AI never writes CRE's fiction

This skill resolves author *calls*, so CRE is always the decider. AI's job is to surface each loop with the span it touches, propose a fix that matches the project's measured voice, and — only after every loop is ruled — assemble the revision. The cross-cutting rule holds at the line: **never long-form-generate CRE's fiction.** That is why the two tiers are handled differently — small line-adds AI may phrase (CRE picks among options); bigger rewrites AI only *demonstrates*, and CRE writes the real prose.

## The two tiers (they fall out of open-loops.md's own sections)

| open-loops.md section | Tier | What it is | How it's handled |
|---|---|---|---|
| **Register-repair ambiguity** | SURGICAL | The Transcoder gave two carriers (Reading A / Reading B); CRE picks. | Present the source span + both carriers + up to 2 more in-voice phrasings. CRE picks or refines. Committed verbatim in CRE's choice. |
| **Image-doubling** | SURGICAL | The same image appears twice; keep the stronger, drop the other. | Present both instances, recommend the stronger with a one-line reason. CRE picks which to keep. The drop is a clean deletion. |
| **Left-for-later** | STRUCTURAL | Load-bearing named emotions the Transcoder did not dramatize — a real rewrite, not a line swap. | Present the beat, why it's load-bearing, and ONE *demonstration* of the fix (the move, not final prose). Lands as a marked demo block; CRE rewrites in place. |

A SURGICAL case the skill judges too big for a line swap is promoted to STRUCTURAL (demo, not authored). When in doubt, demonstrate — don't author.

## Inputs

- **open-loops.md** — the chapter's, read for every entry whose `Status` is not `resolved`. The section a loop sits under sets its default tier (table above). If there are no unresolved entries → halt (nothing to clear).
- **draft.md** — the chapter's current assembled draft; the prose each loop's span lives in and the base the revision is built from.
- **voice-spec.md (optional)** — `<project>/REFERENCE/voice-spec.md`, the empirical voice fingerprint. Anchor surgical phrasings to its bands; run it as a soft drift CHECK on proposed lines (flag, never gate). If absent, skip the check and say so.
- **register.md (optional)** — `<project>/REFERENCE/register.md`. Read for the project's tonal rules so proposals don't fight the register. Not an authority here (the register's own pass runs later); a reference.
- **VOICE SAMPLES / STYLE** — [[KNOWLEDGE/VOICE SAMPLES]] + [[KNOWLEDGE/STYLE]] as the voice reference for phrasing options. Match voice; never invent it.

## Outputs

| Artifact | Destination |
|---|---|
| Loop-clear revision (draft prose + surgical fixes applied + fenced demo blocks for structural loops) | `<chapter>/revisions/YYYY-MM-DD-loops-rev<N>.md` |
| Updated open-loops.md (surgical loops → Resolved w/ date + chosen carrier + provenance; structural loops marked in-progress) | `<chapter>/open-loops.md` |

The revision frontmatter carries `kind: loop-clear`, the `source_draft` it derived from, a `loops_resolved` manifest and a `loops_pending_rewrite` manifest, and `status: loops-cleared` (or `loops-partial` while demo blocks await CRE's rewrite). `<N>` is the next integer for the `loops` slug. The revision is landed later by [[WORKFLOWS/promote-revision]]; `draft.md` is untouched until then.

## Steps

### Step 0 — Vault sentinel
Read `_DIRECTIVES.md` at the mounted root; confirm frontmatter `type: ai-os-brain` + `file: directives`. Mismatch or missing → halt and ask which folder is the vault. (Shared `^obs-004` gate.)

### Step 1 — Resolve the chapter, the loops, and the voice sources
Locate the chapter folder (CRE names it, or the most recently touched). Read `open-loops.md` and `draft.md`. Walk up to the project root (the folder whose `CHAPTERS/` holds this chapter) and read `REFERENCE/voice-spec.md` + `REFERENCE/register.md` if present, plus [[KNOWLEDGE/VOICE SAMPLES]]. If `open-loops.md` is missing or has no unresolved entries → halt (see Stop conditions). Name what you loaded so a misfire is visible.

### Step 2 — Parse and triage every unresolved loop
For each unresolved entry: record its source span and locate that exact span in `draft.md` (quote it back so the anchor is visible). If a span can't be found in `draft.md`, flag it and continue with the others (don't block the batch).

**Classify by fix size, not just the section header.** The template's sections (Register-repair / Image-doubling / Left-for-later) are the *default* tier signal, but `open-loops.md` formats vary across chapters — some carry CRE-ruled **"Revision targets"** or free-form entries with no template section (e.g. CH5 — HER DUE). When the section doesn't map to a tier, triage on the size of the fix the entry calls for: **a clause/line add or a carrier swap → SURGICAL; new dialogue, a beat, or any passage that must be *written* → STRUCTURAL.** Promote any oversized SURGICAL case to STRUCTURAL; when in doubt, demonstrate — don't author. A single entry can also bundle several touches of different sizes (CH5's R2 = three surgical clock clauses), so split it into per-touch proposals. Entries that are thematic guardrails rather than per-line fixes (CH5's Maiden-as-Mother spine) are constraints on the other fixes, not loops to clear — note them and move on.

### Step 3 — Build proposals in voice (no writing yet)
- **SURGICAL (register-repair):** show the named-emotion source line, both Transcoder carriers (A/B), and up to **2** additional drop-in phrasings, each a complete line that matches the voice-spec bands and VOICE SAMPLES. One short reason per option. Flag any option that risks measurable voice-spec drift.
- **SURGICAL (image-doubling):** show both instances; recommend which to keep (the stronger image / better-placed beat) with a one-line reason; the other is a clean cut.
- **STRUCTURAL (left-for-later, + promoted cases):** name the beat, why it's load-bearing, and give **one** demonstration of the fix — the *move* (e.g. how to render the named emotion as observable action/physics in CRE's register), explicitly labeled a demonstration, not final prose.

### Step 4 — Gate: CRE rules every loop (the propose→write boundary)
Present all proposals grouped by tier (surgical first, structural second). CRE picks/refines each surgical option and approves or redirects each structural demo. Capture the rulings. **Do not write the revision until every loop is ruled or explicitly deferred.** (Mirrors the gating shape of `blind-response` / `reconcile`.)

### Step 5 — Assemble the loop-clear revision
After all loops are ruled, copy `draft.md`'s prose into `revisions/YYYY-MM-DD-loops-rev<N>.md` and:
- Apply each **surgical** fix in CRE's chosen wording, in place (register-repair = swap the carrier; image-doubling = delete the dropped instance). Clean prose, no marks.
- For each **structural** fix, insert a fenced block at the exact location, keeping the original so CRE rewrites in place:
  ```
  <<DEMO — CRE to rewrite — loop: [section/§ref]>>
  ORIGINAL: <the untouched original span>
  DEMONSTRATION (not final — CRE writes the real prose): <the worked example of the fix>
  <<END DEMO>>
  ```
- Write frontmatter via `yaml.safe_dump` and gate the write on a real YAML parse (DIR-004): `type`, `chapter`, `kind: loop-clear`, `source_draft`, `rev: <N>`, `status: loops-cleared` (or `loops-partial` if any demo blocks remain), `loops_resolved: [...]`, `loops_pending_rewrite: [...]`, `last_updated`.

### Step 6 — Update open-loops.md
Move each ruled **surgical** loop into the **Resolved** section with the date, the chosen carrier/decision, and provenance `(rev<N>)`. Mark each **structural** loop in place as `in progress — demo in rev<N>, CRE rewriting` — it does **not** move to Resolved until CRE finishes the rewrite and the revision is promoted. Edit with the file tools and verify by re-reading (`^obs-020` / `^obs-014`); `open-loops.md` is a `chapter-meta` file, not an OS/WORKFLOWS canon doc, so DIR-005's no-MCP-rewrite rule does not bind it — but the same verify-by-re-read hygiene applies.

### Step 7 — Hand off
Report: surgical fixes committed in `rev<N>`; structural demos await CRE's rewrite at the marked blocks; once CRE finishes them, run [[WORKFLOWS/promote-revision]] (or [[WORKFLOWS/land-chapter]]) to land the revision into `draft.md`, then [[WORKFLOWS/register-pass]] for the line pass on the cleared draft.

## Stop conditions
- Vault sentinel fails → halt, ask which folder is the vault.
- Chapter doesn't follow the per-chapter folder convention, or no `draft.md` → halt, tell CRE.
- `open-loops.md` absent or no unresolved entries → halt; nothing to clear.
- A loop's source span can't be located in `draft.md` → flag it, skip that loop, continue the rest; never guess a span.
- Voice sources (voice-spec / VOICE SAMPLES) absent → proceed best-effort but say so, and flag that options are unverified against the fingerprint.

## Integration touchpoints (sibling skills)
- **promote-revision** — WIRED 2026-06-16 (canon doc): [[WORKFLOWS/promote-revision]] now reads the promoted rev's `kind` and maps `loop-clear → status: loops-cleared` (default → `register-revised`). `.skill` propagation (rebuild + reinstall via `pack-skills.ps1` / Save-skill) is the desktop-gated follow-up. Was `^backlog-promote-loopclear-status`.
- **register-pass** — WIRED 2026-06-16 (canon doc): [[WORKFLOWS/register-pass]] Step 1 now treats `loops-cleared` as real content (picks `draft.md` as working text, alongside `dev-revised`). `.skill` propagation desktop-gated. Was `^backlog-register-loopcleared-worktext`.

## Logging
On completion append an entry to [[_CHANGELOG]] (fiction lane) and the chapter's `changelog.md`; file any new fragility to [[_OBSERVATIONS]]. See the skill for the exact log format.

---

_Canonical reference for the `loop-clearer` Cowork skill. Per [[_SKILLS MAP#Cowork skills]], procedure changes land here first, then propagate to the skill via skill-creator. Packaging (`.skill` via `pack-skills.ps1` + Save-skill) is the desktop-gated final step — see `_BACKLOG` (`^backlog-loop-clearer-package`)._
