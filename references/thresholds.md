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
| `learning.reset_triggers` | bid strategy change, conversion goal change, campaign status change | [platform guidance] | Google confirms these restart learning. Budget changes do not formally reset it. |

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
| `asset.coverage_floor` | 5 headlines, 5 descriptions, 3 image aspect ratios, 1 video per asset group | [platform guidance] | Google's stated minimums. Missing video means Google auto-generates one. |

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

- Google does not report cost or conversions per placement for PMax. The
  "where ads appeared" report gives impressions only. Any per-placement cost
  figure in an output is an estimate and must be labelled as one.
- Google does not report a channel split (Search vs Shopping vs YouTube vs
  Display vs Discover) natively for PMax. Scripts and third-party tools infer
  it. Label every inferred split as an estimate.
- Search categories in PMax Insights are aggregated and conversion-weighted,
  not a raw search terms report. Treat any derived share as an upper bound.
