---
name: listing-group-segmentation-pmax
description: Decides whether a retail Performance Max campaign should be split by product segment, and which split, using the campaign's own conversion volume as the constraint. Use when high and low margin products share one campaign, or when someone proposes a campaign per category.
---

# Listing group segmentation

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

Splitting is the most over-prescribed move in retail PMax. This skill exists
to say no more often than yes.

## Use this skill when

Someone wants to split a working campaign, or a single campaign genuinely
mixes products with incompatible economics.

## Required input

- Product report with cost, conversions, conversion value.
- Current listing group structure.
- Target ROAS, per segment if targets differ.
- Margin by product or category if it exists.
- Campaign conversion volume for the last 30 days.

## Analysis workflow

1. Start with the constraint, not the idea, and use the right floor for the
   unit you are counting. Monthly conversions divided by
   `conversion.volume_floor` is the ceiling on CAMPAIGNS. Divided by
   `asset_group.volume_floor` it is the ceiling on ASSET GROUPS. Mixing them up
   inflates the campaign count by a factor of two or three, which is how
   six-campaign proposals get waved through. Most proposed splits die here and
   should.
2. Identify whether the products genuinely have different economics: different
   margin bands, different target ROAS, different sales cycles. Different
   categories with the same economics are not a reason to split.
3. Check whether the current structure is already starving anything. A product
   segment getting almost no impressions inside a mixed campaign is the real
   argument for a split; a segment simply performing worse is not.
4. Model the split cost: each new campaign restarts learning
   (`learning.duration`), and the parent loses the volume the child takes.
5. Consider the cheaper alternatives first and say which you rejected:
   listing group subdivision inside the same campaign, a separate asset group,
   a campaign-level exclusion, or nothing.
6. Only then recommend a split, with the number of campaigns the volume
   supports, not the number the catalogue suggests.

## Decision rules

- Proposed campaigns exceed monthly conversions divided by
  `asset_group.volume_floor` -> `ignore` the split. Say the volume cannot feed
  it and name the number it can.
- Margin bands crossing `segment.margin_gap` with volume to support it ->
  `approval_needed` on a split by margin band, which is almost always a better
  cut than by category.
- A segment crossing `segment.starvation_flag` -> `investigate` starvation.
  This is the strongest genuine split argument.
- Same economics, different categories -> `ignore`. Recommend listing group
  subdivision for reporting instead, which costs nothing.
- Campaign below `conversion.volume_floor` -> never split. Consolidate
  instead.

## Output format

Open with one line: split or do not split, and the number of campaigns the
volume supports.

| Proposed segment | Monthly conv | Margin band | Starved | Verdict |
|---|---|---|---|---|

Then the rejected cheaper alternatives with one line each on why, then
`What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: one campaign, 140 conversions/month, catalogue of 6 categories. The
owner wants 6 campaigns. Margin runs 55-62% in four categories and 18-22% in
two.

Reading: 140 conversions divided by `asset_group.volume_floor` supports around
9-14 asset groups or roughly 2-3 campaigns, not 6. Category is the wrong cut
because four of them share economics. Margin band is the right cut and it
produces exactly two segments.

Output: "Split, but into two, not six." High-margin campaign covering four
categories, low-margin campaign covering two, each with its own target ROAS.
Rejected: split by category (volume cannot feed it), separate asset groups
(does not allow separate ROAS targets, which is the actual goal here).
Learning cost stated: both campaigns start fresh for up to
`learning.duration`.

## Guardrails

- Never recommend more campaigns than the conversion volume supports.
- Never split by category when the economics match.
- Never recommend a split without naming the cheaper option you rejected.
- Do not create or restructure campaigns. Recommend, and let a human approve.
