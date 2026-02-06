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

def clamp01(x):
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x

def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)

def compute_case(I_T, disp_vol, KB, KG, FSC_total):
    # BM = I_T / disp_vol
    # KM = KB + BM
    # GM = KM - KG
    # GM_eff = GM - FSC_total
    if not (is_finite(I_T) and is_finite(disp_vol) and is_finite(KB) and is_finite(KG) and is_finite(FSC_total)):
        return None
    if disp_vol <= 0.0 or I_T <= 0.0:
        return None
    BM = I_T / disp_vol
    KM = KB + BM
    GM = KM - KG
    GM_eff = GM - FSC_total
    return BM, KM, GM, GM_eff

def ssb_gate(GM_eff, GM_safe, a_min, s_old, r_safe, s_max):
    # margin = GM_eff / GM_safe
    # a = clamp01(margin)
    # r = max(0, 1 - margin)
    # s = s_old + max(0, r - r_safe)
    margin = GM_eff / max(GM_safe, EPS)
    a = clamp01(margin)
    r = max(0.0, 1.0 - margin)
    s = s_old + max(0.0, r - r_safe)

    if not is_finite(GM_eff):
        return float("nan"), float("nan"), float("nan"), "ABSTAIN"

    if GM_eff <= 0.0:
        return a, r, s, "DENY"

    if (a < a_min) or (s > s_max):
        return a, r, s, "DENY"

    return a, r, s, "ALLOW"

def parse_ladder(s):
    # Example: "0.00,0.04,0.08,0.12,0.16"
    parts = [p.strip() for p in s.split(",") if p.strip() != ""]
    if not parts:
        return []
    out = []
    for p in parts:
        out.append(float(p))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default="ssb_multifsc_out", help="Base output directory.")
    ap.add_argument("--case_id", default="MULTI_FSC_LADDER", help="Case label.")
    ap.add_argument("--tag", default="", help="Optional run tag (e.g., LADDER_DEFAULT).")

    ap.add_argument("--I_T", type=float, default=3.60, help="Waterplane second moment I_T (m^4).")
    ap.add_argument("--disp_vol", type=float, default=8.00, help="Displaced volume ∇ (m^3).")
    ap.add_argument("--KB", type=float, default=0.55, help="KB (m).")
    ap.add_argument("--KG", type=float, default=0.90, help="KG (m).")

    ap.add_argument("--fsc_ladder", default="0.00,0.04,0.08,0.12,0.16,0.20",
                    help="Comma-separated ladder of tank FSC contributions (m).")
    ap.add_argument("--stop_on_deny", action="store_true",
                    help="Stop ladder at first DENY if set.")

    ap.add_argument("--GM_safe", type=float, default=0.15, help="Declared safe GM_eff threshold (m).")
    ap.add_argument("--a_min", type=float, default=0.70, help="Minimum permission.")
    ap.add_argument("--r_safe", type=float, default=0.10, help="Risk tolerance before resistance accumulates.")
    ap.add_argument("--s_max", type=float, default=1.00, help="Maximum allowed resistance.")

    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    run_dir = safe_run_dir(args.out_dir, args.case_id, args.tag)

    ladder = parse_ladder(args.fsc_ladder)
    if not ladder:
        raise SystemExit("fsc_ladder is empty or invalid.")

    out_csv = os.path.join(run_dir, "multifsc_ladder.csv")
    out_txt = os.path.join(run_dir, "multifsc_ladder_report.txt")

    rows = []
    s_acc = 0.0
    FSC_total = 0.0

    first_deny_step = None

    for i, add_fsc in enumerate(ladder):
        FSC_total += add_fsc

        comp = compute_case(args.I_T, args.disp_vol, args.KB, args.KG, FSC_total)
        if comp is None:
            BM = KM = GM = GM_eff = float("nan")
            a = r = float("nan")
            status = "ABSTAIN"
            classical = "UNSTABLE"
        else:
            BM, KM, GM, GM_eff = comp
            classical = "STABLE" if (is_finite(GM_eff) and GM_eff > 0.0) else "UNSTABLE"
            a, r, s_acc, status = ssb_gate(GM_eff, args.GM_safe, args.a_min, s_acc, args.r_safe, args.s_max)

        rows.append([
            i, args.case_id,
            add_fsc, FSC_total,
            args.I_T, args.disp_vol, args.KB, args.KG,
            BM, KM, GM, GM_eff,
            classical,
            args.GM_safe,
            a, r, s_acc, status
        ])

        if first_deny_step is None and status == "DENY":
            first_deny_step = (i, FSC_total, GM_eff, a, r, s_acc)

        if args.stop_on_deny and status == "DENY":
            break

    header = [
        "i","case_id",
        "FSC_add","FSC_total",
        "I_T","disp_vol","KB","KG",
        "BM","KM","GM","GM_eff",
        "classical_GM_sign",
        "GM_safe",
        "a","r","s","SSB_status"
    ]
    write_csv(out_csv, header, rows)

    lines = []
    lines.append("SSB MULTI-TANK FSC LADDER — DETERMINISTIC REPORT")
    lines.append("")
    lines.append(f"case_id: {args.case_id}")
    lines.append(f"I_T (m^4): {args.I_T}")
    lines.append(f"disp_vol ∇ (m^3): {args.disp_vol}")
    lines.append(f"KB (m): {args.KB}")
    lines.append(f"KG (m): {args.KG}")
    lines.append("")
    lines.append(f"FSC ladder contributions (m): {args.fsc_ladder}")
    lines.append("Rule: FSC_total = sum(FSC_i)")
    lines.append("")
    lines.append(f"SSB thresholds: GM_safe={args.GM_safe}  a_min={args.a_min}  r_safe={args.r_safe}  s_max={args.s_max}")
    lines.append("")
    if first_deny_step is None:
        lines.append("First DENY: (not reached)")
    else:
        i, fscT, gme, a, r, s = first_deny_step
        lines.append(f"First DENY at step i={i} with FSC_total={fscT:.6f}  GM_eff={gme:.6f}  a={a:.6f}  r={r:.6f}  s={s:.6f}")
    lines.append("")
    lines.append("Outputs:")
    lines.append(f" - {out_csv}")
    lines.append(f" - {out_txt}")

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
