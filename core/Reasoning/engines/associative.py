"""
Engine 5: Associative Spreading Activation & Bipartite Obsidian Vault Graph Engine.
100% CPU execution via `networkx` & `scipy` (0 MB GPU VRAM).

Capabilities:
- Parses the entire `ObsidianVault/` (`targets/`, `commands/`, `projects/`, `knowledge/`, `reasoning/`)
  into a rich Bipartite / Heterogeneous Concept Graph connecting:
    * Note Nodes (`note:<category>/<slug>`)
    * Concept Nodes: `[[WikiLinks]]`, `#tags`, IPv4/CIDR addresses, hardware devices (`/dev/ttyUSB*`),
      CLI tools (`tio`, `curl`, `iptables`, `ip`, `sysctl`, `nmap`), and Causal/Bayesian hypothesis keys.
- Executes ACT-R style Spreading Activation & Personalized PageRank (`nx.pagerank` with seed
  personalization vector + multi-hop decay) from any problem statement or target query.
- Discovers hidden 2-hop and 3-hop "Bridge Concepts" and multi-hop associative paths connecting
  seemingly unrelated notes (e.g. connecting a failed API scan to `tio_serial_playbook` via `/dev/ttyUSB0`).
- Persists graph topology snapshots to `Reasoning/data/associative_graphs/` and optionally writes
  associative synthesis notes to `ObsidianVault/reasoning/`.
"""
import copy
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .vault_bridge import (
    DATA_DIR,
    VAULT_DIR,
    ensure_directories,
    get_hardware_reasoning_limits,
    load_json_state,
    save_json_data,
    save_json_state,
    save_reasoning_to_vault,
    slugify,
)

VAULT_ENTITIES_CACHE_FILE = str(DATA_DIR / "vault_entities_cache.json")

KNOWN_TECH_CONCEPTS = {
    "tio", "curl", "nmap", "iptables", "nftables", "sysctl", "ip_forward", "masquerade",
    "proxy_arp", "vlan", "arp", "bridge", "ttyusb0", "ttyusb1", "serial", "loopback",
    "reverse_proxy", "bearer", "csrf", "cookie", "x-forwarded-for", "ssh", "socat", "tcpdump",
    "netstat", "ipconfig", "wmic", "icacls", "cacls", "bcdedit", "auditpol", "wevtutil",
    "netsh", "powershell", "pslist", "listdlls", "autorunsc", "dsquery", "tshark", "p0f", "snort",
    "tasklist", "systeminfo", "reg", "sc", "schtasks", "forfiles", "findstr", "takeown",
    "whoami", "gpresult", "nltest", "certutil", "klist", "setspn", "winrm", "psservice",
    "psloggedon", "psloglist", "procdump", "handle", "sigcheck", "accesschk", "tcpvcon",
    "pktmon", "get-ciminstance", "get-winevent", "get-process", "get-service", "get-netadapter",
    "get-nettcpconnection", "get-netroute", "test-netconnection", "invoke-webrequest",
    "invoke-command", "ss", "iproute2", "journalctl", "systemctl", "lsof", "fuser", "strace",
    "findmnt", "lsblk", "getcap", "capsh", "sudo", "chmod", "chown", "find", "grep", "awk",
    "openssl", "wireshark", "bpf", "autopsy", "encase", "ntfs", "mft", "oplocks", "kerberos",
    "ldap", "smb", "rdp", "mpls", "gmpls", "sd-wan", "gpon", "otn", "lte", "5g", "gsm",
    "umts", "sdr", "sqli", "informix", "oracle", "mysql", "mssql", "postgres", "aslr", "dep",
    "pe_header", "apt28", "sysinternals", "windows", "linux", "solaris",
    "revengai", "reait", "creait", "sdk-python", "plugin-ghidra", "plugin-ida", "plugin-binary-ninja",
    "reai-r2", "reai-rz", "ghidra", "ida", "radare2", "rabin2", "rizin", "cutter", "dumpbin",
    "readelf", "objdump", "strings64", "upx", "yara", "sbom", "binnet", "decompile", "disassemble", "unstrip",
    "velociraptor", "hayabusa", "chainsaw", "mftecmd", "pecmd", "amcacheparser", "appcompatcacheparser",
    "recmd", "srumecmd", "srum", "usnjrnl", "prefetch", "amcache", "shimcache", "shellbags", "userassist",
    "vssadmin", "esentutl", "volatility3", "memprocfs", "winpmem", "hollowshunter", "uac", "avml", "lime",
    "dwarf2json", "sleuthkit", "fls", "icat", "mactime", "plaso", "log2timeline", "tracee", "unhide",
    "zeek", "bpftool", "debugfs", "utmpdump", "ausearch", "aureport", "memfd",
}

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
_FM_TAGS_RE = re.compile(r"(?m)^tags:\s*\[([^\]]+)\]")
_FM_YAML_TAGS_BLOCK_RE = re.compile(r"(?ms)^tags:\s*\r?\n((?:[ \t]+-[ \t]+[^\r\n]+\r?\n?)+)")
_INLINE_TAG_RE = re.compile(r"(?:^|\s)#([a-zA-Z][a-zA-Z0-9_\-]{1,30})\b")
_IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b")
_DEV_RE = re.compile(r"(?:/dev/[a-zA-Z0-9_\-]+|\bCOM[1-9]\d*\b)")
_SUMMARY_RE = re.compile(r"(?m)^summary:\s*(.+)$")
_WHEN_TO_APPLY_RE = re.compile(r"(?m)^when_to_apply:\s*(.+)$")
_OS_PLATFORM_RE = re.compile(r"(?m)^os_platform:\s*(.+)$")
_DOMAIN_HUB_RE = re.compile(r"(?m)^domain_hub:\s*(.+)$")
_TEAM_ROLE_RE = re.compile(r"(?m)^team_role:\s*(.+)$")
_TECH_CONCEPTS_RE = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in sorted(KNOWN_TECH_CONCEPTS, key=len, reverse=True)) + r")\b"
)

