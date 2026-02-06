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

def compute_base(I_T, disp_vol, KB, KG):
    # BM = I_T / disp_vol
    # KM = KB + BM
    # GM = KM - KG
    if not (is_finite(I_T) and is_finite(disp_vol) and is_finite(KB) and is_finite(KG)):
        return None
    if disp_vol <= 0.0 or I_T <= 0.0:
        return None
    BM = I_T / disp_vol
    KM = KB + BM
    GM = KM - KG
    return BM, KM, GM

def ssb_gate(GM_eff, GM_safe, a_min, s_old, r_safe, s_max):
    # margin = GM_eff / GM_safe
    # a = clamp01(margin)
    # r = max(0, 1 - margin)
    # s(t+1) = s(t) + max(0, r - r_safe)
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

def schedule_delta(t, mode, amp, period, duty):
    # Deterministic disturbance penalty delta(t) >= 0 applied to GM_eff:
    # GM_eff(t) = GM - FSC - delta(t)
    if mode == "square":
        phase = (t % period) / float(period)
        return amp if phase < duty else 0.0
    elif mode == "sine_abs":
        return amp * abs(math.sin(2.0 * math.pi * (t / float(period))))
    elif mode == "ramp":
        phase = (t % period) / float(period)
        return amp * phase
    else:
        return amp  # constant

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default="ssb_cyclic_out", help="Base output directory.")
    ap.add_argument("--case_id", default="CYCLIC_FATIGUE", help="Case label.")
    ap.add_argument("--tag", default="", help="Optional run tag (e.g., FATIGUE_LATE_DENY).")

    ap.add_argument("--I_T", type=float, default=3.60, help="Waterplane second moment I_T (m^4).")
    ap.add_argument("--disp_vol", type=float, default=8.00, help="Displaced volume ∇ (m^3).")
    ap.add_argument("--KB", type=float, default=0.55, help="KB (m).")
    ap.add_argument("--KG", type=float, default=0.88, help="KG (m).")
    ap.add_argument("--FSC", type=float, default=0.06, help="Base free surface correction FSC (m).")

    ap.add_argument("--T", type=int, default=200, help="Number of steps (deterministic ticks).")

    ap.add_argument("--mode", default="square", choices=["square","sine_abs","ramp","constant"],
                    help="Deterministic disturbance schedule.")
    ap.add_argument("--amp", type=float, default=0.06, help="Disturbance amplitude penalty (m).")
    ap.add_argument("--period", type=int, default=20, help="Schedule period in ticks.")
    ap.add_argument("--duty", type=float, default=0.35, help="Square wave duty cycle (0..1).")

    ap.add_argument("--GM_safe", type=float, default=0.15, help="Declared safe GM_eff threshold (m).")
    ap.add_argument("--a_min", type=float, default=0.70, help="Minimum permission.")
    ap.add_argument("--r_safe", type=float, default=0.10, help="Risk tolerance before resistance accumulates.")
    ap.add_argument("--s_max", type=float, default=1.00, help="Maximum allowed resistance.")

    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    run_dir = safe_run_dir(args.out_dir, args.case_id, args.tag)

    out_csv = os.path.join(run_dir, "cyclic_fatigue.csv")
    out_txt = os.path.join(run_dir, "cyclic_fatigue_report.txt")

    base = compute_base(args.I_T, args.disp_vol, args.KB, args.KG)
    if base is None:
        raise SystemExit("Invalid base inputs (I_T, disp_vol, KB, KG).")
    BM, KM, GM = base

    s = 0.0
    first_deny_t = None

    rows = []
    for t in range(args.T):
        delta = schedule_delta(t, args.mode, args.amp, max(1, args.period), max(0.0, min(1.0, args.duty)))
        GM_eff = GM - args.FSC - delta
        classical = "STABLE" if (is_finite(GM_eff) and GM_eff > 0.0) else "UNSTABLE"

        a, r, s, status = ssb_gate(GM_eff, args.GM_safe, args.a_min, s, args.r_safe, args.s_max)

        if first_deny_t is None and status == "DENY":
            first_deny_t = (t, GM_eff, a, r, s, delta)

        rows.append([
            t, args.case_id,
            args.I_T, args.disp_vol, args.KB, args.KG, args.FSC,
            BM, KM, GM,
            delta, GM_eff,
            classical,
            args.GM_safe,
            a, r, s, status
        ])

    header = [
        "t","case_id",
        "I_T","disp_vol","KB","KG","FSC",
        "BM","KM","GM",
        "delta","GM_eff",
        "classical_GM_sign",
        "GM_safe",
        "a","r","s","SSB_status"
    ]
    write_csv(out_csv, header, rows)

    lines = []
    lines.append("SSB CYCLIC FATIGUE — DETERMINISTIC REPORT")
    lines.append("")
    lines.append(f"case_id: {args.case_id}")
    lines.append("Base relations: BM=I_T/∇, KM=KB+BM, GM=KM-KG")
    lines.append(f"I_T={args.I_T}  ∇={args.disp_vol}  KB={args.KB}  KG={args.KG}  FSC={args.FSC}")
    lines.append(f"Derived: BM={BM:.6f}  KM={KM:.6f}  GM={GM:.6f}")
    lines.append("")
    lines.append("Lifecycle law:")
    lines.append("GM_eff(t) = GM - FSC - delta(t)")
    lines.append(f"delta schedule: mode={args.mode} amp={args.amp} period={args.period} duty={args.duty}")
    lines.append("")
    lines.append(f"SSB thresholds: GM_safe={args.GM_safe}  a_min={args.a_min}  r_safe={args.r_safe}  s_max={args.s_max}")
    lines.append("")
    if first_deny_t is None:
        lines.append("First DENY: (not reached)")
    else:
        t, gme, a, r, s_val, delta = first_deny_t
        lines.append(f"First DENY at t={t} with GM_eff={gme:.6f}  delta={delta:.6f}  a={a:.6f}  r={r:.6f}  s={s_val:.6f}")
    lines.append("")
    lines.append("Outputs:")
    lines.append(f" - {out_csv}")
    lines.append(f" - {out_txt}")

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
