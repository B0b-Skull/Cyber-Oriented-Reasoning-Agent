"""
Engine 15: Hierarchical Tactical Markov Decision Process (H-MDP) & POMDP Policy Solver (`mdp_tactical.py`).
100% CPU execution (0 MB GPU VRAM), sub-3ms Bellman Value Iteration.

Models tactical decision-making across a 4-level factorized hierarchy:
    Level 1: Tactic (14 operational categories including Passive_Enum, Active_Enum,
             Protocol_Chaining, Covert_Infil, Covert_Exfil, Out-of-Band_Access, etc.)
    Level 2: Technique (specific method within the tactic)
    Level 3: Tool (host binary / utility)
    Level 4: Command Template (CEGAR-verified parameterized command)

Mathematical Formulation:
  - Tuple: M = <S, A, T, R, gamma>
  - State Space (S): Abstracted symbolic state fluents derived from Engine 9 (Temporal Fluents),
    Engine 13 (SyGuS), and POMDP belief weights from Engine 4 (Bayesian) & Engine 10 (Dempster-Shafer).
  - Transition Function T(s, a, s') = P(s' | s, a): Computed from Dirichlet pseudo-counts
    alpha(s, a, s') learned offline from TrainingDocuments/ (books, PDFs, playbooks) and updated
    online via Dirichlet feedback after every command execution in `agent-cli.py`.
  - Bellman Optimality Equation:
    Q*(s, a) = sum_{s'} T(s, a, s') * [ R(s, a, s') + gamma * max_{a'} Q*(s', a') ]
"""

from __future__ import annotations

import atexit
import datetime
import math
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .vault_bridge import (
    DATA_DIR,
    ensure_directories,
    get_hardware_reasoning_limits,
    load_json_state,
    render_command_template,
    resolve_problem_targets,
    save_json_data,
    save_json_state,
    save_reasoning_to_vault,
    slugify,
)

MDP_STORE_FILE = DATA_DIR / "mdp_transitions.json"

# 14 Canonical Tactic Categories (including user-specified categories)
TACTIC_CATEGORIES: List[str] = [
    "Passive_Enum",
    "Active_Enum",
    "Reconnaissance",
    "Enumeration",
    "Out-of-Band_Access",
    "Protocol_Chaining",
    "Initial_Access_Exploitation",
    "Defense_Evasion_Firewall",
    "Privilege_Escalation",
    "Credential_Access",
    "Lateral_Movement_Routing_Pivot",
    "Covert_Infil",
    "Covert_Exfil",
    "Post_Exploitation_Verification",
]

# State reward values V_base(s) representing proximity to operational goal achievement
STATE_BASE_REWARDS: Dict[str, float] = {
    "s_init_unknown": 0.0,
    "s_passive_topology_mapped": 18.0,
    "s_l2_l3_verified": 26.0,
    "s_active_services_enumerated": 38.0,
    "s_oob_serial_enumerated": 48.0,
    "s_protocol_chain_established": 62.0,
    "s_firewall_or_acl_unlocked": 68.0,
    "s_credentials_or_certs_acquired": 72.0,
    "s_covert_infil_channel_ready": 76.0,
    "s_initial_shell_or_api_access": 82.0,
    "s_interactive_tty_or_priv_escalated": 90.0,
    "s_cross_subnet_pivot_routed": 94.0,
    "s_covert_exfil_verified": 96.0,
    "s_goal_verified_complete": 100.0,
    "s_command_blocked_or_failed": -25.0,
}

# Seed Hierarchical MDP Transitions (Dirichlet priors alpha_success / alpha_fail)
DEFAULT_MDP_TRANSITIONS: List[Dict[str, Any]] = [
    {
        "id": "MDP_PASSIVE_IFACE_ARP",
        "pre_state": "s_init_unknown",
        "tactic": "Passive_Enum",
        "technique": "Local Interface, ARP Cache & Routing Table Inspection",
        "tool": "ip",
        "command_template": "ip -4 -br addr show; ip route show; ip neigh show",
        "post_state_success": "s_passive_topology_mapped",
        "post_state_fail": "s_init_unknown",
        "alpha_success": 18.0,
        "alpha_fail": 1.0,
        "step_cost": 1.0,
        "source": "seed_core",
    },
    {
        "id": "MDP_PASSIVE_SOCKET_INSPECT",
        "pre_state": "s_init_unknown",
        "tactic": "Passive_Enum",
        "technique": "Passive Local Socket, Tunnel & Listening Port Audit",
        "tool": "ss",
        "command_template": "ss -tulpn; ip -d link show",
        "post_state_success": "s_passive_topology_mapped",
        "post_state_fail": "s_init_unknown",
        "alpha_success": 15.0,
        "alpha_fail": 1.0,
        "step_cost": 1.0,
        "source": "seed_core",
    },
    {
        "id": "MDP_ACTIVE_L2_L3_ROUTE_PROBE",
        "pre_state": "s_passive_topology_mapped",
        "tactic": "Active_Enum",
        "technique": "Kernel Route Selection & L2 Neighbor Reachability Probe",
        "tool": "ip",
        "command_template": "ip route get {target_ip}; ping -c 2 -W 1 {target_ip}",
        "post_state_success": "s_l2_l3_verified",
        "post_state_fail": "s_passive_topology_mapped",
        "alpha_success": 16.0,
        "alpha_fail": 2.0,
        "step_cost": 1.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_ACTIVE_TCP_SERVICE_SWEEP",
        "pre_state": "s_l2_l3_verified",
        "tactic": "Active_Enum",
        "technique": "Targeted Multi-Port TCP & TLS Service Enumeration",
        "tool": "nmap",
        "command_template": "nmap -Pn -sT -p 22,80,443,5000,6000,8000,8080,8443,9000 {target_ip}",
        "post_state_success": "s_active_services_enumerated",
        "post_state_fail": "s_l2_l3_verified",
        "alpha_success": 14.0,
        "alpha_fail": 4.0,
        "step_cost": 2.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_OOB_UART_SERIAL_AUDIT",
        "pre_state": "s_l2_l3_verified",
        "tactic": "Out-of-Band_Access",
        "technique": "Non-Interactive UART Serial Console Socket & Firewall Enumeration",
        "tool": "tio",
        "command_template": (
            "tio -b 115200 --mute --script-run once --script "
            "'write(\"ip -4 addr; ss -tulpn; iptables -L -n\\r\"); while read(4096, 500) > 0 do end; exit(0)' /dev/ttyUSB0"
        ),
        "post_state_success": "s_oob_serial_enumerated",
        "post_state_fail": "s_l2_l3_verified",
        "alpha_success": 22.0,
        "alpha_fail": 1.0,
        "step_cost": 1.2,
        "source": "seed_core",
    },
    {
        "id": "MDP_DEFENSE_FIREWALL_UNLOCK",
        "pre_state": "s_oob_serial_enumerated",
        "tactic": "Defense_Evasion_Firewall",
        "technique": "Out-of-Band Serial Firewall INPUT Acceptance & IPv4 Forwarding Enable",
        "tool": "tio",
        "command_template": (
            "tio -b 115200 --mute --script-run once --script "
            "'write(\"iptables -I INPUT -j ACCEPT; sysctl -w net.ipv4.ip_forward=1\\r\"); while read(4096, 500) > 0 do end; exit(0)' /dev/ttyUSB0"
        ),
        "post_state_success": "s_firewall_or_acl_unlocked",
        "post_state_fail": "s_oob_serial_enumerated",
        "alpha_success": 19.0,
        "alpha_fail": 1.5,
        "step_cost": 1.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_CRED_MTLS_CERT_DISCOVERY",
        "pre_state": "s_active_services_enumerated",
        "tactic": "Credential_Access",
        "technique": "Local PKI X.509 Client Certificate & Key Pair Discovery",
        "tool": "openssl",
        "command_template": "find ~/Projects -iname '*.crt' -o -iname '*.pem' -o -iname '*.key' 2>/dev/null | head -n 30",
        "post_state_success": "s_credentials_or_certs_acquired",
        "post_state_fail": "s_active_services_enumerated",
        "alpha_success": 16.0,
        "alpha_fail": 2.0,
        "step_cost": 1.2,
        "source": "seed_core",
    },
    {
        "id": "MDP_PROTOCOL_CHAIN_MTLS_HTTP",
        "pre_state": "s_credentials_or_certs_acquired",
        "tactic": "Protocol_Chaining",
        "technique": "Chained TLS Client-Cert Handshake + HTTP API Endpoint Enumeration",
        "tool": "curl",
        "command_template": "curl -sS -k -L -i --connect-timeout 5 https://{target_ip}/",
        "post_state_success": "s_protocol_chain_established",
        "post_state_fail": "s_credentials_or_certs_acquired",
        "alpha_success": 17.0,
        "alpha_fail": 2.0,
        "step_cost": 1.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_PROTOCOL_CHAIN_OOB_TO_API",
        "pre_state": "s_firewall_or_acl_unlocked",
        "tactic": "Protocol_Chaining",
        "technique": "Serial OOB Service Unlock Chained into Direct HTTP/HTTPS API Probe",
        "tool": "curl",
        "command_template": "curl -sS -k -L -i --connect-timeout 5 http://{target_ip}/",
        "post_state_success": "s_initial_shell_or_api_access",
        "post_state_fail": "s_firewall_or_acl_unlocked",
        "alpha_success": 20.0,
        "alpha_fail": 1.5,
        "step_cost": 1.2,
        "source": "seed_core",
    },
    {
        "id": "MDP_COVERT_INFIL_STAGE",
        "pre_state": "s_protocol_chain_established",
        "tactic": "Covert_Infil",
        "technique": "Authenticated API Configuration / Encapsulated Payload Staging Verification",
        "tool": "curl",
        "command_template": "curl -sS -k -X OPTIONS -i https://{target_ip}/",
        "post_state_success": "s_covert_infil_channel_ready",
        "post_state_fail": "s_protocol_chain_established",
        "alpha_success": 14.0,
        "alpha_fail": 2.0,
        "step_cost": 1.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_INITIAL_ACCESS_API",
        "pre_state": "s_covert_infil_channel_ready",
        "tactic": "Initial_Access_Exploitation",
        "technique": "Authenticated Management API Execution & Session Establishment",
        "tool": "curl",
        "command_template": "curl -sS -k -i https://{target_ip}/status",
        "post_state_success": "s_initial_shell_or_api_access",
        "post_state_fail": "s_covert_infil_channel_ready",
        "alpha_success": 15.0,
        "alpha_fail": 2.0,
        "step_cost": 1.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_PRIV_ESC_TTY_AND_SUID",
        "pre_state": "s_initial_shell_or_api_access",
        "tactic": "Privilege_Escalation",
        "technique": "Interactive PTY Upgrade & Privileged Binary / Service Permission Audit",
        "tool": "python3",
        "command_template": "id; uname -a; sudo -l 2>/dev/null",
        "post_state_success": "s_interactive_tty_or_priv_escalated",
        "post_state_fail": "s_initial_shell_or_api_access",
        "alpha_success": 16.0,
        "alpha_fail": 2.0,
        "step_cost": 1.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_LATERAL_CROSS_SUBNET_ROUTE",
        "pre_state": "s_firewall_or_acl_unlocked",
        "tactic": "Lateral_Movement_Routing_Pivot",
        "technique": "Cross-Subnet Static Gateway Route Injection & ICMP Reachability Verification",
        "tool": "ip",
        "command_template": "sudo ip route replace {remote_subnet} via {target_ip} && ping -c 2 -W 1 {secondary_target_ip}",
        "post_state_success": "s_cross_subnet_pivot_routed",
        "post_state_fail": "s_firewall_or_acl_unlocked",
        "alpha_success": 18.0,
        "alpha_fail": 1.5,
        "step_cost": 1.4,
        "source": "seed_core",
    },
    {
        "id": "MDP_COVERT_EXFIL_TELEMETRY_CHECK",
        "pre_state": "s_interactive_tty_or_priv_escalated",
        "tactic": "Covert_Exfil",
        "technique": "Low-Footprint Structured Config & State Digest Collection over Approved Channel",
        "tool": "curl",
        "command_template": "curl -sS -k -i https://{target_ip}/logging",
        "post_state_success": "s_covert_exfil_verified",
        "post_state_fail": "s_interactive_tty_or_priv_escalated",
        "alpha_success": 14.0,
        "alpha_fail": 2.0,
        "step_cost": 1.5,
        "source": "seed_core",
    },
    {
        "id": "MDP_POST_EXPLOIT_VERIFY_A",
        "pre_state": "s_cross_subnet_pivot_routed",
        "tactic": "Post_Exploitation_Verification",
        "technique": "End-to-End Multi-Hop Route & Target Service Health Verification",
        "tool": "curl",
        "command_template": "ip route get {secondary_target_ip}; ping -c 2 -W 1 {secondary_target_ip}",
        "post_state_success": "s_goal_verified_complete",
        "post_state_fail": "s_cross_subnet_pivot_routed",
        "alpha_success": 20.0,
        "alpha_fail": 1.0,
        "step_cost": 1.0,
        "source": "seed_core",
    },
    {
        "id": "MDP_POST_EXPLOIT_VERIFY_B",
        "pre_state": "s_covert_exfil_verified",
        "tactic": "Post_Exploitation_Verification",
        "technique": "Objective Proof & Vault Artifact Verification",
        "tool": "ip",
        "command_template": "ip -4 -br addr show; ss -tulpn",
        "post_state_success": "s_goal_verified_complete",
        "post_state_fail": "s_covert_exfil_verified",
        "alpha_success": 18.0,
        "alpha_fail": 1.0,
        "step_cost": 1.0,
        "source": "seed_core",
    },
]


