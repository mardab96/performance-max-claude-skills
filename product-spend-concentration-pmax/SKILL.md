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
2. Check `listing_group.spend_concentration`, then check the health of the top
   block SEPARATELY, whether or not the flag fired. The threshold has an AND in
   it, so it stays silent when the catalogue share is above 20%, and a silent
   flag is not a clean bill of health. Count the zero-conversion products inside
   the top block and their spend. A block that holds most of the budget while a
   quarter of it never converted is a finding the flag will never give you.
3. Split the top spenders into three buckets: beating target, near target,
   below target.
4. Find the zero bucket separately, using `listing_group.zero_tail_flag`.
   It is expressed as a multiple of the account's own target CPA rather than a
   currency amount, so it travels between accounts.
5. Check the tail. Products with impressions and almost no clicks usually have
   a price, image or title problem rather than a bidding problem, and belong
   in the feed skill, not this one.
6. If margin data exists, redo the top-spender split on margin instead of
   revenue. Products that beat ROAS target and lose money are the most
   expensive thing this skill can find.

## Decision rules

- A product crossing `listing_group.zero_tail_flag` -> `approval_needed` on
  exclusion from the listing group, unless the product is new or seasonal, in
  which case `monitor` with a date.
- Concentration above `listing_group.spend_concentration` with top products
  beating target -> `ignore`. This is a working campaign and splitting it
  usually costs more than it returns.
- Top block crossing `listing_group.top_block_dead_weight` -> `investigate`,
  and report it even when the concentration flag is off.
  Report both facts in the same sentence: the flag is off, and this much of the
  block is dead weight.
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

Input: 180 products, campaign cost 24,000, target ROAS 400%, target CPA 60.
Top 12 products hold 17,040, which is 71% of spend. Ten of them run 380-520%
ROAS. Two run 90% and 140% and cost 1,500 and 1,400. That leaves 6,960 across
the remaining 168 products, of which 23 have spent between 180 and 280 each
with zero conversions, totalling 5,290.

Reading: the 180 rows are spending products, not the catalogue (see
Denominators in `thresholds.md`); the full feed is larger and this share does
not describe it. 12 of 180 spending products is 6.7%, holding 71% of spend, so
both halves of `listing_group.spend_concentration` are crossed. Ten of the
twelve beat target, so the concentration itself is healthy and no split is
recommended. `listing_group.zero_tail_flag` sits at 3 x 60 = 180, and all 23
zero-conversion products are at or above it, so the whole tail is flagged. The
two weak top spenders average 115% ROAS against a 400% target, which is under
a third of target, not half.

Output: "A 23-product zero tail and two weak top sellers are costing 8,190 at
below-target return, which is 34% of the campaign." Table, then
`approval_needed` on excluding the tail (5,290) and on excluding the two top
spenders (2,900).

Both top spenders are losses, and this is where margin turns a soft verdict
into a hard one. At 60% gross margin, breakeven is a ROAS of 167%: every 1 of
spend has to return 1.67 of revenue before the gross profit covers it. The two
products run at 90% and 140%, so they lose 0.46 and 0.16 of gross profit per 1
spent. Without margin they merely look below target; with it they are
provably unprofitable, which is why the margin question is worth chasing before
this call rather than after.

## Guardrails

- Never call a product a loser on ROAS alone when margin data exists.
- Never exclude on a sample smaller than a few target CPAs of spend.
- Never treat concentration as a defect by itself.
- Do not edit listing groups or feeds. Recommend, and let a human approve.
