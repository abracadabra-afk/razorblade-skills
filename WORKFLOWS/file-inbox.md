---
type: workflow
name: file-inbox
lane: os
status: active
trigger: scheduled task `file-inbox-runner` (polls _FILE INBOX/, cron 15,45 * * * *) + manual "run the file inbox"
created: 2026-06-15
updated: 2026-06-16
purpose: Remote, drop-and-forget FILE intake. Drop ANY document/spreadsheet/PDF/image into _FILE INBOX/ from phone or desktop (Dropbox). A polling task EXTRACTS the content, decides what to ingest and where, files the facts into the right domain, and stores the ORIGINAL for safekeeping in that domain's _sources/. The document sibling of dictation-runner.
---

# file-inbox

> **The problem this kills:** the INBOX front door takes *text* you type or paste — it can't take a *file*. So a spreadsheet of birthdays, a royalty CSV, or a contract PDF had no path into the vault: nothing read it, ingested what mattered, or stored the original safely. This adds the missing intake — **drop a file in one folder; a polling task reads it, files its contents, and keeps the original.** The file analog of [[WORKFLOWS/dictation-runner|dictation-runner]] (which did this for voice).

## The core idea: every file produces two outputs

A dropped file is not one thing to file — it's two:

1. **Derived data** — the facts *inside* the file, ingested into a domain. A birthday spreadsheet → date entries in `LIFE/REFERENCE`; a royalty CSV → figures in Business.
2. **The original file** — kept for safekeeping in that domain's `_sources/` folder, with the derived note linking back to it.

That dual output is the vault's standing **connector discipline** ([[_VAULT MAP]]) applied to files: *the external file is the source of truth; the vault derives.* The spreadsheet is canonical; the birthday note is the regenerable, queryable mirror — the same relationship as `draft.md` → `canon-sync`.

Some files only want output #2 (a signed contract PDF: keep it whole, derive just a pointer/summary, don't shred it into facts). So Stage B makes a per-file call: **derive-and-store** (a sheet of facts) vs. **store-and-index** (a document kept whole).

> **Design decisions (CRE, 2026-06-15):** originals are stored **per-domain** (`<domain>/_sources/`, next to the data they fed — maximally findable) rather than in one central store; trigger is **polling** (true drop-and-forget), parity with dictation-runner.

## Architecture — one polling loop, extract-then-route

```
phone / desktop (any file) --Dropbox--> _FILE INBOX/<file>
                                              |
              scheduled task "file-inbox-runner" wakes (~every 30 min)
                                              |
  STAGE A . deterministic (runner.py, no LLM)
   * detect_kind(): text / table / sheet / doc / pdf / image / unknown
   * extract(): pull text + tables (csv, xlsx/ods, docx/odt, pdf-text)
       - images: NOT OCR'd here -> staged route `needs-vision` for Stage B
       - scans/empty PDFs: flagged -> Stage B vision/OCR
   * propose_domain(): light keyword heuristic -> a PROPOSED domain (Life /
       Business / Knowledge / Workflows / Vibes) or INBOX when no strong cue
   * write _extracted/<file>.md  (extracted content + proposed domain +
       proposed <domain>/_sources/ destination)
   * move the original to processed/   (audit trail)
                                              |
  STAGE B . the Cowork session (this agent / the scheduled-task prompt)
   for each new _extracted/*.md not in _extracted/done/ :
     * read the extraction + the proposal
     * DECIDE what to ingest and where (the semantic call Stage A can't make)
     * CONFIDENT + structured  -> file the facts into the domain intake +
                                   move the ORIGINAL processed/<file> -> <domain>/_sources/<file>
                                   + write/append the derived note linking the original
     * AMBIGUOUS / spans-domains / unsupported -> summarize into INBOX with a
                                   link to the staged original; the inbox-router
                                   (+ its Needs-review) rules it. Original waits
                                   in processed/ until ruled.
     * DIR-001: a credentials-laden file is flagged, NEVER filed; tell CRE to move+rotate
     * move the staging note to _extracted/done/
   * log ONE consolidated line per file to _CHANGELOG
                                              |
  (decoupled) the inbox-router files any INBOX summaries on its own schedule.
```

**Why polling, not triggers:** same reason as the voice pipeline — every "who fires whom" hand-off is brittle and can't be driven from a phone. One scheduled task watching one folder removes them all. **Transport CUTOVER 2026-07-10 (`^backlog-server-transport`): phone capture now rides Nextcloud, not the Dropbox app.** Phone drops go to `VAULT TRANSPORT/_FILE INBOX` (Nextcloud app → aegis-moon → desktop Nextcloud client), and the desktop scheduled task **`vault-transport-sweep`** (`SYSTEM/maintenance/sweep-transport.ps1`, every 5 min, idle-≥60s guard, moves logged to `transport-sweep.log`) moves them into the vault's `_FILE INBOX/` — where this runner picks them up exactly as before (first proof: `Women - Charles Bukowski.mobi`, phone → server → desktop → vault, 2026-07-10). Drop zone, runner.py, and the scheduled-task prompt are all UNCHANGED (the sweep lives desktop-side because the Cowork sandbox can't see the Nextcloud folder). Dropbox remains the vault's own sync, and desktop drops straight into `_FILE INBOX/` still work.

## The fork (Stage A `propose_domain`, then Stage B rules)

Stage A only **proposes**; the semantic decision is Stage B's (it has the extracted content + the inbox-router's routing table + vision for images). The bias mirrors the voice runner: **uncertainty resolves to INBOX**, because that branch is non-destructive (a summary + link, the router can review-bin it) and no original is moved into a domain until the domain is settled — so a wrong guess is always cheap and recoverable.

