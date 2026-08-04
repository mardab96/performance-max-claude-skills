# Working with this pack

Guidance for the model running these skills, and for anyone extending them.

## The order matters

`conversion-signal-quality-audit-pmax` runs first on any account that has not
been audited before. Not as etiquette: PMax optimises toward whatever it is
told to count, so a structural finding on a campaign with a broken conversion
signal is a finding about the wrong thing. If the signal audit has not been
run, say so before answering a structural question.

After that the usual order is brand cannibalization, then structure, then
scaling. `weekly-pmax-readout` consumes the others rather than replacing them.

## How these skills compose

Several skills produce inputs for others. When you run one, check whether its
output changes an earlier verdict:

- Signal audit fails -> every performance verdict in the session drops to
  `low` confidence, and scaling recommendations are withdrawn.
- Asset coverage below `asset.required_minimum` -> structure recommendations
  wait. Structure cannot fix a group that cannot serve. Note the precision:
  only the required minimum blocks. A group below `asset.working_target` runs
  fine and blocks nothing, and treating those two as one bar is the mistake
  `asset-coverage-completeness-pmax` exists to prevent.
- A learning reset inside the window -> post-change readout and scaling
  guardrail both refuse to attribute. Say the date it becomes readable
  instead of hedging.
- Feed blockers found -> product spend concentration is reading a partial
  catalogue, and its shares are wrong until the blockers clear.

## Numbers

Every threshold lives in `references/thresholds.md` and nowhere else. Cite the
key, do not restate the value. If you need a number that is not there, add it
there first with a unit and a tag, then cite it.

Two skills delegate arithmetic to `scripts/`. Use them rather than eyeballing
the maths; the script and the skill are written to agree, and the script's
docstring names the skill it belongs to.

## Honesty rules that are not optional

These skills exist because PMax hides things. The value is in saying what
cannot be seen, so:

- Never state a per-placement cost as fact; that one really is unavailable.
- Do NOT tell a user the channel split is unavailable. It has been reportable
  with cost since 2025; ask for the channel performance report instead.
- Never present a search-category share as exact. The source is aggregated.
- Never report a period-over-period delta below `conversion.volume_floor`.
- Never attribute a movement before `learning.duration` has passed.
- Always fill the `What this could not see` section. An answer that hides its
  own gaps is worse than no answer, because it reads as complete.

## When the user asks for an action

They cannot have one. Every skill here is diagnosis-only and every
recommendation is a decision for a human. If asked to make the change, say
what to change and where, and stop there.

## Extending the pack

A new skill needs: frontmatter with a natural activation phrase, the required
input list, at least five workflow steps, decision rules whose thresholds all
resolve to `references/thresholds.md`, an output format using the shared
evidence and decision labels, one worked example with real arithmetic, and
guardrails.

Before shipping a change to any threshold, grep the bare number across the
whole pack and reconcile every hit, including scripts, README and worked
examples. A threshold that agrees in four places and disagrees in the fifth is
the failure mode this structure exists to prevent.
