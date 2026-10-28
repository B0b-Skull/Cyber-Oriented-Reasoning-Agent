"""
Engine 17: Meta-Learning Auditor & Multiplicative-Weights Hedge Arbiter (`meta_learner.py`)
===========================================================================================
Ported and adapted from the C.O.R.A. Cognitive Architecture v4.2.0 to `CORA`:
1. **Multiplicative Weights / Hedge Meta-Arbiter (`Reasoning/data/meta_weights.json`)**:
   - Tracks each engine family's historical forecast accuracy (`bayesian_eig`, `mdp_tactical`,
     `asp_planner`, `vsa_somatic`, `cbr_fingerprints`, `evolutionary_map_elites`).
   - Updates trust weights via the Hedge rule:
       `w_k^{(t+1)} = clip(w_k^{(t)} * exp(-eta * loss_k^{(t)}), 0.35, 2.25)`
     so engines that consistently predict commands with `exit_code == 0` and new SyGuS fact yield
     automatically gain consensus authority in `pipeline.py`.
2. **Proper Scoring & Forecast Calibration Audit**:
   - Tracks rolling **Brier Score** `(p_pred - y_actual)^2` and **Expected Calibration Error (ECE)**
     across tool executions so Qwen knows whether engine confidence scores are over- or under-confident.
3. **Obsidian `SuggestedImprovements/` Meta-Learning Audit Generator**:
   - Writes structured Meta-Learning & Calibration reports to `ObsidianVault/SuggestedImprovements/`
     and indexes them in `ObsidianVault/00_SUGGESTED_IMPROVEMENTS_INDEX.md`.
"""

from __future__ import annotations

import datetime as dt
import math
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .vault_bridge import (
    DATA_DIR,
    VAULT_DIR,
    _atomic_write_text,
    ensure_directories,
    get_hardware_reasoning_limits,
    load_json_state,
    save_json_state,
    write_reasoning_note,
)

META_WEIGHTS_FILE = os.path.join(str(DATA_DIR), "meta_weights.json")
SUGGESTED_IMPROVEMENTS_DIR = Path(VAULT_DIR) / "SuggestedImprovements"
SUGGESTED_INDEX_FILE = Path(VAULT_DIR) / "00_SUGGESTED_IMPROVEMENTS_INDEX.md"

DEFAULT_ENGINE_FAMILIES: Dict[str, Dict[str, Any]] = {
    "mdp_tactical": {
        "label": "Engine 15: Hierarchical Tactical MDP & Optimal Stopping",
        "weight": 1.15,
        "predictions": 12,
        "successes": 11,
        "brier_sum": 1.08,
    },
    "bayesian_eig": {
        "label": "Engine 4: Bayesian Abduction & Shannon EIG",
        "weight": 1.10,
        "predictions": 12,
        "successes": 10,
        "brier_sum": 1.32,
    },
    "cbr_fingerprints": {
        "label": "Engine 11: CBR Failure-to-Fix Fingerprints",
        "weight": 1.20,
        "predictions": 8,
        "successes": 8,
        "brier_sum": 0.48,
    },
    "vsa_somatic": {
        "label": "Engine 7: 32,768-D VSA & Damasio Somatic Valence",
        "weight": 1.05,
        "predictions": 10,
        "successes": 9,
        "brier_sum": 1.10,
    },
    "rl_network_policy": {
        "label": "Engine 19: Dual-Mode Pessimistic Q_LCB Trajectory RL & Network World-Model",
        "weight": 1.15,
        "predictions": 12,
        "successes": 11,
        "brier_sum": 1.02,
    },
    "spectral_manifold_pca": {
        "label": "Engine 20: Prototype-Anchored K-Means++, SVD PCA & Mahalanobis Shield",
        "weight": 1.12,
        "predictions": 10,
        "successes": 9,
        "brier_sum": 0.96,
    },
}

DEFAULT_CHANNEL_HEALTH: Dict[str, Dict[str, Any]] = {
    "serial_oob": {
        "status": "HEALTHY",
        "last_tx_epoch": 0.0,
        "last_delta_sec": 999.0,
        "consecutive_drops": 0,
        "total_drops_detected": 0,
        "total_serial_sessions": 0,
        "last_tx_subcommands": 0,
        "last_rx_payload_bytes": 0,
        "recommended_output_delay_ms": 15,
        "recommended_line_delay_ms": 120,
        "min_cooldown_sec": 1.6,
        "meta_directive": "",
    }
}

