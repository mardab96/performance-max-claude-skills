#!/usr/bin/env python3
"""Rank products by spend and flag the zero-conversion tail.

Implements the arithmetic for the skill `product-spend-concentration-pmax`.
The skill owns the decision rules; this script owns the counting, so that two
runs on the same export cannot disagree about the numbers.

Thresholds referenced (defined in ../references/thresholds.md):
  listing_group.spend_concentration  top products absorbing 70%+ of spend
  zero-tail flag                     spend above ~3x target CPA, 0 conversions

Usage:
    python3 spend_concentration.py products.csv --target-cpa 60
    python3 spend_concentration.py products.csv --target-roas 400

Input: a CSV export from Google Ads with, at minimum, a product identifier
column and columns for cost and conversions. Column names are matched
case-insensitively and tolerate the usual Google Ads export variants
("Cost", "Spend", "Conversions", "Conv.", "Conv. value").

Output: JSON on stdout. Nothing is written back to the input file.
"""

import argparse
import csv
import json
import re
import sys

ID_KEYS = ("product id", "item id", "offer id", "product title", "title", "product")
COST_KEYS = ("cost", "spend", "amount spent")
CONV_KEYS = ("conversions", "conv.", "conv", "all conv.")
VALUE_KEYS = ("conv. value", "conversion value", "total conv. value", "revenue")


def _num(raw):
    """Parse a Google Ads export cell into a float. Blank and '--' mean zero."""
    if raw is None:
        return 0.0
    s = str(raw).strip()
    if s in ("", "--", "-", "N/A"):
        return 0.0
    s = re.sub(r"[^\d,.\-]", "", s)
    # Google exports use either 1,234.56 or 1.234,56 depending on locale.
    if "," in s and "." in s:
        s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".") if len(s.split(",")[-1]) <= 2 else s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def _pick(fieldnames, candidates):
    lowered = {f.lower().strip(): f for f in fieldnames if f}
    for want in candidates:
        for low, original in lowered.items():
            if low == want or low.startswith(want):
                return original
    return None


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(fh, dialect=dialect))

    if not rows:
        raise SystemExit("empty export: no data rows found, so nothing was ranked")

    fields = rows[0].keys()
    id_col = _pick(fields, ID_KEYS)
    cost_col = _pick(fields, COST_KEYS)
    conv_col = _pick(fields, CONV_KEYS)
    value_col = _pick(fields, VALUE_KEYS)

    missing = [n for n, c in (("product id", id_col), ("cost", cost_col), ("conversions", conv_col)) if not c]
    if missing:
        raise SystemExit(
            "could not find required column(s): %s. Columns present: %s"
            % (", ".join(missing), ", ".join(fields))
        )

    out = []
    for r in rows:
        pid = (r.get(id_col) or "").strip()
        if not pid or pid.lower().startswith("total"):
            continue
        out.append(
            {
                "product": pid,
                "cost": _num(r.get(cost_col)),
                "conversions": _num(r.get(conv_col)),
                "value": _num(r.get(value_col)) if value_col else None,
            }
        )
    return out


def analyse(rows, target_cpa=None, target_roas=None):
    rows = sorted(rows, key=lambda r: r["cost"], reverse=True)
    total_cost = sum(r["cost"] for r in rows)
    total_conv = sum(r["conversions"] for r in rows)

    if total_cost <= 0:
        raise SystemExit("total cost is zero: the export has no spend to rank")

    cumulative = 0.0
    top_block = []
    for r in rows:
        if cumulative / total_cost >= 0.70:
            break
        cumulative += r["cost"]
        top_block.append(r)

    zero_tail = [r for r in rows if r["conversions"] == 0 and r["cost"] > 0]
    if target_cpa:
        flagged_tail = [r for r in zero_tail if r["cost"] >= 3 * target_cpa]
    else:
        flagged_tail = []

    for r in rows:
        r["cpa"] = round(r["cost"] / r["conversions"], 2) if r["conversions"] else None
        if r["value"] is not None and r["cost"] > 0:
            r["roas_pct"] = round(100 * r["value"] / r["cost"], 1)
        else:
            r["roas_pct"] = None

    return {
        "products": len(rows),
        "total_cost": round(total_cost, 2),
        "total_conversions": round(total_conv, 2),
        "blended_cpa": round(total_cost / total_conv, 2) if total_conv else None,
        "top_block_size": len(top_block),
        "top_block_share_pct": round(100 * cumulative / total_cost, 1),
        # listing_group.spend_concentration: the top 20% of products by cost
        # taking 70%+ of spend. Both halves are required. A larger slice of the
        # catalogue reaching 70% is ordinary retail shape, not concentration.
        "concentration_flag": (len(top_block) / len(rows) <= 0.20) if rows else False,
        "concentration_basis": (
            "top %d of %d products (%.1f%% of catalogue) hold %.1f%% of spend; "
            "flag requires the catalogue share to be 20%% or less"
            % (
                len(top_block),
                len(rows),
                100 * len(top_block) / len(rows),
                100 * cumulative / total_cost,
            )
        ),
        "zero_conversion_products": len(zero_tail),
        "zero_conversion_cost": round(sum(r["cost"] for r in zero_tail), 2),
        "flagged_tail_products": len(flagged_tail),
        "flagged_tail_cost": round(sum(r["cost"] for r in flagged_tail), 2),
        "flagged_tail_basis": "cost >= 3x target CPA of %s" % target_cpa if target_cpa else "not computed: no --target-cpa given",
        "target_roas_pct": target_roas,
        "top_products": rows[:20],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv_path")
    p.add_argument("--target-cpa", type=float, default=None)
    p.add_argument("--target-roas", type=float, default=None, help="as a percentage, e.g. 400")
    args = p.parse_args()

    if args.target_cpa is None and args.target_roas is None:
        print(
            "note: no target given, so the zero-conversion tail cannot be flagged. "
            "Pass --target-cpa or --target-roas.",
            file=sys.stderr,
        )

    result = analyse(load(args.csv_path), args.target_cpa, args.target_roas)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
