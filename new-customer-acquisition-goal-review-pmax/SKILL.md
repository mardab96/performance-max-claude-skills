---
name: new-customer-acquisition-goal-review-pmax
description: Checks whether the new customer acquisition setting on a Performance Max campaign is configured correctly and what it is actually costing, including whether the campaign can tell a new customer from a returning one. Use before turning it on, or when it is on and nobody has priced it.
---

# New customer acquisition goal review

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

The new customer setting is on, or someone wants to turn it on, and nobody has
checked whether the customer lists behind it are good enough for the campaign
to tell new from returning.

## Required input

- The current setting: off, value mode (bid higher for new customers), or
  acquisition mode (new customers only).
- The new customer value assigned, if in value mode.
- Customer lists feeding the setting: source, size, refresh frequency, match
  rate if known.
- Whether a first-party data connection or conversion-level customer type is
  in place.
- New versus returning customer split from the business, if it exists outside
  the ad account.

## Analysis workflow

1. Check what the campaign uses to decide who is new. Uploaded customer lists,
   site tagging, or conversion-level new-customer reporting. If it is a list
   that has not been refreshed in months, the campaign is calling recent buyers
   new and paying a premium for them.
2. Check refresh frequency against sales cycle. A list refreshed quarterly on
   a business with a two-week repeat cycle is wrong most of the time.
3. Check match rate. An unmatched list means the setting is running on
   incomplete knowledge, and the premium is being paid on guesses.
4. Price the setting. In value mode, the assigned new-customer value is added
   on top of conversion value for bidding, so the campaign will pay more per
   new customer by design. Compare that premium against real first-order
   margin and, if it exists, against lifetime value.
5. In acquisition mode, check that returning-customer demand is being served
   somewhere else. Otherwise the account is refusing to sell to its own
   customers.
6. Compare the platform's new-customer split against the business's own
   figure. A large gap means the setting is misclassifying, and every verdict
   built on it inherits that error.

## Decision rules

- Customer list older than one full repeat-purchase cycle [heuristic] ->
  `do_now` on refreshing before trusting any new-customer number.
- New customer value exceeding first-order margin without a lifetime value
  case -> `approval_needed` on lowering it. Name the per-order cost.
- Acquisition mode on with no other campaign serving returning customers ->
  `approval_needed` on switching to value mode.
- Platform new-customer share differing from the business figure by more than
  roughly 15 percentage points [heuristic] -> `investigate` classification
  before acting on anything downstream.
- No first-party data connection and no customer list -> the setting is
  guessing. `do_now` on connecting data, or turn the setting off.

## Output format

Open with one line: is the campaign able to tell a new customer from a
returning one, yes or no.

| Check | Finding | Cost or risk | Recommendation |
|---|---|---|---|

Then a plain-language line on what the setting is costing per new customer,
then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: value mode on, new customer value 40. Customer list of 12,000 emails,
last refreshed 5 months ago, match rate unknown. Average first order 95,
margin 34%. Business says roughly 30% of orders are from new customers; the
platform reports 61%.

Reading: first-order margin is about 32. The setting adds 40 on top, so the
campaign is bidding as if a new customer is worth more than the order makes,
before the list quality is even considered. The 5-month-old list and the
31-point gap between platform and business figures both suggest returning
buyers are being counted as new.

Output: "No." The premium exceeds first-order margin by roughly 8 per order,
and the classification is probably wrong in the campaign's favour.
Recommendation: refresh the list `do_now`, then lower the value to at or below
margin unless a lifetime value case is documented, `approval_needed`.

## Guardrails

- Never accept the platform's new-customer split as fact when a business
  figure exists and disagrees.
- Never recommend acquisition mode without confirming returning demand is
  served elsewhere.
- Never justify a premium with lifetime value unless someone can produce the
  number.
- Do not change the setting. Recommend, and let a human approve.
