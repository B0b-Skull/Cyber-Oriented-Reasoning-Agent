"""
Engine 1: Bayesian Abductive Reasoning Engine (Inference to the Best Explanation).
100% CPU execution (0 MB GPU VRAM).

Capabilities:
- Computes exact posterior probabilities P(Hypothesis | Evidence) using Bayes' rule.
- Quantifies diagnostic uncertainty via Shannon Entropy (bits).
- Ranks unobserved diagnostic probes by Expected Information Gain (EIG / Mutual Information)
  so the LLM executes the single highest-yield verification command next.
- Persists and updates domain priors in `Reasoning/data/bayesian_priors.json` and logs
  reports to `ObsidianVault/reasoning/`.
"""
import json
import math
import re
from typing import Any, Dict, List, Optional, Tuple

from .vault_bridge import (
    DATA_DIR,
    ensure_directories,
    get_hardware_reasoning_limits,
    render_command_template,
    resolve_problem_targets,
    save_reasoning_to_vault,
    slugify,
)

PRIORS_FILE = DATA_DIR / "bayesian_priors.json"

DEFAULT_CYBER_PROFILES: Dict[str, Any] = {
    "http_api_unreachable": {
        "description": "Root-cause abduction when HTTP/API probes fail (e.g. curl exit 7 connection refused, exit 28 timeout, or no route).",
        "hypotheses": {
            "l3_missing_route_or_subnet_isolation": {
                "prior": 0.28,
                "alpha_count": 7.0,
                "description": "Missing Layer-3 route, wrong source interface, or unconfigured local IP in target subnet.",
                "remediation": "Check `ip -4 addr` and `ip route get <target_ip>`; add interface alias or static route.",
            },
            "service_on_nonstandard_port_or_tls": {
                "prior": 0.24,
                "alpha_count": 6.0,
                "description": "Target host is alive at L2/L3, but API listens on a non-standard port (e.g. 8443, 8000, 5000, 9000) or requires TLS.",
                "remediation": "Run fast port discovery (`nc -zv` or `nmap -F -sT`) against the target IP.",
            },
            "l2_arp_incomplete_or_vlan_mismatch": {
                "prior": 0.20,
                "alpha_count": 5.0,
                "description": "Physical link or VLAN mismatch prevents Layer-2 ARP resolution (`FAILED` or `INCOMPLETE` in `ip neigh`).",
                "remediation": "Inspect `ip neigh show`, `ip -d link`, and switch/serial console VLAN assignments.",
            },
            "host_firewall_or_acl_reject": {
                "prior": 0.16,
                "alpha_count": 4.0,
                "description": "Target firewall (iptables/nftables) actively sends TCP RST (curl exit 7) or drops packets from non-management IPs.",
                "remediation": "Inspect target firewall rules via out-of-band serial console (`/dev/ttyUSB0`) or probe from allowed management IP.",
            },
            "api_daemon_stopped_or_bound_loopback": {
                "prior": 0.12,
                "alpha_count": 3.0,
                "description": "API service on the target has crashed or is bound solely to `127.0.0.1` instead of `0.0.0.0`.",
                "remediation": "Access target via serial console (`/dev/ttyUSB0` with `tio`) and check `ss -tulpn` / `systemctl`.",
            },
        },
        "evidence_likelihoods": {
            "curl_exit_7_Immediate_refused": {
                "probe_cmd": "curl -sS -k -I --connect-timeout 3 http://<target>",
                "description": "curl returns exit code 7 immediately (<100ms TCP RST) or 'No route to host'",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.70,
                    "service_on_nonstandard_port_or_tls": 0.85,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.25,
                    "host_firewall_or_acl_reject": 0.75,
                    "api_daemon_stopped_or_bound_loopback": 0.90,
                },
            },
            "curl_exit_28_timeout": {
                "probe_cmd": "curl -sS -k -I --connect-timeout 5 http://<target>",
                "description": "curl times out (exit code 28) with no TCP RST",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.55,
                    "service_on_nonstandard_port_or_tls": 0.15,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.85,
                    "host_firewall_or_acl_reject": 0.80,
                    "api_daemon_stopped_or_bound_loopback": 0.05,
                },
            },
            "arp_resolved_mac_present": {
                "probe_cmd": "ip neigh show <target_ip>",
                "description": "Target IP resolves to a valid MAC address (`REACHABLE`/`STALE`) in `ip neigh`",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.05,
                    "service_on_nonstandard_port_or_tls": 0.92,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.02,
                    "host_firewall_or_acl_reject": 0.90,
                    "api_daemon_stopped_or_bound_loopback": 0.92,
                },
            },
            "icmp_ping_responds": {
                "probe_cmd": "ping -c 2 -W 1 <target_ip>",
                "description": "Target responds to ICMP echo requests (`ping` 0% packet loss)",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.02,
                    "service_on_nonstandard_port_or_tls": 0.90,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.01,
                    "host_firewall_or_acl_reject": 0.65,
                    "api_daemon_stopped_or_bound_loopback": 0.90,
                },
            },
            "alt_port_open_in_scan": {
                "probe_cmd": "nmap -Pn -p 22,80,443,5000,8000,8080,8443,9000 <target_ip>",
                "description": "An alternate TCP port (e.g. 443, 5000, 8000, 8080, 8443) is OPEN on target",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.01,
                    "service_on_nonstandard_port_or_tls": 0.96,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.01,
                    "host_firewall_or_acl_reject": 0.25,
                    "api_daemon_stopped_or_bound_loopback": 0.15,
                },
            },
            "serial_ss_shows_127_0_0_1_only": {
                "probe_cmd": "tio -b 115200 --mute --script-run once --script 'write(\"ss -tulpn\\r\"); while read(4096, 500) > 0 do end; exit(0)' /dev/ttyUSB0",
                "description": "Serial console `ss -tulpn` shows service listening on 127.0.0.1 or not running",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.05,
                    "service_on_nonstandard_port_or_tls": 0.10,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.05,
                    "host_firewall_or_acl_reject": 0.10,
                    "api_daemon_stopped_or_bound_loopback": 0.97,
                },
            },
            "icmp_ping_fails": {
                "probe_cmd": "ping -c 2 -W 1 <target_ip>",
                "description": "ICMP echo request times out (100% packet loss)",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.85,
                    "service_on_nonstandard_port_or_tls": 0.10,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.90,
                    "host_firewall_or_acl_reject": 0.70,
                    "api_daemon_stopped_or_bound_loopback": 0.10,
                },
            },
            "arp_incomplete_or_missing": {
                "probe_cmd": "ip neigh show <target_ip>",
                "description": "ARP table entry for target IP is INCOMPLETE, FAILED, or missing",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.80,
                    "service_on_nonstandard_port_or_tls": 0.05,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.95,
                    "host_firewall_or_acl_reject": 0.10,
                    "api_daemon_stopped_or_bound_loopback": 0.05,
                },
            },
            "http_401_or_403_or_tls_alert": {
                "probe_cmd": "curl -sS -k -I --connect-timeout 3 https://<target_ip>",
                "description": "Target responds with HTTP 401/403 or TLS/mTLS handshake alert",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.01,
                    "service_on_nonstandard_port_or_tls": 0.96,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.01,
                    "host_firewall_or_acl_reject": 0.15,
                    "api_daemon_stopped_or_bound_loopback": 0.05,
                },
            },
            "target_outside_local_24_cidr": {
                "probe_cmd": "ip route get <target_ip>",
                "description": "Target IP lies outside all directly attached local interface subnets",
                "p_given_h": {
                    "l3_missing_route_or_subnet_isolation": 0.88,
                    "service_on_nonstandard_port_or_tls": 0.25,
                    "l2_arp_incomplete_or_vlan_mismatch": 0.40,
                    "host_firewall_or_acl_reject": 0.30,
                    "api_daemon_stopped_or_bound_loopback": 0.20,
                },
            },
        },
    },
    "l2_l3_routing_blackhole": {
        "description": "Root-cause abduction when routing Layer-2/Layer-3 traffic across disjoint subnets fails.",
        "hypotheses": {
            "ip_forwarding_disabled_on_pivot": {
                "prior": 0.26,
                "alpha_count": 6.5,
                "description": "Pivot/gateway host has `net.ipv4.ip_forward = 0`, dropping transit packets between interfaces.",
                "remediation": "Enable `sysctl -w net.ipv4.ip_forward=1` (Linux) or `Set-NetIPInterface -Forwarding Enabled` (Windows) on the transit/pivot node.",
            },
            "asymmetric_missing_return_route_or_nat": {
                "prior": 0.28,
                "alpha_count": 7.0,
                "description": "Packets reach destination ({remote_ip}), but destination lacks a return route to source subnet and needs MASQUERADE/SNAT.",
                "remediation": "Add return static route on destination OR enable `iptables -t nat -A POSTROUTING -o {iface} -j MASQUERADE` on pivot.",
            },
            "firewall_forward_chain_drop": {
                "prior": 0.22,
                "alpha_count": 5.5,
                "description": "`iptables`/`nftables` FORWARD chain policy is DROP or rejects cross-interface traffic.",
                "remediation": "Run `iptables -I FORWARD -j ACCEPT` or allow transit subnets in `nftables` / `netsh advfirewall`.",
            },
            "local_missing_static_route_via_gateway": {
                "prior": 0.14,
                "alpha_count": 3.5,
                "description": "Local workstation routes destination subnet out default gateway instead of the lab pivot IP.",
                "remediation": "Run `sudo ip route replace {remote_subnet} via {gateway_ip} dev {iface}` (Linux) or `route add` / `New-NetRoute` (Windows).",
            },
            "l2_bridge_or_proxy_arp_required": {
                "prior": 0.10,
                "alpha_count": 2.5,
                "description": "Destination expects Layer-2 adjacency / ARP broadcast on same VLAN segment (`proxy_arp` or L2 bridge needed).",
                "remediation": "Enable `sysctl -w net.ipv4.conf.all.proxy_arp=1` or configure bridge / VLAN subinterface.",
            },
        },
        "evidence_likelihoods": {
            "ip_route_get_uses_default_wan": {
                "probe_cmd": "ip route get {remote_ip}",
                "description": "`ip route get` sends traffic to default WAN gateway instead of lab interface",
                "p_given_h": {
                    "ip_forwarding_disabled_on_pivot": 0.10,
                    "asymmetric_missing_return_route_or_nat": 0.10,
                    "firewall_forward_chain_drop": 0.10,
                    "local_missing_static_route_via_gateway": 0.96,
                    "l2_bridge_or_proxy_arp_required": 0.15,
                },
            },
            "sysctl_ip_forward_is_zero": {
                "probe_cmd": "sysctl net.ipv4.ip_forward",
                "description": "`net.ipv4.ip_forward` is 0 on the gateway/pivot device",
                "p_given_h": {
                    "ip_forwarding_disabled_on_pivot": 0.97,
                    "asymmetric_missing_return_route_or_nat": 0.15,
                    "firewall_forward_chain_drop": 0.15,
                    "local_missing_static_route_via_gateway": 0.05,
                    "l2_bridge_or_proxy_arp_required": 0.10,
                },
            },
            "tcpdump_sees_syn_out_no_synack_back": {
                "probe_cmd": "tcpdump -ni any host {remote_ip} -c 6",
                "description": "Egress interface transmits SYN to destination, destination receives it, but return packet never arrives",
                "p_given_h": {
                    "ip_forwarding_disabled_on_pivot": 0.05,
                    "asymmetric_missing_return_route_or_nat": 0.92,
                    "firewall_forward_chain_drop": 0.45,
                    "local_missing_static_route_via_gateway": 0.05,
                    "l2_bridge_or_proxy_arp_required": 0.30,
                },
            },
            "icmp_host_prohibited_or_filtered": {
                "probe_cmd": "ping -c 2 -W 1 {remote_ip}",
                "description": "Transit router returns ICMP Admin Prohibited / Packet Filtered or FORWARD drop counters increment",
                "p_given_h": {
                    "ip_forwarding_disabled_on_pivot": 0.10,
                    "asymmetric_missing_return_route_or_nat": 0.05,
                    "firewall_forward_chain_drop": 0.95,
                    "local_missing_static_route_via_gateway": 0.05,
                    "l2_bridge_or_proxy_arp_required": 0.05,
                },
            },
        },
    },
    "api_auth_rejection": {
        "description": "Root-cause abduction when an API endpoint responds with 401/403/405/400 during security testing.",
        "hypotheses": {
            "missing_bearer_or_api_key_header": {
                "prior": 0.32,
                "alpha_count": 8.0,
                "description": "Endpoint requires `Authorization: Bearer <token>`, `X-API-Key`, or custom header discovered in JS/firmware.",
                "remediation": "Inspect JS bundles, OpenAPI `/swagger.json`, or local config files via serial console for token headers.",
            },
            "wrong_http_method_or_json_content_type": {
                "prior": 0.24,
                "alpha_count": 6.0,
                "description": "Endpoint requires `POST`/`PUT` with `Content-Type: application/json` instead of `GET` or form-urlencoded.",
                "remediation": "Send `OPTIONS -i` and retry with `-X POST -H 'Content-Type: application/json' -d '{}' `.",
            },
            "reverse_proxy_ip_or_host_header_restriction": {
                "prior": 0.20,
                "alpha_count": 5.0,
                "description": "Nginx/Apache/Envoy restricts access by `Host`, `X-Forwarded-For: 127.0.0.1`, or `Origin`/`Referer`.",
                "remediation": "Test `-H 'X-Forwarded-For: 127.0.0.1' -H 'X-Real-IP: 127.0.0.1'` and expected `Host` header.",
            },
            "session_cookie_or_csrf_handshake_needed": {
                "prior": 0.14,
                "alpha_count": 3.5,
                "description": "Stateful session cookie + CSRF token from `/login` or `/api/auth` must precede API calls.",
                "remediation": "Use `curl -c cookies.txt -b cookies.txt` to capture initial CSRF/session cookie first.",
            },
            "local_oob_credential_seed_required": {
                "prior": 0.10,
                "alpha_count": 2.5,
                "description": "Credentials/tokens are dynamically generated on device filesystem (`/etc/`, `/var/`, `/tmp/`).",
                "remediation": "Extract token or hash via serial console (`/dev/ttyUSB0`) or local config backup.",
            },
        },
        "evidence_likelihoods": {
            "www_authenticate_header_present": {
                "probe_cmd": "curl -sS -k -I http://<target>/api",
                "description": "Response headers include `WWW-Authenticate` (Bearer/Basic/Digest)",
                "p_given_h": {
                    "missing_bearer_or_api_key_header": 0.94,
                    "wrong_http_method_or_json_content_type": 0.05,
                    "reverse_proxy_ip_or_host_header_restriction": 0.10,
                    "session_cookie_or_csrf_handshake_needed": 0.25,
                    "local_oob_credential_seed_required": 0.60,
                },
            },
            "http_405_or_415_status": {
                "probe_cmd": "curl -sS -k -i -X OPTIONS http://<target>/api",
                "description": "Response status is 405 Method Not Allowed or 415 Unsupported Media Type",
                "p_given_h": {
                    "missing_bearer_or_api_key_header": 0.05,
                    "wrong_http_method_or_json_content_type": 0.96,
                    "reverse_proxy_ip_or_host_header_restriction": 0.05,
                    "session_cookie_or_csrf_handshake_needed": 0.10,
                    "local_oob_credential_seed_required": 0.05,
                },
            },
            "xff_127_0_0_1_changes_status": {
                "probe_cmd": "curl -sS -k -i -H 'X-Forwarded-For: 127.0.0.1' http://<target>/api",
                "description": "Adding `X-Forwarded-For: 127.0.0.1` changes HTTP status or response length",
                "p_given_h": {
                    "missing_bearer_or_api_key_header": 0.10,
                    "wrong_http_method_or_json_content_type": 0.02,
                    "reverse_proxy_ip_or_host_header_restriction": 0.96,
                    "session_cookie_or_csrf_handshake_needed": 0.05,
                    "local_oob_credential_seed_required": 0.10,
                },
            },
            "set_cookie_csrf_on_root": {
                "probe_cmd": "curl -sS -k -I http://<target>/",
                "description": "Root endpoint sets a `Set-Cookie` header (session/CSRF)",
                "p_given_h": {
                    "missing_bearer_or_api_key_header": 0.15,
                    "wrong_http_method_or_json_content_type": 0.10,
                    "reverse_proxy_ip_or_host_header_restriction": 0.10,
                    "session_cookie_or_csrf_handshake_needed": 0.93,
                    "local_oob_credential_seed_required": 0.20,
                },
            },
        },
    },
}


