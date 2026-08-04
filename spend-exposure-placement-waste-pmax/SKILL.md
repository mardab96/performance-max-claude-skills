---
name: spend-exposure-placement-waste-pmax
description: Ranks where a Performance Max campaign is showing up that it probably should not, using the impression-only data Google actually provides, and names the controls that exist. Use when PMax volume looks cheap but low quality, or when someone asks where the display and video money is going.
---

# Spend exposure and placement waste

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

CPA looks good and lead quality does not. Or someone wants to know how much of
the budget is leaking into apps, autoplay video and parked domains, which is
the single most common suspicion about PMax.

## Required input

- The "where ads appeared" report (Campaigns > the PMax campaign > Insights,
  or the account-level placement report). Impressions only.
- PMax Insights, Search categories tab.
- Asset group performance, if available.
- Any existing account-level placement exclusions and content exclusion
  settings.

## Analysis workflow

1. State the limit precisely, because it is narrower than most people think.
   Per PLACEMENT, Google reports impressions only, never cost and never
   conversions, so placement-level waste can be ranked but not priced. Per
   CHANNEL, cost IS available since 2025 (`thresholds.md`, Reporting limits),
   so "how much is going to display and video" is answerable and should be
   answered rather than refused. Ask for the channel performance report.
2. Rank placements by impression volume. Mark each as plausible, questionable
   or implausible for the advertiser's actual audience.
3. Cluster the questionable ones: mobile game apps, made-for-advertising
   domains, kids content, autoplay video, parked pages.
4. Cross-read against Search categories. A campaign whose search side looks
   sane while its placement side is full of games is spending its display and
   video budget somewhere the search intent never was.
5. List the controls that actually exist for PMax, and be precise, because
   most of the internet is wrong about this: account-level placement
   exclusions, content suitability settings, the mobile app category
   exclusions, and brand exclusions. Per-campaign placement exclusions are not
   available for PMax.
6. Before recommending any exclusion, check whether that placement family has
   ever produced anything. If the data cannot tell you, say the exclusion is a
   judgement call and not a data-backed one.

## Decision rules

- A placement family above roughly 5% of total impressions with no plausible
  audience fit [heuristic] -> `approval_needed` on an account-level exclusion,
  with the caveat that the cost saved cannot be measured in advance.
- Mobile app inventory dominating impressions while the offer is B2B
  -> `do_now` on app category exclusions. This is the highest-confidence call
  in the skill.
- Content exclusions already at the strictest setting and waste still visible
  -> `investigate`, and say plainly that PMax control ends here; the remaining
  option is campaign type, not campaign settings.
- No placement report available -> `needs_data`, and do not guess.
- User asks how much budget goes to display or video -> answer it from the
  channel performance report. Refusing this question was correct before 2025
  and is now simply wrong.

## Output format

Open with the limit in one line, then the ranked table.

| Placement or family | Impressions | Share | Audience fit | Control available | Recommendation |
|---|---|---|---|---|---|

Then `What this could not see` (which here always includes cost and
conversions per placement), `Missing data`, `Approval gates`.

## Practical example

Input: 2.1M impressions total. Top placements include a word-puzzle app
(214k), a video-sharing app (156k), a recipe site (88k) and a set of parked
domains (61k). The advertiser sells industrial fittings to procurement teams.

Reading: three of the top four families have no plausible procurement
audience, together about 20% of impressions. Cost is unknown and unknowable
from this report.

Output: ranked table, then "app category exclusions, `do_now`". The
parked-domain family sits at 2.9% of impressions, under the 5% bar, so it is
`monitor` rather than an exclusion recommendation; saying so is the difference
between a rule and a hunch. Stated clearly: per-placement saving cannot be
quantified before the change, only observed after it. What CAN be quantified
now is the display and video share of spend, from the channel performance
report, and that should be pulled before any exclusion is approved.

## Guardrails

- Never state or imply cost per placement. It does not exist in this report.
- Never present an exclusion as a guaranteed saving.
- Never recommend excluding a placement family that plausibly matches the
  audience just because its name looks unfamiliar.
- Do not apply exclusions. Recommend, and let a human approve.
