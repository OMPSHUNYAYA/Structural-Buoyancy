# ⭐ Shunyaya Structural Buoyancy (SSB)

**Govern Trust Above Physics — Without Changing Physics**

![SSB](https://img.shields.io/badge/SSB-Structural%20Buoyancy-brightgreen)
![Deterministic](https://img.shields.io/badge/Deterministic-Yes-green)
![Trust--Governed](https://img.shields.io/badge/Trust--Governed-Yes-green)
![Structural--Admissibility](https://img.shields.io/badge/Structural%20Admissibility-Explicit-green)
![Refusal--Aware](https://img.shields.io/badge/Refusal--Aware-Yes-green)
![Audit--Ready](https://img.shields.io/badge/Audit--Ready-Yes-green)
![Reproducible](https://img.shields.io/badge/Reproducible-Yes-green)
![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green)

---

## 🔎 What Is Shunyaya Structural Buoyancy?

**Shunyaya Structural Buoyancy (SSB)** is a deterministic **structural governance framework** that determines when buoyancy and stability may continue to be relied upon operationally — even while classical physics remains fully valid.

Classical naval architecture answers:

- Does it float?  
- Is `GM` positive?  
- Is the system statically stable?

SSB introduces a missing layer:

**structural admissibility of reliance**

SSB does **not** modify:

- Archimedes’ principle  
- hydrostatics  
- metacentric height (`GM`)  
- physical forces or geometry  

It governs **when continued reliance on those results becomes structurally inadmissible**.

---

## ⚡ One-Minute Structural Claim (Read This First)

**Positive buoyancy is not the same as safe reliance.**

SSB demonstrates that a system can be:

- classically stable  
- physically floating  
- **yet structurally unsafe to continue relying upon**

SSB is **not** a buoyancy model.  
SSB is a **governance layer above buoyancy**.

It does not ask:

> “Will it capsize?”

It asks:

> **“Is it still structurally responsible to rely on floating?”**

---

## 🔥 Why SSB Matters

Many real-world failures occur **after long periods of apparent safety**:

- vessels that floated safely for years  
- offshore platforms with positive margins  
- systems that failed only after cumulative exposure  

Classical physics has **no formal concept** of:

- lifecycle erosion of trust  
- cumulative structural resistance  
- irreversible withdrawal of reliance  

SSB introduces:

- early governance **without prediction**  
- prevention **without simulation**  
- deterministic denial **without forecasting**

---

## 🧠 One-Minute Mental Model

Classical buoyancy asks:

> “Is the system stable right now?”

SSB asks:

> **“Has this system exhausted its structural permission to be trusted?”**

Physics answers **correctness**.  
SSB governs **permission**.

---

## 🟦 For Non-Mathematical Readers (Important)

You do **not** need formulas to understand SSB.

A bridge may still stand.  
A ship may still float.  
A platform may still appear stable.

Yet continuing to rely on it may **no longer be responsible**.

SSB is the rulebook that says:

> **“Even though nothing has failed yet, continuing reliance is no longer acceptable.”**

SSB does **not** explain *how* failure will happen.  
SSB determines **when trust must be withdrawn**.

---

## 🧪 Deterministic Validation (Executable)

SSB is validated through **deterministic scripts**, not simulations.

Validation families include:

- displacement / KG sweep (static margin erosion)  
- free-surface correction ladder  
- cyclic fatigue accumulation  
- Phase III envelope classification  

All scripts:

- use **standard Python only**  
- are fully **reproducible**  
- contain **no randomness**  
- require **no tuning**  

SSB results remain **invariant under re-run**.

---

## 🔗 Quick Links

### **Documentation**
- [**Concept Flyer (PDF)**](docs/Concept-Flyer_SSB_v2.1.pdf)
- [**Full Specification (PDF)**](docs/SSB_v2.1.pdf)
- [**FAQ**](docs/FAQ.md)
- [**Quickstart Guide**](docs/Quickstart.md)

**Note:** Output folders are intentionally empty.  
All results are reproducible by executing the scripts.

---

### **Executable Validation Scripts**

**Phase II — Canonical Validation Families**
- Displacement sweep (static margin erosion)  
  [`scripts/ssb_disp_sweep.py`](scripts/ssb_disp_sweep.py)

- Free-surface correction ladder (FSC accumulation)  
  [`scripts/ssb_multifsc_ladder.py`](scripts/ssb_multifsc_ladder.py)

- Cyclic fatigue (structural time + lifecycle resistance)  
  [`scripts/ssb_cyclic_fatigue.py`](scripts/ssb_cyclic_fatigue.py)

**Phase III — Operational Envelope Classification**
- Governance envelope synthesis  
  [`scripts/ssb_phase3_envelope.py`](scripts/ssb_phase3_envelope.py)

---

### **Illustrative Utilities (Non-Operational)**
- Governance transition schematic  
  [`scripts/illustrative/ssb_illustrative_governance_plot.py`](scripts/illustrative/ssb_illustrative_governance_plot.py)

- Physical stability vs structural trust visualization  
  [`scripts/illustrative/ssb_illustrative_physics_vs_trust_plot.py`](scripts/illustrative/ssb_illustrative_physics_vs_trust_plot.py)

**Illustrative only — no quantitative inference permitted.**

---

### **Outputs (Reproducible by Design)**

The `outputs/` directory contains **structured folders only**.

- No generated files are committed.
- Folder names document canonical run structure.
- All results are reproduced locally by executing the scripts.

This design ensures:
- clean repositories  
- reproducible science  
- audit clarity  
- no stale or misleading artifacts  

---

### **Repository Metadata**
- **License** — [`LICENSE`](LICENSE)

---

## 🧱 Core Structural Idea (Formal)

SSB separates **physical correctness** from **operational trust**.

Structural state:

- `m` — measured physical value (unchanged physics)  
- `a` — normalized permission / alignment  
- `s` — accumulated structural resistance (lifecycle memory)  

Collapse invariant:

`phi((m, a, s)) = m`

Physics remains exact.  
**Structure governs admissibility.**

---

## 🧭 ALLOW / RESTRICT / DENY (Phase III)

SSB produces **governance envelopes**, not predictions:

- **ALLOW_NORMAL** — reliance structurally admissible  
- **ALLOW_RESTRICTED_MONITOR** — reliance allowed with constraints  
- **DENY_FINAL** — reliance structurally inadmissible  
- **ABSTAIN_HUMAN_REVIEW** — insufficient or invalid inputs  

DENY may occur **before classical instability**.  
This is **intentional and conservative**.

---

## 🛑 What SSB Prevents

SSB prevents situations where:

- `GM` remains positive  
- physics appears safe  
- cumulative exposure silently erodes trust  

It blocks:

- delayed failures  
- false confidence  
- lifecycle-blind operation  

SSB denies **early**, **deterministically**, and **conservatively**.

---

## 🔍 What SSB Evaluates (and What It Does Not)

SSB evaluates **admissibility of reliance**, not stability itself.

It does **not**:

- predict capsizing  
- optimize design  
- correct instability  
- act as a controller  

SSB never intervenes in the system.  
It governs **whether reliance should continue**.

---

## 🧪 Determinism & Closure Guarantees

SSB guarantees:

- identical outputs for identical inputs  
- monotonic resistance accumulation  
- irreversible denial once trust is exhausted  
- idempotent re-evaluation  

No randomness.  
No probability.  
No learning.  
No adaptive tuning.

---

## 📘 Illustrative Governance Schematic (Optional)

SSB includes an **optional illustrative schematic** (Appendix D) that visually explains governance transitions:

`ALLOW_NORMAL → ALLOW_RESTRICTED_MONITOR → DENY_FINAL`

This schematic:

- is **non-quantitative**  
- does **not** represent time or probability  
- does **not** participate in validation or decision-making  

Any reproduction must include:

> **“Illustrative only — no quantitative inference permitted.”**

---

## 🛠 Illustrative Utility Script (Optional)

An optional script is provided under:

`scripts/illustrative/`

This utility:

- reads existing Phase III outputs  
- does **not** compute `GM`, `a`, or `s`  
- does **not** influence SSB decisions  

**Illustrative only — no quantitative inference permitted.**

---

## 👤 Who Is SSB For?

SSB is intended for:

- naval architects and marine engineers  
- offshore and floating-infrastructure safety teams  
- disaster-response system designers  
- researchers studying delayed failure  
- governance and safety-engineering frameworks  

It is **not** intended as:

- an autopilot  
- a real-time controller  
- a predictive safety score  

---

## 🌍 Scope Focus & Future SGS Extensions

This release intentionally centers on **buoyancy** as the canonical demonstration domain for **Structural Governance Systems (SGS)**.

Non-buoyancy worked examples (e.g., structural fatigue, economic equilibria) are intentionally deferred to subsequent dedicated SGS implementations.

**Why this focus?**

Establishing SSB as a complete, executable, and rigorously validated instance first ensures the SGS class (axioms, invariants, contract) is proven in one clean domain before broader application.

This avoids dilution and strengthens foundational credibility.

Future releases will instantiate the same deterministic governance logic in additional equilibrium-critical domains.

---

## 📊 Key Deterministic Findings (Phase II)

Across reproducible tests (no simulation, no tuning):

- SSB consistently denies operational trust while classical stability (`GM_eff > 0`) remains positive  
- denial precedes physical instability, creating a conservative governance buffer  
- lifecycle accumulation enables delayed denial under repeated exposure, even with recovering margins  
- results are identical across machines and runs; monotonic and irreversible by construction  

---

## 🧭 Positioning in the Shunyaya Framework

SSB belongs to the Shunyaya governance family:

- **SGS** — Structural Governance Systems (class)  
- **SSB** — Structural Buoyancy (this work)  
- **SSTS** — Structural Transition Science  
- **SSD** — Structural Diagnosis  

SSB does **not** bypass physics.  
It governs **when physics may be trusted**.

---

## 📄 License & Attribution

**License:** CC BY 4.0  

**Attribution:**  
Shunyaya Structural Buoyancy (SSB)

Provided *as is*, without warranty.

---

## 🏷️ Topics

Structural-Buoyancy • Safety-Governance • Deterministic-Safety •  
Lifecycle-Engineering • Trust-Systems • No-Simulation • Shunyaya

---

## One-Line Summary

**Shunyaya Structural Buoyancy preserves classical buoyancy exactly — and adds a deterministic governance layer that determines when floating must no longer be relied upon.**
