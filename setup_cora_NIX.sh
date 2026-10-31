#!/usr/bin/env bash
# ==============================================================================
# setup_cora_NIX.sh — Master Linux Setup Script for CORA (v4.5.0-15Engine-Core)
# ==============================================================================
# Full Linux equivalent of setup_cora_WIN.ps1. Configures the entire CORA stack:
#   1. Validates system prerequisites (bash, python3, curl/wget, tar, disk space)
#      and auto-detects CPU cores/threads, NUMA topology, System RAM, and GPU VRAM.
#   2. Initializes all workspace directories (core/Log/, core/bin/, models/,
#      Projects/, core/ObsidianVault/, core/Reasoning/, core/Network_Isolation/,
#      Troubleshooting/, Training/, core/Explained/) and 00_MEMORY_INDEX.md.
#   3. Downloads & verifies prebuilt Linux llama.cpp (b11802) CUDA 12.8 x64
#      binaries + CUDA runtime into core/bin/ (with automatic CPU x64 fallback).
#   4. Downloads & verifies GGUF LLM models into models/ with resume + byte-size
#      verification where practical for host RAM/VRAM:
#        - Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.24 GiB)
#        - Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.40 GiB)
#        - Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB, Multiple Token Prediction)
#        - Qwen3.8-27B-Turbo-MTP-Q6_K.gguf   (22.38 GiB, Multiple Token Prediction)
#        - Qwen3.8-27B-Turbo-MTP-Q8_0.gguf   (28.16 GiB, Multiple Token Prediction)
#   5. Runs core/Network_Isolation/ConsolePostureDetection_NIX.sh --detect.
#   6. Runs core/Reasoning/install_reasoning_NIX.sh --all to profile hardware,
#      compute scaling parameters for all 15 CPU Neuro-Symbolic Reasoning Engines,
#      and seed/test all 15 engines.
#   7. Runs Training/train_llm_NIX.sh --check-deps and Troubleshooting/troubleshoot_llm_NIX.sh --quick,
#      then displays ./run_cora_NIX.sh models, ./run_cora_NIX.sh tune, and Quick Start commands.
# ==============================================================================
set -Eeuo pipefail

on_error() {
  local line_no="$1"
  local cmd="$2"
  local exit_code="$3"
  printf '\n\033[1;31m[ERROR] setup_cora_NIX.sh failed at line %s (exit code %s):\033[0m\n  Command: %s\n' \
    "$line_no" "$exit_code" "$cmd" >&2
  exit "$exit_code"
}
trap 'on_error "$LINENO" "$BASH_COMMAND" "$?"' ERR

LLAMA_BUILD_TAG="b11802"
LLAMA_CUDA_URL="https://github.com/ggml-org/llama.cpp/releases/download/${LLAMA_BUILD_TAG}/llama-${LLAMA_BUILD_TAG}-bin-ubuntu-cuda-12.8-x64.tar.gz"
LLAMA_CUDART_URL="https://github.com/ggml-org/llama.cpp/releases/download/${LLAMA_BUILD_TAG}/cudart-llama-${LLAMA_BUILD_TAG}-bin-ubuntu-cuda-12.8-x64.tar.gz"
LLAMA_CPU_URL="https://github.com/ggml-org/llama.cpp/releases/download/${LLAMA_BUILD_TAG}/llama-${LLAMA_BUILD_TAG}-bin-ubuntu-x64.tar.gz"

QWEN38_URL="https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/resolve/main/RVN-Q3_K_M-multilingual.gguf"
QWEN38_FILE="Qwen3.8-27B-Uncensored-Q3_K_M.gguf"
QWEN38_MIN_BYTES=13000000000

QWEN35_URL="https://huggingface.co/HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive/resolve/main/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
QWEN35_FILE="Qwen3.5-9B-Uncensored-Q4_K_M.gguf"
QWEN35_MIN_BYTES=5500000000

QWEN38_TURBO_HF_BASE="https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF/resolve/main"
QWEN38_TURBO_Q4_URL="${QWEN38_TURBO_HF_BASE}/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q4_K_M.gguf"
QWEN38_TURBO_Q4_FILE="Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf"
QWEN38_TURBO_Q4_HF_FILE="Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q4_K_M.gguf"
QWEN38_TURBO_Q4_MIN_BYTES=18000000000

