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
3. State the inventory scope precisely (`thresholds.md`, Mechanism claims):
   brand exclusions apply to Search,
   Shopping AND YouTube search inventory. Display, Discover and non-search
   YouTube serving is not covered, so some branded-looking impressions persist
   and that is expected. Getting this wrong in the other direction is worse:
   a branded YouTube SEARCH impression after an exclusion is a real failure of
   the list, and calling it expected tells the user to stop looking at a live
   leak.
4. Measure what is still getting through, and be strict about what you are
   allowed to measure it with. `brand.overlap_flag` is defined on branded
   CONVERSIONS from the search terms report; with only Search categories you
   cannot compute it and must not compare against it. A category weight is a
   label weight. If you have the search terms report, compute the flag properly
   and say so. If you do not, say the flag is uncomputed and that the residual
   category weight cannot tell you whether the exclusions are working.
5. Separate two different failures: exclusions missing variants, versus
   exclusions working while the remaining branded appearance sits in
   uncovered inventory. The fix differs and confusing them wastes weeks.
6. If competitor brands are excluded too, check whether that was intentional.
   Excluding competitor terms removes a genuine acquisition channel and is a
   business decision, not a hygiene one.

## Decision rules

- A plausible variant missing from the list -> `do_now` on adding it. Cheap,
  reversible, no learning cost.
- Brand terms still appearing on Search or Shopping, and campaign-level
  negative keywords are not in use -> `do_now` on those. They are the more
  direct tool for specific terms than a brand exclusion list alone.
- Brand terms appearing in YouTube SEARCH -> negatives are the wrong tool.
  They cover Search and Shopping inventory and not YouTube search
  (`thresholds.md`, Mechanism claims), while brand exclusions do. Fix the
  exclusion list instead, and do not send anyone chasing that leak with a tool
  that cannot reach it.
- Branded CONVERSIONS still above `brand.overlap_flag`, measured from the
  search terms report, with a complete variant list -> the remaining exposure
  is in uncovered inventory; `monitor`, and stop treating it as a leak.
- Only Search categories available -> `needs_data`. The flag is uncomputed, and
  no verdict on whether the exclusions are working can be issued from a label
  weight. Say what would settle it: the search terms report.
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
Search categories still show branded weight around 12%. No search terms report
supplied. Known variants also include "northwnd" (a common typo) and "nw
logistics" (the legacy name).

Reading: two plausible variants are missing, and that part is checkable without
any conversion data. The 12% is not. It is a label weight, and
`brand.overlap_flag` is defined on branded conversions from the search terms
report, so the flag is uncomputed rather than passed. Three weeks is also
inside `learning.judgement_window`, so even with the right data a verdict would
be premature. Two independent reasons to refuse the verdict, and only one of
them goes away with time.

Output: "Two variants missing. Whether the exclusions are working is not
answerable from this input." Add the two variants, `do_now`, because that is
cheap, reversible and does not depend on the missing data (`AGENTS.md`,
precedence rule 7). The working-or-not question is `needs_data`: it needs the
search terms report, and it needs six weeks. Re-read at 30 August with that
report in hand. Note explicitly that some branded
impressions will never disappear because display, Discover and non-search
YouTube serving sit outside what a brand exclusion reaches, but that anything
branded appearing in YouTube SEARCH would be a real gap and worth checking
separately.

## Guardrails

- Never call an exclusion broken before `learning.judgement_window` has
  passed.
- Never present brand exclusions as covering all inventory.
- Never add competitor exclusions without naming the acquisition cost.
- Do not edit exclusion lists. Recommend, and let a human approve.
