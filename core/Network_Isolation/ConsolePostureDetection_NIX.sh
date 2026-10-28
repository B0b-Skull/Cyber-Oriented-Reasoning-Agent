#!/usr/bin/env bash
# ==============================================================================
# ConsolePostureDetection_NIX.sh — Linux Console Posture Detection & Theme Controller
# ==============================================================================
# Automatically detects the active kernel network isolation posture and tints
# the current terminal window in-place (without opening a separate window):
#
#   1. RED / UNRESTRICTED (`./run_cora_NIX.sh cli -netiso red` or default)
#      - Background: Deep Tactical Crimson (#1C0A0D) | Font: #FFE8E8
#      - Badge:      NET:RED(FULL-ACCESS)
#
#   2. WHITE / AIR_GAPPED_NETNS (`./run_cora_NIX.sh cli -netiso white` or `LLM_NetworkNamespaceSetup_NIX.sh`)
#      - Background: Deep Tactical Slate (#141820) | Font: Pure White (#FFFFFF)
#      - Badge:      NET:WHITE-NETNS(lo-only)
#
#   3. BLUE / ISOLATED_LAN_USB (`./run_cora_NIX.sh cli -netiso blue [ifaces]` or `LLM_NetworkIsolationSetup_NIX.sh`)
#      - Background: Deep Cyber Navy Blue (#081426) | Font: #E0F4FF
#      - Badge:      NET:BLUE(<allowed_ifaces>)
#
# Usage:
#   bash core/Network_Isolation/ConsolePostureDetection_NIX.sh                 # Auto-detect & apply in-place
#   bash core/Network_Isolation/ConsolePostureDetection_NIX.sh --apply blue    # Force Blue Interface-Locked theme
#   bash core/Network_Isolation/ConsolePostureDetection_NIX.sh --apply white   # Force White Namespace theme
#   bash core/Network_Isolation/ConsolePostureDetection_NIX.sh --apply red     # Force Red Unrestricted theme
#   bash core/Network_Isolation/ConsolePostureDetection_NIX.sh --demo          # Cycle through all 3 themes
#   bash core/Network_Isolation/ConsolePostureDetection_NIX.sh --reset         # Restore default terminal colors
#   bash core/Network_Isolation/ConsolePostureDetection_NIX.sh --json          # Emit JSON posture summary
# ==============================================================================
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
if [[ "$(basename "$SCRIPT_DIR")" == "Network_Isolation" ]]; then
  BASE_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd -P)
else
  BASE_DIR="$SCRIPT_DIR"
fi

POSTURE_PY="$BASE_DIR/Network_Isolation/console_posture.py"
mkdir -p "$BASE_DIR/Log"
chmod 775 "$BASE_DIR/Log" 2>/dev/null || true

if [[ -x "$BASE_DIR/Reasoning/.venv/bin/python" ]]; then
  PY_BIN="$BASE_DIR/Reasoning/.venv/bin/python"
else
  PY_BIN="python3"
fi

exec "$PY_BIN" "$POSTURE_PY" "$@"
