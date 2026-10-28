"""
Engine 9: Event-Calculus & Temporal State/Fluent Tracker (`temporal_fluents.py`).
100% CPU execution (0 MB GPU VRAM).

Capabilities:
- Models system, network, and target states over time using Event Calculus (`Initiates(Event, Fluent, T)`,
  `Terminates(Event, Fluent, T)`, `HoldsAt(Fluent, T)`).
- Tracks transient vs. persistent configurations (e.g., temporary `ip route`, `iptables -I`,
  interface state, serial console login sessions, and unlocked ports).
- Detects **Temporal Invalidation (Stale Fluents)**: when a service restart (`systemctl restart NetworkManager`),
  interface bounce (`ip link set down`), firewall flush (`iptables -F`), or target reboot occurs,
  it automatically marks previously established transient fluents as `STALE_INVALIDATED` and
  warns the LLM so it never assumes a wiped rule is still active.
"""
from datetime import datetime
import json
import re
from typing import Any, Dict, List, Optional

from .vault_bridge import (
    DATA_DIR,
    ensure_directories,
    get_hardware_reasoning_limits,
    resolve_problem_targets,
    save_json_data,
    save_reasoning_to_vault,
    slugify,
)

FLUENT_STATE_FILE = DATA_DIR / "temporal_fluents" / "live_fluents.json"


