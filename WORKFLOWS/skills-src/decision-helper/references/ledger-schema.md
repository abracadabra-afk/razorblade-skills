# DECISIONS/ Ledger Schema

One ledger, both lanes. Vault root: `DECISIONS/`.

```
DECISIONS/
├── _QUICK LOG.md          ← append-only one-liners (quick mode)
├── _WEIGHTS.md            ← ratified pattern findings (review-derived only)
└── YYYY-MM-DD <slug>.md   ← one file per in-depth decision
```

All frontmatter is serialized YAML (DIR-004). `_QUICK LOG.md` and `_WEIGHTS.md` are append-style brain docs — size-band them with the log-rotate conventions if they grow.

---

## 1. Quick log line (`_QUICK LOG.md`)

One line per quick decision, table rows, newest at bottom:

```
| 2026-07-10 | Errand order Sat | Post office first | closes the deadline item | ratified |
```

Columns: `date | decision | pick | one-line basis | ruling`. Nothing else. If even this feels heavier than the decision was, skip the log (below-trivial threshold).

---

## 2. In-depth entry (`YYYY-MM-DD <slug>.md`)

### Frontmatter

```yaml
---
type: decision
id: dec-NNN            # sequential, zero-padded
date: 2026-07-10
lane: creative          # creative | life
project: Witchwood      # creative lane only; omit for life
mode: triangulate       # quick | research | triangulate
status: ratified        # open | ratified | parked | reviewed
review-date: 2026-08-10 # required when ratified
parked-until: ""        # condition, not just a date — set when status: parked
outcome: ""             # filled at review, never at decision time
---
```

### Body sections (in order)

```markdown
# Decision
One sentence: what was being chosen, and the deadline if any.

## Goals & criteria
Derived from what CRE said, confirmed in-session. Each criterion with its
weight (default even; adjusted only per _WEIGHTS.md or CRE's in-session say-so).

## Options
### Considered
Each option CRE's-words-first (creative lane: his branches verbatim).
Per option: how it scored against the criteria.
### Discarded
Every option dropped during synthesis, WITH the reason it lost.
This section is where a bad recommendation gets caught on dig-in.

## Receipts
- Research mode: sources pulled; load-bearing claims corroborated across
  independent sources; thin/single-source claims flagged as such.
- Triangulate mode: per-lens findings —
  - Chad likes: (taste anchor + ruling-history evidence)
  - Story prefers: (threads/arcs/bible obligations touched)
  - Reader experience: (blind-read + intensity-contour evidence)
  - Tensions: where the lenses disagree (never averaged away)

## Recommendation
The pick + the one-line basis as presented to CRE.

## Ruling
What CRE actually ruled (ratify / overrule-with-different-pick / park),
and any correction he made to the reasoning — corrections are training data.

## Review
Filled at review-date: what happened, was the call right, what the basis
got wrong. Feeds _WEIGHTS.md only via a ratified proposal.
```

Write order matters: Receipts are written **during** synthesis (dig-in is a view over this file, not a reconstruction).

---

## 3. Weights file (`_WEIGHTS.md`)

Append-only. One block per **ratified** pattern finding:

```markdown
## ^wgt-001 — 2026-09-14
Pattern: overweights cost, underweights energy drain (life lane, n=7 reviews).
Ratified: yes, 2026-09-14.
Effect: energy-drain criterion defaults +1 weight step in life-lane entries.
Evidence: dec-003, dec-007, dec-011, dec-012.
```

Rules:
- Nothing enters this file without CRE ratifying the finding at review.
- Each block cites the entry IDs it derived from (receipts all the way down).
- Retrospective-seeding findings (if CRE ever runs the mining pass) enter
  the same way — as ratified blocks, marked `source: retrospective`.

---

## 4. Parked forks & dev-readiness

Entries with `status: parked` and a `parked-until` condition in a creative
lane are load-bearing dev gaps. Until a native integration exists,
mention parked forks when running dev-readiness on that project, and
re-surface any entry whose parked-until condition has since been met.
