---
name: product-spend-concentration-pmax
description: Finds the products absorbing a Performance Max campaign's budget without returning it, and separates a healthy concentration from a feed-mix problem. Use for retail PMax when overall ROAS is acceptable but nobody knows which products are carrying it.
---

# Product spend concentration

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

A retail PMax campaign has a shopping feed and the account owner cannot name
which products are making the money and which are eating it.

## Required input

- Product report for the campaign: product ID or title, cost, conversions,
  conversion value, impressions, clicks.
- Target ROAS or target CPA.
- Product margin data if it exists, even roughly, even as a category average.

Without margin data every verdict below is about revenue, not profit. Say that
out loud in the output rather than letting the reader assume otherwise.

## Analysis workflow

1. Sort products by cost descending and compute cumulative share of spend. Run
   `../scripts/spend_concentration.py <export.csv> --target-cpa <n>` rather
   than doing this by eye; it owns the arithmetic so two runs on the same
   export cannot disagree about the numbers. The decision rules below stay
   here.
2. Check `listing_group.spend_concentration`. Concentration alone is not a
   defect; concentration with weak returns is.
3. Split the top spenders into three buckets: beating target, near target,
   below target.
4. Find the zero bucket separately: products with meaningful spend and zero
   conversions. Use the account's own CPA to decide what "meaningful" means,
   not a fixed number. A product that has spent one target CPA without
   converting is noise; one that has spent three is a finding.
5. Check the tail. Products with impressions and almost no clicks usually have
   a price, image or title problem rather than a bidding problem, and belong
   in the feed skill, not this one.
6. If margin data exists, redo the top-spender split on margin instead of
   revenue. Products that beat ROAS target and lose money are the most
   expensive thing this skill can find.

## Decision rules

- Spend above roughly 3x target CPA with zero conversions [heuristic] ->
  `approval_needed` on exclusion from the listing group, unless the product is
  new or seasonal, in which case `monitor` with a date.
- Concentration above `listing_group.spend_concentration` with top products
  beating target -> `ignore`. This is a working campaign and splitting it
  usually costs more than it returns.
- Concentration above the same threshold with top products below target ->
  `investigate` the feed mix. The campaign is spending where the feed lets it,
  not where the money is.
- Positive ROAS and negative margin on a top spender -> `do_now`. Name it
  explicitly; this defect survives every ROAS-based review.
- No margin data -> every verdict is labelled revenue-only and confidence caps
  at `medium`.

## Output format

Open with one line naming the single product or product group costing the most
for the least return.

| Product | Cost | Share of spend | Conv | ROAS | Margin-aware | Recommendation |
|---|---|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: 180 products, campaign cost 24,000, target ROAS 400%. Top 12 products
carry 71% of spend. Ten of them run 380-520% ROAS. Two run 90% and 140%. A
further 23 products have spent between 400 and 900 each with zero conversions;
target CPA is 60.

Reading: concentration is above `listing_group.spend_concentration` but is
mostly healthy, so the campaign is not the problem. The two underperforming
top spenders are worth about 3,900 of spend at roughly half the target return.
The 23 zero-conversion products have each spent between 6x and 15x target CPA,
well past the flag.

Output: "Two top sellers and a long zero tail are costing roughly 9,000 at
below-target return." Table, then `approval_needed` on excluding the zero
tail, `investigate` on the two top spenders (check price competitiveness
before excluding, because a 140% ROAS product with 60% margin may still be
profitable).

## Guardrails

- Never call a product a loser on ROAS alone when margin data exists.
- Never exclude on a sample smaller than a few target CPAs of spend.
- Never treat concentration as a defect by itself.
- Do not edit listing groups or feeds. Recommend, and let a human approve.
