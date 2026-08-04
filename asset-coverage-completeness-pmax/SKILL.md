---
name: asset-coverage-completeness-pmax
description: Checks whether each Performance Max asset group gives Google enough material to build good ads, and finds the gaps that force auto-generated substitutes. Use when an asset group underdelivers, or before blaming structure for a performance problem.
---

# Asset coverage completeness

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

Run this before `asset-group-structure-audit-pmax` recommends any structural
change. Structure cannot fix a group Google has nothing to build with.

## Use this skill when

An asset group serves less than expected, ad strength sits at poor or average,
or auto-generated assets are appearing that nobody wrote.

## Required input

- Per asset group: headline count, long headline count, description count,
  image count by aspect ratio, logo count, video count, sitelinks and other
  extensions.
- Ad strength rating per group.
- Whether automatically created assets and auto-generated video are enabled.
- The landing page URL per group.

## Analysis workflow

1. Compare each group against `asset.coverage_floor`. Note which minimums are
   met by real assets rather than by Google's substitutes.
2. Check video specifically. A group without a video gets an auto-generated
   one built from its images, and that asset carries the brand into YouTube
   whether or not anyone approved it. Most owners do not know this is
   happening.
3. Check image aspect ratios. A missing ratio silently removes the group from
   the placements that need it, which reads as a targeting problem and is not.
4. Check headline variety, not just count. Five headlines that say the same
   thing give the system one message with four spares.
5. Check whether automatically created assets are on. If they are, some of the
   copy running is not copy anyone wrote, and it is pulled from the landing
   page.
6. Read ad strength as a coverage proxy only. It measures variety and
   completeness, not persuasion, and chasing it for its own sake is a known
   waste of effort. Say that when recommending against it.

## Decision rules

- Below `asset.coverage_floor` on any dimension -> `do_now` on filling the
  gap, before any structural or budget change.
- No video asset -> `do_now`, and state that an auto-generated one is already
  running in its place.
- Missing an image aspect ratio -> `do_now`. This is the cheapest reach gain
  available in PMax.
- Automatically created assets on, with no review process -> `approval_needed`
  on either reviewing them or turning them off, and name the brand risk.
- Ad strength poor while coverage meets the floor -> `ignore` the rating and
  look at message variety instead. Do not recommend adding assets purely to
  move the rating.

## Output format

Open with one line: does Google have enough to work with in every group.

| Asset group | Headlines | Descriptions | Image ratios | Video | Ad strength | Gap | Recommendation |
|---|---|---|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: 3 groups. Group A: 11 headlines, 4 descriptions, all ratios, 1 video,
strength excellent. Group B: 5 headlines, 5 descriptions, square and landscape
only, no video, strength good. Group C: 3 headlines, 2 descriptions, square
only, no video, strength poor. Automatically created assets on across the
account.

Reading: group C is below `asset.coverage_floor` on three dimensions and is
running auto-generated copy and an auto-generated video. Group B is missing
the portrait ratio, which cuts it out of several vertical placements. Group A
is fine.

Output: "No, in two of three groups." Group C `do_now` on headlines,
descriptions and video, and note it is currently representing the brand with
material nobody wrote. Group B `do_now` on one portrait image. Automatically
created assets flagged `approval_needed` for a review pass.

## Guardrails

- Never recommend assets purely to raise the ad strength rating.
- Never treat a missing aspect ratio as a targeting problem.
- Never leave auto-generated video unmentioned when a group has no video.
- Do not upload or remove assets. Recommend, and let a human approve.
