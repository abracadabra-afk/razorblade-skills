---
name: storyline-sync
description: Mirror a landed chapter into a StoryLine project — derive StoryLine scene files and Codex entries (characters, locations, items, lore) from the chapter's draft.md plus REFERENCE/bible.md + threads.md, so the author gets StoryLine's Board, Timeline, Plotlines, and Codex views over prose written in the per-chapter pipeline. Use whenever the author asks to "sync to storyline," "build the storyline," "storyline this chapter," "mirror to storyline," "update storyline," or wants a landed chapter reflected in their StoryLine project. Runs downstream of promote-revision / canon-sync, on projects using the per-chapter folder convention that keep a REFERENCE/ folder AND have a StoryLine project. draft.md is the single source of truth; StoryLine is a regenerated, one-way mirror — this skill never authors prose and never writes back into a draft. Do NOT use it to revise prose (register-pass), update REFERENCE canon (canon-sync), promote a revision (promote-revision), or author StoryLine content by hand.
---

# StoryLine Sync (mirror the chapter into StoryLine)

You are running the derivation pass that converts a **landed** `draft.md` into StoryLine-format files — one `.md` per scene plus Codex entries for the characters, locations, objects, and lore it touches — so the author gets StoryLine's analytical views (Board, Timeline, Plotlines subway map, Relationship Map, Stats) over prose they wrote in the per-chapter pipeline. StoryLine stores everything as Markdown + YAML frontmatter, so this is a pure file-derivation pass — no API.

You hold **no craft opinion and no plot opinion.** `draft.md` is the single source of truth; StoryLine is a regenerated mirror. Prose flows one way — `draft.md` → StoryLine, never back. If the author drafts inside StoryLine, the two systems drift; your job is to keep StoryLine downstream.

**The hardest-won lesson of this skill (read this before you write anything): a mature plugin does more than you think, and your integration should do less.** StoryLine self-manages three of its highest-value views — the sync writes **nothing** for them:

- **Plotlines** auto-derive from scene `tags` and auto-color by name-hash. No registry, no color file.
- **Codex categories** (Items, Lore, Creatures, …) are built-in and enabled via a *global* plugin setting. Not per-project, not custom — you never write that setting.
- **Plot Grid** has a native "Sync from Scenes" button (additive, author-safe). You never write `System/plotgrid.json`.

Do not diagnose any of these as "broken" from an empty config file. They are plugin-owned. What you DO own: **scene files** and **Codex entries** (characters, locations, items, lore), derived from the draft and bible. You also **invoke** the scene-intensity engine (Step 3b) to seed the intensity fields — it is a dependency, runs inside this sync after segmentation, and its scores must be *run*, never eyeballed.

## Key principles

1. **Derive only from landed text + REFERENCE.** Scene prose comes from `<chapter>/draft.md`; codex facts from `REFERENCE/bible.md`; plotline tags from `REFERENCE/threads.md`; scene end-state (for scene `notes`) from `<chapter>/continuity.md`. Never derive from `slate/` or `revisions/`. A scaffold or pre-register draft → warn and ask before syncing.
2. **One direction only.** Prose flows `draft.md` → StoryLine, never back. StoryLine is the lens; the pipeline is the workshop.
3. **Re-sync is a merge, not a clobber.** StoryLine writes its own frontmatter fields (`wordcount`, `modified`, `notesFile`, corkboard position) and the author hand-tunes others (`intensity`, `emotion`, `status`, `tags`). On re-sync: regenerate the prose body from `draft.md`, but **preserve** (a) StoryLine-owned fields and (b) any field the author changed from this skill's last derived value. Only refresh derived-from-prose facts. When in doubt, tag `<<UNCERTAIN: …; confirm?>>` rather than overwrite.
4. **Intensity = three flagged axes, never asserted.** Each scene carries: native `intensity` = `round(si_local/10)` (the engine's 0–10 pacing/menace scalar — it sits on the native field because StoryLine's tension curve is hardwired to it); custom `arc_valence` = signed −10…+10 good/bad direction; the scene-intensity engine's `si_local`/`si_band`/`si_dread`/`si_scores` = the reproducible full read. Plus `emotion`. Record all as inferred in `notes` ("intensity/emotion inferred — adjust to taste") and note the engine version. They are a first pass for the author to correct. **The `si_*` values MUST be produced by actually running the scene-intensity engine (Step 3b) — never hand-estimated. Eyeballing `si_local` silently reintroduces the run-to-run variance the engine exists to remove, which is the whole reason it exists.**
5. **Threads become plotline tags — all touched.** Each `threads.md` entry the scene plants, advances, OR pays off becomes a scene `tag` (kebab-case of the thread name), bare plantings included. The tags are the whole job: StoryLine auto-derives the Plotlines subway map from them and auto-colors each line by name-hash — no registry, no color file. Get the tags right and the map renders on its own.
6. **Codex is idempotent and spoiler-clean.** Entries derive from bible facts carrying their `(CH<N> rev<M>)` provenance; an entity already present is updated in place, not duplicated. Respect the bible's reveal-point discipline — never write a later-chapter fact into an early-chapter entry.

