"""
Engine 11: Case-Based Reasoning (CBR) & Failure Fingerprinting
==============================================================
Captures command failure signatures:
  (binary, exit_code, error_pattern) -> verified_resolution

Features:
- Pre-seeded library of common Linux/networking/serial/LLM command failures
  (e.g., `RTNETLINK answers: File exists`, `Network is unreachable`, `tio` Lua syntax errors,
   `bind: Address already in use`, `Permission denied`, `Name or service not known`, etc.).
- Live failure recording and automatic fix injection whenever a command fails (`returncode != 0`).
- Structural similarity matching over command tokens + stderr diagnostics.
"""

import json
import os
import re
import time
from typing import Any, Dict, List, Optional

from .vault_bridge import (
    CBR_DIR,
    DATA_DIR,
    ensure_directories,
    get_hardware_reasoning_limits,
    load_json_state,
    parameterize_tactical_template,
    render_command_template,
    resolve_problem_targets,
    save_json_state,
    write_reasoning_note,
)

CBR_LIBRARY_FILE = os.path.join(CBR_DIR, "cbr_library.json")
TRAINED_RULES_FILE = os.path.join(str(DATA_DIR), "trained_rules.json")
LEARNED_CBR_FILE = os.path.join(str(DATA_DIR), "learned_cbr_cases.json")

_CBR_RAM_CACHE: Dict[str, Any] = {"mtimes": (-1.0, -1.0, -1.0), "data": None, "compiled": []}
_TRAINED_CBR_CACHE: Dict[str, Any] = {"mtime": -1.0, "fingerprints": []}
_WORD_TOK_RE = re.compile(r"[a-z0-9_.-]{4,}")
_BACKTICK_CMD_RE = re.compile(r"`([^`]{4,220})`")

SEED_EXECUTABLE_FIX_MAP: Dict[str, Dict[str, str]] = {
    "CBR-001": {
        "linux": "sudo ip route replace {remote_subnet} via {target_ip} && ip route show",
        "windows": "route print -4 & arp -a {target_ip}",
    },
    "CBR-002": {
        "linux": "sudo ip route replace {remote_subnet} via {target_ip} dev {iface} onlink",
        "windows": "route add {remote_subnet} {target_ip}",
    },
    "CBR-003": {
        "linux": "tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(500); write(\"ip -4 addr\\r\"); while read(4096, 600) > 0 do end; exit(0)' {serial_device}",
        "windows": "powershell -NoProfile -Command \"Get-WmiObject Win32_SerialPort | Select-Object DeviceID,Description\"",
    },
    "CBR-004": {
        "linux": "ip neigh show {target_ip} && nmap -Pn -sT -p 22,80,443,8080,8443 {target_ip}",
        "windows": "arp -a {target_ip} & powershell -NoProfile -Command \"22,80,443,8080 | ForEach-Object { Test-NetConnection -ComputerName {target_ip} -Port $_ -WarningAction SilentlyContinue }\"",
    },
    "CBR-005": {
        "linux_serial": "tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(500); write(\"ip -4 addr; ss -tulpn\\r\"); while read(4096, 600) > 0 do end; exit(0)' {serial_device}",
        "linux": "nmap -Pn -sT -p 22,80,443,5000,8000,8080,8443 {target_ip}",
        "windows": "powershell -NoProfile -Command \"22,80,443,8080,8443 | ForEach-Object { Test-NetConnection -ComputerName {target_ip} -Port $_ -WarningAction SilentlyContinue }\"",
    },
    "CBR-006": {
        "linux": "ip route get {target_ip} && ip neigh show {target_ip}",
        "windows": "route print -4 & arp -a {target_ip}",
    },
    "CBR-007": {
        "linux": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=5 root@{target_ip} 'id; uname -a'",
        "windows": "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@{target_ip}",
    },
    "CBR-008": {
        "linux": "ip -4 -br addr show; ip route show; ss -tulpn",
        "windows": "ipconfig /all & route print -4 & netstat -ano",
    },
    "CBR-009": {
        "linux": "ip -4 -br addr show; ip route show; ip neigh show",
        "windows": "ipconfig /all & route print -4 & arp -a",
    },
    "CBR-010": {
        "linux": "id; sudo -n -l 2>/dev/null || ip route show",
        "windows": "whoami /priv & route print -4",
    },
    "CBR-011": {
        "linux": "ip -4 -br addr show",
        "windows": "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"Get-NetIPConfiguration\"",
    },
    "CBR-012": {
        "linux": "tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(500); write(\"id\\r\"); while read(4096, 600) > 0 do end; exit(0)' {serial_device}",
        "windows": "powershell -NoProfile -Command \"Get-WmiObject Win32_SerialPort | Select-Object DeviceID,Description\"",
    },
}


