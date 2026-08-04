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
