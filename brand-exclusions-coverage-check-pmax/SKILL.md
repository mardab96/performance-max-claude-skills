---
name: brand-exclusions-coverage-check-pmax
description: Checks whether the brand exclusions on a Performance Max campaign actually cover the brand, including misspellings, competitor brands and the inventory the exclusion does not reach. Use after adding brand exclusions, or when branded traffic keeps appearing despite them.
---

# Brand exclusions coverage check

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

Run this after `brand-cannibalization-audit-pmax` has made the case for
exclusions. That skill decides whether to exclude; this one checks whether the
exclusion works.

## Use this skill when

Brand exclusions are in place and branded categories still appear, or someone
wants to know why excluding the brand did not change anything.

## Required input

- The brand exclusion list currently applied, exact entries.
- PMax Insights, Search categories, from after the exclusions went live.
- Known brand variants: misspellings, spacing variants, legacy names, product
  brand names, the founder's name if it is used as a brand.
- Competitor brand names, if competitor traffic is a concern.

## Analysis workflow

1. Confirm the date range starts after the exclusions were applied. Categories
   from before tell you nothing about whether they work.
2. List every brand variant a real person might type. Misspellings, missing
   spaces, plurals, the .com typed as a word, the old company name. Compare
   against the applied list.
3. State the inventory limit plainly: brand exclusions apply to Search and
   Shopping inventory. Display, video and Discover serving is not covered, so
   branded-looking impressions can persist and that is expected, not a
   failure.
4. Check whether branded categories still carry meaningful conversion weight
   after the exclusion window. Compare against `brand.overlap_flag`.
5. Separate two different failures: exclusions missing variants, versus
   exclusions working while the remaining branded appearance sits in
   uncovered inventory. The fix differs and confusing them wastes weeks.
6. If competitor brands are excluded too, check whether that was intentional.
   Excluding competitor terms removes a genuine acquisition channel and is a
   business decision, not a hygiene one.

## Decision rules

- A plausible variant missing from the list -> `do_now` on adding it. Cheap,
  reversible, no learning cost.
- Branded categories still above `brand.overlap_flag` with a complete variant
  list -> the remaining exposure is in uncovered inventory; `monitor`, and
  stop treating it as a leak.
- Exclusions applied under `learning.judgement_window` ago -> `monitor` only.
  Any verdict now is premature.
- Competitor brands excluded without a stated reason -> `investigate`; name
  what the exclusion is costing before keeping it.
- No brand campaign running while exclusions are active -> `approval_needed`
  on reversing. The demand is being pushed away with nowhere to land.

## Output format

Open with one line: are the exclusions working, incomplete, or working while
the remaining exposure sits outside their reach.

| Variant | On list | Still appearing | Inventory | Recommendation |
|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: exclusions applied 3 weeks ago covering "northwind" and "north wind".
Search categories still show branded weight around 12%. Known variants also
include "northwnd" (a common typo) and "nw logistics" (the legacy name).

Reading: two plausible variants are missing. Three weeks is inside
`learning.judgement_window`, so the residual 12% cannot yet be read as
success or failure. 12% is below `brand.overlap_flag`, which suggests the
exclusions are largely doing their job.

Output: "Incomplete, but mostly working." Add the two missing variants,
`do_now`. Re-read at the six-week mark. Note explicitly that some branded
impressions will never disappear because display and video serving is outside
what a brand exclusion reaches.

## Guardrails

- Never call an exclusion broken before `learning.judgement_window` has
  passed.
- Never present brand exclusions as covering all inventory.
- Never add competitor exclusions without naming the acquisition cost.
- Do not edit exclusion lists. Recommend, and let a human approve.
