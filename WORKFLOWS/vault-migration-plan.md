---
type: migration-plan
purpose: Sequenced checklist for the 2026-06-14 vault restructure to the eight-root domain model.
status: complete
last_updated: 2026-06-14
---

# Vault Migration Plan — eight-root restructure (2026-06-14)

## Target structure

Eight domain roots (organized by domain, not by source — the property that makes it survive adding connectors), plus `INBOX` and the `_` OS/brain files:

| Root | Holds |
|---|---|
| **VIBES** | Creativity engine (was VIBEBOOK) — CAPTURE + weave |
| **TASKS** | To-dos (was TASKBOOK) |
| **LIFE** | Personal data (was LIFEBOOK) — REFERENCE, FINANCE, FITNESS, FOOD, MENTAL HEALTH, recipes |
| **KNOWLEDGE** | Durable human learning — research, methods, world-general craft, human skills |
| **WRITING** | Creative output — NOVELS, short fiction, essays/articles, STORYLINE mirror |
| **BUSINESS** | The author/media company — sales/royalties/distribution, contracts, business finance/admin/tax, Substack-the-publication, marketing, social, branding, business CRM |
| **WORKFLOWS** | Automations (DoBook brand retired) — workflow docs + skills/ (build artifacts) + prompts/ |
| **GRAVEYARD** | Cold storage — archived + parked + discarded, each with a status header |

Guiding rule for connectors: external system is the source of truth, the vault derives; the **inbox-router** is the only write-path from a connector into a domain; live streams (calendar, unread mail) are surfaced as live views, never mirrored into notes.

## Two constraints discovered during execution

1. **Cloud-only files.** Parts of the vault (e.g. `WRITING/ARCHIVE/Short Stories/*`) live only in Dropbox's cloud, not on local disk. bash/`tar` cannot read or move them; **Obsidian and the Obsidian MCP can**. Any mass move must go through a tool that handles cloud-only files.
2. **Link integrity.** Obsidian only auto-updates wikilinks when the rename happens *inside the Obsidian app*. A programmatic move does **not** heal links — and a programmatic link-sweep also can't see inside cloud-only notes. Conclusion: **folder renames/moves are safest done Obsidian-native.**

## Checklist

### Phase 0 — Safety net
- [x] md-only backup tar (`_pre-migration-md-backup_2026-06-14.tar.gz`, partial — excludes cloud-only files)
- [x] Primary restore point = **Dropbox version history** (has everything)

### Phase 1 — New roots (additive, done)
- [x] `BUSINESS/_BUSINESS.md`
- [x] `KNOWLEDGE/_KNOWLEDGE.md`
- [x] `GRAVEYARD/_GRAVEYARD.md`
- [x] `WORKFLOWS/skills/` (README)
- [x] `WORKFLOWS/prompts/` (README)
- [x] This plan note

### Phase 2 — Renames (Obsidian-native; links auto-heal) — GATED
- [ ] `LIFEBOOK` → `LIFE` (+ `_LIFEBOOK.md` → `_LIFE.md`)
- [ ] `TASKBOOK` → `TASKS` (+ `_TASKBOOK.md` → `_TASKS.md`)
- [ ] `VIBEBOOK` → `VIBES` (+ `_VIBEBOOK.md` → `_VIBES.md`, `CAPTURE.md` path → `VIBES/CAPTURE.md`)
- [ ] Retire DoBook brand: `WORKFLOWS/_DOBOOK.md` → `_WORKFLOWS.md` (reword as plain index)

### Phase 3 — Merges & moves
- [ ] `SKILLS/*` → `WORKFLOWS/skills/` (artifacts + REGISTRY + `_skill-patches/`), delete empty `SKILLS/`
- [ ] `STORYLINE/` → `WRITING/STORYLINE/`
- [ ] `WRITING/DICTATION PROMPTS` → `WORKFLOWS/prompts/`
- [ ] WRITING craft → `KNOWLEDGE`: STYLE, PROCESS, VOICE SAMPLES, general REGISTERS, BOOK HIGHLIGHTS, REFERENCES *(keep per-project register/voice-spec/contamination in each project's `REFERENCE/`)*
- [ ] `WRITING/SUBSTACK` + `WRITING/MARKETING` → `BUSINESS`

### Phase 4 — GRAVEYARD
- [ ] `WRITING/ARCHIVE` → `GRAVEYARD/` (status headers)
- [ ] Parked Inkwell (Orchestrator) → `GRAVEYARD/` tagged *parked — live refs*
- [ ] Decimation / The Never Was → `GRAVEYARD/` (pending CRE's status call)

### Phase 5 — Machine wiring
- [ ] Edit `WORKFLOWS/inbox-router.md` (renamed book paths + add BUSINESS/KNOWLEDGE targets) — doc only, no rebuild
- [ ] Edit `WORKFLOWS/weave-vibebook.md` (`VIBEBOOK/` → `VIBES/`) — doc only, no rebuild
- [ ] `storyline-sync`: update write path `STORYLINE/` → `WRITING/STORYLINE/`; **rebuild + reinstall**
- [ ] `skill-audit`: update `.py` path logic `SKILLS/` → `WORKFLOWS/skills/`; **rebuild + reinstall**

### Phase 6 — OS files
- [ ] `_VAULT MAP.md` — rewrite bucket index for eight roots
- [ ] `_SKILLS MAP.md` — skill-table paths (`SKILLS/` → `WORKFLOWS/skills/`), renamed book paths
- [ ] `_ME.md` — The Books section (renames + KNOWLEDGE/BUSINESS/GRAVEYARD)

### Phase 7 — Log + verify
- [ ] `_CHANGELOG.md` entry
- [ ] `_OBSERVATIONS.md` anchor for the migration
- [ ] `_BACKLOG.md` — the two skill rebuild/reinstall tasks
- [ ] Verify: link-integrity sweep + `skill-audit` run (after rebuild)
- [ ] Remove `_pre-migration-md-backup_2026-06-14.tar.gz` once settled

## Skill rebuilds required (the manual tail)

Only **two** packaged skills hardcode a moved path: `storyline-sync` and `skill-audit`. Both need rebuild (via skill-creator) + reinstall (CRE clicks "Save skill"). The router and weave are bootstrap-run workflow docs — doc edits suffice, no rebuild.
