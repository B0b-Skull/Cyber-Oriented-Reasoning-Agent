"""
Engine 13: Syntax-Guided Synthesis (SyGuS) & Structured Output Extractor
========================================================================
Enforces Guardrail 2 (Additive SyGuS Extraction + High Compression Threshold):
- Deterministic grammar-guided parser that extracts clean structured facts from raw CLI outputs:
  - `ip addr` / `ip -4 addr` / `ifconfig` -> `(iface, state, ipv4_cidrs, mac)`
  - `ip route` -> `(destination, gateway, dev, src)`
  - `ip neigh` / `arp -a` -> `(ip, dev, mac, state)`
  - `ss -tulpn` / `netstat` -> `(proto, local_addr_port, process)`
  - `nmap` -> `(host, port, proto, state, service)`
  - `ping` -> `(target, transmitted, received, loss_pct)`
  - `curl -i` / HTTP headers -> `(status_code, server, location)`
- Feeds structured facts directly into the L1 Symbolic State Register (`temporal_fluents.py` / `context_vm.py`).
- NEVER strips or replaces raw tool output when `len(output) <= 2,500 chars` — instead prepends a compact
  `[SyGuS Structured Summary]` block above the untouched raw output.
"""

import re
from typing import Any, Dict, List

from .vault_bridge import get_hardware_reasoning_limits, write_reasoning_note