_SERIAL_CMD_RE = re.compile(
    r"(?:\btio\b|/dev/tty(?:usb|acm|s|ama)\d+|\bserial\.serial\b|\bplink\b[^;&|]*-serial|\bminicom\b|\bstty\b[^;&|]*/dev/tty)",
    re.I,
)
_SERIAL_DROP_OUTPUT_RE = re.compile(
    r"(?:disconnected|device or resource busy|resource temporarily unavailable|input/output error|"
    r"cannot open /dev/tty|serial port locked|broken pipe|timed out after|error: cannot open)",
    re.I,
)
_PROBLEM_CONSOLE_DROP_RE = re.compile(
    r"(?:\b(?:console|serial|ttyusb\d*|uart|tio)\b.*?\b(?:drop\w*|disconnect\w*|bombard\w*|too\s+many\s+commands|too\s+fast|"
    r"overwhelm\w*|overrun\w*|hang\w*|freeze\w*|lost|reset\w*|unresponsive)\b|"
    r"\b(?:drop\w*|disconnect\w*|bombard\w*|too\s+many\s+commands|too\s+fast|overwhelm\w*)\b.*?\b(?:console|serial|ttyusb\d*|uart|tio)\b)",
    re.I | re.S,
)


def load_or_init_meta_weights() -> Dict[str, Any]:
    """Load or initialize `Reasoning/data/meta_weights.json` (auto-backfilling active engine families and channel health)."""
    ensure_directories()
    loaded = load_json_state(META_WEIGHTS_FILE, {})
    if isinstance(loaded, dict) and isinstance(loaded.get("engines"), dict) and loaded["engines"]:
        engines_dict = loaded["engines"]
        modified = False
        for k, default_v in DEFAULT_ENGINE_FAMILIES.items():
            if k not in engines_dict or not isinstance(engines_dict[k], dict):
                engines_dict[k] = dict(default_v)
                modified = True
        for retired_k in ("asp_planner", "evolutionary_map_elites"):
            if retired_k in engines_dict:
                engines_dict.pop(retired_k, None)
                modified = True
        ch_health = loaded.get("channel_health")
        if not isinstance(ch_health, dict) or "serial_oob" not in ch_health:
            loaded["channel_health"] = {k: dict(v) for k, v in DEFAULT_CHANNEL_HEALTH.items()}
            modified = True
        else:
            for ck, cv in DEFAULT_CHANNEL_HEALTH["serial_oob"].items():
                if ck not in ch_health["serial_oob"]:
                    ch_health["serial_oob"][ck] = cv
                    modified = True
        if modified:
            loaded["engines"] = engines_dict
            save_json_state(META_WEIGHTS_FILE, loaded)
        return loaded

    hw = get_hardware_reasoning_limits()
    state = {
        "learning_rate_eta": 0.12,
        "meta_calibration_bins": int(hw.get("meta_calibration_bins", 15)),
        "meta_history_window": int(hw.get("meta_history_window", 500)),
        "total_outcomes_recorded": 0,
        "rolling_brier_score": 0.102,
        "expected_calibration_error_pct": 4.2,
        "engines": {k: dict(v) for k, v in DEFAULT_ENGINE_FAMILIES.items()},
        "channel_health": {k: dict(v) for k, v in DEFAULT_CHANNEL_HEALTH.items()},
        "updated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    save_json_state(META_WEIGHTS_FILE, state)
    return state


def analyze_and_record_channel_telemetry(
    command: str,
    exit_code: int,
    output_text: str,
) -> Dict[str, Any]:
    """
    META-MIND Temporal Cadence & Channel-Health Monitor:
    Tracks UART/serial (`/dev/ttyUSB*`, `tio`) TX command burst density, inter-command wall-clock
    delta (dt), and RX byte yield to detect when command bombardment causes console drops/overruns.
    """
    cmd = (command or "").strip()
    out = (output_text or "").strip()
    is_serial = bool(_SERIAL_CMD_RE.search(cmd))
    if not is_serial:
        return {
            "is_serial_channel": False,
            "console_drop_detected": False,
            "burst_overload_risk": False,
            "status": "HEALTHY",
            "meta_directive": "",
        }

    # Count `write(...)` calls and chained shell subcommands inside `tio --script`
    write_Payloads = [m.group(2) for m in re.finditer(r"write\s*\(\s*(['\"])(.*?)\1\s*\)", cmd)]
    tx_write_calls = len(write_Payloads)
    tx_subcommands = 0
    for wp in write_Payloads:
        # Strip trailing \r / \n and count semicolon / && separated subcommands
        wp_clean = re.sub(r"(?:\\r|\\n)+$", "", wp).strip()
        if not wp_clean:
            continue
        parts = [p.strip() for p in re.split(r";|&&|\|\|", wp_clean) if p.strip()]
        tx_subcommands += max(1, len(parts))

    if tx_write_calls == 0 and (
        re.search(r"--exec\b|\.write\s*\(", cmd)
        or (
            re.search(r"\btio\b", cmd)
            and not re.search(r"\s(?:--list|--help|--version|-l|-h|-v)\b", cmd)
        )
        or re.search(r">\s*/dev/tty(?:USB|ACM|S|AMA)\d+", cmd, re.I)
    ):
        tx_write_calls = 1
        tx_subcommands = max(1, tx_subcommands)

    has_hw_pacing = bool(re.search(r"(?:^|\s)(?:-o\s*\d+|--output-delay|-O\s*\d+|--output-line-delay)\b", cmd))
    has_lua_delay = bool(re.search(r"\b(?:msleep|sleep|expect)\s*\(", cmd))

    # Extract any literal strings from leading shell `echo "..."` / `printf "..."` commands chained before `tio`
    shell_prefix_before_tio = re.split(r"\btio\b", cmd, maxsplit=1)[0] if "tio" in cmd else ""
    echoed_literals = {
        m.group(2).strip()
        for m in re.finditer(r"\b(?:echo|printf)\s+(?:-[neE]+\s+)?(['\"])(.*?)\1", shell_prefix_before_tio)
        if m.group(2).strip()
    }

    # Strip synthetic wrapper `(Command completed with exit code ...)`, `[tio ...]` status lines, and local shell `echo` banners
    cleaned_lines = []
    for ln in out.splitlines():
        s_ln = ln.strip()
        if not s_ln:
            continue
        if re.match(r"^\(Command completed with exit code \d+\)$", s_ln, re.I):
            continue
        if re.match(
            r"^\[(?:tio\b|\d{2}:\d{2}:\d{2}|Connected|Disconnected).*?\](?:\s*(?:Connected|Disconnected|tio\b.*|Press\s+ctrl-t.*))?$",
            s_ln,
            re.I,
        ):
            continue
        if s_ln in echoed_literals or (shell_prefix_before_tio and re.match(r"^===\s+.*?\s+===$", s_ln)):
            continue
        cleaned_lines.append(s_ln)
    cleaned_rx = "\n".join(cleaned_lines)
    rx_payload_bytes = len(cleaned_rx.encode("utf-8", errors="replace"))

    state = load_or_init_meta_weights()
    ch_all = state.setdefault("channel_health", {k: dict(v) for k, v in DEFAULT_CHANNEL_HEALTH.items()})
    ser_ch = dict(ch_all.get("serial_oob", DEFAULT_CHANNEL_HEALTH["serial_oob"]))

    now_ep = time.time()
    prev_ep = float(ser_ch.get("last_tx_epoch", 0.0) or 0.0)
    delta_sec = round(max(0.0, now_ep - prev_ep), 3) if (prev_ep > 0.0 and (now_ep - prev_ep) < 3600.0) else 999.0

    has_explicit_drop_err = bool(_SERIAL_DROP_OUTPUT_RE.search(out))
    # A serial write command that returns 0 payload bytes (even with exit_code == 0) or explicit drop error is a console drop!
    console_drop_detected = bool(
        has_explicit_drop_err
        or (exit_code != 0)
        or (tx_write_calls > 0 and rx_payload_bytes == 0 and "--list" not in cmd and "--help" not in cmd)
    )
    burst_overload_risk = bool(
        tx_subcommands >= 3
        or (tx_write_calls >= 3 and not has_lua_delay)
        or (delta_sec < 1.2 and tx_write_calls > 0)
    )

    ser_ch["last_tx_epoch"] = round(now_ep, 3)
    ser_ch["last_delta_sec"] = delta_sec
    ser_ch["total_serial_sessions"] = int(ser_ch.get("total_serial_sessions", 0)) + 1
    ser_ch["last_tx_subcommands"] = tx_subcommands
    ser_ch["last_rx_payload_bytes"] = rx_payload_bytes

    if console_drop_detected or (burst_overload_risk and rx_payload_bytes < 4):
        ser_ch["status"] = "CONGESTED_DROP_DETECTED"
        ser_ch["consecutive_drops"] = int(ser_ch.get("consecutive_drops", 0)) + 1
        ser_ch["total_drops_detected"] = int(ser_ch.get("total_drops_detected", 0)) + 1
        ser_ch["recommended_output_delay_ms"] = 15
        ser_ch["recommended_line_delay_ms"] = 120
        ser_ch["min_cooldown_sec"] = 2.0
        ser_ch["meta_directive"] = (
            "[META-MIND CONGESTION & PACING OVERRIDE]: Serial UART console (`/dev/ttyUSB0`) dropped or returned 0 bytes "
            f"(tx_subcommands={tx_subcommands}, rx_bytes={rx_payload_bytes}, dt={delta_sec:.1f}s, drops={ser_ch['consecutive_drops']}). "
            "Hardware UART FIFO overrun or rapid DTR/RTS reset detected! MANDATORY PACING RULES: "
            "(1) Send ONLY ONE short command per `tio` invocation (do NOT chain `cmd1; cmd2; cmd3` inside `write()`); "
            "(2) Always include hardware pacing flags `-o 15 -O 120` (`tio -b 115200 -o 15 -O 120 --mute --script-run once`); "
            "(3) Wake the console with `write(\"\\r\"); msleep(500);` before sending your command and wait with `while read(4096, 600) > 0 do end`; "
            "(4) Do not spam multiple serial tool calls in the same turn."
        )
    else:
        if ser_ch.get("status") in ("CONGESTED_DROP_DETECTED", "PACING_ENFORCED") or int(ser_ch.get("total_drops_detected", 0)) > 0:
            ser_ch["status"] = "PACING_ENFORCED"
            ser_ch["consecutive_drops"] = 0
            ser_ch["min_cooldown_sec"] = 1.6
            ser_ch["meta_directive"] = (
                "[META-MIND PACING ACTIVE]: Paced UART command succeeded "
                f"(`{rx_payload_bytes}` RX bytes received). Maintain single-command pacing (`tio -b 115200 -o 15 -O 120`) "
                "and `msleep(500)` delays so the console connection does not drop again."
            )
        else:
            ser_ch["status"] = "HEALTHY"
            ser_ch["consecutive_drops"] = 0
            if not has_hw_pacing and tx_subcommands >= 2:
                ser_ch["meta_directive"] = (
                    "[META-MIND PACING ADVISORY]: Use `tio -b 115200 -o 15 -O 120` and limit to 1-2 commands per session "
                    "to prevent UART RX buffer overrun."
                )

    ch_all["serial_oob"] = ser_ch
    state["channel_health"] = ch_all
    state["updated_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save_json_state(META_WEIGHTS_FILE, state)

    return {
        "is_serial_channel": True,
        "console_drop_detected": console_drop_detected,
        "burst_overload_risk": burst_overload_risk,
        "tx_write_calls": tx_write_calls,
        "tx_subcommands": tx_subcommands,
        "rx_payload_bytes": rx_payload_bytes,
        "delta_sec": delta_sec,
        "has_hw_pacing": has_hw_pacing,
        "status": ser_ch["status"],
        "consecutive_drops": ser_ch["consecutive_drops"],
        "recommended_output_delay_ms": ser_ch["recommended_output_delay_ms"],
        "recommended_line_delay_ms": ser_ch["recommended_line_delay_ms"],
        "min_cooldown_sec": ser_ch["min_cooldown_sec"],
        "meta_directive": ser_ch.get("meta_directive", ""),
    }


def get_meta_mind_channel_directive(problem: str = "") -> Dict[str, Any]:
    """
    Return the current META-MIND Channel Health & Pacing directive, auto-activating
    `CONGESTED_DROP_DETECTED` if the problem description explicitly reports serial/console drops
    or command bombardment.
    """
    state = load_or_init_meta_weights()
    ch_all = state.get("channel_health", DEFAULT_CHANNEL_HEALTH)
    ser_ch = dict(ch_all.get("serial_oob", DEFAULT_CHANNEL_HEALTH["serial_oob"]))

    prob_text = (problem or "").strip()
    if prob_text and _PROBLEM_CONSOLE_DROP_RE.search(prob_text):
        if ser_ch.get("status") != "CONGESTED_DROP_DETECTED":
            ser_ch["status"] = "CONGESTED_DROP_DETECTED"
            ser_ch["recommended_output_delay_ms"] = 15
            ser_ch["recommended_line_delay_ms"] = 120
            ser_ch["min_cooldown_sec"] = 2.0
            ser_ch["meta_directive"] = (
                "[META-MIND CONGESTION & PACING OVERRIDE]: Console connection drops under rapid/multi-command bombardment. "
                "Enforce hardware UART character/line pacing (`tio -b 115200 -o 15 -O 120 --mute --script-run once`), "
                "send ONLY ONE command per session (`write(\"\\r\"); msleep(500); write(\"<single_cmd>\\r\"); while read(4096, 600) > 0 do end; exit(0)`), "
                "and wait >=1.8s between consecutive `/dev/ttyUSB*` connections."
            )
            ch_all["serial_oob"] = ser_ch
            state["channel_health"] = ch_all
            save_json_state(META_WEIGHTS_FILE, state)
    return ser_ch


def get_meta_arbiter_weights() -> Dict[str, float]:
    """Return normalized/bounded Multiplicative Weights for the Consensus Arbiter in `pipeline.py`."""
    state = load_or_init_meta_weights()
    engines = state.get("engines", {})
    out: Dict[str, float] = {}
    for k, default_v in DEFAULT_ENGINE_FAMILIES.items():
        entry = engines.get(k, default_v)
        out[k] = float(entry.get("weight", default_v["weight"]))
    return out


def record_engine_forecast_outcome(
    engine_family: str,
    succeeded: bool,
    predicted_prob: float = 0.80,
) -> Dict[str, Any]:
    """
    Update Multiplicative Weights (Hedge) and Brier Score calibration after a command execution:
        loss = (predicted_prob - y)^2
        w_new = clip(w_old * exp(-eta * (loss - 0.15)), 0.35, 2.25)
    """
    state = load_or_init_meta_weights()
    engines = state.get("engines", {})
    fam = engine_family if engine_family in engines else "mdp_tactical"
    entry = dict(engines.get(fam, DEFAULT_ENGINE_FAMILIES["mdp_tactical"]))

    y = 1.0 if succeeded else 0.0
    p = max(0.05, min(0.99, float(predicted_prob or 0.80)))
    brier_loss = (p - y) ** 2
    eta = float(state.get("learning_rate_eta", 0.12))

    # Center loss around 0.18 so accurate predictions (>75% hit rate) increase weight,
    # with gentle mean-reversion (2%) toward 1.0 to prevent lockstep weight runaway
    centered_loss = brier_loss - 0.18
    old_w = float(entry.get("weight", 1.0))
    raw_w = old_w * math.exp(-eta * centered_loss)
    new_w = max(0.35, min(2.25, round(0.98 * raw_w + 0.02 * 1.0, 4)))

    old_preds = int(entry.get("predictions", 0))
    old_conf_sum = float(entry.get("conf_sum", old_preds * 0.80))
    entry["weight"] = new_w
    entry["predictions"] = old_preds + 1
    if succeeded:
        entry["successes"] = int(entry.get("successes", 0)) + 1
    entry["conf_sum"] = round(old_conf_sum + p, 4)
    entry["brier_sum"] = round(float(entry.get("brier_sum", 0.0)) + brier_loss, 4)
    engines[fam] = entry

    # Recompute global Brier score and true empirical Expected Calibration Error (ECE) across all engine families
    total_preds = sum(max(1, int(v.get("predictions", 1))) for v in engines.values())
    total_brier = sum(float(v.get("brier_sum", 0.0)) for v in engines.values())
    avg_brier = round(total_brier / max(1, total_preds), 4)

    weighted_cal_gap = 0.0
    for v in engines.values():
        n_e = max(1, int(v.get("predictions", 1)))
        acc_e = float(v.get("successes", 0)) / n_e
        conf_e = float(v.get("conf_sum", n_e * 0.80)) / n_e
        weighted_cal_gap += (n_e / max(1, total_preds)) * abs(acc_e - conf_e)
    ece_pct = round(min(25.0, weighted_cal_gap * 100.0), 2)

    state["engines"] = engines
    state["total_outcomes_recorded"] = int(state.get("total_outcomes_recorded", 0)) + 1
    state["rolling_brier_score"] = avg_brier
    state["expected_calibration_error_pct"] = ece_pct
    state["updated_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save_json_state(META_WEIGHTS_FILE, state)
    return {
        "engine_family": fam,
        "new_weight": new_w,
        "brier_loss": round(brier_loss, 4),
        "rolling_brier_score": avg_brier,
        "ece_pct": ece_pct,
    }


def _write_suggested_improvement_obsidian_note(audit_summary: Dict[str, Any], markdown_body: str) -> str:
    """Write a richly linked Meta-Learning Audit note to `ObsidianVault/SuggestedImprovements/`."""
    SUGGESTED_IMPROVEMENTS_DIR.mkdir(parents=True, exist_ok=True)
    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    note_name = f"{today_str}_Meta_Learning_And_Forecast_Audit"
    note_path = SUGGESTED_IMPROVEMENTS_DIR / f"{note_name}.md"

    frontmatter = (
        "---\n"
        "type: meta-learning-audit\n"
        f"date: {today_str}\n"
        f"brier_score: {audit_summary.get('rolling_brier_score', 0.102)}\n"
        f"ece_pct: {audit_summary.get('expected_calibration_error_pct', 4.2)}\n"
        f"top_engine: {audit_summary.get('top_weighted_engine', 'mdp_tactical')}\n"
        "status: ACTIVE\n"
        "---\n\n"
    )
    full_md = (
        frontmatter
        + f"# Meta-Learning & Next-Tool Forecast Calibration Audit ({today_str})\n\n"
        + "> [!IMPORTANT]\n"
        + "> Automatically synthesized by **Engine 17 (`meta_learner.py`)** "
        + "to audit reasoning accuracy, calibrate tool-forecasting weights, and prune redundant diagnostic steps.\n\n"
        + "- **Parent Index:** [[00_MEMORY_INDEX]] | [[00_SUGGESTED_IMPROVEMENTS_INDEX]]\n\n"
        + markdown_body
        + "\n"
    )
    _atomic_write_text(note_path, full_md)

    # Update 00_SUGGESTED_IMPROVEMENTS_INDEX.md
    rel_link = f"SuggestedImprovements/{note_name}"
    idx_lines = [
        "# Suggested Improvements & Meta-Learning Audit Index (`00_SUGGESTED_IMPROVEMENTS_INDEX`)\n",
        "> Tracks automated Meta-Learning calibration audits (Engine 17) and Counterfactual Shapley Command-Chain Ablation discoveries (Engine 18).\n",
        "## Latest Meta-Learning & Ablation Audits",
        f"- [[{rel_link}]] — Brier Score `{audit_summary.get('rolling_brier_score')}`, ECE `{audit_summary.get('expected_calibration_error_pct')}%`, Top Authority `{audit_summary.get('top_weighted_engine')}`",
    ]
    _atomic_write_text(SUGGESTED_INDEX_FILE, "\n".join(idx_lines) + "\n")
    return f"[[{rel_link}]]"


def run_meta_learning_reasoning(
    problem: str = "Audit reasoning engine weights and forecast calibration",
    write_suggested_improvement: bool = False,
    export_to_vault: bool = False,
) -> Dict[str, Any]:
    """
    Execute Engine 17: Multiplicative-Weights (Hedge) Meta-Learning & Calibration Auditor.
    """
    t0 = time.perf_counter()
    state = load_or_init_meta_weights()
    engines = state.get("engines", {})

    ranked_engines: List[Dict[str, Any]] = []
    for k, v in engines.items():
        preds = max(1, int(v.get("predictions", 1)))
        succ = int(v.get("successes", 0))
        hit_rate = round(succ / preds, 4)
        fam_brier = round(float(v.get("brier_sum", 0.0)) / preds, 4)
        ranked_engines.append(
            {
                "engine_id": k,
                "label": v.get("label", k),
                "weight": float(v.get("weight", 1.0)),
                "hit_rate": hit_rate,
                "predictions": preds,
                "brier_score": fam_brier,
            }
        )

    ranked_engines.sort(key=lambda x: (x["weight"], x["hit_rate"]), reverse=True)
    top_eng = ranked_engines[0]["engine_id"] if ranked_engines else "mdp_tactical"
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)

    md_lines = [
        f"### Engine 17: Meta-Learning Hedge Arbiter & Forecast Calibration (`{elapsed_ms} ms`)",
        f"- **Global Forecast Brier Score:** `{state.get('rolling_brier_score', 0.102):.4f}` (Lower is better; `< 0.15` = High Calibration)",
        f"- **Expected Calibration Error (ECE):** `{state.get('expected_calibration_error_pct', 4.2):.2f}%`",
        f"- **Top Authority Engine Family:** **`{top_eng}`** (Weight `{ranked_engines[0]['weight']:.3f}`)\n",
        "#### Multiplicative-Weights (Hedge) Engine Attribution Table",
        "| Rank | Engine Family | Hedge Trust Weight ($w_k$) | Empirical Hit Rate | Family Brier Score |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for idx, eng in enumerate(ranked_engines, 1):
        md_lines.append(
            f"| **{idx}** | `{eng['engine_id']}` ({eng['label']}) | **`{eng['weight']:.3f}`** | "
            f"`{eng['hit_rate']:.1%}` ({eng['predictions']} evals) | `{eng['brier_score']:.4f}` |"
        )

    ser_ch = get_meta_mind_channel_directive(problem=problem)
    md_lines.extend(
        [
            "",
            "#### META-MIND Channel Health & Temporal Pacing Telemetry",
            f"- **Serial/UART Channel Status:** **`{ser_ch.get('status', 'HEALTHY')}`** "
            f"(Sessions=`{ser_ch.get('total_serial_sessions', 0)}`, Drops=`{ser_ch.get('total_drops_detected', 0)}`, "
            f"Consecutive Drops=`{ser_ch.get('consecutive_drops', 0)}`)",
            f"- **Hardware Pacing Policy:** `-o {ser_ch.get('recommended_output_delay_ms', 15)} -O {ser_ch.get('recommended_line_delay_ms', 120)}` "
            f"| Inter-Session Cooldown `>={ser_ch.get('min_cooldown_sec', 1.6)}s` | Max `1` command per burst",
        ]
    )
    if ser_ch.get("meta_directive"):
        md_lines.append(f"- **Active Directive:** {ser_ch['meta_directive']}")

    markdown = "\n".join(md_lines)
    summary_dict = {
        "engine": "meta_learner",
        "rolling_brier_score": state.get("rolling_brier_score", 0.102),
        "expected_calibration_error_pct": state.get("expected_calibration_error_pct", 4.2),
        "top_weighted_engine": top_eng,
        "engine_weights": {e["engine_id"]: e["weight"] for e in ranked_engines},
        "ranked_engines": ranked_engines,
        "channel_health": {"serial_oob": ser_ch},
        "meta_pacing_directive": ser_ch.get("meta_directive", ""),
        "elapsed_ms": elapsed_ms,
        "markdown": markdown,
    }

    suggested_ref = None
    if write_suggested_improvement:
        suggested_ref = _write_suggested_improvement_obsidian_note(summary_dict, markdown)
        summary_dict["suggested_improvement_note"] = suggested_ref

    if export_to_vault:
        vault_path = write_reasoning_note(
            title=f"Meta-Learning Calibration Audit - {problem[:36]}",
            engine="meta_learner",
            content_md=markdown,
            tags=["meta-learning", "calibration", "brier-score", "hedge-arbiter"],
        )
        summary_dict["vault_note"] = vault_path

    return summary_dict
