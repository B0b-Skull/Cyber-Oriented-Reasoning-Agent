#!/usr/bin/env bash
# ==============================================================================
# Linux Installer, Hardware-Adaptive Profiler & Maintenance Script for CORA
# 15-Engine 5-Layer Lexical Neuro-Symbolic, Somatic, Forecasting, Continual, Meta-Learning,
# Trajectory RL & Spectral PCA/K-Means++ Suite + 80/20 Pareto Gating (v4.5.0-15Engine-Core, 0 MB GPU VRAM)
#
# Engines:
#   1. Associative Bipartite Obsidian Vault Graph + PageRank (engines/associative.py)
#   2. Geometric, Spatial & Z3 SMT Constraint Solver (engines/geometric.py)
#   3. Bayesian Abductive Root-Cause Engine + EIG (engines/bayesian.py)
#   4. Causal DAG Engine & Pearl's do(X) Surgery (engines/causal.py)
#   5. Hyperdimensional VSA (1,024-D) + Damasio Somatic Gut Valence Marker (engines/vsa.py)
#   6. Event-Calculus & Temporal State/Fluent Tracker (engines/temporal_fluents.py)
#   7. Dempster-Shafer Theory of Evidence & Conflict Detector (engines/dempster_shafer.py)
#   8. Case-Based Reasoning (CBR) & Failure Fingerprinting (engines/cbr_fingerprints.py)
#   9. CEGAR Pre-Execution Command Verifier (engines/cegar_verifier.py)
#   10. SyGuS / Structure-Guided CLI Fact Extractor (engines/sygus_extractor.py)
#   11. Hierarchical Tactical MDP + Optimal Stopping & Speculative Forecast (engines/mdp_tactical.py)
#   12. Online Continual Learning (AUTO|START|STOP) & Pass-2 Refinement (engines/continual_learner.py)
#   13. Multiplicative-Weights Hedge Meta-Learner & Brier/ECE Calibration (engines/meta_learner.py)
#   14. Multi-Step Trajectory RL (TD(lambda)) & Symbolic Network World-Model (engines/rl_network_policy.py)
#   15. Spectral Manifold PCA, K-Means++ Regime Clustering & Graph Laplacian (engines/spectral_manifold_pca.py)
#   + Part 1 Zero-Loss Context Virtual Memory & Speculative Lookahead Cache (engines/context_vm.py)
#   + Unified 15-Stage Orchestrator with 80/20 Pareto Gating & Consensus Arbiter (engines/pipeline.py)
#   + Uncapped Multi-Modal Document, PDF & Cross-Platform CLI Training Pipeline (train_llm.py)
#
# Usage:
#   bash core/Reasoning/install_reasoning_NIX.sh               # Full compatibility check, setup, seed & test
#   bash core/Reasoning/install_reasoning_NIX.sh --check       # Verify hardware resources & adaptive limits only
#   bash core/Reasoning/install_reasoning_NIX.sh --status      # Show package, hardware tier, Vault Graph & model status
#   bash core/Reasoning/install_reasoning_NIX.sh --test        # Run 15-engine + 10-guardrail + uncapped extractor self-tests
#   bash core/Reasoning/install_reasoning_NIX.sh --seed        # Re-seed data/ & ObsidianVault/reasoning/
#   bash core/Reasoning/install_reasoning_NIX.sh --offline     # Install from local wheelhouse/
#   bash core/Reasoning/install_reasoning_NIX.sh --save-wheels # Cache wheels for air-gapped labs
# ==============================================================================
set -Eeuo pipefail

trap 'printf "\n[ERROR] install_reasoning_NIX.sh failed at line %s (exit code %s).\n" "$LINENO" "$?" >&2' ERR

_SCRIPT_DIR=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
REASONING_DIR="$_SCRIPT_DIR"
CORA_CORE_DIR=$(dirname "$REASONING_DIR")

mkdir -p "$CORA_CORE_DIR/Log"
chmod 775 "$CORA_CORE_DIR/Log" 2>/dev/null || true
chmod +x "$REASONING_DIR/install_reasoning.py" "$REASONING_DIR/reasoning_cli.py" "$CORA_CORE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" "$CORA_CORE_DIR/Network_Isolation/console_posture.py" 2>/dev/null || true

if [[ -x "$CORA_CORE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" ]]; then
  bash "$CORA_CORE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" --detect || true
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf '[ERROR] python3 is not installed. Please install Python 3.9+ first (e.g., sudo apt install python3 python3-pip).\n' >&2
  exit 1
fi

# Pre-flight Bash hardware & Python version verification
PY_OK=$(python3 -c 'import sys; print(1 if sys.version_info >= (3, 9) else 0)' 2>/dev/null || echo 0)
if [[ "$PY_OK" != "1" ]]; then
  printf '[ERROR] Python 3.9+ is required. Found: %s\n' "$(python3 --version 2>&1)" >&2
  exit 1
fi

MODE="${1:---all}"
case "$MODE" in
  --all|all|--full|full)
    exec python3 "$REASONING_DIR/install_reasoning.py" --all
    ;;
  --check|--check-compat|check)
    exec python3 "$REASONING_DIR/install_reasoning.py" --check-compat
    ;;
  --status|status)
    exec python3 "$REASONING_DIR/install_reasoning.py" --status
    ;;
  --test|test)
    exec python3 "$REASONING_DIR/install_reasoning.py" --test
    ;;
  --seed|seed)
    exec python3 "$REASONING_DIR/install_reasoning.py" --seed
    ;;
  --offline|offline)
    exec python3 "$REASONING_DIR/install_reasoning.py" --check-compat --install-deps --offline --seed --test
    ;;
  --save-wheels|save-wheels|--download-wheels)
    exec python3 "$REASONING_DIR/install_reasoning.py" --download-wheels
    ;;
  --help|-h|help)
    cat <<'EOT'
Usage: bash core/Reasoning/install_reasoning_NIX.sh [OPTION]

Options:
  --all          Analyze system compatibility/hardware scaling limits, install/verify all
                 15-engine Python packages (numpy, scipy, networkx, sympy, z3-solver, shapely),
                 initialize Reasoning/data/ and ObsidianVault/, and run self-tests [DEFAULT]
  --check        Analyze and verify system compatibility, CPU threads, RAM, disk, and 0 MB VRAM isolation
  --status       Display installed packages, hardware tier, Bipartite Vault Graph scale, and stored models
  --test         Run deterministic self-tests across all 15 engines + 10 guardrails + uncapped extractor
  --seed         Initialize/refresh default models in Reasoning/data/ and ObsidianVault/
  --offline      Verify compatibility and install dependencies from Reasoning/wheelhouse/ without internet
  --save-wheels  Download all required wheels to Reasoning/wheelhouse/ for offline replication
EOT
    exit 0
    ;;
  *)
    exec python3 "$REASONING_DIR/install_reasoning.py" "$@"
    ;;
esac
