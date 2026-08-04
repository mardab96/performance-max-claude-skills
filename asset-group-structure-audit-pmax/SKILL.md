---
name: asset-group-structure-audit-pmax
description: Checks whether Performance Max asset groups map cleanly onto real products or themes, and finds the mixed groups that make the campaign unreadable. Use when performance varies wildly between asset groups, or before adding another one.
---

# Asset group structure audit

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

## Use this skill when

One asset group carries the campaign and the rest do nothing, or someone is
about to add a sixth group to a campaign that cannot feed the five it has.

## Required input

- Asset group list: name, stated theme, headlines, descriptions, images,
  video, landing page, conversions, spend.
- The product or service list the campaign is meant to cover.
- Campaign conversion volume for the same period.

## Analysis workflow

1. Run the coverage check first, or confirm it has been run. Coverage outranks
   structure (`AGENTS.md`, precedence rule 4), and a group below
   `asset.required_minimum` is a coverage finding rather than a structural one,
   even when it looks like a structural problem. Reclassify it before counting
   groups.
2. For each asset group, write down in one sentence what it is supposed to
   sell. If that sentence needs an "and", the group is mixed
   (`asset_group.theme_purity`).
3. Check the landing page per group. Two groups pointing at the same page is
   usually a naming exercise, not a structure.
4. Check conversion volume per group against `asset_group.volume_floor`.
   Groups below it cannot be optimised, only consolidated or fed more budget.
5. Check asset coverage against `asset.required_minimum`. A group missing video
   gets an auto-generated one, which is why some groups look cheap and
   convert badly.
6. Count groups against total campaign conversions. More groups than the
   conversion volume can support is fragmentation, and it is the same defect
   as running too many campaigns.
7. Name the single structural change most likely to move performance. One, not
   a list. A list of five structural changes is how accounts get churned.

## Decision rules

- Group below `asset_group.volume_floor` and sharing a landing page with
  another group -> `do_now` on consolidation.
- Group below the floor with a distinct product and a distinct page ->
  `monitor`, not consolidate. Some products are simply small.
- Mixed theme (the "and" test fails) -> `approval_needed` on splitting, and
  state the cost: the new group starts learning from scratch
  (`learning.duration`).
- Coverage below `asset.required_minimum` with NO Merchant Center feed ->
  `do_now` on assets, and structural work waits. Structure cannot fix a group
  that cannot serve.
- Coverage below `asset.required_minimum` WITH a feed -> `do_now` on assets,
  but structural work proceeds and the group counts as live. Google fills the
  gaps from the feed, so the group is serving on material nobody wrote
  (`asset.required_minimum`, retail exception). Calling a running retail group
  dead in front of someone who can watch it spending is the fastest way to lose
  the room.
- Group count crossing `asset_group.fragmentation_flag` -> recommend
  consolidating to the number the volume supports.

## Output format

Open with the one structural change that matters most.

| Asset group | Theme clear | Conversions/mo | Asset coverage | Issue | Recommendation |
|---|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: 5 asset groups, campaign at 46 conversions/month. Groups: "Main" (31
conv, page /), "Brand" (9 conv, page /), "Summer promo" (4 conv, page
/summer), "Accessories and spare parts" (2 conv, page /shop), "Test" (0 conv,
page /, no video).

Reading: 46 conversions divided by `asset_group.volume_floor` supports 3.8
groups, so five exceeds the ceiling and `asset_group.fragmentation_flag` fires.
The account should be running four groups, not five. (One number, not a range:
the floor was collapsed to a single value precisely so this count cannot come
out differently for two people on the same account.) "Main" and
"Brand" share a landing page and neither has a distinct theme. "Accessories and
spare parts" fails the "and" test. "Test" has 3 headlines and no long headline,
which is below `asset.required_minimum`. This account has no Merchant Center
feed, so that group genuinely cannot serve; on a retail account with a feed the
same shortfall would mean it serves on auto-generated assets and still counts
as live. Say which case you are in, every time.

The order is forced here and it is worth naming: coverage outranks structure,
so "Test" being unservable is dealt with first, and it is a coverage finding
rather than a structural one. That leaves exactly one structural change.

Output: one structural change, "merge Main and Brand", because they share a
page and neither carries a distinct theme. Separately, and not as a structural
change, "Test" is `do_now` on either fixing its assets or removing it, since it
currently cannot serve. "Accessories and spare parts" is `monitor`, not a
split: splitting it takes the group count up while the volume supports fewer,
and the "and" problem is real but cannot be fixed by adding groups this
account cannot feed. "Summer promo" is `monitor` because a seasonal group with
its own page is allowed to be small.

## Guardrails

- Never recommend more than one structural change at a time.
- Never recommend a split without stating the learning cost.
- Never treat a small group as broken when it maps to a small product.
- Do not create, merge or pause asset groups. Recommend, and let a human
  approve.
