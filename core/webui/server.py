#!/usr/bin/env python3
"""
C.O.R.A. (Cyber Oriented Reasoning Agent) Custom WebUI Local Backend (`core/webui/server.py`)
==============================================================================================
Replaces the third-party Docker `open-webui` container with a native, zero-Docker local
Python + FastAPI + WebSockets + SQLite + psutil + NVIDIA NVML backend that connects the
Svelte + TypeScript + Tailwind CSS dashboard directly to:
  1. Isolated Project Workspaces (`CORA/Projects/<project>/`) — select, create, rename,
     explore folders (`memory.md`, `goals.md`, `REPORT.md`, `targets/`, `notes/`, `reasoning/`,
     `artifacts/`, `downloads/`), and view/edit scripts & notes.
  2. CLI-Equivalent Session Controls — Personality & Logic Mode (`[1] Default`, `[2] Analyst`
     [locks `WHITE`], `[3] Berserker` [requires `Red`/`Blue`], `[4] Ninja` [requires `Red`/`Blue`]),
     Network Isolation (`Red`, `White`, `Blue` + allowed interfaces), Thinking toggle, Auto-Run
     permission toggle, and Active Goal (`/goal`).
  3. 15-Engine Neuro-Symbolic Reasoning Core (`core/Reasoning/engines/pipeline.py`) & Engine 9
     CEGAR Command Pre-Verifier (`cegar_verifier.py`).
  4. Real-Time Hardware Telemetry (`psutil` CPU/RAM/Disk/Network + NVIDIA `pynvml` / `nvidia-smi`
     GPU utilization, VRAM used/total, temperatures, and power draw) streamed over WebSockets.
  5. Local Inference APIs (`llama-server` on `127.0.0.1:8080/v1` and `Ollama` on `127.0.0.1:11434`)
     with model discovery, health checks, and conversation routing.
  6. Local SQLite Storage (`core/Log/cora_webui.db`) for operator settings, project metadata,
     and persistent conversation/query history.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import datetime as dt
import ipaddress
import json
import os
import platform
import re
import shutil
import socket
import sqlite3
import ssl
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel, Field
    import psutil
except ModuleNotFoundError:
    _req_path = Path(__file__).resolve().parent / "requirements.txt"
    if _req_path.is_file():
        print(f"[CORA WebUI] Installing missing Python dependencies from {_req_path}...", flush=True)
        for _pip_args in (
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(_req_path)],
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "-r", str(_req_path)],
        ):
            if subprocess.run(_pip_args, check=False).returncode == 0:
                break
    from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel, Field
    import psutil

# Ensure `core/` is on sys.path so `Reasoning` and `Network_Isolation` import cleanly
WEBUI_DIR = Path(__file__).resolve().parent
CORE_DIR = WEBUI_DIR.parent
CORA_ROOT = CORE_DIR.parent if CORE_DIR.name.lower() == "core" else CORE_DIR
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
if str(CORA_ROOT) not in sys.path:
    sys.path.insert(0, str(CORA_ROOT))

from Tools.tool_manager import download_missing_tools, get_system_tools_inventory

from Network_Isolation.console_posture import (
    POSTURE_THEMES,
    detect_console_posture,
    load_network_isolation_config,
    _log_posture_event,
    _parse_iface_list,
)
from Reasoning.engines.cbr_fingerprints import match_failure_fingerprint
from Reasoning.engines.cegar_verifier import _get_host_all_interface_subnets, verify_command_cegar
from Reasoning.engines.continual_learner import record_live_command_experience
from Reasoning.engines.pipeline import run_neuro_symbolic_pipeline
from Reasoning.engines.rl_network_policy import record_rl_step_transition
from Reasoning.reasoning_cli import check_environment_status as get_system_status
from Reasoning.engines.sygus_extractor import extract_structured_facts
from Reasoning.engines.temporal_fluents import record_command_event
from Reasoning.engines.vault_bridge import (
    DATA_DIR,
    PROJECTS_DIR,
    VAULT_DIR,
    _atomic_write_text,
    ensure_directories,
    get_active_project_dir,
    get_hardware_reasoning_limits as detect_hardware_tier,
    slugify,
)
from Reasoning.report_generator import generate_project_report

LOG_DIR = CORE_DIR / "Log"
MODELS_DIR = Path(
    os.environ.get("CORA_MODELS_DIR")
    or str((CORA_ROOT / "models") if (CORA_ROOT / "models").is_dir() else (CORE_DIR / "Models"))
).resolve()
ASSETS_DIR = CORE_DIR / "Explained" / "assets"
FRONTEND_DIST_DIR = WEBUI_DIR / "frontend" / "dist"
DB_PATH = LOG_DIR / "cora_webui.db"
ACTIVE_PROJECT_FILE = LOG_DIR / "active-project.txt"
ACTIVE_MODE_ENV_FILE = LOG_DIR / "active_session_mode.env"
VERSION_FILE = LOG_DIR / "cora_version.json"

# ---------------------------------------------------------------------------
# Personality Mode Definitions (Matching `core/agent-cli.py` SESSION_MODES)
# ---------------------------------------------------------------------------
SESSION_MODES: Dict[str, Dict[str, Any]] = {
    "default": {
        "number": "1",
        "key": "default",
        "label": "Default",
        "badge": "MODE:DEFAULT",
        "allowed_isolation": ["red", "blue", "white"],
        "forced_isolation": None,
        "default_permission": "confirm",
        "read_only": False,
        "summary": "Standard balanced tactical assistant. Full 15-Engine reasoning, interactive tool confirmation, and normal pacing.",
        "system_directive": (
            "Operate in DEFAULT balanced mode: combine analytical reasoning with safe, verified command recommendations. "
            "Respect active network isolation boundaries and record verified findings."
        ),
    },
    "analyst": {
        "number": "2",
        "key": "analyst",
        "label": "Analyst (Read-Only / White Air-Gap)",
        "badge": "MODE:ANALYST(READ-ONLY)",
        "allowed_isolation": ["white"],
        "forced_isolation": "white",
        "default_permission": "confirm",
        "read_only": True,
        "summary": "Strictly non-mutating inspection & forensic analysis. Automatically locks Network Isolation to WHITE (loopback air-gap) and blocks any mutating or outbound network commands.",
        "system_directive": (
            "Operate in ANALYST (Strictly Read-Only / White Air-Gap) mode: NEVER execute or propose destructive, mutating, "
            "or active external network commands. Perform deep code/log/vault/architecture analysis, forensic inspection, and verification only."
        ),
    },
    "berserker": {
        "number": "3",
        "key": "berserker",
        "label": "Berserker (Autonomous Multi-Wave)",
        "badge": "MODE:BERSERKER(AUTO-WAVE)",
        "allowed_isolation": ["red", "blue"],
        "forced_isolation": None,
        "default_permission": "auto",
        "read_only": False,
        "summary": "High-tempo autonomous multi-vector execution across L1 Serial -> L2 ARP -> L3 Routing -> L4 Ports -> L7 HTTP. Requires RED or BLUE network isolation.",
        "system_directive": (
            "Operate in BERSERKER (Aggressive Autonomous Multi-Wave) mode: prioritize rapid multi-layer probing (L1 UART, L2 ARP, L3 Routing, L4 TCP/UDP, L7 HTTP), "
            "pivot immediately when a vector is blocked, and synthesize concrete executable command chains."
        ),
    },
    "ninja": {
        "number": "4",
        "key": "ninja",
        "label": "Ninja (Stealth & Low-Noise)",
        "badge": "MODE:NINJA(STEALTH)",
        "allowed_isolation": ["red", "blue"],
        "forced_isolation": None,
        "default_permission": "confirm",
        "read_only": False,
        "summary": "Minimal footprint, passive/low-rate reconnaissance, living-off-the-land socket/ARP/proc inspection, and paced UART I/O. Requires RED or BLUE network isolation.",
        "system_directive": (
            "Operate in NINJA (Stealth & Low-Noise) mode: prefer passive kernel/proc/ARP/socket inspection (`ss`, `ip neigh`, `/proc/net/*`) and "
            "strictly rate-limited, low-signature probes over noisy broad scans."
        ),
    },
}

CORA_MODEL_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "3.8",
        "alias": "Qwen3.8-27B-Uncensored-Q3_K_M",
        "name": "Qwen3.8-27B-Uncensored (Q3_K_M)",
        "filename": "Qwen3.8-27B-Uncensored-Q3_K_M.gguf",
        "alt_filenames": [],
        "provider": "llama-server",
        "role": "Primary Deep Reasoning (Default)",
        "vram_est": "13.5 GB",
    },
    {
        "id": "3.5",
        "alias": "Qwen3.5-9B-Uncensored-Q4_K_M",
        "name": "Qwen3.5-9B-Uncensored (Q4_K_M)",
        "filename": "Qwen3.5-9B-Uncensored-Q4_K_M.gguf",
        "alt_filenames": ["Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"],
        "provider": "llama-server",
        "role": "Fast Low-VRAM / Edge Tactical",
        "vram_est": "5.8 GB",
    },
    {
        "id": "turbo",
        "alias": "Qwen3.8-27B-Turbo-MTP-Q4_K_M",
        "name": "Qwen3.8-27B-Turbo-MTP (Q4_K_M)",
        "filename": "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf",
        "alt_filenames": ["Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q4_K_M.gguf"],
        "provider": "llama-server",
        "role": "Multi-Token Prediction High-Speed",
        "vram_est": "18.2 GB",
    },
    {
        "id": "turbo-q6",
        "alias": "Qwen3.8-27B-Turbo-MTP-Q6_K",
        "name": "Qwen3.8-27B-Turbo-MTP (Q6_K)",
        "filename": "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf",
        "alt_filenames": ["Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q6_K.gguf"],
        "provider": "llama-server",
        "role": "High-Precision 24GB+ VRAM Tier",
        "vram_est": "23.8 GB",
    },
    {
        "id": "turbo-q8",
        "alias": "Qwen3.8-27B-Turbo-MTP-Q8_0",
        "name": "Qwen3.8-27B-Turbo-MTP (Q8_0)",
        "filename": "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf",
        "alt_filenames": ["Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q8_0.gguf"],
        "provider": "llama-server",
        "role": "Max-Precision 32GB+ VRAM Tier",
        "vram_est": "29.8 GB",
    },
]

_LLAMA_LOCK = threading.Lock()
_LLAMA_LAST_ERROR: str = ""

# ---------------------------------------------------------------------------
# NVIDIA NVML Initialization (`pynvml` with `nvidia-smi` fallback)
# ---------------------------------------------------------------------------
_NVML_INITIALIZED = False
_pynvml_mod: Any = None
try:
    import pynvml as _pynvml_mod  # type: ignore

    _pynvml_mod.nvmlInit()
    _NVML_INITIALIZED = True
except Exception:
    _NVML_INITIALIZED = False

_PREV_NET_IO: Optional[Any] = None
_PREV_DISK_IO: Optional[Any] = None
_PREV_IO_TS: float = 0.0


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def get_cora_version() -> Dict[str, Any]:
    if VERSION_FILE.is_file():
        try:
            return json.loads(VERSION_FILE.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            pass
    return {"version": "5.15.12", "codename": "15-Engine Neuro-Symbolic Streamlined Core"}


_CLI_CROW_ASCII_LINES = (
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

_CLI_CORA_BANNER_LINES = (
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

_CLI_DESCRIPTION_LINES = (
    "C.O.R.A. is a multi-layered reasoning agent that combines AI and a cybersecurity focused",
    "Super Intelligence system to support Red, Blue, and Hunt Teams. Its Analyst, Active, and",
    "Passive modes help teams analyze scan results and system data, identify potential",
    "weaknesses and threats, and create clear reports for technical teams and leadership.",
)

_CLI_DISCLAIMER_LINES = (
    "--- OPEN-SOURCE NOTICE, ATTRIBUTION & LIMITATION OF LIABILITY ---",
    "C.O.R.A. is open-source software under active development and continuous refinement.",
    "Redistribution, modification, or operational deployment is permitted provided that clear",
    "attribution and development credit to https://CROWinnovations.com are retained in all copies",
    'and derivative works. C.O.R.A. and its layered reasoning engines are provided "AS IS" without',
    "warranty of any kind. The developer assumes no liability or legal responsibility for any",
    "actions, damages, data loss, or legal consequences arising from the use of this system.",
)

_CLI_LICENSE_HEADER_LINES = (
    "GNU GENERAL PUBLIC LICENSE — Version 3, 29 June 2007",
    "C.O.R.A. — Cyber Oriented Reasoning Agent",
    "Copyright (C) 2026 CROW Innovations (https://CROWinnovations.com)",
    "Repository: https://github.com/B0b-Skull/Cyber-Oriented-Reasoning-Agent",
    "",
    "OPEN-SOURCE ATTRIBUTION & AUTHORIZED SECURITY USE NOTICE:",
    "C.O.R.A. is open-source software licensed under the GNU General Public License v3.0 (GPL-3.0).",
    "Redistribution, modification, or operational deployment is permitted under the terms of the GPL-3.0",
    "provided that clear attribution and development credit to CROW Innovations (https://CROWinnovations.com)",
    "and this copyright notice are retained in all copies and derivative works.",
    "",
    "This software is designed for authorized cybersecurity diagnostics, network engineering, and",
    "defensive/educational research. Users are solely responsible for ensuring they have explicit",
    "authorization before testing any network, host, or device. C.O.R.A. and its layered reasoning",
    'engines are provided "AS IS" without warranty of any kind.',
)


def get_cli_banner_and_licensing_info() -> Dict[str, Any]:
    """
    Return the exact CLI Splash Banner, Description, Session Environment Paths,
    Open-Source Disclaimer (`_CORA_DISCLAIMER_LINES`), and Licensing (`core/LICENSE`)
    so the WebGUI CROW Emblem pop-up modal matches the CLI 1-to-1.
    """
    ver_info = get_cora_version()
    ver_str = str(ver_info.get("version") or "5.15.12")
    banner_width = 100
    crow_w = 32
    left_used = 2 + crow_w
    right_space = max(40, banner_width - left_used)
    ascii_block_w = max(len(ln.rstrip()) for ln in _CLI_CORA_BANNER_LINES[:5])
    gap_after_crow = max(3, (right_space - ascii_block_w) // 2)

    combined_splash_lines: List[str] = []
    for idx, (c_ln, b_ln) in enumerate(zip(_CLI_CROW_ASCII_LINES, _CLI_CORA_BANNER_LINES)):
        if idx < 5:
            b_padded = (" " * gap_after_crow) + b_ln.rstrip()
        elif idx in (7, 8):
            sub_txt = b_ln.strip()
            sub_gap = max(3, gap_after_crow + (ascii_block_w - len(sub_txt)) // 2)
            b_padded = (" " * sub_gap) + sub_txt
        else:
            b_padded = ""
        combined_splash_lines.append(f"  {c_ln}{b_padded}")

    license_file = CORE_DIR / "LICENSE"
    full_license_text = ""
    if license_file.is_file():
        try:
            full_license_text = license_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            full_license_text = "\n".join(_CLI_LICENSE_HEADER_LINES)
    else:
        full_license_text = "\n".join(_CLI_LICENSE_HEADER_LINES)

    return {
        "version": ver_str,
        "developed_by": "https://CROWinnovations.com",
        "repository": "https://github.com/B0b-Skull/Cyber-Oriented-Reasoning-Agent",
        "license_name": "GNU General Public License v3.0 (GPL-3.0)",
        "license_path": str(license_file),
        "crow_ascii_lines": list(_CLI_CROW_ASCII_LINES),
        "cora_banner_lines": list(_CLI_CORA_BANNER_LINES),
        "combined_splash_lines": combined_splash_lines,
        "description_lines": list(_CLI_DESCRIPTION_LINES),
        "disclaimer_lines": list(_CLI_DISCLAIMER_LINES),
        "license_header_lines": list(_CLI_LICENSE_HEADER_LINES),
        "full_license_text": full_license_text,
        "vault_dir": str(VAULT_DIR),
        "projects_dir": str(PROJECTS_DIR),
        "working_dir": str(CORA_ROOT),
    }


# ---------------------------------------------------------------------------
# SQLite Local Storage (`core/Log/cora_webui.db`)
# ---------------------------------------------------------------------------
def get_db_conn() -> sqlite3.Connection:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_sqlite_db() -> None:
    ensure_directories()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with get_db_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS projects_meta (
                slug TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                mode TEXT NOT NULL DEFAULT 'default',
                isolation_level TEXT NOT NULL DEFAULT 'red',
                active_goal TEXT NOT NULL DEFAULT '',
                last_opened_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                project_slug TEXT NOT NULL,
                title TEXT NOT NULL,
                mode TEXT NOT NULL,
                isolation_level TEXT NOT NULL,
                model TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                project_slug TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                thinking TEXT NOT NULL DEFAULT '',
                command_executed TEXT NOT NULL DEFAULT '',
                command_output TEXT NOT NULL DEFAULT '',
                reasoning_json TEXT NOT NULL DEFAULT '{}',
                posture_level TEXT NOT NULL DEFAULT 'RED',
                mode_key TEXT NOT NULL DEFAULT 'default',
                model_used TEXT NOT NULL DEFAULT '3.8',
                latency_ms REAL NOT NULL DEFAULT 0.0,
                created_at TEXT NOT NULL
            );
            """
        )
        conn.commit()

    # Seed defaults from existing CLI state files if not yet set
    _invalid_projs = {"active_session", "active-session", "default", "default-project", "default_session"}
    active_proj = ""
    if ACTIVE_PROJECT_FILE.is_file():
        try:
            raw_p = ACTIVE_PROJECT_FILE.read_text(encoding="utf-8", errors="replace").strip()
            if raw_p and raw_p.lower() not in _invalid_projs:
                cand = slugify(raw_p)
                if cand and cand.lower() not in _invalid_projs and (Path(PROJECTS_DIR) / cand).is_dir():
                    active_proj = cand
        except Exception:
            pass
    if not active_proj and Path(PROJECTS_DIR).is_dir():
        existing_projs = [
            d.name
            for d in sorted(Path(PROJECTS_DIR).iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
            if d.is_dir() and not d.name.startswith(".") and d.name.lower() not in _invalid_projs
        ]
        if existing_projs:
            active_proj = existing_projs[0]

    net_cfg = load_network_isolation_config()
    default_iso = str(net_cfg.get("default_level", "red")).lower()
    default_ifaces = ",".join(net_cfg.get("blue_allowed_ifaces") or ["eth0", "eth1"])

    defaults = {
        "active_project": active_proj,
        "session_mode": "default",
        "isolation_level": default_iso if default_iso in ("red", "blue", "white") else "red",
        "allowed_interfaces": default_ifaces,
        "selected_model": "3.8",
        "inference_provider": "llama-server",
        "llama_api_url": os.environ.get("LLAMA_API_URL", "http://127.0.0.1:8080/v1"),
        "ollama_api_url": os.environ.get("OLLAMA_API_URL", "http://127.0.0.1:11434"),
        "thinking_enabled": "true",
        "permission_mode": "confirm",
        "auto_reason_on_query": "true",
        "theme_mode": "dark",
    }
    now = _now_iso()
    with get_db_conn() as conn:
        for k, v in defaults.items():
            conn.execute(
                "INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES (?, ?, ?)",
                (k, str(v), now),
            )
        # Migrate any stale 'active_session' or 'default' active_project setting to a real project or ''
        conn.execute(
            "UPDATE settings SET value = ?, updated_at = ? WHERE key = 'active_project' AND LOWER(value) IN ('active_session', 'active-session', 'default', 'default-project', 'default_session')",
            (active_proj, now),
        )
        # On Windows, if allowed_interfaces is still the Linux default "eth0,eth1", migrate to detected Windows NIC(s)
        if os.name == "nt" and default_ifaces != "eth0,eth1":
            conn.execute(
                "UPDATE settings SET value = ?, updated_at = ? WHERE key = 'allowed_interfaces' AND value = 'eth0,eth1'",
                (default_ifaces, now),
            )
        conn.commit()


def get_host_interfaces_catalog() -> List[Dict[str, Any]]:
    """Return all detected host network interfaces and their IPv4 subnets for BLUE isolation selection."""
    if_nets = _get_host_all_interface_subnets()
    items: List[Dict[str, Any]] = []
    for iface, nets in if_nets.items():
        subnets = [str(n) for n in nets]
        is_virt = bool(re.search(r"(?:vethernet|vmnet|wsl|docker|virbr|vbox|loopback)", iface, re.I))
        items.append(
            {
                "name": iface,
                "subnets": subnets,
                "label": f"{iface} ({', '.join(subnets)})" if subnets else iface,
                "is_virtual": is_virt,
            }
        )
    items.sort(key=lambda x: (1 if x["is_virtual"] else 0, x["name"].lower()))
    return items


def get_all_settings() -> Dict[str, str]:
    with get_db_conn() as conn:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
    return {str(r["key"]): str(r["value"]) for r in rows}


def update_settings_dict(updates: Dict[str, Any]) -> Dict[str, str]:
    now = _now_iso()
    with get_db_conn() as conn:
        for k, v in updates.items():
            conn.execute(
                "INSERT INTO settings (key, value, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
                (str(k), str(v), now),
            )
        conn.commit()
    cfg = get_all_settings()
    _sync_cli_session_files(cfg)
    return cfg


def _sync_cli_session_files(cfg: Dict[str, str]) -> None:
    """
    Keep `core/Log/active-project.txt`, `core/Log/active_session_mode.env`, and process
    environment variables synchronized with the WebUI so the CLI and WebUI share state.
    """
    raw_proj = (cfg.get("active_project") or "").strip()
    proj = slugify(raw_proj) if (raw_proj and raw_proj.lower() not in {"active_session", "active-session", "default", "default-project", "default_session", "untitled", "unassigned"}) else ""
    mode_key = cfg.get("session_mode", "default").lower()
    if mode_key not in SESSION_MODES:
        mode_key = "default"
    mode_info = SESSION_MODES[mode_key]

    iso = cfg.get("isolation_level", "red").lower()
    if mode_info["forced_isolation"]:
        iso = mode_info["forced_isolation"]
    elif iso not in mode_info["allowed_isolation"]:
        iso = mode_info["allowed_isolation"][0]

    ifaces = cfg.get("allowed_interfaces", "eth0,eth1").strip()
    os.environ["CORA_ACTIVE_PROJECT"] = proj
    os.environ["CORA_SESSION_MODE"] = mode_key
    os.environ["LLM_ISOLATION_MODE"] = iso
    if iso == "blue" and ifaces:
        os.environ["LLM_ALLOWED_IFACES"] = ifaces
        os.environ["LLM_POSTURE_OVERRIDE"] = f"blue:{ifaces}"
    else:
        os.environ["LLM_POSTURE_OVERRIDE"] = iso

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(ACTIVE_PROJECT_FILE, f"{proj}\n")
        env_lines = [
            "# Auto-generated by CORA WebUI / Agent CLI Session Synchronizer",
            f'export CORA_ACTIVE_PROJECT="{proj}"',
            f'export CORA_PERSONALITY_MODE="{mode_key.upper()}"',
            f'export CORA_SESSION_MODE="{mode_key}"',
            f'export CORA_SESSION_MODE_NUMBER="{mode_info["number"]}"',
            f'export LLM_ISOLATION_MODE="{iso.upper()}"',
            f'export LLM_ALLOWED_IFACES="{ifaces}"',
        ]
        _atomic_write_text(ACTIVE_MODE_ENV_FILE, "\n".join(env_lines) + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Hardware Telemetry Collector (`psutil` + NVIDIA `pynvml` / `nvidia-smi`)
# ---------------------------------------------------------------------------
def _query_gpus_metrics() -> List[Dict[str, Any]]:
    gpus: List[Dict[str, Any]] = []
    if _NVML_INITIALIZED and _pynvml_mod is not None:
        try:
            count = _pynvml_mod.nvmlDeviceGetCount()
            for idx in range(count):
                handle = _pynvml_mod.nvmlDeviceGetHandleByIndex(idx)
                raw_name = _pynvml_mod.nvmlDeviceGetName(handle)
                name = raw_name.decode("utf-8", errors="replace") if isinstance(raw_name, bytes) else str(raw_name)
                mem = _pynvml_mod.nvmlDeviceGetMemoryInfo(handle)
                try:
                    util = _pynvml_mod.nvmlDeviceGetUtilizationRates(handle)
                    gpu_util = float(util.gpu)
                except Exception:
                    gpu_util = 0.0
                try:
                    temp_c = float(_pynvml_mod.nvmlDeviceGetTemperature(handle, _pynvml_mod.NVML_TEMPERATURE_GPU))
                except Exception:
                    temp_c = 0.0
                try:
                    power_w = round(float(_pynvml_mod.nvmlDeviceGetPowerUsage(handle)) / 1000.0, 1)
                except Exception:
                    power_w = 0.0
                try:
                    power_limit_w = round(float(_pynvml_mod.nvmlDeviceGetEnforcedPowerLimit(handle)) / 1000.0, 1)
                except Exception:
                    power_limit_w = 0.0
                try:
                    fan_pct = float(_pynvml_mod.nvmlDeviceGetFanSpeed(handle))
                except Exception:
                    fan_pct = 0.0

                used_mb = round(mem.used / (1024 * 1024), 1)
                total_mb = round(mem.total / (1024 * 1024), 1)
                vram_pct = round((mem.used / mem.total) * 100.0, 1) if mem.total else 0.0
                gpus.append(
                    {
                        "index": idx,
                        "name": name,
                        "utilization_pct": gpu_util,
                        "vram_used_mb": used_mb,
                        "vram_total_mb": total_mb,
                        "vram_pct": vram_pct,
                        "temperature_c": temp_c,
                        "power_w": power_w,
                        "power_limit_w": power_limit_w,
                        "fan_speed_pct": fan_pct,
                        "source": "pynvml",
                    }
                )
            if gpus:
                return gpus
        except Exception:
            pass

    # Fallback to `nvidia-smi` CLI if NVML is reinitializing or unavailable
    if shutil.which("nvidia-smi"):
        try:
            proc = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=2.0,
                check=False,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                for ln in proc.stdout.strip().splitlines():
                    parts = [p.strip() for p in ln.split(",")]
                    if len(parts) >= 6:
                        idx = int(parts[0]) if parts[0].isdigit() else 0
                        name = parts[1]
                        gpu_u = float(parts[2]) if parts[2].replace(".", "", 1).isdigit() else 0.0
                        used_mb = float(parts[3]) if parts[3].replace(".", "", 1).isdigit() else 0.0
                        tot_mb = float(parts[4]) if parts[4].replace(".", "", 1).isdigit() else 1.0
                        temp_c = float(parts[5]) if parts[5].replace(".", "", 1).isdigit() else 0.0
                        pwr_w = float(parts[6]) if len(parts) > 6 and parts[6].replace(".", "", 1).isdigit() else 0.0
                        gpus.append(
                            {
                                "index": idx,
                                "name": name,
                                "utilization_pct": gpu_u,
                                "vram_used_mb": used_mb,
                                "vram_total_mb": tot_mb,
                                "vram_pct": round((used_mb / tot_mb) * 100.0, 1) if tot_mb else 0.0,
                                "temperature_c": temp_c,
                                "power_w": pwr_w,
                                "power_limit_w": 0.0,
                                "fan_speed_pct": 0.0,
                                "source": "nvidia-smi",
                            }
                        )
        except Exception:
            pass
    return gpus


_PREV_NET_PERNIC: Dict[str, Any] = {}


def collect_hardware_metrics() -> Dict[str, Any]:
    """
    Collect OS metrics via `psutil` and NVIDIA GPU metrics via `pynvml` (`nvidia-smi` fallback).
    """
    global _PREV_NET_IO, _PREV_DISK_IO, _PREV_IO_TS, _PREV_NET_PERNIC

    now_ts = time.time()
    dt_sec = max(0.2, now_ts - _PREV_IO_TS) if _PREV_IO_TS > 0 else 1.0

    # CPU
    cpu_pct = float(psutil.cpu_percent(interval=None))
    per_cpu = [float(x) for x in psutil.cpu_percent(interval=None, percpu=True)]
    cpu_freq = psutil.cpu_freq()
    freq_mhz = round(float(cpu_freq.current), 0) if cpu_freq else 0.0
    cpu_temp_c: Optional[float] = None
    if hasattr(psutil, "sensors_temperatures"):
        try:
            temps = psutil.sensors_temperatures() or {}
            for entries in temps.values():
                if entries:
                    cpu_temp_c = round(float(entries[0].current), 1)
                    break
        except Exception:
            pass

    # Memory
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    ram_used_gb = round((vm.total - vm.available) / (1024**3), 2)
    ram_total_gb = round(vm.total / (1024**3), 2)

    # Disk
    disk_root = str(CORA_ROOT.anchor or "/")
    du = psutil.disk_usage(disk_root)
    disk_used_gb = round(du.used / (1024**3), 1)
    disk_total_gb = round(du.total / (1024**3), 1)

    disk_io = psutil.disk_io_counters()
    read_mb_s = 0.0
    write_mb_s = 0.0
    if disk_io and _PREV_DISK_IO is not None and _PREV_IO_TS > 0:
        read_mb_s = round(max(0.0, (disk_io.read_bytes - _PREV_DISK_IO.read_bytes) / dt_sec / (1024 * 1024)), 2)
        write_mb_s = round(max(0.0, (disk_io.write_bytes - _PREV_DISK_IO.write_bytes) / dt_sec / (1024 * 1024)), 2)
    _PREV_DISK_IO = disk_io

    # Network (Total + Per-NIC upload/download speed & IP/mask)
    net_io = psutil.net_io_counters()
    tx_kb_s = 0.0
    rx_kb_s = 0.0
    if net_io and _PREV_NET_IO is not None and _PREV_IO_TS > 0:
        tx_kb_s = round(max(0.0, (net_io.bytes_sent - _PREV_NET_IO.bytes_sent) / dt_sec / 1024.0), 1)
        rx_kb_s = round(max(0.0, (net_io.bytes_recv - _PREV_NET_IO.bytes_recv) / dt_sec / 1024.0), 1)
    _PREV_NET_IO = net_io

    pernic_now: Dict[str, Any] = {}
    try:
        pernic_now = psutil.net_io_counters(pernic=True) or {}
    except Exception:
        pernic_now = {}

    # Active Network Interfaces & IPv4/mask addresses via psutil
    nic_details: List[Dict[str, Any]] = []
    try:
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()
        for iface_name, st in stats.items():
            if not st.isup:
                continue
            ipv4_list: List[str] = []
            ip_cidr_list: List[str] = []
            for a in addrs.get(iface_name, []):
                if getattr(a.family, "name", "") == "AF_INET" or int(a.family) == 2:
                    addr_str = str(a.address or "").strip()
                    if not addr_str or addr_str.startswith("169.254."):
                        continue
                    ipv4_list.append(addr_str)
                    mask_str = str(getattr(a, "netmask", "") or "").strip()
                    if mask_str:
                        try:
                            cidr_str = str(ipaddress.IPv4Interface(f"{addr_str}/{mask_str}").with_prefixlen)
                        except Exception:
                            cidr_str = f"{addr_str}/{mask_str}"
                    else:
                        cidr_str = f"{addr_str}/24" if not addr_str.startswith("127.") else f"{addr_str}/8"
                    ip_cidr_list.append(cidr_str)

            if not ip_cidr_list:
                continue

            nic_tx = 0.0
            nic_rx = 0.0
            cur_cnt = pernic_now.get(iface_name)
            prev_cnt = _PREV_NET_PERNIC.get(iface_name) if _PREV_IO_TS > 0 else None
            if cur_cnt is not None and prev_cnt is not None:
                nic_tx = round(max(0.0, (cur_cnt.bytes_sent - prev_cnt.bytes_sent) / dt_sec / 1024.0), 1)
                nic_rx = round(max(0.0, (cur_cnt.bytes_recv - prev_cnt.bytes_recv) / dt_sec / 1024.0), 1)

            is_loop = bool(
                iface_name.lower() == "lo"
                or "loopback" in iface_name.lower()
                or all(ip.startswith("127.") for ip in ipv4_list)
            )
            is_virt = bool(
                re.search(r"(?:vethernet|vmnet|vmware|wsl|docker|virbr|vbox|hyper-v|tailscale|wg|tun|tap)", iface_name, re.I)
            )
            nic_details.append(
                {
                    "name": iface_name,
                    "ipv4": ipv4_list,
                    "ip_cidr": ip_cidr_list,
                    "primary_ip_cidr": ip_cidr_list[0],
                    "tx_kb_s": nic_tx,
                    "rx_kb_s": nic_rx,
                    "speed_mbps": st.speed,
                    "is_loopback": is_loop,
                    "is_virtual": is_virt,
                }
            )
        # Sort order: physical non-loopback NICs first, then virtual NICs, then loopback
        nic_details.sort(
            key=lambda x: (
                2 if x["is_loopback"] else (1 if x["is_virtual"] else 0),
                -int(x.get("speed_mbps") or 0),
                x["name"].lower(),
            )
        )
    except Exception:
        pass

    _PREV_NET_PERNIC = pernic_now
    _PREV_IO_TS = now_ts

    gpus = _query_gpus_metrics()
    hw_tier = detect_hardware_tier()

    return {
        "timestamp": _now_iso(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu": {
            "utilization_pct": cpu_pct,
            "per_core_pct": per_cpu[:16],
            "cores_physical": psutil.cpu_count(logical=False) or 1,
            "cores_logical": psutil.cpu_count(logical=True) or 1,
            "logical_cores": psutil.cpu_count(logical=True) or 1,
            "frequency_mhz": freq_mhz,
            "temperature_c": cpu_temp_c,
        },
        "ram": {
            "used_gb": ram_used_gb,
            "total_gb": ram_total_gb,
            "utilization_pct": float(vm.percent),
            "swap_pct": float(swap.percent),
        },
        "disk": {
            "mount": disk_root,
            "used_gb": disk_used_gb,
            "total_gb": disk_total_gb,
            "utilization_pct": float(du.percent),
            "read_mb_s": read_mb_s,
            "write_mb_s": write_mb_s,
        },
        "network": {
            "tx_kb_s": tx_kb_s,
            "rx_kb_s": rx_kb_s,
            "total_sent_mb": round(net_io.bytes_sent / (1024 * 1024), 1) if net_io else 0.0,
            "total_recv_mb": round(net_io.bytes_recv / (1024 * 1024), 1) if net_io else 0.0,
            "interfaces": nic_details,
        },
        "gpus": gpus,
        "cora_hw_tier": hw_tier,
    }


# ---------------------------------------------------------------------------
# Project Workspace Management (Matching `core/agent-cli.py`)
# ---------------------------------------------------------------------------
_INVALID_PROJECT_NAMES = {"active_session", "active-session", "default", "default-project", "default_session", "untitled", "unassigned"}


def resolve_active_project_slug(candidate: Optional[str] = None, cfg: Optional[Dict[str, str]] = None) -> str:
    """
    Resolve a real user project slug in `Projects/`.
    Never returns or creates `active_session` or `default`.
    If no valid project exists in `Projects/`, returns `""`.
    """
    if candidate:
        raw_c = str(candidate).strip()
        if raw_c and raw_c.lower() not in _INVALID_PROJECT_NAMES:
            slug_c = slugify(raw_c)
            if slug_c and slug_c.lower() not in _INVALID_PROJECT_NAMES:
                return slug_c

    settings = cfg if cfg is not None else get_all_settings()
    saved_cfg = (settings.get("active_project") or "").strip()
    if saved_cfg and saved_cfg.lower() not in _INVALID_PROJECT_NAMES:
        slug_s = slugify(saved_cfg)
        if slug_s and slug_s.lower() not in _INVALID_PROJECT_NAMES and (Path(PROJECTS_DIR) / slug_s).is_dir():
            return slug_s

    if ACTIVE_PROJECT_FILE.is_file():
        try:
            raw_f = ACTIVE_PROJECT_FILE.read_text(encoding="utf-8", errors="replace").strip()
            if raw_f and raw_f.lower() not in _INVALID_PROJECT_NAMES:
                slug_f = slugify(raw_f)
                if slug_f and slug_f.lower() not in _INVALID_PROJECT_NAMES and (Path(PROJECTS_DIR) / slug_f).is_dir():
                    return slug_f
        except Exception:
            pass

    if Path(PROJECTS_DIR).is_dir():
        existing = [
            d.name
            for d in sorted(Path(PROJECTS_DIR).iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
            if d.is_dir() and not d.name.startswith(".") and d.name.lower() not in _INVALID_PROJECT_NAMES
        ]
        if existing:
            return existing[0]

    return ""


def ensure_project_structure(project_name: str) -> Path:
    raw = (project_name or "").strip()
    slug = slugify(raw) if (raw and raw.lower() not in _INVALID_PROJECT_NAMES) else resolve_active_project_slug()
    if slug and slug.lower() not in _INVALID_PROJECT_NAMES:
        proj_dir = Path(PROJECTS_DIR) / slug
    else:
        slug = "unassigned"
        proj_dir = LOG_DIR / "_unassigned_workspace"
    for sub in ("Files", "downloads", "targets", "notes", "reasoning", "artifacts", "assets", "reports", "shadow_archive"):
        (proj_dir / sub).mkdir(parents=True, exist_ok=True)

    mem_file = proj_dir / "memory.md"
    now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not mem_file.is_file():
        mem_template = (
            f"---\n"
            f"title: \"Project {slug} — Isolated Operational Memory\"\n"
            f"category: project\n"
            f"project: \"{slug}\"\n"
            f"status: active\n"
            f"updated: \"{now_str}\"\n"
            f"summary: \"Isolated workspace memory, verified findings, and task checklist for {slug}.\"\n"
            f"---\n\n"
            f"# Project Workspace: `{slug}`\n\n"
            f"## 1. Verified Data & Architecture\n"
            f"- Workspace initialized at `Projects/{slug}/` ({now_str}).\n"
            f"- Local Project Files Directory: `Projects/{slug}/Files/` (custom scripts, configs, and uploaded files for LLM interaction).\n\n"
            f"## 2. Open Verification Questions\n"
            f"- Confirm primary target scope, network interfaces, and operational goals.\n\n"
            f"## 3. Project Plan & Task Checklist\n"
            f"- [x] Initialize isolated project workspace `Projects/{slug}/` and `Projects/{slug}/Files/`\n"
            f"- [ ] Lock operational objective via Goal input (`/goal`)\n"
            f"- [ ] Run 15-Engine Neuro-Symbolic reasoning & target discovery\n\n"
            f"## 4. Saved Project Artifacts & Reports\n"
            f"- [[Projects/{slug}/goals|Project Goals (`goals.md`)]]\n"
            f"- `Projects/{slug}/Files/` — Local Project Files & Custom Scripts Directory\n"
        )
        _atomic_write_text(mem_file, mem_template)

    goals_file = proj_dir / "goals.md"
    if not goals_file.is_file():
        goals_template = (
            f"---\n"
            f"title: \"Project {slug} — Chronological Goals Ledger\"\n"
            f"project: \"{slug}\"\n"
            f"updated: \"{now_str}\"\n"
            f"---\n\n"
            f"# Project Goals Ledger (`Projects/{slug}/goals.md`)\n\n"
        )
        _atomic_write_text(goals_file, goals_template)

    return proj_dir


def get_project_last_goal(proj_dir: Path) -> str:
    goals_file = proj_dir / "goals.md"
    if not goals_file.is_file():
        return ""
    try:
        txt = goals_file.read_text(encoding="utf-8", errors="replace")
        matches = re.findall(
            r"^###\s+Goal\s+#\d+\s+—\s+[^\n]+\n-\s+\*\*Goal:\*\*\s*(.+?)(?=\n###\s+Goal\s+#|\Z)",
            txt,
            flags=re.M | re.S,
        )
        if matches:
            return " ".join(ln.strip() for ln in matches[-1].strip().splitlines() if ln.strip())
    except Exception:
        pass
    return ""


def append_project_goal(proj_dir: Path, goal_text: str) -> int:
    goal_clean = (goal_text or "").strip()
    if not goal_clean:
        return 0
    ensure_project_structure(proj_dir.name)
    goals_file = proj_dir / "goals.md"
    existing = goals_file.read_text(encoding="utf-8", errors="replace") if goals_file.is_file() else ""
    nums = [int(n) for n in re.findall(r"^###\s+Goal\s+#(\d+)\b", existing, flags=re.M)]
    next_num = (max(nums) + 1) if nums else 1
    now_str = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n### Goal #{next_num} — {now_str}\n- **Goal:** {goal_clean}\n"
    _atomic_write_text(goals_file, existing.rstrip() + "\n" + entry)
    return next_num


def list_all_projects() -> List[Dict[str, Any]]:
    Path(PROJECTS_DIR).mkdir(parents=True, exist_ok=True)
    items: List[Dict[str, Any]] = []
    dirs = sorted(
        [
            d
            for d in Path(PROJECTS_DIR).iterdir()
            if d.is_dir() and not d.name.startswith(".") and d.name.lower() not in _INVALID_PROJECT_NAMES
        ],
        key=lambda p: p.name.lower(),
    )
    for idx, d in enumerate(dirs, 1):
        files_subdir = d / "Files"
        files_subdir.mkdir(parents=True, exist_ok=True)
        mem_file = d / "memory.md"
        done_cnt = 0
        todo_cnt = 0
        if mem_file.is_file():
            try:
                m_txt = mem_file.read_text(encoding="utf-8", errors="replace")
                done_cnt = len(re.findall(r"^\s*[-*]\s*\[[xX]\]\s*", m_txt, flags=re.M))
                todo_cnt = len(re.findall(r"^\s*[-*]\s*\[\s\]\s*", m_txt, flags=re.M))
            except Exception:
                pass
        file_cnt = sum(1 for f in d.rglob("*") if f.is_file())
        custom_files_cnt = sum(1 for f in files_subdir.rglob("*") if f.is_file())
        items.append(
            {
                "menu_number": idx,
                "slug": d.name,
                "path": f"Projects/{d.name}",
                "files_dir": f"Projects/{d.name}/Files",
                "custom_files_count": custom_files_cnt,
                "has_report": (d / "REPORT.md").is_file(),
                "last_goal": get_project_last_goal(d),
                "tasks_completed": done_cnt,
                "tasks_pending": todo_cnt,
                "file_count": file_cnt,
                "updated_at": dt.datetime.fromtimestamp(d.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            }
        )
    return items


def list_project_files(project_slug: str) -> Dict[str, Any]:
    proj_dir = ensure_project_structure(project_slug)
    slug = proj_dir.name
    files_dir = proj_dir / "Files"
    files_dir.mkdir(parents=True, exist_ok=True)
    files_list: List[Dict[str, Any]] = []

    for f in sorted(proj_dir.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(proj_dir).as_posix()
        category = rel.split("/")[0] if "/" in rel else "root"
        files_list.append(
            {
                "name": f.name,
                "rel_path": f"Projects/{slug}/{rel}",
                "project_rel": rel,
                "category": category,
                "ext": f.suffix.lower(),
                "size_bytes": f.stat().st_size,
                "modified_at": dt.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    files_list.sort(
        key=lambda item: (
            0 if item["category"] == "Files" else (1 if item["category"] == "root" else 2),
            str(item["project_rel"]).lower(),
        )
    )
    files_dir_items = [item for item in files_list if item["category"] == "Files"]

    # Also include key CORA scripts & Vault indexes for the Script / Vault Viewer
    system_scripts: List[Dict[str, Any]] = []
    candidate_scripts = [
        CORE_DIR / "agent-cli.py",
        CORE_DIR / "Reasoning" / "reasoning_cli.py",
        CORE_DIR / "Reasoning" / "report_generator.py",
        CORE_DIR / "Reasoning" / "train_llm.py",
        CORE_DIR / "Reasoning" / "engines" / "pipeline.py",
        CORE_DIR / "Reasoning" / "engines" / "cegar_verifier.py",
        CORE_DIR / "Reasoning" / "engines" / "vault_bridge.py",
        CORE_DIR / "Reasoning" / "engines" / "context_vm.py",
        CORE_DIR / "Network_Isolation" / "console_posture.py",
        CORE_DIR / "Network_Isolation" / "network_isolation.conf",
        Path(VAULT_DIR) / "00_MEMORY_INDEX.md",
        Path(VAULT_DIR) / "00_TRAINED_INDEX.md",
    ]
    for sc in candidate_scripts:
        if sc.is_file():
            rel_root = sc.relative_to(CORA_ROOT).as_posix()
            system_scripts.append(
                {
                    "name": sc.name,
                    "rel_path": rel_root,
                    "category": "cora_core",
                    "ext": sc.suffix.lower(),
                    "size_bytes": sc.stat().st_size,
                    "modified_at": dt.datetime.fromtimestamp(sc.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

    return {
        "project_slug": slug,
        "files_dir": str(files_dir),
        "files_dir_rel": f"Projects/{slug}/Files",
        "files_dir_items": files_dir_items,
        "project_files": files_list,
        "system_scripts": system_scripts,
    }


def _resolve_safe_workspace_file(rel_path: str) -> Path:
    clean = (rel_path or "").strip().lstrip("/\\")
    if not clean:
        raise HTTPException(status_code=400, detail="Empty file path.")
    target = (CORA_ROOT / clean).resolve()
    root_resolved = CORA_ROOT.resolve()
    if not str(target).startswith(str(root_resolved)):
        raise HTTPException(status_code=403, detail="Access outside CORA repository root is forbidden.")
    return target


_TEXT_PREVIEW_EXTS = {
    ".txt", ".md", ".py", ".sh", ".ps1", ".bat", ".cmd", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".conf", ".csv", ".tsv", ".log", ".xml", ".html", ".htm",
    ".js", ".ts", ".svelte", ".css", ".sql", ".c", ".cpp", ".h", ".hpp", ".rs", ".go",
    ".java", ".rb", ".php", ".pl", ".lua", ".nmap", ".nessus", ".env", ".dockerfile",
}


def _is_likely_text_file(fpath: Path) -> bool:
    if not fpath.is_file():
        return False
    if fpath.suffix.lower() in _TEXT_PREVIEW_EXTS or fpath.name.lower() in ("dockerfile", "makefile", "readme", "license"):
        return True
    try:
        with open(fpath, "rb") as fh:
            chunk = fh.read(2048)
        if not chunk:
            return True
        if b"\x00" in chunk:
            return False
        return True
    except Exception:
        return False


def _resolve_project_file_path(project_slug: str, raw_path: str, for_write: bool = False) -> Path:
    """
    Resolve a file or directory path referenced by the LLM or user inside the active project's
    `Projects/<slug>/Files/` directory (or `Projects/<slug>/`).
    """
    proj_dir = ensure_project_structure(project_slug)
    files_dir = proj_dir / "Files"
    files_dir.mkdir(parents=True, exist_ok=True)

    raw_clean = (raw_path or "").strip().strip('"').strip("'").replace("\\", "/")
    if not raw_clean or raw_clean.lower() in (
        "files", "files/", "file", "file/", "local files", "local file",
        "local files directory", "local file directory", ".", "./",
    ):
        return files_dir.resolve()

    # Strip leading ./ or /
    while raw_clean.startswith("./"):
        raw_clean = raw_clean[2:]
    raw_clean = raw_clean.lstrip("/")

    # Check if it already starts with Projects/<slug>/
    slug_prefix = f"projects/{proj_dir.name.lower()}/"
    if raw_clean.lower().startswith(slug_prefix):
        sub_rel = raw_clean[len(slug_prefix):]
        cand = (proj_dir / sub_rel).resolve()
    elif raw_clean.lower().startswith("files/"):
        sub_rel = raw_clean[6:]
        cand = (files_dir / sub_rel).resolve()
    elif raw_clean.lower().startswith("file/"):
        sub_rel = raw_clean[5:]
        cand = (files_dir / sub_rel).resolve()
    else:
        cand_in_files = (files_dir / raw_clean).resolve()
        cand_in_proj = (proj_dir / raw_clean).resolve()
        cand_in_root = (CORA_ROOT / raw_clean).resolve()
        if for_write:
            cand = cand_in_files
        elif cand_in_files.exists():
            cand = cand_in_files
        elif cand_in_proj.exists():
            cand = cand_in_proj
        elif cand_in_root.exists() and str(cand_in_root).startswith(str(CORA_ROOT.resolve())):
            cand = cand_in_root
        else:
            cand = cand_in_files

    root_resolved = CORA_ROOT.resolve()
    if not str(cand).startswith(str(root_resolved)):
        raise ValueError(f"Path '{raw_path}' resolves outside the CORA workspace.")
    return cand


def _record_project_file_in_memory(proj_dir: Path, rel_in_files: str, action_label: str = "Added to Files/") -> None:
    try:
        mem_file = proj_dir / "memory.md"
        if not mem_file.is_file():
            return
        existing = mem_file.read_text(encoding="utf-8", errors="replace")
        marker = f"`Projects/{proj_dir.name}/Files/{rel_in_files}`"
        if marker in existing:
            return
        stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"- {marker} — {action_label} ({stamp})\n"
        if len(existing) < 28000:
            _atomic_write_text(mem_file, existing.rstrip() + "\n" + line)
    except Exception:
        pass


def get_project_files_context_block(
    proj_dir: Path,
    query_text: str = "",
    attached_files: Optional[List[str]] = None,
) -> str:
    """
    Build a structured context block describing `Projects/<slug>/Files/` and its contents so the LLM
    always knows where the local `Files` directory is, what custom scripts/files are inside it, and can
    immediately see previews of attached or referenced files.
    """
    slug = proj_dir.name
    files_dir = proj_dir / "Files"
    files_dir.mkdir(parents=True, exist_ok=True)

    all_files = sorted([f for f in files_dir.rglob("*") if f.is_file()], key=lambda p: p.name.lower())
    lines: List[str] = [
        f"### Local Project `Files` Directory (`Projects/{slug}/Files/`)",
        f"- **Relative Path:** `Projects/{slug}/Files/` (shorthand: `Files/<filename>`)",
        f"- **Full Host Path (`$PROJECT_FILES_DIR`):** `{files_dir}`",
        "- **How to Access & Use:** Whenever the operator asks you to check, read, analyze, or run anything in the local `Files` or `File` directory (or mentions an uploaded/custom script or file), look inside `Projects/"
        + slug
        + "/Files/`. You can call `read_project_file(path=\"Files/<name>\")`, `list_project_files_tool()`, `write_project_file(filename=\"<name>\", content=\"...\")`, or execute scripts via `run_shell_command` (note: `$PROJECT_FILES_DIR` is exported and `Projects/"
        + slug
        + "/Files` is prepended to `PATH`).",
    ]

    if not all_files:
        lines.append("- **Current Contents of `Projects/" + slug + "/Files/`:** `(empty — 0 files currently in Files/)`")
        return "\n".join(lines)

    lines.append(f"- **Current Contents of `Projects/{slug}/Files/` ({len(all_files)} file{'s' if len(all_files) != 1 else ''}):**")
    for idx, f in enumerate(all_files[:40], 1):
        rel_in_files = f.relative_to(files_dir).as_posix()
        rel_proj = f"Projects/{slug}/Files/{rel_in_files}"
        sz = f.stat().st_size
        mtime = dt.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"  {idx}. `Files/{rel_in_files}` (`{rel_proj}`, {sz} bytes, modified {mtime})")

    # Determine which files should have their contents auto-previewed in context
    q_low = (query_text or "").lower()
    attached_set = {
        str(a).strip().replace("\\", "/").lower()
        for a in (attached_files or [])
        if str(a).strip()
    }
    mentions_files_dir = bool(
        re.search(
            r"\b(?:files?\s+dir(?:ectory)?|local\s+files?|uploaded\s+files?|custom\s+scripts?|in\s+files|from\s+files|project\s+files)\b",
            q_low,
        )
    )

    preview_targets: List[Path] = []
    for f in all_files:
        rel_in_files = f.relative_to(files_dir).as_posix()
        rel_proj = f"Projects/{slug}/Files/{rel_in_files}"
        candidates_low = {
            f.name.lower(),
            f.stem.lower(),
            rel_in_files.lower(),
            f"files/{rel_in_files.lower()}",
            rel_proj.lower(),
        }
        is_attached = bool(attached_set & candidates_low)
        is_named_in_query = f.name.lower() in q_low or (len(f.stem) >= 3 and f.stem.lower() in q_low)
        if is_attached or is_named_in_query:
            preview_targets.append(f)

    if not preview_targets and (mentions_files_dir or len(all_files) <= 3):
        for f in all_files[:4]:
            if _is_likely_text_file(f) and f.stat().st_size <= 120000:
                preview_targets.append(f)

    total_preview_chars = 0
    for f in preview_targets[:5]:
        if total_preview_chars >= 12000:
            break
        rel_in_files = f.relative_to(files_dir).as_posix()
        if _is_likely_text_file(f):
            try:
                raw_txt = f.read_text(encoding="utf-8", errors="replace")
                snippet = raw_txt[:5000]
                total_preview_chars += len(snippet)
                trunc_note = f" (truncated from {len(raw_txt)} chars)" if len(raw_txt) > 5000 else ""
                lines.append(
                    f"\n#### File Preview: `Projects/{slug}/Files/{rel_in_files}`{trunc_note}\n"
                    f"```text\n{snippet}\n```"
                )
            except Exception as exc:
                lines.append(f"\n- Could not preview `Files/{rel_in_files}`: {exc}")
        else:
            lines.append(
                f"\n- Binary file `Projects/{slug}/Files/{rel_in_files}` ({f.stat().st_size} bytes) is available on disk at `{f}`."
            )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Local Inference Discovery (`llama-server` + `Ollama`) & Fast TTL Caches
# ---------------------------------------------------------------------------
_POSTURE_CACHE: Dict[str, Any] = {"ts": 0.0, "override": None, "data": None}
_ENGINE_STATUS_CACHE: Dict[str, Any] = {"ts": 0.0, "data": None}


def _get_cached_posture(override_str: str = "", ttl: float = 5.0) -> Dict[str, Any]:
    now = time.monotonic()
    if (
        _POSTURE_CACHE["data"] is not None
        and _POSTURE_CACHE["override"] == override_str
        and (now - float(_POSTURE_CACHE["ts"])) < ttl
    ):
        return _POSTURE_CACHE["data"]
    data = detect_console_posture(override=override_str)
    _POSTURE_CACHE["ts"] = now
    _POSTURE_CACHE["override"] = override_str
    _POSTURE_CACHE["data"] = data
    return data


def _get_cached_engine_status(ttl: float = 6.0) -> Dict[str, Any]:
    now = time.monotonic()
    if _ENGINE_STATUS_CACHE["data"] is not None and (now - float(_ENGINE_STATUS_CACHE["ts"])) < ttl:
        return _ENGINE_STATUS_CACHE["data"]
    data = get_system_status()
    _ENGINE_STATUS_CACHE["ts"] = now
    _ENGINE_STATUS_CACHE["data"] = data
    return data


def _is_url_port_reachable(url: str, timeout: float = 0.06) -> bool:
    """Fast TCP socket check so offline local ports fail in ~60ms on Windows/Linux."""
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        eff_timeout = 0.06 if host in ("127.0.0.1", "localhost", "::1") else timeout
        with socket.create_connection((host, port), timeout=eff_timeout):
            return True
    except Exception:
        return False


def _resolve_gguf_model(model_id: str) -> Dict[str, Any]:
    """
    Resolve a requested model identifier (`3.8`, `3.5`, `turbo`, `turbo-q6`, `turbo-q8`, or a custom GGUF stem/filename)
    to an installed `.gguf` file inside `MODELS_DIR`. If the requested model is not downloaded on disk yet,
    falls back to the best available installed `.gguf` file (`3.5` or `3.8`).
    """
    raw_id = (model_id or "3.8").strip()
    low_id = raw_id.lower()

    # Map common aliases
    alias_map = {
        "qwen3.8": "3.8",
        "27b": "3.8",
        "q3": "3.8",
        "qwen3.5": "3.5",
        "9b": "3.5",
        "fast": "3.5",
        "turbo-q4": "turbo",
        "mtp": "turbo",
        "q4": "turbo",
        "mtp-q6": "turbo-q6",
        "q6": "turbo-q6",
        "mtp-q8": "turbo-q8",
        "q8": "turbo-q8",
    }
    canon_id = alias_map.get(low_id, raw_id)

    def _find_catalog_path(entry: Dict[str, Any]) -> Optional[Path]:
        candidates = [entry["filename"]] + list(entry.get("alt_filenames") or [])
        for fname in candidates:
            p = MODELS_DIR / fname
            if p.is_file():
                return p
        return None

    # 1. Check catalog entries by id, alias, filename, or alt_filenames
    for item in CORA_MODEL_CATALOG:
        all_names = [
            item["id"].lower(),
            item.get("alias", "").lower(),
            item["filename"].lower(),
            Path(item["filename"]).stem.lower(),
        ] + [fn.lower() for fn in (item.get("alt_filenames") or [])] + [
            Path(fn).stem.lower() for fn in (item.get("alt_filenames") or [])
        ]
        if canon_id.lower() in all_names or raw_id.lower() in all_names:
            found_p = _find_catalog_path(item)
            if found_p is not None:
                return {
                    "id": item["id"],
                    "alias": item.get("alias") or Path(item["filename"]).stem,
                    "name": item["name"],
                    "path": found_p,
                    "installed": True,
                    "fallback": False,
                    "size_mib": int(found_p.stat().st_size // (1024 * 1024)),
                }

    # 2. Check custom .gguf files in MODELS_DIR
    if MODELS_DIR.is_dir():
        for gf in sorted(MODELS_DIR.glob("*.gguf")):
            if gf.name.startswith("mmproj"):
                continue
            if raw_id.lower() in (gf.name.lower(), gf.stem.lower()):
                return {
                    "id": gf.stem,
                    "alias": gf.stem,
                    "name": f"{gf.stem} (Local GGUF)",
                    "path": gf,
                    "installed": True,
                    "fallback": False,
                    "size_mib": int(gf.stat().st_size // (1024 * 1024)),
                }

    # 3. Fallback to any installed catalog GGUF (`3.8`, `3.5`, `turbo`, ...)
    for item in CORA_MODEL_CATALOG:
        found_p = _find_catalog_path(item)
        if found_p is not None:
            return {
                "id": item["id"],
                "alias": item.get("alias") or Path(item["filename"]).stem,
                "name": item["name"],
                "path": found_p,
                "installed": True,
                "fallback": True,
                "requested_id": raw_id,
                "size_mib": int(found_p.stat().st_size // (1024 * 1024)),
            }

    # 4. Fallback to any .gguf in MODELS_DIR
    if MODELS_DIR.is_dir():
        for gf in sorted(MODELS_DIR.glob("*.gguf")):
            if not gf.name.startswith("mmproj"):
                return {
                    "id": gf.stem,
                    "alias": gf.stem,
                    "name": gf.stem,
                    "path": gf,
                    "installed": True,
                    "fallback": True,
                    "requested_id": raw_id,
                    "size_mib": int(gf.stat().st_size // (1024 * 1024)),
                }

    default_item = CORA_MODEL_CATALOG[0]
    return {
        "id": default_item["id"],
        "alias": default_item.get("alias") or "Qwen3.8-27B-Uncensored-Q3_K_M",
        "name": default_item["name"],
        "path": MODELS_DIR / default_item["filename"],
        "installed": False,
        "fallback": False,
        "size_mib": 0,
    }


def _find_running_llama_process() -> Optional[Dict[str, Any]]:
    """
    Return information about any live `llama-server` / `llama-server.exe` process on the host,
    even during the initial 1-5 seconds before it binds TCP port 8080.
    """
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            pname = (proc.info.get("name") or "").lower()
            if pname in ("llama-server", "llama-server.exe"):
                if not proc.is_running() or proc.status() == psutil.STATUS_ZOMBIE:
                    continue
                cmdline = [str(x) for x in (proc.cmdline() or [])]
                alias_val = ""
                model_val = ""
                for idx, arg in enumerate(cmdline):
                    if arg == "--alias" and idx + 1 < len(cmdline):
                        alias_val = cmdline[idx + 1]
                    elif arg in ("--model", "-m") and idx + 1 < len(cmdline):
                        model_val = Path(cmdline[idx + 1]).name
                active_str = alias_val or model_val or "llama-server"
                if alias_val and model_val and model_val not in alias_val:
                    active_str = f"{alias_val} ({model_val})"
                return {
                    "pid": proc.info["pid"],
                    "active_model": active_str,
                    "cmdline": cmdline,
                }
        except Exception:
            continue
    return None


_LLAMA_HEALTH_CACHE: Dict[str, Any] = {"ts": 0.0, "base": "", "data": None}


def _get_llama_health(llama_base: str, ttl: float = 2.0) -> Dict[str, Any]:
    """
    Inspect `llama-server` health and active model on `llama_base` (e.g. `http://127.0.0.1:8080/v1`).
    Distinguishes between:
      - `state == "ok"`: server is ready for `/v1/chat/completions`
      - `state == "loading"`: `llama-server` process is alive and initializing CUDA / loading GGUF weights
      - `state == "offline"`: no `llama-server` process is running and TCP port is not reachable
    """
    base_clean = (llama_base or "http://127.0.0.1:8080/v1").rstrip("/")
    now_mono = time.monotonic()
    if (
        ttl > 0
        and _LLAMA_HEALTH_CACHE["data"] is not None
        and _LLAMA_HEALTH_CACHE["base"] == base_clean
        and (now_mono - float(_LLAMA_HEALTH_CACHE["ts"])) < ttl
    ):
        return dict(_LLAMA_HEALTH_CACHE["data"])

    llama_root = base_clean[:-3] if base_clean.endswith("/v1") else base_clean
    models_url = f"{base_clean}/models" if base_clean.endswith("/v1") else f"{base_clean}/v1/models"
    health_url = f"{llama_root}/health"

    live_proc = _find_running_llama_process()
    active_model = live_proc["active_model"] if live_proc else ""
    if not active_model and (LOG_DIR / "llama-server.model").is_file():
        try:
            active_model = (LOG_DIR / "llama-server.model").read_text(encoding="utf-8", errors="replace").strip()
        except Exception:
            pass

    if not _is_url_port_reachable(base_clean):
        if live_proc is not None:
            res_loading = {
                "online": False,
                "state": "loading",
                "pid": live_proc["pid"],
                "active_model": active_model,
                "detail": "Initializing CUDA & loading GGUF model into VRAM/RAM...",
            }
            _LLAMA_HEALTH_CACHE.update({"ts": now_mono, "base": base_clean, "data": res_loading})
            return dict(res_loading)
        res_off = {"online": False, "state": "offline", "active_model": "", "detail": "Port not reachable"}
        _LLAMA_HEALTH_CACHE.update({"ts": now_mono, "base": base_clean, "data": res_off})
        return dict(res_off)

    state = "offline"
    detail = ""
    try:
        req = urllib.request.Request(health_url, method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                state = "ok"
                detail = "ok"
    except urllib.error.HTTPError as he:
        err_txt = ""
        try:
            err_txt = he.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        if he.code == 503 or "loading" in err_txt.lower():
            res_503 = {
                "online": False,
                "state": "loading",
                "active_model": active_model,
                "detail": "Loading model weights into VRAM/RAM...",
            }
            _LLAMA_HEALTH_CACHE.update({"ts": now_mono, "base": base_clean, "data": res_503})
            return dict(res_503)
        detail = f"HTTP {he.code}: {err_txt[:160]}"
    except Exception as exc:
        detail = str(exc)

    try:
        req_m = urllib.request.Request(models_url, method="GET")
        with urllib.request.urlopen(req_m, timeout=1.5) as resp_m:
            if resp_m.status == 200:
                body = json.loads(resp_m.read().decode("utf-8", errors="replace"))
                if isinstance(body, dict) and body.get("data"):
                    active_model = str(body["data"][0].get("id", "")) or active_model
                if state != "ok":
                    state = "ok"
    except urllib.error.HTTPError as he:
        if he.code == 503 and state != "ok":
            res_m503 = {
                "online": False,
                "state": "loading",
                "active_model": active_model,
                "detail": "Loading model weights into VRAM/RAM...",
            }
            _LLAMA_HEALTH_CACHE.update({"ts": now_mono, "base": base_clean, "data": res_m503})
            return dict(res_m503)
    except Exception:
        pass

    if state == "offline" and live_proc is not None:
        state = "loading"
        detail = "Initializing model server..."

    res_final = {
        "online": state == "ok",
        "state": state,
        "active_model": active_model if state != "offline" else "",
        "detail": detail,
    }
    _LLAMA_HEALTH_CACHE.update({"ts": now_mono, "base": base_clean, "data": res_final})
    return dict(res_final)


def _find_llama_server_binary() -> Optional[Path]:
    bin_dir = CORE_DIR / "bin"
    exe_name = "llama-server.exe" if os.name == "nt" else "llama-server"
    direct = bin_dir / exe_name
    if direct.is_file():
        return direct
    if bin_dir.is_dir():
        for cand in bin_dir.rglob(exe_name):
            if cand.is_file():
                return cand
    which_p = shutil.which(exe_name)
    return Path(which_p) if which_p else None


def _model_matches_active(resolved: Dict[str, Any], active_model_str: str) -> bool:
    if not active_model_str:
        return True
    act_low = active_model_str.lower()
    cand_tokens = [
        str(resolved.get("id") or "").lower(),
        str(resolved.get("alias") or "").lower(),
        resolved["path"].name.lower(),
        resolved["path"].stem.lower(),
    ]
    return any(tok and len(tok) >= 3 and tok in act_low for tok in cand_tokens)


def _stop_llama_server_processes() -> None:
    pid_file = LOG_DIR / "llama-server.pid"
    if pid_file.is_file():
        try:
            raw_pid = pid_file.read_text(encoding="utf-8", errors="replace").strip()
            if raw_pid.isdigit():
                p = psutil.Process(int(raw_pid))
                p.terminate()
                try:
                    p.wait(timeout=2.5)
                except Exception:
                    p.kill()
        except Exception:
            pass
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            pname = (proc.info.get("name") or "").lower()
            if pname in ("llama-server", "llama-server.exe"):
                proc.terminate()
                try:
                    proc.wait(timeout=2.0)
                except Exception:
                    proc.kill()
        except Exception:
            pass
    for f in (LOG_DIR / "llama-server.pid", LOG_DIR / "llama-server.model"):
        try:
            if f.exists():
                f.unlink()
        except Exception:
            pass


def ensure_llama_server_running(
    model_id: str,
    cfg: Dict[str, str],
    wait_ready_sec: float = 90.0,
    force_restart: bool = False,
    prefer_running_model: bool = False,
) -> Dict[str, Any]:
    """
    Ensure `llama-server` is running on the configured local port with the requested `model_id`.
    If `llama-server` is stopped (or running a different model than requested), automatically
    starts/switches `core/bin/llama-server(.exe)` with hardware-tuned GPU/CPU arguments and waits
    for `/health` (`200 OK`).
    """
    global _LLAMA_LAST_ERROR
    llama_base = (cfg.get("llama_api_url") or "http://127.0.0.1:8080/v1").rstrip("/")
    parsed = urllib.parse.urlparse(llama_base)
    bind_host = parsed.hostname or "127.0.0.1"
    bind_port = parsed.port or 8080

    # Fast path before lock: if llama-server is already healthy and matches (or prefer_running_model=True), return immediately
    fast_health = _get_llama_health(llama_base)
    resolved = _resolve_gguf_model(model_id)
    if (
        not force_restart
        and fast_health["state"] == "ok"
        and (prefer_running_model or _model_matches_active(resolved, fast_health.get("active_model", "")))
    ):
        _LLAMA_LAST_ERROR = ""
        return {
            "online": True,
            "state": "ok",
            "active_model": fast_health.get("active_model") or resolved["alias"],
            "resolved": resolved,
        }

    if not resolved.get("installed") or not resolved["path"].is_file():
        err_msg = (
            f"No GGUF model file found at {resolved['path']}. "
            f"Run `run_cora_WIN.ps1 download -m {model_id}` (or `./run_cora_NIX.sh download -m {model_id}`) to download."
        )
        _LLAMA_LAST_ERROR = err_msg
        return {"online": False, "state": "error", "error": err_msg, "resolved": resolved}

    with _LLAMA_LOCK:
        health = _get_llama_health(llama_base)
        if (
            not force_restart
            and health["state"] == "ok"
            and (prefer_running_model or _model_matches_active(resolved, health.get("active_model", "")))
        ):
            _LLAMA_LAST_ERROR = ""
            return {
                "online": True,
                "state": "ok",
                "active_model": health.get("active_model") or resolved["alias"],
                "resolved": resolved,
            }

        # If llama-server is already in the middle of loading the requested model (or any model when prefer_running_model=True), wait for it
        if (
            not force_restart
            and health["state"] == "loading"
            and (prefer_running_model or _model_matches_active(resolved, health.get("active_model", "")))
        ):
            deadline = time.monotonic() + max(5.0, wait_ready_sec)
            while time.monotonic() < deadline:
                time.sleep(0.5)
                h_now = _get_llama_health(llama_base)
                if h_now["state"] == "ok":
                    _LLAMA_LAST_ERROR = ""
                    return {
                        "online": True,
                        "state": "ok",
                        "active_model": h_now.get("active_model") or resolved["alias"],
                        "resolved": resolved,
                    }
                if h_now["state"] == "offline":
                    break

        server_bin = _find_llama_server_binary()
        if server_bin is None or not server_bin.is_file():
            err_msg = f"llama-server binary not found in {CORE_DIR / 'bin'}. Run setup_cora_WIN.ps1 / setup_cora_NIX.sh."
            _LLAMA_LAST_ERROR = err_msg
            return {"online": False, "state": "error", "error": err_msg, "resolved": resolved}

        # Always stop any existing llama-server process before starting the requested model
        _stop_llama_server_processes()
        for _ in range(12):
            if not _is_url_port_reachable(llama_base) and _find_running_llama_process() is None:
                break
            time.sleep(0.25)

        # Hardware-aware tuning for llama-server
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        hw = collect_hardware_metrics()
        gpus = hw.get("gpus") or []
        vram_total_mib = int(gpus[0].get("vram_total_mb") or 0) if gpus else 0
        ram_info = hw.get("ram") or hw.get("memory") or {}
        ram_total_mib = int(float(ram_info.get("total_gb", 16)) * 1024)
        model_size_mib = int(resolved.get("size_mib") or 8000)

        logical_cpus = psutil.cpu_count(logical=True) or 8
        phys_cpus = psutil.cpu_count(logical=False) or max(1, logical_cpus // 2)
        threads = max(1, min(phys_cpus - 1 if phys_cpus > 4 else phys_cpus, 16))
        threads_batch = max(threads, min(logical_cpus, 24))

        gpu_headroom_mib = vram_total_mib - model_size_mib
        total_headroom_mib = (ram_total_mib + vram_total_mib) - model_size_mib
        if vram_total_mib > 0 and model_size_mib <= vram_total_mib:
            ctx_size = 16384 if gpu_headroom_mib >= 4000 else 8192
        elif total_headroom_mib >= 18000:
            ctx_size = 8192
        else:
            ctx_size = 4096

        cmd_args: List[str] = [
            str(server_bin),
            "--model",
            str(resolved["path"]),
            "--alias",
            str(resolved["alias"]),
            "--host",
            bind_host,
            "--port",
            str(bind_port),
            "--ctx-size",
            str(ctx_size),
            "--parallel",
            "1",
            "--context-shift",
            "--no-reasoning-preserve",
            "--reasoning",
            "off",
        ]

        if vram_total_mib > 0:
            fit_target = "256" if model_size_mib <= vram_total_mib else ("384" if vram_total_mib <= 8192 else "512")
            cmd_args.extend(
                [
                    "--fit",
                    "on",
                    "--fit-target",
                    fit_target,
                    "--flash-attn",
                    "on",
                    "--cache-type-k",
                    "q8_0",
                    "--cache-type-v",
                    "q8_0",
                ]
            )
            if gpu_headroom_mib >= 2048:
                cmd_args.extend(["--n-gpu-layers", "999"])
            batch_size, ubatch_size = ("2048", "512")
        else:
            cmd_args.extend(
                [
                    "--n-gpu-layers",
                    "0",
                    "--flash-attn",
                    "on",
                    "--cache-type-k",
                    "q8_0",
                    "--cache-type-v",
                    "q8_0",
                ]
            )
            batch_size, ubatch_size = ("1024", "256")

        cmd_args.extend(
            [
                "--repeat-penalty",
                "1.02",
                "--repeat-last-n",
                "64",
                "--threads",
                str(threads),
                "--threads-batch",
                str(threads_batch),
                "--batch-size",
                batch_size,
                "--ubatch-size",
                ubatch_size,
                "--cont-batching",
                "--no-webui",
            ]
        )

        env = os.environ.copy()
        bin_dir_str = str(server_bin.parent)
        env["PATH"] = bin_dir_str + os.pathsep + env.get("PATH", "")
        if os.name != "nt":
            env["LD_LIBRARY_PATH"] = bin_dir_str + ":" + env.get("LD_LIBRARY_PATH", "")

        err_log_path = LOG_DIR / "llama-server.log"
        out_log_path = LOG_DIR / "llama-server.stdout.log"
        err_fh = None
        out_fh = None
        try:
            err_fh = open(err_log_path, "w", encoding="utf-8", errors="replace")
            out_fh = open(out_log_path, "w", encoding="utf-8", errors="replace")
            popen_kwargs: Dict[str, Any] = {
                "cwd": str(CORE_DIR),
                "env": env,
                "stdout": out_fh,
                "stderr": err_fh,
                "stdin": subprocess.DEVNULL,
            }
            if os.name == "nt":
                popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
            proc = subprocess.Popen(cmd_args, **popen_kwargs)
        except Exception as exc:
            err_msg = f"Failed to spawn llama-server: {exc}"
            _LLAMA_LAST_ERROR = err_msg
            return {"online": False, "state": "error", "error": err_msg, "resolved": resolved}
        finally:
            for _fh in (err_fh, out_fh):
                if _fh is not None:
                    try:
                        _fh.close()
                    except Exception:
                        pass

        try:
            (LOG_DIR / "llama-server.pid").write_text(str(proc.pid), encoding="utf-8")
            (LOG_DIR / "llama-server.model").write_text(
                f"{resolved['alias']} ({resolved['path'].name})",
                encoding="utf-8",
            )
        except Exception:
            pass

        if wait_ready_sec <= 0:
            return {
                "online": False,
                "state": "loading",
                "pid": proc.pid,
                "active_model": f"{resolved['alias']} ({resolved['path'].name})",
                "resolved": resolved,
            }

        deadline = time.monotonic() + wait_ready_sec
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                tail_err = ""
                try:
                    tail_err = "\n".join(err_log_path.read_text(encoding="utf-8", errors="replace").splitlines()[-15:])
                except Exception:
                    pass
                err_msg = f"llama-server exited early (code {proc.returncode}). {tail_err}".strip()
                _LLAMA_LAST_ERROR = err_msg
                return {"online": False, "state": "error", "error": err_msg, "resolved": resolved}

            h_now = _get_llama_health(llama_base)
            if h_now["state"] == "ok":
                _LLAMA_LAST_ERROR = ""
                return {
                    "online": True,
                    "state": "ok",
                    "pid": proc.pid,
                    "active_model": h_now.get("active_model") or f"{resolved['alias']} ({resolved['path'].name})",
                    "resolved": resolved,
                }
            time.sleep(0.5)

        err_msg = f"llama-server is still loading {resolved['path'].name} after {int(wait_ready_sec)}s; retry in a few seconds."
        _LLAMA_LAST_ERROR = err_msg
        return {
            "online": False,
            "state": "loading",
            "pid": proc.pid,
            "error": err_msg,
            "active_model": f"{resolved['alias']} ({resolved['path'].name})",
            "resolved": resolved,
        }


def discover_models_and_backends(cfg: Dict[str, str]) -> Dict[str, Any]:
    llama_base = (cfg.get("llama_api_url") or "http://127.0.0.1:8080/v1").rstrip("/")
    ollama_base = (cfg.get("ollama_api_url") or "http://127.0.0.1:11434").rstrip("/")

    # 1. Check CORA GGUF files on disk (including alt_filenames)
    models_out: List[Dict[str, Any]] = []
    known_fnames = set()
    for item in CORA_MODEL_CATALOG:
        m_copy = dict(item)
        known_fnames.add(item["filename"])
        for af in item.get("alt_filenames") or []:
            known_fnames.add(af)
        gguf_path = MODELS_DIR / item["filename"]
        if not gguf_path.is_file():
            for af in item.get("alt_filenames") or []:
                alt_p = MODELS_DIR / af
                if alt_p.is_file():
                    gguf_path = alt_p
                    break
        m_copy["installed_on_disk"] = gguf_path.is_file()
        if gguf_path.is_file():
            m_copy["size_gb"] = round(gguf_path.stat().st_size / (1024**3), 2)
        models_out.append(m_copy)

    # Also scan Models/ for any custom .gguf files not in CORA_MODEL_CATALOG
    if MODELS_DIR.is_dir():
        for gf in sorted(MODELS_DIR.glob("*.gguf")):
            if gf.name not in known_fnames and not gf.name.startswith("mmproj"):
                models_out.append(
                    {
                        "id": gf.stem,
                        "name": f"{gf.stem} (Local GGUF)",
                        "filename": gf.name,
                        "provider": "llama-server",
                        "role": "Custom Local GGUF Model",
                        "vram_est": f"{round(gf.stat().st_size / (1024**3), 1)} GB",
                        "installed_on_disk": True,
                        "size_gb": round(gf.stat().st_size / (1024**3), 2),
                    }
                )

    # 2. Probe llama-server health / models
    llama_health = _get_llama_health(llama_base)
    llama_online = bool(llama_health.get("online"))
    llama_state = str(llama_health.get("state") or ("ok" if llama_online else "offline"))
    llama_active_model = str(llama_health.get("active_model") or "")

    # 3. Probe local Ollama (`/api/tags`)
    ollama_online = False
    ollama_models: List[Dict[str, Any]] = []
    if _is_url_port_reachable(ollama_base):
        try:
            req = urllib.request.Request(f"{ollama_base}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=1.2) as resp:
                if resp.status == 200:
                    ollama_online = True
                    data = json.loads(resp.read().decode("utf-8", errors="replace"))
                    for om in data.get("models", []):
                        m_name = str(om.get("name", ""))
                        size_b = int(om.get("size", 0))
                        if m_name:
                            entry = {
                                "id": f"ollama:{m_name}",
                                "name": f"{m_name} (Ollama)",
                                "filename": m_name,
                                "provider": "ollama",
                                "role": "Ollama Local Model",
                                "vram_est": f"{round(size_b / (1024**3), 1)} GB" if size_b else "Dynamic",
                                "installed_on_disk": True,
                            }
                            ollama_models.append(entry)
                            models_out.append(entry)
        except Exception:
            pass

    return {
        "selected_model": cfg.get("selected_model", "3.8"),
        "inference_provider": cfg.get("inference_provider", "llama-server"),
        "llama_server": {
            "online": llama_online,
            "state": llama_state,
            "api_url": llama_base,
            "active_model": llama_active_model,
            "last_error": _LLAMA_LAST_ERROR,
        },
        "ollama": {
            "online": ollama_online,
            "api_url": ollama_base,
            "model_count": len(ollama_models),
        },
        "models": models_out,
    }


# ---------------------------------------------------------------------------
# LLM Inference & Agentic Tool Execution
# ---------------------------------------------------------------------------
WEBUI_READONLY_AGENT_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "read_project_file",
            "description": (
                "Read the contents of a file inside the active project's local `Files` directory "
                "(`Projects/<project>/Files/<filename>`) or project workspace (`Projects/<project>/...`). "
                "Use this whenever the operator asks you to look at, inspect, or use a file or script in the local `Files` directory."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "File name or relative path inside `Projects/<project>/Files/` (e.g. 'custom_check.py', "
                            "'Files/custom_check.py', or 'Projects/<project>/Files/custom_check.py')."
                        ),
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_project_files_tool",
            "description": (
                "List all files inside the active project's local `Files` directory (`Projects/<project>/Files/`) "
                "and project workspace subdirectories."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "subdir": {
                        "type": "string",
                        "description": "Optional subdirectory to list (defaults to 'Files').",
                    }
                },
            },
        },
    },
]

WEBUI_AGENT_TOOLS: List[Dict[str, Any]] = [
    *WEBUI_READONLY_AGENT_TOOLS,
    {
        "type": "function",
        "function": {
            "name": "write_project_file",
            "description": (
                "Create or update a script, configuration, or output file inside the active project's local `Files` directory "
                "(`Projects/<project>/Files/<filename>`)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "File name or relative path inside `Projects/<project>/Files/` (e.g. 'helper.py' or 'Files/output.txt').",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full text content to write to the file.",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell_command",
            "description": (
                "Execute a host command (PowerShell/CMD/Sysinternals on Windows, bash on Linux) or run a custom script "
                "located in the active project's local `Files` directory (`$PROJECT_FILES_DIR` / `Projects/<project>/Files/`, "
                "which is automatically on `PATH`)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The single-line command to execute on the host.",
                    }
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scan_target",
            "description": (
                "Probe a target IP, hostname, or URL across common HTTP/HTTPS management ports (80, 443, 8080, 8443, 10443) "
                "to identify appliance/server versions (e.g., Fortinet FortiGate/FortiOS, Apache, Nginx), TLS certificates, "
                "HTTP headers, and login page endpoints."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Target IP address, hostname, or URL (e.g., 192.168.1.99 or https://192.168.1.99).",
                    }
                },
                "required": ["target"],
            },
        },
    },
]


def _execute_webui_read_project_file(path_arg: str, project_slug: str) -> Dict[str, Any]:
    try:
        resolved = _resolve_project_file_path(project_slug, path_arg, for_write=False)
        if resolved.is_dir():
            entries = sorted([p.name + ("/" if p.is_dir() else f" ({p.stat().st_size} bytes)") for p in resolved.iterdir()])
            rel_str = resolved.relative_to(CORA_ROOT.resolve()).as_posix()
            out = f"Directory `{rel_str}` ({len(entries)} entries):\n" + ("\n".join(f"- {e}" for e in entries) if entries else "(empty)")
            return {"executed": True, "blocked": False, "exit_code": 0, "output": out}
        if not resolved.is_file():
            proj_dir = ensure_project_structure(project_slug)
            files_dir = proj_dir / "Files"
            avail = [f.relative_to(files_dir).as_posix() for f in sorted(files_dir.rglob("*")) if f.is_file()]
            avail_str = ", ".join(f"`Files/{a}`" for a in avail) if avail else "(no files in Files/)"
            return {
                "executed": False,
                "blocked": False,
                "exit_code": 1,
                "output": f"File not found: `{path_arg}`. Available files in `Projects/{proj_dir.name}/Files/`: {avail_str}",
            }
        rel_str = resolved.relative_to(CORA_ROOT.resolve()).as_posix()
        if _is_likely_text_file(resolved):
            txt = resolved.read_text(encoding="utf-8", errors="replace")
            out = f"=== File: `{rel_str}` ({resolved.stat().st_size} bytes) ===\n{txt[:25000]}"
        else:
            out = f"=== Binary File: `{rel_str}` ({resolved.stat().st_size} bytes) at `{resolved}` ==="
        return {"executed": True, "blocked": False, "exit_code": 0, "output": out}
    except Exception as exc:
        return {"executed": False, "blocked": False, "exit_code": 1, "output": f"Error reading `{path_arg}`: {exc}"}


def _execute_webui_list_project_files(subdir_arg: str, project_slug: str) -> Dict[str, Any]:
    try:
        proj_dir = ensure_project_structure(project_slug)
        files_dir = proj_dir / "Files"
        files_dir.mkdir(parents=True, exist_ok=True)
        items = sorted([f for f in files_dir.rglob("*") if f.is_file()], key=lambda p: p.name.lower())
        lines = [
            f"=== Local Project `Files` Directory (`Projects/{proj_dir.name}/Files/`) ===",
            f"Full Host Path (`$PROJECT_FILES_DIR`): {files_dir}",
            f"Total Files in `Files/`: {len(items)}",
        ]
        for idx, f in enumerate(items, 1):
            rel = f.relative_to(files_dir).as_posix()
            lines.append(f"  {idx}. Files/{rel} (Projects/{proj_dir.name}/Files/{rel} — {f.stat().st_size} bytes)")
        if not items:
            lines.append("  (No files currently in Projects/" + proj_dir.name + "/Files/)")
        return {"executed": True, "blocked": False, "exit_code": 0, "output": "\n".join(lines)}
    except Exception as exc:
        return {"executed": False, "blocked": False, "exit_code": 1, "output": f"Error listing project files: {exc}"}


def _execute_webui_write_project_file(
    filename_arg: str,
    content_arg: str,
    mode_info: Dict[str, Any],
    project_slug: str,
) -> Dict[str, Any]:
    if mode_info.get("read_only"):
        return {
            "executed": False,
            "blocked": True,
            "reason": "Blocked by [2] Analyst (Read-Only) mode: writing files is disabled.",
        }
    try:
        proj_dir = ensure_project_structure(project_slug)
        files_dir = (proj_dir / "Files").resolve()
        clean_name = (filename_arg or "").strip().replace("\\", "/").lstrip("/")
        if clean_name.lower().startswith(f"projects/{proj_dir.name.lower()}/files/"):
            clean_name = clean_name[len(f"projects/{proj_dir.name.lower()}/files/"):]
        elif clean_name.lower().startswith("files/"):
            clean_name = clean_name[6:]
        if not clean_name or ".." in clean_name.split("/"):
            return {"executed": False, "blocked": True, "reason": f"Invalid target filename: {filename_arg}"}
        target = (files_dir / clean_name).resolve()
        if not str(target).startswith(str(files_dir)):
            return {"executed": False, "blocked": True, "reason": "Target file must reside inside `Projects/<project>/Files/`."}
        target.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(target, content_arg)
        rel_in_files = target.relative_to(files_dir).as_posix()
        _record_project_file_in_memory(proj_dir, rel_in_files, "Created/updated by CORA LLM in Files/")
        return {
            "executed": True,
            "blocked": False,
            "exit_code": 0,
            "output": f"Saved `Projects/{proj_dir.name}/Files/{rel_in_files}` ({target.stat().st_size} bytes).",
        }
    except Exception as exc:
        return {"executed": False, "blocked": False, "exit_code": 1, "output": f"Error writing `{filename_arg}`: {exc}"}


def _extract_xml_tool_calls(text: str) -> List[Dict[str, Any]]:
    """Parse `<tool_call>{"name": ..., "arguments": ...}</tool_call>` blocks if emitted inline by Qwen models."""
    calls: List[Dict[str, Any]] = []
    for idx, m in enumerate(re.finditer(r"(?is)<tool_call>\s*(\{.*?\})\s*</tool_call>", text or "")):
        try:
            obj = json.loads(m.group(1))
            fn_name = str(obj.get("name") or "")
            fn_args = obj.get("arguments") or {}
            if isinstance(fn_args, str):
                try:
                    fn_args = json.loads(fn_args)
                except Exception:
                    fn_args = {"command": fn_args}
            if fn_name:
                calls.append(
                    {
                        "id": f"call_xml_{idx}",
                        "type": "function",
                        "function": {
                            "name": fn_name,
                            "arguments": json.dumps(fn_args),
                        },
                    }
                )
        except Exception:
            continue
    return calls


def _execute_webui_target_scan(
    target: str,
    mode_info: Dict[str, Any],
    posture: Dict[str, Any],
    project_slug: str,
) -> Dict[str, Any]:
    """
    Perform a safe, CEGAR-verified multi-port HTTP/HTTPS/TCP/SSH metadata inspection against `target`
    (respecting WHITE air-gap, BLUE allowed interfaces/subnets, and Analyst read-only mode).
    Implemented directly in Python (`socket`, `ssl`, `urllib.request`) after CEGAR & isolation verification
    so Windows/Linux shell quoting never mangles URLs or headers.
    """
    raw_target = (target or "").strip()
    if not raw_target:
        return {"executed": False, "blocked": True, "command": "scan_target", "reason": "Empty target."}

    if mode_info.get("read_only"):
        return {
            "executed": False,
            "blocked": True,
            "command": f"scan_target({raw_target})",
            "reason": "Blocked by Mode [2] Analyst (Strictly Read-Only & White Air-Gap).",
        }

    host_only = re.sub(r"^https?://", "", raw_target, flags=re.I).split("/")[0].split(":")[0].strip()
    if not host_only:
        return {"executed": False, "blocked": True, "command": f"scan_target({raw_target})", "reason": "Invalid target host."}

    # 1. Run ICMP ping through execute_safe_shell_command so Engine 9 CEGAR + WHITE/BLUE isolation rules
    #    are strictly enforced before any socket connections are attempted.
    ping_cmd = f"ping -n 2 -w 1200 {host_only}" if os.name == "nt" else f"ping -c 2 -W 1 {host_only}"
    ping_res = execute_safe_shell_command(ping_cmd, mode_info, posture, project_slug)
    if ping_res.get("blocked"):
        return ping_res

    t0 = time.perf_counter()
    report_lines: List[str] = [
        f"=== Target Telemetry & Service Inspection: {host_only} ===",
        "--- [1] ICMP Reachability ---",
        str(ping_res.get("output") or "(no ping output)").strip(),
        "",
        "--- [2] TCP Port State & Banner Inspection ---",
    ]

    open_ports: List[int] = []
    for port in (80, 443, 8080, 8443, 10443, 22):
        try:
            with socket.create_connection((host_only, port), timeout=1.5) as sock:
                open_ports.append(port)
                banner_info = ""
                if port == 22:
                    try:
                        sock.settimeout(1.5)
                        raw_banner = sock.recv(256).decode("utf-8", errors="replace").strip()
                        if raw_banner:
                            banner_info = f" | Banner: {raw_banner}"
                    except Exception:
                        pass
                report_lines.append(f"PORT {port}/tcp: OPEN{banner_info}")
        except Exception:
            report_lines.append(f"PORT {port}/tcp: closed/filtered")

    # 3. TLS Certificate & Cipher Inspection on open HTTPS ports
    tls_ports = [p for p in (443, 8443, 10443) if p in open_ports]
    if tls_ports:
        report_lines.append("")
        report_lines.append("--- [3] TLS / SSL Handshake & Certificate Telemetry ---")
        for tp in tls_ports:
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with socket.create_connection((host_only, tp), timeout=2.5) as raw_sock:
                    with ctx.wrap_socket(raw_sock, server_hostname=host_only) as tls_sock:
                        tls_ver = tls_sock.version()
                        cipher = tls_sock.cipher()
                        der_cert = tls_sock.getpeercert(binary_form=True)
                        cert_note = f"DER_len={len(der_cert)}B" if der_cert else "none"
                        if der_cert:
                            # Extract printable ASCII tokens (CN, OU, Fortinet serial/model strings) from DER cert
                            ascii_runs = re.findall(rb"[A-Za-z0-9_.\-: /]{4,64}", der_cert)
                            decoded_runs = []
                            for r_bytes in ascii_runs:
                                s_val = r_bytes.decode("ascii", errors="ignore").strip()
                                if s_val and s_val not in decoded_runs:
                                    decoded_runs.append(s_val)
                            if decoded_runs:
                                cert_note += " | Cert Strings: " + ", ".join(decoded_runs[:16])
                        report_lines.append(f"PORT {tp}/tls: Version={tls_ver}, Cipher={cipher}, {cert_note}")
            except Exception as tls_exc:
                report_lines.append(f"PORT {tp}/tls: Handshake error ({tls_exc})")

    # 4. HTTP / HTTPS Endpoint & Header Inspection
    probe_urls: List[str] = []
    if 443 in open_ports or not open_ports:
        probe_urls.extend(
            [
                f"https://{host_only}/",
                f"https://{host_only}/login",
                f"https://{host_only}/remote/login",
                f"https://{host_only}/ng/",
            ]
        )
    if 8443 in open_ports:
        probe_urls.append(f"https://{host_only}:8443/")
    if 10443 in open_ports:
        probe_urls.append(f"https://{host_only}:10443/remote/login")
    if 80 in open_ports or not open_ports:
        probe_urls.append(f"http://{host_only}/")
    if 8080 in open_ports:
        probe_urls.append(f"http://{host_only}:8080/")

    report_lines.append("")
    report_lines.append("--- [4] HTTP/HTTPS Headers & Page Fingerprints ---")
    unverified_ctx = ssl._create_unverified_context()
    discovered_assets: List[str] = []
    base_origin = f"https://{host_only}" if 443 in open_ports else f"http://{host_only}"
    for url in probe_urls[:6]:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CORA-Diagnostic/5.15"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=3.5, context=unverified_ctx) as resp:
                status_code = resp.getcode()
                final_url = resp.geturl()
                hdrs = {k: v for k, v in resp.info().items()}
                body_bytes = resp.read(16384)
                body_str = body_bytes.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as he:
            status_code = he.code
            final_url = url
            hdrs = {k: v for k, v in he.headers.items()} if he.headers else {}
            try:
                body_str = he.read(8192).decode("utf-8", errors="replace")
            except Exception:
                body_str = ""
        except Exception as req_exc:
            report_lines.append(f"[{url}] -> Connection/Request Error: {req_exc}")
            continue

        title_m = re.search(r"(?is)<title[^>]*>(.*?)</title>", body_str)
        page_title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else "(no <title>)"
        assets = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', body_str, flags=re.I)
        for a_path in assets:
            if a_path.startswith("/") and a_path not in discovered_assets:
                discovered_assets.append(a_path)
        hdr_summary = ", ".join(f"{k}: {v}" for k, v in list(hdrs.items())[:12])
        body_preview = re.sub(r"\s+", " ", body_str).strip()[:600]
        report_lines.append(f"[{url}] -> HTTP {status_code} (Final URL: {final_url})")
        report_lines.append(f"  Headers: {hdr_summary}")
        report_lines.append(f"  Title: {page_title}")
        if assets:
            report_lines.append(f"  Linked Assets: {', '.join(assets[:8])}")
        if body_preview:
            report_lines.append(f"  Body Snippet: {body_preview}")

    # 5. Deep Static Asset & Build/Firmware Timestamp Inspection
    if discovered_assets:
        report_lines.append("")
        report_lines.append("--- [5] Static Asset & Build Timestamp Fingerprints ---")
        for a_rel in discovered_assets[:3]:
            a_url = f"{base_origin}{a_rel}"
            try:
                a_req = urllib.request.Request(
                    a_url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CORA-Diagnostic/5.15"},
                    method="GET",
                )
                with urllib.request.urlopen(a_req, timeout=3.5, context=unverified_ctx) as a_resp:
                    a_code = a_resp.getcode()
                    a_hdrs = {k: v for k, v in a_resp.info().items()}
                    a_body = a_resp.read(16384).decode("utf-8", errors="replace")
                last_mod = a_hdrs.get("Last-Modified") or a_hdrs.get("last-modified") or "N/A"
                etag_val = a_hdrs.get("ETag") or a_hdrs.get("etag") or "N/A"
                ver_tokens = re.findall(
                    r"(?:version|build|release|fortios|fgt|v\d+\.\d+\.\d+)[^;,\n\"']{0,48}",
                    a_body,
                    flags=re.I,
                )
                report_lines.append(
                    f"[{a_url}] -> HTTP {a_code} | Last-Modified (Firmware Build Date): {last_mod} | ETag: {etag_val}"
                )
                if ver_tokens:
                    clean_toks = []
                    for vt in ver_tokens:
                        vt_c = re.sub(r"\s+", " ", vt).strip()
                        if vt_c and vt_c not in clean_toks:
                            clean_toks.append(vt_c)
                    report_lines.append(f"  Extracted Asset Version/Build Tokens: {', '.join(clean_toks[:8])}")
            except Exception as a_exc:
                report_lines.append(f"[{a_url}] -> Asset probe error: {a_exc}")

    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 1)
    combined_out = "\n".join(report_lines)
    sygus_facts = extract_structured_facts(f"scan_target {host_only}", combined_out)
    if not mode_info.get("read_only"):
        try:
            record_command_event(f"scan_target {host_only}", combined_out, 0)
            record_live_command_experience(f"scan_target {host_only}", 0, combined_out)
            facts_cnt = (
                len(sygus_facts.get("arp_neighbors", []))
                + len(sygus_facts.get("open_ports", []))
                + len(sygus_facts.get("routes", []))
                + (1 if sygus_facts.get("summary_header") else 0)
            )
            record_rl_step_transition(
                command=f"scan_target {host_only}",
                exit_code=0,
                new_facts_count=facts_cnt,
            )
        except Exception:
            pass
    return {
        "executed": True,
        "blocked": False,
        "command": f"scan_target({host_only})",
        "exit_code": 0,
        "output": combined_out[:12000],
        "latency_ms": elapsed_ms,
        "sygus_facts": sygus_facts,
        "cegar": ping_res.get("cegar") or {},
    }


def _call_llm_backend(
    messages: List[Dict[str, Any]],
    model_id: str,
    cfg: Dict[str, str],
    thinking_enabled: bool = True,
    tools: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Route conversation to `Ollama` (if `model_id` starts with `ollama:` or provider is `ollama`)
    or `llama-server` (`/v1/chat/completions`).
    Automatically starts `llama-server` if stopped, waits for `/health` (`200 OK`), retries on `HTTP 503`
    (`Loading model`), and supports OpenAI-compatible `tools` / `tool_calls`.
    """
    is_ollama = model_id.startswith("ollama:") or cfg.get("inference_provider") == "ollama"
    if is_ollama:
        ollama_base = (cfg.get("ollama_api_url") or "http://127.0.0.1:11434").rstrip("/")
        if not _is_url_port_reachable(ollama_base):
            return {"online": False, "error": f"Ollama server at {ollama_base} is not listening.", "provider": "ollama"}
        clean_model = model_id.split(":", 1)[1] if model_id.startswith("ollama:") else model_id
        payload = json.dumps(
            {
                "model": clean_model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.4},
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{ollama_base}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                raw = json.loads(resp.read().decode("utf-8", errors="replace"))
            content = str((raw.get("message") or {}).get("content") or "")
            return _split_thinking_and_reply(content, provider="ollama", model=clean_model)
        except urllib.error.HTTPError as he:
            body_err = ""
            try:
                body_err = he.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            return {"online": False, "error": f"Ollama HTTP {he.code}: {body_err or he.reason}", "provider": "ollama"}
        except Exception as exc:
            return {"online": False, "error": f"Ollama error: {exc}", "provider": "ollama"}

    llama_base = (cfg.get("llama_api_url") or "http://127.0.0.1:8080/v1").rstrip("/")
    ensure_res = ensure_llama_server_running(
        model_id=model_id,
        cfg=cfg,
        wait_ready_sec=90.0,
        prefer_running_model=True,
    )
    if not ensure_res.get("online"):
        return {
            "online": False,
            "error": str(ensure_res.get("error") or f"llama-server at {llama_base} could not be started."),
            "provider": "llama-server",
        }

    resolved_info = ensure_res.get("resolved") or {}
    effective_alias = str(ensure_res.get("active_model") or resolved_info.get("alias") or model_id or "cora-model")
    if " (" in effective_alias:
        effective_alias = effective_alias.split(" (", 1)[0].strip()
    chat_url = f"{llama_base}/v1/chat/completions" if not llama_base.endswith("/v1") else f"{llama_base}/chat/completions"

    def _build_request(msgs: List[Dict[str, Any]], max_toks: int = 1536, include_tools: bool = True) -> urllib.request.Request:
        payload_dict: Dict[str, Any] = {
            "model": effective_alias,
            "messages": msgs,
            "temperature": 0.4,
            "max_tokens": max_toks,
            "chat_template_kwargs": {"enable_thinking": bool(thinking_enabled)},
        }
        if tools and include_tools:
            payload_dict["tools"] = tools
            payload_dict["tool_choice"] = "auto"
        return urllib.request.Request(
            chat_url,
            data=json.dumps(payload_dict).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

    cur_messages = list(messages)
    include_tools_flag = bool(tools)
    for attempt in range(3):
        try:
            req = _build_request(cur_messages, max_toks=1536, include_tools=include_tools_flag)
            with urllib.request.urlopen(req, timeout=240) as resp:
                raw = json.loads(resp.read().decode("utf-8", errors="replace"))
            choice_msg = (raw.get("choices") or [{}])[0].get("message") or {}
            content = str(choice_msg.get("content") or "")
            reasoning_field = str(choice_msg.get("reasoning_content") or "")
            tool_calls = choice_msg.get("tool_calls") or []
            if not tool_calls and "<tool_call>" in content:
                tool_calls = _extract_xml_tool_calls(content)
                content = re.sub(r"(?is)<tool_call>.*?</tool_call>", "", content).strip()
            res = _split_thinking_and_reply(content, provider="llama-server", model=effective_alias)
            if reasoning_field and not res["thinking"]:
                res["thinking"] = reasoning_field.strip()
            res["tool_calls"] = tool_calls
            res["raw_assistant_message"] = choice_msg
            return res
        except urllib.error.HTTPError as he:
            err_body = ""
            try:
                err_body = he.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            if he.code == 503 and attempt < 2:
                ensure_llama_server_running(
                    model_id=model_id,
                    cfg=cfg,
                    wait_ready_sec=45.0,
                    prefer_running_model=True,
                )
                continue
            if he.code == 400 and attempt < 2:
                if include_tools_flag and ("tool" in err_body.lower() or "template" in err_body.lower()):
                    include_tools_flag = False
                    continue
                cur_messages = [cur_messages[0]] + [
                    {"role": m.get("role", "user"), "content": str(m.get("content") or "")[:1600]}
                    for m in cur_messages[-2:]
                    if m.get("role") in ("user", "assistant")
                ]
                continue
            return {
                "online": False,
                "error": f"llama-server HTTP {he.code}: {err_body[:300] or he.reason}",
                "provider": "llama-server",
            }
        except (urllib.error.URLError, ConnectionError, TimeoutError) as net_exc:
            if attempt == 0:
                ensure_llama_server_running(
                    model_id=model_id,
                    cfg=cfg,
                    wait_ready_sec=60.0,
                    prefer_running_model=True,
                )
                continue
            return {
                "online": False,
                "error": f"llama-server connection/timeout error: {net_exc}",
                "provider": "llama-server",
            }
        except Exception as exc:
            return {"online": False, "error": f"llama-server error: {exc}", "provider": "llama-server"}

    return {"online": False, "error": "llama-server failed after 3 attempts.", "provider": "llama-server"}


def _split_thinking_and_reply(raw_text: str, provider: str, model: str) -> Dict[str, Any]:
    thinking_parts: List[str] = []
    for m in re.finditer(r"(?is)<think>(.*?)</think>", raw_text or ""):
        if m.group(1).strip():
            thinking_parts.append(m.group(1).strip())
    clean_reply = re.sub(r"(?is)<think>.*?</think>", "", raw_text or "").strip()
    return {
        "online": True,
        "provider": provider,
        "model": model,
        "thinking": "\n\n".join(thinking_parts),
        "content": clean_reply or (raw_text or "").strip(),
    }


def _format_internal_thinking_and_engine_trace(
    thinking_parts: List[str],
    reasoning_res: Dict[str, Any],
    executed_cmds_list: List[str],
    executed_outs_list: List[str],
    posture: Dict[str, Any],
    mode_info: Dict[str, Any],
) -> str:
    """
    Build the full internal thought process, tool execution trace, and 15-Engine Neuro-Symbolic
    diagnostics string. This trace is hidden by default in the CORA output pane and expanded on
    demand when the operator presses `Ctrl+O` (Antigravity-style thought process toggle).
    """
    sections: List[str] = []

    clean_thinks = [t.strip() for t in (thinking_parts or []) if t and t.strip()]
    if clean_thinks:
        sections.append("=== LLM Chain-of-Thought (<think>) Process ===\n" + "\n\n".join(clean_thinks))

    if executed_cmds_list:
        cmd_lines = [f"  {idx + 1}. {c}" for idx, c in enumerate(executed_cmds_list)]
        sections.append("=== Executed Tactical Probes & Tool Calls ===\n" + "\n".join(cmd_lines))

    if reasoning_res:
        consensus_cmd = reasoning_res.get("consensus_immediate_action") or "N/A"
        cegar = reasoning_res.get("cegar_verification") or {}
        top_cause = reasoning_res.get("top_root_cause") or "N/A"
        top_prob = float(reasoning_res.get("top_root_cause_probability") or 0.0)
        conflict_k = float(reasoning_res.get("dempster_shafer_conflict_k") or 0.0)
        ignorance_m = float(reasoning_res.get("dempster_shafer_ignorance") or 0.0)
        mdp_tactic = reasoning_res.get("mdp_optimal_tactic") or "Reconnaissance"
        mdp_tool = reasoning_res.get("mdp_optimal_tool") or "nmap"
        mdp_q = reasoning_res.get("mdp_optimal_q_star") or 0.0
        stop_dec = (reasoning_res.get("optimal_stopping") or {}).get("decision", "HOLD_OPTIMAL_TACTIC_LINE")
        rl_imm = reasoning_res.get("rl_immediate_action") or {}
        pca_cluster = (reasoning_res.get("pca_cluster_assignment") or {}).get("cluster_id", "N/A")
        pca_var = reasoning_res.get("pca_cumulative_variance_pct") or 0.0
        vsa_arch = reasoning_res.get("vsa_top_archetype") or {}
        vsa_name = vsa_arch.get("archetype", str(vsa_arch)) if isinstance(vsa_arch, dict) else str(vsa_arch or "N/A")
        somatic_val = float(reasoning_res.get("somatic_gut_valence") or 0.0)
        brier = float(reasoning_res.get("meta_brier_score") or 0.085)
        ece = float(reasoning_res.get("meta_ece_pct") or 4.2)

        eng_block = "\n".join(
            [
                f"=== 15-Engine Neuro-Symbolic Trace ({reasoning_res.get('pipeline_latency_ms', 0)} ms) ===",
                f"• Session Posture: {posture.get('hud_badge', 'NET:RED')} | Mode: [{mode_info.get('number', 1)}] {mode_info.get('label', 'Default')}",
                f"• Consensus Action: {consensus_cmd}",
                f"• Engine 9 (CEGAR Safety Verifier): {'BLOCKED' if cegar.get('blocked') else 'VERIFIED SAFE'}",
                f"• Engine 11 (H-MDP Bellman Policy): {mdp_tactic} -> {mdp_tool} (Q*={mdp_q} | Stopping={stop_dec})",
                f"• Engine 14 (Trajectory RL): State={reasoning_res.get('rl_state_key', 'N/A')} -> {rl_imm.get('command', 'N/A')} (Q*={rl_imm.get('q_star', 0)})",
                f"• Engine 3 (Bayesian Top Hypothesis): {top_cause} ({round(top_prob * 100, 1)}%)",
                f"• Engine 7 (Dempster-Shafer Fusion): Conflict K={conflict_k:.3f}, Ignorance m(Θ)={ignorance_m:.3f}",
                f"• Engine 5 (1,024-D VSA & Somatic Intuition): {vsa_name} (Valence={somatic_val:+.2f})",
                f"• Engine 15 (Spectral PCA & K-Means): Cluster={pca_cluster} (Top-3 Variance={pca_var}%)",
                f"• Engine 13 (META-MIND Calibration): Brier={brier:.3f} | ECE={ece:.1f}%",
            ]
        )
        sections.append(eng_block)

    return "\n\n".join(sections).strip()


def _synthesize_neuro_symbolic_fallback_response(
    query: str,
    reasoning_res: Dict[str, Any],
    posture: Dict[str, Any],
    mode_info: Dict[str, Any],
    project_slug: str,
    llm_error: str = "",
    cmd_res: Optional[Dict[str, Any]] = None,
) -> str:
    """
    When `llama-server` / `Ollama` is on standby, return a clean, readable tactical response
    without cluttering the main output window with all 15 internal reasoning engine metrics
    (those remain tucked inside the `Ctrl+O` expandable thought process pane).
    """
    consensus_cmd = reasoning_res.get("consensus_immediate_action") or "ip -4 -br addr show"
    top_cause = reasoning_res.get("top_root_cause") or "General Tactical Assessment"
    top_prob = float(reasoning_res.get("top_root_cause_probability") or 0.0)
    mdp_tactic = reasoning_res.get("mdp_optimal_tactic") or "Reconnaissance"

    lines: List[str] = []
    if cmd_res and cmd_res.get("command"):
        if cmd_res.get("blocked"):
            lines.append(f"### Command Guardrail Verdict (`{cmd_res.get('command')}`)")
            lines.append(f"- **Status:** `BLOCKED` — {cmd_res.get('reason')}")
            lines.append("")
        elif cmd_res.get("output"):
            lines.append(f"### Command Probe Output (`{cmd_res.get('command')}`)")
            lines.append(f"```text\n{str(cmd_res.get('output'))[:4000]}\n```")
            lines.append("")

    lines.extend(
        [
            f"### C.O.R.A. Tactical Assessment (`Projects/{project_slug}/`)",
            f"- **Primary Finding / Focus:** `{top_cause}` ({round(top_prob * 100, 1)}% confidence) — Recommended Tactic: **{mdp_tactic}**",
            f"- **Recommended Next Command:**",
            f"```bash\n{consensus_cmd}\n```",
        ]
    )
    if llm_error:
        lines.extend(
            [
                "",
                f"*Local LLM server is currently on standby (`llama.cpp: STANDBY`). Click `llama.cpp: STANDBY` in the top header or run `run_cora_WIN.ps1 start` / `./run_cora_NIX.sh start` to enable full neural prose. Press `Ctrl+O` to expand the internal reasoning & thought process trace.*",
            ]
        )
    return "\n".join(lines)


def execute_safe_shell_command(
    command: str,
    mode_info: Dict[str, Any],
    posture: Dict[str, Any],
    project_slug: str,
) -> Dict[str, Any]:
    """
    Execute a shell command only after passing:
      1. Personality Mode check (`Analyst` mode blocks mutating/active network commands)
      2. Network Isolation check (`WHITE` air-gap blocks external non-loopback network targets;
         `BLUE` locks to allowed host interfaces & subnets on Windows and Linux)
      3. Engine 9 CEGAR Pre-Execution Verifier (`verify_command_cegar`)
    """
    cmd_clean = (command or "").strip()
    if not cmd_clean:
        return {"executed": False, "blocked": True, "reason": "Empty command."}

    # Synchronize active session mode & network isolation into process env before CEGAR evaluation
    color_level = str(posture.get("color_level") or "RED").upper()
    iso_env = "white" if color_level == "WHITE" else ("blue" if color_level == "BLUE" else "red")
    allowed_if_list = posture.get("allowed_interfaces") or []
    allowed_if_csv = ",".join(str(x) for x in allowed_if_list if x)
    os.environ["CORA_PERSONALITY_MODE"] = str(mode_info.get("key") or "default").upper()
    os.environ["LLM_ISOLATION_MODE"] = iso_env
    if iso_env == "blue" and allowed_if_csv:
        os.environ["LLM_ALLOWED_IFACES"] = allowed_if_csv
        os.environ["LLM_POSTURE_OVERRIDE"] = f"blue:{allowed_if_csv}"
    else:
        os.environ["LLM_POSTURE_OVERRIDE"] = iso_env

    # 0. Pre-execution catastrophic host wipe guardrail (applies across all modes)
    catastrophic_re = re.compile(
        r"(?:\brm\s+-[a-zA-Z]*[rf][a-zA-Z]*\s+(?:/(?:\s|$)|\*|--no-preserve-root)|"
        r"\bformat\s+[a-zA-Z]:|"
        r"\bmkfs(?:\.[a-z0-9]+)?\s+/dev/|"
        r"\bdd\s+if=/dev/(?:zero|urandom)\s+of=/dev/|"
        r"\brd\s+/s\s+/q\s+[a-zA-Z]:\\|"
        r"\bRemove-Item\b[^\n]*-Recurse[^\n]*[a-zA-Z]:\\(?:\s|$))",
        flags=re.I,
    )
    if catastrophic_re.search(cmd_clean):
        return {
            "executed": False,
            "blocked": True,
            "command": cmd_clean,
            "reason": "Blocked by Engine 9 (CEGAR): Catastrophic root/filesystem wipe command is strictly prohibited.",
            "cegar": {"blocked": True, "reason": "Catastrophic filesystem destruction guardrail"},
        }

    # 1. Check Engine 9 CEGAR Pre-Verifier (includes WHITE/BLUE/Windows interface & subnet checks)
    cegar = verify_command_cegar(cmd_clean)
    if cegar.get("blocked"):
        repaired = cegar.get("repaired_command") or cegar.get("auto_repaired_command")
        same_bin = (
            bool(repaired)
            and not mode_info.get("read_only")
            and cmd_clean.split()[0].lower().removesuffix(".exe")
            == str(repaired).split()[0].lower().removesuffix(".exe")
        )
        if same_bin and not verify_command_cegar(str(repaired)).get("blocked"):
            cmd_clean = str(repaired)
            cegar = verify_command_cegar(cmd_clean)
        else:
            cegar_msg = (
                cegar.get("counterexample_reason")
                or cegar.get("reason")
                or cegar.get("counterexample")
                or "Safety / Network Isolation policy violation."
            )
            if cegar.get("counterexample") and cegar.get("counterexample") not in str(cegar_msg):
                cegar_msg = f"{cegar_msg} ({cegar.get('counterexample')})"
            return {
                "executed": False,
                "blocked": True,
                "command": cmd_clean,
                "reason": f"Blocked by Engine 9 (CEGAR): {cegar_msg}",
                "cegar": cegar,
            }

    # 2. Check Analyst Read-Only Mode
    if mode_info.get("read_only"):
        mutating_re = re.compile(
            r"\b(?:rm|mv|dd|mkfs|chmod|chown|kill|pkill|reboot|shutdown|iptables|nft|ufw|"
            r"nmap|masscan|hydra|sqlmap|msfconsole|del|erase|Remove-Item|Stop-Process|Restart-Computer)\b",
            flags=re.I,
        )
        if mutating_re.search(cmd_clean) or " >" in cmd_clean:
            return {
                "executed": False,
                "blocked": True,
                "command": cmd_clean,
                "reason": "Blocked by Mode [2] Analyst (Strictly Read-Only & White Air-Gap).",
                "cegar": cegar,
            }

    # 3. Check White Air-Gap External IP, SMB/UNC Share & URL restrictions
    if color_level == "WHITE":
        m_unc = re.search(r"\\\\(?!(?:127\.0\.0\.1|localhost|\.)\\)([A-Za-z0-9_.\-]+)\\", cmd_clean, re.I)
        if m_unc:
            return {
                "executed": False,
                "blocked": True,
                "command": cmd_clean,
                "reason": (
                    f"Blocked by WHITE Network Isolation (lo-only air-gap): remote SMB/UNC share "
                    f"'\\\\{m_unc.group(1)}\\' is not permitted in air-gapped mode."
                ),
                "cegar": cegar,
            }
        m_url = re.search(r"https?://(?!(?:127\.\d+\.\d+\.\d+|localhost|\[::1\])\b)([A-Za-z0-9_.\-]+)", cmd_clean, re.I)
        if m_url:
            return {
                "executed": False,
                "blocked": True,
                "command": cmd_clean,
                "reason": (
                    f"Blocked by WHITE Network Isolation (lo-only air-gap): external URL host "
                    f"'{m_url.group(1)}' is not permitted."
                ),
                "cegar": cegar,
            }
        ext_ips = [
            ip
            for ip in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", cmd_clean)
            if not ip.startswith(("127.", "0.", "255."))
        ]
        if ext_ips:
            return {
                "executed": False,
                "blocked": True,
                "command": cmd_clean,
                "reason": f"Blocked by WHITE Network Isolation (lo-only air-gap): external target IP(s) {', '.join(ext_ips)} not permitted.",
                "cegar": cegar,
            }

    proj_dir = ensure_project_structure(project_slug)
    files_dir = proj_dir / "Files"
    files_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PROJECT_DIR"] = str(proj_dir)
    env["PROJECT_FILES_DIR"] = str(files_dir)
    env["CORA_ACTIVE_PROJECT"] = project_slug
    os_tools_dir = CORA_ROOT / "Tools" / ("Windows" if os.name == "nt" else "Linux")
    path_prefixes = [str(files_dir)]
    if os_tools_dir.is_dir():
        path_prefixes.append(str(os_tools_dir))
    env["PATH"] = os.pathsep.join(path_prefixes) + os.pathsep + env.get("PATH", "")

    t0 = time.perf_counter()
    try:
        exec_cmd_str = cmd_clean
        if os.name == "nt" and "tio " not in exec_cmd_str:
            exec_cmd_str = re.sub(r"\barp\s+-accepteula\b", "arp -a", exec_cmd_str, flags=re.I)
            exec_cmd_str = re.sub(r"\bping\s+-c\s+(\d+)\s+-W\s+\d+\b", r"ping -n \1 -w 1200", exec_cmd_str)
            exec_cmd_str = re.sub(r"\bping\s+-c\s+(\d+)\b", r"ping -n \1", exec_cmd_str)
            exec_cmd_str = re.sub(r"\bip\s+neigh\s+show\b", "arp -a", exec_cmd_str)
        elif os.name != "nt":
            exec_cmd_str = re.sub(r"\bping\s+-n\s+(\d+)\b", r"ping -c \1", exec_cmd_str)
        # Automatically add -k to curl https:// invocations if not already present so self-signed appliance certs do not fail with Exit Code 60
        if re.search(r"\bcurl(?:\.exe)?\b", exec_cmd_str, flags=re.I) and "https://" in exec_cmd_str.lower():
            if not re.search(r"(?:^|\s)(?:-k|--insecure)\b", exec_cmd_str):
                exec_cmd_str = re.sub(r"\b(curl(?:\.exe)?)\b", r"\1 -k", exec_cmd_str, count=1, flags=re.I)

        use_ps_wrapper = False
        if os.name == "nt" and not re.match(r"^(?:powershell|pwsh|cmd(?:\.exe)?)\b", exec_cmd_str, flags=re.I):
            if re.search(
                r"\b(?:Select-String|Select-Object|Where-Object|ForEach-Object|Get-[A-Za-z]+|Set-[A-Za-z]+|New-[A-Za-z]+|Remove-[A-Za-z]+|Test-NetConnection|Invoke-WebRequest|Invoke-RestMethod|Out-String|Measure-Object)\b|\$[A-Za-z_]",
                exec_cmd_str,
                flags=re.I,
            ) or (";" in exec_cmd_str and "&" not in exec_cmd_str):
                use_ps_wrapper = True

        if use_ps_wrapper:
            # In PowerShell, 'curl' is aliased to Invoke-WebRequest unless invoked as curl.exe
            ps_cmd = re.sub(r"\bcurl\b(?!\.exe)", "curl.exe", exec_cmd_str)
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                shell=False,
                cwd=str(proj_dir),
                env=env,
                capture_output=True,
                text=True,
                timeout=25.0,
                check=False,
            )
        else:
            run_kwargs: Dict[str, Any] = {
                "shell": True,
                "cwd": str(proj_dir),
                "env": env,
                "capture_output": True,
                "text": True,
                "timeout": 25.0,
                "check": False,
            }
            if os.name != "nt":
                bash_bin = shutil.which("bash")
                if bash_bin:
                    run_kwargs["executable"] = bash_bin
            proc = subprocess.run(exec_cmd_str, **run_kwargs)
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 1)
        combined_out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
        sygus_facts = extract_structured_facts(cmd_clean, combined_out)
        cbr_match = None
        if not mode_info.get("read_only"):
            try:
                if proc.returncode != 0:
                    cbr_match = match_failure_fingerprint(cmd_clean, proc.returncode, combined_out)
                    if cbr_match and cbr_match.get("verified_fix"):
                        combined_out = (
                            combined_out.rstrip()
                            + f"\n[CBR Engine 11 Verified Fix ({cbr_match.get('case_id')})]: {cbr_match.get('verified_fix')}"
                        )
                record_command_event(cmd_clean, combined_out, proc.returncode)
                record_live_command_experience(cmd_clean, proc.returncode, combined_out)
                facts_cnt = (
                    len(sygus_facts.get("arp_neighbors", []))
                    + len(sygus_facts.get("open_ports", []))
                    + len(sygus_facts.get("routes", []))
                    + (1 if sygus_facts.get("summary_header") else 0)
                )
                record_rl_step_transition(
                    command=cmd_clean,
                    exit_code=proc.returncode,
                    new_facts_count=facts_cnt,
                )
            except Exception:
                pass
        return {
            "executed": True,
            "blocked": False,
            "command": cmd_clean,
            "exit_code": proc.returncode,
            "output": combined_out.strip()[:12000],
            "latency_ms": elapsed_ms,
            "sygus_facts": sygus_facts,
            "cbr_match": cbr_match,
            "cegar": cegar,
        }
    except subprocess.TimeoutExpired:
        return {
            "executed": False,
            "blocked": True,
            "command": cmd_clean,
            "reason": "Command timed out after 25.0s.",
            "cegar": cegar,
        }
    except Exception as exc:
        return {
            "executed": False,
            "blocked": True,
            "command": cmd_clean,
            "reason": f"Execution error: {exc}",
            "cegar": cegar,
        }


# ---------------------------------------------------------------------------
# FastAPI Application & Pydantic Request Models
# ---------------------------------------------------------------------------
app = FastAPI(
    title="C.O.R.A. Custom Web Interface & Neuro-Symbolic Dashboard API",
    version="5.15.12",
    description=(
        "Local Python + FastAPI backend connecting the Svelte + TypeScript + Tailwind CSS dashboard "
        "to CORA Projects, 15-Engine Neuro-Symbolic Reasoning, psutil + NVIDIA NVML telemetry, "
        "SQLite persistence, and local inference APIs (llama-server & Ollama)."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SessionConfigUpdateRequest(BaseModel):
    active_project: Optional[str] = None
    session_mode: Optional[str] = None
    isolation_level: Optional[str] = None
    allowed_interfaces: Optional[str] = None
    selected_model: Optional[str] = None
    inference_provider: Optional[str] = None
    llama_api_url: Optional[str] = None
    ollama_api_url: Optional[str] = None
    thinking_enabled: Optional[bool] = None
    permission_mode: Optional[str] = None
    active_goal: Optional[str] = None
    theme_mode: Optional[str] = None
    ui_font_family: Optional[str] = None
    ui_font_size: Optional[int] = None
    ui_font_color: Optional[str] = None
    ui_line_height: Optional[str] = None
    ui_panel_density: Optional[str] = None
    ui_glow_intensity: Optional[str] = None


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    goal: Optional[str] = ""


class ProjectRenameRequest(BaseModel):
    old_slug: str
    new_name: str


class ProjectSelectRequest(BaseModel):
    slug: str


class FileSaveRequest(BaseModel):
    rel_path: str
    content: str


class UploadedFileItem(BaseModel):
    filename: str
    content_base64: Optional[str] = None
    content_text: Optional[str] = None


class ProjectFileUploadRequest(BaseModel):
    project_slug: Optional[str] = None
    files: Optional[List[UploadedFileItem]] = None
    local_path: Optional[str] = None


class ProjectFileDeleteRequest(BaseModel):
    project_slug: Optional[str] = None
    rel_path: str


class QuerySubmitRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    project_slug: Optional[str] = None
    session_mode: Optional[str] = None
    isolation_level: Optional[str] = None
    allowed_interfaces: Optional[str] = None
    selected_model: Optional[str] = None
    thinking_enabled: Optional[bool] = None
    permission_mode: Optional[str] = None
    run_reasoning: bool = True
    execute_command: Optional[str] = None
    attached_files: Optional[List[str]] = None


class CommandExecuteRequest(BaseModel):
    command: str
    project_slug: Optional[str] = None


class ReportGenerateRequest(BaseModel):
    project_slug: Optional[str] = None
    focus: Optional[str] = ""
    use_llm: bool = False


class ToolSyncRequest(BaseModel):
    tool_ids: Optional[List[str]] = None


class ModelStartRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: Optional[str] = None
    force_restart: bool = False


@app.on_event("startup")
async def _on_startup() -> None:
    init_sqlite_db()
    cfg = get_all_settings()
    _sync_cli_session_files(cfg)
    if (
        (cfg.get("inference_provider") or "llama-server") == "llama-server"
        and os.environ.get("CORA_SKIP_AUTO_LLAMA") != "1"
    ):
        target_model = cfg.get("selected_model") or "3.8"
        threading.Thread(
            target=ensure_llama_server_running,
            kwargs={"model_id": target_model, "cfg": cfg, "wait_ready_sec": 90.0},
            daemon=True,
        ).start()


# ---------------------------------------------------------------------------
# Brand Assets & Static Frontend Serving
# ---------------------------------------------------------------------------
@app.get("/api/assets/logo")
async def get_crow_logo(theme: str = Query("dark")) -> FileResponse:
    """
    Serve the CROW Emblem for the active theme:
      - Dark Mode (`theme=dark`): White Crow Emblem (`CROW_Logo_White_TransparentBackground.png`)
      - Light Mode (`theme=light`): Dark/Glow Crow Emblem (`CROW_Logo-NoWords_Transparent_Glow-NoBackground.png`)
    """
    white_logo = ASSETS_DIR / "CROW_Logo_White_TransparentBackground.png"
    glow_logo = ASSETS_DIR / "CROW_Logo-NoWords_Transparent_Glow-NoBackground.png"
    if (theme or "dark").strip().lower() == "dark" and white_logo.is_file():
        logo_path = white_logo
    else:
        logo_path = glow_logo if glow_logo.is_file() else white_logo
    if not logo_path.is_file():
        raise HTTPException(status_code=404, detail="CROW logo asset not found.")
    return FileResponse(str(logo_path), media_type="image/png")


@app.get("/api/assets/logo-dark")
async def get_crow_logo_dark() -> FileResponse:
    return await get_crow_logo(theme="dark")


@app.get("/api/assets/logo-light")
async def get_crow_logo_light() -> FileResponse:
    return await get_crow_logo(theme="light")


@app.get("/api/assets/splash")
async def get_cora_splash() -> FileResponse:
    splash_path = ASSETS_DIR / "cora_splash_and_versioning_guide.svg"
    if not splash_path.is_file():
        raise HTTPException(status_code=404, detail="CORA splash SVG not found.")
    return FileResponse(str(splash_path), media_type="image/svg+xml")


@app.get("/api/health")
async def get_webui_health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "cora-webui",
        "version": get_cora_version().get("version", "5.15.12"),
    }


# ---------------------------------------------------------------------------
# Dashboard Bootstrap & Session Configuration Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/bootstrap")
async def get_dashboard_bootstrap() -> Dict[str, Any]:
    """
    Single fast call returning everything the Svelte dashboard needs on load:
    version, active settings, projects list, session modes, network isolation posture,
    installed/online models, hardware snapshot, 15-Engine status, and recent conversation messages.
    """
    cfg = get_all_settings()
    active_proj = resolve_active_project_slug(cfg=cfg)
    if active_proj and cfg.get("active_project") != active_proj:
        cfg = update_settings_dict({"active_project": active_proj})
    proj_dir = ensure_project_structure(active_proj) if active_proj else (LOG_DIR / "_unassigned_workspace")

    mode_key = cfg.get("session_mode", "default").lower()
    if mode_key not in SESSION_MODES:
        mode_key = "default"
    mode_info = SESSION_MODES[mode_key]

    iso_level = cfg.get("isolation_level", "red").lower()
    if mode_info["forced_isolation"]:
        iso_level = mode_info["forced_isolation"]
    ifaces = cfg.get("allowed_interfaces", "eth0,eth1")
    override_str = f"blue:{ifaces}" if iso_level == "blue" else iso_level
    posture = _get_cached_posture(override_str)

    projects = list_all_projects()
    files_info = list_project_files(active_proj)
    models_info = discover_models_and_backends(cfg)
    if (
        (cfg.get("inference_provider") or "llama-server") == "llama-server"
        and (models_info.get("llama_server") or {}).get("state") == "offline"
        and os.environ.get("CORA_SKIP_AUTO_LLAMA") != "1"
    ):
        target_model = cfg.get("selected_model") or "3.5"
        threading.Thread(
            target=ensure_llama_server_running,
            kwargs={"model_id": target_model, "cfg": cfg, "wait_ready_sec": 90.0},
            daemon=True,
        ).start()
        if isinstance(models_info.get("llama_server"), dict):
            models_info["llama_server"]["state"] = "loading"
    hw_metrics = collect_hardware_metrics()
    engine_status = _get_cached_engine_status()
    system_tools = get_system_tools_inventory()
    host_interfaces = get_host_interfaces_catalog()

    with get_db_conn() as conn:
        msg_rows = conn.execute(
            "SELECT * FROM messages WHERE project_slug = ? ORDER BY id DESC LIMIT 40",
            (active_proj,),
        ).fetchall()
    messages = [
        {
            **dict(r),
            "reasoning": json.loads(r["reasoning_json"] or "{}"),
        }
        for r in reversed(msg_rows)
    ]

    return {
        "version": get_cora_version(),
        "cli_banner": get_cli_banner_and_licensing_info(),
        "settings": {
            **cfg,
            "active_project": active_proj,
            "session_mode": mode_key,
            "isolation_level": iso_level,
            "theme_mode": cfg.get("theme_mode", "dark"),
            "active_goal": get_project_last_goal(proj_dir) or cfg.get("active_goal", ""),
        },
        "session_modes": list(SESSION_MODES.values()),
        "active_mode": mode_info,
        "posture": posture,
        "posture_themes": POSTURE_THEMES,
        "host_interfaces": host_interfaces,
        "projects": projects,
        "files": files_info,
        "models": models_info,
        "hardware": hw_metrics,
        "reasoning_status": engine_status,
        "system_tools": system_tools,
        "messages": messages,
    }


@app.post("/api/session/config")
async def update_session_configuration(req: SessionConfigUpdateRequest) -> Dict[str, Any]:
    current = get_all_settings()
    updates: Dict[str, Any] = {}

    if req.active_project is not None:
        proj_slug = slugify(req.active_project)
        ensure_project_structure(proj_slug)
        updates["active_project"] = proj_slug

    mode_key = (req.session_mode or current.get("session_mode") or "default").lower()
    if mode_key not in SESSION_MODES:
        raise HTTPException(status_code=400, detail=f"Unknown session_mode: {mode_key}")
    mode_info = SESSION_MODES[mode_key]
    updates["session_mode"] = mode_key

    iso_level = (req.isolation_level or current.get("isolation_level") or "red").lower()
    if mode_info["forced_isolation"]:
        # Analyst mode automatically locks Network Isolation to WHITE (air-gapped loopback)
        iso_level = mode_info["forced_isolation"]
    elif iso_level not in mode_info["allowed_isolation"]:
        # Berserker & Ninja require RED or BLUE network isolation
        iso_level = mode_info["allowed_isolation"][0]
    updates["isolation_level"] = iso_level

    if req.allowed_interfaces is not None:
        parsed_ifaces = _parse_iface_list(req.allowed_interfaces)
        clean_ifaces = ",".join(parsed_ifaces)
        updates["allowed_interfaces"] = clean_ifaces or str(current.get("allowed_interfaces") or "eth0,eth1")

    if req.selected_model is not None:
        updates["selected_model"] = req.selected_model.strip()
        if req.selected_model.startswith("ollama:"):
            updates["inference_provider"] = "ollama"
        elif req.inference_provider is None:
            updates["inference_provider"] = "llama-server"

    if req.inference_provider is not None:
        updates["inference_provider"] = req.inference_provider.strip().lower()
    if req.llama_api_url is not None:
        updates["llama_api_url"] = req.llama_api_url.strip()
    if req.ollama_api_url is not None:
        updates["ollama_api_url"] = req.ollama_api_url.strip()
    if req.thinking_enabled is not None:
        updates["thinking_enabled"] = "true" if req.thinking_enabled else "false"
    if req.permission_mode is not None:
        updates["permission_mode"] = "auto" if req.permission_mode.lower() == "auto" else "confirm"
    if req.theme_mode is not None:
        updates["theme_mode"] = "light" if req.theme_mode.strip().lower() == "light" else "dark"
    if req.ui_font_family is not None:
        updates["ui_font_family"] = req.ui_font_family.strip()
    if req.ui_font_size is not None:
        updates["ui_font_size"] = str(max(10, min(24, int(req.ui_font_size))))
    if req.ui_font_color is not None:
        updates["ui_font_color"] = req.ui_font_color.strip()
    if req.ui_line_height is not None:
        updates["ui_line_height"] = req.ui_line_height.strip()
    if req.ui_panel_density is not None:
        updates["ui_panel_density"] = req.ui_panel_density.strip()
    if req.ui_glow_intensity is not None:
        updates["ui_glow_intensity"] = req.ui_glow_intensity.strip()

    active_proj = resolve_active_project_slug(updates.get("active_project"), cfg=current)
    proj_dir = ensure_project_structure(active_proj) if active_proj else (LOG_DIR / "_unassigned_workspace")
    if req.active_goal is not None:
        goal_str = req.active_goal.strip()
        updates["active_goal"] = goal_str
        if active_proj:
            current_last = get_project_last_goal(proj_dir)
            if goal_str and goal_str != current_last:
                append_project_goal(proj_dir, goal_str)
    elif req.active_project is not None and active_proj != resolve_active_project_slug(cfg=current):
        updates["active_goal"] = get_project_last_goal(proj_dir) if active_proj else ""

    cfg = update_settings_dict(updates)
    ifaces = cfg.get("allowed_interfaces", "eth0,eth1")
    override_str = f"blue:{ifaces}" if iso_level == "blue" else iso_level
    posture = _get_cached_posture(override_str, ttl=1.5)
    _log_posture_event("WEBUI_APPLY", posture)

    model_changed = req.selected_model is not None and req.selected_model.strip() != current.get("selected_model")
    if (
        (cfg.get("inference_provider") or "llama-server") == "llama-server"
        and os.environ.get("CORA_SKIP_AUTO_LLAMA") != "1"
    ):
        llama_health = _get_llama_health(cfg.get("llama_api_url") or "http://127.0.0.1:8080/v1")
        if model_changed or llama_health["state"] == "offline":
            threading.Thread(
                target=ensure_llama_server_running,
                kwargs={
                    "model_id": cfg.get("selected_model") or "3.8",
                    "cfg": cfg,
                    "wait_ready_sec": 90.0,
                },
                daemon=True,
            ).start()

    models_info = discover_models_and_backends(cfg)
    resolved_goal = (
        updates["active_goal"]
        if req.active_goal is not None
        else (get_project_last_goal(proj_dir) or cfg.get("active_goal", ""))
    )
    return {
        "ok": True,
        "settings": {
            **cfg,
            "active_goal": resolved_goal,
        },
        "active_mode": mode_info,
        "posture": posture,
        "llama_server": models_info.get("llama_server"),
    }


# ---------------------------------------------------------------------------
# Projects & File / Script Explorer Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/projects")
async def api_list_projects() -> Dict[str, Any]:
    cfg = get_all_settings()
    return {
        "active_project": resolve_active_project_slug(cfg=cfg),
        "projects": list_all_projects(),
    }


@app.post("/api/projects/select")
async def api_select_project(req: ProjectSelectRequest) -> Dict[str, Any]:
    raw_slug = (req.slug or "").strip()
    if not raw_slug or raw_slug.lower() in _INVALID_PROJECT_NAMES:
        raise HTTPException(status_code=400, detail="Please select a valid project name.")
    slug = slugify(raw_slug)
    if not slug or slug.lower() in _INVALID_PROJECT_NAMES:
        raise HTTPException(status_code=400, detail="Please select a valid project name.")
    proj_dir = ensure_project_structure(slug)
    proj_goal = get_project_last_goal(proj_dir)
    cfg = update_settings_dict({"active_project": slug, "active_goal": proj_goal})
    with get_db_conn() as conn:
        msg_rows = conn.execute(
            "SELECT * FROM messages WHERE project_slug = ? ORDER BY id DESC LIMIT 40",
            (slug,),
        ).fetchall()
    messages = [
        {**dict(r), "reasoning": json.loads(r["reasoning_json"] or "{}")}
        for r in reversed(msg_rows)
    ]
    return {
        "ok": True,
        "active_project": slug,
        "active_goal": proj_goal,
        "projects": list_all_projects(),
        "files": list_project_files(slug),
        "messages": messages,
        "settings": cfg,
    }


@app.post("/api/projects/create")
async def api_create_project(req: ProjectCreateRequest) -> Dict[str, Any]:
    raw_name = (req.name or "").strip()
    if not raw_name or raw_name.lower() in _INVALID_PROJECT_NAMES:
        raise HTTPException(status_code=400, detail="Invalid project name. Please choose a specific project name.")
    slug = slugify(raw_name)
    if not slug or slug.lower() in _INVALID_PROJECT_NAMES:
        raise HTTPException(status_code=400, detail="Invalid project name. Please choose a specific project name.")
    proj_dir = ensure_project_structure(slug)
    if req.goal and req.goal.strip():
        append_project_goal(proj_dir, req.goal.strip())
    cfg = update_settings_dict({"active_project": slug, "active_goal": (req.goal or "").strip()})
    return {
        "ok": True,
        "created_slug": slug,
        "active_project": slug,
        "active_goal": get_project_last_goal(proj_dir),
        "projects": list_all_projects(),
        "files": list_project_files(slug),
        "settings": cfg,
    }


@app.post("/api/projects/rename")
async def api_rename_project(req: ProjectRenameRequest) -> Dict[str, Any]:
    raw_old = (req.old_slug or "").strip()
    raw_new = (req.new_name or "").strip()
    if not raw_old or not raw_new or raw_new.lower() in _INVALID_PROJECT_NAMES:
        raise HTTPException(status_code=400, detail="Invalid project name.")
    old_slug = slugify(raw_old)
    new_slug = slugify(raw_new)
    if not new_slug or new_slug.lower() in _INVALID_PROJECT_NAMES:
        raise HTTPException(status_code=400, detail="Invalid project name.")
    old_dir = Path(PROJECTS_DIR) / old_slug
    new_dir = Path(PROJECTS_DIR) / new_slug
    if not old_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"Project '{old_slug}' does not exist.")
    if new_dir.exists() and old_slug != new_slug:
        raise HTTPException(status_code=409, detail=f"Project '{new_slug}' already exists.")

    if old_slug != new_slug:
        shutil.move(str(old_dir), str(new_dir))
        # Update wiki-links inside markdown files in the renamed project
        for md_f in new_dir.rglob("*.md"):
            try:
                txt = md_f.read_text(encoding="utf-8", errors="replace")
                updated = txt.replace(f"Projects/{old_slug}", f"Projects/{new_slug}").replace(
                    f"project: \"{old_slug}\"", f"project: \"{new_slug}\""
                )
                if updated != txt:
                    _atomic_write_text(md_f, updated)
            except Exception:
                pass
        with get_db_conn() as conn:
            conn.execute("UPDATE messages SET project_slug = ? WHERE project_slug = ?", (new_slug, old_slug))
            conn.execute("UPDATE conversations SET project_slug = ? WHERE project_slug = ?", (new_slug, old_slug))
            conn.commit()

    cfg = update_settings_dict({"active_project": new_slug})
    return {
        "ok": True,
        "old_slug": old_slug,
        "new_slug": new_slug,
        "active_project": new_slug,
        "projects": list_all_projects(),
        "files": list_project_files(new_slug),
        "settings": cfg,
    }


@app.get("/api/files/content")
async def api_read_file_content(rel_path: str = Query(...)) -> Dict[str, Any]:
    target = _resolve_safe_workspace_file(rel_path)
    if not target.is_file():
        raise HTTPException(status_code=404, detail=f"File not found: {rel_path}")
    content = target.read_text(encoding="utf-8", errors="replace")
    return {
        "rel_path": rel_path,
        "name": target.name,
        "ext": target.suffix.lower(),
        "size_bytes": target.stat().st_size,
        "modified_at": dt.datetime.fromtimestamp(target.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "content": content[:150000],
    }


@app.post("/api/files/save")
async def api_save_file_content(req: FileSaveRequest) -> Dict[str, Any]:
    cfg = get_all_settings()
    if cfg.get("session_mode") == "analyst":
        raise HTTPException(status_code=403, detail="File modification is disabled in [2] Analyst (Read-Only) mode.")
    target = _resolve_safe_workspace_file(req.rel_path)
    # Only allow writing inside Projects/ or ObsidianVault/
    rel_norm = target.relative_to(CORA_ROOT.resolve()).as_posix()
    if not (rel_norm.startswith("Projects/") or rel_norm.startswith("core/ObsidianVault/")):
        raise HTTPException(
            status_code=403,
            detail="Only files inside `Projects/<project>/` or `core/ObsidianVault/` can be edited from the WebUI.",
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(target, req.content)
    return {
        "ok": True,
        "rel_path": rel_norm,
        "size_bytes": target.stat().st_size,
        "modified_at": dt.datetime.fromtimestamp(target.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.get("/api/projects/files")
async def api_get_project_files(project_slug: Optional[str] = Query(None)) -> Dict[str, Any]:
    cfg = get_all_settings()
    slug = resolve_active_project_slug(project_slug, cfg=cfg)
    if not slug:
        return {
            "project_slug": "",
            "files_dir": "",
            "files_dir_rel": "",
            "files_dir_items": [],
            "project_files": [],
            "system_scripts": [],
        }
    return list_project_files(slug)


@app.post("/api/projects/files/upload")
async def api_upload_project_files(req: ProjectFileUploadRequest) -> Dict[str, Any]:
    """
    Upload or add one or more files into `Projects/<project_slug>/Files/` so the LLM can directly
    inspect, read, edit, or execute them.
    Supports:
      1. `files`: list of `{ filename, content_base64, content_text }` from browser File Picker or Drag-and-Drop.
      2. `local_path`: local host file or directory path to copy into `Projects/<project_slug>/Files/`.
    """
    cfg = get_all_settings()
    slug = resolve_active_project_slug(req.project_slug, cfg=cfg)
    if not slug:
        raise HTTPException(
            status_code=400,
            detail="Please select an existing project or create a new project before uploading files.",
        )
    proj_dir = ensure_project_structure(slug)
    files_dir = (proj_dir / "Files").resolve()
    files_dir.mkdir(parents=True, exist_ok=True)

    uploaded_items: List[Dict[str, Any]] = []

    # 1. Handle browser-uploaded files (base64 or text)
    for item in req.files or []:
        raw_name = (item.filename or "").strip().replace("\\", "/").lstrip("/")
        # Allow relative paths under Files/ if nested, but block any .. traversal
        if raw_name.lower().startswith("files/"):
            raw_name = raw_name[6:]
        parts = [p for p in raw_name.split("/") if p and p not in (".", "..")]
        safe_rel = "/".join(parts) if parts else ""
        if not safe_rel:
            continue
        dest = (files_dir / safe_rel).resolve()
        if not str(dest).startswith(str(files_dir)):
            raise HTTPException(status_code=400, detail=f"Invalid file destination: {item.filename}")
        dest.parent.mkdir(parents=True, exist_ok=True)

        if item.content_base64 is not None:
            b64_str = item.content_base64.strip()
            if "," in b64_str and b64_str.lower().startswith("data:"):
                b64_str = b64_str.split(",", 1)[1]
            try:
                raw_bytes = base64.b64decode(b64_str)
            except Exception as exc:
                raise HTTPException(status_code=400, detail=f"Invalid base64 payload for {safe_rel}: {exc}")
            dest.write_bytes(raw_bytes)
        elif item.content_text is not None:
            _atomic_write_text(dest, item.content_text)
        else:
            dest.write_bytes(b"")

        # If script on Linux/macOS, ensure executable bit if it starts with shebang or is .sh/.py
        if os.name != "nt" and dest.suffix.lower() in (".sh", ".py", ".pl", ".rb"):
            try:
                dest.chmod(dest.stat().st_mode | 0o755)
            except Exception:
                pass

        rel_in_files = dest.relative_to(files_dir).as_posix()
        _record_project_file_in_memory(proj_dir, rel_in_files, "Uploaded via WebGUI Console into Files/")
        uploaded_items.append(
            {
                "name": dest.name,
                "rel_path": f"Projects/{slug}/Files/{rel_in_files}",
                "project_rel": f"Files/{rel_in_files}",
                "size_bytes": dest.stat().st_size,
                "modified_at": dt.datetime.fromtimestamp(dest.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    # 2. Handle local host path import (`local_path`)
    if req.local_path and req.local_path.strip():
        src_str = os.path.expandvars(os.path.expanduser(req.local_path.strip().strip('"').strip("'")))
        src_path = Path(src_str)
        if not src_path.is_absolute():
            src_path = (CORA_ROOT / src_path).resolve()
        else:
            src_path = src_path.resolve()

        if not src_path.exists():
            raise HTTPException(status_code=404, detail=f"Local path not found on host: {src_path}")

        if src_path.is_file():
            dest = (files_dir / src_path.name).resolve()
            if src_path != dest:
                shutil.copy2(src_path, dest)
            rel_in_files = dest.relative_to(files_dir).as_posix()
            _record_project_file_in_memory(proj_dir, rel_in_files, f"Imported from `{src_path}` into Files/")
            uploaded_items.append(
                {
                    "name": dest.name,
                    "rel_path": f"Projects/{slug}/Files/{rel_in_files}",
                    "project_rel": f"Files/{rel_in_files}",
                    "size_bytes": dest.stat().st_size,
                    "modified_at": dt.datetime.fromtimestamp(dest.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        elif src_path.is_dir():
            sub_dest_root = (files_dir / src_path.name).resolve()
            sub_dest_root.mkdir(parents=True, exist_ok=True)
            copied_cnt = 0
            for f in sorted(src_path.rglob("*")):
                if not f.is_file() or copied_cnt >= 100:
                    continue
                rel_sub = f.relative_to(src_path)
                dest = (sub_dest_root / rel_sub).resolve()
                dest.parent.mkdir(parents=True, exist_ok=True)
                if f.resolve() != dest:
                    shutil.copy2(f, dest)
                rel_in_files = dest.relative_to(files_dir).as_posix()
                uploaded_items.append(
                    {
                        "name": dest.name,
                        "rel_path": f"Projects/{slug}/Files/{rel_in_files}",
                        "project_rel": f"Files/{rel_in_files}",
                        "size_bytes": dest.stat().st_size,
                        "modified_at": dt.datetime.fromtimestamp(dest.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
                copied_cnt += 1
            _record_project_file_in_memory(proj_dir, f"{src_path.name}/", f"Imported directory ({copied_cnt} files) into Files/")

    if not uploaded_items:
        raise HTTPException(status_code=400, detail="No valid files or local_path provided to upload.")

    return {
        "ok": True,
        "project_slug": slug,
        "files_dir": str(files_dir),
        "files_dir_rel": f"Projects/{slug}/Files",
        "uploaded": uploaded_items,
        "projects": list_all_projects(),
        "files": list_project_files(slug),
    }


@app.post("/api/projects/files/delete")
async def api_delete_project_file(req: ProjectFileDeleteRequest) -> Dict[str, Any]:
    cfg = get_all_settings()
    if cfg.get("session_mode") == "analyst":
        raise HTTPException(status_code=403, detail="Deleting files is disabled in [2] Analyst (Read-Only) mode.")
    slug = resolve_active_project_slug(req.project_slug, cfg=cfg)
    if not slug:
        raise HTTPException(status_code=400, detail="Please select an existing project first.")
    proj_dir = ensure_project_structure(slug)
    files_dir = (proj_dir / "Files").resolve()

    raw_rel = (req.rel_path or "").strip().replace("\\", "/").lstrip("/")
    if raw_rel.lower().startswith(f"projects/{slug.lower()}/files/"):
        sub_rel = raw_rel[len(f"projects/{slug.lower()}/files/"):]
    elif raw_rel.lower().startswith("files/"):
        sub_rel = raw_rel[6:]
    else:
        sub_rel = raw_rel

    target = (files_dir / sub_rel).resolve()
    if not str(target).startswith(str(files_dir)) or target == files_dir:
        raise HTTPException(
            status_code=403,
            detail="Only files inside `Projects/<project>/Files/` can be deleted with this action.",
        )
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"File not found in Projects/{slug}/Files/: {sub_rel}")
    if target.is_file():
        target.unlink()
    elif target.is_dir():
        shutil.rmtree(target)

    return {
        "ok": True,
        "project_slug": slug,
        "deleted": f"Projects/{slug}/Files/{sub_rel}",
        "projects": list_all_projects(),
        "files": list_project_files(slug),
    }


# ---------------------------------------------------------------------------
# Hardware, Models & Reasoning Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/hardware")
async def api_get_hardware() -> Dict[str, Any]:
    return await asyncio.to_thread(collect_hardware_metrics)


@app.get("/api/models")
async def api_get_models() -> Dict[str, Any]:
    cfg = get_all_settings()
    return await asyncio.to_thread(discover_models_and_backends, cfg)


@app.post("/api/models/start")
async def api_start_model(req: ModelStartRequest) -> Dict[str, Any]:
    cfg = get_all_settings()
    target_model = (req.model_id or cfg.get("selected_model") or "3.8").strip()
    if req.model_id:
        cfg = update_settings_dict({"selected_model": target_model, "inference_provider": "llama-server"})
    res = await asyncio.to_thread(
        ensure_llama_server_running,
        model_id=target_model,
        cfg=cfg,
        wait_ready_sec=90.0,
        force_restart=req.force_restart,
    )
    models_info = discover_models_and_backends(cfg)
    return {
        "ok": bool(res.get("online")),
        "result": res,
        "models": models_info,
    }


WEBUI_SWITCH_HELP_MAP: Dict[str, str] = {
    "mode": (
        "=== Switch Help: /mode ===\n"
        "  Select or inspect the C.O.R.A. Session Personality & Logic Enforcement Mode (Unique per session):\n"
        "    [1] Default   (Default) : Standard operation with no behavioral guidance or extra restrictions.\n"
        "    [2] Analyst             : Analyze local system data only; external network scanning blocked. (locks Network Isolation WHITE)\n"
        "    [3] Berserker           : Aggressively pursue target goals using all available tools. (Red=All or Blue=Allowed NICs)\n"
        "    [4] Ninja               : Find answers covertly using stealthy, low-noise commands only. (Red=All or Blue=Allowed NICs)\n"
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
        "    -m 3.5       | -m:3.5       | --model 3.5       : Qwen3.5-9B-Uncensored-Q4_K_M (~6.5 GB VRAM, fast)\n"
        "    -m turbo-q4  | -m:turbo-q4  | --model turbo-q4  : Qwen3.8-27B-Turbo-Uncensored-Q4_K_M (4-step distilled)\n"
        "    -m turbo-q8  | -m:turbo-q8  | --model turbo-q8  : Qwen3.8-27B-Turbo-Uncensored-Q8_0 (4-step distilled)\n"
        "    -m -h        | -m --help    | --model --help    : Show this help message"
    ),
    "netiso": (
        "=== Switch Help: -netiso / --network-isolation / /netiso / /posture ===\n"
        "  Configure C.O.R.A. Network Isolation & Security Posture (Red / White / Blue):\n"
        "    -netiso red              | /netiso -mode:red         : RED (UNRESTRICTED) — Full host network stack access\n"
        "    -netiso white            | /netiso -mode:white       : WHITE (AIR_GAPPED_NETNS) — Loopback 127.0.0.1 / lo only\n"
        "    -netiso blue             | /netiso -mode:blue        : BLUE (ISOLATED_LAN_USB) — Lock to interfaces in Network_Isolation/network_isolation.conf\n"
        "    -netiso -blue:eth0,eth1  | /netiso -blue:eth0,eth1   : BLUE (ISOLATED_LAN_USB) — Lock strictly to specified interfaces\n"
        "    /netiso status           | /posture -mode:status     : Display current active network isolation posture and allowed interfaces\n"
        "    -netiso -h | -netiso --help | /netiso -h | /netiso --help : Show this help message"
    ),
    "continue": (
        "=== Switch Help: -c / --continue / /continue ===\n"
        "  Restore and continue from the last saved C.O.R.A. session (last_cli_session.json + relentless_ledger.json):\n"
        "    /continue | /resume                     : Restore the previous session state\n"
        "    -c -h | -c --help | /continue -h | /continue --help : Show this help message"
    ),
    "project": (
        "=== Switch Help: -P / --project / /project ===\n"
        "  Manage isolated project workspaces inside CORA/Projects/<project-name>/:\n"
        "    /project list | /project -mode:list    : List all current projects in Projects/\n"
        "    /project -new:<name>                   : Create a new project in Projects/<name>/ (with Files/) and set it active\n"
        "    /project -rename:<old>:<new>           : Rename Projects/<old>/ -> Projects/<new>/\n"
        "    /project -load:<name> [\"<task>\"]       : Switch active project to Projects/<name>/\n"
        "    -P -h | --project --help | /project -h | /project --help : Show this help message"
    ),
    "files": (
        "=== Switch Help: /files / /file / /upload / /add ===\n"
        "  Manage and inspect the active project's local `Files` directory (Projects/<project>/Files/) for LLM interaction:\n"
        "    /files | /files list                   : List all custom scripts and files inside Projects/<project>/Files/\n"
        "    /files add <path> | /upload <path>     : Copy a local file or directory into Projects/<project>/Files/\n"
        "    /files read <filename>                 : Display the contents of Projects/<project>/Files/<filename>\n"
        "    /files rm <filename>                   : Delete a file inside Projects/<project>/Files/\n"
        "    /files -h | /files --help              : Show this help message"
    ),
    "goal": (
        "=== Switch Help: /goal ===\n"
        "  Set, inspect, or clear project-scoped mission objectives (Projects/<project>/goals.md):\n"
        "  (Goal text MUST be enclosed in quotation marks \"...\"; parameters MUST begin with a dash -)\n"
        "    /goal \"<objective text>\" [-max:<#>] : Append \"<objective text>\" to Projects/<project>/goals.md, lock active goal, and execute\n"
        "                                          (optional -max:<#> sets wave limit; use -max:0 or -max:unlimited to never stop)\n"
        "    /goal | /goal status | -mode:status : Display the very last goal saved in Projects/<project>/goals.md\n"
        "    /goal list | /goal -mode:list       : List all historical goals appended in Projects/<project>/goals.md\n"
        "    /goal audit | /goal -mode:audit     : Display full Relentless Attempt Ledger & capability vector audit\n"
        "    /goal clear | /goal -mode:clear     : Clear the active in-memory goal and reset the session Attempt Ledger\n"
        "    /goal -h | /goal --help             : Show this help message"
    ),
    "relentless": (
        "=== Switch Help: /relentless ===\n"
        "  Control the Autonomous Multi-Wave /relentless Execution Controller:\n"
        "  (When setting a goal, the goal MUST be enclosed in quotation marks \"...\"; parameters MUST begin with -)\n"
        "    /relentless                             : Enable Relentless Mode and start looping on the active /goal until achieved\n"
        "    /relentless \"<goal text>\" [-max:<#>]    : Set \"<goal text>\" as the active goal and immediately start autonomous waves\n"
        "                                              Example: /relentless \"You must try to the max and never stop\" -max:100\n"
        "    /relentless -max:<#>                    : Set maximum autonomous waves per run (e.g. -max:15, -max:100)\n"
        "    /relentless -max:0                      : Set UNLIMITED waves (0 / -max:unlimited) — never stop until goal is achieved\n"
        "    /relentless on  | -mode:on              : Arm persistent Relentless Mode\n"
        "    /relentless off | -mode:off             : Disable Relentless Mode and return to single-turn execution\n"
        "    /relentless status | -mode:status       : Show concise 3-line Relentless Mode status (Mode, Max Waves Cap, Active Goal)\n"
        "    /relentless audit  | -mode:audit        : Display full Relentless Controller Audit and Attempt Ledger\n"
        "    /relentless -h | /relentless --help     : Show this help message"
    ),
    "generate-report": (
        "=== Switch Help: /generate-report / /report ===\n"
        "  Generate a 5-Section Project Status & Findings Report (Projects/<project>/REPORT.md + assets/report_dashboard.svg):\n"
        "    /generate-report                          : Generate report for the active project (with LLM prose polish)\n"
        "    /generate-report -project:<name>          : Generate report for a specific project in Projects/<name>/\n"
        "    /generate-report -focus:<topic>           : Highlight a specific objective or finding in the report\n"
        "    /generate-report -mode:fast | --fast      : Instant deterministic report generation without waiting for LLM call\n"
        "    /generate-report -h | /generate-report --help | /report -h | /report --help : Show this help message"
    ),
    "rl": (
        "=== Switch Help: /rl ===\n"
        "  Control Engine 14/19 (Trajectory RL, Factored Network World-Model & Live Local Network Topology):\n"
        "    /rl | /rl status | -mode:status   : Predict optimal 3-step Pessimistic Q_LCB trajectory for the current goal\n"
        "    /rl <problem>                     : Compute 3-step RL rollout for <problem>\n"
        "    /rl topology | /rl -mode:topology : Sense live local NICs, gateways, ARP neighbors, and serial ports\n"
        "    /rl -train:<#> | /rl train        : Run offline simulated world-model Q-learning episodes (default: 400)\n"
        "    /rl -h | /rl --help               : Show this help message"
    ),
    "pca": (
        "=== Switch Help: /pca / /kmeans ===\n"
        "  Control Engine 15/20 (Spectral PCA, K-Means++ Regime Clustering & Graph Laplacian Bottlenecks):\n"
        "    /pca | /pca status | -mode:status    : Run SVD PCA & K-Means++ clustering on the active problem/goal\n"
        "    /pca <problem>                       : Project <problem> into the 3D principal subspace and identify regime\n"
        "    /pca -mode:recompute | /pca recompute: Force full SVD/K-Means++ recomputation across all telemetry vectors\n"
        "    /pca -h | /pca --help | /kmeans -h   : Show this help message"
    ),
    "continual": (
        "=== Switch Help: --continual / /continual / /learn-mode ===\n"
        "  Control Engine 12/16 (5-Tier Continual Learning & Adaptive Plasticity):\n"
        "    /continual status | -mode:status         : Show 5-tier memory counts and continual learning state\n"
        "    /continual -mode:auto  | /continual auto : Enable automatic background continual learning after every tool call\n"
        "    /continual -mode:start | /continual start: Force an immediate Dirichlet consolidation & Hedge calibration pass\n"
        "    /continual -mode:stop  | /continual stop : Freeze all continual learning weights and priors\n"
        "    --continual -h | /continual -h | /continual --help : Show this help message"
    ),
    "train": (
        "=== Switch Help: /train ===\n"
        "  Run the Multi-Modal Document & Image OCR Training Pipeline (Training/ -> core/ObsidianVault/):\n"
        "    /train                               : Incremental training on CORA/Training/\n"
        "    /train -path:<folder>                : Train on documents/PDFs/images in <folder>\n"
        "    /train -mode:force | /train force    : Force full re-distillation of all files\n"
        "    /train status | /train -mode:status  : Show training ledger status and indexed document counts\n"
        "    /train -h | /train --help            : Show this help message"
    ),
    "reason": (
        "=== Switch Help: /reason / /mdp ===\n"
        "  Run the 15-Engine CPU-Only Neuro-Symbolic Reasoning Suite (0 MB GPU VRAM):\n"
        "    /reason <problem>                          : Run full 15-Engine 5-Layer Lexical Pipeline on <problem>\n"
        "    /reason status | -mode:status              : Show status of all 15 engines and learned weight files\n"
        "    /reason test   | -mode:test                : Run deterministic self-tests across all reasoning engines\n"
        "    /reason -engine:mdp [problem] | /mdp       : Run Engine 11 Hierarchical MDP Bellman planner\n"
        "    /reason -engine:rl [problem]               : Run Engine 14 Trajectory RL planner\n"
        "    /reason -engine:pca [problem]              : Run Engine 15 Spectral PCA & K-Means++ engine\n"
        "    /reason -h | /reason --help | /mdp -h      : Show this help message"
    ),
    "hud": (
        "=== Switch Help: --hud / --no-hud / /hud ===\n"
        "  Control the Live Hardware & Telemetry HUD Bar:\n"
        "    /hud on | /hud off | /hud pin | /hud prompt | /hud title\n"
        "    --hud -h | /hud -h | /hud --help    : Show this help message"
    ),
    "scan": (
        "=== Switch Help: /scan ===\n"
        "  Scan a target URL, API endpoint, or host and save the report to Projects/<project>/targets/:\n"
        "    /scan -target:<url_or_ip> | /scan <url_or_ip> : Probe HTTP headers, status, forms, endpoints, and TLS certs\n"
        "    /scan -h | /scan --help                       : Show this help message"
    ),
    "vault": (
        "=== Switch Help: /vault ===\n"
        "  Display the Long-Term Obsidian Knowledge Vault index (ObsidianVault/00_MEMORY_INDEX.md):\n"
        "    /vault                              : Print full hot memory index\n"
        "    /vault -h | /vault --help           : Show this help message"
    ),
    "remember": (
        "=== Switch Help: /remember ===\n"
        "  Save a permanent fact or rule into ObsidianVault/knowledge/:\n"
        "    /remember -fact:\"<text>\" | /remember \"<fact text>\" : Store <fact text> in long-term vault memory\n"
        "    /remember -h | /remember --help                    : Show this help message"
    ),
    "search": (
        "=== Switch Help: /search ===\n"
        "  Search across both the active Projects/<project>/ workspace and ObsidianVault/:\n"
        "    /search -query:<keyword> | /search <keyword> : Search notes, targets, playbooks, and reasoning reports\n"
        "    /search -h | /search --help                  : Show this help message"
    ),
    "permissions": (
        "=== Switch Help: --confirm / --dangerously-skip-permissions / /permissions ===\n"
        "  Control confirmation prompts before executing shell commands or writing files:\n"
        "    /permissions                         : Toggle between AUTO-RUN and CONFIRM ON\n"
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
        "  Control Qwen3 Chain-of-Thought (<think>) reasoning budget on llama-server:\n"
        "    --no-think                          : Disable <think> blocks (--reasoning-budget 0, fastest, default)\n"
        "    --think                             : Enable full Chain-of-Thought <think> blocks (--reasoning-budget -1)\n"
        "    --think -h | --think --help         : Show this help message"
    ),
}

WEBUI_SWITCH_ALIASES: Dict[str, str] = {
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
    "p": "project",
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
    "status": "hw",
    "think": "think",
    "no-think": "think",
}


def _format_webui_switch_help(switch_name: str = "") -> str:
    key = switch_name.strip().lstrip("-/").lower()
    resolved = WEBUI_SWITCH_ALIASES.get(key, key)
    if resolved and resolved in WEBUI_SWITCH_HELP_MAP:
        return f"```text\n{WEBUI_SWITCH_HELP_MAP[resolved]}\n```"

    lines_out = [
        "### C.O.R.A. (Cyber Oriented Reasoning Agent) CLI & WebUI Switch Help",
        "Pass `-h` or `--help` after ANY `/` command (e.g. `/relentless -h`, `/goal -h`, `/mode -h`, `/netiso -h`, `/rl -h`) for detailed options:\n",
        "```text",
    ]
    for k, block in WEBUI_SWITCH_HELP_MAP.items():
        b_lines = block.splitlines()
        header = b_lines[0].replace("=== Switch Help: ", "").replace(" ===", "")
        first_desc = b_lines[1].strip() if len(b_lines) > 1 else ""
        lines_out.append(f"  {header:<46} {first_desc}")
    lines_out.append("```")
    return "\n".join(lines_out)


@app.post("/api/query")
async def api_submit_query(req: QuerySubmitRequest) -> Dict[str, Any]:
    """
    Main dashboard query handler:
      1. Applies any inline dropdown selections (Project, Mode, Network Isolation, Model, Thinking, Permissions).
      2. Runs the 15-Engine Neuro-Symbolic Reasoning Pipeline (`run_full_20_engine_pipeline`).
      3. Optionally executes a requested shell command (guarded by CEGAR + Analyst/White isolation rules).
      4. Automatically starts/switches `llama-server` if needed and queries the selected local LLM (`llama-server` or `Ollama`).
      5. Saves both the user query and CORA response to SQLite (`messages`) and updates `Projects/<slug>/reasoning/`.
    """
    t0 = time.perf_counter()
    cfg = get_all_settings()

    # Apply any inline selector overrides
    active_proj = resolve_active_project_slug(req.project_slug, cfg=cfg)
    if not active_proj:
        raise HTTPException(
            status_code=400,
            detail="No project selected. Please select an existing project or create a new project first.",
        )
    mode_key = (req.session_mode or cfg.get("session_mode") or "default").lower()
    if mode_key not in SESSION_MODES:
        mode_key = "default"
    mode_info = SESSION_MODES[mode_key]

    iso_level = (req.isolation_level or cfg.get("isolation_level") or "red").lower()
    if mode_info["forced_isolation"]:
        iso_level = mode_info["forced_isolation"]
    elif iso_level not in mode_info["allowed_isolation"]:
        iso_level = mode_info["allowed_isolation"][0]

    ifaces = req.allowed_interfaces or cfg.get("allowed_interfaces") or "eth0,eth1"
    model_id = req.selected_model or cfg.get("selected_model") or "3.8"
    thinking_on = req.thinking_enabled if req.thinking_enabled is not None else (cfg.get("thinking_enabled") == "true")
    perm_mode = req.permission_mode or cfg.get("permission_mode") or "confirm"

    cfg = update_settings_dict(
        {
            "active_project": active_proj,
            "session_mode": mode_key,
            "isolation_level": iso_level,
            "allowed_interfaces": ifaces,
            "selected_model": model_id,
            "thinking_enabled": "true" if thinking_on else "false",
            "permission_mode": perm_mode,
        }
    )

    proj_dir = ensure_project_structure(active_proj)
    override_str = f"blue:{ifaces}" if iso_level == "blue" else iso_level
    posture = _get_cached_posture(override_str)

    active_goal = get_project_last_goal(proj_dir) or cfg.get("active_goal", "")
    query_text = (req.query or "").strip()
    if not query_text and not req.execute_command:
        if active_goal:
            query_text = f"/goal {active_goal}"
        else:
            raise HTTPException(status_code=400, detail="Query text cannot be empty.")

    # -----------------------------------------------------------------------
    # 1. Intercept `/help` or ANY `<switch> -h` / `--help` before executing
    #    shell probes or invoking the LLM (Full CLI Switch Parity)
    # -----------------------------------------------------------------------
    q_tokens = query_text.split()
    if q_tokens and (query_text.startswith("/") or query_text.startswith("-")):
        first_tok = q_tokens[0].lstrip("-/").split(":")[0].lower()
        has_help_flag = any(
            t.lower() in ("-h", "--help", "-?") or t.lower().endswith((":-h", ":--help"))
            for t in q_tokens[1:]
        )
        if first_tok in ("help", "h", "?"):
            target_sw = q_tokens[1] if len(q_tokens) > 1 else ""
            help_md = _format_webui_switch_help(target_sw)
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=help_md,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Switch Help",
                t0=t0,
                llm_online=True,
                llm_error="",
            )
        if has_help_flag and first_tok in WEBUI_SWITCH_ALIASES:
            rel_on = cfg.get("relentless_mode", "false") == "true"
            rel_max = cfg.get("relentless_max_waves", "12")
            max_lbl = "0 (UNLIMITED — never stop)" if str(rel_max) == "0" else f"{rel_max} waves"
            help_md = (
                f"{_format_webui_switch_help(first_tok)}\n\n"
                f"**Active Session Context (`Projects/{active_proj}/`):**\n"
                f"- **Active Goal:** `{active_goal or '(none set)'}`\n"
                f"- **Relentless Mode:** `{'ON (ARMED)' if rel_on else 'OFF (Single-Turn)'}` (`Max Waves: {max_lbl}`)\n"
                f"- **Session Mode / Posture:** `[{mode_info['number']}] {mode_info['label']}` | `{posture.get('hud_badge')}`"
            )
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=help_md,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Switch Help",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

    # -----------------------------------------------------------------------
    # 2. Handle `/clear`, `/status`, `/hw`, `/vault`, `/remember`, `/search`, `/state`
    # -----------------------------------------------------------------------
    q_low = query_text.lower()
    if q_low in ("/clear", "/clear status"):
        with get_db_conn() as conn:
            conn.execute("DELETE FROM messages WHERE project_slug = ?", (active_proj,))
            conn.commit()
        return {
            "ok": True,
            "conversation_id": req.conversation_id or f"conv-{active_proj}",
            "project_slug": active_proj,
            "reply": f"Cleared conversation display for `Projects/{active_proj}/`.",
            "thinking": "",
            "command_result": {},
            "reasoning": {},
            "posture": posture,
            "active_mode": mode_info,
            "model_used": "CORA System",
            "latency_ms": round((time.perf_counter() - t0) * 1000.0, 1),
            "llm_online": True,
            "llm_error": "",
        }

    if q_low in ("/status", "/hw", "/state", "/context"):
        hw = await asyncio.to_thread(collect_hardware_metrics)
        llama_st = await asyncio.to_thread(
            _get_llama_health, cfg.get("llama_api_base", "http://127.0.0.1:8080/v1")
        )
        gpu_lines = []
        for g in hw.get("gpus") or []:
            gpu_lines.append(
                f"GPU{g.get('index', 0)} {g.get('name')}: {g.get('utilization_pct', 0):.0f}% util | "
                f"VRAM {g.get('vram_used_mb', 0)/1024:.1f}/{g.get('vram_total_mb', 0)/1024:.1f} GB | {g.get('temperature_c', 0)}C"
            )
        rel_on = cfg.get("relentless_mode", "false") == "true"
        rel_max = cfg.get("relentless_max_waves", "12")
        status_md = (
            f"### C.O.R.A. Live Hardware & Session Telemetry (`Projects/{active_proj}/`)\n"
            f"- **CPU / RAM:** `{hw['cpu']['utilization_pct']:.1f}%` ({hw['cpu']['logical_cores']} threads) | "
            f"`{hw['ram']['used_gb']:.1f}/{hw['ram']['total_gb']:.1f} GB` (`{hw['ram']['utilization_pct']:.0f}%`)\n"
            f"- **GPUs:** `{' ; '.join(gpu_lines) if gpu_lines else 'CPU-Only Mode'}`\n"
            f"- **Local LLM (`llama-server`):** `{'ONLINE' if llama_st.get('online') else 'STANDBY'}` "
            f"(Active Model: `{llama_st.get('active_model') or model_id}`, API: `{llama_st.get('api_url')}`)\n"
            f"- **Session Mode & Network Isolation:** `[{mode_info['number']}] {mode_info['label']}` | `{posture.get('hud_badge')}`\n"
            f"- **Active Goal:** `{active_goal or '(none set)'}`\n"
            f"- **Relentless Controller:** `{'ON (ARMED)' if rel_on else 'OFF'}` (Max Waves: `{rel_max}`)"
        )
        return _persist_and_return_turn(
            conversation_id=req.conversation_id or f"conv-{active_proj}",
            project_slug=active_proj,
            user_query=query_text,
            reply_content=status_md,
            thinking_content="",
            cmd_res={},
            reasoning_res={},
            posture=posture,
            mode_info=mode_info,
            model_id="CORA Telemetry",
            t0=t0,
            llm_online=True,
            llm_error="",
        )

    if q_low.startswith("/vault"):
        idx_file = Path(VAULT_DIR) / "00_MEMORY_INDEX.md"
        idx_txt = idx_file.read_text(encoding="utf-8", errors="replace")[:4500] if idx_file.is_file() else "(Vault index empty)"
        proj_mem = (proj_dir / "memory.md").read_text(encoding="utf-8", errors="replace")[:2500] if (proj_dir / "memory.md").is_file() else ""
        vault_md = (
            f"### Obsidian Knowledge Vault (`core/ObsidianVault/00_MEMORY_INDEX.md`)\n"
            f"```markdown\n{idx_txt}\n```\n\n"
            f"### Active Project Memory (`Projects/{active_proj}/memory.md`)\n"
            f"```markdown\n{proj_mem}\n```"
        )
        return _persist_and_return_turn(
            conversation_id=req.conversation_id or f"conv-{active_proj}",
            project_slug=active_proj,
            user_query=query_text,
            reply_content=vault_md,
            thinking_content="",
            cmd_res={},
            reasoning_res={},
            posture=posture,
            mode_info=mode_info,
            model_id="CORA Vault",
            t0=t0,
            llm_online=True,
            llm_error="",
        )

    if q_low.startswith("/remember"):
        fact_arg = re.sub(r"^/remember\s+(-fact:)?", "", query_text, flags=re.IGNORECASE).strip().strip('"')
        if not fact_arg:
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=_format_webui_switch_help("remember"),
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Vault",
                t0=t0,
                llm_online=True,
                llm_error="",
            )
        mem_path = proj_dir / "memory.md"
        existing = mem_path.read_text(encoding="utf-8", errors="replace") if mem_path.is_file() else ""
        mem_path.write_text(existing.rstrip() + f"\n- **[{_now_iso()}] Operator Fact:** {fact_arg}\n", encoding="utf-8")
        return _persist_and_return_turn(
            conversation_id=req.conversation_id or f"conv-{active_proj}",
            project_slug=active_proj,
            user_query=query_text,
            reply_content=f"Saved permanent fact to `Projects/{active_proj}/memory.md`:\n> {fact_arg}",
            thinking_content="",
            cmd_res={},
            reasoning_res={},
            posture=posture,
            mode_info=mode_info,
            model_id="CORA Vault",
            t0=t0,
            llm_online=True,
            llm_error="",
        )

    if q_low.startswith("/search"):
        kw = re.sub(r"^/search\s+(-query:)?", "", query_text, flags=re.IGNORECASE).strip().strip('"')
        if not kw:
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=_format_webui_switch_help("search"),
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Search",
                t0=t0,
                llm_online=True,
                llm_error="",
            )
        hits: List[str] = []
        for root_p in (proj_dir, Path(VAULT_DIR)):
            if not root_p.is_dir():
                continue
            for fp in root_p.rglob("*.md"):
                try:
                    txt = fp.read_text(encoding="utf-8", errors="replace")
                    if kw.lower() in txt.lower():
                        rel_f = fp.relative_to(CORA_ROOT).as_posix()
                        for line in txt.splitlines():
                            if kw.lower() in line.lower():
                                hits.append(f"- `{rel_f}`: {line.strip()[:160]}")
                                break
                except Exception:
                    pass
                if len(hits) >= 20:
                    break
        search_md = (
            f"### Workspace & Vault Search Results for `{kw}` ({len(hits)} matches)\n\n"
            + ("\n".join(hits) if hits else "_No matching markdown notes found._")
        )
        return _persist_and_return_turn(
            conversation_id=req.conversation_id or f"conv-{active_proj}",
            project_slug=active_proj,
            user_query=query_text,
            reply_content=search_md,
            thinking_content="",
            cmd_res={},
            reasoning_res={},
            posture=posture,
            mode_info=mode_info,
            model_id="CORA Search",
            t0=t0,
            llm_online=True,
            llm_error="",
        )

    # -----------------------------------------------------------------------
    # 3. Handle `/relentless` & `/goal` Subcommands and Autonomous Pursuit
    # -----------------------------------------------------------------------
    is_goal_pursuit = False
    relentless_waves_requested = False

    if q_low.startswith("/relentless"):
        rel_rest = query_text[11:].strip()
        rel_low = rel_rest.lower()
        cur_rel_on = cfg.get("relentless_mode", "false") == "true"
        cur_rel_max = int(cfg.get("relentless_max_waves") or 12)

        # Parse optional -max:<#>
        max_match = re.search(r"-max:([0-9]+|unlimited|inf|infinite)", rel_rest, flags=re.IGNORECASE)
        if max_match:
            m_val = max_match.group(1).lower()
            cur_rel_max = 0 if m_val in ("0", "unlimited", "inf", "infinite") else max(1, int(m_val))
            cfg = update_settings_dict({"relentless_max_waves": str(cur_rel_max)})
            rel_rest = (rel_rest[: max_match.start()] + rel_rest[max_match.end() :]).strip()
            rel_low = rel_rest.lower()

        if rel_low in ("status", "-mode:status"):
            max_lbl = "0 (UNLIMITED — never stop)" if cur_rel_max == 0 else f"{cur_rel_max} waves"
            goal_lbl = active_goal or '(none — set via /goal "<objective>" or /relentless "<objective>")'
            status_txt = (
                "```text\n"
                f"Relentless Mode : {'ON (ARMED)' if cur_rel_on else 'OFF (Single-Turn)'}\n"
                f"Max Waves Cap   : {max_lbl}\n"
                f"Active Goal     : {goal_lbl}\n"
                "```"
            )
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=status_txt,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Relentless Controller",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

        if rel_low in ("on", "-mode:on", "off", "-mode:off") or (max_match and not rel_rest):
            if rel_low in ("on", "-mode:on"):
                cur_rel_on = True
            elif rel_low in ("off", "-mode:off"):
                cur_rel_on = False
            cfg = update_settings_dict({"relentless_mode": "true" if cur_rel_on else "false"})
            max_lbl = "0 (UNLIMITED — never stop)" if cur_rel_max == 0 else f"{cur_rel_max} waves"
            goal_lbl = active_goal or '(none — set via /goal "<objective>" or /relentless "<objective>")'
            status_txt = (
                "```text\n"
                f"Relentless Mode : {'ON (ARMED)' if cur_rel_on else 'OFF (Single-Turn)'}\n"
                f"Max Waves Cap   : {max_lbl}\n"
                f"Active Goal     : {goal_lbl}\n"
                "```"
            )
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=status_txt,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Relentless Controller",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

        if rel_low in ("audit", "-mode:audit"):
            goals_file = proj_dir / "goals.md"
            goals_txt = goals_file.read_text(encoding="utf-8", errors="replace")[:3500] if goals_file.is_file() else "(no goals recorded)"
            audit_md = (
                f"### Relentless Controller Audit (`Projects/{active_proj}/`)\n"
                f"- **Relentless Mode:** `{'ON (ARMED)' if cur_rel_on else 'OFF'}`\n"
                f"- **Max Waves Cap:** `{cur_rel_max if cur_rel_max > 0 else '0 (UNLIMITED)'}`\n"
                f"- **Active Goal:** `{active_goal or '(none)'}`\n\n"
                f"#### Project Goal Ledger (`Projects/{active_proj}/goals.md`)\n"
                f"```markdown\n{goals_txt}\n```"
            )
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=audit_md,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Relentless Controller",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

        # Otherwise `/relentless` or `/relentless "<goal text>" [-max:<#>]`: arm and pursue goal!
        is_goal_pursuit = True
        relentless_waves_requested = True
        cfg = update_settings_dict({"relentless_mode": "true"})
        cleaned_goal = rel_rest.strip().strip('"').strip("'")
        if cleaned_goal:
            active_goal = cleaned_goal
            update_settings_dict({"active_goal": active_goal})
            if active_goal != get_project_last_goal(proj_dir):
                append_project_goal(proj_dir, active_goal)
        elif not active_goal:
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=(
                    "No active goal is set for `/relentless`. Set one via:\n"
                    "- `/relentless \"<objective text>\" [-max:<#>]`\n"
                    "- `/goal \"<objective text>\"`\n\n"
                    + _format_webui_switch_help("relentless")
                ),
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Relentless Controller",
                t0=t0,
                llm_online=True,
                llm_error="",
            )
        query_text = (
            f"[Relentless Autonomous Goal Pursuit (Max Waves={cur_rel_max or 'UNLIMITED'})]: {active_goal}\n"
            "Execute multi-step diagnostic/reconnaissance tools (`scan_target`, `run_shell_command`), pivot across "
            "capabilities if any probe fails or times out, and deliver a complete, verified resolution for every requirement of this goal."
        )

    elif q_low.startswith("/goal"):
        goal_rest = query_text[5:].strip()
        goal_low = goal_rest.lower()
        if goal_low in ("status", "-mode:status"):
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=f"### Active Project Goal (`Projects/{active_proj}/goals.md`)\n- **Active Goal:** `{active_goal or '(none set)'}`",
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Goal Manager",
                t0=t0,
                llm_online=True,
                llm_error="",
            )
        if goal_low in ("list", "-mode:list", "audit", "-mode:audit"):
            goals_file = proj_dir / "goals.md"
            goals_txt = goals_file.read_text(encoding="utf-8", errors="replace")[:4000] if goals_file.is_file() else "(no goals recorded)"
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=f"### Historical Goals (`Projects/{active_proj}/goals.md`)\n```markdown\n{goals_txt}\n```",
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Goal Manager",
                t0=t0,
                llm_online=True,
                llm_error="",
            )
        if goal_low in ("clear", "-mode:clear"):
            active_goal = ""
            update_settings_dict({"active_goal": ""})
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=f"Cleared active in-memory goal for `Projects/{active_proj}/`.",
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Goal Manager",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

        is_goal_pursuit = True
        max_match = re.search(r"-max:([0-9]+|unlimited|inf|infinite)", goal_rest, flags=re.IGNORECASE)
        if max_match:
            m_val = max_match.group(1).lower()
            cur_rel_max = 0 if m_val in ("0", "unlimited", "inf", "infinite") else max(1, int(m_val))
            update_settings_dict({"relentless_max_waves": str(cur_rel_max), "relentless_mode": "true"})
            relentless_waves_requested = True
            goal_rest = (goal_rest[: max_match.start()] + goal_rest[max_match.end() :]).strip()

        goal_arg = goal_rest.strip().strip('"').strip("'")
        if goal_arg:
            active_goal = goal_arg
            update_settings_dict({"active_goal": active_goal})
            if active_goal != get_project_last_goal(proj_dir):
                append_project_goal(proj_dir, active_goal)
        elif not active_goal:
            raise HTTPException(status_code=400, detail="No active goal is set. Provide `/goal \"<objective>\"`.")
        query_text = (
            f"[Active Goal Pursuit]: {active_goal}\n"
            "Execute necessary diagnostic/reconnaissance tools (`scan_target`, `run_shell_command`) and provide a complete, "
            "actionable resolution for every requirement of this goal."
        )

    # Handle /files, /file, /upload, /add slash commands for Projects/<project>/Files/
    if q_low.startswith(("/files", "/file", "/upload", "/add")) and (
        q_low in ("/files", "/file", "/upload", "/add")
        or q_low.startswith(("/files ", "/file ", "/upload ", "/add "))
    ):
        cmd_tok = query_text.split(" ", 1)[0].lower()
        rest_arg = query_text.split(" ", 1)[1].strip() if " " in query_text else ""
        if cmd_tok in ("/upload", "/add") and rest_arg and not rest_arg.lower().startswith(("add ", "list", "read ", "rm ")):
            rest_arg = f"add {rest_arg}"
        rest_low = rest_arg.lower()
        files_dir = (proj_dir / "Files").resolve()
        files_dir.mkdir(parents=True, exist_ok=True)

        if not rest_arg or rest_low in ("list", "-mode:list", "status", "-mode:status"):
            res_list = _execute_webui_list_project_files("Files", active_proj)
            reply_md = (
                f"### Project Local `Files` Directory (`Projects/{active_proj}/Files/`)\n"
                f"- **Full Path (`$PROJECT_FILES_DIR`):** `{files_dir}`\n"
                f"- **LLM Integration:** Every file placed or uploaded in `Projects/{active_proj}/Files/` is automatically visible to the LLM via `read_project_file`, `list_project_files_tool`, `write_project_file`, and `run_shell_command`.\n\n"
                f"```text\n{res_list.get('output', '')}\n```"
            )
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=reply_md,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Project Files Manager",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

        if rest_low.startswith(("add ", "-add:", "-path:")):
            raw_p = re.sub(r"^(?:add\s+|-add:|-path:)", "", rest_arg, flags=re.I).strip().strip('"').strip("'")
            up_res = await api_upload_project_files(
                ProjectFileUploadRequest(project_slug=active_proj, local_path=raw_p)
            )
            up_list = up_res.get("uploaded") or []
            up_lines = [f"- `{item['rel_path']}` ({item['size_bytes']} bytes)" for item in up_list]
            reply_md = (
                f"### Added {len(up_list)} File(s) to `Projects/{active_proj}/Files/`\n"
                + "\n".join(up_lines)
                + f"\n\nThe LLM can now directly inspect, read, edit, or execute these files in `Projects/{active_proj}/Files/`."
            )
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=reply_md,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Project Files Manager",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

        if rest_low.startswith(("read ", "cat ", "view ")):
            target_f = rest_arg.split(" ", 1)[1].strip().strip('"').strip("'")
            r_res = _execute_webui_read_project_file(target_f, active_proj)
            reply_md = f"### Read Project File (`Projects/{active_proj}/Files/`)\n```text\n{r_res.get('output', '')}\n```"
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=reply_md,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Project Files Manager",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

        if rest_low.startswith(("rm ", "del ", "delete ")):
            target_f = rest_arg.split(" ", 1)[1].strip().strip('"').strip("'")
            del_res = await api_delete_project_file(
                ProjectFileDeleteRequest(project_slug=active_proj, rel_path=target_f)
            )
            reply_md = f"Deleted `{del_res.get('deleted')}` from `Projects/{active_proj}/Files/`."
            return _persist_and_return_turn(
                conversation_id=req.conversation_id or f"conv-{active_proj}",
                project_slug=active_proj,
                user_query=query_text,
                reply_content=reply_md,
                thinking_content="",
                cmd_res={},
                reasoning_res={},
                posture=posture,
                mode_info=mode_info,
                model_id="CORA Project Files Manager",
                t0=t0,
                llm_online=True,
                llm_error="",
            )

    # Handle /generate-report or /report slash command shortcuts typed into the WebUI query box
    if query_text.lower().startswith(("/generate-report", "/report")):
        focus_arg = query_text.split(" ", 1)[1].strip() if " " in query_text else (active_goal or "")
        rep = await asyncio.to_thread(
            generate_project_report,
            project_name=active_proj,
            report_focus=focus_arg,
            use_llm=True,
        )
        reply_md = (
            f"### Generated 5-Section Project Report (`Projects/{active_proj}/REPORT.md`)\n\n"
            f"- **Report Path:** `Projects/{active_proj}/REPORT.md`\n"
            f"- **SVG Dashboard:** `Projects/{active_proj}/assets/report_dashboard.svg`\n"
            f"- **Overall Status:** `{rep.get('overall_status')}` (`{rep.get('task_completion_pct')}%` milestones)\n\n"
            + str(rep.get("markdown", ""))[:6000]
        )
        reasoning_res = await asyncio.to_thread(
            run_neuro_symbolic_pipeline,
            problem=focus_arg or f"Project {active_proj} status report",
            save_to_vault=True,
        )
        return _persist_and_return_turn(
            conversation_id=req.conversation_id or f"conv-{active_proj}",
            project_slug=active_proj,
            user_query=query_text,
            reply_content=reply_md,
            thinking_content="",
            cmd_res={},
            reasoning_res=reasoning_res,
            posture=posture,
            mode_info=mode_info,
            model_id=model_id,
            t0=t0,
            llm_online=True,
            llm_error="",
        )

    # Optional pre-execution of a shell command if explicitly requested in the Command Probe box
    cmd_res: Dict[str, Any] = {}
    if req.execute_command:
        cmd_res = await asyncio.to_thread(
            execute_safe_shell_command,
            req.execute_command,
            mode_info,
            posture,
            active_proj,
        )

    # Run 15-Engine Neuro-Symbolic Reasoning Pipeline
    reasoning_res: Dict[str, Any] = {}
    if req.run_reasoning:
        t_pipe = time.perf_counter()
        problem_input = query_text or req.execute_command or active_goal or "System check"
        if cmd_res.get("output"):
            problem_input += "\n" + str(cmd_res.get("output"))[:1500]
        reasoning_res = await asyncio.to_thread(
            run_neuro_symbolic_pipeline,
            problem=problem_input,
            save_to_vault=(not mode_info["read_only"]),
        )
        reasoning_res["pipeline_latency_ms"] = round((time.perf_counter() - t_pipe) * 1000.0, 2)
        reasoning_res["cegar_verification"] = verify_command_cegar(
            str(reasoning_res.get("consensus_immediate_action") or "")
        )

    # Build KV-cache-friendly static system prompt + clean multi-turn history
    mem_excerpt = ""
    mem_file = proj_dir / "memory.md"
    if mem_file.is_file():
        mem_excerpt = mem_file.read_text(encoding="utf-8", errors="replace")[:900]
    host_os_label = "Windows (PowerShell / CMD / Sysinternals)" if os.name == "nt" else "Linux (Bash / iproute2)"
    project_files_block = get_project_files_context_block(
        proj_dir=proj_dir,
        query_text=query_text,
        attached_files=req.attached_files,
    )

    sys_prompt = (
        f"You are C.O.R.A. (Cyber Oriented Reasoning Agent) v{get_cora_version().get('version', '5.15.12')}, "
        f"an elite cybersecurity, network reconnaissance, and incident response agent running on {host_os_label}.\n"
        f"- Active Project Workspace: `Projects/{active_proj}/`\n"
        f"- Local Project `Files` Directory (`$PROJECT_FILES_DIR`): `Projects/{active_proj}/Files/` (full path: `{proj_dir / 'Files'}`)\n"
        f"- Active Goal: `{active_goal or 'General interactive session'}`\n"
        f"- Session Personality Mode: `[{mode_info['number']}] {mode_info['label']}` — {mode_info['system_directive']}\n"
        f"- Network Isolation Posture: `{posture.get('hud_badge')}` ({posture.get('description')})\n"
        f"- Permission Policy: `{perm_mode.upper()}`\n\n"
        "### Operational Directives:\n"
        "1. Directly address the operator's specific request, target IP/hostname, and Active Goal in clear, comprehensive detail.\n"
        "2. When the operator asks to probe, scan, ping, or identify a service/appliance (such as a Fortinet firewall, web server, "
        "or host process) and live command output is not yet attached, call `scan_target` or `run_shell_command` to gather real telemetry first.\n"
        "3. When live command/probe output IS provided, analyze the exact findings (open/closed ports, TLS certificate serial/model strings, "
        "HTTP headers, `Last-Modified` firmware build dates, static asset hashes, relevant CVEs for that firmware window, and concrete "
        "administrative/CLI/HTTPS access procedures) and provide copy-pasteable commands.\n"
        f"4. **Local Project `Files` Directory (`Projects/{active_proj}/Files/`)**: Every project has a dedicated `Files` directory at `Projects/{active_proj}/Files/`. Anything placed or uploaded into `Projects/{active_proj}/Files/` is directly visible and usable by you. When the operator tells you to go to the local `Files` or `File` directory to look at, analyze, or use a custom script or file, inspect `Projects/{active_proj}/Files/` using `read_project_file`, `list_project_files_tool`, `write_project_file`, or execute scripts there via `run_shell_command`.\n"
        "5. Keep your output clean, structured, and easy to read. Do NOT dump internal reasoning engine numbers or raw thought processes into your main response unless the operator explicitly runs `/reason`.\n\n"
        f"{project_files_block}\n\n"
        f"### Active Project Memory (`Projects/{active_proj}/memory.md`)\n{mem_excerpt}\n"
    )

    # Load up to 4 clean messages from SQLite (filtering out any fallback synthesis blocks, incomplete phase stubs, or test strings)
    history_msgs: List[Dict[str, str]] = []
    try:
        with get_db_conn() as conn:
            recent_rows = conn.execute(
                "SELECT role, content FROM messages WHERE project_slug = ? ORDER BY id DESC LIMIT 6",
                (active_proj,),
            ).fetchall()
        for r in reversed(recent_rows):
            r_role = str(r["role"] or "user")
            r_content = str(r["content"] or "").strip()
            if r_role not in ("user", "assistant") or not r_content:
                continue
            if r_content.upper() == "ONLINE" or r_content.startswith("Reply with the single word ONLINE"):
                continue
            if r_content.startswith("### 15-Engine Neuro-Symbolic Synthesis") or r_content.startswith("### C.O.R.A. Tactical Assessment"):
                continue
            if r_content.endswith("extract the version string:"):
                continue
            # Maintain strict user/assistant alternation for Jinja chat templates
            if history_msgs and history_msgs[-1]["role"] == r_role:
                history_msgs[-1]["content"] = r_content[:1200]
            else:
                history_msgs.append({"role": r_role, "content": r_content[:1200]})
        if history_msgs and history_msgs[0]["role"] == "assistant":
            history_msgs = history_msgs[1:]
        if history_msgs and history_msgs[-1]["role"] == "user":
            history_msgs = history_msgs[:-1]
    except Exception:
        history_msgs = []

    user_prompt = query_text
    if req.attached_files:
        clean_attached = [str(a).strip() for a in req.attached_files if str(a).strip()]
        if clean_attached:
            user_prompt += (
                f"\n\n[Attached Project Files in `Projects/{active_proj}/Files/`]: "
                + ", ".join(f"`{a}`" for a in clean_attached)
                + f"\n{project_files_block}"
            )
    elif re.search(r"\b(?:files?\s+dir(?:ectory)?|local\s+files?|uploaded|custom\s+scripts?|in\s+files|from\s+files)\b", query_text, flags=re.I):
        user_prompt += f"\n\n{project_files_block}"

    if active_goal and not is_goal_pursuit and active_goal.lower() not in query_text.lower():
        user_prompt += f"\n\n[Active Project Goal Context]: {active_goal}"
    if cmd_res.get("command"):
        if cmd_res.get("blocked"):
            user_prompt += (
                f"\n\n[Command Guardrail Verdict for `{cmd_res.get('command')}`]: "
                f"BLOCKED — {cmd_res.get('reason')}"
            )
        else:
            user_prompt += (
                f"\n\n[Live Host Command Executed]: `{cmd_res.get('command')}` (exit={cmd_res.get('exit_code')}, {cmd_res.get('latency_ms')} ms)\n"
                f"```text\n{str(cmd_res.get('output', ''))[:3500]}\n```"
            )

    wire_messages: List[Dict[str, Any]] = [{"role": "system", "content": sys_prompt}]
    wire_messages.extend(history_msgs)
    wire_messages.append({"role": "user", "content": user_prompt})

    agent_tools = WEBUI_AGENT_TOOLS if not mode_info["read_only"] else WEBUI_READONLY_AGENT_TOOLS
    executed_cmds_list: List[str] = [str(cmd_res["command"])] if cmd_res.get("command") else []
    executed_outs_list: List[str] = [str(cmd_res.get("output") or cmd_res.get("reason") or "")] if cmd_res.get("command") else []
    all_thinking_parts: List[str] = []

    llm_res: Dict[str, Any] = {}
    last_round_called_tools = False
    max_tool_rounds = 6 if (relentless_waves_requested or is_goal_pursuit or cfg.get("relentless_mode") == "true") else 3
    for tool_round in range(max_tool_rounds):
        llm_res = await asyncio.to_thread(
            _call_llm_backend,
            messages=wire_messages,
            model_id=model_id,
            cfg=cfg,
            thinking_enabled=thinking_on,
            tools=agent_tools,
        )
        if not llm_res.get("online"):
            break
        if llm_res.get("thinking"):
            all_thinking_parts.append(str(llm_res["thinking"]))

        t_calls = llm_res.get("tool_calls") or []
        if not t_calls:
            last_round_called_tools = False
            break

        last_round_called_tools = True
        # Append the assistant's tool_calls message
        wire_messages.append(
            {
                "role": "assistant",
                "content": str(llm_res.get("content") or ""),
                "tool_calls": t_calls,
            }
        )

        for tc in t_calls:
            tc_id = str(tc.get("id") or f"call_{tool_round}")
            fn_obj = tc.get("function") or {}
            fn_name = str(fn_obj.get("name") or "")
            raw_args = fn_obj.get("arguments") or "{}"
            try:
                parsed_args = json.loads(raw_args) if isinstance(raw_args, str) else dict(raw_args)
            except Exception:
                parsed_args = {"command": str(raw_args)}

            if fn_name == "read_project_file":
                p_val = str(parsed_args.get("path") or parsed_args.get("filename") or "Files").strip()
                t_res = await asyncio.to_thread(_execute_webui_read_project_file, p_val, active_proj)
                label_cmd = f"read_project_file({p_val})"
            elif fn_name == "list_project_files_tool":
                s_val = str(parsed_args.get("subdir") or "Files").strip()
                t_res = await asyncio.to_thread(_execute_webui_list_project_files, s_val, active_proj)
                label_cmd = f"list_project_files({s_val})"
            elif fn_name == "write_project_file":
                f_val = str(parsed_args.get("filename") or parsed_args.get("path") or "").strip()
                c_txt = str(parsed_args.get("content") or "")
                t_res = await asyncio.to_thread(_execute_webui_write_project_file, f_val, c_txt, mode_info, active_proj)
                label_cmd = f"write_project_file({f_val})"
            elif fn_name == "scan_target":
                t_val = str(parsed_args.get("target") or "").strip()
                t_res = await asyncio.to_thread(
                    _execute_webui_target_scan,
                    t_val,
                    mode_info,
                    posture,
                    active_proj,
                )
                label_cmd = f"scan_target({t_val})"
            elif fn_name == "run_shell_command":
                c_val = str(parsed_args.get("command") or "").strip()
                t_res = await asyncio.to_thread(
                    execute_safe_shell_command,
                    c_val,
                    mode_info,
                    posture,
                    active_proj,
                )
                label_cmd = c_val
            else:
                t_res = {"executed": False, "blocked": True, "reason": f"Unknown tool: {fn_name}"}
                label_cmd = fn_name

            if label_cmd:
                executed_cmds_list.append(label_cmd)
            out_txt = (
                f"BLOCKED: {t_res.get('reason')}"
                if t_res.get("blocked")
                else f"Exit Code: {t_res.get('exit_code', 0)}\n{t_res.get('output') or '(no output)'}"
            )
            executed_outs_list.append(f"=== Tool Executed: `{label_cmd}` ===\n{out_txt[:4500]}")
            wire_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc_id,
                    "name": fn_name,
                    "content": out_txt[:3500],
                }
            )

    # Re-evaluate the 15-Engine Neuro-Symbolic Pipeline with the live tool telemetry when tools were executed
    if req.run_reasoning and executed_outs_list:
        t_pipe2 = time.perf_counter()
        enriched_problem = f"{query_text}\n\n" + "\n\n".join(executed_outs_list)[:3000]
        reasoning_res = await asyncio.to_thread(
            run_neuro_symbolic_pipeline,
            problem=enriched_problem,
            save_to_vault=(not mode_info["read_only"]),
        )
        reasoning_res["pipeline_latency_ms"] = round((time.perf_counter() - t_pipe2) * 1000.0, 2)
        reasoning_res["cegar_verification"] = verify_command_cegar(
            str(reasoning_res.get("consensus_immediate_action") or "")
        )

    # Whenever the last tool round executed tools (`last_round_called_tools=True`) or the response content is empty/short,
    # perform a clean final synthesis call with all live tool telemetry embedded in the user message so the LLM
    # ALWAYS delivers a complete, thorough resolution of the query and goal.
    if llm_res.get("online") and executed_outs_list and (
        last_round_called_tools or len(str(llm_res.get("content") or "").strip()) < 240
    ):
        synth_user_prompt = (
            f"{user_prompt}\n\n"
            f"### Live Telemetry & Command Output Collected by C.O.R.A.:\n"
            f"```text\n" + "\n\n".join(executed_outs_list)[:8000] + "\n```\n\n"
            "Based on ALL of the live telemetry above, provide a complete, clear, and well-structured final analysis directly resolving every part of the operator's query and active goal (including exact hardware/software model, firmware version/build date from headers/certs/hashes, applicable CVEs, and step-by-step login/access instructions). Keep your response clean and do not repeat internal reasoning engine telemetry."
        )
        synth_messages: List[Dict[str, Any]] = [{"role": "system", "content": sys_prompt}]
        synth_messages.extend(history_msgs)
        synth_messages.append({"role": "user", "content": synth_user_prompt})
        synth_res = await asyncio.to_thread(
            _call_llm_backend,
            messages=synth_messages,
            model_id=model_id,
            cfg=cfg,
            thinking_enabled=thinking_on,
            tools=None,
        )
        if synth_res.get("online") and str(synth_res.get("content") or "").strip():
            llm_res = synth_res
            if synth_res.get("thinking"):
                all_thinking_parts.append(str(synth_res["thinking"]))

    # Persist concise tactical summary into Projects/<active_proj>/memory.md when pursuing a goal or executing tools
    if llm_res.get("online") and (is_goal_pursuit or executed_cmds_list) and not mode_info["read_only"]:
        try:
            mem_path = proj_dir / "memory.md"
            existing_mem = mem_path.read_text(encoding="utf-8", errors="replace") if mem_path.is_file() else ""
            stamp = _now_iso()
            summary_snip = re.sub(r"\s+", " ", str(llm_res.get("content") or "")).strip()[:320]
            cmds_str = ", ".join(executed_cmds_list) if executed_cmds_list else "LLM Analysis"
            mem_entry = f"\n- **[{stamp}]** (`{cmds_str}`): {summary_snip}\n"
            if len(existing_mem) < 24000:
                mem_path.write_text(existing_mem.rstrip() + "\n" + mem_entry, encoding="utf-8")
        except Exception:
            pass

    if executed_cmds_list:
        cmd_res = {
            "executed": True,
            "blocked": False,
            "command": " ; ".join(executed_cmds_list),
            "exit_code": cmd_res.get("exit_code", 0),
            "output": "\n\n".join(executed_outs_list)[:12000],
        }

    llm_online = bool(llm_res.get("online"))
    llm_error = str(llm_res.get("error") or "")
    effective_model_used = str(llm_res.get("model") or model_id)

    thinking_content = _format_internal_thinking_and_engine_trace(
        thinking_parts=all_thinking_parts,
        reasoning_res=reasoning_res,
        executed_cmds_list=executed_cmds_list,
        executed_outs_list=executed_outs_list,
        posture=posture,
        mode_info=mode_info,
    )

    if llm_online:
        reply_content = str(llm_res.get("content") or "").strip()
        if not reply_content and executed_outs_list:
            reply_content = (
                f"### Executed Tactical Probe (`{cmd_res.get('command')}`)\n\n"
                f"```text\n{cmd_res.get('output', '')[:4000]}\n```"
            )
    else:
        reply_content = _synthesize_neuro_symbolic_fallback_response(
            query=query_text,
            reasoning_res=reasoning_res,
            posture=posture,
            mode_info=mode_info,
            project_slug=active_proj,
            llm_error=llm_error,
            cmd_res=cmd_res,
        )

    return _persist_and_return_turn(
        conversation_id=req.conversation_id or f"conv-{active_proj}",
        project_slug=active_proj,
        user_query=query_text or f"[Command] {req.execute_command}",
        reply_content=reply_content,
        thinking_content=thinking_content,
        cmd_res=cmd_res,
        reasoning_res=reasoning_res,
        posture=posture,
        mode_info=mode_info,
        model_id=effective_model_used,
        t0=t0,
        llm_online=llm_online,
        llm_error=llm_error,
    )


def _persist_and_return_turn(
    conversation_id: str,
    project_slug: str,
    user_query: str,
    reply_content: str,
    thinking_content: str,
    cmd_res: Dict[str, Any],
    reasoning_res: Dict[str, Any],
    posture: Dict[str, Any],
    mode_info: Dict[str, Any],
    model_id: str,
    t0: float,
    llm_online: bool = True,
    llm_error: str = "",
) -> Dict[str, Any]:
    now = _now_iso()
    total_ms = round((time.perf_counter() - t0) * 1000.0, 1)
    rl_imm = reasoning_res.get("rl_immediate_action") or {}
    pca_cluster = reasoning_res.get("pca_cluster_assignment") or {}
    vsa_arch = reasoning_res.get("vsa_top_archetype") or {}
    compact_reasoning = {
        "pipeline_latency_ms": reasoning_res.get("pipeline_latency_ms", 0),
        "consensus_immediate_action": reasoning_res.get("consensus_immediate_action", ""),
        "cegar_verification": reasoning_res.get("cegar_verification", {}),
        "bayesian_top": {
            "cause": reasoning_res.get("top_root_cause", "N/A"),
            "posterior": reasoning_res.get("top_root_cause_probability", 0.0),
        },
        "dempster_shafer": {
            "top_hypothesis": reasoning_res.get("top_root_cause", "N/A"),
            "conflict_mass_K": reasoning_res.get("dempster_shafer_conflict_k", 0.0),
        },
        "mdp_policy": {
            "recommended_tactic_category": reasoning_res.get("mdp_optimal_tactic", "Reconnaissance"),
            "recommended_tool": reasoning_res.get("mdp_optimal_tool", "nmap"),
            "bellman_q_star": reasoning_res.get("mdp_optimal_q_star", 0.0),
            "optimal_stopping_decision": (reasoning_res.get("optimal_stopping") or {}).get("decision", "CONTINUE"),
        },
        "rl_network_policy": {
            "stage": reasoning_res.get("rl_state_key", "N/A"),
            "immediate_action": rl_imm.get("command", "N/A"),
            "immediate_q_value": rl_imm.get("q_star", 0.0),
        },
        "spectral_pca_kmeans": {
            "assigned_cluster_label": pca_cluster.get("cluster_id", "N/A"),
            "silhouette_score": pca_cluster.get("silhouette_score", 0.0),
            "cumulative_top3_variance_pct": reasoning_res.get("pca_cumulative_variance_pct", 0.0),
        },
        "vsa_top": {
            "archetype": vsa_arch.get("archetype", str(vsa_arch)) if isinstance(vsa_arch, dict) else str(vsa_arch),
            "somatic_valence": reasoning_res.get("somatic_gut_valence", 0.0),
        },
        "meta_calibration": {
            "rolling_brier_score": reasoning_res.get("meta_brier_score", 0.085),
            "expected_calibration_error_pct": reasoning_res.get("meta_ece_pct", 4.2),
        },
        "vault_note_saved": reasoning_res.get("vault_note", ""),
    }

    with get_db_conn() as conn:
        conn.execute(
            "INSERT INTO conversations (id, project_slug, title, mode, isolation_level, model, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET updated_at=excluded.updated_at, mode=excluded.mode, "
            "isolation_level=excluded.isolation_level, model=excluded.model",
            (
                conversation_id,
                project_slug,
                user_query[:80],
                mode_info["key"],
                posture.get("color_level", "RED").lower(),
                model_id,
                now,
                now,
            ),
        )
        conn.execute(
            "INSERT INTO messages (conversation_id, project_slug, role, content, thinking, command_executed, "
            "command_output, reasoning_json, posture_level, mode_key, model_used, latency_ms, created_at) "
            "VALUES (?, ?, 'user', ?, '', ?, '', '{}', ?, ?, ?, 0.0, ?)",
            (
                conversation_id,
                project_slug,
                user_query,
                str(cmd_res.get("command") or ""),
                posture.get("color_level", "RED"),
                mode_info["key"],
                model_id,
                now,
            ),
        )
        cur = conn.execute(
            "INSERT INTO messages (conversation_id, project_slug, role, content, thinking, command_executed, "
            "command_output, reasoning_json, posture_level, mode_key, model_used, latency_ms, created_at) "
            "VALUES (?, ?, 'assistant', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                conversation_id,
                project_slug,
                reply_content,
                thinking_content,
                str(cmd_res.get("command") or ""),
                str(cmd_res.get("output") or ""),
                json.dumps(compact_reasoning),
                posture.get("color_level", "RED"),
                mode_info["key"],
                model_id,
                total_ms,
                now,
            ),
        )
        assistant_msg_id = cur.lastrowid
        conn.commit()

    cfg_now = get_all_settings()
    llama_base = (cfg_now.get("llama_api_url") or "http://127.0.0.1:8080/v1").rstrip("/")
    llama_h = _get_llama_health(llama_base)

    return {
        "ok": True,
        "message_id": assistant_msg_id,
        "conversation_id": conversation_id,
        "project_slug": project_slug,
        "user_query": user_query,
        "reply": reply_content,
        "thinking": thinking_content,
        "command_result": cmd_res,
        "reasoning": compact_reasoning,
        "full_reasoning": reasoning_res,
        "posture": posture,
        "active_mode": mode_info,
        "model_used": model_id,
        "llm_online": llm_online,
        "llm_error": llm_error,
        "llama_server": {
            "online": bool(llama_h.get("online")),
            "state": str(llama_h.get("state") or ("ok" if llama_h.get("online") else "offline")),
            "api_url": llama_base,
            "active_model": str(llama_h.get("active_model") or model_id),
            "last_error": _LLAMA_LAST_ERROR,
        },
        "latency_ms": total_ms,
        "created_at": now,
        "files": list_project_files(project_slug),
    }


@app.post("/api/command/execute")
async def api_execute_command(req: CommandExecuteRequest) -> Dict[str, Any]:
    cfg = get_all_settings()
    proj_slug = resolve_active_project_slug(req.project_slug, cfg=cfg)
    if not proj_slug:
        raise HTTPException(status_code=400, detail="Please select or create a project first.")
    mode_key = cfg.get("session_mode", "default").lower()
    mode_info = SESSION_MODES.get(mode_key, SESSION_MODES["default"])
    iso_level = cfg.get("isolation_level", "red").lower()
    if mode_info["forced_isolation"]:
        iso_level = mode_info["forced_isolation"]
    ifaces = cfg.get("allowed_interfaces", "eth0,eth1")
    override_str = f"blue:{ifaces}" if iso_level == "blue" else iso_level
    posture = _get_cached_posture(override_str)

    res = await asyncio.to_thread(
        execute_safe_shell_command,
        req.command,
        mode_info,
        posture,
        proj_slug,
    )
    return res


@app.post("/api/reports/generate")
async def api_generate_report(req: ReportGenerateRequest) -> Dict[str, Any]:
    cfg = get_all_settings()
    proj_slug = resolve_active_project_slug(req.project_slug, cfg=cfg)
    if not proj_slug:
        raise HTTPException(status_code=400, detail="Please select or create a project first.")
    rep = await asyncio.to_thread(
        generate_project_report,
        project_name=proj_slug,
        report_focus=req.focus or "",
        use_llm=req.use_llm,
    )
    return {
        "ok": True,
        "report": rep,
        "files": list_project_files(proj_slug),
    }


@app.get("/api/tools")
async def api_get_system_tools() -> Dict[str, Any]:
    return await asyncio.to_thread(get_system_tools_inventory)


@app.post("/api/tools/sync")
async def api_sync_system_tools(req: ToolSyncRequest) -> Dict[str, Any]:
    return await asyncio.to_thread(download_missing_tools, tool_ids=req.tool_ids)


@app.delete("/api/messages/{project_slug}")
async def api_clear_project_messages(project_slug: str) -> Dict[str, Any]:
    slug = slugify(project_slug)
    with get_db_conn() as conn:
        conn.execute("DELETE FROM messages WHERE project_slug = ?", (slug,))
        conn.commit()
    return {"ok": True, "project_slug": slug}


# ---------------------------------------------------------------------------
# WebSocket Live Hardware Telemetry & Posture Stream (`/ws/metrics`)
# ---------------------------------------------------------------------------
@app.websocket("/ws/metrics")
async def websocket_hardware_metrics(ws: WebSocket) -> None:
    await ws.accept()
    try:
        while True:
            cfg = get_all_settings()
            mode_key = cfg.get("session_mode", "default").lower()
            mode_info = SESSION_MODES.get(mode_key, SESSION_MODES["default"])
            iso_level = cfg.get("isolation_level", "red").lower()
            if mode_info["forced_isolation"]:
                iso_level = mode_info["forced_isolation"]
            ifaces = cfg.get("allowed_interfaces", "eth0,eth1")
            override_str = f"blue:{ifaces}" if iso_level == "blue" else iso_level
            llama_base = (cfg.get("llama_api_url") or "http://127.0.0.1:8080/v1").rstrip("/")
            llama_h, hw_data = await asyncio.gather(
                asyncio.to_thread(_get_llama_health, llama_base),
                asyncio.to_thread(collect_hardware_metrics),
            )
            payload = {
                "type": "telemetry",
                "hardware": hw_data,
                "posture": _get_cached_posture(override_str),
                "active_project": resolve_active_project_slug(cfg=cfg),
                "session_mode": mode_key,
                "llama_server": {
                    "online": bool(llama_h.get("online")),
                    "state": str(llama_h.get("state") or ("ok" if llama_h.get("online") else "offline")),
                    "api_url": llama_base,
                    "active_model": str(llama_h.get("active_model") or ""),
                    "last_error": _LLAMA_LAST_ERROR,
                },
            }
            await ws.send_json(payload)
            await asyncio.sleep(1.5)
    except WebSocketDisconnect:
        return
    except Exception:
        return


# ---------------------------------------------------------------------------
# Serve Compiled Svelte + TypeScript + Tailwind CSS Frontend (`frontend/dist`)
# ---------------------------------------------------------------------------
if (FRONTEND_DIST_DIR / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST_DIR / "assets")), name="frontend_assets")


@app.get("/{full_path:path}")
async def serve_spa_frontend(full_path: str) -> Any:
    if full_path.startswith("api/") or full_path.startswith("ws/"):
        raise HTTPException(status_code=404, detail="Endpoint not found.")
    no_cache_headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }
    if FRONTEND_DIST_DIR.is_dir():
        candidate = (FRONTEND_DIST_DIR / full_path).resolve()
        if full_path and candidate.is_file() and str(candidate).startswith(str(FRONTEND_DIST_DIR.resolve())):
            return FileResponse(str(candidate), headers=no_cache_headers)
        # If browser has a stale cached index.html referencing an older hashed asset in /assets/,
        # serve the current built JS/CSS bundle instead of falling back to index.html
        if full_path.startswith("assets/"):
            assets_dir = FRONTEND_DIST_DIR / "assets"
            if full_path.endswith(".js"):
                js_files = sorted(assets_dir.glob("index-*.js"))
                if js_files:
                    return FileResponse(str(js_files[-1]), media_type="application/javascript", headers=no_cache_headers)
            elif full_path.endswith(".css"):
                css_files = sorted(assets_dir.glob("index-*.css"))
                if css_files:
                    return FileResponse(str(css_files[-1]), media_type="text/css", headers=no_cache_headers)
        index_html = FRONTEND_DIST_DIR / "index.html"
        if index_html.is_file():
            return FileResponse(str(index_html), headers=no_cache_headers)
    return HTMLResponse(
        content=(
            "<html><body style='background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:2rem;'>"
            "<h2>CORA Custom WebUI Backend is Online</h2>"
            "<p>Run <code>npm run build</code> inside <code>core/webui/frontend</code> to build the Svelte + TypeScript + Tailwind CSS UI.</p>"
            "</body></html>"
        ),
        status_code=200,
        headers=no_cache_headers,
    )


def _ensure_single_webui_on_port(host: str, port: int) -> None:
    """
    Guarantee that only a single CORA WebUI server instance is running and that
    it binds strictly to `port` (default `1337`). Terminates any prior `webui/server.py`
    process holding the port and records the active PID in `core/Log/webui.pid`.
    """
    my_pid = os.getpid()
    my_ppid = os.getppid()
    killed_any = False
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            pid = proc.info.get("pid")
            if not pid or pid in (my_pid, my_ppid):
                continue
            pname = (proc.info.get("name") or "").lower()
            if "python" not in pname:
                continue
            cmdline = " ".join(proc.cmdline() or []).lower().replace("\\", "/")
            if "webui/server.py" in cmdline:
                proc.terminate()
                killed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if killed_any:
        for _ in range(15):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((host, port))
                    break
            except OSError:
                time.sleep(0.2)

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        (LOG_DIR / "webui.pid").write_text(f"{my_pid}\n", encoding="ascii")
    except Exception:
        pass


def main() -> None:
    default_port = int(os.environ.get("CORA_WEBUI_PORT") or os.environ.get("WEBUI_PORT") or "1337")
    parser = argparse.ArgumentParser(description="Start the C.O.R.A. Custom WebUI Backend (FastAPI + WebSockets + SQLite + NVML).")
    parser.add_argument("--host", default=os.environ.get("CORA_WEBUI_HOST", "127.0.0.1"), help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=default_port, help="Bind port (strictly 1337 by default)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()

    if not args.reload:
        _ensure_single_webui_on_port(args.host, args.port)

    import uvicorn

    uvicorn.run(
        "server:app" if args.reload else app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
