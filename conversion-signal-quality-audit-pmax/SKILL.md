---
name: conversion-signal-quality-audit-pmax
description: Checks whether the conversion actions a Performance Max campaign optimises toward actually represent money, and finds the ones that teach it to buy the cheapest worthless outcome. Use before any scaling decision, or when PMax volume rises while sales stay flat.
---

# Conversion signal quality audit

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

This is the first skill to run on any PMax account. Every other diagnosis in
this pack is unreliable while the signal is wrong, because PMax optimises
toward whatever it is told to count.

## Use this skill when

Conversions are up and revenue is not. Or before recommending a budget
increase, a structural change, or an exclusion. Or when nobody can say what
the campaign is actually bidding on.

## Required input

- Conversion actions list: name, count, value, primary or secondary status,
  attribution model, counting setting.
- The campaign's conversion goal configuration (account-default or
  campaign-specific).
- CRM or offline outcomes for the same period if they exist: qualified leads,
  closed deals, revenue.
- How leads are qualified, in the user's own words.

## Analysis workflow

1. List every conversion action marked primary. These, and only these, are
   what the campaign bids toward. Secondary actions are reporting only; say so
   if the user has been treating them as targets.
2. For each primary action, ask what business outcome it represents and what
   value it carries. Flag any action with no value assigned, or a value that
   was set once and never revisited.
3. Check `conversion.value_spread_flag`. Two primary actions carrying equal
   value while representing unequal outcomes is the most common defect in this
   whole pack, and it is invisible in the performance report.
4. Check the counting setting. "Every" on a lead form inflates the signal with
   repeat submissions from the same person.
5. Check for offline import: does closed-won revenue ever reach the account,
   and how stale is it (`conversion.offline_lag_floor`)? Without it the
   campaign is optimising on form fills and calling them sales.
6. Look for spam exposure: form fills with no phone validation, no honeypot, no
   reCAPTCHA. Spam is a conversion signal like any other and the campaign will
   chase it.
7. Compare platform-reported conversions to CRM outcomes for the same window.
   A large gap is the finding; the direction of the gap tells you whether the
   campaign is being lied to or the reporting is.

## Decision rules

- Any primary action with no value and no offline import -> `do_now` on
  assigning values. Nothing else in the pack is worth doing first.
- `conversion.value_spread_flag` crossed -> `do_now`. Name the two actions and
  what each is really worth.
- Offline data staler than `conversion.offline_lag_floor` -> `investigate` the
  import, and mark every downstream performance verdict `low` confidence.
- Form-fill-only signal, no qualification loop -> `approval_needed` on moving
  to a qualified-lead conversion, and state the cost: reported volume drops
  hard, and the campaign re-enters learning (`learning.reset_triggers`).
- Signal clean -> say so plainly and name what made it clean. This is the
  green light other skills in the pack look for.

## Output format

Open with one line: is this campaign optimising toward money, yes or no.

| Conversion action | Primary | Value | What it really represents | Risk | Recommendation |
|---|---|---|---|---|---|

Then a single sentence naming the one change that would most improve the
signal, then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: three primary actions. "Contact form" 412 conversions, value 100.
"Newsletter signup" 890 conversions, value 100. "Phone call 60s" 51
conversions, no value. CRM shows 38 qualified leads and 6 closed deals at an
average 4,200.

Reading: `conversion.value_spread_flag` is crossed hard. A newsletter signup
and a contact form both count as 100, so the campaign has learned that
newsletter signups are the cheap win and is buying them. 890 of 1,353 primary
conversions are worth close to nothing. Real revenue per platform conversion
is about 18.6, not 100.

Output: "No. This campaign is optimising toward newsletter signups." One
change: demote newsletter signup to secondary. Expect reported conversions to
fall by roughly two thirds and the campaign to re-enter learning for up to
`learning.duration`. That drop is the reporting getting honest.

## Guardrails

- Never recommend scaling on an unaudited signal.
- Never treat secondary conversions as targets.
- Never quote a CRM-to-platform gap without confirming both cover the same
  dates and the same attribution window.
- Do not edit conversion actions. Recommend, and let a human approve.