Stage A's deterministic proposal cues (filename + extracted text):
- **Life** — birthday / birthdate / DOB / anniversary / contacts / phone / address / recipe / health logs.
- **Business** — invoice / royalty / payout / KDP / sales / earnings / contract / ISBN / tax / 1099 / publishing / marketing / Substack.
- **Knowledge** — research / study / paper / article / reference / method / technique / craft / book highlight.
- **no strong cue → INBOX** (Stage B + router decide).

This parallels the inbox-router's own routing table and tie-breakers ([[WORKFLOWS/inbox-router]]) — file-inbox reuses those definitions so a file and a typed note about the same thing land in the same place.

## Per-domain originals map (`<domain>/_sources/`)

| Proposed domain | Original stored at |
|---|---|
| Life | `LIFE/REFERENCE/_sources/` |
| Business | `BUSINESS/_sources/` |
| Knowledge | `KNOWLEDGE/_sources/` |
| Workflows | `WORKFLOWS/_sources/` |
| Vibes | `VIBES/_sources/` |
| INBOX (unsure) | stays in `_FILE INBOX/processed/` until ruled |

## Relationship to the inbox-router (sole write-path preserved)

The router stays the **sole write-path into a domain for genuinely uncertain items.** file-inbox is allowed to file a **confident, structured** extraction straight into its domain — exactly as dictation-runner's *fiction* branch goes straight to the chapter pipeline rather than through INBOX, while its *non-fiction* branch defers to the router. Anything Stage B isn't confident about becomes an INBOX summary (+ original link) and the router rules it. Net: confident files are filed directly; ambiguous files defer to the one human-in-the-loop triage you already trust.

## Scope boundary

- **Automated:** drop → extract → stage → (confident) file facts + store original, or (ambiguous) INBOX summary. All non-destructive until the domain is settled.
- **Stays a desk action:** anything that should become *prose* in a chapter (e.g. a `.docx` of dictated scene text) is a manuscript action, not an intake — route it through the fiction pipeline at the desk, not here. file-inbox ingests *reference/data*, it does not draft.

## Guards (inherited)

- **DIR-001 — secrets:** a file of API keys / tokens / passwords is flagged and **not** filed into any note; CRE is told to move + rotate.
- **DIR-004 — serialized YAML:** every staging note's frontmatter is emitted via `yaml.safe_dump` and parse-gated; never hand-formatted.
- **DIR-005 — OS-doc edits:** the `_CHANGELOG` line and any `_SKILLS MAP` edits use the file tools only (no `patch_vault_file` / whole-file MCP rewrite), verified by re-reading via the file tools.
- **Vault sentinel (`^obs-004`):** Stage B confirms `_DIRECTIVES.md` before writing into a domain.
- **Mounted-script integrity (`^obs-103`):** never execute `runner.py` off the bash mount — always run a file-tools-staged `/tmp` copy with `VAULT_ROOT` set (the *code* runs from `/tmp`, the *data* from the real vault), so a stale-mount truncation of the *script* can't run. Extends the DIR-005 stale-mount read guard to *executes*. See the run step.

## Dependencies (installed at runtime by the scheduled task)

