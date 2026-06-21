---
type: dev-readme
project: {{PROJECT}}
bucket: registry
last_updated: {{DATE}}
---

# registry/ — the wiki

Each entry is its own wikilinked note, so **Obsidian's graph *is* the connection map.** Subfolders: `characters/`, `locations/`, `lore/`, plus `items.md` (light enough to stay a single note until it needs splitting).

**Standalone by design.** Registry entries never hard-code the macro shape — which is what lets them be lifted *upward* into a shared series-level registry later without a migration (commitment (b) in the workflow doc).

**Braids route to both.** When a segment legitimately feeds a character *and* a scene/sequence (transformation braided with intensity), `dev-capture` routes to both and wikilinks them — dual-destination is a recognized shape, not a failure.

Entry shapes: `templates/_character-entry.md`, `templates/_location-entry.md`, `templates/_lore-entry.md`.
