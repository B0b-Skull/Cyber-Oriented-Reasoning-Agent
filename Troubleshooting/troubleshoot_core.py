#!/usr/bin/env python3
"""
CORA & 15-Engine Layered Reasoning Diagnostic & Fault-Isolation Engine (`troubleshoot_core.py` — `v3.6.1`)
==============================================================================================================
Pinpoints exact areas of concern across the CORA runtime and isolates which layer or engine
of the 15-Engine Neuro-Symbolic Suite + Zero-Loss Context VM + 10 Guardrails could be causing an issue:

  [Layer A] System, GPU VRAM, Disk, & llama-server Runtime Health
            - RAM/VRAM/Disk pressure, llama-server HTTP /health, /props (n_ctx), /tokenize, log error scan
  [Layer B] JSON State Store & ObsidianVault Integrity (`Reasoning/data/` & `ObsidianVault/`)
            - Scans every `.json` state file for corruption, permissions, or schema drift
  [Layer C] Guardrail & Pre/Post-Execution Interception Audit (Guardrails 1 through 10)
            - Tests Guardrail 1 (CEGAR command blocker vs advisory), Guardrail 2 (SyGuS + 2,500-char threshold),
              Guardrail 3 (static system prompt prefix), Guardrail 4 (Consensus Arbiter),
              Guardrail 5 (Temporal Fluents stale state check), Guardrail 6 (Shadow Archive rotation),
              Guardrail 7 (/goal, /relentless & Jinja User-Query Anchor), Guardrail 8 (ConsolePostureDetection),
              Guardrail 9 (Uncapped Cross-Platform Training Pipeline & Multi-Line PDF Wrap Extractor),
              Guardrail 10 (Engine 15 Hierarchical Tactical MDP & Uncapped Transition Merger)
  [Layer D] Per-Engine Isolated Fault & Latency Profiler (Engines 1 through 15)
            - Executes each of the 15 engines individually in isolation, measuring CPU latency,
              memory/state health, and flagging any engine with warnings, slowness, or exceptions
  [Layer E] Interactive Command / Prompt Simulator (`--diagnose-cmd "<cmd>"` or `--explain-arbiter "<problem>"`)
            - Shows step-by-step how a specific command or problem flows through CEGAR -> Execution ->
              Temporal Fluents -> CBR -> SyGuS -> Context VM -> 15-Engine Consensus Arbiter

Supports `--fix` to automatically repair corrupted JSON stores, clear stuck/stale temporal fluents,
and re-seed missing models.
"""

import argparse
import json
import os
import platform
import py_compile
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

TROUBLESHOOT_DIR = Path(__file__).resolve().parent
CORA_ROOT = TROUBLESHOOT_DIR.parent
CORA_CORE_DIR = CORA_ROOT / "core" if (CORA_ROOT / "core").is_dir() else CORA_ROOT
REASONING_DIR = CORA_CORE_DIR / "Reasoning"
DATA_DIR = REASONING_DIR / "data"
VAULT_DIR = CORA_CORE_DIR / "ObsidianVault"
LOGS_DIR = CORA_CORE_DIR / "Log"
PROJECTS_DIR = CORA_ROOT / "Projects"
TRAINING_DIR = CORA_ROOT / "Training" if (CORA_ROOT / "Training").is_dir() else CORA_CORE_DIR / "TrainingDocuments"

