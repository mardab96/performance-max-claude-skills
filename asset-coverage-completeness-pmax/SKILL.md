---
name: asset-coverage-completeness-pmax
description: Checks what a Performance Max asset group is missing, separating Google's actual minimum for a servable group from the practitioner target that improves performance. Use when an asset group underdelivers or serves less than expected. Do not use for whether the groups are split correctly; that is asset-group-structure-audit-pmax, and it should run after this one.
---

# Asset coverage completeness

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

Run this before `asset-group-structure-audit-pmax` recommends any structural
change. Structure cannot fix a group Google has nothing to build with.

**Two different bars, and conflating them is the mistake this skill exists to
avoid.** `asset.required_minimum` is what Google requires for the group to run
at all; below it the group is broken. `asset.working_target` is a practitioner
target; below it the group runs fine and probably underperforms. A group can be
fully compliant and still be worth improving, and telling a user their
compliant group is deficient burns your credibility on the one claim they can
check in a minute.

Note the ceilings inside `asset.working_target`. Descriptions max out at 5, so
a group with 5 descriptions is at the platform limit, not short of one.

## Use this skill when

An asset group serves less than expected, ad strength sits at poor or average,
or auto-generated assets are appearing that nobody wrote.

## Required input

- Per asset group: counts of headlines, long headlines, descriptions, images by
  aspect ratio, logos, business name, videos.
- Ad strength per group.
- Whether automatically created assets and auto-generated video are enabled.
- The landing page per group.
- Whether the campaign is linked to a Merchant Center feed. This decides what a
  shortfall means and the skill cannot run correctly without it.
- Whether brand guidelines are switched on, since that moves logo and business
  name from the group to the campaign.

Most of this is not exportable and has to be read off the interface per group.
Say so if the user has many groups, because the transcription cost is real and
it is the reason this audit often does not get done.

## Analysis workflow

1. Check each group against `asset.required_minimum` first, and check whether
   the campaign is linked to Merchant Center before saying what a shortfall
   means. Without a feed, below-minimum means the group cannot serve. With a
   feed, Google fills the gaps from the product data and the group serves on
   material nobody wrote (`asset.required_minimum`, retail exception). Both are
   urgent; only one of them is an outage, and calling a running retail group
   dead is the fastest way to be wrong in front of someone who can see it
   running.
2. Then check against `asset.working_target`, and label these findings clearly
   as improvements rather than compliance failures.
3. Check video separately, using `asset.video_note`. A group without video gets
   an auto-generated one built from its images, which carries the brand into
   YouTube whether or not anyone approved it. Say this, and do not call it a
   compliance failure, because it is not one.
4. Check image aspect ratios. Landscape and square are required; portrait 4:5
   is optional but its absence removes the group from placements that need it,
   which reads like a targeting problem and is not.
5. Check headline variety, not just count. Five headlines saying the same thing
   give the system one message and four spares.
6. Check whether automatically created assets are on. If they are, some of the
   live copy was written by Google from the landing page, not by anyone here.
7. Read ad strength as a coverage proxy only. It measures variety and
   completeness, not persuasion, and chasing it for its own sake is known
   wasted effort.

## Decision rules

- Below `asset.required_minimum` on any dimension, no Merchant Center feed ->
  `do_now`. The group cannot serve, and this blocks every structural and budget
  recommendation elsewhere.
- Below `asset.required_minimum` with a feed attached -> `do_now` too, but say
  what is actually happening: the group runs on auto-generated assets. It does
  not block structural work, because the group is serving.
- Meets the minimum but below `asset.working_target` -> `test`, phrased as an
  improvement. Never `do_now`, and never phrased as a rule breach.
- No video -> `test` on adding one, and state plainly that an auto-generated
  one is already running in its place. Not `do_now`: the group is servable.
- Missing portrait 4:5 -> `test`. It is the cheapest reach gain available in
  PMax, and it is still optional.
- Automatically created assets on with no review process -> `approval_needed`
  on either reviewing them or switching them off, and name the brand risk.
- Ad strength poor while the group meets `asset.working_target` -> `ignore` the
  rating and look at message variety instead. Do not add assets to move a
  score.

## Output format

Open with one line: is any group unable to serve, and separately, is any group
below the working target.

| Asset group | Meets minimum | vs working target | Video | Ad strength | Gap | Recommendation |
|---|---|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: three groups. Group A: 11 headlines, 2 long headlines, 4 descriptions,
all three image ratios, logo and business name present, 1 video, strength
excellent. Group B: 5 headlines, 1 long headline, 5 descriptions, landscape and
square only, logo and business name present, no video, strength good. Group C:
3 headlines, no long headline, 2 descriptions, square only, logo and business
name present, no video, strength poor. Automatically created assets on across
the account.

Reading against `asset.required_minimum`: Group C fails twice, on the missing
long headline and the missing landscape image, so it cannot serve. Groups A and
B both clear the minimum in full. Group B's 5 descriptions are the platform
ceiling, so that is the top of the range, not a shortfall.

Reading against `asset.working_target`: Group A meets it on every dimension.
11 headlines is inside the 8-12 band and 4 descriptions is inside the 4-5 band,
so Group A gets no recommendation at all. Group B clears the minimum but sits
at 5 headlines against a band of 8-12, which is its largest gap, and it has no
video and no portrait image. Group C is short on everything, but that is
secondary to the fact that it cannot serve.

Output: "One group cannot serve. One is servable and below target. One is
fine."

Group C `do_now` on the long headline and the landscape image, because until
those exist nothing else about that group matters and its structural
recommendations elsewhere are blocked.

Group B `test` on headlines first, since 5 against a band of 8-12 is the
biggest gap, then on a video and a portrait image, with the note that an
auto-generated video is already representing the brand on YouTube.

Group A gets nothing. Inventing a recommendation for a compliant, at-target
group is exactly the failure this skill opens by warning against.

Automatically created assets `approval_needed` for a review pass, since live
copy is being written from the landing page by Google rather than by anyone
here.

## Guardrails

- Never present `asset.working_target` as a Google requirement. It is a
  practitioner target and the user can check the real minimum in one search.
- Never recommend a 6th description. Five is the platform maximum.
- Never call a missing video a compliance failure. It is optional.
- Never recommend assets purely to raise the ad strength rating.
- Never leave auto-generated video unmentioned when a group has no video.
- Do not upload or remove assets. Recommend, and let a human approve.
