#!/usr/bin/env python3
"""
Cross-Platform Console Posture Detection & Dynamic Terminal Theme Engine (`console_posture.py`)
==============================================================================================
Automatically inspects the active OS/kernel network isolation posture on Linux and Windows and
applies an in-place "Hacker Console" background hue, font color, cursor tint, window title,
and Bottom-HUD / Startup-Banner security badge without spawning a separate terminal window.

Three Security Posture Modes:
  1. UNRESTRICTED (`./run_cora_NIX.sh cli` without isolation wrapper)
     - Background Hue: `#1C0A0D` (Deep Tactical Crimson / Blood-Obsidian)
     - Primary Font:   `#FFE8E8` (Warm Phosphor White)
     - Prompt/Border:  Neon Crimson (`#FF4D6D` / ANSI Bold Red)
     - HUD Badge:      `NET:UNRESTRICTED(FULL-ACCESS)`

  2. ISOLATED_LAN_USB (`LLM_NetworkIsolationSetup_NIX.sh --run ...` / `llm-local` group firewall)
     - Background Hue: `#081426` (Deep Cyber Navy Blue)
     - Primary Font:   `#E0F4FF` (Ice-Cyan Hacker Text)
     - Prompt/Border:  Electric Cyan (`#00E5FF` / ANSI Bold Cyan)
     - HUD Badge:      `NET:ISOLATED-LAN+USB(llm-local)`

  3. AIR_GAPPED_NETNS (`LLM_NetworkNamespaceSetup_NIX.sh --run|--unshare ...` / `llm-isolated` netns)
     - Background Hue: `#061A0E` (Deep Matrix Bunker Green)
     - Primary Font:   `#D1FAE5` (Crisp Matrix Phosphor Green)
     - Prompt/Border:  Neon Matrix Green (`#00FF66` / ANSI Bold Green)
     - HUD Badge:      `NET:AIR-GAPPED(llm-isolated)`
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "Network_Isolation" else SCRIPT_DIR
LOG_DIR = BASE_DIR / "Log"
POSTURE_LOG_FILE = LOG_DIR / "console_posture.log"
NETISO_CONF_FILE = SCRIPT_DIR / "network_isolation.conf"


def load_network_isolation_config() -> Dict[str, Any]:
    """
    Read static defaults from `Network_Isolation/network_isolation.conf`.
    Any CLI or environment override (`LLM_ISOLATION_MODE`, `LLM_ALLOWED_IFACES`)
    takes precedence over the static config file.
    """
    cfg: Dict[str, Any] = {
        "default_level": "red",
        "blue_allowed_ifaces": ["eth0", "eth1"],
        "blue_usb_devices": ["/dev/ttyUSB0", "/dev/ttyUSB1"],
    }
    if NETISO_CONF_FILE.is_file():
        try:
            for raw_ln in NETISO_CONF_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
                ln = raw_ln.strip()
                if not ln or ln.startswith("#") or "=" not in ln:
                    continue
                k, v = ln.split("=", 1)
                k = k.strip().upper()
                v = v.strip().strip("\"'")
                if k == "DEFAULT_ISOLATION_LEVEL" and v:
                    cfg["default_level"] = v.lower()
                elif k == "BLUE_ALLOWED_IFACES" and v:
                    ifaces = [x.strip() for x in v.replace(" ", ",").split(",") if x.strip() and x.strip() != "lo"]
                    if ifaces:
                        cfg["blue_allowed_ifaces"] = ifaces
                elif k == "BLUE_USB_DEVICES" and v:
                    devs = [x.strip() for x in v.replace(" ", ",").split(",") if x.strip()]
                    if devs:
                        cfg["blue_usb_devices"] = devs
        except Exception:
            pass
    env_ifaces = os.environ.get("LLM_ALLOWED_IFACES", "").strip()
    if env_ifaces:
        parsed = [x.strip() for x in env_ifaces.replace(" ", ",").split(",") if x.strip() and x.strip() != "lo"]
        if parsed:
            cfg["blue_allowed_ifaces"] = parsed
    return cfg


POSTURE_THEMES: Dict[str, Dict[str, str]] = {
    "UNRESTRICTED": {
        "mode": "UNRESTRICTED",
        "color_level": "RED",
        "short_tag": "RED:UNRESTRICTED",
        "hud_badge": "NET:RED(FULL-ACCESS)",
        "banner_badge": "[POSTURE: RED — UNRESTRICTED FULL NETWORK STACK ACCESS]",
        "description": "Full system & network stack access active (Red level — no namespace or interface restriction).",
        "bg_hex": "#1C0A0D",
        "fg_hex": "#FFE8E8",
        "cursor_hex": "#FF3B5C",
        "window_title": "CORA CLI [RED: UNRESTRICTED - FULL NETWORK ACCESS]",
        "ansi_border": "\033[1;31m",
        "ansi_accent": "\033[38;2;255;77;109m",
        "ansi_prompt": "\033[1;38;2;255;77;109m",
        "ansi_hud_bar": "\033[48;2;52;12;18;38;2;255;232;232;1m",
        "ps_bg": "DarkRed",
        "ps_fg": "White",
    },
    "ISOLATED_LAN_USB": {
        "mode": "ISOLATED_LAN_USB",
        "color_level": "BLUE",
        "short_tag": "BLUE:eth0,eth1",
        "hud_badge": "NET:BLUE(eth0,eth1)",
        "banner_badge": "[POSTURE: BLUE — INTERFACE-LOCKED ISOLATION (ALLOWED: eth0,eth1 + USB SERIAL)]",
        "description": "Blue interface-locked isolation active; only specified interfaces (CLI override or config) + USB serial allowed.",
        "bg_hex": "#081426",
        "fg_hex": "#E0F4FF",
        "cursor_hex": "#00E5FF",
        "window_title": "CORA CLI [BLUE: INTERFACE-LOCKED ISOLATION]",
        "ansi_border": "\033[1;36m",
        "ansi_accent": "\033[38;2;0;229;255m",
        "ansi_prompt": "\033[1;38;2;0;229;255m",
        "ansi_hud_bar": "\033[48;2;10;30;58;38;2;224;244;255;1m",
        "ps_bg": "DarkBlue",
        "ps_fg": "Cyan",
    },
    "AIR_GAPPED_NETNS": {
        "mode": "AIR_GAPPED_NETNS",
        "color_level": "WHITE",
        "short_tag": "WHITE:NETNS",
        "hud_badge": "NET:WHITE-NETNS(lo-only)",
        "banner_badge": "[POSTURE: WHITE — NETWORK NAMESPACE ISOLATED (LOOPBACK lo ONLY)]",
        "description": "White kernel network namespace isolation active (`llm-isolated` / `unshare -n` loopback `lo` only, zero external NICs).",
        "bg_hex": "#141820",
        "fg_hex": "#FFFFFF",
        "cursor_hex": "#FFFFFF",
        "window_title": "CORA CLI [WHITE: NAMESPACE ISOLATED (lo ONLY)]",
        "ansi_border": "\033[1;97m",
        "ansi_accent": "\033[38;2;255;255;255m",
        "ansi_prompt": "\033[1;38;2;255;255;255m",
        "ansi_hud_bar": "\033[48;2;36;42;54;38;2;255;255;255;1m",
        "ps_bg": "Black",
        "ps_fg": "White",
    },
}


def _normalize_mode_name(raw: str) -> str:
    val = (raw or "").strip().lower()
    if val.startswith("blue:") or val.startswith("blue="):
        return "ISOLATED_LAN_USB"
    if val in ("unrestricted", "full", "red", "live", "default"):
        return "UNRESTRICTED"
    if val in ("isolated_lan_usb", "lan_usb", "lan", "group", "llm-local", "blue", "restricted"):
        return "ISOLATED_LAN_USB"
    if val in ("air_gapped_netns", "airgap", "air-gap", "netns", "namespace", "llm-isolated", "white", "green"):
        return "AIR_GAPPED_NETNS"
    return ""


def _get_linux_active_interfaces() -> List[str]:
    # Query kernel netlink directly via `ip -o link show` so unshare -n / netns without sysfs remount
    # accurately reflects the process's actual network namespace interfaces.
    try:
        proc = subprocess.run(
            ["ip", "-o", "link", "show"],
            capture_output=True,
            text=True,
            timeout=1.5,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            active_nl: List[str] = []
            for ln in proc.stdout.splitlines():
                parts = ln.split(":", 2)
                if len(parts) >= 2:
                    iface_name = parts[1].strip().split("@")[0]
                    if "UP" in ln or "UNKNOWN" in ln:
                        active_nl.append(iface_name)
            return active_nl or ["lo"]
    except Exception:
        pass

    net_dir = Path("/sys/class/net")
    active: List[str] = []
    if not net_dir.is_dir():
        return active
    for iface_dir in sorted(net_dir.iterdir()):
        name = iface_dir.name
        try:
            flags_hex = (iface_dir / "flags").read_text(encoding="utf-8").strip()
            flags = int(flags_hex, 16)
            # IFF_UP == 0x1
            if flags & 0x1:
                active.append(name)
        except Exception:
            active.append(name)
    return active


def _customize_blue_theme_ifaces(theme: Dict[str, Any], all_ifaces: List[str]) -> Dict[str, Any]:
    cfg = load_network_isolation_config()
    allowed_list: List[str] = list(cfg.get("blue_allowed_ifaces") or ["eth0", "eth1"])
    allowed_csv = ",".join(allowed_list)
    theme["allowed_interfaces"] = allowed_list
    theme["short_tag"] = f"BLUE:{allowed_csv}"
    theme["hud_badge"] = f"NET:BLUE({allowed_csv})"
    theme["banner_badge"] = f"[POSTURE: BLUE — INTERFACE-LOCKED ISOLATION (ALLOWED: {allowed_csv} + lo)]"
    theme["window_title"] = f"CORA CLI [BLUE: ISOLATED TO {allowed_csv}]"
    filtered = [i for i in all_ifaces if i in allowed_list or i == "lo"]
    theme["active_interfaces"] = filtered or (["lo"] + allowed_list)
    return theme


def detect_console_posture(override: str = "") -> Dict[str, Any]:
    """
    Inspect the live OS/kernel environment and return the active posture dictionary.
    Works on both Linux and Windows.
    """
    os_name = platform.system().lower()
    evidence: List[str] = []
    raw_override = (override or os.environ.get("LLM_POSTURE_OVERRIDE", "")).strip()
    if raw_override.lower().startswith(("blue:", "blue=")):
        iface_part = raw_override.split(":", 1)[1] if ":" in raw_override else raw_override.split("=", 1)[1]
        if iface_part.strip():
            os.environ["LLM_ALLOWED_IFACES"] = iface_part.strip()

    forced = _normalize_mode_name(raw_override)
    active_ifaces = _get_linux_active_interfaces() if os_name == "linux" else _get_windows_active_interfaces()
    if forced:
        theme = dict(POSTURE_THEMES[forced])
        theme["detected_by"] = f"Explicit switch override ({forced})"
        theme["os"] = os_name
        theme["active_interfaces"] = ["lo"] if forced == "AIR_GAPPED_NETNS" else active_ifaces
        theme["effective_group"] = _get_effective_group_name()
        theme["netns"] = _get_linux_netns() or ("unshare-netns" if forced == "AIR_GAPPED_NETNS" else "(host-default)")
        if forced == "ISOLATED_LAN_USB":
            _customize_blue_theme_ifaces(theme, active_ifaces)
            theme["detected_by"] = f"BLUE Interface Isolation (Allowed: {','.join(theme['allowed_interfaces'])})"
        return theme

    env_mode = _normalize_mode_name(os.environ.get("LLM_ISOLATION_MODE", ""))
    netns_name = _get_linux_netns()
    egroup_name = _get_effective_group_name()

    # 1. Check Full Network Namespace / Loopback-Only Air-Gap (WHITE)
    non_loopback_up = [i for i in active_ifaces if i not in ("lo", "Loopback Pseudo-Interface 1")]
    if env_mode == "AIR_GAPPED_NETNS":
        evidence.append("LLM_ISOLATION_MODE=white (Namespace Isolation)")
        chosen = "AIR_GAPPED_NETNS"
    elif netns_name:
        evidence.append(f"Linux network namespace `{netns_name}`")
        chosen = "AIR_GAPPED_NETNS"
    elif os_name == "linux" and active_ifaces and len(non_loopback_up) == 0:
        evidence.append("Only loopback (`lo`) interface is UP in current network namespace")
        chosen = "AIR_GAPPED_NETNS"
    # 2. Check Interface-Locked Isolation (`BLUE` / `llm-local`)
    elif env_mode == "ISOLATED_LAN_USB":
        evidence.append("LLM_ISOLATION_MODE=blue (Interface Isolation)")
        chosen = "ISOLATED_LAN_USB"
    elif egroup_name == "llm-local":
        evidence.append("Effective kernel group GID is `llm-local` (iptables owner filter active)")
        chosen = "ISOLATED_LAN_USB"
    elif os_name == "windows" and _check_windows_firewall_isolation():
        evidence.append("Windows Defender Firewall rule `LLM_ISOLATION` is enabled")
        chosen = "ISOLATED_LAN_USB"
    # 3. Default: Unrestricted Full System & Network Access (RED)
    else:
        evidence.append(
            f"RED Unrestricted host network context (group=`{egroup_name}`, active NICs={','.join(active_ifaces) or 'default'})"
        )
        chosen = "UNRESTRICTED"

    theme = dict(POSTURE_THEMES[chosen])
    theme["detected_by"] = "; ".join(evidence)
    theme["os"] = os_name
    theme["active_interfaces"] = ["lo"] if chosen == "AIR_GAPPED_NETNS" else active_ifaces
    theme["effective_group"] = egroup_name
    theme["netns"] = netns_name or ("unshare-netns" if chosen == "AIR_GAPPED_NETNS" else "(host-default)")
    if chosen == "ISOLATED_LAN_USB":
        _customize_blue_theme_ifaces(theme, active_ifaces)
        theme["detected_by"] = f"{theme['detected_by']} [Locked to: {','.join(theme['allowed_interfaces'])}]"
    return theme


def _get_effective_group_name() -> str:
    if platform.system().lower() == "windows":
        return os.environ.get("USERNAME", "windows-user")
    try:
        import grp

        return grp.getgrgid(os.getegid()).gr_name
    except Exception:
        return str(os.getegid())


def _get_linux_netns() -> str:
    if platform.system().lower() != "linux":
        return ""
    try:
        proc = subprocess.run(
            ["ip", "netns", "identify", str(os.getpid())],
            capture_output=True,
            text=True,
            timeout=1.5,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception:
        pass
    return ""


def _get_windows_active_interfaces() -> List[str]:
    if platform.system().lower() != "windows":
        return []
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "(Get-NetAdapter | Where-Object Status -eq 'Up').Name"],
            capture_output=True,
            text=True,
            timeout=3.0,
            check=False,
        )
        if proc.returncode == 0:
            return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    except Exception:
        pass
    return ["default"]


def _check_windows_firewall_isolation() -> bool:
    if os.environ.get("LLM_FIREWALL_ISOLATED") == "1":
        return True
    if platform.system().lower() != "windows":
        return False
    try:
        proc = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", "name=LLM_ISOLATION"],
            capture_output=True,
            text=True,
            timeout=2.5,
            check=False,
        )
        return proc.returncode == 0 and "Enabled:" in proc.stdout and "Yes" in proc.stdout
    except Exception:
        return False


def _log_posture_event(action: str, info: Dict[str, Any]) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(LOG_DIR, 0o775)
        except OSError:
            pass
        ts = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
        line = (
            f"[{ts}] action={action} mode={info.get('mode', 'RESET')} "
            f"group={info.get('effective_group', '-')} netns={info.get('netns', '-')} "
            f"bg={info.get('bg_hex', '-')} reason=\"{info.get('detected_by', '')}\"\n"
        )
        with open(POSTURE_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
        try:
            os.chmod(POSTURE_LOG_FILE, 0o664)
        except OSError:
            pass
    except Exception:
        pass


def apply_console_posture(override: str = "", quiet: bool = False, force_osc: bool = False) -> Dict[str, Any]:
    """
    Detect (or override) the console posture, emit XTerm OSC 11/10/12 + Window Title sequences
    in-place to tint the current terminal window, log to `Log/console_posture.log`, and optionally
    print the posture status banner.
    """
    info = detect_console_posture(override=override)
    if (sys.stdout.isatty() or force_osc) and os.environ.get("TERM", "") != "dumb":
        osc_seq = (
            f"\033]11;{info['bg_hex']}\007"
            f"\033]10;{info['fg_hex']}\007"
            f"\033]12;{info['cursor_hex']}\007"
            f"\033]0;{info['window_title']}\007"
        )
        sys.stdout.write(osc_seq)
        sys.stdout.flush()

    _log_posture_event("APPLY", info)

    if not quiet:
        print(format_posture_banner(info), flush=True)
    return info


def reset_console_posture(quiet: bool = True, force_osc: bool = False) -> None:
    """Restore the terminal's default profile background, foreground, and cursor colors."""
    if (sys.stdout.isatty() or force_osc) and os.environ.get("TERM", "") != "dumb":
        # OSC 111 = reset background, OSC 110 = reset foreground, OSC 112 = reset cursor
        sys.stdout.write("\033]111\007\033]110\007\033]112\007\033]0;Terminal\007\033[0m")
        sys.stdout.flush()
    _log_posture_event("RESET", {"mode": "DEFAULT_RESTORED", "detected_by": "Session exit / manual reset"})
    if not quiet:
        print("\033[0m[Console Posture] Restored default terminal background & font colors.", flush=True)


