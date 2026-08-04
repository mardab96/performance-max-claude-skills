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

1. State the limit before doing anything else, so nothing downstream reads as
   more certain than it is: Google reports impressions per placement for PMax,
   never cost and never conversions (`thresholds.md`, Reporting limits). This
   skill ranks suspicion, not spend.
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
- No placement report available -> `needs_data`, and do not guess a split.

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

Output: ranked table, then "app category exclusions, `do_now`" and
"parked-domain exclusion list, `approval_needed`". Stated clearly: the saving
cannot be quantified before the change, only observed after it, by comparing
CPA over a window of at least `learning.judgement_window`.

## Guardrails

- Never state or imply cost per placement. It does not exist in this report.
- Never present an exclusion as a guaranteed saving.
- Never recommend excluding a placement family that plausibly matches the
  audience just because its name looks unfamiliar.
- Do not apply exclusions. Recommend, and let a human approve.
