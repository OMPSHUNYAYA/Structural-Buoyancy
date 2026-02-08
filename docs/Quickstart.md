# ⭐ Shunyaya Structural Buoyancy (SSB)

## Quickstart

**Deterministic • Trust-Governed • Structurally Conservative**  
**No Simulation • No Tuning • Audit-Friendly**

---

## What You Need

Shunyaya Structural Buoyancy (SSB) is intentionally conservative and operational.

It does **not** modify hydrostatics.  
It does **not** predict capsizing or failure.

SSB governs whether reliance on classical buoyancy and stability remains **structurally admissible over time**.

This is **trust governance**, not physics modeling.

---

## Requirements

- **Python 3.9+ (CPython)**
- **Standard library only** (no external dependencies)

Everything is:

- deterministic  
- offline  
- reproducible  
- identical across machines  

No randomness.  
No training.  
No simulation.  
No probabilistic heuristics.  
No adaptive tuning.

---

## Minimal Project Layout

A minimal public Shunyaya Structural Buoyancy (SSB) validation release contains:

```
SSB/  
  README.md  
  LICENSE  

docs/  
  SSB_v2.1.pdf  
  Concept-Flyer_SSB_v2.1.pdf  
  Quickstart.md  
  FAQ.md  

scripts/  
  ssb_disp_sweep.py  
  ssb_multifsc_ladder.py  
  ssb_cyclic_fatigue.py  
  ssb_phase3_envelope.py  

scripts/illustrative/  
  ssb_illustrative_governance_plot.py  
  ssb_illustrative_physics_vs_trust_plot.py  

outputs/  
  ssb_disp_sweep_out/  
  ssb_multifsc_out/  
  ssb_cyclic_out/  
  ssb_phase3_out/

reference_outputs/
  ssb_disp_sweep_out/
  ssb_multifsc_out/
  ssb_cyclic_out/
  ssb_phase3_out/
```

---

## Important Design Note

SSB is **not a single script**.

SSB uses multiple deterministic scripts because Phase II requires multiple canonical validation families:

- displacement sweep (static margin erosion)
- free-surface accumulation (FSC ladder)
- lifecycle fatigue (cyclic disturbance with `s(t)` accumulation)
- Phase III envelope classification (operational posture)

All scripts preserve:

- determinism  
- reproducibility  
- cross-test invariance of governance rules  

No script learns from another.  
No script tunes parameters.

---

## What SSB Does (One-Minute Mental Model)

Classical buoyancy answers:

- “Does it float?”
- “Is GM positive?”

SSB asks first:

- “Is it safe to continue relying on this floating state — now and across time?”

SSB may withdraw operational reliance while classical stability remains positive.

This is **not prediction**.  
This is **deterministic governance**.

---

## Core Structural Idea (One Line)

**Correctness is not trust.  
Trust is a governed permission.**

---

## Classical Relations (Unchanged)

`BM = I_T / ∇`  
`KM = KB + BM`  
`GM = KM - KG`  
`GM_eff = GM - FSC_total`

SSB preserves these relations **exactly**.

---

## SSB Governance (Unchanged)

`margin = GM_eff / GM_safe`  
`a = clamp01(margin)`  
`r = max(0, 1 - margin)`  
`s(t+1) = s(t) + max(0, r(t) - r_safe)`

---

## Decision Rule (Phase II)

- DENY if `GM_eff <= 0`
- DENY if `a < a_min`
- DENY if `s >= s_max`
- else ALLOW

Decisions are **deterministic and final**.

No trend interpretation.  
No visual inference.  
No probabilistic meaning.

---

## Phase III Envelope (Operational Classification)

Phase III does **not** change Phase II decisions.

It classifies outcomes into operational postures:

- **ALLOW_NORMAL**
- **ALLOW_RESTRICTED_MONITOR**
- **DENY_FINAL**
- **ABSTAIN_HUMAN_REVIEW**

Phase III adds **operational context**, not authority.

---

## Quick Run (Phase II Validation)

Run all commands from the project root.