_PRIORS_RAM_CACHE: Dict[str, Any] = {"mtime": -1.0, "data": None}


def load_or_init_profiles() -> Dict[str, Any]:
    ensure_directories()
    if PRIORS_FILE.is_file():
        try:
            mtime = PRIORS_FILE.stat().st_mtime
            if _PRIORS_RAM_CACHE["mtime"] == mtime and _PRIORS_RAM_CACHE["data"] is not None:
                return _PRIORS_RAM_CACHE["data"]
            raw_txt = PRIORS_FILE.read_text(encoding="utf-8")
            data = json.loads(raw_txt)
            # If legacy hardcoded IPs exist in the persisted priors file, migrate to parameterized templates
            if isinstance(data, dict) and data and "172.24." not in raw_txt:
                dirty = False
                for prof_k, def_prof in DEFAULT_CYBER_PROFILES.items():
                    if prof_k not in data:
                        data[prof_k] = json.loads(json.dumps(def_prof))
                        dirty = True
                    else:
                        ev_map = data[prof_k].setdefault("evidence_likelihoods", {})
                        for ek, ev_def in def_prof.get("evidence_likelihoods", {}).items():
                            if ek not in ev_map:
                                ev_map[ek] = json.loads(json.dumps(ev_def))
                                dirty = True
                if dirty:
                    PRIORS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                    mtime = PRIORS_FILE.stat().st_mtime
                _PRIORS_RAM_CACHE["mtime"] = mtime
                _PRIORS_RAM_CACHE["data"] = data
                return data
        except Exception:
            pass
    PRIORS_FILE.write_text(json.dumps(DEFAULT_CYBER_PROFILES, indent=2) + "\n", encoding="utf-8")
    data = json.loads(json.dumps(DEFAULT_CYBER_PROFILES))
    try:
        _PRIORS_RAM_CACHE["mtime"] = PRIORS_FILE.stat().st_mtime
    except Exception:
        pass
    _PRIORS_RAM_CACHE["data"] = data
    return data


