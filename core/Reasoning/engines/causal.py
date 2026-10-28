"""
Engine 2: Causal Reasoning Engine (Structural Causal Models, DAGs, do-Calculus & Counterfactuals).
100% CPU execution via `networkx` (lazy-loaded, 0 MB GPU VRAM).

Capabilities:
- Constructs and validates Causal Directed Acyclic Graphs (DAGs).
- Performs Pearl's `do(X = x)` graph surgery (removes incoming edges to intervened variables
  and propagates downstream causal probabilities/effects).
- Separates upstream root causes from downstream symptoms.
- Identifies backdoor confounders and minimal cut-sets (choke points) between source and target nodes.
- Persists learned/custom DAGs in `Reasoning/data/causal_dags/` and writes Mermaid-illustrated
  reports to `ObsidianVault/reasoning/`.
"""
from typing import Any, Dict, List, Optional, Set, Tuple

from .vault_bridge import get_hardware_reasoning_limits, load_json_data, save_json_data, save_reasoning_to_vault, slugify

DEFAULT_CAUSAL_DAGS: Dict[str, Dict[str, Any]] = {
    "network_api_reachability": {
        "description": "Causal DAG for target API reachability and Out-of-Band (OOB) serial console intervention.",
        "nodes": {
            "Physical_Link": {"base_prob": 0.95, "role": "root_infra"},
            "Local_Subnet_IP_Route": {"base_prob": 0.70, "role": "local_config"},
            "VLAN_Tag_Alignment": {"base_prob": 0.75, "role": "l2_config"},
            "ARP_MAC_Resolution": {"base_prob": 0.80, "role": "l2_state"},
            "Serial_Console_OOB": {"base_prob": 0.90, "role": "oob_control"},
            "Target_Firewall_Allow": {"base_prob": 0.65, "role": "target_security"},
            "API_Daemon_Bound_0000": {"base_prob": 0.70, "role": "target_service"},
            "TCP_SYN_ACK_Handshake": {"base_prob": 0.50, "role": "l4_transport"},
            "HTTP_API_Access": {"base_prob": 0.40, "role": "target_goal"},
        },
        "edges": [
            {"source": "Physical_Link", "target": "ARP_MAC_Resolution", "weight": 0.95, "mechanism": "electrical/optical carrier"},
            {"source": "Local_Subnet_IP_Route", "target": "ARP_MAC_Resolution", "weight": 0.90, "mechanism": "egress interface selection"},
            {"source": "VLAN_Tag_Alignment", "target": "ARP_MAC_Resolution", "weight": 0.90, "mechanism": "802.1Q broadcast domain"},
            {"source": "Serial_Console_OOB", "target": "VLAN_Tag_Alignment", "weight": 0.85, "mechanism": "inspect/reconfigure target NIC via /dev/ttyUSB0"},
            {"source": "Serial_Console_OOB", "target": "Target_Firewall_Allow", "weight": 0.95, "mechanism": "flush/allow iptables via /dev/ttyUSB0"},
            {"source": "Serial_Console_OOB", "target": "API_Daemon_Bound_0000", "weight": 0.95, "mechanism": "restart/bind service or SSH/socat forward"},
            {"source": "ARP_MAC_Resolution", "target": "TCP_SYN_ACK_Handshake", "weight": 0.95, "mechanism": "L2 frame delivery"},
            {"source": "Target_Firewall_Allow", "target": "TCP_SYN_ACK_Handshake", "weight": 0.95, "mechanism": "INPUT chain permit"},
            {"source": "API_Daemon_Bound_0000", "target": "TCP_SYN_ACK_Handshake", "weight": 0.95, "mechanism": "listening socket backlog"},
            {"source": "TCP_SYN_ACK_Handshake", "target": "HTTP_API_Access", "weight": 0.98, "mechanism": "HTTP request/response stream"},
        ],
    },
    "l2_l3_cross_subnet_routing": {
        "description": "Causal DAG for multi-hop Layer-2 / Layer-3 traffic routing across isolated subnets.",
        "nodes": {
            "Local_Static_Route": {"base_prob": 0.65, "role": "local_config"},
            "L2_Neighbor_Adjacency": {"base_prob": 0.80, "role": "l2_state"},
            "Pivot_Gateway_Ingress": {"base_prob": 0.75, "role": "transit"},
            "Pivot_IP_Forward_Sysctl": {"base_prob": 0.60, "role": "transit_config"},
            "Pivot_Forward_Firewall": {"base_prob": 0.65, "role": "transit_security"},
            "Destination_Reachability": {"base_prob": 0.85, "role": "target_host"},
            "Return_Route_Or_MASQUERADE": {"base_prob": 0.55, "role": "return_path"},
            "End_To_End_L3_Routing": {"base_prob": 0.35, "role": "target_goal"},
        },
        "edges": [
            {"source": "Local_Static_Route", "target": "Pivot_Gateway_Ingress", "weight": 0.95, "mechanism": "next-hop forwarding"},
            {"source": "L2_Neighbor_Adjacency", "target": "Pivot_Gateway_Ingress", "weight": 0.95, "mechanism": "L2 MAC framing"},
            {"source": "Pivot_Gateway_Ingress", "target": "Destination_Reachability", "weight": 0.90, "mechanism": "packet arrival at router"},
            {"source": "Pivot_IP_Forward_Sysctl", "target": "Destination_Reachability", "weight": 0.95, "mechanism": "net.ipv4.ip_forward=1"},
            {"source": "Pivot_Forward_Firewall", "target": "Destination_Reachability", "weight": 0.95, "mechanism": "FORWARD chain ACCEPT"},
            {"source": "Destination_Reachability", "target": "End_To_End_L3_Routing", "weight": 0.95, "mechanism": "forward packet delivery"},
            {"source": "Return_Route_Or_MASQUERADE", "target": "End_To_End_L3_Routing", "weight": 0.95, "mechanism": "symmetric return path / SNAT"},
        ],
    },
    "api_auth_exploitation_chain": {
        "description": "Causal DAG for API authentication, reverse-proxy trust, and privilege escalation.",
        "nodes": {
            "HTTP_Transport_Ready": {"base_prob": 0.90, "role": "prerequisite"},
            "Endpoint_Route_Enumeration": {"base_prob": 0.80, "role": "recon"},
            "Reverse_Proxy_Header_Bypass": {"base_prob": 0.45, "role": "bypass_vector"},
            "OOB_Or_Config_Token_Leak": {"base_prob": 0.60, "role": "credential_vector"},
            "Valid_Auth_Context": {"base_prob": 0.50, "role": "auth_state"},
            "Method_And_Schema_Match": {"base_prob": 0.80, "role": "request_validity"},
            "Privileged_API_Execution": {"base_prob": 0.35, "role": "target_goal"},
        },
        "edges": [
            {"source": "HTTP_Transport_Ready", "target": "Endpoint_Route_Enumeration", "weight": 0.95, "mechanism": "HTTP probing"},
            {"source": "Endpoint_Route_Enumeration", "target": "Method_And_Schema_Match", "weight": 0.90, "mechanism": "OPTIONS / OpenAPI discovery"},
            {"source": "Reverse_Proxy_Header_Bypass", "target": "Valid_Auth_Context", "weight": 0.85, "mechanism": "X-Forwarded-For / Host trust"},
            {"source": "OOB_Or_Config_Token_Leak", "target": "Valid_Auth_Context", "weight": 0.95, "mechanism": "extracted Bearer/API key"},
            {"source": "Valid_Auth_Context", "target": "Privileged_API_Execution", "weight": 0.95, "mechanism": "authorization middleware pass"},
            {"source": "Method_And_Schema_Match", "target": "Privileged_API_Execution", "weight": 0.95, "mechanism": "controller handler execution"},
        ],
    },
}


