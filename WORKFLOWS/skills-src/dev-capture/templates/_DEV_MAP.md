---
type: dev-map
project: {{PROJECT}}
profile: {{PROFILE}}
file: dev-map
last_updated: {{DATE}}
---

# {{PROJECT}} — DEV Map (local index + routing rules)

> The `dev-capture` router reads this first (Step 1). It holds this project's cue table and any **graduated** `_POETICS` patterns. Edit the cue table here to teach the router project-specific vocabulary.

## The DEV/ tree
```
DEV/
├── _DEV.md            taste anchor — what I love / what I know so far
├── project.md         macro read (novel/novella) — DERIVED, authority flows up
├── sequences/         evolving sequence reads (novel)  ·  movements/ (novella)
├── scenes/            THE GRANULAR UNIT — scene = truth
├── registry/          the wiki — characters / locations / lore / items (wikilinked)
├── _intake/           holding pen + _audit/ transcript floor + _LEDGER.md
├── _POETICS.md        observed patterns in HOW CRE develops
└── _DEV_MAP.md        this file
```
*(profile `{{PROFILE}}` — some rungs may be intentionally absent: short = no sequences/ or project.md; novella = movements/ instead of sequences/.)*

## Cue table (head of a segment → destination)
| CRE says | Routes to | Builds / updates |
|---|---|---|
| "project level…" / "what I love about this book…" | `_DEV.md` (+ `project.md`) | taste anchor + macro read |
| "sequence — the part where…" | `sequences/SEQ NN.md` | evolving sequence entry |
| "scene — …" / "the moment when…" | `scenes/SC NN.md` | evolving scene entry (granular) |
| "character — everything about…" / arc talk | `registry/characters/<name>.md` | character entry |
| "world / lore — …" / "the magic works like…" | `registry/lore/<topic>.md` | lore entry |
| "place — …" | `registry/locations/<name>.md` | location entry |
| (no cue, project-bound) | inferred per the segmentation contract → else HOLD in `_intake/` | best-guess (tagged inferred) or held |

## Segmentation contract (graceful degradation)
1. **Explicit cue wins, always** — hard boundary + hard destination, no second-guessing.
2. **Missed cue → infer with confidence, and TAG the boundary `(inferred)`** — sustained character focus → registry; GOAL→BUT→THEREFORE chain → sequence; concrete sensory moment + stumbled dialogue → scene.
3. **Below the confidence bar → HOLD in `_intake/`** — never force-file. A confident misfile costs more than an unrouted fragment.

## Standing rules
- **Preserve the kind.** A question CRE left open stays a question. Stumbled dialogue is captured as a *target to reach toward*, flagged un-pressure-tested — never as committed prose.
- **Sculptor, not historian.** Sharpening overwrites in place; the raw transcript is the recoverable floor in `_intake/_audit/`; the entry keeps only a one-line `superseded prior take: see intake <date>` pointer.
- **DIR-001.** A detected secret/credential is never filed — flag + advise rotate.

## Graduated poetics patterns (router-binding once promoted)
<!-- dev-capture lists ^poe-NNN patterns here ONLY after CRE promotes them. Empty until the poetics log has recurrences. -->
_(none yet)_
