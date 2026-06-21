---
type: dev-readme
project: {{PROJECT}}
bucket: _intake/_audit
last_updated: {{DATE}}
---

# _intake/_audit/ — the transcript floor

The recoverable bedrock under the sculptor. Every raw cleaned transcript whose segments have been routed is swept here verbatim, dated (`<date>-<source>.md`). This is what makes **overwrite-in-place safe**: a superseded take is always recoverable from the floor, so routed entries can hold only the current sharpest version + a one-line pointer. Never edited, never pruned by the router.
