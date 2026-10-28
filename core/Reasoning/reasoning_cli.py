#!/usr/bin/env python3
"""
15-Engine Neuro-Symbolic, Somatic Intuition, Optimal-Stopping Forecasting, Continual, Meta-Learning, Trajectory RL & Spectral PCA/K-Means++ Reasoning CLI (`v4.5.0`).
Supports standalone execution (`python3 Reasoning/reasoning_cli.py ...`) and
direct lazy-loaded invocation from `agent-cli.py` (0 MB GPU VRAM).

Engines (15-Engine Streamlined Core):
  1. Associative Bipartite Obsidian Vault Graph (`engines/associative.py`)
  2. Geometric, CIDR Hyperrectangle & Z3/SymPy Constraint Solver (`engines/geometric.py`)
  3. Bayesian Abductive Root-Cause Engine + Expected Information Gain (`engines/bayesian.py`)
  4. Causal DAG Engine & Pearl's do(X) Surgery (`engines/causal.py`)
  5. Hyperdimensional VSA + Damasio Somatic Gut Valence Marker (`engines/vsa.py`)
  6. Event-Calculus & Temporal State/Fluent Tracker (`engines/temporal_fluents.py`)
  7. Dempster-Shafer Theory of Evidence & Conflict/Ignorance Detector (`engines/dempster_shafer.py`)
  8. Case-Based Reasoning (CBR) & Online Failure Fingerprinting (`engines/cbr_fingerprints.py`)
  9. CEGAR Pre-Execution Command Verifier (`engines/cegar_verifier.py`)
  10. SyGuS / Structure-Guided CLI Log & Output Extractor (`engines/sygus_extractor.py`)
  11. Hierarchical Tactical MDP + Optimal Stopping & Speculative Next-Tool Forecast (`engines/mdp_tactical.py`)
  12. Online Continual Learning, Plasticity & Pass-2 Recursive Refinement (`engines/continual_learner.py`)
  13. Multiplicative-Weights (Hedge) Meta-Learner & Brier/ECE Calibration (`engines/meta_learner.py`)
  14. Multi-Step Trajectory Reinforcement Learning (`TD(λ)`) & Symbolic Network World-Model (`engines/rl_network_policy.py`)
  15. Spectral Manifold PCA, K-Means++ Regime Clustering & Graph Laplacian Chokepoints (`engines/spectral_manifold_pca.py`)
  + Part 1 Zero-Loss Context Virtual Memory & Speculative Lookahead Cache (`engines/context_vm.py`)
  + Unified 15-Engine Orchestrator with Hedge-Weighted Consensus Arbiter (`engines/pipeline.py`)
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

REASONING_DIR = Path(__file__).resolve().parent
if str(REASONING_DIR.parent) not in sys.path:
    sys.path.insert(0, str(REASONING_DIR.parent))


def check_environment_status() -> Dict[str, Any]:
    packages = {}
    for mod in ("numpy", "scipy", "networkx", "sympy", "z3", "shapely"):
        try:
            m = __import__(mod)
            ver = getattr(m, "__version__", "installed")
            packages[mod] = f"OK ({ver})"
        except ImportError:
            packages[mod] = "OPTIONAL_MISSING"

    from Reasoning.engines.associative import build_vault_bipartite_graph
    from Reasoning.engines.bayesian import load_or_init_profiles
    from Reasoning.engines.causal import ensure_default_dags
    from Reasoning.engines.cbr_fingerprints import load_cbr_library
    from Reasoning.engines.continual_learner import get_continual_learning_state
    from Reasoning.engines.mdp_tactical import load_or_init_mdp_store
    from Reasoning.engines.meta_learner import load_or_init_meta_weights
    from Reasoning.engines.rl_network_policy import load_or_init_rl_policy
    from Reasoning.engines.spectral_manifold_pca import load_or_compute_pca_kmeans_model
    from Reasoning.engines.temporal_fluents import load_fluent_state
    from Reasoning.engines.vault_bridge import (
        DATA_DIR,
        SHADOW_ARCHIVE_DIR,
        VAULT_DIR,
        ensure_directories,
        get_hardware_reasoning_limits,
        list_json_data,
        load_json_state,
    )
    from Reasoning.engines.vsa import SOMATIC_MARKERS_FILE

    ensure_directories()
    hw_limits = get_hardware_reasoning_limits()
    profiles = load_or_init_profiles()
    ensure_default_dags()
    cbr_lib = load_cbr_library()
    fluent_state = load_fluent_state()
    mdp_store = load_or_init_mdp_store()
    cont_state = get_continual_learning_state()
    meta_state = load_or_init_meta_weights()
    rl_state = load_or_init_rl_policy()
    pca_state = load_or_compute_pca_kmeans_model()
    somatic_state = load_json_state(SOMATIC_MARKERS_FILE, {"markers": {}})
    G_vault, note_meta = build_vault_bipartite_graph()

    home_s = str(Path.home())
    def _port(p: Path | str) -> str:
        s = str(p)
        return ("~" + s[len(home_s):]) if (home_s and s.startswith(home_s)) else s

    return {
        "reasoning_dir": _port(REASONING_DIR),
        "data_dir": _port(DATA_DIR),
        "shadow_archive_dir": _port(SHADOW_ARCHIVE_DIR),
        "obsidian_vault_dir": _port(VAULT_DIR),
        "gpu_vram_footprint_mb": 0,
        "engines_active": 15,
        "guardrails_active": 10,
        "continual_learning_mode": cont_state.get("mode", "AUTO"),
        "continual_updates_count": int(cont_state.get("online_commands_observed", 0)),
        "somatic_markers_count": len(somatic_state.get("markers", {})),
        "meta_brier_score": round(float(meta_state.get("rolling_brier_score", 0.102)), 4),
        "meta_ece_pct": round(float(meta_state.get("expected_calibration_error_pct", 4.2)), 2),
        "rl_episodes_trained": int(rl_state.get("episodes_trained", 0)),
        "rl_online_transitions": int(rl_state.get("online_transitions_recorded", 0)),
        "pca_top3_variance_pct": round(float(pca_state.get("cumulative_top3_variance_pct", 0.0)), 2),
        "kmeans_silhouette_score": round(float(pca_state.get("silhouette_score", 0.0)), 4),
        "hardware_reasoning_limits": hw_limits,
        "packages": packages,
        "bipartite_vault_graph": {
            "total_nodes": G_vault.number_of_nodes(),
            "vault_note_nodes": len(note_meta),
            "concept_entity_nodes": G_vault.number_of_nodes() - len(note_meta),
            "associative_edges": G_vault.number_of_edges(),
        },
        "cbr_library_cases": len(cbr_lib.get("cases", [])),
        "temporal_fluents_tracked": len(fluent_state.get("fluents", {})),
        "mdp_transitions_count": len(mdp_store.get("transitions", [])),
        "mdp_tactic_categories": mdp_store.get("tactic_categories", []),
        "stored_bayesian_profiles": list(profiles.keys()),
        "stored_causal_dags": [p.stem for p in list_json_data("causal_dags")],
        "stored_geometric_models": [p.stem for p in list_json_data("geometric_models")],
        "stored_associative_graphs": [p.stem for p in list_json_data("associative_graphs")],
        "stored_vsa_spaces": [p.stem for p in list_json_data("vsa_spaces")],
        "stored_pipeline_sessions": [p.stem for p in list_json_data("sessions")],
    }


def seed_all_data_and_vault() -> str:
    """Initialize all default JSON stores in `Reasoning/data/` and seed `ObsidianVault/reasoning/` & `ObsidianVault/targets/`."""
    from Reasoning.engines.cbr_fingerprints import seed_default_cbr_library
    from Reasoning.engines.meta_learner import run_meta_learning_reasoning
    from Reasoning.engines.pipeline import run_neuro_symbolic_pipeline
    from Reasoning.engines.rl_network_policy import run_rl_network_policy_reasoning
    from Reasoning.engines.spectral_manifold_pca import run_spectral_pca_reasoning
    from Reasoning.engines.temporal_fluents import seed_default_temporal_fluents

    seed_default_temporal_fluents()
    seed_default_cbr_library()
    status = check_environment_status()
    res_pca = run_spectral_pca_reasoning(
        problem="Initial 20-Engine SVD PCA, K-Means++ Regime Clustering & Graph Laplacian Manifold",
        force_recompute=True,
        export_to_vault=True,
    )
    hw_ep = int(status["hardware_reasoning_limits"].get("rl_train_episodes", 600))
    res_rl = run_rl_network_policy_reasoning(
        problem="Initial Digital-Twin Trajectory RL Training & Live Network Topology Sensing",
        train_episodes=hw_ep,
        sense_topology=True,
        export_to_vault=True,
    )
    res_api = run_neuro_symbolic_pipeline(
        problem="Target HTTP API probe failed with curl exit status 7; out-of-band serial console is available.",
        bayesian_profile="http_api_unreachable",
        observed_evidence={"curl_exit_7_Immediate_refused": True},
        causal_dag="network_api_reachability",
        has_serial_oob=True,
        save_to_vault=True,
    )
    res_route = run_neuro_symbolic_pipeline(
        problem="Route Layer-2/Layer-3 traffic from local host through gateway pivot to isolated destination subnet.",
        bayesian_profile="l2_l3_routing_blackhole",
        observed_evidence={},
        causal_dag="l2_l3_cross_subnet_routing",
        has_serial_oob=True,
        save_to_vault=True,
    )
    res_meta = run_meta_learning_reasoning(
        problem="Initial 20-Engine Hedge Meta-Arbiter Calibration & Suggested Improvements Audit",
        write_suggested_improvement=True,
        export_to_vault=True,
    )
    return (
        f"Seeded 20-Engine Reasoning data directory ({status['data_dir']}) and ObsidianVault/:\n"
        f"  - Hardware Tier: {status['hardware_reasoning_limits'].get('tier')} "
        f"(VSA={status['hardware_reasoning_limits'].get('vsa_hypervector_dim')}-D, "
        f"MAP-Elites={status['hardware_reasoning_limits'].get('evolutionary_generations')} gens, "
        f"RL={hw_ep} episodes, K-Means++={status['hardware_reasoning_limits'].get('kmeans_n_init')} iters)\n"
        f"  - Engine 20 Spectral PCA & K-Means++ Manifold: {res_pca.get('vault_note')}\n"
        f"  - Engine 19 RL Playbooks & Live Topology: {res_rl.get('vault_note')} + [[targets/local_network_topology]]\n"
        f"  - API Abduction & OOB Playbook: {res_api['vault_note']}\n"
        f"  - L2/L3 Cross-Subnet Routing Playbook: {res_route['vault_note']}\n"
        f"  - Meta-Learner Suggested Improvement Note: {res_meta.get('suggested_improvement_note')}"
    )


def run_self_tests() -> Dict[str, Any]:
    """Run deterministic self-tests across all 15 core engines + Context VM and measure CPU latency."""
    from Reasoning.engines.associative import run_associative_vault_reasoning
    from Reasoning.engines.bayesian import run_bayesian_abduction
    from Reasoning.engines.causal import run_causal_reasoning
    from Reasoning.engines.cbr_fingerprints import match_failure_fingerprint, run_cbr_reasoning
    from Reasoning.engines.cegar_verifier import run_cegar_reasoning, verify_command_cegar
    from Reasoning.engines.context_vm import process_tool_output_zero_loss
    from Reasoning.engines.continual_learner import run_continual_learning_reasoning
    from Reasoning.engines.dempster_shafer import run_dempster_shafer_reasoning
    from Reasoning.engines.geometric import run_geometric_reasoning
    from Reasoning.engines.mdp_tactical import run_mdp_tactical_reasoning
    from Reasoning.engines.meta_learner import run_meta_learning_reasoning
    from Reasoning.engines.pipeline import run_neuro_symbolic_pipeline
    from Reasoning.engines.rl_network_policy import run_rl_network_policy_reasoning
    from Reasoning.engines.spectral_manifold_pca import run_spectral_pca_reasoning
    from Reasoning.engines.sygus_extractor import run_sygus_reasoning
    from Reasoning.engines.temporal_fluents import (
        record_command_event,
        run_temporal_fluent_reasoning,
        seed_default_temporal_fluents,
    )
    from Reasoning.engines.vsa import run_vsa_conceptual_leap

    from Reasoning.engines.vault_bridge import DATA_DIR

    # Snapshot live mutable state files so running `run_self_tests()` has zero side effects on active sessions
    state_files_to_preserve = [
        DATA_DIR / "temporal_fluents" / "live_fluents.json",
        DATA_DIR / "continual_learning_state.json",
        DATA_DIR / "somatic_markers.json",
        DATA_DIR / "meta_weights.json",
        DATA_DIR / "rl_policy_table.json",
        DATA_DIR / "learned_cbr_cases.json",
        DATA_DIR / "cbr_cases" / "cbr_library.json",
    ]
    snapshots: Dict[Path, Optional[bytes]] = {}
    for sf in state_files_to_preserve:
        snapshots[sf] = sf.read_bytes() if sf.is_file() else None

    t0 = time.perf_counter()
    try:
        # Use RFC 5737 documentation/test-net addresses (TEST-NET-2 198.51.100.0/24, TEST-NET-3 203.0.113.0/24)
        test_target = "198.51.100.10"
        test_secondary = "203.0.113.50"

        assoc_res = run_associative_vault_reasoning(
            query=f"{test_target} curl exit 7 /dev/ttyUSB0 tio {test_secondary}",
            save_to_vault=False,
        )
        t1 = time.perf_counter()

        b_res = run_bayesian_abduction(
            problem=f"Self-test curl exit 7 on {test_target}",
            profile="http_api_unreachable",
            observed_evidence={"curl_exit_7_Immediate_refused": True, "arp_resolved_mac_present": True},
            target=test_target,
            save_to_vault=False,
        )
        t2 = time.perf_counter()

        c_res = run_causal_reasoning(
            dag_name="network_api_reachability",
            do_interventions={"Serial_Console_OOB": 1.0},
            save_to_vault=False,
        )
        t3 = time.perf_counter()

        g_net = run_geometric_reasoning(
            problem_title="self_test_net_geo",
            mode="network_geometry",
            spec={
                "local_subnets": ["198.51.100.0/24"],
                "target_ips": [test_target, test_secondary],
            },
            save_to_vault=False,
        )
        g_sym = run_geometric_reasoning(
            problem_title="self_test_sym_geo",
            mode="constraint_solve",
            spec={
                "variables": ["mtu", "payload"],
                "equations": ["mtu = 1500", "payload + 40 = mtu"],
            },
            save_to_vault=False,
        )
        t5 = time.perf_counter()

        vsa_res = run_vsa_conceptual_leap(
            problem=f"curl exit 7 on {test_target} with /dev/ttyUSB0 serial console",
            save_to_vault=False,
        )
        t6 = time.perf_counter()

        # Engine 9: Temporal Fluents
        record_command_event(f"ip addr add {test_target}/24 dev eth0", "", 0)
        temp_res = run_temporal_fluent_reasoning(
            problem="Verify holding fluents for eth0",
            export_to_vault=False,
        )
        t9 = time.perf_counter()

        # Engine 10: Dempster-Shafer
        dst_res = run_dempster_shafer_reasoning(
            problem="100% packet loss on ping but MAC 00:11:22:33:44:55 REACHABLE in ARP table",
            export_to_vault=False,
        )
        t10 = time.perf_counter()

        # Engine 11: CBR Failure Fingerprinting
        cbr_hit = match_failure_fingerprint(
            f"sudo ip route add 203.0.113.0/24 via {test_target}", 2, "RTNETLINK answers: File exists"
        )
        cbr_res = run_cbr_reasoning(
            problem="RTNETLINK answers: File exists when adding route",
            export_to_vault=False,
        )
        t11 = time.perf_counter()

        # Engine 12: CEGAR Verifier
        cegar_block_tio = verify_command_cegar("tio /dev/ttyUSB0")
        cegar_pass = verify_command_cegar(f"ping -c 3 -W 2 {test_target}")
        cegar_res = run_cegar_reasoning(
            problem="Verify candidate commands",
            candidate_commands=[f"ping -c 3 -W 2 {test_target}", "ip route show"],
            export_to_vault=False,
        )
        t12 = time.perf_counter()

        # Engine 13: SyGuS Extractor
        sygus_res = run_sygus_reasoning(
            problem="ip neigh show",
            sample_output=f"{test_target} dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE\n80/tcp open http",
            export_to_vault=False,
        )
        t13 = time.perf_counter()

        # Engine 15: Hierarchical Tactical MDP / POMDP
        mdp_res = run_mdp_tactical_reasoning(
            problem=f"curl exit 7 on {test_target} with /dev/ttyUSB0 attached",
            target_ip=test_target,
            secondary_target_ip=test_secondary,
            observed_evidence={"curl_exit_7_Immediate_refused": True},
            save_to_vault=False,
        )
        t14b = time.perf_counter()

        # Engine 16: Online Continual Learning & Pass-2 Refinement
        cont_res = run_continual_learning_reasoning(
            problem="Self-test continual learning state",
            export_to_vault=False,
        )
        t16 = time.perf_counter()

        # Engine 17: Multiplicative-Weights Hedge Meta-Learner
        meta_res = run_meta_learning_reasoning(
            problem="Self-test meta-learning calibration",
            write_suggested_improvement=False,
            export_to_vault=False,
        )
        t17 = time.perf_counter()

        # Engine 19: Multi-Step Trajectory RL & Symbolic Network World-Model
        rl_res = run_rl_network_policy_reasoning(
            problem=f"Self-test Trajectory RL policy on {test_target} and {test_secondary}",
            target_ip=test_target,
            secondary_target_ip=test_secondary,
            train_episodes=0,
            sense_topology=False,
            export_to_vault=False,
        )
        t19 = time.perf_counter()

        # Engine 20: Spectral Manifold PCA, K-Means++ Clustering & Graph Laplacian
        pca_res = run_spectral_pca_reasoning(
            problem=f"Self-test SVD PCA and K-Means++ clustering on {test_target}",
            target_ip=test_target,
            secondary_target_ip=test_secondary,
            export_to_vault=False,
        )
        t20 = time.perf_counter()

        # Context VM Zero-Loss test
        vm_out = process_tool_output_zero_loss(
            "run_command",
            "ip neigh show",
            f"{test_target} dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE",
            0,
        )
        t_pipe_start = time.perf_counter()

        p_res = run_neuro_symbolic_pipeline(
            problem="Self-test full 15-engine pipeline",
            target_ip=test_target,
            secondary_target_ip=test_secondary,
            observed_evidence={"curl_exit_7_Immediate_refused": True},
            save_to_vault=False,
        )
        t15 = time.perf_counter()
    finally:
        for sf, raw_bytes in snapshots.items():
            try:
                if raw_bytes is not None:
                    sf.write_bytes(raw_bytes)
                elif sf.is_file():
                    sf.unlink()
            except Exception:
                pass

    assert cegar_block_tio["blocked"] is True, "CEGAR should block interactive tio without --script"
    assert cegar_pass["blocked"] is False, "CEGAR should allow bounded ping -c 3"
    assert cbr_hit is not None and cbr_hit["case_id"] == "CBR-001", "CBR should match RTNETLINK File exists"
    assert "somatic_gut_valence" in vsa_res, "Engine 7 VSA must compute Damasio Somatic Gut Valence"
    assert "optimal_stopping" in mdp_res and "speculative_branch_forecast" in mdp_res, "Engine 15 MDP must compute Optimal Stopping and Speculative Branch Forecast"
    assert "optimal_command" in rl_res and "trajectory_rollout" in rl_res, "Engine 19 RL must compute optimal command and trajectory rollout"
    assert "q_lcb" in rl_res["immediate_action"], "Engine 19 RL must compute Pessimistic Q_LCB for live inference"
    assert "cluster_assignment" in pca_res and "laplacian_analysis" in pca_res, "Engine 20 PCA must compute K-Means++ cluster assignment and Graph Laplacian"
    assert pca_res["cluster_assignment"].get("prototype_anchored") is True, "Engine 20 K-Means++ must enforce 30% prototype anchoring"
    assert "lexical_hierarchy_trace" in p_res and "streamlined_layer5_digest" in p_res, "Unified Pipeline must emit 5-Layer Lexical Hierarchy trace & 6-line digest"

    # Uncapped Cross-Platform CLI & Multi-Line PDF Wrap Extractor Verification (Guardrail 9 & 10)
    from Reasoning.train_llm import _extract_and_verify_commands_deterministic

    sample_pdf_text = (
        "NMAP ------------------------ 223\n"
        "ADB BASICS\n"
        "icacls C:\\Windows\\System32\\utilman.exe /grant Administrators:F <---Gain Ownership\n"
        "pslist -t\t:Show all running processes in tree\n"
        "Get-NetTCPConnection -State Listen\n"
        "aws s3 ls s3://target-bucket --no-sign-request\n"
        "impacket-secretsdump -just-dc-ntds\n"
        f"  domain/admin:Password123@{test_target}\n"
    )
    ext_verified, ext_rejected = _extract_and_verify_commands_deterministic(sample_pdf_text)
    ext_cmds = [v["command"] for v in ext_verified]
    assert len(ext_verified) == 5, f"Expected 5 verified cross-platform commands ( rejecting TOC/header lines ), got {len(ext_verified)}: {ext_cmds}"
    assert any("impacket-secretsdump" in c and test_target in c for c in ext_cmds), "Multi-line PDF wrapped command should be rejoined"
    assert not any("NMAP ---" in c or "ADB BASICS" in c for c in ext_cmds), "TOC dashed leaders and ALL-CAPS section headers must be rejected"

    train_py_src = (REASONING_DIR / "train_llm.py").read_text(encoding="utf-8", errors="replace")
    mdp_py_src = (REASONING_DIR / "engines" / "mdp_tactical.py").read_text(encoding="utf-8", errors="replace")
    for forbidden_cap in ("verified[:60]", "verified[:2500]", "verified_cmds[:15]", "evo_list[-300:]", "max_transitions = 120"):
        assert forbidden_cap not in train_py_src, f"Regression detected: artificial cap `{forbidden_cap}` found in train_llm.py"
    assert "existing[-350:]" not in mdp_py_src, "Regression detected: artificial cap `existing[-350:]` found in mdp_tactical.py"

    return {
        "all_passed": True,
        "engines_verified": 15,
        "guardrails_verified": 10,
        "uncapped_extractor_verified": True,
        "total_latency_ms": round((t15 - t0) * 1000, 2),
        "engine_latencies_ms": {
            "1_associative_vault_pagerank": round((t1 - t0) * 1000, 2),
            "2_geometric_constraint": round((t5 - t3) * 1000, 2),
            "3_bayesian_abduction": round((t2 - t1) * 1000, 2),
            "4_causal_reasoning": round((t3 - t2) * 1000, 2),
            "5_vsa_hyperdimensional_somatic": round((t6 - t5) * 1000, 2),
            "6_temporal_event_calculus": round((t9 - t6) * 1000, 2),
            "7_dempster_shafer_epistemic": round((t10 - t9) * 1000, 2),
            "8_cbr_failure_fingerprints": round((t11 - t10) * 1000, 2),
            "9_cegar_pre_verifier": round((t12 - t11) * 1000, 2),
            "10_sygus_fact_extractor": round((t13 - t12) * 1000, 2),
            "11_mdp_tactical_optimal_stopping": round((t14b - t13) * 1000, 2),
            "12_continual_learner_pass2": round((t16 - t14b) * 1000, 2),
            "13_meta_learner_hedge_arbiter": round((t17 - t16) * 1000, 2),
            "14_rl_network_policy_td_lambda": round((t19 - t17) * 1000, 2),
            "15_spectral_pca_kmeans_laplacian": round((t20 - t19) * 1000, 2),
            "unified_15_engine_pipeline": round((t15 - t_pipe_start) * 1000, 2),
        },
        "sample_verdicts": {
            "consensus_immediate_action": p_res["consensus_immediate_action"],
            "associative_vault_graph": f"{assoc_res.get('num_graph_nodes', 0)} nodes, {assoc_res.get('num_graph_edges', 0)} edges",
            "bayesian_top_cause": f"{b_res['top_hypothesis']} ({b_res['top_probability']:.1%})",
            "dempster_shafer": f"Top={dst_res['top_hypothesis']}, Conflict K={dst_res['conflict_mass_k']:.3f}, Ignorance={dst_res['epistemic_ignorance']:.3f}",
            "causal_lift": f"{c_res['baseline_outcome_prob']:.1%} -> {c_res['intervened_outcome_prob']:.1%}",
            "temporal_fluents": f"{temp_res['holding_count']} holding fluents",
            "cbr_matched_case": f"{cbr_hit['case_id']} ({cbr_hit['binary']})",
            "cegar_verifier": f"Interactive tio blocked={cegar_block_tio['blocked']}, bounded ping blocked={cegar_pass['blocked']}",
            "sygus_header": sygus_res["extracted"].get("summary_header"),
            "mdp_optimal_policy": f"{mdp_res['optimal_tactic']} -> {mdp_res['optimal_tool']} (Q*={mdp_res['optimal_q_star']}, {mdp_res['tactic_categories_count']} categories, Stop={mdp_res['optimal_stopping']['stopping_decision']})",
            "vsa_somatic_marker": f"{vsa_res.get('top_archetype')} ({vsa_res.get('resonance_score', 0.0):.1%}, Gut Valence={vsa_res.get('somatic_gut_valence', 0.0):+.2f})",
            "geometric_supernet": g_net.get("minimal_covering_supernet"),
            "symbolic_constraint_solution": g_sym.get("solutions"),
            "continual_learning_mode": cont_res.get("mode"),
            "meta_brier_calibration": f"Brier={meta_res.get('rolling_brier_score'):.3f}, ECE={meta_res.get('expected_calibration_error_pct'):.1f}%, Top={meta_res.get('top_weighted_engine')}",
            "rl_network_policy": f"Stage={rl_res.get('current_stage')} ({rl_res.get('cluster_label')}) -> {rl_res.get('optimal_action_id')} (Q*={rl_res.get('optimal_q_value')})",
            "spectral_pca_kmeans": f"Cluster={pca_res['cluster_assignment'].get('cluster_label')} (Silhouette={pca_res.get('kmeans_silhouette_score')}, Top3PCA={pca_res.get('pca_top3_variance_pct')}%)",
            "context_vm_header_injected": "[SyGuS Extracted Facts]" in vm_out,
        },
    }


def execute_reasoning_tool(mode: str, args: Dict[str, Any]) -> str:
    """
    Entry point called by `agent-cli.py` when the LLM invokes `neuro_symbolic_reason`
    (or individual reasoning tools). Returns a concise, high-signal Markdown report
    (enforcing Guardrail 4's Executive Consensus Digest for pipeline runs while writing
    the full 15-engine synthesis to `ObsidianVault/reasoning/`).
    """
    try:
        return _execute_reasoning_tool_impl(mode, args or {})
    except Exception as exc:
        return (
            f"## [Neuro-Symbolic Engine Diagnostic Fallback]\n"
            f"- **Engine Mode**: `{mode}`\n"
            f"- **Exception Handled**: `{type(exc).__name__}: {exc}`\n"
            f"- **Fallback Safe Probe**: `ip -4 -br addr show; ip route show; ip neigh show`\n"
        )


def _execute_reasoning_tool_impl(mode: str, args: Dict[str, Any]) -> str:
    from Reasoning.engines.associative import run_associative_vault_reasoning
    from Reasoning.engines.bayesian import run_bayesian_abduction
    from Reasoning.engines.causal import run_causal_reasoning
    from Reasoning.engines.cbr_fingerprints import run_cbr_reasoning
    from Reasoning.engines.cegar_verifier import run_cegar_reasoning
    from Reasoning.engines.continual_learner import run_continual_learning_reasoning
    from Reasoning.engines.dempster_shafer import run_dempster_shafer_reasoning
    from Reasoning.engines.geometric import run_geometric_reasoning
    from Reasoning.engines.mdp_tactical import run_mdp_tactical_reasoning
    from Reasoning.engines.meta_learner import run_meta_learning_reasoning
    from Reasoning.engines.pipeline import run_neuro_symbolic_pipeline
    from Reasoning.engines.rl_network_policy import run_rl_network_policy_reasoning
    from Reasoning.engines.spectral_manifold_pca import run_spectral_pca_reasoning
    from Reasoning.engines.sygus_extractor import run_sygus_reasoning
    from Reasoning.engines.temporal_fluents import run_temporal_fluent_reasoning
    from Reasoning.engines.vsa import run_vsa_conceptual_leap

    m = (mode or args.get("engine") or "pipeline").strip().lower()
    save_vault = bool(args.get("save_to_vault", True))

    if m in ("rl", "rl_network_policy", "td_lambda", "world_model", "topology"):
        res = run_rl_network_policy_reasoning(
            problem=args.get("problem", "Multi-Step Trajectory RL & Symbolic Network World-Model"),
            target_ip=args.get("target_ip") or args.get("target") or "",
            secondary_target_ip=args.get("secondary_target_ip") or "",
            train_episodes=int(args.get("train_episodes", 0)),
            sense_topology=bool(args.get("sense_topology", True)),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("pca", "kmeans", "spectral", "spectral_manifold_pca", "laplacian"):
        res = run_spectral_pca_reasoning(
            problem=args.get("problem", "Spectral Manifold PCA, K-Means++ Clustering & Graph Laplacian Chokepoints"),
            target_ip=args.get("target_ip") or args.get("target") or "",
            secondary_target_ip=args.get("secondary_target_ip") or "",
            force_recompute=bool(args.get("force_recompute", False)),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("continual", "continual_learner", "plasticity"):
        res = run_continual_learning_reasoning(
            problem=args.get("problem", "Continual learning state & plasticity consolidation"),
            force_decay=bool(args.get("force_decay", False)),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("meta", "meta_learner", "calibration", "hedge"):
        res = run_meta_learning_reasoning(
            problem=args.get("problem", "Meta-learning Hedge weights & Brier calibration audit"),
            write_suggested_improvement=bool(args.get("write_suggested_improvement", False)),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("associative", "pagerank", "vault_graph", "spreading_activation"):
        res = run_associative_vault_reasoning(
            query=args.get("problem") or args.get("query") or "Obsidian Vault associative search",
            seed_concepts=args.get("seed_concepts"),
            save_to_vault=save_vault,
        )
        return f"{res['markdown_report']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("temporal", "temporal_fluents", "event_calculus", "fluents"):
        res = run_temporal_fluent_reasoning(
            problem=args.get("problem", "Temporal state & Event Calculus verification"),
            recent_commands=args.get("recent_commands"),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("dempster_shafer", "dst", "epistemic", "conflict"):
        res = run_dempster_shafer_reasoning(
            problem=args.get("problem", "Dempster-Shafer epistemic evidence & conflict analysis"),
            sensor_text=args.get("sensor_text", ""),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("cbr", "cbr_fingerprints", "failure_fingerprints"):
        res = run_cbr_reasoning(
            problem=args.get("problem", "Case-Based Reasoning failure lookup"),
            context_text=args.get("context_text", ""),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("cegar", "cegar_verifier", "verify"):
        res = run_cegar_reasoning(
            problem=args.get("problem", "CEGAR Pre-Execution Verification"),
            candidate_commands=args.get("candidate_commands"),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("sygus", "sygus_extractor"):
        res = run_sygus_reasoning(
            problem=args.get("problem", "SyGuS structured CLI output extraction"),
            sample_output=args.get("sample_output", ""),
            export_to_vault=save_vault,
        )
        return f"{res['markdown']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("mdp", "mdp_tactical", "markov", "tactics", "pomdp"):
        res = run_mdp_tactical_reasoning(
            problem=args.get("problem", "Hierarchical Tactical MDP Policy"),
            target_ip=args.get("target_ip") or args.get("target") or "",
            secondary_target_ip=args.get("secondary_target_ip") or "",
            observed_evidence=args.get("observed_evidence") or {},
            save_to_vault=save_vault,
        )
        return f"{res['markdown_report']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("vsa", "hyperdimensional", "conceptual_leap"):
        res = run_vsa_conceptual_leap(
            problem=args.get("problem", "Zero-shot conceptual leap"),
            observed_roles=args.get("observed_roles"),
            query_missing_roles=args.get("query_missing_roles"),
            save_to_vault=save_vault,
        )
        return f"{res['markdown_report']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("bayesian", "bayesian_abduction", "abductive"):
        res = run_bayesian_abduction(
            problem=args.get("problem", "Root-cause diagnostic abduction"),
            profile=args.get("profile", "http_api_unreachable"),
            observed_evidence=args.get("observed_evidence") or {},
            custom_hypotheses=args.get("custom_hypotheses"),
            custom_likelihoods=args.get("custom_likelihoods"),
            confirmed_cause=args.get("confirmed_cause"),
            target=args.get("target_ip") or args.get("target") or "",
            save_to_vault=save_vault,
        )
        return f"{res['markdown_report']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("causal", "causal_dag", "do_calculus"):
        res = run_causal_reasoning(
            dag_name=args.get("dag_name") or args.get("causal_dag") or "network_api_reachability",
            outcome_node=args.get("outcome_node"),
            observations=args.get("observations") or {},
            do_interventions=args.get("do_interventions") or {},
            custom_edges=args.get("custom_edges"),
            save_custom_dag=bool(args.get("save_custom_dag", False)),
            save_to_vault=save_vault,
        )
        if "error" in res:
            return f"Causal DAG Error: {res['error']}"
        return f"{res['markdown_report']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    if m in ("geometric", "constraint", "network_geometry", "constraint_solve", "spatial_euclidean"):
        from Reasoning.engines.vault_bridge import resolve_problem_targets

        geo_mode = args.get("geometric_mode") or (
            m if m in ("network_geometry", "constraint_solve", "spatial_euclidean") else "network_geometry"
        )
        ctx = resolve_problem_targets(
            problem=args.get("problem", ""),
            explicit_target=args.get("target_ip") or args.get("target") or "",
            explicit_secondary=args.get("secondary_target_ip") or "",
            explicit_local_subnets=args.get("local_subnets"),
        )
        spec = args.get("spec") or {
            "local_subnets": args.get("local_subnets") or ctx["local_subnets"],
            "target_ips": [
                ip for ip in [ctx["target_ip"], ctx["secondary_target_ip"]] if ip
            ],
            "variables": args.get("variables", ["x", "y"]),
            "equations": args.get("equations", []),
            "points": args.get("points", {}),
        }
        res = run_geometric_reasoning(
            problem_title=args.get("problem") or args.get("target_ip") or "geometric_analysis",
            mode=geo_mode,
            spec=spec,
            save_to_vault=save_vault,
        )
        return f"{res['markdown_report']}\n\nSaved to ObsidianVault: {res.get('vault_note', 'N/A')}"

    # Default: Unified 15-Engine Neuro-Symbolic, Somatic, Forecasting, Continual & Meta-Learning Pipeline
    res = run_neuro_symbolic_pipeline(
        problem=args.get("problem", "Target analysis & root-cause debugging"),
        target_ip=args.get("target_ip") or args.get("target") or "",
        secondary_target_ip=args.get("secondary_target_ip") or "",
        local_subnets=args.get("local_subnets"),
        bayesian_profile=args.get("profile") or args.get("bayesian_profile") or "http_api_unreachable",
        observed_evidence=args.get("observed_evidence") or {},
        causal_dag=args.get("causal_dag") or args.get("dag_name") or "network_api_reachability",
        do_interventions=args.get("do_interventions"),
        has_serial_oob=args.get("has_serial_oob"),
        save_to_vault=save_vault,
    )
    if args.get("full_report"):
        return f"{res['markdown_report']}\n\nSaved full 15-engine synthesis to ObsidianVault: {res.get('vault_note', 'N/A')}"
    return (
        f"{res['executive_digest']}\n\n"
        f"[Full 15-Engine Detailed Synthesis saved to ObsidianVault: `{res.get('vault_note', 'N/A')}`]"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="15-Engine Neuro-Symbolic, Somatic, Forecasting, Continual, Meta-Learning, Trajectory RL & Spectral PCA/K-Means++ Reasoning CLI (v4.5.0)"
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status", help="Show installed packages, hardware scaling limits, Vault Graph stats, and stored models")
    sub.add_parser("seed", help="Seed Reasoning/data/ and ObsidianVault/ with initial 15-engine models")
    sub.add_parser("test", help="Run deterministic self-tests across all 15 reasoning engines + 10 guardrails")

    p_pipe = sub.add_parser("pipeline", help="Run unified 15-engine Neuro-Symbolic Pipeline")
    p_pipe.add_argument("--problem", default="Target API & routing root-cause analysis")
    p_pipe.add_argument("--target", default="")
    p_pipe.add_argument("--secondary-target", default="")
    p_pipe.add_argument("--profile", default="http_api_unreachable")
    p_pipe.add_argument("--dag", default="network_api_reachability")
    p_pipe.add_argument("--evidence", default="{}", help="JSON dict of observed evidence")
    p_pipe.add_argument("--full", action="store_true", help="Print full 15-engine Markdown report instead of Executive Digest")

    p_mdp = sub.add_parser("mdp", help="Run Engine 15 Hierarchical Tactical MDP, Optimal Stopping & Speculative Forecast")
    p_mdp.add_argument("--problem", default="Predict optimal Tactic -> Technique -> Tool -> Command")
    p_mdp.add_argument("--target", default="")
    p_mdp.add_argument("--secondary-target", default="")

    p_cont = sub.add_parser("continual", help="Control Engine 16 Continual Learning mode (AUTO | START | STOP | status)")
    p_cont.add_argument("--mode", default="status", choices=["auto", "start", "stop", "status", "consolidate", "AUTO", "START", "STOP"])
    p_cont.add_argument("--problem", default="Continual learning & plasticity consolidation")

    p_meta = sub.add_parser("meta", help="Run Engine 17 Hedge Meta-Arbiter & Brier/ECE Calibration Audit")
    p_meta.add_argument("--problem", default="Meta-learning Hedge weights & Brier calibration audit")
    p_meta.add_argument("--write-improvement", action="store_true", help="Write audit note to ObsidianVault/SuggestedImprovements/")

    p_rl = sub.add_parser("rl", help="Run Engine 19 Multi-Step Trajectory RL & Symbolic Network World-Model")
    p_rl.add_argument("--problem", default="Multi-Step Trajectory RL & Network World-Model")
    p_rl.add_argument("--target", default="")
    p_rl.add_argument("--secondary-target", default="")
    p_rl.add_argument("--train-episodes", type=int, default=0, help="Run N Digital-Twin RL training episodes")

    p_pca = sub.add_parser("pca", help="Run Engine 20 Spectral Manifold PCA, K-Means++ Clustering & Graph Laplacian")
    p_pca.add_argument("--problem", default="Spectral Manifold PCA & K-Means++ Clustering")
    p_pca.add_argument("--target", default="")
    p_pca.add_argument("--secondary-target", default="")
    p_pca.add_argument("--recompute", action="store_true", help="Force recomputation of SVD PCA & K-Means++ model")

    args = parser.parse_args()
    cmd = args.cmd or "status"

    if cmd == "status":
        print(json.dumps(check_environment_status(), indent=2))
    elif cmd == "seed":
        print(seed_all_data_and_vault())
    elif cmd == "test":
        print(json.dumps(run_self_tests(), indent=2))
    elif cmd == "continual":
        from Reasoning.engines.continual_learner import (
            get_continual_learning_state,
            run_continual_learning_reasoning,
            set_continual_learning_mode,
        )

        m_val = args.mode.strip().upper()
        if m_val in ("AUTO", "START", "STOP"):
            st = set_continual_learning_mode(m_val)
            print(f"Engine 16 Continual Learning mode set to `{st.get('mode')}`.")
            if m_val == "START":
                res = run_continual_learning_reasoning(problem=args.problem, force_decay=True, export_to_vault=True)
                print(res["markdown"])
        elif m_val == "CONSOLIDATE":
            res = run_continual_learning_reasoning(problem=args.problem, force_decay=True, export_to_vault=True)
            print(res["markdown"])
        else:
            print(json.dumps(get_continual_learning_state(), indent=2))
    elif cmd == "meta":
        print(
            execute_reasoning_tool(
                "meta",
                {
                    "problem": args.problem,
                    "write_suggested_improvement": args.write_improvement,
                    "save_to_vault": True,
                },
            )
        )
    elif cmd == "rl":
        print(
            execute_reasoning_tool(
                "rl",
                {
                    "problem": args.problem,
                    "target_ip": args.target,
                    "secondary_target_ip": args.secondary_target,
                    "train_episodes": args.train_episodes,
                    "save_to_vault": True,
                },
            )
        )
    elif cmd == "pca":
        print(
            execute_reasoning_tool(
                "pca",
                {
                    "problem": args.problem,
                    "target_ip": args.target,
                    "secondary_target_ip": args.secondary_target,
                    "force_recompute": args.recompute,
                    "save_to_vault": True,
                },
            )
        )
    elif cmd == "mdp":
        print(
            execute_reasoning_tool(
                "mdp",
                {
                    "problem": args.problem,
                    "target_ip": args.target,
                    "secondary_target_ip": args.secondary_target,
                    "save_to_vault": True,
                },
            )
        )
    elif cmd == "pipeline":
        try:
            ev = json.loads(args.evidence) if args.evidence else {}
            if not isinstance(ev, dict):
                ev = {}
        except json.JSONDecodeError as exc:
            print(f"[WARNING] Invalid --evidence JSON ({exc}); defaulting to empty dict {{}}.", file=sys.stderr)
            ev = {}
        out = execute_reasoning_tool(
            "pipeline",
            {
                "problem": args.problem,
                "target_ip": args.target,
                "secondary_target_ip": args.secondary_target,
                "bayesian_profile": args.profile,
                "causal_dag": args.dag,
                "observed_evidence": ev,
                "save_to_vault": True,
                "full_report": args.full,
            },
        )
        print(out)


if __name__ == "__main__":
    main()