_BLUE_TEAM_INTENT_RE = re.compile(
    r"\b(?:blue[\s_\-]*team|defend|defensive|harden|hardening|lockdown|contain|containment|eradicate|eradication|"
    r"remediate|remediation|mitigate|mitigation|patch|block[\s_\-]+ip|firewall[\s_\-]+rule|acl[\s_\-]+lockdown|"
    r"audit[\s_\-]+policy|runasppl|wdigest)\b",
    re.I,
)
_RED_TEAM_INTENT_RE = re.compile(
    r"\b(?:red[\s_\-]*team|offensive|adversary[\s_\-]*emulation|pentest|exploit|exploitation|payload|bypass|"
    r"privesc|privilege[\s_\-]+escalation|kerberoast|lateral[\s_\-]+movement|pivot|pivoting|portproxy|"
    r"reverse[\s_\-]+shell|masquerade|oob[\s_\-]+unlock|berserker)\b",
    re.I,
)
_HUNT_TEAM_INTENT_RE = re.compile(
    r"\b(?:hunt[\s_\-]*team|threat[\s_\-]*hunt|threat[\s_\-]*hunting|assumed[\s_\-]*breach|anomaly|anomalies|"
    r"ioc|ioa|persistence[\s_\-]*hunt|lolbin|hollowing|unbacked|rwxp|timestomp|ads[\s_\-]*stream|beacon|beaconing|"
    r"c2|rootkit|dfir|forensic|forensics|autorunsc|p0f|pcap)\b",
    re.I,
)
_REVENG_INTENT_RE = re.compile(
    r"\b(?:reverse[\s_\-]*engineer|reverse[\s_\-]*engineering|reversing|revengai|reveng\.ai|reait|creait|"
    r"sdk[\s_\-]*python|plugin[\s_\-]*ghidra|plugin[\s_\-]*ida|plugin[\s_\-]*binary[\s_\-]*ninja|reai[\s_\-]*r2|"
    r"reai[\s_\-]*rz|ghidra|ida[\s_\-]*pro|binary[\s_\-]*ninja|radare2|rizin|cutter|rabin2|dumpbin|readelf|"
    r"objdump|decompile|decompilation|disassemble|disassembly|unstrip|unstripping|binnet|binary[\s_\-]*similarity|"
    r"pe[\s_\-]*header|elf[\s_\-]*binary|upx|sbom)\b",
    re.I,
)
_WINDOWS_FORENSICS_INTENT_RE = re.compile(
    r"\b(?:windows[\s_\-]*forensic|windows[\s_\-]*forensics|windows[\s_\-]*dfir|mftecmd|pecmd|amcacheparser|"
    r"appcompatcacheparser|recmd|srumecmd|srum|srudb|usnjrnl|prefetch|amcache|shimcache|shellbags|userassist|"
    r"vssadmin|esentutl|hayabusa|chainsaw|memprocfs|winpmem|hollowshunter|evtx|ntuser\.dat|usrclass\.dat)\b",
    re.I,
)
_LINUX_FORENSICS_INTENT_RE = re.compile(
    r"\b(?:linux[\s_\-]*forensic|linux[\s_\-]*forensics|linux[\s_\-]*dfir|uac|avml|lime|dwarf2json|sleuthkit|"
    r"mactime|plaso|log2timeline|tracee|unhide|bpftool|debugfs|utmpdump|wtmp|btmp|memfd|ld\.so\.preload|"
    r"crtime|dtime)\b",
    re.I,
)