def _split_unquoted_segments(cmd: str) -> List[str]:
    """Split a shell command string on `&&`, `||`, or `;` only when outside single/double quotes."""
    segments: List[str] = []
    cur: List[str] = []
    in_sq = False
    in_dq = False
    i = 0
    n = len(cmd)
    while i < n:
        ch = cmd[i]
        if ch == "\\" and i + 1 < n and not in_sq:
            cur.append(ch)
            cur.append(cmd[i + 1])
            i += 2
            continue
        if ch == "'" and not in_dq:
            in_sq = not in_sq
            cur.append(ch)
            i += 1
            continue
        if ch == '"' and not in_sq:
            in_dq = not in_dq
            cur.append(ch)
            i += 1
            continue
        if not in_sq and not in_dq:
            if cmd[i : i + 2] in ("&&", "||"):
                seg = "".join(cur).strip()
                if seg:
                    segments.append(seg)
                cur = []
                i += 2
                continue
            if ch == ";":
                seg = "".join(cur).strip()
                if seg:
                    segments.append(seg)
                cur = []
                i += 1
                continue
        cur.append(ch)
        i += 1
    tail = "".join(cur).strip()
    if tail:
        segments.append(tail)
    return segments


def classify_tactic_category(text: str, cmd: str = "") -> Tuple[str, str, str]:
    """
    Classify a command and its surrounding documentation context into:
      (tactic_category, technique_name, tool_binary)
    Covers all 14 canonical tactic categories including Covert_Exfil, Covert_Infil,
    Active_Enum, Passive_Enum, and Protocol_Chaining across Linux, Solaris, Windows CMD,
    Sysinternals, Active Directory, PowerShell, and network appliances.
    """
    combined = f"{text} {cmd}".lower()
    cmd_clean = cmd.strip()
    cmd_low = cmd_clean.lower()

    # Extract clean tool binary name (skipping leading `cd ... &&`, `echo ...;`, `sudo`, `env`, `timeout`)
    segments = _split_unquoted_segments(cmd_clean) or ([cmd_clean] if cmd_clean else [])
    tool_bin = "sh"
    for idx, seg in enumerate(segments):
        unwrapped = re.sub(r"^\$[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*", "", seg).lstrip("(").strip()
        tokens = unwrapped.split()
        while tokens and (
            tokens[0].lower() in ("sudo", "time", "timeout", "env", "nohup")
            or "=" in tokens[0]
            or (tokens[0].isdigit() and len(tokens) > 1)
        ):
            tokens.pop(0)
        if not tokens:
            continue
        first_tok = tokens[0].split("|")[0].split(";")[0].strip("()\"'")
        b = re.split(r"[\\/]", first_tok)[-1].lower()
        if b.endswith(".exe"):
            b = b[:-4]
        if b in ("cd", "echo", "printf", "export", "true") and len(segments) > 1 and idx < len(segments) - 1:
            tool_bin = b
            continue
        tool_bin = b
        break

    # 1. Out-of-Band Access (Serial / UART / BMC / Console) — must match the command itself, not unrelated PDF prose
    if any(
        k in cmd_low
        for k in ("tio ", "/dev/ttyusb", "/dev/ttyacm", "/dev/ttys", "minicom", "stty ", "plink -serial", "serialport", "ipmitool")
    ) or (tool_bin in ("tio", "minicom", "stty", "ipmitool")):
        return ("Out-of-Band_Access", "UART/Serial Console Out-of-Band Enumeration & Control", tool_bin or "tio")

    # 2. Covert Exfil — match command markers in `cmd_low` so adjacent PDF prose doesn't misclassify unrelated tools
    if any(
        k in cmd_low
        for k in (
            "iodine",
            "dnscat",
            "ptunnel",
            "bitsadmin /transfer",
            "vssadmin create shadow",
            "ntdsutil",
            "reg save hklm\\sam",
            "reg save hklm\\system",
            "reg save hklm\\security",
        )
    ) or any(k in combined for k in ("covert_exfil", "dns tunnel", "icmp tunnel", "data transfer out")):
        return ("Covert_Exfil", "Encapsulated / Low-Signature Data Telemetry Transfer", tool_bin)

    # 3. Covert Infil — match command markers in `cmd_low`
    if any(
        k in cmd_low
        for k in (
            "certutil -urlcache",
            "certutil.exe -urlcache",
            "bitsadmin /addfile",
            "invoke-webrequest",
            "wget -q",
            "curl -o /tmp",
            "scp ",
            "base64 -d",
        )
    ) or any(k in combined for k in ("covert_infil", "stage payload", "upload binary")):
        return ("Covert_Infil", "Staged Artifact / Encapsulated Ingress Delivery", tool_bin)

    # 4. Protocol Chaining — match command markers in `cmd_low`
    if (
        any(
            k in cmd_low
            for k in (
                "socat ",
                "proxychains",
                "ssh -l",
                "ssh -d",
                "ssh -r",
                "chisel",
                "stunnel",
                "--cert ",
                "--cacert ",
                "s_client",
                "netsh interface portproxy",
                "enter-pssession",
                "new-pssession",
                "invoke-command -computername",
            )
        )
        or any(k in combined for k in ("protocol_chain", "protocol chain"))
        or ("&&" in cmd_low and len({w for w in ("curl", "tio", "openssl", "ip", "ssh", "socat") if re.search(rf"\b{w}\b", cmd_low)}) >= 2)
    ):
        return ("Protocol_Chaining", "Multi-Protocol Handshake & Tunnel Relay Chaining", tool_bin)

    # 5. Lateral Movement & Routing Pivot (including remote Windows WMI/RPC/SCM/SMB execution & route manipulation)
    if any(
        k in cmd_low
        for k in (
            "ip route add",
            "ip route replace",
            "ip rule",
            "route add ",
            "route -p add",
            "route change ",
            "psexec",
            "smbexec",
            "wmiexec",
            "atexec",
            "dcomexec",
            "evil-winrm",
            "xfreerdp",
            "rdesktop",
            "wmic /node:",
            "tasklist /s ",
            "taskkill /s ",
            "taskkill /pid ",
            "pslist \\\\",
            "pskill - \\\\",
            "pskill \\\\",
            "sc \\\\",
            "net use \\\\",
            "-computername ",
            "-computer ",
            "telnet ",
        )
    ) or any(
        k in combined
        for k in (
            "ip_forward",
            "masquerade",
            "postrouting",
            "pivot",
            "cross-subnet",
            "lateral",
        )
    ):
        return ("Lateral_Movement_Routing_Pivot", "Remote Host Execution, L2/L3 Route Injection & Subnet Pivot", tool_bin)

    # 6. Defense Evasion / Firewall / Audit / Boot / LOLBin & System File Protection Manipulation
    if any(
        k in cmd_low
        for k in (
            "iptables",
            "ip6tables",
            "nft ",
            "ufw ",
            "firewall-cmd",
            "ipfstat",
            "ipf ",
            "netsh advfirewall",
            "netsh firewall",
            "auditpol",
            "auditctl",
            "setenforce",
            "bcdedit",
            "sfc ",
            "movelatr",
            "pechksum",
            "dllcache",
            "sfcfiles",
            "unset histfile",
            "wevtutil cl",
            "attrib -s -h",
            "attrib +h",
            "sdelete",
            "ntfsdisablelastaccessupdate",
            "copy %systemroot%\\system32\\",
            "del %systemroot%\\system32\\",
            "ren c:\\windows\\",
            "rename %systemroot%\\",
            "rundll32",
            "regsvr32",
            "mshta",
            "cmstp",
            "odbcconf",
            "regasm",
            "regsvcs",
            "pcalua",
            "installutil",
        )
    ) or any(k in combined for k in ("iptables", "nft ", "ufw ", "firewall", "setenforce", "apparmor", "lolbin", "applocker")):
        return ("Defense_Evasion_Firewall", "Host Firewall, Audit Policy, LOLBin & Integrity Control Adjustment", tool_bin)

    # 7. Privilege Escalation & ACL / Permission / Service Modification
    if any(
        k in cmd_low
        for k in (
            "takeown",
            "icacls",
            "cacls",
            "accesschk",
            "sc config",
            "sc sdset",
            "sc create",
            "net localgroup administrators",
            "net localgroup \"power users\"",
            "dsmod group",
            "runas",
            "chmod ",
            "chown ",
            "chgrp ",
            "-perm -u=s",
            "/etc/sudoers",
            "sudo -l",
            "token::elevate",
            "privilege::debug",
        )
    ) or any(
        k in combined
        for k in (
            "powerup",
            "invoke-allchecks",
            "serviceabuse",
            "unquoted",
            "pty.spawn",
            "stty raw",
            "sudo -l",
            "suid",
            "setuid",
            "privilege escalation",
            "privesc",
        )
    ):
        return ("Privilege_Escalation", "ACL/Permission Modification, Service Abuse & Privilege Escalation", tool_bin)

    # 8. Credential Access & Account/Identity Management
    if any(
        k in cmd_low
        for k in (
            "get-credential",
            "mimikatz",
            "sekurlsa::",
            "lsadump::",
            "kerberos::",
            "vault::",
            "dpapi::",
            "crypto::",
            "rubeus",
            "hashcat",
            "john ",
            "unshadow",
            "hydra ",
            "medusa ",
            "ncrack",
            "crowbar",
            "responder",
            "secretsdump",
            "getnpusers",
            "getuserspns",
            "ticketer",
            "ntlmrelayx",
            "aircrack-ng",
            "cmdkey",
            "vaultcmd",
            "procdump",
            "net user ",
            "dsadd user",
            "dsmod user",
            "/etc/shadow",
            "/var/adm/sulog",
            "find / -name password",
        )
    ) or re.search(r"\bklist\b", cmd_low) or any(
        k in combined
        for k in (
            ".crt",
            ".pem",
            ".key",
            "pkcs12",
            "x509",
            "password",
            "credential",
            "hash",
            "shadow",
            "keepass",
            "bearer",
        )
    ):
        return ("Credential_Access", "Credential, Account, Kerberos Ticket, Hash Cracking & Certificate Operations", tool_bin)

    # 9. Initial Access / Exploitation (SQLi, Payload Generation, API injection, Web)
    if any(
        k in cmd_low
        for k in (
            "sqlmap",
            "msfvenom",
            "msfconsole",
            "searchsploit",
            "wpscan",
        )
    ) or any(
        k in combined
        for k in (
            "sqlmap",
            "union select",
            "sql injection",
            "sqli",
            "informix",
            "sysmaster",
            "netsparker",
            "-x post",
            "exploit",
        )
    ):
        return ("Initial_Access_Exploitation", "Structured Query / Payload / Web API Endpoint Exploitation", tool_bin)

    # 10. Passive Enumeration (Local Host Survey, Registry, Process, Socket, File & Log Triage)
    if any(
        k in cmd_low
        for k in (
            "ip -br",
            "ip addr",
            "ip -4 addr",
            "ip route show",
            "ip neigh show",
            "ss -",
            "netstat",
            "ifconfig",
            "ipconfig ",
            "arp -",
            "route print",
            "route -",
            "nbtstat",
            "tasklist",
            "pslist",
            "psloggedon",
            "psloglist",
            "psservice",
            "psinfo",
            "psfile",
            "psgetsid",
            "listdlls",
            "handle",
            "autorunsc",
            "sigcheck",
            "tcpvcon",
            "fport",
            "systeminfo",
            "wmic ",
            "reg query",
            "dir ",
            "forfiles",
            "findstr",
            "wevtutil ",
            "net start",
            "net share",
            "net session",
            "net statistics",
            "net use",
            "net users",
            "net localgroup",
            "net accounts",
            "net view",
            "sc query",
            "sc qc",
            "schtasks",
            "gpresult",
            "driverquery",
            "fltmc",
            "date /t",
            "time /t",
            "time/t",
            "prompt ",
            "type ",
            "get-childitem",
            "gci ",
            "get-process",
            "get-service",
            "get-wmiobject",
            "gwmi ",
            "get-ciminstance",
            "gcim ",
            "get-hotfix",
            "get-eventlog",
            "get-winevent",
            "get-acl",
            "get-host",
            "get-module",
            "get-command",
            "gcm ",
            "get-help",
            "get-alias",
            "get-psprovider",
            "get-executionpolicy",
            "get-windowspackage",
            "$psversiontable",
            "cat /etc/",
            "cat /proc/",
            "cat /var/",
            "cat /root/",
            "ls -",
            "ls /etc/",
            "ps -",
            "ps aux",
            "ps awx",
            "ptree",
            "pfiles",
            "fuser",
            "pwdx",
            "lsof",
            "lsmod",
            "modinfo",
            "psrinfo",
            "prtconf",
            "prtdiag",
            "sysdef",
            "vmstat",
            "uptime",
            "dmesg",
            "sestatus",
            "getenforce",
            "ausearch",
            "aureport",
            "crontab -l",
            "svcs",
            "inetadm",
            "chkconfig",
            "service --status-all",
            "df -",
            "stat ",
            "file ",
            "strings ",
            "objdump ",
            "readelf ",
            "ldd ",
            "binwalk",
            "exiftool",
            "volatility",
            "vol.py",
            "yara ",
            "osqueryi",
            "splunk ",
            "find /",
            "find .",
            "find ~",
            "grep ",
            "sed ",
            "awk ",
            "tail ",
            "head ",
            "p0f",
            "tshark -r",
            "tcpdump -r",
            "ip flow-",
        )
    ) or cmd_low in (
        "systeminfo",
        "tasklist",
        "ipconfig",
        "listdlls",
        "psloggedon",
        "fport",
        "ver",
        "date",
        "uptime",
        "vmstat",
        "lsmod",
        "lsof",
        "dmesg",
        "sestatus",
        "getenforce",
        "aureport",
        "history",
        "w",
        "last",
        "who",
        "mount",
        "run-parts",
        "$psversiontable",
        "osqueryi",
    ):
        return ("Passive_Enum", "Local Host State, Memory/Artifact Forensics, Process, Registry & Socket Survey", tool_bin)

    # 11. Active Enumeration (Active Network, Cloud, Wireless, Domain/AD & Service Probing)
    if any(
        k in cmd_low
        for k in (
            "dsquery",
            "dsget",
            "nltest",
            "csvde",
            "ldifde",
            "sharphound",
            "rpcinfo",
            "rpcping",
            "showmount",
            "smbclient",
            "rpcclient",
            "nbtscan",
            "nmblookup",
            "tracert",
            "traceroute",
            "pathping",
            "tcpdump",
            "tshark",
            "snort",
            "ping ",
            "aws ",
            "az ",
            "gcloud ",
            "gsutil ",
            "kubectl ",
            "docker ",
            "adb ",
            "frida",
            "airmon-ng",
            "airodump-ng",
            "feroxbuster",
            "wfuzz",
        )
    ) or any(
        k in combined
        for k in (
            "nmap",
            "masscan",
            "nikto",
            "gobuster",
            "dirb",
            "ffuf",
            "enum4linux",
            "snmpwalk",
            "onesixtyone",
            "arping",
            "ping -c",
            "curl -i",
            "curl -s",
        )
    ):
        return ("Active_Enum", "Active Network, Cloud, Directory Service & Endpoint Probing", tool_bin)

    # 12. Post-Exploitation Verification
    if any(k in cmd_low for k in ("whoami", "id;", "id ", "hostname", "uname", "groups", "runlevel", "echo $0")) or any(
        k in combined for k in ("whoami", "id;", "hostname", "uname -a", "verify")
    ):
        return ("Post_Exploitation_Verification", "Post-Action Host Identity, Privilege & Objective Verification", tool_bin)

    # 13. Reconnaissance / General Enumeration
    if any(k in combined for k in ("whois", "dig ", "nslookup", "host ", "shodan", "greynoise", "recon", "osint")):
        return ("Reconnaissance", "Domain, DNS, OSINT & Target Footprint Reconnaissance", tool_bin)

    return ("Enumeration", "General System & Service Enumeration", tool_bin)


