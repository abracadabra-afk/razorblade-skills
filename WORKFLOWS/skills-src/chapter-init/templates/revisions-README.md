# revisions/

One-way door out of the [[WORKFLOWS/transcoder|Transcoder]] workflow.

When a slate is ready to leave the rough phase, run the revision stage — [[WORKFLOWS/register-pass]] ("run the register") — which takes the newest `slate/` `clean-draft.md`, revises it against the project register (`REFERENCE/register.md`), and writes the revised passage here plus an editorial-note sidecar. ([[WORKFLOWS/dictation-cleanup]] remains available for a lighter, word-preserving copy-edit.) Once material is in this folder, the Transcoder never reads from it again.

**Naming:** `YYYY-MM-DD-<segment-slug>-rev<N>.md` (revised passage) + `…-rev<N>-note.md` (editorial note).
