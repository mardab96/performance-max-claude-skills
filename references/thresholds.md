# Thresholds

Single home for every number used across this pack. Skills cite this file by
name instead of restating a value. If a skill needs a number that is not here,
add it here first, then cite it.

Every entry carries a unit and a tag:

- `[platform guidance]` - stated by Google in its own documentation or UI.
- `[heuristic]` - a practitioner starting point, not a platform rule.
  Recalibrate against the account's own history and say which one you moved
  and why.

## Learning and stability

| Key | Value | Tag | Notes |
|---|---|---|---|
| `learning.duration` | up to ~3 weeks, or 1-2 conversion cycles, whichever is longer | [platform guidance] | Google's stated learning period after a significant change. |
| `learning.judgement_window` | ~4-6 weeks | [heuristic] | Minimum elapsed time before drawing a conclusion about a change. Shorter reads are noise. |
| `learning.reset_triggers` | a new or reactivated bid strategy, a setting change to the bid strategy, a composition change (campaigns or asset groups added to or removed from the strategy) | [platform guidance] | Google's own wording ([learning period](https://support.google.com/google-ads/answer/13020501), checked 2026-08-04). Conversion goal and campaign status changes are our reading of "composition change", so treat those two as [heuristic], not as something Google states. |
| `learning.target_change_note` | changing the target value on an existing strategy does not trigger learning | [platform guidance] | Google states this explicitly and practitioners routinely get it backwards. Changing tCPA or tROAS is not the same as changing the strategy. |
| `learning.budget_note` | budget changes are absent from Google's trigger list | [heuristic] | This is an argument from absence, not a Google statement. Large budget jumps still cause volatility; they just do not formally restart learning. |

## Budget movement

| Key | Value | Tag | Notes |
|---|---|---|---|
| `budget.step` | ~15-20% per increment | [heuristic] | Step size that usually avoids a volatility spike. |
| `budget.step_wait` | at least 1 full conversion cycle between steps | [heuristic] | Cite `learning.duration` for what a cycle means on this account. |
| `budget.starve_floor` | daily budget below ~10x target CPA | [heuristic] | Below this the campaign rarely leaves learning. Compute from the account's own CPA, never a fixed currency amount. |

## Structure

| Key | Value | Tag | Notes |
|---|---|---|---|
| `asset_group.volume_floor` | ~10-15 conversions per month per group | [heuristic] | Below this, consolidation is usually the better call than optimisation. |
| `asset_group.theme_purity` | one theme or product line per group | [heuristic] | Mixed groups make the asset-to-query match unreadable. |
| `listing_group.spend_concentration` | the top 20% of products by cost absorbing 70%+ of campaign spend | [heuristic] | Both halves matter: a small slice of the catalogue taking most of the budget. 25% of products taking 70% is ordinary retail shape, not a flag. Healthy when those products beat target ROAS; a feed-mix constraint when they do not. Implemented in `../scripts/spend_concentration.py` as `concentration_flag`. |
| `asset.required_minimum` | 3 headlines, 1 long headline, 2 descriptions, 1 landscape (1.91:1) image, 1 square (1:1) image, 1 logo, 1 business name | [platform guidance] | Google's actual minimum for a servable asset group ([asset requirements](https://developers.google.com/google-ads/api/performance-max/asset-requirements), checked 2026-08-04). Video and portrait (4:5) images are **optional**. Below this the group cannot run. |
| `asset.working_target` | 8-12 headlines, 4-5 descriptions, all three image ratios, at least 1 video | [heuristic] | A practitioner target, not a Google rule. Note the ceilings: 15 headlines, 5 long headlines, 5 descriptions. Asking for a 6th description is asking for something the platform will not accept. |
| `asset.video_note` | a group with no video gets an auto-generated one | [platform guidance] | True and worth saying, but it is not a compliance failure. The group is servable without video. |

## Brand and cannibalization

| Key | Value | Tag | Notes |
|---|---|---|---|
| `brand.overlap_flag` | branded categories at roughly 20%+ of search categories or spend | [heuristic] | Flag threshold when an active brand Search campaign exists alongside PMax. |
| `brand.cpa_gap_flag` | brand Search CPA below ~50% of blended PMax CPA | [heuristic] | Indicates PMax is buying conversions the brand campaign would have won cheaper. |

## Signal quality

| Key | Value | Tag | Notes |
|---|---|---|---|
| `conversion.value_spread_flag` | two or more primary conversion actions carrying the same value while their business outcomes differ | [heuristic] | The single most common cause of a campaign that improves on paper and not in the bank. |
| `conversion.offline_lag_floor` | offline import older than 7 days behind | [heuristic] | Beyond this, bidding is optimising on a stale picture. |
| `conversion.volume_floor` | ~30 conversions per 30 days per campaign | [heuristic] | Below this, most period-over-period comparisons in this pack are not readable. Say so instead of reporting a delta. |

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
