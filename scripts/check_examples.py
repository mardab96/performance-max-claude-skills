#!/usr/bin/env python3
"""Re-derive every worked example's arithmetic from references/thresholds.md.

Why this exists. Across three review rounds the same defect recurred: threshold
values were edited with discipline and worked examples were edited by hand,
so an example that was correct against the old value silently became wrong
against the new one. Key reconciliation was automatic and caught every drift;
the arithmetic had no equivalent and drifted every round.

This is that equivalent. It hard-codes the inputs each example states and
re-derives the conclusions from the current thresholds, so changing a threshold
makes the affected examples fail here rather than in front of a reader.

Run it after ANY change to references/thresholds.md, and before shipping.

    python3 scripts/check_examples.py

Exit 0 = every example agrees with the thresholds. Exit 1 = at least one does
not, with the file, the claim and the correct figure.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
THRESHOLDS = ROOT / "references" / "thresholds.md"


def threshold_value(key, pattern, cast=float):
    """Pull a live value out of thresholds.md so this script cannot drift from it."""
    text = THRESHOLDS.read_text()
    # The key must be the row's SUBJECT, not merely mentioned in it. Several
    # entries cite other keys in their notes, so a substring match lands on the
    # wrong row and reads the wrong number, which is the same class of defect
    # this script exists to catch.
    row = next(
        (l for l in text.splitlines() if l.lstrip().startswith("| `%s`" % key)), None
    )
    if row is None:
        fail("threshold key %s not found in thresholds.md" % key)
        return None
    m = re.search(pattern, row)
    if not m:
        fail("could not read a value for %s out of its row" % key)
        return None
    return cast(m.group(1))


FAILURES = []


def fail(msg):
    FAILURES.append(msg)


def check(name, condition, detail):
    if not condition:
        fail("%s: %s" % (name, detail))


def words_between(path, start, end):
    t = (ROOT / path).read_text()
    return len(t[t.index(start):t.index(end)].split())


def main():
    # --- live threshold values -------------------------------------------
    group_floor = threshold_value("asset_group.volume_floor", r"\*\*(\d+) conversions")
    campaign_floor = threshold_value("conversion.volume_floor", r"\*\*(\d+) primary")
    judgement_weeks = threshold_value("learning.judgement_window", r"\*\*(\d+) weeks\*\*")
    budget_step = threshold_value("budget.step", r"\*\*(\d+)%\*\*")
    if None in (group_floor, campaign_floor, judgement_weeks, budget_step):
        report()
        return

    # --- asset-group-structure: 46 conversions, 5 groups ------------------
    ceiling = 46 / group_floor
    supported = int(ceiling)  # round DOWN: the flag fires on "more than the ceiling"
    txt = (ROOT / "asset-group-structure-audit-pmax" / "SKILL.md").read_text()
    m = re.search(r"should be running (\w+) groups", txt)
    words = {"two": 2, "three": 3, "four": 4, "five": 5}
    check(
        "asset-group-structure example",
        m and words.get(m.group(1)) == supported,
        "says %s groups; 46/%g = %.2f so the supported number is %d"
        % (m.group(1) if m else "?", group_floor, ceiling, supported),
    )
    check(
        "asset-group-structure example",
        ("%.1f" % ceiling) in txt,
        "should state the ceiling %.1f explicitly" % ceiling,
    )

    # --- scaling: 90 conversions/month, does the 4-week recalibration apply?
    scaling = (ROOT / "scaling-learning-phase-guardrail-pmax" / "SKILL.md").read_text()
    campaign_conversions = 90
    recalibrates = campaign_conversions >= 3 * campaign_floor
    claims_no_recalibration = "does not" in scaling.split("by 3x")[1][:60] if "by 3x" in scaling else False
    check(
        "scaling example",
        recalibrates != claims_no_recalibration,
        "campaign has %d conversions and 3x the floor is %g, so the "
        "recalibration %s apply; the example says the opposite"
        % (campaign_conversions, 3 * campaign_floor, "does" if recalibrates else "does not"),
    )
    # The stated date must match the window the recalibration actually gives.
    weeks = 4 if recalibrates else judgement_weeks
    expected_date = {4: "16 August", 6: "30 August"}[int(weeks)]
    check(
        "scaling example",
        expected_date in scaling,
        "window is %d weeks from 19 July, so the date is %s"
        % (int(weeks), expected_date),
    )
    # Headline must not contradict the body.
    check(
        "scaling example",
        not ("feed it" in scaling and "the answer is not 'raise it'" in scaling),
        "headline says feed it while the body refuses to raise budget",
    )

    # --- listing-group: 140 conversions -----------------------------------
    lg = (ROOT / "listing-group-segmentation-pmax" / "SKILL.md").read_text()
    check(
        "listing-group example",
        "%.1f" % (140 / campaign_floor) in lg or "%.2f" % (140 / campaign_floor) in lg,
        "campaign ceiling should be %.2f (140/%g)" % (140 / campaign_floor, campaign_floor),
    )
    check(
        "listing-group example",
        "%.1f" % (140 / group_floor) in lg,
        "asset group ceiling should be %.1f (140/%g)" % (140 / group_floor, group_floor),
    )

    # --- product-spend-concentration: the stated totals must reconcile -----
    top, tail, weak = 17040, 5290, 2900
    total = 24000
    check(
        "product-spend-concentration example",
        tail <= total - top,
        "tail of %d cannot fit in the %d left after a top block of %d"
        % (tail, total - top, top),
    )
    psc = (ROOT / "product-spend-concentration-pmax" / "SKILL.md").read_text()
    check(
        "product-spend-concentration example",
        str(tail + weak) in psc.replace(",", ""),
        "headline should total %d (%d tail + %d weak)" % (tail + weak, tail, weak),
    )

    # --- margin arithmetic wherever breakeven is quoted --------------------
    for rel in ("product-spend-concentration-pmax/SKILL.md",
                "examples/worked-example-full-audit.md"):
        t = (ROOT / rel).read_text()
        # Every "at X% margin, breakeven is Y%" pair in the file, in either
        # phrasing, because the flagship example quotes two margins at once.
        pairs = re.findall(
            r"(\d+)% (?:gross )?margin,?\s*breakeven is (?:a ROAS of )?(\d+)%", t
        )
        if "breakeven" in t and not pairs:
            fail("%s: quotes a breakeven with no margin attached to check it against" % rel)
        for margin, claimed in pairs:
            correct = round(100 / (int(margin) / 100))
            check(
                "%s margin arithmetic" % rel,
                abs(int(claimed) - correct) <= 1,
                "says breakeven is %s%% at %s%% margin; it is %d%%"
                % (claimed, margin, correct),
            )

    # --- the client readout's stated word count must be true --------------
    actual = words_between(
        "examples/worked-example-full-audit.md",
        '"In July the campaign spent',
        "Word count:",
    )
    full = (ROOT / "examples" / "worked-example-full-audit.md").read_text()
    m = re.search(r"Word count: (\d+)", full)
    check(
        "worked-example word count",
        m and abs(int(m.group(1)) - actual) <= 3,
        "states %s words; the readout is %d" % (m.group(1) if m else "?", actual),
    )

    report()


def report():
    if FAILURES:
        print("EXAMPLES DISAGREE WITH THRESHOLDS:\n")
        for f in FAILURES:
            print("  FAIL  %s" % f)
        print("\n%d failure(s)." % len(FAILURES))
        sys.exit(1)
    print("All worked examples agree with references/thresholds.md.")


if __name__ == "__main__":
    main()
