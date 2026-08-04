---
name: weekly-pmax-readout
description: Turns a week of Performance Max data into a short summary a client or a manager can read without translation, saying what changed, what it means and what needs a decision. Use for the recurring weekly or monthly update on a PMax campaign.
---

# Weekly PMax readout

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

This is the only skill in the pack whose output is written for someone who
does not run the account. Every other skill talks to the operator; this one
talks past them to the person paying.

## Use this skill when

The weekly or monthly update is due, or someone needs to explain a PMax
campaign to a person who will not open Google Ads.

## Required input

- Campaign performance this period and the comparable previous period.
- Change history for the period.
- Any findings already produced by other skills in this pack.
- Business context: promotions, stock, seasonality, targets.
- Who the readout is for, and what decision they own.

## Analysis workflow

1. Establish whether the period is readable at all. Below
   `conversion.volume_floor`, or inside `learning.duration` of a reset, the
   honest readout says so instead of reporting a delta.
2. Pick at most three QUANTITIES the reader is meant to remember. Not three
   digits: a quantity can need two figures to make sense ("196 reported sales,
   only 78 real"). The test is how many things the reader has to hold, not how
   many characters are numeric. A readout carrying twelve quantities is a data
   dump and gets skipped.
3. For each number, write the movement and the reason in the same sentence. A
   number without a reason generates a question, which is the thing the
   readout was supposed to prevent.
4. Name what was changed during the period and by whom, so the reader can
   connect action to outcome.
5. Name exactly one decision the reader owns this period, or say plainly that
   nothing needs them. Manufacturing a decision every week trains people to
   ignore the readout.
6. Strip the jargon in a final pass. Asset group, listing group, learning
   phase and impression share all need translating or removing.

## Decision rules

- Below `conversion.volume_floor` -> lead with that. No deltas, no trend
  language, one line on what would make the period readable.
- A reset trigger inside the period -> say the campaign is still settling and
  give the date it becomes readable, rather than reporting the movement as a
  result.
- Movement inside normal variance -> report it as steady. Do not dramatise
  noise.
- Nothing needs a decision -> say so in one line. This is a legitimate and
  useful readout.
- Bad news in the period -> it goes first, in plain words, before any context.
  Context after bad news reads as explanation; context before it reads as
  excuse.

## Output format

Plain prose, no table, under 200 words. Structure:

1. One line: how the period went.
2. Two or three numbers with their reasons.
3. What we changed.
4. The one decision needed, or a line saying none is.

No metric names the reader would have to look up. No asset group names. No
percentages without the underlying number when the base is small.

## Practical example

Input: spend 8,400 (prior 8,100), conversions 96 (prior 141), CPA 87.50
(prior 57.45). Conversion goal changed 22 July. Promotion ended 20 July.
Reader is the client, who owns the budget decision.

Output:

"Last week was worse than the one before, and two things caused it. Sales came
in at 96 against 141, and each one cost 87.50 against 57.45. The promotion
finished on the 20th, which removed the discount that was carrying a lot of
those sales. On the 22nd we changed what the campaign counts as a result, so
it is currently relearning and its numbers will be unreliable for another
two weeks or so. Spend was flat at 8,400.

Nothing needs a decision from you this week. Around 12 August we will know
whether the change is working, and if it is not we will put it back. If you
want the promotion repeated before then, that is the one call worth making
early, because it would sit on top of the relearning and make both harder to
read."

## Guardrails

- Never report a delta on a period the data cannot support.
- Never open with context when the news is bad.
- Never use platform jargon in the output.
- Never invent a decision to make the readout feel useful.
- Do not change anything. This skill reports and asks.