def shannon_entropy(probs: Dict[str, float]) -> float:
    h = 0.0
    for p in probs.values():
        if p > 1e-12:
            h -= p * math.log2(p)
    return h


def compute_posteriors(
    priors: Dict[str, float],
    evidence_likelihoods: Dict[str, Dict[str, Any]],
    observed_evidence: Dict[str, bool],
) -> Dict[str, float]:
    """Compute exact Bayesian posteriors P(H | E) given True/False observed evidence."""
    unnormalized: Dict[str, float] = {}
    total_prior = sum(max(1e-6, float(v)) for v in priors.values())
    for h, p0 in priors.items():
        prob = max(1e-6, float(p0)) / total_prior
        for ev_key, is_present in observed_evidence.items():
            if ev_key not in evidence_likelihoods:
                continue
            p_e_given_h = float(evidence_likelihoods[ev_key].get("p_given_h", {}).get(h, 0.5))
            p_e_given_h = min(0.999, max(0.001, p_e_given_h))
            likelihood = p_e_given_h if is_present else (1.0 - p_e_given_h)
            prob *= likelihood
        unnormalized[h] = prob

    norm = sum(unnormalized.values())
    if norm <= 0:
        n = len(priors) or 1
        return {h: 1.0 / n for h in priors}
    return {h: val / norm for h, val in unnormalized.items()}


