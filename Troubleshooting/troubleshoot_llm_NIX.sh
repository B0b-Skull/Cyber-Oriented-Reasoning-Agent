#!/usr/bin/env bash
# ==============================================================================
# Linux Troubleshooting & Layered Reasoning Fault-Isolation Script for CORA
# (`Troubleshooting/troubleshoot_llm_NIX.sh` — `v3.6.1`)
#
# Identifies areas of concern across:
#   - Host CPU / RAM / GPU VRAM / Disk / Serial (`/dev/ttyUSB*`) permissions
#   - `llama-server` process, port 8080, `/health`, `/props`, and `core/Log/llama-server.log`
#   - Layer A: Bytecode & syntax integrity of `agent-cli.py` and `core/Reasoning/`
#   - Layer B: JSON state file corruption & stale Event-Calculus fluents (`live_fluents.json`)
#   - Layer C: All 10 Guardrails (including Uncapped Cross-Platform CLI Extractor & H-MDP Solver)
#   - Layer D: Isolated execution & latency benchmark of all 15 Reasoning Engines
#   - Layer E: Interactive command interception tracer & Consensus Arbiter explainer
#
# Usage:
#   bash Troubleshooting/troubleshoot_llm_NIX.sh                              # Full diagnostic audit
#   bash Troubleshooting/troubleshoot_llm_NIX.sh --fix                        # Auto-repair corrupted JSONs & clear stale fluents
#   bash Troubleshooting/troubleshoot_llm_NIX.sh --diagnose-cmd "tio /dev/ttyUSB0"
#   bash Troubleshooting/troubleshoot_llm_NIX.sh --explain-arbiter "curl exit 7 on target API endpoint"
#   bash Troubleshooting/troubleshoot_llm_NIX.sh --json                       # Include JSON report
# ==============================================================================
set -Eeuo pipefail

TROUBLESHOOT_DIR=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
CORA_ROOT=$(dirname "$TROUBLESHOOT_DIR")
CORA_CORE_DIR="$CORA_ROOT/core"
CORE_PY="$TROUBLESHOOT_DIR/troubleshoot_core.py"

chmod +x "$CORE_PY" "$TROUBLESHOOT_DIR/troubleshoot_llm_NIX.sh" 2>/dev/null || true

printf '\033[1;34m==============================================================================\033[0m\n'
printf '\033[1;37m  PRE-FLIGHT LINUX OS, GPU, SERIAL & PROCESS CHECK (C.O.R.A.)\033[0m\n'
printf '\033[1;34m==============================================================================\033[0m\n'

# 1. Check Bash syntax of run_cora_NIX.sh, setup_cora_NIX.sh, train_llm_NIX.sh, install_reasoning_NIX.sh, and Network_Isolation/*_NIX.sh
for sh_file in "$CORA_ROOT/run_cora_NIX.sh" "$CORA_ROOT/setup_cora_NIX.sh" "$CORA_ROOT/Training/train_llm_NIX.sh" "$CORA_CORE_DIR/Reasoning/install_reasoning_NIX.sh" "$CORA_CORE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" "$CORA_CORE_DIR/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh" "$CORA_CORE_DIR/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh"; do
  if [[ -f "$sh_file" ]]; then
    if bash -n "$sh_file" 2>/dev/null; then
      printf '  \033[1;32m[OK]\033[0m      Bash syntax verified: `%s`\n' "$(basename "$sh_file")"
    else
      printf '  \033[1;31m[FAULT]\033[0m   Bash syntax error in: `%s`\n' "$sh_file"
    fi
  fi
done

# 2. Check RAM & Swap pressure
if [[ -f /proc/meminfo ]]; then
  MEM_TOTAL_MIB=$(awk '/MemTotal:/ {printf "%d", $2/1024}' /proc/meminfo)
  MEM_AVAIL_MIB=$(awk '/MemAvailable:/ {printf "%d", $2/1024}' /proc/meminfo)
  MEM_USED_PCT=$(( (MEM_TOTAL_MIB - MEM_AVAIL_MIB) * 100 / (MEM_TOTAL_MIB > 0 ? MEM_TOTAL_MIB : 1) ))
  if (( MEM_USED_PCT >= 90 )); then
    printf '  \033[1;33m[CONCERN]\033[0m System RAM usage is high: %d%% used (%d MiB available of %d MiB)\n' "$MEM_USED_PCT" "$MEM_AVAIL_MIB" "$MEM_TOTAL_MIB"
  else
    printf '  \033[1;32m[OK]\033[0m      System RAM healthy: %d%% used (%d MiB available of %d MiB)\n' "$MEM_USED_PCT" "$MEM_AVAIL_MIB" "$MEM_TOTAL_MIB"
  fi
fi

# 3. Check NVIDIA GPU VRAM & Temperature
if command -v nvidia-smi >/dev/null 2>&1; then
  GPU_LINE=$(nvidia-smi --query-gpu=name,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits 2>/dev/null | head -n1 || true)
  if [[ -n "$GPU_LINE" ]]; then
    G_NAME=$(printf '%s' "$GPU_LINE" | awk -F', ' '{print $1}')
    G_USED=$(printf '%s' "$GPU_LINE" | awk -F', ' '{print int($2)}')
    G_TOTAL=$(printf '%s' "$GPU_LINE" | awk -F', ' '{print int($3)}')
    G_TEMP=$(printf '%s' "$GPU_LINE" | awk -F', ' '{print int($4)}')
    G_PCT=$(( G_USED * 100 / (G_TOTAL > 0 ? G_TOTAL : 1) ))
    printf '  \033[1;32m[OK]\033[0m      GPU Detected: %s | VRAM: %d / %d MiB (%d%%) | Temp: %dC\n' "$G_NAME" "$G_USED" "$G_TOTAL" "$G_PCT" "$G_TEMP"
  fi
else
  printf '  \033[1;36m[INFO]\033[0m    No `nvidia-smi` binary found (CPU-only mode).\n'
fi

# 4. Check Serial `/dev/ttyUSB*` / `dialout` group permissions if serial device exists
shopt -s nullglob
SERIAL_DEVS=(/dev/ttyUSB* /dev/ttyACM*)
shopt -u nullglob
if (( ${#SERIAL_DEVS[@]} > 0 )); then
  for sdev in "${SERIAL_DEVS[@]}"; do
    if [[ -r "$sdev" && -w "$sdev" ]]; then
      printf '  \033[1;32m[OK]\033[0m      Serial device `%s` is readable & writable by current user.\n' "$sdev"
    else
      printf '  \033[1;33m[CONCERN]\033[0m Serial device `%s` exists but lacks read/write permission (Fix: `sudo usermod -aG dialout $USER`).\n' "$sdev"
    fi
  done
fi

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOT'

Usage: bash Troubleshooting/troubleshoot_llm_NIX.sh [OPTIONS]

Options:
  (no args)                            Run full 5-layer diagnostic & 15-engine + 10-guardrail isolation audit
  --fix / --auto-repair                Automatically fix corrupted JSON stores, clear stale fluents & re-seed
  --diagnose-cmd "<bash_cmd>"          Trace how a command flows through CEGAR -> CBR -> SyGuS -> Context VM
  --sim-output "<text>"                Simulated command output for --diagnose-cmd
  --sim-exit <code_int>                Simulated exit code for --diagnose-cmd
  --explain-arbiter "<problem_text>"   Explain why the 15-Engine Consensus Arbiter chose its action
  --json                               Append a machine-readable JSON diagnostic summary
EOT
  exit 0
fi

exec python3 "$CORE_PY" "$@"