def extract_structured_facts(command: str, raw_output: str) -> Dict[str, Any]:
    """
    Parses raw CLI stdout/stderr into structured symbolic records.
    Returns a dictionary of extracted entities and a compact 1-5 line header summary.
    """
    text = raw_output or ""
    cmd = (command or "").strip()
    facts: Dict[str, Any] = {
        "interfaces": [],
        "routes": [],
        "arp_neighbors": [],
        "open_ports": [],
        "ping_stats": [],
        "http_responses": [],
    }
    summary_lines: List[str] = []

    # 1. `ip addr` interface blocks
    if re.search(r"\bip\s+(?:-[0-9a-zA-Z]+\s+)*(?:addr|a|address)\b", cmd) or re.search(
        r"^\d+:\s+[a-zA-Z0-9_.-]+:\s+<", text, re.MULTILINE
    ):
        current_iface = None
        for line in text.splitlines():
            m_hdr = re.match(r"^\d+:\s+([a-zA-Z0-9_.-]+)(?:@\S+)?:\s+<([^>]*)>.*state\s+(\S+)", line)
            if m_hdr:
                current_iface = {
                    "iface": m_hdr.group(1),
                    "flags": m_hdr.group(2),
                    "state": m_hdr.group(3),
                    "ipv4": [],
                    "mac": None,
                }
                facts["interfaces"].append(current_iface)
            elif current_iface is not None:
                m_mac = re.search(r"link/(?:ether|loopback)\s+([0-9a-fA-F:]{17})", line)
                if m_mac:
                    current_iface["mac"] = m_mac.group(1)
                m_ip = re.search(r"\binet\s+(\d+\.\d+\.\d+\.\d+(?:/\d+)?)", line)
                if m_ip:
                    current_iface["ipv4"].append(m_ip.group(1))
        if facts["interfaces"]:
            compact_ifaces = [
                f"{i['iface']}({i['state']}): {','.join(i['ipv4']) or 'no-ipv4'}"
                for i in facts["interfaces"]
            ]
            summary_lines.append(f"Interfaces: {' | '.join(compact_ifaces[:8])}")

    # 1b. Windows `ipconfig` / `Get-NetIPAddress` interface blocks
    if "ipconfig" in cmd.lower() or "IPv4 Address" in text or "Subnet Mask" in text:
        win_iface = None
        for line in text.splitlines():
            s = line.strip()
            if s.endswith(":") and "adapter" in s.lower():
                win_iface = {
                    "iface": re.sub(r"(?i)^.*adapter\s+", "", s[:-1]).strip(),
                    "flags": "WINDOWS_ADAPTER",
                    "state": "UP",
                    "ipv4": [],
                    "mac": None,
                }
                facts["interfaces"].append(win_iface)
            elif win_iface is not None:
                if "Media disconnected" in s:
                    win_iface["state"] = "DOWN"
                m_wip = re.search(r"(?:IPv4 Address|IP Address)[^:]*:\s*(\d+\.\d+\.\d+\.\d+)", s, re.I)
                if m_wip:
                    win_iface["ipv4"].append(m_wip.group(1))
                m_wmac = re.search(r"Physical Address[^:]*:\s*([0-9A-Fa-f-]{17})", s, re.I)
                if m_wmac:
                    win_iface["mac"] = m_wmac.group(1).replace("-", ":").lower()
        if facts["interfaces"] and not any(ln.startswith("Interfaces:") for ln in summary_lines):
            compact_ifaces = [
                f"{i['iface']}({i['state']}): {','.join(i['ipv4']) or 'no-ipv4'}"
                for i in facts["interfaces"]
            ]
            summary_lines.append(f"Interfaces: {' | '.join(compact_ifaces[:8])}")

    # 2. `ip route` / Windows `route print` / `Get-NetRoute` lines
    if (
        re.search(r"\b(?:ip\s+route|route\s+print|get-netroute)\b", cmd, re.I)
        or re.search(r"\b(?:default via|\d+\.\d+\.\d+\.\d+/\d+\s+dev)\b", text)
    ):
        for line in text.splitlines():
            line_s = line.strip()
            if re.match(r"^(default|\d+\.\d+\.\d+\.\d+(?:/\d+)?)\s+(?:via|dev)\s+", line_s):
                facts["routes"].append(line_s)
            elif re.match(r"^\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+\s+(?:On-link|\d+\.\d+\.\d+\.\d+)\s+\d+\.\d+\.\d+\.\d+", line_s):
                facts["routes"].append(re.sub(r"\s+", " ", line_s))
        if facts["routes"]:
            summary_lines.append(f"Routes ({len(facts['routes'])}): " + " ; ".join(facts["routes"][:5]))

    # 3. `ip neigh` / Linux & Windows `arp -a` table
    for m_arp in re.finditer(
        r"^(\d+\.\d+\.\d+\.\d+)\s+dev\s+(\S+)(?:\s+lladdr\s+([0-9a-fA-F:]{17}))?\s+(\S+)$",
        text,
        re.MULTILINE,
    ):
        facts["arp_neighbors"].append(
            {
                "ip": m_arp.group(1),
                "dev": m_arp.group(2),
                "mac": m_arp.group(3) or "NONE",
                "state": m_arp.group(4),
            }
        )
    for m_warp in re.finditer(
        r"^\s*(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F:-]{17})\s+(dynamic|static)\b",
        text,
        re.MULTILINE | re.IGNORECASE,
    ):
        facts["arp_neighbors"].append(
            {
                "ip": m_warp.group(1),
                "dev": "lan",
                "mac": m_warp.group(2).replace("-", ":").lower(),
                "state": m_warp.group(3).upper(),
            }
        )
    if facts["arp_neighbors"]:
        arp_str = ", ".join(
            f"{a['ip']}->{a['mac']}({a['state']} on {a['dev']})" for a in facts["arp_neighbors"][:6]
        )
        summary_lines.append(f"ARP Neighbors: {arp_str}")

    # 4. `nmap`, `ss -tulpn`, Windows `netstat -ano`, or `Test-NetConnection` open ports
    for m_nmap in re.finditer(r"^(\d+)/(tcp|udp)\s+(open|filtered|closed)\s+(\S+)", text, re.MULTILINE):
        facts["open_ports"].append(
            {
                "port": int(m_nmap.group(1)),
                "proto": m_nmap.group(2),
                "state": m_nmap.group(3),
                "service": m_nmap.group(4),
            }
        )
    for m_ss in re.finditer(
        r"^(tcp|udp)\s+LISTEN\s+\d+\s+\d+\s+(\S+):(\d+)\s+\S+(?:\s+users:\(\(\"([^\"]+)\")?",
        text,
        re.MULTILINE,
    ):
        facts["open_ports"].append(
            {
                "port": int(m_ss.group(3)),
                "proto": m_ss.group(1),
                "state": "LISTEN",
                "bind": m_ss.group(2),
                "service": m_ss.group(4) or "local",
            }
        )
    for m_wnet in re.finditer(
        r"^\s*(TCP|UDP)\s+(\S+):(\d+)\s+\S+\s+(LISTENING|ESTABLISHED)(?:\s+(\d+))?",
        text,
        re.MULTILINE | re.IGNORECASE,
    ):
        facts["open_ports"].append(
            {
                "port": int(m_wnet.group(3)),
                "proto": m_wnet.group(1).lower(),
                "state": m_wnet.group(4).upper(),
                "bind": m_wnet.group(2),
                "service": f"pid:{m_wnet.group(5)}" if m_wnet.group(5) else "local",
            }
        )
    m_tnc = re.search(
        r"RemoteAddress\s*:\s*(\S+).*?RemotePort\s*:\s*(\d+).*?TcpTestSucceeded\s*:\s*(True|False)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if m_tnc:
        t_ok = m_tnc.group(3).lower() == "true"
        facts["open_ports"].append(
            {
                "port": int(m_tnc.group(2)),
                "proto": "tcp",
                "state": "open" if t_ok else "closed",
                "bind": m_tnc.group(1),
                "service": "Test-NetConnection",
            }
        )
    if facts["open_ports"]:
        ports_str = ", ".join(
            f"{p['port']}/{p['proto']}({p['state']}:{p['service']})" for p in facts["open_ports"][:8]
        )
        summary_lines.append(f"Ports: {ports_str}")

    # 5. `ping` packet statistics (Linux & Windows formats)
    m_ping = re.search(
        r"(\d+)\s+packets transmitted,\s+(\d+)\s+received,.*?(\d+(?:\.\d+)?)%\s+packet loss",
        text,
    )
    if m_ping:
        tx, rx, loss = int(m_ping.group(1)), int(m_ping.group(2)), float(m_ping.group(3))
        facts["ping_stats"].append({"tx": tx, "rx": rx, "loss_pct": loss})
        summary_lines.append(f"ICMP Ping: tx={tx}, rx={rx}, loss={loss}%")
    else:
        m_wping = re.search(
            r"Sent\s*=\s*(\d+),\s*Received\s*=\s*(\d+),\s*Lost\s*=\s*\d+\s*\((\d+(?:\.\d+)?)%\s*loss\)",
            text,
            re.IGNORECASE,
        )
        if m_wping:
            tx, rx, loss = int(m_wping.group(1)), int(m_wping.group(2)), float(m_wping.group(3))
            facts["ping_stats"].append({"tx": tx, "rx": rx, "loss_pct": loss})
            summary_lines.append(f"ICMP Ping: tx={tx}, rx={rx}, loss={loss}%")

    # 6. HTTP status lines (`curl -i` / `-I`)
    for m_http in re.finditer(r"^HTTP/\d(?:\.\d)?\s+(\d{3})\s*([^\r\n]*)", text, re.MULTILINE):
        facts["http_responses"].append({"status": int(m_http.group(1)), "reason": m_http.group(2).strip()})
    if facts["http_responses"]:
        http_str = ", ".join(f"HTTP {h['status']} {h['reason']}" for h in facts["http_responses"][:4])
        summary_lines.append(f"HTTP: {http_str}")

    facts["summary_header"] = (
        "[SyGuS Extracted Facts] " + " || ".join(summary_lines) if summary_lines else ""
    )
    return facts


def run_sygus_reasoning(
    problem: str,
    sample_output: str = "",
    export_to_vault: bool = True,
) -> Dict[str, Any]:
    """
    Runs Engine 13 (SyGuS Structured Output Extractor) over provided or live system state output.
    """
    hw = get_hardware_reasoning_limits()
    max_lines = int(hw.get("sygus_max_parse_lines", 2500))
    raw_thresh = int(hw.get("raw_preserve_threshold_chars", 2500))
    combined = "\n".join(f"{problem}\n{sample_output}".splitlines()[:max_lines])
    extracted = extract_structured_facts(problem, combined)

    md_lines = [
        "### SyGuS Grammar-Guided Structured Fact Extraction",
        f"- **Guardrail 2 Policy**: Additive-only header injection for outputs `<= {raw_thresh:,} chars` (100% raw text preserved); full raw logs archived in `Reasoning/data/shadow_archive/` when `> {raw_thresh:,} chars`.",
        f"- **Summary Header**: `{extracted.get('summary_header') or 'No CLI telemetry patterns in prompt text (ready for live tool output).'}`",
        "",
        "#### Extracted Symbolic Entities",
        f"- **Interfaces Parsed**: `{len(extracted['interfaces'])}`",
        f"- **Routes Parsed**: `{len(extracted['routes'])}`",
        f"- **ARP Neighbors Parsed**: `{len(extracted['arp_neighbors'])}`",
        f"- **Ports / Listeners Parsed**: `{len(extracted['open_ports'])}`",
        f"- **ICMP / HTTP Probes Parsed**: `{len(extracted['ping_stats']) + len(extracted['http_responses'])}`",
    ]

    markdown = "\n".join(md_lines)
    vault_path = None
    if export_to_vault:
        vault_path = write_reasoning_note(
            title=f"SyGuS Fact Extraction - {problem[:40]}",
            engine="sygus_extractor",
            content_md=markdown,
            tags=["sygus", "parser", "structured-extraction"],
        )

    return {
        "engine": "sygus_extractor",
        "extracted": extracted,
        "vault_note": vault_path,
        "markdown": markdown,
    }