_MDP_STORE_RAM_CACHE: Dict[str, Any] = {"mtime": -1.0, "data": None}


def load_or_init_mdp_store() -> Dict[str, Any]:
    """Load `Reasoning/data/mdp_transitions.json` or initialize with default 14-tactic transitions (mtime-cached in RAM)."""
    ensure_directories()
    try:
        cur_mtime = os.path.getmtime(MDP_STORE_FILE) if os.path.exists(MDP_STORE_FILE) else -1.0
    except OSError:
        cur_mtime = -1.0
    if cur_mtime > 0 and _MDP_STORE_RAM_CACHE["mtime"] == cur_mtime and _MDP_STORE_RAM_CACHE["data"] is not None:
        return _MDP_STORE_RAM_CACHE["data"]

    data = load_json_state(str(MDP_STORE_FILE), default={})
    if not isinstance(data, dict) or not data.get("transitions"):
        now_iso = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
        data = {
            "version": "1.1.0",
            "updated_at": now_iso,
            "discount_gamma": 0.92,
            "tactic_categories": TACTIC_CATEGORIES,
            "state_rewards": STATE_BASE_REWARDS,
            "transitions": DEFAULT_MDP_TRANSITIONS,
            "online_updates_count": 0,
        }
        save_json_state(str(MDP_STORE_FILE), data)
    else:
        # Ensure all 14 tactic categories are registered
        existing_cats = set(data.get("tactic_categories", []))
        for c in TACTIC_CATEGORIES:
            if c not in existing_cats:
                data.setdefault("tactic_categories", []).append(c)
        data.setdefault("state_rewards", {}).update(STATE_BASE_REWARDS)
        # Filter out any natural-language prose lines, PDF citations, or legacy hardcoded subnet strings
        prose_re = re.compile(
            r"^[a-z0-9_.\-/]+\s+(?:is|are|was|were|can|will|should|allows|provides|uses|works|supports|helps|means|has|have|or\s+echo|command\.)\b",
            re.I,
        )
        dummy_ip_re = re.compile(r"\b(?:1\.1\.1\.1|2\.2\.2\.2|(?:192\.16[8]|172\.24)\.11\.13|(?:192\.16[8]|172\.24)\.1\.249)\b")
        raw_trs = data.get("transitions", [])
        clean_trs = []
        modified = False
        seed_map = {t["id"]: t for t in DEFAULT_MDP_TRANSITIONS}
        non_exec_exts = (".txt", ".log", ".md", ".json", ".xml", ".csv", ".yml", ".yaml", ".ini", ".cfg", ".conf", ".pdf", ".docx", ".html", ".htm")
        for tr in raw_trs:
            cmd_tpl = str(tr.get("command_template", "")).strip()
            tool_s = str(tr.get("tool", "")).strip().lower()
            is_seed = tr.get("source") == "seed_core"
            if (
                prose_re.match(cmd_tpl)
                or tool_s.endswith(non_exec_exts)
                or (cmd_tpl.startswith("./") and cmd_tpl.lower().endswith(non_exec_exts))
                or (not is_seed and tool_s in (".", "echo", "cd", "type", "true", "false") and "/proc/" not in cmd_tpl and "/sys/" not in cmd_tpl)
                or "[accessed:" in cmd_tpl.lower()
                or re.match(r"^echo\s+\d+$", cmd_tpl, re.I)
            ):
                modified = True
                continue
            # Ensure trained tcpdump commands include a bounded `-c 15` packet limit so they never hang
            if tool_s == "tcpdump" and not re.search(r"\s-c\s*\d+\b", cmd_tpl):
                tr = dict(tr)
                cmd_tpl = re.sub(r"\btcpdump\b", "tcpdump -c 15", cmd_tpl, count=1)
                tr["command_template"] = cmd_tpl
                modified = True
            # Parameterize hardcoded textbook dummy IPs (`1.1.1.1`, `2.2.2.2`, etc.)
            if not is_seed and dummy_ip_re.search(cmd_tpl):
                tr = dict(tr)
                cmd_tpl = dummy_ip_re.sub("{target_ip}", cmd_tpl)
                tr["command_template"] = cmd_tpl
                modified = True
            # Re-classify any non-seed transition that was falsely tagged Out-of-Band_Access due to surrounding PDF prose
            if (
                not is_seed
                and tr.get("tactic") == "Out-of-Band_Access"
                and not re.search(r"\b(?:tio|ttyusb\d*|ttyacm\d*|ttys\d*|minicom|stty|serial|ipmitool|com[1-9]\d*)\b", cmd_tpl.lower())
            ):
                new_tactic, new_tech, new_tool = classify_tactic_category("", cmd_tpl)
                tr = dict(tr)
                tr["tactic"] = new_tactic
                tr["technique"] = new_tech
                tr["tool"] = new_tool
                modified = True
            if tr.get("id") in seed_map and tr.get("command_template") != seed_map[tr["id"]]["command_template"]:
                tr = dict(tr)
                tr["command_template"] = seed_map[tr["id"]]["command_template"]
                modified = True
            elif "<REMOTE_SUBNET>" in cmd_tpl:
                tr = dict(tr)
                tr["command_template"] = cmd_tpl.replace("<REMOTE_SUBNET>", "{remote_subnet}")
                modified = True
            clean_trs.append(tr)
        if modified or len(clean_trs) != len(raw_trs):
            data["transitions"] = clean_trs
            save_json_state(str(MDP_STORE_FILE), data)

    try:
        _MDP_STORE_RAM_CACHE["mtime"] = os.path.getmtime(MDP_STORE_FILE) if os.path.exists(MDP_STORE_FILE) else 0.0
    except OSError:
        _MDP_STORE_RAM_CACHE["mtime"] = 0.0
    _MDP_STORE_RAM_CACHE["data"] = data
    return data


