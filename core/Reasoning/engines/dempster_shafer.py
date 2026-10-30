"""
Engine 10: Dempster-Shafer Theory of Evidence & Conflict/Ignorance Engine (`dempster_shafer.py`).
100% CPU execution (0 MB GPU VRAM).

Capabilities:
- Computes Basic Probability Assignments (BPA / mass functions `m(A)`), exact `[Belief(H), Plausibility(H)]`
  uncertainty intervals, and explicitly tracks **Epistemic Ignorance (`m(Theta)`)**.
- Applies Murphy's Damped Dempster Rule of Combination so even strongly conflicting sensor readings
  never cause divide-by-zero instability.
- Quantifies **Inter-Sensor Conflict Mass (`K`)**: detects when two network/system probes contradict
  one another (e.g., `curl exit 7` or `ping 100% loss` vs. `ARP REACHABLE` or `serial socket active`),
  and deduces the exact architectural reconciliation (such as L3/L4 host firewall filtering or loopback-only binding).
"""
import re
from typing import Any, Dict, List, Optional, Tuple

from .vault_bridge import ensure_directories, get_hardware_reasoning_limits, save_json_data, save_reasoning_to_vault, slugify

FRAME_HYPOTHESES = (
    "l2_l3_network_unreachable",
    "host_firewall_or_acl_filtering",
    "service_loopback_or_nonstandard_port",
)

SENSOR_MASS_PROFILES: Dict[str, Dict[str, float]] = {
    "curl_exit_7_Immediate_refused": {
        "l2_l3_network_unreachable": 0.25,
        "host_firewall_or_acl_filtering": 0.30,
        "service_loopback_or_nonstandard_port": 0.35,
        "OMEGA_IGNORANCE": 0.10,
    },
    "curl_exit_28_timeout": {
        "l2_l3_network_unreachable": 0.45,
        "host_firewall_or_acl_filtering": 0.40,
        "service_loopback_or_nonstandard_port": 0.05,
        "OMEGA_IGNORANCE": 0.10,
    },
    "curl_exit_28_Timeout": {
        "l2_l3_network_unreachable": 0.45,
        "host_firewall_or_acl_filtering": 0.40,
        "service_loopback_or_nonstandard_port": 0.05,
        "OMEGA_IGNORANCE": 0.10,
    },
    "arp_resolved_mac_present": {
        "l2_l3_network_unreachable": 0.02,
        "host_firewall_or_acl_filtering": 0.42,
        "service_loopback_or_nonstandard_port": 0.46,
        "OMEGA_IGNORANCE": 0.10,
    },
    "arp_mac_resolved": {
        "l2_l3_network_unreachable": 0.02,
        "host_firewall_or_acl_filtering": 0.42,
        "service_loopback_or_nonstandard_port": 0.46,
        "OMEGA_IGNORANCE": 0.10,
    },
    "arp_incomplete_or_missing": {
        "l2_l3_network_unreachable": 0.72,
        "host_firewall_or_acl_filtering": 0.12,
        "service_loopback_or_nonstandard_port": 0.04,
        "OMEGA_IGNORANCE": 0.12,
    },
    "icmp_ping_fails": {
        "l2_l3_network_unreachable": 0.55,
        "host_firewall_or_acl_filtering": 0.35,
        "service_loopback_or_nonstandard_port": 0.02,
        "OMEGA_IGNORANCE": 0.08,
    },
    "ping_100pct_packet_loss": {
        "l2_l3_network_unreachable": 0.55,
        "host_firewall_or_acl_filtering": 0.35,
        "service_loopback_or_nonstandard_port": 0.02,
        "OMEGA_IGNORANCE": 0.08,
    },
    "icmp_ping_responds": {
        "l2_l3_network_unreachable": 0.01,
        "host_firewall_or_acl_filtering": 0.34,
        "service_loopback_or_nonstandard_port": 0.55,
        "OMEGA_IGNORANCE": 0.10,
    },
    "http_401_or_403_or_tls_alert": {
        "l2_l3_network_unreachable": 0.01,
        "host_firewall_or_acl_filtering": 0.14,
        "service_loopback_or_nonstandard_port": 0.77,
        "OMEGA_IGNORANCE": 0.08,
    },
    "alt_port_open_in_scan": {
        "l2_l3_network_unreachable": 0.01,
        "host_firewall_or_acl_filtering": 0.19,
        "service_loopback_or_nonstandard_port": 0.72,
        "OMEGA_IGNORANCE": 0.08,
    },
    "target_outside_local_24_cidr": {
        "l2_l3_network_unreachable": 0.52,
        "host_firewall_or_acl_filtering": 0.22,
        "service_loopback_or_nonstandard_port": 0.11,
        "OMEGA_IGNORANCE": 0.15,
    },
    "serial_ss_shows_127_0_0_1_only": {
        "l2_l3_network_unreachable": 0.01,
        "host_firewall_or_acl_filtering": 0.07,
        "service_loopback_or_nonstandard_port": 0.87,
        "OMEGA_IGNORANCE": 0.05,
    },
    "serial_console_oob_available": {
        "l2_l3_network_unreachable": 0.05,
        "host_firewall_or_acl_filtering": 0.30,
        "service_loopback_or_nonstandard_port": 0.55,
        "OMEGA_IGNORANCE": 0.10,
    },
    "post_exploitation_shell_active": {
        "l2_l3_network_unreachable": 0.02,
        "host_firewall_or_acl_filtering": 0.18,
        "service_loopback_or_nonstandard_port": 0.70,
        "OMEGA_IGNORANCE": 0.10,
    },
}