def extract_executable_cbr_command(case: Dict[str, Any], ctx: Optional[Dict[str, Any]] = None) -> str:
    """
    Return a clean, CEGAR-safe executable shell command for a matched CBR case,
    resolving OS family (`linux` vs `windows`), serial OOB availability, and target IPs.
    Never returns natural-language prose explanations that would fail `bash -n`.
    """
    c = ctx or resolve_problem_targets()
    target_os = str(c.get("target_os") or ("windows" if os.name == "nt" else "linux")).lower()
    cid = str(case.get("case_id") or "")

    if cid in SEED_EXECUTABLE_FIX_MAP:
        fmap = SEED_EXECUTABLE_FIX_MAP[cid]
        if target_os == "windows":
            tpl = fmap.get("windows", "")
        elif cid == "CBR-005" and c.get("has_serial_oob"):
            tpl = fmap.get("linux_serial", fmap.get("linux", ""))
        else:
            tpl = fmap.get("linux", "")
        if tpl:
            return render_command_template(tpl, c)

    raw_fix = str(case.get("verified_fix") or case.get("verified_remediation") or "").strip()
    if not raw_fix:
        return ""

    def _normalize_cbr_placeholders(s_cmd: str) -> str:
        s_out = re.sub(r"<(?:target_?ip|target|ip)>", "{target_ip}", s_cmd, flags=re.I)
        s_out = re.sub(r"<(?:remote_?subnet|subnet)>", "{remote_subnet}", s_out, flags=re.I)
        s_out = re.sub(r"<(?:gateway_?ip|gw)>", "{gateway_ip}", s_out, flags=re.I)
        s_out = re.sub(r"<(?:iface|interface)>", "{iface}", s_out, flags=re.I)
        s_out = re.sub(r"<(?:serial_?(?:device|port|dev))>", "{serial_device}", s_out, flags=re.I)
        return s_out

    # If the verified_fix contains backticked command snippets, pick the best executable snippet
    bt_matches = _BACKTICK_CMD_RE.findall(raw_fix)
    if bt_matches:
        for snip in bt_matches:
            s_clean = snip.strip()
            if " " in s_clean and not any(ph in s_clean.lower() for ph in ("<cmd>", "<script", "<user>", "<local_ip>")):
                return render_command_template(_normalize_cbr_placeholders(s_clean), c)

    # Check if raw_fix itself is already a command rather than an English sentence
    if not re.match(r"^(?:Use|First|Check|Verify|For|On|Run|\d+\.)\b", raw_fix):
        return render_command_template(_normalize_cbr_placeholders(raw_fix), c)
    return ""