def format_posture_banner(info: Dict[str, Any]) -> str:
    border = info["ansi_border"]
    accent = info["ansi_accent"]
    reset = "\033[0m"
    lines = [
        f"{border}======================================================================{reset}",
        f"  {accent}{info['banner_badge']}{reset}",
        f"  Posture Mode:   {accent}{info['mode']}{reset} ({info['hud_badge']})",
        f"  Console Theme:  BG `{info['bg_hex']}` | Font `{info['fg_hex']}` | Cursor `{info['cursor_hex']}`",
        f"  Kernel State:   Group=`{info['effective_group']}` | NetNS=`{info['netns']}` | NICs=`{','.join(info['active_interfaces']) or 'lo'}`",
        f"  Detection Rule: {info['detected_by']}",
        f"{border}======================================================================{reset}",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CORA Console Posture Detection & In-Place Terminal Theme Controller"
    )
    parser.add_argument(
        "--detect",
        "--status",
        dest="action",
        action="store_const",
        const="detect",
        default="detect",
        help="Auto-detect current security posture, tint terminal in-place, and display banner [DEFAULT]",
    )
    parser.add_argument(
        "--apply",
        dest="apply_mode",
        type=str,
        default="",
        help="Apply a specific posture theme (`auto`, `unrestricted`, `lan`, `airgap`)",
    )
    parser.add_argument(
        "--reset",
        dest="action",
        action="store_const",
        const="reset",
        help="Restore default terminal background, foreground, and cursor colors",
    )
    parser.add_argument(
        "--demo",
        "--test-all",
        dest="action",
        action="store_const",
        const="demo",
        help="Preview all 3 posture themes (Red Unrestricted -> Blue LAN+USB -> Green Air-Gap) then restore active posture",
    )
    parser.add_argument("--json", action="store_true", help="Output detected posture as JSON")
    parser.add_argument("--env", action="store_true", help="Output shell-evaluatable KEY=VALUE lines")
    parser.add_argument("--quiet", "-q", action="store_true", help="Apply terminal colors quietly without banner")
    parser.add_argument("--force-osc", action="store_true", help="Emit OSC color sequences even if stdout is piped")

    args = parser.parse_args()

    if args.apply_mode.strip().lower() in ("demo", "test", "test-all"):
        args.action = "demo"
    elif args.apply_mode.strip().lower() == "reset":
        args.action = "reset"

    if args.action == "reset":
        reset_console_posture(quiet=args.quiet, force_osc=args.force_osc)
        return

    if args.action == "demo":
        for mode_key in ("UNRESTRICTED", "ISOLATED_LAN_USB", "AIR_GAPPED_NETNS"):
            apply_console_posture(override=mode_key, quiet=False, force_osc=True)
            time.sleep(1.2)
        print("\n[Demo Complete] Restoring live auto-detected posture...", flush=True)
        apply_console_posture(override="", quiet=False, force_osc=True)
        return

    override = "" if args.apply_mode in ("", "auto") else args.apply_mode
    if args.json:
        info = detect_console_posture(override=override)
        print(json.dumps(info, indent=2))
        return

    if args.env:
        info = detect_console_posture(override=override)
        for k in ("mode", "short_tag", "hud_badge", "bg_hex", "fg_hex", "cursor_hex", "ps_bg", "ps_fg"):
            print(f"POSTURE_{k.upper()}={json.dumps(info[k])}")
        return

    apply_console_posture(override=override, quiet=args.quiet, force_osc=args.force_osc)


if __name__ == "__main__":
    main()
