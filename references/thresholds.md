# Thresholds

Single home for every number used across this pack. Skills cite this file by
name instead of restating a value. If a skill needs a number that is not here,
add it here first, then cite it.

Every entry carries a unit and a tag:

- `[platform guidance]` - stated by Google in its own documentation or UI.
- `[heuristic]` - a practitioner starting point, not a platform rule.

## Every threshold is ONE number, not a range

A range is not a threshold. "4 to 6 weeks" means two people applying the same
rule to the same account land two weeks apart, both correctly, and neither can
defend their number to a client. So every entry below states a single default
and, where the value genuinely depends on the account, the rule for moving it.

**Use the default unless the recalibration rule fires.** When you move a value,
say in the output which one you moved, to what, and why. An unexplained
recalibration is worse than the default, because it looks like a fact.

## Denominators

Half of a threshold is the number; the other half is what it is measured
against. These are the six that decide the most verdicts in this pack, and each
is fixed here rather than left to the reader:

| Term | Means | Not |
|---|---|---|
| **conversions** | primary conversion actions only, as configured on the campaign | all reported conversions including secondary. Where a skill needs the real-money subset, it says "purchases" or "qualified" explicitly and you must state which you used |
| **catalogue** | every product in the Merchant Center feed | the rows in a Google Ads product report, which lists only products that spent. Call that "spending products" and never "catalogue" |
| **campaign impressions** | impressions across the whole campaign, all channels | impressions in the placement report, which covers Display, YouTube and Discover only. A placement share must state which denominator it used, and the default is the placement report's own total |
| **placement family** | one domain, one app, or one named Google-defined category | a cluster you assembled by theme. If you group placements, the group must clear the flag on its own, and you must list its members |
| **target CPA** | the target configured on the campaign | the achieved CPA. On a tROAS campaign, derive an implied target CPA as average order value divided by target ROAS, and say you derived it |
| **branded share** | share of conversions, from the search terms report | share of category labels. A label count is a label count and never converts into a conversion share |

## Learning and stability

| Key | Value | Tag | Notes |
|---|---|---|---|
| `learning.duration` | **3 weeks**, or one full conversion cycle if that is longer | [platform guidance] | Google's stated learning period. **Conversion cycle** means the account's own median days-to-conversion from its lag report; if nobody can produce that number, use 3 weeks and say you did. |
| `learning.judgement_window` | **6 weeks** | [heuristic] | Minimum elapsed time before concluding anything about a change. Move to 4 weeks only when the campaign clears `conversion.volume_floor` by 3x or more, because volume buys you the time back. State the window as a date, not a range. |
| `learning.reset_triggers` | a new or reactivated bid strategy, a setting change to the bid strategy, a composition change (campaigns or asset groups added to or removed from the strategy) | [platform guidance] | Google's own wording ([learning period](https://support.google.com/google-ads/answer/13020501), checked 2026-08-04). Conversion goal and campaign status changes are our reading of "composition change", so treat those two as [heuristic], not as something Google states. |
| `learning.target_change_note` | changing the target value on an existing strategy does not trigger learning | [platform guidance] | Google states this explicitly and practitioners routinely get it backwards. Changing tCPA or tROAS is not the same as changing the strategy. |
| `learning.budget_note` | budget changes are absent from Google's trigger list | [heuristic] | This is an argument from absence, not a Google statement. Large budget jumps still cause volatility; they just do not formally restart learning. |

## Budget movement

| Key | Value | Tag | Notes |
|---|---|---|---|
| `budget.step` | **20%** per increment | [heuristic] | Drop to 15% when the campaign has had a reset inside the last `learning.judgement_window`, or when it sits below `conversion.volume_floor`. Both mean it is fragile. |
| `budget.step_wait` | at least 1 full conversion cycle between steps | [heuristic] | Cite `learning.duration` for what a cycle means on this account. |
| `budget.starve_floor` | daily budget below **10x target CPA** | [heuristic] | Uses the configured target, not the achieved CPA (see Denominators). Before calling a campaign starved, check impression share lost to budget: a campaign under the floor that is not losing impressions to budget is not constrained, and this rule does not apply to it. |

