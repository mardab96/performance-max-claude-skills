---
name: post-change-readout-pmax
description: Reads what happened after a change to a Performance Max campaign and separates the effect of the change from seasonality, promotions and competitor pressure. Use when performance moved after an edit and someone needs to know whether to revert.
---

# Post-change readout

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

Something was changed, the numbers moved, and the pressure to revert is
building before enough time has passed to know anything.

## Required input

- The change: what, when, and why, in one line.
- Performance daily or weekly, covering at least the same span before and
  after the change.
- The equivalent period last year, if the account is old enough.
- Any promotions, price changes, stock outages or PR events in the window.
- Auction insights or impression share trend, if available.

## Analysis workflow

1. Check elapsed time first, before looking at any number. If less than
   `learning.duration` has passed since a reset trigger, the readout is
   premature and saying so is the entire answer.
2. Establish the pre-period baseline with its own variance, not a single
   number. A change that moves CPA less than the pre-period week-to-week swing
   has not been detected at all. Run
   `../scripts/variance_check.py <series.csv> --change-date <YYYY-MM-DD> --metric cpa`
   for this step; it answers detection only, and refuses the question when
   there are fewer than three pre-change periods. Attribution stays here.
3. Check seasonality against last year's same weeks. A decline that also
   happened last year is a season, and reverting the change will not fix it.
4. Check for confounders inside the window: promotions, stock, price, site
   changes, competitor entry visible in impression share.
5. Only after all of the above, attribute. State the attribution as a range or
   as one of several candidate causes, never as a single certain cause.
6. Give the revert decision a stop condition: what would have to be true, and
   by when, for the change to be judged a failure.

## Decision rules

- Less than `learning.duration` since a reset trigger -> `monitor`. Refuse the
  readout and give the date it becomes readable.
- Movement smaller than pre-period variance -> `ignore`. Nothing has been
  detected.
- Same-direction movement in last year's equivalent weeks -> seasonality is
  the leading candidate; `monitor`, do not revert.
- A confounder inside the window -> `investigate` it before attributing
  anything to the change.
- Campaign below `conversion.volume_floor` -> refuse the readout entirely.
  Small numbers move a lot for no reason.
- Clean window, movement beyond variance, no seasonal match, no confounder ->
  attribute to the change, and still say what else could explain it.

## Output format

Open with one line: readable or not readable, and if not, the date it becomes
readable.

| Question | Answer | Evidence | Weight |
|---|---|---|---|

Rows cover: elapsed time, pre-period variance, seasonal match, confounders,
competitor pressure. Then the attribution, then the revert decision with its
stop condition, then `What this could not see`, `Missing data`,
`Approval gates`.

## Practical example

Input: conversion goal changed 22 July. CPA rose from 54 to 71 over the
following two weeks. Pre-period CPA ranged 49-58 week to week. Last year the
same fortnight ran 12% above its own preceding month. A promotion ended 20
July.

Reading: 13 days have passed, under `learning.duration`, so the campaign is
still in learning from a formal reset. The rise to 71 is outside pre-period
variance of 49-58, so something moved. But two other explanations sit in the
window: last year showed the same seasonal direction, and a promotion ended
two days before the change.

Output: "Not readable until roughly 12 August." Three candidate causes,
ordered: promotion ending (strongest, because the timing is closest and the
mechanism is direct), seasonality (supported by last year), the conversion
goal change (plausible but unmeasurable while learning is still running).
Revert decision: hold. Stop condition, if CPA is still above 65 on 12 August
with the promotion effect washed out, revert the conversion goal and accept
another learning period.

## Guardrails

- Never attribute a movement before `learning.duration` has passed.
- Never compare a single post-period number to a single pre-period number.
- Never skip the seasonal check when last year's data exists.
- Do not revert anything. Recommend, and let a human approve.
