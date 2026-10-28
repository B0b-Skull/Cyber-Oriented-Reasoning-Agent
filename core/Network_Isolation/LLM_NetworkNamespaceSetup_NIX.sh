#!/usr/bin/env bash
# ==============================================================================
# LLM_NetworkNamespaceSetup_NIX.sh — Air-Gapped Linux Network Namespace for CORA
# ==============================================================================
# Creates and manages a dedicated Linux Network Namespace (`llm-isolated`) that
# contains ONLY a private virtual loopback adapter (`lo` -> 127.0.0.1).
#
# Inside this namespace:
#   - No Ethernet, Wi-Fi, WAN, or VPN network interfaces exist.
#   - No default gateway or external routing table exists.
#   - `llama-server` and `agent-cli.py` communicate normally over 127.0.0.1:8080.
#   - Full access to local files, ObsidianVault, CPU, NVIDIA GPU (/dev/nvidia*),
#     and local USB serial devices (/dev/ttyUSB*, /dev/tty/usb*) is preserved.
#   - Any outbound internet connection attempt immediately fails with:
#     "Network is unreachable".
#
# ------------------------------------------------------------------------------
# SWITCHES & OPTIONS:
#   --setup, setup       Create the persistent `llm-isolated` network namespace
#                        and bring up its internal loopback (`lo` 127.0.0.1)
#                        interface with zero external network interfaces.
#
#   --remove, remove     Terminate any processes still running inside
#                        `llm-isolated` and delete the network namespace.
#
#   --status, status     Show whether `llm-isolated` is active, inspect its
#                        interfaces/routes, and list any processes inside it.
#
#   --run, run <cmd...>  Execute a command (such as `./run_cora_NIX.sh cli -m 3.5`)
#                        inside the air-gapped `llm-isolated` namespace as your
#                        normal user account.
#
#   --unshare <cmd...>   Run a command in an ephemeral rootless network namespace
#                        (`unshare -r -n`) without requiring sudo or prior setup.
#
#   -h, --help, help     Show this header documentation and exit.
#
# ------------------------------------------------------------------------------
# EXAMPLES:
#   1. Create and initialize the `llm-isolated` network namespace:
#        sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --setup
#
#   2. Check namespace status, interfaces, and running processes:
#        sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --status
#
#   3. Run the CORA Agent CLI inside the air-gapped namespace:
#        sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.5
#        sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.8 --dangerously-skip-permissions
#
#   4. Verify that external internet access is completely unreachable:
#        sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --run curl -I https://1.1.1.1
#        (Output: curl: (7) Failed to connect to 1.1.1.1 port 443: Network is unreachable)
#
#   5. Tear down and remove the `llm-isolated` network namespace:
#        sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --remove
# ==============================================================================
set -euo pipefail

NS_NAME="llm-isolated"
TARGET_USER="${SUDO_USER:-$USER}"
BASE_DIR=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)

