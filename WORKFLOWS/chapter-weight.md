---
type: convention
name: chapter-weight
trigger: none — this is a referenced convention, not an invoked workflow
referenced_by: [spec-check, scene-intensity, workshop-chapter, chapter-init]
lane: fiction
status: active
scope: Any per-chapter-folder project. First adopter — Witchwood.
last_updated: 2026-06-13
---

# CONVENTION: Chapter Weight (scope-based effort)

> A one-field tag that tells the QA pipeline **how much diagnostic effort a chapter is worth** — so a turning-point chapter gets the full battery and a connective chapter gets a lean pass. From the archive's scope-based-excellence idea (ROSETTA) + load-bearing-scene classification (Plot-Character V7), kept to a single tag instead of a 7-criteria apparatus.
>
> **The iron rule: depth scales, the standard never does.** Weight changes how many diagnostic passes run, never how good the prose has to be. A bridge chapter is not allowed to be sloppy — it still gets the register. It just doesn't need five fresh-context diagnostic passes thrown at it to get there. (ROSETTA: *"Execution depth scales; standards don't."*)

## The field

In a chapter's `brief.md` frontmatter:

```yaml
weight: load-bearing | standard | bridge
```

**Resolution order** (any workflow reads it this way): `brief.md` `weight:` → else `_status.md` `weight:` → else **default `standard`**. Absent is always treated as `standard` — the system never silently runs a chapter lean just because the tag is missing.

## The three weights

- **`load-bearing`** — the chapter *turns the book*: a major reveal, a character-arc pivot, a climax or confrontation, a planted seal that must land here, or the book's opening / closing chapter. Maximum scrutiny.
- **`standard`** *(default)* — a normal forward-motion chapter. The ordinary selective battery.
- **`bridge`** — connective tissue: travel, low-stakes setup, a beat with no turn, reveal, or seal. Lean pass.

## Assigning it (quick rubric)

Ask, in order:
1. Does the chapter contain a major reveal, an arc turn, a climax/confrontation, a must-land seal, or is it the book's first/last chapter? → **load-bearing**.
2. Is it pure connective tissue — no turn, no reveal, no seal it has to carry? → **bridge**.
3. Otherwise → **standard**.

**When uncertain, round UP** (toward more scrutiny): an ambiguous chapter is `standard`, never `bridge`. Weight is CRE's call — it's a judgment about the chapter's role in the book — set at brief-fill. `chapter-init` seeds `weight: standard` for CRE to confirm. **Weight is a starting estimate, not a cage:** a chapter that turns out to carry more than expected gets bumped; if a pass on a `bridge` chapter trips heavy flags, treat that as a signal to re-weight it, not to wave it through.

## What weight throttles

| Stage | `load-bearing` | `standard` | `bridge` |
|---|---|---|---|
| **blind-read** (spec-check Pass 1) | run | run | optional — skip if the chapter carries no reader-experience risk |
| **developmental pass** (blind-response) | as needed | as needed | rarely |
| **spec-passes 2–5** | all four + reconcile | all four + reconcile (the default selective battery) | Pass 2 (carries) only, or skip the battery and go straight to the register |
| **scene-intensity** | full per-scene, both tracks | standard | chapter-level contour only; skip per-scene deep scoring unless a valley shows |
| **register-pass** | full | full | **full** — the register runs on every chapter; weight never lowers the line-quality bar |

The register is the floor for all three weights. Weight only decides how much *diagnosis* runs upstream of it. The whole point is to spend CRE's grading attention (the expensive, human part of the battery) where the book can actually go wrong.

## Stop / safety
- Missing tag → `standard`, never `bridge`.
- A `bridge` chapter returning heavy flags on the one pass it gets → surface it; recommend re-weighting to `standard`/`load-bearing` before continuing.

---

_Canonical reference for the chapter-weight convention. Referenced by spec-check, scene-intensity, workshop-chapter, and chapter-init; procedure changes land here first, then propagate to those skills via skill-creator._
