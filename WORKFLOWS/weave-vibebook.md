---
type: workflow
name: weave-vibebook
trigger: weave the vibes
aliases: [weave the vibebook, weave my vibes, run the weave, connect the vibes, process the vibes]
inputs: [raw fragments in VIBES/CAPTURE.md ⚡ Inbox zone]
outputs: [anchored fragments in CAPTURE.md stream, updated threads.md, proposed constellations.md entries, optional synthesis.md note]
lane: vibes
status: active
last_updated: 2026-06-14
---

# WORKFLOW: weave-vibebook

> Bucket renamed Vibebook → **Vibes** in the 2026-06-14 restructure. The workflow keeps its filename (`weave-vibebook`); the trigger **"weave the vibes"** is primary and the legacy **"weave the vibebook"** still works as an alias.

## When to use
CRE says **"weave the vibes"** (or "weave the vibebook", or has dumped new fragments and wants them connected). This is the AI half of the Vibes creativity engine — CRE captures raw; this workflow anchors, links, and surfaces connections he didn't make himself. See [[VIBES/_VIBES]].

## Core discipline
**Capture is canonical and immutable; the weave is a regenerable one-way mirror** (same contract as `canon-sync` / `storyline-sync`). Never reword, merge, split, or delete a captured fragment — only add structure *around* it (anchor, facets, links). If the weave is wrong, regenerate it; the capture stream is never the thing that changes.

## Task-guard (Vibes is a creativity engine, not a productivity tool)
If a fragment in the Inbox is actually a **to-do / task / action item**, do NOT anchor or weave it. Pull it out, list it in the run report under "→ Tasks," and leave it for the inbox router (or CRE) to file into [[TASKS/_TASKS|Tasks]]. Vibes never holds tasks.

## Inputs
Raw fragments under the **⚡ Inbox** zone of [[VIBES/CAPTURE]] (text, quotes, image embeds), plus the existing corpus (anchored stream + `weave/`).

## Outputs
- New fragments anchored (`^vb-NNN`) + faceted, moved Inbox → Stream in CAPTURE.md.
- `weave/threads.md` updated with any new/extended themes.
- `weave/constellations.md` updated with new **proposed** connections (reasoning + anchors).
- `weave/synthesis.md` appended with a dated insight note **only** when the corpus warrants it.
- A short report to CRE: what was woven + the strongest 1–3 new connections to rule on + any task-shaped fragments pulled out for Tasks.

## Steps

### Step 1 — Vault sentinel + load
Confirm `_DIRECTIVES.md` frontmatter is present (the `^obs-004` guard). Read [[VIBES/_VIBES]], CAPTURE.md (both zones), and the three `weave/` files. Find the highest existing `^vb-NNN` to continue numbering.

### Step 2 — Intake (anchor + facet)
For each Inbox fragment, in capture order — **after** removing any task-shaped items per the Task-guard:
1. Assign the next `^vb-NNN` anchor.
2. Classify a **type** (thought / quote / theory / lesson / image / question / fragment-link).
3. Tag 1–4 **facets** — concrete recurring handles (e.g. `grief`, `repetition`, `myth`, `craft:withholding`, `southwestern`, `Witchwood`). Reuse existing facets before coining new ones; facets are the grounding that keeps connections from going generic.
4. Write the fragment into the **Stream** zone (newest first) as:
   ```
   ### ^vb-NNN — YYYY-MM-DD
   **type:** <type> · **facets:** a, b, c · **links:** [[#^vb-XXX]] …
   <CRE's verbatim text, untouched>
   ```
5. Remove the now-processed fragment from the Inbox zone (it lives in the Stream now — the only "move," text byte-identical).
**Note:** if a fragment is ambiguous, tag a best-guess facet and flag `<<UNCERTAIN>>` rather than guessing silently — never invent content.

### Step 3 — Weave (incremental)
Link the newly-anchored fragments against the whole corpus:
- **Threads:** for each facet/theme that now has ≥2 members, ensure a `T-NN` thread exists in `threads.md` and its member list + count are current. Extend existing threads before creating new ones.
- **Constellations:** propose connections *between specific fragments* — especially **non-obvious** ones (a craft note that mirrors a grief theory; a Godsrift image that rhymes with a Witchwood fragment; two fragments months apart circling one unnamed idea). Each new entry gets `status: proposed`, both fragment anchors, the **reasoning**, and a **"so what"** (the opportunity it opens). Don't re-propose anything already `rejected`.
**Discipline:** quality over volume. A few sharp, grounded connections beat a wall of "these both mention death." Cite anchors, not vibes.

### Step 4 — Synthesis (conditional)
If the corpus has grown enough that a **higher-order pattern** is visible (rule of thumb: a thread crossed ~5+ fragments, or several threads now interlock), append a dated note to `synthesis.md`: the pattern, what it suggests, and one open question it raises. If nothing has truly crystallized, **skip this step** (don't manufacture insight).

### Step 5 — Report + rule
Bump `last_updated` on every file touched. Tell CRE: how many fragments anchored, threads touched, the **strongest 1–3 new connections** with reasoning (invite him to mark each `affirmed`/`rejected` in constellations.md), and any task-shaped fragments routed to Tasks. Record his rulings when he gives them.

## Stop conditions
- Inbox empty and no corpus change → report "nothing to weave," stop.
- A fragment contains a secret/credential (DIR-001) → flag, do not propagate, advise CRE to move + rotate it.
- Asked to reword/delete a fragment → refuse by default; capture is canonical. Confirm with CRE before any destructive change to CAPTURE.md.

## Notes / fragility
- Use the **file tools** (Read/Write/Edit) on the mounted folder, not `patch_vault_file`; verify writes via the file tools, not a bash read (`^obs-020` / `^obs-014`).
- On-demand only — no scheduled pass yet (CRE's choice; revisit when the corpus is large).

## Logging
On completion, append an entry to [[_CHANGELOG]] under the `vibes` lane.
