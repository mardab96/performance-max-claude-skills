#!/usr/bin/env python3
"""Decide whether a post-change movement is larger than the pre-change noise.

Implements the arithmetic for the skill `post-change-readout-pmax`, step 2:
establish the baseline with its own variance before attributing anything. The
skill owns the decision rules; this script owns the counting.

The question it answers is narrow and deliberately so: did the metric move
further than it routinely moved before anyone touched anything? A "no" here
ends the readout, because nothing has been detected.

Usage:
    python3 variance_check.py series.csv --change-date 2026-07-22 --metric cpa

Input: a CSV with a date column and one or more metric columns, one row per
day or per week. Column names are matched case-insensitively.

Output: JSON on stdout.

This script does not attribute causes, check seasonality or look for
confounders. Those are judgement steps and they stay in the skill.
"""

import argparse
import csv
import json
import re
import statistics
import sys
from datetime import datetime

DATE_KEYS = ("date", "day", "week", "week starting")


def _num(raw):
    if raw is None:
        return None
    s = str(raw).strip()
    if s in ("", "--", "-", "N/A"):
        return None
    s = re.sub(r"[^\d,.\-]", "", s)
    if "," in s and "." in s:
        s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".") if len(s.split(",")[-1]) <= 2 else s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date(s):
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d.%m.%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _pick(fieldnames, candidates):
    lowered = {f.lower().strip(): f for f in fieldnames if f}
    for want in candidates:
        for low, original in lowered.items():
            if low == want or low.startswith(want):
                return original
    return None


def load(path, metric):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit("empty export: no data rows found, so no baseline could be built")

    fields = rows[0].keys()
    date_col = _pick(fields, DATE_KEYS)
    metric_col = _pick(fields, (metric.lower(),))

    if not date_col:
        raise SystemExit("no date column found. Columns present: %s" % ", ".join(fields))
    if not metric_col:
        raise SystemExit(
            "no column matching '%s'. Columns present: %s" % (metric, ", ".join(fields))
        )

    series = []
    for r in rows:
        d = _parse_date(r.get(date_col))
        v = _num(r.get(metric_col))
        if d and v is not None:
            series.append((d, v))
    series.sort(key=lambda t: t[0])
    return series, metric_col


BASELINE_PERIODS = 8  # fixed by post-change-readout-pmax; see note in main()


def analyse(series, change_date, baseline=BASELINE_PERIODS):
    before_all = [v for d, v in series if d < change_date]
    after = [v for d, v in series if d >= change_date]

    # The detection band is built from the spread of the pre-change periods, so
    # its width depends on how much history was pasted in. Two people pasting 8
    # and 12 weeks of the same account get opposite answers about whether
    # anything happened. The skill fixes the window at 8; the script enforces
    # it rather than trusting the caller, and reports what it discarded.
    discarded = max(0, len(before_all) - baseline)
    before = before_all[-baseline:]

    if len(before) < 3:
        raise SystemExit(
            "only %d period(s) before the change date: too few to establish a baseline. "
            "The honest answer is 'not readable', not a number." % len(before)
        )
    if not after:
        raise SystemExit("no periods on or after the change date")

    pre_mean = statistics.mean(before)
    pre_sd = statistics.pstdev(before) if len(before) > 1 else 0.0
    post_mean = statistics.mean(after)
    delta = post_mean - pre_mean

    # Movement counts as detected only if it clears the pre-period band.
    band_low, band_high = min(before), max(before)
    detected = post_mean < band_low or post_mean > band_high

    return {
        "baseline_periods_used": len(before),
        "baseline_periods_discarded": discarded,
        "baseline_note": (
            "Baseline fixed at %d periods. %d older period(s) were discarded so "
            "the detection band cannot widen with however much history was "
            "pasted in." % (baseline, discarded)
            if discarded
            else "Baseline fixed at %d periods; the export supplied %d."
            % (baseline, len(before))
        ),
        "periods_before": len(before),
        "periods_after": len(after),
        "pre_mean": round(pre_mean, 2),
        "pre_min": round(band_low, 2),
        "pre_max": round(band_high, 2),
        "pre_stdev": round(pre_sd, 2),
        "post_mean": round(post_mean, 2),
        "delta": round(delta, 2),
        "delta_pct": round(100 * delta / pre_mean, 1) if pre_mean else None,
        "detected": detected,
        "verdict": (
            "movement is outside the pre-change range, so something happened"
            if detected
            else "movement sits inside the pre-change range, so nothing has been detected"
        ),
        "note": (
            "Detection is not attribution. Seasonality, promotions and learning "
            "resets are checked in the skill, not here."
        ),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv_path")
    p.add_argument("--change-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--metric", default="cpa", help="column name to test, e.g. cpa, roas, conversions")
    args = p.parse_args()

    change = _parse_date(args.change_date)
    if not change:
        raise SystemExit("could not parse --change-date, expected YYYY-MM-DD")

    series, used_col = load(args.csv_path, args.metric)
    result = analyse(series, change)
    if result["baseline_periods_discarded"]:
        print(
            "NOTE: %d pre-change period(s) discarded. The baseline is fixed at %d "
            "so the detection band cannot widen with however much history was "
            "pasted in." % (result["baseline_periods_discarded"], BASELINE_PERIODS),
            file=sys.stderr,
        )
    elif result["baseline_periods_used"] < BASELINE_PERIODS:
        print(
            "WARNING: only %d pre-change period(s) supplied against a required %d. "
            "The detection band is narrower than intended and this run is more "
            "likely to report a movement that is not there."
            % (result["baseline_periods_used"], BASELINE_PERIODS),
            file=sys.stderr,
        )
    result["metric_column"] = used_col
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
