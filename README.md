# 15 Claude Skills for Google Ads Performance Max

A pack of 15 production-ready Claude Skills for auditing Performance Max
campaigns: brand cannibalization, conversion signal quality, spend exposure,
asset groups, product feeds, scaling guardrails and the weekly readout.

Every skill is diagnosis-only. None of them log into an account, change a
campaign, edit a feed or move a budget. They read exports you already have and
hand you a decision.

## What is inside

| # | Skill | Folder | What it answers |
|---|---|---|---|
| 1 | Conversion signal quality audit | `conversion-signal-quality-audit-pmax` | Is this campaign optimising toward money, or toward the cheapest worthless outcome? |
| 2 | Brand cannibalization audit | `brand-cannibalization-audit-pmax` | How much of the reported performance is branded demand the brand campaign would have won cheaper? |
| 3 | Brand exclusions coverage check | `brand-exclusions-coverage-check-pmax` | Do the brand exclusions actually cover the brand, and what do they never reach? |
| 4 | Spend exposure and placement waste | `spend-exposure-placement-waste-pmax` | Where is this campaign showing up that it should not, given that Google hides per-placement cost? |
| 5 | Asset group structure audit | `asset-group-structure-audit-pmax` | Do the asset groups map onto real products, and which single change would help most? |
| 6 | Asset coverage completeness | `asset-coverage-completeness-pmax` | Does Google have enough material to build good ads, or is it generating substitutes? |
| 7 | Audience signal and search themes audit | `audience-signal-search-themes-audit-pmax` | Is this campaign being steered, or is it guessing? |
| 8 | Product spend concentration | `product-spend-concentration-pmax` | Which products absorb the budget without returning it? |
| 9 | Listing group segmentation | `listing-group-segmentation-pmax` | Should this campaign be split, and into how many? Usually fewer than proposed. |
| 10 | Product feed blockers | `product-feed-blockers-pmax` | Why are approved products still not serving? |
| 11 | New customer acquisition goal review | `new-customer-acquisition-goal-review-pmax` | Can this campaign tell a new customer from a returning one, and what is the premium costing? |
| 12 | PMax versus Shopping comparison | `pmax-vs-shopping-comparison-pmax` | Which campaign type is actually winning once overlap and attribution are accounted for? |
| 13 | Scaling and learning-phase guardrail | `scaling-learning-phase-guardrail-pmax` | Is this campaign stable enough to scale, and how big should the step be? |
| 14 | Post-change readout | `post-change-readout-pmax` | Did the change cause this, or was it the season? |
| 15 | Weekly PMax readout | `weekly-pmax-readout` | What do I tell the client, in words they will read? |

## Where to start

Run `conversion-signal-quality-audit-pmax` first, always. Every other skill in
this pack is unreliable while the conversion signal is wrong, because PMax
optimises toward whatever it is told to count.

After that, the usual order is: brand cannibalization, then structure, then
scaling.

## How to install

### You do not need Claude Code

Start here, because the install below is the slowest way in and most people do
not need it. **Every skill is a markdown file and a markdown file is a prompt.**
Open any `SKILL.md` on GitHub, copy the whole thing, paste it into Claude,
ChatGPT or whatever you already use, then paste your exported data underneath.
That is 90% of the value with none of the setup.

The only parts that genuinely need a terminal are the two Python scripts, and
only two of the fifteen skills call them.

### Claude Code, for the full install

```bash
git clone https://github.com/mardab96/performance-max-claude-skills.git
mkdir -p ~/.claude/skills
cp -r performance-max-claude-skills/*-pmax \
      performance-max-claude-skills/weekly-pmax-readout \
      performance-max-claude-skills/references \
      performance-max-claude-skills/scripts \
      performance-max-claude-skills/examples \
      performance-max-claude-skills/AGENTS.md \
      ~/.claude/skills/
```

Four of those lines are not optional and it is worth knowing why:

- `references` holds every number the skills cite. Without it the thresholds
  do not resolve.
- `scripts` is called by two skills.
- `AGENTS.md` holds how the skills compose, including the rule that a failed
  conversion signal audit drops every later verdict to low confidence. Without
  it you have fifteen prompts rather than a system.
- `examples` holds the sample exports the worked example runs against.

Start a new Claude Code session afterwards. Skills activate on their own when
the conversation matches their description.

### Other clients

Any client that reads `SKILL.md` files works. Point it at the cloned folder,
keeping `references/` and `scripts/` as siblings of the skill folders.

## How thresholds work

Every number in this pack lives in exactly one place:
`references/thresholds.md`. Skills cite it by key rather than restating the
value, so a threshold cannot drift between skills.

Each entry is tagged:

- `[platform guidance]` - stated by Google in its own documentation or UI.
- `[heuristic]` - a practitioner starting point. Recalibrate against the
  account's own history, and say which one you moved and why.

Skills cite the key, not the value, so you will not see tags inside a skill.
Follow the key into `references/thresholds.md` and the tag is there. If you find
a bare number in a skill's decision rules with no key behind it, that is a bug.
Open an issue.

## What these skills will not do

- They will not log into your Google Ads account.
- They will not change campaigns, budgets, feeds, exclusions or conversion
  actions.
- They will not tell you a per-placement cost as if it were fact, because
  Google reports impressions per placement and nothing else.
- They will not read a trend on a campaign too small to carry one. They will
  tell you the sample is too small instead.

## Licence

MIT. Use them, change them, ship them inside your own process.
