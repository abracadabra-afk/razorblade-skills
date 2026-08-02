---
type: workflow
name: reviewer-sweep
status: draft (source authored 2026-08-01; desktop pack pending)
trigger: "sweep the reviewers" / "run the reviewer sweep"
lane: writing-ops (Lane 5)
created: 2026-08-01
governed-by: "[[BUSINESS/MARKETING/ARC DISTRIBUTION]]"
input: "[[BUSINESS/MARKETING/REVIEWER SET]]"
output: "BUSINESS/MARKETING/reviewer-outreach.xlsx"
cadence: quarterly (re-verify accepting-status; it drifts)
---

# reviewer-sweep

Walk the ruled scope of the BookSirens reviewer directory in Chrome, capture a fixed field set per reviewer, enrich each with the real contact method from the reviewer's own policy page, and write rows into `reviewer-outreach.xlsx`. **Capture + verify only. It never sends, never drafts a pitch, never ranks who to approach — CRE rules that.**

Input: [[BUSINESS/MARKETING/REVIEWER SET]] (scope + schema). Output: `BUSINESS/MARKETING/reviewer-outreach.xlsx`.

## Position & guards

- **Attended, never scheduled.** Needs a live Chrome session; the directory + policy pages are JS-rendered. CRE kicks it off. Sibling of comp-sweep / link-sweep in this respect.
- **The sweep never sends.** This is the hard line. It compiles a list and verifies contact methods. Every outreach email is personalized to the reviewer's stated policy and sent by CRE (or a future gated, per-reviewer draft step). **Automated blasting of this list is the single move most likely to get an author blacklisted** — it is out of scope by design, not by omission.
- **Free + indie-accepting + on-genre only in the pitch pool.** Paid reviewers → quarantine tab. A reviewer who doesn't accept Indie Authors is excluded. Honor every card's "Does not accept" list.
- **Verify, never recall.** Every field comes off a loaded page. Never supply an email, status, or genre from memory.
- **Stage-2 status overrides the card** (see below). The directory's green "Currently Accepting" flag is not evidence.

## The two stages

### Stage 1 — listing capture
For each in-scope directory page (see REVIEWER SET → Source URLs):
1. Navigate to the page (`get_page_text` returns all visible cards as structured text).
2. Click **"Show More"** and re-read until the full list is loaded (222 horror reviewers ≈ 22 loads).
3. Per card, capture: reviewer/blog name, handle, accepting-flag, genre preferences, "Does not accept" exclusions, accepts-from, cross-posts-to, formats, blog URL, last-post date, compensation, follower count.
4. Drop rows that fail scope: paid → quarantine; no Indie Authors → drop; off-genre → drop; excluded genre matches GR → drop.

### Stage 2 — policy-page enrichment (the load-bearing step)
The contact method is **not on the card.** For each surviving row:
1. `find` the card's "Contact" link → click it (opens the reviewer's own site in a new tab).
2. `get_page_text` the policy page. Extract: **contact method** (email / web form / social DM / tour-company / closed), **contact detail** (the address or form URL), and **verified status** (OPEN / CLOSED / EBOOKS-NO / UNMONITORED / physical-only).
3. **The policy page wins over the directory card.** Record the verified status even when it contradicts the green flag.
4. Close the spawned tab; move to the next.

> Founding-walk proof this stage is mandatory: *damppebbles* — card says accepting, policy says closed since Dec 2025. *So many books* — card says accepting, email is unmonitored + no ebooks. 2 of the first 4 enriched were effectively closed behind a green flag. (DIR-010: a platform's capability/status surface is a dated claim, not a probe.)

## Mechanics that will bite otherwise

1. **Reviewer-name link vs. Contact link.** The reviewer's *name* links to their blog homepage; the **"Contact"** and **"Review Policy"** links (in the card's GET IN TOUCH block) open the policy page. Use the Contact link, not the name.
2. **Contact links open a NEW tab** (`window.open`), one per click. Batch a few clicks, read the resulting tabs, then close them — don't let tabs pile up.
3. **Contact hrefs are not in the accessibility tree** as plain links — `read_page` won't surface the destination. You must click to resolve where it goes.
4. **Expect throttling on heavy pagination.** Navigate normally; a full-scope run is long — cap a session at a few sub-genre pages and resume, rather than one marathon.
5. **No structured email field exists.** Emails live in prose ("email me at x@y.com"), sometimes deliberately obfuscated. Extract from the policy text; if none, the method is form/social/closed.

## Output

Append/update rows in `reviewer-outreach.xlsx` per the REVIEWER SET schema (main tab; paid → quarantine tab; codes in legend tab). A re-sweep **refreshes** verified-status + last-checked on existing rows (liveness drifts) and adds new reviewers; it does not blow away CRE's manual Outreach-status column.

## What this is NOT
Not the BookSirens **Promote** platform funnel (that's automatic, paid, [[BUSINESS/MARKETING/ARC DISTRIBUTION]]). Not a pitch writer. Not a sender. It builds and verifies the list; the human does the outreach.