def infer_current_mdp_state(
    problem: str = "",
    observed_evidence: Optional[Dict[str, bool]] = None,
    has_serial_oob: bool = True,
) -> Tuple[str, List[str]]:
    """
    Map live Problem Context + Engine 9 Temporal Fluents + Observed Evidence
    into the current Markov state `s_t in S` and return `(current_state, active_fluents_summary)`.
    """
    prob_low = (problem or "").lower()
    ev = dict(observed_evidence or {})
    fluent_tags: List[str] = []

    try:
        from .temporal_fluents import load_fluent_state

        f_store = load_fluent_state()
        for k, v in (f_store.get("fluents") or {}).items():
            if isinstance(v, dict) and v.get("status") in ("ACTIVE", "HOLDING"):
                f_name = v.get("fluent") or k
                f_val = v.get("value") or v.get("attribute") or "HOLDING"
                fluent_tags.append(f"{f_name}={f_val}")
    except Exception:
        pass

    joined_fluents = " ".join(fluent_tags).lower()

    if "goal_achieved" in prob_low or "verified_complete" in prob_low:
        return "s_goal_verified_complete", fluent_tags
    if "exfil" in prob_low:
        return "s_interactive_tty_or_priv_escalated", fluent_tags
    if (
        "firewall_unlocked" in joined_fluents
        or "firewall_input_policy" in joined_fluents
        or "windows_firewall_state" in joined_fluents
        or "iptables -i input -j accept" in prob_low
        or "netsh advfirewall" in prob_low
    ):
        return "s_firewall_or_acl_unlocked", fluent_tags
    if (
        "serial_enumerated" in joined_fluents
        or "oob_serial_console_session" in joined_fluents
        or ("ss -tulpn" in prob_low and "ttyusb" in prob_low)
    ):
        return "s_oob_serial_enumerated", fluent_tags
    if "privesc" in prob_low or "privilege" in prob_low or "powerup" in prob_low or "pty.spawn" in prob_low or "interactive tty" in prob_low:
        return "s_initial_shell_or_api_access", fluent_tags
    if "infil" in prob_low or "stage" in prob_low or "injection" in prob_low or "command injection" in prob_low:
        return "s_protocol_chain_established", fluent_tags
    if (
        "mtls" in prob_low
        or "client.crt" in prob_low
        or "certificate" in prob_low
        or "443" in prob_low
        or "https://" in prob_low
        or ev.get("http_401_or_403_or_tls_alert")
        or ev.get("http_401_or_403_auth")
        or ev.get("tls_cert_or_sni_mismatch")
        or "http_endpoint_status=" in joined_fluents
    ):
        return "s_credentials_or_certs_acquired", fluent_tags
    if (
        ev.get("icmp_ping_responds")
        or ev.get("ping_icmp_ok")
        or ev.get("arp_resolved_mac_present")
        or ev.get("arp_resolved_ok")
        or ev.get("alt_port_open_in_scan")
        or ev.get("nonstandard_port_open")
        or ev.get("curl_exit_7_Immediate_refused")
        or "icmp_reachability=reachable" in joined_fluents
        or "arp_reachability=reachable" in joined_fluents
        or "tcp_service_ports=" in joined_fluents
        or "exit 7" in prob_low
        or "connection refused" in prob_low
        or "ttyusb" in prob_low
        or "ttyacm" in prob_low
        or "arp_l2_" in joined_fluents
        or (has_serial_oob and bool(re.search(r"\b(?:serial|tio|uart|oob)\b|unreachable|refused|timed out|exit 7|exit 28", prob_low)))
    ):
        return "s_l2_l3_verified", fluent_tags
    if (
        "route" in prob_low
        or "subnet" in prob_low
        or "route_to_" in joined_fluents
        or "172.24." in prob_low
        or "10." in prob_low
        or "172." in prob_low
        or "192.168." in prob_low
    ):
        return "s_passive_topology_mapped", fluent_tags

    return "s_init_unknown", fluent_tags


