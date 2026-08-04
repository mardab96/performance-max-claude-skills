---
name: scaling-learning-phase-guardrail-pmax
description: Decides whether a Performance Max campaign is stable enough to scale, and sizes the budget step so the increase does not reset what the campaign learned. Use before raising budget, after a performance drop, or when someone wants to know if a change caused the dip.
---

# Scaling and learning-phase guardrail

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

Someone wants to increase budget, or performance dropped and nobody knows
whether it was the market, the season or the last edit.

## Required input

- Change history: every budget change, bid strategy change, conversion goal
  change, asset group edit and status change, with dates.
- Daily or weekly CPA and ROAS trend over at least the last 8 weeks.
- Campaign start date and current daily budget.
- Target CPA or target ROAS, if one is set.

## Analysis workflow

1. Plot every change from the history against the performance trend. Do this
   before forming any opinion about the trend, or you will read the season as
   an edit.
2. Mark which changes are formal learning resets
   (`learning.reset_triggers`). Budget changes are not on that list, which
   surprises people; they cause volatility without formally restarting
   learning.
3. For each reset, check whether `learning.duration` had elapsed before the
   next change landed. A campaign edited more often than that never leaves
   learning and its numbers are not readable.
4. Check whether the observation window is at least
   `learning.judgement_window`. Below that, a conclusion about a change is
   noise dressed as insight.
5. Check `budget.starve_floor`. A campaign whose daily budget is small
   relative to its own target CPA will sit in learning permanently regardless
   of how patiently it is left alone.
6. Size the next step from `budget.step`, with `budget.step_wait` between
   steps, and say what the plan looks like over the next month rather than
   giving a single number.

## Decision rules

- A reset trigger inside `learning.duration` of today -> `monitor`, do not
  scale, do not diagnose. State the date the campaign should be readable
  again.
- Two or more reset triggers inside the last `learning.judgement_window` ->
  `do_now` on a change freeze. The account is being managed faster than it can
  respond.
- Stable for at least `learning.judgement_window`, CPA at or under target ->
  `approval_needed` on a budget step of `budget.step`, then hold for
  `budget.step_wait`.
- Below `budget.starve_floor` -> the answer to "why is it not learning" is the
  budget, not the structure. `approval_needed` on a step up, or on pausing the
  campaign if the budget cannot go there.
- Below `conversion.volume_floor` -> refuse the trend read entirely and say
  why. Weekly CPA on a campaign with four conversions a week is not a signal.

## Output format

Open with one line: scale, hold, or freeze.

| Date | Change | Reset trigger | Days to next change | Readable | Effect visible |
|---|---|---|---|---|---|

Then the scaling plan as a short sequence of steps with dates, then
`What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: budget raised from 200 to 400/day on 14 July. Conversion goal changed
19 July. CPA rose from 61 to 94 across late July. Target CPA 70. Campaign at
about 90 conversions/month.

Reading: the budget doubled, which is far above `budget.step`, and five days
later the conversion goal changed, which is a formal reset
(`learning.reset_triggers`). The CPA rise starts after both. Only 16 days have
elapsed, well under `learning.judgement_window`, so the campaign is not yet
readable.

Output: "Freeze." No further changes until roughly 25 August, which is
`learning.judgement_window` from the last reset. Then re-read. If CPA has not
returned toward 70 by then, the conversion goal change is the suspect, not the
budget. Next budget step when stable: 400 to 460-480, hold one conversion
cycle, then reassess.

## Guardrails

- Never call a change the cause of a trend without checking elapsed time
  first.
- Never recommend a budget jump above `budget.step` because the campaign
  "looks strong".
- Never read a weekly trend on a campaign below `conversion.volume_floor`.
- Do not change budgets or settings. Recommend, and let a human approve.
