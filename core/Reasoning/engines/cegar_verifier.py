"""
Engine 12: Counterexample-Guided Abstraction Refinement (CEGAR) Pre-Execution Verifier
======================================================================================
Enforces Guardrail 1 (Strict Non-Blocking CEGAR Mode for semantic routes, Hard-Block for impossible/broken commands):
1. HARD-BLOCKS 4 fatal classes of obviously broken commands before execution:
   (a) Invalid Bash syntax (`bash -n` fails),
   (b) Guaranteed infinite hangs on non-TTY subprocesses (`tio /dev/tty...` without `--script`,
       or `ping` without `-c` / `-w`),
   (c) Passing Python `import ...` inside `tio --script` (which expects Lua),
   (d) Truncated / Malformed IPv4 addresses or network targets (e.g. `http://172.24`, `https://192.16`,
       `192.1`, `ip route get 1`, trailing dots `192.0.2.`, or octets > 255).
2. ADVISORY MODE (`blocked = False`) for semantic/network preconditions:
   - Inspects `ip route add <subnet> via <gw>` against live kernel interfaces/subnets (`ip -j addr`)
     or symbolic state and emits a helpful `[CEGAR Advisory]` note if the gateway subnet is not yet
     configured, NEVER trapping the LLM in a rejection loop.
"""

import ipaddress
import os
from pathlib import Path
import re
import subprocess
import time
from typing import Any, Dict, List, Optional, Tuple

from .vault_bridge import get_hardware_reasoning_limits, resolve_problem_targets, write_reasoning_note

_BASH_N_AVAILABLE: Optional[bool] = None
_LOCAL_NETS_CACHE: Tuple[float, List[ipaddress.IPv4Network]] = (0.0, [])
_CEGAR_CMD_CACHE: Dict[str, Dict[str, Any]] = {}


def _is_bash_n_available() -> bool:
    """
    Verify once whether `bash -n` works on the host OS.
    On Windows machines (`os.name == "nt"`), commands run under PowerShell/cmd rather than bash,
    and an unconfigured WSL `C:\\Windows\\System32\\bash.exe` stub either blocks or exits with code 1.
    """
    global _BASH_N_AVAILABLE
    if _BASH_N_AVAILABLE is not None:
        return _BASH_N_AVAILABLE
    if os.name == "nt":
        _BASH_N_AVAILABLE = False
        return False
    try:
        proc = subprocess.run(
            ["bash", "-n"],
            input="true\n",
            capture_output=True,
            text=True,
            timeout=2,
        )
        _BASH_N_AVAILABLE = proc.returncode == 0
    except Exception:
        _BASH_N_AVAILABLE = False
    return _BASH_N_AVAILABLE


