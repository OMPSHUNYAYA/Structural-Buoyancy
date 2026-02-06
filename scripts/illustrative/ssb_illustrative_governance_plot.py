#!/usr/bin/env python3
"""
SSB Illustrative Governance Plot
--------------------------------
Illustrative only — no quantitative inference permitted.

This script visualizes governance state transitions
(ALLOW / RESTRICTED / DENY) from an EXISTING Phase III CSV.

It does NOT:
- compute GM, a, r, or s
- change thresholds
- predict failure
- infer probabilities
- modify SSB logic

This script is strictly explanatory.
"""

import csv
import sys
import os
import matplotlib.pyplot as plt

# --- Mandatory label (do not remove) ---
DISCLAIMER = "Illustrative only — no quantitative inference permitted."

# --- Expected CSV name ---
EXPECTED_CSV = "phase3_classification.csv"

# --- Map envelopes to symbolic levels (non-quantitative) ---
LEVEL_MAP = {
    "ALLOW_NORMAL": 2,
    "ALLOW_RESTRICTED_MONITOR": 1,
    "DENY_FINAL": 0,
    "ABSTAIN_HUMAN_REVIEW": 0
}

LABEL_MAP = {
    2: "ALLOW",
    1: "RESTRICTED",
    0: "DENY / ABSTAIN"
}

def resolve_csv_path(path):
    """
    Accepts either:
    - direct path to phase3_classification.csv
    - directory containing phase3_classification.csv
    """
    if os.path.isfile(path):
        return path

    if os.path.isdir(path):
        candidate = os.path.join(path, EXPECTED_CSV)
        if os.path.isfile(candidate):
            return candidate

    return None

def main(input_path):
    csv_path = resolve_csv_path(input_path)

    if csv_path is None:
        print("ERROR: Could not locate Phase III classification CSV.")
        print()
        print("Expected one of the following:")
        print("  1) Direct path to phase3_classification.csv")
        print("  2) Directory containing phase3_classification.csv")
        print()
        print("Provided path:")
        print(f"  {input_path}")
        sys.exit(1)

    steps = []
    levels = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "PHASE3_envelope" not in reader.fieldnames:
            print("ERROR: CSV does not contain required column 'PHASE3_envelope'")
            print("Found columns:", reader.fieldnames)
            sys.exit(1)

        for i, row in enumerate(reader):
            env = (row.get("PHASE3_envelope") or "").strip()
            if env in LEVEL_MAP:
                steps.append(i)
                levels.append(LEVEL_MAP[env])

    if not steps:
        print("ERROR: No valid governance states found in CSV.")
        sys.exit(1)

    # --- Plot ---
    plt.figure(figsize=(10, 4))
    plt.step(steps, levels, where="post", linewidth=2)

    plt.yticks([0, 1, 2], [LABEL_MAP[0], LABEL_MAP[1], LABEL_MAP[2]])
    plt.xlabel("Evaluation Step (Illustrative Index)")
    plt.ylabel("Governance State")
    plt.title("SSB Governance State Progression (Illustrative)")

    plt.grid(True, axis="y", linestyle="--", alpha=0.6)

    # Mandatory disclaimer on plot
    plt.figtext(0.5, -0.18, DISCLAIMER, ha="center", fontsize=9, style="italic")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python ssb_illustrative_governance_plot.py <csv_or_directory>")
        sys.exit(1)

    main(sys.argv[1])