def rank_next_probes_by_eig(
    current_posteriors: Dict[str, float],
    evidence_likelihoods: Dict[str, Dict[str, Any]],
    observed_evidence: Dict[str, bool],
) -> List[Dict[str, Any]]:
    """
    Compute Expected Information Gain (EIG = H(current) - E[H(posterior | probe)])
    for every unobserved diagnostic probe.
    """
    current_h = shannon_entropy(current_posteriors)
    ranked = []

    for ev_key, ev_meta in evidence_likelihoods.items():
        if ev_key in observed_evidence:
            continue
        p_given_h = ev_meta.get("p_given_h", {})
        # Marginal probability P(E = True) under current posteriors
        p_true = sum(
            current_posteriors[h] * min(0.999, max(0.001, float(p_given_h.get(h, 0.5))))
            for h in current_posteriors
        )
        p_false = 1.0 - p_true

        post_if_true = compute_posteriors(current_posteriors, {ev_key: ev_meta}, {ev_key: True})
        post_if_false = compute_posteriors(current_posteriors, {ev_key: ev_meta}, {ev_key: False})

        expected_post_h = p_true * shannon_entropy(post_if_true) + p_false * shannon_entropy(post_if_false)
        eig_bits = max(0.0, current_h - expected_post_h)

        ranked.append(
            {
                "evidence_key": ev_key,
                "eig_bits": round(eig_bits, 4),
                "p_positive": round(p_true, 3),
                "probe_cmd": ev_meta.get("probe_cmd", ""),
                "description": ev_meta.get("description", ev_key),
            }
        )

    ranked.sort(key=lambda x: -x["eig_bits"])
    return ranked