## Step 0 — Vault sentinel check

The gate every skill in this family shares (`^obs-004`). Risk: a mounted folder that *looks* empty reads as a fresh start-up and you write into the wrong tree.

1. From the mounted folder root, read `_DIRECTIVES.md`.
2. Confirm its YAML frontmatter contains both `type: ai-os-brain` and `file: directives`.
3. Missing or mismatched → **halt and ask** which folder is the intended vault. Write nothing.

## Step 1 — Locate chapter + target project; verify landed

Resolve the chapter folder and read `draft.md` frontmatter — expect `status: register-revised` (or `dev-revised`/`hand-revised` if the author syncs mid-pipeline; confirm if so). Record `source_revision` as the provenance tag. Resolve the target StoryLine project under `WRITING/STORYLINE/<Project>/` (confirm with the author if more than one exists). A scaffold or missing draft → halt.

## Step 2 — Load sources + current StoryLine state

Read `REFERENCE/bible.md`, `REFERENCE/threads.md`, `REFERENCE/arcs.md`, the chapter's `continuity.md`, and any existing files in `WRITING/STORYLINE/<Project>/Scenes/` and `/Codex/`. Index existing scenes by title and codex entries by name, capturing StoryLine-owned and author-tuned frontmatter values for the Step 5 merge.

## Step 3 — Segment into scenes

**One scene per hard break.** Split on every `***` (or other hard scene-break) in the draft; a chapter with no break is one scene. No word-count floor/cap. Cross-check against the chapter's envelope segments as a sanity check on the count, not as the split unit. Assign `sequence` in reading order across the whole project (continue from the highest existing; renumber only with the author's OK). Map `act`/`chapter` from the draft frontmatter as **plain integers — no beat sheet** (do not write a StoryLine `beatsheet` or apply a stock scaffold).

## Step 3b — Score scene intensity (RUN the engine; do not estimate)

The intensity axes Step 4 writes are **not hand-derived** — they are the output of actually running the scene-intensity engine on the scenes segmented in Step 3. scene-intensity is its own skill/engine; this sync is its *caller*. Per segmented scene:

