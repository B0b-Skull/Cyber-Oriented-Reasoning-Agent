"""
Engine 16: Online Continual Reasoning & Learning Loop Controller (`continual_learner.py`)
=========================================================================================
Ported and adapted from the C.O.R.A. Cognitive Architecture v4.2.0 to `CORA`:
1. **3-Mode User Control Switch (`AUTO` | `START` | `STOP`)** persisted in
   `Reasoning/data/continual_learning_state.json`.
2. **Real-Time Post-Command Experience Plasticity (`record_live_command_experience`)**:
   - Updates Engine 15 Dirichlet MDP transition counts `alpha(s, a, s')`.
   - Updates Engine 7 (`32,768-D` VSA) Damasio Somatic Marker Valence (`somatic_markers.json`).
   - **Autonomous CBR Failure -> Fix Discovery**: Tracks the most recent failed command in working
     memory; when a subsequent command succeeds (`exit_code == 0`), automatically synthesizes a
     reusable Case-Based Reasoning fingerprint in `Reasoning/data/learned_cbr_cases.json`.
3. **Pass-2 Recursive Reasoning Refinement (`run_iterative_reasoning_refinement`)**:
   - When Pass 1 of `run_neuro_symbolic_pipeline` encounters Dempster-Shafer sensor conflict
     (`K >= 0.35`), a Somatic Trap Warning (`valence <= -0.25`), or an Optimal Stopping Pivot signal,
     automatically runs Pass-2 counterexample refinement to reconcile the conflict before Qwen acts.
4. **Dirichlet Exponential Forgetting (`apply_dirichlet_forgetting_factor`, `lambda = 0.96`)**:
   - Prevents historical transition counts and Bayesian priors from ossifying across changing environments.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import time
from typing import Any, Dict, List, Optional

from .mdp_tactical import (
    MDP_STORE_FILE,
    _MDP_STORE_RAM_CACHE,
    _split_unquoted_segments,
    flush_mdp_store_if_dirty,
    record_mdp_transition_outcome,
)
from .vault_bridge import (
    DATA_DIR,
    ensure_directories,
    get_hardware_reasoning_limits,
    load_json_state,
    render_command_template,
    resolve_problem_targets,
    save_json_state,
    write_reasoning_note,
)
from .vsa import record_somatic_valence_marker

CONTINUAL_STATE_FILE = os.path.join(str(DATA_DIR), "continual_learning_state.json")
LEARNED_CBR_FILE = os.path.join(str(DATA_DIR), "learned_cbr_cases.json")
BAYESIAN_PROFILES_FILE = os.path.join(str(DATA_DIR), "bayesian_profiles.json")

VALID_MODES = ("AUTO", "START", "STOP")

_IPV4_SUB_RE = re.compile(
    r"\b(?!127\.0\.0\.1\b|0\.0\.0\.0\b|255\.255\.255\.\d+\b)"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b"
)


def _parameterize_tactical_template(text: str) -> str:
    """
    Abstract concrete target IPs (`-> <TARGET_IP>`) and local host/project paths (`-> $PROJECT_DIR`)
    before persisting online learned CBR rules so long-term tactical memory grows in reusable tactics
    without ever storing dirty local network IPs or host paths.
    """
    if not text:
        return ""
    s = _IPV4_SUB_RE.sub("<TARGET_IP>", text)
    s = re.sub(r"/home/[^/\s'\"]+/Projects/CORA/Projects/[^/\s'\"]+", "$PROJECT_DIR", s)
    s = re.sub(r"/home/[^/\s'\"]+", "~", s)
    return s


def get_continual_learning_state() -> Dict[str, Any]:
    """Load the persistent Continual & Meta-Learning controller state."""
    ensure_directories()
    hw = get_hardware_reasoning_limits()
    default_state: Dict[str, Any] = {
        "mode": "AUTO",
        "hardware_tier": hw.get("tier", "HIGH_PERFORMANCE"),
        "continual_pass2_max_candidates": int(hw.get("continual_pass2_max_candidates", 8)),
        "continual_audit_window": int(hw.get("continual_audit_window", 250)),
        "is_currently_running": False,
        "last_fast_refinement_utc": None,
        "last_consolidation_utc": None,
        "last_meta_audit_utc": None,
        "last_ablation_sweep_utc": None,
        "online_commands_observed": 0,
        "online_cbr_rules_learned": 0,
        "consolidation_cycles_completed": 0,
        "dirichlet_forgetting_lambda": 0.96,
        "pending_failure_context": None,
        "memory_tiers_status": {
            "1_working_memory": "ACTIVE (ZeroLossContextVM + SpeculativeLookaheadCache < 1 ms)",
            "2_episodic_memory": "ACTIVE (temporal_fluents + shadow_archive + ObsidianVault/reasoning/)",
            "3_semantic_memory": "ACTIVE (32,768-D VSA Somatic Markers + FCA Lattices + Bipartite Graph)",
            "4_procedural_memory": "ACTIVE (H-MDP 5,039 Transitions + Clingo ASP + CBR Library)",
            "5_experimental_memory": "ACTIVE (ablation_ledger.json + SuggestedImprovements/)",
        },
    }
    loaded = load_json_state(CONTINUAL_STATE_FILE, {})
    if isinstance(loaded, dict) and loaded:
        default_state.update(loaded)
    return default_state


def save_continual_learning_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """Persist the Continual & Meta-Learning controller state atomically."""
    ensure_directories()
    state["updated_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save_json_state(CONTINUAL_STATE_FILE, state)
    return state


def set_continual_learning_mode(mode: str) -> Dict[str, Any]:
    """Set the 3-Mode Continual Learning switch (`AUTO` | `START` | `STOP`)."""
    clean_mode = str(mode or "AUTO").strip().upper()
    if clean_mode not in VALID_MODES:
        clean_mode = "AUTO"
    st = get_continual_learning_state()
    st["mode"] = clean_mode
    return save_continual_learning_state(st)


def apply_dirichlet_forgetting_factor(forgetting_lambda: float = 0.96) -> Dict[str, Any]:
    """
    Applies exponential forgetting factor `lambda` in `[0.88, 0.999]` to `mdp_transitions.json`
    so ancient transition counts do not over-saturate and block adaptation to new network/system states.
    """
    lam = max(0.88, min(0.999, float(forgetting_lambda or 0.96)))
    mdp_updated = 0
    flush_mdp_store_if_dirty()
    if os.path.exists(MDP_STORE_FILE):
        try:
            mdp_data = load_json_state(str(MDP_STORE_FILE), {})
            transitions = mdp_data.get("transitions", [])
            if isinstance(transitions, list):
                for tr in transitions:
                    if isinstance(tr, dict):
                        tr["alpha_success"] = round(max(1.5, float(tr.get("alpha_success", 5.0)) * lam), 3)
                        tr["alpha_fail"] = round(max(1.0, float(tr.get("alpha_fail", 1.0)) * lam), 3)
                        mdp_updated += 1
                mdp_data["last_forgetting_decay_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
                save_json_state(str(MDP_STORE_FILE), mdp_data)
                _MDP_STORE_RAM_CACHE["data"] = mdp_data
                _MDP_STORE_RAM_CACHE["mtime"] = os.path.getmtime(MDP_STORE_FILE)
                _MDP_STORE_RAM_CACHE["dirty_count"] = 0
        except Exception:
            pass
    return {
        "lambda_applied": lam,
        "mdp_transitions_decayed": mdp_updated,
    }


_NETWORK_OR_PROBE_BINS = {
    "curl", "wget", "ping", "nc", "ncat", "netcat", "socat", "nmap", "masscan",
    "ssh", "scp", "sftp", "tio", "minicom", "arping", "traceroute", "tracepath",
    "tracert", "ip", "ifconfig", "ipconfig", "route", "iptables", "ip6tables",
    "nft", "netsh", "test-netconnection", "tnc", "invoke-webrequest", "iwr",
    "invoke-restmethod", "irm", "openssl", "sqlmap", "nikto", "gobuster", "ffuf",
}
_LOCAL_READER_BINS = {
    "cat", "head", "tail", "grep", "egrep", "fgrep", "ls", "dir", "find",
    "locate", "stat", "file", "wc", "pwd", "cd", "echo", "printf", "awk", "sed",
}


def _extract_effective_binary(cmd_clean: str) -> str:
    """Extract the primary actionable binary from a command (skipping `cd ... &&`, `sudo`, `env`, `echo ...;`)."""
    segments = _split_unquoted_segments(cmd_clean)
    chosen_bin = "sh"
    for idx, seg in enumerate(segments):
        tokens = seg.split()
        while tokens and (tokens[0] in ("sudo", "env", "time", "timeout", "nohup") or "=" in tokens[0]):
            tokens.pop(0)
        if not tokens:
            continue
        b = tokens[0].rsplit("/", 1)[-1].lower()
        if b in ("cd", "echo", "printf", "export", "true") and len(segments) > 1 and idx < len(segments) - 1:
            chosen_bin = b
            continue
        return b
    return chosen_bin


def record_live_command_experience(
    command: str,
    exit_code: int,
    output_text: str,
    problem_context: str = "",
) -> Dict[str, Any]:
    """
    Fast Continual Plasticity Hook (called automatically after every tool execution):
    1. Updates Engine 15 Dirichlet MDP transition counts (`alpha_success` / `alpha_fail`).
    2. Updates Engine 7 Somatic Marker Valence (`+0.65` on clean breakthrough, `-0.70` on failure/timeout).
    3. Auto-synthesizes a new Case-Based Reasoning (CBR) failure->fix rule whenever a failed command
       is followed by a successful remediation command.
    """
    st = get_continual_learning_state()
    if st.get("mode") == "STOP":
        return {"skipped": True, "reason": "Continual learning mode is STOP"}

    cmd_clean = (command or "").strip()
    if not cmd_clean:
        return {"skipped": True, "reason": "Empty command"}

    first_bin = _extract_effective_binary(cmd_clean)
    cmd_low = cmd_clean.lower()
    is_network_probe = first_bin in _NETWORK_OR_PROBE_BINS or any(
        re.search(rf"\b{re.escape(nb)}\b", cmd_low) for nb in ("curl", "wget", "ping", "nmap", "tio", "nc", "socat", "ssh")
    )

    from .meta_learner import analyze_and_record_channel_telemetry

    channel_telemetry = analyze_and_record_channel_telemetry(cmd_clean, exit_code, output_text)
    has_serial_drop = bool(channel_telemetry.get("console_drop_detected", False))

    succeeded = exit_code == 0
    out_low = (output_text or "").lower()
    # Only treat stdout timeout/refused strings as command failure when running a network/OOB probe,
    # NEVER when reading local text/log files with `cat`, `head`, `grep`, `ls`, or `find`.
    has_timeout_or_refused = is_network_probe and any(
        k in out_low for k in ("timed out", "timeout", "100% packet loss", "connection refused", "network is unreachable", "no route to host")
    )
    effective_success = succeeded and not has_timeout_or_refused and not has_serial_drop

    # 1. Update MDP Dirichlet counts (only for tactical/network commands or non-trivial operations)
    mdp_upd = None
    if is_network_probe or first_bin not in _LOCAL_READER_BINS:
        mdp_upd = record_mdp_transition_outcome(
            command=cmd_clean,
            succeeded=effective_success,
            context_text=f"{problem_context} {output_text[:300]}",
        )

    # 2. Update Somatic Marker Valence (only for tactical/network probes, never for local file/dir readers)
    somatic_upd = {}
    if is_network_probe or first_bin not in _LOCAL_READER_BINS:
        if has_serial_drop:
            valence_delta = -0.80
            symptom_tag = "serial_console_drop"
            somatic_reason = "serial_rx_zero_yield_or_drop"
        else:
            valence_delta = 0.65 if effective_success else (-0.75 if has_timeout_or_refused else -0.45)
            symptom_tag = (
                "l2_l3_routing"
                if bool(re.search(r"\b(?:ip\s+route|route|ip\s+neigh|arp|ping|arping|traceroute)\b", cmd_low))
                else "general"
            )
            somatic_reason = f"exit={exit_code}"
        somatic_upd = record_somatic_valence_marker(
            command=cmd_clean,
            succeeded=effective_success,
            valence_delta=valence_delta,
            symptom_tag=symptom_tag,
            reason=somatic_reason,
        )

    # 3. Autonomous Failure -> Fix CBR Discovery
    learned_cbr = None
    pending_fail = st.get("pending_failure_context")

    if not effective_success and first_bin not in _LOCAL_READER_BINS:
        # Record parameterized failure context for potential subsequent fix pairing
        if has_serial_drop:
            err_snippet = "Serial console dropped or returned 0 bytes (Command completed with exit code 0) under command burst"
        else:
            err_lines = [
                ln.strip()
                for ln in (output_text or "").splitlines()
                if ln.strip() and not re.match(r"^\(Command completed with exit code \d+\)$", ln.strip(), re.I)
            ]
            err_snippet = _parameterize_tactical_template(err_lines[-1][:120] if err_lines else f"exit code {exit_code}")
        st["pending_failure_context"] = {
            "failed_command": _parameterize_tactical_template(cmd_clean[:160]),
            "binary": first_bin,
            "exit_code": exit_code if exit_code != 0 else 1,
            "error_snippet": err_snippet,
            "steps_remaining": 4,
            "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
    elif effective_success and isinstance(pending_fail, dict) and pending_fail.get("error_snippet") and first_bin not in _LOCAL_READER_BINS:
        fail_bin = str(pending_fail.get("binary", "")).lower()
        same_or_related_domain = bool(
            first_bin == fail_bin
            or (first_bin in _NETWORK_OR_PROBE_BINS and fail_bin in _NETWORK_OR_PROBE_BINS)
        )
        err_snip = _parameterize_tactical_template(str(pending_fail.get("error_snippet", "")).strip())
        param_cmd = _parameterize_tactical_template(cmd_clean[:180])
        if same_or_related_domain and len(err_snip) >= 6 and param_cmd != pending_fail.get("failed_command"):
            cbr_store = load_json_state(LEARNED_CBR_FILE, {"cases": []})
            cases = cbr_store.get("cases", []) if isinstance(cbr_store, dict) else []
            escaped_pat = re.escape(err_snip[:48])
            already_exists = any(
                (c.get("stderr_pattern") == escaped_pat or c.get("error_pattern") == escaped_pat)
                for c in cases
                if isinstance(c, dict)
            )
            if not already_exists:
                new_case = {
                    "case_id": f"CBR-AUTO-{len(cases) + 101:03d}",
                    "binary": str(pending_fail.get("binary", first_bin)),
                    "exit_code": int(pending_fail.get("exit_code") or 1),
                    "error_pattern": escaped_pat,
                    "stderr_pattern": escaped_pat,
                    "symptom": f"Auto-learned failure on `{pending_fail.get('binary', first_bin)}` ({err_snip[:70]})",
                    "root_cause": f"Auto-learned failure on `{pending_fail.get('failed_command', '')[:60]}` ({err_snip[:80]})",
                    "verified_fix": param_cmd,
                    "verified_remediation": param_cmd,
                    "verification_probe": param_cmd,
                    "learned_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                }
                cases.append(new_case)
                if not isinstance(cbr_store, dict):
                    cbr_store = {"cases": cases}
                else:
                    cbr_store["cases"] = cases
                save_json_state(LEARNED_CBR_FILE, cbr_store)
                learned_cbr = new_case
                st["online_cbr_rules_learned"] = int(st.get("online_cbr_rules_learned", 0)) + 1
            st["pending_failure_context"] = None
        else:
            rem = int(pending_fail.get("steps_remaining", 1)) - 1
            if rem <= 0:
                st["pending_failure_context"] = None
            else:
                pending_fail["steps_remaining"] = rem
                st["pending_failure_context"] = pending_fail

    obs_cnt = int(st.get("online_commands_observed", 0)) + 1
    st["online_commands_observed"] = obs_cnt
    # Periodic Dirichlet consolidation every 25 online commands in AUTO/START mode
    if obs_cnt % 25 == 0 and st.get("mode", "AUTO") in ("AUTO", "START"):
        apply_dirichlet_forgetting_factor(float(st.get("dirichlet_forgetting_lambda", 0.96)))
        st["consolidation_cycles_completed"] = int(st.get("consolidation_cycles_completed", 0)) + 1
        st["last_consolidation_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save_continual_learning_state(st)

    return {
        "effective_success": effective_success,
        "mdp_updated": mdp_upd,
        "somatic_updated": somatic_upd,
        "learned_cbr_case": learned_cbr,
        "channel_telemetry": channel_telemetry,
    }


def run_iterative_reasoning_refinement(
    pipeline_result: Dict[str, Any],
    problem: str,
    target_ip: str = "",
) -> Dict[str, Any]:
    """
    Fast Loop (Pass-2 Counterexample-Guided Recursive Refinement):
    Inspects Pass 1 of `run_neuro_symbolic_pipeline`. If any of the following hold:
      1. Dempster-Shafer inter-sensor conflict `K >= 0.35` (e.g., ARP reachable vs ICMP/TCP drop),
      2. Damasio Somatic Gut Valence `<= -0.25` (`SOMATIC_RABBIT_HOLE_TRAP_WARNING`),
      3. Optimal Stopping Decision == `PIVOT_TACTIC_IMMEDIATELY`,
    executes a Pass-2 refinement that overrides repetitive in-band retries with a conflict-resolving
    L2/OOB or no-ping (`nmap -Pn` / `Test-NetConnection` / `tio`) pivot command.
    """
    res = dict(pipeline_result or {})
    conflict_k = float(res.get("dempster_shafer_conflict_k", 0.0) or 0.0)
    somatic_v = float(res.get("somatic_gut_valence", 0.0) or 0.0)
    stopping = res.get("optimal_stopping", {}) if isinstance(res.get("optimal_stopping"), dict) else {}
    stop_dec = str(stopping.get("stopping_decision", "HOLD_OPTIMAL_TACTIC_LINE"))

    res["refinement_loop_passes"] = 1
    res["refinement_applied"] = False
    res["refinement_rationale"] = "Pass-1 consensus verified with low inter-sensor conflict."

    needs_pass2 = (conflict_k >= 0.35) or (somatic_v <= -0.25) or (stop_dec == "PIVOT_TACTIC_IMMEDIATELY")
    if not needs_pass2:
        return res

    ctx = resolve_problem_targets(problem=problem, explicit_target=target_ip)
    resolved_target = ctx["target_ip"]
    is_windows = os.name == "nt"

    res["refinement_loop_passes"] = 2
    res["refinement_applied"] = True

    # Determine the conflict-reconciling Pass-2 command
    branch_forecast = res.get("speculative_branch_forecast", {}) or {}
    fail_branch = branch_forecast.get("on_failure_branch", {}) if isinstance(branch_forecast, dict) else {}
    pivot_cmd = str(stopping.get("recommended_command") or fail_branch.get("pivot_command") or "")

    if conflict_k >= 0.35 and not pivot_cmd:
        if is_windows:
            pivot_cmd = f"arp -a {resolved_target} & powershell -NoProfile -Command \"Test-NetConnection -ComputerName {resolved_target} -Port 80 -InformationLevel Detailed\""
        else:
            pivot_cmd = f"ip neigh show {resolved_target} && nmap -Pn -sT -p 22,80,443,8080,8443 --open {resolved_target}"

    if pivot_cmd:
        pivot_cmd = render_command_template(pivot_cmd, ctx)
        res["pass1_initial_action"] = res.get("consensus_immediate_action")
        res["consensus_immediate_action"] = pivot_cmd

    reasons = []
    if conflict_k >= 0.35:
        reasons.append(f"Dempster-Shafer Conflict K={conflict_k:.2f} (L2/L3 sensor divergence)")
    if somatic_v <= -0.25:
        reasons.append(f"Somatic Gut Trap Warning ({somatic_v:+.2f})")
    if stop_dec == "PIVOT_TACTIC_IMMEDIATELY":
        reasons.append(f"Optimal Stopping V_pivot ({stopping.get('v_pivot')}) > V_continue ({stopping.get('v_continue')})")

    res["refinement_rationale"] = (
        f"Pass-2 Recursive Refinement triggered by {', '.join(reasons)} -> "
        f"Promoted conflict-reconciling probe `{res.get('consensus_immediate_action')}`."
    )

    st = get_continual_learning_state()
    st["last_fast_refinement_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save_continual_learning_state(st)
    return res


def run_continual_learning_reasoning(
    problem: str = "Consolidate online continual learning state",
    force_decay: bool = False,
    export_to_vault: bool = False,
) -> Dict[str, Any]:
    """
    Execute Engine 16: Online Continual Learning & Plasticity Status / Consolidation.
    """
    t0 = time.perf_counter()
    st = get_continual_learning_state()
    decay_res = {}
    if force_decay and st.get("mode") != "STOP":
        decay_res = apply_dirichlet_forgetting_factor(float(st.get("dirichlet_forgetting_lambda", 0.96)))
        st["consolidation_cycles_completed"] = int(st.get("consolidation_cycles_completed", 0)) + 1
        st["last_consolidation_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        save_continual_learning_state(st)

    cbr_store = load_json_state(LEARNED_CBR_FILE, {"cases": []})
    learned_cases = cbr_store.get("cases", []) if isinstance(cbr_store, dict) else []
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)

    md_lines = [
        f"### Engine 16: Online Continual Learning & Pass-2 Refinement (`{elapsed_ms} ms`)",
        f"- **Control Mode:** `{st.get('mode', 'AUTO')}` | **Dirichlet Forgetting ($\\lambda$):** `{st.get('dirichlet_forgetting_lambda', 0.96)}`",
        f"- **Online Commands Observed:** `{st.get('online_commands_observed', 0)}` | **Auto-Learned CBR Fixes:** `{len(learned_cases)}`",
        "- **5-Tier Cognitive Memory Status:**",
    ]
    for k, v in (st.get("memory_tiers_status") or {}).items():
        md_lines.append(f"  - `{k}`: {v}")
    markdown = "\n".join(md_lines)

    vault_path = None
    if export_to_vault:
        vault_path = write_reasoning_note(
            title=f"Continual Learning State - {problem[:36]}",
            engine="continual_learner",
            content_md=markdown,
            tags=["continual-learning", "plasticity", "memory-tiers"],
        )

    return {
        "engine": "continual_learner",
        "mode": st.get("mode", "AUTO"),
        "online_commands_observed": st.get("online_commands_observed", 0),
        "online_cbr_rules_learned": len(learned_cases),
        "dirichlet_forgetting_lambda": st.get("dirichlet_forgetting_lambda", 0.96),
        "decay_applied": decay_res,
        "memory_tiers_status": st.get("memory_tiers_status", {}),
        "elapsed_ms": elapsed_ms,
        "vault_note": vault_path,
        "markdown": markdown,
    }