show_help() {
  sed -n '2,57p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

require_root() {
  if [[ $EUID -ne 0 ]]; then
    printf 'Re-running with sudo for Linux network namespace management...\n'
    exec sudo -E bash "${BASH_SOURCE[0]}" "$@"
  fi
}

ns_exists() {
  ip netns list 2>/dev/null | awk '{print $1}' | grep -qx "$NS_NAME"
}

setup_namespace() {
  require_root "--setup"

  printf '=== Setting Up Air-Gapped Linux Network Namespace (%s) ===\n' "$NS_NAME"
  if ns_exists; then
    printf '  [=] Network namespace "%s" already exists.\n' "$NS_NAME"
  else
    ip netns add "$NS_NAME"
    printf '  [+] Created network namespace: %s\n' "$NS_NAME"
  fi

  # Bring up only the internal loopback interface (127.0.0.1 / ::1)
  ip netns exec "$NS_NAME" ip link set dev lo up
  printf '  [+] Activated internal loopback (lo -> 127.0.0.1) inside %s\n' "$NS_NAME"
  printf '  [+] External interfaces inside %s: NONE (100%% internet air-gap)\n' "$NS_NAME"
  printf '====================================================================\n'
  printf 'Namespace ready! Launch CORA inside "%s" with:\n' "$NS_NAME"
  printf '  sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.5\n'
}

remove_namespace() {
  require_root "--remove"

  printf '=== Removing Linux Network Namespace (%s) ===\n' "$NS_NAME"
  if ! ns_exists; then
    printf '  [=] Namespace "%s" is not present.\n' "$NS_NAME"
    return 0
  fi

  # Stop any processes still running inside the namespace
  local pids
  pids=$(ip netns pids "$NS_NAME" 2>/dev/null || true)
  if [[ -n "$pids" ]]; then
    printf '  [-] Stopping processes inside %s: %s\n' "$NS_NAME" "$(echo "$pids" | tr '\n' ' ')"
    echo "$pids" | xargs -r kill 2>/dev/null || true
    sleep 1
    echo "$pids" | xargs -r kill -9 2>/dev/null || true
  fi

  ip netns delete "$NS_NAME"
  printf '  [-] Deleted network namespace: %s\n' "$NS_NAME"
  printf '=========================================================\n'
}

status_namespace() {
  printf '=== Linux Network Namespace (%s) Status ===\n' "$NS_NAME"
  if ! ns_exists; then
    printf '  Status: STOPPED / NOT CREATED\n'
    printf '  (Run "sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --setup" to create it)\n'
    printf '=====================================================\n'
    return 0
  fi

  printf '  Status: ACTIVE\n\n'
  if [[ $EUID -eq 0 ]]; then
    printf '  Interfaces inside %s:\n' "$NS_NAME"
    ip netns exec "$NS_NAME" ip -br addr | sed 's/^/    /'
    printf '\n  Routing table inside %s:\n' "$NS_NAME"
    local routes
    routes=$(ip netns exec "$NS_NAME" ip route 2>/dev/null || true)
    if [[ -n "$routes" ]]; then
      printf '%s\n' "$routes" | sed 's/^/    /'
    else
      printf '    (empty — no external routes, internet unreachable)\n'
    fi
    printf '\n  Processes running inside %s:\n' "$NS_NAME"
    local pids
    pids=$(ip netns pids "$NS_NAME" 2>/dev/null || true)
    if [[ -n "$pids" ]]; then
      ps -o pid,user,comm,args -p $(echo "$pids" | tr '\n' ',') | sed 's/^/    /'
    else
      printf '    (none)\n'
    fi
  else
    printf '  (Run "sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --status" to view internal interfaces & PIDs)\n'
  fi
  printf '=====================================================\n'
}

run_in_namespace() {
  if [[ $# -eq 0 ]]; then
    printf 'Error: --run requires a command (e.g. sudo ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.5)\n' >&2
    exit 2
  fi
  require_root "--run" "$@"

  if ! ns_exists; then
    setup_namespace
  fi

  export LLM_ISOLATION_MODE="airgap"
  local script_dir
  script_dir=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
  if [[ -x "$script_dir/ConsolePostureDetection_NIX.sh" ]]; then
    bash "$script_dir/ConsolePostureDetection_NIX.sh" --apply airgap --quiet || true
  fi

  exec ip netns exec "$NS_NAME" sudo -E -u "$TARGET_USER" \
    env PATH="$PATH" HOME="$(eval echo "~$TARGET_USER")" USER="$TARGET_USER" LLM_ISOLATION_MODE="airgap" \
    "$@"
}

run_unshare() {
  if [[ $# -eq 0 ]]; then
    printf 'Error: --unshare requires a command (e.g. ./core/Network_Isolation/LLM_NetworkNamespaceSetup_NIX.sh --unshare ./run_cora_NIX.sh cli -m 3.5)\n' >&2
    exit 2
  fi
  export LLM_ISOLATION_MODE="airgap"
  local script_dir
  script_dir=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
  if [[ -x "$script_dir/ConsolePostureDetection_NIX.sh" ]]; then
    bash "$script_dir/ConsolePostureDetection_NIX.sh" --apply airgap --quiet || true
  fi
  local quoted_cmd
  printf -v quoted_cmd '%q ' "$@"
  exec unshare -r -n bash -c "export LLM_ISOLATION_MODE=airgap; ip link set dev lo up && exec $quoted_cmd"
}

case "${1:---help}" in
  --setup|setup)
    setup_namespace
    ;;
  --remove|remove|--teardown|teardown)
    remove_namespace
    ;;
  --status|status)
    status_namespace
    ;;
  --run|run)
    shift
    run_in_namespace "$@"
    ;;
  --unshare|unshare)
    shift
    run_unshare "$@"
    ;;
  -h|--help|help)
    show_help
    ;;
  *)
    printf 'Unknown switch: %s\n\n' "$1" >&2
    show_help >&2
    exit 2
    ;;
esac