1. **Judgment dims (model).** Score D1 (stakes), D2 (proximity), D3 (turns), D4 (irreversibility) with quoted evidence, and apply the carried-dread gate (most scenes 0; cite a `dread_source` for any +1/+2; set `on_page_detonation: true` where the established threat acts in full view). Honor the project rulings: the **D2 predator-POV clause** (a hunt of unbound prey does not raise D2) and the **juxtaposition-dread hand-flag** (an off-page-catastrophe scene scores low locally but is flagged reader-HIGH by hand — the engine's documented blind spot).
2. **Build `scenes.json`** with those dims + each scene's `prose`.
3. **Run the engine:** `python scene_intensity.py score scenes.json --config intensity_config.json`. It computes D5/D6 mechanically (dialogue-aware), the weighted composite, the band, the spread-based seam, and the carried-dread band math — deterministically (same input → same output).
4. **Carry the output into Step 4 verbatim:** native `intensity = round(si_local/10)`; the `si_local`/`si_band`/`si_seam`/`si_dread`/`si_reader_band`/`si_scores` block as the engine returned them; `arc_valence` (signed direction) by judgment. Record all as inferred in `notes`, with the engine version.

Skipping this step (writing `si_*`/`intensity` by eye) is the one move that silently breaks the instrument — see principle 4. Use the patched engine (`_skill-patches/scene-intensity/`, or the installed scene-intensity skill once rebundled), not the stock horror-tuned defaults. scene-intensity needs the scenes segmented first, which Step 3 produces — that's why this runs here, between segmentation and extraction.

## Step 4 — Extract per scene + build codex

For each scene, derive frontmatter from prose + sources (see Schema reference): `pov`, `characters` (`[[wikilinks]]`), `location` (`[[wikilink]]`), `storyDate`/`storyTime`, `conflict` (one sentence), `emotion` + the three intensity axes from Step 3b's engine output (`intensity` = `round(si_local/10)` + `arc_valence` + the `si_*` block, all flagged inferred), `tags` (all touched threads), `status` via the full lifecycle map (`scaffold→idea`, slate→`draft`, `dev-revised→written`, `register-revised→revised`, `final→final`), `timeline_mode` if non-linear, and a `notes` block recording source, inferred-field caveat, threads touched, and end-state from `continuity.md`.

For every character / location / world / **object / lore-rule** a scene references, create or update its Codex entry from `bible.md`, including structured `relations`. **Mirror character arc state from `arcs.md` into the Codex character fields StoryLine already has (no new fields):** entry state → `startingPoint`; exit/current state → `goal`/`expectedChange`; key relationship arcs → `relations[]`; the waypoint trajectory + arc_type → the codex `notes` body, flagged inferred (`arc inferred from arcs.md — adjust to taste`). Spoiler discipline (principle 6) holds — write only state through the chapter being synced, never a later chapter's exit state into an earlier scene's entry. **All categories are built-in StoryLine categories** — mirror the bible's sections: Characters→`Codex/Characters/`, Places→`Codex/Locations/`, Objects→`Codex/Items/`, Lore & rules→`Codex/Lore/`. `items` and `lore` are *toggleable* built-ins governed by the **global** `data.json codexEnabledCategories` — NOT per-project, NOT custom (`codexCustomCategories` stays empty). You never write that setting; you verify it (Step 6). Use the project's existing names exactly so wikilinks resolve.

## Step 5 — Gate conflicts, then write (merge)

If a derived value contradicts existing StoryLine data that looks author-tuned (a scene moved to a different act; a renamed entity), stop and present the conflict (existing value + new evidence + recommendation) for the author's ruling. Otherwise write:

- `Scenes/<NN> - <Title>.md` — regenerate the prose body from `draft.md`; merge frontmatter per principle 3.
- `Codex/Characters/`, `Codex/Locations/`, `Codex/Items/`, `Codex/Lore/` (+ the world file) — add/update entries idempotently, gaps-only on author-written lines.

Omit any field with no data (StoryLine dislikes empty strings/lists). Filenames: `<sequence> - <title>.md` for scenes, `<Entity Name>.md` for codex.

> **YAML emission discipline (MANDATORY — `^obs-025`/`^obs-028`/`^obs-029`, recurred on CH2/CH4/CH5; DIR-004).** Do **not** hand-write frontmatter. Build each file's frontmatter as a dict, then write the file with the bundled serializer:
>
> ```
> scripts/write_storyline.py --out "<PATH>" --frontmatter @fm.json --body @body.md
> ```
>
> It emits the frontmatter via `yaml.safe_dump(..., default_flow_style=False, sort_keys=False, allow_unicode=True, width=100000)` — which auto-escapes every value that has bitten this lane (a wikilink with an apostrophe like `[[Baby Bird's Box]]`, a `conflict`/`significance`/`notes` scalar that starts with `"` or contains `: `, a list of `[[wikilinks]]`) — writes the prose body **verbatim** (never reflows), and **gates the write on a real `yaml.safe_load` round-trip** of the file it just produced (exit 1 if it doesn't parse or doesn't round-trip). Pass the prose body with `--body @body.md` or `--body-stdin` for large prose. If you ever must hand-write a single-quoted scalar instead, **double every internal apostrophe** (`'[[Baby Bird''s Box]]'`) and **never start a scalar with a bare `"`** — but the serializer is the supported path; hand-writing is the failure mode this skill exists to retire.

## Step 5b — Plotlines, Codex categories, Plot Grid: write NOTHING

These are plugin-self-managed. Confirmed against the installed plugin and live runs:

- **Plotlines** auto-derive from scene `tags` and auto-color from a hash of the tag name. The tags you wrote in Step 4 are the entire job. Do **not** write `System/plotlines.json` (the plugin resets it) or hand-edit `data.json`. `tagColors` is an in-app override only.
- **Codex categories** are enabled via the global `data.json codexEnabledCategories`. Do **not** write it. Verify in Step 6.
- **Plot Grid** is built by StoryLine's native "Sync from Scenes" button (scenes × characters, additive, preserves manual rows). Do **not** write `System/plotgrid.json`. If the author wants the grid refreshed, they click the button.

## Step 6 — Verify

Programmatically parse every written file via `scripts/write_storyline.py --verify <files…>` (a real `yaml.safe_load` on a fresh handle, **not** the bash mount — `^obs-014`) and confirm: all frontmatter loads, every scene `characters`/`location` wikilink resolves to a real codex file, `sequence` numbers are unique, `type` is correct, and every scene `tag` resolves to a known `threads.md` entry (plotlines + colors are auto-managed — no color/registry file to check). **Codex-category readiness (read-only):** for any category you wrote into beyond the always-on Characters/Locations (e.g. `Items`, `Lore`), confirm it is listed in `data.json codexEnabledCategories`; if missing, **warn** ("entries in `Codex/Items/` won't display until you enable Items in StoryLine → Codex settings") — do NOT write `data.json`. **Intensity-engine check:** confirm every scene's `intensity` equals `round(si_local/10)` and the `si_*` block is present and well-formed — a mismatch or missing block means Step 3b was skipped or eyeballed; halt and re-run the engine. Report a pass/fail table. StoryLine silently ignores a malformed file rather than erroring, so this check matters.

## Step 7 — Log

Append to the chapter `changelog.md` and the vault `_CHANGELOG.md` (fiction lane): chapter synced to which project, scenes written, codex entries added/updated, conflicts ruled/deferred. File any fragilities to `_OBSERVATIONS.md`.

---

## Schema reference (StoryLine YAML)

Use exact field names; camelCase where shown; omit empty fields; list syntax for arrays.

**Scene** — `type: scene` (req), `title` (req), `act`, `chapter`, `sequence`, `chronologicalOrder` (only if non-linear), `pov`, `characters` (`[[wikilinks]]`), `location` (`[[wikilink]]`), `storyDate`, `storyTime`, `status` (`idea`→`outlined`→`draft`→`written`→`revised`→`final`), `conflict`, `emotion`, `intensity` (`round(si_local/10)`, the pacing scalar — native field drives the tension curve), `arc_valence` (custom, signed −10…+10), `si_local`/`si_band`/`si_seam`/`si_dread`/`si_reader_band`/`si_scores` (custom, scene-intensity engine), `target_wordcount`, `tags` (all touched threads), `setup_scenes`/`payoff_scenes`, `timeline_mode` + `timeline_strand` (non-linear), `notes`. Body after `---` = manuscript prose. StoryLine writes back `wordcount`, `modified`, `notesFile` — StoryLine-owned.

**Character** — `type: character` (req), `name` (req), `tagline`, `nickname`, `age`, `role`, `occupation`, `residency`, `locations[]`, `family`, `relations[]` (`{category, type, target}`), `appearance`, `distinguishingFeatures`, `style`, `quirks`, `personality`, `internalMotivation`, `externalMotivation`, `strengths`, `flaws`, `fears`, `belief`, `misbelief`, `formativeMemories`, `accomplishments`, `secrets`, `startingPoint`, `goal`, `expectedChange`, `habits`, `props`, `custom{}`. Body = notes. **Arc mirror:** `arcs.md` entry → `startingPoint`, exit/current → `goal`/`expectedChange`, relationship arcs → `relations[]`, waypoints + arc_type → `notes` (flagged inferred). No custom fields — these are StoryLine's own character-arc fields.

**Location** — `type: location` (req), `name` (req), `locationType`, `world`, `parent`, `description`, `atmosphere`, `significance`, `inhabitants`, `connectedLocations`, `mapNotes`, `custom{}`. Body = notes.

**World** — `type: world` (req), `name` (req), `description`, `geography`, `culture`, `politics`, `magicTechnology`, `beliefs`, `economy`, `history`, `custom{}`. Body = notes.

**Item** — `type: item` (req), `name` (req), `itemType`, `description`, `origin`, `history`, `owner` (`[[wikilink]]`), `previousOwners`, `properties`, `limitations`, `significance`. Folder `Codex/Items/` (built-in category `items`). Body = notes.

**Lore** — `type: lore` (req), `name` (req), `loreType`, `description`, `fullText`, `sources`, `significance`, `relatedEntries` (`[[wikilinks]]`). Folder `Codex/Lore/` (built-in category `lore`). Body = notes.

**Relation taxonomy** — `family`: sibling, parent, child, guardian, ward · `romantic`: partner, spouse, ex-partner · `social`: ally, friend, best-friend, confidant, acquaintance · `conflict`: enemy, rival, betrayer, avenger · `guidance`: mentor, mentee, leader, follower, commander · `professional`: colleague, business-partner, client, handler, asset · `story`: protector, dependent, owes-debt-to, sworn-to, idolizes, fears, obsessed-with · `custom`: any string.

**Plot Grid** (`System/plotgrid.json`, **plugin-owned — do NOT write**; reference only). `{ rows:[...], columns:[...], cells:{...}, zoom, stickyHeaders }`. Row `{id:"r-<base36time>-<rand>", label, height:80, bgColor:"", sourceType?:"auto", sourceId?:"<scene path>"}`. Column `{id:"c-...", label, width:160, bgColor:"", sourceType?:"auto", sourceId?, sourceKind?:"characters"}`. Cell keyed `"<rowId>-<colId>"` -> `{id, content, bgColor, textColor, bold, italic, align:"center", manualContent?, linkedSceneId?}`. The native "Sync from Scenes" button preserves hand-made rows (no `sourceType`) and tags generated ones `sourceType:"auto"`.

**Project layout** — `WRITING/STORYLINE/<Project>/` -> `Scenes/`, `Notes/`, `Archive/`, `Research/`, `Codex/{Characters,Locations,Items,Lore}/` (all built-in), `System/` (plugin-owned — the sync writes none of it), `Exports/`.