def ensure_default_dags() -> None:
    for name, dag_data in DEFAULT_CAUSAL_DAGS.items():
        existing = load_json_data("causal_dags", name)
        if existing is None or "172.24." in str(existing.get("description", "")):
            save_json_data("causal_dags", name, dag_data)


def _propagate_scm_probabilities(
    G: Any,
    base_probs: Dict[str, float],
    interventions: Dict[str, float],
    observations: Dict[str, float],
) -> Dict[str, float]:
    """
    Propagate structural causal probabilities in topological order.
    - Intervened nodes (`do(X = val)`) have incoming edges severed and their value fixed to `val`.
    - Non-intervened nodes combine parent states via weighted noisy-AND / structural gate.
    """
    import networkx as nx

    probs: Dict[str, float] = {}
    for node in nx.topological_sort(G):
        if node in interventions:
            probs[node] = min(1.0, max(0.0, float(interventions[node])))
            continue
        preds = list(G.predecessors(node))
        if not preds:
            val = float(observations.get(node, base_probs.get(node, 0.7)))
            probs[node] = min(1.0, max(0.0, val))
            continue

        # Differentiate OR-like bypass/control parents vs AND-like infrastructure prerequisites
        oob_or_bypass_preds = [
            p for p in preds if any(k in p.lower() for k in ("oob", "serial", "bypass", "leak", "masquerade"))
        ]
        standard_preds = [p for p in preds if p not in oob_or_bypass_preds]

        and_factor = 1.0
        for p in standard_preds:
            w = float(G[p][node].get("weight", 0.9))
            p_val = probs.get(p, 0.5)
            # Weighted prerequisite contribution
            and_factor *= (1.0 - w) + w * p_val

        if oob_or_bypass_preds:
            # Noisy-OR boost from out-of-band / alternative causal mechanisms
            noisy_or_fail = 1.0 - (and_factor if standard_preds else (1.0 - base_probs.get(node, 0.5)))
            for p in oob_or_bypass_preds:
                w = float(G[p][node].get("weight", 0.9))
                p_val = probs.get(p, 0.0)
                noisy_or_fail *= 1.0 - (w * p_val)
            computed = 1.0 - noisy_or_fail
        else:
            computed = and_factor

        if node in observations:
            # Blend observation with structural propagation if not a hard intervention
            obs_v = float(observations[node])
            computed = 0.75 * obs_v + 0.25 * computed

        probs[node] = round(min(1.0, max(0.0, computed)), 4)

    return probs