def _dempster_combine_two(
    m1: Dict[str, float],
    m2: Dict[str, float],
) -> Tuple[Dict[str, float], float]:
    """
    Combine two mass functions `m1` and `m2` over singleton hypotheses + `OMEGA_IGNORANCE`
    and return `(combined_mass, pairwise_conflict_K)`.
    """
    hyps = list(FRAME_HYPOTHESES)
    conflict_k = 0.0
    raw: Dict[str, float] = {h: 0.0 for h in hyps}
    raw["OMEGA_IGNORANCE"] = 0.0

    for k1, v1 in m1.items():
        for k2, v2 in m2.items():
            prod = v1 * v2
            if k1 == "OMEGA_IGNORANCE" and k2 == "OMEGA_IGNORANCE":
                raw["OMEGA_IGNORANCE"] += prod
            elif k1 == "OMEGA_IGNORANCE":
                raw[k2] = raw.get(k2, 0.0) + prod
            elif k2 == "OMEGA_IGNORANCE":
                raw[k1] = raw.get(k1, 0.0) + prod
            elif k1 == k2:
                raw[k1] = raw.get(k1, 0.0) + prod
            else:
                conflict_k += prod

    # Damped normalization (Murphy's safeguard against K -> 1.0)
    if conflict_k >= 0.995:
        avg = {k: 0.5 * (m1.get(k, 0.0) + m2.get(k, 0.0)) for k in raw}
        return avg, round(conflict_k, 4)

    norm = 1.0 - conflict_k
    combined = {k: val / norm for k, val in raw.items()}
    return combined, round(conflict_k, 4)


