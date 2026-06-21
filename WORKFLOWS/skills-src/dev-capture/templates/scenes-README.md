---
type: dev-readme
project: {{PROJECT}}
bucket: scenes
last_updated: {{DATE}}
---

# scenes/ — the granular unit (scene = truth)

One evolving entry per scene: `SC NN - <name>.md`. **This is where most discovery happens and the unit everything else derives from.** Authority flows **up** from here: a changed scene re-derives its sequence read above it, which may shift `project.md`.

**Sculptor, not historian.** When a scene sharpens, `dev-capture` **overwrites the entry in place** so it always holds the current sharpest take. The raw transcript is swept to `_intake/_audit/` (the recoverable floor); the entry keeps only a one-line `superseded prior take: see intake <date>` pointer — never the old prose.

**Preserve the kind.** Questions CRE left open stay questions. Stumbled dialogue is captured as a *target to reach toward*, flagged un-pressure-tested — never committed prose.

Entry shape: see `templates/_scene-entry.md` (the router copies it for a new scene).
