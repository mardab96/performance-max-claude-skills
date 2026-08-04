# Worked example: full audit of one PMax campaign

A complete pass over a real-shaped account, showing what the skills produce
and how one finding changes another. Numbers are illustrative; the arithmetic
is real and reproducible from the sample files in this folder.

Account: retail, 1,240 SKUs, one PMax campaign, one brand Search campaign.
Period: 30 days. Spend 38,412. Reported conversions 196. Target CPA 60.

---

## Step 1. Conversion signal quality audit

**Verdict: no, this campaign is not optimising toward money.**

| Conversion action | Primary | Value | What it really represents | Risk | Recommendation |
|---|---|---|---|---|---|
| Purchase | yes | dynamic | Revenue | none | keep |
| Add to cart | yes | 25 | Intent, not revenue | high | `do_now` demote |
| Newsletter signup | yes | 25 | Nothing yet | high | `do_now` demote |

Two of three primary actions carry a fixed 25 while representing no revenue,
which crosses `conversion.value_spread_flag`. Of 196 reported conversions, 118
are carts and signups. The campaign has learned that carts are the cheap win.

**Everything below inherits this.** Confidence caps at `medium` until the
signal is fixed, and no scaling recommendation is issued this session.

---

## Step 2. Product spend concentration

Run: `python3 ../scripts/spend_concentration.py sample-product-report.csv --target-cpa 60`

```
products                    96
total_cost              38412.12
top_block_size              24
top_block_share_pct       71.5
concentration_flag       false
concentration_basis  top 24 of 96 products (25.0% of catalogue)
                     hold 71.5% of spend; flag requires the
                     catalogue share to be 20% or less
zero_conversion_products    24
flagged_tail_products       23
flagged_tail_cost      15138.35
```

**Verdict: the zero tail is the finding, not the concentration.**

25% of the catalogue holding 71.5% of spend is ordinary retail shape, so
`listing_group.spend_concentration` does not fire and no split is
recommended. What does fire is the tail: 23 products have each spent at least
three times target CPA with zero conversions, together 15,138, which is 39% of
the campaign budget.

Two top spenders also run below target: SKU-TOP-013 at 90% ROAS and
SKU-TOP-014 at 140%.

`approval_needed` on excluding the flagged tail. `investigate` on the two top
spenders, checking price competitiveness before excluding, because a 140% ROAS
product on a 60% margin may still be profitable.

---

## Step 3. Product feed blockers

Reconciliation: **1,240 in feed, 1,190 approved, 610 serving.**

The gap that matters is the second one. 580 approved products never served,
and sampling shows 400 sit outside the listing group structure entirely.

**This changes step 2.** The concentration figures above describe the 610
products that serve, not the catalogue. Their shares are provisional until the
400 excluded products are either included or deliberately excluded.

---

## Step 4. Brand cannibalization audit

Brand Search: 3,100 spend, 148 conversions, CPA 20.95.
Blended PMax CPA on purchases only: 38,412 / 78 = 492.

Search categories: 9 of 31 carry the brand name, roughly 29%, above
`brand.overlap_flag`. Brand CPA is far below `brand.cpa_gap_flag`.

**Verdict: strong case.** Estimated 20-35 of the 78 purchases are branded
demand the brand campaign wins at a twentieth of the cost.

`approval_needed` on brand exclusions, with the consequence stated: reported
PMax ROAS falls, blended account CPA improves.

---

## Step 5. Scaling and learning-phase guardrail

**Verdict: freeze.**

Not because the campaign is unstable, but because three approved changes are
queued: conversion goal demotions, a tail exclusion and brand exclusions. The
first is a formal reset (`learning.reset_triggers`).

Sequence, rather than all at once:

1. Fix the conversion signal. Wait `learning.duration`.
2. Exclude the flagged tail and resolve the 400 excluded products.
3. Brand exclusions. Wait `learning.judgement_window`.
4. Re-read. Only then consider a budget step of `budget.step`.

Doing all three in one week makes the next readout unattributable, which is
how accounts end up with four months of changes nobody can evaluate.

---

## Step 6. Weekly readout, for the client

"Last month the campaign spent 38,412 and reported 196 sales, but only 78 of
those were actual purchases. The rest were people adding to basket or joining
the mailing list, which the campaign had been told to treat as sales worth 25
each, so it has been buying the cheap ones. We are fixing that first.

Two other things: nearly 40% of the budget went to products that have not sold
anything at all, and a chunk of what the campaign claims is being won by your
brand campaign anyway at a twentieth of the cost.

We are making these changes one at a time over the next six weeks rather than
together, so we can tell which one worked. Nothing needs a decision from you
this week. The one call worth making early is whether to keep spending on the
23 products that have never sold, and we would recommend stopping."
