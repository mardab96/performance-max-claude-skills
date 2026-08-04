---
name: pmax-vs-shopping-comparison-pmax
description: Compares Performance Max against a standard Shopping campaign covering the same products, using the post-2024 auction rules where the higher Ad Rank serves rather than PMax taking automatic priority. Use when both run on the same catalogue, or when a Shopping campaign declined after a PMax launch. Do not use to attribute a movement to a specific change; that is post-change-readout-pmax.
---

# PMax versus Shopping comparison

Shared quality bar: `../references/output-standard.md`. All numbers and
platform facts cited here live in `../references/thresholds.md`.

**Start by correcting the assumption almost everyone brings to this question.**
Until October 2024, a PMax campaign automatically beat a standard Shopping
campaign in the same account for the same product. That is no longer true. The
higher Ad Rank serves, exactly as between any other pair of campaign types
(`thresholds.md`, Auction behaviour). Most articles and most practitioners
still repeat the old rule, so the first job of this skill is often to tell the
user that the mechanism they are reasoning from was retired.

This changes the diagnosis in a specific way. Under the old rule, a Shopping
decline after a PMax launch was mechanical and told you nothing. Now it may be
a genuine auction loss, which is information: it says the Shopping campaign's
Ad Rank is lower, and Ad Rank is something you can act on.

## Use this skill when

Both campaign types cover overlapping products, or a Shopping campaign declined
after PMax launched and someone wants to know whether to pause one.

## Required input

- Both campaigns: cost, conversions, conversion value, impression share and
  lost impression share (rank), over the same date range.
- The product overlap: which items appear in both.
- Bid strategy and target for each campaign.
- Launch dates and change history for both.
- Attribution model and conversion window.

Impression share lost to rank is the input this skill needs most and the one
users most often omit. Without it, the central question cannot be answered.

## Analysis workflow

1. State the auction rule and check whether the user was reasoning from the old
   one. If they were, that correction is the most valuable thing in the output
   and it goes first.
2. Establish the overlap. Compare on overlapping products only; comparing
   campaign totals when the product sets differ measures the catalogue, not the
   campaign type.
3. Check the window is clean: no reset triggers (`learning.reset_triggers`)
   inside it for either campaign, and at least `learning.judgement_window` long.
4. Read impression share lost to rank for the declining campaign. This is the
   test that separates the two explanations. High rank-lost share means it is
   losing the auction on merit, which is a bid, quality or feed problem, not a
   structural inevitability.
5. Check attribution. With overlapping journeys, a conversion credited to one
   campaign may have been assisted by the other. Never present the split as
   clean.
6. Look at combined account performance before and after the second campaign
   launched. Whether the account made more money in total is the only question
   that matters; which row looks better is not.
7. If a decision is genuinely needed, frame it as a time-boxed test with a stop
   condition, and price the cost of the test itself.

## Decision rules

- User is reasoning from PMax priority -> correct it first, `do_now`. Every
  downstream conclusion they have drawn from it is suspect.
- Shopping declining with high impression share lost to rank -> the campaign is
  losing on Ad Rank. `investigate` bid strategy, target, feed quality and
  landing page experience before considering a pause. This is now the most
  common correct answer and it did not exist as an answer before 2024.
- Shopping declining with low rank-lost share and stable impression share ->
  demand shifted rather than the auction. `investigate` seasonality and total
  demand.
- Product sets overlap and cannot be separated -> `needs_data`. Say the
  comparison as asked cannot be answered, and name the segmentation that would
  make it answerable.
- Combined account performance improved after the launch -> `ignore` the
  which-is-better question. Both are earning their place.
- Combined performance flat while one campaign's numbers rose -> the second
  campaign is absorbing existing demand. `investigate`, and call the rise
  reallocation, not growth.
- Either campaign below `conversion.volume_floor` -> refuse the comparison and
  say why.
- A pause test is proposed -> `approval_needed`, and the output must price two
  things the test costs: restarting the paused campaign is a status change,
  which is a learning event (`learning.reset_triggers`), and the test window
  sits in a season. A six-week pause running into Q4 is a different decision
  from the same pause in February.

## Output format

Open with one line: which campaign is winning, or a plain statement that the
comparison cannot be made with what is available. If the user was reasoning
from PMax priority, that correction is the second line.

| Metric | PMax | Shopping | Overlapping products only | Read |
|---|---|---|---|---|

Then the combined-account view, then, if a test is recommended, its cost and
stop condition, then `What this could not see`, `Missing data`,
`Approval gates`.

## Practical example

Input: PMax launched 12 June. Shopping campaign running since March. Since
mid-June Shopping conversions fell 62% while PMax reports 340 conversions at a
better ROAS. Shopping impression share lost to rank rose from 18% to 54% over
the same period. The products overlap almost entirely. Combined account
conversions are up 4%, combined spend up 27%. The owner wants to pause
Shopping and it is early September.

Reading: the owner's stated reason for pausing is that PMax takes priority so
Shopping cannot win. That has not been true since October 2024. The rank-lost
share tripling to 54% says Shopping is losing the auction on Ad Rank, which is
a fixable problem rather than a structural one. Separately, the account bought
a 4% conversion gain for 27% more spend, so the launch mostly reallocated
demand.

Output: "Neither is clearly winning, and the reason you were given for pausing
Shopping is out of date." Correction first. Then: Shopping's decline is an Ad
Rank loss, so `investigate` its bid strategy and target before pausing, because
a campaign losing on rank at a low target will keep losing after PMax is
paused too. On the account view, spend rose 27% for a 4% gain, which is
expensive growth and the real finding. Any pause test is `approval_needed` and
should not run in September: it lands in Q4 build-up, and restarting the paused
campaign afterwards costs a learning period on top.

## Guardrails

- Never state or imply that PMax outranks standard Shopping by campaign type.
  That rule was retired in October 2024.
- Never read a Shopping decline as automatically mechanical, and never read it
  as automatically a performance verdict either. Impression share lost to rank
  is what separates them.
- Never compare campaign totals when the product sets differ.
- Never present an attribution split between overlapping campaigns as clean.
- Never recommend a pause test without pricing the restart and naming the
  season it lands in.
- Do not pause campaigns. Recommend, and let a human approve.