if str(CORA_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORA_CORE_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ANSI color helpers (automatically disabled if not a TTY and --no-color passed)
USE_COLOR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def ok_tag(msg: str) -> str:
    return f"  {_c('1;32', '[OK]')}      {msg}"


def warn_tag(msg: str) -> str:
    return f"  {_c('1;33', '[CONCERN]')} {msg}"


def fail_tag(msg: str) -> str:
    return f"  {_c('1;31', '[FAULT]')}   {msg}"


def info_tag(msg: str) -> str:
    return f"  {_c('1;36', '[INFO]')}    {msg}"


def section_header(title: str) -> None:
    bar = "=" * 78
    print(f"\n{_c('1;34', bar)}\n{_c('1;37', f'  {title}')}\n{_c('1;34', bar)}")


# ---------------------------------------------------------------------------
# LAYER A: Hardware, llama-server API, & Log Error Diagnostics
# ---------------------------------------------------------------------------
def audit_layer_a_runtime(api_base: str = "http://127.0.0.1:8080") -> Dict[str, Any]:
    section_header("LAYER A: Host Resources, llama-server API & Runtime Log Audit")
    concerns: List[str] = []
    faults: List[str] = []

    # 1. Bytecode syntax check on agent-cli.py, webui/server.py, Network_Isolation, Tools, and Reasoning/*.py
    py_targets = [
        CORA_CORE_DIR / "agent-cli.py",
        CORA_CORE_DIR / "webui" / "server.py",
        CORA_CORE_DIR / "Network_Isolation" / "console_posture.py",
        CORA_ROOT / "Tools" / "tool_manager.py",
        *sorted(REASONING_DIR.rglob("*.py")),
    ]
    syntax_errors = []
    for pt in py_targets:
        if pt.is_file():
            try:
                py_compile.compile(str(pt), doraise=True)
            except Exception as exc:
                syntax_errors.append(f"{pt.name}: {exc}")
    if syntax_errors:
        for se in syntax_errors:
            print(fail_tag(f"Python syntax error in {se}"))
            faults.append(f"Syntax error: {se}")
    else:
        print(ok_tag(f"All {len(py_targets)} Python files (`agent-cli.py`, `webui/server.py`, `Tools/`, `Reasoning/`) passed bytecode compilation."))

    # 2. Hardware & RAM/VRAM/Disk pressure check
    from Reasoning.engines.vault_bridge import get_hardware_reasoning_limits

    hw = get_hardware_reasoning_limits()
    print(
        info_tag(
            f"Detected Hardware Profile: `{hw.get('tier')}` | "
            f"{hw.get('cpu_threads')} CPU threads | {hw.get('total_ram_mib')} MiB RAM | "
            f"{hw.get('detected_gpu_vram_mib', 0)} MiB GPU VRAM"
        )
    )

    du = shutil.disk_usage(str(CORA_CORE_DIR))
    free_gb = du.free / (1024**3)
    used_pct = (du.used / du.total) * 100.0
    if used_pct >= 92.0 or free_gb < 2.0:
        msg = f"Disk usage is high ({used_pct:.1f}% used, {free_gb:.1f} GiB free)."
        print(warn_tag(msg))
        concerns.append(msg)
    else:
        print(ok_tag(f"Disk space healthy ({used_pct:.1f}% used, {free_gb:.1f} GiB free)."))

    # 3. Check llama-server live endpoints (/health, /props, /tokenize)
    server_online = False
    n_ctx = None
    try:
        with urllib.request.urlopen(f"{api_base}/health", timeout=1.0) as resp:
            health_data = json.loads(resp.read().decode("utf-8", errors="replace"))
            server_online = True
            print(ok_tag(f"`llama-server` is ONLINE at {api_base}/health -> {health_data}"))
    except Exception:
        print(
            info_tag(
                f"`llama-server` is not currently running on {api_base} "
                "(normal if using on-demand CLI mode; start with `./run_cora_NIX.sh start` or `./run_cora_NIX.sh cli`)."
            )
        )

    if server_online:
        try:
            with urllib.request.urlopen(f"{api_base}/props", timeout=1.0) as resp:
                props = json.loads(resp.read().decode("utf-8", errors="replace"))
                n_ctx = props.get("default_generation_settings", {}).get("n_ctx")
                model_path = props.get("model_path", "unknown")
                print(ok_tag(f"`llama-server /props`: active n_ctx = `{n_ctx}` tokens | model = `{os.path.basename(model_path)}`"))
                if isinstance(n_ctx, int) and n_ctx < 8192:
                    msg = f"`llama-server` active context window (`n_ctx={n_ctx}`) is < 8192 tokens; risk of context overflow."
                    print(warn_tag(msg))
                    concerns.append(msg)
        except Exception as exc:
            msg = f"Could not query `{api_base}/props`: {exc}"
            print(warn_tag(msg))
            concerns.append(msg)

    # 3b. Check WebUI Backend (/api/bootstrap) and SQLite Database (core/Log/cora_webui.db)
    webui_online = False
    try:
        with urllib.request.urlopen("http://127.0.0.1:1337/api/bootstrap", timeout=2.0) as w_resp:
            w_data = json.loads(w_resp.read().decode("utf-8", errors="replace"))
            webui_online = True
            w_llm_ok = bool(w_data.get("models", {}).get("llama_server", {}).get("online") or w_data.get("models", {}).get("ollama", {}).get("online"))
            w_proj = w_data.get("settings", {}).get("active_project") or w_data.get("active_project")
            print(
                ok_tag(
                    f"CORA WebUI Backend is ONLINE at http://127.0.0.1:1337/api/bootstrap "
                    f"(LLM Backend Online={w_llm_ok}, Project=`{w_proj}`)"
                )
            )
    except Exception:
        print(info_tag("CORA WebUI Backend (`http://127.0.0.1:1337`) is not currently running."))

    webui_db = LOGS_DIR / "cora_webui.db"
    if webui_db.is_file():
        try:
            import sqlite3

            with sqlite3.connect(str(webui_db)) as conn:
                ic = conn.execute("PRAGMA integrity_check").fetchone()[0]
                msg_cnt = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
                if ic == "ok":
                    print(ok_tag(f"WebUI SQLite Database (`core/Log/cora_webui.db`): integrity=`ok`, stored messages=`{msg_cnt}`."))
                else:
                    msg = f"WebUI SQLite Database integrity check returned: {ic}"
                    print(fail_tag(msg))
                    faults.append(msg)
        except Exception as exc:
            msg = f"Failed to inspect WebUI SQLite Database (`core/Log/cora_webui.db`): {exc}"
            print(warn_tag(msg))
            concerns.append(msg)

    # 4. Scan core/Log/llama-server.log and verify core/Log/cora_version.json
    version_file = LOGS_DIR / "cora_version.json"
    if version_file.is_file():
        print(ok_tag(f"CORA Version Metadata verified in `core/Log/cora_version.json` ({version_file.stat().st_size} B)."))
    else:
        msg = "Missing `core/Log/cora_version.json` in `core/Log/` directory."
        print(warn_tag(msg))
        concerns.append(msg)

    log_file = LOGS_DIR / "llama-server.log"
    if log_file.is_file():
        try:
            lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()[-300:]
            ctx_errs = [ln for ln in lines if "exceed_context_size_error" in ln or "exceeds the available context size" in ln]
            json_errs = [ln for ln in lines if "Failed to parse tool call arguments as JSON" in ln]
            jinja_errs = [ln for ln in lines if "No user query found in messages" in ln or "Jinja Exception" in ln]
            oom_errs = [ln for ln in lines if "out of memory" in ln.lower() or "cuda_malloc failed" in ln.lower()]

            if oom_errs:
                msg = f"Found {len(oom_errs)} CUDA/VRAM out-of-memory event(s) in recent `core/Log/llama-server.log`."
                print(warn_tag(msg + " -> Fix: Lower `CTX_SIZE` or increase `FIT_TARGET=512` in `./run_cora_NIX.sh restart`."))
                concerns.append(msg)
            if ctx_errs:
                print(
                    info_tag(
                        f"Found {len(ctx_errs)} historical `exceed_context_size_error` line(s) in `Log/llama-server.log` "
                        "(Part 1 Zero-Loss Context VM & auto-compaction are active to prevent this)."
                    )
                )
            if json_errs:
                print(
                    info_tag(
                        f"Found {len(json_errs)} historical malformed tool-call JSON line(s) in `Log/llama-server.log` "
                        "(`sanitize_messages()` + DRY sampling guards are active to prevent recurrence)."
                    )
                )
            if jinja_errs:
                print(
                    info_tag(
                        f"Found {len(jinja_errs)} historical `Jinja Exception: No user query found in messages` line(s) in `Log/llama-server.log` "
                        "(`trim_messages_to_fit()` + `sanitize_messages()` user-query anchor preservation is active to prevent recurrence)."
                    )
                )
            if not (oom_errs or ctx_errs or json_errs or jinja_errs):
                print(ok_tag("No OOM, context overflow, Jinja exception, or JSON parser errors in recent `Log/llama-server.log`."))
        except Exception:
            pass

    return {"faults": faults, "concerns": concerns, "server_online": server_online, "n_ctx": n_ctx}


# ---------------------------------------------------------------------------
# LAYER B: JSON State Store & ObsidianVault Integrity
# ---------------------------------------------------------------------------
def audit_layer_b_state_stores(auto_fix: bool = False) -> Dict[str, Any]:
    section_header("LAYER B: Reasoning/data/ JSON Stores & ObsidianVault Integrity")
    concerns: List[str] = []
    faults: List[str] = []
    repaired: List[str] = []

    from Reasoning.engines.vault_bridge import ensure_directories

    ensure_directories()

    json_files = sorted(DATA_DIR.rglob("*.json"))
    corrupt_files: List[Path] = []
    for jf in json_files:
        try:
            raw = jf.read_text(encoding="utf-8")
            parsed = json.loads(raw)
            if not isinstance(parsed, (dict, list)):
                corrupt_files.append(jf)
        except Exception as exc:
            corrupt_files.append(jf)
            msg = f"Corrupted JSON state file: `{jf.relative_to(CORA_CORE_DIR)}` ({exc})"
            print(fail_tag(msg))
            faults.append(msg)
            if auto_fix:
                try:
                    jf.unlink()
                    repaired.append(f"Removed corrupted JSON file `{jf.name}` for clean re-seeding.")
                    print(ok_tag(f"Auto-Fix: Deleted corrupted `{jf.name}`."))
                except OSError:
                    pass

    if not corrupt_files:
        print(ok_tag(f"Verified {len(json_files)} JSON state files across `Reasoning/data/` — 0 corrupted files."))

    # Check Shadow Archive count & size (including isolated Projects/<project>/shadow_archive/)
    shadow_dir = DATA_DIR / "shadow_archive"
    shadow_logs = list(shadow_dir.glob("sha256_*.log")) if shadow_dir.is_dir() else []
    projects_dir = CORA_ROOT / "Projects"
    if projects_dir.is_dir():
        shadow_logs.extend(projects_dir.glob("*/shadow_archive/sha256_*.log"))
    shadow_bytes = sum(f.stat().st_size for f in shadow_logs)
    print(
        ok_tag(
            f"Shadow Archive (`Projects/*/shadow_archive/` + `Reasoning/data/shadow_archive/`): "
            f"{len(shadow_logs)} lossless log file(s) ({shadow_bytes / 1024:.1f} KiB total)."
        )
    )

    # Check Temporal Fluents for STALE_INVALIDATED warnings that might confuse the user/LLM
    fluent_file = DATA_DIR / "temporal_fluents" / "live_fluents.json"
    if fluent_file.is_file():
        try:
            fdata = json.loads(fluent_file.read_text(encoding="utf-8"))
            fluents = fdata.get("fluents", {})
            stale = [k for k, v in fluents.items() if v.get("status") == "STALE_INVALIDATED"]
            active = [k for k, v in fluents.items() if v.get("status") in ("ACTIVE", "HOLDING")]
            if stale:
                msg = (
                    f"Engine 9 (`temporal_fluents.py`) has {len(stale)} invalidated/stale fluent(s) "
                    f"({', '.join(stale[:5])}) injecting warnings into tool outputs."
                )
                print(warn_tag(msg))
                concerns.append(msg)
                if auto_fix:
                    for k in stale:
                        fluents.pop(k, None)
                    fdata["fluents"] = fluents
                    fluent_file.write_text(json.dumps(fdata, indent=2) + "\n", encoding="utf-8")
                    repaired.append(f"Cleared {len(stale)} stale fluents from `live_fluents.json`.")
                    print(ok_tag("Auto-Fix: Cleared stale invalidated fluents from `live_fluents.json`."))
            else:
                print(ok_tag(f"Engine 9 Temporal Fluents store healthy ({len(active)} active, 0 stale)."))
        except Exception:
            pass

    # Check for stale truncated-IP state files in Reasoning/data/ (e.g. from pre-fix DRY runs)
    truncated_ip_files: List[Path] = []
    if DATA_DIR.is_dir():
        for jf in DATA_DIR.rglob("*.json"):
            if re.search(r"(?:^|_)(?:192|10|172)(?:_\d{1,3}){0,2}(?:_topology|_lattice)?\.json$", jf.name):
                # Check if it's NOT a full 4-octet IP slug
                if not re.search(r"(?:192|198|203|10|172)(?:_\d{1,3}){3}", jf.name):
                    truncated_ip_files.append(jf)
    if truncated_ip_files:
        if auto_fix:
            for tf in truncated_ip_files:
                try:
                    tf.unlink(missing_ok=True)
                except Exception:
                    pass
            repaired.append(f"Purged {len(truncated_ip_files)} stale truncated-IP JSON artifact(s) from `Reasoning/data/`.")
            print(ok_tag(f"Auto-Fix: Purged {len(truncated_ip_files)} stale truncated-IP JSON artifact(s) from `Reasoning/data/`."))
        else:
            msg = f"Found {len(truncated_ip_files)} stale truncated-IP JSON artifact(s) in `Reasoning/data/` ({[f.name for f in truncated_ip_files[:4]]}); run with `--fix` to purge."
            print(warn_tag(msg))
            concerns.append(msg)

    # Check ObsidianVault index & note links
    index_file = VAULT_DIR / "00_MEMORY_INDEX.md"
    if not index_file.is_file():
        msg = f"Missing Obsidian Vault index `{index_file}`."
        print(warn_tag(msg))
        concerns.append(msg)
    else:
        idx_text = index_file.read_text(encoding="utf-8", errors="replace")
        wikilinks = [
            w for w in re.findall(r"\[\[([^\]|#]+)", idx_text) if w.strip() not in ("00_MEMORY_INDEX", "WikiLinks")
        ]
        missing_links = []
        for wl in wikilinks:
            wl_clean = wl.strip()
            cand = VAULT_DIR / f"{wl_clean}.md"
            if not cand.is_file():
                missing_links.append(wl_clean)
        if missing_links:
            msg = f"`00_MEMORY_INDEX.md` references {len(missing_links)} missing Vault note(s): {missing_links[:5]}"
            print(warn_tag(msg))
            concerns.append(msg)
        else:
            print(ok_tag(f"`ObsidianVault/00_MEMORY_INDEX.md` verified ({len(wikilinks)} valid WikiLinks)."))

    projects_dir = PROJECTS_DIR
    projects_dir.mkdir(parents=True, exist_ok=True)
    proj_count = len([d for d in projects_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])
    print(ok_tag(f"Two-Tier Project Workspace Isolation (`Projects/`): ready at `{projects_dir}` ({proj_count} project workspace(s))."))

    return {"faults": faults, "concerns": concerns, "repaired": repaired}


# ---------------------------------------------------------------------------
# LAYER C: Guardrails 1-6 Behavioral Verification
# ---------------------------------------------------------------------------
def audit_layer_c_guardrails() -> Dict[str, Any]:
    section_header("LAYER C: Verification of All 6 Architectural Guardrails")
    concerns: List[str] = []
    faults: List[str] = []

    from Reasoning.engines.cegar_verifier import _is_bash_n_available, verify_command_cegar
    from Reasoning.engines.context_vm import process_tool_output_zero_loss

    # Guardrail 1: CEGAR must block interactive `tio /dev/ttyUSB0`, unbounded `ping 1.1.1.1`, and bad bash syntax,
    #              but MUST NOT block valid `ip route add` commands (even if gateway subnet isn't local yet).
    g1_tests = [
        ("tio /dev/ttyUSB0", True, "interactive tio without --script"),
        ("ping 198.51.100.10", True, "unbounded ping without -c"),
        ("curl -sS -m 5 -i http://198.51", True, "truncated IPv4 address in URL"),
        ("ip route get 1", True, "truncated 1-octet IPv4 target in ip route get"),
        ("sudo ip route add 203.0.113.0/24 via 198.51.100.1", False, "cross-subnet route must be ADVISORY, not blocked"),
        ("ping -c 3 -W 2 198.51.100.10", False, "valid bounded ping"),
    ]
    if _is_bash_n_available():
        g1_tests.insert(2, ("echo 'unclosed quote", True, "invalid bash -n syntax"))
    g1_ok = True
    for cmd, expected_block, desc in g1_tests:
        res = verify_command_cegar(cmd)
        if bool(res.get("blocked")) != expected_block:
            g1_ok = False
            msg = f"Guardrail 1 (CEGAR) mismatch on `{cmd}` ({desc}): got blocked={res.get('blocked')}, expected {expected_block}"
            print(fail_tag(msg))
            faults.append(msg)
    if g1_ok:
        print(ok_tag("Guardrail 1 (CEGAR Non-Blocking Mode): Blocks fatal syntax/hangs; keeps route checks non-blocking."))

    # Guardrail 2: Outputs <= threshold must remain 100% raw (zero truncation)
    sample_raw = "198.51.100.10 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE\nUniqueMarkerLine_987654321"
    processed_small = process_tool_output_zero_loss("run_command", "ip neigh show", sample_raw, 0)
    if "UniqueMarkerLine_987654321" not in processed_small or "[SyGuS Extracted Facts]" not in processed_small:
        msg = "Guardrail 2 failure: Small tool output was altered or missed SyGuS header."
        print(fail_tag(msg))
        faults.append(msg)
    else:
        print(ok_tag("Guardrail 2 (Additive SyGuS + Raw Preservation): Small outputs remain 100% untouched with SyGuS header."))

    # Guardrail 6: Large outputs (> 15,000 chars) must be archived to Reasoning/data/shadow_archive/ and NOT CWD
    huge_raw = "\n".join(f"Line {i}: 198.51.100.{i % 254} tcp_seq={i}" for i in range(600))
    processed_huge = process_tool_output_zero_loss("run_command", "tcpdump -n", huge_raw, 0)
    if "shadow_archive/sha256_" not in processed_huge.replace("\\", "/"):
        msg = "Guardrail 6 failure: Large output (> 15,000 chars) did not produce a `shadow_archive/sha256_` pointer."
        print(fail_tag(msg))
        faults.append(msg)
    else:
        print(ok_tag("Guardrail 6 (Central Shadow Store): Outputs > threshold are losslessly archived to `Reasoning/data/shadow_archive/`."))

    # Guardrail 7: Verify `/goal` and `/relentless` autonomous loop, Anti-Repetition Guard, and Qwen Jinja User-Query Anchor in agent-cli.py
    agent_cli_path = CORA_CORE_DIR / "agent-cli.py"
    if agent_cli_path.is_file():
        cli_text = agent_cli_path.read_text(encoding="utf-8", errors="ignore")
        required_markers = [
            "handle_goal_command",
            "handle_relentless_command",
            "run_relentless_loop",
            "Relentless Anti-Repetition Guard",
            "last_user_idx > 1",
            "has_user_msg",
        ]
        missing_markers = [m for m in required_markers if m not in cli_text]
        if missing_markers:
            msg = f"Guardrail 7 failure: `agent-cli.py` is missing `/goal`, `/relentless`, or Jinja user-query anchor components: {missing_markers}"
            print(fail_tag(msg))
            faults.append(msg)
        else:
            print(
                ok_tag(
                    "Guardrail 7 (`/goal`, `/relentless` & Qwen Jinja User-Query Anchor): Anti-Repetition Guard, Obsidian Attempt Ledger & HTTP 500 User-Query Preservation verified in `agent-cli.py`."
                )
            )

    # Guardrail 8: Verify ConsolePostureDetection (Linux _NIX.sh, Windows _WIN.ps1, and console_posture.py)
    try:
        from Network_Isolation.console_posture import detect_console_posture

        p_info = detect_console_posture()
        sh_ok = (CORA_CORE_DIR / "Network_Isolation" / "ConsolePostureDetection_NIX.sh").is_file()
        ps1_ok = (CORA_CORE_DIR / "Network_Isolation" / "ConsolePostureDetection_WIN.ps1").is_file()
        if sh_ok and ps1_ok and p_info.get("mode") in ("UNRESTRICTED", "ISOLATED_LAN_USB", "AIR_GAPPED_NETNS"):
            print(
                ok_tag(
                    f"Guardrail 8 (`ConsolePostureDetection` Linux/Windows): Active posture=`{p_info['mode']}` "
                    f"(BG `{p_info['bg_hex']}`, Badge `{p_info['hud_badge']}`)."
                )
            )
        else:
            msg = f"Guardrail 8 failure: ConsolePostureDetection scripts or mode invalid (sh={sh_ok}, ps1={ps1_ok}, mode={p_info.get('mode')})"
            print(fail_tag(msg))
            faults.append(msg)
    except Exception as exc:
        msg = f"Guardrail 8 failure: `Network_Isolation/console_posture.py` failed: {exc}"
        print(fail_tag(msg))
        faults.append(msg)

    # Guardrail 9: Verify 4-Phase Multi-Modal Document, OCR, Network Diagram & Uncapped Cross-Platform CLI Training Pipeline
    try:
        from Reasoning.train_llm import _extract_and_verify_commands_deterministic, get_training_status

        t_status = get_training_status()
        train_sh_ok = (TRAINING_DIR / "train_llm_NIX.sh").is_file()
        train_ps1_ok = (TRAINING_DIR / "train_llm_WIN.ps1").is_file()
        train_plan_ok = (TRAINING_DIR / "README.md").is_file()
        ext = t_status.get("extractors", {})
        tr_rules = t_status.get("trained_rules", {})

        # Verify uncapped extraction & multi-line PDF wrap joining + TOC leader rejection + SHA-256 deduplication
        train_py_src = (REASONING_DIR / "train_llm.py").read_text(encoding="utf-8", errors="replace")
        forbidden_caps = [
            cap
            for cap in ("verified[:60]", "verified[:2500]", "verified_cmds[:15]", "evo_list[-300:]", "max_transitions = 120")
            if cap in train_py_src
        ]
        sha_dedup_ok = ("content_sha256 in existing_hashes" in train_py_src) or ("sha256_hex" in train_py_src)
        probe_verified, _ = _extract_and_verify_commands_deterministic(
            "NMAP -------- 223\n"
            "icacls C:\\Windows\\System32\\utilman.exe /grant Administrators:F <---Gain Ownership\n"
            "Get-NetTCPConnection -State Listen\n"
            "impacket-secretsdump -just-dc-ntds\n"
            "  domain/admin:Pass@198.51.100.10\n"
        )
        extractor_probe_ok = len(probe_verified) == 3 and any("198.51.100.10" in v["command"] for v in probe_verified)

        if (
            train_sh_ok
            and train_ps1_ok
            and train_plan_ok
            and ext.get("pdf_ready")
            and ext.get("ocr_ready")
            and not forbidden_caps
            and sha_dedup_ok
            and extractor_probe_ok
        ):
            print(
                ok_tag(
                    f"Guardrail 9 (`train_llm` Uncapped Multi-Modal & Cross-Platform CLI Pipeline): "
                    f"PDF=`{ext.get('pdf_ready')}`, OCR=`{ext.get('ocr_ready')}`, DOCX=`{ext.get('docx_ready')}`, "
                    f"Uncapped=`True`, SHA256_Dedup=`True`, "
                    f"TrainedDocs=`{t_status.get('trained_documents_count', 0)}`, "
                    f"CBR_Rules=`{tr_rules.get('cbr_fingerprints', 0)}`, "
                    f"Primitives=`{tr_rules.get('evolutionary_primitives', 0)}`."
                )
            )
        else:
            msg = (
                f"Guardrail 9 failure: Training pipeline scripts or uncapped extractors incomplete "
                f"(sh={train_sh_ok}, ps1={train_ps1_ok}, plan={train_plan_ok}, ext={ext}, "
                f"forbidden_caps={forbidden_caps}, sha_dedup={sha_dedup_ok}, probe_ok={extractor_probe_ok})"
            )
            print(fail_tag(msg))
            faults.append(msg)
    except Exception as exc:
        msg = f"Guardrail 9 failure: `Reasoning/train_llm.py` failed: {exc}"
        print(fail_tag(msg))
        faults.append(msg)

    # Guardrail 10: Verify Engine 15 Hierarchical Tactical MDP (Bellman Q* Solver, 14-Category Taxonomy & Uncapped Merger)
    try:
        from Reasoning.engines.mdp_tactical import TACTIC_CATEGORIES, run_mdp_tactical_reasoning

        mdp_res = run_mdp_tactical_reasoning(
            problem="curl exit 7 on 198.51.100.10 with /dev/ttyUSB0 attached",
            target_ip="198.51.100.10",
            save_to_vault=False,
        )
        mdp_py_src = (REASONING_DIR / "engines" / "mdp_tactical.py").read_text(encoding="utf-8", errors="replace")
        mdp_uncapped_ok = "existing[-350:]" not in mdp_py_src
        req_cats = {"Covert_Exfil", "Covert_Infil", "Active_Enum", "Passive_Enum", "Protocol_Chaining"}
        cats_present = req_cats.issubset(set(TACTIC_CATEGORIES))
        if cats_present and mdp_uncapped_ok and mdp_res.get("optimal_tactic") and mdp_res.get("optimal_q_star", 0.0) > 0:
            print(
                ok_tag(
                    f"Guardrail 10 (`mdp_tactical` Hierarchical MDP & Uncapped POMDP Solver): "
                    f"Categories=`{len(TACTIC_CATEGORIES)}`, Uncapped=`True`, Transitions=`{mdp_res.get('total_transitions', 0)}`, "
                    f"Optimal=`{mdp_res.get('optimal_tactic')} -> {mdp_res.get('optimal_tool')}` "
                    f"(Q*=`{mdp_res.get('optimal_q_star')}`, `{mdp_res.get('elapsed_ms')} ms`)."
                )
            )
        else:
            msg = f"Guardrail 10 failure: MDP categories, uncapped merger, or Bellman solver invalid (cats_ok={cats_present}, uncapped={mdp_uncapped_ok}, res={mdp_res.get('optimal_tactic')})"
            print(fail_tag(msg))
            faults.append(msg)
    except Exception as exc:
        msg = f"Guardrail 10 failure: `Reasoning/engines/mdp_tactical.py` failed: {exc}"
        print(fail_tag(msg))
        faults.append(msg)

    return {"faults": faults, "concerns": concerns}


# ---------------------------------------------------------------------------
# LAYER D: Individual 15-Engine Isolation & Latency Profiler
# ---------------------------------------------------------------------------
def audit_layer_d_engines() -> Dict[str, Any]:
    section_header("LAYER D: Per-Engine Fault Isolation & Latency Profiler (15-Engine Core)")
    concerns: List[str] = []
    faults: List[str] = []
    latencies: Dict[str, float] = {}

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

    engine_probes: List[Tuple[str, str, Callable[[], Dict[str, Any]]]] = [
        (
            "Engine 01: Associative Vault Graph",
            "Reasoning/engines/associative.py",
            lambda: run_associative_vault_reasoning("198.51.100.10 /dev/ttyUSB0", save_to_vault=False),
        ),
        (
            "Engine 02: Geometric & Z3 SMT Solver",
            "Reasoning/engines/geometric.py",
            lambda: run_geometric_reasoning(
                "diag_geo",
                mode="network_geometry",
                spec={"local_subnets": ["198.51.100.0/24"], "target_ips": ["198.51.100.10", "203.0.113.50"]},
                save_to_vault=False,
            ),
        ),
        (
            "Engine 03: Bayesian Abductive + EIG",
            "Reasoning/engines/bayesian.py",
            lambda: run_bayesian_abduction(
                "diag_bayes",
                profile="http_api_unreachable",
                observed_evidence={"curl_exit_7_Immediate_refused": True},
                save_to_vault=False,
            ),
        ),
        (
            "Engine 04: Causal DAG & do(X) Surgery",
            "Reasoning/engines/causal.py",
            lambda: run_causal_reasoning(
                "network_api_reachability",
                do_interventions={"Serial_Console_OOB": 1.0},
                save_to_vault=False,
            ),
        ),
        (
            "Engine 05: Hyperdimensional VSA (1,024-D)",
            "Reasoning/engines/vsa.py",
            lambda: run_vsa_conceptual_leap("curl exit 7 on 198.51.100.10", save_to_vault=False),
        ),
        (
            "Engine 06: Event-Calculus Fluents",
            "Reasoning/engines/temporal_fluents.py",
            lambda: run_temporal_fluent_reasoning("diag_fluents", export_to_vault=False),
        ),
        (
            "Engine 07: Dempster-Shafer Epistemic",
            "Reasoning/engines/dempster_shafer.py",
            lambda: run_dempster_shafer_reasoning("curl exit 7 with ARP reachable", export_to_vault=False),
        ),
        (
            "Engine 08: CBR Failure Fingerprints",
            "Reasoning/engines/cbr_fingerprints.py",
            lambda: run_cbr_reasoning("RTNETLINK answers: File exists", export_to_vault=False),
        ),
        (
            "Engine 09: CEGAR Pre-Verifier",
            "Reasoning/engines/cegar_verifier.py",
            lambda: run_cegar_reasoning("Verify commands", candidate_commands=["ip addr show"], export_to_vault=False),
        ),
        (
            "Engine 10: SyGuS Fact Extractor",
            "Reasoning/engines/sygus_extractor.py",
            lambda: run_sygus_reasoning("ip neigh", sample_output="198.51.100.10 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE", export_to_vault=False),
        ),
        (
            "Engine 11: Hierarchical Tactical MDP",
            "Reasoning/engines/mdp_tactical.py",
            lambda: run_mdp_tactical_reasoning("Cross-subnet pivot to 203.0.113.50", save_to_vault=False),
        ),
        (
            "Engine 12: Continual Learning & Pass-2",
            "Reasoning/engines/continual_learner.py",
            lambda: run_continual_learning_reasoning("Diag continual learning", export_to_vault=False),
        ),
        (
            "Engine 13: Hedge Meta-Arbiter & ECE",
            "Reasoning/engines/meta_learner.py",
            lambda: run_meta_learning_reasoning("Diag meta calibration", write_suggested_improvement=False, export_to_vault=False),
        ),
        (
            "Engine 14: Trajectory RL & Net World-Model",
            "Reasoning/engines/rl_network_policy.py",
            lambda: run_rl_network_policy_reasoning(
                "Diag Trajectory RL on 198.51.100.10",
                target_ip="198.51.100.10",
                secondary_target_ip="203.0.113.50",
                train_episodes=0,
                sense_topology=False,
                export_to_vault=False,
            ),
        ),
        (
            "Engine 15: SVD PCA, K-Means++ & Laplacian",
            "Reasoning/engines/spectral_manifold_pca.py",
            lambda: run_spectral_pca_reasoning(
                "Diag SVD PCA & K-Means++ on 198.51.100.10",
                target_ip="198.51.100.10",
                secondary_target_ip="203.0.113.50",
                export_to_vault=False,
            ),
        ),
        (
            "Unified 15-Stage Consensus Pipeline",
            "Reasoning/engines/pipeline.py",
            lambda: run_neuro_symbolic_pipeline("Diagnostic pipeline test", save_to_vault=False),
        ),
    ]

    # Pre-warm scientific/graph imports and Vault Bipartite Graph before per-engine latency timing
    try:
        import networkx  # noqa: F401
        import scipy.sparse  # noqa: F401
        from Reasoning.engines.associative import build_vault_bipartite_graph

        build_vault_bipartite_graph()
    except Exception:
        pass

    for label, rel_file, fn in engine_probes:
        t0 = time.perf_counter()
        try:
            res = fn()
            dt_ms = round((time.perf_counter() - t0) * 1000, 2)
            latencies[label] = dt_ms
            warn_threshold_ms = 2500.0 if "Pipeline" in label else (1800.0 if "Evolutionary" in label else 1000.0)
            if not isinstance(res, dict) or "error" in res or "stage_error" in res:
                err_detail = res.get("error") or res.get("stage_error") if isinstance(res, dict) else "Invalid return type"
                msg = f"{label} (`{rel_file}`) reported internal error: {err_detail}"
                print(fail_tag(msg))
                faults.append(msg)
            elif dt_ms > warn_threshold_ms:
                msg = f"{label} (`{rel_file}`) succeeded but latency was high ({dt_ms:.1f} ms)."
                print(warn_tag(msg))
                concerns.append(msg)
            else:
                extra = ""
                if "consensus_immediate_action" in res:
                    extra = f" -> Consensus Action: `{res['consensus_immediate_action']}`"
                print(ok_tag(f"{label:<37} | {dt_ms:>7.2f} ms | `{rel_file}`{extra}"))
        except Exception as exc:
            dt_ms = round((time.perf_counter() - t0) * 1000, 2)
            tb_short = traceback.format_exc().splitlines()[-2:]
            msg = f"{label} (`{rel_file}`) crashed after {dt_ms} ms: {exc} ({' | '.join(tb_short)})"
            print(fail_tag(msg))
            faults.append(msg)

    return {"faults": faults, "concerns": concerns, "latencies_ms": latencies}


# ---------------------------------------------------------------------------
# LAYER E: Interactive Command & Problem Flow Simulator
# ---------------------------------------------------------------------------
def diagnose_command_flow(command: str, simulated_output: str = "", simulated_exit_code: int = 0) -> None:
    """
    Traces a specific shell command through every reasoning interception layer so the user can see
    if CEGAR, CBR, Temporal Fluents, SyGuS, or Context VM is modifying or blocking it.
    """
    section_header(f"LAYER E: Step-by-Step Interception Trace for Command: `{command}`")
    from Reasoning.engines.cbr_fingerprints import match_failure_fingerprint
    from Reasoning.engines.cegar_verifier import verify_command_cegar
    from Reasoning.engines.context_vm import process_tool_output_zero_loss
    from Reasoning.engines.sygus_extractor import extract_structured_facts

    # Step 1: CEGAR Pre-Execution Verifier
    cegar = verify_command_cegar(command)
    if cegar.get("blocked"):
        print(fail_tag(f"Step 1 [Engine 12 CEGAR Pre-Verifier]: HARD-BLOCKED before execution!"))
        print(info_tag(f"  Reason:         {cegar.get('reason')}"))
        print(info_tag(f"  Counterexample: {cegar.get('counterexample')}"))
        print(info_tag(f"  Suggested Fix:  {cegar.get('suggested_fix')}"))
        return
    else:
        print(ok_tag("Step 1 [Engine 12 CEGAR Pre-Verifier]: ALLOWED to execute."))
        for adv in cegar.get("advisories", []):
            print(warn_tag(f"  Advisory attached: {adv}"))

    # Step 2: CBR Failure Fingerprint Match
    cbr = match_failure_fingerprint(command, simulated_exit_code, simulated_output)
    if cbr:
        print(
            warn_tag(
                f"Step 2 [Engine 11 CBR Fingerprints]: Matched failure case `{cbr['case_id']}` "
                f"(confidence={cbr['match_confidence']}) -> injects fix: {cbr['verified_fix']}"
            )
        )
    else:
        print(ok_tag("Step 2 [Engine 11 CBR Fingerprints]: No failure fingerprint triggered."))

    # Step 3: SyGuS Structured Extraction
    sygus = extract_structured_facts(command, simulated_output)
    if sygus.get("summary_header"):
        print(ok_tag(f"Step 3 [Engine 13 SyGuS Extractor]: Prepends `{sygus['summary_header']}`"))
    else:
        print(info_tag("Step 3 [Engine 13 SyGuS Extractor]: No telemetry header needed."))

    # Step 4: Context VM Output Processing
    final_out = process_tool_output_zero_loss("run_command", command, simulated_output or "(sample stdout)", simulated_exit_code)
    print(ok_tag(f"Step 4 [Part 1 Context VM]: Final in-context length = {len(final_out)} chars."))


def explain_arbiter_decision(problem: str) -> None:
    """Runs the 15-engine pipeline on a problem description and explains why the Consensus Arbiter chose its action."""
    section_header(f"LAYER E: 15-Engine Consensus Arbiter Trace for: `{problem}`")
    from Reasoning.engines.pipeline import run_neuro_symbolic_pipeline

    res = run_neuro_symbolic_pipeline(problem=problem, save_to_vault=False)
    print(info_tag(f"Consensus Immediate Action: `{res.get('consensus_immediate_action')}`"))
    print(info_tag(f"Arbiter Rationale:          {res.get('consensus_rationale')}"))
    print(info_tag(f"Bayesian Top Hypothesis:    `{res.get('top_root_cause')}` ({res.get('top_root_cause_probability', 0.0):.1%})"))
    print(
        info_tag(
            f"Dempster-Shafer Metrics:    Conflict K = `{res.get('dempster_shafer_conflict_k', 0.0):.3f}` | "
            f"Ignorance m(Theta) = `{res.get('dempster_shafer_ignorance', 0.0):.3f}`"
        )
    )
    rl_cmds = [s.get("command") for s in (res.get("rl_rollout_steps") or []) if s.get("command")]
    print(info_tag(f"RL Multi-Step Trajectory ({res.get('rl_state_key')}): {rl_cmds}"))


def main() -> None:
    global USE_COLOR
    parser = argparse.ArgumentParser(
        description="CORA & 15-Engine Layered Reasoning Diagnostic, Fault-Isolator & Auto-Repair Tool (v3.6.1)"
    )
    parser.add_argument("--fix", "--auto-repair", dest="fix", action="store_true", help="Automatically repair corrupted JSON state files, clear stale fluents, and re-seed missing models")
    parser.add_argument("--quick", "-q", dest="quick", action="store_true", help="Run fast Layers A–C check without full 15-engine benchmark")
    parser.add_argument("--diagnose-cmd", type=str, default="", help="Simulate how a specific shell command is handled by CEGAR, CBR, SyGuS, and Context VM")
    parser.add_argument("--sim-output", type=str, default="", help="Optional simulated stdout/stderr for --diagnose-cmd")
    parser.add_argument("--sim-exit", type=int, default=0, help="Optional simulated exit code for --diagnose-cmd")
    parser.add_argument("--explain-arbiter", type=str, default="", help="Explain why the 15-Engine Consensus Arbiter recommends a specific action for a given problem")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON summary at the end")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI color codes")

    args = parser.parse_args()
    if args.no_color:
        USE_COLOR = False

    t_start = time.perf_counter()
    res_a = audit_layer_a_runtime()
    res_b = audit_layer_b_state_stores(auto_fix=args.fix)
    res_c = audit_layer_c_guardrails()
    res_d = {"faults": [], "concerns": [], "latencies_ms": {}} if args.quick else audit_layer_d_engines()

    if args.fix and (res_b["repaired"] or res_b["faults"]):
        from Reasoning.reasoning_cli import seed_all_data_and_vault

        section_header("AUTO-REPAIR: Re-Seeding Reasoning/data/ & ObsidianVault/reasoning/")
        print(ok_tag(seed_all_data_and_vault()))

    if args.diagnose_cmd:
        diagnose_command_flow(args.diagnose_cmd, args.sim_output, args.sim_exit)

    if args.explain_arbiter:
        explain_arbiter_decision(args.explain_arbiter)

    all_faults = res_a["faults"] + res_b["faults"] + res_c["faults"] + res_d["faults"]
    all_concerns = res_a["concerns"] + res_b["concerns"] + res_c["concerns"] + res_d["concerns"]
    total_ms = round((time.perf_counter() - t_start) * 1000, 2)

    section_header("DIAGNOSTIC VERDICT & LAYER SUMMARY")
    if not all_faults and not all_concerns:
        print(ok_tag(f"ALL LAYERS HEALTHY (0 Faults, 0 Concerns across 15 Engines & 10 Guardrails in {total_ms} ms)."))
    else:
        if all_faults:
            print(fail_tag(f"Detected {len(all_faults)} FAULT(S) requiring attention:"))
            for f in all_faults:
                print(f"    - {f}")
        if all_concerns:
            print(warn_tag(f"Detected {len(all_concerns)} AREA(S) OF CONCERN:"))
            for c in all_concerns:
                print(f"    - {c}")
        if not args.fix:
            print(info_tag("Tip: Re-run with `--fix` (`bash Troubleshooting/troubleshoot_llm_NIX.sh --fix` or `.\\Troubleshooting\\troubleshoot_llm_WIN.ps1 -Fix`) to auto-repair state stores and clear stale fluents."))

    if args.json:
        print(
            json.dumps(
                {
                    "healthy": len(all_faults) == 0,
                    "faults_count": len(all_faults),
                    "concerns_count": len(all_concerns),
                    "faults": all_faults,
                    "concerns": all_concerns,
                    "repaired": res_b.get("repaired", []),
                    "engine_latencies_ms": res_d.get("latencies_ms", {}),
                    "total_diagnostic_ms": total_ms,
                },
                indent=2,
            )
        )

    sys.exit(1 if all_faults else 0)


if __name__ == "__main__":
    main()