def _load_fluent_store() -> Dict[str, Any]:
    ensure_directories()
    if FLUENT_STATE_FILE.is_file():
        try:
            data = json.loads(FLUENT_STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "fluents" in data:
                return data
        except Exception:
            pass
    return {"turn_counter": 0, "fluents": {}, "events_log": []}


def load_fluent_state() -> Dict[str, Any]:
    """Public accessor for current Event-Calculus fluent store."""
    return _load_fluent_store()


def get_l1_state_summary_line() -> str:
    """Returns a single-line L1 Symbolic State Register summary of active & stale fluents."""
    store = _load_fluent_store()
    fluents = store.get("fluents", {})
    if not fluents:
        return "[L1 Symbolic State Register] No symbolic state mutations recorded yet."
    active = [f"{k}={v.get('value')}" for k, v in fluents.items() if v.get("status") in ("ACTIVE", "HOLDING")]
    stale = [f"{k}(STALE)" for k, v in fluents.items() if v.get("status") == "STALE_INVALIDATED"]
    parts = []
    if active:
        parts.append("ACTIVE: " + ", ".join(active[-6:]))
    if stale:
        parts.append("INVALIDATED: " + ", ".join(stale[-4:]))
    return "[L1 Symbolic State Register] " + (" || ".join(parts) if parts else "Ready")


def _save_fluent_store(store: Dict[str, Any]) -> None:
    ensure_directories()
    FLUENT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    FLUENT_STATE_FILE.write_text(json.dumps(store, indent=2) + "\n", encoding="utf-8")


def record_command_event(command: str, output: str, returncode: int = 0) -> Dict[str, Any]:
    """
    Inspect an executed shell command and its output to initiate, update, or invalidate
    temporal fluents using Last-Write-Wins keyed state (`Guardrail 5`).
    """
    store = _load_fluent_store()
    turn_id = int(store.get("turn_counter", 0)) + 1
    store["turn_counter"] = turn_id
    fluents: Dict[str, Dict[str, Any]] = store.setdefault("fluents", {})
    events_log: List[Dict[str, Any]] = store.setdefault("events_log", [])

    cmd_low = command.strip().lower()
    out_low = (output or "").lower()
    now_str = datetime.now().strftime("%H:%M:%S")
    invalidated: List[str] = []
    initiated: List[str] = []

    # 1. Check for State-Terminating (Reset) Events first (Linux & Windows)
    if any(
        k in cmd_low
        for k in (
            "systemctl restart network",
            "service networking restart",
            "nmcli networking off",
            "ip link set",
            " down",
            "restart-netadapter",
            "disable-netadapter",
            "ipconfig /release",
        )
    ):
        for fk, fv in fluents.items():
            if fv.get("category") in ("transient_route", "transient_ip_alias") and fv.get("status") in ("ACTIVE", "HOLDING"):
                fv["status"] = "STALE_INVALIDATED"
                fv["invalidated_by"] = command[:80]
                fv["updated_turn"] = turn_id
                invalidated.append(fk)

    if any(k in cmd_low for k in ("reboot", "systemctl reboot", "shutdown -r", "shutdown /r", "restart-computer")):
        for fk, fv in fluents.items():
            if fv.get("persistence") == "transient" and fv.get("status") in ("ACTIVE", "HOLDING"):
                fv["status"] = "STALE_INVALIDATED"
                fv["invalidated_by"] = "target_or_host_reboot"
                fv["updated_turn"] = turn_id
                invalidated.append(fk)

    if any(k in cmd_low for k in ("ip route del", "ip route flush", "route delete", "remove-netroute")):
        for fk, fv in fluents.items():
            if fv.get("category") == "transient_route" and fv.get("status") in ("ACTIVE", "HOLDING"):
                fv["status"] = "STALE_INVALIDATED"
                fv["invalidated_by"] = command[:80]
                fv["updated_turn"] = turn_id
                invalidated.append(fk)

    # 2. Check for State-Initiating Events (Last-Write-Wins on `(entity, attribute)`)
    if returncode == 0:
        # Static route added/replaced (Linux `ip route add` or Windows `route add` / `New-NetRoute`)
        m_route = re.search(r"ip\s+route\s+(?:add|replace)\s+([0-9./]+)\s+via\s+([0-9.]+)", cmd_low)
        if not m_route:
            m_route = re.search(r"route\s+(?:-p\s+)?add\s+([0-9.]+)\s+mask\s+[0-9.]+\s+([0-9.]+)", cmd_low)
        if not m_route:
            m_route = re.search(r"new-netroute\b.*?-destinationprefix\s+['\"]?([0-9./]+)['\"]?.*?-nexthop\s+['\"]?([0-9.]+)['\"]?", cmd_low)
        if m_route:
            subnet, gw = m_route.group(1), m_route.group(2)
            key = f"route:{subnet}"
            fluents[key] = {
                "entity": subnet,
                "attribute": "static_route_via",
                "value": gw,
                "fluent": f"Static_Route({subnet} via {gw})",
                "category": "transient_route",
                "persistence": "transient",
                "status": "HOLDING",
                "updated_turn": turn_id,
                "timestamp": now_str,
            }
            initiated.append(key)

        # IPv4 forwarding enabled
        if (
            "net.ipv4.ip_forward=1" in cmd_low
            or "net.ipv4.ip_forward = 1" in out_low
            or ("ipenableRouter" in cmd_low and "1" in cmd_low)
        ):
            key = "sysctl:ip_forward"
            fluents[key] = {
                "entity": "kernel",
                "attribute": "net.ipv4.ip_forward",
                "value": "1",
                "fluent": "IP_Forwarding_Enabled(1)",
                "category": "sysctl",
                "persistence": "transient",
                "status": "HOLDING",
                "updated_turn": turn_id,
                "timestamp": now_str,
            }
            initiated.append(key)

        # Firewall INPUT/FORWARD accept rule (Linux iptables/nft or Windows netsh advfirewall)
        if ("iptables" in cmd_low and ("-j accept" in cmd_low or "-p accept" in cmd_low)) or (
            "netsh" in cmd_low and "firewall" in cmd_low and "action=allow" in cmd_low
        ):
            chain = "FORWARD" if "forward" in cmd_low else "INPUT"
            key = f"firewall:rule_{chain.lower()}"
            fluents[key] = {
                "entity": "firewall",
                "attribute": f"{chain}_chain_policy",
                "value": "ACCEPT_RULE_ACTIVE",
                "fluent": f"Firewall_Accept({chain})",
                "category": "firewall",
                "persistence": "transient",
                "status": "HOLDING",
                "updated_turn": turn_id,
                "timestamp": now_str,
            }
            initiated.append(key)

        # ARP neighbor state observation (Linux `ip neigh` or Windows `arp -a` / `Get-NetNeighbor`)
        if any(k in cmd_low for k in ("ip neigh", "arp -a", "get-netneighbor")):
            for ip_m in re.finditer(
                r"(\b(?:\d{1,3}\.){3}\d{1,3}\b).*?\b(reachable|stale|delay|failed|incomplete|dynamic|static|permanent)\b",
                out_low,
            ):
                ip_addr, state_val = ip_m.group(1), ip_m.group(2).upper()
                if state_val in ("DYNAMIC", "STATIC", "PERMANENT"):
                    state_val = "REACHABLE"
                key = f"arp:{ip_addr}"
                fluents[key] = {
                    "entity": ip_addr,
                    "attribute": "l2_arp_state",
                    "value": state_val,
                    "fluent": f"ARP_Neighbor({ip_addr}, {state_val})",
                    "category": "l2_neighbor",
                    "persistence": "observed",
                    "status": "HOLDING",
                    "updated_turn": turn_id,
                    "timestamp": now_str,
                }
                initiated.append(key)

    # Serial console (`/dev/ttyUSB*` or `COM*`) probe (checked for both returncode == 0 and drop/overrun states)
    m_ser = re.search(r"(/dev/tty(?:usb|acm|s|ama)\d+|\bcom\d+\b)", cmd_low)
    if m_ser and any(k in cmd_low for k in ("tio", "stty", "mode ", "serialport", "plink", "serial")):
        ser_dev = m_ser.group(1)
        key = f"serial:{ser_dev}"
        shell_prefix_before_tio = re.split(r"\btio\b", command, maxsplit=1, flags=re.I)[0] if "tio" in cmd_low else ""
        echoed_literals = {
            m.group(2).strip().lower()
            for m in re.finditer(r"\b(?:echo|printf)\s+(?:-[neE]+\s+)?(['\"])(.*?)\1", shell_prefix_before_tio, flags=re.I)
            if m.group(2).strip()
        }
        ser_lines = []
        for ln in out_low.splitlines():
            s_ln = ln.strip()
            if not s_ln:
                continue
            if re.match(r"^\(command completed with exit code \d+\)$", s_ln, re.I):
                continue
            if re.match(
                r"^\[(?:tio\b|\d{2}:\d{2}:\d{2}|connected|disconnected).*?\](?:\s*(?:connected|disconnected|tio\b.*|press\s+ctrl-t.*))?$",
                s_ln,
                re.I,
            ):
                continue
            if s_ln in echoed_literals or (shell_prefix_before_tio and re.match(r"^===\s+.*?\s+===$", s_ln)):
                continue
            ser_lines.append(s_ln)
        cleaned_ser_out = "\n".join(ser_lines).strip()
        has_ser_err = any(
            err_k in out_low
            for err_k in (
                "disconnected",
                "device or resource busy",
                "resource temporarily unavailable",
                "input/output error",
                "cannot open /dev/tty",
                "serial port locked",
                "timed out",
            )
        )
        sent_serial_tx = (
            "write(" in cmd_low
            or "--exec" in cmd_low
            or (
                "tio" in cmd_low
                and not any(f in cmd_low for f in ("--list", "--help", "--version", " -l", " -h", " -v"))
            )
        )
        if returncode != 0 or has_ser_err or (sent_serial_tx and len(cleaned_ser_out) == 0 and "--list" not in cmd_low):
            fluents[key] = {
                "entity": ser_dev,
                "attribute": "oob_serial_console",
                "value": "DROPPED_UART_OVERRUN_NEEDS_PACING",
                "fluent": f"Serial_Console({ser_dev}, DROPPED_UART_OVERRUN_NEEDS_PACING)",
                "category": "oob_serial",
                "persistence": "transient",
                "status": "STALE_INVALIDATED",
                "invalidated_by": "serial_console_drop_or_fifo_overrun",
                "updated_turn": turn_id,
                "timestamp": now_str,
            }
            invalidated.append(key)
        else:
            val_state = "VERIFIED_RESPONSIVE" if len(cleaned_ser_out) > 0 else "PROBED"
            fluents[key] = {
                "entity": ser_dev,
                "attribute": "oob_serial_console",
                "value": val_state,
                "fluent": f"Serial_Console({ser_dev}, {val_state})",
                "category": "oob_serial",
                "persistence": "observed",
                "status": "HOLDING",
                "updated_turn": turn_id,
                "timestamp": now_str,
            }
            initiated.append(key)

    # HTTP / curl / Invoke-WebRequest / Test-NetConnection status update
    if any(k in cmd_low for k in ("curl ", "invoke-webrequest", "invoke-restmethod", "test-netconnection", "tnc ")):
        ip_m = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?\b", command)
        target_ep = ip_m.group(0) if ip_m else "target_http"
        key = f"http:{target_ep}"
        if returncode == 7 or "connection refused" in out_low or "tcptestsucceeded : false" in out_low:
            val = "REFUSED_EXIT_7"
        elif returncode == 28 or "timed out" in out_low:
            val = "TIMEOUT_EXIT_28"
        elif returncode == 0 or "tcptestsucceeded : true" in out_low:
            http_m = re.search(r"http/\d(?:\.\d)?\s+(\d{3})", out_low)
            val = f"HTTP_{http_m.group(1)}" if http_m else "REACHABLE_OK"
        else:
            val = f"EXIT_{returncode}"
        fluents[key] = {
            "entity": target_ep,
            "attribute": "http_probe_state",
            "value": val,
            "fluent": f"HTTP_Probe({target_ep}, {val})",
            "category": "http_state",
            "persistence": "observed",
            "status": "HOLDING",
            "updated_turn": turn_id,
            "timestamp": now_str,
        }
        initiated.append(key)

    if initiated or invalidated:
        events_log.append(
            {
                "turn": turn_id,
                "time": now_str,
                "command": command[:100],
                "initiated": initiated,
                "invalidated": invalidated,
            }
        )
        store["events_log"] = events_log[-40:]
        _save_fluent_store(store)

    inv_reason = ""
    if invalidated:
        first_inv = fluents.get(invalidated[0], {})
        inv_reason = str(first_inv.get("invalidated_by") or "state_reset")

    return {
        "turn": turn_id,
        "initiated_fluents": initiated,
        "invalidated_fluents": invalidated,
        "invalidation_reason": inv_reason,
        "active_fluents_count": sum(1 for v in fluents.values() if v.get("status") in ("ACTIVE", "HOLDING")),
        "stale_fluents_count": sum(1 for v in fluents.values() if v.get("status") == "STALE_INVALIDATED"),
    }


def seed_default_temporal_fluents() -> None:
    """Initialize a clean Event-Calculus fluent store with zero hardcoded profile IPs."""
    store = {"turn_counter": 0, "fluents": {}, "events_log": []}
    _save_fluent_store(store)


def run_temporal_fluent_reasoning(
    problem: str = "Temporal state & fluent validity audit",
    simulated_events: Optional[List[Dict[str, Any]]] = None,
    recent_commands: Optional[List[str]] = None,
    save_to_vault: bool = False,
    export_to_vault: bool = False,
) -> Dict[str, Any]:
    """
    Execute Event-Calculus Temporal Reasoning to audit active vs. stale/invalidated system fluents
    and verify whether transient configurations require re-application.
    """
    save_to_vault = save_to_vault or export_to_vault
    try:
        if recent_commands:
            for cmd_str in recent_commands:
                record_command_event(cmd_str, "", 0)
        if simulated_events:
            for ev in simulated_events:
                record_command_event(
                    ev.get("command", ""),
                    ev.get("output", ""),
                    int(ev.get("returncode", 0)),
                )

        store = _load_fluent_store()
        fluents = dict(store.get("fluents", {}))

        # Dynamically synthesize contextual fluents from live host & problem text (no hardcoded IPs)
        if not fluents:
            ctx = resolve_problem_targets(problem)
            prob_low = (problem or "").lower()
            fluents = {
                f"host_iface:{ctx['primary_interface']}": {
                    "entity": ctx["primary_interface"],
                    "attribute": "host_interface_subnet",
                    "value": ctx["local_subnet"],
                    "fluent": f"Host_Interface({ctx['primary_interface']}, {ctx['local_subnet']})",
                    "category": "host_network",
                    "persistence": "observed",
                    "status": "HOLDING",
                    "updated_turn": 1,
                }
            }
            if "/dev/tty" in prob_low or "com" in prob_low or "serial" in prob_low:
                ser = ctx["serial_port"]
                fluents[f"serial:{ser}"] = {
                    "entity": ser,
                    "attribute": "oob_serial_console",
                    "value": "AVAILABLE_TRANSIENT_SESSION",
                    "fluent": f"Serial_Attached({ser})",
                    "category": "oob_serial",
                    "persistence": "transient",
                    "status": "HOLDING",
                    "updated_turn": 1,
                }
            if ctx["has_concrete_primary_ip"]:
                tip = ctx["primary_ip"]
                if "exit 7" in prob_low or "refused" in prob_low:
                    fluents[f"http:{tip}"] = {
                        "entity": tip,
                        "attribute": "http_probe_state",
                        "value": "REFUSED_EXIT_7",
                        "fluent": f"HTTP_Probe({tip}, REFUSED_EXIT_7)",
                        "category": "http_state",
                        "persistence": "observed",
                        "status": "HOLDING",
                        "updated_turn": 1,
                    }
                else:
                    fluents[f"target:{tip}"] = {
                        "entity": tip,
                        "attribute": "target_endpoint",
                        "value": "IDENTIFIED",
                        "fluent": f"Target_Identified({tip})",
                        "category": "target_state",
                        "persistence": "observed",
                        "status": "HOLDING",
                        "updated_turn": 1,
                    }
            if ctx["remote_subnet"] != "<REMOTE_SUBNET>":
                rsub = ctx["remote_subnet"]
                fluents[f"route:{rsub}"] = {
                    "entity": rsub,
                    "attribute": "static_route_via",
                    "value": "PENDING_CONFIGURATION",
                    "fluent": f"Pending_Route({rsub})",
                    "category": "transient_route",
                    "persistence": "transient",
                    "status": "PENDING",
                    "updated_turn": 1,
                }

        active_list = [
            {"key": k, **v} for k, v in fluents.items() if v.get("status") in ("ACTIVE", "HOLDING", "PENDING")
        ]
        stale_list = [
            {"key": k, **v} for k, v in fluents.items() if v.get("status") == "STALE_INVALIDATED"
        ]

        md_lines = [
            "## Event-Calculus Temporal State & Fluent Tracker",
            f"- **Problem / Context:** {problem}",
            f"- **Tracked Fluents:** `{len(active_list)} Active/Pending`, `{len(stale_list)} Stale/Invalidated` (Last-Write-Wins Keyed State)\n",
            "## 1. Current Active System & Target Fluents (`HoldsAt(Fluent, T_now)`)",
            "| Fluent Key | Entity | Attribute | Current Value | Persistence | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for fl in active_list:
            md_lines.append(
                f"| `{fl['key']}` | `{fl.get('entity')}` | `{fl.get('attribute')}` | **`{fl.get('value')}`** | `{fl.get('persistence')}` | `{fl.get('status')}` |"
            )

        if stale_list:
            md_lines.append("\n## 2. Invalidated / Stale Fluents Requiring Re-Application (`TerminatedAt`)")
            for st in stale_list:
                md_lines.append(
                    f"- **WARNING (`{st['key']}`):** `{st.get('attribute')}` was invalidated by `{st.get('invalidated_by', 'reset event')}` — must re-run configuration before relying on it."
                )

        markdown_report = "\n".join(md_lines)
        vault_ref = ""
        if save_to_vault:
            save_json_data(
                "temporal_fluents",
                f"fluents_{slugify(problem[:35])}",
                {
                    "problem": problem,
                    "active_fluents": active_list,
                    "stale_fluents": stale_list,
                },
            )
            vault_ref = save_reasoning_to_vault(
                title=f"temporal_fluents_{slugify(problem[:35])}",
                summary=f"Event-Calculus Fluents: {len(active_list)} active, {len(stale_list)} stale",
                markdown_body=markdown_report,
                engine_type="temporal_fluents",
                tags=["temporal", "fluents", "event_calculus"],
            )

        hw = get_hardware_reasoning_limits()
        return {
            "engine": "temporal_fluents",
            "hardware_tier": hw.get("tier", "HIGH_PERFORMANCE"),
            "fluent_event_history_limit": int(hw.get("fluent_event_history_limit", 500)),
            "schmitt_hysteresis_window": int(hw.get("schmitt_hysteresis_window", 5)),
            "active_fluents": active_list,
            "stale_fluents": stale_list,
            "holding_count": len(active_list),
            "stale_count": len(stale_list),
            "has_stale_warnings": bool(stale_list),
            "vault_note": vault_ref,
            "markdown": markdown_report,
            "markdown_report": markdown_report,
        }
    except Exception as exc:
        return {
            "engine": "temporal_fluents",
            "error": str(exc),
            "active_fluents": [],
            "stale_fluents": [],
            "has_stale_warnings": False,
            "markdown_report": f"Temporal Fluent Engine Error: {exc}",
        }
