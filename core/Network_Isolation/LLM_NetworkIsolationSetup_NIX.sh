#!/usr/bin/env bash
# ==============================================================================
# LLM_NetworkIsolationSetup_NIX.sh — Group-Based Firewall & USB Console Isolation
# ==============================================================================
# Isolates the CORA server and Agent CLI using Linux Group-Based Firewalling
# (iptables / ip6tables owner module) and udev/ACL device rules so that processes
# running under the `llm-local` group can ONLY communicate over:
#   - Loopback:     lo (127.0.0.1 / ::1 for local llama-server <-> CLI/WebUI)
#   - Lab Ethernet: eth0, eth1, eth2
#   - USB Consoles: /dev/tty/usb0, /dev/tty/usb1 (and /dev/ttyUSB0, /dev/ttyUSB1)
# All other interfaces (Wi-Fi wlan0/wlp*, WAN uplinks, VPNs, broader internet)
# are strictly blocked at the Linux kernel packet filter level.
#
# ------------------------------------------------------------------------------
# SWITCHES & OPTIONS:
#   --setup, setup       Create the `llm-local` group, add current user to
#                        `llm-local` & `dialout`, configure USB serial console
#                        permissions/udev rules (/dev/tty/usb0 & /dev/tty/usb1),
#                        and apply iptables/ip6tables OUTPUT rules restricting
#                        `llm-local` to lo, eth0, eth1, and eth2.
#
#   --remove, remove     Remove all `LLM_ISOLATION` iptables/ip6tables firewall
#                        rules and remove the USB console udev rule.
#
#   --status, status     Display current `llm-local` group membership, active
#                        `LLM_ISOLATION` firewall rules, and USB console device
#                        status.
#
#   --run, run <cmd...>  Execute a command (such as `./run_cora_NIX.sh cli` or
#                        `./run_cora_NIX.sh start`) inside the `llm-local` group
#                        so all LLM and child shell processes are bound by the
#                        firewall isolation rules.
#
#   -h, --help, help     Show this header documentation and exit.
#
# ------------------------------------------------------------------------------
# EXAMPLES:
#   1. Apply Group-Based Firewall & USB Console isolation (requires sudo):
#        sudo ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --setup
#
#   2. Check active firewall isolation rules and USB console permissions:
#        sudo ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --status
#
#   3. Launch the CORA Agent CLI inside the isolated `llm-local` group:
#        ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.5
#        ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.8 --dangerously-skip-permissions
#
#   4. Test that internet access is blocked while local eth0/1/2 & lo work:
#        ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --run curl -I https://1.1.1.1
#        (Returns: curl: (7) Failed to connect ... Network is unreachable / Connection refused)
#
#   5. Remove all isolation firewall rules and restore normal access:
#        sudo ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --remove
# ==============================================================================
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
CONF_FILE="$SCRIPT_DIR/network_isolation.conf"
BLUE_ALLOWED_IFACES="eth0,eth1"
BLUE_USB_DEVICES="/dev/ttyUSB0,/dev/ttyUSB1"
if [[ -f "$CONF_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$CONF_FILE"
fi
if [[ -n "${LLM_ALLOWED_IFACES:-}" ]]; then
  BLUE_ALLOWED_IFACES="$LLM_ALLOWED_IFACES"
fi

LLM_GROUP="llm-local"
CHAIN_NAME="LLM_ISOLATION"
ALLOWED_IFACES=("lo")
USB_DEVICES=()

rebuild_iface_and_usb_arrays() {
  local raw_csv="${1:-$BLUE_ALLOWED_IFACES}"
  ALLOWED_IFACES=("lo")
  local item
  IFS=', ' read -r -a _parsed_ifaces <<< "$raw_csv"
  for item in "${_parsed_ifaces[@]}"; do
    item="${item//,/}"
    if [[ -n "$item" && "$item" != "lo" ]]; then
      ALLOWED_IFACES+=("$item")
    fi
  done
  local clean_non_lo=()
  local x
  for x in "${ALLOWED_IFACES[@]}"; do
    [[ "$x" != "lo" ]] && clean_non_lo+=("$x")
  done
  BLUE_ALLOWED_IFACES=$(IFS=,; echo "${clean_non_lo[*]}")

  USB_DEVICES=()
  IFS=', ' read -r -a _parsed_usb <<< "${BLUE_USB_DEVICES:-/dev/ttyUSB0,/dev/ttyUSB1}"
  for item in "${_parsed_usb[@]}"; do
    item="${item//,/}"
    [[ -n "$item" ]] && USB_DEVICES+=("$item")
  done
}

rebuild_iface_and_usb_arrays "$BLUE_ALLOWED_IFACES"
UDEV_RULE_FILE="/etc/udev/rules.d/99-llm-usb-console.rules"
TARGET_USER="${SUDO_USER:-$USER}"

show_help() {
  sed -n '2,55p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

require_root() {
  if [[ $EUID -ne 0 ]]; then
    printf 'Re-running with sudo for kernel firewall / group configuration...\n'
    exec sudo -E bash "${BASH_SOURCE[0]}" "$@"
  fi
}

setup_isolation() {
  if [[ "${1:-}" == "--ifaces" && -n "${2:-}" ]]; then
    rebuild_iface_and_usb_arrays "$2"
  fi
  require_root "--setup" "--ifaces" "$BLUE_ALLOWED_IFACES"

  printf '=== Setting Up CORA Group-Based Firewall & USB Isolation ===\n'

  # 1. Create dedicated group and add user
  if ! getent group "$LLM_GROUP" >/dev/null 2>&1; then
    groupadd -f "$LLM_GROUP"
    printf '  [+] Created group: %s\n' "$LLM_GROUP"
  else
    printf '  [=] Group already exists: %s\n' "$LLM_GROUP"
  fi

  usermod -aG "$LLM_GROUP" "$TARGET_USER"
  if getent group dialout >/dev/null 2>&1; then
    usermod -aG dialout "$TARGET_USER"
  fi
  printf '  [+] Added user "%s" to group "%s" (and "dialout")\n' "$TARGET_USER" "$LLM_GROUP"

  # 2. Configure USB Console permissions & udev rules (/dev/ttyUSB0, /dev/ttyUSB1)
  for dev in "${USB_DEVICES[@]}"; do
    if [[ -e "$dev" ]]; then
      chgrp "$LLM_GROUP" "$dev" 2>/dev/null || true
      chmod 0660 "$dev" 2>/dev/null || true
      if command -v setfacl >/dev/null 2>&1; then
        setfacl -m "g:${LLM_GROUP}:rw" "$dev" 2>/dev/null || true
        setfacl -m "u:${TARGET_USER}:rw" "$dev" 2>/dev/null || true
      fi
      printf '  [+] Granted %s & %s read/write access on USB console: %s\n' "$LLM_GROUP" "$TARGET_USER" "$dev"
    fi
  done

  cat <<EOF > "$UDEV_RULE_FILE"
# Grant llm-local group read/write access to USB serial consoles
KERNEL=="ttyUSB[01]", GROUP="${LLM_GROUP}", MODE="0666"
EOF
  if command -v udevadm >/dev/null 2>&1; then
    udevadm control --reload-rules 2>/dev/null || true
    udevadm trigger --subsystem-match=tty 2>/dev/null || true
  fi
  printf '  [+] Installed persistent udev rule: %s\n' "$UDEV_RULE_FILE"

  # 3. Apply IPv4 iptables rules for group llm-local
  iptables -D OUTPUT -m owner --gid-owner "$LLM_GROUP" -j "$CHAIN_NAME" 2>/dev/null || true
  iptables -F "$CHAIN_NAME" 2>/dev/null || iptables -N "$CHAIN_NAME"

  for iface in "${ALLOWED_IFACES[@]}"; do
    iptables -A "$CHAIN_NAME" -o "$iface" -j ACCEPT
  done
  iptables -A "$CHAIN_NAME" -j REJECT --reject-with icmp-net-unreachable
  iptables -I OUTPUT 1 -m owner --gid-owner "$LLM_GROUP" -j "$CHAIN_NAME"
  printf '  [+] Applied IPv4 iptables OUTPUT rules (Allowed: %s | Blocked: all other interfaces)\n' "${ALLOWED_IFACES[*]}"

  # 4. Apply IPv6 ip6tables rules for group llm-local
  if command -v ip6tables >/dev/null 2>&1; then
    ip6tables -D OUTPUT -m owner --gid-owner "$LLM_GROUP" -j "$CHAIN_NAME" 2>/dev/null || true
    ip6tables -F "$CHAIN_NAME" 2>/dev/null || ip6tables -N "$CHAIN_NAME"

    for iface in "${ALLOWED_IFACES[@]}"; do
      ip6tables -A "$CHAIN_NAME" -o "$iface" -j ACCEPT
    done
    ip6tables -A "$CHAIN_NAME" -j REJECT --reject-with icmp6-no-route
    ip6tables -I OUTPUT 1 -m owner --gid-owner "$LLM_GROUP" -j "$CHAIN_NAME"
    printf '  [+] Applied IPv6 ip6tables OUTPUT rules (Allowed: %s | Blocked: all other interfaces)\n' "${ALLOWED_IFACES[*]}"
  fi

  printf '================================================================\n'
  printf 'Setup complete! Run CORA inside the isolated group with:\n'
  printf '  ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.5\n'
}

remove_isolation() {
  require_root "--remove"

  printf '=== Removing CORA Group-Based Firewall & USB Isolation ===\n'

  while iptables -D OUTPUT -m owner --gid-owner "$LLM_GROUP" -j "$CHAIN_NAME" 2>/dev/null; do :; done
  iptables -F "$CHAIN_NAME" 2>/dev/null || true
  iptables -X "$CHAIN_NAME" 2>/dev/null || true
  printf '  [-] Removed IPv4 iptables chain: %s\n' "$CHAIN_NAME"

  if command -v ip6tables >/dev/null 2>&1; then
    while ip6tables -D OUTPUT -m owner --gid-owner "$LLM_GROUP" -j "$CHAIN_NAME" 2>/dev/null; do :; done
    ip6tables -F "$CHAIN_NAME" 2>/dev/null || true
    ip6tables -X "$CHAIN_NAME" 2>/dev/null || true
    printf '  [-] Removed IPv6 ip6tables chain: %s\n' "$CHAIN_NAME"
  fi

  if [[ -f "$UDEV_RULE_FILE" ]]; then
    rm -f "$UDEV_RULE_FILE"
    if command -v udevadm >/dev/null 2>&1; then
      udevadm control --reload-rules 2>/dev/null || true
    fi
    printf '  [-] Removed udev rule: %s\n' "$UDEV_RULE_FILE"
  fi

  printf '==============================================================\n'
  printf 'Isolation rules removed.\n'
}

status_isolation() {
  printf '=== CORA Group-Based Firewall Isolation Status ===\n'
  if getent group "$LLM_GROUP" >/dev/null 2>&1; then
    printf '  Group (%s): PRESENT (%s)\n' "$LLM_GROUP" "$(getent group "$LLM_GROUP")"
  else
    printf '  Group (%s): NOT CREATED\n' "$LLM_GROUP"
  fi

  printf '\n  USB Console Devices:\n'
  for dev in "${USB_DEVICES[@]}"; do
    if [[ -e "$dev" ]]; then
      printf '    [PRESENT] %s -> %s\n' "$dev" "$(ls -l "$dev")"
    else
      printf '    [ABSENT]  %s (will be auto-configured by udev when plugged in)\n' "$dev"
    fi
  done

  printf '\n  IPv4 Firewall Rules (%s):\n' "$CHAIN_NAME"
  if sudo -n iptables -L "$CHAIN_NAME" -n -v 2>/dev/null; then
    :
  elif [[ $EUID -eq 0 ]]; then
    iptables -L "$CHAIN_NAME" -n -v 2>/dev/null || printf '    (Chain %s is not active)\n' "$CHAIN_NAME"
  else
    printf '    (Run "sudo ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --status" to inspect kernel iptables counters)\n'
  fi
  printf '======================================================\n'
}

run_in_isolated_group() {
  if [[ "${1:-}" == "--ifaces" && $# -ge 2 ]]; then
    rebuild_iface_and_usb_arrays "$2"
    shift 2
  fi
  if [[ $# -eq 0 ]]; then
    printf 'Error: --run requires a command (e.g. ./core/Network_Isolation/LLM_NetworkIsolationSetup_NIX.sh --run ./run_cora_NIX.sh cli -m 3.8)\n' >&2
    exit 2
  fi
  export LLM_ISOLATION_MODE="blue"
  export LLM_ALLOWED_IFACES="$BLUE_ALLOWED_IFACES"
  if [[ -x "$SCRIPT_DIR/ConsolePostureDetection_NIX.sh" ]]; then
    bash "$SCRIPT_DIR/ConsolePostureDetection_NIX.sh" --apply blue --quiet || true
  fi
  # If passwordless sudo is available, ensure kernel iptables chain matches the requested BLUE interfaces
  if [[ $EUID -eq 0 ]] || sudo -n true 2>/dev/null; then
    sudo -n -E bash "${BASH_SOURCE[0]}" --setup --ifaces "$BLUE_ALLOWED_IFACES" >/dev/null 2>&1 || true
  fi
  if getent group "$LLM_GROUP" >/dev/null 2>&1 && id -nG "$USER" 2>/dev/null | tr ' ' '\n' | grep -qx "$LLM_GROUP"; then
    local quoted_cmd
    printf -v quoted_cmd '%q ' "$@"
    exec sg "$LLM_GROUP" -c "export LLM_ISOLATION_MODE=blue LLM_ALLOWED_IFACES='$BLUE_ALLOWED_IFACES'; $quoted_cmd"
  else
    exec "$@"
  fi
}

case "${1:---help}" in
  --setup|setup)
    shift
    setup_isolation "$@"
    ;;
  --remove|remove|--teardown|teardown)
    remove_isolation
    ;;
  --status|status)
    if [[ "${2:-}" == "--ifaces" && -n "${3:-}" ]]; then
      rebuild_iface_and_usb_arrays "$3"
    fi
    status_isolation
    ;;
  --run|run)
    shift
    run_in_isolated_group "$@"
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
