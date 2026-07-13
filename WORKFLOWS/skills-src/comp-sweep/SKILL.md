---
name: comp-sweep
description: Walk CRE's ruled Amazon comp set in Chrome and write one dated snapshot note per book — the capture leg of the Ghost River competitive board. Use when CRE says "sweep the comps," "run the comp sweep," "snapshot the comps," or wants the tracked competitor listings re-captured. Reads BUSINESS/MARKETING/COMP SET.md (CRE-founded, dec-003-governed), navigates each listing normally, extracts a fixed field set (BSR, rating, ratings count, Kindle/print price, KU, category ranks, A+, series, publisher, blurb), and writes dated snapshots to COMP LISTINGS/ plus a regenerated _BOARD.md staircase. CAPTURE ONLY — never interprets, ranks, recommends, or adds a book that is not on the board. Attended, never scheduled. Three load-bearing traps — never key an extracted field `author` (the Chrome extension redacts the key NAME and silently blanks it; key it `by`); never use in-page fetch() (Amazon throttles it — navigate normally, capping a run at 8-12 books); read #kindle-price before the format swatch (the swatch reads $0.00 on KU titles). Do NOT use it to analyze the board (that is comp-read, unbuilt) or to clip an ad-hoc listing (that is the Web Clipper template).
---

# comp-sweep

The capture leg of the competitive board. You walk the ruled comp set, pull a fixed field set off each live listing, and write dated snapshots. You do not interpret. Interpretation is a separate, gated skill that does not exist yet — do not drift into it.

Canonical doc: `WORKFLOWS/comp-sweep.md`. Input: `BUSINESS/MARKETING/COMP SET.md`. Governed by `DECISIONS/2026-07-13 ghost-river-shelf.md` (dec-003, ratified).

## Position & guards

- **Attended, never scheduled.** Amazon's bot detection makes headless sweeping fragile and ToS-adjacent. CRE kicks it off.
- **Capture only.** No analysis, no ranking, no "what this means." A sweep that editorializes is a sweep whose numbers stop being trusted.
- **Never invents a row.** If a book is not on the board, it is not swept. No opportunistic additions.
- **Verify, never recall.** Every field comes off a loaded page. Never supply an author, title, imprint, or ASIN from model memory — that fabricated a phantom author and a phantom book title in one session, both caught only by a page load (`^obs-179`). Genre names, small-press imprints, and indie titles are exactly where the model sounds most expert and is least reliable.
- **Point-in-time.** A re-sweep writes a NEW dated note. Never overwrite. Rank movement over time is the whole product.

## The three traps (load-bearing — do not rediscover)

1. **Never key an extracted field `author`** (`^obs-178`). The Chrome extension's redaction layer matches the **key name**, not the value, and returns `"[BLOCKED: Sensitive key]"`. The DOM read succeeds; the value dies on the way out. **Key it `by`; map to `author` on write.** When any field comes back empty, check the redactor before "fixing" a selector that already works.
2. **Never use in-page `fetch()`.** Amazon throttles it — the loop hangs and returns nothing. **Navigate each listing normally.** This caps a run at ~8–12 books; the comp set is capped at 9 for exactly this reason. Adding a row means retiring a row.
3. **`#kindle-price` before the swatch.** `#tmm-grid-swatch-KINDLE .slot-price` reads **$0.00 on any KU title** (it shows the member price). The real buy price is `#kindle-price`, which is absent on non-KU listings. Read it first, fall back to the swatch. Otherwise every KU competitor looks free.

Also: never capture `meta:name:*` fields — Amazon's meta tags carry live session/CSRF tokens (DIR-001).

## Verified selectors

| Field | Selector |
|---|---|
| title | `#productTitle` |
| **by** (→ author) | `#bylineInfo .author a` |
| series | `#seriesBulletWidget_feature_div` |
| rating | `#acrPopover` → `title` attr → split on space, take first |
| ratings_count | `#acrCustomerReviewText` → strip parens + commas |
| price_kindle | `#kindle-price` else `#tmm-grid-swatch-KINDLE .slot-price span` |
| price_print | `#tmm-grid-swatch-PAPERBACK .slot-price span` |
| kindle_unlimited | presence of `.a-icon-kindle-unlimited` |
| bsr | `#detailBulletsWrapper_feature_div` → split `"Best Sellers Rank:"` → split `"in Kindle Store"` → strip `#`/commas |
| category_ranks | `#detailBulletsWrapper_feature_div .zg_hrsr li` |
| publisher / pub_date / pages | detail bullets + `#rpi-attribute-book_details-*` |
| has_aplus | presence of `#aplus` |
| description | `#bookDescription_feature_div` |
| cover | `#landingImage?src` |

Field shape mirrors `launch_competitors` (Inkwell Supabase) so a later push there is trivial. Writes go to vault notes, not Supabase.

## Procedure

**0 — Read the ground.** `COMP SET.md` + dec-003. If a board row contradicts dec-003, surface it; do not sweep it.

**1 — Announce.** List the ASINs and the count. If count > 12, STOP: the set has outgrown the sweep and needs a retirement, not a longer run.

**2 — Walk.** Per ASIN: `navigate` to `https://www.amazon.com/dp/<ASIN>`, then one extraction against the selectors above (author keyed `by`). Include **Ghost River (B08H4ZWB5R)** in every run — a board without your own row is useless.

**3 — Write** one dated snapshot per book to `BUSINESS/MARKETING/COMP LISTINGS/<Title> — <Author> — YYYY-MM-DD.md`. Frontmatter = the field shape, serialized YAML (DIR-004 — never hand-formatted, parse-gate before treating as done). Body = snapshot table + category ranks + blurb.

**4 — Regenerate `COMP LISTINGS/_BOARD.md`**: the staircase (every row by BSR) and each row's delta since the previous sweep. Numbers only. If a number moved, say by how much; never say why.

**5 — Flag, don't fix.** Any listing that failed, any empty field, any book that changed edition or vanished — report it and stop. A silently-missing row is worse than a failed run.

## Standing exclusions

- **Drew Strickland — *Murder in the Mountains***. Off-shelf under dec-003 (weird-western/rural mystery). Two pre-ruling snapshot notes live in `COMP LISTINGS/` as the record of the walk that produced the ruling. **Never sweep it.**
- The Publisher Rocket scrape in `launch_competitors` (King, Crouch, Sager) — market ceiling, not comps.

## Cadence

Monthly. Daily BSR swing is noise. For real rank history, Keepa's API beats any scrape — say so rather than building something clever.

## What this skill never does

- Interpret, rank, score, or recommend (that is `comp-read`, unbuilt)
- Add a book that is not on the board
- Supply any name, title, or ASIN from memory rather than a page load
- Overwrite a previous snapshot
- Run unattended or on a schedule