def solve_bellman_mdp(
    transitions: List[Dict[str, Any]],
    state_rewards: Dict[str, float],
    gamma: float = 0.92,
    max_iterations: int = 25,
    tolerance: float = 1e-4,
) -> Tuple[Dict[str, float], List[Dict[str, Any]], int]:
    """
    Solve Bellman Value Iteration over all states and hierarchical actions:
        V_{k+1}(s) = max_a sum_{s'} T(s, a, s') * [ R(s, a, s') + gamma * V_k(s') ]
    Returns `(V_star, enriched_transitions_with_Q_star, iterations_run)`.
    """
    states = set(state_rewards.keys())
    for tr in transitions:
        states.add(tr.get("pre_state", "s_init_unknown"))
        states.add(tr.get("post_state_success", "s_l2_l3_verified"))
        states.add(tr.get("post_state_fail", "s_command_blocked_or_failed"))

    V: Dict[str, float] = {s: float(state_rewards.get(s, 0.0)) for s in states}
    # Precompute static transition parameters once so Bellman Value Iteration scales to 10,000+ transitions in < 2 ms
    by_state_compiled: Dict[str, List[Tuple[float, float, float, float, str, str]]] = {s: [] for s in states}
    compiled_all: List[Tuple[Dict[str, Any], str, float, float, float, float, str, str]] = []
    for tr in transitions:
        s = tr.get("pre_state", "s_init_unknown")
        a_succ = max(0.1, float(tr.get("alpha_success", 5.0)))
        a_fail = max(0.1, float(tr.get("alpha_fail", 1.0)))
        p_succ = a_succ / (a_succ + a_fail)
        p_fail = 1.0 - p_succ
        s_succ = tr.get("post_state_success", s)
        s_fail = tr.get("post_state_fail", s)
        cost = float(tr.get("step_cost", 1.0))
        phi_s = float(state_rewards.get(s, 0.0))
        phi_succ = float(state_rewards.get(s_succ, 20.0))
        term_bonus = 60.0 if s_succ == "s_goal_verified_complete" else 0.0
        r_succ = max(4.0, phi_succ - phi_s) + term_bonus - cost
        r_fail = -cost
        by_state_compiled.setdefault(s, []).append((p_succ, p_fail, r_succ, r_fail, s_succ, s_fail))
        compiled_all.append((tr, s, p_succ, p_fail, r_succ, r_fail, s_succ, s_fail))

    iters = 0
    for it in range(1, max_iterations + 1):
        iters = it
        max_delta = 0.0
        V_next = dict(V)
        for s in states:
            acts = by_state_compiled.get(s, [])
            if not acts or s == "s_goal_verified_complete":
                continue
            best_q = V[s]
            for p_succ, p_fail, r_succ, r_fail, s_succ, s_fail in acts:
                q_val = p_succ * (r_succ + gamma * V.get(s_succ, 0.0)) + p_fail * (
                    r_fail + gamma * V.get(s_fail, 0.0)
                )
                if q_val > best_q:
                    best_q = q_val
            delta = abs(best_q - V[s])
            if delta > max_delta:
                max_delta = delta
            V_next[s] = best_q
        V = V_next
        if max_delta < tolerance:
            break

    # Compute final Q*(s, a) for every transition
    enriched: List[Dict[str, Any]] = []
    for tr, s, p_succ, p_fail, r_succ, r_fail, s_succ, s_fail in compiled_all:
        q_star = p_succ * (r_succ + gamma * V.get(s_succ, 0.0)) + p_fail * (
            r_fail + gamma * V.get(s_fail, 0.0)
        )
        item = dict(tr)
        item["transition_prob_success"] = round(p_succ, 4)
        item["q_star_value"] = round(q_star, 2)
        enriched.append(item)

    enriched.sort(key=lambda x: x["q_star_value"], reverse=True)
    return {k: round(v, 2) for k, v in V.items()}, enriched, iters


def flush_mdp_store_if_dirty() -> bool:
    """Persist any pending in-RAM Dirichlet MDP transition updates to `mdp_transitions.json`."""
    store = _MDP_STORE_RAM_CACHE.get("data")
    dirty_cnt = int(_MDP_STORE_RAM_CACHE.get("dirty_count", 0))
    if store is not None and dirty_cnt > 0:
        try:
            save_json_state(str(MDP_STORE_FILE), store)
            new_mt = os.path.getmtime(MDP_STORE_FILE) if os.path.exists(MDP_STORE_FILE) else 0.0
            _MDP_STORE_RAM_CACHE["mtime"] = new_mt
            _MDP_STORE_RAM_CACHE["dirty_count"] = 0
            if _MDP_SOLVED_CACHE.get("stratified_pool") is not None:
                _MDP_SOLVED_CACHE["mtime"] = new_mt
            return True
        except Exception:
            pass
    return False


