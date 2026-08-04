---
name: brand-cannibalization-audit-pmax
description: Estimates how much of a Performance Max campaign's reported conversions are branded searches the brand campaign would have won anyway, and prices the gap. Use when PMax ROAS looks strong but total account revenue has not moved, or when deciding whether to add brand exclusions.
---

# Brand cannibalization audit

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

PMax reports a healthy CPA or ROAS while blended account performance is flat,
or a brand Search campaign is running alongside PMax and nobody has checked
whether they are bidding on the same demand.

## Required input

- PMax Insights, Search categories tab (export or screenshot).
- Brand Search campaign: spend, conversions, CPA, over the same date range.
- Total PMax spend and conversions for that range.
- The brand name and any obvious misspellings or variants.

If the Search categories tab is empty or unavailable, stop and say so. Every
number in this skill derives from it.

## Analysis workflow

1. Confirm the date ranges match across all inputs. A mismatch invalidates
   every comparison below; say so and stop rather than adjusting silently.
2. Read the Search categories list and mark every category that contains the
   brand name or a recognisable variant. Categories are aggregated and
   conversion-weighted, so the resulting share is an upper bound, never an
   exact figure (`thresholds.md`, Reporting limits).
3. Sum the conversion share sitting in branded categories. Express it as a
   range, not a point value.
4. Compare brand Search CPA against blended PMax CPA. A brand campaign buying
   the same demand materially cheaper is the whole finding.
5. Check `brand.overlap_flag` and `brand.cpa_gap_flag`. Either one crossing is
   a case; both crossing is a strong case.
6. Decide what the exclusion would actually cost. Brand exclusions in PMax
   apply to Search and Shopping inventory, so reported PMax ROAS falls after
   they go on. State that plainly: the drop is the reporting getting honest,
   not the account getting worse.

## Decision rules

- Branded share above `brand.overlap_flag` with an active brand Search
  campaign -> `approval_needed` on brand exclusions, with the ROAS drop stated
  up front.
- Brand Search CPA below `brand.cpa_gap_flag` relative to blended PMax CPA ->
  the gap is the money being left on the table. Quantify it as
  (branded PMax conversions x CPA difference), labelled an estimate.
- No brand Search campaign running -> exclusions are usually the wrong move.
  The demand still has to be bought somewhere; recommend building the brand
  campaign first, then re-running this skill.
- Campaign under `conversion.volume_floor` -> report the categories, refuse the
  CPA comparison, and say the sample cannot carry it.

## Output format

Open with one line: is there a cannibalization case, yes or no, and how strong.

| Finding | Evidence | Estimated scale | Recommendation | Confidence |
|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: PMax spend 42,000, 610 conversions, blended CPA 68.85. Brand Search
spend 3,100, 148 conversions, CPA 20.95. Search categories show 9 of 31
categories carrying the brand name.

Reading: branded categories are roughly 29% of the list, above
`brand.overlap_flag`. Brand CPA is 30% of blended PMax CPA, below
`brand.cpa_gap_flag`. Both flags cross.

Output: "Cannibalization case: strong." Estimated 120-180 PMax conversions are
branded (range, because categories are conversion-weighted and aggregated). At
the CPA difference of 47.90, that is roughly 5,700-8,600 of spend buying
demand the brand campaign already owned. Recommendation: brand exclusions,
`approval_needed`, with the note that reported PMax ROAS will fall and total
account CPA should improve.

## Guardrails

- Never present the branded share as exact. The source data is aggregated.
- Never recommend exclusions without stating the reported-ROAS consequence.
- Never recommend exclusions when no brand campaign exists to catch the demand.
- Do not add or remove exclusions. This skill produces a decision, not an edit.
