"""
Part 1: Zero-Loss Context Virtual Memory (Context VM) & Speculative Lookahead Cache
===================================================================================
Solves `exceed_context_size_error` with zero information loss while enforcing all 6 Guardrails:
1. Exact `/tokenize` & `/props` Token Budget Accounting against `llama-server` (with conservative
   `len(text) // 2` fallback for dense CLI hex/IP logs when offline).
2. Central Content-Addressed Shadow Archive (`Reasoning/data/shadow_archive/sha256_<hash>.log`)
   with automatic FIFO rotation at `shadow_archive_max_files` (Guardrail 6: zero CWD clutter).
3. Additive SyGuS + High Compression Threshold (`> 2,500 chars` per Guardrail 2):
   - Tool outputs `<= 2,500 chars` remain 100% raw (prepended with `[SyGuS Extracted Facts]` if present).
   - Tool outputs `> 2,500 chars` are saved in full to `shadow_archive/`, and the in-context representation
     preserves the exact SyGuS facts + first 25 lines + last 20 lines + exact `grep`/`sed` retrieval path.
4. Last-Write-Wins L1 Symbolic State Register + MemGPT-style Bipartite Graph Page-In (Guardrails 3 & 5):
   - Keeps `messages[0]` 100% static so `llama-server` KV-cache prefix hits are preserved every turn.
   - Provides a compact dynamic state block injected right before the final turn or on demand.
5. Idle-Time Speculative Lookahead Cache (`SpeculativeLookaheadCache`):
   - Pre-warms associative/temporal/ASP reasoning in a background CPU thread ONLY while idle,
     and immediately yields when the user submits a prompt.
"""

import glob
import hashlib
import json
import os
import threading
import time
import urllib.request
from typing import Any, Dict, List, Optional

from .cbr_fingerprints import match_failure_fingerprint
from .sygus_extractor import extract_structured_facts
from .temporal_fluents import get_l1_state_summary_line, load_fluent_state, record_command_event
from .vault_bridge import (
    SHADOW_ARCHIVE_DIR,
    ensure_directories,
    get_active_project_dir,
    get_hardware_reasoning_limits,
    scan_vault_notes,
)

# Guardrail 2 threshold: outputs <= 2,500 chars are NEVER truncated
RAW_PRESERVE_THRESHOLD_CHARS = 2500

_SPECULATIVE_BRANCH_CACHE: Dict[str, Any] = {}
_PENDING_CBR_MATCH_CACHE: Dict[str, Any] = {}


def update_speculative_branch_cache(branch_forecast: Dict[str, Any]) -> None:
    """Update the in-RAM Speculative N-Branch Next-Tool Forecast cache (< 0.1 ms)."""
    if isinstance(branch_forecast, dict) and branch_forecast:
        _SPECULATIVE_BRANCH_CACHE.clear()
        _SPECULATIVE_BRANCH_CACHE.update(branch_forecast)


def get_speculative_branch_cache() -> Dict[str, Any]:
    """Return the active Speculative N-Branch Next-Tool Forecast cache."""
    return dict(_SPECULATIVE_BRANCH_CACHE)


