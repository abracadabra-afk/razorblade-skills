---
type: workflow
name: link-sweep
status: spec
trigger: "sweep the links" / "run the link sweep"
lane: writing-ops (Lane 5)
created: 2026-07-16
governed-by: "[[DECISIONS/2026-07-16 ghost-river-1e-distribution|dec-016]]"
input: "[[BUSINESS/MARKETING/AUTHOR AND BOOK LINKS]]"
output: "registry updates + SYSTEM/reports/ run reports; site grid updates ride the attended deploy leg"
cadence: weekly during the dec-016 propagation window, monthly once stable, park when the watch set is empty
---

# link-sweep

Walk the ruled retailer watch set for CRE's books and detect **buy buttons coming alive or dying**, keeping [[BUSINESS/MARKETING/AUTHOR AND BOOK LINKS]] (the registry, source of truth) and the site's `retailers:` grid current. The capture sibling of comp-sweep, pointed at CRE's own listings instead of competitors'.

Born 2026-07-16: dec-016 re-enabled Ingram print + relisted the ebook wide via D2D the same day the site's universal-book-link grid shipped (branch `book-links`). The 1–6 week propagation window is the sweep's whole reason to exist.

## Position & guards

- **The registry is the board.** The probe set = the registry's live links (regression check) + its ruled watch note (discovery). **Never invents a row**: a retailer not on the watch set is never added — it goes to Needs-review. (comp-sweep's rule, same reason.)
- **A title record is not a link** (dec-016's lesson — the dormant B&N/Walmart pages). LIVE means a working buy path: price shown + a functioning buy/add-to-cart control. Orderable-on-request at a library/store counts for the libraries row only.
- **Additions are safe-ops; removals gate.** A watch-set channel found live → write it to the registry with a provenance comment (the channel was pre-ruled by dec-016; the URL is verified off the loaded page). A previously-live link found dead → **flag, never delete** (could be throttling, region, or a transient) — CRE rules removals.
- **The site leg is attended.** Registry → `retailers:` frontmatter → build → grep dist → push is the `book-links` pattern: desktop git/build via windows-cli (DIR-007), never through the sandbox mount. An unattended run stops at the registry + report.
- **Verify, never recall** (`^obs-179`). Every URL comes off a loaded page. No supplying links, prices, or retailer names from memory.
- **Affiliate hygiene rides the link touch.** When a link is added or edited: Bookshop.org uses CRE's affiliate URL once enrolled (dec-016 leg 5); the Amazon buy button's `tag=books2read02-20` (B2R's tag) is queued for swap/strip — never propagate a third party's affiliate tag onto a new link.
- **DIR-001:** never capture meta-tag/session-token data off retailer pages.

## Inherited comp-sweep traps (do not rediscover)

1. **Never key an extracted field `author`** — the Chrome extension redacts on key NAME. Key it `by` (`^obs-178`).
2. **No in-page `fetch()` against Amazon** — navigate normally; cap a run at ~8–12 page loads.
3. **Client-rendered storefronts lie to web_fetch.** Bookshop.org and B&N return empty shells (verified 2026-07-16). Order of escalation: `web_fetch` → Chrome navigate. If both fail, report NOT-VERIFIABLE, never guess.

## The cheap check first (DIR-008)

**Step 0 of every run: load `books2read.com/ghostriver`.** The B2R UBL is D2D's own propagation dashboard — its retailer buttons appear as D2D delivers. One page load tells you which ebook channels are worth probing this run. Only channels B2R shows (plus the print/non-D2D set: Bookshop, B&N print, Walmart) get individual probes.

## The watch set (current — dec-016 wave)

| Channel | Format | Identifier / probe | Status 2026-07-16 |
|---|---|---|---|
| Kobo | ebook | via B2R, then direct listing | D2D relisted, propagating |
| Apple Books | ebook | via B2R, then direct listing | D2D relisted, propagating |
| B&N Nook | ebook | via B2R, then direct listing | D2D relisted, propagating |
| Libraries (OverDrive et al.) | ebook | via B2R | D2D relisted, propagating |
| B&N print | print | ISBN 9781735676920 | dormant record — watch for buy button |
| Walmart | print | ISBN 9781735676920 **+ title+author search** | **LIVE 2026-07-21** — new copy $16.99, sold+shipped by Walmart.com (item 647899467) |
| Bookshop.org | print | ISBN 9781735676920; affiliate URL once enrolled | Ingram re-enabled 07-16 |

<!-- link-sweep 2026-07-21 (run 1): the watch-set print ISBN read 9781735676926 — an invalid ISBN-13
     (ISBN-10 1735676926 with a 978 prefix and no recomputed check digit). Bookshop.org returned
     ZERO results on it and the live product on 9781735676920. Corrected to 9781735676920, verified
     off three independent loaded pages (B&N ean=, Bookshop ean=, Walmart's ISBN-10/13 pairing).
     Left uncorrected this would have failed every Bookshop/Walmart probe forever. -->

Live set (regression check each run): Amazon ebook `B08H4ZWB5R` · Amazon paperback `1735676926` · Audible `B0BTQ6G9YX` · Godless `godless.com/products/ghost-river-by-chad-ryan` · B2R `books2read.com/ghostriver`.

## Procedure

**Step 0 — cheap check.** Load the B2R page; diff its retailer buttons against the registry. Nothing new + watch set unchanged → report "no movement," stop.

**Step 1 — probe the movers.** For each channel B2R newly shows, and each dormant print record: load the listing, apply the live-buy-button test, capture the URL off the page.

> **Never probe a retailer on ISBN alone (`^obs-205`, run 1).** Walmart's ISBN search returned only the third-party *pre-owned* record while the first-party "Sold and shipped by Walmart.com" new copy sat at the top of a **title + author** search — so the sweep reported the channel dark when it was live. Run both keys (`?q=<ISBN>` *and* `?q=<title> <author>`) before recording any channel dark, and confirm the item is CRE's off the product page (author line + ISBN, never the title alone — "Ghost River" collides heavily). A **thin or wrong-item** result is as untrustworthy as a null one, and more dangerous: it looks like a successful probe.

**Step 2 — write the registry** (safe-op, additions only): new live link under the book's section with an HTML provenance comment (`<!-- link-sweep YYYY-MM-DD -->`). Dead-link findings go to the report as flags, not edits.

**Step 3 — report** to `SYSTEM/reports/YYYY-MM-DD-link-sweep.md`: found-live table, still-dark table, regressions, NOT-VERIFIABLEs. No interpretation.

**Step 4 — the site leg (attended only).** Mirror new registry links into `src/content/books/<book>.md` `retailers:`, trim `retailersNote` as channels land, build, grep dist (the whitespace trap), commit, push, verify preview. Unattended: queue this as the report's "deploy pending" line instead.

## Cadence

Weekly while the dec-016 window runs (started 2026-07-16 — CRE executed Ingram + D2D same day). Monthly once all watch-set channels resolve. Park (status note in the registry) when the watch set is empty — a sweep with nothing to watch is noise.

## Downstream / not this skill

- **comp-sweep** — competitor listings. Never merge the two: this sweep's subject is CRE's own books.
- **link-audit** — vault-internal broken wikilinks. Different "link," different doctor.
- Back-matter link updates (KDP/ACX re-uploads) are CRE's seat; the report lists candidates.
