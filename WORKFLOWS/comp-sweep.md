---
type: workflow
name: comp-sweep
status: built
trigger: "sweep the comps" / "run the comp sweep"
lane: writing-ops (Lane 5)
created: 2026-07-13
built: 2026-07-13
governed-by: "[[DECISIONS/2026-07-13 ghost-river-shelf|dec-003]]"
input: "[[BUSINESS/MARKETING/COMP SET]]"
output: "BUSINESS/MARKETING/COMP LISTINGS/"
cadence: monthly
---

# comp-sweep

Walk the ruled comp set in Chrome, extract a fixed field set from each listing, and write **one dated snapshot note per book**. Capture only. It never interprets, never ranks, never proposes action — that line is what keeps the downstream read honest.

Input: [[BUSINESS/MARKETING/COMP SET]] (CRE-founded, dec-003-governed). Output: `BUSINESS/MARKETING/COMP LISTINGS/`.

## Position & guards

- **Attended, never scheduled.** Amazon's bot detection makes headless sweeping fragile and ToS-adjacent. CRE kicks it off.
- **Capture only.** No analysis, no recommendations, no "what this means." A sweep that editorializes is a sweep whose numbers you stop trusting.
- **Never invents a row.** The set is `COMP SET.md`. If a book is not on the board, it is not swept — no "while I was there" additions.
- **Verify, never recall** (`^obs-179`). Every field comes off a loaded page. The AI does not supply an author, title, imprint, or ASIN from memory. It fabricated two in one session (a phantom author "Sodergren"; a phantom Volpe title *Say Goodbye*) and both were caught only by a page load.
- **Point-in-time.** Rank and price are snapshots. A re-sweep creates a **new dated note**, never an overwrite. Rank movement over time is the entire product.

## The five constraints that cost a session to learn

Do not rediscover these.

1. **Amazon throttles in-page `fetch()`.** A JS loop fetching DP pages from the page context hangs and returns nothing. **Navigate each listing normally.** This caps a run at ~8–12 books, which is why the comp set is capped at 9. Adding a row means retiring a row.
2. **Never key an extracted field `author`** (`^obs-178`). The Chrome extension's redaction layer pattern-matches the **key name**, not the value, and returns `"[BLOCKED: Sensitive key]"`. The DOM read succeeds; the value is destroyed on the way out. **Key it `by`, map to `author` on write.** The selector was never wrong — five rows were captured with a blank author column before the cause was spotted. General rule: when a scraped field comes back empty, distinguish *selector missed* from *value redacted* before "fixing" a selector that works.
3. **The Kindle format swatch reads `$0.00` on any KU title.** `#tmm-grid-swatch-KINDLE .slot-price` shows the KU-member price. The real buy price is `#kindle-price` — which is **absent on non-KU listings**. Read `#kindle-price` first, fall back to the swatch. Get this wrong and every KU competitor looks free.
4. **Carousels are lazy-loaded and frequently sponsored.** Ghost River's "also bought" carousel holds 5 items and they are *ads*. Do not treat carousel contents as a co-purchase signal without checking for sponsorship.
5. **Never capture `{{meta:name:*}}`-class data.** Amazon's meta tags carry live session/CSRF tokens (DIR-001).

## Verified selectors

Live-tested 2026-07-13 against `B08H4ZWB5R`, `B08TW3LBRQ`, and the eight comp-set DPs.

| Field | Selector | Note |
|---|---|---|
| title | `#productTitle` | |
| **by** | `#bylineInfo .author a` | **key it `by`, not `author`** — `^obs-178` |
| series | `#seriesBulletWidget_feature_div` | "Book 2 of 9: …" or empty |
| rating | `#acrPopover` → `title` attr | "4.3 out of 5 stars" → `4.3` |
| ratings_count | `#acrCustomerReviewText` | "(4,830)" → `4830` |
| price_kindle | `#kindle-price` **else** `#tmm-grid-swatch-KINDLE .slot-price span` | the KU trap |
| price_print | `#tmm-grid-swatch-PAPERBACK .slot-price span` | |
| kindle_unlimited | presence of `.a-icon-kindle-unlimited` | |
| bsr | `#detailBulletsWrapper_feature_div` text → split `"Best Sellers Rank:"` → split `"in Kindle Store"` | strip `#` and commas |
| category_ranks | `#detailBulletsWrapper_feature_div .zg_hrsr li` | array |
| publisher / pub_date / pages | detail bullets + `#rpi-attribute-book_details-*` | |
| has_aplus | presence of `#aplus` | |
| description | `#bookDescription_feature_div` | full sales copy |
| cover | `#landingImage` → `src` | |

Field shape mirrors `launch_competitors` in the Inkwell Supabase project — that schema was designed for exactly this and is a free spec. Writes go to **vault notes, not Supabase** (CRE-ruled); keeping the shape means a later push into `launch_competitors` is trivial if the KDP launcher resurrects.

## Procedure

**Step 0 — read the ground.** `COMP SET.md` (the board + the exclusions) and dec-003. If a row on the board contradicts dec-003, stop and surface it; do not sweep it.

**Step 1 — announce the run.** List the ASINs about to be walked and the count. If the count exceeds 12, stop: the set has outgrown the sweep and needs a retirement, not a longer run.

**Step 2 — walk each listing.** For each ASIN, in order:
- `navigate` to `https://www.amazon.com/dp/<ASIN>` (normal page load — never `fetch()`)
- run one extraction against the verified selectors, keying the author field **`by`**
- if any field returns empty, check the redaction trap before touching the selector

**Step 3 — write one dated snapshot note per book** to `BUSINESS/MARKETING/COMP LISTINGS/`:

`<Title> — <Author> — YYYY-MM-DD.md`

Frontmatter is the field shape (serialized YAML, DIR-004 — never hand-formatted). Body carries the snapshot table, category ranks, and the blurb. **Always sweep Ghost River in the same run** — a comp board without your own row is useless.

**Step 4 — write the run report** to `BUSINESS/MARKETING/COMP LISTINGS/_BOARD.md` (regenerated each run): the staircase, every row's BSR delta since the previous sweep, and nothing else. **No interpretation.** If a number moved, say by how much; do not say why.

**Step 5 — flag, don't fix.** Any listing that failed to resolve, any field that came back empty, any book that has vanished or changed edition — report it and stop. A silently-missing row is worse than a failed run.

## Exclusions (standing)

- **Drew Strickland — *Murder in the Mountains*.** Two snapshot notes sit in `COMP LISTINGS/` from the 2026-07-13 category walk, captured **before** dec-003 was ruled. It is a weird-western/rural mystery — off-shelf. The notes are kept as the record of the walk that produced the ruling. **Never sweep it.**
- The Publisher Rocket scrape in `launch_competitors` (King, Crouch, Sager) — market ceiling, not a comp set.

## Cadence

**Monthly.** BSR swings hard day to day; weekly snapshots are noise dressed as signal. If real rank *history* is wanted, Keepa has a legitimate API and tracks BSR over time — a better data source than any scrape, and worth buying before building anything clever here.

## Downstream

`comp-read` (analysis + action plan, gated) — **not yet built.** Do not let this skill drift into it. dec-003's honest ceiling stands: re-shelving and comp-tracking make the *other* levers aim right; they do not substitute for them.
