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

def compute_case(I_T, disp_vol, KB, KG, FSC):
    # BM = I_T / disp_vol
    # KM = KB + BM
    # GM = KM - KG
    # GM_eff = GM - FSC
    if not (is_finite(I_T) and is_finite(disp_vol) and is_finite(KB) and is_finite(KG) and is_finite(FSC)):
        return None
    if disp_vol <= 0.0 or I_T <= 0.0:
        return None
    BM = I_T / disp_vol
    KM = KB + BM
    GM = KM - KG
    GM_eff = GM - FSC
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default="ssb_disp_sweep_out", help="Base output directory.")
    ap.add_argument("--case_id", default="DISP_SWEEP", help="Case label.")
    ap.add_argument("--tag", default="", help="Optional run tag (e.g., KG0p95_FSC0p05).")

    ap.add_argument("--I_T", type=float, default=3.60, help="Waterplane second moment I_T (m^4).")
    ap.add_argument("--KB", type=float, default=0.55, help="KB (m).")
    ap.add_argument("--KG", type=float, default=0.90, help="KG (m).")
    ap.add_argument("--FSC", type=float, default=0.00, help="Free surface correction FSC (m).")

    ap.add_argument("--disp_start", type=float, default=5.0, help="Start displaced volume ∇ (m^3).")
    ap.add_argument("--disp_end", type=float, default=12.0, help="End displaced volume ∇ (m^3).")
    ap.add_argument("--disp_step", type=float, default=0.25, help="Step for ∇ (m^3).")

    ap.add_argument("--GM_safe", type=float, default=0.15, help="Declared safe GM_eff threshold (m).")
    ap.add_argument("--a_min", type=float, default=0.70, help="Minimum permission.")
    ap.add_argument("--r_safe", type=float, default=0.10, help="Risk tolerance before resistance accumulates.")
    ap.add_argument("--s_max", type=float, default=1.00, help="Maximum allowed resistance.")

    args = ap.parse_args()

    # Base directory exists; each run gets its own unique subfolder
    os.makedirs(args.out_dir, exist_ok=True)
    run_dir = safe_run_dir(args.out_dir, args.case_id, args.tag)

    out_csv = os.path.join(run_dir, "disp_sweep.csv")
    out_txt = os.path.join(run_dir, "disp_sweep_report.txt")

    rows = []
    s = 0.0
    n_allow = n_deny = n_abstain = 0

    first_below_safe = None
    first_ssb_deny = None
    first_classical_unstable = None

    j = 0
    disp_vol = args.disp_start
    while disp_vol <= args.disp_end + 0.5 * args.disp_step:
        comp = compute_case(args.I_T, disp_vol, args.KB, args.KG, args.FSC)
        if comp is None:
            BM = KM = GM = GM_eff = float("nan")
            a = r = float("nan")
            status = "ABSTAIN"
            classical = "UNSTABLE"
            n_abstain += 1
        else:
            BM, KM, GM, GM_eff = comp
            classical = "STABLE" if (is_finite(GM_eff) and GM_eff > 0.0) else "UNSTABLE"

            a, r, s, status = ssb_gate(GM_eff, args.GM_safe, args.a_min, s, args.r_safe, args.s_max)
            if status == "ALLOW":
                n_allow += 1
            elif status == "DENY":
                n_deny += 1
            else:
                n_abstain += 1

            if first_below_safe is None and is_finite(GM_eff) and GM_eff < args.GM_safe:
                first_below_safe = (disp_vol, GM_eff)
            if first_ssb_deny is None and status == "DENY":
                first_ssb_deny = (disp_vol, GM_eff)
            if first_classical_unstable is None and classical == "UNSTABLE":
                first_classical_unstable = (disp_vol, GM_eff)

        rows.append([
            j, args.case_id, args.I_T, disp_vol, args.KB, args.KG, args.FSC,
            BM, KM, GM, GM_eff,
            classical,
            args.GM_safe,
            a, r, s, status
        ])

        j += 1
        disp_vol = args.disp_start + j * args.disp_step

    header = [
        "j","case_id","I_T","disp_vol","KB","KG","FSC",
        "BM","KM","GM","GM_eff",
        "classical_GM_sign",
        "GM_safe",
        "a","r","s","SSB_status"
    ]
    write_csv(out_csv, header, rows)

    def fmt_hit(label, hit):
        if hit is None:
            return f"{label}: (not reached)"
        x, y = hit
        return f"{label}: disp_vol={x:.6f}  GM_eff={y:.6f}"

    lines = []
    lines.append("SSB DISPLACEMENT SWEEP — DETERMINISTIC REPORT")
    lines.append("")
    lines.append(f"case_id: {args.case_id}")
    lines.append(f"I_T (m^4): {args.I_T}")
    lines.append(f"KB (m): {args.KB}")
    lines.append(f"KG (m): {args.KG}")
    lines.append(f"FSC (m): {args.FSC}")
    lines.append("")
    lines.append(f"disp_vol ∇ sweep: {args.disp_start} .. {args.disp_end} step {args.disp_step}")
    lines.append("")
    lines.append(f"SSB thresholds: GM_safe={args.GM_safe}  a_min={args.a_min}  r_safe={args.r_safe}  s_max={args.s_max}")
    lines.append("")
    lines.append(f"ALLOW: {n_allow}")
    lines.append(f"DENY: {n_deny}")
    lines.append(f"ABSTAIN: {n_abstain}")
    lines.append("")
    lines.append(fmt_hit("First GM_eff < GM_safe", first_below_safe))
    lines.append(fmt_hit("First SSB DENY", first_ssb_deny))
    lines.append(fmt_hit("First Classical UNSTABLE (GM_eff<=0)", first_classical_unstable))
    lines.append("")
    lines.append("Outputs:")
    lines.append(f" - {out_csv}")
    lines.append(f" - {out_txt}")

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
