#!/usr/bin/env python3
"""
SSB Figure D.2 — Illustrative Separation of Physical Stability and Structural Trust
-------------------------------------------------------------------------------
Illustrative only — no quantitative inference permitted.

This script visualizes:
- GM_eff(t)  (classical effective stability signal)
- s(t)       (structural resistance accumulation)

and overlays vertical markers at the FIRST occurrence of:
- ALLOW_RESTRICTED_MONITOR
- DENY_FINAL

It does NOT:
- compute GM, a, r, or s
- change thresholds
- predict failure
- infer probabilities
- modify SSB logic

Input:
- A direct path to phase3_classification.csv, OR
- A directory containing phase3_classification.csv
"""

import csv
import os
import sys
import matplotlib.pyplot as plt

DISCLAIMER = "Illustrative only — no quantitative inference permitted."
EXPECTED_CSV = "phase3_classification.csv"

ENV_COL_CANDIDATES = ["PHASE3_envelope", "phase3_envelope", "envelope_class", "phase3_status", "phase2_status"]
GM_COL_CANDIDATES  = ["GM_eff", "GM_EFF", "gm_eff"]
S_COL_CANDIDATES   = ["s", "S", "s_t", "S_t", "structural_resistance"]

RESTRICT_STATE = "ALLOW_RESTRICTED_MONITOR"
DENY_STATE     = "DENY_FINAL"


def resolve_csv_path(path: str) -> str | None:
    if os.path.isfile(path):
        return path
    if os.path.isdir(path):
        candidate = os.path.join(path, EXPECTED_CSV)
        if os.path.isfile(candidate):
            return candidate
    return None


def pick_column(fieldnames, candidates):
    for c in candidates:
        if c in fieldnames:
            return c
    return None


def parse_float(x):
    try:
        if x is None:
            return None
        x = str(x).strip()
        if x == "":
            return None
        return float(x)
    except Exception:
        return None


def main(input_path: str):
    csv_path = resolve_csv_path(input_path)
    if csv_path is None:
        print("ERROR: Could not locate Phase III classification CSV.")
        print("Expected one of:")
        print("  1) Direct path to phase3_classification.csv")
        print("  2) Directory containing phase3_classification.csv")
        print("Provided:", input_path)
        sys.exit(1)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print("ERROR: CSV has no header / fieldnames.")
            sys.exit(1)

        env_col = pick_column(reader.fieldnames, ENV_COL_CANDIDATES)
        gm_col  = pick_column(reader.fieldnames, GM_COL_CANDIDATES)
        s_col   = pick_column(reader.fieldnames, S_COL_CANDIDATES)

        missing = []
        if env_col is None:
            missing.append("envelope column (one of " + ", ".join(ENV_COL_CANDIDATES) + ")")
        if gm_col is None:
            missing.append("GM column (one of " + ", ".join(GM_COL_CANDIDATES) + ")")
        if s_col is None:
            missing.append("s column (one of " + ", ".join(S_COL_CANDIDATES) + ")")

        if missing:
            print("ERROR: Missing required column(s):")
            for m in missing:
                print("  -", m)
            print("\nFound columns:")
            for name in reader.fieldnames:
                print("  -", name)
            sys.exit(1)

        steps = []
        gm_vals = []
        s_vals = []
        env_vals = []

        for i, row in enumerate(reader):
            gm = parse_float(row.get(gm_col))
            ss = parse_float(row.get(s_col))
            env = (row.get(env_col) or "").strip()

            # Require GM_eff and s to be present to plot this step
            if gm is None or ss is None:
                continue

            steps.append(i)
            gm_vals.append(gm)
            s_vals.append(ss)
            env_vals.append(env)

    if not steps:
        print("ERROR: No usable rows found (need numeric GM_eff and s).")
        sys.exit(1)

    # Find first transition indices (within plotted steps)
    first_restrict_step = None
    first_deny_step = None

    for i, env in enumerate(env_vals):
        if first_restrict_step is None and env == RESTRICT_STATE:
            first_restrict_step = steps[i]
        if first_deny_step is None and env == DENY_STATE:
            first_deny_step = steps[i]
        if first_restrict_step is not None and first_deny_step is not None:
            break

    # Plot
    plt.figure(figsize=(11, 4.5))
    plt.plot(steps, gm_vals, linewidth=2, label="GM_eff(t) (classical stability signal)")
    plt.plot(steps, s_vals, linewidth=2, label="s(t) (structural resistance accumulation)")

    # Vertical markers
    if first_restrict_step is not None:
        plt.axvline(first_restrict_step, linewidth=1.5, linestyle="--", label="First RESTRICTED")
    if first_deny_step is not None:
        plt.axvline(first_deny_step, linewidth=1.5, linestyle="--", label="First DENY")

    plt.xlabel("Evaluation Step (illustrative index)")
    plt.ylabel("Value (illustrative plot of existing run outputs)")
    plt.title("Figure D.2 — Physical Stability vs Structural Trust (Illustrative)")

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="best")

    # Mandatory disclaimer on plot
    plt.figtext(0.5, 0.01, DISCLAIMER, ha="center", fontsize=9, style="italic")

    plt.tight_layout()
    plt.show()

    # Console summary (helpful for docs)
    print("OK: Figure D.2 plot displayed.")
    print("CSV:", csv_path)
    print("Columns used:", {"envelope": env_col, "GM_eff": gm_col, "s": s_col})
    print("First RESTRICTED step:", first_restrict_step)
    print("First DENY step:", first_deny_step)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python ssb_illustrative_physics_vs_trust_plot.py <csv_or_directory>")
        sys.exit(1)

    main(sys.argv[1])