def update_learned_prior(profile_name: str, confirmed_hypothesis: str) -> str:
    """Update Dirichlet alpha pseudo-counts when a root cause is confirmed, growing system intelligence."""
    profiles = load_or_init_profiles()
    if profile_name not in profiles:
        return f"Profile '{profile_name}' not found."
    hyps = profiles[profile_name].get("hypotheses", {})
    if confirmed_hypothesis not in hyps:
        return f"Hypothesis '{confirmed_hypothesis}' not in profile '{profile_name}'."

    hyps[confirmed_hypothesis]["alpha_count"] = float(hyps[confirmed_hypothesis].get("alpha_count", 3.0)) + 1.0
    total_alpha = sum(float(h.get("alpha_count", 3.0)) for h in hyps.values())
    for h_key, h_obj in hyps.items():
        h_obj["prior"] = round(float(h_obj.get("alpha_count", 3.0)) / total_alpha, 4)

    PRIORS_FILE.write_text(json.dumps(profiles, indent=2) + "\n", encoding="utf-8")
    return (
        f"Updated Bayesian prior for `{confirmed_hypothesis}` in profile `{profile_name}` "
        f"(new prior: {hyps[confirmed_hypothesis]['prior']:.1%})."
    )


def run_bayesian_abduction(
    problem: str,
    profile: str = "http_api_unreachable",
    observed_evidence: Optional[Dict[str, bool]] = None,
    custom_hypotheses: Optional[Dict[str, float]] = None,
    custom_likelihoods: Optional[Dict[str, Dict[str, float]]] = None,
    confirmed_cause: Optional[str] = None,
    target: Optional[str] = None,
    save_to_vault: bool = True,
) -> Dict[str, Any]:
    """
    Execute Bayesian Abductive Reasoning and optionally save to ObsidianVault.
    """
    profiles = load_or_init_profiles()
    if not isinstance(observed_evidence, dict):
        observed_evidence = {}
    else:
        alias_map = {
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
            "serial_oob_shows_filtered_or_custom_port": "serial_ss_shows_127_0_0_1_only",
        }
        observed_evidence = {alias_map.get(k, k): bool(v) for k, v in observed_evidence.items()}

    learning_note = ""
    if confirmed_cause and profile in profiles:
        learning_note = update_learned_prior(profile, confirmed_cause)
        profiles = load_or_init_profiles()

    if isinstance(custom_hypotheses, dict) and custom_hypotheses:
        priors = {k: float(v) for k, v in custom_hypotheses.items()}
        hyp_meta = {k: {"description": k, "remediation": "Verify hypothesis directly."} for k in priors}
        ev_map = {}
        if isinstance(custom_likelihoods, dict) and custom_likelihoods:
            for ev_k, p_map in custom_likelihoods.items():
                ev_map[ev_k] = {"description": ev_k, "probe_cmd": "", "p_given_h": p_map}
    else:
        prof_key = profile if profile in profiles else "http_api_unreachable"
        prof_obj = profiles[prof_key]
        priors = {k: float(v.get("prior", 0.2)) for k, v in prof_obj["hypotheses"].items()}
        hyp_meta = prof_obj["hypotheses"]
        ev_map = prof_obj.get("evidence_likelihoods", {})

    prior_entropy = shannon_entropy(priors)
    posteriors = compute_posteriors(priors, ev_map, observed_evidence)
    posterior_entropy = shannon_entropy(posteriors)
    ranked_hyps: List[Tuple[str, float]] = sorted(posteriors.items(), key=lambda x: -x[1])
    next_probes = rank_next_probes_by_eig(posteriors, ev_map, observed_evidence)

    ctx = resolve_problem_targets(problem, target_ip=target or "")
    target_str = ctx["primary_ip"] if ctx["has_concrete_primary_ip"] else (target or "<TARGET_IP>")
    for p in next_probes:
        cmd_tpl = p.get("probe_cmd", "")
        cmd_tpl = cmd_tpl.replace("<target>", "{target_ip}").replace("<target_ip>", "{target_ip}").replace("<gateway_ip>", "{gateway_ip}").replace("<iface>", "{iface}")
        rendered_cmd = render_command_template(cmd_tpl, ctx)
        if ctx["target_os"] == "windows":
            if rendered_cmd.startswith("ip neigh show"):
                rendered_cmd = f"arp -a {ctx['primary_ip']}" if ctx["has_concrete_primary_ip"] else "arp -a"
            elif rendered_cmd.startswith("ip route get"):
                rendered_cmd = "route print -4"
            elif rendered_cmd.startswith("ping -c "):
                rendered_cmd = re.sub(r"^ping\s+-c\s+(\d+)(?:\s+-W\s+\d+)?", r"ping -n \1 -w 1000", rendered_cmd)
        p["probe_cmd"] = rendered_cmd
        p["description"] = render_command_template(p.get("description", ""), ctx)

    top_h, top_p = ranked_hyps[0]
    md_lines = [
        f"## Problem Statement\n- **Target / Context:** `{target_str}`\n- **Problem:** {problem}\n- **Profile:** `{profile}`",
        f"- **Uncertainty Reduction:** `{prior_entropy:.3f} bits` (prior) $\\rightarrow$ `{posterior_entropy:.3f} bits` (posterior)",
    ]
    if learning_note:
        md_lines.append(f"- **Continual Learning Update:** {learning_note}")

    if observed_evidence:
        ev_items = [f"`{k}={v}`" for k, v in observed_evidence.items()]
        md_lines.append(f"- **Observed Evidence:** {', '.join(ev_items)}\n")
    else:
        md_lines.append("- **Observed Evidence:** *(None provided yet — ranking from learned priors & EIG)*\n")

    md_lines.append("## 1. Posterior Root-Cause Ranking $P(H_i \\mid E)$")
    md_lines.append("| Rank | Hypothesis | Posterior $P(H \\mid E)$ | Prior $P(H)$ | Recommended Remediation / Action |")
    md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for idx, (h_key, post_p) in enumerate(ranked_hyps, 1):
        prior_p = priors.get(h_key, 0.0)
        rem = render_command_template(hyp_meta.get(h_key, {}).get("remediation", ""), ctx)
        md_lines.append(f"| **{idx}** | `{h_key}` | **{post_p:.1%}** | {prior_p:.1%} | {rem} |")

    if next_probes:
        md_lines.append("\n## 2. Optimal Next Diagnostic Probes (Ranked by Expected Information Gain)")
        md_lines.append("| Priority | Diagnostic Evidence Key | EIG (bits) | $P(\\text{Positive})$ | Exact Verification Command |")
        md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for idx, pr in enumerate(next_probes[:4], 1):
            cmd_str = f"`{pr['probe_cmd']}`" if pr["probe_cmd"] else "*(custom check)*"
            md_lines.append(
                f"| **#{idx}** | `{pr['evidence_key']}` | **`{pr['eig_bits']:.4f}`** | {pr['p_positive']:.1%} | {cmd_str} |"
            )

    markdown_report = "\n".join(md_lines)
    vault_ref = ""
    if save_to_vault:
        title_slug = f"bayesian_{slugify(target_str)}_{slugify(profile)}"
        summary = f"Bayesian Abduction for {target_str}: top cause `{top_h}` ({top_p:.1%})"
        vault_ref = save_reasoning_to_vault(
            title=title_slug,
            summary=summary,
            markdown_body=markdown_report,
            engine_type="bayesian",
            tags=["bayesian", "abduction", slugify(target_str)],
        )

    hw = get_hardware_reasoning_limits()
    max_hyps = int(hw.get("max_abductive_hypotheses", 16))
    eig_depth = int(hw.get("eig_lookahead_depth", 3))
    return {
        "engine": "bayesian_abduction",
        "profile": profile,
        "target": target_str,
        "hardware_tier": hw.get("tier", "HIGH_PERFORMANCE"),
        "eig_lookahead_depth": eig_depth,
        "prior_entropy_bits": round(prior_entropy, 4),
        "posterior_entropy_bits": round(posterior_entropy, 4),
        "top_hypothesis": top_h,
        "top_probability": round(top_p, 4),
        "ranked_hypotheses": [
            {
                "hypothesis": h,
                "posterior": round(p, 4),
                "prior": round(priors.get(h, 0.0), 4),
                "remediation": hyp_meta.get(h, {}).get("remediation", ""),
            }
            for h, p in ranked_hyps[:max_hyps]
        ],
        "recommended_next_probes": next_probes[: max(4, eig_depth * 2)],
        "learning_update": learning_note,
        "vault_note": vault_ref,
        "markdown_report": markdown_report,
    }
