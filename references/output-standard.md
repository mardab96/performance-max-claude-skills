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

`high` / `medium` / `low`. Drop to `low` whenever the campaign is under
`conversion.volume_floor` (see `thresholds.md`), and say that is why.

## Hard rules

- Diagnosis only. Never edit a campaign, budget, feed, exclusion list,
  conversion action or page. Every recommendation is a decision put in front
  of a human.
- Separate what was observed from what was inferred. An inference never enters
  a findings table labelled `export`.
- Never state a per-placement cost or a channel split as fact. Both are
  unavailable in PMax reporting; both are estimates when they appear at all.
- Never recommend scaling before the conversion signal has been assessed.
  PMax amplifies whatever it is fed.
- Never report a period-over-period delta on a campaign below
  `conversion.volume_floor`. Say the sample is too small instead.
- Name missing data. An answer that hides its own gaps is worse than no
  answer, because it reads as complete.
