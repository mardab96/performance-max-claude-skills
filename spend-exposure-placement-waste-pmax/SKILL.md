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
3. Group the questionable ones ONLY where the group is a real family per
   `thresholds.md` (Denominators): one domain, one app, or one Google-defined
   category. A theme you assembled yourself is not a family. If you do group,
   the group must clear `placement.waste_flag` on its own and you must list its
   members, because aggregating small families over the line is how a hunch
   gets dressed as a rule.
4. Cross-read against Search categories. A campaign whose search side looks
   sane while its placement side is full of games is spending its display and
   video budget somewhere the search intent never was.
5. List the controls that actually exist for PMax, and be precise, because
   most of the internet is wrong about this: account-level placement
   exclusions, content suitability settings, the mobile app category
   exclusions, and brand exclusions. Per-campaign placement exclusions are not
   available for PMax.
6. Before recommending any exclusion, be honest that the check you would want
   is impossible. Per-placement conversions are not reported, so you can never
   confirm a family produced nothing. That means EVERY exclusion this skill
   produces is a judgement call, not a data-backed one, and the output must
   carry that label rather than implying evidence it cannot have. What you can
   do instead: check the channel performance report to size the channel the
   family sits in, so at least the order of magnitude is known.

## Decision rules

- A placement family crossing `placement.waste_flag` -> `approval_needed` on
  an account-level exclusion, with the caveat that the per-placement cost saved
  cannot be measured in advance.
- A family below `placement.waste_flag` -> `monitor`, and say it is below the
  bar. Recommending an exclusion under the flag turns the rule into a hunch.
- A mobile app category, which is a Google-defined family and therefore a
  legitimate grouping, crossing `placement.waste_flag` while the offer is B2B
  -> `approval_needed` on app category exclusions. This is the strongest call
  in the skill, and it is still a judgement call rather than a data-backed one,
  because per-placement conversions do not exist (step 6). Label it as such.
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

Reading: the puzzle app is 10.2% of placement-report impressions and the
video app 7.4%, so both clear `placement.waste_flag` on their own. The recipe
site is 4.2% and does not, so it is reported separately rather than folded in
to make a bigger number; adding it to reach "about 20%" would be exactly the
aggregation the threshold forbids. Cost per placement is unknown and
unknowable from this report.

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