def infer_team_role_from_query(query: str) -> str:
    """Infer whether a query/problem primarily aligns with `blue_team`, `red_team`, `hunt_team`, `reverse_engineering`, `windows_forensics`, or `linux_forensics`."""
    q_low = (query or "").lower()
    if not q_low:
        return ""
    blue_hits = len(_BLUE_TEAM_INTENT_RE.findall(q_low))
    red_hits = len(_RED_TEAM_INTENT_RE.findall(q_low))
    hunt_hits = len(_HUNT_TEAM_INTENT_RE.findall(q_low))
    reveng_hits = len(_REVENG_INTENT_RE.findall(q_low))
    win_dfir_hits = len(_WINDOWS_FORENSICS_INTENT_RE.findall(q_low))
    lin_dfir_hits = len(_LINUX_FORENSICS_INTENT_RE.findall(q_low))
    if "blue team" in q_low or "blue_team" in q_low:
        blue_hits += 4
    if "red team" in q_low or "red_team" in q_low:
        red_hits += 4
    if "hunt team" in q_low or "hunt_team" in q_low or "threat hunt" in q_low:
        hunt_hits += 4
    if any(k in q_low for k in ("reverse engineer", "reverse_engineer", "revengai", "reveng.ai", "reait")):
        reveng_hits += 5
    if ("forensic" in q_low or "dfir" in q_low or "volatility" in q_low or "velociraptor" in q_low) and any(
        k in q_low for k in ("windows", "ntfs", "mft", "evtx", "registry", "prefetch", "amcache", "srum")
    ):
        win_dfir_hits += 5
    if ("forensic" in q_low or "dfir" in q_low or "volatility" in q_low or "velociraptor" in q_low) and any(
        k in q_low for k in ("linux", "unix", "/proc", "ext4", "inode", "journalctl", "auditd", "wtmp", "avml", "lime")
    ):
        lin_dfir_hits += 5
    best_role, best_score = "", 0
    for role, sc in (
        ("windows_forensics", win_dfir_hits),
        ("linux_forensics", lin_dfir_hits),
        ("reverse_engineering", reveng_hits),
        ("blue_team", blue_hits),
        ("red_team", red_hits),
        ("hunt_team", hunt_hits),
    ):
        if sc > best_score:
            best_role, best_score = role, sc
    return best_role if best_score > 0 else ""

_GRAPH_CACHE: Dict[str, Any] = {
    "signature": None,
    "graph": None,
    "metadata": None,
    "last_check_ts": 0.0,
}

_PPR_QUERY_CACHE: Dict[Tuple[Any, ...], Dict[str, Any]] = {}


def _strip_yaml_quotes(val: str) -> str:
    s = (val or "").strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return s[1:-1].strip()
    return s


def _extract_entities_from_markdown(rel_note: str, text: str) -> Dict[str, Set[str]]:
    """Extract structured concepts (wikilinks, tags, IPs/CIDRs, devices, CLI tools) from a Vault note using pre-compiled regexes."""
    entities: Dict[str, Set[str]] = {
        "wikilinks": set(),
        "tags": set(),
        "ips_and_cidrs": set(),
        "devices": set(),
        "tech_concepts": set(),
    }

    # 1. WikiLinks [[category/note]] or [[note]]
    for m in _WIKILINK_RE.findall(text):
        cleaned = m.strip().strip("/")
        if cleaned and not cleaned.startswith("00_"):
            entities["wikilinks"].add(cleaned.lower())

    # 2. Frontmatter tags: [a, b, c], multi-line YAML tags:\n  - a, and inline #tags
    fm_match = _FM_TAGS_RE.search(text)
    if fm_match:
        for t in fm_match.group(1).split(","):
            ct = re.sub(r"[^a-zA-Z0-9_\-]", "", t.strip()).lower()
            if ct:
                entities["tags"].add(ct)

    fm_yaml_match = _FM_YAML_TAGS_BLOCK_RE.search(text[:1500])
    if fm_yaml_match:
        for ln in fm_yaml_match.group(1).splitlines():
            item = re.sub(r"^[ \t]*-[ \t]*", "", ln).strip()
            ct = re.sub(r"[^a-zA-Z0-9_\-]", "", item).lower()
            if ct:
                entities["tags"].add(ct)

    for m in _INLINE_TAG_RE.findall(text):
        entities["tags"].add(m.lower())

    # 3. IPv4 addresses and CIDR blocks
    for m in _IPV4_RE.findall(text):
        if not m.startswith("0.0.0.") and not m.startswith("255."):
            entities["ips_and_cidrs"].add(m)

    # 4. Device paths (/dev/ttyUSB0, COM1, etc.)
    for m in _DEV_RE.findall(text):
        entities["devices"].add(m.lower())

    # 5. Technical concepts & tools (single-pass compiled alternation regex)
    lower_text = f"{rel_note} {text}".lower()
    for kw in _TECH_CONCEPTS_RE.findall(lower_text):
        entities["tech_concepts"].add(kw)

    return entities


