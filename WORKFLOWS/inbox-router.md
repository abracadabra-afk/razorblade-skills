---
type: workflow
name: inbox-router
trigger: sort the inbox
aliases: [route the inbox, process the inbox, file my inbox, run the inbox router, empty the inbox]
inputs: [raw mixed items in INBOX.md ⚡ Inbox]
outputs: [items filed into Vibes / Tasks / Workflows / Life / Knowledge / Business / _BACKLOG intakes; ambiguous items left in INBOX Needs-review; a sort-log line + run report]
lane: os
status: active
last_updated: 2026-06-15
---

# WORKFLOW: inbox-router

## When to use
CRE says **"sort the inbox"** (or has dumped a pile into [[INBOX]] and wants it filed), or the scheduled ingest task fires. This is the universal triage: one inbox in, the domain books out. The router **classifies and dispatches only** — it does NOT do each book's deep processing (it doesn't weave Vibes or anchor fragments; it drops items into each book's intake zone, and that book's own workflow runs later).

> Renamed-bucket note (2026-06-14 restructure): Vibebook→**Vibes**, Taskbook→**Tasks**, LifeBook→**Life**, DoBook→**Workflows** (brand retired). Two new routing targets added: **Knowledge** and **Business**. As connectors are added (calendar, email, etc.), the router stays the single write-path from any source into a domain — a connector is just another intake into INBOX.

## Core discipline
- **Auto-file the confident; review-bin the rest.** High-confidence items get filed immediately; ambiguous or spans-two-books items stay in INBOX's **🔍 Needs review** with the candidate books + reasoning. Never guess on a low-confidence item — and never pester CRE item-by-item. (This makes the router safe to run **unattended on a schedule**.)
- **Capture text is preserved verbatim** when filing to Vibes (no inline provenance that would pollute a creative fragment). Provenance lives in the sort log, not inside creative text.
- **Voice-note intent hints (from the dictation-runner).** An item may be immediately preceded by an HTML comment like `<!-- voice-note 2026-06-14 · intent: file under marketing · confidence: uncertain -->`. That intent is CRE's own spoken steer routed here by the [[WORKFLOWS/dictation-runner]] - treat it as a **strong** classification signal (often enough to lift a borderline item to high-confidence and file it). Still file the item body **verbatim**; never carry the comment into the filed note (provenance lives in the sort log).
- File-tools write rule (`^obs-020`); verify writes with the file tools, not a bash read (`^obs-014`).

## The routing table (book definitions the classifier uses)

| Book | Folder / target | Files items that are… |
|---|---|---|
| **Vibes** | `VIBES/CAPTURE.md` → ⚡ Inbox | Creative/intellectual fragments — thoughts, quotes, theories, craft lessons, images, "these two ideas connect." **Open loops** to keep alive. |
| **Tasks** | `TASKS/TASKS.md` → ⚡ Inbox | Personal/author **to-dos** — actionable, dischargeable ("call X", "send the newsletter", "renew domain"). **Closed loops.** A task with a date still goes here. |
| **Workflows** | `WORKFLOWS/_WORKFLOWS.md` → ⚡ Intake | **Automation/skill/workflow ideas** — "we should have a skill that…", "automate the X step." (Raw idea only; building it is a separate act.) |
| **Life** | `LIFE/REFERENCE/<note>` or `LIFE/<domain>/` | **Personal facts/data** — birthdays, contacts, key dates, and finance/fitness/food/mental-health notes (incl. recipes). A date with no action is reference data, not a task. **Personal** money/contacts. |
| **Knowledge** | `KNOWLEDGE/<area>/` | **Durable, reusable human learning** — research, methods, craft technique, book highlights, human (non-LLM) skills. Reusable beyond one project. |
| **Business** | `BUSINESS/<area>/` | **Author/media-company material** — sales/royalties/distribution (KDP), contracts, business finance/admin/tax, the Substack publication, marketing, social, branding, business contacts. **Company** money/contacts. |
| **_BACKLOG** (special) | `_BACKLOG.md` (matching lane section) | **AI-OS engineering tasks** — "rebuild the canon-sync skill", "fix the preflight bug", vault/workflow build work. Distinct from Tasks' life/author to-dos. |