def _get_local_ipv4_networks() -> List[ipaddress.IPv4Network]:
    """Queries live local IPv4 networks via `ip -o -4 addr show` (Linux) or `ipconfig` (Windows) with 10s TTL cache."""
    global _LOCAL_NETS_CACHE
    now = time.monotonic()
    if _LOCAL_NETS_CACHE[1] and (now - _LOCAL_NETS_CACHE[0]) < 10.0:
        return _LOCAL_NETS_CACHE[1]
    nets: List[ipaddress.IPv4Network] = []
    try:
        if os.name != "nt":
            proc = subprocess.run(
                ["ip", "-o", "-4", "addr", "show"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if proc.returncode == 0:
                for m in re.finditer(r"inet\s+(\d+\.\d+\.\d+\.\d+/\d+)", proc.stdout):
                    try:
                        nets.append(ipaddress.ip_network(m.group(1), strict=False))
                    except ValueError:
                        pass
        else:
            proc = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            if proc.returncode == 0:
                ips = re.findall(r"IPv4 Address[.\s]*:\s*(\d+\.\d+\.\d+\.\d+)", proc.stdout)
                masks = re.findall(r"Subnet Mask[.\s]*:\s*(\d+\.\d+\.\d+\.\d+)", proc.stdout)
                for ip_s, mask_s in zip(ips, masks):
                    try:
                        nets.append(ipaddress.ip_network(f"{ip_s}/{mask_s}", strict=False))
                    except ValueError:
                        pass
    except Exception:
        pass
    _LOCAL_NETS_CACHE = (now, nets)
    return nets


def _find_truncated_or_malformed_ipv4(text: str) -> Optional[str]:
    """
    Detects truncated/incomplete IPv4 addresses in URLs or networking commands, such as:
      - `http://172.24` or `https://192.16` or `http://10.0.1` (1-3 numeric octets in a URL host)
      - `ip route get 1` or `ip route get 172.24` or `ping -c 3 172.24`
      - Trailing dot IPv4 like `192.0.2.`
      - 4-octet numeric strings where an octet > 255 (e.g. `172.24.300.1`)
    Returns a human-readable counterexample string if found, else None.
    """
    s = (text or "").strip()
    if not s:
        return None

    # 1. URL with purely numeric/dot host that does NOT have 4 valid octets (e.g. http://172.24 or https://192.16)
    for m_url in re.finditer(r"https?://([0-9.]+)(?::\d+)?(?:/|\s|$|\"|')", s):
        host_num = m_url.group(1)
        parts = host_num.split(".")
        if len(parts) != 4 or any(not p.isdigit() or int(p) > 255 for p in parts):
            return f"Truncated or invalid IPv4 host `{host_num}` in URL `{m_url.group(0).strip()}` (expected 4 octets `A.B.C.D`)."

    # 2. `ip route get <arg>` or `ip neigh show <arg>` or `ping ... <arg>` or `nmap ... <arg>` ending in 1-3 octets
    for m_net in re.finditer(
        r"\b(?:ip\s+route\s+get|ip\s+neigh\s+(?:show|get)|arping|traceroute|tracepath)\s+([0-9.]+)(?:\s|$|;|&&|\|)",
        s,
    ):
        target_num = m_net.group(1)
        parts = target_num.split(".")
        if len(parts) != 4 or any(not p.isdigit() or int(p) > 255 for p in parts):
            return f"Truncated or invalid IPv4 target `{target_num}` in `{m_net.group(0).strip()}` (expected 4 octets `A.B.C.D`)."

    # 3. Any standalone private-prefix partial IP (e.g. `172.24`, `192.16`, `192.1`, `192.0.2`, `10.0.0.`)
    #    at the end of a command or token (not followed by `.digit`)
    for m_part in re.finditer(
        r"(?:^|\s|://|@)(192\.\d{1,3}(?:\.\d{1,3})?\.?|192\.|10\.\d{1,3}(?:\.\d{1,3})?\.?|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3})?\.?)(?=\s|$|;|&&|\||\"|')",
        s,
    ):
        cand = m_part.group(1)
        # Make sure it's not a valid 4-octet IP
        parts = cand.split(".")
        if len(parts) != 4 or any(not p.isdigit() or int(p) > 255 for p in parts):
            return f"Truncated IPv4 address `{cand}` detected (fewer than 4 octets)."

    # 4. Any 4-octet IP with an octet > 255
    for m_ip4 in re.finditer(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b", s):
        octets = [int(m_ip4.group(i)) for i in range(1, 5)]
        if any(o > 255 for o in octets):
            return f"Invalid IPv4 address `{m_ip4.group(0)}` (octet > 255)."

    return None


def _get_host_all_interface_subnets() -> Dict[str, List[ipaddress.IPv4Network]]:
    """Map every host interface on Linux and Windows to its IPv4 networks (unfiltered) to detect disallowed subnet probes in BLUE mode."""
    out: Dict[str, List[ipaddress.IPv4Network]] = {}
    if os.name == "nt":
        try:
            proc = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=1.5,
                check=False,
            )
            if proc.returncode == 0 and proc.stdout:
                cur_iface = ""
                cur_ip = ""
                for ln in proc.stdout.splitlines():
                    s = ln.strip()
                    if s.endswith(":") and "adapter" in s.lower():
                        cur_iface = re.sub(r"(?i)^.*adapter\s+", "", s[:-1]).strip()
                    elif ("IPv4 Address" in s or "IP Address" in s) and cur_iface:
                        m = re.search(r"(\d+\.\d+\.\d+\.\d+)", s)
                        if m:
                            cur_ip = m.group(1)
                    elif "Subnet Mask" in s and cur_iface and cur_ip:
                        m = re.search(r"(\d+\.\d+\.\d+\.\d+)", s)
                        mask = m.group(1) if m else "255.255.255.0"
                        try:
                            net = ipaddress.ip_network(f"{cur_ip}/{mask}", strict=False)
                            out.setdefault(cur_iface, []).append(net)
                        except ValueError:
                            pass
                        cur_ip = ""
        except Exception:
            pass
        return out
    try:
        proc = subprocess.run(
            ["ip", "-o", "-4", "addr", "show"],
            capture_output=True,
            text=True,
            timeout=1.2,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout:
            for ln in proc.stdout.splitlines():
                parts = ln.split()
                if len(parts) >= 4:
                    iface = parts[1].split("@")[0]
                    for tok in parts[2:]:
                        if "/" in tok and re.match(r"^\d+\.\d+\.\d+\.\d+/\d+$", tok):
                            try:
                                net = ipaddress.ip_network(tok, strict=False)
                                out.setdefault(iface, []).append(net)
                            except ValueError:
                                pass
    except Exception:
        pass
    return out


def _is_iface_in_allowed(iface_name: str, allowed_set: set[str]) -> bool:
    ilow = (iface_name or "").strip().lower()
    if not ilow:
        return False
    allowed_low = {a.lower() for a in allowed_set}
    if ilow in allowed_low:
        return True
    if os.name == "nt":
        return any(len(a) >= 3 and (a in ilow or ilow in a) for a in allowed_low if a != "lo")
    return False


def _check_network_isolation_policy(cmd_or_target: str, is_target_only: bool = False) -> Optional[Dict[str, Any]]:
    """
    Enforce WHITE (Namespace Isolation) and BLUE (Interface-Locked Isolation) policies in CEGAR.
    Returns a blocking dict if `cmd_or_target` violates the active isolation level, else `None`.
    """
    from .vault_bridge import _get_isolation_filter

    iso_level, blue_ifaces = _get_isolation_filter()
    if iso_level == "red":
        return None

    allowed_set = set(blue_ifaces) | {"lo"}
    all_if_nets = _get_host_all_interface_subnets()
    host_ifaces = set(all_if_nets.keys())
    try:
        net_sys = Path("/sys/class/net")
        if net_sys.is_dir():
            host_ifaces |= {p.name for p in net_sys.iterdir()}
    except Exception:
        pass

    if iso_level == "white":
        if is_target_only:
            if not re.search(r"\b(?:127\.\d+\.\d+\.\d+|localhost)\b", cmd_or_target, re.I):
                return {
                    "blocked": True,
                    "reason": "WHITE Network Isolation (Namespace Mode) blocks external network targets (`lo` loopback only).",
                    "counterexample": f"Target `{cmd_or_target}` is external to loopback (`127.0.0.1`).",
                    "suggested_fix": "Switch to `-netiso blue <ifaces>` or `-netiso red` if external network probing is required.",
                }
            return None

        # Command-level WHITE mode checks (enforced on both Windows and Linux):
        # 1. Remote Windows SMB / UNC share paths (`\\live.sysinternals.com\...`, `\\target\...`)
        m_unc = re.search(r"\\\\(?!(?:127\.0\.0\.1|localhost|\.)\\)([A-Za-z0-9_.\-]+)\\", cmd_or_target, re.I)
        if m_unc:
            return {
                "blocked": True,
                "reason": "WHITE Network Isolation (Air-Gap Mode) blocks remote SMB/UNC share access (`127.0.0.1` loopback only).",
                "counterexample": f"Command references external UNC share host `\\\\{m_unc.group(1)}\\`.",
                "suggested_fix": "Use locally installed binaries in `Tools/Windows/` or switch to BLUE/RED network isolation.",
            }

        # 2. External HTTP/HTTPS URLs not targeting 127.x.x.x or localhost
        m_url = re.search(r"https?://(?!(?:127\.\d+\.\d+\.\d+|localhost|\[::1\])\b)([A-Za-z0-9_.\-]+)", cmd_or_target, re.I)
        if m_url:
            return {
                "blocked": True,
                "reason": "WHITE Network Isolation (Air-Gap Mode) blocks outbound HTTP/HTTPS requests (`127.0.0.1` loopback only).",
                "counterexample": f"Command references external URL host `{m_url.group(1)}`.",
                "suggested_fix": "Restrict requests to `127.0.0.1` / `localhost` or switch to BLUE/RED network isolation.",
            }

        # 3. Non-loopback IPv4 addresses in command arguments
        for m_ip in re.finditer(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", cmd_or_target):
            try:
                ip_obj = ipaddress.IPv4Address(m_ip.group(1))
            except ValueError:
                continue
            if ip_obj.is_loopback or str(ip_obj) in ("0.0.0.0", "255.255.255.255", "255.255.255.0", "255.255.0.0"):
                continue
            return {
                "blocked": True,
                "reason": "WHITE Network Isolation (Namespace Mode) blocks external network targets (`lo` / `127.0.0.1` loopback only).",
                "counterexample": f"Command references non-loopback IPv4 address `{ip_obj}`.",
                "suggested_fix": "Switch to `-netiso blue <ifaces>` or `-netiso red` if external network probing is required.",
            }
        return None

    # BLUE mode enforcement: Only `blue_ifaces` (+ `lo`) are allowed
    if not is_target_only:
        # 1. Check explicit interface flags (`dev <iface>`, `-i <iface>`, `-I <iface>`, `--interface <iface>`, `-InterfaceAlias <iface>`)
        for m_if in re.finditer(
            r"(?:\bdev\s+|\s-[iI]\s*|\s--interface(?:=|\s+)|\s-InterfaceAlias\s+|\bifconfig\s+|\bip\s+link\s+set\s+(?:dev\s+)?)([\"']?[a-zA-Z0-9_.\-() ]+?[\"']?)(?=\s|$|;|&|\|)",
            cmd_or_target,
            re.I,
        ):
            cand_if = m_if.group(1).strip().strip("\"'")
            if any(cand_if.lower() == h.lower() for h in host_ifaces) and not _is_iface_in_allowed(cand_if, allowed_set):
                return {
                    "blocked": True,
                    "reason": f"BLUE Network Isolation Policy locks CLI interaction strictly to `{', '.join(blue_ifaces)}`.",
                    "counterexample": f"Command references disallowed interface `{cand_if}` (Allowed: `{', '.join(blue_ifaces)}`).",
                    "suggested_fix": f"Use only allowed interface(s): `{', '.join(blue_ifaces)}`.",
                }
        # 2. Check any bare mention of a known disallowed host NIC (e.g., `eth2`, `wlan0`, `Wi-Fi`, `VMnet1`)
        for h_if in host_ifaces:
            if not _is_iface_in_allowed(h_if, allowed_set) and len(h_if) >= 3:
                if re.search(rf"(?<![a-zA-Z0-9_.\-/]){re.escape(h_if)}(?![a-zA-Z0-9_.\-/])", cmd_or_target, re.I):
                    return {
                        "blocked": True,
                        "reason": f"BLUE Network Isolation Policy locks CLI interaction strictly to `{', '.join(blue_ifaces)}`.",
                        "counterexample": f"Command references disallowed host interface `{h_if}` (Allowed: `{', '.join(blue_ifaces)}`).",
                        "suggested_fix": f"Restrict all commands to allowed interface(s): `{', '.join(blue_ifaces)}`.",
                    }

    # 3. Check if any IPv4 address in the command/target belongs to a disallowed local interface subnet (or outside allowed subnets on Windows)
    allowed_nets = [
        n
        for iface, nets in all_if_nets.items()
        if _is_iface_in_allowed(iface, allowed_set)
        for n in nets
    ]
    disallowed_if_map: List[tuple[str, ipaddress.IPv4Network]] = [
        (iface, net)
        for iface, nets in all_if_nets.items()
        if not _is_iface_in_allowed(iface, allowed_set)
        for net in nets
    ]
    for m_ip in re.finditer(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", cmd_or_target):
        try:
            ip_obj = ipaddress.IPv4Address(m_ip.group(1))
        except ValueError:
            continue
        if ip_obj.is_loopback or str(ip_obj) in ("0.0.0.0", "255.255.255.255", "255.255.255.0", "255.255.0.0"):
            continue
        if any(ip_obj in anet for anet in allowed_nets):
            continue
        for bad_if, bad_net in disallowed_if_map:
            if ip_obj in bad_net:
                return {
                    "blocked": True,
                    "reason": f"BLUE Network Isolation Policy blocks traffic to `{ip_obj}` on disallowed interface `{bad_if}` (`{bad_net}`).",
                    "counterexample": f"Target `{ip_obj}` resides on disallowed interface `{bad_if}` (Allowed interfaces: `{', '.join(blue_ifaces)}`).",
                    "suggested_fix": f"Only interact with targets reachable via allowed interface(s): `{', '.join(blue_ifaces)}`.",
                }
        if os.name == "nt" and allowed_nets:
            allowed_subnets_str = ", ".join(str(n) for n in allowed_nets)
            return {
                "blocked": True,
                "reason": (
                    f"BLUE Network Isolation Policy on Windows locks traffic strictly to allowed interface "
                    f"`{', '.join(blue_ifaces)}` subnet(s) (`{allowed_subnets_str}`)."
                ),
                "counterexample": (
                    f"Target `{ip_obj}` is outside the allowed Windows interface subnet(s) `{allowed_subnets_str}` "
                    f"for `{', '.join(blue_ifaces)}`."
                ),
                "suggested_fix": (
                    f"Target only hosts within `{allowed_subnets_str}` (`{', '.join(blue_ifaces)}`), add the required "
                    f"Windows adapter to BLUE allowed interfaces, or switch to RED isolation."
                ),
            }
    return None


def _check_personality_mode_policy(cmd_or_target: str, is_target_only: bool = False) -> Optional[Dict[str, Any]]:
    """
    Enforce C.O.R.A. Session Personality & Logic Modes (`DEFAULT`, `ANALYST`, `BERSERKER`, `NINJA`):
      - `DEFAULT`  : No extra personality restrictions.
      - `ANALYST`  : Strictly local offline analysis only (WHITE Network Isolation). Blocks ALL network scanning
                     and any outbound data transmission outside the local laptop from CLI or WebGUI.
      - `BERSERKER`: Full aggressive tool execution within the chosen Red/Blue network isolation group.
      - `NINJA`    : Covert, low-noise operations only. Blocks noisy flood scanners (`masscan`, `zmap`, `nikto`,
                     `hydra`, `gobuster`, `ffuf`, etc.) and aggressive `nmap` flags (`-T4`, `-T5`, `-A`, `--min-rate`).
    """
    mode = os.environ.get("CORA_PERSONALITY_MODE", "DEFAULT").strip().upper() or "DEFAULT"
    s = (cmd_or_target or "").strip()
    if not s or mode in ("DEFAULT", "BERSERKER"):
        return None

    _ls_proj_fallback = "dir %PROJECT_DIR%" if os.name == "nt" else "ls -la $PROJECT_DIR"
    _passive_net_fallback = (
        "ipconfig & route print & arp -a"
        if os.name == "nt"
        else "ip -4 -br addr show; ip route show; ip neigh show"
    )
    if mode == "ANALYST":
        if is_target_only:
            return {
                "blocked": True,
                "reason": "ANALYST Mode (WHITE Network Isolation) strictly prohibits network scanning (`scan_target`) and outbound data transmission.",
                "counterexample": f"Target scan `{s}` attempted while in ANALYST mode (local laptop data analysis only).",
                "suggested_fix": "Use `read_file`, `list_directory`, `vault_search`, `vault_read_note`, or `generate_project_report` to analyze existing local project data.",
                "repaired_command": _ls_proj_fallback,
            }
        # 1. Block all network scanning and active enumeration binaries unconditionally
        m_scan = re.search(
            r"(?:^|&&|\|\||;|\||\bsudo\s+)\s*\b("
            r"nmap|masscan|zmap|rustscan|unicornscan|nikto|gobuster|ffuf|dirb|dirbuster|wfuzz|feroxbuster|"
            r"sqlmap|wpscan|nuclei|whatweb|wafw00f|hydra|medusa|ncrack|patator|crowbar|responder|"
            r"impacket-[a-z0-9_\-]+|crackmapexec|netexec|nxc|enum4linux|smbclient|smbmap|rpcclient|"
            r"ldapsearch|snmpwalk|onesixtyone|arp-scan|netdiscover|fping|hping3|arping|nbtscan|fierce|"
            r"dnsenum|dnsrecon|amass|subfinder|theharvester|msfconsole|msfvenom|bettercap|ettercap"
            r")\b",
            s,
            re.I,
        )
        if m_scan:
            tool_found = m_scan.group(1)
            return {
                "blocked": True,
                "reason": "ANALYST Mode (WHITE Network Isolation) strictly prohibits network scanning and external enumeration.",
                "counterexample": f"Network scanner `{tool_found}` detected in `{s[:100]}`.",
                "suggested_fix": "Analyze local scan reports, logs, and files inside `Projects/<active_project>/` instead of running network scans.",
                "repaired_command": _ls_proj_fallback,
            }

        # 2. Block outbound network clients, packet senders, remote shells, and serial OOB transmitters
        m_outbound = re.search(
            r"(?:^|&&|\|\||;|\||\bsudo\s+)\s*\b("
            r"ping|ping6|traceroute|tracepath|mtr|nc|ncat|netcat|socat|telnet|ssh|scp|sftp|rsync|ftp|tftp|"
            r"dig|nslookup|host|whois|sendmail|tcpdump|tshark|wireshark|tio|"
            r"curl|wget|invoke-webrequest|invoke-restmethod|iwr|irm|test-netconnection"
            r")\b|/dev/(?:tcp|udp)/|/dev/tty(?:USB|ACM)\d+",
            s,
            re.I,
        )
        if m_outbound:
            tok_found = m_outbound.group(0).strip()
            return {
                "blocked": True,
                "reason": "ANALYST Mode (WHITE Network Isolation) strictly prohibits network scanning or sending data outside the local laptop system.",
                "counterexample": f"Network/outbound command `{tok_found}` detected in `{s[:100]}`.",
                "suggested_fix": "Use local filesystem analysis tools (`cat`, `grep`, `jq`, `awk`, `python3` on local files, `read_file`, `vault_search`) only.",
                "repaired_command": _ls_proj_fallback,
            }

        # 3. Block inline scripting socket/HTTP connections (e.g. `python3 -c "...socket/urllib/requests/http.client..."`)
        if re.search(r"\b(?:urllib\.request|requests\.(?:get|post|put|delete|head|Session)|http\.client|socket\.socket|paramiko|ftplib|smtplib)\b", s, re.I):
            return {
                "blocked": True,
                "reason": "ANALYST Mode (WHITE Network Isolation) prohibits outbound network connections via scripting libraries.",
                "counterexample": f"Outbound network library call detected in `{s[:100]}`.",
                "suggested_fix": "Process only local files on the workstation disk in ANALYST mode.",
                "repaired_command": _ls_proj_fallback,
            }
        return None

    if mode == "NINJA" and not is_target_only:
        # 1. Block high-noise flood scanners, directory brute-forcers, and credential flood tools
        m_noisy_bin = re.search(
            r"(?:^|&&|\|\||;|\||\bsudo\s+)\s*\b("
            r"masscan|zmap|rustscan|unicornscan|nikto|wpscan|nuclei|hydra|medusa|ncrack|patator|crowbar|"
            r"dirb|dirbuster|gobuster|ffuf|wfuzz|feroxbuster|responder|bettercap|ettercap"
            r")\b",
            s,
            re.I,
        )
        if m_noisy_bin:
            noisy_tool = m_noisy_bin.group(1)
            return {
                "blocked": True,
                "reason": f"[NINJA MODE COVERT GUARD] `{noisy_tool}` is a high-noise, aggressive tool prohibited in Ninja mode.",
                "counterexample": f"Command `{s[:100]}` uses noisy/flood scanner `{noisy_tool}`.",
                "suggested_fix": "Use covert, low-noise techniques: passive local inspection (`ss -tulnp`, `ip neigh`, `arp -a`), targeted single-request `curl -sS -m 5`, or stealthy `nmap -sS -T2 -Pn --max-rate 15 -p <specific_ports> <target>`.",
                "repaired_command": _passive_net_fallback,
            }

        # 2. Block aggressive `nmap` flags (`-T4`, `-T5`, `-A`, `--min-rate` > 50, noisy NSE scripts, full `-p-` without `-T1/-T2`)
        if re.search(r"(?:^|&&|\|\||;|\||\bsudo\s+)\s*\bnmap\b", s, re.I):
            m_agg_nmap = re.search(
                r"(?:\s-T[45]\b|\s-A\b|\s--min-rate(?:=|\s+)(?:[5-9]\d|\d{3,})\b|\s--script(?:=|\s+)[^\s]*(?:vuln|exploit|dos|brute|intrusive|fuzzer|broadcast)|\s--flood\b)",
                s,
                re.I,
            )
            if m_agg_nmap or ("-p-" in s and not re.search(r"\s-T[012]\b", s)):
                bad_flag = m_agg_nmap.group(0).strip() if m_agg_nmap else "-p- (full 65535-port sweep without -T1/-T2 stealth timing)"
                repaired_nmap = re.sub(r"\s-T[345]\b", " -T2", s)
                repaired_nmap = re.sub(r"\s-A\b", " -sV --version-light", repaired_nmap)
                repaired_nmap = re.sub(r"\s--min-rate(?:=|\s+)\d+", " --max-rate 15", repaired_nmap)
                if "-T" not in repaired_nmap:
                    repaired_nmap = re.sub(r"\bnmap\b", "nmap -T2 --max-rate 15", repaired_nmap, count=1)
                return {
                    "blocked": True,
                    "reason": "[NINJA MODE COVERT GUARD] Aggressive/noisy `nmap` flag detected. Ninja mode requires covert, low-noise commands at all times.",
                    "counterexample": f"Detected aggressive flag `{bad_flag}` in `{s[:100]}`.",
                    "suggested_fix": f"Replace aggressive scan flags with covert polite/sneaky timing (`-T2 --max-rate 15`) and targeted ports: `{repaired_nmap}`.",
                    "repaired_command": repaired_nmap,
                }

        # 3. Block packet floods (`ping -f`, `hping3 --flood`, `hping3 --faster`)
        if re.search(r"\bping\b[^;&|]*\s-f\b|\bhping3\b[^;&|]*\s--(?:flood|faster|rand-source)\b", s, re.I):
            return {
                "blocked": True,
                "reason": "[NINJA MODE COVERT GUARD] Packet flooding (`ping -f` / `hping3 --flood`) is strictly prohibited in Ninja mode.",
                "counterexample": f"Flood flag detected in `{s[:100]}`.",
                "suggested_fix": "Use a covert 1-packet probe (`ping -c 1 -W 2 <target>`) or passive ARP inspection (`ip neigh show`).",
                "repaired_command": "ip neigh show",
            }
    return None


def verify_target_address_cegar(target: str) -> Dict[str, Any]:
    """Verifies a URL or IP/host passed to `scan_target` or `neuro_symbolic_reason`."""
    t = (target or "").strip()
    if not t:
        return {
            "blocked": True,
            "reason": "Target URL/IP is empty.",
            "counterexample": "Empty `target` argument.",
            "suggested_fix": "Provide a complete 4-octet IPv4 address (`A.B.C.D`) or valid hostname.",
        }
    mode_blk = _check_personality_mode_policy(t, is_target_only=True)
    if mode_blk:
        return mode_blk
    check_str = t if re.match(r"^https?://", t, re.I) else f"http://{t}"
    bad_ip = _find_truncated_or_malformed_ipv4(check_str)
    if bad_ip:
        return {
            "blocked": True,
            "reason": "Truncated or malformed IPv4 target address detected by CEGAR pre-verifier.",
            "counterexample": bad_ip,
            "suggested_fix": "Provide the full 4-octet IPv4 address from the user's prompt (`A.B.C.D`).",
        }
    iso_blk = _check_network_isolation_policy(t, is_target_only=True)
    if iso_blk:
        return iso_blk
    return {"blocked": False, "reason": "Valid target.", "counterexample": "", "suggested_fix": ""}


_WINDOWS_OR_PS_CMD_RE = re.compile(
    r"^(?:"
    r"wmic|icacls|cacls|bcdedit|auditpol|wevtutil|wevutil|reg|regedit|net|net1|netsh|ipconfig|nbtstat|"
    r"tasklist|taskkill|systeminfo|takeown|sfc|attrib|forfiles|findstr|dir|copy|xcopy|robocopy|"
    r"del|erase|ren|rename|md|rd|rmdir|type|sc|schtasks|runas|gpresult|gpupdate|nltest|"
    r"dsquery|dsget|dsmod|dsadd|dsrm|csvde|ldifde|dnscmd|ntdsutil|certutil|certreq|bitsadmin|vssadmin|wbadmin|"
    r"dism|pktmon|fport|tracert|pathping|driverquery|fltmc|fsutil|openfiles|qwinsta|rwinsta|quser|"
    r"klist|vaultcmd|cmdkey|setx|ver|prompt|cmd|pushd|popd|rpcping|rundll32|regsvr32|mshta|msiexec|"
    r"makecab|expand|esentutl|cmstp|odbcconf|pcalua|regasm|regsvcs|wscript|cscript|csc|jsc|at|"
    r"for\s+/[flrd]|start\s+\\\\|"
    r"pslist|psloggedon|psloglist|psservice|psexec|pskill|psinfo|psfile|psgetsid|pspasswd|psping|"
    r"autorunsc|autoruns|sigcheck|handle|listdlls|tcpvcon|accesschk|accessenum|procdump|procmon|"
    r"sysmon|sdelete|logonsessions|pipelist|portmon|movefile|movelatr|pechksum|"
    r"sharphound|rubeus|mimikatz|"
    r"(?:privilege|sekurlsa|lsadump|kerberos|crypto|token|vault|dpapi|sid|iis|misc|process|service|ts|event|net|standard)::|"
    r"powershell|pwsh|import-module|gcm|gci|gwmi|gcim|iex|iwr|irm|\$psversiontable|"
    r"(?:get|set|new|remove|invoke|write|install|uninstall|restore|find|select|where|sort|format|"
    r"out|export|import|start|stop|restart|enable|disable|test|enter|exit|register|unregister|"
    r"update|clear|copy|move|rename|measure|compare|group|tee|resolve|resume|suspend|wait)-[a-z0-9]+|"
    r"ip\s+flow-|interface\s+(?:gigabitethernet|fastethernet|serial|vlan|loopback|tunnel)|show\s+(?:ip|interfaces|running-config|arp|mac|vlan)"
    r")(?:\.exe)?(?:\s|$|/|\||:)",
    re.I,
)


def _is_windows_or_powershell_command(cmd: str) -> bool:
    """
    Detect Windows CMD, Sysinternals, Active Directory, PowerShell, or Cisco IOS commands
    so `bash -n` does not falsely reject valid Windows/PowerShell syntax such as `%systemroot%`,
    `:(OI)(CI)F`, `wmic ... where (processid=...)`, or `@{Expression=...}`.
    """
    s = (cmd or "").strip()
    if not s:
        return False
    s_unwrapped = s.lstrip("(").strip()
    if _WINDOWS_OR_PS_CMD_RE.match(s_unwrapped):
        return True
    if re.match(r"^\$[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*", s):
        return True
    if re.search(r"%[a-zA-Z_][a-zA-Z0-9_]*%", s):
        return True
    if re.search(r"\b[A-Za-z]:\\|\\\\[A-Za-z0-9_.\-]+\\", s):
        return True
    if re.search(r":\((?:OI|CI|IO|NP|F|M|RX|R|W|D)\)|\$_\.|@\{|\bfindstr\b|\broute\s+print\b|\b(?:date|time)\s*/t\b", s, flags=re.I):
        return True
    return False


def apply_serial_pacing_transform(command: str) -> tuple[str, Optional[str]]:
    """
    Hardware UART Pacing Transformer for `tio` serial console commands:
    1. Automatically injects `-o 15 -O 120` (15ms per character, 120ms per line) into `tio --script`
       invocations when hardware output-delay flags are absent, preventing embedded UART FIFO overrun.
    2. Automatically inserts `msleep(450);` between back-to-back `write(...); write(...)` calls in Lua
       that lack an intermediate `msleep()`, `sleep()`, `expect()`, or `read()`.
    """
    cmd = (command or "").strip()
    if not cmd or not re.search(r"(?:^|\s|sudo\s+)tio\s+", cmd) or "--script" not in cmd:
        return cmd, None

    notes: List[str] = []
    paced = cmd

    # 1. Inject `-o 15 -O 120` hardware character/line pacing if not already specified
    if not re.search(r"(?:^|\s)(?:-o\s*\d+|--output-delay|-O\s*\d+|--output-line-delay)\b", paced):
        paced = re.sub(r"\btio\s+", "tio -o 15 -O 120 ", paced, count=1)
        notes.append("injected `-o 15 -O 120` UART char/line pacing")

    # 2. Insert `msleep(450); ` between back-to-back Lua `write(...); write(...)` calls with no delay
    prev = None
    while prev != paced:
        prev = paced
        paced = re.sub(
            r"(write\s*\(\s*(['\"])(?:\\.|(?!\2).)*?\2\s*\)\s*;)\s*(?=write\s*\()",
            r"\1 msleep(450); ",
            paced,
        )
    if paced != cmd and "msleep(450)" in paced and "msleep(450)" not in cmd:
        notes.append("inserted `msleep(450)` between consecutive `write()` calls")

    note_str = f"[META-MIND Serial Pacing Auto-Applied: {', '.join(notes)}]" if notes else None
    return paced, note_str


def verify_command_cegar(command: str) -> Dict[str, Any]:
    """
    Pre-execution formal & syntactic verifier for shell commands.
    Returns:
      {
        "blocked": bool,
        "reason": str,
        "counterexample": str,
        "suggested_fix": str,
        "advisories": List[str]
      }
    """
    cmd = (command or "").strip()
    from .vault_bridge import _get_isolation_filter

    iso_level, blue_ifaces = _get_isolation_filter()
    personality_mode = os.environ.get("CORA_PERSONALITY_MODE", "DEFAULT").strip().upper() or "DEFAULT"
    cache_key = f"{personality_mode}:{iso_level}:{','.join(blue_ifaces)}::{cmd}"
    if cache_key in _CEGAR_CMD_CACHE:
        return dict(_CEGAR_CMD_CACHE[cache_key])
    advisories: List[str] = []

    if not cmd:
        return {
            "blocked": False,
            "reason": "",
            "counterexample": "",
            "suggested_fix": "",
            "advisories": [],
        }

    is_win_ps = _is_windows_or_powershell_command(cmd)

    # --- HARD-BLOCK 1: Syntax Verification (`bash -n` for POSIX/Bash; Paren/Quote check for Windows CMD/PS) ---
    if is_win_ps:
        if cmd.count("(") != cmd.count(")"):
            return {
                "blocked": True,
                "reason": "Unbalanced parentheses in Windows CMD / PowerShell command.",
                "counterexample": f"`{cmd}` has {cmd.count('(')} '(' vs {cmd.count(')')} ')'.",
                "suggested_fix": "Ensure all ACL permission groups like `:(OI)(CI)(F)` and WMI/PowerShell expressions have matching parentheses.",
                "advisories": advisories,
            }
    elif _is_bash_n_available():
        # Fast-path syntax check for simple single-line commands with no quotes/parens/braces/subshells/redirections
        if "\n" not in cmd and not any(ch in cmd for ch in "\"'`()[]{}$<>\\|&;"):
            pass
        else:
            try:
                proc = subprocess.run(
                    ["bash", "-n"],
                    input=cmd,
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if proc.returncode != 0:
                    err = (proc.stderr or "Syntax error").strip()
                    return {
                        "blocked": True,
                        "reason": "Invalid Bash syntax detected by `bash -n` pre-execution check.",
                        "counterexample": err,
                        "suggested_fix": "Fix unmatched quotes, parentheses, or malformed bash tokens before re-running.",
                        "advisories": advisories,
                    }
            except Exception:
                pass

    # --- HARD-BLOCK 1B: Session Personality Mode Policy Enforcement (`ANALYST` / `NINJA`) ---
    mode_blk = _check_personality_mode_policy(cmd, is_target_only=False)
    if mode_blk:
        mode_blk["advisories"] = advisories
        return mode_blk

    # --- HARD-BLOCK 2: `tio` without `--script` or with Python inside `--script` ---
    if re.search(r"(?:^|\s|sudo\s+)tio\s+", cmd):
        if "--script" not in cmd and "-s" not in cmd and "--list" not in cmd and "--version" not in cmd and "--help" not in cmd:
            return {
                "blocked": True,
                "reason": "Interactive `tio` without `--script` will hang indefinitely in a non-interactive subprocess.",
                "counterexample": f"Command `{cmd}` opens an interactive serial session with no termination script.",
                "suggested_fix": "Use `tio --script \"expect('login: ', 5000); write('root\\\\r\\\\n'); sleep(1); exit()\" /dev/ttyUSB0` or a short `python3 -c 'import serial...'` one-liner.",
                "advisories": advisories,
            }
        if re.search(r"import\s+(serial|time|sys|os)", cmd):
            return {
                "blocked": True,
                "reason": "`tio --script` uses Lua inside tio, NOT Python (`import ...` is invalid inside `tio --script`).",
                "counterexample": "Detected Python `import` statement inside a `tio` command.",
                "suggested_fix": "Either use Lua functions inside `tio --script` (`expect()`, `write()`, `sleep()`, `exit()`) OR invoke `python3 -c \"import serial...\"` directly without `tio`.",
                "advisories": advisories,
            }
        write_payloads = [m.group(2) for m in re.finditer(r"write\s*\(\s*(['\"])(.*?)\1\s*\)", cmd)]
        tx_subcommands = 0
        for wp in write_payloads:
            wp_clean = re.sub(r"(?:\\r|\\n)+$", "", wp).strip()
            if wp_clean:
                tx_subcommands += max(1, len([p for p in re.split(r";|&&|\|\|", wp_clean) if p.strip()]))
        if tx_subcommands >= 5:
            return {
                "blocked": True,
                "reason": "Excessive multi-command burst inside a single `tio` serial session will overrun the UART RX FIFO buffer and drop the console connection.",
                "counterexample": f"Detected {tx_subcommands} chained commands inside `tio --script` (`{cmd[:110]}...`).",
                "suggested_fix": "Send only 1-2 short commands per `tio` session with hardware pacing (`tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\\\r\"); msleep(500); write(\"<single_cmd>\\\\r\"); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0`).",
                "advisories": advisories,
            }
        if tx_subcommands >= 3 or (len(write_payloads) >= 2 and not re.search(r"\b(?:msleep|sleep|expect)\s*\(", cmd)):
            advisories.append(
                "[CEGAR Serial Pacing Advisory] Sending multiple serial commands at once can overrun the UART RX buffer and drop `/dev/ttyUSB0`. "
                "Use `-o 15 -O 120`, `msleep(500)` between writes, and prefer 1 command per `tio` invocation."
            )

    # --- HARD-BLOCK 3: Unbounded `ping` without `-c`, `-w`, or `-n` ---
    if re.search(r"(?:^|&&|\|\||;|\bsudo\s+)\bping\b", cmd):
        if not re.search(r"\bping\b[^;&|]*\s[-/](?:[a-zA-Z]*[cwn])\b", cmd):
            ping_rep = "ping -n 3 -w 2000" if (os.name == "nt" or is_win_ps) else "ping -c 3 -W 2"
            return {
                "blocked": True,
                "reason": "Unbounded `ping` runs forever on Linux without `-c <count>` or `-w <deadline>`.",
                "counterexample": f"`{cmd}` lacks `-c` / `-n` packet count limit.",
                "suggested_fix": "Add `-c 3 -W 2` (Linux) or `-n 3 -w 2000` (Windows) to `ping`.",
                "repaired_command": re.sub(r"\bping\b", ping_rep, cmd, count=1),
                "advisories": advisories,
            }

    # --- HARD-BLOCK 3b: Unbounded `tcpdump` / `tshark` live capture without `-c <count>`, `-r <file>`, or `timeout` ---
    if re.search(r"(?:^|&&|\|\||;|\bsudo\s+)\b(?:tcpdump|tshark)\b", cmd):
        if not re.search(r"\btimeout\s+\d+|\s-(?:[a-zA-Z]*[cr]|G|W)\b", cmd):
            repaired_cap = re.sub(r"\b(tcpdump|tshark)\b", r"\1 -c 15", cmd, count=1)
            return {
                "blocked": True,
                "reason": "Unbounded `tcpdump` / `tshark` live packet capture hangs indefinitely without `-c <count>` or `timeout <sec>`.",
                "counterexample": f"`{cmd}` lacks `-c <count>` packet limit or `timeout` wrapper.",
                "suggested_fix": f"Add `-c 15` packet count limit (e.g., `{repaired_cap}`).",
                "repaired_command": repaired_cap,
                "advisories": advisories,
            }

    # --- HARD-BLOCK 4: Truncated or Malformed IPv4 Addresses / Targets ---
    bad_ip = _find_truncated_or_malformed_ipv4(cmd)
    if bad_ip:
        return {
            "blocked": True,
            "reason": "Truncated or malformed IPv4 address detected in command.",
            "counterexample": bad_ip,
            "suggested_fix": "Use the complete 4-octet IPv4 address (`A.B.C.D`) instead of a partial prefix.",
            "advisories": advisories,
        }

    # --- HARD-BLOCK 5: Network Isolation Policy Enforcement ---
    iso_blk = _check_network_isolation_policy(cmd, is_target_only=False)
    if iso_blk:
        iso_blk["advisories"] = advisories
        return iso_blk

    # --- ADVISORY CHECKS (Non-Blocking per Guardrail 1) ---
    m_route = re.search(
        r"\bip\s+route\s+(?:add|replace)\s+(\S+)\s+via\s+(\d+\.\d+\.\d+\.\d+)",
        cmd,
    )
    if m_route:
        dst_str, gw_str = m_route.group(1), m_route.group(2)
        try:
            gw_ip = ipaddress.ip_address(gw_str)
            local_nets = _get_local_ipv4_networks()
            if local_nets and not any(gw_ip in net for net in local_nets) and "onlink" not in cmd:
                advisories.append(
                    f"[CEGAR Advisory] Gateway `{gw_str}` for route `{dst_str}` is not in any currently active local IPv4 subnet "
                    f"({', '.join(str(n) for n in local_nets[:5])}). If the kernel returns `Nexthop has invalid gateway`, "
                    f"assign an IP in `{gw_str}`'s subnet first or append `dev <iface> onlink`."
                )
        except ValueError:
            pass

    if re.search(r"(?:^|\s)curl\s+", cmd) and "--connect-timeout" not in cmd and "-m " not in cmd and "--max-time" not in cmd:
        advisories.append(
            "[CEGAR Advisory] Consider adding `--connect-timeout 5 --max-time 15` to `curl` when probing potentially unreachable subnets."
        )

    res_ok = {
        "blocked": False,
        "reason": "Passed CEGAR pre-execution verification.",
        "counterexample": "",
        "suggested_fix": "",
        "advisories": advisories,
    }
    if len(_CEGAR_CMD_CACHE) < 1024:
        _CEGAR_CMD_CACHE[cache_key] = dict(res_ok)
    return res_ok


def run_cegar_reasoning(
    problem: str,
    candidate_commands: List[str] = None,
    export_to_vault: bool = True,
) -> Dict[str, Any]:
    """
    Runs Engine 12 (CEGAR Pre-Execution Verifier) over candidate commands extracted from the problem
    or explicitly provided.
    """
    if not candidate_commands:
        candidate_commands = re.findall(r"`([^`]+)`", problem)
        if not candidate_commands:
            ctx = resolve_problem_targets(problem)
            if ctx["os_family"] == "windows":
                candidate_commands = ["ipconfig /all", "route print", "arp -a"]
                if ctx["has_concrete_primary_ip"]:
                    candidate_commands.append(f"ping -n 3 -w 2000 {ctx['primary_ip']}")
            else:
                candidate_commands = ["ip -4 addr show", "ip route show", "ip neigh show"]
                if ctx["has_concrete_primary_ip"]:
                    candidate_commands.append(f"ping -c 3 -W 2 {ctx['primary_ip']}")

    hw = get_hardware_reasoning_limits()
    max_loops = int(hw.get("cegar_max_refinement_loops", 8))
    verifications = []
    seen_cmds = set()
    for cmd in candidate_commands[: max(6, max_loops)]:
        if cmd in seen_cmds:
            continue
        seen_cmds.add(cmd)
        res = verify_command_cegar(cmd)
        verifications.append({"command": cmd, **res})

    local_nets = [str(n) for n in _get_local_ipv4_networks()]
    md_lines = [
        "### CEGAR Pre-Execution Command Verifier",
        f"- **Active Local Subnets Checked**: `{', '.join(local_nets) if local_nets else 'None detected'}`",
        "- **Guardrail 1 Policy**: Hard-blocks syntax errors (`bash -n`), infinite non-TTY hangs (`tio` without `--script`, `ping` without `-c`), Python inside `tio --script`, and truncated/malformed IPv4 addresses (`http://172.24`, `ip route get 1`). All semantic route checks are non-blocking advisories.",
        "",
        "#### Verified Candidate Commands",
    ]
    for v in verifications:
        status = "BLOCKED" if v["blocked"] else "VERIFIED_SAFE"
        md_lines.append(f"- `{v['command']}` -> **{status}**")
        if v["blocked"]:
            md_lines.append(f"  - *Counterexample*: {v['counterexample']}")
            md_lines.append(f"  - *Refinement Fix*: {v['suggested_fix']}")
        for adv in v.get("advisories", []):
            md_lines.append(f"  - {adv}")

    markdown = "\n".join(md_lines)
    vault_path = None
    if export_to_vault:
        vault_path = write_reasoning_note(
            title=f"CEGAR Verification - {problem[:40]}",
            engine="cegar_verifier",
            content_md=markdown,
            tags=["cegar", "verification", "guardrail"],
        )

    return {
        "engine": "cegar_verifier",
        "local_subnets": local_nets,
        "verifications": verifications,
        "vault_note": vault_path,
        "markdown": markdown,
    }