def build_vault_bipartite_graph() -> Tuple[Any, Dict[str, Dict[str, Any]]]:
    """
    Construct the heterogeneous bipartite NetworkX graph over all Markdown notes in `ObsidianVault/`.
    Partition A (`bipartite=0`): Note nodes (`note:<rel_path>`)
    Partition B (`bipartite=1`): Concept/Entity nodes (`ip:...`, `dev:...`, `tag:...`, `concept:...`)
    Plus direct note-to-note `[[WikiLink]]` edges.
    Uses a 5.0s monotonic RAM cache + a persistent `(mtime_ns, size)` disk entity index
    (`Reasoning/data/vault_entities_cache.json`) so cold CLI starts build in `< 35 ms`.
    """
    import networkx as nx

    ensure_directories()
    if not VAULT_DIR.is_dir():
        return nx.Graph(), {}

    now_mono = time.monotonic()
    if (
        _GRAPH_CACHE.get("graph") is not None
        and _GRAPH_CACHE.get("metadata") is not None
        and (now_mono - float(_GRAPH_CACHE.get("last_check_ts", 0.0))) < 5.0
    ):
        return _GRAPH_CACHE["graph"], _GRAPH_CACHE["metadata"]

    md_files: List[Tuple[Path, int, int]] = []
    sig_parts: List[Tuple[str, int, int]] = []
    for md_path in sorted(VAULT_DIR.rglob("*.md")):
        if ".obsidian" in md_path.parts or "archive" in md_path.parts or md_path.name.startswith("00_"):
            continue
        try:
            st = md_path.stat()
            mtime_ns = int(st.st_mtime_ns)
            fsize = int(st.st_size)
            # Volatile self-echo files (`projects/goal_*.md` and auto-generated `reasoning/*.md`) are indexed by path existence
            # rather than mtime_ns, whereas curated strategy playbooks (`*_strategy_playbook.md`) are tracked by mtime_ns.
            is_team_playbook = md_path.name.endswith("_strategy_playbook.md")
            is_volatile = (("reasoning" in md_path.parts) and not is_team_playbook) or md_path.name.startswith("goal_")
            sig_parts.append((str(md_path), 0 if is_volatile else mtime_ns, 0 if is_volatile else fsize))
            md_files.append((md_path, mtime_ns, fsize))
        except Exception:
            continue

    sig = tuple(sig_parts)
    if _GRAPH_CACHE.get("signature") == sig and _GRAPH_CACHE.get("graph") is not None:
        _GRAPH_CACHE["last_check_ts"] = now_mono
        return _GRAPH_CACHE["graph"], _GRAPH_CACHE["metadata"]

    disk_cache = load_json_state(VAULT_ENTITIES_CACHE_FILE, {"files": {}})
    cached_files_map: Dict[str, Dict[str, Any]] = (
        disk_cache.get("files", {}) if isinstance(disk_cache, dict) and isinstance(disk_cache.get("files"), dict) else {}
    )
    disk_cache_dirty = False

    G = nx.Graph()
    note_metadata: Dict[str, Dict[str, Any]] = {}

    for md_path, mtime_ns, fsize in md_files:
        rel_Obj = md_path.relative_to(VAULT_DIR).with_suffix("")
        rel_str = str(rel_Obj).replace("\\", "/")
        if rel_str == "00_MEMORY_INDEX":
            continue

        cache_entry = cached_files_map.get(rel_str)
        if (
            isinstance(cache_entry, dict)
            and cache_entry.get("mtime_ns") == mtime_ns
            and cache_entry.get("size") == fsize
            and isinstance(cache_entry.get("entities"), dict)
            and "when_to_apply" in cache_entry
        ):
            summary = str(cache_entry.get("summary") or rel_str)
            when_to_apply = str(cache_entry.get("when_to_apply") or "")
            os_platform = str(cache_entry.get("os_platform") or "cross-platform")
            domain_hub = str(cache_entry.get("domain_hub") or "")
            team_role = str(cache_entry.get("team_role") or "")
            extracted = cache_entry["entities"]
        else:
            try:
                text = md_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            summary_m = _SUMMARY_RE.search(text)
            summary = _strip_yaml_quotes(summary_m.group(1)) if summary_m else rel_str
            wta_m = _WHEN_TO_APPLY_RE.search(text)
            when_to_apply = _strip_yaml_quotes(wta_m.group(1)) if wta_m else ""
            os_m = _OS_PLATFORM_RE.search(text)
            os_platform = _strip_yaml_quotes(os_m.group(1)) if os_m else "cross-platform"
            hub_m = _DOMAIN_HUB_RE.search(text)
            domain_hub = _strip_yaml_quotes(hub_m.group(1)) if hub_m else ""
            tr_m = _TEAM_ROLE_RE.search(text)
            team_role = _strip_yaml_quotes(tr_m.group(1)) if tr_m else ""
            raw_ext = _extract_entities_from_markdown(rel_str, text)
            extracted = {k: sorted(v) for k, v in raw_ext.items()}
            cached_files_map[rel_str] = {
                "mtime_ns": mtime_ns,
                "size": fsize,
                "summary": summary,
                "when_to_apply": when_to_apply,
                "os_platform": os_platform,
                "domain_hub": domain_hub,
                "team_role": team_role,
                "entities": extracted,
            }
            disk_cache_dirty = True

        note_id = f"note:{rel_str.lower()}"
        category = rel_Obj.parts[0] if len(rel_Obj.parts) > 1 else "root"
        is_team_playbook = rel_str.lower().endswith("_strategy_playbook")
        # Curated strategy playbooks (`blue/red/hunt_team_strategy_playbook`, `reverse_engineering_strategy_playbook`)
        # and operational notes have higher edge authority than auto-generated `reasoning/` reports.
        cat_mult = 1.65 if is_team_playbook else (0.65 if category == "reasoning" else 1.35)

        G.add_node(
            note_id,
            node_type="note",
            bipartite=0,
            label=rel_str,
            category=category,
            summary=summary,
            when_to_apply=when_to_apply,
            os_platform=os_platform,
            domain_hub=domain_hub,
            team_role=team_role,
        )
        note_metadata[note_id] = {
            "wiki_link": rel_str,
            "category": category,
            "summary": summary,
            "when_to_apply": when_to_apply,
            "os_platform": os_platform,
            "domain_hub": domain_hub,
            "team_role": team_role,
            "path": str(md_path),
        }

        for wl in extracted.get("wikilinks", ()):
            if wl.startswith("00_"):
                continue
            target_note_id = f"note:{wl}"
            if not G.has_node(target_note_id):
                G.add_node(target_note_id, node_type="note", bipartite=0, label=wl, category="linked", summary=wl)
            if wl in (
                "commands/windows_master_command_playbook",
                "commands/linux_master_command_playbook",
                "commands/tio_serial_playbook",
                "commands/curl_playbook",
            ):
                wl_weight = 0.05 * cat_mult
            elif wl.startswith("knowledge/0") or wl.startswith("knowledge/10_"):
                wl_weight = 0.25 * cat_mult
            else:
                wl_weight = 2.5 * cat_mult
            G.add_edge(note_id, target_note_id, weight=wl_weight, relation="wikilink")

        for ip_str in extracted.get("ips_and_cidrs", ()):
            cid = f"ip:{ip_str}"
            G.add_node(cid, node_type="ip_or_cidr", bipartite=1, label=ip_str)
            G.add_edge(note_id, cid, weight=2.2 * cat_mult, relation="mentions_ip")

        for dev in extracted.get("devices", ()):
            cid = f"dev:{dev}"
            G.add_node(cid, node_type="device", bipartite=1, label=dev)
            G.add_edge(note_id, cid, weight=2.4 * cat_mult, relation="uses_device")

        for tech in extracted.get("tech_concepts", ()):
            cid = f"concept:{tech}"
            G.add_node(cid, node_type="concept", bipartite=1, label=tech)
            G.add_edge(note_id, cid, weight=1.6 * cat_mult, relation="uses_concept")

        for tag in extracted.get("tags", ()):
            cid = f"tag:{tag}"
            G.add_node(cid, node_type="tag", bipartite=1, label=f"#{tag}")
            G.add_edge(note_id, cid, weight=1.2 * cat_mult, relation="tagged_with")

    if disk_cache_dirty:
        try:
            save_json_state(VAULT_ENTITIES_CACHE_FILE, {"files": cached_files_map})
        except Exception:
            pass

    # Precompute vectorized PageRank transition arrays & neighbor lookups for < 1.5 ms query latency
    import numpy as np

    node_list = list(G.nodes())
    n_nodes = len(node_list)
    node_to_idx = {n: i for i, n in enumerate(node_list)}
    search_index: List[Tuple[int, str, str, str, float]] = []
    note_connected_concepts: Dict[str, List[str]] = {}
    concept_connected_notes: Dict[str, List[str]] = {}

    for idx, node in enumerate(node_list):
        ndata = G.nodes[node]
        label_low = str(ndata.get("label", node)).lower()
        summary_low = (
            f"{ndata.get('summary', '')} {ndata.get('when_to_apply', '')} {ndata.get('os_platform', '')}"
        ).lower()
        cat_low = str(ndata.get("category", "")).lower()
        is_team_playbook = label_low.endswith("_strategy_playbook")
        is_hub_or_master = bool(
            re.search(
                r"(?:^|/)(?:0[1-9]_|10_|windows_master_|linux_master_|curl_playbook|tio_serial_playbook|revengai_and_binary_reversing_playbook|(?:windows|linux)_digital_forensics_playbook|(?:blue_team|red_team|hunt_team|reverse_engineering|windows_digital_forensics|linux_digital_forensics)_strategy_playbook)",
                label_low,
            )
        )
        cat_boost = 2.05 if is_team_playbook else (0.65 if cat_low == "reasoning" else (1.85 if is_hub_or_master else 1.5))
        search_index.append((idx, node, label_low, summary_low, cat_boost))
        if ndata.get("bipartite") == 0:
            note_connected_concepts[node] = [
                G.nodes[nbr].get("label", nbr)
                for nbr in G.neighbors(node)
                if G.nodes[nbr].get("bipartite") == 1
            ][:8]
        elif ndata.get("bipartite") == 1:
            c_notes = [
                G.nodes[nbr].get("label", nbr)
                for nbr in G.neighbors(node)
                if G.nodes[nbr].get("bipartite") == 0
            ]
            if len(c_notes) >= 2:
                concept_connected_notes[node] = c_notes

    src_list: List[int] = []
    dst_list: List[int] = []
    w_list: List[float] = []
    out_deg = np.zeros(max(1, n_nodes), dtype=np.float64)
    for u, v, edata in G.edges(data=True):
        ui = node_to_idx[u]
        vi = node_to_idx[v]
        w = float(edata.get("weight", 1.0))
        src_list.extend((ui, vi))
        dst_list.extend((vi, ui))
        w_list.extend((w, w))
        out_deg[ui] += w
        out_deg[vi] += w

    edge_src = np.array(src_list, dtype=np.int32)
    edge_dst = np.array(dst_list, dtype=np.int32)
    edge_w = np.array(w_list, dtype=np.float64)
    if len(edge_src) > 0:
        denom = np.where(out_deg[edge_src] > 1e-12, out_deg[edge_src], 1.0)
        edge_norm_w = edge_w / denom
    else:
        edge_norm_w = edge_w

    _GRAPH_CACHE["signature"] = sig
    _GRAPH_CACHE["graph"] = G
    _GRAPH_CACHE["metadata"] = note_metadata
    _GRAPH_CACHE["node_list"] = node_list
    _GRAPH_CACHE["search_index"] = search_index
    _GRAPH_CACHE["note_connected_concepts"] = note_connected_concepts
    _GRAPH_CACHE["concept_connected_notes"] = concept_connected_notes
    _GRAPH_CACHE["edge_src"] = edge_src
    _GRAPH_CACHE["edge_dst"] = edge_dst
    _GRAPH_CACHE["edge_norm_w"] = edge_norm_w
    _GRAPH_CACHE["dangling_mask"] = (out_deg <= 1e-12)
    _GRAPH_CACHE["last_check_ts"] = now_mono
    _PPR_QUERY_CACHE.clear()
    return G, note_metadata



