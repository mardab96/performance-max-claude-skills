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
- Performance weekly, covering exactly 8 weeks before the change and whatever
  exists after it. Eight is fixed on purpose: the detection band is built from
  the spread of the pre-change weeks, so a longer window with one outlier
  widens the band and a shorter one narrows it, and two people pasting
  different amounts of history get different answers about whether anything
  happened. If fewer than 8 weeks exist, say so and treat detection as weaker.
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
   for this step. It answers detection only, refuses the question when there
   are fewer than three pre-change periods, and trims the baseline to the fixed
   8 weeks itself rather than trusting whatever was pasted in, reporting how
   many older periods it discarded. Attribution stays here.
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
probably still in learning. "Probably" is doing real work there: a conversion
goal change is our reading of Google's "composition change", not something
Google lists (`learning.reset_triggers`). The rise to 71 is outside pre-period
variance of 49-58, so something moved. But two other explanations sit in the
window: last year showed the same seasonal direction, and a promotion ended
two days before the change.

Output: "Not readable until 12 August." Three candidate causes, listed and
deliberately NOT ranked: the promotion ending on the 20th, the seasonal
direction last year showed in the same weeks, and the conversion goal change on
the 22nd. Ranking them would be attribution, and attribution inside
`learning.duration` is what this skill exists to refuse. Naming a strongest
candidate while calling the period unreadable is a hedge, not a finding.

Revert decision: hold. Stop condition, if CPA is still above 65 on 12 August
with the promotion effect washed out, revert the conversion goal and accept
another learning period. That is the date the ranking becomes possible.

## Guardrails

- Never attribute a movement before `learning.duration` has passed.
- Never compare a single post-period number to a single pre-period number.
- Never skip the seasonal check when last year's data exists.
- Do not revert anything. Recommend, and let a human approve.
