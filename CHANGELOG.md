# Changelog

## [1.0.0] - 2026-08-04

First public release. 15 skills.

### Added

- Five skills carried over from the original five-skill guide published
  2026-07-07: brand cannibalization, conversion signal quality, spend exposure
  and placement waste, asset group structure, scaling and learning-phase
  guardrail.
- Ten new skills: brand exclusions coverage, asset coverage completeness,
  audience signal and search themes, product spend concentration, listing
  group segmentation, product feed blockers, new customer acquisition goal,
  PMax versus Shopping comparison, post-change readout, weekly readout.
- `references/thresholds.md` as the single home for every number in the pack,
  each tagged `[platform guidance]` or `[heuristic]`. Skills cite keys rather
  than restating values.
- `references/output-standard.md` with shared evidence labels, decision labels
  and the required `What this could not see` section.
- `scripts/spend_concentration.py` and `scripts/variance_check.py` for the two
  skills where eyeballing the arithmetic produces disagreement between runs.
- `examples/` with a full worked audit and the sample exports its numbers come
  from.

### Changed from the original five

- Every skill now carries decision rules with unit-bearing thresholds. The
  original five relied on judgement without stated criteria in four of five
  cases, which meant two runs on the same export could reach different
  verdicts.

## [1.1.0] - 2026-08-04

Factual correction release, after an external accuracy review. Three claims
about how Google Ads works were wrong, and being internally consistent across
five files is exactly why the pack's own checks did not see them.

### Fixed

- **PMax no longer outranks standard Shopping by campaign type.** Google
  removed that behaviour in October 2024; the higher Ad Rank serves.
  `pmax-vs-shopping-comparison-pmax` was built on the retired rule and gave the
  opposite recommendation to the correct one. Rewritten around impression share
  lost to rank, which is what now separates a mechanical decline from a real
  auction loss.
- **Asset minimums were wrong and mislabelled as a Google rule.** The pack said
  5 headlines, 5 descriptions, 3 image ratios and 1 video were Google's
  minimums. Google's actual minimum is 3 headlines, 1 long headline, 2
  descriptions, 1 landscape and 1 square image, 1 logo, 1 business name, and
  video is optional. Five descriptions is Google's *maximum*. Split into
  `asset.required_minimum` [platform guidance] and `asset.working_target`
  [heuristic].
- **The channel split is reportable, with cost, since 2025.** The pack told
  users it was unavailable and instructed skills to refuse the question. Three
  files corrected.
- **A search terms report exists for PMax.** `brand-cannibalization-audit-pmax`
  now asks for it first and treats Search categories as the fallback. Its
  worked example no longer converts a count of category labels into a
  conversion share, which was the estimate laundering the caveat was hiding.
- **Brand exclusions cover YouTube search too.** The pack said display and
  video were uncovered without qualification, which would tell a user to
  ignore a real leak.
- Added campaign-level negative keywords as a control, available since 2025 and
  previously absent from the pack entirely.
- `learning.reset_triggers` now uses Google's own wording, with our paraphrase
  marked as ours. Added that changing a target value does not trigger learning.

### Changed

- Install command now copies `AGENTS.md` and `examples/`. Without `AGENTS.md`
  the composition rules never reached the user, so the pack installed as
  fifteen prompts rather than a system.
- README leads with the no-terminal path: the skills are markdown, so they can
  be pasted into any assistant. The full install was gating the pack behind a
  tool most of the audience does not have.
