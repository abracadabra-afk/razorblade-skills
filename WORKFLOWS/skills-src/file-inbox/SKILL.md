---
name: file-inbox
description: Remote FILE intake — ingest a file (doc, sheet, PDF, image) dropped into _FILE INBOX/ into the right vault domain while keeping the original. Use when CRE says "run the file inbox," or on the file-inbox-runner scheduled task (polls _FILE INBOX/, cron 15,45). Stage A (deterministic runner.py) extracts content + proposes a domain; this skill is Stage B, the semantic call a script can't make — read each _extracted/*.md staging note and either file a CONFIDENT + structured extraction straight into its domain intake (moving the ORIGINAL to the domain's _sources/ folder, linked from the derived note) or summarize an AMBIGUOUS / spans-domains / unsupported file to INBOX for the inbox-router. Every file yields two outputs — derived facts + the kept original (external = source of truth, note = mirror). Guards — DIR-001 (secrets never filed), DIR-004 (serialized YAML), ^obs-004 sentinel, ^obs-103 staged-runner. Do NOT use it to draft chapter prose from a file (a desk action) or to delete an original (CRE's call).
---

# file-inbox

You are running CRE's **remote FILE intake** — the document sibling of [[WORKFLOWS/dictation-runner|dictation-runner]] (which did this for voice). The INBOX front door takes *text* CRE types or pastes; it can't take a *file*. This intake adds the missing path: **drop any file in one folder; a polling task reads it, files its contents into the right domain, and keeps the original.**

Canonical reference: `WORKFLOWS/file-inbox.md`. This is the AI-trigger surface; that doc is the in-vault canon.

---

## The core idea: every file produces two outputs

A dropped file is not one thing to file — it's two:

1. **Derived data** — the facts *inside* the file, ingested into a domain. A birthday spreadsheet → date entries in `LIFE/REFERENCE`; a royalty CSV → figures in Business.
2. **The original file** — kept for safekeeping in that domain's `_sources/` folder, with the derived note linking back to it.

That dual output is the vault's standing **connector discipline** ([[_VAULT MAP]]) applied to files: *the external file is the source of truth; the vault derives.* The spreadsheet is canonical; the birthday note is the regenerable, queryable mirror — the same relationship as `draft.md` → `canon-sync`.

Some files only want output #2 (a signed contract PDF: keep it whole, derive just a pointer/summary, don't shred it into facts). So make a per-file call: **derive-and-store** (a sheet of facts) vs. **store-and-index** (a document kept whole).

---

## Two stages — extract-then-route

```
phone / desktop (any file) --Dropbox--> _FILE INBOX/<file>
            |
  STAGE A . deterministic (runner.py, no LLM)
   detect_kind -> extract (csv/xlsx/ods/docx/odt/pdf-text; images -> needs-vision)
   -> propose_domain (keyword heuristic) -> write _extracted/<file>.md
   -> move original to processed/
            |
  STAGE B . THIS SKILL (the Cowork session)
   for each new _extracted/*.md not in _extracted/done/ :
     read extraction + proposal -> DECIDE what to ingest + where
     CONFIDENT + structured  -> file facts into the domain + move original to <domain>/_sources/ + link it
     AMBIGUOUS / spans / unsupported -> summarize to INBOX (+ link to staged original)
     log ONE consolidated line per file to _CHANGELOG
```

**Stage A is the runner; Stage B is you.** Stage A only *proposes* a domain — the semantic decision (what to ingest, where, derive-vs-keep-whole) is Stage B's, because it has the extracted content, the inbox-router's routing table, and vision for images.

---

## The fork (uncertainty resolves to INBOX)

The bias mirrors the voice runner: **when unsure, resolve to INBOX**, because that branch is non-destructive (a summary + link, the router can review-bin it) and no original is moved into a domain until the domain is settled — so a wrong guess is always cheap and recoverable.

Stage A's deterministic proposal cues (filename + extracted text), which you honor and can override:

- **Life** — birthday / birthdate / DOB / anniversary / contacts / phone / address / recipe / health logs.
- **Business** — invoice / royalty / payout / KDP / sales / earnings / contract / ISBN / tax / 1099 / publishing / marketing / Substack.
- **Knowledge** — research / study / paper / article / reference / method / technique / craft / book highlight.
- **no strong cue → INBOX** (you + the router decide).

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

## Sole write-path preserved

The inbox-router stays the **sole write-path into a domain for genuinely uncertain items.** file-inbox is allowed to file a **confident, structured** extraction straight into its domain — exactly as dictation-runner's *fiction* branch goes straight to the chapter pipeline rather than through INBOX, while its *non-fiction* branch defers to the router. Anything you aren't confident about becomes an INBOX summary (+ original link) and the router rules it.

## Scope boundary

- **In scope:** drop → extract → stage → (confident) file facts + store original, or (ambiguous) INBOX summary. All non-destructive until the domain is settled.
- **Stays a desk action:** anything that should become *prose* in a chapter (e.g. a `.docx` of dictated scene text) is a manuscript action, not an intake — route it through the fiction pipeline at the desk, not here. file-inbox ingests *reference/data*; it does not draft.

---

## Steps

### Step 0 — Vault sentinel
Confirm `_DIRECTIVES.md` frontmatter is `type: ai-os-brain` / `file: directives` (the `^obs-004` guard) before any domain write. Mismatch/missing → halt and ask which folder is the vault.

### Step 1 — Run Stage A (or pick up its output)
On the scheduled task, run the Stage A extractor first. Install deps to a fixed root-fs target — **never** `--break-system-packages` (it lands in `~/.local` on the shared full device → ENOSPC, `^obs-102`):
```
pip install --no-cache-dir --target /tmp/fi_libs odfpy openpyxl pdfplumber python-docx pyyaml
```
**Stage the runner off the mount, then run it (`^obs-103` structural kill).** NEVER run `runner.py` directly off the Dropbox mount — the mount can serve a stale, TRUNCATED copy of the *script* that crashes `python3` with a SyntaxError. Read `runner.py` via the **file tools** and **write it to the session outputs folder** (session scratch, not Dropbox-synced, so never stale-truncated), then:
```
OUT=$(ls -d /sessions/*/mnt/outputs | head -1)
PYTHONPATH=/tmp/fi_libs VAULT_ROOT="<vault>" python3 "$OUT/runner.py"
```
`runner.py` reads `VAULT_ROOT` for every vault path, so the *code* runs from the clean staged copy while reads/writes land in the **real** vault. Sanity: `py_compile "$OUT/runner.py"`; if it won't compile, re-read via the file tools — never fall back to the mount. It prints JSON of what it processed; each result carries a `route` (`domain` / `inbox` / `needs-vision`), a `proposed_domain`, and a `source_dest`. If `processed: 0`, stop — nothing to do, no log entry.

### Step 2 — For each new `_FILE INBOX/_extracted/*.md` not in `_extracted/done/`
Read the staging note (frontmatter `proposed_domain` / `proposed_source_dest` / `route` / `kind`, and the `## Extracted content`). For an image (`route: needs-vision`), read the original in `processed/` natively (vision) to pull text/data.

### Step 3 — DIR-001 secrets check (before anything else)
If the content is credentials / API keys / tokens / passwords, do **NOT** file it anywhere. Note it in the `_CHANGELOG` line, flag CRE to move + rotate, move the staging note to `done/`, and skip the rest for that file.

### Step 4 — Decide + file
Is the domain clear and the content structured?
- **Confident path:** ingest the facts into the chosen domain, honoring the inbox-router's definitions (birthdays → a `LIFE/REFERENCE` dates note; royalty figures → Business). Then **move the original** `processed/<file>` → `<domain>/_sources/<file>` and make the derived note link to it (`[[_sources/<file>]]` or a relative path). For a keep-whole document (a contract PDF), store-and-index: move the original + write a pointer/summary note, don't shred it into facts. File-tools for note edits (`^obs-020`); serialize any derived frontmatter (DIR-004).
- **Ambiguous path** (spans two domains / unsupported / low confidence): append a short summary item to `INBOX.md` under `## ⚡ Inbox` with a leading hint comment `<!-- file-note <date> · proposed: <domain> · source: _FILE INBOX/processed/<file> -->` and a link to the original; leave the original in `processed/`. The inbox-router files it later.

Then move the staging note to `_extracted/done/`.

### Step 5 — Log
Append ONE consolidated line per processed file to `_CHANGELOG.md` (top-insert via the file tools), e.g. `- file-inbox: family_birthdays.ods [sheet→Life] (3 birthdays → LIFE/REFERENCE; original → LIFE/REFERENCE/_sources/)` or `- file-inbox: scan.pdf [pdf→INBOX] (unclear; summarized to INBOX, original in processed/)`.

---

## Run modes
- **Unattended (scheduled `file-inbox-runner`):** empty drop zone = silent no-op. Never block on a gate — ambiguous files defer to INBOX rather than stalling.
- **Manual:** "run the file inbox" — same steps, on demand.

## Guards (inherited)
- **DIR-001 — secrets:** a file of keys/tokens/passwords is flagged and **never** filed into any note; tell CRE to move + rotate.
- **DIR-004 — serialized YAML:** every derived/staging frontmatter is emitted via `yaml.safe_dump` and parse-gated; never hand-formatted.
- **DIR-005 — OS-doc edits:** the `_CHANGELOG` line and any `_SKILLS MAP` edits use the file tools only (no `patch_vault_file` / whole-file MCP rewrite), verified by re-reading via the file tools.
- **Vault sentinel (`^obs-004`):** confirm `_DIRECTIVES.md` before writing into a domain.
- **Mounted-script integrity (`^obs-103`):** never execute `runner.py` off the bash mount — always run a file-tools-staged outputs/`/tmp` copy with `VAULT_ROOT` set (code from the clean copy, data from the real vault).

## Files writes / must-not
- **Writes:** facts into a domain intake + the moved original into `<domain>/_sources/` (confident); or a summary into `INBOX.md` (ambiguous); the staging note into `_extracted/done/`; one line in `_CHANGELOG.md`.
- **Must not:** never delete an original (it lives in a domain `_sources/` or `processed/`; deletion is CRE's call); never file a secret; never draft chapter prose; never write straight into a domain for a genuinely uncertain item (that's the router's job).

## Stop conditions
- `processed: 0` / empty drop zone → silent no-op, no log entry.
- A secret surfaces (DIR-001) → flag, don't file, log the flag, move staging note to `done/`.
- A staging note can't be parsed / an extractor failed (flagged in the note) → summarize to INBOX with the failure noted; don't fabricate the missing content.
- Genuinely ambiguous domain → INBOX, never a guess into a domain.

## What this is NOT
- Not the voice intake — that's `dictation-runner` (audio → transcript/draft).
- Not the typed front door — that's `INBOX` + the `inbox-router`; this skill *feeds* the router for uncertain files.
- Not a manuscript tool — it ingests reference/data, it does not draft prose.

## Build status
**status: active** (workflow); `.skill` packaging is this source (`^backlog-file-inbox-skill-package`). Source-ahead of any install until desktop `pack-skills.ps1` + Save-skill.
