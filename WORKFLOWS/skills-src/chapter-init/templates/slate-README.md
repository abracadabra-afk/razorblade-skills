# slate/

[[WORKFLOWS/transcoder|Transcoder]] outputs. **Immutable** — one folder per run, never overwritten.

**Layout per run:**
```
slate/
└── YYYY-MM-DD-NN/
    ├── clean-draft.md
    ├── cut-log.md
    ├── synthesis-ledger.md
    └── leaves-left.md
```

Accepted clean-drafts get stitched into `../draft.md`. The slate folder stays as the audit trail — when a misread surfaces three sessions later, you come back here to see exactly what the Transcoder did and why.