QWEN38_TURBO_Q6_URL="${QWEN38_TURBO_HF_BASE}/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q6_K.gguf"
QWEN38_TURBO_Q6_FILE="Qwen3.8-27B-Turbo-MTP-Q6_K.gguf"
QWEN38_TURBO_Q6_HF_FILE="Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q6_K.gguf"
QWEN38_TURBO_Q6_MIN_BYTES=23500000000

QWEN38_TURBO_Q8_URL="${QWEN38_TURBO_HF_BASE}/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q8_0.gguf"
QWEN38_TURBO_Q8_FILE="Qwen3.8-27B-Turbo-MTP-Q8_0.gguf"
QWEN38_TURBO_Q8_HF_FILE="Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q8_0.gguf"
QWEN38_TURBO_Q8_MIN_BYTES=29500000000

SCRIPT_DIR=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
if [[ -n "${CORA_ROOT:-}" ]]; then
  CORA_ROOT=$(readlink -m "$CORA_ROOT")
elif [[ -n "${INSTALL_DIR:-}" ]]; then
  CORA_ROOT=$(readlink -m "$INSTALL_DIR")
elif [[ "$(basename "$SCRIPT_DIR")" == "core" ]]; then
  CORA_ROOT=$(dirname "$SCRIPT_DIR")
else
  CORA_ROOT="$SCRIPT_DIR"
fi
BASE_DIR="$CORA_ROOT/core"

DOWNLOAD_MODE="auto" # auto | all | all-turbo | turbo-q4 | turbo-q6 | turbo-q8 | 3.8 | 3.5 | none
SETUP_REASONING=1
OFFLINE=0
SKIP_TESTS=0

