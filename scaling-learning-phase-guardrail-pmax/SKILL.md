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
- Impression share lost to budget. Without it the starve-floor rule cannot
  fire, and a budget recommendation made without it dies the moment anyone
  opens the account.

## Analysis workflow

1. Plot every change from the history against the performance trend. Do this
   before forming any opinion about the trend, or you will read the season as
   an edit.
2. Mark which changes are learning events (`learning.reset_triggers`). Two
   distinctions that people get wrong constantly, and both are worth stating in
   the output because they change what gets blamed:
   - Budget changes are not on Google's list (`learning.budget_note`). They
     cause volatility without formally restarting learning.
   - Changing the VALUE of an existing target is not the same as changing the
     bid strategy (`learning.target_change_note`). Moving tCPA from 70 to 60 is
     not a reset; switching from Maximise Conversions to tCPA is.
3. For each reset, check whether `learning.duration` had elapsed before the
   next change landed. A campaign edited more often than that never leaves
   learning and its numbers are not readable.
4. Check whether the observation window is at least
   `learning.judgement_window`. Below that, a conclusion about a change is
   noise dressed as insight.
5. Check `budget.starve_floor`, then check whether the campaign is actually
   constrained. The ratio alone proves nothing: a campaign under the floor that
   is not losing impressions to budget is not spending what it already has, and
   more budget changes nothing for it. Impression share lost to budget is the
   corroboration, and without it you do not have a starvation finding.
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
- Below `budget.starve_floor` AND losing impressions to budget -> the answer to
  "why is it not learning" is the budget. `approval_needed` on a step up, or on
  pausing the campaign if the budget cannot go there.
- Below `budget.starve_floor` and NOT losing impressions to budget -> the
  campaign is not spending what it already has, so more budget changes nothing.
  Say that instead, and look at the target.
- A freeze and the starve floor both firing -> both, in that order
  (`AGENTS.md`, precedence rule 6). Do nothing now; name budget as the lever
  for when the window opens. Neither rule cancels the other.
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
later the conversion goal changed. Treat that as a learning event, while
saying where the claim comes from: Google names a "composition change" and we
read a conversion goal change as one (`learning.reset_triggers`). It is our
reading, not Google's wording, and the freeze below rests on it. The CPA rise starts after both. Only 16 days have
elapsed, well under `learning.judgement_window`, so the campaign is not yet
readable.

`budget.starve_floor` fires on the ratio: at a target CPA of 70 the floor is
700/day and the campaign sits at 400. But the ratio is only half the test, and
the other half fails here. At roughly 90 conversions a month and a CPA near 94,
this campaign spends about 8,500 a month, which is 280 a day against a budget
of 400, so it is using roughly two thirds of what it has.

That is suggestive and it is not the required datum. Daily pacing varies and
Google may spend up to twice the daily budget on a given day, so a monthly
ratio cannot establish daily impression share lost to budget. The skill's own
required input names that figure and says the rule cannot fire without it, and
it was not supplied here. So the honest output is that the starvation reading
is `needs_data`, with the monthly ratio noted as a reason to expect it will not
hold. Inventing the corroboration from an unrelated ratio would be the exact
move this skill tells other people not to make. So only one rule actually fires here, not
two: the freeze. The starve floor looked like it fired on the ratio and then
failed its corroboration, which is not the same as a collision. `AGENTS.md`
precedence rule 6 resolves two rules that both genuinely fire; it does not
promote a flag that failed its own second half.

Output: "Freeze, then look at the target." No further changes until 16 August.
Working: the last reset was 19 July. `learning.judgement_window` defaults to six
weeks, but it recalibrates to four when the campaign clears
`conversion.volume_floor` by 3x or more. The floor is 30 primary conversions
per 30 days and this campaign runs about 90, which is exactly 3x, and the rule
says "or more", so it qualifies and the window is four weeks. 19 July plus four
weeks is 16 August.

Say the working out, not just the date, whenever a recalibration fires and
especially when the account sits exactly on the boundary as this one does.
A reader who checks 90 against 30 and gets a different answer from yours will
trust nothing else in the output. Then re-read. If CPA has not returned toward 70, the
conversion goal change is the suspect, not the budget.

Then the budget, and the answer is not "raise it". The campaign is not
spending the budget it has, so adding more buys nothing. The floor is telling
you the target and the budget disagree, and the cheap side of that disagreement
is the target: lowering it brings the floor down with it, and lowering a target
VALUE does not restart learning (`learning.target_change_note`), so it costs no
waiting period on top of the one already running. Raising budget on a campaign
with impression share to spare is the recommendation that dies the moment a
client's analyst opens the account.

## Guardrails

- Never call a change the cause of a trend without checking elapsed time
  first.
- Never recommend a budget jump above `budget.step` because the campaign
  "looks strong".
- Never read a weekly trend on a campaign below `conversion.volume_floor`.
- Do not change budgets or settings. Recommend, and let a human approve.
