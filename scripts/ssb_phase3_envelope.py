#!/usr/bin/env python3
import argparse
import csv
import math
import os
import datetime

EPS = 1e-12

def safe_run_dir(base_out_dir, case_id, tag):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    case = str(case_id).strip().replace(" ", "_")
    tg = str(tag).strip().replace(" ", "_") if str(tag).strip() else "RUN"
    run_dir = os.path.join(base_out_dir, f"{ts}__{case}__{tg}")
    os.makedirs(run_dir, exist_ok=False)
    return run_dir

def is_finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)

def parse_float(s):
    try:
        x = float(s)
        return x
    except Exception:
        return float("nan")

def envelope_label(ssb_status, a, s, a_min, s_max, s_warn_frac):
    # Phase III envelope classification:
    # - DENY => DENY_FINAL
    # - ABSTAIN => ABSTAIN_HUMAN_REVIEW
    # - ALLOW with s near s_max => ALLOW_RESTRICTED_MONITOR
    # - ALLOW otherwise => ALLOW_NORMAL
    if ssb_status == "DENY":
        return "DENY_FINAL"
    if ssb_status == "ABSTAIN":
        return "ABSTAIN_HUMAN_REVIEW"
    if ssb_status != "ALLOW":
        return "ABSTAIN_HUMAN_REVIEW"

    # If a is not finite, treat as abstain
    if not is_finite(a) or not is_finite(s):
        return "ABSTAIN_HUMAN_REVIEW"

    # If near denial by resistance, mark restricted
    s_warn = s_warn_frac * s_max
    if s >= s_warn:
        return "ALLOW_RESTRICTED_MONITOR"

    # If a barely above a_min, also mark restricted (optional conservative rule)
    # (This does NOT change DENY rule; it only classifies ALLOW into restricted.)
    if a <= a_min + 0.05:
        return "ALLOW_RESTRICTED_MONITOR"

    return "ALLOW_NORMAL"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_csv", required=True, help="Input CSV from a Phase-II run (disp_sweep/multifsc/cyclic).")
    ap.add_argument("--out_dir", default="ssb_phase3_out", help="Output directory.")
    ap.add_argument("--case_id", default="PHASE3", help="Case label.")
    ap.add_argument("--tag", default="PHASE3_ENVELOPE", help="Run tag.")

    # These must match the run's declared thresholds (from the report)
    ap.add_argument("--a_min", type=float, default=0.70, help="Minimum permission threshold used in Phase-II.")
    ap.add_argument("--s_max", type=float, default=1.00, help="Max resistance used in Phase-II.")
    ap.add_argument("--s_warn_frac", type=float, default=0.80, help="Restricted envelope starts at this fraction of s_max.")

    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    run_dir = safe_run_dir(args.out_dir, args.case_id, args.tag)

    out_csv = os.path.join(run_dir, "phase3_classification.csv")
    out_txt = os.path.join(run_dir, "phase3_summary.txt")

    with open(args.in_csv, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        fieldnames = list(r.fieldnames) if r.fieldnames else []
        # Expected common columns from your scripts:
        # "a","s","SSB_status" (disp), or "a","s","SSB_status" (multi), or "a","s","SSB_status" (cyclic)
        # If names differ, user can map by editing header in source or script.

        # Add Phase III columns
        extra_cols = ["PHASE3_envelope"]
        for c in extra_cols:
            if c not in fieldnames:
                fieldnames.append(c)

        rows = []
        counts = {"ALLOW_NORMAL":0, "ALLOW_RESTRICTED_MONITOR":0, "DENY_FINAL":0, "ABSTAIN_HUMAN_REVIEW":0}

        first_restricted = None
        first_deny = None
        first_abstain = None

        idx = 0
        for row in r:
            a = parse_float(row.get("a", "nan"))
            s = parse_float(row.get("s", "nan"))
            status = (row.get("SSB_status", "") or "").strip().upper()

            env = envelope_label(status, a, s, args.a_min, args.s_max, args.s_warn_frac)
            row["PHASE3_envelope"] = env
            rows.append(row)

            counts[env] = counts.get(env, 0) + 1

            if first_restricted is None and env == "ALLOW_RESTRICTED_MONITOR":
                first_restricted = idx
            if first_deny is None and env == "DENY_FINAL":
                first_deny = idx
            if first_abstain is None and env == "ABSTAIN_HUMAN_REVIEW":
                first_abstain = idx

            idx += 1

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    def fmt_first(label, v):
        return f"{label}: (not reached)" if v is None else f"{label}: row_index={v}"

    lines = []
    lines.append("SSB PHASE III — ENVELOPE CLASSIFICATION REPORT")
    lines.append("")
    lines.append(f"input_csv: {args.in_csv}")
    lines.append(f"a_min: {args.a_min}")
    lines.append(f"s_max: {args.s_max}")
    lines.append(f"s_warn_frac: {args.s_warn_frac}")
    lines.append("")
    lines.append("Counts:")
    for k in ["ALLOW_NORMAL","ALLOW_RESTRICTED_MONITOR","DENY_FINAL","ABSTAIN_HUMAN_REVIEW"]:
        lines.append(f" - {k}: {counts.get(k,0)}")
    lines.append("")
    lines.append(fmt_first("First Restricted", first_restricted))
    lines.append(fmt_first("First Deny", first_deny))
    lines.append(fmt_first("First Abstain", first_abstain))
    lines.append("")
    lines.append("Outputs:")
    lines.append(f" - {out_csv}")
    lines.append(f" - {out_txt}")

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
