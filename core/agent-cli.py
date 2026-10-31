#!/usr/bin/env python3
"""
Interactive CORA System Agent CLI for Qwen3.8-27B & Qwen3.5-9B (via local llama-server)
with integrated two-tier Obsidian Knowledge Vault (CORA/core/ObsidianVault).

Tools provided to the LLM:
  - scan_target        : Scan a URL/API/host and auto-save the report to ObsidianVault/targets/
  - vault_save_note    : Save/update distilled knowledge, working curl commands, or project notes
                         in ObsidianVault/ and auto-index them in 00_MEMORY_INDEX.md
  - vault_search       : Search across all Markdown notes in ObsidianVault/
  - vault_read_note    : Read a specific note from ObsidianVault/ on demand
  - run_shell_command  : Execute bash/curl commands on the host system (with smart output compaction)
  - write_file         : Create or overwrite documents/scripts/files
  - edit_file          : Replace text inside an existing file
  - read_file          : Read local files
  - list_directory     : List files and folders in a directory
"""
from datetime import datetime
import atexit
import ctypes
import html
import json
import os
import platform
import re
try:
    import readline  # Enables arrow-key history and line editing in input()
except ImportError:
    readline = None  # type: ignore[assignment]
import shutil
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

if os.name == "nt":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            try:
                _stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
    try:
        # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004) on Windows stdout/stderr handles
        _k32 = ctypes.windll.kernel32
        for _std_id in (-11, -12):
            _h = _k32.GetStdHandle(_std_id)
            _mode = ctypes.c_uint32()
            if _k32.GetConsoleMode(_h, ctypes.byref(_mode)):
                _k32.SetConsoleMode(_h, _mode.value | 0x0004)
    except Exception:
        pass


def _rl_wrap(ansi_seq: str) -> str:
    """Wrap non-printing ANSI escape sequences in \\001..\\002 only when GNU readline is active."""
    if readline is not None and os.name != "nt":
        return f"\001{ansi_seq}\002"
    return ansi_seq

BASE_DIR = Path(__file__).resolve().parent
CORA_ROOT = BASE_DIR.parent if BASE_DIR.name.lower() == "core" else BASE_DIR
LOG_DIR = BASE_DIR / "Log"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
VAULT_DIR = Path(os.environ.get("OBSIDIAN_VAULT_DIR", str(BASE_DIR / "ObsidianVault"))).resolve()
PROJECTS_DIR = Path(
    os.environ.get("CORA_PROJECTS_DIR")
    or str(CORA_ROOT / "Projects")
).resolve()
INDEX_FILE = VAULT_DIR / "00_MEMORY_INDEX.md"

API_URL = os.environ.get("LLAMA_API_URL", "http://127.0.0.1:8080/v1/chat/completions")
MODEL_NAME = os.environ.get("MODEL_ALIAS", "Qwen3.8-27B-Uncensored-Q3_K_M")
SKIP_PERMISSIONS = os.environ.get("SKIP_PERMISSIONS", "0") == "1"
def _default_cli_limits() -> tuple[int, int]:
    try:
        from Reasoning.engines.vault_bridge import get_hardware_reasoning_limits

        hw = get_hardware_reasoning_limits()
        return int(hw.get("max_tool_output_chars", 3500)), int(hw.get("max_history_chars", 24000))
    except Exception:
        return 3500, 24000


_DEF_TOOL_CHARS, _DEF_HIST_CHARS = _default_cli_limits()
MAX_TOOL_OUTPUT_CHARS = int(os.environ.get("MAX_TOOL_OUTPUT_CHARS", str(_DEF_TOOL_CHARS)))
MAX_HISTORY_CHARS = int(os.environ.get("MAX_HISTORY_CHARS", str(_DEF_HIST_CHARS)))
VALID_CATEGORIES = ("targets", "commands", "projects", "knowledge", "reasoning")
ACTIVE_PROJECT: str = ""
ACTIVE_GOAL: str = ""
ACTIVE_PERSONALITY_MODE: str = "DEFAULT"
CLI_OVERRIDE_BLUE_IFACES: str = os.environ.get("LLM_CLI_BLUE_IFACES", "").strip()
RELENTLESS_MODE: bool = os.environ.get("RELENTLESS_MODE", "0") == "1"
MAX_RELENTLESS_WAVES: int = int(os.environ.get("MAX_RELENTLESS_WAVES", "15"))
CURRENT_WAVE: int = 0
ATTEMPT_LEDGER: list[dict] = []
ACTIVE_POSTURE: dict = {}
HUD_ENABLED = os.environ.get("HUD_ENABLED", "1") != "0"
KEEP_SERVER_ON_EXIT: bool = os.environ.get("KEEP_SERVER_ON_EXIT", "0") == "1"
_SPECULATIVE_CACHE_REF = None
_CLI_SHUTDOWN_DONE: bool = False
_ACTIVE_MESSAGES_REF: list = []
SESSION_STATE_DIR = BASE_DIR / "Reasoning" / "data" / "sessions"
LAST_SESSION_FILE = SESSION_STATE_DIR / "last_cli_session.json"
RELENTLESS_LEDGER_FILE = SESSION_STATE_DIR / "relentless_ledger.json"
ACTIVE_SESSION_MODE_FILE = BASE_DIR / "Log" / "active_session_mode.env"


def get_configured_blue_interfaces() -> tuple[list[str], str]:
    """
    Return `(allowed_ifaces_list, source_label)` for Blue network isolation:
      - If the user started the session with a CLI switch override (`-netiso blue <ifaces>` or `-blue <ifaces>`),
        `CLI_OVERRIDE_BLUE_IFACES` overrides `Network_Isolation/network_isolation.conf`.
      - Otherwise, reads `blue_allowed_ifaces` from `Network_Isolation/network_isolation.conf`.
    """
    cli_ovr = (CLI_OVERRIDE_BLUE_IFACES or os.environ.get("LLM_CLI_BLUE_IFACES", "")).strip()
    if cli_ovr:
        parsed = [x.strip() for x in re.split(r"[,\s]+", cli_ovr) if x.strip() and x.strip() != "lo"]
        if parsed:
            return parsed, "CLI switch override"
    try:
        from Network_Isolation.console_posture import load_network_isolation_config

        cfg = load_network_isolation_config()
        cfg_ifaces = [x.strip() for x in (cfg.get("blue_allowed_ifaces") or ["eth0", "eth1"]) if str(x).strip() and str(x).strip() != "lo"]
        if cfg_ifaces:
            return cfg_ifaces, "network_isolation.conf"
    except Exception:
        pass
    return ["eth0", "eth1"], "network_isolation.conf"


def apply_network_isolation_level(level: str, cli_ifaces: str = "", record_cli_override: bool = False) -> tuple[str, list[str]]:
    """
    Configure the active Network Isolation Level (`RED`, `WHITE`, or `BLUE`) and optional
    CLI-specified interface allowlist for `BLUE` mode (overriding `network_isolation.conf`).
    Returns `(normalized_level, allowed_ifaces_list)`.
    """
    global CLI_OVERRIDE_BLUE_IFACES
    raw = (level or "").strip().lower()
    extra_ifaces = (cli_ifaces or "").strip()
    if ":" in raw and not extra_ifaces:
        raw, extra_ifaces = raw.split(":", 1)
    elif "=" in raw and not extra_ifaces:
        raw, extra_ifaces = raw.split("=", 1)

    try:
        from Network_Isolation.console_posture import load_network_isolation_config

        cfg = load_network_isolation_config()
    except Exception:
        cfg = {"blue_allowed_ifaces": ["eth0", "eth1"]}

    if raw in ("white", "netns", "namespace", "airgap", "airgapped", "air_gapped_netns"):
        os.environ["LLM_ISOLATION_MODE"] = "WHITE"
        os.environ["LLM_POSTURE_OVERRIDE"] = "WHITE"
        os.environ["LLM_ALLOWED_IFACES"] = "lo"
        return "WHITE", ["lo"]

    if raw in ("blue", "lan", "usb", "isolated", "isolated_lan_usb", "iface", "interfaces"):
        if extra_ifaces:
            parsed = [x.strip() for x in re.split(r"[,\s]+", extra_ifaces) if x.strip() and x.strip() != "lo"]
            if record_cli_override and parsed:
                CLI_OVERRIDE_BLUE_IFACES = ",".join(parsed)
                os.environ["LLM_CLI_BLUE_IFACES"] = CLI_OVERRIDE_BLUE_IFACES
        else:
            parsed, _ = get_configured_blue_interfaces()
        if not parsed:
            parsed = ["eth0", "eth1"]
        csv_ifaces = ",".join(parsed)
        os.environ["LLM_ISOLATION_MODE"] = "BLUE"
        os.environ["LLM_POSTURE_OVERRIDE"] = "BLUE"
        os.environ["LLM_ALLOWED_IFACES"] = csv_ifaces
        return "BLUE", parsed

    # Default / RED: Full network stack access
    os.environ["LLM_ISOLATION_MODE"] = "RED"
    os.environ["LLM_POSTURE_OVERRIDE"] = "RED"
    os.environ.pop("LLM_ALLOWED_IFACES", None)
    return "RED", []


def save_current_cli_session(messages: list | None = None) -> None:
    """
    Persist the active CLI session state (`ACTIVE_PROJECT`, `ACTIVE_GOAL`, `RELENTLESS_MODE`,
    `CURRENT_WAVE`, `MAX_RELENTLESS_WAVES`, `ATTEMPT_LEDGER`, `LLM_ISOLATION_MODE`,
    `LLM_ALLOWED_IFACES`, and conversation history `messages[1:]`) to `last_cli_session.json`
    so `./run_cora_NIX.sh cli -c` / `--continue` can seamlessly resume where the user left off.
    """
    msgs = messages if messages is not None else _ACTIVE_MESSAGES_REF
    non_sys = []
    if msgs and len(msgs) > 1:
        for m in msgs[1:]:
            if isinstance(m, dict) and m.get("role") in ("user", "assistant", "tool"):
                non_sys.append(m)
    # Do not write or overwrite the session file if the user hasn't taken any actions in this session
    if not non_sys and not ACTIVE_GOAL and not ACTIVE_PROJECT and not ATTEMPT_LEDGER:
        return
    try:
        LAST_SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_name": MODEL_NAME,
            "active_project": ACTIVE_PROJECT,
            "personality_mode": ACTIVE_PERSONALITY_MODE,
            "active_goal": ACTIVE_GOAL,
            "relentless_mode": RELENTLESS_MODE,
            "current_wave": CURRENT_WAVE,
            "max_waves": MAX_RELENTLESS_WAVES,
            "isolation_mode": os.environ.get("LLM_ISOLATION_MODE", ""),
            "allowed_interfaces": os.environ.get("LLM_ALLOWED_IFACES", ""),
            "attempt_ledger": ATTEMPT_LEDGER[-80:],
            "messages": non_sys[-40:],
        }
        tmp_path = LAST_SESSION_FILE.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.replace(LAST_SESSION_FILE)
    except Exception:
        pass


def restore_last_cli_session(messages: list) -> dict:
    """
    Restore the most recent CLI session from `last_cli_session.json` (or fall back to
    `relentless_ledger.json` if `last_cli_session.json` does not exist yet).
    Updates global state (`ACTIVE_PROJECT`, `ACTIVE_GOAL`, `ATTEMPT_LEDGER`, `CURRENT_WAVE`,
    `MAX_RELENTLESS_WAVES`) and populates `messages`.
    """
    global ACTIVE_PROJECT, ACTIVE_GOAL, RELENTLESS_MODE, CURRENT_WAVE, MAX_RELENTLESS_WAVES
    data: dict = {}
    source_label = ""
    if LAST_SESSION_FILE.is_file():
        try:
            data = json.loads(LAST_SESSION_FILE.read_text(encoding="utf-8", errors="replace"))
            source_label = str(LAST_SESSION_FILE.relative_to(BASE_DIR))
        except Exception:
            data = {}
    if not data and RELENTLESS_LEDGER_FILE.is_file():
        try:
            led = json.loads(RELENTLESS_LEDGER_FILE.read_text(encoding="utf-8", errors="replace"))
            if isinstance(led, dict):
                data = {
                    "saved_at": datetime.fromtimestamp(RELENTLESS_LEDGER_FILE.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "active_project": led.get("active_project", ""),
                    "active_goal": led.get("active_goal", ""),
                    "relentless_mode": False,
                    "current_wave": led.get("current_wave", 0),
                    "max_waves": led.get("max_waves", 15),
                    "attempt_ledger": led.get("attempts", []),
                    "messages": [],
                }
                source_label = str(RELENTLESS_LEDGER_FILE.relative_to(BASE_DIR))
        except Exception:
            data = {}

    if not data:
        return {"restored": False, "reason": "No previous session file found."}

    if data.get("active_project"):
        ACTIVE_PROJECT = str(data["active_project"]).strip()
        os.environ["CORA_ACTIVE_PROJECT"] = ACTIVE_PROJECT
        try:
            ensure_project_workspace(ACTIVE_PROJECT)
        except Exception:
            pass
    saved_iso = str(data.get("isolation_mode") or "").strip().lower()
    saved_ifaces = data.get("allowed_interfaces")
    saved_ifaces_str = ""
    if isinstance(saved_ifaces, list) and saved_ifaces:
        saved_ifaces_str = ",".join(str(x).strip() for x in saved_ifaces if str(x).strip())
    elif isinstance(saved_ifaces, str) and saved_ifaces.strip():
        saved_ifaces_str = saved_ifaces.strip()
    if saved_ifaces_str:
        os.environ["LLM_ALLOWED_IFACES"] = saved_ifaces_str
    if saved_iso:
        try:
            apply_network_isolation_level(saved_iso, saved_ifaces_str)
        except Exception:
            pass
    if data.get("personality_mode"):
        saved_pmode = str(data["personality_mode"]).strip().upper()
        try:
            apply_personality_mode(saved_pmode, netiso_group=saved_iso)
        except Exception:
            pass
    if data.get("active_goal"):
        ACTIVE_GOAL = str(data["active_goal"]).strip()
    if isinstance(data.get("current_wave"), int):
        CURRENT_WAVE = int(data["current_wave"])
    if isinstance(data.get("max_waves"), int) and int(data["max_waves"]) >= 0:
        MAX_RELENTLESS_WAVES = int(data["max_waves"])

    saved_attempts = data.get("attempt_ledger")
    if isinstance(saved_attempts, list) and saved_attempts:
        ATTEMPT_LEDGER.clear()
        ATTEMPT_LEDGER.extend(saved_attempts)

    # Refresh system prompt now that ACTIVE_PROJECT / ACTIVE_GOAL are restored
    messages.clear()
    messages.append({"role": "system", "content": build_system_prompt(force_refresh_hw=False)})

    saved_msgs = data.get("messages")
    restored_msg_count = 0
    if isinstance(saved_msgs, list) and saved_msgs:
        for m in saved_msgs:
            if isinstance(m, dict) and m.get("role") in ("user", "assistant", "tool"):
                messages.append(m)
                restored_msg_count += 1
        sanitize_messages(messages)
    elif ACTIVE_GOAL or ATTEMPT_LEDGER:
        # Synthesize a continuation context block from the restored goal & attempt ledger
        digest, _, _ = _build_vault_and_attempt_summary_for_relentless(ACTIVE_GOAL or "Resumed Session")
        messages.append(
            {
                "role": "user",
                "content": f"[RESUMED PREVIOUS SESSION (`--continue`)]:\n{digest}",
            }
        )
        messages.append(
            {
                "role": "assistant",
                "content": (
                    f"Session restored for project `{ACTIVE_PROJECT or 'None'}` "
                    f"with active goal `{ACTIVE_GOAL}` and `{len(ATTEMPT_LEDGER)}` recorded tool attempts. "
                    "Ready to continue from where we left off."
                ),
            }
        )
        restored_msg_count = 2

    return {
        "restored": True,
        "source": source_label,
        "saved_at": data.get("saved_at", "unknown"),
        "active_project": ACTIVE_PROJECT,
        "active_goal": ACTIVE_GOAL,
        "attempt_count": len(ATTEMPT_LEDGER),
        "message_count": restored_msg_count,
        "current_wave": CURRENT_WAVE,
    }


def _get_live_continual_mode() -> str:
    try:
        from Reasoning.engines.continual_learner import get_continual_learning_state

        return str(get_continual_learning_state().get("mode", "AUTO")).upper()
    except Exception:
        return os.environ.get("CONTINUAL_LEARNING_MODE", "AUTO").upper()


CONTINUAL_MODE: str = _get_live_continual_mode()


def _is_webui_or_other_cli_engaged() -> bool:
    """
    Return True if the CORA WebGUI (`127.0.0.1:1337` / `Log/webui.pid`) or another
    `agent-cli.py` process is currently running so `llama-server` is never stopped
    while either interface remains engaged.
    """
    webui_port = int(os.environ.get("CORA_WEBUI_PORT") or os.environ.get("WEBUI_PORT") or "1337")
    try:
        import socket

        with socket.create_connection(("127.0.0.1", webui_port), timeout=0.35):
            return True
    except Exception:
        pass

    webui_pid_file = BASE_DIR / "Log" / "webui.pid"
    if webui_pid_file.is_file():
        try:
            wpid_str = webui_pid_file.read_text(encoding="utf-8", errors="ignore").strip().splitlines()[0].strip()
            if wpid_str.isdigit():
                wpid = int(wpid_str)
                if wpid != os.getpid():
                    import psutil

                    if psutil.pid_exists(wpid):
                        return True
        except Exception:
            pass

    try:
        import psutil

        my_pid = os.getpid()
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                pid = proc.info.get("pid")
                if not pid or pid == my_pid:
                    continue
                pname = (proc.info.get("name") or "").lower()
                if "python" not in pname:
                    continue
                cmdline = " ".join(proc.cmdline() or []).lower().replace("\\", "/")
                if "webui/server.py" in cmdline or "agent-cli.py" in cmdline:
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False


_CLI_KEEPALIVE_WATCHDOG_STARTED = False


def _start_cli_llama_keepalive_watchdog() -> None:
    """
    Keep `llama-server` continuously online and engaged for the entire duration of the
    interactive CLI session so it never drops into standby mode.
    """
    global _CLI_KEEPALIVE_WATCHDOG_STARTED
    if _CLI_KEEPALIVE_WATCHDOG_STARTED or os.environ.get("CORA_SKIP_AUTO_LLAMA") == "1":
        return
    _CLI_KEEPALIVE_WATCHDOG_STARTED = True

    def _cli_watchdog_loop() -> None:
        health_url = API_URL.split("/v1/")[0].rstrip("/") + "/health"
        while not _CLI_SHUTDOWN_DONE:
            try:
                is_up = False
                try:
                    with urllib.request.urlopen(health_url, timeout=2.0) as r:
                        if r.status == 200:
                            is_up = True
                except urllib.error.HTTPError as he:
                    if he.code == 503:
                        is_up = True
                except Exception:
                    pass
                if not is_up and not _CLI_SHUTDOWN_DONE:
                    _ensure_llama_server_running()
            except Exception:
                pass
            for _ in range(16):
                if _CLI_SHUTDOWN_DONE:
                    return
                time.sleep(0.5)

    threading.Thread(target=_cli_watchdog_loop, daemon=True, name="cora-cli-llama-keepalive").start()


def _shutdown_cli_and_engines(stop_llm: bool = True, quiet: bool = False) -> None:
    """
    Deterministic shutdown hook triggered on `/exit`, `Ctrl+D`, `Ctrl+C` at prompt,
    or terminal window close (`SIGHUP` / `SIGTERM` on Linux; `SIGBREAK` on Windows).
    1. Immediately halts Engine 16 Continual Learning (`is_currently_running = False`)
       and pauses/stops the Speculative Lookahead Cache thread.
    2. Stops the local `llama-server` process (`Log/llama-server.pid`) ONLY if neither the
       CORA WebGUI nor another CLI instance is currently engaged (unless `--keep-server` /
       `KEEP_SERVER_ON_EXIT=1` was explicitly requested).
    """
    global _CLI_SHUTDOWN_DONE
    if _CLI_SHUTDOWN_DONE:
        return
    _CLI_SHUTDOWN_DONE = True

    try:
        save_current_cli_session()
    except Exception:
        pass

    try:
        if "HUD" in globals() and HUD.active:
            HUD.stop()
    except Exception:
        pass

    try:
        if _SPECULATIVE_CACHE_REF is not None:
            if hasattr(_SPECULATIVE_CACHE_REF, "stop"):
                _SPECULATIVE_CACHE_REF.stop()
    except Exception:
        pass

    try:
        from Reasoning.engines.mdp_tactical import flush_mdp_store_if_dirty

        flush_mdp_store_if_dirty()
    except Exception:
        pass

    try:
        from Reasoning.engines.continual_learner import get_continual_learning_state, save_continual_learning_state

        st = get_continual_learning_state()
        if st.get("is_currently_running"):
            st["is_currently_running"] = False
            save_continual_learning_state(st)
    except Exception:
        pass

    try:
        from Network_Isolation.console_posture import reset_console_posture

        reset_console_posture(quiet=True)
    except Exception:
        pass

    if stop_llm and not KEEP_SERVER_ON_EXIT and not _is_webui_or_other_cli_engaged():
        pid_file = BASE_DIR / "Log" / "llama-server.pid"
        active_mod_file = BASE_DIR / "Log" / "llama-server.model"
        legacy_mod_file = BASE_DIR / "Log" / "active-model.txt"
        if pid_file.is_file():
            try:
                pid_str = pid_file.read_text(encoding="utf-8", errors="ignore").strip().splitlines()[0].strip()
                pid = int(pid_str)
                if os.name == "nt":
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(pid)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=4,
                    )
                else:
                    os.kill(pid, signal.SIGTERM)
                if not quiet:
                    print(f"\033[1;33m[Shutdown]\033[0m Stopped llama-server (PID {pid}) and Engine 12 continual learning.")
            except Exception:
                pass
            for f_clean in (pid_file, active_mod_file, legacy_mod_file):
                try:
                    f_clean.unlink(missing_ok=True)
                except Exception:
                    pass
DOC_EXTENSIONS = {
    ".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".conf", ".csv", ".tsv", ".xml", ".html", ".htm", ".sh", ".py", ".log", ".pdf",
}


def _refresh_active_posture(override: str = "", apply_osc: bool = False, quiet: bool = True) -> dict:
    """Detect or apply the active console security posture and cache it in ACTIVE_POSTURE."""
    global ACTIVE_POSTURE
    try:
        from Network_Isolation.console_posture import apply_console_posture, detect_console_posture

        if apply_osc:
            ACTIVE_POSTURE = apply_console_posture(override=override, quiet=quiet)
        else:
            ACTIVE_POSTURE = detect_console_posture(override=override)
    except Exception:
        ACTIVE_POSTURE = {
            "mode": "UNRESTRICTED",
            "short_tag": "UNRESTRICTED",
            "hud_badge": "NET:UNRESTRICTED(FULL-ACCESS)",
            "banner_badge": "[POSTURE: UNRESTRICTED / FULL HOST & WAN ACCESS]",
            "bg_hex": "#1C0A0D",
            "fg_hex": "#FFE8E8",
            "cursor_hex": "#FF3B5C",
            "ansi_border": "\033[1;31m",
            "ansi_accent": "\033[38;2;255;77;109m",
            "ansi_prompt": "\033[1;38;2;255;77;109m",
            "ansi_hud_bar": "\033[48;2;52;12;18;38;2;255;232;232;1m",
        }
    return ACTIVE_POSTURE


import contextlib

_CLI_VIEW_STATE: str = "startup"
_SESSION_TRANSCRIPT_CHUNKS: list[str] = []
_SESSION_TRANSCRIPT_MAX_CHARS: int = 120000
_SUPPRESS_TRANSCRIPT_DEPTH: int = 0
_ACTIVE_MENU_REDRAW_FN = None
_ACTIVE_PROMPT_REDRAW_FN = None
_LAST_RESTORED_SESSION_INFO: dict = {}
_LAST_STARTUP_CONTINUE: bool = False
_ANSI_VIS_RE = re.compile(r"\x01?\x1b\[[0-?]*[ -/]*[@-~]\x02?|\x01?\x1b\][^\x07]*\x07\x02?|\x01|\x02")


@contextlib.contextmanager
def _raw_terminal_output():
    """Suppress recording of transient HUD/cursor/spinner/repaint sequences in `_SESSION_TRANSCRIPT_CHUNKS`."""
    global _SUPPRESS_TRANSCRIPT_DEPTH
    _SUPPRESS_TRANSCRIPT_DEPTH += 1
    try:
        yield
    finally:
        _SUPPRESS_TRANSCRIPT_DEPTH = max(0, _SUPPRESS_TRANSCRIPT_DEPTH - 1)


def _append_session_transcript(text: str) -> None:
    """Append committed session text to `_SESSION_TRANSCRIPT_CHUNKS` so window resizes can repaint cleanly."""
    global _SESSION_TRANSCRIPT_CHUNKS
    if not text or _SUPPRESS_TRANSCRIPT_DEPTH > 0 or _CLI_VIEW_STATE != "main_session":
        return
    _SESSION_TRANSCRIPT_CHUNKS.append(text)
    total_len = sum(len(c) for c in _SESSION_TRANSCRIPT_CHUNKS)
    while total_len > _SESSION_TRANSCRIPT_MAX_CHARS and len(_SESSION_TRANSCRIPT_CHUNKS) > 1:
        removed = _SESSION_TRANSCRIPT_CHUNKS.pop(0)
        total_len -= len(removed)


class _TranscriptTeeStdout:
    """Wraps `sys.stdout` on interactive TTYs to capture committed session output for resize repainting."""

    def __init__(self, wrapped) -> None:
        self._wrapped = wrapped

    def write(self, s: str) -> int:
        res = self._wrapped.write(s)
        try:
            _append_session_transcript(s)
        except Exception:
            pass
        return res

    def flush(self) -> None:
        self._wrapped.flush()

    def isatty(self) -> bool:
        return self._wrapped.isatty()

    def fileno(self) -> int:
        return self._wrapped.fileno()

    def __getattr__(self, name: str):
        return getattr(self._wrapped, name)


if sys.stdout.isatty() and not isinstance(sys.stdout, _TranscriptTeeStdout):
    sys.stdout = _TranscriptTeeStdout(sys.stdout)  # type: ignore[assignment]


class BottomPinnedHUD:
    """
    Pins an ultra-compact, auto-centered, color-coded hardware monitor (`C:xx% M:xx% G:xx%/xx% D:xx%`)
    to the bottom terminal row using DECSTBM scroll-region locking (`\\033[1;{rows-1}r`).
    Adjusts dynamically on window resize (`SIGWINCH` / ConPTY size polling) and repaints the active
    CLI viewport so text never disappears into blank reflow gaps on resize.
    """

    def __init__(self) -> None:
        self.active = False
        self._stop_evt = threading.Event()
        self._lock = threading.RLock()
        self._stream_paused = False
        self._thread: threading.Thread | None = None
        self._prev_cpu_idle = 0
        self._prev_cpu_total = 0
        self._metrics = {"cpu": 0, "mem": 0, "gpu": 0, "vram": 0, "disk": 0}
        self._last_cols = 0
        self._last_rows = 0
        self._pending_resize_dims = (0, 0)
        self._pending_resize_ts = 0.0
        self._in_readline_input = False
        self._in_interactive_input = False
        self._resize_in_progress = False
        self._resize_flag = False
        # Default both Linux and Windows to 'pin' mode (pins the HUD metric bar to the very bottom
        # row of the terminal window, BELOW the `[POSTURE] You>` input prompt).
        # On Windows PowerShell/ConPTY, we combine `cols - 1` bottom-right wrap prevention (`\033[?7l`),
        # pre-prompt scroll reservation (`\n\033[1A`), and full-viewport resize repainting so the bar
        # stays below the input prompt without scrolling, duplicating, or wiping text on window resize.
        default_mode = "pin"
        self.mode = os.environ.get("HUD_MODE", default_mode).strip().lower()
        if self.mode not in ("pin", "prompt", "title"):
            self.mode = default_mode

    def _sample_cpu_pct(self) -> int:
        try:
            if os.path.exists("/proc/stat"):
                with open("/proc/stat", "r", encoding="utf-8") as f:
                    first = f.readline()
                parts = [int(x) for x in first.split()[1:]]
                idle = parts[3] + (parts[4] if len(parts) > 4 else 0)
                total = sum(parts)
            elif os.name == "nt":
                class _FILETIME(ctypes.Structure):
                    _fields_ = [("dwLowDateTime", ctypes.c_uint32), ("dwHighDateTime", ctypes.c_uint32)]

                idle_ft, kernel_ft, user_ft = _FILETIME(), _FILETIME(), _FILETIME()
                if not ctypes.windll.kernel32.GetSystemTimes(
                    ctypes.byref(idle_ft), ctypes.byref(kernel_ft), ctypes.byref(user_ft)
                ):
                    return self._metrics["cpu"]
                idle = (idle_ft.dwHighDateTime << 32) | idle_ft.dwLowDateTime
                kernel = (kernel_ft.dwHighDateTime << 32) | kernel_ft.dwLowDateTime
                user = (user_ft.dwHighDateTime << 32) | user_ft.dwLowDateTime
                total = kernel + user
            else:
                return 0
            d_total = total - self._prev_cpu_total
            d_idle = idle - self._prev_cpu_idle
            self._prev_cpu_total = total
            self._prev_cpu_idle = idle
            if d_total <= 0:
                return self._metrics["cpu"]
            pct = int(round(100.0 * (1.0 - (d_idle / d_total))))
            return max(0, min(100, pct))
        except Exception:
            return 0

    def _sample_mem_pct(self) -> int:
        try:
            if os.path.exists("/proc/meminfo"):
                total = 0
                avail = 0
                with open("/proc/meminfo", "r", encoding="utf-8") as f:
                    for ln in f:
                        if ln.startswith("MemTotal:"):
                            total = int(ln.split()[1])
                        elif ln.startswith("MemAvailable:"):
                            avail = int(ln.split()[1])
                        if total and avail:
                            break
                if total > 0:
                    return max(0, min(100, int(round(100.0 * (total - avail) / total))))
            elif os.name == "nt":
                class _MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_uint32),
                        ("dwMemoryLoad", ctypes.c_uint32),
                        ("ullTotalPhys", ctypes.c_uint64),
                        ("ullAvailPhys", ctypes.c_uint64),
                        ("ullTotalPageFile", ctypes.c_uint64),
                        ("ullAvailPageFile", ctypes.c_uint64),
                        ("ullTotalVirtual", ctypes.c_uint64),
                        ("ullAvailVirtual", ctypes.c_uint64),
                        ("ullAvailExtendedVirtual", ctypes.c_uint64),
                    ]

                ms = _MEMORYSTATUSEX()
                ms.dwLength = ctypes.sizeof(ms)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms)):
                    return max(0, min(100, int(ms.dwMemoryLoad)))
        except Exception:
            pass
        return 0

    def _sample_gpu_pcts(self) -> tuple[int, int]:
        try:
            out = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu,memory.used,memory.total",
                    "--format=csv,noheader,nounits",
                ],
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=1.2,
            ).strip()
            if out:
                first = out.splitlines()[0]
                g_str, mu_str, mt_str = [x.strip() for x in first.split(",")[:3]]
                g_pct = max(0, min(100, int(float(g_str))))
                mt = float(mt_str)
                v_pct = max(0, min(100, int(round(100.0 * float(mu_str) / mt)))) if mt > 0 else 0
                return g_pct, v_pct
        except Exception:
            pass
        return 0, 0

    def _sample_disk_pct(self) -> int:
        try:
            du = shutil.disk_usage(str(BASE_DIR))
            if du.total > 0:
                return max(0, min(100, int(round(100.0 * du.used / du.total))))
        except Exception:
            pass
        return 0

    @staticmethod
    def _color_pct(val: int) -> str:
        # Green < 70%, Yellow 70-88%, Bright Red >= 89%
        if val >= 89:
            return f"\033[1;31m{val}%\033[22;37m"
        if val >= 70:
            return f"\033[1;33m{val}%\033[22;37m"
        return f"\033[1;32m{val}%\033[22;37m"

    @staticmethod
    def _short_model_name() -> str:
        low = MODEL_NAME.lower()
        if "3.5" in low or "9b" in low:
            return "Qwen3.5-9B"
        if "turbo" in low or "mtp" in low:
            if "q8" in low:
                return "Qwen3.8-MTP-Q8"
            if "q6" in low:
                return "Qwen3.8-MTP-Q6"
            return "Qwen3.8-MTP-Q4"
        if "3.8" in low or "27b" in low:
            return "Qwen3.8-27B"
        return MODEL_NAME[:14]

    @staticmethod
    def _active_switches() -> tuple[str, str]:
        """Return (plain_flags, colored_flags) for active startup/session switches & security posture."""
        plain_parts = []
        color_parts = []
        posture = ACTIVE_POSTURE or _refresh_active_posture()
        p_tag = posture.get("short_tag", "UNRESTRICTED")
        p_mode = posture.get("mode", "UNRESTRICTED")
        if p_mode == "AIR_GAPPED_NETNS":
            plain_parts.append(f"NET:{p_tag}")
            color_parts.append(f"\033[1;97mNET:{p_tag}\033[22;37m")
        elif p_mode == "ISOLATED_LAN_USB":
            plain_parts.append(f"NET:{p_tag}")
            color_parts.append(f"\033[1;36mNET:{p_tag}\033[22;37m")
        else:
            plain_parts.append(f"NET:{p_tag}")
            color_parts.append(f"\033[1;31mNET:{p_tag}\033[22;37m")

        if SKIP_PERMISSIONS:
            plain_parts.append("AUTO")
            color_parts.append("\033[1;31mAUTO\033[22;37m")
        else:
            plain_parts.append("CONFIRM")
            color_parts.append("\033[1;32mCONFIRM\033[22;37m")

        if os.environ.get("REASONING_MODE", "off").lower() == "on":
            plain_parts.append("THINK")
            color_parts.append("\033[1;35mTHINK\033[22;37m")

        if ACTIVE_PROJECT:
            p_short = ACTIVE_PROJECT[:12]
            plain_parts.append(f"PROJ:{p_short}")
            color_parts.append(f"\033[1;36mPROJ:{p_short}\033[22;37m")

        pmode = (ACTIVE_PERSONALITY_MODE or "DEFAULT").upper()
        plain_parts.append(f"MODE:{pmode}")
        if pmode == "BERSERKER":
            color_parts.append(f"\033[1;31mMODE:{pmode}\033[22;37m")
        elif pmode == "NINJA":
            color_parts.append(f"\033[1;35mMODE:{pmode}\033[22;37m")
        elif pmode == "ANALYST":
            color_parts.append(f"\033[1;97mMODE:{pmode}\033[22;37m")
        else:
            color_parts.append(f"\033[1;32mMODE:{pmode}\033[22;37m")

        if ACTIVE_GOAL:
            g_short = slugify(ACTIVE_GOAL)[:12]
            plain_parts.append(f"GOAL:{g_short}")
            color_parts.append(f"\033[1;33mGOAL:{g_short}\033[22;37m")

        if RELENTLESS_MODE:
            plain_parts.append("RELENTLESS")
            color_parts.append("\033[1;35mRELENTLESS\033[22;37m")

        lrn_mode = (CONTINUAL_MODE or "AUTO").upper()
        plain_parts.append(f"LRN:{lrn_mode}")
        if lrn_mode == "START":
            color_parts.append(f"\033[1;32mLRN:{lrn_mode}\033[22;37m")
        elif lrn_mode == "STOP":
            color_parts.append(f"\033[1;33mLRN:{lrn_mode}\033[22;37m")
        else:
            color_parts.append(f"\033[1;36mLRN:{lrn_mode}\033[22;37m")

        return " ".join(plain_parts), " ".join(color_parts)

    def _build_centered_bar(self, cols: int) -> str:
        m = self._metrics
        mod_short = self._short_model_name()
        flags_plain, flags_color = self._active_switches()
        cwd_name = Path(os.getcwd()).name or "/"
        posture = ACTIVE_POSTURE or _refresh_active_posture()
        hud_bg = posture.get("ansi_hud_bar", "\033[48;5;235m\033[37m")

        c_col = self._color_pct(m["cpu"])
        m_col = self._color_pct(m["mem"])
        g_col = self._color_pct(m["gpu"])
        v_col = self._color_pct(m["vram"])
        d_col = self._color_pct(m["disk"])

        # Tier 1: Full labels + Model + Switches + CWD
        t1_plain = (
            f"[ CPU:{m['cpu']}% | MEM:{m['mem']}% | GPU:{m['gpu']}% VRAM:{m['vram']}% | "
            f"DISK:{m['disk']}% | {mod_short} [{flags_plain}] | CWD: {cwd_name} ]"
        )
        t1_color = (
            f"{hud_bg}[ CPU:{c_col} | MEM:{m_col} | GPU:{g_col} VRAM:{v_col} | "
            f"DISK:{d_col} | \033[1;36m{mod_short}\033[22;37m [{flags_color}] | "
            f"CWD: \033[1;33m{cwd_name}\033[22;37m ]\033[0m{hud_bg}"
        )

        # Tier 2: Compact labels + Model + Switches + CWD
        t2_plain = (
            f"CPU:{m['cpu']}% MEM:{m['mem']}% GPU:{m['gpu']}%/{m['vram']}% "
            f"DSK:{m['disk']}% | {mod_short} [{flags_plain}] | CWD: {cwd_name}"
        )
        t2_color = (
            f"{hud_bg}CPU:{c_col} MEM:{m_col} GPU:{g_col}/{v_col} "
            f"DSK:{d_col} | \033[1;36m{mod_short}\033[22;37m [{flags_color}] | "
            f"CWD: \033[1;33m{cwd_name}\033[22;37m\033[0m{hud_bg}"
        )

        # Tier 3: Narrow window (~50-72 cols)
        mod_tiny = "3.5" if "3.5" in mod_short else ("3.8" if "3.8" in mod_short else mod_short[:6])
        t3_plain = (
            f"CPU:{m['cpu']}% MEM:{m['mem']}% GPU:{m['vram']}% DSK:{m['disk']}% | "
            f"{mod_tiny} {flags_plain} | CWD:{cwd_name[:10]}"
        )
        t3_color = (
            f"{hud_bg}CPU:{c_col} MEM:{m_col} GPU:{v_col} DSK:{d_col} | "
            f"\033[1;36m{mod_tiny}\033[22;37m {flags_color} | "
            f"CWD:\033[1;33m{cwd_name[:10]}\033[22;37m\033[0m{hud_bg}"
        )

        # Tier 4: Ultra-narrow (~400px / <50 cols)
        mode_tag = "AUTO" if SKIP_PERMISSIONS else "CONF"
        mode_col = "\033[1;31mAUTO\033[22;37m" if SKIP_PERMISSIONS else "\033[1;32mCONF\033[22;37m"
        t4_plain = f"CPU:{m['cpu']}% MEM:{m['mem']}% GPU:{m['vram']}% DSK:{m['disk']}% {mod_tiny}/{mode_tag} CWD:{cwd_name[:8]}"
        t4_color = (
            f"{hud_bg}CPU:{c_col} MEM:{m_col} GPU:{v_col} DSK:{d_col} "
            f"\033[1;36m{mod_tiny}\033[22;37m/{mode_col} CWD:\033[1;33m{cwd_name[:8]}\033[22;37m\033[0m{hud_bg}"
        )

        if cols >= len(t1_plain):
            plain, colored = t1_plain, t1_color
        elif cols >= len(t2_plain):
            plain, colored = t2_plain, t2_color
        elif cols >= len(t3_plain):
            plain, colored = t3_plain, t3_color
        elif cols >= len(t4_plain):
            plain, colored = t4_plain, t4_color
        else:
            plain = t4_plain[: max(1, cols)]
            colored = f"{hud_bg}{plain}"

        vis_len = len(plain)
        # On Windows consoles (conhost/ConPTY), writing to the very last column (rows, cols)
        # can trigger an automatic line-wrap scroll; use cols - 1 on Windows to prevent wrap.
        eff_cols = max(1, cols - 1) if os.name == "nt" else cols
        if vis_len > eff_cols:
            plain = plain[:eff_cols]
            colored = f"{hud_bg}{plain}"
            vis_len = len(plain)
        pad_left = max(0, (eff_cols - vis_len) // 2)
        pad_right = max(0, eff_cols - vis_len - pad_left)
        return f"{hud_bg}{' ' * pad_left}{colored}{' ' * pad_right}\033[0m"

    def _build_plain_title(self) -> str:
        m = self._metrics
        mod_short = self._short_model_name()
        flags_plain, _ = self._active_switches()
        cwd_name = Path(os.getcwd()).name or "/"
        return (
            f"CORA | CPU:{m['cpu']}% MEM:{m['mem']}% GPU:{m['gpu']}% VRAM:{m['vram']}% "
            f"DISK:{m['disk']}% | {mod_short} [{flags_plain}] | CWD:{cwd_name}"
        )

    def _update_window_title(self) -> None:
        if os.name == "nt":
            try:
                ctypes.windll.kernel32.SetConsoleTitleW(self._build_plain_title())
            except Exception:
                pass

    def clear_bottom_row(self) -> None:
        """
        Keep the bottom-pinned HUD row intact during CLI operation.
        Only `stop()` unlocks the DECSTBM scroll region (`1..{rows}`) on exit.
        """
        if not self.active or self.mode != "pin" or not sys.stdout.isatty():
            return
        self.render(force_region=False)

    def pause_stream(self) -> None:
        """Keep the bottom-pinned HUD visible and updating live while the LLM is responding."""
        self._stream_paused = False
        if self.active and self.mode == "pin":
            self.render(force_region=False)

    def resume_stream(self) -> None:
        self._stream_paused = False
        if self.active and self.mode == "pin":
            self.render(force_region=False)

    def render_before_prompt(self) -> None:
        """
        Called synchronously on the main thread right before `input()`.
        Keeps DECSTBM locked to `1..{rows-1}` so all CLI text and the `[POSTURE] You>`
        prompt remain strictly above the bottom HUD metric bar on row `rows`.
        """
        if not self.active or not sys.stdout.isatty():
            return
        self._update_window_title()
        if self.mode == "prompt":
            with self._lock, _raw_terminal_output():
                try:
                    sz = shutil.get_terminal_size((80, 24))
                    cols = max(20, sz.columns)
                    bar = self._build_centered_bar(cols)
                    sys.stdout.write(f"{bar}\n")
                    sys.stdout.flush()
                except Exception:
                    pass
        elif self.mode == "pin":
            self.render(force_region=True)

    def begin_resize_transition(self, cols: int, rows: int) -> None:
        """
        Immediately unlock DECSTBM (`\\033[r`) and erase the old bottom HUD bar row as soon
        as a terminal resize starts so ConPTY/Windows Terminal never anchors reflow to a
        stale bottom HUD row or clips reflow inside an outdated scroll region.
        """
        with self._lock, _raw_terminal_output():
            now_m = time.monotonic()
            was_in_progress = self._resize_in_progress
            self._resize_in_progress = True
            self._pending_resize_dims = (cols, rows)
            self._pending_resize_ts = now_m
            if not was_in_progress and self.active and self.mode == "pin" and sys.stdout.isatty():
                try:
                    old_r = self._last_rows
                    clear_old = f"\033[{old_r};1H\033[2K" if old_r > 0 else ""
                    sys.stdout.write(f"\0337\033[r{clear_old}\033[0m\0338")
                    sys.stdout.flush()
                except Exception:
                    pass

    def render(self, force_region: bool = False) -> None:
        if not self.active or not sys.stdout.isatty():
            return
        self._update_window_title()
        if self.mode != "pin":
            return
        with self._lock, _raw_terminal_output():
            try:
                sz = shutil.get_terminal_size((80, 24))
                cols, rows = max(20, sz.columns), max(6, sz.lines)
                if cols < 24 or rows < 6:
                    return

                # Debounce active drag-resizing from background thread so ConPTY/PowerShell
                # never receives DECSTBM/cursor escape sequences mid-reflow.
                size_changed = (cols != self._last_cols or rows != self._last_rows)
                if size_changed and not force_region and self._last_rows > 0:
                    now_m = time.monotonic()
                    if (cols, rows) != self._pending_resize_dims:
                        self.begin_resize_transition(cols, rows)
                        return
                    if (now_m - self._pending_resize_ts) < 0.35:
                        return
                    self._resize_in_progress = False
                    redraw_cli_on_resize()
                    if _ACTIVE_PROMPT_REDRAW_FN is not None:
                        try:
                            _ACTIVE_PROMPT_REDRAW_FN()
                        except Exception:
                            pass
                    return

                if self._resize_in_progress and not force_region:
                    return

                posture = ACTIVE_POSTURE or _refresh_active_posture()
                hud_bg = posture.get("ansi_hud_bar", "\033[48;5;235m")
                bar = self._build_centered_bar(cols)
                cleanup_old_row = ""
                if self._last_rows > 0 and self._last_rows != rows:
                    old_r = min(self._last_rows, rows)
                    cleanup_old_row = f"\033[{old_r};1H\033[2K"
                prefix = ""
                if self._last_rows > 0 and rows < self._last_rows:
                    # Terminal shrunk vertically; nudge cursor up 1 row in case it was clamped to new bottom row
                    prefix = "\033[1A"
                if force_region or size_changed:
                    self._last_cols, self._last_rows = cols, rows
                    self._pending_resize_dims = (cols, rows)
                    self._resize_in_progress = False
                    seq = f"{prefix}\0337{cleanup_old_row}\033[1;{rows - 1}r\033[?7l\033[{rows};1H{hud_bg}\033[2K{bar}\033[0m\033[?7h\0338"
                else:
                    seq = f"\0337\033[?7l\033[{rows};1H{hud_bg}\033[2K{bar}\033[0m\033[?7h\0338"
                sys.stdout.write(seq)
                sys.stdout.flush()
            except Exception:
                pass

    def _loop(self) -> None:
        last_sample_ts = 0.0
        while not self._stop_evt.is_set():
            now_m = time.monotonic()
            if (now_m - last_sample_ts) >= 1.5:
                last_sample_ts = now_m
                self._metrics["cpu"] = self._sample_cpu_pct()
                self._metrics["mem"] = self._sample_mem_pct()
                g_pct, v_pct = self._sample_gpu_pcts()
                self._metrics["gpu"] = g_pct
                self._metrics["vram"] = v_pct
                self._metrics["disk"] = self._sample_disk_pct()
                self._update_window_title()
                if self.mode == "pin" and not self._in_readline_input and not self._in_interactive_input and not self._resize_in_progress:
                    self.render(force_region=False)

            # On POSIX/Linux, handle debounced SIGWINCH resize events cleanly outside the signal handler
            if os.name != "nt" and self._resize_flag:
                try:
                    sz = shutil.get_terminal_size((80, 24))
                    cols, rows = max(20, sz.columns), max(6, sz.lines)
                    if (cols, rows) != self._pending_resize_dims:
                        self.begin_resize_transition(cols, rows)
                    elif (now_m - self._pending_resize_ts) >= 0.22:
                        self._resize_flag = False
                        self._resize_in_progress = False
                        redraw_cli_on_resize()
                        if _ACTIVE_PROMPT_REDRAW_FN is not None:
                            try:
                                _ACTIVE_PROMPT_REDRAW_FN()
                            except Exception:
                                pass
                        elif self._in_readline_input and readline is not None and hasattr(readline, "redisplay"):
                            try:
                                readline.redisplay()
                            except Exception:
                                pass
                except Exception:
                    self._resize_flag = False

            self._stop_evt.wait(0.15)

    def _on_resize(self, signum, frame) -> None:
        # Never call sys.stdout.write() inside a signal handler (avoids RuntimeError: reentrant call inside BufferedWriter)
        self._resize_flag = True
        self._pending_resize_ts = time.monotonic()

    def start(self) -> None:
        if self.active or not sys.stdout.isatty():
            return
        self.active = True
        self._stream_paused = False
        self._stop_evt.clear()
        self._sample_cpu_pct()
        self._metrics["mem"] = self._sample_mem_pct()
        g_pct, v_pct = self._sample_gpu_pcts()
        self._metrics["gpu"] = g_pct
        self._metrics["vram"] = v_pct
        self._metrics["disk"] = self._sample_disk_pct()
        self._update_window_title()

        if self.mode == "pin":
            with self._lock, _raw_terminal_output():
                sz = shutil.get_terminal_size((80, 24))
                cols, rows = max(20, sz.columns), max(6, sz.lines)
                self._last_cols, self._last_rows = cols, rows
                self._pending_resize_dims = (cols, rows)
                # Reserve 1 bottom row (scrolling up if cursor was on `rows`), move cursor to `<= rows - 1`,
                # and lock DECSTBM scroll region to `1..{rows - 1}` so CLI output always sits above row `rows`.
                sys.stdout.write(f"\n\033[1A\0337\033[1;{rows - 1}r\0338")
                sys.stdout.flush()
            self.render(force_region=True)

        if hasattr(signal, "SIGWINCH"):
            try:
                signal.signal(signal.SIGWINCH, self._on_resize)
            except Exception:
                pass

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self.active:
            return
        was_pin = self.mode == "pin"
        self.active = False
        self._stop_evt.set()
        if was_pin and sys.stdout.isatty():
            with self._lock, _raw_terminal_output():
                try:
                    sz = shutil.get_terminal_size((80, 24))
                    rows = max(6, sz.lines)
                    # Clear bottom HUD line and restore full terminal scroll region
                    sys.stdout.write(f"\0337\033[r\033[1;{rows}r\033[{rows};1H\033[2K\033[0m\0338")
                    sys.stdout.flush()
                except Exception:
                    pass


HUD = BottomPinnedHUD()
atexit.register(HUD.stop)


def ensure_vault_structure() -> None:
    for sub in (".obsidian", *VALID_CATEGORIES):
        (VAULT_DIR / sub).mkdir(parents=True, exist_ok=True)
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    app_json = VAULT_DIR / ".obsidian" / "app.json"
    if not app_json.exists():
        app_json.write_text(
            json.dumps(
                {
                    "alwaysUpdateLinks": True,
                    "newFileLocation": "folder",
                    "newFileFolderPath": "knowledge",
                    "showUnsupportedFiles": False,
                    "strictLineBreaks": False,
                    "readableLineLength": True,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    if not INDEX_FILE.exists():
        home_str = str(Path.home())
        base_disp = str(BASE_DIR).replace(home_str, "~", 1) if str(BASE_DIR).startswith(home_str) else str(BASE_DIR)
        vault_disp = str(VAULT_DIR).replace(home_str, "~", 1) if str(VAULT_DIR).startswith(home_str) else str(VAULT_DIR)
        INDEX_FILE.write_text(
            "# CORA Knowledge & Memory Index (`00_MEMORY_INDEX`)\n\n"
            "> **Tier-1 Hot Memory:** Automatically loaded into Qwen 3.8 / 3.5 on every session.\n\n"
            "## Core Facts & Environment\n"
            f"- CORA Base Path: `{base_disp}`\n"
            f"- Obsidian Vault Path: `{vault_disp}`\n"
            "- Always use `scan_target` before crafting `curl` requests against an unfamiliar URL or host.\n"
            "- Save verified working `curl` commands, endpoints, and solutions using `vault_save_note`.\n\n"
            "## Indexed Vault Notes\n"
            "<!-- AUTO-INDEX-START -->\n"
            "<!-- AUTO-INDEX-END -->\n",
            encoding="utf-8",
        )


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_\-]+", "_", name.strip()).strip("_").lower()
    return s[:64] or "note"


_INVALID_PROJECT_NAMES = {"active_session", "active-session", "default", "default-project", "default_session"}


def slugify_project_name(name: str) -> str:
    """
    Sanitize a project name for `Projects/<project_name>/`:
    Spaces, strange characters, and special characters are automatically converted to dashes (`-`).
    If an existing directory with that exact name already exists in `Projects/`,
    preserve its exact folder name.
    """
    raw = str(name or "").strip()
    if not raw or raw.lower() in _INVALID_PROJECT_NAMES:
        return ""
    if (PROJECTS_DIR / raw).is_dir() and re.match(r"^[a-zA-Z0-9_\-]+$", raw):
        return raw
    s = re.sub(r"[^a-zA-Z0-9\-]+", "-", raw).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    clean = s[:64].strip("-")
    return "" if clean.lower() in _INVALID_PROJECT_NAMES else clean


def get_active_project_slug() -> str:
    """Return the active project slug, resolving from ACTIVE_PROJECT, env, session state, or existing `Projects/` folders."""
    if ACTIVE_PROJECT and ACTIVE_PROJECT.strip():
        cand = slugify_project_name(ACTIVE_PROJECT)
        if cand:
            return cand
    env_proj = os.environ.get("CORA_ACTIVE_PROJECT", "").strip()
    if env_proj and env_proj.lower() not in _INVALID_PROJECT_NAMES:
        cand = slugify_project_name(env_proj)
        if cand and (PROJECTS_DIR / cand).is_dir():
            return cand
    for ap_file in (LOG_DIR / "active-project.txt", SESSION_STATE_DIR / "active_project.txt"):
        try:
            if ap_file.is_file():
                saved_p = ap_file.read_text(encoding="utf-8", errors="replace").strip()
                if saved_p and saved_p.lower() not in _INVALID_PROJECT_NAMES and (PROJECTS_DIR / saved_p).is_dir():
                    return saved_p
        except Exception:
            pass
    if PROJECTS_DIR.is_dir():
        existing = [
            d.name
            for d in sorted(PROJECTS_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
            if d.is_dir() and not d.name.startswith(".") and d.name.lower() not in _INVALID_PROJECT_NAMES
        ]
        if existing:
            return existing[0]
    if env_proj and env_proj.lower() not in _INVALID_PROJECT_NAMES:
        return slugify_project_name(env_proj)
    return ""


def ensure_project_workspace(project_slug: str = "") -> Path:
    """
    Ensure `CORA/Projects/<project_slug>/` exists with isolated subdirectories
    (`Files/`, `downloads/`, `artifacts/`, `targets/`, `notes/`, `reasoning/`), `memory.md`, and `goals.md`.
    Never creates a dummy `active_session` or `default` folder inside `Projects/`.
    """
    ensure_vault_structure()
    slug = slugify_project_name(project_slug) if project_slug.strip() else get_active_project_slug()
    if slug:
        os.environ["CORA_ACTIVE_PROJECT"] = slug
        proj_dir = PROJECTS_DIR / slug
    else:
        slug = "unassigned"
        proj_dir = SESSION_STATE_DIR / "_unassigned_workspace"
    for sub in ("Files", "downloads", "artifacts", "targets", "notes", "reasoning"):
        (proj_dir / sub).mkdir(parents=True, exist_ok=True)
    mem_file = proj_dir / "memory.md"
    if not mem_file.exists():
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mem_file.write_text(
            "---\n"
            f"title: Project Memory ({slug})\n"
            "category: project_workspace\n"
            f"project: {slug}\n"
            f"summary: Isolated project memory, custom Files/, downloaded artifacts, target scans & test state for {slug}\n"
            f"updated: {now_str}\n"
            "---\n"
            f"# Project Workspace Memory (`Projects/{slug}/memory.md`)\n\n"
            "> **Two-Tier Memory Isolation:** Custom scripts and uploaded files (`Files/`), ephemeral test data, target scans, "
            "downloaded files (`downloads/`), and session notes for this project are isolated here so long-term universal knowledge in `ObsidianVault/` is never polluted.\n\n"
            "## 1. Verified Data & Architecture\n"
            f"- Workspace initialized at `Projects/{slug}/`\n"
            f"- Local Project Files & Custom Scripts directory: `Projects/{slug}/Files/`\n"
            f"- Project goals log: `Projects/{slug}/goals.md`\n"
            f"- Downloaded files directory: `Projects/{slug}/downloads/`\n\n"
            "## 2. Open Verification Questions\n"
            "- None\n\n"
            "## 3. Project Plan & Task Tracking\n"
            "- [ ] Initial project / test workspace ready\n\n"
            "## 4. Indexed Project Notes, Target Scans & Downloads\n"
            "<!-- PROJECT-INDEX-START -->\n"
            "<!-- PROJECT-INDEX-END -->\n",
            encoding="utf-8",
        )
    goals_file = proj_dir / "goals.md"
    if not goals_file.exists():
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        goals_file.write_text(
            "---\n"
            f"title: Project Goals History ({slug})\n"
            "category: project_goals\n"
            f"project: {slug}\n"
            f"summary: Chronological log of project goals and objectives for {slug}\n"
            f"updated: {now_str}\n"
            "---\n"
            f"# Project Goals (`Projects/{slug}/goals.md`)\n\n"
            f"> All goals set for project `{slug}` via `/goal <objective>` or `/relentless <objective>` are appended chronologically below. Running `/goal` displays the very last goal.\n\n"
            "## Goals History\n"
            "<!-- GOALS-HISTORY-START -->\n",
            encoding="utf-8",
        )
    return proj_dir


def get_project_goals_file(project_slug: str = "") -> Path:
    """Return `Projects/<project_slug>/goals.md`, ensuring the project workspace exists."""
    proj_dir = ensure_project_workspace(project_slug)
    return proj_dir / "goals.md"


def get_project_goals(project_slug: str = "") -> list[dict]:
    """
    Parse and return all chronological goals stored in `Projects/<project_slug>/goals.md`.
    Each item is `{"index": int, "timestamp": str, "goal": str}`.
    If `goals.md` has no entries yet but a legacy `notes/goal_*.md` exists in the project,
    automatically migrates that objective into `goals.md`.
    """
    proj_dir = ensure_project_workspace(project_slug)
    goals_file = proj_dir / "goals.md"
    txt = goals_file.read_text(encoding="utf-8", errors="replace") if goals_file.is_file() else ""
    entries: list[dict] = []

    pattern = re.compile(
        r"^###\s+Goal\s+#(\d+)\s+—\s+([^\n]+)\n-\s+\*\*Goal:\*\*\s*(.+?)(?=\n###\s+Goal\s+#|\Z)",
        flags=re.M | re.S,
    )
    for m in pattern.finditer(txt):
        g_idx = int(m.group(1))
        g_ts = m.group(2).strip()
        g_text = " ".join(line.strip() for line in m.group(3).strip().splitlines() if line.strip())
        if g_text:
            entries.append({"index": g_idx, "timestamp": g_ts, "goal": g_text})

    if not entries:
        # Check if legacy `notes/goal_*.md` files exist for this project and migrate them chronologically
        notes_dir = proj_dir / "notes"
        if notes_dir.is_dir():
            migrated = False
            for g_note in sorted(notes_dir.glob("goal_*.md"), key=lambda p: p.stat().st_mtime):
                try:
                    n_txt = g_note.read_text(encoding="utf-8", errors="replace")
                    m_obj = re.search(r"^-\s+\*\*Objective:\*\*\s*(.+)$", n_txt, flags=re.M)
                    m_upd = re.search(r"^updated:\s*(.+)$", n_txt, flags=re.M)
                    ts_val = m_upd.group(1).strip() if m_upd else datetime.fromtimestamp(g_note.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    if m_obj:
                        obj_str = m_obj.group(1).strip()
                        if obj_str and obj_str != "0" and not obj_str.startswith("Project "):
                            append_project_goal(obj_str, proj_dir.name, timestamp_override=ts_val)
                            migrated = True
                except Exception:
                    pass
            if migrated:
                txt = goals_file.read_text(encoding="utf-8", errors="replace") if goals_file.is_file() else ""
                for m in pattern.finditer(txt):
                    g_text = " ".join(line.strip() for line in m.group(3).strip().splitlines() if line.strip())
                    if g_text:
                        entries.append({"index": int(m.group(1)), "timestamp": m.group(2).strip(), "goal": g_text})
    return entries


def get_last_project_goal(project_slug: str = "") -> str:
    """Return the very last goal saved in `Projects/<project_slug>/goals.md` (or '' if none)."""
    goals = get_project_goals(project_slug)
    return goals[-1]["goal"] if goals else ""


def append_project_goal(goal_text: str, project_slug: str = "", timestamp_override: str = "") -> tuple[Path, int, bool]:
    """
    Append `goal_text` to `Projects/<project_slug>/goals.md` (if it is not already identical to the very last goal).
    Also indexes `goals.md` inside `Projects/<project_slug>/memory.md`.
    Returns `(goals_file_path, goal_number, was_appended)`.
    """
    clean_goal = " ".join(line.strip() for line in (goal_text or "").strip().splitlines() if line.strip())
    proj_dir = ensure_project_workspace(project_slug)
    goals_file = proj_dir / "goals.md"
    if not clean_goal:
        existing = get_project_goals(proj_dir.name)
        return goals_file, len(existing), False

    # Read current entries directly without recursion
    txt = goals_file.read_text(encoding="utf-8", errors="replace") if goals_file.is_file() else ""
    pattern = re.compile(
        r"^###\s+Goal\s+#(\d+)\s+—\s+([^\n]+)\n-\s+\*\*Goal:\*\*\s*(.+?)(?=\n###\s+Goal\s+#|\Z)",
        flags=re.M | re.S,
    )
    existing = []
    for m in pattern.finditer(txt):
        g_text = " ".join(line.strip() for line in m.group(3).strip().splitlines() if line.strip())
        if g_text:
            existing.append({"index": int(m.group(1)), "timestamp": m.group(2).strip(), "goal": g_text})

    if existing and existing[-1]["goal"] == clean_goal:
        return goals_file, existing[-1]["index"], False

    next_num = (existing[-1]["index"] + 1) if existing else 1
    now_str = (timestamp_override or "").strip() or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_block = f"\n### Goal #{next_num} — {now_str}\n- **Goal:** {clean_goal}\n"

    if not txt.strip():
        txt = (
            "---\n"
            f"title: Project Goals History ({proj_dir.name})\n"
            "category: project_goals\n"
            f"project: {proj_dir.name}\n"
            f"summary: Chronological log of project goals and objectives for {proj_dir.name}\n"
            f"updated: {now_str}\n"
            "---\n"
            f"# Project Goals (`Projects/{proj_dir.name}/goals.md`)\n\n"
            f"> All goals set for project `{proj_dir.name}` via `/goal <objective>` or `/relentless <objective>` are appended chronologically below. Running `/goal` displays the very last goal.\n\n"
            "## Goals History\n"
            "<!-- GOALS-HISTORY-START -->\n"
        )
    else:
        txt = re.sub(r"^updated:\s*.*$", f"updated: {now_str}", txt, flags=re.M)

    goals_file.write_text(txt.rstrip() + "\n" + entry_block, encoding="utf-8")
    update_project_memory_index(
        proj_dir,
        "goals",
        f"Project Goals History ({next_num} goal(s); latest: {clean_goal[:75]})",
        ["goal", "objectives"],
    )
    return goals_file, next_num, True


def update_project_memory_index(proj_dir: Path, rel_link: str, summary: str, tags: list = None) -> Path:
    """Update the `<!-- PROJECT-INDEX-START -->` section inside `Projects/<slug>/memory.md`."""
    mem_file = proj_dir / "memory.md"
    if not mem_file.exists():
        ensure_project_workspace(proj_dir.name)
    text = mem_file.read_text(encoding="utf-8", errors="replace")
    tag_str = " ".join(f"#{str(t).lstrip('#')}" for t in (tags or []) if str(t).strip())
    entry_line = f"- [[{rel_link}]] — {summary.strip()}" + (f" ({tag_str})" if tag_str else "")
    start_marker = "<!-- PROJECT-INDEX-START -->"
    end_marker = "<!-- PROJECT-INDEX-END -->"
    if start_marker in text and end_marker in text:
        before, rest = text.split(start_marker, 1)
        middle, after = rest.split(end_marker, 1)
        lines = [ln for ln in middle.strip().splitlines() if ln.strip()]
        updated = False
        for idx, ln in enumerate(lines):
            if f"[[{rel_link}]]" in ln:
                lines[idx] = entry_line
                updated = True
                break
        if not updated:
            lines.append(entry_line)
        lines = lines[-50:]
        new_text = f"{before}{start_marker}\n" + "\n".join(lines) + f"\n{end_marker}{after}"
    else:
        new_text = text.rstrip() + f"\n\n## 4. Indexed Project Notes, Target Scans & Downloads\n{start_marker}\n{entry_line}\n{end_marker}\n"
    mem_file.write_text(new_text, encoding="utf-8")
    return mem_file


def _redirect_tmp_downloads_to_project(cmd: str) -> str:
    """
    Redirect `/tmp/<filename>` download/output targets in shell commands (e.g. `curl -o /tmp/out.json`,
    `wget -O /tmp/file`, `> /tmp/dump.txt`) into `CORA/Projects/<project>/downloads/<filename>`
    so downloaded project data is stored inside the active project workspace.
    """
    if "/tmp/" not in cmd:
        return cmd
    proj_dl_dir = ensure_project_workspace() / "downloads"
    return re.sub(
        r"((?:-o|-O|--output|--output-document|>|>>|\btee\s+(?:-a\s+)?)\s*['\"]?)/tmp/([a-zA-Z0-9_.\-]+)",
        lambda m: f"{m.group(1)}{proj_dl_dir}/{m.group(2)}",
        cmd,
    )


def update_vault_index(wiki_link: str, summary: str, tags: list) -> None:
    ensure_vault_structure()
    text = INDEX_FILE.read_text(encoding="utf-8", errors="replace")
    tag_str = " ".join(f"#{t.lstrip('#')}" for t in tags if t.strip())
    entry_line = f"- [[{wiki_link}]] — {summary.strip()}" + (f" ({tag_str})" if tag_str else "")

    start_marker = "<!-- AUTO-INDEX-START -->"
    end_marker = "<!-- AUTO-INDEX-END -->"
    if start_marker in text and end_marker in text:
        before, rest = text.split(start_marker, 1)
        middle, after = rest.split(end_marker, 1)
        lines = [ln for ln in middle.strip().splitlines() if ln.strip()]
        # Replace existing line for same wiki_link or append
        updated = False
        for idx, ln in enumerate(lines):
            if f"[[{wiki_link}]]" in ln:
                lines[idx] = entry_line
                updated = True
                break
        if not updated:
            lines.append(entry_line)
        # Keep index compact (latest 35 entries)
        lines = lines[-35:]
        new_text = f"{before}{start_marker}\n" + "\n".join(lines) + f"\n{end_marker}{after}"
    else:
        new_text = text.rstrip() + f"\n\n## Indexed Vault Notes\n{start_marker}\n{entry_line}\n{end_marker}\n"

    INDEX_FILE.write_text(new_text, encoding="utf-8")


def save_note_to_vault(
    category: str,
    title: str,
    summary: str,
    content: str,
    tags: list = None,
    persist_long_term: bool = False,
) -> str:
    """
    Two-Tier Memory Saver:
    - When `persist_long_term=False` (default for `project_tracker`, `scan_target`, `_sync_goal_and_attempts_to_vault`,
      and `vault_save_note` during active project/test work), notes and target scans are saved into
      `CORA/Projects/<active_project>/` and indexed in `Projects/<active_project>/memory.md`.
    - When `persist_long_term=True` (used by `/remember <fact>`), universal facts are saved into
      `CORA/core/ObsidianVault/<category>/<slug>.md` and indexed in `00_MEMORY_INDEX.md`.
    """
    ensure_vault_structure()
    cat = category.strip().lower() if category else "knowledge"
    if cat not in VALID_CATEGORIES:
        cat = "knowledge"
    slug = slugify(title)
    tags = tags or [cat]
    clean_tags = [re.sub(r"[^a-zA-Z0-9_\-]", "", t.lstrip("#")).lower() for t in tags if t]
    clean_tags = [t for t in clean_tags if t] or [cat]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if persist_long_term:
        note_path = VAULT_DIR / cat / f"{slug}.md"
        frontmatter = (
            "---\n"
            f"title: {title}\n"
            f"category: {cat}\n"
            f"summary: {summary}\n"
            f"tags: [{', '.join(clean_tags)}]\n"
            f"updated: {now_str}\n"
            "---\n"
        )
        body = (
            f"# {title}\n\n"
            f"> **Summary:** {summary}  \n"
            f"> **Backlink:** [[00_MEMORY_INDEX]] | **Updated:** `{now_str}`\n\n"
            f"{content.strip()}\n"
        )
        note_path.write_text(frontmatter + body, encoding="utf-8")
        wiki_link = f"{cat}/{slug}"
        update_vault_index(wiki_link, summary, clean_tags)
        return f"Saved long-term Obsidian note `[[{wiki_link}]]` ({note_path}) and updated `00_MEMORY_INDEX.md`."

    # Project-scoped storage inside CORA/Projects/<project_slug>/
    proj_slug = slugify_project_name(title) if (cat == "projects" and not slug.startswith("goal_")) else get_active_project_slug()
    proj_dir = ensure_project_workspace(proj_slug)
    mem_file = proj_dir / "memory.md"

    if cat == "projects" and not slug.startswith("goal_"):
        # Preserve existing indexed project notes block when updating `memory.md` via `project_tracker`
        index_section = (
            "## 4. Indexed Project Notes, Target Scans & Downloads\n"
            "<!-- PROJECT-INDEX-START -->\n"
            "<!-- PROJECT-INDEX-END -->\n"
        )
        if mem_file.exists():
            old_txt = mem_file.read_text(encoding="utf-8", errors="replace")
            m_idx = re.search(
                r"(## 4\. Indexed Project Notes.*<!-- PROJECT-INDEX-END -->)",
                old_txt,
                flags=re.S,
            )
            if m_idx:
                index_section = m_idx.group(1).strip() + "\n"
        frontmatter = (
            "---\n"
            f"title: {title}\n"
            "category: project_workspace\n"
            f"project: {proj_slug}\n"
            f"summary: {summary}\n"
            f"tags: [{', '.join(clean_tags)}]\n"
            f"updated: {now_str}\n"
            "---\n"
        )
        body = (
            f"# Project Workspace Memory (`Projects/{proj_slug}/memory.md`)\n\n"
            f"> **Summary:** {summary}  \n"
            f"> **Workspace:** `{proj_dir}` | **Downloads:** `{proj_dir / 'downloads'}` | **Updated:** `{now_str}`\n\n"
            f"{content.strip()}\n\n"
            f"{index_section}"
        )
        mem_file.write_text(frontmatter + body, encoding="utf-8")
        return f"Saved project memory `[[Projects/{proj_slug}/memory]]` ({mem_file})."

    sub_folder = "targets" if cat == "targets" else ("reasoning" if cat == "reasoning" else "notes")
    note_path = proj_dir / sub_folder / f"{slug}.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = (
        "---\n"
        f"title: {title}\n"
        f"category: {cat}\n"
        f"project: {proj_dir.name}\n"
        f"summary: {summary}\n"
        f"tags: [{', '.join(clean_tags)}]\n"
        f"updated: {now_str}\n"
        "---\n"
    )
    body = (
        f"# {title}\n\n"
        f"> **Summary:** {summary}  \n"
        f"> **Project Workspace:** `Projects/{proj_dir.name}/` | **Backlink:** [[memory]] | **Updated:** `{now_str}`\n\n"
        f"{content.strip()}\n"
    )
    note_path.write_text(frontmatter + body, encoding="utf-8")
    rel_link = f"{sub_folder}/{slug}"
    update_project_memory_index(proj_dir, rel_link, summary, clean_tags)
    return (
        f"Saved project note `[[Projects/{proj_dir.name}/{rel_link}]]` ({note_path}) "
        f"and updated `Projects/{proj_dir.name}/memory.md` (long-term `ObsidianVault/` kept clean)."
    )


def search_vault(query: str) -> str:
    ensure_vault_structure()
    q = query.strip().lower()
    tokens = [t for t in re.split(r"\s+", q) if t]
    results = []

    # 1. Search active & existing project workspaces in `CORA/Projects/`
    if PROJECTS_DIR.is_dir():
        for md in sorted(PROJECTS_DIR.rglob("*.md")):
            try:
                rel = md.relative_to(CORA_ROOT).with_suffix("")
            except ValueError:
                try:
                    rel = Path("Projects") / md.relative_to(PROJECTS_DIR).with_suffix("")
                except ValueError:
                    rel = Path(md.stem)
            text = md.read_text(encoding="utf-8", errors="replace")
            haystack = f"{rel}\n{text}".lower()
            score = sum(1 for tok in tokens if tok in haystack)
            if not tokens or score > 0:
                matching_lines = []
                for ln in text.splitlines():
                    if any(tok in ln.lower() for tok in tokens):
                        matching_lines.append(ln.strip())
                    if len(matching_lines) >= 4:
                        break
                snippet = " | ".join(matching_lines) if matching_lines else text[:200].replace("\n", " ")
                # Slightly boost active project hits so current project context ranks first
                boost = 1 if get_active_project_slug() in md.parts else 0
                results.append((score + boost, str(rel), snippet[:300]))

    # 2. Search long-term universal `ObsidianVault/`
    for md in sorted(VAULT_DIR.rglob("*.md")):
        if ".obsidian" in md.parts:
            continue
        rel = md.relative_to(VAULT_DIR).with_suffix("")
        text = md.read_text(encoding="utf-8", errors="replace")
        haystack = f"{rel}\n{text}".lower()
        score = sum(1 for tok in tokens if tok in haystack)
        if not tokens or score > 0:
            # Find matching lines
            matching_lines = []
            for ln in text.splitlines():
                if any(tok in ln.lower() for tok in tokens):
                    matching_lines.append(ln.strip())
                if len(matching_lines) >= 4:
                    break
            snippet = " | ".join(matching_lines) if matching_lines else text[:200].replace("\n", " ")
            results.append((score, str(rel), snippet[:300]))

    results.sort(key=lambda x: (-x[0], x[1]))
    out = []
    if results:
        out.append(f"Projects & ObsidianVault keyword search results for '{query}' (use `vault_read_note` to read full note):")
        for score, rel, snip in results[:10]:
            out.append(f"  - [[{rel}]]: {snip}")
    else:
        out.append(f"No direct keyword matches in Projects/ or ObsidianVault/ for '{query}'.")

    # Augment with Associative Bipartite Vault Graph Spreading Activation (Personalized PageRank + Bridge Concepts)
    try:
        from Reasoning.engines.associative import run_associative_vault_reasoning

        assoc = run_associative_vault_reasoning(query=query, top_k=4, save_to_vault=False)
        act_notes = assoc.get("activated_notes", [])
        bridges = assoc.get("bridge_concepts", [])
        if act_notes:
            out.append("\n[Associative Bipartite Graph (Personalized PageRank) Top Activated Notes]:")
            for an in act_notes[:4]:
                out.append(
                    f"  - [[{an['wiki_link']}]] (activation={an['activation_score']:.4f}, shared={an['shared_concepts'][:3]}) — {an['summary']}"
                )
        if bridges:
            bridge_str = ", ".join(f"`{b['concept']}` ({b['bridged_notes_count']} notes)" for b in bridges[:4])
            out.append(f"[Discovered Cross-Note Bridge Concepts]: {bridge_str}")
    except Exception:
        pass

    return "\n".join(out)


def read_vault_note(note_ref: str) -> str:
    ensure_vault_structure()
    cleaned = note_ref.strip().strip("[]")
    if not cleaned.endswith(".md"):
        cleaned_md = cleaned + ".md"
    else:
        cleaned_md = cleaned

    proj_slug = get_active_project_slug()
    proj_dir = PROJECTS_DIR / proj_slug

    # Check if `projects/<name>` refers to `Projects/<name>/memory.md`
    proj_candidates = []
    if cleaned.startswith("projects/"):
        p_name = slugify_project_name(Path(cleaned).stem)
        proj_candidates.append(PROJECTS_DIR / p_name / "memory.md")
        proj_candidates.append(PROJECTS_DIR / slugify(Path(cleaned).stem) / "memory.md")
        proj_candidates.append(proj_dir / "notes" / f"{slugify(Path(cleaned).stem)}.md")
    elif cleaned in ("memory", "memory.md"):
        proj_candidates.append(proj_dir / "memory.md")

    candidates = [
        *proj_candidates,
        CORA_ROOT / cleaned_md,
        CORA_ROOT / cleaned,
        BASE_DIR / cleaned_md,
        BASE_DIR / cleaned,
        proj_dir / cleaned_md,
        proj_dir / cleaned,
        proj_dir / "targets" / Path(cleaned_md).name,
        proj_dir / "notes" / Path(cleaned_md).name,
        proj_dir / "reasoning" / Path(cleaned_md).name,
        VAULT_DIR / cleaned_md,
        VAULT_DIR / cleaned,
        *[VAULT_DIR / c / Path(cleaned_md).name for c in VALID_CATEGORIES],
    ]
    for cand in candidates:
        if cand.is_file():
            return compact_text(cand.read_text(encoding="utf-8", errors="replace"), MAX_TOOL_OUTPUT_CHARS)

    # Fuzzy filename match across Projects/ first, then ObsidianVault/
    slug = slugify(Path(cleaned).stem)
    if PROJECTS_DIR.is_dir():
        for md in PROJECTS_DIR.rglob("*.md"):
            if md.stem.lower() == slug or (md.name == "memory.md" and md.parent.name.lower() == slug):
                return compact_text(md.read_text(encoding="utf-8", errors="replace"), MAX_TOOL_OUTPUT_CHARS)
    for md in VAULT_DIR.rglob("*.md"):
        if md.stem.lower() == slug:
            return compact_text(md.read_text(encoding="utf-8", errors="replace"), MAX_TOOL_OUTPUT_CHARS)

    return f"Note '{note_ref}' not found in {PROJECTS_DIR} or {VAULT_DIR}. Try `vault_search` first."


def get_vault_context_for_prompt() -> str:
    ensure_vault_structure()
    index_text = INDEX_FILE.read_text(encoding="utf-8", errors="replace").strip()
    return compact_text(index_text, 1800)


def read_single_doc_file(path: Path, max_chars: int = 6000) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            out = subprocess.check_output(
                ["pdftotext", str(path), "-"], text=True, stderr=subprocess.DEVNULL, timeout=15
            )
            return compact_text(out.strip(), max_chars)
        except Exception as exc:
            return f"(Could not extract PDF text from {path.name}: {exc})"
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        return compact_text(raw.strip(), max_chars)
    except Exception as exc:
        return f"(Could not read {path.name}: {exc})"


def load_documentation_source(doc_source: str, max_total_chars: int = 8000) -> tuple[str, str]:
    """Load documentation from a local file, directory of files, or URL.
    Returns (derived_project_name, formatted_documentation_digest).
    """
    src = doc_source.strip()
    if re.match(r"^https?://", src, re.I):
        derived = slugify(re.sub(r"^https?://", "", src))
        report = perform_target_scan(src)
        return derived, f"Documentation URL: {src}\n\n{compact_text(report, max_total_chars)}"

    p = Path(os.path.expanduser(src)).resolve()
    if not p.exists():
        raise FileNotFoundError(f"Documentation path not found: {p}")

    if p.is_file():
        derived = slugify(p.stem)
        content = read_single_doc_file(p, max_total_chars)
        return derived, f"### Documentation File: `{p}`\n\n{content}"

    # Directory: gather readable documentation files
    derived = slugify(p.name)
    doc_files = []
    for candidate in sorted(p.rglob("*")):
        if candidate.is_file() and not any(part.startswith(".") for part in candidate.relative_to(p).parts):
            if candidate.suffix.lower() in DOC_EXTENSIONS or candidate.stat().st_size < 100_000:
                doc_files.append(candidate)
        if len(doc_files) >= 25:
            break

    if not doc_files:
        return derived, f"### Documentation Directory: `{p}`\n(No readable documentation files found)"

    per_file_budget = max(800, max_total_chars // max(1, min(len(doc_files), 8)))
    sections = [f"### Documentation Directory: `{p}` ({len(doc_files)} files discovered)"]
    used = 0
    for df in doc_files[:12]:
        rel = df.relative_to(p)
        snippet = read_single_doc_file(df, per_file_budget)
        block = f"\n#### File: `{rel}` ({df.stat().st_size} bytes)\n{snippet}\n"
        if used + len(block) > max_total_chars and len(sections) > 1:
            sections.append(f"\n*(Additional files in `{p}` omitted from initial digest; use `read_file` to inspect on demand)*")
            break
        sections.append(block)
        used += len(block)

    return derived, "\n".join(sections)


_CROW_LOGO_FALLBACK_LINES = (
    ".=+:.                      .:+=.",
    ".=##**++=-            -=+***##= ",
    "  -###%#*+%*  =%%- .*%+*#####-  ",
    "   .=++#%%***-#@@*:*#*%%#*+=.   ",
    "     =+**###*#*##*#*###**+=     ",
    "       .-+*#%***#**%#*+-.       ",
    "            .#%%#%#.            ",
    "           :+**%%**+:           ",
    "              :++:              ",
)

_CORA_BANNER_LINES = (
    "  _____       ____       _____         ___       ",
    " / ____|     / __ \\     |  __ \\       / _ \\      ",
    "| |         | |  | |    | |__) |     / /_\\ \\     ",
    "| |____  _  | |__| | _  |  _  /  _  / _____ \\  _ ",
    " \\_____|(_)  \\____/ (_) |_| \\_\\ (_) /_/   \\_\\ (_)",
    "",
    "",
    "  Cyber Oriented Reasoning Agent",
    "  ------------------------------",
)


def _load_crow_logo_ascii(width: int = 32, height: int = 9) -> list[str]:
    """
    Dynamically render the CROW logo (`CROW_Logo-NoWords_Transparent_Glow-NoBackground.png`
    or `CROW_Logo_White_TransparentBackground.webp`) to a left-aligned
    `width x height` ASCII block matching the height from the top of the `C.O.R.A.` banner (`5` lines)
    to the bottom of the `Cyber Oriented Reasoning Agent` subtitle (`9` lines total).
    Falls back to the pre-rendered `_CROW_LOGO_FALLBACK_LINES` if Pillow or the image file is unavailable.
    """
    candidates = [
        BASE_DIR / "Explained" / "assets" / "CROW_Logo-NoWords_Transparent_Glow-NoBackground.png",
        BASE_DIR / "Explained" / "assets" / "CROW_Logo_White_TransparentBackground.webp",
        Path.home() / "Pictures" / "CROW_Logo-NoWords_Transparent_Glow-NoBackground.png",
        Path.home() / "Pictures" / "CROW_Logo_White_TransparentBackground.webp",
    ]
    for img_path in candidates:
        if img_path.is_file():
            try:
                from PIL import Image

                img = Image.open(img_path).convert("RGBA")
                w_orig, h_orig = img.size
                # Sample into width x height grid using box/bilinear averaging
                resample_mode = getattr(getattr(Image, "Resampling", Image), "BOX", Image.BILINEAR)
                small = img.resize((width, height), resample_mode)
                chars = " .:-=+*#%@"
                lines = []
                for y in range(height):
                    row_chars = []
                    for x in range(width):
                        r, g, b, a = small.getpixel((x, y))
                        luma = (0.299 * r + 0.587 * g + 0.114 * b) * (a / 255.0)
                        c_idx = min(len(chars) - 1, int(luma / 256.0 * len(chars)))
                        row_chars.append(chars[c_idx])
                    lines.append("".join(row_chars))
                if any(ln.strip() for ln in lines):
                    return lines
            except Exception:
                pass
    return list(_CROW_LOGO_FALLBACK_LINES)


import hashlib

CORA_VERSION_FILE = BASE_DIR / "Log" / "cora_version.json"
# 1st section: Major CLI Overhaul version (v5 = C.O.R.A. Splash + Project Menu + Continuation + Red/White/Blue -netiso + Quoted Goals & -param:value + Switch Table & Legal Disclaimer)
CORA_MAJOR_CLI_OVERHAUL = 5
# Baseline historical counts from Log/VERSION_HISTORY_AND_CHANGELOG.md
CORA_BASELINE_ENGINE_REV = 11
CORA_BASELINE_PATCH_REV = 8


def _compute_files_digest(paths: list[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda x: str(x)):
        try:
            if p.is_file():
                st = p.stat()
                h.update(f"{p.name}:{st.st_size}:".encode("utf-8"))
                h.update(p.read_bytes())
        except Exception:
            pass
    return h.hexdigest()


def get_cora_version_info(bump_patch_reason: str = "", bump_engine_reason: str = "") -> dict:
    """
    Compute and persist the 3-section C.O.R.A. semantic version (`<CLI_Overhaul>.<Engine_Rev>.<Patch_Rev>`):
      - 1st Decimal Section (`major_cli`): Major CLI Overhaul (currently `5`, reflecting today's C.O.R.A. overhaul).
      - 2nd Decimal Section (`engine_rev`): Increments automatically whenever any Reasoning or Logic Engine
        in `Reasoning/engines/*.py` or `Reasoning/reasoning_cli.py` is updated or modified.
      - 3rd Decimal Section (`patch_rev`): Increments automatically whenever documentation (`README.md`,
        `CORA_RunCMDs.md`, `SetupHowItWorks.md`, `Explained/*.md`), tools (`report_generator.py`,
        `train_llm.py`), or system training (`training_manifest.json` / `/train`) are updated.
    """
    eng_dir = BASE_DIR / "Reasoning" / "engines"
    eng_files = list(eng_dir.glob("*.py")) if eng_dir.is_dir() else []
    r_cli = BASE_DIR / "Reasoning" / "reasoning_cli.py"
    if r_cli.is_file():
        eng_files.append(r_cli)
    cur_eng_sha = _compute_files_digest(eng_files)

    patch_files = [
        CORA_ROOT / "README.md",
        CORA_ROOT / "run_cora_NIX.sh",
        CORA_ROOT / "run_cora_WIN.ps1",
        CORA_ROOT / "setup_cora_NIX.sh",
        CORA_ROOT / "setup_cora_WIN.ps1",
        BASE_DIR / "CORA_RunCMDs.md",
        BASE_DIR / "SetupHowItWorks.md",
        BASE_DIR / "Reasoning" / "report_generator.py",
        BASE_DIR / "Reasoning" / "train_llm.py",
        BASE_DIR / "Reasoning" / "data" / "training_manifest.json",
        BASE_DIR / "Reasoning" / "data" / "trained_rules.json",
    ]
    exp_dir = BASE_DIR / "Explained"
    if exp_dir.is_dir():
        patch_files.extend(exp_dir.glob("*.md"))
    cur_patch_sha = _compute_files_digest(patch_files)

    data: dict = {}
    if CORA_VERSION_FILE.is_file():
        try:
            data = json.loads(CORA_VERSION_FILE.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            data = {}

    major_cli = max(CORA_MAJOR_CLI_OVERHAUL, int(data.get("major_cli", CORA_MAJOR_CLI_OVERHAUL)))
    engine_rev = max(CORA_BASELINE_ENGINE_REV, int(data.get("engine_rev", CORA_BASELINE_ENGINE_REV)))
    patch_rev = max(CORA_BASELINE_PATCH_REV, int(data.get("patch_rev", CORA_BASELINE_PATCH_REV)))

    prev_eng_sha = data.get("engine_tree_sha256", "")
    prev_patch_sha = data.get("patch_tree_sha256", "")
    changed = not bool(data)
    reason = data.get(
        "last_update_reason",
        "Major CLI Overhaul v5 + 11 Tracked Engine Milestones + Docs/Tools/Training Rev 8",
    )

    if bump_engine_reason or (prev_eng_sha and prev_eng_sha != cur_eng_sha):
        engine_rev += 1
        reason = bump_engine_reason or "Reasoning/logic engine module modified"
        changed = True

    if bump_patch_reason or (prev_patch_sha and prev_patch_sha != cur_patch_sha):
        patch_rev += 1
        reason = bump_patch_reason or "Documentation, tools, or training corpus updated"
        changed = True

    ver_str = f"{major_cli}.{engine_rev}.{patch_rev}"
    if data.get("version") != ver_str:
        changed = True

    out = {
        "major_cli": major_cli,
        "engine_rev": engine_rev,
        "patch_rev": patch_rev,
        "version": ver_str,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S") if changed else data.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "engine_tree_sha256": cur_eng_sha,
        "patch_tree_sha256": cur_patch_sha,
        "last_update_reason": reason,
    }
    if changed:
        try:
            CORA_VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
            CORA_VERSION_FILE.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        except Exception:
            pass
    return out


import textwrap

DEFAULT_BANNER_WIDTH = 100


def get_terminal_banner_width(default_width: int = DEFAULT_BANNER_WIDTH) -> int:
    """Return banner width adapted to the live terminal width (up to `default_width`)."""
    if not sys.stdout.isatty():
        return default_width
    try:
        cols = shutil.get_terminal_size((default_width, 24)).columns
        return max(48, min(default_width, cols - 1))
    except Exception:
        return default_width


_CORA_DESCRIPTION_LINES = (
    "C.O.R.A. is a multi-layered reasoning agent that combines AI and a cybersecurity focused",
    "Super Intelligence system to support Red, Blue, and Hunt Teams. Its Analyst, Active, and",
    "Passive modes help teams analyze scan results and system data, identify potential",
    "weaknesses and threats, and create clear reports for technical teams and leadership.",
)

_CORA_DISCLAIMER_LINES = (
    "--- OPEN-SOURCE NOTICE, ATTRIBUTION & LIMITATION OF LIABILITY ---",
    "C.O.R.A. is open-source software under active development and continuous refinement.",
    "Redistribution, modification, or operational deployment is permitted provided that clear",
    "attribution and development credit to https://CROWinnovations.com are retained in all copies",
    'and derivative works. C.O.R.A. and its layered reasoning engines are provided "AS IS" without',
    "warranty of any kind. The developer assumes no liability or legal responsibility for any",
    "actions, damages, data loss, or legal consequences arising from the use of this system.",
)


def render_cora_splash_screen(posture: dict | None = None, banner_width: int | None = None) -> None:
    """
    Display the C.O.R.A. (Cyber Oriented Reasoning Agent) ASCII splash screen at CLI opening (default 100 columns wide,
    automatically adapting when the terminal window is narrower so lines never wrap or corrupt on resize):
      - Left-aligned Crow ASCII graphic (height = top of C.O.R.A. banner to bottom of full name, width = 32 cols).
      - Top banner displaying 5-line ASCII `C.O.R.A.` with spacing rows below to `Cyber Oriented Reasoning Agent`,
        centered cleanly in the banner area to the right of the Crow.
      - Below the title & crow image (and above the Version/Developed by lines): centered multi-layered reasoning description
        supporting Red, Blue, and Hunt Teams.
      - Above the Developed by line (bottom-left): `Version: <CLI_Overhaul>.<Engine_Rev>.<Patch_Rev>` (e.g. `Version: 5.14.11`).
      - Bottom-left subtly sized developer line: `Developed by: https://CROWinnovations.com`.
    """
    bw = banner_width if banner_width is not None else get_terminal_banner_width(DEFAULT_BANNER_WIDTH)
    p = posture or ACTIVE_POSTURE or _refresh_active_posture()
    border_col = p.get("ansi_border", "\033[1;36m")
    accent_col = p.get("ansi_accent", "\033[1;37m")
    ascii_block_w = max(len(ln.rstrip()) for ln in _CORA_BANNER_LINES[:5])
    ver_info = get_cora_version_info()
    ver_str = ver_info["version"]

    print(f"\n{border_col}{'=' * bw}\033[0m")
    if bw >= 86:
        crow_w = min(32, max(18, bw - ascii_block_w - 5))
        crow_lines = _load_crow_logo_ascii(width=crow_w, height=len(_CORA_BANNER_LINES))
        left_used = 2 + crow_w
        right_space = max(ascii_block_w, bw - left_used)
        gap_after_crow = max(2, (right_space - ascii_block_w) // 2)
        for idx, (c_ln, b_ln) in enumerate(zip(crow_lines, _CORA_BANNER_LINES)):
            if idx < 5:
                b_padded = (" " * gap_after_crow) + b_ln.rstrip()
                b_styled = f"\033[1;97m{b_padded}\033[0m"
            elif idx in (7, 8):
                sub_txt = b_ln.strip()
                sub_gap = max(2, gap_after_crow + (ascii_block_w - len(sub_txt)) // 2)
                if idx == 7:
                    b_styled = (" " * sub_gap) + f"{accent_col}\033[1m{sub_txt}\033[0m"
                else:
                    b_styled = (" " * sub_gap) + f"\033[2;37m{sub_txt}\033[0m"
            else:
                b_styled = ""
            print(f"  \033[1;37m{c_ln}\033[0m{b_styled}")
    else:
        # Compact stacked layout for narrow terminal windows (< 86 columns)
        for idx, b_ln in enumerate(_CORA_BANNER_LINES):
            if idx < 5:
                print(f"\033[1;97m{b_ln.rstrip()[:bw].center(bw)}\033[0m")
            elif idx == 7:
                print(f"{accent_col}\033[1m{b_ln.strip().center(bw)}\033[0m")
            elif idx == 8:
                print(f"\033[2;37m{b_ln.strip().center(bw)}\033[0m")

    print()
    desc_lines = (
        list(_CORA_DESCRIPTION_LINES)
        if bw >= max(len(ln) for ln in _CORA_DESCRIPTION_LINES)
        else textwrap.wrap(" ".join(_CORA_DESCRIPTION_LINES), width=max(40, bw - 4))
    )
    for desc_ln in desc_lines:
        print(f"\033[0;37m{desc_ln.center(bw)}\033[0m")
    print()
    print(f"  \033[2;37mVersion: {ver_str}\033[0m")
    print("  \033[2;37mDeveloped by: https://CROWinnovations.com\033[0m")
    print(f"{border_col}{'=' * bw}\033[0m\n")


def render_session_intro_banner(
    posture: dict | None = None,
    restored_session_info: dict | None = None,
    startup_continue_session: bool = False,
) -> None:
    """Render the C.O.R.A. session status & legal disclaimer block scaled to the active terminal width."""
    bw = get_terminal_banner_width(DEFAULT_BANNER_WIDTH)
    p = posture or ACTIVE_POSTURE or _refresh_active_posture()
    p_border = p.get("ansi_border", "\033[1;32m")
    p_accent = p.get("ansi_accent", "\033[1;32m")
    p_badge = p.get("banner_badge", "[POSTURE: UNRESTRICTED]")
    p_ifaces = p.get("allowed_interfaces") or []
    pmode_key = (ACTIVE_PERSONALITY_MODE or "DEFAULT").upper()
    pmode_num = {"DEFAULT": "1", "ANALYST": "2", "BERSERKER": "3", "NINJA": "4"}.get(pmode_key, "1")
    pmode_meta = PERSONALITY_MODES_META[pmode_num]
    perm_status = (
        "\033[1;31mAUTO-RUN (--dangerously-skip-permissions enabled)\033[0m"
        if SKIP_PERMISSIONS
        else "\033[1;32mCONFIRM ON [y/N/a] (pass --dangerously-skip-permissions to auto-run)\033[0m"
    )

    if startup_continue_session:
        r_info = restored_session_info or {}
        if r_info.get("restored"):
            print(
                f"\033[1;32m=== Session Restored (`--continue` from `{r_info.get('source')}`) ===\033[0m\n"
                f"  Saved At:       `{r_info.get('saved_at')}`\n"
                f"  Active Project: `{r_info.get('active_project') or 'None'}`\n"
                f"  Active Goal:    `{r_info.get('active_goal') or 'None'}`\n"
                f"  History Loaded: `{r_info.get('message_count')}` messages | `{r_info.get('attempt_count')}` tool attempts (Wave `{r_info.get('current_wave')}`)\n"
                f"  Tip:            Type `/relentless` to immediately resume autonomous wave execution, or enter your next instruction below.\n"
            )
        else:
            print(
                f"\033[1;33m[Continuation Notice]\033[0m {r_info.get('reason', 'No previous session found.')} Starting a fresh session.\n"
            )

    intro_hdr = " C.O.R.A. Local System Agent CLI + Obsidian Vault ".center(bw, "=")
    print(f"{p_border}{intro_hdr}\033[0m")
    print(f"  Active Project: \033[1;36mProjects/{get_active_project_slug()}/\033[0m (`/project` to switch, rename, or create)")
    print(f"  Session Mode:   {pmode_meta['color']}[{pmode_num}] {pmode_meta['label']}\033[0m — {pmode_meta['purpose']} (`/mode` to view/switch)")
    print(f"  Security Mode:  {p_accent}{p_badge}\033[0m")
    if p.get("mode") == "ISOLATED_LAN_USB" and p_ifaces:
        print(f"  Allowed Ifaces: \033[1;36m{', '.join(p_ifaces)}\033[0m (Locked by Blue Network Isolation; all other host NICs blocked)")
    elif p.get("mode") == "AIR_GAPPED_NETNS":
        print("  Namespace Lock: \033[1;97mLinux Network Namespace (`unshare -r -n`, `lo` loopback only — 0 external NICs)\033[0m")
    print(f"  Active Model:   \033[1m{MODEL_NAME}\033[0m")
    print(f"  Obsidian Vault: \033[1;36m{VAULT_DIR}\033[0m (Long-Term Universal Knowledge)")
    print(f"  Projects Dir:   \033[1;36m{PROJECTS_DIR}\033[0m (Isolated Project Downloads, Scans & `memory.md`)")
    print(f"  Project Files:  \033[1;36mProjects/{get_active_project_slug()}/Files/\033[0m (`/files` or `/upload <path>` to add files for LLM)")
    print(f"  Working Dir:    {os.getcwd()}")
    print(f"  Permissions:    {perm_status}")
    print()
    disc_header = _CORA_DISCLAIMER_LINES[0].center(bw)
    print(f"\033[1;33m{disc_header}\033[0m")
    disc_body = (
        list(_CORA_DISCLAIMER_LINES[1:])
        if bw >= max(len(ln) for ln in _CORA_DISCLAIMER_LINES[1:])
        else textwrap.wrap(" ".join(_CORA_DISCLAIMER_LINES[1:]), width=max(40, bw - 4))
    )
    for d_line in disc_body:
        print(f"\033[2;37m{d_line.center(bw)}\033[0m")
    print(f"{p_border}{'=' * bw}\033[0m\n")


def redraw_cli_on_resize() -> None:
    """
    Repaint the active CLI view (interactive menu or C.O.R.A. splash + session header +
    recorded session transcript + bottom-pinned HUD bar) when the terminal window is resized,
    preventing ConPTY/terminal reflow from scrolling text into blank space or overwriting prompts.
    """
    if not sys.stdout.isatty():
        return
    with HUD._lock, _raw_terminal_output():
        try:
            sz = shutil.get_terminal_size((80, 24))
            cols, rows = max(20, sz.columns), max(6, sz.lines)
            # Unlock DECSTBM scroll margins to full screen, reset SGR, and clear viewport & reflow artifacts
            sys.stdout.write(f"\033[r\033[1;{rows}r\033[0m\033[2J\033[3J\033[H")
            sys.stdout.flush()
            posture = _refresh_active_posture(apply_osc=True, quiet=True)
            if _ACTIVE_MENU_REDRAW_FN is not None:
                _ACTIVE_MENU_REDRAW_FN()
            elif _CLI_VIEW_STATE == "main_session":
                render_cora_splash_screen(posture)
                render_session_intro_banner(
                    posture=posture,
                    restored_session_info=_LAST_RESTORED_SESSION_INFO,
                    startup_continue_session=_LAST_STARTUP_CONTINUE,
                )
                if _SESSION_TRANSCRIPT_CHUNKS:
                    transcript_text = "".join(_SESSION_TRANSCRIPT_CHUNKS)
                    sys.stdout.write(transcript_text)
                    if not transcript_text.endswith("\n"):
                        sys.stdout.write("\n")
            sys.stdout.flush()
            if HUD.active and HUD.mode == "pin":
                HUD._last_cols, HUD._last_rows = cols, rows
                HUD._pending_resize_dims = (cols, rows)
                HUD._resize_in_progress = False
                sys.stdout.write(f"\n\033[1A\0337\033[1;{rows - 1}r\0338")
                sys.stdout.flush()
                HUD.render(force_region=True)
        except Exception:
            pass


def render_simplified_switches_table(posture: dict | None = None, table_width: int = DEFAULT_BANNER_WIDTH) -> None:
    """
    Render a simplified, scannable table of available `run_cora_NIX.sh` / `run_cora_WIN.ps1` startup switches/commands
    and in-CLI `/` slash commands (default 200 columns wide with centered headers).
    """
    p = posture or ACTIVE_POSTURE or _refresh_active_posture()
    border_col = p.get("ansi_border", "\033[1;36m")
    ver_str = get_cora_version_info()["version"]
    inner_w = max(78, table_width - 2)
    col1_w = 56
    col2_w = inner_w - col1_w - 5  # accounts for " " + col1_w + " │ " + col2_w + " " = inner_w

    title_str = f"C.O.R.A. v{ver_str} — Simplified Available Switches & Commands Reference".center(inner_w)
    h1_left = "Startup Switch / Command".center(col1_w)
    h1_right = "Purpose & Options (pass -h or --help to any switch for full help)".center(col2_w)
    h2_left = "In-CLI Slash Switch (`You>`)".center(col1_w)
    h2_right = 'Syntax (`"Goal"` in quotes & `-param:value` with leading dash)'.center(col2_w)

    print(f"{border_col}┌{'─' * inner_w}┐\033[0m")
    print(f"{border_col}│\033[0m\033[1;97m{title_str}\033[0m{border_col}│\033[0m")
    print(f"{border_col}├{'─' * (col1_w + 2)}┬{'─' * (col2_w + 2)}┤\033[0m")
    print(f"{border_col}│\033[0m \033[1;33m{h1_left}\033[0m {border_col}│\033[0m \033[1;36m{h1_right}\033[0m {border_col}│\033[0m")
    print(f"{border_col}├{'─' * (col1_w + 2)}┼{'─' * (col2_w + 2)}┤\033[0m")
    startup_rows = [
        ("cli | start | stop | restart | status", "Launch interactive C.O.R.A. CLI, start/stop background services, or view status"),
        ("-m <3.8|3.5|turbo|turbo-q6|turbo-q8>", "Select GGUF model (default: 3.8 27B; 3.5 9B fast; turbo MTP Q4/Q6/Q8)"),
        ("-c | --continue | continue", "Resume directly from the last saved CLI session, active project, goal & wave"),
        ("-netiso <red|white|blue> [eth0,eth1]", "Set Network Isolation posture (Red=Full, White=NetNS Air-Gap, Blue=NIC Lock)"),
        ("-P <project_name_or_doc_path>", "Select/create active project workspace or ingest project documentation"),
        ("--dangerously-skip-permissions", "Auto-execute shell/file agent tool commands without [y/N] confirmation prompt"),
        ("--think | --no-think | --no-hud", "Enable/disable <think> chain-of-thought reasoning or bottom-pinned HUD bar"),
        ("-train [folder] | reason | posture", "Distill Training/ (PDF/OCR) into Vault+MDP, run 15 engines, or posture"),
    ]
    for left_col, right_col in startup_rows:
        print(f"{border_col}│\033[0m \033[0;37m{left_col:<{col1_w}}\033[0m {border_col}│\033[0m \033[0;37m{right_col:<{col2_w}}\033[0m {border_col}│\033[0m")
    print(f"{border_col}├{'─' * (col1_w + 2)}┼{'─' * (col2_w + 2)}┤\033[0m")
    print(f"{border_col}│\033[0m \033[1;33m{h2_left}\033[0m {border_col}│\033[0m \033[1;36m{h2_right}\033[0m {border_col}│\033[0m")
    print(f"{border_col}├{'─' * (col1_w + 2)}┼{'─' * (col2_w + 2)}┤\033[0m")
    slash_rows = [
        ('/goal "<objective>" [-max:<#|0|unlimited>]', "Save quoted goal to Projects/<name>/goals.md or view latest goal (-max:0=never stop)"),
        ('/relentless ["<goal>"] [-max:<#|0|unlimited>]', "Run autonomous multi-wave goal loop until [GOAL_ACHIEVED] (-max:0=unlimited waves)"),
        ("/project [-new:<name>|-rename:<old>:<new>]", "Open interactive project selector menu, create new project, or rename project"),
        ("/mode [-mode:1|2|3|4|default|analyst|berserker|ninja]", "Select Session Personality Mode (1=Default, 2=Analyst, 3=Berserker, 4=Ninja)"),
        ("/generate-report [-project:<name>|-focus:<txt>]", "Synthesize 5-section REPORT.md + standalone SVG dashboard in Projects/<name>/"),
        ("/netiso <red|white|blue> [-blue:<eth0,eth1>]", "Switch Red/White/Blue network isolation live and lock allowed NIC interfaces"),
        ("/rl [-train:<episodes>|topology|status]", "Engine 14 Trajectory RL rollout, live host NIC topology scan & Q_LCB policy table"),
        ("/pca [-mode:recompute|<problem_description>]", "Engine 15 Exact SVD PCA (3 PCs), K-Means++ 5-regime clustering & cut-vertex scan"),
        ("/continual [-mode:auto|start|stop|consolidate]", "Engine 12 5-tier continual learning & offline experience replay consolidation"),
        ("/train [-path:<folder>|-mode:force|status]", "4-Phase multi-modal PDF/Docx/OCR training into ObsidianVault/ & H-MDP transitions"),
        ("/reason [-engine:<name>|<problem_description>]", "Execute 15-Engine 5-Layer Lexical Priority Neuro-Symbolic reasoning pipeline"),
        ("/scan -target:<url_or_ip> | /search -query:<q>", "Scan target HTTP/API into Projects/<name>/targets/ or search ObsidianVault/"),
        ('/remember -fact:"<universal_fact>" | /vault', "Save curated universal knowledge to ObsidianVault/ or view Vault index"),
        ("/hud [-mode:on|off|pin] | /permissions | /state", "Configure bottom-pinned HUD bar, toggle tool confirmation, or inspect Context VM"),
        ("/continue | /clear | /help [-switch:<s >] | /exit", "Restore last CLI session, clear conversation, view switch help, or exit cleanly"),
    ]
    for left_col, right_col in slash_rows:
        print(f"{border_col}│\033[0m \033[0;37m{left_col:<{col1_w}}\033[0m {border_col}│\033[0m \033[0;37m{right_col:<{col2_w}}\033[0m {border_col}│\033[0m")
    print(f"{border_col}└{'─' * (col1_w + 2)}┴{'─' * (col2_w + 2)}┘\033[0m")
    tip_txt = "Tip: Add `-h` or `--help` to ANY switch (e.g. `./run_cora_NIX.sh -netiso -h` or `/relentless -h`) for full options."
    print(f"\033[2;37m{tip_txt.center(table_width)}\033[0m\n")


def get_existing_project_dirs() -> list[Path]:
    """Return sorted list of project directories inside `CORA/Projects/`, ensuring each has a `Files/` directory."""
    ensure_vault_structure()
    if not PROJECTS_DIR.is_dir():
        return []
    out = []
    for pdir in sorted(PROJECTS_DIR.iterdir(), key=lambda x: x.name.lower()):
        if pdir.is_dir() and not pdir.name.startswith(".") and pdir.name.lower() not in _INVALID_PROJECT_NAMES:
            try:
                (pdir / "Files").mkdir(parents=True, exist_ok=True)
            except Exception:
                pass
            out.append(pdir)
    return out


def rename_project_workspace(old_slug: str, new_raw_name: str) -> tuple[bool, str, str]:
    """
    Rename an existing project directory `Projects/<old_slug>` -> `Projects/<new_slug>`,
    converting spaces and special characters in `new_raw_name` to dashes (`-`), and
    updating internal references in `memory.md` and `last_cli_session.json`.
    Returns `(success, new_slug, message)`.
    """
    global ACTIVE_PROJECT
    src_dir = PROJECTS_DIR / old_slug
    if not src_dir.is_dir():
        return False, old_slug, f"Project `{old_slug}` does not exist in `{PROJECTS_DIR}`."
    new_slug = slugify_project_name(new_raw_name)
    if not new_slug:
        return False, old_slug, "Invalid new project name."
    if new_slug == old_slug:
        return True, old_slug, f"Project name is already `{old_slug}`."
    dst_dir = PROJECTS_DIR / new_slug
    if dst_dir.exists():
        return False, old_slug, f"A project named `{new_slug}` already exists in `{PROJECTS_DIR}`."
    try:
        src_dir.rename(dst_dir)
        mem_file = dst_dir / "memory.md"
        if mem_file.is_file():
            txt = mem_file.read_text(encoding="utf-8", errors="replace")
            txt = txt.replace(f"Projects/{old_slug}", f"Projects/{new_slug}")
            txt = re.sub(r"^project:\s*.*$", f"project: {new_slug}", txt, flags=re.M)
            txt = re.sub(rf"^title:\s*(?:Project Memory \(.*\)|{re.escape(old_slug)})$", f"title: Project Memory ({new_slug})", txt, flags=re.M)
            txt = re.sub(rf"(\btags:\s*\[[^\]]*?)\b{re.escape(old_slug)}\b", rf"\1{new_slug}", txt, flags=re.M)
            mem_file.write_text(txt, encoding="utf-8")
        goals_file = dst_dir / "goals.md"
        if goals_file.is_file():
            g_txt = goals_file.read_text(encoding="utf-8", errors="replace")
            g_txt = g_txt.replace(f"Projects/{old_slug}", f"Projects/{new_slug}")
            g_txt = g_txt.replace(f"project `{old_slug}`", f"project `{new_slug}`")
            g_txt = re.sub(r"^project:\s*.*$", f"project: {new_slug}", g_txt, flags=re.M)
            g_txt = re.sub(r"^title:\s*Project Goals History \(.*\)$", f"title: Project Goals History ({new_slug})", g_txt, flags=re.M)
            goals_file.write_text(g_txt, encoding="utf-8")
        for sess_f in (LAST_SESSION_FILE, RELENTLESS_LEDGER_FILE):
            if sess_f.is_file():
                try:
                    s_data = json.loads(sess_f.read_text(encoding="utf-8", errors="replace"))
                    if s_data.get("active_project") == old_slug:
                        s_data["active_project"] = new_slug
                        sess_f.write_text(json.dumps(s_data, indent=2) + "\n", encoding="utf-8")
                except Exception:
                    pass
        try:
            SESSION_STATE_DIR.mkdir(parents=True, exist_ok=True)
            ap_file = SESSION_STATE_DIR / "active_project.txt"
            if not ap_file.is_file() or ap_file.read_text(encoding="utf-8", errors="replace").strip() == old_slug:
                ap_file.write_text(new_slug + "\n", encoding="utf-8")
        except Exception:
            pass
        if ACTIVE_PROJECT == old_slug:
            ACTIVE_PROJECT = new_slug
            os.environ["CORA_ACTIVE_PROJECT"] = new_slug
        return True, new_slug, f"Renamed project `{old_slug}` -> `{new_slug}` (`Projects/{new_slug}/`)."
    except Exception as exc:
        return False, old_slug, f"Failed to rename project `{old_slug}`: {exc}"


_PENDING_FIRST_COMMAND: str = ""


def _persist_selected_project(slug: str) -> None:
    """Persist the selected active project slug and load its latest saved goal from `Projects/<slug>/goals.md`."""
    global ACTIVE_PROJECT, ACTIVE_GOAL
    prev_proj = ACTIVE_PROJECT
    ACTIVE_PROJECT = slug
    os.environ["CORA_ACTIVE_PROJECT"] = slug
    ensure_project_workspace(slug)
    last_goal = get_last_project_goal(slug)
    if last_goal:
        ACTIVE_GOAL = last_goal
    elif prev_proj and prev_proj != slug:
        ACTIVE_GOAL = ""
    try:
        SESSION_STATE_DIR.mkdir(parents=True, exist_ok=True)
        (SESSION_STATE_DIR / "active_project.txt").write_text(slug + "\n", encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# C.O.R.A. 4-MODE SESSION PERSONALITY & LOGIC ENFORCEMENT SYSTEM
# (`Default`, `Analyst`, `Berserker`, `Ninja` — Unique per session, never persisted across sessions)
# ==============================================================================
PERSONALITY_MODES_META: dict[str, dict] = {
    "1": {
        "key": "DEFAULT",
        "label": "Default",
        "color": "\033[1;32m",
        # 9 words (<= 10 words)
        "purpose": "Standard operation with no behavioral guidance or extra restrictions.",
        "is_default": True,
    },
    "2": {
        "key": "ANALYST",
        "label": "Analyst",
        "color": "\033[1;97m",
        # 9 words (<= 10 words)
        "purpose": "Analyze local system data only; external network scanning blocked.",
        "is_default": False,
    },
    "3": {
        "key": "BERSERKER",
        "label": "Berserker",
        "color": "\033[1;31m",
        # 8 words (<= 10 words)
        "purpose": "Aggressively pursue target goals using all available tools.",
        "is_default": False,
    },
    "4": {
        "key": "NINJA",
        "label": "Ninja",
        "color": "\033[1;35m",
        # 8 words (<= 10 words)
        "purpose": "Find answers covertly using stealthy, low-noise commands only.",
        "is_default": False,
    },
}


def write_active_session_mode_env() -> None:
    """
    Write current runtime session mode & isolation variables to `Log/active_session_mode.env`
    so `run_cora_NIX.sh` (`start_services` for WebGUI) can read and enforce the session-selected mode
    and network isolation (`WHITE` for `Analyst`, `RED` or `BLUE` for `Berserker`/`Ninja`).
    """
    try:
        ACTIVE_SESSION_MODE_FILE.parent.mkdir(parents=True, exist_ok=True)
        iso_lvl = os.environ.get("LLM_ISOLATION_MODE", "RED")
        allow_if = os.environ.get("LLM_ALLOWED_IFACES", "")
        proj = ACTIVE_PROJECT or get_active_project_slug()
        pmode = ACTIVE_PERSONALITY_MODE or "DEFAULT"
        lines = [
            f'export CORA_ACTIVE_PROJECT="{proj}"',
            f'export CORA_PERSONALITY_MODE="{pmode}"',
            f'export LLM_ISOLATION_MODE="{iso_lvl}"',
            f'export LLM_POSTURE_OVERRIDE="{iso_lvl}"',
            f'export LLM_ALLOWED_IFACES="{allow_if}"',
        ]
        ACTIVE_SESSION_MODE_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except Exception:
        pass


def apply_personality_mode(mode_key: str, netiso_group: str = "") -> tuple[str, str, list[str]]:
    """
    Activate one of the 4 session-unique personality modes (`DEFAULT`, `ANALYST`, `BERSERKER`, `NINJA`)
    and enforce its corresponding Network Isolation posture:
      - `DEFAULT`   : Standard operation with no behavioral guidance/discretion. Preserves active network isolation (or `netiso_group` if given).
      - `ANALYST`   : Automatically forces Network Isolation `WHITE` (`lo` loopback only; all external scanning/outbound traffic blocked).
      - `BERSERKER` : Requires `Red` (`All` interfaces) or `Blue` (`config` or `CLI switch override` interfaces); pre-emptive aggressive goal pursuit.
      - `NINJA`     : Requires `Red` (`All` interfaces) or `Blue` (`config` or `CLI switch override` interfaces); pre-emptive covert/low-noise execution.
    Returns `(normalized_mode_key, applied_netiso_level, allowed_interfaces)`.
    """
    global ACTIVE_PERSONALITY_MODE
    norm = (mode_key or "DEFAULT").strip().upper()
    alias_to_key = {
        "1": "DEFAULT",
        "DEFAULT": "DEFAULT",
        "STD": "DEFAULT",
        "STANDARD": "DEFAULT",
        "2": "ANALYST",
        "ANALYST": "ANALYST",
        "PASSIVE": "ANALYST",
        "WHITE": "ANALYST",
        "3": "BERSERKER",
        "BERSERKER": "BERSERKER",
        "BERSERK": "BERSERKER",
        "ACTIVE": "BERSERKER",
        "AGGRESSIVE": "BERSERKER",
        "4": "NINJA",
        "NINJA": "NINJA",
        "STEALTH": "NINJA",
        "COVERT": "NINJA",
    }
    norm = alias_to_key.get(norm, "DEFAULT")
    ACTIVE_PERSONALITY_MODE = norm
    os.environ["CORA_PERSONALITY_MODE"] = norm

    if norm == "ANALYST":
        iso_lvl, ifaces = apply_network_isolation_level("white", "")
        _refresh_active_posture(override="WHITE", apply_osc=True, quiet=True)
    elif norm in ("BERSERKER", "NINJA"):
        grp = (netiso_group or "").strip().lower()
        if grp in ("2", "blue", "lan", "usb", "isolated"):
            blue_ifaces, _ = get_configured_blue_interfaces()
            iso_lvl, ifaces = apply_network_isolation_level("blue", ",".join(blue_ifaces))
            _refresh_active_posture(override="BLUE", apply_osc=True, quiet=True)
        else:
            iso_lvl, ifaces = apply_network_isolation_level("red", "")
            _refresh_active_posture(override="RED", apply_osc=True, quiet=True)
    else:
        # DEFAULT mode: no extra guidance or forced change unless netiso_group was explicitly passed
        if netiso_group:
            grp = netiso_group.strip().lower()
            if grp in ("2", "blue"):
                blue_ifaces, _ = get_configured_blue_interfaces()
                iso_lvl, ifaces = apply_network_isolation_level("blue", ",".join(blue_ifaces))
            elif grp in ("white",):
                iso_lvl, ifaces = apply_network_isolation_level("white", "")
            else:
                iso_lvl, ifaces = apply_network_isolation_level("red", "")
            _refresh_active_posture(override=iso_lvl, apply_osc=True, quiet=True)
        else:
            cur_iso = os.environ.get("LLM_ISOLATION_MODE", "RED").upper()
            cur_if = [x.strip() for x in os.environ.get("LLM_ALLOWED_IFACES", "").split(",") if x.strip()]
            iso_lvl, ifaces = cur_iso, cur_if
            _refresh_active_posture(override="", apply_osc=True, quiet=True)

    write_active_session_mode_env()
    if HUD.active:
        HUD.render(force_region=False)
    return norm, iso_lvl, ifaces


def _prompt_berserker_or_ninja_netiso_group(mode_label: str, mode_color: str) -> str:
    """
    Sub-menu required when the user selects `Berserker` (`[3]`) or `Ninja` (`[4]`):
    Prompts the user to select which Network Isolation Group (`Red` or `Blue`) they want from a numbered list,
    with a brief, concise example of which interfaces `Red` and `Blue` have access to:
      - `[1] Red  — Interfaces: All`
      - `[2] Blue — Interfaces: <eth0,eth1> (<network_isolation.conf | CLI switch override>)`
    Returns `"red"`, `"blue"`, or `"__BACK__"` if the user selects `B` (`Go Back`).
    """
    global _PENDING_FIRST_COMMAND
    blue_ifaces, blue_src = get_configured_blue_interfaces()
    blue_csv = ", ".join(blue_ifaces)

    def _render_netiso_submenu() -> None:
        bw = get_terminal_banner_width(DEFAULT_BANNER_WIDTH)
        sub_hdr = f" {mode_label} Mode: Select Network Isolation Group (Red or Blue) ".center(bw, "-")
        print(f"\n{mode_color}{sub_hdr}\033[0m")
        print("  \033[1;31m[1] Red \033[0m — Interfaces: \033[1;37mAll\033[0m (Unrestricted full host network access)")
        print(f"  \033[1;36m[2] Blue\033[0m — Interfaces: \033[1;36m{blue_csv}\033[0m (Locked via {blue_src})")
        print("  \033[1;33m[B]\033[0m Go Back to Mode Selection")
        print("  \033[2;37m[C]\033[0m CANCEL / Exit")
        print(f"{mode_color}{'-' * bw}\033[0m")

    while True:
        _render_netiso_submenu()

        try:
            iso_choice = _read_interactive_cli_line(
                f"\n{mode_color}Select Network Isolation Group for {mode_label} [1=Red, 2=Blue, B=Back, C=CANCEL]:\033[0m ",
                allow_autocomplete=False,
                menu_redraw_fn=_render_netiso_submenu,
            ).strip()
        except (EOFError, KeyboardInterrupt):
            if not sys.stdin.isatty():
                return "red"
            print("\n Returning to Mode Selection...")
            return "__BACK__"

        if not iso_choice:
            if not sys.stdin.isatty():
                return "red"
            continue

        if not sys.stdin.isatty() and iso_choice.startswith("/"):
            _PENDING_FIRST_COMMAND = iso_choice
            return "red"

        low_iso = iso_choice.lower()
        if low_iso in ("b", "back", "go back"):
            return "__BACK__"
        if low_iso in ("c", "cancel", "q", "quit", "exit"):
            print("Selection cancelled. Exiting C.O.R.A. CLI...")
            _shutdown_cli_and_engines(stop_llm=True, quiet=False)
            sys.exit(0)
        if low_iso in ("1", "red", "r", "all"):
            return "red"
        if low_iso in ("2", "blue", "lan", "usb"):
            return "blue"

        print("\033[1;31mInvalid selection. Enter `1` (Red — Interfaces: All), `2` (Blue — Interfaces: " + blue_csv + "), `B` (Back), or `C` (CANCEL).\033[0m")


def interactive_personality_mode_menu(project_slug: str = "", allow_back_to_project: bool = True) -> str:
    """
    Interactive Session Personality & Logic Enforcement Menu presented immediately AFTER a Project
    is selected or created:
      - `[1] Default   (Default)` — Standard operation with no behavioral guidance or extra restrictions. (9 words)
      - `[2] Analyst`             — Analyze local system data only; external network scanning blocked. (9 words)
      - `[3] Berserker`           — Aggressively pursue target goals using all available tools. (8 words)
      - `[4] Ninja`               — Find answers covertly using stealthy, low-noise commands only. (8 words)
    Modes are unique to the active session only (never persisted across sessions), so the user always
    selects their desired mode after selecting or creating a project.
    Returns the activated mode key (`"DEFAULT"`, `"ANALYST"`, `"BERSERKER"`, `"NINJA"`), or `"__BACK__"`
    if the user selects `[B] Go Back to Project Selection`.
    """
    global _PENDING_FIRST_COMMAND
    proj_disp = project_slug or ACTIVE_PROJECT or get_active_project_slug()

    # If a non-interactive piped command was already captured during project selection, default to DEFAULT mode
    if not sys.stdin.isatty() and _PENDING_FIRST_COMMAND:
        apply_personality_mode("DEFAULT")
        return "DEFAULT"

    def _render_mode_menu() -> None:
        bw = get_terminal_banner_width(DEFAULT_BANNER_WIDTH)
        hdr = " C.O.R.A. Session Personality & Logic Mode Selection (Session-Only) ".center(bw, "=")
        print(f"\033[1;35m{hdr}\033[0m")
        print(f"  Active Project: `Projects/{proj_disp}/`  |  Select mode number [1-4] (Default: [1]):")
        for num_k in ("1", "2", "3", "4"):
            m_info = PERSONALITY_MODES_META[num_k]
            def_badge = " \033[1;32m(Default)\033[0m" if m_info["is_default"] else "          "
            lbl_padded = f"{m_info['label']:<9}"
            print(
                f"  \033[1;33m[{num_k}]\033[0m {m_info['color']}{lbl_padded}\033[0m{def_badge} — {m_info['purpose']}"
            )
        if allow_back_to_project:
            print("  \033[1;36m[B]\033[0m Go Back to Project Selection")
        print("  \033[2;37m[C]\033[0m CANCEL / Exit")
        print(f"\033[1;35m{'=' * bw}\033[0m")

    while True:
        _render_mode_menu()

        try:
            raw_sel = _read_interactive_cli_line(
                "\n\033[1;35mSelect Session Mode [1-4, Enter=1 (Default)" + (", B=Back" if allow_back_to_project else "") + ", C=CANCEL]:\033[0m ",
                allow_autocomplete=False,
                menu_redraw_fn=_render_mode_menu,
            ).strip()
        except (EOFError, KeyboardInterrupt):
            if not sys.stdin.isatty():
                apply_personality_mode("DEFAULT")
                return "DEFAULT"
            print("\nCancelled.")
            if allow_back_to_project:
                return "__BACK__"
            return ACTIVE_PERSONALITY_MODE or "DEFAULT"

        # Pressing Enter (empty input) selects [1] Default
        if not raw_sel:
            mode_key, iso_lvl, _ = apply_personality_mode("DEFAULT")
            print(
                f"\n\033[1;32m[Session Mode Locked -> Default]\033[0m Standard operation (no extra LLM behavioral guidance | Network Isolation: `{iso_lvl}`).\n"
            )
            return mode_key

        # Non-interactive piped slash command fallback
        if not sys.stdin.isatty() and raw_sel.startswith("/"):
            _PENDING_FIRST_COMMAND = raw_sel
            mode_key, _, _ = apply_personality_mode("DEFAULT")
            return mode_key

        low_s = raw_sel.lower()
        if allow_back_to_project and low_s in ("b", "back", "go back"):
            print("Returning to Project Selection Menu...\n")
            return "__BACK__"
        if low_s in ("c", "cancel", "q", "quit", "exit"):
            if allow_back_to_project:
                print("Mode selection cancelled. Exiting C.O.R.A. CLI...")
                _shutdown_cli_and_engines(stop_llm=True, quiet=False)
                sys.exit(0)
            print("Mode switch cancelled.\n")
            return ACTIVE_PERSONALITY_MODE or "DEFAULT"

        if low_s in ("1", "default", "std", "standard"):
            mode_key, iso_lvl, _ = apply_personality_mode("DEFAULT")
            print(
                f"\n\033[1;32m[Session Mode Locked -> Default]\033[0m Standard operation (no extra LLM behavioral guidance | Network Isolation: `{iso_lvl}`).\n"
            )
            return mode_key

        if low_s in ("2", "analyst", "passive"):
            mode_key, iso_lvl, _ = apply_personality_mode("ANALYST")
            print(
                "\n\033[1;97m[Session Mode Locked -> Analyst]\033[0m\n"
                "  - Purpose:           Analyze local system data only; external network scanning blocked.\n"
                f"  - Network Isolation: \033[1;97m{iso_lvl} (AIR_GAPPED_NETNS — `lo` loopback only)\033[0m\n"
                "  - Enforcement:       External network scanning and outbound data transmission are strictly blocked in CLI & WebGUI.\n"
            )
            return mode_key

        if low_s in ("3", "berserker", "berserk", "aggressive"):
            iso_grp = _prompt_berserker_or_ninja_netiso_group("Berserker", "\033[1;31m")
            if iso_grp == "__BACK__":
                continue
            mode_key, iso_lvl, ifaces = apply_personality_mode("BERSERKER", netiso_group=iso_grp)
            iface_desc = "All" if iso_lvl == "RED" else (", ".join(ifaces) if ifaces else "eth0, eth1")
            print(
                "\n\033[1;31m[Session Mode Locked -> Berserker]\033[0m\n"
                "  - Purpose:           Aggressively pursue target goals using all available tools.\n"
                f"  - Network Isolation: \033[1;31m{iso_lvl}\033[0m (Interfaces: `{iface_desc}`)\n"
                "  - Enforcement:       Pre-emptive prompt active — aggressively pursues target goals with all available tools at all times.\n"
            )
            return mode_key

        if low_s in ("4", "ninja", "stealth", "covert"):
            iso_grp = _prompt_berserker_or_ninja_netiso_group("Ninja", "\033[1;35m")
            if iso_grp == "__BACK__":
                continue
            mode_key, iso_lvl, ifaces = apply_personality_mode("NINJA", netiso_group=iso_grp)
            iface_desc = "All" if iso_lvl == "RED" else (", ".join(ifaces) if ifaces else "eth0, eth1")
            print(
                "\n\033[1;35m[Session Mode Locked -> Ninja]\033[0m\n"
                "  - Purpose:           Find answers covertly using stealthy, low-noise commands only.\n"
                f"  - Network Isolation: \033[1;35m{iso_lvl}\033[0m (Interfaces: `{iface_desc}`)\n"
                "  - Enforcement:       Pre-emptive covert prompt & CEGAR stealth guard active — finds answers covertly using low-noise commands at all times.\n"
            )
            return mode_key

        print("\033[1;31mInvalid selection `" + raw_sel + "`. Please enter `1` (Default), `2` (Analyst), `3` (Berserker), or `4` (Ninja).\033[0m\n")


def get_personality_mode_system_prompt_block() -> str:
    """
    Return the Session Personality & Logic Enforcement block for `build_system_prompt()`.
    - When `ACTIVE_PERSONALITY_MODE == "DEFAULT"`, returns `""` (zero behavioral guidance or discretion).
    - When `ANALYST`, `BERSERKER`, or `NINJA`, returns the strict session-enforced operational rules.
    """
    pmode = (ACTIVE_PERSONALITY_MODE or "DEFAULT").upper()
    if pmode == "DEFAULT":
        return ""

    iso_lvl = os.environ.get("LLM_ISOLATION_MODE", "RED").upper()
    allow_if = os.environ.get("LLM_ALLOWED_IFACES", "").strip()
    iface_summary = "lo (Local Loopback Only)" if iso_lvl == "WHITE" else ("All Host Interfaces" if iso_lvl == "RED" else f"{allow_if} (+ lo)")

    if pmode == "ANALYST":
        return (
            "\nSESSION PERSONALITY & LOGIC ENFORCEMENT — [MODE 2: ANALYST | NETWORK ISOLATION: WHITE (LOCAL SYSTEM ONLY)]:\n"
            "  - PURPOSE: Analyze local system data only; external network scanning blocked.\n"
            "  - MANDATORY LOGIC ENFORCEMENT:\n"
            "    1. Network Isolation is locked to `WHITE` (`lo` loopback only). You are STRICTLY FORBIDDEN from performing any network scans (`scan_target`, `nmap`, `masscan`, `zmap`, `rustscan`, `nikto`, `gobuster`, `ffuf`, `ping`, `arping`, `traceroute`) or sending/fetching data outside the local laptop system (`curl`, `wget`, `ssh`, `scp`, `sftp`, `rsync`, `nc`, `ncat`, `socat`, `tio`, `/dev/tcp`, or Python sockets/HTTP clients).\n"
            "    2. Focus 100% on analyzing existing local files, saved scan reports in `Projects/` and `ObsidianVault/`, system logs, configuration files, and running `neuro_symbolic_reason`, `read_file`, `list_directory`, `vault_search`, `vault_read_note`, `vault_save_note`, `project_tracker`, and `generate_project_report`.\n"
            "    3. If `run_shell_command` is used, execute ONLY local file/log/process inspection commands (`ls`, `cat`, `grep`, `awk`, `jq`, `find`, `head`, `tail`, `ps`, `ss -tulnp`, `sha256sum`) on the local laptop.\n"
        )

    if pmode == "BERSERKER":
        return (
            f"\nSESSION PERSONALITY & LOGIC ENFORCEMENT — [MODE 3: BERSERKER | NETWORK ISOLATION: {iso_lvl} (INTERFACES: {iface_summary})]:\n"
            "  - PURPOSE: Aggressively pursue target goals using all available tools.\n"
            "  - PRE-EMPTIVE BERSERKER DIRECTIVE (ACTIVE AT ALL TIMES):\n"
            "    1. You MUST aggressively, decisively, and relentlessly pursue the target goal at all times using ALL tools available (`run_shell_command`, `scan_target`, `neuro_symbolic_reason`, `vault_search`, `vault_read_note`, `vault_save_note`, `project_tracker`, `read_file`, `write_file`, `edit_file`, `list_directory`, `generate_project_report`).\n"
            "    2. NEVER stop at passive explanations or ask unnecessary permission when a tool can be invoked right now. Immediately execute active reconnaissance, multi-port service discovery, API/web exploitation, L2/L3 routing probes, OOB serial probes, and 15-Engine neuro-symbolic synthesis.\n"
            f"    3. Operate within your selected Network Isolation Group (`{iso_lvl}` — Allowed Interfaces: `{iface_summary}`). When any command fails or blocks, immediately pivot to an alternate capability vector (`L1_Serial_OOB`, `L2_ARP_Link`, `L3_Routing_NAT`, `L4_Port_Service`, `L7_HTTP_Web_Exploit`, `Neuro_Symbolic_15_Engines`) until the target goal is 100% achieved.\n"
        )

    if pmode == "NINJA":
        return (
            f"\nSESSION PERSONALITY & LOGIC ENFORCEMENT — [MODE 4: NINJA | NETWORK ISOLATION: {iso_lvl} (INTERFACES: {iface_summary})]:\n"
            "  - PURPOSE: Find answers covertly using stealthy, low-noise commands only.\n"
            "  - PRE-EMPTIVE NINJA COVERT DIRECTIVE (ACTIVE AT ALL TIMES):\n"
            "    1. You MUST find answers and accomplish the user's objective, but NEVER aggressively. Attempt covert action and use covert, low-noise, minimal-footprint commands at all times.\n"
            "    2. PASSIVE-FIRST DOCTRINE: Always check existing local knowledge and passive host telemetry first (`vault_search`, `vault_read_note`, `read_file`, `ip -br addr`, `ip route`, `ip neigh show`, `ss -tulnp`, `/etc/hosts`, ARP cache) before transmitting any network packets.\n"
            "    3. COVERT COMMAND DISCIPLINE: When active network interaction is required within your allowed interfaces (`" + iface_summary + "`), use ONLY surgical, low-rate, single-target commands:\n"
            "       - NEVER use noisy flood scanners or brute-forcers (`masscan`, `zmap`, `rustscan`, `nikto`, `wpscan`, `nuclei`, `hydra`, `medusa`, `gobuster`, `ffuf`, `dirb`, `wfuzz`, `ping -f`, `hping3 --flood`).\n"
            "       - NEVER use aggressive `nmap` flags (`-T4`, `-T5`, `-A`, `--min-rate` > 50, or full `-p-` sweeps without `-T1`/`-T2`). Instead use stealthy targeted probes (`nmap -sT -Pn -T2 --max-rate 15 -p 22,80,443,8080 <target>` or single-request `curl -sS -k --connect-timeout 5 <url>`).\n"
        )

    return ""


def get_personality_mode_preemptive_turn_prefix() -> str:
    """
    Return the pre-emptive per-turn directive prepended to the active user query during `chat_step()`
    for `BERSERKER`, `NINJA`, and `ANALYST` modes.
    Returns `""` when `ACTIVE_PERSONALITY_MODE == "DEFAULT"` (zero guidance or discretion).
    """
    pmode = (ACTIVE_PERSONALITY_MODE or "DEFAULT").upper()
    if pmode == "DEFAULT":
        return ""

    iso_lvl = os.environ.get("LLM_ISOLATION_MODE", "RED").upper()
    allow_if = os.environ.get("LLM_ALLOWED_IFACES", "").strip()
    iface_summary = "lo (Local Loopback Only)" if iso_lvl == "WHITE" else ("All" if iso_lvl == "RED" else allow_if)

    if pmode == "ANALYST":
        return (
            "[PRE-EMPTIVE ANALYST MODE ENFORCEMENT (NETISO: WHITE — LOCAL SYSTEM ONLY)]: "
            "Analyze local system data, files, logs, and ObsidianVault notes only. External network scanning and sending data outside the local laptop are strictly blocked.\n\n"
        )
    if pmode == "BERSERKER":
        return (
            f"[PRE-EMPTIVE BERSERKER MODE DIRECTIVE (NETISO: {iso_lvl} | INTERFACES: {iface_summary})]: "
            "Aggressively pursue the target goal right now using ALL available tools (`run_shell_command`, `scan_target`, `neuro_symbolic_reason`, `vault_search`, `vault_read_note`, `read_file`, `write_file`). "
            "Execute multi-vector tool calls immediately and pivot across L1-L7 without hesitation until the target goal is achieved.\n\n"
        )
    if pmode == "NINJA":
        return (
            f"[PRE-EMPTIVE NINJA MODE DIRECTIVE (NETISO: {iso_lvl} | INTERFACES: {iface_summary})]: "
            "You MUST find the answers and achieve the objective, but DO NOT act aggressively. Attempt covert action and use covert, low-noise commands at all times "
            "(prioritize passive local state `ip neigh`/`ip route`/`ss -tulnp`/Vault notes first; if probing, use stealthy single-request `curl -sS` or `nmap -sT -Pn -T2 --max-rate 15` on specific ports; never run noisy scans or floods).\n\n"
        )
    return ""


def interactive_project_selection_menu(require_selection: bool = True, prompt_mode_after: bool = True) -> str:
    """
    Interactive Project Workspace Menu presented at CLI startup (and via `/project menu` / `/project select`):
      - Lists all current projects in `Projects/` numbered `1 .. N`.
      - Option `N + 1` (just above Create New Project): `Rename Current Project`
        (opens a secondary screen where the user selects the project number to rename, with `Go Back` and `CANCEL`).
      - Option `N + 2` (very last numbered item): `CREATE NEW PROJECT`
        (prompts for the new project name, auto-converting spaces and special characters to dashes `-`,
        creates `Projects/<new-name>/`, and sets it as the active project, with `Go Back` and `CANCEL`).
      - Also supports `CANCEL` / `Q` to cancel or exit cleanly.
      - Immediately after selecting or creating a project (when `prompt_mode_after=True`), prompts the
        4-Mode Session Personality & Logic Enforcement menu (`[1] Default`, `[2] Analyst`, `[3] Berserker`, `[4] Ninja`).
    """
    global ACTIVE_PROJECT, _PENDING_FIRST_COMMAND
    while True:
        proj_dirs = get_existing_project_dirs()
        n_projs = len(proj_dirs)
        rename_num = n_projs + 1
        create_num = n_projs + 2

        def _render_proj_menu() -> None:
            bw = get_terminal_banner_width(DEFAULT_BANNER_WIDTH)
            proj_header = " C.O.R.A. Project Workspace Selection (Required Before LLM Interaction) ".center(bw, "=")
            print(f"\033[1;36m{proj_header}\033[0m")
            print(f"  Projects Directory: `{PROJECTS_DIR}`")
            if proj_dirs:
                for idx, pdir in enumerate(proj_dirs, 1):
                    active_tag = " \033[1;32m[ACTIVE]\033[0m" if pdir.name == ACTIVE_PROJECT else ""
                    mem_f = pdir / "memory.md"
                    summary = ""
                    if mem_f.is_file():
                        try:
                            m_sum = re.search(r"^summary:\s*(.+)$", mem_f.read_text(encoding="utf-8", errors="replace"), re.M)
                            if m_sum:
                                summary = f" — {m_sum.group(1).strip()[:140]}"
                        except Exception:
                            pass
                    print(f"  \033[1;33m[{idx}]\033[0m {pdir.name}{active_tag}{summary}")
            else:
                print("  *(No existing projects in `/Projects` yet)*")

            print(f"  \033[1;35m[{rename_num}]\033[0m Rename Current Project")
            print(f"  \033[1;32m[{create_num}]\033[0m CREATE NEW PROJECT")
            print("  \033[2;37m[C] CANCEL / Exit\033[0m")
            print(f"\033[1;36m{'=' * bw}\033[0m")

        _render_proj_menu()

        try:
            choice = _read_interactive_cli_line(
                f"\n\033[1;36mSelect Project or Action [1-{create_num}, or C to CANCEL]:\033[0m ",
                allow_autocomplete=False,
                menu_redraw_fn=_render_proj_menu,
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            if require_selection and not ACTIVE_PROJECT:
                _shutdown_cli_and_engines(stop_llm=True, quiet=False)
                sys.exit(0)
            return ACTIVE_PROJECT

        if not choice:
            continue

        # If running non-interactively via piped stdin where the caller sent a slash command directly
        # (e.g., `printf "/relentless status\n/exit\n" | ./run_cora_NIX.sh cli`), select the first existing
        # project automatically and queue the slash command for immediate execution.
        if not sys.stdin.isatty() and choice.startswith("/"):
            if not proj_dirs:
                print("\n\033[1;31m[Project Selection Required]\033[0m Please create or select a project first.\n")
                continue
            default_slug = proj_dirs[0].name
            _persist_selected_project(default_slug)
            _PENDING_FIRST_COMMAND = choice
            apply_personality_mode("DEFAULT")
            print(f"\n\033[1;32m[Project Auto-Selected for Piped Command]\033[0m `Projects/{default_slug}/`\n")
            return default_slug

        low_c = choice.lower()
        if low_c in ("c", "cancel", "q", "quit", "exit"):
            if require_selection and not ACTIVE_PROJECT:
                print("Project selection cancelled. Exiting C.O.R.A. CLI...")
                _shutdown_cli_and_engines(stop_llm=True, quiet=False)
                sys.exit(0)
            print("Cancelled project switch; keeping current project.\n")
            return ACTIVE_PROJECT

        if choice.isdigit():
            sel_num = int(choice)
            # 1..N: Select existing project
            if 1 <= sel_num <= n_projs:
                chosen_slug = proj_dirs[sel_num - 1].name
                _persist_selected_project(chosen_slug)
                print(f"\n\033[1;32m[Project Selected]\033[0m Active workspace locked to `Projects/{chosen_slug}/`.\n")
                if prompt_mode_after:
                    m_res = interactive_personality_mode_menu(chosen_slug, allow_back_to_project=True)
                    if m_res == "__BACK__":
                        continue
                return chosen_slug

            # N+1: Rename Current Project
            if sel_num == rename_num:
                if not proj_dirs:
                    print("\n\033[1;33mNo projects exist yet to rename. Please select CREATE NEW PROJECT.\033[0m\n")
                    continue
                while True:
                    def _render_rename_menu() -> None:
                        print("\n\033[1;35m--- Rename Current Project ---\033[0m")
                        for idx, pdir in enumerate(proj_dirs, 1):
                            print(f"  \033[1;33m[{idx}]\033[0m {pdir.name}")
                        print("  \033[1;36m[B]\033[0m Go Back")
                        print("  \033[1;31m[C]\033[0m CANCEL")

                    _render_rename_menu()
                    try:
                        r_sel = _read_interactive_cli_line(
                            f"Select project number to rename [1-{n_projs}, B=Go Back, C=CANCEL]: ",
                            allow_autocomplete=False,
                            menu_redraw_fn=_render_rename_menu,
                        ).strip()
                    except (EOFError, KeyboardInterrupt):
                        print()
                        break
                    if not r_sel:
                        continue
                    if r_sel.lower() in ("b", "back", "go back"):
                        print("Returning to Project Selection Menu...\n")
                        break
                    if r_sel.lower() in ("c", "cancel"):
                        print("Rename cancelled.\n")
                        break
                    if r_sel.isdigit() and 1 <= int(r_sel) <= n_projs:
                        target_old = proj_dirs[int(r_sel) - 1].name
                        try:
                            new_raw = _read_interactive_cli_line(
                                f"Enter new name for `{target_old}` (spaces/special chars auto-convert to `-`, B=Go Back, C=CANCEL): ",
                                allow_autocomplete=False,
                                menu_redraw_fn=_render_rename_menu,
                            ).strip()
                        except (EOFError, KeyboardInterrupt):
                            print()
                            break
                        if not new_raw or new_raw.lower() in ("b", "back", "go back"):
                            print("Returning to Rename Project list...")
                            continue
                        if new_raw.lower() in ("c", "cancel"):
                            print("Rename cancelled.\n")
                            break
                        ok, new_slug, msg = rename_project_workspace(target_old, new_raw)
                        color = "\033[1;32m" if ok else "\033[1;31m"
                        print(f"\n{color}{msg}\033[0m\n")
                        break
                    print(f"\033[1;31mInvalid selection `{r_sel}`. Enter 1-{n_projs}, B (Go Back), or C (CANCEL).\033[0m")
                continue

            # N+2 (very last number): CREATE NEW PROJECT
            if sel_num == create_num:
                created_project_slug = ""
                while True:
                    def _render_create_menu() -> None:
                        print("\n\033[1;32m--- CREATE NEW PROJECT ---\033[0m")
                        print("  (Spaces and special characters will be automatically converted to dashes `-`)")
                        print("  Type `B` to Go Back or `C` to CANCEL.")

                    _render_create_menu()
                    try:
                        raw_new = _read_interactive_cli_line(
                            "Enter New Project Name: ",
                            allow_autocomplete=False,
                            menu_redraw_fn=_render_create_menu,
                        ).strip()
                    except (EOFError, KeyboardInterrupt):
                        print()
                        break
                    if not raw_new:
                        print("\033[1;33mA project name is required. Please enter a name, or B (Go Back) / C (CANCEL).\033[0m")
                        continue
                    if raw_new.lower() in ("b", "back", "go back"):
                        print("Returning to Project Selection Menu...\n")
                        break
                    if raw_new.lower() in ("c", "cancel"):
                        print("Create New Project cancelled.\n")
                        break
                    new_slug = slugify_project_name(raw_new)
                    _persist_selected_project(new_slug)
                    proj_ws = PROJECTS_DIR / new_slug
                    print(
                        f"\n\033[1;32m[New Project Created]\033[0m `{new_slug}` created in `{proj_ws}`\n"
                        f"  Memory File:  `{proj_ws / 'memory.md'}`\n"
                        f"  Project Files:`{proj_ws / 'Files'}`\n"
                        f"  Downloads:    `{proj_ws / 'downloads'}`\n"
                    )
                    created_project_slug = new_slug
                    break
                if created_project_slug:
                    if prompt_mode_after:
                        m_res = interactive_personality_mode_menu(created_project_slug, allow_back_to_project=True)
                        if m_res == "__BACK__":
                            continue
                    return created_project_slug
                continue

        print(f"\033[1;31mInvalid selection `{choice}`. Please enter a number between 1 and {create_num} (or C to CANCEL).\033[0m\n")


def list_vault_projects() -> str:
    ensure_vault_structure()
    entries = []
    if PROJECTS_DIR.is_dir():
        for pdir in sorted(PROJECTS_DIR.iterdir()):
            if pdir.is_dir() and not pdir.name.startswith("."):
                mem_f = pdir / "memory.md"
                summary = "Isolated project workspace & memory (`Projects/" + pdir.name + "/`)"
                if mem_f.is_file():
                    text = mem_f.read_text(encoding="utf-8", errors="replace")
                    summary_match = re.search(r"^summary:\s*(.+)$", text, re.M)
                    if summary_match:
                        summary = summary_match.group(1).strip()
                active_marker = " [ACTIVE]" if pdir.name == get_active_project_slug() else ""
                entries.append(f"  - [[Projects/{pdir.name}/memory]]{active_marker} — {summary}")

    proj_dir = VAULT_DIR / "projects"
    for n in sorted(proj_dir.glob("*.md")):
        if not any(f"Projects/{n.stem}/" in e for e in entries):
            active_marker = " [ACTIVE]" if n.stem == ACTIVE_PROJECT else ""
            text = n.read_text(encoding="utf-8", errors="replace")
            summary_match = re.search(r"^summary:\s*(.+)$", text, re.M)
            summary = summary_match.group(1).strip() if summary_match else "Project tracker note"
            entries.append(f"  - [[projects/{n.stem}]]{active_marker} — {summary}")

    if not entries:
        return f"No projects exist yet in `{PROJECTS_DIR}`. Start one with `/project <doc_path> [project_name]`."
    return f"=== CORA Isolated Projects (`{PROJECTS_DIR}`) ===\n" + "\n".join(entries)


def get_live_hardware_summary() -> str:
    cpu = "Unknown CPU"
    try:
        out = subprocess.check_output(["lscpu"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if "Model name:" in line:
                cpu = line.split(":", 1)[1].strip()
                break
    except Exception:
        try:
            from Reasoning.engines.vault_bridge import detect_hardware_tier_specs

            hw_specs = detect_hardware_tier_specs()
            if hw_specs.get("cpu_model"):
                cpu = f"{hw_specs['cpu_model']} ({hw_specs.get('cpu_threads', 1)} threads)"
        except Exception:
            cpu = platform.processor() or "Unknown CPU"

    ram = "Unknown RAM"
    try:
        out = subprocess.check_output(["free", "-h"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if line.startswith("Mem:"):
                parts = line.split()
                ram = f"{parts[1]} total, {parts[6]} available"
                break
    except Exception:
        if os.name == "nt":
            try:
                class _MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_uint32),
                        ("dwMemoryLoad", ctypes.c_uint32),
                        ("ullTotalPhys", ctypes.c_uint64),
                        ("ullAvailPhys", ctypes.c_uint64),
                        ("ullTotalPageFile", ctypes.c_uint64),
                        ("ullAvailPageFile", ctypes.c_uint64),
                        ("ullTotalVirtual", ctypes.c_uint64),
                        ("ullAvailVirtual", ctypes.c_uint64),
                        ("ullAvailExtendedVirtual", ctypes.c_uint64),
                    ]

                ms = _MEMORYSTATUSEX()
                ms.dwLength = ctypes.sizeof(ms)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms)):
                    tot_gi = ms.ullTotalPhys / (1024.0 ** 3)
                    avl_gi = ms.ullAvailPhys / (1024.0 ** 3)
                    ram = f"{tot_gi:.1f}Gi total, {avl_gi:.1f}Gi available"
            except Exception:
                pass

    gpu = "None"
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,temperature.gpu", "--format=csv,noheader"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if out:
            gpu = out.splitlines()[0]
    except Exception:
        pass

    user_str = os.environ.get("USER") or os.environ.get("USERNAME") or "user"
    net_summary = "Auto-sensed on demand via Engine 19 (`[[targets/local_network_topology]]`)"
    try:
        from Reasoning.engines.rl_network_policy import sense_live_local_network_topology

        topo = sense_live_local_network_topology(force_refresh=False, export_to_vault=False)
        raw_ifaces = topo.get("interfaces", [])
        iface_parts = []
        for i in raw_ifaces:
            if isinstance(i, dict):
                if i.get("cidrs"):
                    iface_parts.append(f"{i.get('name', 'if')}({','.join(i['cidrs'])})")
            elif isinstance(i, str) and i.strip():
                iface_parts.append(i.strip())
        ifaces_str = ", ".join(iface_parts) or "none"
        gw = topo.get("default_gateway") or "none"
        arp_cnt = int(topo.get("reachable_neighbors_count", topo.get("reachable_arp_count", 0)))
        ip_fwd = topo.get("ip_forward_enabled", topo.get("ip_forwarding_enabled", False))
        ser_str = ", ".join(topo.get("serial_devices", [])) or "none"
        net_summary = (
            f"IFs=[{ifaces_str}] | DefaultGW={gw} | IPForward={ip_fwd} | "
            f"ReachableARP={arp_cnt} | SerialOOB=[{ser_str}] (full map: `[[targets/local_network_topology]]`)"
        )
    except Exception:
        pass

    return (
        f"- Hostname: {platform.node()}\n"
        f"- User: {user_str}\n"
        f"- OS: {platform.system()} {platform.release()} ({platform.machine()})\n"
        f"- CPU: {cpu}\n"
        f"- System RAM: {ram}\n"
        f"- GPU: {gpu}\n"
        f"- Local Network Topology: {net_summary}\n"
        f"- Active Local LLM: {MODEL_NAME} (running locally on 127.0.0.1:8080 via llama.cpp CUDA)\n"
        f"- Long-Term Obsidian Knowledge Vault: {VAULT_DIR}\n"
        f"- Isolated Projects Workspace Dir: {PROJECTS_DIR} (Active: `{PROJECTS_DIR / get_active_project_slug()}`)\n"
        f"- Current Working Directory: {os.getcwd()}"
    )


_STATIC_HW_SUMMARY = ""


def resolve_cli_project_file_path(raw_path: str, for_write: bool = False) -> Path:
    """
    Resolve a file or directory path referenced by the LLM or user inside the active project's
    `Projects/<project>/Files/` directory, `Projects/<project>/`, or the local filesystem.
    """
    proj_ws = ensure_project_workspace()
    files_dir = proj_ws / "Files"
    files_dir.mkdir(parents=True, exist_ok=True)

    clean = (raw_path or "").strip().strip('"').strip("'")
    if not clean:
        return files_dir.resolve()

    norm = clean.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]

    if norm.lower() in (
        "files", "files/", "file", "file/", "local files", "local file",
        "local files directory", "local file directory",
    ):
        return files_dir.resolve()

    if norm.lower().startswith("files/"):
        return (files_dir / norm[6:]).resolve()
    if norm.lower().startswith("file/"):
        return (files_dir / norm[5:]).resolve()
    if norm.lower().startswith(f"projects/{proj_ws.name.lower()}/"):
        sub_p = norm[len(f"projects/{proj_ws.name.lower()}/"):]
        return (proj_ws / sub_p).resolve()

    expanded = Path(os.path.expanduser(clean))
    if str(expanded).startswith("/tmp/"):
        return (proj_ws / "downloads" / expanded.name).resolve()
    if expanded.is_absolute():
        return expanded.resolve()

    cand_files = (files_dir / expanded).resolve()
    cand_proj = (proj_ws / expanded).resolve()
    cand_cwd = (Path.cwd() / expanded).resolve()
    cand_root = (CORA_ROOT / expanded).resolve()

    if for_write:
        if norm.startswith("Projects/"):
            return cand_root
        if cand_cwd.exists():
            return cand_cwd
        if "/" not in norm:
            return cand_files
        return cand_proj

    if cand_files.exists():
        return cand_files
    if cand_proj.exists():
        return cand_proj
    if cand_cwd.exists():
        return cand_cwd
    if cand_root.exists():
        return cand_root
    return cand_files


def get_cli_project_files_block(proj_dir: Path, query_text: str = "") -> str:
    """
    Build a structured manifest and optional content preview of `Projects/<slug>/Files/`
    so the CLI LLM always knows where the local `Files` directory is and what is inside it.
    """
    slug = proj_dir.name
    files_dir = proj_dir / "Files"
    files_dir.mkdir(parents=True, exist_ok=True)
    all_files = sorted([f for f in files_dir.rglob("*") if f.is_file()], key=lambda p: p.name.lower())

    lines = [
        f"\nLOCAL PROJECT `Files` DIRECTORY (`Projects/{slug}/Files/` | `$PROJECT_FILES_DIR` = `{files_dir}`):",
        f"  - Anything placed or uploaded into `Projects/{slug}/Files/` is directly accessible to you.",
        f"  - If the user tells you to go to the local `Files` or `File` directory to look at, inspect, or use a custom script or file, look inside `{files_dir}` (`Projects/{slug}/Files/`).",
        f"  - You can read files there with `read_file(path=\"Files/<name>\")`, list it with `list_directory(path=\"Files\")`, edit/create files with `edit_file` / `write_file(path=\"Files/<name>\", ...)`, or run scripts via `run_shell_command` (`$PROJECT_FILES_DIR` is exported and `{files_dir}` is prepended to `PATH`).",
    ]
    if not all_files:
        lines.append(f"  - Current Files in `Projects/{slug}/Files/`: (empty — 0 files currently in Files/)")
        return "\n".join(lines)

    lines.append(f"  - Current Files in `Projects/{slug}/Files/` ({len(all_files)} file{'s' if len(all_files) != 1 else ''}):")
    for idx, f in enumerate(all_files[:40], 1):
        rel = f.relative_to(files_dir).as_posix()
        lines.append(f"    {idx}. `Files/{rel}` (`Projects/{slug}/Files/{rel}`, {f.stat().st_size} bytes)")

    q_low = (query_text or "").lower()
    preview_list: list[Path] = []
    for f in all_files:
        if f.name.lower() in q_low or (len(f.stem) >= 3 and f.stem.lower() in q_low):
            preview_list.append(f)
    if not preview_list and len(all_files) <= 3:
        preview_list = all_files[:3]

    for f in preview_list[:3]:
        try:
            if f.stat().st_size <= 80000:
                raw_b = f.read_bytes()[:1024]
                if b"\x00" not in raw_b:
                    rel = f.relative_to(files_dir).as_posix()
                    txt_snip = f.read_text(encoding="utf-8", errors="replace")[:3500]
                    lines.append(
                        f"\n  [Preview of `Projects/{slug}/Files/{rel}`]:\n```text\n{txt_snip}\n```"
                    )
        except Exception:
            pass

    return "\n".join(lines)


def build_system_prompt(force_refresh_hw: bool = False) -> str:
    global _STATIC_HW_SUMMARY
    if not _STATIC_HW_SUMMARY or force_refresh_hw:
        _STATIC_HW_SUMMARY = get_live_hardware_summary()
    hw = _STATIC_HW_SUMMARY
    vault_index = get_vault_context_for_prompt()
    active_slug = get_active_project_slug()
    active_proj_dir = ensure_project_workspace(active_slug)
    proj_note = read_vault_note(f"projects/{active_slug}")
    existing_projs = [p.name for p in get_existing_project_dirs()]
    proj_menu_lines = [f"  [{i}] {pname}{' [ACTIVE]' if pname == active_slug else ''}" for i, pname in enumerate(existing_projs, 1)]
    proj_menu_lines.append(f"  [{len(existing_projs) + 1}] Rename Current Project")
    proj_menu_lines.append(f"  [{len(existing_projs) + 2}] CREATE NEW PROJECT")
    proj_menu_str = "\n".join(proj_menu_lines)
    proj_files_block = get_cli_project_files_block(active_proj_dir)
    active_proj_block = (
        f"\nCURRENT PROJECTS IN `{PROJECTS_DIR}`:\n{proj_menu_str}\n"
        f"{proj_files_block}\n"
        f"\nACTIVE PROJECT WORKSPACE (`Projects/{active_slug}/` | Files: `{active_proj_dir / 'Files'}` | Memory: `{active_proj_dir / 'memory.md'}` | Downloads: `{active_proj_dir / 'downloads'}`):\n"
        f"{compact_text(proj_note, 1600)}\n"
    )
    os_label = "Windows" if os.name == "nt" else "Linux"
    shell_label = "Windows CMD / PowerShell" if os.name == "nt" else "bash shell"
    personality_block = get_personality_mode_system_prompt_block()
    return (
        f"You are C.O.R.A. (Cyber Oriented Reasoning Agent, Author: https://CROWinnovations.com), an autonomous local AI "
        f"cybersecurity, networking & coding agent for Red Team and Blue Team operations running directly on the user's {os_label} workstation "
        "(NOT on a cloud server). You have full, direct access to the user's hardware, operating system, "
        f"network, filesystem, {shell_label}, a long-term universal Obsidian Knowledge Vault (`ObsidianVault/`), "
        f"and an isolated Project Workspace (`Projects/{active_slug}/`) with a dedicated local `Files` directory (`Projects/{active_slug}/Files/`).\n"
        f"{personality_block}\n"
        "PROJECT SELECTION & WORKSPACE ISOLATION RULES:\n"
        f"  - Every session operates inside a dedicated project folder under `{PROJECTS_DIR}` (currently `{active_proj_dir}`). "
        "Any spaces or special characters in project names are automatically converted to dashes (`-`).\n"
        f"  - **Local Project `Files` Directory (`{active_proj_dir / 'Files'}` / `Projects/{active_slug}/Files/`)**: Every project has a `Files` directory. Anything placed or uploaded into `Projects/{active_slug}/Files/` is directly visible and usable by you. When the user tells you to go to the local `Files` or `File` directory to look at or use a custom script or file, inspect `{active_proj_dir / 'Files'}` (`Projects/{active_slug}/Files/`).\n"
        "  - In the Web Interface (or if the user asks to view, select, create, or rename a project), present the numbered list of "
        f"current projects in `{PROJECTS_DIR}` (`1..{len(existing_projs)}`), followed by `[{len(existing_projs) + 1}] Rename Current Project` "
        f"and `[{len(existing_projs) + 2}] CREATE NEW PROJECT`, and use `project_tracker` (`action='select'|'create'|'rename'|'update'`) to switch, create, or rename the project.\n"
        f"  - Tier-1 Long-Term Universal Knowledge (`{VAULT_DIR}`): Contains universal playbooks, trained reference docs (`00_TRAINED_INDEX.md`), "
        "and cross-system rules. Read from it anytime with `vault_search` / `vault_read_note`, but NEVER pollute it with temporary test data or internal local network state.\n"
        f"  - Tier-2 Isolated Project Workspace (`{active_proj_dir}`): Put custom user scripts/uploads in `{active_proj_dir / 'Files'}`, downloaded files in `{active_proj_dir / 'downloads'}`, "
        f"temporary test scripts/files, target scans, and project-specific memory (`{active_proj_dir / 'memory.md'}`) inside `{active_proj_dir}`.\n\n"
        "YOUR BUILT-IN TOOLS:\n"
        f"  1. `project_tracker`: Select, create, rename, or update an isolated project in `Projects/<project_name>/memory.md` "
        "(auto-converts spaces/special characters to dashes `-`; tracks documentation findings, verification questions, verified data, project plan milestones, and execution log).\n"
        f"  2. `scan_target`: Inspect any URL/API/host (headers, status, endpoints, forms, JSON structure) AND "
        f"auto-save the report into `Projects/{active_slug}/targets/`. ALWAYS use `scan_target` or `vault_read_note` before "
        "crafting `curl` commands.\n"
        f"  3. `vault_save_note`: Save project findings, verified working `curl` commands, endpoints, or session "
        f"notes into `Projects/{active_slug}/notes/<title>.md` (and index them in `Projects/{active_slug}/memory.md`).\n"
        "  4. `vault_search`: Search both your active `Projects/` workspace and your long-term `ObsidianVault/` for notes, targets, or playbooks.\n"
        "  5. `vault_read_note`: Read a specific note (e.g. `commands/curl_playbook`, `commands/tio_serial_playbook`, or `memory`) from `Projects/` or `ObsidianVault/`.\n"
        "  6. `neuro_symbolic_reason`: Deterministic 15-Engine CPU-based Neuro-Symbolic, Somatic Intuition, Optimal-Stopping Forecasting, "
        "Continual, Meta-Learning, Trajectory RL & Spectral PCA/K-Means++ Reasoning Suite (0 MB GPU VRAM). "
        f"Returns a single authoritative `>>> CONSENSUS IMMEDIATE ACTION <<<` + Speculative Next-Tool Branches + 3-Step RL Rollout and saves session reports to `Projects/{active_slug}/reasoning/`.\n"
        f"  7. `run_shell_command`: Execute any {shell_label} command or custom script in `{active_proj_dir / 'Files'}` (`$PROJECT_FILES_DIR`, which is on `PATH`; pre-verified by CEGAR; save downloaded files to `{active_proj_dir / 'downloads'}`; outputs > 2,500 chars are losslessly archived to `Reasoning/data/shadow_archive/`).\n"
        f"  8. `write_file` / `edit_file` / `read_file` / `list_directory`: Full local filesystem access, including direct shorthand access to `Files/<filename>` inside `{active_proj_dir / 'Files'}`.\n"
        f"  9. `generate_project_report`: Generate a comprehensive 5-section Project Status & Findings Report (`Projects/{active_slug}/REPORT.md` + standalone SVG graphic `assets/report_dashboard.svg`) containing an Executive Summary, a High-School Reading Level Walkthrough, Visual Graphics/Mermaid Diagrams, a Technical Evidence Write-Up, and a Final Conclusion.\n\n"
        "PEAK PERFORMANCE & MEMORY RULES:\n"
        "- NEVER say you are a cloud AI or that you cannot access local files, network targets, hardware, or commands.\n"
        "- Check the Obsidian Memory Index and Active Project Memory below first! If a target, playbook, reasoning synthesis, or project is already indexed, read it "
        "with `vault_read_note` instead of guessing.\n"
        f"- When downloading files with `curl -o`, `wget -O`, or creating test scripts/files for the current project, store them in `{active_proj_dir / 'downloads'}` or `{active_proj_dir}`.\n"
        "- For `/dev/ttyUSB0` serial console: NEVER use Python scripts or `import ...` inside `tio --script`, and NEVER bombard the console with chained commands (`cmd1; cmd2; cmd3`) or rapid back-to-back calls (which overruns the UART RX buffer and drops the connection). Always use hardware character/line pacing `-o 15 -O 120` and send ONLY 1 command per `tio` invocation (`tio -b 115200 -o 15 -O 120 --mute --script-run once --script 'write(\"\\r\"); msleep(500); write(\"cmd\\r\"); while read(4096, 600) > 0 do end; exit(0)' /dev/ttyUSB0`). Read `[[commands/tio_serial_playbook]]` with `vault_read_note` before running `tio`.\n"
        f"- Keep `run_shell_command` arguments concise and focused on a single {shell_label} command.\n"
        "- When debugging connection failures (e.g. curl exit 7), multi-hop L2/L3 routing, or API auth rejections, call "
        "`neuro_symbolic_reason` to compute the 15-Engine 5-Layer Lexical Hedge-weighted consensus action, Damasio Somatic Gut Valence, Optimal Stopping decision, "
        "Speculative Next-Tool Branches (`on_success` / `on_failure`), Pessimistic Q_LCB RL trajectory, and Bayesian root-cause probabilities instead of guessing.\n"
        "- When onboarding a project from documentation: first call `project_tracker` to create the project workspace under "
        "`Projects/<project_name>/memory.md`, summarize what you learned from the docs, and ask the user targeted verification questions "
        "to confirm IPs, credentials, interfaces, or goals. Whenever the user answers or a task completes, update the project "
        "memory with `project_tracker`.\n\n"
        f"LIVE LOCAL SYSTEM SNAPSHOT:\n{hw}\n\n"
        f"OBSIDIAN VAULT MEMORY INDEX (Tier-1 Universal Hot Memory):\n{vault_index}"
        f"{active_proj_block}"
    )


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "project_tracker",
            "description": (
                "Select, create, rename, or update an isolated project workspace and tracking note in Projects/<project_name>/memory.md "
                "(auto-converts spaces and special characters to dashes `-`), set it as the active project, and record ingested "
                "documentation, verification questions, verified user answers, step-by-step project plans, and task progress."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["select", "create", "rename", "update"],
                        "description": "Project action: 'select' existing, 'create' new, 'rename' existing (uses new_name), or 'update' memory.md.",
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Project name or slug (spaces/special chars auto-convert to dashes; stored at Projects/<project_name>/memory.md).",
                    },
                    "new_name": {
                        "type": "string",
                        "description": "When action='rename', the new name for the project (spaces/special chars auto-convert to dashes `-`).",
                    },
                    "summary": {
                        "type": "string",
                        "description": "One-line project status summary for Projects/<project_name>/memory.md.",
                    },
                    "verified_data": {
                        "type": "string",
                        "description": "Markdown bullet list of key facts, targets, IPs, ports, and user-verified data.",
                    },
                    "questions": {
                        "type": "string",
                        "description": "Markdown bullet list of open verification/clarification questions for the user (or 'All verified').",
                    },
                    "plan_and_tasks": {
                        "type": "string",
                        "description": "Markdown checklist (- [ ] / - [x]) of project phases, planned tasks, and execution log.",
                    },
                },
                "required": ["project_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scan_target",
            "description": (
                "Scan a URL, API endpoint, or host to discover HTTP response headers, status code, "
                "API routes/links, HTML forms/inputs, JSON keys, and clean readable content. "
                "Automatically saves the scan report to Projects/<active_project>/targets/ and indexes it in memory.md."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "The URL or hostname/IP to scan (e.g. 'https://example.com' or 'http://127.0.0.1:8080/health').",
                    }
                },
                "required": ["target"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_save_note",
            "description": (
                "Save or update a structured Markdown note in the active project workspace "
                "(Projects/<active_project>/notes/<title>.md) and index it in Projects/<active_project>/memory.md "
                "so long-term ObsidianVault memory stays clean."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["targets", "commands", "projects", "knowledge", "reasoning"],
                        "description": "Vault folder category.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Short descriptive title for the note (e.g. 'local_api_curl_commands').",
                    },
                    "summary": {
                        "type": "string",
                        "description": "One-line summary for 00_MEMORY_INDEX.md.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Distilled Markdown content (working commands, endpoints, findings).",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of tags (e.g. ['curl', 'api']).",
                    },
                },
                "required": ["category", "title", "summary", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_search",
            "description": "Search all Markdown notes in the local Obsidian Knowledge Vault by keyword or tag.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords or tag to search for in ObsidianVault.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_read_note",
            "description": "Read the full contents of a note from ObsidianVault (e.g. 'commands/curl_playbook' or 'targets/example_com').",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {
                        "type": "string",
                        "description": "WikiLink or relative path of the note (e.g. 'commands/curl_playbook').",
                    }
                },
                "required": ["note"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell_command",
            "description": "Execute a shell command (bash on Linux; CMD/PowerShell on Windows) on the local host system and return stdout/stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command line to execute.",
                    }
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create a new file or overwrite an existing file on the local filesystem.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path (absolute or relative to current directory, ~ is expanded).",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full text content to write to the file.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replace old_text with new_text inside an existing local file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to edit."},
                    "old_text": {"type": "string", "description": "Exact existing text to replace."},
                    "new_text": {"type": "string", "description": "New replacement text."},
                },
                "required": ["path", "old_text", "new_text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a local file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and directories at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list (defaults to current working directory).",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "neuro_symbolic_reason",
            "description": (
                "Run deterministic 15-Engine CPU-based Neuro-Symbolic, Somatic Intuition, Optimal-Stopping Forecasting, "
                "Continual, Meta-Learning, Trajectory RL & Spectral PCA/K-Means++ Reasoning (0 MB GPU VRAM) with Hedge-Weighted Consensus Arbiter. Supports "
                "`engine='pipeline'` (chains all 15 engines together and outputs `>>> CONSENSUS IMMEDIATE ACTION <<<` + "
                "Speculative Next-Tool Branches + 3-Step RL Rollout), `associative`, `geometric`, `bayesian`, `dempster_shafer`, "
                "`causal`, `temporal`, `cbr`, `vsa`, `sygus`, `cegar`, `mdp`, "
                "`continual`, `meta`, `rl`, or `pca`. Automatically saves full reports to ObsidianVault/reasoning/."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "engine": {
                        "type": "string",
                        "enum": [
                            "pipeline",
                            "associative",
                            "bayesian",
                            "dempster_shafer",
                            "causal",
                            "temporal",
                            "cbr",
                            "vsa",
                            "sygus",
                            "cegar",
                            "geometric",
                            "mdp",
                            "continual",
                            "meta",
                            "rl",
                            "pca",
                        ],
                        "description": "Reasoning engine mode ('pipeline' runs all 15 core engines synergistically; 'rl' runs Trajectory RL & Network World-Model; 'pca' runs SVD PCA, K-Means++ & Graph Laplacian).",
                    },
                    "problem": {
                        "type": "string",
                        "description": "Problem statement or debugging goal (e.g. 'curl exit 7 on target API endpoint').",
                    },
                    "target_ip": {
                        "type": "string",
                        "description": "Primary target IP or host (optional; auto-resolved from problem/host if omitted).",
                    },
                    "secondary_target_ip": {
                        "type": "string",
                        "description": "Optional secondary/destination IP for L2/L3 routing.",
                    },
                    "profile": {
                        "type": "string",
                        "enum": ["http_api_unreachable", "l2_l3_routing_blackhole", "api_auth_rejection"],
                        "description": "Bayesian diagnostic profile.",
                    },
                    "observed_evidence": {
                        "type": "object",
                        "description": "Dict of observed boolean evidence (e.g. {'curl_exit_7_Immediate_refused': true}).",
                    },
                    "confirmed_cause": {
                        "type": "string",
                        "description": "Optional confirmed root cause hypothesis key to update learned Bayesian priors.",
                    },
                    "causal_dag": {
                        "type": "string",
                        "enum": ["network_api_reachability", "l2_l3_cross_subnet_routing", "api_auth_exploitation_chain"],
                        "description": "Causal DAG model name.",
                    },
                    "do_interventions": {
                        "type": "object",
                        "description": "Optional Pearl do(Node=Prob) interventions (e.g. {'Serial_Console_OOB': 1.0}).",
                    },
                    "local_subnets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Local CIDR subnets (auto-detected from host interfaces if omitted).",
                    },
                },
                "required": ["problem"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_project_report",
            "description": (
                "Generate a comprehensive 5-section Project Status & Findings Report (Executive Summary, "
                "Plain-English High-School Reading Level Walkthrough, Standalone SVG Infographic + Mermaid Diagrams, "
                "Technical Findings & Verified Evidence Write-Up, and Final Conclusion) saved to Projects/<active_project>/REPORT.md."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Optional project name/slug under Projects/ (defaults to the active project).",
                    },
                    "report_focus": {
                        "type": "string",
                        "description": "Optional focus topic or objective to highlight in the report.",
                    },
                },
            },
        },
    },
]


def compact_text(text: str, limit: int = MAX_TOOL_OUTPUT_CHARS) -> str:
    """Strip bulky script/style blocks from HTML and cap length with head+tail preservation."""
    if not text:
        return ""
    if "<html" in text.lower() or "<script" in text.lower() or "<style" in text.lower():
        text = re.sub(r"(?is)<(script|style|svg|noscript)\b.*?>.*?</\1>", " ", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) <= limit:
        return text
    half = limit // 2
    omitted = len(text) - limit
    return f"{text[:half]}\n\n... [TRUNCATED {omitted} chars to fit context window] ...\n\n{text[-half:]}"


def perform_target_scan(target: str) -> str:
    url = target.strip()
    if not re.match(r"^https?://", url, re.I):
        url = "http://" + url

    hdr_cmd = ["curl", "-sS", "-k", "-L", "-I", "--max-time", "15", url]
    body_cmd = ["curl", "-sS", "-k", "-L", "--max-time", "20", url]

    headers_out = ""
    try:
        headers_out = subprocess.check_output(hdr_cmd, text=True, stderr=subprocess.STDOUT, timeout=20).strip()
    except Exception as exc:
        headers_out = f"(Header probe failed: {exc})"

    body_out = ""
    try:
        body_out = subprocess.check_output(body_cmd, text=True, stderr=subprocess.STDOUT, timeout=25)
    except Exception as exc:
        body_out = f"(Body fetch failed: {exc})"

    summary = [f"=== Scan Report for {url} ==="]
    status_line = headers_out.splitlines()[0] if headers_out else "Unknown status"
    summary.append(f"\n[1] HTTP Response Headers:\n{headers_out[:1000]}")

    stripped = body_out.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            parsed = json.loads(stripped)
            pretty = json.dumps(parsed, indent=2)
            summary.append(f"\n[2] JSON Payload Structure ({len(stripped)} bytes):\n{compact_text(pretty, 2000)}")
            report_text = "\n".join(summary)
            host_slug = slugify(re.sub(r"^https?://", "", url))
            save_note_to_vault(
                "targets",
                f"scan_{host_slug}",
                f"Target scan of {url} ({status_line}, JSON endpoint)",
                report_text,
                ["target", "scan", "json", "curl"],
            )
            return report_text
        except Exception:
            pass

    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", body_out)
    page_title = html.unescape(title_match.group(1).strip()) if title_match else "No title"
    if title_match:
        summary.append(f"\n[2] Page Title: {page_title}")

    forms = re.findall(r"(?is)<form\b[^>]*>.*?</form>", body_out)
    if forms:
        form_summaries = []
        for idx, f in enumerate(forms[:5], 1):
            action = re.search(r'(?i)\baction=["\']?([^"\' >]+)', f)
            method = re.search(r'(?i)\bmethod=["\']?([^"\' >]+)', f)
            inputs = re.findall(r'(?i)<input\b[^>]*\bname=["\']?([^"\' >]+)', f)
            form_summaries.append(
                f"  - Form #{idx}: method={(method.group(1).upper() if method else 'GET')} "
                f"action={(action.group(1) if action else url)} inputs={inputs}"
            )
        summary.append("\n[3] Discovered HTML Forms:\n" + "\n".join(form_summaries))

    endpoints = sorted(
        set(
            re.findall(
                r'(?:href|src|action|url|fetch|axios\.\w+)\s*[\(="\']+\s*([/a-zA-Z0-9_.\-?:=&%]+)',
                body_out,
            )
        )
    )
    if endpoints:
        summary.append("\n[4] Discovered Links / Endpoints (up to 40):\n  " + ", ".join(endpoints[:40]))

    clean = re.sub(r"(?is)<(script|style|svg|noscript)\b.*?>.*?</\1>", " ", body_out)
    clean = re.sub(r"(?s)<[^>]+>", " ", clean)
    clean = html.unescape(re.sub(r"\s+", " ", clean)).strip()
    summary.append(f"\n[5] Page Content Preview ({len(body_out)} raw bytes):\n{clean[:1200]}")

    report_text = "\n".join(summary)
    host_slug = slugify(re.sub(r"^https?://", "", url))
    save_note_to_vault(
        "targets",
        f"scan_{host_slug}",
        f"Target scan of {url} ({status_line}, title: {page_title[:50]})",
        report_text,
        ["target", "scan", "curl"],
    )
    return report_text


def confirm_action(action_desc: str) -> bool:
    global SKIP_PERMISSIONS
    if SKIP_PERMISSIONS:
        return True
    try:
        p_start = _rl_wrap("\033[1;35m")
        p_end = _rl_wrap("\033[0m")
        ans = input(f"{p_start}  Allow {action_desc}? [y/N/a (always)]: {p_end}").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    if ans in ("a", "always"):
        SKIP_PERMISSIONS = True
        HUD.render(force_region=False)
        print("  \033[1;33m-> Auto-run enabled for the remainder of this session.\033[0m")
        return True
    return ans in ("y", "yes")


ALL_CAPABILITY_VECTORS = (
    "L1_Serial_OOB",
    "L2_ARP_Link",
    "L3_Routing_NAT",
    "L4_Port_Service",
    "L7_HTTP_Web_Exploit",
    "Vault_Knowledge_Playbooks",
    "Neuro_Symbolic_15_Engines",
)


def _normalize_cmd_for_dedup(tool_name: str, target_or_cmd: str) -> str:
    s = (target_or_cmd or "").strip()
    if tool_name == "run_shell_command":
        # Strip trailing stderr/stdout redirections and trailing slashes so trivial variants match
        s = re.sub(r"\s+(?:[12]?>>?\s*/dev/null|[12]>&[12]|&>\s*/dev/null)\s*$", "", s)
        s = re.sub(r"/+(?=\s|$)", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _classify_attempt_layer(tool_name: str, target_or_cmd: str) -> str:
    raw = (target_or_cmd or "").strip()
    low = raw.lower()
    if tool_name == "neuro_symbolic_reason":
        return "Neuro_Symbolic_15_Engines"
    if tool_name in ("vault_search", "vault_read_note", "project_tracker", "vault_save_note"):
        return "Vault_Knowledge_Playbooks"
    if tool_name in ("read_file", "list_directory", "write_file", "edit_file"):
        return "Filesystem_Host_Inspection"
    # Check if shell command is purely local file/directory inspection first
    first_bin = re.sub(r"^(?:sudo\s+|env\s+)+", "", low).split()[0] if low.split() else ""
    if (
        tool_name == "run_shell_command"
        and first_bin in ("ls", "find", "locate", "cat", "head", "tail", "grep", "egrep", "fgrep", "stat", "file", "wc", "pwd", "cd")
        and not re.search(r"\b(?:curl|wget|tio|nmap|nc|ncat|socat|ssh|ping|ip\s+(?:route|neigh|addr|link)|arping)\b", low)
    ):
        return "Filesystem_Host_Inspection"
    if re.search(r"\b(?:tio|ttyusb\d*|ttyacm\d*|minicom|stty|com[1-9]\d*)\b|plink\s+-serial|/dev/tty(?:usb|acm|s)\d+", low):
        return "L1_Serial_OOB"
    if re.search(r"\b(?:ip\s+(?:-[46brs]+\s+)*(?:neigh|link)|arping|arp\s+-[a-z]|bridge|vlan|get-netneighbor|get-netadapter)\b", low):
        return "L2_ARP_Link"
    if re.search(
        r"\b(?:ip\s+(?:-[46brs]+\s+)*(?:route|addr|address|rule|netns)|ipconfig|route\s+(?:print|add|delete)|"
        r"new-netroute|get-netroute|get-netipaddress|iptables|ip6tables|netsh|nft|sysctl|ip_forward|ping|traceroute|tracert)\b",
        low,
    ):
        return "L3_Routing_NAT"
    if re.search(r"\b(?:nmap|masscan|ss\s+-|netstat|nc|ncat|socat|ssh|test-netconnection|get-nettcpconnection)\b", low):
        return "L4_Port_Service"
    if tool_name == "scan_target" or re.search(
        r"\b(?:curl|wget|invoke-webrequest|invoke-restmethod|iwr|irm|gobuster|ffuf|nikto|sqlmap|python3|openssl)\b|https?://",
        low,
    ):
        return "L7_HTTP_Web_Exploit"
    return "Filesystem_Host_Inspection"


def _find_duplicate_failed_attempt(tool_name: str, target_or_cmd: str) -> dict | None:
    """In Relentless Mode, check if this exact command/target (or trivial redirection variant) was already executed."""
    norm = _normalize_cmd_for_dedup(tool_name, target_or_cmd)
    if not norm:
        return None
    for entry in reversed(ATTEMPT_LEDGER):
        entry_norm = _normalize_cmd_for_dedup(entry.get("tool", ""), entry.get("norm_key") or entry.get("target_or_cmd", ""))
        if entry.get("tool") == tool_name and entry_norm == norm:
            if entry.get("status") in ("FAIL", "BLOCKED", "OK"):
                return entry
    return None


def _sync_goal_and_attempts_to_vault() -> str:
    """Persist the active `/goal` and full `ATTEMPT_LEDGER` to `ObsidianVault/projects/` and `Reasoning/data/sessions/`."""
    if not ACTIVE_GOAL and not ATTEMPT_LEDGER:
        return ""
    goal_title = ACTIVE_GOAL or (f"Project {ACTIVE_PROJECT}" if ACTIVE_PROJECT else "Session Objective")
    goal_slug = f"goal_{slugify(ACTIVE_PROJECT or goal_title[:36])}"

    tried_vectors = sorted({a.get("layer", "") for a in ATTEMPT_LEDGER if a.get("layer")})
    untried_vectors = [v for v in ALL_CAPABILITY_VECTORS if v not in tried_vectors]

    max_w_disp = "∞ (UNLIMITED)" if MAX_RELENTLESS_WAVES == 0 else str(MAX_RELENTLESS_WAVES)
    lines = [
        f"## 1. Active Goal (`/goal`)",
        f"- **Objective:** {goal_title}",
        f"- **Active Project:** `{ACTIVE_PROJECT or 'None'}`",
        f"- **Relentless Mode (`/relentless`):** `{'ON' if RELENTLESS_MODE else 'OFF'}` (Wave `{CURRENT_WAVE}` / `{max_w_disp}`)",
        f"- **Total Tool Attempts Logged:** `{len(ATTEMPT_LEDGER)}`",
        f"- **Capability Vectors Tried:** `{', '.join(tried_vectors) if tried_vectors else 'None yet'}`",
        f"- **Untried Capability Vectors Remaining:** `{', '.join(untried_vectors) if untried_vectors else 'All vectors probed — refine parameters/combine chains'}`",
        "",
        "## 2. Attempt Ledger (Already Tried — Do Not Repeat Failed Commands)",
    ]
    if not ATTEMPT_LEDGER:
        lines.append("- *(No tool attempts recorded yet for this goal)*")
    else:
        for idx, att in enumerate(ATTEMPT_LEDGER[-30:], 1):
            lines.append(
                f"{idx}. **[Wave {att['wave']} | {att['status']} | `{att['layer']}`]** "
                f"`{att['tool']}` -> `{att['target_or_cmd'][:110]}` — *{att['summary'][:140]}*"
            )

    body_md = "\n".join(lines)
    try:
        save_note_to_vault(
            "projects",
            goal_slug,
            f"Active Goal & Attempt Ledger: {goal_title[:70]} ({len(ATTEMPT_LEDGER)} attempts)",
            body_md,
            ["goal", "relentless", "ledger", ACTIVE_PROJECT or "session"],
        )
        from Reasoning.engines.vault_bridge import save_json_data

        save_json_data(
            "sessions",
            "relentless_ledger",
            {
                "active_goal": ACTIVE_GOAL,
                "active_project": ACTIVE_PROJECT,
                "relentless_mode": RELENTLESS_MODE,
                "current_wave": CURRENT_WAVE,
                "max_waves": MAX_RELENTLESS_WAVES,
                "tried_vectors": tried_vectors,
                "untried_vectors": untried_vectors,
                "attempts": ATTEMPT_LEDGER[-60:],
            },
        )
    except Exception:
        pass
    return f"projects/{goal_slug}"


def _record_attempt(tool_name: str, target_or_cmd: str, status: str, result_text: str) -> None:
    """Record a tool execution into `ATTEMPT_LEDGER` and sync to ObsidianVault when a goal or relentless mode is active."""
    norm = re.sub(r"\s+", " ", (target_or_cmd or "").strip())
    first_line = ""
    for ln in (result_text or "").splitlines():
        s = ln.strip()
        if s and not s.startswith("==="):
            first_line = s
            break
    layer = _classify_attempt_layer(tool_name, norm)
    ATTEMPT_LEDGER.append(
        {
            "wave": max(1, CURRENT_WAVE),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "tool": tool_name,
            "target_or_cmd": norm[:180],
            "norm_key": norm,
            "layer": layer,
            "status": status,
            "summary": (first_line or status)[:180],
        }
    )
    if ACTIVE_GOAL or RELENTLESS_MODE:
        _sync_goal_and_attempts_to_vault()


_LAST_SERIAL_IO_EPOCH = 0.0


def execute_tool(name: str, args: dict) -> str:
    global ACTIVE_PROJECT, _LAST_SERIAL_IO_EPOCH
    try:
        if name == "project_tracker":
            act = str(args.get("action") or "update").strip().lower()
            proj_name = args.get("project_name") or ACTIVE_PROJECT or "active_project"
            slug = slugify_project_name(proj_name)
            if act == "rename":
                new_raw = str(args.get("new_name") or "").strip()
                if not new_raw:
                    return "Error: `new_name` is required when `action='rename'`."
                ok, new_slug, msg = rename_project_workspace(slug, new_raw)
                if ok:
                    _persist_selected_project(new_slug)
                return msg
            _persist_selected_project(slug)
            if act == "select" and not args.get("summary") and not args.get("verified_data"):
                print(
                    f"\n\033[1;32m[Isolated Project -> project_tracker (select)]\033[0m [[Projects/{slug}/memory]] (Active Project)",
                    flush=True,
                )
                return f"Selected active project `Projects/{slug}/`.\n\n" + read_vault_note(f"projects/{slug}")
            summary = args.get("summary", f"Project tracker for {slug}")
            verified_data = args.get("verified_data", "- Pending verification")
            questions = args.get("questions", "- None")
            plan_and_tasks = args.get("plan_and_tasks", "- [ ] Initial documentation review")
            body = (
                "## 1. Verified Data & Architecture\n"
                f"{verified_data.strip()}\n\n"
                "## 2. Open Verification Questions\n"
                f"{questions.strip()}\n\n"
                "## 3. Project Plan & Task Tracking\n"
                f"{plan_and_tasks.strip()}\n"
            )
            print(
                f"\n\033[1;32m[Isolated Project -> project_tracker]\033[0m [[Projects/{slug}/memory]] (Active Project)",
                flush=True,
            )
            return save_note_to_vault("projects", slug, summary, body, ["project", "plan", slug])

        elif name == "scan_target":
            target = (args.get("target") or "").strip()
            if (ACTIVE_PERSONALITY_MODE or os.environ.get("CORA_PERSONALITY_MODE", "DEFAULT")).upper() == "ANALYST":
                res_blk = (
                    f"[ANALYST MODE ENFORCEMENT — `scan_target` BLOCKED]: `{target}`\n"
                    "- Reason: Analyst Mode (WHITE Network Isolation) strictly prohibits network scanning and sending data outside the local laptop system.\n"
                    "- Allowed Action: Analyze existing local scan results, files, and notes inside `Projects/` and `ObsidianVault/` using `read_file`, `list_directory`, `vault_search`, `vault_read_note`, and `neuro_symbolic_reason`."
                )
                print(f"\n\033[1;31m[Analyst Mode Blocked scan_target]\033[0m Network scanning is disabled in Analyst Mode (`WHITE` isolation).", flush=True)
                _record_attempt("scan_target", target, "BLOCKED", res_blk)
                return res_blk
            if RELENTLESS_MODE:
                dup = _find_duplicate_failed_attempt("scan_target", target)
                if dup:
                    msg = (
                        f"[Relentless Anti-Repetition Guard] You already ran `scan_target({target})` in Wave #{dup['wave']} "
                        f"and it failed (`{dup['summary']}`). Do NOT repeat the exact same failed scan — try a different port, "
                        "protocol, `run_shell_command` (e.g. `nmap`, `ip neigh`, `tio`, `curl` with headers), or `neuro_symbolic_reason`!"
                    )
                    print(f"\n\033[1;35m{msg}\033[0m", flush=True)
                    return msg
            try:
                from Reasoning.engines.cegar_verifier import verify_target_address_cegar

                t_ver = verify_target_address_cegar(target)
                if t_ver.get("blocked"):
                    print(
                        f"\n\033[1;31m[CEGAR Pre-Verifier Blocked scan_target]\033[0m {t_ver.get('counterexample')}",
                        flush=True,
                    )
                    res_blk = (
                        f"[CEGAR Pre-Execution Verifier BLOCKED `scan_target`]: `{target}`\n"
                        f"- Reason: {t_ver.get('reason')}\n"
                        f"- Counterexample: {t_ver.get('counterexample')}\n"
                        f"- Suggested Fix: {t_ver.get('suggested_fix')}"
                    )
                    _record_attempt("scan_target", target, "BLOCKED", res_blk)
                    return res_blk
            except Exception:
                pass
            print(
                f"\n\033[1;36m[Agent Tool -> scan_target]\033[0m {target} (auto-saving to Projects/{get_active_project_slug()}/targets/)",
                flush=True,
            )
            scan_out = perform_target_scan(target)
            status = "FAIL" if "(Header probe failed:" in scan_out and "(Body fetch failed:" in scan_out else "OK"
            _record_attempt("scan_target", target, status, scan_out)
            return scan_out

        elif name == "vault_save_note":
            cat = args.get("category", "knowledge")
            title = args.get("title", "note")
            summary = args.get("summary", title)
            content = args.get("content", "")
            tags = args.get("tags") or [cat]
            print(
                f"\n\033[1;32m[Project Memory -> save_note]\033[0m [[Projects/{get_active_project_slug()}/notes/{slugify(title)}]]",
                flush=True,
            )
            out = save_note_to_vault(cat, title, summary, content, tags, persist_long_term=False)
            _record_attempt("vault_save_note", f"{cat}/{title}", "OK", out)
            return out

        elif name == "vault_search":
            query = args.get("query", "")
            print(f"\n\033[1;36m[Obsidian Vault -> search]\033[0m '{query}'", flush=True)
            out = search_vault(query)
            _record_attempt("vault_search", query, "OK", out)
            return out

        elif name == "vault_read_note":
            note_ref = args.get("note", "")
            print(f"\n\033[1;36m[Obsidian Vault -> read_note]\033[0m [[{note_ref}]]", flush=True)
            out = read_vault_note(note_ref)
            _record_attempt("vault_read_note", note_ref, "FAIL" if out.startswith("Note `") else "OK", out)
            return out

        elif name == "run_shell_command":
            cmd = (args.get("command") or "").strip()
            if not cmd:
                print("\n\033[1;33m[Agent Tool -> run_shell_command]\033[0m (Skipped empty command)", flush=True)
                return "Error: `command` argument was empty or malformed JSON. Provide a concise single-line bash command."

            # Route /tmp/ downloaded outputs into Projects/<active_project>/downloads/
            cmd = _redirect_tmp_downloads_to_project(cmd)
            proj_ws = ensure_project_workspace()

            if RELENTLESS_MODE:
                dup = _find_duplicate_failed_attempt("run_shell_command", cmd)
                if dup:
                    msg = (
                        f"[Relentless Anti-Repetition Guard] You already executed `$ {cmd}` in Wave #{dup['wave']} "
                        f"and it failed (`{dup['summary']}`). Do NOT run the exact same failed command again! "
                        "Check the Obsidian Vault & Attempt Ledger and try a DIFFERENT command, flag, port, interface, OOB channel, or tool!"
                    )
                    print(f"\n\033[1;35m{msg}\033[0m", flush=True)
                    return msg

            # Normalize HTTPS curl self-signed cert handling (`-k`) and Windows CLI flag syntax before CEGAR
            if re.match(r"^\s*curl(?:\.exe)?\b", cmd, re.I) and "https://" in cmd.lower():
                if not re.search(r"(?:\s-[a-zA-Z]*k\b|\s--insecure\b)", cmd):
                    cmd = re.sub(r"^(\s*curl(?:\.exe)?)\b", r"\1 -k", cmd, count=1, flags=re.I)
            if os.name == "nt":
                if re.match(r"^\s*ping(?:\.exe)?\b", cmd, re.I):
                    cmd = re.sub(r"\s-c\s+(\d+)", r" -n \1", cmd)
                    cmd = re.sub(
                        r"\s-W\s+(\d+)",
                        lambda m: f" -w {int(m.group(1)) * 1000 if int(m.group(1)) < 50 else int(m.group(1))}",
                        cmd,
                    )
                elif re.match(r"^\s*ip\s+neigh(?:\s+show)?\s*$", cmd, re.I):
                    cmd = "arp -a"

            # Engine 12: CEGAR Pre-Execution Verifier + Hardware UART Pacing Auto-Transform
            cegar_advisories = []
            try:
                from Reasoning.engines.cegar_verifier import (
                    apply_serial_pacing_transform,
                    is_analyst_mode,
                    verify_command_cegar,
                )

                cmd, pacing_note = apply_serial_pacing_transform(cmd)
                if pacing_note:
                    cegar_advisories.append(pacing_note)

                cegar_res = verify_command_cegar(cmd)
                if cegar_res.get("blocked"):
                    repaired = cegar_res.get("repaired_command") or cegar_res.get("auto_repaired_command")
                    same_bin = (
                        bool(repaired)
                        and not is_analyst_mode()
                        and cmd.split()[0].lower().removesuffix(".exe")
                        == str(repaired).split()[0].lower().removesuffix(".exe")
                    )
                    if same_bin and not verify_command_cegar(str(repaired)).get("blocked"):
                        cmd = str(repaired)
                        cegar_res = verify_command_cegar(cmd)
                    else:
                        print(
                            f"\n\033[1;31m[CEGAR Pre-Verifier Blocked]\033[0m {cegar_res.get('reason')}",
                            flush=True,
                        )
                        res_blk = (
                            f"[CEGAR Pre-Execution Verifier BLOCKED Command]: `{cmd}`\n"
                            f"- Reason: {cegar_res.get('reason')}\n"
                            f"- Counterexample: {cegar_res.get('counterexample')}\n"
                            f"- Suggested Fix: {cegar_res.get('suggested_fix')}"
                        )
                        _record_attempt("run_shell_command", cmd, "BLOCKED", res_blk)
                        return res_blk
                cegar_advisories.extend(cegar_res.get("advisories") or [])
            except Exception:
                pass

            print(f"\n\033[1;33m[Agent Tool -> run_shell_command]\033[0m $ {cmd}", flush=True)
            if not confirm_action(f"shell command `{cmd}`"):
                print("  \033[1;31m-> Denied by user.\033[0m", flush=True)
                return "Action denied by user: shell command was not executed."

            # Enforce hardware UART settle cooldown between consecutive `/dev/ttyUSB*` / `tio` sessions
            is_serial_cmd = bool(re.search(r"\btio\b|/dev/tty(?:usb|acm|s|ama)\d+", cmd, re.I))
            if is_serial_cmd and _LAST_SERIAL_IO_EPOCH > 0.0:
                since_last_ser = time.time() - _LAST_SERIAL_IO_EPOCH
                if 0.0 <= since_last_ser < 1.6:
                    time.sleep(1.6 - since_last_ser)

            if os.name == "nt" and "tio " not in cmd:
                cmd = re.sub(r"\barp\s+-accepteula\b", "arp -a", cmd, flags=re.I)
                cmd = re.sub(r"\bping\s+-c\s+(\d+)\s+-W\s+\d+\b", r"ping -n \1 -w 1200", cmd)
                cmd = re.sub(r"\bping\s+-c\s+(\d+)\b", r"ping -n \1", cmd)
                cmd = re.sub(r"\bip\s+neigh\s+show\b", "arp -a", cmd)
            elif os.name != "nt":
                cmd = re.sub(r"\bping\s+-n\s+(\d+)\b", r"ping -c \1", cmd)
            if re.search(r"\bcurl(?:\.exe)?\b", cmd, flags=re.I) and "https://" in cmd.lower():
                if not re.search(r"(?:^|\s)(?:-k|--insecure)\b", cmd):
                    cmd = re.sub(r"\b(curl(?:\.exe)?)\b", r"\1 -k", cmd, count=1, flags=re.I)

            exec_cmd: str | list[str] = cmd
            use_shell = True
            iso_mode_active = ""
            iso_allowed_ifaces: list[str] = []
            try:
                from Reasoning.engines.vault_bridge import _get_isolation_filter

                iso_mode_active, iso_allowed_ifaces = _get_isolation_filter()
            except Exception:
                pass

            if os.name == "nt" and not re.match(r"^(?:powershell|pwsh|cmd(?:\.exe)?)\b", cmd.strip(), flags=re.I) and (
                re.search(
                    r"\b(?:Get-[A-Za-z]+|Set-[A-Za-z]+|New-[A-Za-z]+|Remove-[A-Za-z]+|Test-[A-Za-z]+|Invoke-[A-Za-z]+|Restart-[A-Za-z]+|Disable-[A-Za-z]+|Enable-[A-Za-z]+|Start-[A-Za-z]+|Stop-[A-Za-z]+|Select-String|Select-Object|Where-Object|ForEach-Object|Out-String|Measure-Object)\b|\$[A-Za-z_]",
                    cmd.strip(),
                    flags=re.I,
                )
                or (";" in cmd and "&" not in cmd)
            ):
                ps_cmd = re.sub(r"\bcurl\b(?!\.exe)", "curl.exe", cmd)
                exec_cmd = ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd]
                use_shell = False
            elif os.name != "nt" and iso_mode_active == "white":
                # WHITE Mode (`-netiso white`): Execute command inside an unprivileged Linux network namespace
                # (`unshare -r -n`) with only loopback `lo` brought up, guaranteeing 100% kernel network isolation.
                exec_cmd = [
                    "unshare",
                    "-r",
                    "-n",
                    "bash",
                    "-c",
                    f"ip link set dev lo up 2>/dev/null || true; {cmd}",
                ]
                use_shell = False
            try:
                child_env = os.environ.copy()
                files_ws_dir = proj_ws / "Files"
                files_ws_dir.mkdir(parents=True, exist_ok=True)
                child_env["CORA_ACTIVE_PROJECT"] = proj_ws.name
                child_env["PROJECT_DIR"] = str(proj_ws)
                child_env["PROJECT_FILES_DIR"] = str(files_ws_dir)
                child_env["PROJECT_DOWNLOADS_DIR"] = str(proj_ws / "downloads")
                child_env["PROJECT_MEMORY_FILE"] = str(proj_ws / "memory.md")
                os_tools_dir = CORA_ROOT / "Tools" / ("Windows" if os.name == "nt" else "Linux")
                path_prefixes = [str(files_ws_dir)]
                if os_tools_dir.is_dir():
                    path_prefixes.append(str(os_tools_dir))
                child_env["PATH"] = os.pathsep.join(path_prefixes) + os.pathsep + child_env.get("PATH", "")
                popen_kwargs: dict = {
                    "shell": use_shell,
                    "cwd": os.getcwd(),
                    "env": child_env,
                    "text": True,
                    "encoding": "utf-8",
                    "errors": "replace",
                    "stdout": subprocess.PIPE,
                    "stderr": subprocess.PIPE,
                }
                if os.name != "nt":
                    popen_kwargs["start_new_session"] = True
                    if use_shell:
                        bash_bin = shutil.which("bash")
                        if bash_bin:
                            popen_kwargs["executable"] = bash_bin
                proc = subprocess.Popen(exec_cmd, **popen_kwargs)
                try:
                    out_s, err_s = proc.communicate(timeout=60)
                    ret_code = int(proc.returncode or 0)
                    output = (out_s or "") + (err_s or "")
                except subprocess.TimeoutExpired:
                    # Improvement #4: Kill entire process group on timeout so child processes (tio/nmap/curl) never orphan or lock /dev/ttyUSB0
                    if os.name != "nt":
                        try:
                            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                        except Exception:
                            try:
                                proc.kill()
                            except Exception:
                                pass
                    else:
                        try:
                            proc.kill()
                        except Exception:
                            pass
                    try:
                        part_out, part_err = proc.communicate(timeout=2)
                    except Exception:
                        part_out, part_err = "", ""
                    ret_code = 124
                    output = (
                        ((part_out or "") + (part_err or "")).strip()
                        + "\n[Command timed out after 60 seconds (exit code 124; process group terminated cleanly). Add explicit timeout flags (-c/-W/--connect-timeout) or pivot to L2/L3/OOB probe.]"
                    ).strip()
            except Exception as sub_exc:
                ret_code = 1
                output = f"Subprocess execution error: {sub_exc}"
            finally:
                if is_serial_cmd:
                    _LAST_SERIAL_IO_EPOCH = time.time()

            # BLUE Mode (`-netiso blue [ifaces]`): Filter interface/route/neighbor discovery outputs
            # so only `lo` and the allowed interfaces (`iso_allowed_ifaces`) are exposed to the LLM.
            if (
                os.name != "nt"
                and iso_mode_active == "blue"
                and iso_allowed_ifaces
                and output
                and re.search(r"\b(?:ip\s+(?:-[46brs]+\s+)*(?:addr|address|link|route|neigh)|ifconfig|arp\s+-)\b", cmd, re.I)
            ):
                allowed_set = set(iso_allowed_ifaces) | {"lo"}
                try:
                    from Reasoning.engines.cegar_verifier import _get_host_all_interface_subnets

                    all_host_ifaces = set(_get_host_all_interface_subnets().keys())
                except Exception:
                    all_host_ifaces = set()
                disallowed_ifaces = {i for i in all_host_ifaces if i not in allowed_set}
                if disallowed_ifaces:
                    filtered_lines = []
                    skip_block = False
                    for ln in output.splitlines():
                        # Handle multi-line `ip addr` / `ip link` blocks (`2: eth2: <BROADCAST...`)
                        m_blk = re.match(r"^\d+:\s+([a-zA-Z0-9_.\-]+?)(?:@[^\s:]+)?:\s+<", ln)
                        if m_blk:
                            if_name = m_blk.group(1)
                            skip_block = if_name in disallowed_ifaces or (if_name not in allowed_set)
                            if skip_block:
                                continue
                        elif skip_block and ln.startswith(" "):
                            continue
                        else:
                            skip_block = False
                        # Handle single-line `ip -br addr`, `ip route`, `ip neigh`
                        toks = re.findall(r"[a-zA-Z0-9_.\-]+", ln)
                        if any(t in disallowed_ifaces for t in toks):
                            continue
                        filtered_lines.append(ln)
                    output = "\n".join(filtered_lines)

            raw_output_was_empty = not output.strip()
            if raw_output_was_empty:
                output = f"(Command completed with exit code {ret_code})"

            serial_drop_or_empty = bool(
                is_serial_cmd
                and (
                    (raw_output_was_empty and "write(" in cmd.lower() and "--list" not in cmd.lower())
                    or re.search(
                        r"(?:disconnected|device or resource busy|resource temporarily unavailable|input/output error|cannot open /dev/tty)",
                        output,
                        re.I,
                    )
                )
            )
            if cegar_advisories and (ret_code != 0 or serial_drop_or_empty):
                output = "\n".join(cegar_advisories) + "\n" + output

            attempt_status = "OK" if (ret_code == 0 and not serial_drop_or_empty) else "FAIL"
            _record_attempt("run_shell_command", cmd, attempt_status, output)

            # Part 1 Context VM + Engine 9 (Temporal Fluents) + Engine 11 (CBR) + Engine 13 (SyGuS) + Engine 15/16/17/19 Continual & RL Updates
            try:
                from Reasoning.engines.context_vm import process_tool_output_zero_loss

                return process_tool_output_zero_loss("run_command", cmd, output, ret_code)
            except Exception:
                return compact_text(output, MAX_TOOL_OUTPUT_CHARS)

        elif name == "write_file":
            raw_path = (args.get("path") or "").strip()
            if not raw_path:
                return "Error: `path` argument is required for `write_file`."
            content = args.get("content", "")
            proj_ws = ensure_project_workspace()
            p = resolve_cli_project_file_path(raw_path, for_write=True)
            if p.exists() and p.is_dir():
                return f"Error: Cannot write file because `{p}` is an existing directory."
            print(f"\n\033[1;32m[Agent Tool -> write_file]\033[0m {p} ({len(content)} bytes)", flush=True)
            if not confirm_action(f"writing {len(content)} bytes to `{p}`"):
                print("  \033[1;31m-> Denied by user.\033[0m", flush=True)
                return f"Action denied by user: file {p} was not written."
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            try:
                if proj_ws in p.parents:
                    rel_to_proj = p.relative_to(proj_ws)
                    if str(rel_to_proj) != "memory.md":
                        update_project_memory_index(proj_ws, str(rel_to_proj), f"Created file ({len(content)} bytes)", ["artifact"])
            except Exception:
                pass
            _record_attempt("write_file", str(p), "OK", f"Wrote {len(content)} bytes")
            return f"Successfully wrote {len(content)} bytes to {p}"

        elif name == "edit_file":
            raw_path = (args.get("path") or "").strip()
            if not raw_path:
                return "Error: `path` argument is required for `edit_file`."
            old_text = args.get("old_text", "")
            new_text = args.get("new_text", "")
            p = resolve_cli_project_file_path(raw_path, for_write=False)
            print(f"\n\033[1;32m[Agent Tool -> edit_file]\033[0m {p}", flush=True)
            if not p.exists():
                return f"Error: File not found: {p}"
            if p.is_dir():
                return f"Error: `{p}` is a directory, not a file."
            if not confirm_action(f"editing `{p}`"):
                print("  \033[1;31m-> Denied by user.\033[0m", flush=True)
                return f"Action denied by user: file {p} was not modified."
            text = p.read_text(encoding="utf-8", errors="replace")
            if old_text not in text:
                return f"Error: old_text not found in {p}"
            p.write_text(text.replace(old_text, new_text, 1), encoding="utf-8")
            _record_attempt("edit_file", str(p), "OK", "Updated file")
            return f"Successfully updated {p}"

        elif name == "read_file":
            raw_path = (args.get("path") or "").strip()
            if not raw_path:
                return "Error: `path` argument is required for `read_file`."
            p = resolve_cli_project_file_path(raw_path, for_write=False)
            print(f"\n\033[1;36m[Agent Tool -> read_file]\033[0m {p}", flush=True)
            if not p.exists():
                _record_attempt("read_file", str(p), "FAIL", "File not found")
                return f"Error: File not found: {p}"
            if p.is_dir():
                _record_attempt("read_file", str(p), "FAIL", "Path is a directory")
                return f"Error: `{p}` is a directory; use `list_directory` instead."
            content = p.read_text(encoding="utf-8", errors="replace")
            _record_attempt("read_file", str(p), "OK", content[:160])
            return compact_text(content, MAX_TOOL_OUTPUT_CHARS)

        elif name == "list_directory":
            raw_path = (args.get("path") or ".").strip() or "."
            p = Path.cwd().resolve() if raw_path == "." else resolve_cli_project_file_path(raw_path, for_write=False)
            print(f"\n\033[1;36m[Agent Tool -> list_directory]\033[0m {p}", flush=True)
            if not p.exists():
                _record_attempt("list_directory", str(p), "FAIL", "Directory not found")
                return f"Error: Directory not found: {p}"
            if not p.is_dir():
                _record_attempt("list_directory", str(p), "FAIL", "Not a directory")
                return f"Error: `{p}` is a file, not a directory; use `read_file` instead."
            entries = sorted(os.listdir(p))
            formatted = []
            for e in entries[:200]:
                full = p / e
                try:
                    suffix = "/" if full.is_dir() else f" ({full.stat().st_size} B)"
                except OSError:
                    suffix = " (broken-link/unreadable)"
                formatted.append(f"{e}{suffix}")
            out_dir = "\n".join(formatted) if formatted else "(empty directory)"
            _record_attempt("list_directory", str(p), "OK", out_dir[:160])
            return out_dir

        elif name == "neuro_symbolic_reason":
            eng = args.get("engine", "pipeline")
            prob = args.get("problem", "Target analysis")
            print(
                f"\n\033[1;35m[Neuro-Symbolic Engine -> {eng}]\033[0m {prob} (CPU-only, auto-saving to ObsidianVault/reasoning/)",
                flush=True,
            )
            from Reasoning.reasoning_cli import execute_reasoning_tool

            report = execute_reasoning_tool(eng, args)
            _record_attempt("neuro_symbolic_reason", f"{eng}:{prob}", "OK", report)
            return compact_text(report, MAX_TOOL_OUTPUT_CHARS)

        elif name == "generate_project_report":
            proj_arg = (args.get("project_name") or "").strip() or ACTIVE_PROJECT
            focus_arg = (args.get("report_focus") or "").strip() or ACTIVE_GOAL
            print(
                f"\n\033[1;32m[Agent Tool -> generate_project_report]\033[0m Project=`{proj_arg or get_active_project_slug()}`",
                flush=True,
            )
            from Reasoning.report_generator import generate_project_report

            rep_res = generate_project_report(
                project_name=proj_arg,
                active_goal=ACTIVE_GOAL,
                attempt_ledger=ATTEMPT_LEDGER,
                report_focus=focus_arg,
                use_llm=True,
            )
            _record_attempt("generate_project_report", rep_res["project_slug"], "OK", rep_res["report_path"])
            return (
                f"Generated 5-Section Project Status & Findings Report:\n"
                f"- Markdown Report: `{rep_res['report_path']}`\n"
                f"- Dated Archive:   `{rep_res['dated_report_path']}`\n"
                f"- SVG Dashboard:   `{rep_res['svg_path']}`\n\n"
                f"{compact_text(rep_res['markdown'], MAX_TOOL_OUTPUT_CHARS)}"
            )

        else:
            return f"Error: Unknown tool '{name}'"
    except Exception as exc:
        err_msg = f"Tool execution error ({name}): {exc}"
        _record_attempt(name, str(args)[:120], "FAIL", err_msg)
        return err_msg


def sanitize_messages(messages: list) -> None:
    """
    Validate and repair message history so `llama-server` never fails JSON parsing
    or raises `Jinja Exception: No user query found in messages.` (HTTP 500).
    """
    cleaned = []
    idx = 0
    while idx < len(messages):
        m = messages[idx]
        if m.get("role") == "assistant" and m.get("tool_calls"):
            valid_tcs = []
            for tc in m["tool_calls"]:
                fn = tc.get("function") or {}
                raw_args = fn.get("arguments") or "{}"
                try:
                    parsed = json.loads(raw_args)
                    if not isinstance(parsed, dict):
                        parsed = {}
                except Exception:
                    parsed = {}
                fn["arguments"] = json.dumps(parsed)
                tc["function"] = fn
                valid_tcs.append(tc)
            m["tool_calls"] = valid_tcs
        if m.get("role") == "user":
            content_str = str(m.get("content") or "").strip()
            if not content_str:
                m["content"] = f"Active Goal: {ACTIVE_GOAL}" if ACTIVE_GOAL else "Continue analysis."
        cleaned.append(m)
        idx += 1

    # Qwen3/Qwen3.8 Jinja chat template strictly requires at least one `role == "user"` message
    # in `messages` or it throws HTTP 500: `Jinja Exception: No user query found in messages.`
    has_user_msg = any(
        m.get("role") == "user" and isinstance(m.get("content"), str) and m.get("content").strip()
        for m in cleaned
    )
    if not has_user_msg:
        fallback_user = {
            "role": "user",
            "content": (
                f"Continue working toward the active goal: {ACTIVE_GOAL}"
                if ACTIVE_GOAL
                else "Continue executing the task and synthesize findings."
            ),
        }
        insert_pos = 1 if (cleaned and cleaned[0].get("role") == "system") else 0
        cleaned.insert(insert_pos, fallback_user)

    messages[:] = cleaned


MAX_HISTORY_TOKENS = int(os.environ.get("MAX_HISTORY_TOKENS", "14000"))
_TOKENIZE_ENDPOINT_STATE = {"checked_ts": 0.0, "available": False}


def _estimate_message_tokens(msg: dict, allow_remote: bool = False) -> int:
    """
    Improvement #3: Exact Token-Budget Governor with per-message memoization.
    Uses a fast (< 0.05 ms) symbol/hex/JSON-density calibrated estimator by default during hot-path
    context trimming so `llama-server` is never blocked on synchronous HTTP `/tokenize` calls while generating.
    """
    content = str(msg.get("content") or "")
    tc_str = json.dumps(msg.get("tool_calls")) if msg.get("tool_calls") else ""
    raw_text = f"{content}\n{tc_str}" if tc_str else content
    cur_len = len(raw_text)
    if msg.get("_cached_content_len") == cur_len and isinstance(msg.get("_cached_tokens"), int):
        return int(msg["_cached_tokens"])

    tok_count = 0
    if allow_remote:
        now = time.monotonic()
        if (now - float(_TOKENIZE_ENDPOINT_STATE["checked_ts"])) > 15.0:
            _TOKENIZE_ENDPOINT_STATE["checked_ts"] = now
            try:
                tok_url = API_URL.split("/v1/")[0].rstrip("/") + "/tokenize"
                req = urllib.request.Request(
                    tok_url,
                    data=json.dumps({"content": "ping"}).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=0.15) as resp:
                    _TOKENIZE_ENDPOINT_STATE["available"] = resp.status == 200
            except Exception:
                _TOKENIZE_ENDPOINT_STATE["available"] = False

        if _TOKENIZE_ENDPOINT_STATE["available"] and cur_len > 0:
            try:
                tok_url = API_URL.split("/v1/")[0].rstrip("/") + "/tokenize"
                req = urllib.request.Request(
                    tok_url,
                    data=json.dumps({"content": raw_text}).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=0.20) as resp:
                    data = json.loads(resp.read().decode("utf-8", errors="replace"))
                    if isinstance(data, dict) and isinstance(data.get("tokens"), list):
                        tok_count = len(data["tokens"]) + 6
            except Exception:
                _TOKENIZE_ENDPOINT_STATE["available"] = False

    if tok_count <= 0:
        # Density-aware fallback: JSON/hex/tables/punctuation tokenize at ~2.2 chars/tok; prose at ~3.5 chars/tok
        punct_and_digits = sum(1 for ch in raw_text if not ch.isalpha() and not ch.isspace())
        density_ratio = punct_and_digits / max(1, cur_len)
        chars_per_tok = 2.2 if density_ratio > 0.28 else 3.5
        tok_count = int(cur_len / chars_per_tok) + 6

    msg["_cached_content_len"] = cur_len
    msg["_cached_tokens"] = tok_count
    return tok_count


def _total_conversation_tokens(messages: list) -> int:
    return sum(_estimate_message_tokens(m) for m in messages if isinstance(m, dict))


def trim_messages_to_fit(
    messages: list,
    max_chars: int = MAX_HISTORY_CHARS,
    max_tokens: int = MAX_HISTORY_TOKENS,
) -> None:
    """
    Zero-Loss Context Virtual Memory (Part 1 & Guardrail 3 + Improvement #3 Token Budget Governor):
    - Keeps `messages[0]["content"]` static across turns so `llama-server` preserves 100% KV-cache hits
      on the system prompt prefix (only rebuilding `messages[0]` if it's empty).
    - Archives any older tool outputs > 2,500 chars losslessly to `Reasoning/data/shadow_archive/`
      before compacting them in-context.
    - Enforces BOTH character (`max_chars`) and exact/density-calibrated token (`max_tokens`) budgets.
    - NEVER pops the last remaining `role == "user"` message (prevents Qwen Jinja HTTP 500
      `No user query found in messages` during deep multi-step tool chains).
    """
    sanitize_messages(messages)
    if messages and messages[0].get("role") == "system" and not messages[0].get("content"):
        messages[0]["content"] = build_system_prompt()

    for m in messages[1:-2]:
        if m.get("role") == "tool" and isinstance(m.get("content"), str) and len(m["content"]) > 2500:
            try:
                from Reasoning.engines.context_vm import archive_to_shadow_store

                shadow_path = archive_to_shadow_store(m.get("name", "tool_output"), m["content"])
                m["content"] = (
                    compact_text(m["content"], 1400)
                    + f"\n[Full lossless raw output archived at `{shadow_path}`]"
                )
            except Exception:
                m["content"] = compact_text(m["content"], 1400)

    # Phase 1: Drop older turns BEFORE the last `role == "user"` message first when either char or token budget is exceeded
    while len(messages) > 3 and (
        len(json.dumps(messages)) > max_chars or _total_conversation_tokens(messages) > max_tokens
    ):
        user_indices = [i for i, m in enumerate(messages) if m.get("role") == "user"]
        last_user_idx = user_indices[-1] if user_indices else -1
        if last_user_idx > 1:
            # Safe to pop messages[1] because there is a newer `user` message at `last_user_idx`
            messages.pop(1)
            while len(messages) > 2 and messages[1].get("role") == "tool":
                messages.pop(1)
        else:
            # The ONLY `user` message is at index 1 (or 0). NEVER pop it!
            # Instead, pop the oldest `(assistant, tool...)` step AFTER the user message (at index 2).
            if len(messages) > 4:
                messages.pop(2)
                while len(messages) > 3 and messages[2].get("role") == "tool":
                    messages.pop(2)
            else:
                # Compact remaining large tool/user contents in-place if only [system, user, assistant, tool] remain
                for m in messages[1:]:
                    if isinstance(m.get("content"), str) and len(m["content"]) > 1800:
                        m["content"] = compact_text(m["content"], 1400)
                break

    sanitize_messages(messages)


def _ensure_llama_server_running() -> bool:
    """If llama-server on 127.0.0.1:8080 is down (Connection refused) or loading (503), auto-start/wait for /health."""
    health_url = API_URL.split("/v1/")[0].rstrip("/") + "/health"
    already_loading = False
    try:
        with urllib.request.urlopen(health_url, timeout=1.5) as r:
            if r.status == 200:
                return True
    except urllib.error.HTTPError as he:
        if he.code == 503:
            already_loading = True
    except Exception:
        pass

    if not already_loading:
        m_up = MODEL_NAME.upper()
        if "TURBO" in m_up and "Q8" in m_up:
            model_flag = "turbo-q8"
        elif "TURBO" in m_up and "Q6" in m_up:
            model_flag = "turbo-q6"
        elif "TURBO" in m_up:
            model_flag = "turbo"
        elif "3.5" in m_up or "9B" in m_up:
            model_flag = "3.5"
        else:
            model_flag = "3.8"
        manage_ps1 = CORA_ROOT / "run_cora_WIN.ps1"
        manage_sh = CORA_ROOT / "run_cora_NIX.sh"

        if os.name == "nt" and manage_ps1.is_file():
            start_cmd = [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(manage_ps1),
                "start",
                "-m",
                model_flag,
                "--no-browser",
            ]
        elif manage_sh.is_file():
            start_cmd = ["bash", str(manage_sh), "start", "-m", model_flag, "--no-browser"]
        else:
            return False

        print(
            f"\n\033[1;33m[Auto-Recovery] `llama-server` is not listening on 127.0.0.1:8080 — starting model `{model_flag}` automatically...\033[0m",
            flush=True,
        )
        child_env = os.environ.copy()
        child_env["CORA_ACTIVE_PROJECT"] = child_env.get("CORA_ACTIVE_PROJECT") or ACTIVE_PROJECT or ""
        child_env["CORA_NON_INTERACTIVE"] = "1"
        try:
            subprocess.run(
                start_cmd,
                cwd=str(BASE_DIR),
                env=child_env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60,
            )
        except Exception:
            pass
    else:
        print(
            "\n\033[1;33m[Auto-Recovery] `llama-server` is loading model weights into VRAM/RAM — waiting for readiness...\033[0m",
            flush=True,
        )

    for _ in range(60):
        try:
            with urllib.request.urlopen(health_url, timeout=1.5) as r:
                if r.status == 200:
                    print("\033[1;32m[Auto-Recovery] `llama-server` is now ONLINE and ready.\033[0m", flush=True)
                    return True
        except Exception:
            time.sleep(1.0)
    return False


def _build_wire_messages_with_personality_prefix(messages: list) -> list[dict]:
    """
    Prepare clean OpenAI-format messages for `llama-server` and inject the active session
    personality mode's pre-emptive directive (`BERSERKER`, `NINJA`, or `ANALYST`) into the latest
    `user` message turn. When `ACTIVE_PERSONALITY_MODE == "DEFAULT"`, no directive is injected.
    """
    wire_msgs: list[dict] = []
    for m in messages:
        if not isinstance(m, dict):
            continue
        clean_m = {k: v for k, v in m.items() if not str(k).startswith("_cached_")}
        wire_msgs.append(clean_m)

    prefix = get_personality_mode_preemptive_turn_prefix()
    if prefix:
        for idx in range(len(wire_msgs) - 1, -1, -1):
            if wire_msgs[idx].get("role") == "user" and isinstance(wire_msgs[idx].get("content"), str):
                cur_c = wire_msgs[idx]["content"]
                if not cur_c.startswith("[PRE-EMPTIVE "):
                    wire_msgs[idx] = {**wire_msgs[idx], "content": f"{prefix}{cur_c}"}
                break
    return wire_msgs


LAST_THINKING_TRACE: str = ""
SHOW_THINKING_EXPANDED_CLI: bool = False


def print_last_thinking_trace_cli() -> None:
    """Display or toggle the last captured LLM <think> thought process & engine trace (Ctrl+O)."""
    global SHOW_THINKING_EXPANDED_CLI
    SHOW_THINKING_EXPANDED_CLI = not SHOW_THINKING_EXPANDED_CLI
    state_lbl = "EXPANDED (ON)" if SHOW_THINKING_EXPANDED_CLI else "HIDDEN by default (OFF)"
    if LAST_THINKING_TRACE.strip():
        print(
            f"\n\033[1;33m=== 🧠 C.O.R.A. Thought Process & Internal Reasoning Trace (Ctrl+O: {state_lbl}) ===\033[0m\n"
            f"\033[0;37m{LAST_THINKING_TRACE.strip()}\033[0m\n"
            "\033[1;33m====================================================================================\033[0m\n",
            flush=True,
        )
    else:
        print(
            f"\n\033[1;33m[🧠 Thought Process (Ctrl+O)]\033[0m Live thought auto-expansion toggled to `{state_lbl}` "
            "(No `<think>` trace recorded yet in this session).\n",
            flush=True,
        )


def chat_step(messages: list) -> dict:
    global LAST_THINKING_TRACE, SHOW_THINKING_EXPANDED_CLI
    trim_messages_to_fit(messages)
    wire_messages = _build_wire_messages_with_personality_prefix(messages)

    payload = {
        "model": MODEL_NAME,
        "messages": wire_messages,
        "tools": TOOLS,
        "tool_choice": "auto",
        "stream": True,
        "temperature": 0.6,
        "max_tokens": 2048,
        "repeat_penalty": 1.0,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    content_parts: list[str] = []
    tool_calls_by_index: dict = {}
    printed_header = False
    printed_Visible_len = 0
    in_think_block = False
    think_start_t = time.monotonic()

    spinner_stop = threading.Event()
    spinner_lock = HUD._lock
    spinner_active = [True]

    def _clear_spinner_locked() -> None:
        if spinner_active[0]:
            spinner_active[0] = False
            spinner_stop.set()
            with _raw_terminal_output():
                sys.stdout.write("\r\033[2K")
                sys.stdout.flush()

    def _wait_spinner() -> None:
        frames = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
        t0 = time.monotonic()
        idx = 0
        while not spinner_stop.wait(0.25):
            with spinner_lock, _raw_terminal_output():
                if not spinner_active[0]:
                    break
                elapsed = time.monotonic() - t0
                frame = frames[idx % len(frames)]
                idx += 1
                max_c = max(24, shutil.get_terminal_size((80, 24)).columns - 2)
                msg_sp = f"{frame} [C.O.R.A. Thinking / Processing... {elapsed:.1f}s | Press Ctrl+O to expand thought process | Ctrl+C to cancel]"
                sys.stdout.write(f"\r\033[2K\033[0;36m{msg_sp[:max_c]}\033[0m")
                sys.stdout.flush()

    spinner_thread = threading.Thread(target=_wait_spinner, daemon=True)
    spinner_thread.start()

    try:
        try:
            resp_ctx = urllib.request.urlopen(req, timeout=300)
        except urllib.error.HTTPError as err:
            with spinner_lock:
                _clear_spinner_locked()
            body = err.read().decode("utf-8", errors="replace")
            if err.code == 503 or "loading model" in body.lower():
                if _ensure_llama_server_running():
                    req = urllib.request.Request(
                        API_URL,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    resp_ctx = urllib.request.urlopen(req, timeout=300)
                else:
                    raise urllib.error.HTTPError(err.url, err.code, body, err.headers, None)
            elif ("exceeds the available context size" in body and len(messages) > 3) or (
                "No user query found in messages" in body
            ):
                print("\n\033[1;33m[Auto-Compacting & Healing Context Window and Retrying...]\033[0m", flush=True)
                sanitize_messages(messages)
                trim_messages_to_fit(messages, max_chars=MAX_HISTORY_CHARS // 2)
                retry_wire = _build_wire_messages_with_personality_prefix(messages)
                req = urllib.request.Request(
                    API_URL,
                    data=json.dumps({**payload, "messages": retry_wire}).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                resp_ctx = urllib.request.urlopen(req, timeout=300)
            else:
                raise urllib.error.HTTPError(err.url, err.code, body, err.headers, None)
        except urllib.error.URLError:
            with spinner_lock:
                _clear_spinner_locked()
            if _ensure_llama_server_running():
                req = urllib.request.Request(
                    API_URL,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                resp_ctx = urllib.request.urlopen(req, timeout=300)
            else:
                raise

        with resp_ctx as resp:
            for raw_line in resp:
                # Check if user pressed Ctrl+O (\x0f) during streaming on Windows TTY
                if os.name == "nt":
                    try:
                        import msvcrt

                        while msvcrt.kbhit():
                            k_ch = msvcrt.getwch()
                            if k_ch == "\x0f":  # Ctrl+O
                                SHOW_THINKING_EXPANDED_CLI = not SHOW_THINKING_EXPANDED_CLI
                    except Exception:
                        pass

                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                choices = chunk.get("choices") or []
                if not choices:
                    continue
                delta = choices[0].get("delta") or {}

                c = delta.get("content")
                if c:
                    content_parts.append(c)
                    full_so_far = "".join(content_parts)
                    if "<think>" in full_so_far and "</think>" not in full_so_far:
                        in_think_block = True
                        with spinner_lock:
                            _clear_spinner_locked()
                            think_elapsed = time.monotonic() - think_start_t
                            if SHOW_THINKING_EXPANDED_CLI:
                                if not printed_header:
                                    print(f"\n\033[1;33m[🧠 Thought Process (Ctrl+O Expanded)]>\033[0m ", end="", flush=True)
                                    printed_header = True
                                print(f"\033[2;37m{c}\033[0m", end="", flush=True)
                            else:
                                with _raw_terminal_output():
                                    max_c = max(24, shutil.get_terminal_size((80, 24)).columns - 3)
                                    th_msg = f"🧠 [C.O.R.A. Thinking & Processing... ({think_elapsed:.1f}s) — Press Ctrl+O to expand thought process]"
                                    sys.stdout.write(f"\r\033[2K\033[1;33m{th_msg[:max_c]}\033[0m")
                                    sys.stdout.flush()
                        continue

                    if in_think_block and "</think>" in full_so_far:
                        in_think_block = False
                        m_th = re.search(r"<think>([\s\S]*?)</think>", full_so_far, flags=re.I)
                        if m_th:
                            LAST_THINKING_TRACE = m_th.group(1).strip()
                        think_elapsed = time.monotonic() - think_start_t
                        with spinner_lock:
                            with _raw_terminal_output():
                                sys.stdout.write("\r\033[2K")
                            print(
                                f"\n\033[2;33m[🧠 Thought for {think_elapsed:.1f}s — Press Ctrl+O (or type /ctrl-o) to expand thought process]\033[0m",
                                flush=True,
                            )
                            printed_header = False

                    visible_full = re.sub(r"<think>[\s\S]*?</think>", "", full_so_far, flags=re.I).lstrip("\r\n")
                    if len(visible_full) > printed_Visible_len:
                        new_vis = visible_full[printed_Visible_len:]
                        printed_Visible_len = len(visible_full)
                        with spinner_lock:
                            _clear_spinner_locked()
                            if not printed_header:
                                print(f"\n\033[1;32m🤖 C.O.R.A. ({MODEL_NAME})>\033[0m ", end="", flush=True)
                                printed_header = True
                            print(new_vis, end="", flush=True)

                for tc in delta.get("tool_calls") or []:
                    with spinner_lock:
                        _clear_spinner_locked()
                    idx = tc.get("index", 0)
                    entry = tool_calls_by_index.setdefault(
                        idx,
                        {
                            "id": tc.get("id") or f"call_{idx}",
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        },
                    )
                    if tc.get("id"):
                        entry["id"] = tc["id"]
                    fn = tc.get("function") or {}
                    if fn.get("name"):
                        entry["function"]["name"] += fn["name"]
                    if fn.get("arguments"):
                        entry["function"]["arguments"] += fn["arguments"]
    finally:
        with spinner_lock:
            _clear_spinner_locked()
        spinner_stop.set()
        spinner_thread.join(timeout=0.5)

    if printed_header:
        print("", flush=True)

    raw_joined = "".join(content_parts)
    m_final_th = re.search(r"<think>([\s\S]*?)</think>", raw_joined, flags=re.I)
    if m_final_th:
        LAST_THINKING_TRACE = m_final_th.group(1).strip()
    clean_joined = re.sub(r"<think>[\s\S]*?</think>", "", raw_joined, flags=re.I).strip()

    msg = {"role": "assistant", "content": clean_joined or raw_joined or None}
    if tool_calls_by_index:
        msg["tool_calls"] = [tool_calls_by_index[k] for k in sorted(tool_calls_by_index)]
    return msg


def _heal_truncated_ips_in_args(args: dict, messages: list) -> None:
    """
    If the user's recent messages or active goal/project contain full 4-octet IPv4 addresses
    and a tool call argument ends with a truncated prefix of that IP (e.g. `http://198.51`,
    `http://198.5`, `198.1`, or `ip route get 192.`), automatically restore the full IPv4 address.
    Never modifies shell file-descriptor redirections (e.g., `2>&1`, `1>&2`) or bare integers/flags.
    """
    user_text = "\n".join(
        str(m.get("content") or "") for m in reversed(messages) if m.get("role") == "user"
    )
    if ACTIVE_GOAL:
        user_text = f"{ACTIVE_GOAL}\n{user_text}"
    known_ips = []
    for m_ip in re.finditer(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", user_text):
        ip_s = m_ip.group(1)
        if (
            ip_s not in ("0.0.0.0", "127.0.0.1", "255.255.255.255")
            and all(int(o) <= 255 for o in ip_s.split("."))
            and ip_s not in known_ips
        ):
            known_ips.append(ip_s)
    if not known_ips:
        return

    for k, val in list(args.items()):
        if not isinstance(val, str) or not val.strip():
            continue
        s_val = val.strip()
        # Never touch commands ending in shell redirections (`2>&1`, `1>&2`, `>&1`, `>&2`)
        if re.search(r"[0-9]*>&[0-9]+\s*$", s_val):
            continue
        for full_ip in known_ips:
            m_tail = re.search(
                r"(https?://|ip\s+route\s+get\s+|ip\s+neigh\s+show\s+|ping\s+(?:-[cWwn]\s+\d+\s+)*|(?<![>&0-9.\-/])\b)([0-9]+(?:\.[0-9]*)*)$",
                s_val,
            )
            if m_tail:
                prefix_ctx, partial_num = m_tail.group(1), m_tail.group(2)
                # Require at least one dot (`.`) unless preceded by an explicit URL/IP command prefix
                if not prefix_ctx and "." not in partial_num:
                    continue
                if (
                    partial_num != full_ip
                    and full_ip.startswith(partial_num)
                    and len([p for p in partial_num.split(".") if p]) < 4
                ):
                    healed = s_val[: -len(partial_num)] + full_ip
                    print(
                        f"\n\033[1;33m[CEGAR Auto-Healed Truncated IP]\033[0m Restored `{partial_num}` -> `{full_ip}` in `{k}`",
                        flush=True,
                    )
                    args[k] = healed
                    break


def run_turn(messages: list, max_steps: int = 14) -> str:
    """
    Execute a single multi-step tool-calling turn.
    Always performs a final synthesis `chat_step()` if the tool loop reaches `max_steps`
    so the LLM never stops silently after a tool call without supplying output.
    Returns the final assistant text content produced during the turn.
    """
    turn_start_len = len(messages)
    last_text = ""
    HUD.pause_stream()
    try:
        for step_idx in range(max_steps):
            assistant_msg = chat_step(messages)
            messages.append(assistant_msg)
            if assistant_msg.get("content"):
                last_text = str(assistant_msg["content"])
            tool_calls = assistant_msg.get("tool_calls")
            if not tool_calls:
                break
            for tc in tool_calls:
                fn_name = tc["function"]["name"]
                raw_args = tc["function"]["arguments"] or "{}"
                try:
                    args = json.loads(raw_args)
                    if not isinstance(args, dict):
                        args = {}
                except json.JSONDecodeError:
                    args = {}
                _heal_truncated_ips_in_args(args, messages)
                # Always normalize stored arguments to valid JSON so subsequent turns never 500
                tc["function"]["arguments"] = json.dumps(args)
                result = execute_tool(fn_name, args)
                if fn_name == "project_tracker" and messages and messages[0].get("role") == "system":
                    messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "name": fn_name,
                        "content": result,
                    }
                )
            # If we hit the step limit right after executing tool(s), force a synthesis step so the user gets output
            if step_idx == max_steps - 1:
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "[System Note] Summarize the results of the tools just executed and state whether "
                            "the goal is achieved (`[GOAL_ACHIEVED: <proof>]`) or what next method should be tried."
                        ),
                    }
                )
                final_msg = chat_step(messages)
                messages.append(final_msg)
                if final_msg.get("content"):
                    last_text = str(final_msg["content"])
    except KeyboardInterrupt:
        # Clean up any incomplete assistant tool_calls so the next turn doesn't fail validation
        while len(messages) > 1 and messages[-1].get("role") == "tool":
            messages.pop()
        if len(messages) > 1 and messages[-1].get("role") == "assistant" and messages[-1].get("tool_calls"):
            messages.pop()
        print("\n\033[1;33m[Interrupted by Ctrl+C — stopped current task. Ready for next prompt.]\033[0m")
        raise
    except Exception:
        # Roll back corrupted messages from a failed turn so the session stays healthy
        del messages[turn_start_len:]
        raise
    finally:
        HUD.resume_stream()
        save_current_cli_session(messages)
    return last_text


def _build_vault_and_attempt_summary_for_relentless(goal_text: str) -> tuple[str, list[str], list[str]]:
    """
    Build a concise digest of:
      1. What has ALREADY been attempted in `ATTEMPT_LEDGER` (failed vs succeeded commands/tools),
      2. Which capability vectors remain UNTRIED,
      3. Relevant notes in `ObsidianVault/` (projects, targets, playbooks, reasoning).
    """
    tried_vectors = sorted({a.get("layer", "") for a in ATTEMPT_LEDGER if a.get("layer")})
    untried_vectors = [v for v in ALL_CAPABILITY_VECTORS if v not in tried_vectors]

    failed_cmds = []
    ok_cmds = []
    for a in ATTEMPT_LEDGER[-24:]:
        entry_str = f"`{a['tool']}({a['target_or_cmd'][:90]})` -> {a['status']}: {a['summary'][:90]}"
        if a["status"] in ("FAIL", "BLOCKED"):
            if entry_str not in failed_cmds:
                failed_cmds.append(entry_str)
        else:
            if entry_str not in ok_cmds:
                ok_cmds.append(entry_str)

    vault_hits = ""
    try:
        vault_hits = compact_text(search_vault(goal_text[:80]), 1200)
    except Exception:
        pass

    proj_snippet = ""
    if ACTIVE_PROJECT:
        try:
            proj_snippet = compact_text(read_vault_note(f"projects/{ACTIVE_PROJECT}"), 1200)
        except Exception:
            pass

    lines = [
        f"=== RELENTLESS CONTROLLER AUDIT (Goal: `{goal_text}`) ===",
        f"- Active Project: `{ACTIVE_PROJECT or 'None'}`",
        f"- Total Tool Attempts So Far: `{len(ATTEMPT_LEDGER)}`",
        f"- Capability Vectors Already Tried: `{', '.join(tried_vectors) if tried_vectors else 'None'}`",
        f"- UNTRIED Capability Vectors Remaining: `{', '.join(untried_vectors) if untried_vectors else 'All base vectors probed — combine multi-step chains or new parameters'}`",
    ]
    if failed_cmds:
        lines.append("\n[FAILED / BLOCKED ATTEMPTS — DO NOT REPEAT THESE EXACT COMMANDS]:")
        for fc in failed_cmds[-10:]:
            lines.append(f"  - {fc}")
    if ok_cmds:
        lines.append("\n[SUCCEEDED TOOL CALLS & GATHERED INTEL]:")
        for oc in ok_cmds[-8:]:
            lines.append(f"  - {oc}")
    if proj_snippet:
        lines.append(f"\n[ACTIVE OBSIDIAN PROJECT NOTE (`[[projects/{ACTIVE_PROJECT}]]`)]:\n{proj_snippet}")
    if vault_hits:
        lines.append(f"\n[RELEVANT OBSIDIAN VAULT NOTES & PLAYBOOKS]:\n{vault_hits}")

    return "\n".join(lines), tried_vectors, untried_vectors


def _parse_goal_and_relentless_args(
    raw_text: str, switch_name: str = "relentless"
) -> tuple[str, int | None, str, str]:
    """
    Parse `/goal` and `/relentless` arguments with strict quote & dash-parameter isolation:
      1. Any new goal text MUST be enclosed in quotation marks (`"..."` or `'...'`) so words inside the
         goal (such as `"max"`, `"status"`, `"off"`) are never confused with switch parameters.
      2. All parameterized options MUST begin with a leading dash `-` and use a colon `:` (`-max:<#>`,
         `-max:0`, `-max:unlimited`, `-mode:<value>`).
    Returns `(quoted_goal, parsed_max_waves_or_None, subcommand_mode, error_message)`:
      - `parsed_max_waves == 0` -> UNLIMITED / NEVER STOP (`∞` waves)
      - `parsed_max_waves >= 1` -> Finite wave limit (`1..N` waves)
    """
    s = (raw_text or "").strip()
    if not s:
        return "", None, "", ""

    quoted_goals: list[str] = []

    def _extract_quote(m: re.Match) -> str:
        q_val = m.group(1) if m.group(1) is not None else m.group(2)
        quoted_goals.append((q_val or "").replace('\\"', '"').replace("\\'", "'").strip())
        return " "

    remainder = re.sub(r'"((?:\\"|[^"])*)"|\'((?:\\\'|[^\'])*)\'', _extract_quote, s).strip()

    # Check for unclosed quotation marks
    if ('"' in remainder) or ("'" in remainder and not re.search(r"\w'\w", remainder)):
        return (
            "",
            None,
            "",
            f'Unclosed quotation mark detected. Enclose the entire goal in quotes — e.g. `/{switch_name} "You must try to the max and never stop" -max:100`.',
        )

    if len(quoted_goals) > 1:
        return (
            "",
            None,
            "",
            f'Multiple quoted strings detected. Enclose your single goal in quotation marks — e.g. `/{switch_name} "You must try to the max and never stop" -max:100`.',
        )

    if len(quoted_goals) == 1 and not quoted_goals[0]:
        return (
            "",
            None,
            "",
            f'Goal inside quotation marks cannot be empty — e.g. `/{switch_name} "You must try to the max and never stop" -max:100`.',
        )

    quoted_goal = quoted_goals[0] if quoted_goals else ""
    parsed_max: int | None = None
    subcommand_mode = ""

    # Check for space-separated `-max <#>` or `max <#>` (where value is numeric/unlimited or `-max` has a dash)
    m_space_max = re.search(
        r"(?:^|\s)(-max\s+\S+|max\s+(?:\d+|unlimited|inf|infinite|never|nonstop))(?=\s|$)",
        remainder,
        flags=re.I,
    )
    if m_space_max:
        val_tok = m_space_max.group(1).split(None, 1)[1].strip()
        return (
            "",
            None,
            "",
            f'Parameters require a leading dash `-` and colon `:` (`-max:<#>`) — e.g. `/{switch_name} "Your goal" -max:{val_tok}` (use `-max:0` for unlimited / never stop).',
        )

    m_space_mode = re.search(
        r"(?:^|\s)(-mode\s+\S+|mode\s+(?:on|off|status|list|audit|ledger|clear))(?=\s|$)",
        remainder,
        flags=re.I,
    )
    if m_space_mode:
        val_tok = m_space_mode.group(1).split(None, 1)[1].strip()
        return (
            "",
            None,
            "",
            f"Parameters require a leading dash `-` and colon `:` (`-mode:<value>`) — e.g. `/{switch_name} -mode:{val_tok}`.",
        )

    allowed_goal_subcommands = {
        "status",
        "last",
        "latest",
        "current",
        "list",
        "all",
        "history",
        "audit",
        "ledger",
        "clear",
        "off",
        "reset",
        "none",
    }
    allowed_relentless_subcommands = {
        "on",
        "run",
        "start",
        "go",
        "resume",
        "off",
        "stop",
        "status",
        "audit",
        "ledger",
    }
    allowed_subcommands = (
        allowed_goal_subcommands if switch_name == "goal" else allowed_relentless_subcommands
    )

    unrecognized_tokens: list[str] = []
    for tok in remainder.split():
        t_low = tok.lower()
        if t_low.startswith("-max:") or t_low.startswith("--max:"):
            val = tok.split(":", 1)[1].strip().lower()
            if val in ("0", "unlimited", "inf", "infinite", "never", "nonstop"):
                parsed_max = 0
            elif val.isdigit() and int(val) >= 1:
                parsed_max = int(val)
            else:
                return (
                    "",
                    None,
                    "",
                    f"Invalid `{tok}` parameter. Use `-max:<#>` where `<#>` is `0` / `unlimited` (never stop) or a positive integer (e.g. `-max:15`, `-max:100`).",
                )
        elif t_low.startswith("max:"):
            val = tok.split(":", 1)[1].strip()
            return (
                "",
                None,
                "",
                f'Parameters must be preceded by a dash `-` — use `-max:{val}` instead of `{tok}` (e.g. `/{switch_name} "You must try to the max and never stop" -max:{val}`).',
            )
        elif t_low.startswith("-mode:") or t_low.startswith("--mode:"):
            m_val = tok.split(":", 1)[1].strip().lower()
            if m_val in allowed_subcommands:
                subcommand_mode = m_val
            else:
                return (
                    "",
                    None,
                    "",
                    f"Unknown `-mode:{m_val}` for `/{switch_name}`. Run `/{switch_name} -h` to see valid options.",
                )
        elif t_low.startswith("mode:"):
            m_val = tok.split(":", 1)[1].strip()
            return (
                "",
                None,
                "",
                f"Parameters must be preceded by a dash `-` — use `-mode:{m_val}` instead of `{tok}`.",
            )
        elif not quoted_goal and t_low in allowed_subcommands and not subcommand_mode:
            subcommand_mode = t_low
        elif t_low.startswith("-") and ":" in t_low:
            return (
                "",
                None,
                "",
                f"Unknown parameter `{tok}` for `/{switch_name}`. Supported parameters: `-max:<#>` (or `-max:0` for unlimited) and `-mode:<option>`. Run `/{switch_name} -h` for help.",
            )
        elif ":" in t_low and not t_low.startswith("-"):
            return (
                "",
                None,
                "",
                f"Parameters must be preceded by a dash `-` (e.g. `-{tok}`). If `{tok}` is part of your goal, enclose the goal in quotation marks (`\"...\"`).",
            )
        else:
            unrecognized_tokens.append(tok)

    if unrecognized_tokens:
        sample_goal = remainder if not quoted_goal else f"{quoted_goal} {' '.join(unrecognized_tokens)}"
        sample_goal = re.sub(r"\s+-?max:\S+", "", sample_goal, flags=re.I).strip() or "You must try to the max and never stop"
        max_suffix = f" -max:{parsed_max}" if parsed_max is not None else " -max:100"
        return (
            "",
            None,
            "",
            f'When setting a goal, the goal text MUST be enclosed in quotation marks (`"..."`) so words inside the goal are never confused with parameters, and parameters must start with `-`.\n'
            f'  Example: `/{switch_name} "{sample_goal}"{max_suffix}`',
        )

    return quoted_goal, parsed_max, subcommand_mode, ""


def _format_max_waves_label(waves_limit: int | None = None) -> str:
    w = MAX_RELENTLESS_WAVES if waves_limit is None else waves_limit
    return "0 (UNLIMITED / NEVER STOP)" if w == 0 else f"{w} waves"


def run_relentless_loop(messages: list, max_waves: int | None = None) -> None:
    """
    Autonomous Multi-Wave `/relentless` Execution Loop:
    Keeps driving the LLM back to `ACTIVE_GOAL`, checking `ObsidianVault/` and `ATTEMPT_LEDGER`
    for what has already been attempted, invoking the 14-Engine Neuro-Symbolic & Evolutionary
    MAP-Elites Pipeline for fresh strategies, and forcing the LLM to try untried tools and methods
    until `[GOAL_ACHIEVED: <concrete proof>]` or true exhaustion (`[EXHAUSTED_ALL_METHODS]`).
    When `max_waves == 0` (`max:0` / `max:unlimited`), the loop runs with NO wave limit and never stops
    until `[GOAL_ACHIEVED]` with verified tool proof or user `Ctrl+C`.
    """
    global CURRENT_WAVE, ACTIVE_GOAL
    waves_limit = MAX_RELENTLESS_WAVES if max_waves is None else max_waves
    is_unlimited = waves_limit == 0
    limit_disp = "∞ (UNLIMITED — never stop)" if is_unlimited else str(waves_limit)

    # If no explicit `/goal` was set yet, check project `goals.md` first, then promote the most recent user message
    if not ACTIVE_GOAL:
        ACTIVE_GOAL = get_last_project_goal()
    if not ACTIVE_GOAL:
        for m in reversed(messages):
            if m.get("role") == "user" and m.get("content"):
                txt = str(m["content"]).strip()
                if not txt.startswith("[System Note]") and not txt.startswith("=== RELENTLESS"):
                    ACTIVE_GOAL = txt[:240]
                    break
    if not ACTIVE_GOAL:
        print(
            '\n\033[1;33m[Relentless Mode]\033[0m Set a goal first with `/goal "<your objective>"` or `/relentless "<your objective>" [-max:<#>]`.\n'
        )
        return

    append_project_goal(ACTIVE_GOAL)
    HUD.render(force_region=False)
    vault_goal_ref = _sync_goal_and_attempts_to_vault()
    print(
        f"\n\033[1;35m==============================================================================\033[0m\n"
        f"\033[1;35m  RELENTLESS AUTONOMOUS LOOP ENGAGED (`Wave 1..{limit_disp}` | Press Ctrl+C to pause)\033[0m\n"
        f"  \033[1;33mActive Goal:\033[0m   {ACTIVE_GOAL}\n"
        f"  \033[1;36mWave Limit:\033[0m    `{_format_max_waves_label(waves_limit)}`\n"
        f"  \033[1;36mVault Ledger:\033[0m  [[{vault_goal_ref}]] (auto-updated on every tool call)\n"
        f"\033[1;35m==============================================================================\033[0m\n",
        flush=True,
    )

    try:
        wave_num = 0
        while True:
            wave_num += 1
            if not is_unlimited and wave_num > waves_limit:
                print(
                    f"\n\033[1;33m[Relentless Mode] Reached wave limit ({waves_limit} waves, {len(ATTEMPT_LEDGER)} tool attempts logged). "
                    f"Type `/relentless` to run another {waves_limit} waves, `/relentless -max:30` to increase the wave limit, or `/relentless -max:0` for unlimited (never stop).\033[0m\n",
                    flush=True,
                )
                break

            CURRENT_WAVE = wave_num
            HUD.render(force_region=False)
            attempts_before_wave = len(ATTEMPT_LEDGER)
            wave_ratio_str = f"{wave_num}/∞" if is_unlimited else f"{wave_num}/{waves_limit}"

            audit_digest, tried_vecs, untried_vecs = _build_vault_and_attempt_summary_for_relentless(ACTIVE_GOAL)

            # Query the 14-Engine Neuro-Symbolic & Evolutionary MAP-Elites Pipeline for novel strategies
            reasoning_hint = ""
            try:
                from Reasoning.reasoning_cli import execute_reasoning_tool

                recent_fails = "; ".join(
                    f"{a['target_or_cmd']} -> {a['summary']}"
                    for a in ATTEMPT_LEDGER[-5:]
                    if a["status"] in ("FAIL", "BLOCKED")
                )
                prob_query = f"Goal: {ACTIVE_GOAL}. Prior failed attempts: {recent_fails or 'none yet'}. Untried vectors: {', '.join(untried_vecs)}"
                raw_reason = execute_reasoning_tool("pipeline", {"problem": prob_query, "save_to_vault": (wave_num == 1)})
                reasoning_hint = compact_text(raw_reason, 1600)
            except Exception:
                pass

            print(
                f"\n\033[1;35m>>> [Relentless Wave {wave_ratio_str}] Focusing on Goal: `{ACTIVE_GOAL[:80]}` "
                f"(Attempts so far: {len(ATTEMPT_LEDGER)} | Untried vectors: {len(untried_vecs)}) <<<\033[0m",
                flush=True,
            )

            pmode_now = (ACTIVE_PERSONALITY_MODE or "DEFAULT").upper()
            if pmode_now == "ANALYST":
                mode_wave_rule = (
                    "3. ANALYST MODE (`WHITE` LOCAL-ONLY ISOLATION): Do NOT run network scans (`scan_target`, `nmap`, `ping`) or outbound network tools (`curl`, `wget`, `ssh`, `tio`). "
                    "Use ONLY local analysis tools (`read_file`, `list_directory`, `vault_search`, `vault_read_note`, `neuro_symbolic_reason`, and local-only `run_shell_command` like `ls`, `cat`, `grep`, `jq`).\n"
                )
            elif pmode_now == "NINJA":
                mode_wave_rule = (
                    "3. NINJA COVERT MODE: You MUST find the answers and achieve the goal, but DO NOT act aggressively. Use covert, low-noise commands at all times:\n"
                    "   - Check passive host state (`ip -br addr`, `ip route`, `ip neigh`, `ss -tulnp`, local files, and `ObsidianVault/` notes) first.\n"
                    "   - When active probing is needed, use stealthy single-request `curl -sS` or `nmap -sT -Pn -T2 --max-rate 15` on specific ports only; never run noisy flood scanners or `-T4`/`-T5`/`-A`.\n"
                )
            elif pmode_now == "BERSERKER":
                mode_wave_rule = (
                    f"3. BERSERKER AGGRESSIVE MODE: Aggressively pursue the target goal with ALL available tools (`run_shell_command`, `scan_target`, `vault_read_note`, `vault_search`, `neuro_symbolic_reason`, `read_file`, `write_file`) across `{', '.join(untried_vecs) if untried_vecs else 'multi-step chain / alternate ports / credentials / OOB serial / routing pivot'}`.\n"
                    f"   - Immediately chain active probes across Layer-1/2/3/4/7 (`ip -4 addr`, `ip route`, `ip neigh`, `arping`, `nmap -Pn`, `curl`, `[[commands/tio_serial_playbook]]`, `/dev/ttyUSB0`, and `[[projects/{ACTIVE_PROJECT or get_active_project_slug()}]]`).\n"
                )
            else:
                mode_wave_rule = (
                    f"3. TRY UNEXPLORED METHODS & TOOLS NOW: You must immediately invoke your tools (`run_shell_command`, `scan_target`, `vault_read_note`, `vault_search`, `neuro_symbolic_reason`, `read_file`, `write_file`) to test an untried method or capability vector (`{', '.join(untried_vecs) if untried_vecs else 'multi-step chain / alternate ports / credentials / OOB serial / routing pivot'}`).\n"
                    f"   - If direct HTTP/TCP fails, check Layer-2/Layer-3 (`ip -4 addr`, `ip route`, `ip neigh`, `arping` on Linux or `ipconfig /all`, `route print -4`, `arp -a` on Windows), check alternate ports (`nmap -Pn` or `Test-NetConnection`), check Obsidian Vault playbooks (`[[commands/tio_serial_playbook]]`, `[[commands/curl_playbook]]`, `[[projects/{ACTIVE_PROJECT or get_active_project_slug()}]]`), or check serial OOB (`/dev/ttyUSB0`).\n"
                )

            wave_directive = (
                f"{audit_digest}\n\n"
                + (f"[20-ENGINE 5-LAYER LEXICAL NEURO-SYMBOLIC STRATEGY]:\n{reasoning_hint}\n\n" if reasoning_hint else "")
                + f"=== MANDATORY RELENTLESS WAVE #{wave_num} DIRECTIVE ===\n"
                f"1. PRIMARY GOAL: `{ACTIVE_GOAL}`\n"
                f"2. DO NOT STOP EARLY AND DO NOT REPEAT FAILED COMMANDS: Review the Attempt Ledger above. Never re-run a failed command identically.\n"
                + mode_wave_rule
                + f"4. COMPLETION CRITERIA:\n"
                f"   - ONLY output `[GOAL_ACHIEVED: <exact proof and command output>]` once you have concrete, verified evidence from tool output that `{ACTIVE_GOAL}` is 100% achieved.\n"
                + (
                    "   - UNLIMITED MODE (`max:0`) IS ACTIVE: Do NOT output `[EXHAUSTED_ALL_METHODS]`. Keep synthesizing new multi-step chains, parameter variations, OOB serial commands, API endpoints, and routing pivots until the goal is achieved."
                    if is_unlimited
                    else "   - ONLY output `[EXHAUSTED_ALL_METHODS: <summary>]` if every single capability vector (`L1_Serial_OOB`, `L2_ARP_Link`, `L3_Routing_NAT`, `L4_Port_Service`, `L7_HTTP_Web_Exploit`, `Vault_Knowledge_Playbooks`, `Neuro_Symbolic_20_Engines`) has been tested and proven impossible."
                )
            )

            messages.append({"role": "user", "content": wave_directive})
            assistant_text = run_turn(messages, max_steps=14)
            _sync_goal_and_attempts_to_vault()

            new_attempts = ATTEMPT_LEDGER[attempts_before_wave:]
            any_ok_tool = any(a["status"] == "OK" for a in ATTEMPT_LEDGER)

            # Check if the goal was genuinely achieved
            if "[GOAL_ACHIEVED" in (assistant_text or "").upper() and any_ok_tool:
                print(
                    f"\n\033[1;32m==============================================================================\033[0m\n"
                    f"\033[1;32m  [RELENTLESS GOAL ACHIEVED in Wave {wave_ratio_str}!]\033[0m\n"
                    f"  \033[1;33mGoal:\033[0m {ACTIVE_GOAL}\n"
                    f"  \033[1;36mTotal Tool Executions Logged to ObsidianVault:\033[0m {len(ATTEMPT_LEDGER)}\n"
                    f"\033[1;32m==============================================================================\033[0m\n",
                    flush=True,
                )
                break

            # Check if the LLM claimed exhaustion
            _, tried_after, untried_after = _build_vault_and_attempt_summary_for_relentless(ACTIVE_GOAL)
            if "[EXHAUSTED_ALL_METHODS" in (assistant_text or "").upper():
                if is_unlimited:
                    print(
                        f"\n\033[1;35m[Relentless Unlimited Mode (`max:0`)]\033[0m Model claimed exhaustion at Wave {wave_num}, "
                        f"but `max:0` (never stop) is active — forcing new multi-step chain & parameter synthesis in Wave {wave_num + 1}...",
                        flush=True,
                    )
                elif len(tried_after) >= 4 or wave_num >= 4:
                    print(
                        f"\n\033[1;33m==============================================================================\033[0m\n"
                        f"\033[1;33m  [RELENTLESS LOOP COMPLETED — ALL VIABLE VECTORS TESTED (Wave {wave_num})]\033[0m\n"
                        f"  \033[1;36mVectors Probed:\033[0m {', '.join(tried_after)}\n"
                        f"  \033[1;36mVault Attempt Ledger:\033[0m [[{_sync_goal_and_attempts_to_vault()}]]\n"
                        f"\033[1;33m==============================================================================\033[0m\n",
                        flush=True,
                    )
                    break
                else:
                    print(
                        f"\n\033[1;33m[Relentless Controller Override]\033[0m Model claimed exhaustion after only "
                        f"{len(tried_after)} vector(s), but `{', '.join(untried_after)}` remain untried! Continuing to Wave {wave_num + 1}...",
                        flush=True,
                    )

            # If the LLM didn't call any tools at all in this wave, prod it harder in the next wave
            if not new_attempts:
                print(
                    f"\n\033[1;33m[Relentless Controller]\033[0m Wave {wave_num} produced 0 tool calls — forcing tool execution on untried vectors in Wave {wave_num + 1}...",
                    flush=True,
                )
    except KeyboardInterrupt:
        print(
            f"\n\033[1;33m[Relentless Loop Paused by User at Wave {CURRENT_WAVE}]\033[0m "
            f"All {len(ATTEMPT_LEDGER)} attempts are saved in `ObsidianVault/projects/`. "
            "Type `/relentless` at any time to resume from where it left off!\n",
            flush=True,
        )


def handle_goal_command(arg_str: str, messages: list) -> None:
    """
    Handle in-CLI `/goal` switch (project-scoped goals stored in `Projects/<active_project>/goals.md`):
      - `/goal` or `/goal status` or `/goal -mode:status` : Display the very last goal saved in `Projects/<project>/goals.md`
      - `/goal list` or `/goal -mode:list`                : List all chronological goals saved in `Projects/<project>/goals.md`
      - `/goal audit` or `/goal -mode:audit`              : Show full Relentless Attempt Ledger & capability vector audit
      - `/goal clear` or `/goal -mode:clear`              : Clear active in-memory goal and attempt ledger
      - `/goal "<objective text>" [-max:<#>]`             : Append `<objective text>` (must be in quotes) to `Projects/<project>/goals.md`, set as active goal, and execute
    """
    global ACTIVE_GOAL, CURRENT_WAVE, MAX_RELENTLESS_WAVES
    cleaned = arg_str.strip()
    if _is_help_arg(cleaned.lower()):
        print_switch_help("goal")
        return

    proj_slug = get_active_project_slug()
    goals_file = get_project_goals_file(proj_slug)

    cleaned_goal, parsed_max, sub_mode, parse_err = _parse_goal_and_relentless_args(cleaned, switch_name="goal")
    if parse_err:
        print(f"\n\033[1;31m[Parameter / Goal Syntax Error]\033[0m {parse_err}\n")
        return

    if not cleaned or sub_mode in ("status", "last", "latest", "current"):
        proj_goals = get_project_goals(proj_slug)
        if not proj_goals and ACTIVE_GOAL:
            append_project_goal(ACTIVE_GOAL, proj_slug)
            proj_goals = get_project_goals(proj_slug)
        if not proj_goals:
            print(
                f"\n\033[1;33m=== Project Goal (`Projects/{proj_slug}/goals.md`) ===\033[0m\n"
                f"  Active Project: `{proj_slug}` (`{PROJECTS_DIR / proj_slug}`)\n"
                f"  Goals File:     `{goals_file}`\n"
                "  Current Goal:   `None` (No goals recorded for this project yet)\n"
                '  Set one with:   `/goal "<your specific objective>" [-max:<#>]`\n'
            )
            return
        last_entry = proj_goals[-1]
        ACTIVE_GOAL = last_entry["goal"]
        HUD.render(force_region=False)
        print(
            f"\n\033[1;36m=== Project Goal (`Projects/{proj_slug}/goals.md`) ===\033[0m\n"
            f"  Active Project: `{proj_slug}`\n"
            f"  Goals File:     `{goals_file}` (`{len(proj_goals)}` goal(s) saved; type `/goal list` to view all)\n"
            f"  Max Waves Cap:  `{_format_max_waves_label()}`\n"
            f"  \033[1;32mLast Goal (#{last_entry['index']} | {last_entry['timestamp']}):\033[0m\n"
            f"    {last_entry['goal']}\n"
        )
        return

    if sub_mode in ("list", "all", "history"):
        proj_goals = get_project_goals(proj_slug)
        if not proj_goals and ACTIVE_GOAL:
            append_project_goal(ACTIVE_GOAL, proj_slug)
            proj_goals = get_project_goals(proj_slug)
        print(f"\n\033[1;36m=== All Project Goals (`Projects/{proj_slug}/goals.md`) ===\033[0m")
        if not proj_goals:
            print('  *(No goals saved for this project yet. Use `/goal "<objective>"` to add one.)*\n')
            return
        for entry in proj_goals:
            is_last = entry["index"] == proj_goals[-1]["index"]
            tag = " \033[1;32m[LATEST / ACTIVE]\033[0m" if is_last else ""
            print(f"  \033[1;33m[Goal #{entry['index']}]\033[0m ({entry['timestamp']}){tag}: {entry['goal']}")
        print()
        return

    if sub_mode in ("audit", "ledger"):
        cur_g = ACTIVE_GOAL or get_last_project_goal(proj_slug) or "(No active goal set)"
        digest, _, _ = _build_vault_and_attempt_summary_for_relentless(cur_g)
        print(f"\n\033[1;36m{digest}\033[0m\n")
        return

    if sub_mode in ("clear", "off", "reset", "none"):
        ACTIVE_GOAL = ""
        ATTEMPT_LEDGER.clear()
        CURRENT_WAVE = 0
        HUD.render(force_region=False)
        save_current_cli_session(messages)
        print(
            f"\n\033[1;32m[Goal Cleared]\033[0m Active session goal and attempt ledger reset "
            f"(historical goals remain preserved in `{goals_file}`).\n"
        )
        return

    if parsed_max is not None:
        MAX_RELENTLESS_WAVES = parsed_max
    if not cleaned_goal:
        print(
            f"\n\033[1;32m[Goal Wave Cap Updated]\033[0m Max waves per run set to `{_format_max_waves_label()}`.\n"
        )
        return

    # New goal set: append to `Projects/<project>/goals.md` and update `ACTIVE_GOAL`
    if cleaned_goal != ACTIVE_GOAL:
        ACTIVE_GOAL = cleaned_goal
        CURRENT_WAVE = 0
        ATTEMPT_LEDGER.clear()
    g_path, g_num, _ = append_project_goal(ACTIVE_GOAL, proj_slug)
    HUD.render(force_region=False)
    vault_ref = _sync_goal_and_attempts_to_vault()
    save_current_cli_session(messages)
    print(
        f"\n\033[1;32m[Project Goal #{g_num} Saved & Locked]\033[0m `{ACTIVE_GOAL}`\n"
        f"\033[1;36m[Project Goals File]\033[0m `{g_path}` (`[[Projects/{proj_slug}/goals]]`)\n"
        f"\033[1;36m[Obsidian Ledger]\033[0m    [[{vault_ref}]] | Relentless Mode: `{'ON' if RELENTLESS_MODE else 'OFF (type /relentless to loop until achieved)'}` | Max Waves: `{_format_max_waves_label()}`\n",
        flush=True,
    )

    if RELENTLESS_MODE:
        run_relentless_loop(messages)
    else:
        messages.append(
            {
                "role": "user",
                "content": (
                    f"[ACTIVE GOAL SET]: `{ACTIVE_GOAL}`\n"
                    f"Active Obsidian Project: `{ACTIVE_PROJECT or 'None'}`\n"
                    "Focus 100% on achieving this goal. First check `ObsidianVault/` (`vault_search` / `vault_read_note`) "
                    "for existing target scans, project docs, or playbooks, and begin executing tools toward this goal."
                ),
            }
        )
        try:
            run_turn(messages)
            print()
        except Exception as exc:
            print(f"\n\033[1;31m[Error]\033[0m {exc}\n")


def handle_relentless_command(arg_str: str, messages: list) -> None:
    """
    Handle in-CLI `/relentless` switch:
      - `/relentless`                          : Enable Relentless Mode and immediately start looping on `ACTIVE_GOAL`
      - `/relentless "<goal text>" [-max:<#>]` : Set `ACTIVE_GOAL = <goal text>` (must be in quotes), append to `Projects/<project>/goals.md`, enable Relentless Mode, and start looping
      - `/relentless -max:<#>`                 : Set maximum waves per `/relentless` run (`-max:0` or `-max:unlimited` = never stop / unlimited; default: `15`)
      - `/relentless on` | `-mode:on`          : Enable persistent Relentless Mode (and start looping if `ACTIVE_GOAL` is set)
      - `/relentless off` | `-mode:off`        : Disable persistent Relentless Mode
      - `/relentless status` | `-mode:status`  : Show Relentless Mode state, wave limit, and active goal
    """
    global RELENTLESS_MODE, ACTIVE_GOAL, MAX_RELENTLESS_WAVES, CURRENT_WAVE
    cleaned = arg_str.strip()
    if _is_help_arg(cleaned.lower()):
        print_switch_help("relentless")
        return

    cleaned_goal, parsed_max, sub_mode, parse_err = _parse_goal_and_relentless_args(
        cleaned, switch_name="relentless"
    )
    if parse_err:
        print(f"\n\033[1;31m[Parameter / Goal Syntax Error]\033[0m {parse_err}\n")
        return

    if sub_mode in ("off", "stop"):
        RELENTLESS_MODE = False
        HUD.render(force_region=False)
        print("\n\033[1;33m[Relentless Mode: OFF]\033[0m Standard single-turn execution restored.\n")
        return

    if sub_mode == "status":
        cur_g = ACTIVE_GOAL or get_last_project_goal()
        if cur_g and not ACTIVE_GOAL:
            ACTIVE_GOAL = cur_g
        _none_goal_lbl = 'None (set with /goal "<objective>")'
        print(
            f"\n\033[1;35m=== Relentless Mode Status ===\033[0m\n"
            f"  Relentless Mode: `{'ON' if RELENTLESS_MODE else 'OFF'}`\n"
            f"  Max Waves Cap:   `{_format_max_waves_label()}` (up to 14 tool calls/wave; use `/relentless -max:<#>` or `-max:0` for unlimited)\n"
            f"  Active Goal:     `{ACTIVE_GOAL or _none_goal_lbl}`\n"
        )
        return

    if sub_mode in ("audit", "ledger"):
        digest, _, _ = _build_vault_and_attempt_summary_for_relentless(
            ACTIVE_GOAL or get_last_project_goal() or "(No active goal set)"
        )
        print(f"\n{digest}\n")
        return

    if parsed_max is not None:
        MAX_RELENTLESS_WAVES = parsed_max
        save_current_cli_session(messages)
        if not cleaned_goal and not sub_mode:
            print(
                f"\n\033[1;32m[Relentless Mode]\033[0m Max waves per run set to `{_format_max_waves_label()}`.\n"
            )
            return

    # Enable Relentless Mode
    RELENTLESS_MODE = True
    HUD.render(force_region=False)

    # If the user passed a quoted goal inline (`/relentless "You must try to the max and never stop" -max:100`), set it as ACTIVE_GOAL and append to project `goals.md`
    if cleaned_goal:
        if cleaned_goal != ACTIVE_GOAL:
            ACTIVE_GOAL = cleaned_goal
            CURRENT_WAVE = 0
            ATTEMPT_LEDGER.clear()
        append_project_goal(ACTIVE_GOAL)
        HUD.render(force_region=False)

    if not ACTIVE_GOAL:
        ACTIVE_GOAL = get_last_project_goal()

    if ACTIVE_GOAL:
        append_project_goal(ACTIVE_GOAL)
        run_relentless_loop(messages)
    else:
        # Check if there is a previous user prompt in `messages` to promote to `ACTIVE_GOAL`
        for m in reversed(messages):
            if m.get("role") == "user" and m.get("content"):
                txt = str(m["content"]).strip()
                if not txt.startswith("[System Note]") and not txt.startswith("=== RELENTLESS"):
                    ACTIVE_GOAL = txt[:240]
                    break
        if ACTIVE_GOAL:
            append_project_goal(ACTIVE_GOAL)
            HUD.render(force_region=False)
            run_relentless_loop(messages)
        else:
            print(
                "\n\033[1;35m[Relentless Mode: ON]\033[0m\n"
                '  Relentless Mode is now armed! Set your objective with `/goal "<objective>"` (or just type your task),\n'
                "  and the CLI will autonomously loop across all tools, Obsidian Vault notes, and 15 reasoning engines\n"
                "  until the goal is achieved!\n"
            )


def start_project_onboarding(doc_source: str, custom_name: str, messages: list, prompt_mode: bool = True) -> None:
    """Read documentation from doc_source, initialize or select an isolated project in `Projects/`, and trigger LLM onboarding."""
    global ACTIVE_PROJECT
    derived_name, doc_digest = load_documentation_source(doc_source)
    proj_slug = slugify_project_name(custom_name) if custom_name else slugify_project_name(derived_name)
    _persist_selected_project(proj_slug)
    proj_ws = PROJECTS_DIR / proj_slug

    print(f"\n\033[1;36m[Project Onboarding]\033[0m Loaded documentation from: {doc_source}")
    print(f"\033[1;32m[Active Isolated Project]\033[0m [[Projects/{proj_slug}/memory]] -> {proj_ws / 'memory.md'}\n")

    if prompt_mode:
        interactive_personality_mode_menu(proj_slug, allow_back_to_project=False)
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)

    onboarding_prompt = (
        f"I am starting/updating a project using documentation from `{doc_source}`.\n"
        f"Suggested project name: `{proj_slug}` (you may refine the project name in `project_tracker` if the "
        "documentation specifies a clearer official project/system name).\n\n"
        f"Here is the extracted documentation:\n\n{doc_digest}\n\n"
        "Please perform these exact steps right now:\n"
        "1. Call `project_tracker` to create the isolated project memory note under `Projects/<project_name>/memory.md` with:\n"
        "   - Key facts, IPs, hardware/interfaces, credentials, and architecture extracted from the documentation.\n"
        "   - Specific verification questions to confirm any missing, ambiguous, or environment-specific details with me.\n"
        "   - An initial phased project plan with `- [ ]` checkboxes.\n"
        "2. Present a concise summary of what you learned from the documentation and ask me your verification questions "
        "so we can confirm the data and begin executing the plan."
    )
    messages.append({"role": "user", "content": onboarding_prompt})
    run_turn(messages)
    print()


def handle_project_command(arg_str: str, messages: list) -> None:
    """
    Handle `/project ...` and `/project/<name> [optional task]` interactive commands.
    Enforces dash-prefixed colon-delimited `-<param>:<value>` syntax for parameterized sub-commands:
      - `/project` or `/project menu` or `/project -mode:menu` : Open interactive numbered Project Selection / Rename / Create menu
      - `/project list` or `/project -mode:list`               : List all projects in `Projects/`
      - `/project -new:<name>` (or `/project new`)             : Create a new project in `Projects/<name>/` (auto-converts spaces/special chars to `-`)
      - `/project -rename:<old>:<new>` (or `/project rename`)  : Rename an existing project (or open interactive rename menu)
      - `/project -load:<name> ["<task>"]`                     : Switch active project to `<name>` (and optionally run `"<task>"`)
      - `/project -doc:<path> [-name:<project_name>]`          : Onboard documentation into a project
    """
    global ACTIVE_PROJECT, ACTIVE_GOAL
    cleaned_arg = arg_str.strip().lstrip("/")
    if not cleaned_arg or cleaned_arg.lower() in ("menu", "select", "-mode:menu", "-mode:select"):
        chosen = interactive_project_selection_menu(require_selection=False)
        if chosen and messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
        HUD.render(force_region=False)
        return

    parts = cleaned_arg.split(maxsplit=1)
    cmd_sub = parts[0].lower()
    if cmd_sub in ("-h", "--help", "help"):
        print_switch_help("project")
        return

    # Reject colon parameters that are missing the required leading dash `-`
    if re.match(r"^(new|create|rename|load|switch|open|doc|mode|name):", cmd_sub):
        print(
            f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — "
            f"use `-{parts[0]}` instead of `{parts[0]}` (e.g. `/project -{parts[0]}`).\n"
        )
        return

    if cmd_sub in ("list", "-mode:list", "--mode:list"):
        print("\n" + list_vault_projects() + "\n")
        return

    if cmd_sub in ("new", "create", "-new", "-create") or cmd_sub.startswith(("-new:", "--new:", "-create:", "--create:")):
        if cmd_sub in ("new", "create", "-new", "-create") and len(parts) > 1:
            print(
                f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-new:<name>` (with a leading dash `-` and colon `:`) instead of a space — "
                f"e.g. `/project -new:{slugify_project_name(parts[1])}` (or type `/project new` to use the interactive prompt).\n"
            )
            return
        raw_new = cleaned_arg.split(":", 1)[1].strip() if ":" in cmd_sub else ""
        if not raw_new:
            try:
                raw_new = input("Enter New Project Name (spaces/special chars auto-convert to `-`, C=CANCEL): ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
        if not raw_new or raw_new.lower() in ("c", "cancel", "b", "back"):
            print("Create New Project cancelled.\n")
            return
        new_slug = slugify_project_name(raw_new)
        _persist_selected_project(new_slug)
        print(f"\n\033[1;32m[New Project Created]\033[0m Active project set to `Projects/{new_slug}/` (`{PROJECTS_DIR / new_slug / 'memory.md'}`).\n")
        interactive_personality_mode_menu(new_slug, allow_back_to_project=False)
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
        HUD.render(force_region=False)
        return

    if cmd_sub in ("rename", "-rename") or cmd_sub.startswith(("-rename:", "--rename:")):
        if cmd_sub in ("rename", "-rename") and len(parts) > 1:
            rem_sp = parts[1].strip().split(maxsplit=1)
            ex_old = rem_sp[0] if rem_sp else "old-name"
            ex_new = slugify_project_name(rem_sp[1]) if len(rem_sp) > 1 else "new-name"
            print(
                f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-rename:<old>:<new>` (with a leading dash `-` and colons `:`) instead of spaces — "
                f"e.g. `/project -rename:{ex_old}:{ex_new}` (or type `/project rename` to open the interactive Rename menu).\n"
            )
            return
        if cmd_sub.startswith(("-rename:", "--rename:")):
            rem_body = cleaned_arg.split(":", 1)[1].strip()
            if ":" not in rem_body:
                print(
                    "\n\033[1;31mUsage:\033[0m `/project -rename:<old_project>:<new_project>` (or `/project rename` for interactive menu).\n"
                )
                return
            old_raw, new_raw = rem_body.split(":", 1)
            old_s = slugify_project_name(old_raw)
            ok, new_s, msg = rename_project_workspace(old_s, new_raw)
            if ok and ACTIVE_PROJECT == new_s:
                _persist_selected_project(new_s)
                if messages and messages[0].get("role") == "system":
                    messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
                HUD.render(force_region=False)
            color = "\033[1;32m" if ok else "\033[1;31m"
            print(f"\n{color}{msg}\033[0m\n")
            return
        # Open interactive menu for rename
        interactive_project_selection_menu(require_selection=False)
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
        HUD.render(force_region=False)
        return

    def _find_project_note(slug: str) -> Path | None:
        cand_ws = PROJECTS_DIR / slug / "memory.md"
        if cand_ws.is_file():
            return cand_ws
        cand_legacy = VAULT_DIR / "projects" / f"{slug}.md"
        if cand_legacy.is_file():
            return cand_legacy
        return None

    if cmd_sub in ("load", "switch", "open", "-load", "-switch", "-open") and len(parts) > 1:
        clean_k = cmd_sub.lstrip("-")
        print(
            f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-{clean_k}:<name>` (with a leading dash `-` and colon `:`) instead of a space — "
            f"e.g. `/project -{clean_k}:{slugify_project_name(parts[1].split()[0])}`.\n"
        )
        return

    follow_up_task = ""
    if cmd_sub.startswith(("-load:", "--load:", "-switch:", "--switch:", "-open:", "--open:")):
        first_tok_val = parts[0].split(":", 1)[1].strip()
        cand_slug = slugify_project_name(first_tok_val)
        follow_up_task = parts[1].strip().strip("\"'") if len(parts) > 1 else ""
        note_path = _find_project_note(cand_slug)
        if note_path is None:
            print(f"\n\033[1;31mProject `{cand_slug}` not found in {PROJECTS_DIR} or {VAULT_DIR / 'projects'}.\033[0m\n")
            print(list_vault_projects() + "\n")
            return
    elif cmd_sub.startswith(("-doc:", "--doc:")):
        doc_source = parts[0].split(":", 1)[1].strip()
        custom_name = ""
        if len(parts) > 1:
            rem_doc = parts[1].strip()
            if rem_doc.lower().startswith("name:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{rem_doc}`.\n"
                )
                return
            if rem_doc.lower().startswith(("-name:", "--name:")):
                custom_name = rem_doc.split(":", 1)[1].strip()
            else:
                custom_name = rem_doc
        try:
            start_project_onboarding(doc_source, custom_name, messages)
        except Exception as exc:
            print(f"\n\033[1;31m[Project Error]\033[0m {exc}\n")
        return
    else:
        cand_slug = slugify_project_name(parts[0])
        note_path = _find_project_note(cand_slug)
        if note_path is not None and not Path(os.path.expanduser(parts[0])).exists():
            follow_up_task = parts[1].strip().strip("\"'") if len(parts) > 1 else ""
        else:
            note_path = None

    if note_path is not None and note_path.is_file():
        _persist_selected_project(cand_slug)
        if follow_up_task:
            ACTIVE_GOAL = follow_up_task
            append_project_goal(follow_up_task, cand_slug)
        print(f"\n\033[1;32m[Project Selected]\033[0m Switched active project to `[[Projects/{cand_slug}/memory]]`.\n")
        interactive_personality_mode_menu(cand_slug, allow_back_to_project=False)
        HUD.render(force_region=False)
        content = read_vault_note(f"projects/{cand_slug}")
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt()
        print(f"\n\033[1;32mActive Project Memory (`[[Projects/{cand_slug}/memory]]`):\033[0m\n{content}\n")
        if follow_up_task:
            prompt_body = (
                f"Active project switched to `[[Projects/{cand_slug}/memory]]`. Here is the project note:\n\n"
                f"{content}\n\n"
                f"USER TASK / GOAL FOR THIS PROJECT: {follow_up_task}"
            )
        else:
            prompt_body = (
                f"We have switched to existing project `[[Projects/{cand_slug}/memory]]`. Here is the current project note:\n\n"
                f"{content}\n\nSummarize current status, next uncompleted `- [ ]` tasks, and any open questions."
            )
        messages.append({"role": "user", "content": prompt_body})
        try:
            if follow_up_task and RELENTLESS_MODE:
                run_relentless_loop(messages)
            else:
                run_turn(messages)
            print()
        except Exception as exc:
            print(f"\n\033[1;31m[Error]\033[0m {exc}\n")
        return

    # Otherwise: `/project <doc_path_or_dir> [-name:<project_name>]`
    doc_source = parts[0]
    custom_name = parts[1].strip() if len(parts) > 1 else ""
    if custom_name.lower().startswith("name:"):
        print(
            f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{custom_name}`.\n"
        )
        return
    if custom_name.lower().startswith(("-name:", "--name:")):
        custom_name = custom_name.split(":", 1)[1].strip()
    try:
        start_project_onboarding(doc_source, custom_name, messages)
    except Exception as exc:
        print(f"\n\033[1;31m[Project Error]\033[0m {exc}\n")


def handle_generate_report_command(arg_str: str) -> None:
    """
    Handle `/generate-report [-project:<name>] [-focus:<topic>] [-mode:<fast|full>]` (and `/report` alias) in-CLI switch:
    Generates the 5-Section Project Status & Findings Report (Executive Summary, High-School
    Reading Level Walkthrough, Standalone SVG Infographic + Mermaid Diagrams, Technical Findings
    Write-Up, and Final Conclusion) inside `Projects/<project>/REPORT.md`.
    """
    cleaned = arg_str.strip()
    if cleaned.lower() in ("-h", "--help", "help"):
        print_switch_help("generate-report")
        return

    # Reject accidental space syntax for `-project <name>`, `-focus <topic>`, or `-mode <fast|full>`
    m_bad_rep = re.match(r"^-?(project|focus|mode)\s+(\S+.*)$", cleaned, flags=re.I)
    if m_bad_rep:
        k_name = m_bad_rep.group(1).lower()
        v_name = m_bad_rep.group(2).strip()
        print(
            f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-{k_name}:<value>` (with a leading dash `-` and colon `:`) instead of a space — "
            f"e.g. `/generate-report -{k_name}:{v_name}`.\n"
        )
        return

    use_llm = True
    target_proj = ACTIVE_PROJECT or get_active_project_slug()
    focus_parts: list[str] = []

    tokens = [t for t in cleaned.split() if t]
    filtered_tokens = []
    for t in tokens:
        t_low = t.lower()
        if t_low.startswith(("project:", "focus:", "mode:")):
            print(
                f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — "
                f"use `-{t}` instead of `{t}` (e.g. `/generate-report -{t}`).\n"
            )
            return
        if t_low in ("--no-llm", "fast", "--fast", "-fast", "-mode:fast", "--mode:fast", "-mode:no-llm"):
            use_llm = False
        elif t_low in ("-mode:full", "--mode:full", "-mode:llm"):
            use_llm = True
        elif t_low.startswith(("-project:", "--project:")):
            p_val = t.split(":", 1)[1].strip()
            if p_val:
                target_proj = slugify_project_name(p_val)
        elif t_low.startswith(("-focus:", "--focus:")):
            f_val = t.split(":", 1)[1].strip().strip("\"'")
            if f_val:
                focus_parts.append(f_val)
        else:
            filtered_tokens.append(t)

    if filtered_tokens:
        cand_slug = slugify_project_name(filtered_tokens[0])
        if (PROJECTS_DIR / cand_slug).is_dir() or (VAULT_DIR / "projects" / f"{cand_slug}.md").is_file():
            target_proj = cand_slug
            if len(filtered_tokens) > 1:
                focus_parts.append(" ".join(filtered_tokens[1:]).strip())
        else:
            focus_parts.append(" ".join(filtered_tokens).strip())
    focus_str = " ".join(focus_parts).strip()

    try:
        from Reasoning.report_generator import generate_project_report

        print(
            f"\n\033[1;36m[Generating Project Status & Findings Report -> `{target_proj}`]\033[0m "
            "(Executive Summary + High-School Walkthrough + SVG Graphic + Technical Evidence + Conclusion)...",
            flush=True,
        )
        res = generate_project_report(
            project_name=target_proj,
            active_goal=ACTIVE_GOAL,
            attempt_ledger=ATTEMPT_LEDGER,
            report_focus=focus_str,
            use_llm=use_llm,
        )
        print(
            f"\n\033[1;32m=== Project Status & Findings Report Generated ===\033[0m\n"
            f"  Project Workspace: `Projects/{res['project_slug']}/` (Status: `{res['overall_status']}`)\n"
            f"  Primary Report:    \033[1;36m{res['report_path']}\033[0m (`[[Projects/{res['project_slug']}/REPORT]]`)\n"
            f"  Dated Copy:        `{res['dated_report_path']}`\n"
            f"  SVG Dashboard:     \033[1;35m{res['svg_path']}\033[0m\n"
            f"  Metrics:           Milestone Progress `{res['task_completion_pct']}%` | Command Accuracy `{res['cmd_hit_pct']}%`\n"
        )
        print(f"{compact_text(res['markdown'], 3200)}\n")
    except Exception as exc:
        print(f"\n\033[1;31m[Report Generator Error]\033[0m {exc}\n")


def handle_mode_command(arg_str: str, messages: list) -> None:
    """
    Handle `/mode` in-CLI switch for the 4 Session Personality & Logic Enforcement Modes:
      - `/mode` or `/mode menu` or `/mode -mode:menu`     : Open interactive numbered Mode Selection Menu (`[1] Default`, `[2] Analyst`, `[3] Berserker`, `[4] Ninja`)
      - `/mode status` or `/mode -mode:status`            : Display active Session Personality Mode, purpose, and Network Isolation group
      - `/mode <1|2|3|4|default|analyst|berserker|ninja>` : Switch session personality mode (prompts Red/Blue isolation group for Berserker/Ninja unless `-netiso:<red|blue>` is passed)
    """
    cleaned = arg_str.strip()
    if not cleaned or cleaned.lower() in ("menu", "select", "-mode:menu", "-mode:select"):
        interactive_personality_mode_menu(ACTIVE_PROJECT, allow_back_to_project=False)
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
        HUD.render(force_region=False)
        return

    if _is_help_arg(cleaned.lower()):
        print_switch_help("mode")
        return

    # Check for space syntax `-mode <val>` or `-netiso <val>`
    m_bad_sp = re.match(r"^-?(mode|netiso)\s+(\S+.*)$", cleaned, flags=re.I)
    if m_bad_sp:
        k_n = m_bad_sp.group(1).lower()
        v_n = m_bad_sp.group(2).strip()
        print(
            f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-{k_n}:<value>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/mode -{k_n}:{v_n}`.\n"
        )
        return

    mode_tok = ""
    netiso_tok = ""
    for tok in cleaned.split():
        t_low = tok.lower()
        if t_low.startswith(("mode:", "netiso:")):
            print(
                f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{tok}` instead of `{tok}`.\n"
            )
            return
        if t_low.startswith(("-mode:", "--mode:")):
            mode_tok = tok.split(":", 1)[1].strip().lower()
        elif t_low.startswith(("-netiso:", "--netiso:")):
            netiso_tok = tok.split(":", 1)[1].strip().lower()
        elif not mode_tok:
            mode_tok = t_low
        elif not netiso_tok and t_low in ("red", "blue", "1", "2"):
            netiso_tok = t_low

    if mode_tok in ("status", "info", "current"):
        pmode = (ACTIVE_PERSONALITY_MODE or "DEFAULT").upper()
        num_map = {"DEFAULT": "1", "ANALYST": "2", "BERSERKER": "3", "NINJA": "4"}
        m_num = num_map.get(pmode, "1")
        m_meta = PERSONALITY_MODES_META[m_num]
        iso_lvl = os.environ.get("LLM_ISOLATION_MODE", "RED").upper()
        allow_if = os.environ.get("LLM_ALLOWED_IFACES", "").strip()
        iface_str = "lo (Local Loopback Only)" if iso_lvl == "WHITE" else ("All" if iso_lvl == "RED" else allow_if)
        print(
            f"\n\033[1;35m=== Active Session Personality & Logic Enforcement Mode ===\033[0m\n"
            f"  Active Project:    `Projects/{get_active_project_slug()}/`\n"
            f"  Session Mode:      {m_meta['color']}[{m_num}] {m_meta['label']}\033[0m — {m_meta['purpose']}\n"
            f"  Network Isolation: `{iso_lvl}` (Interfaces: `{iface_str}`)\n"
            f"  Scope:             Session-only (unique to this session; always selected after Project selection)\n"
        )
        return

    if mode_tok in ("1", "default", "std", "standard"):
        mode_key, iso_lvl, _ = apply_personality_mode("DEFAULT", netiso_group=netiso_tok)
        print(
            f"\n\033[1;32m[Session Mode Locked -> Default]\033[0m Standard operation (no extra LLM behavioral guidance | Network Isolation: `{iso_lvl}`).\n"
        )
    elif mode_tok in ("2", "analyst", "passive"):
        mode_key, iso_lvl, _ = apply_personality_mode("ANALYST")
        print(
            "\n\033[1;97m[Session Mode Locked -> Analyst]\033[0m\n"
            "  - Purpose:           Analyze local system data only; external network scanning blocked.\n"
            f"  - Network Isolation: \033[1;97m{iso_lvl} (AIR_GAPPED_NETNS — `lo` loopback only)\033[0m\n"
        )
    elif mode_tok in ("3", "berserker", "berserk", "aggressive"):
        iso_grp = netiso_tok if netiso_tok in ("1", "2", "red", "blue") else _prompt_berserker_or_ninja_netiso_group("Berserker", "\033[1;31m")
        if iso_grp == "__BACK__":
            return
        mode_key, iso_lvl, ifaces = apply_personality_mode("BERSERKER", netiso_group=iso_grp)
        iface_desc = "All" if iso_lvl == "RED" else (", ".join(ifaces) if ifaces else "eth0, eth1")
        print(
            "\n\033[1;31m[Session Mode Locked -> Berserker]\033[0m\n"
            "  - Purpose:           Aggressively pursue target goals using all available tools.\n"
            f"  - Network Isolation: \033[1;31m{iso_lvl}\033[0m (Interfaces: `{iface_desc}`)\n"
        )
    elif mode_tok in ("4", "ninja", "stealth", "covert"):
        iso_grp = netiso_tok if netiso_tok in ("1", "2", "red", "blue") else _prompt_berserker_or_ninja_netiso_group("Ninja", "\033[1;35m")
        if iso_grp == "__BACK__":
            return
        mode_key, iso_lvl, ifaces = apply_personality_mode("NINJA", netiso_group=iso_grp)
        iface_desc = "All" if iso_lvl == "RED" else (", ".join(ifaces) if ifaces else "eth0, eth1")
        print(
            "\n\033[1;35m[Session Mode Locked -> Ninja]\033[0m\n"
            "  - Purpose:           Find answers covertly using stealthy, low-noise commands only.\n"
            f"  - Network Isolation: \033[1;35m{iso_lvl}\033[0m (Interfaces: `{iface_desc}`)\n"
        )
    else:
        print(
            f"\n\033[1;31m[Unknown Mode `{mode_tok}`]\033[0m Choose `1` (`Default`), `2` (`Analyst`), `3` (`Berserker`), or `4` (`Ninja`), or type `/mode` for the interactive menu.\n"
        )
        return

    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
    HUD.render(force_region=False)


SWITCH_HELP_MAP: dict[str, str] = {
    "mode": (
        "=== Switch Help: /mode ===\n"
        "  Select or inspect the C.O.R.A. Session Personality & Logic Enforcement Mode (Unique per session):\n"
        "    [1] Default   (Default) : Standard operation with no behavioral guidance or extra restrictions. (9 words)\n"
        "    [2] Analyst             : Analyze local system data only; external network scanning blocked. (9 words; locks Network Isolation WHITE)\n"
        "    [3] Berserker           : Aggressively pursue target goals using all available tools. (8 words; prompts Red=All or Blue=Allowed NICs)\n"
        "    [4] Ninja               : Find answers covertly using stealthy, low-noise commands only. (8 words; prompts Red=All or Blue=Allowed NICs)\n"
        "  Usage:\n"
        "    /mode | /mode -mode:menu                  : Open interactive numbered Mode Selection Menu [1-4]\n"
        "    /mode status | /mode -mode:status         : Show active session personality mode and network isolation group\n"
        "    /mode -mode:<1|2|3|4|default|analyst|berserker|ninja> [-netiso:<red|blue>] : Switch session mode directly\n"
        "    /mode -h | /mode --help                   : Show this help message"
    ),
    "m": (
        "=== Switch Help: -m / --model ===\n"
        "  Select the active GGUF local LLM model to run on llama-server (127.0.0.1:8080):\n"
        "    -m 3.8       | -m:3.8       | --model 3.8       : Qwen3.8-27B-Uncensored-Q3_K_M (~13.5 GB VRAM, default)\n"
        "    -m q4        | -m:q4        | --model q4        : Qwen3.8-27B-Uncensored-Q4_K_M (~16.7 GB VRAM)\n"
        "    -m q6        | -m:q6        | --model q6        : Qwen3.8-27B-Uncensored-Q6_K (~22.0 GB VRAM)\n"
        "    -m 3.5       | -m:3.5       | --model 3.5       : Qwen3.5-9B-Uncensored-Q8_0 (~9.5 GB VRAM, fast)\n"
        "    -m turbo-q4  | -m:turbo-q4  | --model turbo-q4  : Qwen3.8-27B-Turbo-Uncensored-Q4_K_M (4-step distilled)\n"
        "    -m turbo-q8  | -m:turbo-q8  | --model turbo-q8  : Qwen3.8-27B-Turbo-Uncensored-Q8_0 (4-step distilled)\n"
        "    -m -h        | -m --help    | --model --help    : Show this help message"
    ),
    "netiso": (
        "=== Switch Help: -netiso / --network-isolation / /netiso / /posture ===\n"
        "  Configure C.O.R.A. Network Isolation & Security Posture (Red / White / Blue):\n"
        "    -netiso red              | /netiso -mode:red         : RED (UNRESTRICTED) — Full host network stack access\n"
        "    -netiso white            | /netiso -mode:white       : WHITE (AIR_GAPPED_NETNS) — Linux network namespace (`unshare -r -n`), loopback `lo` only\n"
        "    -netiso blue             | /netiso -mode:blue        : BLUE (ISOLATED_LAN_USB) — Lock to interfaces in `Network_Isolation/network_isolation.conf`\n"
        "    -netiso -blue:eth0,eth1  | /netiso -blue:eth0,eth1   : BLUE (ISOLATED_LAN_USB) — Lock strictly to `eth0,eth1` (also supports `-netiso blue eth0,eth1`)\n"
        "    /netiso status           | /posture -mode:status     : Display current active network isolation posture and allowed interfaces\n"
        "    /posture -mode:demo      | /posture demo             : Cycle through Red, Blue, and White terminal palettes\n"
        "    /posture -mode:reset     | /posture reset            : Restore default terminal background/foreground colors\n"
        "    -netiso -h | -netiso --help | /netiso -h | /netiso --help : Show this help message"
    ),
    "continue": (
        "=== Switch Help: -c / --continue / /continue ===\n"
        "  Restore and continue from the last saved C.O.R.A. CLI session (`last_cli_session.json` + `relentless_ledger.json`):\n"
        "    ./run_cora_NIX.sh cli -m 3.8 -c         : Launch CLI and immediately restore previous project, goal, wave, and messages\n"
        "    ./run_cora_NIX.sh cli -m 3.8 --continue : Same as `-c`\n"
        "    /continue | /resume                     : Restore the previous session from inside the running CLI\n"
        "    -c -h | -c --help | /continue -h | /continue --help : Show this help message"
    ),
    "project": (
        "=== Switch Help: -P / --project / /project ===\n"
        "  Manage isolated project workspaces inside `CORA/Projects/<project-name>/`:\n"
        "  (All spaces and special characters in project names are automatically converted to dashes `-`; parameters require a leading `-`)\n"
        "    /project | /project -mode:menu         : Open the interactive numbered Project Selection / Rename / Create menu\n"
        "    /project list | /project -mode:list    : List all current projects in `Projects/`\n"
        "    /project -new:<name>                   : Create a new project in `Projects/<name>/` and set it active (or `/project new` for interactive prompt)\n"
        "    /project -rename:<old>:<new>           : Rename `Projects/<old>/` -> `Projects/<new>/` (or `/project rename` for interactive Rename menu)\n"
        "    /project -load:<name> [\"<task>\"]       : Switch active project to `Projects/<name>/` (and optionally run `\"<task>\"`)\n"
        "    /project -doc:<path> [-name:<project>] : Ingest documentation file/folder into `Projects/<project>/memory.md`\n"
        "    -P:<doc_or_project> | -P <doc_path>    : Startup flag to select an existing project or onboard documentation\n"
        "    -P -h | --project --help | /project -h | /project --help : Show this help message"
    ),
    "files": (
        "=== Switch Help: /files / /file / /upload / /add ===\n"
        "  Manage and inspect the active project's local `Files` directory (`Projects/<project>/Files/`) for LLM interaction:\n"
        "    /files | /files list                   : List all custom scripts and files inside `Projects/<project>/Files/`\n"
        "    /files add <path> | /upload <path>     : Copy a local file or directory into `Projects/<project>/Files/`\n"
        "    /files read <filename>                 : Display the contents of `Projects/<project>/Files/<filename>`\n"
        "    /files rm <filename>                   : Delete a file inside `Projects/<project>/Files/`\n"
        "    /files -h | /files --help              : Show this help message"
    ),
    "goal": (
        "=== Switch Help: /goal ===\n"
        "  Set, inspect, or clear project-scoped mission objectives (`Projects/<project>/goals.md`):\n"
        "  (Goal text MUST be enclosed in quotation marks `\"...\"`; parameters MUST begin with a dash `-`)\n"
        "    /goal \"<objective text>\" [-max:<#>] : Append `\"<objective text>\"` to `Projects/<project>/goals.md`, lock active goal, and execute\n"
        "                                          (optional `-max:<#>` sets wave limit; use `-max:0` or `-max:unlimited` to never stop)\n"
        "    /goal | /goal status | -mode:status : Display the very last goal saved in `Projects/<project>/goals.md`\n"
        "    /goal list | /goal -mode:list       : List all historical goals appended in `Projects/<project>/goals.md`\n"
        "    /goal audit | /goal -mode:audit     : Display full Relentless Attempt Ledger & capability vector audit\n"
        "    /goal clear | /goal -mode:clear     : Clear the active in-memory goal and reset the session Attempt Ledger\n"
        "    /goal -h | /goal --help             : Show this help message"
    ),
    "relentless": (
        "=== Switch Help: /relentless ===\n"
        "  Control the Autonomous Multi-Wave `/relentless` Execution Controller:\n"
        "  (When setting a goal, the goal MUST be enclosed in quotation marks `\"...\"`; parameters MUST begin with `-`)\n"
        "    /relentless                             : Enable Relentless Mode and start looping on the active `/goal` until achieved\n"
        "    /relentless \"<goal text>\" [-max:<#>]    : Set `\"<goal text>\"` as the active goal and immediately start autonomous waves\n"
        "                                              Example: `/relentless \"You must try to the max and never stop\" -max:100`\n"
        "    /relentless -max:<#>                    : Set maximum autonomous waves per run (e.g. `-max:15`, `-max:100`)\n"
        "    /relentless -max:0                      : Set UNLIMITED waves (`0` / `-max:unlimited`) — never stop until goal is achieved or Ctrl+C\n"
        "    /relentless on  | -mode:on              : Arm persistent Relentless Mode\n"
        "    /relentless off | -mode:off             : Disable Relentless Mode and return to single-turn execution\n"
        "    /relentless status | -mode:status       : Show concise 3-line Relentless Mode status (Mode, Max Waves Cap, Active Goal)\n"
        "    /relentless audit  | -mode:audit        : Display full Relentless Controller Audit and Attempt Ledger\n"
        "    /relentless -h | /relentless --help     : Show this help message"
    ),
    "generate-report": (
        "=== Switch Help: /generate-report / /report ===\n"
        "  Generate a 5-Section Project Status & Findings Report (`Projects/<project>/REPORT.md` + `assets/report_dashboard.svg`):\n"
        "  (Includes Executive Summary, High-School Reading Level Walkthrough, SVG & Mermaid Graphics, Technical Evidence, and Conclusion)\n"
        "    /generate-report                          : Generate report for the active project (with LLM prose polish)\n"
        "    /generate-report -project:<name>          : Generate report for a specific project in `Projects/<name>/`\n"
        "    /generate-report -focus:<topic>           : Highlight a specific objective or finding in the report\n"
        "    /generate-report -mode:fast | --fast      : Instant deterministic report generation without waiting for LLM call\n"
        "    /generate-report -h | /generate-report --help | /report -h | /report --help : Show this help message"
    ),
    "rl": (
        "=== Switch Help: /rl ===\n"
        "  Control Engine 14/19 (Trajectory RL, Factored Network World-Model & Live Local Network Topology):\n"
        "    /rl | /rl status | -mode:status   : Predict optimal 3-step Pessimistic Q_LCB trajectory for the current goal\n"
        "    /rl <problem>                     : Compute 3-step RL rollout for `<problem>`\n"
        "    /rl topology | /rl -mode:topology : Sense live local NICs, gateways, ARP neighbors, and serial ports\n"
        "    /rl -train:<#> | /rl train        : Run offline simulated world-model Q-learning episodes (default: `400`, e.g. `/rl -train:500`)\n"
        "    /rl -h | /rl --help               : Show this help message"
    ),
    "pca": (
        "=== Switch Help: /pca / /kmeans ===\n"
        "  Control Engine 15/20 (Spectral PCA, K-Means++ Regime Clustering & Graph Laplacian Bottlenecks):\n"
        "    /pca | /pca status | -mode:status    : Run SVD PCA & K-Means++ clustering on the active problem/goal\n"
        "    /pca <problem>                       : Project `<problem>` into the 3D principal subspace and identify regime\n"
        "    /pca -mode:recompute | /pca recompute: Force full SVD/K-Means++ recomputation across all telemetry vectors\n"
        "    /pca -h | /pca --help | /kmeans -h   : Show this help message"
    ),
    "continual": (
        "=== Switch Help: --continual / /continual / /learn-mode ===\n"
        "  Control Engine 12/16 (5-Tier Continual Learning & Adaptive Plasticity):\n"
        "    /continual status | -mode:status         : Show 5-tier memory counts and continual learning state\n"
        "    /continual -mode:auto  | /continual auto : Enable automatic background continual learning after every tool call (default)\n"
        "    /continual -mode:start | /continual start: Force an immediate Dirichlet consolidation & Hedge calibration pass\n"
        "    /continual -mode:stop  | /continual stop : Freeze all continual learning weights and priors\n"
        "    /continual consolidate                   : Run on-demand Dirichlet forgetting and Meta-Arbiter Brier/ECE audit\n"
        "    --continual:<auto|start|stop>            : Startup CLI flag to set continual learning mode\n"
        "    --continual -h | /continual -h | /continual --help : Show this help message"
    ),
    "train": (
        "=== Switch Help: /train ===\n"
        "  Run the Multi-Modal Document & Image OCR Training Pipeline (`Training/` -> `core/ObsidianVault/`):\n"
        "    /train                               : Incremental training on `CORA/Training/`\n"
        "    /train -path:<folder>                : Train on documents/PDFs/images in `<folder>`\n"
        "    /train -mode:force | /train force    : Force full re-distillation of all files\n"
        "    /train status | /train -mode:status  : Show training ledger status and indexed document counts\n"
        "    /train -h | /train --help            : Show this help message"
    ),
    "reason": (
        "=== Switch Help: /reason / /mdp ===\n"
        "  Run the 15-Engine CPU-Only Neuro-Symbolic Reasoning Suite (`0 MB` GPU VRAM):\n"
        "    /reason <problem>                          : Run full 15-Engine 5-Layer Lexical Pipeline on `<problem>`\n"
        "    /reason status | -mode:status              : Show status of all 15 engines and learned weight files\n"
        "    /reason test   | -mode:test                : Run deterministic self-tests across all reasoning engines\n"
        "    /reason -engine:mdp [problem] | /mdp       : Run Engine 11 Hierarchical MDP Bellman planner\n"
        "    /reason -engine:rl [problem]               : Run Engine 14 Trajectory RL planner\n"
        "    /reason -engine:pca [problem]              : Run Engine 15 Spectral PCA & K-Means++ engine\n"
        "    /reason -engine:continual                  : Run Engine 12 Continual Learning engine\n"
        "    /reason -engine:meta                       : Run Engine 13 Hedge Meta-Arbiter & self-improvement audit\n"
        "    /reason -h | /reason --help | /mdp -h      : Show this help message"
    ),
    "hud": (
        "=== Switch Help: --hud / --no-hud / /hud ===\n"
        "  Control the Live Bottom-Pinned Hardware & Telemetry HUD Bar:\n"
        "    /hud on    | /hud -mode:on          : Enable the live hardware HUD\n"
        "    /hud off   | /hud -mode:off         : Disable the live hardware HUD\n"
        "    /hud pin   | /hud -mode:pin         : Pin single-line HUD to the bottom terminal row (default)\n"
        "    /hud prompt| /hud -mode:prompt      : Print HUD banner above each prompt\n"
        "    /hud title | /hud -mode:title       : Update terminal window title bar only\n"
        "    --hud | --no-hud                    : Startup flags to enable or disable the HUD\n"
        "    --hud -h | /hud -h | /hud --help    : Show this help message"
    ),
    "scan": (
        "=== Switch Help: /scan ===\n"
        "  Scan a target URL, API endpoint, or host and save the report to `Projects/<project>/targets/`:\n"
        "    /scan -target:<url_or_ip> | /scan <url_or_ip> : Probe HTTP headers, status, forms, endpoints, and JSON structure\n"
        "    /scan -h | /scan --help                       : Show this help message"
    ),
    "vault": (
        "=== Switch Help: /vault ===\n"
        "  Display the Long-Term Obsidian Knowledge Vault index (`ObsidianVault/00_MEMORY_INDEX.md`):\n"
        "    /vault                              : Print full hot memory index\n"
        "    /vault -h | /vault --help           : Show this help message"
    ),
    "remember": (
        "=== Switch Help: /remember ===\n"
        "  Save a permanent fact or rule into `ObsidianVault/knowledge/`:\n"
        "    /remember -fact:\"<text>\" | /remember \"<fact text>\" : Store `<fact text>` in long-term vault memory\n"
        "    /remember -h | /remember --help                    : Show this help message"
    ),
    "search": (
        "=== Switch Help: /search ===\n"
        "  Search across both the active `Projects/<project>/` workspace and `ObsidianVault/`:\n"
        "    /search -query:<keyword> | /search <keyword> : Search notes, targets, playbooks, and reasoning reports\n"
        "    /search -h | /search --help                  : Show this help message"
    ),
    "permissions": (
        "=== Switch Help: --confirm / --dangerously-skip-permissions / /permissions ===\n"
        "  Control confirmation prompts before executing shell commands or writing files:\n"
        "    /permissions                         : Toggle between AUTO-RUN and CONFIRM ON `[y/N/a]`\n"
        "    --confirm                            : Startup flag to require `[y/N/a]` confirmation before commands\n"
        "    --dangerously-skip-permissions       : Startup flag to auto-run tool calls without prompting (default in CLI)\n"
        "    --confirm -h | /permissions -h | /permissions --help : Show this help message"
    ),
    "state": (
        "=== Switch Help: /state / /context ===\n"
        "  Inspect the Zero-Loss Context Virtual Memory (Context VM) and L1 Symbolic State Register:\n"
        "    /state | /context                   : Show token budget usage, shadow archive file count, and L1 state\n"
        "    /state -h | /state --help           : Show this help message"
    ),
    "clear": (
        "=== Switch Help: /clear ===\n"
        "  Clear active conversation history while keeping Project Memory and ObsidianVault intact:\n"
        "    /clear                              : Reset conversation messages and refresh hardware snapshot\n"
        "    /clear -h | /clear --help           : Show this help message"
    ),
    "hw": (
        "=== Switch Help: /hw ===\n"
        "  Display live host hardware, CPU, RAM, GPU VRAM, and local network topology summary:\n"
        "    /hw                                 : Print live system snapshot\n"
        "    /hw -h | /hw --help                 : Show this help message"
    ),
    "think": (
        "=== Switch Help: --think / --no-think ===\n"
        "  Control Qwen3 Chain-of-Thought (`<think>`) reasoning budget on `llama-server`:\n"
        "    --no-think                          : Disable `<think>` blocks (`--reasoning-budget 0`, fastest, default)\n"
        "    --think                             : Enable full Chain-of-Thought `<think>` blocks (`--reasoning-budget -1`)\n"
        "    --think -h | --think --help         : Show this help message"
    ),
    "prompt": (
        "=== Switch Help: -p / --prompt ===\n"
        "  Execute a single non-interactive prompt and exit:\n"
        "    ./run_cora_NIX.sh cli -p \"Check listening ports\" : Run single prompt and exit\n"
        "    -p -h | -p --help | --prompt --help            : Show this help message"
    ),
    "keep-server": (
        "=== Switch Help: --keep-server / --keep-alive ===\n"
        "  Keep `llama-server` running in the background after exiting the CLI:\n"
        "    --keep-server                       : Do not stop `llama-server` on `/exit`\n"
        "    --keep-server -h | --keep-server --help : Show this help message"
    ),
    "exit": (
        "=== Switch Help: /exit / /quit ===\n"
        "  Save session state, consolidate continual learning weights, and exit C.O.R.A. CLI:\n"
        "    /exit | /quit | exit | quit         : Cleanly shut down CLI and background engines\n"
        "    /exit -h | /exit --help             : Show this help message"
    ),
}


def print_switch_help(switch_name: str = "") -> None:
    """Print detailed help for a specific switch (`-h`) or full CLI help if no switch is specified."""
    key = switch_name.strip().lstrip("-/").lower()
    alias_map = {
        "model": "m",
        "m": "m",
        "network-isolation": "netiso",
        "netiso": "netiso",
        "n": "netiso",
        "posture": "netiso",
        "red": "netiso",
        "white": "netiso",
        "blue": "netiso",
        "c": "continue",
        "continue": "continue",
        "resume": "continue",
        "p": "project" if switch_name.startswith("-P") else "prompt",
        "project": "project",
        "projects": "project",
        "files": "files",
        "file": "files",
        "upload": "files",
        "add": "files",
        "mode": "mode",
        "personality": "mode",
        "goal": "goal",
        "relentless": "relentless",
        "generate-report": "generate-report",
        "report": "generate-report",
        "rl": "rl",
        "pca": "pca",
        "kmeans": "pca",
        "continual": "continual",
        "learn-mode": "continual",
        "train": "train",
        "reason": "reason",
        "mdp": "reason",
        "hud": "hud",
        "no-hud": "hud",
        "scan": "scan",
        "vault": "vault",
        "remember": "remember",
        "search": "search",
        "permissions": "permissions",
        "confirm": "permissions",
        "dangerously-skip-permissions": "permissions",
        "state": "state",
        "context": "state",
        "clear": "clear",
        "hw": "hw",
        "think": "think",
        "no-think": "think",
        "prompt": "prompt",
        "keep-server": "keep-server",
        "keep-alive": "keep-server",
        "exit": "exit",
        "quit": "exit",
    }
    resolved = alias_map.get(key, key)
    if resolved and resolved in SWITCH_HELP_MAP:
        print(f"\n\033[1;36m{SWITCH_HELP_MAP[resolved]}\033[0m\n")
        return

    print("\n\033[1;36m=== C.O.R.A. (Cyber Oriented Reasoning Agent) CLI & Switch Help ===\033[0m")
    print("  Pass `-h` or `--help` after ANY startup switch or in-CLI `/` command for detailed options:\n")
    for k in (
        "m",
        "netiso",
        "continue",
        "project",
        "files",
        "mode",
        "goal",
        "relentless",
        "generate-report",
        "rl",
        "pca",
        "continual",
        "train",
        "reason",
        "hud",
        "scan",
        "vault",
        "remember",
        "search",
        "permissions",
        "state",
        "clear",
        "hw",
        "think",
        "prompt",
        "keep-server",
        "exit",
    ):
        lines = SWITCH_HELP_MAP[k].splitlines()
        header = lines[0].replace("=== Switch Help: ", "").replace(" ===", "")
        first_desc = lines[1].strip() if len(lines) > 1 else ""
        print(f"  \033[1;33m{header:<48}\033[0m {first_desc}")
    print("\n  Tip: Run `<switch> -h` (e.g., `-netiso -h`, `/project -h`, `/relentless -h`, `/rl -h`) to see all options for that switch.\n")


def _is_help_arg(val: str) -> bool:
    v = val.strip().lower()
    return v in ("-h", "--help", "help", "-?") or v.endswith(":-h") or v.endswith(":--help")


CLI_HISTORY_FILE = BASE_DIR / "Log" / "cli_command_history.json"
_CLI_HISTORY: list[str] = []
_CLI_BASE_VOCAB: list[str] = [
    "/help",
    "/exit",
    "/quit",
    "/continue",
    "/resume",
    "/project",
    "/files",
    "/file",
    "/upload",
    "/add",
    "/mode",
    "/mode:red_team",
    "/mode:blue_team",
    "/mode:hunt",
    "/mode:research",
    "/mode:analyst",
    "/mode:default",
    "/goal",
    "/relentless",
    "/relentless:on",
    "/relentless:off",
    "/generate-report",
    "/netiso",
    "/netiso:red",
    "/netiso:blue",
    "/netiso:white",
    "/rl",
    "/pca",
    "/continual",
    "/train",
    "/reason",
    "/hud",
    "/scan",
    "/vault",
    "/remember",
    "/search",
    "/permissions",
    "/state",
    "/clear",
    "/hw",
    "/think",
    "procdump.exe",
    "psexec.exe",
    "autorunsc.exe",
    "sysmon.exe",
    "accesschk.exe",
    "pslist.exe",
    "handle.exe",
    "pipelist.exe",
    "tcpvcon.exe",
    "sigcheck.exe",
    "strings.exe",
    "wevtutil.exe",
    "netstat.exe",
    "tasklist.exe",
    "reg.exe",
    "Get-CimInstance",
    "Get-Process",
    "Get-Service",
    "Get-WinEvent",
    "Get-NetTCPConnection",
    "powershell",
    "reconnaissance",
    "enumeration",
    "vulnerability",
    "exploitation",
    "privilege",
    "escalation",
    "persistence",
    "credentials",
    "lateral",
    "movement",
    "exfiltration",
    "telemetry",
    "mitigation",
    "remediation",
    "forensics",
    "incident",
    "response",
    "active_directory",
    "kerberoasting",
    "mimikatz",
    "bloodhound",
    "wireshark",
    "nmap",
    "metasploit",
    "localhost",
    "127.0.0.1",
]


def _load_cli_history() -> list[str]:
    global _CLI_HISTORY
    if _CLI_HISTORY:
        return _CLI_HISTORY
    try:
        if CLI_HISTORY_FILE.is_file():
            data = json.loads(CLI_HISTORY_FILE.read_text(encoding="utf-8", errors="ignore"))
            if isinstance(data, list):
                _CLI_HISTORY = [str(x).strip() for x in data if str(x).strip()][:150]
    except Exception:
        pass
    return _CLI_HISTORY


def _save_cli_history_entry(entry: str) -> None:
    global _CLI_HISTORY
    cleaned = (entry or "").strip()
    if not cleaned:
        return
    _load_cli_history()
    _CLI_HISTORY = [cleaned] + [x for x in _CLI_HISTORY if x != cleaned]
    _CLI_HISTORY = _CLI_HISTORY[:150]
    try:
        CLI_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        CLI_HISTORY_FILE.write_text(json.dumps(_CLI_HISTORY, indent=2), encoding="utf-8")
    except Exception:
        pass


def _get_cli_vocabulary() -> list[str]:
    words = list(_CLI_BASE_VOCAB)
    seen = {w.lower() for w in words}
    try:
        proj_ws = ensure_project_workspace()
        files_dir = proj_ws / "Files"
        if files_dir.is_dir():
            for f in sorted(files_dir.rglob("*")):
                if f.is_file():
                    rel = f.relative_to(files_dir).as_posix()
                    for cand in (f.name, f"Files/{rel}", f"Projects/{proj_ws.name}/Files/{rel}"):
                        if cand.lower() not in seen:
                            seen.add(cand.lower())
                            words.append(cand)
    except Exception:
        pass
    for hist_item in _load_cli_history():
        for tok in re.split(r"\s+", hist_item):
            clean = tok.strip(",.;:()[]{}\"'")
            if len(clean) >= 3 and clean.lower() not in seen:
                seen.add(clean.lower())
                words.append(clean)
    return words


def handle_files_command(arg_str: str, messages: list) -> None:
    """
    CLI handler for `/files`, `/file`, `/upload`, and `/add` to manage the active project's
    `Projects/<project>/Files/` directory so the LLM can inspect and interact with custom files/scripts.
    """
    proj_ws = ensure_project_workspace()
    slug = proj_ws.name
    files_dir = (proj_ws / "Files").resolve()
    files_dir.mkdir(parents=True, exist_ok=True)

    clean_arg = (arg_str or "").strip()
    low_arg = clean_arg.lower()

    if not clean_arg or low_arg in ("list", "-mode:list", "status", "-mode:status"):
        items = sorted([f for f in files_dir.rglob("*") if f.is_file()], key=lambda p: p.name.lower())
        print(f"\n\033[1;36m=== Project Local `Files` Directory (`Projects/{slug}/Files/`) ===\033[0m")
        print(f"  Full Host Path (`$PROJECT_FILES_DIR`): `{files_dir}`")
        print(f"  Total Files in `Files/`:               `{len(items)}`")
        if items:
            for idx, f in enumerate(items, 1):
                rel = f.relative_to(files_dir).as_posix()
                mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                print(f"    [{idx}] \033[1;32mFiles/{rel}\033[0m (`Projects/{slug}/Files/{rel}` — {f.stat().st_size} bytes, {mtime})")
        else:
            print(f"    (No files currently in `Projects/{slug}/Files/` — use `/files add <path>` or `/upload <path>` to add files)")
        print("  \033[2;37mTip: Anything placed in `Projects/" + slug + "/Files/` is automatically visible to the LLM.\033[0m\n")
        return

    if low_arg.startswith(("add ", "-add:", "-path:")):
        raw_p = re.sub(r"^(?:add\s+|-add:|-path:)", "", clean_arg, flags=re.I).strip().strip('"').strip("'")
        if not raw_p:
            print_switch_help("files")
            return
        src = Path(os.path.expandvars(os.path.expanduser(raw_p)))
        if not src.is_absolute():
            src = (Path.cwd() / src).resolve() if (Path.cwd() / src).exists() else (CORA_ROOT / src).resolve()
        else:
            src = src.resolve()
        if not src.exists():
            print(f"\n\033[1;31m[Files Error]\033[0m Local path not found: `{src}`\n")
            return
        added_list: list[Path] = []
        if src.is_file():
            dest = (files_dir / src.name).resolve()
            if src != dest:
                shutil.copy2(src, dest)
            added_list.append(dest)
            rel_in_proj = dest.relative_to(proj_ws).as_posix()
            update_project_memory_index(proj_ws, rel_in_proj, f"Added custom file to Files/ ({dest.stat().st_size} bytes)", ["files"])
        elif src.is_dir():
            sub_root = (files_dir / src.name).resolve()
            sub_root.mkdir(parents=True, exist_ok=True)
            for f in sorted(src.rglob("*")):
                if not f.is_file() or len(added_list) >= 100:
                    continue
                rel_sub = f.relative_to(src)
                dest = (sub_root / rel_sub).resolve()
                dest.parent.mkdir(parents=True, exist_ok=True)
                if f.resolve() != dest:
                    shutil.copy2(f, dest)
                added_list.append(dest)
            update_project_memory_index(proj_ws, f"Files/{src.name}/", f"Imported directory ({len(added_list)} files) to Files/", ["files"])

        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
        print(f"\n\033[1;32m[Added {len(added_list)} File(s) to `Projects/{slug}/Files/`]\033[0m")
        for f_added in added_list[:20]:
            rel_f = f_added.relative_to(files_dir).as_posix()
            print(f"  - `Projects/{slug}/Files/{rel_f}` ({f_added.stat().st_size} bytes)")
        print("  The LLM can now directly inspect, read, edit, or execute these files in `Projects/" + slug + "/Files/`.\n")
        return

    if low_arg.startswith(("read ", "cat ", "view ")):
        target_name = clean_arg.split(" ", 1)[1].strip().strip('"').strip("'")
        resolved = resolve_cli_project_file_path(target_name, for_write=False)
        if not resolved.is_file():
            print(f"\n\033[1;31m[Files Error]\033[0m File not found in `Projects/{slug}/Files/`: `{target_name}`\n")
            return
        txt = resolved.read_text(encoding="utf-8", errors="replace")
        print(f"\n\033[1;36m=== `Projects/{slug}/Files/{resolved.name}` ({resolved.stat().st_size} bytes) ===\033[0m\n{txt[:12000]}\n")
        return

    if low_arg.startswith(("rm ", "del ", "delete ")):
        target_name = clean_arg.split(" ", 1)[1].strip().strip('"').strip("'")
        raw_rel = target_name.replace("\\", "/").lstrip("/")
        if raw_rel.lower().startswith("files/"):
            raw_rel = raw_rel[6:]
        target_p = (files_dir / raw_rel).resolve()
        if not str(target_p).startswith(str(files_dir)) or target_p == files_dir or not target_p.exists():
            print(f"\n\033[1;31m[Files Error]\033[0m File not found inside `Projects/{slug}/Files/`: `{target_name}`\n")
            return
        if target_p.is_file():
            target_p.unlink()
        elif target_p.is_dir():
            shutil.rmtree(target_p)
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
        print(f"\n\033[1;32m[Removed]\033[0m Deleted `Projects/{slug}/Files/{raw_rel}`.\n")
        return

    # Otherwise, treat `/files <path>` as `/files add <path>` if `<path>` exists on disk
    cand_p = Path(os.path.expandvars(os.path.expanduser(clean_arg.strip('"').strip("'"))))
    if cand_p.exists() or (CORA_ROOT / cand_p).exists():
        handle_files_command(f"add {clean_arg}", messages)
        return

    print_switch_help("files")


def _compute_cli_autocomplete(buf: str, cycle_index: int = 0) -> tuple[str, str, list[str]]:
    """Return `(token, suffix, matches)` for the word at the end of `buf`."""
    if not buf:
        return "", "", []
    m = re.search(r"([/\\a-zA-Z0-9_.:-]+)$", buf)
    if not m:
        return "", "", []
    token = m.group(1)
    if len(token) < 2 and not token.startswith("/"):
        return "", "", []
    low = token.lower()
    matches = [w for w in _get_cli_vocabulary() if w.lower().startswith(low) and w.lower() != low][:8]
    if not matches:
        return token, "", []
    chosen = matches[cycle_index % len(matches)]
    suffix = chosen[len(token):]
    return token, suffix, matches


def _setup_posix_readline_completer() -> None:
    if readline is None:
        return
    try:
        _load_cli_history()
        for item in reversed(_CLI_HISTORY):
            readline.add_history(item)

        def _completer(text: str, state: int) -> str | None:
            low = (text or "").lower()
            options = [w for w in _get_cli_vocabulary() if w.lower().startswith(low)]
            return options[state] if state < len(options) else None

        readline.set_completer_delims(" \t\n;")
        readline.set_completer(_completer)
        readline.parse_and_bind("tab: complete")
        readline.parse_and_bind(r'"\C-o": "\C-a\C-k/ctrl-o\n"')
    except Exception:
        pass


def _read_interactive_cli_line(
    prompt_text: str,
    allow_autocomplete: bool = True,
    menu_redraw_fn=None,
) -> str:
    """
    Read an interactive CLI line with:
      - Real-time terminal window resize detection & full-viewport repaint (`redraw_cli_on_resize`)
      - Up/Down arrow history navigation (`_CLI_HISTORY`)
      - Live shaded ANSI ghost-text word autocomplete (`\\033[2;36m<suffix>\\033[0m`)
      - Tab key completion (`Tab` accepts shaded word completion)
    Falls back cleanly to standard `input(prompt_text)` when stdin/stdout is not a Windows console TTY.
    """
    global _ACTIVE_MENU_REDRAW_FN, _ACTIVE_PROMPT_REDRAW_FN
    if allow_autocomplete:
        _load_cli_history()

    if os.name != "nt" or not sys.stdin.isatty() or not sys.stdout.isatty():
        HUD._in_readline_input = True
        _ACTIVE_MENU_REDRAW_FN = menu_redraw_fn
        try:
            with _raw_terminal_output():
                raw_line = input(prompt_text)
        finally:
            HUD._in_readline_input = False
            _ACTIVE_MENU_REDRAW_FN = None
            _ACTIVE_PROMPT_REDRAW_FN = None
        if "\x0f" in raw_line:
            return "/ctrl-o"
        line = raw_line.strip()
        if menu_redraw_fn is None and _CLI_VIEW_STATE == "main_session":
            _append_session_transcript(f"{prompt_text}{line}\n")
        if allow_autocomplete and line and line != "/ctrl-o":
            _save_cli_history_entry(line)
        return line

    try:
        import msvcrt
    except ImportError:
        with _raw_terminal_output():
            line = input(prompt_text).strip()
        if menu_redraw_fn is None and _CLI_VIEW_STATE == "main_session":
            _append_session_transcript(f"{prompt_text}{line}\n")
        if allow_autocomplete and line:
            _save_cli_history_entry(line)
        return line

    stripped_prompt = prompt_text.lstrip("\n")
    leading_nl = "\n" * (len(prompt_text) - len(stripped_prompt))
    single_prompt = stripped_prompt
    vis_prompt_len = len(_ANSI_VIS_RE.sub("", single_prompt))

    buf: list[str] = []
    history_idx = -1
    draft_before_history = ""

    def _redraw() -> None:
        with HUD._lock, _raw_terminal_output():
            cols = max(24, shutil.get_terminal_size((80, 24)).columns)
            current_text = "".join(buf)
            _, suffix, _ = _compute_cli_autocomplete(current_text, 0) if allow_autocomplete else ("", "", [])
            avail_for_text = max(8, cols - 2 - vis_prompt_len)
            if len(current_text) > avail_for_text:
                disp_text = current_text[-avail_for_text:]
                suffix = ""
            else:
                disp_text = current_text
                max_suf = max(0, avail_for_text - len(disp_text))
                suffix = suffix[:max_suf]
            ghost_hint = f"\033[2;36m{suffix}\033[0m" if suffix else ""
            sys.stdout.write(f"\r{single_prompt}{disp_text}{ghost_hint}\033[K")
            if suffix:
                sys.stdout.write(f"\033[{len(suffix)}D")
            sys.stdout.flush()

    _ACTIVE_MENU_REDRAW_FN = menu_redraw_fn
    _ACTIVE_PROMPT_REDRAW_FN = _redraw
    HUD._in_interactive_input = True
    try:
        if leading_nl:
            with _raw_terminal_output():
                sys.stdout.write(leading_nl)
                sys.stdout.flush()
        _redraw()

        sz0 = shutil.get_terminal_size((80, 24))
        last_cols, last_rows = max(20, sz0.columns), max(6, sz0.lines)
        resize_pending = False
        resize_ts = 0.0
        last_hud_refresh = time.monotonic()

        while True:
            while not msvcrt.kbhit():
                now_m = time.monotonic()
                sz = shutil.get_terminal_size((80, 24))
                c_now, r_now = max(20, sz.columns), max(6, sz.lines)
                if (c_now, r_now) != (last_cols, last_rows):
                    last_cols, last_rows = c_now, r_now
                    resize_pending = True
                    resize_ts = now_m
                    HUD.begin_resize_transition(c_now, r_now)
                elif resize_pending and (now_m - resize_ts) >= 0.18:
                    resize_pending = False
                    redraw_cli_on_resize()
                    if leading_nl:
                        with _raw_terminal_output():
                            sys.stdout.write(leading_nl)
                            sys.stdout.flush()
                    _redraw()
                    last_hud_refresh = time.monotonic()
                elif not resize_pending and HUD.active and HUD.mode == "pin" and (now_m - last_hud_refresh) >= 1.5:
                    last_hud_refresh = now_m
                    HUD.render(force_region=False)
                time.sleep(0.04)

            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                current_text = "".join(buf)
                with HUD._lock, _raw_terminal_output():
                    sys.stdout.write(f"\r{single_prompt}{current_text}\033[K\n")
                    sys.stdout.flush()
                if menu_redraw_fn is None and _CLI_VIEW_STATE == "main_session":
                    _append_session_transcript(f"{leading_nl}{single_prompt}{current_text}\n")
                result = current_text.strip()
                if allow_autocomplete and result:
                    _save_cli_history_entry(result)
                return result
            if ch == "\x03":  # Ctrl+C
                raise KeyboardInterrupt
            if ch == "\x0f" and allow_autocomplete:  # Ctrl+O -> Expand/toggle LLM thought process & engine trace
                with _raw_terminal_output():
                    sys.stdout.write("\r\033[K\n")
                print_last_thinking_trace_cli()
                _redraw()
                continue
            if ch == "\x04":  # Ctrl+D / EOF
                if not buf:
                    raise EOFError
                continue
            if ch == "\t" and allow_autocomplete:  # Tab -> accept shaded autocomplete suffix
                current_text = "".join(buf)
                _, suffix, _ = _compute_cli_autocomplete(current_text, 0)
                if suffix:
                    buf.extend(list(suffix))
                    if not suffix.endswith((":", "/", "\\", "-")):
                        buf.append(" ")
                    _redraw()
                continue
            if ch in ("\x08", "\x7f"):  # Backspace
                if buf:
                    buf.pop()
                    _redraw()
                continue
            if ch in ("\x00", "\xe0"):  # Special key prefix (arrows, delete, etc.)
                key2 = msvcrt.getwch()
                if key2 == "H" and allow_autocomplete:  # Up arrow -> older command in history
                    if _CLI_HISTORY:
                        if history_idx == -1:
                            draft_before_history = "".join(buf)
                        if history_idx < len(_CLI_HISTORY) - 1:
                            history_idx += 1
                        buf = list(_CLI_HISTORY[history_idx])
                        _redraw()
                elif key2 == "P" and allow_autocomplete:  # Down arrow -> newer command in history
                    if history_idx > 0:
                        history_idx -= 1
                        buf = list(_CLI_HISTORY[history_idx])
                        _redraw()
                    elif history_idx == 0:
                        history_idx = -1
                        buf = list(draft_before_history)
                        _redraw()
                elif key2 == "M" and allow_autocomplete:  # Right arrow -> accept ghost completion if present
                    current_text = "".join(buf)
                    _, suffix, _ = _compute_cli_autocomplete(current_text, 0)
                    if suffix:
                        buf.extend(list(suffix))
                        _redraw()
                continue
            if ch >= " ":
                buf.append(ch)
                _redraw()
    finally:
        HUD._in_interactive_input = False
        _ACTIVE_MENU_REDRAW_FN = None
        _ACTIVE_PROMPT_REDRAW_FN = None


def main() -> None:
    global SKIP_PERMISSIONS, ACTIVE_PROJECT, ACTIVE_GOAL, ACTIVE_PERSONALITY_MODE, RELENTLESS_MODE, HUD_ENABLED, CONTINUAL_MODE, KEEP_SERVER_ON_EXIT, _SPECULATIVE_CACHE_REF, _ACTIVE_MESSAGES_REF, _PENDING_FIRST_COMMAND, _CLI_VIEW_STATE, _LAST_RESTORED_SESSION_INFO, _LAST_STARTUP_CONTINUE
    ensure_vault_structure()
    # Session personality mode is strictly unique to the current session (never inherited across sessions)
    ACTIVE_PERSONALITY_MODE = "DEFAULT"
    os.environ["CORA_PERSONALITY_MODE"] = "DEFAULT"

    args = sys.argv[1:]
    # Check for standalone `-h` / `--help` or `<switch> -h` / `<switch> --help`
    for i, a in enumerate(args):
        if _is_help_arg(a):
            if ":" in a and (a.lower().endswith(":-h") or a.lower().endswith(":--help")):
                print_switch_help(a.split(":", 1)[0])
            elif i > 0:
                print_switch_help(args[i - 1])
            elif i + 1 < len(args):
                print_switch_help(args[i + 1])
            else:
                print_switch_help("")
            sys.exit(0)

    filtered_args = []
    startup_project_doc = ""
    startup_project_name = ""
    startup_continual_mode = os.environ.get("CONTINUAL_LEARNING_MODE", "").strip().upper()
    startup_continue_session = os.environ.get("LLM_CONTINUE_SESSION", "0") == "1"
    startup_netiso_level = ""
    startup_netiso_ifaces = ""
    select_project_only = False
    idx = 0
    while idx < len(args):
        a = args[idx]
        a_low = a.lower()
        if idx + 1 < len(args) and _is_help_arg(args[idx + 1]):
            print_switch_help(a)
            sys.exit(0)
        if a_low == "--select-project-only":
            select_project_only = True
            idx += 1
        elif a_low == "--print-switches-table":
            posture = _refresh_active_posture(apply_osc=False, quiet=True)
            render_simplified_switches_table(posture)
            sys.exit(0)
        elif a_low in ("--version", "-v", "version"):
            v_info = get_cora_version_info()
            print(f"Version: {v_info['version']}")
            sys.exit(0)
        elif a == "--dangerously-skip-permissions":
            SKIP_PERMISSIONS = True
            idx += 1
        elif a == "--confirm":
            SKIP_PERMISSIONS = False
            idx += 1
        elif a == "--no-hud":
            HUD_ENABLED = False
            idx += 1
        elif a == "--hud":
            HUD_ENABLED = True
            idx += 1
        elif a in ("--keep-server", "--keep-alive"):
            KEEP_SERVER_ON_EXIT = True
            idx += 1
        elif a_low in ("-c", "--continue", "-continue", "--resume", "-resume", "continue", "resume"):
            startup_continue_session = True
            idx += 1
        elif a_low in ("--network-isolation", "-netiso", "--netiso", "-n"):
            if idx + 1 >= len(args):
                print("Error: --network-isolation / -netiso requires a color level: red, white, or blue [ifaces]", file=sys.stderr)
                sys.exit(2)
            startup_netiso_level = args[idx + 1].strip()
            idx += 2
            if startup_netiso_level.lower().startswith("blue") and ":" not in startup_netiso_level and "=" not in startup_netiso_level:
                if idx < len(args) and not args[idx].startswith("-") and args[idx].lower() not in ("-p", "--prompt", "continue", "resume"):
                    startup_netiso_ifaces = args[idx].strip()
                    idx += 1
        elif a_low.startswith(("--network-isolation=", "-netiso=", "--netiso=", "--network-isolation:", "-netiso:", "--netiso:")):
            startup_netiso_level = re.split(r"[:=]", a, maxsplit=1)[1].strip()
            idx += 1
            if startup_netiso_level.lower() == "blue" and idx < len(args) and not args[idx].startswith("-"):
                startup_netiso_ifaces = args[idx].strip()
                idx += 1
        elif a_low in ("-red", "--red"):
            startup_netiso_level = "red"
            idx += 1
        elif a_low in ("-white", "--white"):
            startup_netiso_level = "white"
            idx += 1
        elif a_low in ("-blue", "--blue"):
            startup_netiso_level = "blue"
            idx += 1
            if idx < len(args) and not args[idx].startswith("-") and args[idx].lower() not in ("-p", "--prompt", "continue", "resume"):
                startup_netiso_ifaces = args[idx].strip()
                idx += 1
        elif a_low.startswith(("-blue=", "--blue=", "-blue:", "--blue:")):
            startup_netiso_level = "blue"
            startup_netiso_ifaces = re.split(r"[:=]", a, maxsplit=1)[1].strip()
            idx += 1
        elif a in ("--continual", "--learn-mode") and idx + 1 < len(args):
            startup_continual_mode = args[idx + 1].strip().upper()
            idx += 2
        elif a.startswith(("--continual=", "--learn-mode=", "--continual:", "--learn-mode:")):
            startup_continual_mode = re.split(r"[:=]", a, maxsplit=1)[1].strip().upper()
            idx += 1
        elif a in ("-P", "--project"):
            if idx + 1 >= len(args):
                print("Error: --project requires a documentation file, directory path, or project name.", file=sys.stderr)
                sys.exit(2)
            startup_project_doc = args[idx + 1]
            idx += 2
            if idx < len(args) and not args[idx].startswith("-"):
                startup_project_name = args[idx]
                idx += 1
        elif a.startswith(("--project=", "--project:", "-P:", "-P=")):
            startup_project_doc = re.split(r"[:=]", a, maxsplit=1)[1]
            idx += 1
        elif a in ("posture", "-detect", "--detect", "--status"):
            idx += 1
        elif a in ("--posture", "-posture"):
            if idx + 1 < len(args) and not args[idx + 1].startswith("-"):
                startup_netiso_level = args[idx + 1].strip()
                idx += 2
            else:
                idx += 1
        else:
            filtered_args.append(a)
            idx += 1

    if startup_netiso_level:
        apply_network_isolation_level(startup_netiso_level, startup_netiso_ifaces, record_cli_override=True)
    elif os.environ.get("LLM_ISOLATION_MODE"):
        apply_network_isolation_level(
            os.environ.get("LLM_ISOLATION_MODE", "red"),
            os.environ.get("LLM_ALLOWED_IFACES", ""),
            record_cli_override=bool(os.environ.get("LLM_CLI_BLUE_IFACES", "").strip()),
        )

    if select_project_only:
        chosen = interactive_project_selection_menu(require_selection=True, prompt_mode_after=True)
        _persist_selected_project(chosen)
        write_active_session_mode_env()
        posture = _refresh_active_posture(apply_osc=True, quiet=True)
        render_cora_splash_screen(posture)
        return

    if startup_continual_mode in ("AUTO", "START", "STOP"):
        try:
            from Reasoning.engines.continual_learner import set_continual_learning_mode

            set_continual_learning_mode(startup_continual_mode)
            CONTINUAL_MODE = startup_continual_mode
        except Exception:
            pass
    else:
        CONTINUAL_MODE = _get_live_continual_mode()

    messages = [{"role": "system", "content": build_system_prompt()}]
    _ACTIVE_MESSAGES_REF = messages
    restored_session_info: dict = {}
    if startup_continue_session:
        restored_session_info = restore_last_cli_session(messages)

    if len(filtered_args) > 1 and filtered_args[0] in ("-p", "--prompt"):
        if _is_help_arg(filtered_args[1]):
            print_switch_help("prompt")
            return
        prompt_text = " ".join(filtered_args[1:])
        messages.append({"role": "user", "content": prompt_text})
        run_turn(messages)
        return

    perm_status = (
        "\033[1;31mAUTO-RUN (--dangerously-skip-permissions enabled)\033[0m"
        if SKIP_PERMISSIONS
        else "\033[1;32mCONFIRM ON [y/N/a] (pass --dangerously-skip-permissions to auto-run)\033[0m"
    )

    posture = _refresh_active_posture(apply_osc=True, quiet=True)
    _start_cli_llama_keepalive_watchdog()
    atexit.register(_shutdown_cli_and_engines, True, True)
    for _sig_name in ("SIGHUP", "SIGTERM", "SIGBREAK"):
        _sig_obj = getattr(signal, _sig_name, None)
        if _sig_obj is not None:
            try:
                signal.signal(_sig_obj, lambda signum, frame: (_shutdown_cli_and_engines(True, True), sys.exit(0)))
            except Exception:
                pass

    p_border = posture.get("ansi_border", "\033[1;32m")
    p_accent = posture.get("ansi_accent", "\033[1;32m")
    p_badge = posture.get("banner_badge", "[POSTURE: UNRESTRICTED]")
    p_hud_badge = posture.get("hud_badge", "NET:UNRESTRICTED")
    p_bg = posture.get("bg_hex", "#1C0A0D")
    p_fg = posture.get("fg_hex", "#FFE8E8")
    p_ifaces = posture.get("allowed_interfaces") or []

    pending_onboarding_doc = ""
    if startup_project_doc:
        # Check if `startup_project_doc` is an existing or new project name in `Projects/` rather than a doc path
        cand_existing = slugify_project_name(startup_project_doc)
        doc_path_candidate = Path(os.path.expanduser(startup_project_doc))
        looks_like_doc_path = (
            doc_path_candidate.exists()
            or "/" in startup_project_doc
            or "\\" in startup_project_doc
            or doc_path_candidate.suffix.lower() in (".md", ".txt", ".pdf", ".json", ".yaml", ".yml", ".rst", ".html")
        )
        if cand_existing and ((PROJECTS_DIR / cand_existing).is_dir() or not looks_like_doc_path):
            ensure_project_workspace(cand_existing)
            _persist_selected_project(cand_existing)
            print(f"\033[1;32m[Active Project Selected]\033[0m `Projects/{cand_existing}/` (`Projects/{cand_existing}/Files/` ready)\n")
        else:
            try:
                derived_name, _ = load_documentation_source(startup_project_doc)
                proj_slug = slugify_project_name(startup_project_name) if startup_project_name else slugify_project_name(derived_name)
                _persist_selected_project(proj_slug)
                pending_onboarding_doc = startup_project_doc
            except Exception as exc:
                print(f"\n\033[1;31m[Project Error]\033[0m {exc}\n")

    # 1. Require a project in `/Projects` to be selected or created, followed immediately by selecting
    #    the session-unique Personality & Logic Enforcement Mode (`Default`, `Analyst`, `Berserker`, `Ninja`).
    if not ACTIVE_PROJECT:
        chosen_proj = interactive_project_selection_menu(require_selection=True, prompt_mode_after=True)
        _persist_selected_project(chosen_proj)
    else:
        m_res = interactive_personality_mode_menu(ACTIVE_PROJECT, allow_back_to_project=True)
        if m_res == "__BACK__":
            chosen_proj = interactive_project_selection_menu(require_selection=True, prompt_mode_after=True)
            _persist_selected_project(chosen_proj)

    posture = _refresh_active_posture(apply_osc=True, quiet=True)
    messages[0] = {"role": "system", "content": build_system_prompt(force_refresh_hw=False)}
    _CLI_VIEW_STATE = "main_session"
    _LAST_RESTORED_SESSION_INFO = restored_session_info
    _LAST_STARTUP_CONTINUE = startup_continue_session
    _SESSION_TRANSCRIPT_CHUNKS.clear()
    HUD.render(force_region=False)

    # 2. Once Project and Mode have been selected, display the main C.O.R.A. login splash banner page
    with _raw_terminal_output():
        render_cora_splash_screen(posture)
        render_session_intro_banner(
            posture=posture,
            restored_session_info=restored_session_info,
            startup_continue_session=startup_continue_session,
        )
    if startup_continue_session and restored_session_info.get("restored"):
        HUD.render(force_region=False)

    if pending_onboarding_doc:
        try:
            start_project_onboarding(pending_onboarding_doc, startup_project_name, messages, prompt_mode=False)
        except Exception as exc:
            print(f"\n\033[1;31m[Project Error]\033[0m {exc}\n")

    speculative_cache = None
    try:
        from Reasoning.engines.context_vm import SpeculativeLookaheadCache

        speculative_cache = SpeculativeLookaheadCache()
        _SPECULATIVE_CACHE_REF = speculative_cache
    except Exception:
        pass

    _setup_posix_readline_completer()
    if HUD_ENABLED:
        HUD.start()

    while True:
        if HUD.active:
            HUD.render_before_prompt()
        if speculative_cache is not None and CONTINUAL_MODE != "STOP":
            speculative_cache.prewarm_async(ACTIVE_GOAL or "")
        cur_posture = ACTIVE_POSTURE or _refresh_active_posture()
        p_prompt_col = cur_posture.get("ansi_prompt", "\033[1;32m")
        p_short = cur_posture.get("short_tag", "UNRESTRICTED")
        p_col = _rl_wrap(p_prompt_col)
        p_rst = _rl_wrap("\033[0m")
        if _PENDING_FIRST_COMMAND:
            user_input = _PENDING_FIRST_COMMAND
            _PENDING_FIRST_COMMAND = ""
            _save_cli_history_entry(user_input)
        else:
            try:
                user_input = _read_interactive_cli_line(f"{p_col}[{p_short}:{get_active_project_slug()}] You>{p_rst} ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                _shutdown_cli_and_engines(stop_llm=True, quiet=False)
                break
        if speculative_cache is not None:
            if hasattr(speculative_cache, "stop"):
                speculative_cache.stop()

        if not user_input:
            continue
        if HUD.active and HUD.mode == "pin":
            HUD.clear_bottom_row()

        # Universal `-h` / `--help` / `/help` handler for every `/` slash switch
        if user_input.startswith("/"):
            slash_tokens = user_input.split()
            slash_cmd_name = slash_tokens[0].lstrip("/").split(":", 1)[0].lower()
            if slash_cmd_name in ("help", "h", "?"):
                target_sw = slash_tokens[1] if len(slash_tokens) > 1 else ""
                print_switch_help(target_sw)
                continue
            if _is_help_arg(slash_tokens[0]) or any(_is_help_arg(tok) for tok in slash_tokens[1:]):
                print_switch_help(slash_cmd_name)
                continue

        if user_input.lower() in ("/exit", "exit", "quit", "/quit"):
            print("Exiting...")
            _shutdown_cli_and_engines(stop_llm=True, quiet=False)
            break
        if user_input.lower() in ("/continue", "/resume"):
            r_info = restore_last_cli_session(messages)
            if r_info.get("restored"):
                print(
                    f"\n\033[1;32m=== Session Restored (`{r_info.get('source')}`) ===\033[0m\n"
                    f"  Saved At:       `{r_info.get('saved_at')}`\n"
                    f"  Active Project: `{r_info.get('active_project') or 'None'}`\n"
                    f"  Active Goal:    `{r_info.get('active_goal') or 'None'}`\n"
                    f"  History Loaded: `{r_info.get('message_count')}` messages | `{r_info.get('attempt_count')}` tool attempts (Wave `{r_info.get('current_wave')}`)\n"
                )
                interactive_personality_mode_menu(ACTIVE_PROJECT, allow_back_to_project=False)
                if messages and messages[0].get("role") == "system":
                    messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
            else:
                print(f"\n\033[1;33m[Continuation]\033[0m {r_info.get('reason', 'No previous session found.')}\n")
            HUD.render(force_region=False)
            continue
        if (
            user_input.lower() == "/mode"
            or user_input.lower().startswith("/mode ")
            or user_input.lower().startswith("/mode/")
        ):
            arg_str = re.sub(r"^/mode(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            handle_mode_command(arg_str, messages)
            continue
        if (
            user_input.lower() == "/posture"
            or user_input.lower().startswith("/posture ")
            or user_input.lower() == "/netiso"
            or user_input.lower().startswith("/netiso ")
        ):
            p_arg = re.sub(r"^/(?:posture|netiso)\s*", "", user_input, flags=re.I).strip()
            p_low = p_arg.lower()
            if p_low.startswith(("-mode ", "mode ")):
                v_m = re.sub(r"^-?mode\s+", "", p_arg, flags=re.I).strip()
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-mode:<value>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/netiso -mode:{v_m}`.\n"
                )
                continue
            if p_low.startswith("mode:") or p_low.startswith("blue:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{p_arg}` instead of `{p_arg}`.\n"
                )
                continue
            if p_low.startswith(("-mode:", "--mode:")):
                p_arg = p_arg.split(":", 1)[1].strip()
                p_low = p_arg.lower()
            elif p_low.startswith(("-blue:", "--blue:")):
                p_arg = "blue:" + p_arg.split(":", 1)[1].strip()
                p_low = p_arg.lower()
            try:
                from Network_Isolation.console_posture import format_posture_banner, reset_console_posture

                if p_low == "reset":
                    reset_console_posture(quiet=False, force_osc=True)
                elif p_low in ("demo", "test"):
                    for m_key in ("UNRESTRICTED", "ISOLATED_LAN_USB", "AIR_GAPPED_NETNS"):
                        _refresh_active_posture(override=m_key, apply_osc=True, quiet=False)
                        HUD.render(force_region=False)
                        time.sleep(1.2)
                    _refresh_active_posture(override="", apply_osc=True, quiet=False)
                    HUD.render(force_region=False)
                elif p_low in ("", "status", "detect", "auto"):
                    info = _refresh_active_posture(override="", apply_osc=True, quiet=True)
                    HUD.render(force_region=False)
                    print("\n" + format_posture_banner(info) + "\n")
                else:
                    parts_p = p_arg.split(maxsplit=1)
                    lvl_tok = parts_p[0]
                    ifaces_tok = parts_p[1] if len(parts_p) > 1 else ""
                    if (
                        (ACTIVE_PERSONALITY_MODE or "DEFAULT").upper() == "ANALYST"
                        and lvl_tok.lower().split(":", 1)[0] not in ("white", "netns", "namespace", "airgap", "airgapped", "air_gapped_netns")
                    ):
                        print(
                            "\n\033[1;31m[Analyst Mode Restriction]\033[0m Analyst Mode strictly enforces Network Isolation `WHITE` (`lo` loopback only; no external network access).\n"
                            "  To use `Red` or `Blue` network isolation, switch your session mode first with `/mode`.\n"
                        )
                        continue
                    apply_network_isolation_level(lvl_tok, ifaces_tok)
                    write_active_session_mode_env()
                    info = _refresh_active_posture(override="", apply_osc=True, quiet=True)
                    HUD.render(force_region=False)
                    messages[0] = {"role": "system", "content": build_system_prompt(force_refresh_hw=False)}
                    print("\n" + format_posture_banner(info) + "\n")
            except Exception as exc:
                print(f"\n[Posture Error]: {exc}\n")
            continue
        if user_input.lower() == "/hud" or user_input.lower().startswith("/hud "):
            h_arg = user_input[4:].strip().lower()
            if h_arg.startswith(("-mode ", "mode ")):
                v_h = re.sub(r"^-?mode\s+", "", h_arg, flags=re.I).strip()
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-mode:<value>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/hud -mode:{v_h}`.\n"
                )
                continue
            if h_arg.startswith("mode:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{h_arg}` instead of `{h_arg}`.\n"
                )
                continue
            if h_arg.startswith(("-mode:", "--mode:")):
                h_arg = h_arg.split(":", 1)[1].strip()
            if h_arg in ("prompt", "title", "pin"):
                was_active = HUD.active
                if was_active:
                    HUD.stop()
                HUD.mode = h_arg
                HUD.start()
                print(f"Hardware HUD mode set to `{h_arg}`.\n")
            elif h_arg == "on" or (h_arg == "" and not HUD.active):
                HUD.start()
                print(f"Hardware HUD enabled (mode: `{HUD.mode}`).\n")
            else:
                HUD.stop()
                print("Hardware HUD disabled.\n")
            continue
        if user_input.lower() == "/clear":
            messages = [{"role": "system", "content": build_system_prompt(force_refresh_hw=True)}]
            _SESSION_TRANSCRIPT_CHUNKS.clear()
            if sys.stdout.isatty():
                redraw_cli_on_resize()
            print("Conversation history cleared (Obsidian Vault memory & L1 Symbolic State remain active).\n")
            continue
        if user_input.lower() in ("/ctrl-o", "/ctrlo", "/think", "/think-view", "/thinking"):
            print_last_thinking_trace_cli()
            continue
        if user_input.lower() in ("/state", "/context"):
            try:
                from Reasoning.engines.context_vm import build_dynamic_l1_state_block, count_tokens_exact_or_est, query_server_n_ctx
                from Reasoning.engines.vault_bridge import SHADOW_ARCHIVE_DIR

                total_toks = count_tokens_exact_or_est(json.dumps(messages))
                n_ctx = query_server_n_ctx()
                proj_shadow_dir = ensure_project_workspace() / "shadow_archive"
                shadow_files = (
                    (len(list(Path(SHADOW_ARCHIVE_DIR).glob("sha256_*.log"))) if Path(SHADOW_ARCHIVE_DIR).is_dir() else 0)
                    + (len(list(proj_shadow_dir.glob("sha256_*.log"))) if proj_shadow_dir.is_dir() else 0)
                )
                l1_block = build_dynamic_l1_state_block()
                print(
                    f"\n\033[1;36m=== Zero-Loss Context VM & L1 Symbolic State ===\033[0m\n"
                    f"  Context Budget: `{total_toks}` / `{n_ctx}` tokens ({len(messages)} messages in active window)\n"
                    f"  Shadow Archive: `{shadow_files}` lossless log files in `{proj_shadow_dir}` & `{SHADOW_ARCHIVE_DIR}`\n"
                    f"  {l1_block or '[L1 Symbolic State Register] Ready'}\n"
                )
            except Exception as exc:
                print(f"\n[State Error]: {exc}\n")
            continue
        if user_input.lower() == "/hw":
            print("\n" + get_live_hardware_summary() + "\n")
            continue
        if user_input.lower() == "/vault":
            print(f"\n\033[1;36m=== Obsidian Vault ({VAULT_DIR}) ===\033[0m")
            print(INDEX_FILE.read_text(encoding="utf-8", errors="replace"))
            continue
        if user_input.lower() == "/remember" or user_input.lower().startswith("/remember "):
            fact = user_input[9:].strip()
            if not fact:
                print_switch_help("remember")
                continue
            if fact.lower().startswith("fact:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{fact}` instead of `{fact}`.\n"
                )
                continue
            if fact.lower().startswith(("-fact:", "--fact:")):
                fact = fact.split(":", 1)[1].strip()
            fact = fact.strip("\"'")
            if fact:
                slug = slugify(fact[:40])
                msg = save_note_to_vault("knowledge", slug, fact[:90], fact, ["remembered", "fact"], persist_long_term=True)
                print(f"\n\033[1;32m{msg}\033[0m\n")
            continue
        if user_input.lower() == "/search" or user_input.lower().startswith("/search "):
            q = user_input[7:].strip()
            if not q:
                print_switch_help("search")
                continue
            if q.lower().startswith("query:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{q}` instead of `{q}`.\n"
                )
                continue
            if q.lower().startswith(("-query:", "--query:")):
                q = q.split(":", 1)[1].strip()
            q = q.strip("\"'")
            if q:
                print("\n" + search_vault(q) + "\n")
            continue
        if user_input.lower() == "/permissions":
            SKIP_PERMISSIONS = not SKIP_PERMISSIONS
            HUD.render(force_region=False)
            state = "AUTO-RUN (no confirmation)" if SKIP_PERMISSIONS else "CONFIRM ON ([y/N/a] before commands/writes)"
            print(f"Permissions mode set to: {state}\n")
            continue
        if (
            user_input.lower() == "/generate-report"
            or user_input.lower().startswith("/generate-report ")
            or user_input.lower().startswith("/generate-report/")
            or user_input.lower() == "/report"
            or user_input.lower().startswith("/report ")
            or user_input.lower().startswith("/report/")
        ):
            arg_str = re.sub(r"^/(?:generate-report|report)(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            handle_generate_report_command(arg_str)
            continue
        if (
            user_input.lower() == "/goal"
            or user_input.lower().startswith("/goal ")
            or user_input.lower().startswith("/goal/")
        ):
            arg_str = re.sub(r"^/goal(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            handle_goal_command(arg_str, messages)
            continue
        if (
            user_input.lower() == "/relentless"
            or user_input.lower().startswith("/relentless ")
            or user_input.lower().startswith("/relentless/")
        ):
            arg_str = re.sub(r"^/relentless(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            handle_relentless_command(arg_str, messages)
            continue
        if (
            user_input.lower() == "/train"
            or user_input.lower().startswith("/train ")
            or user_input.lower().startswith("/train/")
        ):
            t_arg = re.sub(r"^/train(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            m_bad_tr = re.match(r"^-?(path|mode)\s+(\S+.*)$", t_arg, flags=re.I)
            if m_bad_tr:
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-{m_bad_tr.group(1).lower()}:<value>` (with a leading dash `-` and colon `:`) instead of a space — "
                    f"e.g. `/train -{m_bad_tr.group(1).lower()}:{m_bad_tr.group(2).strip()}`.\n"
                )
                continue
            if any(p.lower().startswith(("path:", "mode:")) for p in t_arg.split()):
                bad_p = next(p for p in t_arg.split() if p.lower().startswith(("path:", "mode:")))
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{bad_p}` instead of `{bad_p}`.\n"
                )
                continue
            try:
                from Reasoning.train_llm import get_training_status, resolve_training_target, run_training_pipeline

                if t_arg.lower() in ("status", "-mode:status", "--mode:status"):
                    print("\n\033[1;36m=== Multi-Modal Training & OCR Distillation Status ===\033[0m")
                    print(json.dumps(get_training_status(), indent=2) + "\n")
                else:
                    force_flag = False
                    parts = [p for p in t_arg.split() if p]
                    target_folder = ""
                    for p in parts:
                        p_low = p.lower()
                        if p_low in ("--force", "-f", "force", "-mode:force", "--mode:force"):
                            force_flag = True
                        elif p_low.startswith(("-path:", "--path:")):
                            target_folder = p.split(":", 1)[1].strip()
                        elif not target_folder:
                            target_folder = p
                    train_target = resolve_training_target(target_folder)
                    tr_summary = run_training_pipeline(target_path=train_target, force=force_flag, use_llm=True, quiet=False)
                    if tr_summary and tr_summary.get("newly_trained_files", 0) > 0:
                        v_upd = get_cora_version_info()
                        print(f"  \033[1;35m[C.O.R.A. Version Updated]\033[0m `v{v_upd['version']}` (3rd decimal bumped on retraining)\n")
                    # Refresh system prompt so newly trained rules/index are immediately visible
                    messages[0] = {"role": "system", "content": build_system_prompt(force_refresh_hw=False)}
            except Exception as exc:
                print(f"\n\033[1;31m[Training Error]\033[0m {exc}\n")
            continue
        if (
            user_input.lower() == "/project"
            or user_input.lower().startswith("/project ")
            or user_input.lower().startswith("/project/")
            or user_input.lower().startswith("/projects/")
        ):
            arg_str = re.sub(r"^/projects?(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            handle_project_command(arg_str, messages)
            continue
        if (
            user_input.lower() in ("/files", "/file", "/upload", "/add")
            or user_input.lower().startswith(("/files ", "/file ", "/upload ", "/add "))
        ):
            cmd_head = user_input.split(maxsplit=1)[0].lower()
            arg_str = user_input.split(maxsplit=1)[1].strip() if " " in user_input else ""
            if cmd_head in ("/upload", "/add") and arg_str and not arg_str.lower().startswith(("add ", "list", "read ", "rm ")):
                arg_str = f"add {arg_str}"
            handle_files_command(arg_str, messages)
            continue
        if (
            user_input.lower() == "/continual"
            or user_input.lower().startswith("/continual ")
            or user_input.lower().startswith("/continual/")
            or user_input.lower() == "/learn-mode"
            or user_input.lower().startswith("/learn-mode ")
        ):
            c_arg = re.sub(r"^/(?:continual|learn-mode)(?:\s+|/|$)", "", user_input, flags=re.I).strip().lower()
            if c_arg.startswith(("-mode ", "mode ")):
                v_c = re.sub(r"^-?mode\s+", "", c_arg, flags=re.I).strip()
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-mode:<value>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/continual -mode:{v_c}`.\n"
                )
                continue
            if c_arg.startswith("mode:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{c_arg}` instead of `{c_arg}`.\n"
                )
                continue
            if c_arg.startswith(("-mode:", "--mode:")):
                c_arg = c_arg.split(":", 1)[1].strip()
            try:
                from Reasoning.engines.continual_learner import (
                    get_continual_learning_state,
                    run_continual_learning_reasoning,
                    set_continual_learning_mode,
                )
                from Reasoning.engines.meta_learner import run_meta_learning_reasoning

                if c_arg in ("auto", "start", "stop"):
                    st = set_continual_learning_mode(c_arg.upper())
                    CONTINUAL_MODE = st.get("mode", c_arg.upper())
                    HUD.render(force_region=False)
                    print(
                        f"\n\033[1;32mEngine 16 Continual Learning mode set to `{CONTINUAL_MODE}`\033[0m "
                        f"(persisted in `Reasoning/data/continual_learning_state.json`).\n"
                    )
                    if CONTINUAL_MODE == "START":
                        res_c = run_continual_learning_reasoning(
                            problem="Manual START Continual Consolidation & Dirichlet Forgetting Pass",
                            force_decay=True,
                            export_to_vault=True,
                        )
                        res_m = run_meta_learning_reasoning(
                            problem="Manual START Hedge Meta-Arbiter Calibration Audit",
                            write_suggested_improvement=True,
                            export_to_vault=True,
                        )
                        print(f"\033[1;36m{res_c['markdown']}\033[0m\n")
                        print(f"\033[1;35mMeta-Learning Audit saved: {res_m.get('suggested_improvement_note')}\033[0m\n")
                elif c_arg in ("consolidate", "decay", "audit"):
                    res_c = run_continual_learning_reasoning(
                        problem="On-Demand Continual Plasticity & Dirichlet Consolidation",
                        force_decay=True,
                        export_to_vault=True,
                    )
                    res_m = run_meta_learning_reasoning(
                        problem="On-Demand Hedge Meta-Arbiter & Brier/ECE Audit",
                        write_suggested_improvement=True,
                        export_to_vault=True,
                    )
                    print(f"\n\033[1;36m{res_c['markdown']}\033[0m\n")
                    print(f"\033[1;35m{res_m['markdown']}\033[0m\n")
                else:
                    st = get_continual_learning_state()
                    CONTINUAL_MODE = str(st.get("mode", "AUTO")).upper()
                    HUD.render(force_region=False)
                    print("\n\033[1;36m=== Engine 16 Continual Learning & 5-Tier Memory Status ===\033[0m")
                    print(json.dumps(st, indent=2) + "\n")
                    print("Usage: `/continual -mode:auto` | `/continual -mode:start` | `/continual -mode:stop` | `/continual consolidate`\n")
            except Exception as exc:
                print(f"\n\033[1;31m[Continual Learner Error]\033[0m {exc}\n")
            continue
        if (
            user_input.lower() == "/rl"
            or user_input.lower().startswith("/rl ")
            or user_input.lower().startswith("/rl/")
        ):
            rl_arg = re.sub(r"^/rl(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            try:
                from Reasoning.engines.rl_network_policy import (
                    run_rl_network_policy_reasoning,
                    run_rl_training_cycle,
                    sense_live_local_network_topology,
                )

                low_rl = rl_arg.lower()
                if low_rl.startswith(("train:", "mode:")):
                    print(
                        f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{rl_arg}` instead of `{rl_arg}`.\n"
                    )
                    continue
                if low_rl in ("topology", "topo", "net", "network", "-mode:topology", "--mode:topology"):
                    topo = sense_live_local_network_topology(force_refresh=True, export_to_vault=True)
                    print("\n\033[1;36m=== Live Local Network Topology (`[[targets/local_network_topology]]`) ===\033[0m")
                    print(json.dumps(topo, indent=2) + "\n")
                elif low_rl in ("train", "-train") or low_rl.startswith(("-train:", "--train:", "train ", "-train ")):
                    if low_rl.startswith(("train ", "-train ")):
                        val_t = re.sub(r"^-?train\s+", "", rl_arg, flags=re.I).strip()
                        print(
                            f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-train:<#>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/rl -train:{val_t or '400'}`.\n"
                        )
                        continue
                    n_ep = 400
                    if low_rl.startswith(("-train:", "--train:")):
                        ep_str = rl_arg.split(":", 1)[1].strip()
                        if ep_str.isdigit() and int(ep_str) >= 1:
                            n_ep = int(ep_str)
                        else:
                            print("\n\033[1;31mUsage:\033[0m `/rl -train:<#>` (e.g. `/rl -train:400`)\n")
                            continue
                    stats = run_rl_training_cycle(episodes=n_ep, export_to_vault=True)
                    print(
                        f"\n\033[1;32m[Engine 19 RL Training Complete]\033[0m Trained `{stats['episodes_run']}` episodes in `{stats['elapsed_ms']} ms` "
                        f"(Success rate=`{stats['goal_reach_rate']*100:.1f}%`, Total episodes=`{stats['total_episodes_trained']}`).\n"
                        f"Exported playbooks to `{stats['vault_note']}` (`[[reasoning/rl_network_policy_playbooks]]`).\n"
                    )
                else:
                    res_rl = run_rl_network_policy_reasoning(
                        problem=rl_arg if (rl_arg and low_rl not in ("status", "next", "-mode:status", "--mode:status")) else (ACTIVE_GOAL or "Predict optimal 3-step RL network trajectory"),
                        train_episodes=0,
                        sense_topology=True,
                        export_to_vault=True,
                    )
                    print(f"\n\033[1;35m{res_rl['markdown']}\033[0m\n")
            except Exception as exc:
                print(f"\n\033[1;31m[Engine 19 RL Error]\033[0m {exc}\n")
            continue
        if (
            user_input.lower() == "/pca"
            or user_input.lower().startswith("/pca ")
            or user_input.lower().startswith("/pca/")
            or user_input.lower() == "/kmeans"
            or user_input.lower().startswith("/kmeans ")
        ):
            pca_arg = re.sub(r"^/(?:pca|kmeans)(?:\s+|/|$)", "", user_input, flags=re.I).strip()
            if pca_arg.lower().startswith(("-mode ", "mode ")):
                v_p = re.sub(r"^-?mode\s+", "", pca_arg, flags=re.I).strip()
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-mode:<value>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/pca -mode:{v_p}`.\n"
                )
                continue
            if pca_arg.lower().startswith("mode:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{pca_arg}` instead of `{pca_arg}`.\n"
                )
                continue
            if pca_arg.lower().startswith(("-mode:", "--mode:")):
                pca_arg = pca_arg.split(":", 1)[1].strip()
            try:
                from Reasoning.engines.spectral_manifold_pca import run_spectral_pca_reasoning

                force_rec = pca_arg.lower() in ("recompute", "rebuild", "train", "force")
                res_pca = run_spectral_pca_reasoning(
                    problem=pca_arg if (pca_arg and not force_rec and pca_arg.lower() != "status") else (ACTIVE_GOAL or "SVD PCA, K-Means++ Regime Clustering & Graph Laplacian Chokepoints"),
                    force_recompute=force_rec,
                    export_to_vault=True,
                )
                print(f"\n\033[1;36m{res_pca['markdown']}\033[0m\n")
            except Exception as exc:
                print(f"\n\033[1;31m[Engine 20 PCA/K-Means++ Error]\033[0m {exc}\n")
            continue
        if (
            user_input.lower() == "/reason"
            or user_input.lower().startswith("/reason ")
            or user_input.lower() == "/mdp"
            or user_input.lower().startswith("/mdp ")
        ):
            if user_input.lower().startswith("/mdp"):
                r_arg = "-engine:mdp " + user_input[4:].strip()
            else:
                r_arg = user_input[7:].strip()
            if r_arg.lower().startswith(("-engine ", "engine ")):
                v_e = re.sub(r"^-?engine\s+", "", r_arg, flags=re.I).strip()
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-engine:<name>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/reason -engine:{v_e}`.\n"
                )
                continue
            if r_arg.lower().startswith(("engine:", "mode:")):
                bad_tok = r_arg.split()[0]
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{bad_tok}` instead of `{bad_tok}`.\n"
                )
                continue
            from Reasoning.reasoning_cli import check_environment_status, execute_reasoning_tool, run_self_tests

            if not r_arg or r_arg.lower() in ("status", "-mode:status", "--mode:status"):
                print("\n\033[1;35m=== 15-Engine Neuro-Symbolic Reasoning Status ===\033[0m")
                print(json.dumps(check_environment_status(), indent=2) + "\n")
                continue
            if r_arg.lower() in ("test", "-mode:test", "--mode:test"):
                print("\n\033[1;35m=== Running 15-Engine + Guardrail Self-Tests ===\033[0m")
                print(json.dumps(run_self_tests(), indent=2) + "\n")
                continue
            _SINGLE_ENGINE_KEYS = (
                "associative",
                "geometric",
                "bayesian",
                "dempster_shafer",
                "dst",
                "causal",
                "mdp",
                "temporal",
                "cbr",
                "vsa",
                "sygus",
                "cegar",
                "continual",
                "meta",
                "rl",
                "pca",
                "kmeans",
            )
            if r_arg.lower().startswith(("-engine:", "--engine:")):
                parts_r = r_arg.split(maxsplit=1)
                eng_key = parts_r[0].split(":", 1)[1].strip().lower()
                sub_prob = parts_r[1].strip() if len(parts_r) > 1 else ""
                r_arg = f"{eng_key} {sub_prob}".strip()
            if r_arg.lower() == "mdp" or r_arg.lower().startswith("mdp "):
                mdp_prob = r_arg[3:].strip() or ACTIVE_GOAL or "Predict optimal Tactic -> Technique -> Tool -> Command"
                mdp_report = execute_reasoning_tool("mdp", {"problem": mdp_prob, "save_to_vault": True})
                print(f"\n\033[1;35m{mdp_report}\033[0m\n")
                continue
            if r_arg.lower() in _SINGLE_ENGINE_KEYS or any(
                r_arg.lower().startswith(f"{k} ") for k in _SINGLE_ENGINE_KEYS
            ):
                parts_r = r_arg.split(maxsplit=1)
                eng_key = parts_r[0].lower()
                if eng_key == "dst":
                    eng_key = "dempster_shafer"
                sub_prob = parts_r[1].strip() if len(parts_r) > 1 else (ACTIVE_GOAL or f"Run {eng_key} engine analysis")
                sub_rep = execute_reasoning_tool(
                    eng_key,
                    {
                        "problem": sub_prob,
                        "command": sub_prob,
                        "raw_output": sub_prob,
                        "save_to_vault": True,
                        "write_suggested_improvement": (eng_key == "meta"),
                    },
                )
                print(f"\n\033[1;35m{sub_rep}\033[0m\n")
                continue
            report = execute_reasoning_tool("pipeline", {"problem": r_arg, "save_to_vault": True})
            print(f"\n\033[1;35m{compact_text(report, 2800)}\033[0m\n")
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"I ran the 15-Engine Neuro-Symbolic Reasoning Pipeline on: `{r_arg}`.\n"
                        f"Here is the verified Consensus Arbiter synthesis:\n\n{compact_text(report, 2800)}\n\n"
                        "Use the `>>> CONSENSUS IMMEDIATE ACTION <<<`, Somatic Gut Valence, Optimal Stopping decision, Speculative Next-Tool Branches, Engine 19 3-Step Trajectory RL Rollout, Engine 20 K-Means++ Regime & Laplacian Chokepoints, Bayesian posteriors, Dempster-Shafer conflict metrics, Causal `do()` interventions, and H-MDP Bellman policy to guide our next action."
                    ),
                }
            )
            try:
                run_turn(messages)
                print()
            except Exception as exc:
                print(f"\n\033[1;31m[Error]\033[0m {exc}\n")
            continue
        if user_input.lower() == "/scan" or user_input.lower().startswith("/scan "):
            if (ACTIVE_PERSONALITY_MODE or os.environ.get("CORA_PERSONALITY_MODE", "DEFAULT")).upper() == "ANALYST":
                print(
                    "\n\033[1;31m[Analyst Mode Restriction — `/scan` Blocked]\033[0m\n"
                    "  Analyst Mode (`WHITE` Network Isolation) strictly prohibits external network scanning and sending data outside the local laptop system.\n"
                    "  Analyze existing local scan reports in `Projects/` or `ObsidianVault/`, or switch session modes with `/mode`.\n"
                )
                continue
            target = user_input[5:].strip()
            if not target:
                print_switch_help("scan")
                continue
            if target.lower().startswith(("-target ", "target ")):
                v_tg = re.sub(r"^-?target\s+", "", target, flags=re.I).strip()
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Use `-target:<url_or_ip>` (with a leading dash `-` and colon `:`) instead of a space — e.g. `/scan -target:{v_tg}`.\n"
                )
                continue
            if target.lower().startswith("target:"):
                print(
                    f"\n\033[1;31m[Parameter Syntax Error]\033[0m Parameters must be preceded by a dash `-` — use `-{target}` instead of `{target}`.\n"
                )
                continue
            if target.lower().startswith(("-target:", "--target:")):
                target = target.split(":", 1)[1].strip()
            if target:
                report = perform_target_scan(target)
                print(f"\n\033[1;36m{report}\033[0m\n")
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            f"I scanned `{target}` (auto-saved to ObsidianVault). Here is the scan report:\n\n{report}\n\n"
                            "Use this scan report to help me craft valid curl commands or interact with this target."
                        ),
                    }
                )
                try:
                    run_turn(messages)
                    print()
                except Exception as exc:
                    print(f"\n\033[1;31m[Error]\033[0m {exc}\n")
            continue

        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = build_system_prompt(force_refresh_hw=False)
        messages.append({"role": "user", "content": user_input})
        try:
            if RELENTLESS_MODE:
                if not ACTIVE_GOAL:
                    ACTIVE_GOAL = user_input[:240]
                    append_project_goal(ACTIVE_GOAL)
                    HUD.render(force_region=False)
                run_relentless_loop(messages)
            else:
                run_turn(messages)
            print()
        except KeyboardInterrupt:
            print()
        except urllib.error.HTTPError as err:
            print(f"\n\033[1;31m[Server Error {err.code}]\033[0m {err.reason}\n")
            messages.pop()
        except Exception as exc:
            print(f"\n\033[1;31m[Error]\033[0m {exc}\n")
            messages.pop()


if __name__ == "__main__":
    main()