**Tie-breakers:**
- *Task vs. fact with a date:* is there an action? action → Tasks; pure date-to-remember → Life.
- *Personal to-do vs. _BACKLOG:* is it about the vault/AI-OS itself? → _BACKLOG; about CRE's life/writing → Tasks.
- *Idea vs. automation idea:* a creative/story idea → Vibes; an idea for the *system to do something* → Workflows.
- *Vibes vs. Knowledge:* a raw creative spark / open loop to keep alive → Vibes; a durable, reusable method/research/lesson to look up later → Knowledge.
- *Business vs. Life:* company money/contacts/contracts → Business; personal money/contacts/dates → Life. (The art/business test: would it exist if nothing were ever sold? No → Business.)
- *Business asset vs. to-do:* a business fact/document (sales figure, contract, marketing copy) → Business; an actionable business to-do ("renew ISBN") → Tasks.
- *Cleanly separable multi-item* (e.g. "Mom's birthday May 3 — get her a gift"): split into a Life fact **and** a Tasks task. *Not cleanly separable* → Needs review.

> Note: creative manuscripts (novels, short fiction) are managed through the fiction pipeline (chapter folders), not dumped via the inbox. A creative *spark* → Vibes; drafting a piece is a separate, deliberate act in WRITING.

## Steps

### Step 1 — Vault sentinel + load
Confirm `_DIRECTIVES.md` frontmatter (the `^obs-004` guard). Read [[INBOX]] (Inbox + Needs-review), and the book anchors so the routing definitions are current.

### Step 2 — Segment
Split the Inbox into discrete items: by blank line, by bullet/checkbox, or by obvious topic boundary. One captured thought = one item. Don't merge unrelated lines; don't split a single multi-sentence thought.

### Step 3 — Classify
For each item, assign the best-fit book using the routing table, with a **confidence**: high (file) / low (review). Watch for: a secret/credential (DIR-001 → do not file into any note; flag in the report, tell CRE to move + rotate); a cleanly-separable multi-item (split); a spans-two-books item that won't separate (→ review). If an item carries a leading `<!-- voice-note … intent: … -->` comment, weight that spoken intent heavily (see Core discipline); a clear directive (e.g. *task*, *file under marketing*) usually settles the book.

### Step 4 — File (confident items)
Append each high-confidence item to its target's intake zone, preserving CRE's wording:
- **Vibes** → under `VIBES/CAPTURE.md` "⚡ Inbox" (verbatim, no inline tag — the weave anchors it later).
- **Tasks** → under `TASKS/TASKS.md` "⚡ Inbox" as `- [ ] <item>`.
- **Workflows** → under `WORKFLOWS/_WORKFLOWS.md` "⚡ Intake" as `- <idea>`.
- **Life** → the right `REFERENCE/` note (create + link from `_REFERENCE` if a new category) or the matching domain folder.
- **Knowledge** → the matching `KNOWLEDGE/<area>/` note (create + note in the report if a new area).
- **Business** → the matching `BUSINESS/<area>/` note (create + note in the report if a new area).
- **_BACKLOG** → the matching lane section as a `- [ ]` item.
Remove filed items from INBOX's Inbox.

### Step 5 — Review-bin the rest
Leave low-confidence / unsplittable items in INBOX's **🔍 Needs review**, each with: the item, the 2 candidate books, and one line on why it's ambiguous. Don't auto-file these.

### Step 6 — Log + report
Append a dated line to INBOX's **Sort log** (counts per book). Bump `last_updated` on every file touched. Report to CRE a compact table: *item → book* for everything filed, plus the Needs-review list to rule on. If anything went to Vibes, note it'll be picked up by the next weave (manual "weave the vibebook" or the scheduled weave task).

## Stop conditions
- Inbox empty → "nothing to sort," stop.
- Secret/credential detected → do not file it anywhere; flag + advise rotate (DIR-001).
- A target intake is missing/renamed → halt that item to Needs review with a note; don't create books ad hoc (except a new `REFERENCE/` category note under Life, or a new `<area>/` note under Knowledge/Business, which is expected).

## Notes
- Router dispatches only; each book's own workflow (e.g. `weave-vibebook`) does the deep processing.
- Safe to run **unattended on a schedule** (auto-file confident, review-bin the rest). Pipeline order when chained: **inbox-router → weave-vibebook** (router files new fragments into Vibes' inbox; the weave then anchors + connects them).

## Logging
On completion, append an entry to [[_CHANGELOG]] under the `os` lane (or note in the INBOX Sort log for routine/scheduled runs).
