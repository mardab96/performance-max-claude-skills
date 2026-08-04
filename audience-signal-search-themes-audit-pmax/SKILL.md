---
name: audience-signal-search-themes-audit-pmax
description: Reviews the audience signals and search themes feeding a Performance Max campaign, and separates the ones steering it from the ones that are decoration. Use when PMax reaches the wrong people, or before adding more signals in the hope of fixing targeting.
---

# Audience signal and search themes audit

Shared quality bar: `../references/output-standard.md`. All numbers cited here
live in `../references/thresholds.md`.

The most common misunderstanding this skill corrects: audience signals are a
hint about where to start looking, not a targeting restriction. A campaign
will serve outside them and is supposed to.

## Use this skill when

Lead quality is wrong, the campaign reaches an audience nobody wanted, or
someone is about to add a fifth audience signal to fix targeting.

## Required input

- Audience signals per asset group: type (customer list, custom segment,
  interest, demographic, remarketing), size, source.
- Search themes per asset group, if used.
- The customer definition in the user's own words: who buys, who does not.
- Asset group performance, so signals can be read against outcomes.

## Analysis workflow

1. Classify each signal by strength. First-party data (customer lists,
   converters, high-intent site visitors) steers hardest. Custom segments
   built from competitor URLs and search terms are next. Broad interest and
   demographic signals are the weakest and are frequently just noise.
2. Check customer list sizes against Google's match minimums. A list that
   never matched is a signal that does not exist, and it will sit in the UI
   looking active.
3. Read search themes against the Search categories the campaign actually
   serves on. Themes that appear nowhere in the categories are either too
   narrow or being ignored.
4. Check for contradiction: a remarketing signal plus a new-customer goal, or
   a signal describing existing buyers on a campaign meant to find new ones.
   This is common and it pulls in two directions at once.
5. Ask what the signal is supposed to change. If nobody can say what the
   campaign would do differently without it, it is decoration.
6. Count signals per asset group. More signals is not more steering; a group
   with six weak signals is steering less than one with a single converter
   list.

## Decision rules

- No first-party signal on any asset group -> `do_now` on adding a converter
  list. This is the highest-leverage change available in the whole skill.
- Customer list below Google's stated match minimum -> `investigate`; the
  signal is inactive regardless of what the UI shows.
- Search theme absent from Search categories after at least
  `learning.judgement_window` -> `monitor` or remove; it is not landing.
- Remarketing signal on a campaign carrying a new-customer goal ->
  `approval_needed` on removing one or the other, and name which goal wins.
- A group crossing `audience.signal_cap` -> consolidate. Say plainly that
  signals do not restrict serving.

## Output format

Open with one line: is this campaign being steered, or is it guessing.

| Asset group | Signal | Type | Strength | Landing | Recommendation |
|---|---|---|---|---|---|

Then `What this could not see`, `Missing data`, `Approval gates`.

## Practical example

Input: 3 asset groups. Group A has 4 interest signals and one demographic.
Group B has a customer list of 340 emails plus 2 interests. Group C has a
custom segment built from three competitor domains. Search themes: 6 in group
A, none elsewhere. The offer is B2B software for logistics teams.

Reading: group B's list is likely below the match minimum, so B is effectively
running on two weak interest signals. Group A is running on five weak signals,
which steers less than one good one. Group C's custom segment is the strongest
thing in the account. No group has a converter list.

Output: "Guessing, in two of three groups." One change first: build a
converter list from the last 12 months of closed deals and put it on every
group. Then the table, with group A's five signals marked for consolidation
and the 340-email list marked `investigate` for match rate.

## Guardrails

- Never describe an audience signal as targeting or a restriction.
- Never recommend adding signals as a fix for lead quality; that is the
  conversion signal's job, not the audience signal's.
- Never assume a customer list is active because it appears in the UI.
- Do not add or remove signals. Recommend, and let a human approve.
