---
type: meta-learning-audit
date: 2026-10-26
brier_score: 0.1052
ece_pct: 4.7
top_engine: mdp_tactical
status: ACTIVE
---

# Meta-Learning & Next-Tool Forecast Calibration Audit (2026-10-26)

> [!IMPORTANT]
> Automatically synthesized by **Engine 17 (`meta_learner.py`)** to audit reasoning accuracy, calibrate tool-forecasting weights, and prune redundant diagnostic steps.

- **Parent Index:** [[00_MEMORY_INDEX]] | [[00_SUGGESTED_IMPROVEMENTS_INDEX]]

### Engine 17: Meta-Learning Hedge Arbiter & Forecast Calibration (`0.17 ms`)
- **Global Forecast Brier Score:** `0.1052` (Lower is better; `< 0.15` = High Calibration)
- **Expected Calibration Error (ECE):** `4.70%`
- **Top Authority Engine Family:** **`mdp_tactical`** (Weight `1.879`)

#### Multiplicative-Weights (Hedge) Engine Attribution Table
| Rank | Engine Family | Hedge Trust Weight ($w_k$) | Empirical Hit Rate | Family Brier Score |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `mdp_tactical` (Engine 15: Hierarchical Tactical MDP & Optimal Stopping) | **`1.879`** | `90.4%` (73 evals) | `0.0975` |
| **2** | `rl_network_policy` (Engine 19: Dual-Mode Pessimistic Q_LCB Trajectory RL & Network World-Model) | **`1.512`** | `87.0%` (54 evals) | `0.1167` |
| **3** | `cbr_fingerprints` (Engine 11: CBR Failure-to-Fix Fingerprints) | **`1.200`** | `100.0%` (8 evals) | `0.0600` |
| **4** | `spectral_manifold_pca` (Engine 20: Prototype-Anchored K-Means++, SVD PCA & Mahalanobis Shield) | **`1.120`** | `90.0%` (10 evals) | `0.0960` |
| **5** | `bayesian_eig` (Engine 4: Bayesian Abduction & Shannon EIG) | **`1.100`** | `83.3%` (12 evals) | `0.1100` |
| **6** | `asp_planner` (Engine 8: Clingo Non-Monotonic ASP Lookahead) | **`1.050`** | `90.0%` (10 evals) | `0.1150` |
| **7** | `vsa_somatic` (Engine 7: 32,768-D VSA & Damasio Somatic Valence) | **`1.050`** | `90.0%` (10 evals) | `0.1100` |
| **8** | `evolutionary_map_elites` (Engine 14: Evolutionary MAP-Elites Capability Chains) | **`1.000`** | `87.5%` (8 evals) | `0.1300` |
