---
name: product-feed-blockers-pmax
description: Finds the feed problems stopping products from serving in Performance Max, separating hard disapprovals from the quiet quality issues that suppress reach without any warning. Use when products get no impressions, or before blaming bidding for a coverage problem.
---

# Product feed blockers

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

Part of the catalogue gets no impressions, Merchant Center shows disapprovals
nobody has read, or a retail campaign underspends its budget.

## Required input

- Merchant Center diagnostics: disapproved, pending, and active product
  counts, with reasons.
- Product report from Google Ads: impressions, clicks, cost by product.
- A sample of feed rows, ideally including a well-performing product and a
  non-serving one.
- The listing group structure, to check for products excluded by structure
  rather than by the feed.

## Analysis workflow

1. Reconcile three numbers before anything else: products in the feed,
   products approved in Merchant Center, and products with impressions in Ads.
   The gaps between them are the whole skill, and each gap has a different
   cause.
2. Feed to approved gap: disapprovals and pending review. Group by reason and
   rank by product count, not by how alarming the reason sounds.
3. Approved to serving gap: this is the quiet one. Approved products can still
   fail to serve because of listing group exclusions, missing GTIN, low
   quality images, price mismatch against the landing page, or simply losing
   every auction.
4. Check the fields that suppress without disapproving: missing GTIN or brand,
   thin titles, missing product type or google_product_category, no sale
   price, and availability that disagrees with the page.
5. Check price and availability consistency against the live landing page for
   a sample. A mismatch here is a suspension risk, not just a reach issue.
6. Rank findings by number of products affected multiplied by their commercial
   importance, and say when importance came from the user rather than data.

## Decision rules

- Any disapproval reason crossing `feed.disapproval_flag` -> `do_now`.
- Approved products with zero impressions over at least
  `learning.judgement_window` -> `investigate` listing group exclusions first,
  feed quality second, auction losses last. That order matters; most people
  start at the last one.
- Price or availability mismatch on any sampled product -> `do_now`. This
  escalates to account suspension if it spreads.
- Missing GTIN on branded resale products -> `do_now`; on own-brand products
  -> `ignore`, provided the brand field is set correctly.
- Merchant Center diagnostics unavailable -> `needs_data`. Do not infer feed
  health from Ads-side impressions alone.

## Output format

Open with the three-number reconciliation in one line: in feed, approved,
serving.

| Issue | Products affected | Type | Effect | Recommendation |
|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: 1,240 products in feed, 1,190 approved, 610 with impressions in the
last 30 days.

Reading: 50 products blocked by disapprovals, and 580 approved products that
never served. The second gap is 11.6 times larger than the first and nobody
was looking at it. Sampling shows 400 of the non-serving products sit outside
the listing group structure entirely, and 90 lack GTIN on branded resale
items.

Output: "1,240 in feed, 1,190 approved, 610 serving." The listing group gap is
the headline, `do_now`, because 400 products are excluded by structure rather
than by any feed problem. GTIN gap second. The 50 disapprovals, which is where
this review would normally have started, come third.

## Guardrails

- Never treat approved as serving.
- Never rank disapprovals above the approved-to-serving gap without checking
  which is larger.
- Never infer feed health from the Ads side alone.
- Do not edit feeds or Merchant Center settings. Recommend, and let a human
  approve.
