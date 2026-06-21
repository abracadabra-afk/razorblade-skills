---
type: dev-readme
project: {{PROJECT}}
bucket: _intake
last_updated: {{DATE}}
---

# _intake/ — holding pen + the floor

Two jobs:

1. **Landing + holding.** A raw cleaned transcript lands here first; **below-confidence / unsplittable segments stay here** with their candidate destinations + one line on why held. The router *declines to act* rather than force-file — a confident misfile costs more than an unrouted fragment. Held files: `HOLD-<date>-<n>.md`.
2. **`_audit/` — the transcript floor.** Once a segment is routed and an entry sharpened in place, the **source transcript is swept to `_audit/`** as the recoverable record. Routed entries keep only a one-line pointer back here; the old prose lives only on the floor.

`_LEDGER.md` (the deferred contradiction ledger) also lives here.
