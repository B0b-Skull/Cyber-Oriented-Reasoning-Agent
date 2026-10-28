#!/usr/bin/env bash
# ==============================================================================
# train_llm_NIX.sh (v3.6.1)
# ------------------------------------------------------------------------------
# Standalone & Integrated Multi-Modal Document, OCR, Diagram & Uncapped
# Cross-Platform CLI/MDP Training Script for C.O.R.A.
# Reads documents and images from Training/ (or a custom directory/file),
# auto-installs any missing Python/system extraction modules, rejoins multi-line
# wrapped PDF commands, verifies 100% of extracted cross-platform commands
# (Linux, Windows CMD/LOLBins, Sysinternals, Active Directory, PowerShell, Cloud,
# Mobile/Forensics, Red Team, Solaris, Cisco IOS) through Engine 12 (CEGAR) with
# zero artificial slice caps, deduplicates by SHA-256 content hash, and writes
# structured notes to core/ObsidianVault/, core/Reasoning/data/trained_rules.json, and
# core/Reasoning/data/mdp_transitions.json (Engine 11 Bellman Q* policy store).
#
# Usage:
#   ./Training/train_llm_NIX.sh                 # Train on ./Training
#   ./Training/train_llm_NIX.sh /path/to/docs   # Train on custom folder or file
#   ./Training/train_llm_NIX.sh --force         # Force re-distill all files
#   ./Training/train_llm_NIX.sh --no-llm        # Deterministic + OCR only (fastest)
#   ./Training/train_llm_NIX.sh --status        # Show training ledger & vault status
#   ./Training/train_llm_NIX.sh --check-deps    # Verify/auto-install Python & OCR deps
# ==============================================================================

set -Eeuo pipefail
trap 'printf "\n\033[1;31m[ERROR]\033[0m train_llm_NIX.sh failed at line %s (exit %s): %s\n" "$LINENO" "$?" "$BASH_COMMAND" >&2' ERR

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORA_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CORE_DIR="${CORA_ROOT}/core"
TRAIN_PY="${CORE_DIR}/Reasoning/train_llm.py"
DEFAULT_TRAIN_DIR="${SCRIPT_DIR}"
export CORA_ROOT CORA_CORE_DIR="${CORE_DIR}" CORA_TRAINING_DIR="${DEFAULT_TRAIN_DIR}" OBSIDIAN_VAULT_DIR="${CORE_DIR}/ObsidianVault"

if [[ ! -f "${TRAIN_PY}" ]]; then
    echo -e "\033[1;31m[ERROR]\033[0m Missing training engine: ${TRAIN_PY}" >&2
    exit 1
fi

mkdir -p "${DEFAULT_TRAIN_DIR}"

# Ensure required Python multi-modal & OCR packages are installed before running
ensure_python_training_deps() {
    python3 -c "import PIL, pypdf, pymupdf, docx, bs4, rapidocr_onnxruntime" >/dev/null 2>&1 && return 0
    echo -e "\033[1;36m[TRAIN-DEPS]\033[0m Verifying and auto-installing multi-modal extraction & CPU Neural OCR modules..."
    python3 "${TRAIN_PY}" --check-deps
}

ensure_python_training_deps

# Pass all arguments directly to Reasoning/train_llm.py
exec python3 "${TRAIN_PY}" "$@"