## Structure

| Key | Value | Tag | Notes |
|---|---|---|---|
| `asset_group.volume_floor` | **12 conversions per month per group** | [heuristic] | Single value on purpose: a range here produces different group counts for the same account. Move to 15 for considered purchases with cycles over 30 days, to 10 for impulse retail, and say which you used. |
| `asset_group.theme_purity` | one theme or product line per group | [heuristic] | Mixed groups make the asset-to-query match unreadable. |
| `listing_group.spend_concentration` | the top **20%** of SPENDING products by cost absorbing **70%+** of campaign spend | [heuristic] | Denominator is spending products, not the catalogue, per Denominators; the script prints the count it used. Both halves matter: a small slice of the catalogue taking most of the budget. 25% of products taking 70% is ordinary retail shape, not a flag. Healthy when those products beat target ROAS; a feed-mix constraint when they do not. Implemented in `../scripts/spend_concentration.py` as `concentration_flag`. |
| `asset.required_minimum` | 3 headlines, 1 long headline, 2 descriptions, 1 landscape (1.91:1) image, 1 square (1:1) image; plus 1 logo and 1 business name when brand guidelines are off | [platform guidance] | Google's minimum for a servable asset group ([asset requirements](https://developers.google.com/google-ads/api/performance-max/asset-requirements), checked 2026-08-04). Video and portrait (4:5) images are **optional**. With brand guidelines enabled, logo and business name come from campaign-level brand assets instead of the group. **Retail exception:** on a campaign linked to Merchant Center, Google auto-generates missing assets from the feed and the group serves anyway, usually at poor ad strength. So on retail, below-minimum means "running on material nobody wrote", not "not running". |
| `asset.working_target` | 8-12 headlines, 4-5 descriptions, all three image ratios, at least 1 video | [heuristic] | A band, not a threshold: anywhere inside it counts as met, and a group at 4 descriptions is at target, not one short. This is the one entry that stays a range, because it describes a healthy zone rather than a decision point. A practitioner target, not a Google rule. Note the ceilings: 15 headlines, 5 long headlines, 5 descriptions. Asking for a 6th description is asking for something the platform will not accept. |
| `asset.video_note` | a group with no video gets an auto-generated one | [platform guidance] | True and worth saying, but it is not a compliance failure. The group is servable without video. |

## Brand and cannibalization

| Key | Value | Tag | Notes |
|---|---|---|---|
| `brand.overlap_flag` | branded conversions at **20%+ of PMax conversions**, from the search terms report | [heuristic] | One meter, not "categories or spend". With only Search categories, you cannot compute this: report the label count as a label count and say the size is unknown (see Denominators, branded share). |
| `brand.cpa_gap_flag` | brand Search CPA below **50%** of PMax CPA | [heuristic] | Both sides must be computed on the same conversion basis. Comparing PMax purchases-only CPA against brand all-conversions CPA is the most common way this flag fires falsely. |

## Signal quality

| Key | Value | Tag | Notes |
|---|---|---|---|
| `conversion.value_spread_flag` | two or more primary conversion actions carrying the same value while their business outcomes differ | [heuristic] | The single most common cause of a campaign that improves on paper and not in the bank. |
| `conversion.offline_lag_floor` | offline import more than **7 days** behind | [heuristic] | Beyond this, bidding is optimising on a stale picture. |
| `conversion.volume_floor` | **30 primary conversions per 30 days per campaign** | [heuristic] | Primary only, per Denominators. Below this, period-over-period comparisons are not readable; say so instead of reporting a delta. Where a skill needs money-real conversions rather than primary ones, it says so and you report both counts. |

## Flags

Thresholds that decide whether a finding is raised at all. Each is a starting
point, not a rule; recalibrate and say which one you moved.