usage() {
  cat <<'EOF'
Usage: ./setup_cora_NIX.sh [options]

Options:
  --all-models       Download all 5 models: Qwen3.5-9B (5.24 GiB), Qwen3.8-27B Q3_K_M (12.40 GiB),
                     and Qwen3.8-27B Turbo MTP Q4_K_M (17.23 GiB), Q6_K (22.38 GiB), Q8_0 (28.16 GiB)
  --all-turbo        Download all 3 Qwen3.8-27B Turbo MTP models (Q4_K_M, Q6_K, and Q8_0)
  --turbo            Download Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB, Multiple Token Prediction)
  --only-turbo-q4    Download only Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB)
  --only-turbo-q6    Download only Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.38 GiB)
  --only-turbo-q8    Download only Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.16 GiB)
  --only-3.8         Download only Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.40 GiB)
  --only-3.5         Download only Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.24 GiB)
  --skip-models      Configure folders and install binaries without downloading models
  --full-reasoning   Install, verify compatibility, seed, and test the 15-Engine Streamlined Core
                     Neuro-Symbolic, Somatic, Forecasting, Continual, Meta-Learning, Trajectory RL &
                     Spectral PCA/K-Means++ Reasoning Suite (v4.5.0-15Engine-Core) [DEFAULT]
  --skip-reasoning   Skip automatic setup of the 15-Engine Reasoning Suite
  --offline          Configure environment offline without network downloads
  --skip-tests       Skip final quick troubleshooting suite verification
  --dir PATH         Target installation directory (default: current CORA root)
  -h, --help         Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all-models)                 DOWNLOAD_MODE="all"; shift ;;
    --all-turbo|--turbo-all)      DOWNLOAD_MODE="all-turbo"; shift ;;
    --turbo|--only-turbo-q4)      DOWNLOAD_MODE="turbo-q4"; shift ;;
    --only-turbo-q6|--turbo-q6)   DOWNLOAD_MODE="turbo-q6"; shift ;;
    --only-turbo-q8|--turbo-q8)   DOWNLOAD_MODE="turbo-q8"; shift ;;
    --only-3.8)                   DOWNLOAD_MODE="3.8"; shift ;;
    --only-3.5)                   DOWNLOAD_MODE="3.5"; shift ;;
    --skip-models)                DOWNLOAD_MODE="none"; shift ;;
    --full-reasoning|--with-reasoning) SETUP_REASONING=1; shift ;;
    --skip-reasoning)             SETUP_REASONING=0; shift ;;
    --offline)                    OFFLINE=1; DOWNLOAD_MODE="none"; shift ;;
    --skip-tests)                 SKIP_TESTS=1; shift ;;
    --dir)
      if [[ $# -lt 2 || -z "${2:-}" ]]; then
        printf 'Error: --dir requires a target directory path.\n' >&2
        exit 2
      fi
      CORA_ROOT=$(readlink -m "$2"); BASE_DIR="$CORA_ROOT/core"
      shift 2
      ;;
    --dir=*)
      CORA_ROOT=$(readlink -m "${1#*=}"); BASE_DIR="$CORA_ROOT/core"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

check_dependencies() {
  local missing=()
  for cmd in python3 tar awk stat sed grep; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      missing+=("$cmd")
    fi
  done
  if (( OFFLINE == 0 )) && ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
    missing+=("curl (or wget)")
  fi
  if (( ${#missing[@]} > 0 )); then
    printf 'Error: Missing required system utilities: %s\n' "${missing[*]}" >&2
    printf 'Install them first with: sudo apt update && sudo apt install -y python3 curl wget tar coreutils gawk sed grep tio\n' >&2
    exit 1
  fi
}

fetch_stream_extract() {
  local url="$1"
  local dest_dir="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fL --retry 3 --retry-delay 2 --connect-timeout 20 "$url" | tar -xz --strip-components=1 -C "$dest_dir"
  else
    wget -qO- --tries=3 --timeout=20 "$url" | tar -xz --strip-components=1 -C "$dest_dir"
  fi
}

check_dependencies

printf '==============================================================================\n'
printf '  CORA Linux Master Setup + GGUF Models + 15-Engine Suite (v4.5.0-15Engine-Core)\n'
printf '  Target Directory: %s\n' "$CORA_ROOT"
printf '==============================================================================\n\n'

# 1. Create folder structure & ensure executable permissions
printf '[Step 1/7] Creating CORA directory structure & initializing Obsidian Knowledge Vault...\n'
mkdir -p "$CORA_ROOT/Projects" \
  "$CORA_ROOT/Training" "$CORA_ROOT/Troubleshooting" "$CORA_ROOT/models" \
  "$BASE_DIR/Log" "$BASE_DIR/Explained/assets" \
  "$BASE_DIR/bin" \
  "$BASE_DIR/ObsidianVault/.obsidian" "$BASE_DIR/ObsidianVault/targets" \
  "$BASE_DIR/ObsidianVault/commands" "$BASE_DIR/ObsidianVault/projects" \
  "$BASE_DIR/ObsidianVault/knowledge" "$BASE_DIR/ObsidianVault/reasoning" \
  "$BASE_DIR/Reasoning" "$BASE_DIR/Network_Isolation"
chmod 775 "$BASE_DIR/Log" "$CORA_ROOT/Projects" 2>/dev/null || true
for _pdir in "$CORA_ROOT/Projects"/*/; do
  if [[ -d "$_pdir" ]]; then
    mkdir -p "${_pdir%/}/Files" 2>/dev/null || true
  fi
done

if (( OFFLINE == 0 )) && [[ -f "$BASE_DIR/webui/requirements.txt" ]]; then
  python3 -m pip install -q -r "$BASE_DIR/webui/requirements.txt" 2>/dev/null || \
    python3 -m pip install --break-system-packages -q -r "$BASE_DIR/webui/requirements.txt" 2>/dev/null || true
fi

# Initialize ObsidianVault/.obsidian/app.json and 00_MEMORY_INDEX.md if missing
if [[ ! -f "$BASE_DIR/ObsidianVault/.obsidian/app.json" ]]; then
  cat <<'EOF' > "$BASE_DIR/ObsidianVault/.obsidian/app.json"
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "folder",
  "newFileFolderPath": "knowledge",
  "showUnsupportedFiles": false,
  "strictLineBreaks": false,
  "readableLineLength": true
}
EOF
fi

if [[ ! -f "$BASE_DIR/ObsidianVault/00_MEMORY_INDEX.md" ]]; then
  cat <<EOF > "$BASE_DIR/ObsidianVault/00_MEMORY_INDEX.md"
# CORA Knowledge & Memory Index (\`00_MEMORY_INDEX\`)

> **Tier-1 Hot Memory:** Automatically loaded into Qwen 3.8 / 3.5 on every session.

## Core Facts & Environment
- CORA Base Path: \`$BASE_DIR\`
- Obsidian Vault Path: \`$BASE_DIR/ObsidianVault\`
- Always use \`scan_target\` before crafting \`curl\` requests against an unfamiliar URL or host.
- Save verified working \`curl\` commands, endpoints, and solutions using \`vault_save_note\`.

## Indexed Vault Notes
<!-- AUTO-INDEX-START -->
<!-- AUTO-INDEX-END -->
EOF
fi

chmod +x \
  "$CORA_ROOT/run_cora_NIX.sh" \
  "$CORA_ROOT/setup_cora_NIX.sh" \
  "$CORA_ROOT/Training/train_llm_NIX.sh" \
  "$CORA_ROOT/Troubleshooting/troubleshoot_llm_NIX.sh" \
  "$CORA_ROOT/Troubleshooting/troubleshoot_core.py" \
  "$BASE_DIR/agent-cli.py" \
  "$BASE_DIR/Reasoning/install_reasoning_NIX.sh" \
  "$BASE_DIR/Reasoning/install_reasoning.py" \
  "$BASE_DIR/Reasoning/reasoning_cli.py" \
  "$BASE_DIR/Reasoning/train_llm.py" \
  "$BASE_DIR/Reasoning/report_generator.py" \
  "$BASE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" \
  "$BASE_DIR/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh" \
  "$BASE_DIR/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh" 2>/dev/null || true

# 2. Download & extract llama.cpp binaries if not already installed
printf '\n[Step 2/7] Checking llama.cpp binaries in %s/bin ...\n' "$BASE_DIR"
if [[ -x "$BASE_DIR/bin/llama-server" ]] && LD_LIBRARY_PATH="$BASE_DIR/bin:${LD_LIBRARY_PATH:-}" "$BASE_DIR/bin/llama-server" --version >/dev/null 2>&1; then
  printf '  -> llama-server binary already installed and verified.\n'
elif (( OFFLINE == 1 )); then
  printf '  [WARN] Offline mode active and llama-server binary is not present in %s/bin.\n' "$BASE_DIR"
else
  if command -v nvidia-smi >/dev/null 2>&1; then
    printf '  -> NVIDIA GPU detected. Downloading llama.cpp %s CUDA 12.8 binaries + CUDA runtime ...\n' "$LLAMA_BUILD_TAG"
    if ! (fetch_stream_extract "$LLAMA_CUDA_URL" "$BASE_DIR/bin" && fetch_stream_extract "$LLAMA_CUDART_URL" "$BASE_DIR/bin"); then
      printf '  [!] Warning: CUDA binary download failed; falling back to CPU x64 binaries...\n' >&2
      fetch_stream_extract "$LLAMA_CPU_URL" "$BASE_DIR/bin"
    fi
  else
    printf '  -> No NVIDIA GPU detected. Downloading llama.cpp %s CPU x64 binaries ...\n' "$LLAMA_BUILD_TAG"
    fetch_stream_extract "$LLAMA_CPU_URL" "$BASE_DIR/bin"
  fi
  chmod +x "$BASE_DIR/bin/llama-server" "$BASE_DIR/bin/llama-cli" 2>/dev/null || true
  if ! LD_LIBRARY_PATH="$BASE_DIR/bin:${LD_LIBRARY_PATH:-}" "$BASE_DIR/bin/llama-server" --version >/dev/null 2>&1; then
    printf 'Error: llama-server binary failed verification after extraction in %s/bin\n' "$BASE_DIR" >&2
    exit 1
  fi
  printf '  -> Binaries installed and verified.\n'
fi

# 3. Download LLM models (Qwen3.5-9B, Qwen3.8-27B Q3_K_M, and Qwen3.8-27B Turbo MTP Q4_K_M / Q6_K / Q8_0 as practical)
printf '\n[Step 3/7] Checking & downloading CORA GGUF models in %s/models ...\n' "$CORA_ROOT"

TOTAL_RAM_MIB=$(awk '/MemTotal:/ {printf "%d", $2/1024}' /proc/meminfo 2>/dev/null || echo 16384)
TOTAL_VRAM_MIB=0
if command -v nvidia-smi >/dev/null 2>&1; then
  TOTAL_VRAM_MIB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | awk '{s+=int($1)} END {print s+0}' || echo 0)
fi

WANT_35=0
WANT_38=0
WANT_TURBO_Q4=0
WANT_TURBO_Q6=0
WANT_TURBO_Q8=0

case "$DOWNLOAD_MODE" in
  all)
    WANT_35=1
    WANT_38=1
    WANT_TURBO_Q4=1
    WANT_TURBO_Q6=1
    WANT_TURBO_Q8=1
    ;;
  all-turbo)
    WANT_TURBO_Q4=1
    WANT_TURBO_Q6=1
    WANT_TURBO_Q8=1
    ;;
  turbo-q4)
    WANT_TURBO_Q4=1
    ;;
  turbo-q6)
    WANT_TURBO_Q6=1
    ;;
  turbo-q8)
    WANT_TURBO_Q8=1
    ;;
  3.8)
    WANT_38=1
    ;;
  3.5)
    WANT_35=1
    ;;
  none)
    WANT_35=0
    WANT_38=0
    WANT_TURBO_Q4=0
    WANT_TURBO_Q6=0
    WANT_TURBO_Q8=0
    ;;
  auto)
    WANT_35=1
    if (( TOTAL_RAM_MIB >= 15000 )); then
      WANT_38=1
    else
      printf '  -> Host has %d MiB RAM (< 16 GiB): defaulting to Qwen3.5-9B (pass --all-models to force Qwen3.8-27B).\n' "$TOTAL_RAM_MIB"
    fi
    # Auto-select Qwen3.8-27B Turbo MTP models where balanced for both GPU VRAM and host RAM
    if (( TOTAL_VRAM_MIB >= 16000 || (TOTAL_RAM_MIB >= 32000 && TOTAL_VRAM_MIB >= 12000) )); then
      WANT_TURBO_Q4=1
    fi
    if (( TOTAL_VRAM_MIB >= 24000 || (TOTAL_RAM_MIB >= 48000 && TOTAL_VRAM_MIB >= 16000) )); then
      WANT_TURBO_Q6=1
    fi
    if (( TOTAL_VRAM_MIB >= 32000 || (TOTAL_RAM_MIB >= 64000 && TOTAL_VRAM_MIB >= 24000) )); then
      WANT_TURBO_Q8=1
    fi
    ;;
esac

download_model() {
  local name="$1"
  local url="$2"
  local dest="$3"
  local min_bytes="$4"

  if [[ -f "$dest" ]]; then
    local actual_bytes
    actual_bytes=$(stat -Lc%s "$dest" 2>/dev/null || echo 0)
    if (( actual_bytes >= min_bytes )); then
      printf '  -> %s already downloaded (%d MiB).\n' "$name" "$(( actual_bytes / 1048576 ))"
      return 0
    fi
    printf '  -> %s is incomplete (%d MiB); resuming download...\n' "$name" "$(( actual_bytes / 1048576 ))"
  else
    local avail_mb
    avail_mb=$(df -Pm "$CORA_ROOT/models" | awk 'NR==2 {print $4}' 2>/dev/null || echo 999999)
    local needed_mb=$(( min_bytes / 1048576 + 512 ))
    if (( avail_mb < needed_mb )); then
      printf 'Error: Insufficient disk space in %s/models (%d MiB free, need at least %d MiB for %s).\n' \
        "$CORA_ROOT" "$avail_mb" "$needed_mb" "$name" >&2
      exit 1
    fi
    printf '  -> Downloading %s ...\n' "$name"
  fi

  if command -v wget >/dev/null 2>&1; then
    wget -c --tries=5 --timeout=30 --progress=bar:force:noscroll -O "$dest" "$url"
  else
    curl -fL --retry 5 --retry-delay 3 -C - -o "$dest" "$url"
  fi

  local final_bytes
  final_bytes=$(stat -Lc%s "$dest" 2>/dev/null || echo 0)
  if (( final_bytes < min_bytes )); then
    printf 'Error: Downloaded file %s is smaller than expected (%d bytes < %d bytes). Re-run ./setup_cora_NIX.sh to resume.\n' \
      "$dest" "$final_bytes" "$min_bytes" >&2
    exit 1
  fi
}

if (( WANT_35 == 1 )); then
  download_model "Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.24 GiB)" \
    "$QWEN35_URL" "$CORA_ROOT/models/$QWEN35_FILE" "$QWEN35_MIN_BYTES"
  ln -sf "$QWEN35_FILE" "$CORA_ROOT/models/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
fi

if (( WANT_38 == 1 )); then
  download_model "Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.40 GiB)" \
    "$QWEN38_URL" "$CORA_ROOT/models/$QWEN38_FILE" "$QWEN38_MIN_BYTES"
fi

if (( WANT_TURBO_Q4 == 1 )); then
  download_model "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB Multiple Token Prediction)" \
    "$QWEN38_TURBO_Q4_URL" "$CORA_ROOT/models/$QWEN38_TURBO_Q4_FILE" "$QWEN38_TURBO_Q4_MIN_BYTES"
  ln -sf "$QWEN38_TURBO_Q4_FILE" "$CORA_ROOT/models/$QWEN38_TURBO_Q4_HF_FILE"
fi

if (( WANT_TURBO_Q6 == 1 )); then
  download_model "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.38 GiB Multiple Token Prediction)" \
    "$QWEN38_TURBO_Q6_URL" "$CORA_ROOT/models/$QWEN38_TURBO_Q6_FILE" "$QWEN38_TURBO_Q6_MIN_BYTES"
  ln -sf "$QWEN38_TURBO_Q6_FILE" "$CORA_ROOT/models/$QWEN38_TURBO_Q6_HF_FILE"
fi

if (( WANT_TURBO_Q8 == 1 )); then
  download_model "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.16 GiB Multiple Token Prediction)" \
    "$QWEN38_TURBO_Q8_URL" "$CORA_ROOT/models/$QWEN38_TURBO_Q8_FILE" "$QWEN38_TURBO_Q8_MIN_BYTES"
  ln -sf "$QWEN38_TURBO_Q8_FILE" "$CORA_ROOT/models/$QWEN38_TURBO_Q8_HF_FILE"
fi

# 4. Run ConsolePostureDetection_NIX.sh
if [[ -f "$BASE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" ]]; then
  printf '\n[Step 4/7] Detecting active console security posture...\n'
  bash "$BASE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" --detect || true
fi

# 5. Run 15-Engine Neuro-Symbolic Reasoning Suite Installer
if (( SETUP_REASONING == 1 )) && [[ -f "$BASE_DIR/Reasoning/install_reasoning_NIX.sh" ]]; then
  printf '\n[Step 5/7] Verifying system compatibility and setting up the 15-Engine Neuro-Symbolic, RL & Spectral PCA/K-Means++ Reasoning Suite (v4.5.0-15Engine-Core)...\n'
  if (( OFFLINE == 1 )); then
    bash "$BASE_DIR/Reasoning/install_reasoning_NIX.sh" --offline
  else
    bash "$BASE_DIR/Reasoning/install_reasoning_NIX.sh" --all
  fi
fi

# 6. Verify Multi-Modal Training & CPU Neural OCR Modules
if (( OFFLINE == 0 )) && [[ -f "$CORA_ROOT/Training/train_llm_NIX.sh" ]]; then
  printf '\n[Step 6/7] Verifying Multi-Modal (PDF/DOCX/HTML/SVG) & CPU Neural OCR modules...\n'
  bash "$CORA_ROOT/Training/train_llm_NIX.sh" --check-deps || true
fi

# 7. Run Quick Troubleshooting Verification
if (( SKIP_TESTS == 0 )) && [[ -f "$CORA_ROOT/Troubleshooting/troubleshoot_llm_NIX.sh" ]]; then
  printf '\n[Step 7/7] Verifying All 8 Layers, 15 Engines & 10 Guardrails...\n'
  bash "$CORA_ROOT/Troubleshooting/troubleshoot_llm_NIX.sh" --quick
fi

printf '\nSetup complete! Verifying installed models and hardware profile:\n\n'
"$CORA_ROOT/run_cora_NIX.sh" models
printf '\n'
"$CORA_ROOT/run_cora_NIX.sh" tune
printf '\nQuick Start Commands (Bash in %s):\n' "$CORA_ROOT"
printf '  ./run_cora_NIX.sh webui                                      # Launch C.O.R.A. WebUI + local llama-server (http://127.0.0.1:1337)\n'
printf '  ./run_cora_NIX.sh cli                                        # Launch interactive C.O.R.A. CLI (Default 3.8 27B)\n'
printf '  ./run_cora_NIX.sh cli -m 3.5 --dangerously-skip-permissions  # Launch fast Qwen3.5-9B Agent CLI (Auto-run)\n'
printf '  ./run_cora_NIX.sh cli -m turbo --dangerously-skip-permissions # Launch Qwen3.8-27B Turbo MTP Q4_K_M Agent CLI\n'
printf '  ./run_cora_NIX.sh start                                      # Start background llama-server + Custom CORA WebUI (port 1337)\n'
printf '  ./run_cora_NIX.sh -train                                     # Distill & OCR ./Training/\n'
printf '  ./run_cora_NIX.sh status                                     # Check server & GPU VRAM status\n'