def run_associative_vault_reasoning(
    query: str,
    seed_concepts: Optional[List[str]] = None,
    alpha_damping: float = 0.82,
    top_k: int = 6,
    save_to_vault: bool = False,
) -> Dict[str, Any]:
    """
    Execute Spreading Activation & Personalized PageRank across the ObsidianVault Bipartite Graph
    to surface multi-hop associative notes, hidden bridge concepts, and conceptual leap paths.
    """
    import networkx as nx

    try:
        if isinstance(query, (list, tuple, set)):
            query = " ".join(str(x) for x in query)
        else:
            query = str(query or "")
        G, note_metadata = build_vault_bipartite_graph()
        if G.number_of_nodes() == 0:
            return {
                "engine": "associative_vault_pagerank",
                "query": query,
                "num_graph_nodes": 0,
                "num_graph_edges": 0,
                "activated_notes": [],
                "bridge_concepts": [],
                "conceptual_leap_paths": [],
                "markdown_report": "*(ObsidianVault graph is currently empty)*",
            }

        cache_key = (
            id(G),
            query,
            tuple(seed_concepts or ()),
            round(float(alpha_damping), 4),
            int(top_k),
        )
        if not save_to_vault and cache_key in _PPR_QUERY_CACHE:
            return copy.deepcopy(_PPR_QUERY_CACHE[cache_key])

        raw_tokens = {t for t in re.findall(r"[a-zA-Z0-9_.\-/]+", query.lower()) if len(t) >= 2}
        if seed_concepts:
            for sc in seed_concepts:
                raw_tokens.update(t for t in re.findall(r"[a-zA-Z0-9_.\-/]+", str(sc).lower()) if len(t) >= 2)

        import numpy as np

        node_list: List[str] = _GRAPH_CACHE.get("node_list") or list(G.nodes())
        n_nodes = len(node_list)
        search_index = _GRAPH_CACHE.get("search_index") or []
        note_connected_concepts = _GRAPH_CACHE.get("note_connected_concepts") or {}
        concept_connected_notes = _GRAPH_CACHE.get("concept_connected_notes") or {}
        edge_src = _GRAPH_CACHE.get("edge_src")
        edge_dst = _GRAPH_CACHE.get("edge_dst")
        edge_norm_w = _GRAPH_CACHE.get("edge_norm_w")
        dangling_mask = _GRAPH_CACHE.get("dangling_mask")

        # Build IDF-weighted Personalized PageRank seed activation vector so specific command/tool
        # tokens (e.g. `auditpol`, `wevtutil`, `bpf`, `tio`, `netsh`) strongly outweigh generic OS words (`windows`, `linux`).
        import math

        tok_df: Dict[str, int] = {tok: 0 for tok in raw_tokens}
        for _idx, _node, label_low, summary_low, _cb in search_index:
            for tok in raw_tokens:
                if tok in label_low or tok in summary_low:
                    tok_df[tok] += 1
        tok_idf: Dict[str, float] = {
            tok: max(0.25, math.log(1.0 + float(max(1, n_nodes)) / float(1 + df)))
            for tok, df in tok_df.items()
        }

        pers_vec = np.full(n_nodes, 0.002, dtype=np.float64)
        matched_seed_nodes: List[str] = []

        inferred_team_role = infer_team_role_from_query(query)
        role_to_playbook = {
            "windows_forensics": "windows_digital_forensics_strategy_playbook",
            "linux_forensics": "linux_digital_forensics_strategy_playbook",
        }
        pb_slug = role_to_playbook.get(inferred_team_role, f"{inferred_team_role}_strategy_playbook")
        target_team_note = f"note:reasoning/{pb_slug}" if inferred_team_role else ""

        for idx, node, label_low, summary_low, cat_boost in search_index:
            score = 0.0
            label_clean = label_low.lstrip("#")
            for tok in raw_tokens:
                idf_w = tok_idf.get(tok, 1.0)
                if tok == label_low or tok == label_clean:
                    score += 5.0 * cat_boost * idf_w
                elif tok in label_low:
                    score += 3.2 * cat_boost * idf_w
                elif tok in summary_low:
                    score += 1.1 * cat_boost * idf_w
            if target_team_note:
                if node == target_team_note:
                    score += 18.0 * cat_boost
                elif node.endswith("_strategy_playbook"):
                    score *= 0.05
            if score > 0.0:
                pers_vec[idx] = score
                matched_seed_nodes.append(node)

        pers_sum = float(np.sum(pers_vec)) or 1.0
        pers_vec /= pers_sum

        # Fast vectorized Personalized PageRank power iteration (< 0.8 ms for 1,000+ nodes)
        if edge_src is not None and len(edge_src) > 0:
            p = pers_vec.copy()
            for _ in range(35):
                p_prev = p
                dangling_mass = float(np.sum(p_prev[dangling_mask])) if dangling_mask is not None else 0.0
                p = (1.0 - alpha_damping + alpha_damping * dangling_mass) * pers_vec
                np.add.at(p, edge_dst, alpha_damping * p_prev[edge_src] * edge_norm_w)
                if float(np.sum(np.abs(p - p_prev))) < 1e-6:
                    break
            final_p = 0.55 * pers_vec + 0.45 * p
            ppr_scores = {node_list[i]: float(final_p[i]) for i in range(n_nodes)}
        else:
            total_deg = sum(dict(G.degree()).values()) or 1
            ppr_scores = {n: G.degree(n) / total_deg for n in G.nodes()}

        # Separate ranked notes (`bipartite=0`) and bridge concepts (`bipartite=1`)
        activated_notes = []
        bridge_concepts = []

        for node, act_score in ppr_scores.items():
            if node in note_metadata:
                meta = note_metadata[node]
                activated_notes.append(
                    {
                        "node_id": node,
                        "wiki_link": meta["wiki_link"],
                        "category": meta["category"],
                        "summary": meta["summary"],
                        "when_to_apply": meta.get("when_to_apply", ""),
                        "os_platform": meta.get("os_platform", "cross-platform"),
                        "domain_hub": meta.get("domain_hub", ""),
                        "team_role": meta.get("team_role", ""),
                        "activation_score": round(float(act_score), 5),
                        "shared_concepts": note_connected_concepts.get(node, []),
                    }
                )
            elif node in concept_connected_notes:
                ndata = G.nodes[node]
                c_notes = concept_connected_notes[node]
                bridge_concepts.append(
                    {
                        "concept": ndata.get("label", node),
                        "type": ndata.get("node_type", "concept"),
                        "activation_score": round(float(act_score), 5),
                        "bridged_notes_count": len(c_notes),
                        "bridged_notes": c_notes[:5],
                    }
                )

        activated_notes.sort(key=lambda x: -x["activation_score"])
        bridge_concepts.sort(key=lambda x: (-x["activation_score"], -x["bridged_notes_count"]))

        # Discover multi-hop Conceptual Leap Paths between top activated notes from different categories
        conceptual_leap_paths = []
        top_note_nodes = [item["node_id"] for item in activated_notes[:5]]
        for i in range(len(top_note_nodes)):
            for j in range(i + 1, len(top_note_nodes)):
                u, v = top_note_nodes[i], top_note_nodes[j]
                if G.nodes[u].get("category") == G.nodes[v].get("category"):
                    continue
                if nx.has_path(G, u, v):
                    shortest = nx.shortest_path(G, source=u, target=v)
                    if 2 <= len(shortest) <= 5:
                        readable_chain = " $\\leftrightarrow$ ".join(
                            f"`[[{G.nodes[n].get('label', n)}]]`"
                            if G.nodes[n].get("bipartite") == 0
                            else f"**`{G.nodes[n].get('label', n)}`**"
                            for n in shortest
                        )
                        conceptual_leap_paths.append(
                            {
                                "from_note": G.nodes[u].get("label", u),
                                "to_note": G.nodes[v].get("label", v),
                                "hops": len(shortest) - 1,
                                "path_chain": readable_chain,
                            }
                        )
                if len(conceptual_leap_paths) >= 4:
                    break
            if len(conceptual_leap_paths) >= 4:
                break

        md_lines = [
            f"## Associative Spreading Activation & Bipartite Vault Graph",
            f"- **Query / Context:** {query}",
            f"- **Bipartite Graph Scale:** `{G.number_of_nodes()} nodes` (`{len(note_metadata)} Vault notes` + `{G.number_of_nodes() - len(note_metadata)} extracted entities/concepts`), `{G.number_of_edges()} associative edges`",
            f"- **Matched Seed Activations:** `{len(matched_seed_nodes)} nodes` (PageRank damping $\\alpha = {alpha_damping}$)\n",
            "## 1. Top Activated Obsidian Vault Notes (Personalized PageRank)",
            "| Rank | Obsidian Note | Category | OS | Activation | Key Connected Concepts | Summary & When to Apply |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for idx, an in enumerate(activated_notes[:top_k], 1):
            conc_str = ", ".join(f"`{c}`" for c in an["shared_concepts"][:4])
            wta_s = f" *(Apply when: {an['when_to_apply'][:70]})*" if an.get("when_to_apply") else ""
            md_lines.append(
                f"| **#{idx}** | `[[{an['wiki_link']}]]` | `{an['category']}` | `{an.get('os_platform', 'cross-platform')}` | **`{an['activation_score']:.4f}`** | {conc_str} | {an['summary'][:95]}{wta_s} |"
            )

        if bridge_concepts:
            md_lines.append("\n## 2. Discovered Cross-Note Bridge Concepts (Lateral Conceptual Connectors)")
            md_lines.append("| Bridge Concept | Type | Activation | Notes Linked | Connected Vault Notes |")
            md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for bc in bridge_concepts[:top_k]:
                linked_str = ", ".join(f"`[[{n}]]`" for n in bc["bridged_notes"][:4])
                md_lines.append(
                    f"| **`{bc['concept']}`** | `{bc['type']}` | `{bc['activation_score']:.4f}` | `{bc['bridged_notes_count']}` | {linked_str} |"
                )

        if conceptual_leap_paths:
            md_lines.append("\n## 3. Multi-Hop Conceptual Leap Pathways Across Categories")
            for idx, lp in enumerate(conceptual_leap_paths, 1):
                md_lines.append(f"{idx}. *({lp['hops']}-hop bridge)*: {lp['path_chain']}")

        markdown_report = "\n".join(md_lines)

        vault_ref = ""
        if save_to_vault:
            save_json_data(
                "associative_graphs",
                f"assoc_{slugify(query[:40])}",
                {
                    "query": query,
                    "num_graph_nodes": G.number_of_nodes(),
                    "num_graph_edges": G.number_of_edges(),
                    "activated_notes": activated_notes[:top_k],
                    "bridge_concepts": bridge_concepts[:top_k],
                    "conceptual_leap_paths": conceptual_leap_paths,
                },
            )
            title_slug = f"associative_{slugify(query[:40])}"
            top_note_link = activated_notes[0]["wiki_link"] if activated_notes else "none"
            vault_ref = save_reasoning_to_vault(
                title=title_slug,
                summary=f"Associative Spreading Activation for '{query[:50]}' (Top: [[{top_note_link}]])",
                markdown_body=markdown_report,
                engine_type="associative",
                tags=["associative", "pagerank", "bipartite", "vault"],
            )

        result_payload = {
            "engine": "associative_vault_pagerank",
            "query": query,
            "num_graph_nodes": G.number_of_nodes(),
            "num_graph_edges": G.number_of_edges(),
            "activated_notes": activated_notes[:top_k],
            "bridge_concepts": bridge_concepts[:top_k],
            "conceptual_leap_paths": conceptual_leap_paths,
            "vault_note": vault_ref,
            "markdown_report": markdown_report,
        }
        if not save_to_vault:
            if len(_PPR_QUERY_CACHE) >= 64:
                _PPR_QUERY_CACHE.clear()
            _PPR_QUERY_CACHE[cache_key] = copy.deepcopy(result_payload)
        return result_payload
    except Exception as exc:
        return {
            "engine": "associative_vault_pagerank",
            "error": str(exc),
            "activated_notes": [],
            "bridge_concepts": [],
            "conceptual_leap_paths": [],
            "markdown_report": f"Associative Engine Error: {exc}",
        }
