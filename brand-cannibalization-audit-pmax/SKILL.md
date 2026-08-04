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

- The PMax search terms report, if available. This is the preferred source:
  it carries actual triggering queries. Ask for it first.
- PMax Insights, Search categories tab, as the fallback when the search terms
  report is not available.
- Brand Search campaign: spend, conversions, CPA, over the same date range.
- Total PMax spend and conversions for that range.
- The brand name and any obvious misspellings or variants.

If neither source is available, stop and say so. Every number in this skill
derives from one of them, and which one it came from changes how firm the
answer is. Say which you used, every time.

## Analysis workflow

1. Confirm the date ranges match across all inputs. A mismatch invalidates
   every comparison below; say so and stop rather than adjusting silently.
2. If you have the search terms report, mark branded queries and sum their
   actual conversions. This gives a real number, not an estimate, and the rest
   of the skill gets firmer accordingly.
3. If you only have Search categories, mark branded categories and be honest
   about what that gives you: a count of category LABELS, not a conversion
   share. Nine branded categories out of thirty-one does not mean 29% of
   conversions, because one category can carry most of the volume. Report the
   label count as a label count, give any conversion figure as a wide range,
   and say the range comes from counting labels.
4. Compare brand Search CPA against PMax CPA on THE SAME conversion basis.
   This is the step that goes wrong most often: PMax CPA computed on purchases
   only, against brand CPA computed on all its conversions, is not a comparison
   and it fires `brand.cpa_gap_flag` falsely. Pick one basis, apply it to both,
   and say which you picked.
5. Check `brand.overlap_flag` and `brand.cpa_gap_flag`. Either one crossing is
   a case; both crossing is a strong case.
6. Decide what the exclusion would actually cost. Brand exclusions in PMax
   apply to Search, Shopping and YouTube search inventory, so reported PMax
   ROAS falls after
   they go on. State that plainly: the drop is the reporting getting honest,
   not the account getting worse.

## Decision rules

- Branded share above `brand.overlap_flag` with an active brand Search
  campaign -> `approval_needed` on brand exclusions, with the ROAS drop stated
  up front.
- Brand Search CPA below `brand.cpa_gap_flag` relative to PMax CPA on the SAME
  conversion basis -> the gap is the money being left on the table. State which
  basis you used before quoting the ratio; purchases-only against
  all-conversions is not a comparison. Quantify the gap as (branded PMax
  conversions x CPA difference) only when the branded count is measured rather
  than inferred, and label it an estimate either way.
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
spend 3,100, 148 conversions, CPA 20.95. No search terms report supplied;
Search categories show 9 of 31 categories carrying the brand name.

Reading: 9 of 31 is a count of category labels, not a conversion share.
`brand.overlap_flag` measures branded conversions from the search terms report,
so with labels alone it cannot be computed and it is not crossed; it is
uncomputed. The label count is a reason to look, nothing more. One branded
category could hold most of the branded volume or almost none. Brand CPA at 20.95 is
30% of blended PMax CPA, below `brand.cpa_gap_flag`, and that comparison is
solid because both figures are measured.

Output: "Cannibalization case: confirmed in kind, unknown in size." The cheap
comparison is real: brand demand is being bought at 20.95 in one campaign and
somewhere near 68.85 in the other. The share of PMax conversions that is
branded cannot be stated from category labels, so the next step is the search
terms report, which turns this from an estimate into a number.
Recommendation: pull the search terms report, `do_now`, then re-run. Brand
exclusions stay `approval_needed` and should wait for the real figure, with
the note that reported PMax ROAS will fall once they go on.

## Guardrails

- Never present the branded share as exact. The source data is aggregated.
- Never recommend exclusions without stating the reported-ROAS consequence.
- Never recommend exclusions when no brand campaign exists to catch the demand.
- Do not add or remove exclusions. This skill produces a decision, not an edit.