```
pip install --no-cache-dir --target /tmp/fi_libs odfpy openpyxl pdfplumber python-docx pyyaml
```
Install to a fixed root-fs `--target` dir and put it on `PYTHONPATH` (this runner has no self-bootstrap), **not** `--break-system-packages` — the latter lands in `~/.local` on the shared full device (`/dev/sdc`) → ENOSPC (`^obs-102`). All pure-Python; no system binaries. `pyyaml` is required by the staging-note writer (DIR-004). Each extractor degrades gracefully: a missing lib (or a `.docx`/`.odt` that won't parse) falls back to a raw-XML strip and a flag in the note rather than crashing the run. **Upgrade path:** vendor the wheels offline (like the whisper model) to drop the per-run install; add image OCR (tesseract) if Stage-B vision proves insufficient.

## The scheduled task prompt (Stage A + B)

> Bootstrap is NOT required for this task. Do exactly this:
> 1. Install deps **without** `--break-system-packages` (it lands in `~/.local` on the shared full device → ENOSPC, `^obs-102`). This runner has no self-bootstrap, so install to a fixed root-fs dir and put it on `PYTHONPATH` at run time: `pip install --no-cache-dir --target /tmp/fi_libs odfpy openpyxl pdfplumber python-docx pyyaml` (reuse the same dir each run; if pip ENOSPCs, clear stale `/tmp/*` dep dirs first).
> 2. **Stage the runner off the mount, then run it (`^obs-103` structural kill).** NEVER run `runner.py` directly off the Dropbox mount — the mount can serve a stale, TRUNCATED copy of the *script* (the `^obs-073`/`^obs-095` hazard; a truncated script is wrong **behavior**, not just wrong data) that crashes `python3` with a SyntaxError. Instead always run a clean copy read via the **file tools** (cloud-authoritative): read `runner.py` via the file tools and **write it to the session outputs folder** (the Write tool reaches outputs, NOT sandbox `/tmp`; outputs is session scratch — not Dropbox-synced, so never stale-truncated — bash reads it at `/sessions/*/mnt/outputs/`); it is standalone — no sibling to stage. Then `OUT=$(ls -d /sessions/*/mnt/outputs|head -1); PYTHONPATH=/tmp/fi_libs VAULT_ROOT="<vault>" python3 "$OUT/runner.py"`. `runner.py` reads `VAULT_ROOT` for every vault path (drop zone, domain `_sources/`), so all reads/writes land in the **real** vault while the *code* runs from the clean staged copy — the mount copy of the script is never trusted (sanity: `py_compile "$OUT/runner.py"`; if it won't compile, re-read via the file tools, never fall back to the mount; you may instead bash-`cp` the outputs copy into `/tmp` and run there). It prints JSON of what it processed; each result carries a `route` (`domain` / `inbox` / `needs-vision`) and a `proposed_domain` + `source_dest`. If `processed: 0`, stop — nothing to do, no log entry.
> 3. Confirm `_DIRECTIVES.md` frontmatter (the `^obs-004` vault sentinel) before any domain write.
> 4. **For each new `_FILE INBOX/_extracted/*.md` not yet in `_extracted/done/`:**
>    - Read the staging note (frontmatter `proposed_domain` / `proposed_source_dest` / `route` / `kind`, and the `## Extracted content`). For an image, read the original in `processed/` natively (vision) to pull text/data.
>    - **DIR-001 check:** if the content is credentials/keys/tokens, do NOT file it anywhere; note it in the `_CHANGELOG` line and flag CRE to move + rotate. Move staging note to `done/`. Skip the rest.
>    - **Decide:** is the domain clear and the content structured? → file directly. Ambiguous / spans two domains / unsupported? → summarize to INBOX (see below).
>    - **Confident path:** ingest the facts into the chosen domain, honoring the inbox-router's definitions (e.g. birthdays → a `LIFE/REFERENCE` dates note; royalty figures → Business). Then **move the original** `processed/<file>` → `<domain>/_sources/<file>` and make the derived note link to it (`[[_sources/<file>]]` or a relative path). Use the file tools for the note edits (`^obs-020`); serialize any derived frontmatter (DIR-004).
>    - **Ambiguous path:** append a short summary item to `INBOX.md` under `## ⚡ Inbox` with a leading hint comment `<!-- file-note <date> · proposed: <domain> · source: _FILE INBOX/processed/<file> -->` and a link to the original; leave the original in `processed/`. The inbox-router files it later.
>    - Move the staging note to `_extracted/done/`.
> 5. Append ONE consolidated line per processed file to `_CHANGELOG.md`, e.g. `- file-inbox: family_birthdays.ods [sheet→Life] (3 birthdays → LIFE/REFERENCE; original → LIFE/REFERENCE/_sources/) ` or `- file-inbox: scan.pdf [pdf→INBOX] (unclear; summarized to INBOX, original in processed/)`.
> 6. Never delete an original — it lives in a domain `_sources/` (filed) or `processed/` (pending). Deletion is always CRE's call.

## Run modes

- **Unattended (scheduled):** empty drop zone = silent no-op. Never blocks on a gate — ambiguous files defer to INBOX rather than stalling.
- **Manual:** "run the file inbox" — same steps, on demand.

## Known v1 limits (tracked)

- **Domain proposal is a heuristic** (keyword + filename). It only *proposes*; Stage B (LLM) makes the real call and defaults uncertain files to INBOX. Upgrade path: LLM classify in Stage B (same as the voice runner's planned upgrade).
- **Images / scanned PDFs aren't OCR'd in Stage A** — they're routed `needs-vision` for Stage B to read natively. A purely offline run (no Stage B) would leave them staged. Upgrade path: tesseract OCR in Stage A if needed.
- **Per-run pip install** of the extractors. Upgrade path: vendor the wheels offline.
- **Stage B ingest is a documented prompt, not yet a deterministic skill** — packaging it as a `.skill` (like the rest of the pipeline) is a follow-up.

## Files

- `WORKFLOWS/file-inbox/runner.py` — Stage A orchestrator: scan, `detect_kind()`, `extract()` (csv/xlsx/ods/docx/odt/pdf/text), `propose_domain()`, `write_staging_note()`, move to `processed/`. Self-locating. `--selftest` prints classification over fixtures.
- `_FILE INBOX/` — drop zone (`README.md`, `_extracted/` + `done/`, `processed/`).
- `<domain>/_sources/` — per-domain originals store (created on first file filed there).