def run_dempster_shafer_reasoning(
    problem: str,
    observed_evidence: Optional[Dict[str, bool]] = None,
    sensor_text: str = "",
    save_to_vault: bool = False,
    export_to_vault: bool = False,
) -> Dict[str, Any]:
    """
    Execute Dempster-Shafer Evidence Combination to compute `[Belief, Plausibility]` intervals,
    remaining Epistemic Ignorance `m(Theta)`, and Sensor Conflict Mass `K`.
    """
    save_to_vault = save_to_vault or export_to_vault
    try:
        ensure_directories()
        ev = dict(observed_evidence or {})
        p_low = f"{problem} {sensor_text}".lower()
        if "exit 7" in p_low or "refused" in p_low:
            ev.setdefault("curl_exit_7_Immediate_refused", True)
        if "exit 28" in p_low or "timed out" in p_low:
            ev.setdefault("curl_exit_28_timeout", True)
        if "100% packet loss" in p_low or "network is unreachable" in p_low:
            ev.setdefault("icmp_ping_fails", True)
        if ("arp" in p_low or bool(re.search(r"\breachable\b", p_low)) or "lladdr" in p_low) and "network is unreachable" not in p_low:
            ev.setdefault("arp_resolved_mac_present", True)
        if any(k in p_low for k in ("401", "403", "mtls", "client.crt", "https://", "http/1.1 200", "http/2 200")):
            ev.setdefault("http_401_or_403_or_tls_alert", True)
        if re.search(r"\b(?:ttyusb\d*|ttyacm\d*|serial|tio|uart|oob|console)\b", p_low):
            ev.setdefault("serial_console_oob_available", True)
        if any(k in p_low for k in ("privesc", "privilege escalation", "suid", "sudoers", "capabilities", "www-data", "active directory", "ldap", "smb")):
            ev.setdefault("post_exploitation_shell_active", True)

        # Deduplicate equivalent canonical keys so aliases are not double-counted
        canonical_map = {
            "curl_exit_28_Timeout": "curl_exit_28_timeout",
            "arp_mac_resolved": "arp_resolved_mac_present",
            "arp_resolved_ok": "arp_resolved_mac_present",
            "ping_icmp_ok": "icmp_ping_responds",
            "ping_100pct_packet_loss": "icmp_ping_fails",
            "arp_incomplete": "arp_incomplete_or_missing",
            "nonstandard_port_open": "alt_port_open_in_scan",
            "open_tcp_port": "alt_port_open_in_scan",
            "http_401_or_403_auth": "http_401_or_403_or_tls_alert",
            "tls_cert_or_sni_mismatch": "http_401_or_403_or_tls_alert",
        }
        norm_ev: Dict[str, bool] = {}
        for k, v in ev.items():
            if v:
                norm_ev[canonical_map.get(k, k)] = True

        active_masses: List[Tuple[str, Dict[str, float]]] = []
        for ev_k, is_true in norm_ev.items():
            if is_true and ev_k in SENSOR_MASS_PROFILES:
                active_masses.append((ev_k, SENSOR_MASS_PROFILES[ev_k]))

        if not active_masses:
            # High-ignorance uninformative prior when no sensors have fired yet
            current_m = {h: 0.15 for h in FRAME_HYPOTHESES}
            current_m["OMEGA_IGNORANCE"] = 0.55
            max_conflict_k = 0.0
        else:
            current_m = dict(active_masses[0][1])
            max_conflict_k = 0.0
            for _, next_m in active_masses[1:]:
                current_m, k_step = _dempster_combine_two(current_m, next_m)
                max_conflict_k = max(max_conflict_k, k_step)

        omega = round(current_m.get("OMEGA_IGNORANCE", 0.0), 4)
        intervals = []
        for h in FRAME_HYPOTHESES:
            bel = round(current_m.get(h, 0.0), 4)
            plaus = round(min(1.0, bel + omega), 4)
            pignistic = round(bel + (omega / len(FRAME_HYPOTHESES)), 4)
            intervals.append(
                {
                    "hypothesis": h,
                    "belief": bel,
                    "plausibility": plaus,
                    "pignistic_prob": pignistic,
                    "interval_str": f"[{bel:.1%}, {plaus:.1%}]",
                }
            )
        intervals.sort(key=lambda x: -x["pignistic_prob"])

        if max_conflict_k >= 0.45:
            conflict_verdict = (
                f"HIGH SENSOR CONFLICT (K={max_conflict_k:.2f}): L2/L3 reachability contradicts L4/L7 refusal — "
                "target is alive on L2, but service is either bound to 127.0.0.1 or filtered by host firewall."
            )
        elif omega >= 0.35:
            conflict_verdict = (
                f"HIGH EPISTEMIC IGNORANCE (m(Theta)={omega:.1%}): Insufficient sensor probes collected — "
                "run the highest-EIG probe before committing to remediation."
            )
        else:
            conflict_verdict = f"CONSISTENT EVIDENCE (K={max_conflict_k:.2f}, Ignorance={omega:.1%}): Sensor readings converge cleanly."

        md_lines = [
            "## Dempster-Shafer Evidence Theory (`[Belief, Plausibility]` & Conflict $K$)",
            f"- **Problem:** {problem}",
            f"- **Epistemic Ignorance Mass $m(\\Theta)$:** **`{omega:.1%}`**",
            f"- **Inter-Sensor Conflict Mass $K$:** **`{max_conflict_k:.3f}`** $\\rightarrow$ {conflict_verdict}\n",
            "## 1. Belief & Plausibility Intervals",
            "| Hypothesis Frame | Belief $\\text{Bel}(H)$ | Plausibility $\\text{Pl}(H)$ | Uncertainty Interval | BetP (Pignistic) |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for item in intervals:
            md_lines.append(
                f"| `{item['hypothesis']}` | `{item['belief']:.1%}` | `{item['plausibility']:.1%}` | **`{item['interval_str']}`** | **{item['pignistic_prob']:.1%}** |"
            )

        markdown_report = "\n".join(md_lines)
        vault_ref = ""
        if save_to_vault:
            save_json_data(
                "dempster_shafer",
                f"ds_{slugify(problem[:35])}",
                {
                    "problem": problem,
                    "ignorance_omega": omega,
                    "conflict_mass_k": max_conflict_k,
                    "conflict_verdict": conflict_verdict,
                    "intervals": intervals,
                },
            )
            vault_ref = save_reasoning_to_vault(
                title=f"dempster_shafer_{slugify(problem[:35])}",
                summary=f"Dempster-Shafer: Top `{intervals[0]['hypothesis']}` {intervals[0]['interval_str']}, Conflict K={max_conflict_k:.2f}",
                markdown_body=markdown_report,
                engine_type="dempster_shafer",
                tags=["dempster_shafer", "belief", "conflict"],
            )

        hw = get_hardware_reasoning_limits()
        return {
            "engine": "dempster_shafer",
            "hardware_tier": hw.get("tier", "HIGH_PERFORMANCE"),
            "dst_focal_set_limit": int(hw.get("dst_focal_set_limit", 128)),
            "dst_monte_carlo_samples": int(hw.get("dst_monte_carlo_samples", 1000)),
            "ignorance_omega": omega,
            "epistemic_ignorance": omega,
            "conflict_mass_k": max_conflict_k,
            "conflict_verdict": conflict_verdict,
            "top_hypothesis": intervals[0]["hypothesis"],
            "top_interval": intervals[0]["interval_str"],
            "intervals": intervals,
            "vault_note": vault_ref,
            "markdown": markdown_report,
            "markdown_report": markdown_report,
        }
    except Exception as exc:
        return {
            "engine": "dempster_shafer",
            "error": str(exc),
            "ignorance_omega": 0.0,
            "conflict_mass_k": 0.0,
            "intervals": [],
            "markdown_report": f"Dempster-Shafer Engine Error: {exc}",
        }
