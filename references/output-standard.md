# Output standard

Shared across every skill in this pack.

## Required sections

Every skill returns, in this order:

1. Its own findings table.
2. `What this could not see` - the reporting limits that apply to this
   specific answer. Cite `thresholds.md` (Reporting limits) rather than
   restating them.
3. `Missing data` - the exact export or field that would change the answer,
   and which finding each one would firm up.
4. `Approval gates` - what needs a human yes before anything moves.

Skills that produce a single verdict (triage, readouts, scale readiness) open
with a one-line verdict before the table. Skills that produce a ranked list do
not; a verdict line on a ranked table is theatre.

## Evidence labels

Use exactly one per row:

- `export` - came from a downloaded report.
- `screenshot` - read off the UI.
- `url` - checked on a live page.
- `notes` - supplied by the user in conversation.
- `hypothesis` - inferred, not observed.
- `needs_data` - cannot be assessed with what was provided.

## Decision labels

Use exactly one per row:

- `do_now`
- `test`
- `investigate`
- `monitor`
- `ignore`
- `approval_needed`

## Confidence

Three values, each with a stated test, so two people reading the same evidence
land on the same label.

- **`high`** - the finding comes from an export, the period clears
  `conversion.volume_floor`, no learning event sits inside it, and no
  denominator had to be assumed. All four.
- **`medium`** - exactly one of those four is missing, and it is NOT the
  volume one. Say which in the row.
- **`low`** - two or more missing, OR the campaign is under
  `conversion.volume_floor` (even if that is the only thing missing), OR the
  conversion signal audit failed. Any one of these is enough on its own.

The volume condition is deliberately listed in both directions so there is no
overlap: under the floor is always `low`, never `medium`, whatever else is in
place.

A row labelled `high` with an assumed denominator is the most common way this
scale gets abused. If you had to decide what a number was measured against,
that is `medium` at best.

## Hard rules

- Diagnosis only. Never edit a campaign, budget, feed, exclusion list,
  conversion action or page. Every recommendation is a decision put in front
  of a human.
- Separate what was observed from what was inferred. An inference never enters
  a findings table labelled `export`.
- Never state a per-placement cost as fact. That is genuinely unavailable, so
  any figure is an estimate and must be labelled as one.
- The channel split is a different case: it is reportable with cost since
  2025. Never say it cannot be seen. Ask for the channel performance report.
- Never recommend scaling before the conversion signal has been assessed.
  PMax amplifies whatever it is fed.
- Never report a period-over-period delta on a campaign below
  `conversion.volume_floor`. Say the sample is too small instead.
- Name missing data. An answer that hides its own gaps is worse than no
  answer, because it reads as complete.