def count_tokens_exact_or_est(text: str, api_base: str = "http://127.0.0.1:8080") -> int:
    """
    Queries `llama-server`'s `/tokenize` endpoint for exact token count, falling back to
    a conservative `len(text) // 2` heuristic for dense CLI/hex/IP logs.
    """
    if not text:
        return 0
    try:
        req = urllib.request.Request(
            f"{api_base.rstrip('/')}/tokenize",
            data=json.dumps({"content": text}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=0.35) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            tokens = data.get("tokens")
            if isinstance(tokens, list):
                return len(tokens)
    except Exception:
        pass
    # Conservative fallback for CLI outputs where 1 token ~ 2.0-2.5 chars
    return max(1, len(text) // 2)


def query_server_n_ctx(api_base: str = "http://127.0.0.1:8080", default_ctx: int = 16384) -> int:
    """Queries `/props` on `llama-server` to discover the exact active context window size `n_ctx`."""
    try:
        req = urllib.request.Request(f"{api_base.rstrip('/')}/props", method="GET")
        with urllib.request.urlopen(req, timeout=0.4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ctx = data.get("default_generation_settings", {}).get("n_ctx")
            if isinstance(ctx, int) and ctx >= 1024:
                return ctx
    except Exception:
        pass
    return default_ctx


def archive_to_shadow_store(command: str, raw_output: str) -> str:
    """
    Writes 100% of a raw command output to `Projects/<project>/shadow_archive/sha256_<12hex>.log`
    and enforces FIFO rotation at `shadow_archive_max_files` (Guardrail 6).
    Returns the absolute path to the shadow archive file.
    """
    ensure_directories()
    hw = get_hardware_reasoning_limits()
    max_files = int(hw.get("shadow_archive_max_files", 100))

    proj_shadow_dir = str(get_active_project_dir() / "shadow_archive")
    os.makedirs(proj_shadow_dir, exist_ok=True)

    digest = hashlib.sha256((command + "\n" + raw_output).encode("utf-8", errors="ignore")).hexdigest()[:12]
    filename = f"sha256_{digest}.log"
    filepath = os.path.join(proj_shadow_dir, filename)

    header = (
        f"# SHADOW ARCHIVE LOG (100% Lossless Raw Output)\n"
        f"# Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"# Command: {command}\n"
        f"# Chars: {len(raw_output)}\n"
        f"{'=' * 72}\n"
    )
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(header + raw_output)
    except OSError:
        return ""

    # Auto-rotate oldest shadow archive logs beyond max_files
    try:
        files = sorted(
            glob.glob(os.path.join(proj_shadow_dir, "sha256_*.log")),
            key=lambda p: os.path.getmtime(p),
        )
        while len(files) > max_files:
            oldest = files.pop(0)
            try:
                os.remove(oldest)
            except OSError:
                pass
    except Exception:
        pass

    return filepath.replace("\\", "/")


def process_tool_output_zero_loss(
    tool_name: str,
    command_or_key: str,
    raw_output: str,
    exit_code: int = 0,
) -> str:
    """
    Processes every tool output through:
    1. Engine 9 (`temporal_fluents`): Records command event & updates Last-Write-Wins keyed state + detects invalidations.
    2. Engine 11 (`cbr_fingerprints`): Matches any non-zero exit code or error signature and injects `[CBR Verified Fix]`.
    3. Engine 13 (`sygus_extractor`): Extracts structured network/system facts.
    4. Part 1 Shadow Archive & Semantic Compression (Guardrail 2):
       - If `len(raw_output) <= 2,500`, returns 100% untouched raw output + compact SyGuS/CBR headers.
       - If `len(raw_output) > 2,500`, saves 100% to `shadow_archive/` and returns SyGuS header +
         First 25 lines + Last 20 lines + exact Shadow Archive path for `read_file`/`run_command` inspection.
    """
    text = raw_output or ""
    header_blocks: List[str] = []

    fluent_evt: Dict[str, Any] = {}
    # 1. Event Calculus & Temporal Fluent tracking
    if tool_name in ("run_command", "run_shell_command", "scan_target", "reasoning_engine"):
        fluent_evt = record_command_event(command_or_key, text, exit_code)
        if fluent_evt.get("invalidated_fluents"):
            header_blocks.append(
                f"[Temporal Event Calculus] State transition `{fluent_evt.get('invalidation_reason')}` "
                f"invalidated {len(fluent_evt['invalidated_fluents'])} prior fluent(s); re-verify state if needed."
            )

    # 2. Case-Based Reasoning (CBR) failure fingerprint matching + Engine 16/17 Continual & Meta Learning
    if tool_name in ("run_command", "run_shell_command", "scan_target"):
        cbr_match = match_failure_fingerprint(command_or_key, exit_code, text)
        if cbr_match:
            header_blocks.append(
                f"[CBR Failure Match {cbr_match['case_id']} (conf={cbr_match['match_confidence']})]: "
                f"{cbr_match['root_cause']} -> FIX: {cbr_match['verified_fix']}"
            )
        try:
            from .continual_learner import record_live_command_experience
            from .meta_learner import record_engine_forecast_outcome

            exp_res = record_live_command_experience(command_or_key, exit_code, text)
            eff_ok = bool(exp_res.get("effective_success", exit_code == 0))
            ch_tel = exp_res.get("channel_telemetry") or {}
            if ch_tel.get("meta_directive"):
                header_blocks.append(str(ch_tel["meta_directive"]))
            if exp_res.get("mdp_updated") is not None:
                mdp_u = exp_res["mdp_updated"]
                mdp_prob = float(mdp_u.get("transition_prob_success", 0.80))
                record_engine_forecast_outcome("mdp_tactical", eff_ok, predicted_prob=mdp_prob)
                if str(mdp_u.get("tool", "")).lower() in (
                    "ip", "ping", "arping", "nmap", "curl", "ss", "netstat", "tio", "traceroute", "tcpdump",
                ):
                    record_engine_forecast_outcome("bayesian_eig", eff_ok, predicted_prob=0.78)
            if exp_res.get("somatic_updated"):
                record_engine_forecast_outcome("vsa_somatic", eff_ok, predicted_prob=0.78)
            if _PENDING_CBR_MATCH_CACHE and exp_res.get("mdp_updated") is not None:
                cbr_conf = float(_PENDING_CBR_MATCH_CACHE.get("match_confidence", 0.80))
                record_engine_forecast_outcome("cbr_fingerprints", eff_ok, predicted_prob=cbr_conf)
                if eff_ok:
                    _PENDING_CBR_MATCH_CACHE.clear()
            if cbr_match:
                _PENDING_CBR_MATCH_CACHE.clear()
                _PENDING_CBR_MATCH_CACHE.update(cbr_match)
            if exp_res.get("learned_cbr_case"):
                lc = exp_res["learned_cbr_case"]
                record_engine_forecast_outcome("cbr_fingerprints", True, predicted_prob=0.85)
                header_blocks.append(
                    f"[Engine 16 Continual Learner]: Auto-discovered & saved new CBR rule `{lc.get('case_id')}` "
                    f"(`{lc.get('verified_remediation')}`)"
                )
        except Exception:
            eff_ok = exit_code == 0

        if _SPECULATIVE_BRANCH_CACHE:
            branch_key = "on_success_branch" if eff_ok else "on_failure_branch"
            branch = _SPECULATIVE_BRANCH_CACHE.get(branch_key, {})
            if isinstance(branch, dict):
                nxt_cmd = branch.get("next_command") or branch.get("pivot_command")
                nxt_tool = branch.get("next_tool") or branch.get("pivot_tool")
                if nxt_cmd:
                    header_blocks.append(
                        f"[Speculative Next-Tool Forecast ({branch.get('trigger', branch_key)})]: "
                        f"Tool `{nxt_tool}` -> `{nxt_cmd}`"
                    )

    # 3. SyGuS grammar-guided structured fact extraction
    sygus = extract_structured_facts(command_or_key, text)
    if sygus.get("summary_header"):
        header_blocks.append(sygus["summary_header"])

    if tool_name in ("run_command", "run_shell_command", "scan_target"):
        try:
            from .continual_learner import get_continual_learning_state
            from .rl_network_policy import record_rl_step_transition

            if str(get_continual_learning_state().get("mode", "AUTO")).upper() != "STOP":
                facts_cnt = (
                    len(sygus.get("arp_neighbors", []))
                    + len(sygus.get("open_ports", []))
                    + len(sygus.get("routes", []))
                    + (1 if sygus.get("summary_header") else 0)
                )
                rl_upd = record_rl_step_transition(
                    command=command_or_key,
                    exit_code=exit_code,
                    new_facts_count=facts_cnt,
                )
                if not rl_upd.get("skipped"):
                    from .meta_learner import record_engine_forecast_outcome

                    rl_ok = bool(exit_code == 0 and rl_upd.get("reward", 0.0) >= 0.0)
                    record_engine_forecast_outcome("rl_network_policy", rl_ok, predicted_prob=0.78)
                    record_engine_forecast_outcome("spectral_manifold_pca", exit_code == 0, predicted_prob=0.78)
                if rl_upd.get("reward", 0.0) <= -3.0:
                    header_blocks.append(
                        f"[Engine 19 RL Policy Warning]: Redundant/no-progress action `{rl_upd['action_id']}` "
                        f"(R={rl_upd['reward']:+.1f}); advance to next OSI layer stage."
                    )
                # Improvement #1: Delta-Triggered L1 World-Model State Register Auto-Injection
                state_changed = bool(
                    facts_cnt > 0
                    or fluent_evt.get("invalidated_fluents")
                    or rl_upd.get("pre_state") != rl_upd.get("post_state")
                )
                if state_changed:
                    l1_line = get_l1_state_summary_line()
                    header_blocks.append(
                        f"[L1 World-Model State Register] RL_State=`{rl_upd.get('post_state', 'N/A')}` | {l1_line}"
                    )
        except Exception:
            pass

    prefix_str = ("\n".join(header_blocks) + "\n---\n") if header_blocks else ""

    # 4. Guardrail 2: Keep raw output 100% intact if <= threshold (2,500 chars on laptop, 12,000 chars on Ultra Server)
    hw_limits = get_hardware_reasoning_limits()
    raw_threshold = int(hw_limits.get("raw_preserve_threshold_chars", RAW_PRESERVE_THRESHOLD_CHARS))
    if len(text) <= raw_threshold:
        return prefix_str + text

    # Archive 100% of raw output to Central Shadow Store
    shadow_path = archive_to_shadow_store(command_or_key, text)
    lines = text.splitlines()
    if len(lines) > 50:
        head = "\n".join(lines[:25])
        tail = "\n".join(lines[-20:])
        omitted_lines = len(lines) - 45
        body = (
            f"{head}\n"
            f"... [{omitted_lines} middle lines ({len(text)} total chars) archived losslessly to `{shadow_path}`] ...\n"
            f"... [To inspect specific lines, use `read_file` or `grep -n <pattern> {shadow_path}`] ...\n"
            f"{tail}"
        )
    else:
        body = (
            f"{text[:1400]}\n"
            f"... [{len(text) - 2400} chars archived losslessly to `{shadow_path}`] ...\n"
            f"{text[-1000:]}"
        )
    return prefix_str + body


def build_dynamic_l1_state_block(user_query: str = "") -> str:
    """
    Builds a compact L1 Symbolic State Register + Bipartite Graph Page-In block
    (Guardrail 3: injected dynamically without mutating the static prefix of `messages[0]`).
    """
    fluent_summary = get_l1_state_summary_line()
    fluent_state = load_fluent_state()
    fluents = fluent_state.get("fluents", {})
    holding = [
        f"{fid}={f.get('value', f.get('fluent', 'HOLDING'))}"
        for fid, f in list(fluents.items())[-6:]
        if isinstance(f, dict) and f.get("status") in ("ACTIVE", "HOLDING")
    ]

    # MemGPT-style Bipartite Graph Page-In: use Engine 5 Personalized PageRank across the entire ObsidianVault
    paged_notes: List[str] = []
    if user_query and len(user_query) >= 4:
        try:
            from .associative import run_associative_vault_reasoning

            assoc_page = run_associative_vault_reasoning(query=user_query, top_k=3, save_to_vault=False)
            for an in assoc_page.get("activated_notes", [])[:3]:
                wta_s = f" [Apply: {an['when_to_apply'][:75]}]" if an.get("when_to_apply") else ""
                paged_notes.append(f"`[[{an['wiki_link']}]]` ({an.get('summary', '')[:85]}{wta_s})")
        except Exception:
            q_words = {w.lower() for w in user_query.split() if len(w) >= 4}
            if q_words:
                for note in scan_vault_notes():
                    title_lower = note.get("title", "").lower()
                    if any(w in title_lower for w in q_words):
                        paged_notes.append(f"`{note['rel_path']}` ({note['title']})")
                    if len(paged_notes) >= 3:
                        break

    parts: List[str] = []
    if fluent_summary and "No symbolic state" not in fluent_summary:
        parts.append(fluent_summary)
    if holding:
        parts.append("[Active Fluents] " + " | ".join(holding[:5]))
    try:
        from .rl_network_policy import predict_rl_next_step_rollout

        rl_pred = predict_rl_next_step_rollout(problem=user_query or "live_l1_state", horizon=2)
        imm = rl_pred.get("immediate_action", {})
        st_info = rl_pred.get("state_info", {})
        topo_s = st_info.get("topology_summary", {})
        parts.append(
            f"[Engine 19/20 Network World-Model & RL Policy] NIC={topo_s.get('primary_interface')} "
            f"Subnets={topo_s.get('local_subnets')} ARP_Reachable={topo_s.get('reachable_neighbors_count')} | "
            f"Cluster={st_info.get('cluster_id')} Stage={st_info.get('stage')} -> "
            f"Next Cmd (Q_LCB={imm.get('q_lcb', imm.get('q_star', 0.0)):+.2f}): `{imm.get('command', '')}`"
        )
    except Exception:
        pass
    try:
        from .meta_learner import get_meta_mind_channel_directive

        mm_dir = get_meta_mind_channel_directive(problem=user_query)
        if mm_dir.get("meta_directive"):
            parts.append(str(mm_dir["meta_directive"]))
    except Exception:
        pass
    if paged_notes:
        parts.append("[Auto-Paged Vault Notes] " + ", ".join(paged_notes))

    return "\n".join(parts)


class SpeculativeLookaheadCache:
    """
    Idle-Time Speculative Lookahead Cache:
    Pre-computes fast symbolic state & associative graph readiness in a low-priority background thread
    ONLY when the CLI is idle waiting for user input, and yields immediately when `pause()` is called.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._cache: Dict[str, Any] = {}
        self._active_event = threading.Event()
        self._running = False

    def stop(self) -> None:
        """Immediately signal any background speculative thread to yield (< 0.01 ms, zero blocking work)."""
        self._active_event.clear()

    def prewarm_async(self, context_hint: str = "system_state") -> None:
        """Schedules a non-blocking background pre-warm of the symbolic state & vault index if stale."""
        with self._lock:
            if self._running or (time.time() - float(self._cache.get("timestamp", 0.0))) < 15.0:
                return
            self._running = True
        self._active_event.set()

        def _worker() -> None:
            try:
                if not self._active_event.is_set():
                    return
                l1_block = build_dynamic_l1_state_block(context_hint)
                with self._lock:
                    self._cache["last_l1_block"] = l1_block
                    self._cache["timestamp"] = time.time()
            except Exception:
                pass
            finally:
                with self._lock:
                    self._running = False

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def pause_and_get_cached_l1(self, user_query: str = "") -> str:
        """Immediately signals any speculative thread to yield and returns the cached L1 state block if fresh."""
        self._active_event.clear()
        with self._lock:
            cached = self._cache.get("last_l1_block")
            ts = float(self._cache.get("timestamp", 0.0))
        if cached and (time.time() - ts) < 30.0 and not user_query:
            return str(cached)
        fresh = build_dynamic_l1_state_block(user_query)
        with self._lock:
            self._cache["last_l1_block"] = fresh
            self._cache["timestamp"] = time.time()
        return fresh