DEFAULT_SEED_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "CBR-001",
        "binary": "ip",
        "exit_code": 2,
        "error_pattern": "RTNETLINK answers: File exists",
        "symptom": "Adding IP address or route fails with 'RTNETLINK answers: File exists'",
        "root_cause": "The IP address or static route already exists in the kernel routing/address table.",
        "verified_fix": "Use `ip addr replace <ip>/<cidr> dev <iface>` or `ip route replace <subnet> via <gw>` instead of `add`, or inspect existing entries with `ip addr show` / `ip route show`.",
        "success_count": 5,
    },
    {
        "case_id": "CBR-002",
        "binary": "ip",
        "exit_code": 2,
        "error_pattern": "Error: Nexthop has invalid gateway|Network is unreachable",
        "symptom": "Adding a route fails with 'Nexthop has invalid gateway' or 'Network is unreachable'",
        "root_cause": "The gateway IP is not on any directly connected L2 subnet (no local interface has an IP in the same subnet as the gateway).",
        "verified_fix": "First assign a local interface IP in the gateway's subnet (`sudo ip addr replace <local_ip>/<mask> dev <iface>` and `sudo ip link set <iface> up`) OR add an onlink route (`sudo ip route replace <subnet> via <gw> dev <iface> onlink`).",
        "success_count": 6,
    },
    {
        "case_id": "CBR-003",
        "binary": "tio",
        "exit_code": 1,
        "error_pattern": "unexpected symbol|syntax error|attempt to call|import ",
        "symptom": "tio --script fails with Lua syntax error or hangs on Python syntax",
        "root_cause": "`tio --script` uses Lua inside tio, NOT Python! Passing `import time` or Python code breaks tio.",
        "verified_fix": "Use valid Lua syntax inside `tio --script`: e.g. `expect('login: ', 5000); write('root\\r\\n'); expect('# ', 5000); write('ip addr\\r\\n'); sleep(1); exit()` or use `python3 -c 'import serial...'` instead.",
        "success_count": 8,
    },
    {
        "case_id": "CBR-004",
        "binary": "ping",
        "exit_code": 1,
        "error_pattern": "100% packet loss|Destination Host Unreachable",
        "symptom": "ICMP ping shows 100% packet loss or Destination Host Unreachable",
        "root_cause": "Target host blocks ICMP, lacks a return route back to our source IP, or L2 ARP resolution failed (`INCOMPLETE` / `FAILED`).",
        "verified_fix": "1. Check `ip neigh show` to see if ARP resolved a MAC address (if MAC is present, host is alive at L2!). 2. Check `sudo iptables -t nat -L -n -v` to ensure MASQUERADE is enabled if routing across subnets. 3. Probe TCP ports (`nmap -Pn -p 22,80,443 <ip>`).",
        "success_count": 7,
    },
    {
        "case_id": "CBR-005",
        "binary": "curl",
        "exit_code": 7,
        "error_pattern": "Failed to connect|Connection refused",
        "symptom": "curl exits with code 7 (Connection refused)",
        "root_cause": "The target host is reachable at L3, but no service is listening on that TCP port or a local firewall rejected the SYN packet.",
        "verified_fix": "Verify listening ports with `ss -tulpn` (local) or `nmap -Pn -sT --top-ports 100 <target>` (remote).",
        "success_count": 4,
    },
    {
        "case_id": "CBR-006",
        "binary": "curl",
        "exit_code": 28,
        "error_pattern": "Operation timed out|Connection timed out",
        "symptom": "curl exits with code 28 (Connection timed out)",
        "root_cause": "Packets are being silently dropped (DROP firewall policy, missing NAT MASQUERADE return path, or wrong routing table entry).",
        "verified_fix": "Check `ip route get <target_ip>`, verify ARP table `ip neigh show`, and add `--connect-timeout 5 --max-time 10` to curl.",
        "success_count": 5,
    },
    {
        "case_id": "CBR-007",
        "binary": "ssh",
        "exit_code": 255,
        "error_pattern": "Permission denied \\(publickey|Host key verification failed|no matching host key type",
        "symptom": "SSH connection fails with exit code 255",
        "root_cause": "Strict host key checking, legacy SSH algorithms on embedded router/device, or missing credentials.",
        "verified_fix": "For embedded/legacy devices, use `ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o HostKeyAlgorithms=+ssh-rsa,ssh-dss <user>@<ip>`.",
        "success_count": 4,
    },
    {
        "case_id": "CBR-008",
        "binary": "any",
        "exit_code": 127,
        "error_pattern": "command not found",
        "symptom": "Shell returns exit code 127 (command not found)",
        "root_cause": "The requested binary is not installed or is in `/sbin` / `/usr/sbin` outside non-root PATH.",
        "verified_fix": "Check `which <cmd>` or `/usr/sbin/<cmd>`, or use standard POSIX/iproute2 equivalents (`ip`, `ss`, `python3`).",
        "success_count": 5,
    },
    {
        "case_id": "CBR-009",
        "binary": "any",
        "exit_code": 1,
        "error_pattern": "is not recognized as an internal or external command|is not recognized as the name of a cmdlet",
        "symptom": "Windows CMD or PowerShell reports command/cmdlet is not recognized",
        "root_cause": "A Linux command was run on Windows, or a PowerShell cmdlet was invoked inside `cmd.exe` without `powershell -NoProfile -Command`.",
        "verified_fix": "On Windows, use `powershell -NoProfile -ExecutionPolicy Bypass -Command \"<cmdlet>\"` or native Windows tools (`ipconfig /all`, `route print`, `arp -a`, `netstat -ano`, `curl.exe`).",
        "success_count": 5,
    },
    {
        "case_id": "CBR-010",
        "binary": "any",
        "exit_code": 5,
        "error_pattern": "Access is denied|requires elevation|Operation not permitted",
        "symptom": "Command fails with 'Access is denied', 'requires elevation', or 'Operation not permitted'",
        "root_cause": "Modifying network routes, firewall rules, or protected ACLs requires Administrator (Windows) or root/sudo (Linux) privileges.",
        "verified_fix": "Use `sudo <cmd>` on Linux, an elevated Administrator shell on Windows, or non-privileged read-only inspection (`ip route show`, `route print`, `whoami /priv`).",
        "success_count": 5,
    },
    {
        "case_id": "CBR-011",
        "binary": "powershell",
        "exit_code": 1,
        "error_pattern": "running scripts is disabled on this system|PSSecurityException|AuthorizationManager check failed",
        "symptom": "PowerShell blocks script execution due to ExecutionPolicy",
        "root_cause": "Windows PowerShell Restricted execution policy blocks `.ps1` scripts by default.",
        "verified_fix": "Run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <script.ps1>` or `-Command \"...\"`.",
        "success_count": 6,
    },
    {
        "case_id": "CBR-012",
        "binary": "tio",
        "exit_code": 0,
        "error_pattern": "Command completed with exit code 0|Disconnected|Device or resource busy|Resource temporarily unavailable|Input/output error|console.*drop|too many commands",
        "symptom": "Serial console (/dev/ttyUSB0) drops connection, freezes, or returns 0 bytes ('Command completed with exit code 0') when bombarded with rapid or chained commands",
        "root_cause": "Hardware UART RX FIFO buffer overrun or rapid DTR/RTS port cycling caused by sending multiple commands without character/line pacing (-o/-O) or opening /dev/ttyUSB0 back-to-back.",
        "verified_fix": "Use hardware UART pacing `-o 15 -O 120` and send ONLY ONE command per session: `tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(500); write(\"id\\r\"); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0`.",
        "success_count": 9,
    },
]


