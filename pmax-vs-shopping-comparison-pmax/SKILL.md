---
name: pmax-vs-shopping-comparison-pmax
description: Compares Performance Max against a standard Shopping or Search campaign covering the same products, and says which one is actually winning once overlap and attribution are accounted for. Use when deciding whether to keep both, or when PMax was blamed for a decline that started elsewhere.
---

# PMax versus Shopping comparison

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

The comparison people usually run is invalid, because the two campaigns are
not independent. This skill exists to make it valid or to refuse it.

## Use this skill when

Both campaign types cover overlapping products and someone wants to know which
to keep, or PMax launched and a Shopping campaign declined at the same time.

## Required input

- Both campaigns: cost, conversions, conversion value, impression share where
  available, over the same date range.
- The product overlap between them: which SKUs appear in both.
- Campaign priority settings and any inventory filters.
- Launch dates and change history for both.
- Attribution model and conversion window for the account.

## Analysis workflow

1. Establish whether the campaigns compete for the same inventory. Where they
   overlap, PMax takes precedence over standard Shopping for the same product
   and account, so the Shopping campaign's decline may be mechanical rather
   than a performance verdict.
2. Check whether the comparison window is clean: no reset triggers
   (`learning.reset_triggers`) inside it for either campaign, and at least
   `learning.judgement_window` long.
3. Compare on the overlapping products only. Comparing total campaign numbers
   when the product sets differ measures the catalogue, not the campaign type.
4. Check attribution. With a data-driven model and overlapping journeys, a
   conversion credited to one campaign may have been assisted by the other.
   Say this explicitly rather than presenting the split as clean.
5. Look at combined performance before and after the second campaign launched.
   The only question that matters is whether the account made more money in
   total, not which campaign's row looks better.
6. If a decision is needed, frame it as a test with a stop condition rather
   than a permanent verdict.

## Decision rules

- Product sets overlap and no like-for-like comparison is possible ->
  `needs_data`. Say the comparison as asked cannot be answered and name the
  segmentation that would make it answerable.
- Combined account performance improved after the second campaign launched ->
  `ignore` the which-is-better question. Both are earning their place.
- Combined performance flat while one campaign's numbers rose -> the second
  campaign is absorbing existing demand. `investigate`, and treat the rise as
  reallocation rather than growth.
- Either campaign below `conversion.volume_floor` -> refuse the comparison and
  say why.
- A genuine decision is required -> `approval_needed` on a time-boxed test:
  pause one for at least `learning.judgement_window`, measure combined
  account performance, and state up front what result would reverse it.

## Output format

Open with one line: which campaign is winning, or a plain statement that the
comparison cannot be made with what is available.

| Metric | PMax | Shopping | Overlapping products only | Read |
|---|---|---|---|---|

Then the combined-account view, then `What this could not see`,
`Missing data`, `Approval gates`.

## Practical example

Input: PMax launched 12 June. Shopping campaign existing since March. Since
mid-June Shopping conversions fell 62% and PMax reports 340 conversions at a
better ROAS. The owner wants to pause Shopping.

Reading: the products overlap almost entirely, and PMax takes precedence for
shared inventory, so Shopping's decline is largely mechanical. Combined
account conversions over the same period are up 4%, while combined spend is up
27%.

Output: "The comparison as asked cannot be answered, and the account view is
worse than either row suggests." Spend rose 27% for a 4% conversion gain, so
the launch reallocated demand and bought a little growth expensively.
Recommendation: `approval_needed` on a six-week test pausing PMax rather than
Shopping, which is the opposite of the instinct, because Shopping's numbers
were suppressed mechanically and have never been measured against a fair
field.

## Guardrails

- Never compare campaign totals when the product sets differ.
- Never read a Shopping decline after a PMax launch as a performance verdict.
- Never present an attribution split between overlapping campaigns as clean.
- Do not pause campaigns. Recommend, and let a human approve.