def run_causal_reasoning(
    dag_name: str = "network_api_reachability",
    outcome_node: Optional[str] = None,
    observations: Optional[Dict[str, float]] = None,
    do_interventions: Optional[Dict[str, float]] = None,
    custom_edges: Optional[List[Dict[str, Any]]] = None,
    save_custom_dag: bool = False,
    save_to_vault: bool = True,
) -> Dict[str, Any]:
    """
    Execute Causal DAG analysis, Pearl's `do(X)` intervention simulation, root-cause
    ancestry tracing, confounder detection, and minimal choke-point identification.
    """
    import networkx as nx

    ensure_default_dags()
    observations = observations or {}
    do_interventions = do_interventions or {}

    dag_spec = load_json_data("causal_dags", dag_name)
    if dag_spec is None and not custom_edges:
        dag_spec = DEFAULT_CAUSAL_DAGS["network_api_reachability"]
        dag_name = "network_api_reachability"
    elif dag_spec is None:
        dag_spec = {"description": f"Custom Causal DAG ({dag_name})", "nodes": {}, "edges": []}

    G = nx.DiGraph()
    base_probs: Dict[str, float] = {}

    for n_name, n_meta in dag_spec.get("nodes", {}).items():
        G.add_node(n_name, **n_meta)
        base_probs[n_name] = float(n_meta.get("base_prob", 0.7))

    edges_to_load = custom_edges if custom_edges else dag_spec.get("edges", [])
    for e in edges_to_load:
        u = e["source"]
        v = e["target"]
        w = float(e.get("weight", 0.9))
        mech = e.get("mechanism", "causal link")
        if u not in base_probs:
            base_probs[u] = 0.7
            G.add_node(u, base_prob=0.7)
        if v not in base_probs:
            base_probs[v] = 0.5
            G.add_node(v, base_prob=0.5)
        G.add_edge(u, v, weight=w, mechanism=mech)

    if not nx.is_directed_acyclic_graph(G):
        cycles = list(nx.simple_cycles(G))
        return {"error": f"Graph contains cycles and is not a valid Causal DAG: {cycles}"}

    if save_custom_dag and custom_edges:
        save_json_data(
            "causal_dags",
            dag_name,
            {
                "description": dag_spec.get("description", f"Custom causal graph {dag_name}"),
                "nodes": {n: {"base_prob": base_probs.get(n, 0.7)} for n in G.nodes()},
                "edges": edges_to_load,
            },
        )

    # Identify outcome node (default to sink node in topological sort)
    topo_nodes = list(nx.topological_sort(G))
    if not outcome_node or outcome_node not in G:
        sinks = [n for n in G.nodes() if G.out_degree(n) == 0]
        outcome_node = sinks[0] if sinks else topo_nodes[-1]

    # 1. Observational baseline probabilities P(Y | Observations)
    baseline_probs = _propagate_scm_probabilities(G, base_probs, interventions={}, observations=observations)

    # 2. Interventional probabilities P(Y | do(X), Observations) via graph surgery (G_do)
    G_do = G.copy()
    severed_edges: List[Tuple[str, str]] = []
    for int_node in do_interventions:
        if int_node in G_do:
            in_edges = list(G_do.in_edges(int_node))
            severed_edges.extend(in_edges)
            G_do.remove_edges_from(in_edges)

    intervened_probs = _propagate_scm_probabilities(
        G_do, base_probs, interventions=do_interventions, observations=observations
    )

    # 3. Single-node Average Causal Effect (ACE) ranking: P(Outcome | do(Node=1)) - P(Outcome | do(Node=0))
    causal_leverage_ranking = []
    for candidate in topo_nodes:
        if candidate == outcome_node:
            continue
        p_do_1 = _propagate_scm_probabilities(
            G, base_probs, interventions={**do_interventions, candidate: 1.0}, observations=observations
        )[outcome_node]
        p_do_0 = _propagate_scm_probabilities(
            G, base_probs, interventions={**do_interventions, candidate: 0.0}, observations=observations
        )[outcome_node]
        ace = round(p_do_1 - p_do_0, 4)
        causal_leverage_ranking.append(
            {
                "node": candidate,
                "ace_on_outcome": ace,
                "p_outcome_if_do_1": round(p_do_1, 4),
                "p_outcome_if_do_0": round(p_do_0, 4),
                "is_root_cause": G.in_degree(candidate) == 0,
            }
        )
    causal_leverage_ranking.sort(key=lambda x: -x["ace_on_outcome"])

    # 4. Confounders (common ancestors of multiple pathways) & Root Causes
    root_nodes = [n for n in topo_nodes if G.in_degree(n) == 0]
    confounders = [n for n in topo_nodes if G.out_degree(n) >= 2]

    # 5. Minimal Cut-Set (choke points between roots and outcome_node)
    choke_points: List[str] = []
    ancestors = nx.ancestors(G, outcome_node)
    for cand in ancestors:
        G_removed = G.copy()
        G_removed.remove_node(cand)
        still_reachable = any(
            r in G_removed and outcome_node in G_removed and nx.has_path(G_removed, r, outcome_node)
            for r in root_nodes
        )
        if not still_reachable:
            choke_points.append(cand)

    # Build Mermaid diagram
    mermaid_lines = ["```mermaid", "flowchart TD"]
    for n in topo_nodes:
        p_base = baseline_probs.get(n, 0.0)
        p_int = intervened_probs.get(n, p_base)
        if n in do_interventions:
            label = f'{n}["do({n} = {do_interventions[n]:.2f})"]'
        elif do_interventions:
            label = f'{n}["{n} ({p_base:.0%} -> {p_int:.0%})"]'
        else:
            label = f'{n}["{n} ({p_base:.0%})"]'
        mermaid_lines.append(f"    {label}")
    for u, v, d in G.edges(data=True):
        mech = d.get("mechanism", "")
        if (u, v) in severed_edges:
            mermaid_lines.append(f'    {u} -. "severed by do()" .-> {v}')
        else:
            mermaid_lines.append(f'    {u} -- "{mech}" --> {v}')
    mermaid_lines.append("```")

    outcome_delta = round(intervened_probs[outcome_node] - baseline_probs[outcome_node], 4)
    md_lines = [
        f"## Causal Model: `{dag_name}`",
        f"- **Description:** {dag_spec.get('description', '')}",
        f"- **Target Outcome Node:** `{outcome_node}`",
        f"- **Baseline $P(\\text{{{outcome_node}}})$:** `{baseline_probs[outcome_node]:.1%}`",
    ]
    if do_interventions:
        do_str = ", ".join(f"do({k}={v})" for k, v in do_interventions.items())
        md_lines.append(
            f"- **Interventional $P(\\text{{{outcome_node}}} \\mid {do_str})$:** "
            f"**`{intervened_probs[outcome_node]:.1%}`** (Causal Lift $\\Delta = {outcome_delta:+.1%}$)"
        )
    md_lines.append(f"- **Upstream Root Causes:** {', '.join(f'`{r}`' for r in root_nodes)}")
    md_lines.append(
        f"- **Single-Node Choke Points (Cut-Sets):** "
        f"{', '.join(f'`{c}`' for c in choke_points) if choke_points else '*(Multiple redundant paths exist)*'}"
    )
    if confounders:
        md_lines.append(f"- **Shared Confounders / Branch Nodes:** {', '.join(f'`{c}`' for c in confounders)}")

    md_lines.append("\n## 1. Causal DAG Topology & Signal Propagation\n" + "\n".join(mermaid_lines))
    md_lines.append(f"\n## 2. Highest-Leverage `do(X=1)` Interventions on `{outcome_node}`")
    md_lines.append("| Rank | Variable $X$ | Causal Effect $\\text{ACE}$ | $P(\\text{Outcome} \\mid \\text{do}(X=1))$ | $P(\\text{Outcome} \\mid \\text{do}(X=0))$ | Role |")
    md_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for idx, item in enumerate(causal_leverage_ranking[:6], 1):
        role_tag = "Root Cause" if item["is_root_cause"] else "Intermediate Mechanism"
        md_lines.append(
            f"| **{idx}** | `{item['node']}` | **`{item['ace_on_outcome']:+.1%}`** | "
            f"{item['p_outcome_if_do_1']:.1%} | {item['p_outcome_if_do_0']:.1%} | {role_tag} |"
        )

    markdown_report = "\n".join(md_lines)
    vault_ref = ""
    if save_to_vault:
        title_slug = f"causal_{slugify(dag_name)}_{slugify(outcome_node)}"
        summary = (
            f"Causal DAG `{dag_name}` -> `{outcome_node}` "
            f"(Baseline {baseline_probs[outcome_node]:.0%}, Intervened {intervened_probs[outcome_node]:.0%})"
        )
        vault_ref = save_reasoning_to_vault(
            title=title_slug,
            summary=summary,
            markdown_body=markdown_report,
            engine_type="causal",
            tags=["causal", "dag", slugify(dag_name)],
        )

    hw = get_hardware_reasoning_limits()
    max_paths = int(hw.get("causal_counterfactual_paths", 32))
    return {
        "engine": "causal_reasoning",
        "dag_name": dag_name,
        "outcome_node": outcome_node,
        "hardware_tier": hw.get("tier", "HIGH_PERFORMANCE"),
        "causal_counterfactual_paths": max_paths,
        "baseline_outcome_prob": baseline_probs[outcome_node],
        "intervened_outcome_prob": intervened_probs[outcome_node],
        "causal_lift_delta": outcome_delta,
        "root_causes": root_nodes,
        "choke_points": choke_points,
        "confounders": confounders,
        "highest_leverage_interventions": causal_leverage_ranking[: max(6, min(16, max_paths // 4))],
        "node_probabilities": intervened_probs,
        "vault_note": vault_ref,
        "markdown_report": markdown_report,
    }