| Key | Value | Tag | Notes |
|---|---|---|---|
| `placement.waste_flag` | a placement family above **5%** of placement-report impressions with no plausible audience fit | [heuristic] | See Denominators for both "family" and the impression base. A group of placements must clear 5% on its own and list its members; aggregating small families over the line is the failure this threshold exists to prevent. Below the flag: `monitor`, and say it is below the bar. |
| `listing_group.top_block_dead_weight` | zero-conversion products holding more than **20%** of the top block's spend | [heuristic] | Checked separately from `listing_group.spend_concentration`, and reported even when that flag is off. The concentration flag has an AND in it and goes silent on ordinary catalogue shapes, so this is the check that catches a top block quietly carrying dead products. |
| `listing_group.zero_tail_flag` | a product with spend at or above **3x target CPA** and zero conversions | [heuristic] | Compute from the account's own target, never a fixed currency amount. One target CPA of spend is noise; three is a finding. Implemented in `../scripts/spend_concentration.py` as `flagged_tail_products`. |
| `feed.disapproval_flag` | a single disapproval reason affecting more than **5% of the catalogue** | [heuristic] | Catalogue means the full feed, per Denominators. Group by reason before applying it; the total disapproval count is not a reason. |
| `segment.margin_gap` | margin bands differing by more than **20 percentage points** | [heuristic] | Below this, splitting by margin buys nothing that separate targets inside one campaign could not. |
| `segment.starvation_flag` | a product segment below **5% of campaign impressions** despite matching demand | [heuristic] | Campaign impressions per Denominators. The strongest genuine argument for a split. Underperforming is not starving. |
| `newcustomer.list_staleness` | a customer list older than one full repeat-purchase cycle | [heuristic] | Measure the cycle from the account's own order data. Beyond it, recent buyers are being counted as new and carrying a premium. |
| `newcustomer.classification_gap` | platform new-customer share differing from the business figure by more than **15 percentage points** | [heuristic] | Above this the classification is wrong and every verdict built on it inherits the error. |
| `audience.signal_cap` | more than **3** audience signals on one asset group, none of them first-party | [heuristic] | More signals is not more steering. One converter list outsteers five interest signals. |
| `asset_group.fragmentation_flag` | more asset groups than monthly conversions divided by `asset_group.volume_floor` | [heuristic] | Same defect as running too many campaigns. Consolidate to the number the volume supports. |

## Reporting limits (not thresholds, but load-bearing facts)

All three checked against Google documentation on 2026-08-04. This section is
the most time-sensitive part of the pack: Performance Max reporting has gained
capabilities repeatedly, and a limit that was real in 2024 is the fastest way
for this pack to give confidently wrong advice. Re-check before trusting.

- **Per placement: still no cost or conversions.** The "where ads showed"
  report gives impressions only, and is positioned as a brand-safety surface.
  Any per-placement cost figure in an output is an estimate and must be
  labelled as one.
- **Per channel: cost IS available, since 2025.** The channel performance
  report breaks PMax down by Search, Display, YouTube, Discover, Maps, Gmail
  and Search partners, with impressions, clicks, conversions, conversion value
  **and cost**, for any date range after 6 June 2025
  ([channel performance report](https://support.google.com/google-ads/answer/16260130)).
  Do not tell a user the channel split is unavailable. Ask for this report.
- **Search terms: a real report exists for PMax.** Google runs a search terms
  report for Performance Max with actual triggering queries and performance
  metrics ([search terms report](https://support.google.com/google-ads/answer/16327396)).
  Prefer it over the Search categories tab wherever a skill needs query data.
- **Search categories remain aggregated.** The Insights categories tab is
  conversion-weighted and aggregated, so any share derived from it is an upper
  bound. Use it only when the search terms report is unavailable, and say which
  source the number came from.

## Auction behaviour

- **PMax does not outrank standard Shopping by campaign type.** Until October
  2024 a PMax campaign automatically won against a standard Shopping campaign
  in the same account for the same product. Google removed that: the higher Ad
  Rank now serves, the same as between any other campaign types
  ([change writeup](https://www.seroundtable.com/google-ads-pmax-priority-standard-shopping-38265.html)).
  Most of the internet still repeats the old rule, which makes this a common
  source of wrong diagnosis rather than an obscure detail.