def record_mdp_transition_outcome(
    command: str,
    succeeded: bool,
    context_text: str = "",
    flush: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Online Bayesian Dirichlet Update:
    Whenever a shell command or scan runs in `agent-cli.py`, update the best-matching transition's
    `alpha_success` or `alpha_fail` in RAM and flush to `Reasoning/data/mdp_transitions.json`
    periodically (every 10 online updates, on `flush=True`, or at process exit via `atexit`).
    """
    cmd_clean = (command or "").strip()
    if not cmd_clean:
        return None
    try:
        store = load_or_init_mdp_store()
        transitions = store.get("transitions", [])
        tactic, technique, tool_bin = classify_tactic_category(context_text, cmd_clean)
        if tool_bin in ("cd", "echo", "printf", "cat", "ls", "head", "tail", "pwd", "true", "false", "."):
            return None

        cur_state, _ = infer_current_mdp_state(f"{context_text} {cmd_clean}")
        cmd_tokens = set(re.findall(r"[a-z0-9_\-]{2,}", cmd_clean.lower()))

        best_tr = None
        best_score = -1.0
        matching_tools = {tool_bin}
        if tool_bin == "scan_target":
            matching_tools.update({"nmap", "curl", "ping"})
        for tr in transitions:
            tr_tool = str(tr.get("tool", "")).lower()
            if tr_tool not in matching_tools:
                continue
            score = 1.0
            if tr.get("tactic") == tactic:
                score += 3.0
            if tr.get("pre_state") == cur_state:
                score += 2.5
            if tr.get("source") == "seed_core":
                score += 1.5
            tpl_tokens = set(re.findall(r"[a-z0-9_\-]{2,}", str(tr.get("command_template", "")).lower()))
            if cmd_tokens and tpl_tokens:
                score += min(3.0, 0.5 * len(cmd_tokens & tpl_tokens))
            if score > best_score:
                best_score = score
                best_tr = tr

        matched_tr = best_tr
        if matched_tr is not None:
            if succeeded:
                matched_tr["alpha_success"] = round(float(matched_tr.get("alpha_success", 5.0)) + 1.0, 2)
            else:
                matched_tr["alpha_fail"] = round(float(matched_tr.get("alpha_fail", 1.0)) + 1.0, 2)
            a_s = max(0.1, float(matched_tr.get("alpha_success", 5.0)))
            a_f = max(0.1, float(matched_tr.get("alpha_fail", 1.0)))
            p_succ = round(a_s / (a_s + a_f), 4)
            store["online_updates_count"] = int(store.get("online_updates_count", 0)) + 1
            store["updated_at"] = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
            _MDP_STORE_RAM_CACHE["data"] = store
            dirty = int(_MDP_STORE_RAM_CACHE.get("dirty_count", 0)) + 1
            _MDP_STORE_RAM_CACHE["dirty_count"] = dirty
            if flush or dirty >= 10:
                flush_mdp_store_if_dirty()
            return {
                "id": matched_tr.get("id"),
                "tactic": matched_tr.get("tactic"),
                "tool": matched_tr.get("tool"),
                "alpha_success": matched_tr["alpha_success"],
                "alpha_fail": matched_tr["alpha_fail"],
                "transition_prob_success": p_succ,
            }
    except Exception:
        pass
    return None


atexit.register(flush_mdp_store_if_dirty)


def merge_trained_mdp_transitions(new_transitions: List[Dict[str, Any]]) -> int:
    """
    Merge transitions extracted from books, PDFs, playbooks, and diagrams during `train_llm.py`
    into `Reasoning/data/mdp_transitions.json` using Dirichlet prior aggregation with no artificial cap.
    """
    if not new_transitions:
        return 0
    store = load_or_init_mdp_store()
    existing: List[Dict[str, Any]] = store.get("transitions", [])
    by_sig: Dict[str, Dict[str, Any]] = {}
    for tr in existing:
        sig = f"{tr.get('pre_state')}|{tr.get('tactic')}|{tr.get('tool')}|{tr.get('command_template', '')}"
        by_sig[sig] = tr

    added_or_updated = 0
    for ntr in new_transitions:
        sig = f"{ntr.get('pre_state')}|{ntr.get('tactic')}|{ntr.get('tool')}|{ntr.get('command_template', '')}"
        if sig in by_sig:
            # Reinforce prior count if corroborated across multiple book chapters/docs
            by_sig[sig]["alpha_success"] = round(
                min(50.0, float(by_sig[sig].get("alpha_success", 8.0)) + 1.5), 2
            )
            added_or_updated += 1
        else:
            existing.append(ntr)
            by_sig[sig] = ntr
            added_or_updated += 1

    # Retain 100% of unique transitions across the training corpus
    store["transitions"] = existing
    store["updated_at"] = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
    save_json_state(str(MDP_STORE_FILE), store)
    return added_or_updated


_MDP_SOLVED_CACHE: Dict[str, Any] = {
    "mtime": -1.0,
    "max_iters": 0,
    "store": None,
    "V_star": None,
    "enriched_all": None,
    "stratified_pool": None,
    "iters_run": 0,
}


def _get_cached_solved_mdp(max_iters: int) -> Tuple[Dict[str, Any], Dict[str, float], List[Dict[str, Any]], int]:
    """Load and solve Bellman Value Iteration once per `mdp_transitions.json` modification time, caching a stratified high-Q pool."""
    try:
        mtime = os.path.getmtime(MDP_STORE_FILE) if os.path.exists(MDP_STORE_FILE) else 0.0
    except OSError:
        mtime = 0.0

    if (
        _MDP_SOLVED_CACHE["mtime"] == mtime
        and _MDP_SOLVED_CACHE["max_iters"] == max_iters
        and _MDP_SOLVED_CACHE["store"] is not None
        and _MDP_SOLVED_CACHE["V_star"] is not None
        and _MDP_SOLVED_CACHE["stratified_pool"] is not None
    ):
        return (
            _MDP_SOLVED_CACHE["store"],
            _MDP_SOLVED_CACHE["V_star"],
            _MDP_SOLVED_CACHE["stratified_pool"],
            int(_MDP_SOLVED_CACHE["iters_run"]),
        )

    store = load_or_init_mdp_store()
    transitions = store.get("transitions", DEFAULT_MDP_TRANSITIONS)
    state_rewards = store.get("state_rewards", STATE_BASE_REWARDS)
    gamma = float(store.get("discount_gamma", 0.92))
    V_star, enriched_all, iters_run = solve_bellman_mdp(
        transitions=transitions,
        state_rewards=state_rewards,
        gamma=gamma,
        max_iterations=max_iters,
    )
    # Build stratified top-Q pool per (pre_state, tactic, has_target, is_linux_ok) bucket so POMDP scoring runs in < 1.5 ms
    # without Windows PDF cmdlets starving Linux transitions in any bucket
    bucket_counts: Dict[Tuple[str, str, bool, bool], int] = {}
    stratified_pool: List[Dict[str, Any]] = []
    for tr in enriched_all:
        cmd_t = tr.get("command_template", "")
        has_t = ("{target_ip}" in cmd_t) or ("<target_ip>" in cmd_t.lower())
        linux_ok = _is_transition_os_compatible(tr, "linux")
        bkey = (str(tr.get("pre_state", "")), str(tr.get("tactic", "")), has_t, linux_ok)
        cnt = bucket_counts.get(bkey, 0)
        if cnt < 15 or tr.get("source") == "seed_core":
            stratified_pool.append(tr)
            bucket_counts[bkey] = cnt + 1

    _MDP_SOLVED_CACHE["mtime"] = mtime
    _MDP_SOLVED_CACHE["max_iters"] = max_iters
    _MDP_SOLVED_CACHE["store"] = store
    _MDP_SOLVED_CACHE["V_star"] = V_star
    _MDP_SOLVED_CACHE["enriched_all"] = enriched_all
    _MDP_SOLVED_CACHE["stratified_pool"] = stratified_pool
    _MDP_SOLVED_CACHE["iters_run"] = iters_run
    return store, V_star, stratified_pool, iters_run


_WINDOWS_ONLY_TOOLS = {
    "wmic", "powershell", "pwsh", "cmd", "ipconfig", "netsh", "tasklist", "taskkill",
    "reg", "sc", "icacls", "cacls", "certutil", "bitsadmin", "vssadmin", "ntdsutil",
    "pslist", "pskill", "psloggedon", "psloglist", "psservice", "psinfo", "psfile",
    "psgetsid", "pspasswd", "psping", "autorunsc", "autoruns", "sigcheck", "handle",
    "listdlls", "tcpvcon", "accesschk", "accessenum", "procdump", "procmon", "sysmon",
    "sdelete", "logonsessions", "pipelist", "portmon", "movefile", "movelatr", "pechksum",
    "bcdedit", "wevtutil", "auditpol", "dsquery", "dsget", "dsadd", "dsmod", "dsmove",
    "dsrm", "csvde", "ldifde", "dnscmd", "gpresult", "gpupdate", "qwinsta", "rwinsta",
    "quser", "klist", "vaultcmd", "cmdkey", "fltmc", "fsutil", "openfiles", "driverquery",
    "wbadmin", "dism", "pktmon", "fport", "nltest", "mimikatz",
    "sekurlsa::logonpasswords", "lsadump::sam", "lsadump::secrets", "lsadump::cache",
    "privilege::debug", "token::elevate", "token::revert",
    "new-cimsession", "get-ciminstance", "enter-pssession", "new-pssession",
    "invoke-command", "invoke-webrequest", "invoke-restmethod", "get-credential",
    "get-wmiobject", "get-process", "get-service", "get-childitem", "get-acl",
    "get-hotfix", "get-eventlog", "get-winevent", "test-netconnection", "net",
    "findstr", "forfiles", "takeown", "attrib", "sfc", "rundll32", "regsvr32",
    "schtasks", "runas", "xcopy", "robocopy", "esentutl", "mshta", "msiexec", "cscript", "wscript",
}
_POWERSHELL_CMDLET_RE = re.compile(
    r"^(?:get|set|new|remove|invoke|enter|exit|import|export|start|stop|restart|enable|disable|"
    r"test|register|unregister|update|clear|select|where|foreach|out|format|write|copy|move|"
    r"rename|measure|compare|group|tee|resolve|resume|suspend|wait|find|install|uninstall|restore)-[a-z0-9]+$"
)
_WINDOWS_CMD_MARKERS = (
    "wmic ", "powershell", "cmd.exe", "ipconfig", "netsh ", "tasklist", "get-wmi",
    "get-net", "get-process", "get-service", "get-childitem", "set-net", "invoke-",
    "new-net", "new-cimsession", "get-ciminstance", "enter-pssession", "new-pssession",
    "get-credential", "test-netconnection", "/format:htable", "c:\\", "hklm\\", "hkcu\\",
    "netstat -ano", "netstat -anob", "route print", "%systemroot%", "%windir%",
)
_LINUX_ONLY_TOOLS = {
    "ip", "ss", "iptables", "nft", "sysctl", "tio", "systemctl", "uname", "arping",
    "tcpdump", "sudo", "chmod", "chown", "journalctl", "nmcli",
}
_LINUX_CMD_MARKERS = (
    "ip -4", "ip -br", "ip route", "ip addr", "ip neigh", "ss -", "iptables",
    "sysctl", "tio ", "/dev/tty", "/etc/", "sudo ", "uname -a",
)


def _is_transition_os_compatible(tr: Dict[str, Any], target_os: str) -> bool:
    """Ensure Windows-only commands (e.g. wmic/powershell) are never selected on Linux targets and vice versa."""
    if tr.get("source") == "seed_core":
        return True
    tool = str(tr.get("tool", "")).lower().strip()
    cmd_low = str(tr.get("command_template", "")).lower()
    if target_os == "linux":
        if (
            tool in _WINDOWS_ONLY_TOOLS
            or bool(_POWERSHELL_CMDLET_RE.match(tool))
            or any(m in cmd_low for m in _WINDOWS_CMD_MARKERS)
        ):
            return False
    elif target_os == "windows":
        if tool in _LINUX_ONLY_TOOLS or any(m in cmd_low for m in _LINUX_CMD_MARKERS):
            return False
    return True


def solve_in_task_optimal_stopping_mdp(
    current_state: str,
    V_star: Dict[str, float],
    top_policies: List[Dict[str, Any]],
    problem: str = "",
    dempster_shafer_ignorance: float = 0.0,
    somatic_valence: float = 0.0,
) -> Dict[str, Any]:
    """
    In-Task Optimal Stopping & Dead-End Pivot Solver (V_continue vs. V_pivot):
    Compares the expected continuation value of persisting on the current tactic/layer (`V_continue`)
    against pivoting immediately to an alternative layer/channel (`V_pivot`).
    """
    prob_low = (problem or "").lower()
    has_tcp_refused = any(k in prob_low for k in ("connection refused", "exit 7"))
    has_timeout_loss = any(k in prob_low for k in ("100% packet loss", "timed out", "timeout", "exit 28"))
    has_acl_block = any(k in prob_low for k in ("filtered", "permission denied", "blocked", "access is denied"))
    has_repeated_fail = any(k in prob_low for k in ("still failing", "repeated", "again", "multiple attempts", "hung", "exhaust"))
    absorption_signals = int(has_tcp_refused) + int(has_timeout_loss) + int(has_acl_block) + int(has_repeated_fail)
    primary_pol = top_policies[0] if top_policies else {}
    alt_pol = next(
        (p for p in top_policies[1:] if p.get("tactic") != primary_pol.get("tactic")),
        top_policies[1] if len(top_policies) > 1 else primary_pol,
    )

    q_primary = float(primary_pol.get("pomdp_adjusted_q", V_star.get(current_state, 100.0)))
    q_alt = float(alt_pol.get("pomdp_adjusted_q", q_primary * 0.85))

    # Penalty on continuing a blocked in-band path when absorption signals or negative somatic valence appear
    absorption_penalty = (absorption_signals * 18.0) + (max(0.0, -somatic_valence) * 25.0)
    v_continue = round(q_primary - (absorption_penalty if primary_pol.get("tactic") == "Active_Enum" else 0.0), 2)
    v_pivot = round(q_alt + (15.0 if absorption_signals >= 2 else 0.0) + (dempster_shafer_ignorance * 20.0), 2)

    if v_pivot > v_continue and absorption_signals >= 2:
        decision = "PIVOT_TACTIC_IMMEDIATELY"
        pivot_target_tactic = str(alt_pol.get("tactic", "Out-of-Band_Access"))
        pivot_target_cmd = str(alt_pol.get("instantiated_command", primary_pol.get("instantiated_command", "")))
        rationale = (
            f"V_pivot ({v_pivot}) > V_continue ({v_continue}): Detected {absorption_signals} absorption/block "
            f"signals on current path; abandon repetitive retries and pivot to `{pivot_target_tactic}`."
        )
    elif dempster_shafer_ignorance >= 0.35:
        decision = "EIG_DISCOVERY_PROBE_FIRST"
        pivot_target_tactic = str(primary_pol.get("tactic", "Passive_Enum"))
        pivot_target_cmd = str(primary_pol.get("instantiated_command", ""))
        rationale = (
            f"Epistemic ignorance m(Theta)={dempster_shafer_ignorance:.2f} is elevated; run high-EIG "
            f"verification probe (`{pivot_target_tactic}`) before state-mutating actions."
        )
    else:
        decision = "HOLD_OPTIMAL_TACTIC_LINE"
        pivot_target_tactic = str(primary_pol.get("tactic", "Active_Enum"))
        pivot_target_cmd = str(primary_pol.get("instantiated_command", ""))
        rationale = (
            f"V_continue ({v_continue}) >= V_pivot ({v_pivot}): Current tactical trajectory has highest "
            f"expected goal-completion value."
        )

    return {
        "stopping_decision": decision,
        "v_continue": v_continue,
        "v_pivot": v_pivot,
        "absorption_wall_signals": absorption_signals,
        "recommended_tactic": pivot_target_tactic,
        "recommended_command": pivot_target_cmd,
        "rationale": rationale,
    }


def forecast_next_tools_and_branches(
    current_state: str,
    top_policies: List[Dict[str, Any]],
    all_candidates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Speculative N-Branch Next-Tool Forecaster:
    Predicts:
      1. `immediate`: The #1 optimal tool & command to execute right now (`t`).
      2. `on_success_branch`: If command `t` succeeds (`exit_code == 0`), the exact next state `s_succ`
         and optimal follow-up tool & command `a*(s_succ)` at `t+1`.
      3. `on_failure_branch`: If command `t` fails or is blocked (`exit_code != 0`), the fallback state `s_fail`
         and highest-value pivot tool & command `a*(s_fail)` at `t+1`.
    """
    if not top_policies:
        return {}
    step0 = top_policies[0]
    s_succ = str(step0.get("post_state_success", "s_l2_l3_verified"))
    s_fail = str(step0.get("post_state_fail", "s_command_blocked_or_failed"))

    succ_cands = [
        c for c in all_candidates
        if c.get("pre_state") == s_succ and c.get("id") != step0.get("id") and c.get("source") == "seed_core"
    ] or [
        c for c in all_candidates if c.get("pre_state") == s_succ and c.get("id") != step0.get("id")
    ]
    if not succ_cands:
        succ_cands = [c for c in top_policies[1:] if c.get("id") != step0.get("id")]
    best_succ = succ_cands[0] if succ_cands else step0

    fail_cands = [
        c for c in top_policies[1:] if c.get("tactic") != step0.get("tactic") and c.get("id") != step0.get("id")
    ] or [
        c for c in all_candidates
        if c.get("tactic") != step0.get("tactic") and c.get("id") != step0.get("id") and c.get("source") == "seed_core"
    ] or [
        c for c in all_candidates if c.get("tactic") != step0.get("tactic") and c.get("id") != step0.get("id")
    ]
    best_fail = fail_cands[0] if fail_cands else (top_policies[1] if len(top_policies) > 1 else step0)

    return {
        "immediate": {
            "state": current_state,
            "tactic": step0.get("tactic"),
            "tool": step0.get("tool"),
            "command": step0.get("instantiated_command"),
            "q_star": step0.get("pomdp_adjusted_q"),
            "p_success": step0.get("transition_prob_success"),
        },
        "on_success_branch": {
            "trigger": "exit_code == 0 (State Advances)",
            "predicted_state": s_succ,
            "next_tactic": best_succ.get("tactic"),
            "next_tool": best_succ.get("tool"),
            "next_command": best_succ.get("instantiated_command"),
            "q_star": best_succ.get("pomdp_adjusted_q"),
        },
        "on_failure_branch": {
            "trigger": "exit_code != 0 or Timeout (Pivot Triggered)",
            "predicted_state": s_fail,
            "pivot_tactic": best_fail.get("tactic"),
            "pivot_tool": best_fail.get("tool"),
            "pivot_command": best_fail.get("instantiated_command"),
            "q_star": best_fail.get("pomdp_adjusted_q"),
        },
    }


def run_mdp_tactical_reasoning(
    problem: str,
    target_ip: str = "",
    secondary_target_ip: str = "",
    observed_evidence: Optional[Dict[str, bool]] = None,
    has_serial_oob: bool = True,
    bayesian_top_hypothesis: str = "",
    dempster_shafer_ignorance: float = 0.0,
    somatic_valence: float = 0.0,
    save_to_vault: bool = True,
) -> Dict[str, Any]:
    """
    Execute Engine 15: Hierarchical Tactical MDP, Live Optimal Stopping & Speculative Next-Tool Forecaster.
    Computes optimal Bellman values V*(s) and Q*(s, a) in `< 3 ms` via mtime-keyed RAM caching,
    ranks the Top-5 `Tactic -> Technique -> Tool -> Command` actions, evaluates `V_continue` vs `V_pivot`,
    and projects a multi-step Markov lookahead trajectory + speculative branch forecast.
    """
    t0 = time.perf_counter()
    hw_limits = get_hardware_reasoning_limits()
    ctx = resolve_problem_targets(
        problem=problem,
        explicit_target=target_ip,
        explicit_secondary=secondary_target_ip,
    )
    resolved_target = ctx["target_ip"]
    resolved_secondary = ctx["secondary_target_ip"] or resolved_target
    remote_subnet = ctx["remote_subnet"]
    serial_dev = ctx["serial_device"]
    target_os = str(ctx.get("target_os") or ("windows" if os.name == "nt" else "linux")).lower()
    is_windows = (target_os == "windows")

    max_iters = int(get_hardware_reasoning_limits().get("mdp_bellman_sweeps", 25))
    store, V_star, enriched_all, iters_run = _get_cached_solved_mdp(max_iters)
    transitions = store.get("transitions", DEFAULT_MDP_TRANSITIONS)
    gamma = float(store.get("discount_gamma", 0.92))

    current_state, fluent_tags = infer_current_mdp_state(
        problem=problem,
        observed_evidence=observed_evidence,
        has_serial_oob=has_serial_oob,
    )

    prob_low = (problem or "").lower()
    has_serial_kw = bool(re.search(r"\b(?:ttyusb\d*|ttyacm\d*|serial|tio|uart|oob|console)\b|exit 7|connection refused", prob_low))
    has_route_kw = any(k in prob_low for k in ("route", "subnet", "pivot", "cross-subnet", "disjoint", "network is unreachable", "gateway"))
    has_privesc_kw = any(k in prob_low for k in ("privesc", "privilege", "suid", "sudo", "capabilities", "getcap", "www-data"))
    h_low = (bayesian_top_hypothesis or "").lower()

    # Fast OS-filtered numeric scoring across stratified transitions without regex instantiation first
    scored_raw: List[Tuple[float, Dict[str, Any]]] = []
    for tr in enriched_all:
        if not _is_transition_os_compatible(tr, target_os):
            continue
        pomdp_bonus = 0.0
        tactic = tr.get("tactic", "")
        cmd_tmpl = tr.get("command_template", "")
        if tr.get("source") == "seed_core":
            pomdp_bonus += 22.0
        if tr.get("pre_state") == current_state:
            pomdp_bonus += 90.0
        if "{target_ip}" in cmd_tmpl or "<target_ip>" in cmd_tmpl.lower():
            pomdp_bonus += 8.0
        if has_serial_kw and has_serial_oob:
            if tactic in ("Out-of-Band_Access", "Defense_Evasion_Firewall"):
                pomdp_bonus += 24.0
            elif tactic == "Active_Enum":
                pomdp_bonus += 12.0
        elif not has_serial_oob and (tactic == "Out-of-Band_Access" or tr.get("tool") == "tio"):
            pomdp_bonus -= 80.0
        if has_route_kw and tactic in ("Lateral_Movement_Routing_Pivot", "Passive_Enum", "Active_Enum"):
            pomdp_bonus += 22.0
        if has_privesc_kw and tactic == "Privilege_Escalation":
            pomdp_bonus += 28.0
        if dempster_shafer_ignorance > 0.40 and tactic in ("Passive_Enum", "Active_Enum") and not has_privesc_kw:
            pomdp_bonus += 12.0
        if h_low:
            if ("firewall" in h_low or "port" in h_low or "loopback" in h_low) and tactic in (
                "Out-of-Band_Access",
                "Defense_Evasion_Firewall",
                "Active_Enum",
            ):
                pomdp_bonus += 10.0
            elif "route" in h_low and tactic in ("Lateral_Movement_Routing_Pivot", "Passive_Enum"):
                pomdp_bonus += 10.0
            elif ("auth" in h_low or "tls" in h_low or "cert" in h_low) and tactic in (
                "Credential_Access",
                "Protocol_Chaining",
            ):
                pomdp_bonus += 10.0

        adj_q = round(float(tr["q_star_value"]) + pomdp_bonus, 2)
        scored_raw.append((adj_q, tr))

    scored_raw.sort(key=lambda pair: pair[0], reverse=True)

    # Select top 30 overall + top 2 per pre_state so multi-step lookahead & branch forecasts are 100% covered
    selected_trs: List[Tuple[float, Dict[str, Any]]] = []
    seen_ids = set()
    state_counts: Dict[str, int] = {}
    for adj_q, tr in scored_raw:
        tid = tr.get("id")
        ps = tr.get("pre_state", "")
        if len(selected_trs) < 30 or state_counts.get(ps, 0) < 2:
            if tid not in seen_ids:
                seen_ids.add(tid)
                selected_trs.append((adj_q, tr))
                state_counts[ps] = state_counts.get(ps, 0) + 1

    candidates: List[Dict[str, Any]] = []
    for adj_q, tr in selected_trs:
        item = dict(tr)
        cmd_inst = (
            item.get("command_template", "")
            .replace("{target_ip}", resolved_target)
            .replace("{secondary_target_ip}", resolved_secondary)
            .replace("{remote_subnet}", remote_subnet)
            .replace("/dev/ttyUSB0", serial_dev)
        )
        cmd_inst = render_command_template(cmd_inst, ctx)
        local_shell_is_windows = (os.name == "nt") or any(
            k in prob_low for k in ("c:\\", "cmd.exe", "powershell", "ipconfig", "whoami /priv", "route print")
        )
        if is_windows and local_shell_is_windows and item.get("source") == "seed_core":
            tid = item.get("id")
            if tid == "MDP_PASSIVE_IFACE_ARP":
                cmd_inst = "ipconfig /all & route print -4 & arp -a"
                item["tool"] = "ipconfig"
            elif tid == "MDP_PASSIVE_SOCKET_INSPECT":
                cmd_inst = "netstat -ano"
                item["tool"] = "netstat"
            elif tid == "MDP_PASSIVE_LOCAL_WORKSPACE":
                cmd_inst = "dir /b %PROJECT_DIR%"
                item["tool"] = "dir"
            elif tid == "MDP_RECON_VERIFY_REACHABILITY":
                cmd_inst = f"ping -n 3 -w 1500 {resolved_target}"
                item["tool"] = "ping"
            elif tid == "MDP_SERIAL_UART_DETECTION":
                cmd_inst = r"reg query HKLM\HARDWARE\DEVICEMAP\SERIALCOMM"
                item["tool"] = "reg"
            elif tid == "MDP_ACTIVE_L2_L3_ROUTE_PROBE":
                cmd_inst = f"route print -4 & ping -n 2 -w 1000 {resolved_target}"
                item["tool"] = "ping"
            elif tid == "MDP_PRIV_ESC_LOCAL_ENUM":
                cmd_inst = "whoami /all & systeminfo"
                item["tool"] = "whoami"
            elif tid == "MDP_LATERAL_CROSS_SUBNET_ROUTE":
                cmd_inst = f"route add {remote_subnet} {resolved_target} && ping -n 2 -w 1000 {resolved_secondary}"
                item["tool"] = "route"
            elif tid == "MDP_POST_EXPLOIT_VERIFY_A":
                cmd_inst = f"route print -4 & ping -n 2 -w 1000 {resolved_secondary}"
                item["tool"] = "ping"
            elif tid == "MDP_POST_EXPLOIT_VERIFY_B":
                cmd_inst = "ipconfig /all & netstat -ano"
                item["tool"] = "ipconfig"
        item["instantiated_command"] = cmd_inst
        item["pomdp_adjusted_q"] = adj_q
        candidates.append(item)

    candidates.sort(key=lambda x: x["pomdp_adjusted_q"], reverse=True)
    top_policies = candidates[:5]

    stopping_info = solve_in_task_optimal_stopping_mdp(
        current_state=current_state,
        V_star=V_star,
        top_policies=top_policies,
        problem=problem,
        dempster_shafer_ignorance=dempster_shafer_ignorance,
        somatic_valence=somatic_valence,
    )
    branch_forecast = forecast_next_tools_and_branches(
        current_state=current_state,
        top_policies=top_policies,
        all_candidates=candidates,
    )

    # Build 3-step Markov Lookahead Trajectory starting from the #1 optimal action
    trajectory: List[Dict[str, Any]] = []
    if top_policies:
        step1 = top_policies[0]
        trajectory.append(
            {
                "step": 1,
                "state": current_state,
                "tactic": step1["tactic"],
                "technique": step1["technique"],
                "tool": step1["tool"],
                "command": step1["instantiated_command"],
                "p_success": step1["transition_prob_success"],
                "q_star": step1["pomdp_adjusted_q"],
                "next_state": step1["post_state_success"],
            }
        )
        cur_s = step1["post_state_success"]
        for step_idx in (2, 3):
            next_matches = [c for c in candidates if c.get("pre_state") == cur_s]
            if not next_matches:
                break
            best_next = next_matches[0]
            trajectory.append(
                {
                    "step": step_idx,
                    "state": cur_s,
                    "tactic": best_next["tactic"],
                    "technique": best_next["technique"],
                    "tool": best_next["tool"],
                    "command": best_next["instantiated_command"],
                    "p_success": best_next["transition_prob_success"],
                    "q_star": best_next["q_star_value"],
                    "next_state": best_next["post_state_success"],
                }
            )
            cur_s = best_next["post_state_success"]
            if cur_s == "s_goal_verified_complete":
                break

    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    optimal = top_policies[0] if top_policies else {}
    default_cmd = f"route print -4 & ping -n 2 -w 1000 {resolved_target}" if is_windows else f"ip route get {resolved_target}"

    md_lines = [
        f"### Engine 15: Hierarchical Tactical MDP, Optimal Stopping & Next-Tool Forecaster (`{elapsed_ms} ms`, `{iters_run}` Bellman sweeps)",
        f"- **Current Markov State ($s_t$):** `{current_state}` (Base Value $V^*(s_t) = {V_star.get(current_state, 0.0)}$)",
        f"- **In-Task Optimal Stopping ($V_{{\\text{{continue}}}} = {stopping_info['v_continue']}$ vs $V_{{\\text{{pivot}}}} = {stopping_info['v_pivot']}$):** **`{stopping_info['stopping_decision']}`** — {stopping_info['rationale']}",
        f"- **Active Tactic Taxonomy (`{len(TACTIC_CATEGORIES)}` Categories):** `{', '.join(TACTIC_CATEGORIES)}`",
        f"- **Transition Matrix Size:** `{len(transitions)}` state-action transitions (`{store.get('online_updates_count', 0)}` online Dirichlet updates)",
        "",
        "#### Top Ranked `Tactic -> Technique -> Tool -> Command` Policies ($Q^*(s, a)$)",
        "| Rank | Tactic ($\\tau$) | Technique ($k$) | Tool ($u$) | $P(s' \\mid s,a)$ | $Q^*(s,a)$ | Recommended Command ($c$) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for idx, pol in enumerate(top_policies, 1):
        md_lines.append(
            f"| **{idx}** | `{pol['tactic']}` | {pol['technique']} | `{pol['tool']}` | "
            f"**{pol['transition_prob_success']:.0%}** | **`{pol['pomdp_adjusted_q']}`** | `{pol['instantiated_command']}` |"
        )

    if branch_forecast:
        succ_b = branch_forecast.get("on_success_branch", {})
        fail_b = branch_forecast.get("on_failure_branch", {})
        md_lines.extend(
            [
                "\n#### Speculative N-Branch Next-Tool Forecast ($t+1$)",
                f"- **If Command Succeeds (`exit_code == 0` $\\to$ `{succ_b.get('predicted_state')}`):** Next Tool **`{succ_b.get('next_tool')}`** (`{succ_b.get('next_tactic')}`) $\\rightarrow$ `{succ_b.get('next_command')}`",
                f"- **If Command Fails/Blocks (`exit_code != 0` $\\to$ `{fail_b.get('predicted_state')}`):** Pivot Tool **`{fail_b.get('pivot_tool')}`** (`{fail_b.get('pivot_tactic')}`) $\\rightarrow$ `{fail_b.get('pivot_command')}`",
            ]
        )

    if len(trajectory) > 1:
        md_lines.append("\n#### Multi-Step Markov Lookahead Trajectory ($\\pi^*(s_t) \\to s_{t+1} \\to s_{t+2}$)")
        for step in trajectory:
            md_lines.append(
                f"{step['step']}. **`[{step['tactic']}]`** ({step['technique']} via `{step['tool']}`, "
                f"$P={step['p_success']:.0%}$, $Q^*={step['q_star']}$) $\\rightarrow$ `{step['command']}` "
                f"$\\implies$ **`{step['next_state']}`**"
            )

    markdown_report = "\n".join(md_lines)

    result = {
        "engine": "mdp_tactical",
        "current_state": current_state,
        "active_fluents": fluent_tags,
        "bellman_iterations": iters_run,
        "discount_gamma": gamma,
        "total_transitions": len(transitions),
        "tactic_categories_count": len(TACTIC_CATEGORIES),
        "tactic_categories": TACTIC_CATEGORIES,
        "optimal_tactic": optimal.get("tactic", "Active_Enum"),
        "optimal_technique": optimal.get("technique", ""),
        "optimal_tool": optimal.get("tool", "ipconfig" if is_windows else "ip"),
        "optimal_command": optimal.get("instantiated_command", default_cmd),
        "optimal_q_star": optimal.get("pomdp_adjusted_q", 0.0),
        "optimal_prob_success": optimal.get("transition_prob_success", 0.9),
        "optimal_stopping": stopping_info,
        "speculative_branch_forecast": branch_forecast,
        "top_policies": top_policies,
        "lookahead_trajectory": trajectory,
        "elapsed_ms": elapsed_ms,
        "markdown_report": markdown_report,
    }

    if save_to_vault:
        save_json_data("mdp_policies", f"mdp_{slugify(resolved_target)}_{slugify(current_state)}", result)
        save_reasoning_to_vault(
            title=f"mdp_policy_{slugify(resolved_target)}",
            summary=(
                f"MDP Policy for {resolved_target}: Tactic `{result['optimal_tactic']}` -> "
                f"Tool `{result['optimal_tool']}` (Q*={result['optimal_q_star']}, P={result['optimal_prob_success']:.0%})"
            ),
            markdown_body=markdown_report,
            engine_type="mdp_tactical",
            tags=["mdp", "markov", "tactics", slugify(result["optimal_tactic"]), slugify(resolved_target)],
        )
    return result