def seed_default_cbr_library() -> None:
    """Initialize or reset `cbr_library.json` with clean cross-platform seed cases and empty failure history."""
    ensure_directories()
    data = {
        "cases": list(DEFAULT_SEED_CASES),
        "recent_failures": [],
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_json_state(CBR_LIBRARY_FILE, data)


def load_cbr_library() -> Dict[str, Any]:
    ensure_directories()
    try:
        mt1 = os.path.getmtime(CBR_LIBRARY_FILE) if os.path.exists(CBR_LIBRARY_FILE) else 0.0
        mt2 = os.path.getmtime(TRAINED_RULES_FILE) if os.path.exists(TRAINED_RULES_FILE) else 0.0
        mt3 = os.path.getmtime(LEARNED_CBR_FILE) if os.path.exists(LEARNED_CBR_FILE) else 0.0
    except OSError:
        mt1, mt2, mt3 = 0.0, 0.0, 0.0

    if _CBR_RAM_CACHE["mtimes"] == (mt1, mt2, mt3) and _CBR_RAM_CACHE["data"] is not None:
        return _CBR_RAM_CACHE["data"]

    data = load_json_state(CBR_LIBRARY_FILE, {})
    if not data or "cases" not in data:
        data = {
            "cases": list(DEFAULT_SEED_CASES),
            "recent_failures": [],
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        save_json_state(CBR_LIBRARY_FILE, data)
    else:
        existing_seed_ids = {c.get("case_id") for c in data.get("cases", []) if isinstance(c, dict)}
        seed_added = False
        for sc in DEFAULT_SEED_CASES:
            if sc["case_id"] not in existing_seed_ids:
                data["cases"].append(dict(sc))
                seed_added = True
        if seed_added:
            save_json_state(CBR_LIBRARY_FILE, data)

    # Dynamically merge verified CBR fingerprints learned from TrainingDocuments/ via train_llm.py (cached by mt2)
    if _TRAINED_CBR_CACHE["mtime"] == mt2 and _TRAINED_CBR_CACHE["fingerprints"] is not None:
        trained_cbr = _TRAINED_CBR_CACHE["fingerprints"]
    else:
        trained_data = load_json_state(TRAINED_RULES_FILE, {})
        trained_cbr = trained_data.get("cbr_fingerprints", []) if isinstance(trained_data, dict) else []
        _TRAINED_CBR_CACHE["mtime"] = mt2
        _TRAINED_CBR_CACHE["fingerprints"] = trained_cbr

    learned_data = load_json_state(LEARNED_CBR_FILE, {})
    learned_cbr = learned_data.get("cases", []) if isinstance(learned_data, dict) else []

    existing_ids = {c.get("case_id") for c in data.get("cases", [])}
    existing_patterns = {(c.get("binary"), c.get("error_pattern")) for c in data.get("cases", [])}
    merged_cases = list(data.get("cases", []))

    for idx, tc in enumerate(trained_cbr, 1):
        if not isinstance(tc, dict):
            continue
        cid = tc.get("case_id") or f"CBR-TRN-{idx:03d}"
        key = (tc.get("binary", "any"), tc.get("error_pattern", ""))
        if cid not in existing_ids and key not in existing_patterns and tc.get("error_pattern"):
            merged_cases.append(
                {
                    "case_id": cid,
                    "binary": tc.get("binary", "any"),
                    "exit_code": int(tc.get("exit_code", 1)),
                    "error_pattern": tc.get("error_pattern", ""),
                    "symptom": tc.get("symptom", f"Trained failure pattern on {tc.get('binary', 'any')}"),
                    "root_cause": tc.get("root_cause", f"Distilled from {tc.get('source_doc', 'TrainingDocuments')}"),
                    "verified_fix": tc.get("verified_fix", ""),
                    "success_count": int(tc.get("success_count", 2)),
                }
            )
            existing_ids.add(cid)
            existing_patterns.add(key)

    for idx, lc in enumerate(learned_cbr, 1):
        if not isinstance(lc, dict):
            continue
        lc_bin = str(lc.get("binary", "any")).lower()
        lc_exit = int(lc.get("exit_code", 1))
        # Guard against bogus rules learned from successful local file readers (`cat`, `head`, `ls`, `find`, `grep` with exit_code 0)
        if lc_exit == 0 and lc_bin in ("cat", "head", "tail", "ls", "find", "grep", "cd", "pwd", "echo"):
            continue
        cid = lc.get("case_id") or f"CBR-AUTO-{idx:03d}"
        pat = lc.get("error_pattern") or lc.get("stderr_pattern", "")
        key = (lc_bin, pat)
        if cid not in existing_ids and key not in existing_patterns and pat:
            merged_cases.append(
                {
                    "case_id": cid,
                    "binary": lc_bin,
                    "exit_code": lc_exit if lc_exit != 0 else 1,
                    "error_pattern": pat,
                    "symptom": lc.get("symptom", f"Online learned failure on {lc_bin}"),
                    "root_cause": lc.get("root_cause", "Online Continual Learning (Engine 16)"),
                    "verified_fix": lc.get("verified_fix") or lc.get("verified_remediation", ""),
                    "success_count": int(lc.get("success_count", 1)),
                }
            )
            existing_ids.add(cid)
            existing_patterns.add(key)

    data["cases"] = merged_cases
    compiled_list = []
    for c in merged_cases:
        pat = c.get("error_pattern", "")
        bin_name = c.get("binary", "any")
        try:
            pat_re = re.compile(pat, re.IGNORECASE) if pat else None
        except re.error:
            pat_re = None
        try:
            bin_re = re.compile(rf"\b{re.escape(bin_name)}\b", re.IGNORECASE) if (bin_name and bin_name != "any") else None
        except re.error:
            bin_re = None
        c_words = set(_WORD_TOK_RE.findall((c.get("symptom", "") + " " + c.get("root_cause", "")).lower()))
        compiled_list.append((c, pat_re, bin_re, c_words))

    _CBR_RAM_CACHE["mtimes"] = (mt1, mt2, mt3)
    _CBR_RAM_CACHE["data"] = data
    _CBR_RAM_CACHE["compiled"] = compiled_list
    return data


def _extract_binary(command: str) -> str:
    from .mdp_tactical import _split_unquoted_segments

    segments = _split_unquoted_segments((command or "").strip())
    chosen = "unknown"
    for idx, seg in enumerate(segments):
        tokens = seg.split()
        while tokens and (tokens[0] in ("sudo", "env", "timeout", "time", "nohup") or "=" in tokens[0] or tokens[0].startswith("-")):
            tokens.pop(0)
        if not tokens:
            continue
        b = os.path.basename(tokens[0]).lower()
        if b in ("cd", "echo", "printf", "export", "true") and len(segments) > 1 and idx < len(segments) - 1:
            chosen = b
            continue
        return b
    return chosen


def match_failure_fingerprint(
    command: str,
    exit_code: int,
    output_text: str,
) -> Optional[Dict[str, Any]]:
    """
    Matches a failed command `(command, exit_code, output_text)` against the CBR case library
    and records the failure occurrence in `recent_failures`.
    """
    binary = _extract_binary(command).lower()
    if exit_code == 0 and (
        binary in ("ls", "cat", "head", "tail", "grep", "egrep", "fgrep", "find", "locate", "stat", "file", "wc", "pwd", "cd", "echo")
        or not re.search(
            r"(RTNETLINK answers:|Network is unreachable|100% packet loss|Destination Host Unreachable|Connection refused|"
            r"Command completed with exit code 0|Disconnected|Device or resource busy|Resource temporarily unavailable|Input/output error)",
            output_text or "",
            re.IGNORECASE,
        )
    ):
        return None
    if (
        exit_code == 0
        and "command completed with exit code 0" in (output_text or "").lower()
        and binary != "tio"
        and "/dev/tty" not in (command or "").lower()
    ):
        return None

    lib = load_cbr_library()
    best_case = None
    best_score = 0.0
    out_txt = output_text or ""
    cmd_low = (command or "").lower()

    compiled_cases = _CBR_RAM_CACHE.get("compiled") or []
    for case, pat_re, _bin_re, _case_words in compiled_cases:
        score = 0.0
        case_bin = str(case.get("binary", "any")).lower()
        if case_bin == binary or (case_bin != "any" and re.search(rf"\b{re.escape(case_bin)}\b", cmd_low)):
            score += 0.45
        elif case_bin == "any":
            score += 0.15
        else:
            # Never match a tool-specific CBR case (e.g. `tio` CBR-003) against an unrelated binary (e.g. `ls`)
            continue

        if case.get("exit_code") == exit_code:
            score += 0.20

        if pat_re is not None and pat_re.search(out_txt):
            score += 0.65

        if score > best_score and score >= 0.55:
            best_score = score
            best_case = dict(case)
            best_case["match_confidence"] = round(min(1.0, score), 3)

    # Record in recent_failures (parameterized so concrete local IPs/paths never pollute CBR stores)
    recent = lib.get("recent_failures", [])
    recent.append(
        {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "command": parameterize_tactical_template(command[:240]),
            "binary": binary,
            "exit_code": exit_code,
            "error_excerpt": parameterize_tactical_template((output_text or "").strip()[:240]),
            "matched_case_id": best_case["case_id"] if best_case else None,
        }
    )
    lib["recent_failures"] = recent[-40:]
    lib["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_json_state(CBR_LIBRARY_FILE, lib)
    try:
        mt1_new = os.path.getmtime(CBR_LIBRARY_FILE) if os.path.exists(CBR_LIBRARY_FILE) else 0.0
        old_mtimes = _CBR_RAM_CACHE.get("mtimes") or (0.0, 0.0, 0.0)
        _CBR_RAM_CACHE["mtimes"] = (mt1_new, old_mtimes[1], old_mtimes[2])
        _CBR_RAM_CACHE["data"] = lib
    except OSError:
        pass
    return best_case


def record_cbr_resolution(
    command: str,
    exit_code: int,
    error_pattern: str,
    verified_fix: str,
    symptom: str = "",
) -> Dict[str, Any]:
    """Allows dynamically adding a newly discovered failure->resolution case to the library."""
    lib = load_cbr_library()
    cases = lib.get("cases", [])
    new_case = {
        "case_id": f"CBR-{len(cases) + 1:03d}",
        "binary": _extract_binary(command),
        "exit_code": int(exit_code),
        "error_pattern": error_pattern,
        "symptom": symptom or f"Command `{_extract_binary(command)}` failed with code {exit_code}",
        "root_cause": "Learned from live execution failure/recovery cycle.",
        "verified_fix": verified_fix,
        "success_count": 1,
    }
    cases.append(new_case)
    lib["cases"] = cases
    save_json_state(CBR_LIBRARY_FILE, lib)
    return new_case


def run_cbr_reasoning(
    problem: str,
    context_text: str = "",
    export_to_vault: bool = True,
) -> Dict[str, Any]:
    """
    Executes Engine 11 (Case-Based Reasoning & Failure Fingerprinting) over the problem
    and recent failure logs using pre-compiled regex & token sets (< 1.5 ms).
    """
    lib = load_cbr_library()
    combined = f"{problem}\n{context_text}"
    words = set(_WORD_TOK_RE.findall(combined.lower()))
    ctx = resolve_problem_targets(problem=problem)
    matched_cases: List[Dict[str, Any]] = []

    compiled_cases = _CBR_RAM_CACHE.get("compiled") or []
    for case, pat_re, bin_re, case_words in compiled_cases:
        score = 0.0
        if pat_re is not None and pat_re.search(combined):
            score += 0.65
        if bin_re is not None and bin_re.search(combined):
            score += 0.30
        if words and case_words:
            overlap = len(words & case_words)
            score += min(0.35, overlap * 0.06)

        if score >= 0.35:
            item = dict(case)
            item["relevance_score"] = round(min(1.0, score), 3)
            exec_cmd = extract_executable_cbr_command(item, ctx)
            if exec_cmd:
                item["executable_fix_command"] = exec_cmd
            matched_cases.append(item)

    matched_cases.sort(key=lambda c: c["relevance_score"], reverse=True)
    recent_failures = lib.get("recent_failures", [])[-5:]

    md_lines = [
        f"### Case-Based Reasoning (CBR) & Failure Fingerprints",
        f"- **Problem**: {problem}",
        f"- **Library Size**: `{len(lib.get('cases', []))}` verified failure cases | `{len(lib.get('recent_failures', []))}` recorded runtime failures",
        "",
        "#### Top Matched Failure Cases & Verified Fixes",
    ]
    if matched_cases:
        for c in matched_cases[:4]:
            md_lines.append(
                f"- **[{c['case_id']}] `{c['binary']}`** (Relevance `{c['relevance_score']:.2f}`): {c['symptom']}\n"
                f"  - *Root Cause*: {c['root_cause']}\n"
                f"  - *Verified Fix*: {c['verified_fix']}"
            )
    else:
        md_lines.append("- No specific failure error pattern triggered; standard CBR library standing by.")

    if recent_failures:
        md_lines.append("\n#### Recent Runtime Command Failures")
        for rf in reversed(recent_failures):
            md_lines.append(
                f"- `{rf['timestamp']}` `{rf['command'][:70]}` (exit `{rf['exit_code']}`) -> matched `{rf.get('matched_case_id') or 'None'}`"
            )

    markdown = "\n".join(md_lines)
    vault_path = None
    if export_to_vault:
        vault_path = write_reasoning_note(
            title=f"CBR Failure Fingerprints - {problem[:40]}",
            engine="cbr_fingerprints",
            content_md=markdown,
            tags=["cbr", "failure-fingerprints", "troubleshooting"],
        )

    hw = get_hardware_reasoning_limits()
    top_k = int(hw.get("cbr_top_k_retrievals", 5))
    return {
        "engine": "cbr_fingerprints",
        "hardware_tier": hw.get("tier", "HIGH_PERFORMANCE"),
        "cbr_max_library_cases": int(hw.get("cbr_max_library_cases", 1000)),
        "library_size": len(lib.get("cases", [])),
        "matched_cases": matched_cases[:top_k],
        "recent_failures": recent_failures,
        "vault_note": vault_path,
        "markdown": markdown,
    }