### 1) Displacement Sweep (Static Margin Erosion)

Command:  
`python scripts/ssb_disp_sweep.py`

Outputs written to:  
`outputs/ssb_disp_sweep_out/YYYYMMDD_HHMMSS__DISP_SWEEP__RUN_TAG/`

---

### 2) Multi-Tank Free-Surface Ladder (FSC Accumulation)

Command:  
`python scripts/ssb_multifsc_ladder.py`

Outputs written to:  
`outputs/ssb_multifsc_out/YYYYMMDD_HHMMSS__MULTI_FSC_LADDER__RUN_TAG/`

---

### 3) Cyclic Fatigue (Structural Time + `s(t)`)

Command:  
`python scripts/ssb_cyclic_fatigue.py`

Outputs written to:  
`outputs/ssb_cyclic_out/YYYYMMDD_HHMMSS__CYCLIC_FATIGUE__RUN_TAG/`

---

## Phase III Envelope Run (Operational Posture)

After generating a Phase II CSV:

Command:  
`python scripts/ssb_phase3_envelope.py --in_csv outputs/ssb_cyclic_out/<RUN_FOLDER>/cyclic_fatigue.csv --tag CYCLIC_PHASE3`

Example:  
`python scripts/ssb_phase3_envelope.py --in_csv outputs/ssb_cyclic_out/20260205_000723__CYCLIC_FATIGUE__FATIGUE_LATE_DENY/cyclic_fatigue.csv --tag CYCLIC_PHASE3`

Outputs written to:  
`outputs/ssb_phase3_out/YYYYMMDD_HHMMSS__PHASE3__CYCLIC_PHASE3/`

---

## Optional: Illustrative Governance Plots (Appendix D)

These utilities reproduce the illustrative figures shown in Appendix D.

They:

- read existing Phase III outputs  
- do not compute `GM`, `a`, or `s`  
- do not influence SSB decisions  
- must not be used for analysis or prediction  

Figure D.1 — Governance Schematic  
Command:  
`python scripts/illustrative/ssb_illustrative_governance_plot.py outputs/ssb_phase3_out/<PHASE3_RUN_FOLDER>`

Figure D.2 — Physical Stability vs Structural Trust  
Command:  
`python scripts/illustrative/ssb_illustrative_physics_vs_trust_plot.py outputs/ssb_phase3_out/<PHASE3_RUN_FOLDER>`

or  

`python scripts/illustrative/ssb_illustrative_physics_vs_trust_plot.py outputs/ssb_phase3_out/<PHASE3_RUN_FOLDER>/phase3_classification.csv`

Mandatory interpretation rule:

**Illustrative only — no quantitative inference permitted.**

---

## Common “File Not Found” Fix (Windows)

If the run folder name is not exact:

Command:  
`dir outputs\ssb_phase3_out`

Copy the exact folder name into the command.

SSB run folders are deterministic strings.  
One character mismatch will fail.

---

## What To Expect (Sanity Checks)

**Displacement sweep**
- SSB DENY begins while GM remains positive
- classical instability occurs later

**FSC ladder**
- SSB may DENY even when `GM_eff > 0`
- `FSC_total` is strictly cumulative

**Cyclic fatigue**
- delayed DENY driven by `s(t)` reaching `s_max`
- lifecycle denial may occur while stability remains positive

**Phase III**
- ALLOW_NORMAL appears early (if at all)
- ALLOW_RESTRICTED_MONITOR near warning thresholds
- DENY_FINAL once hard limits are reached

---

## Why SSB Matters (Buoyancy View)

Many real failures are not physics failures.  
They are **trust failures after long apparent safety**.

SSB formalizes the missing layer:

- stable enough to float  
- but not safe enough to keep trusting indefinitely  

SSB identifies when reliance should be withdrawn, even while physics remains correct.

This is **trust denial**, not failure prediction.

---

## One-Line Summary

**Shunyaya Structural Buoyancy preserves hydrostatics exactly — and adds a deterministic governance envelope that decides when floating remains safe to rely on.**
