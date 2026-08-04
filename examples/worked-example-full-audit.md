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

**Everything below inherits this.** `AGENTS.md` is explicit about what a
failed signal audit does: every later verdict in the session drops to `low`
confidence and scaling recommendations are withdrawn. So everything below is
`low`, and that is not a formality. It means these findings are worth acting on
in order of size, not worth defending to a client as precise.

---

## Step 2. Product spend concentration

Run: `python3 ../scripts/spend_concentration.py sample-product-report.csv --target-cpa 60`

```
products                    96
total_cost              38412.12
top_block_size              24
top_block_share_pct       71.5
concentration_flag       false
concentration_basis  top 24 of 96 SPENDING products (25.0% of
                     them) hold 71.5% of spend; flag requires
                     that share to be 20% or less. NOTE:
                     spending products are only those with cost
                     in the export, not the full catalogue
zero_conversion_products    24
flagged_tail_products       23
flagged_tail_cost      15138.35
```

**Read the denominator before the verdict.** The export has 96 rows because
the Google Ads product report only lists products that spent something. The
catalogue is far larger; step 3 gets to that. So every share below is a share
of spending products, not of the catalogue, and that distinction decides the
next paragraph.

**Verdict: the zero tail is the finding, and the concentration needs a second
look.**

`listing_group.spend_concentration` requires both halves: a small slice of the
catalogue and 70%+ of spend. Here the top block is 25.0% of spending products,
above the 20% half, so the flag does not fire and no split is recommended.

But the flag not firing is not the same as the concentration being healthy, and
this is where the AND in the threshold can hide a finding. Checking the health
half separately: of the 24 products in the top block, 10 have zero conversions
and hold 7,767 of spend, which is 28.3% of the block. So the block is not
simply carrying the campaign. Report both: the flag is off, and more than a
quarter of the top block is dead weight.

What fires cleanly is the tail: 23 products crossing
`listing_group.zero_tail_flag`, together 15,138, which is 39.4% of campaign
spend.

Two top spenders also run below target: SKU-TOP-013 at 90% ROAS and
SKU-TOP-014 at 140%.

`approval_needed` on excluding the flagged tail. On the two top spenders, the
answer depends on a number this account has not supplied. At 60% gross margin,
breakeven is a ROAS of 167%, so 90% and 140% are both losses. At 80% margin,
breakeven is 125% and the 140% product is marginally profitable while the 90%
one is not. `investigate`, and the thing to investigate is the margin, not the
price.

---

## Step 3. Product feed blockers

Reconciliation: **1,240 in feed, 1,190 approved, 610 serving.**

The gap that matters is the second one. 580 approved products never served,
and sampling shows 400 sit outside the listing group structure entirely.

**This reconciles step 2 rather than contradicting it.** Three different
counts are in play and they are not the same thing: 1,240 products exist in the
feed, 610 got impressions, and 96 spent money. The product report in step 2
lists only the 96, which is why its denominator looked small.

**It does change what step 2's shares mean.** They are shares of spending
products, and 400 products are excluded by listing group structure so they
never had the chance to spend. Until those 400 are either included or
deliberately excluded, every percentage in step 2 describes a partial
catalogue. Say so wherever those percentages travel, including to the client.

---

## Step 4. Brand cannibalization audit

Brand Search: 3,100 spend, 148 conversions, CPA 20.95.
PMax CPA on purchases only: 38,412 / 78 = 492.

Search categories: 9 of 31 carry the brand name. No search terms report was
supplied.

**Verdict: confirmed in kind, unknown in size.** Two things are worth separating
here, because collapsing them is the easy mistake.

What is measured: nothing about the branded share. 9 of 31 is a count of
category labels, and one category can hold most of the volume.
`brand.overlap_flag` measures branded conversions from the search terms report,
which was not supplied, so the flag is uncomputed rather than crossed. There is
a reason to look; there is no measured size, and any number stated here would
be invented.

What is also not clean: the CPA comparison. 492 is PMax cost over purchases
only, while 20.95 is brand cost over all 148 of its conversions. The brand
campaign runs on the same account-level goals, so it is almost certainly
carrying the same cart and newsletter inflation that step 1 found in PMax. Like
for like, the brand figure would rise. The gap is real and large; the ratio is
not 23:1 and should not be quoted as one.

`do_now` on pulling the search terms report, which converts this whole step
from an estimate into a number. Brand exclusions stay `approval_needed` and
should wait for it, with the consequence stated: reported PMax ROAS falls,
blended account CPA improves.

---

## Step 5. Scaling and learning-phase guardrail

**Verdict: freeze.**

Not because the campaign is unstable, but because three approved changes are
queued: conversion goal demotions, a tail exclusion and brand exclusions. The
first is a learning event on our reading of Google's "composition change"
(`learning.reset_triggers`), which is worth saying because the whole sequence
below rests on it and Google does not list conversion goal changes by name.

Sequence, rather than all at once:

1. Fix the conversion signal. Wait `learning.duration`.
2. Exclude the flagged tail and resolve the 400 excluded products.
3. Brand exclusions. Wait `learning.judgement_window`.
4. Re-read. Only then consider a budget step of `budget.step`.

Doing all three in one week makes the next readout unattributable, which is
how accounts end up with four months of changes nobody can evaluate.

---

## Step 6. Weekly readout, for the client

"In July the campaign spent GBP 38,412 and reported 196 sales. Only 78 were
actual purchases. The rest were baskets and mailing-list signups, which the
account counts as sales worth 25 each, so the campaign has been buying the
cheap ones. We are fixing that first.

Separately, GBP 15,138 went to 23 products that have not sold anything at all.
(There are 24 products with no sales; the 24th has spent too little to be worth
acting on, so this figure covers the 23 that have.)

One decision for you: whether to keep spending on those 23. We would stop.
Everything else can wait, and we are making the changes one at a time over the
next two months so we can tell which one worked.

One caveat on the figures: 400 of your products are currently excluded from the
campaign by how it is built, so the percentages describe the part of the
catalogue that is running, not all of it. We will come back to you on that by
the end of the month."

Word count: 148, against the skill's 200-word limit. Three quantities the
reader has to hold: how much of the reported sales figure is real, how much
went to products that never sold, and how many products are excluded. The
supporting figures inside each of those do not count as separate things to
remember. The earlier draft ran 218 words and asked the reader to hold six
quantities, breaking both rules of the skill it was demonstrating.

---

## What this example could not see

Deliberately included, because every skill in the pack is required to produce
this section and the flagship example was previously the one document that
skipped it.

- **The branded share.** Step 4 works from category labels, which give a case
  but not a size. The search terms report would turn it into a number and was
  not available here.
- **Per-placement cost.** Not reported by Google at all. The channel split
  would be available and was not pulled for this example.
- **Margin.** Every product verdict above is about revenue. Two of the products
  recommended for exclusion could be profitable on margin and this example
  cannot tell.
- **The 400 excluded products.** They have never had the chance to spend, so
  nothing here describes them.

## Missing data

The search terms report, the channel performance report, product-level margin,
and the listing group configuration that excludes 400 products.

## Approval gates

Nothing above has been done. Demoting two conversion actions, excluding 23
products, adding brand exclusions and resolving the listing group exclusions
are four separate decisions, each needing a human yes, and the sequencing in
step 5 exists so they do not land at once.
