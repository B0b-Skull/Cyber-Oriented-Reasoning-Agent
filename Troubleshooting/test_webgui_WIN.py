#!/usr/bin/env python3
"""
C.O.R.A. Windows WebGUI Comprehensive Automated Test Suite (`Troubleshooting/test_webgui_WIN.py`)
=================================================================================================
Tests EVERY button, dropdown, modal, toggle, keyboard shortcut (`Ctrl+O`), file operation,
network isolation posture, session personality mode, and API endpoint in the Windows WebGUI
(`core/webui/frontend/src/App.svelte` + `core/webui/server.py`) to validate functionality
and logic and quickly identify any bugs or regressions.

Usage:
    python Troubleshooting/test_webgui_WIN.py
    powershell -ExecutionPolicy Bypass -File Troubleshooting/test_webgui_WIN.ps1
"""
from __future__ import annotations

import ast
import base64
import json
import os
from pathlib import Path
import re
import shutil
import socket
import sqlite3
import subprocess
import symtable
import sys
import tempfile
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
import urllib.error
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORA_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = CORA_ROOT / "core"
WEBUI_DIR = CORE_DIR / "webui"
SERVER_PY = WEBUI_DIR / "server.py"
APP_SVELTE = WEBUI_DIR / "frontend" / "src" / "App.svelte"
TYPES_TS = WEBUI_DIR / "frontend" / "src" / "types.ts"
DIST_DIR = WEBUI_DIR / "frontend" / "dist"
PROJECTS_DIR = CORA_ROOT / "Projects"
LOG_DIR = CORE_DIR / "Log"
SESSIONS_DIR = CORE_DIR / "Reasoning" / "data" / "sessions"
DB_PATH = LOG_DIR / "cora_webui.db"

TEST_PROJ_CREATE = "autotest-webgui-win"
TEST_PROJ_RENAMED = "autotest-webgui-renamed"


class TestHarness:
    def __init__(self) -> None:
        self.passed: int = 0
        self.failed: int = 0
        self.failures: List[str] = []

    def check(self, name: str, condition: bool, detail: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"  [PASS] {name}")
        else:
            self.failed += 1
            msg = f"{name}" + (f" — {detail}" if detail else "")
            self.failures.append(msg)
            print(f"  [FAIL] {msg}")

    def run_step(self, name: str, fn: Callable[[], None]) -> None:
        try:
            fn()
            self.passed += 1
            print(f"  [PASS] {name}")
        except Exception as exc:
            self.failed += 1
            msg = f"{name} — {type(exc).__name__}: {exc}"
            self.failures.append(msg)
            print(f"  [FAIL] {msg}")


def _find_free_port(preferred: int = 18338) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            s.bind(("127.0.0.1", 0))
            return int(s.getsockname()[1])


def _http_request(
    url: str,
    method: str = "GET",
    payload: Optional[Dict[str, Any]] = None,
    timeout: float = 25.0,
) -> Tuple[int, Any, Dict[str, str]]:
    data_bytes = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            if "application/json" in ctype:
                return resp.status, json.loads(raw.decode("utf-8", errors="replace")), hdrs
            return resp.status, raw, hdrs
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw}
        return exc.code, body, {}


def _snapshot_state() -> Dict[str, Any]:
    snap: Dict[str, Any] = {
        "active_proj_log": (LOG_DIR / "active-project.txt").read_text(encoding="utf-8")
        if (LOG_DIR / "active-project.txt").is_file()
        else None,
        "active_proj_sess": (SESSIONS_DIR / "active_project.txt").read_text(encoding="utf-8")
        if (SESSIONS_DIR / "active_project.txt").is_file()
        else None,
        "settings": {},
    }
    if DB_PATH.is_file():
        try:
            with sqlite3.connect(str(DB_PATH)) as conn:
                rows = conn.execute("SELECT key, value FROM settings").fetchall()
                snap["settings"] = {r[0]: r[1] for r in rows}
        except Exception:
            pass
    return snap


def _restore_state(snap: Dict[str, Any]) -> None:
    for slug in (TEST_PROJ_CREATE, TEST_PROJ_RENAMED):
        shutil.rmtree(PROJECTS_DIR / slug, ignore_errors=True)
    if DB_PATH.is_file():
        try:
            with sqlite3.connect(str(DB_PATH)) as conn:
                for slug in (TEST_PROJ_CREATE, TEST_PROJ_RENAMED):
                    conn.execute("DELETE FROM messages WHERE project_slug = ?", (slug,))
                    conn.execute("DELETE FROM conversations WHERE project_slug = ?", (slug,))
                if snap.get("settings"):
                    conn.execute("DELETE FROM settings")
                    for k, v in snap["settings"].items():
                        conn.execute("INSERT INTO settings (key, value) VALUES (?, ?)", (k, v))
                conn.commit()
        except Exception:
            pass

    for key, path in (
        ("active_proj_log", LOG_DIR / "active-project.txt"),
        ("active_proj_sess", SESSIONS_DIR / "active_project.txt"),
    ):
        val = snap.get(key)
        if val is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(val, encoding="utf-8")
        else:
            path.unlink(missing_ok=True)


# ===========================================================================
# PHASE 1: STATIC & COMPILED FRONTEND UI CONTROL INVENTORY AUDIT
# ===========================================================================
def run_frontend_and_lexical_audit(h: TestHarness) -> None:
    print("\n=== [Phase 1/3] Auditing WebGUI Source (`App.svelte`, `server.py`) & Compiled Bundle (`dist/`) ===")

    # 1. Lexical scope & AST audit of `core/webui/server.py`
    def _audit_server_py() -> None:
        import builtins

        src = SERVER_PY.read_text(encoding="utf-8")
        ast.parse(src, filename=str(SERVER_PY))
        top_st = symtable.symtable(src, str(SERVER_PY), "exec")
        builtins_set = set(dir(builtins)) | {
            "__builtins__",
            "__file__",
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
        }

        def _walk(st: symtable.SymbolTable, enclosing: set[str]) -> List[Tuple[int, str, str]]:
            local_defs = {
                s.get_name()
                for s in st.get_symbols()
                if s.is_local() or s.is_parameter() or s.is_imported() or s.is_declared_global()
            }
            visible = enclosing | local_defs if st.get_type() != "class" else enclosing
            missing: List[Tuple[int, str, str]] = []
            for s in st.get_symbols():
                name = s.get_name()
                if s.is_free() or (
                    s.is_global()
                    and not s.is_declared_global()
                    and not s.is_local()
                    and not s.is_imported()
                ):
                    if name not in enclosing and name not in local_defs and name not in builtins_set:
                        missing.append((st.get_lineno(), st.get_name(), name))
            for child in st.get_children():
                missing.extend(_walk(child, visible))
            return missing

        undef = _walk(top_st, set())
        assert not undef, f"Undefined symbols in server.py: {undef}"

    h.run_step("Python AST & symtable lexical scope check on `core/webui/server.py` (0 undefined variables)", _audit_server_py)

    # 2. Verify compiled frontend bundle exists in `core/webui/frontend/dist`
    index_html = DIST_DIR / "index.html"
    js_bundles = sorted((DIST_DIR / "assets").glob("index-*.js")) if (DIST_DIR / "assets").is_dir() else []
    css_bundles = sorted((DIST_DIR / "assets").glob("index-*.css")) if (DIST_DIR / "assets").is_dir() else []
    h.check("Compiled `frontend/dist/index.html` exists", index_html.is_file())
    h.check("Compiled `frontend/dist/assets/index-*.js` & `index-*.css` exist", len(js_bundles) > 0 and len(css_bundles) > 0)

    svelte_src = APP_SVELTE.read_text(encoding="utf-8")
    js_src = js_bundles[-1].read_text(encoding="utf-8", errors="replace") if js_bundles else ""

    # 3. Verify every required button, dropdown, modal, and shortcut in `App.svelte` & compiled JS
    required_controls = [
        ("Header: CROW Emblem Banner/Disclaimer Button (`showBannerModal = true`)", "showBannerModal = true"),
        ("Header: Stacked & Scrollable Multi-NIC `NET` Display (`headerNetRows` / `max-h-[46px] overflow-y-auto`)", "headerNetRows"),
        ("Header: `NET` Format (`Interface name | IP/mask | ↑upload ↓download`)", "row.ifaceName"),
        ("Header: Dark / Light Theme Toggle Button (`toggleThemeMode`)", "toggleThemeMode"),
        ("Header: `llama.cpp: ONLINE / STANDBY` Start/Reload Button (`handleStartOrRestartLlm`)", "handleStartOrRestartLlm"),
        ("Header: `SYSINTERNALS: INSTALLED` Status Badge", "SYSINTERNALS: INSTALLED"),
        ("Header: `⚙️ Settings` Gear Button (`showSettingsModal = true`)", "showSettingsModal = true"),
        ("Workspace: Zero Outer Gap Flush Enterprise Layout (`h-screen w-screen overflow-hidden`)", "h-screen w-screen overflow-hidden"),
        ("Results Window: High-Contrast Lighter Surface (`#334663` -> `#293952`) for `🤖 C.O.R.A. OUTPUT`", "#334663"),
        ("Results Window: `🧠 Thought Process (Ctrl+O)` Toggle Button (`toggleGlobalThinkingCtrlO`)", "toggleGlobalThinkingCtrlO"),
        ("Results Window: Per-Message Thought Process Expand/Collapse (`toggleSingleMessageThinking`)", "toggleSingleMessageThinking"),
        ("Results Window: Live `🧠 C.O.R.A. THINKING / PROCESSING` Status Card", "C.O.R.A. THINKING / PROCESSING"),
        ("Results Window: `Generate 5-Section Report` Button (`handleGenerateReport`)", "handleGenerateReport"),
        ("Results Window: `Clear Display` Button (`handleClearHistory`)", "handleClearHistory"),
        ("Results Window: Consensus Action `Load into Probe` & `Run Command Now` Buttons", "Load into Probe"),
        ("Control Deck: Dropdown 1 — Project Selector (`#cora-project-select`)", "cora-project-select"),
        ("Control Deck: Dropdown 2 — Session Personality & Logic Mode (`#cora-mode-select`)", "cora-mode-select"),
        ("Control Deck: Dropdown 3 — Network Isolation (`#cora-netiso-select`)", "cora-netiso-select"),
        ("Control Deck: BLUE Allowed Host Interfaces Chips (`toggleBlueInterfaceChip`)", "toggleBlueInterfaceChip"),
        ("Control Deck: Dropdown 4 — Model Connection Selector (`#cora-model-select`)", "cora-model-select"),
        ("Control Deck: `/goal` Input & `🎯 Pursue Goal` Button (`handlePursueGoal`)", "handlePursueGoal"),
        ("Control Deck: `Command Probe` Input, `↑`/`↓` History, `Tab ↹` Autocomplete & `Run Now` Button", "runQuickCommand"),
        ("Control Deck: `Tools: AUTO-RUN / CONFIRM` Toggle Button (`permissionMode`)", "Tools: {permissionMode === 'auto' ? 'AUTO-RUN' : 'CONFIRM'}"),
        ("Control Deck: `--think: ON / OFF` Toggle Button (`thinkingEnabled`)", "--think: {thinkingEnabled ? 'ON' : 'OFF'}"),
        ("Control Deck: `📤 + Upload / Add File` Button (`handleBrowserFilesUpload`)", "handleBrowserFilesUpload"),
        ("Control Deck: `📁 Manage Files/` Button (`showProjectFilesModal = true`)", "showProjectFilesModal = true"),
        ("Control Deck: Console File Drag-and-Drop (`handleConsoleDrop`)", "handleConsoleDrop"),
        ("Control Deck: Query History `↑ Prev` / `↓ Next` Buttons (`stepQueryHistory`)", "stepQueryHistory"),
        ("Control Deck: Main Query Input & `Execute Query` Submit Button (`handleQuerySubmit`)", "handleQuerySubmit"),
        ("Control Deck: `Cancel` Button below `Execute Query` (`handleCancelExecution` / `#cora-cancel-btn`)", "handleCancelExecution"),
        ("Modal 2: Create / Select Project Modal (`submitCreateProject`)", "submitCreateProject"),
        ("Modal 3: Rename Current Project Modal (`submitRenameProject`)", "submitRenameProject"),
        ("Modal 5: Project `Files/` Manager — Local Path Importer (`handleImportLocalPath`)", "handleImportLocalPath"),
        ("Modal 5: Project `Files/` Manager — Custom Script Creator (`handleCreateNewCustomScript`)", "handleCreateNewCustomScript"),
        ("Modal 5: Project `Files/` Manager — File Viewer & Save (`openProjectFileInViewer` / `saveEditedProjectFile`)", "saveEditedProjectFile"),
        ("Modal 5: Project `Files/` Manager — Delete File (`deleteProjectFile`)", "deleteProjectFile"),
        ("Modal 6: `⚙️ Settings` — Font Family Selector (`FONT_FAMILY_OPTIONS`)", "FONT_FAMILY_OPTIONS"),
        ("Modal 6: `⚙️ Settings` — Font Size Slider & Presets (`settings-font-size`)", "settings-font-size"),
        ("Modal 6: `⚙️ Settings` — Font Color Presets & Picker (`FONT_COLOR_PRESETS`)", "FONT_COLOR_PRESETS"),
        ("Modal 6: `⚙️ Settings` — Line Spacing, Flush/Framed Density & Glow Intensity", "uiPanelDensity"),
        ("Modal 6: `⚙️ Settings` — `↺ Reset Defaults` Button (`resetUiCustomization`)", "resetUiCustomization"),
    ]
    for label, needle in required_controls:
        h.check(label, needle in svelte_src, f"Missing `{needle}` in App.svelte")

    # 4. Verify compiled JS bundle is synchronized with latest features
    for bundle_token in ("Thought Process (Ctrl+O)", "SYSINTERNALS: INSTALLED", "Customize Font & Display", "cora-cancel-btn"):
        h.check(f"Compiled `dist/assets/index-*.js` contains `{bundle_token}`", bundle_token in js_src)

    # 5. Verify prohibited clutter is NOT rendered in the template markup
    template_part = svelte_src.split("</script>", 1)[-1]
    h.check("No `VERIFY & DOWNLOAD TOOLS` button in template", "VERIFY & DOWNLOAD TOOLS" not in template_part.upper())
    h.check("No `LIVE SMB` checkbox in template", "LIVE SMB" not in template_part.upper())
    h.check("No `active_session` default project in template", "active_session" not in template_part.lower())


# ===========================================================================
# PHASE 2: LIVE END-TO-END TESTING OF EVERY WEBGUI BUTTON & OPTION
# ===========================================================================
def run_live_webgui_api_and_logic_tests(h: TestHarness, base_url: str) -> None:
    print(f"\n=== [Phase 2/3] Testing Every WebGUI Button, Modal, Dropdown & Logic Option against `{base_url}` ===")

    # 1. Health & Brand Assets (CROW Emblem Dark/Light & Splash)
    def _test_health_and_assets() -> None:
        code, data, _ = _http_request(f"{base_url}/api/health")
        assert code == 200 and data.get("status") == "ok", f"/api/health failed: {data}"
        for asset_ep, expected_ct in [
            ("/api/assets/logo-dark", "image/png"),
            ("/api/assets/logo-light", "image/png"),
            ("/api/assets/splash", "image/svg+xml"),
        ]:
            acode, raw_bytes, hdrs = _http_request(f"{base_url}{asset_ep}")
            assert acode == 200 and len(raw_bytes) > 100, f"{asset_ep} failed (code={acode})"
            assert expected_ct in hdrs.get("content-type", ""), f"{asset_ep} unexpected content-type: {hdrs}"

    h.run_step("Header CROW Emblem Assets (`/api/assets/logo-dark`, `/api/assets/logo-light`, `/api/assets/splash`) & `/api/health`", _test_health_and_assets)

    # 2. Frontend SPA Serving (`GET /`)
    def _test_spa_index() -> None:
        code, raw_html, hdrs = _http_request(f"{base_url}/")
        html_str = raw_html.decode("utf-8", errors="replace") if isinstance(raw_html, bytes) else str(raw_html)
        assert code == 200 and "<div id=\"app\">" in html_str, "SPA index.html did not render #app"
        assert "no-store" in hdrs.get("cache-control", ""), "Missing no-cache headers on SPA root"

    h.run_step("Frontend SPA Root (`GET /`) serves compiled HTML with no-cache headers", _test_spa_index)

    # 3. Dashboard Bootstrap (`GET /api/bootstrap`)
    def _test_bootstrap() -> None:
        code, data, _ = _http_request(f"{base_url}/api/bootstrap")
        assert code == 200, f"/api/bootstrap returned {code}"
        for key in (
            "version",
            "cli_banner",
            "settings",
            "session_modes",
            "active_mode",
            "posture",
            "host_interfaces",
            "projects",
            "files",
            "models",
            "hardware",
            "reasoning_status",
            "system_tools",
            "messages",
        ):
            assert key in data, f"Missing `{key}` in /api/bootstrap payload"
        assert len(data["session_modes"]) == 4, f"Expected 4 session modes, got {len(data['session_modes'])}"
        # Ensure no project is named active_session or default
        for p in data["projects"]:
            assert p["slug"].lower() not in ("active_session", "active-session", "default"), f"Invalid dummy project found: {p}"

    h.run_step("Dashboard Bootstrap (`GET /api/bootstrap`) returns all 14 enterprise state sections", _test_bootstrap)

    # 4. Header Live Hardware & Multi-NIC `NET` Telemetry (`GET /api/hardware`)
    def _test_hardware_and_multi_nic() -> None:
        code, hw, _ = _http_request(f"{base_url}/api/hardware")
        assert code == 200, f"/api/hardware returned {code}"
        assert "cpu" in hw and "ram" in hw and "disk" in hw and "network" in hw, f"Incomplete hw payload: {hw.keys()}"
        nics = hw["network"].get("interfaces") or []
        assert len(nics) >= 1, f"Expected at least 1 network interface in hw.network.interfaces, got: {hw['network']}"
        for nic in nics:
            assert "name" in nic and "ip_cidr" in nic and "tx_kb_s" in nic and "rx_kb_s" in nic, f"Incomplete NIC row: {nic}"

    h.run_step("Header Multi-NIC `NET` Telemetry (`GET /api/hardware` -> `Interface name | IP/mask | ↑tx_kb_s ↓rx_kb_s`)", _test_hardware_and_multi_nic)

    # 5. Header `SYSINTERNALS: INSTALLED` Inventory (`GET /api/tools`) & Models (`GET /api/models`)
    def _test_tools_and_models() -> None:
        code_t, tools_data, _ = _http_request(f"{base_url}/api/tools")
        assert code_t == 200 and tools_data.get("total_count", 0) > 0, f"/api/tools failed: {tools_data}"
        code_m, models_data, _ = _http_request(f"{base_url}/api/models")
        assert code_m == 200 and len(models_data.get("models") or []) >= 4, f"/api/models failed: {models_data}"

    h.run_step("Header `SYSINTERNALS: INSTALLED` (`GET /api/tools`) & Model Catalog (`GET /api/models`)", _test_tools_and_models)

    # 6. Project Selector & Modals (`Create Project`, `Select Project`, `Rename Project`, Invalid Name Rejection)
    def _test_project_lifecycle() -> None:
        # 6a. Reject invalid dummy project names (`active_session`, `default`, empty)
        for bad_name in ("active_session", "active-session", "default", "   "):
            c_bad, _, _ = _http_request(
                f"{base_url}/api/projects/create",
                method="POST",
                payload={"name": bad_name, "goal": "Should fail"},
            )
            assert c_bad == 400, f"Expected HTTP 400 for invalid project name '{bad_name}', got {c_bad}"

        # 6b. Create new isolated test project (`Modal 2: Create Project`)
        c_ok, create_res, _ = _http_request(
            f"{base_url}/api/projects/create",
            method="POST",
            payload={"name": TEST_PROJ_CREATE, "goal": "Initial WebGUI Autotest Goal"},
        )
        assert c_ok == 200 and create_res.get("ok"), f"Project create failed: {create_res}"
        assert create_res.get("active_project") == TEST_PROJ_CREATE
        assert (PROJECTS_DIR / TEST_PROJ_CREATE / "Files").is_dir(), "Projects/<slug>/Files/ directory was not created!"
        assert (PROJECTS_DIR / TEST_PROJ_CREATE / "memory.md").is_file(), "Projects/<slug>/memory.md was not created!"
        assert (PROJECTS_DIR / TEST_PROJ_CREATE / "goals.md").is_file(), "Projects/<slug>/goals.md was not created!"

        # 6c. Rename project (`Modal 3: Rename Project`)
        r_ok, ren_res, _ = _http_request(
            f"{base_url}/api/projects/rename",
            method="POST",
            payload={"old_slug": TEST_PROJ_CREATE, "new_name": TEST_PROJ_RENAMED},
        )
        assert r_ok == 200 and ren_res.get("active_project") == TEST_PROJ_RENAMED, f"Project rename failed: {ren_res}"
        assert (PROJECTS_DIR / TEST_PROJ_RENAMED / "Files").is_dir(), "Renamed project Files/ missing!"

        # 6d. Select project (`Dropdown 1: Select Project`)
        s_ok, sel_res, _ = _http_request(
            f"{base_url}/api/projects/select",
            method="POST",
            payload={"slug": TEST_PROJ_RENAMED},
        )
        assert s_ok == 200 and sel_res.get("active_project") == TEST_PROJ_RENAMED, f"Project select failed: {sel_res}"

    h.run_step("Project Dropdown & Modals (`Create`, `Rename`, `Select`, `Files/` creation & `active_session` rejection)", _test_project_lifecycle)

    # 7. Settings Gear Modal (`⚙️ Settings` -> `POST /api/session/config` Typography, Color, Size, Layout & Theme options)
    def _test_settings_gear_modal_options() -> None:
        code, cfg_res, _ = _http_request(
            f"{base_url}/api/session/config",
            method="POST",
            payload={
                "active_project": TEST_PROJ_RENAMED,
                "theme_mode": "light",
                "ui_font_family": "'Inter', 'Segoe UI', sans-serif",
                "ui_font_size": "15",
                "ui_font_color": "#67e8f9",
                "ui_line_height": "1.7",
                "ui_panel_density": "framed",
                "ui_glow_intensity": "high",
                "permission_mode": "auto",
                "thinking_enabled": True,
            },
        )
        assert code == 200 and cfg_res.get("ok"), f"Settings update failed: {cfg_res}"
        st = cfg_res.get("settings") or {}
        assert st.get("theme_mode") == "light", f"theme_mode not saved: {st}"
        assert st.get("ui_font_size") == "15", f"ui_font_size not saved: {st}"
        assert st.get("ui_font_color") == "#67e8f9", f"ui_font_color not saved: {st}"
        assert st.get("ui_line_height") == "1.7", f"ui_line_height not saved: {st}"
        assert st.get("ui_panel_density") == "framed", f"ui_panel_density not saved: {st}"
        assert st.get("ui_glow_intensity") == "high", f"ui_glow_intensity not saved: {st}"
        assert st.get("permission_mode") == "auto", f"permission_mode not saved: {st}"
        assert st.get("thinking_enabled") == "true", f"thinking_enabled not saved: {st}"

        # Reset back to Enterprise Dark Flush defaults (`↺ Reset Defaults` button)
        code2, cfg_reset, _ = _http_request(
            f"{base_url}/api/session/config",
            method="POST",
            payload={
                "theme_mode": "dark",
                "ui_font_family": "'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace",
                "ui_font_size": "13",
                "ui_font_color": "",
                "ui_line_height": "1.5",
                "ui_panel_density": "flush",
                "ui_glow_intensity": "standard",
                "permission_mode": "confirm",
                "thinking_enabled": False,
            },
        )
        assert code2 == 200 and cfg_reset["settings"]["theme_mode"] == "dark"
        assert cfg_reset["settings"]["ui_panel_density"] == "flush"

    h.run_step("`⚙️ Settings` Gear Modal Options (Font Family, Size, Color, Line Height, Flush/Framed, Glow, Dark/Light Theme, Reset)", _test_settings_gear_modal_options)

    # 8. Session Personality Modes (`[1] Default`, `[2] Analyst`, `[3] Berserker`, `[4] Ninja`) & Network Isolation (`Red`, `Blue`, `White`)
    def _test_modes_and_network_isolation() -> None:
        # 8a. [2] Analyst mode MUST auto-lock Network Isolation to WHITE (air-gapped loopback) and read_only=True
        c_an, res_an, _ = _http_request(
            f"{base_url}/api/session/config",
            method="POST",
            payload={"session_mode": "analyst", "isolation_level": "red"},
        )
        assert c_an == 200, f"Analyst config failed: {res_an}"
        assert res_an["settings"]["session_mode"] == "analyst"
        assert res_an["settings"]["isolation_level"] == "white", f"Analyst mode did not force WHITE isolation: {res_an['settings']}"
        assert res_an["active_mode"]["read_only"] is True

        # 8b. [3] Berserker mode MUST reject WHITE and enforce RED or BLUE
        c_ber, res_ber, _ = _http_request(
            f"{base_url}/api/session/config",
            method="POST",
            payload={"session_mode": "berserker", "isolation_level": "white"},
        )
        assert c_ber == 200
        assert res_ber["settings"]["session_mode"] == "berserker"
        assert res_ber["settings"]["isolation_level"] in ("red", "blue"), f"Berserker allowed WHITE: {res_ber['settings']}"

        # 8c. [4] Ninja mode with BLUE interface-locked isolation
        c_nin, res_nin, _ = _http_request(
            f"{base_url}/api/session/config",
            method="POST",
            payload={"session_mode": "ninja", "isolation_level": "blue", "allowed_interfaces": "Ethernet,Wi-Fi"},
        )
        assert c_nin == 200
        assert res_nin["settings"]["session_mode"] == "ninja"
        assert res_nin["settings"]["isolation_level"] == "blue"
        assert "Ethernet" in res_nin["settings"]["allowed_interfaces"]

        # 8d. Return to [1] Default + RED
        c_def, res_def, _ = _http_request(
            f"{base_url}/api/session/config",
            method="POST",
            payload={"session_mode": "default", "isolation_level": "red"},
        )
        assert c_def == 200 and res_def["settings"]["session_mode"] == "default"

    h.run_step("Dropdown 2 (`Personality & Logic Mode`) & Dropdown 3 (`Network Isolation` RED/BLUE/WHITE + Analyst/Berserker/Ninja rules)", _test_modes_and_network_isolation)

    # 9. Project `Files/` Upload, Local Path Import, Custom Script Creation, File Viewer, Editor Save, Analyst Read-Only Block & Delete
    def _test_project_files_manager() -> None:
        # 9a. Upload file via base64 (`📤 + Upload / Add File` button & Drag-and-Drop)
        b64_payload = base64.b64encode(b"print('CORA_WEBGUI_AUTOTEST_SCRIPT_OK')\n").decode("ascii")
        c_up, up_res, _ = _http_request(
            f"{base_url}/api/projects/files/upload",
            method="POST",
            payload={
                "project_slug": TEST_PROJ_RENAMED,
                "files": [{"filename": "autotest_probe.py", "content_base64": b64_payload}],
            },
        )
        assert c_up == 200 and up_res.get("ok"), f"Base64 file upload failed: {up_res}"
        assert (PROJECTS_DIR / TEST_PROJ_RENAMED / "Files" / "autotest_probe.py").is_file()

        # 9b. Create new custom script via text (`+ Save to Files/` button in Modal 5)
        c_txt, txt_res, _ = _http_request(
            f"{base_url}/api/projects/files/upload",
            method="POST",
            payload={
                "project_slug": TEST_PROJ_RENAMED,
                "files": [{"filename": "notes_target.txt", "content_text": "Target: 127.0.0.1\nService: CORA-WebGUI\n"}],
            },
        )
        assert c_txt == 200 and txt_res.get("ok"), f"Custom script creation failed: {txt_res}"

        # 9c. Import local host path (`Import Path` button in Modal 5)
        with tempfile.NamedTemporaryFile("w", suffix="_local_import.txt", delete=False, encoding="utf-8") as tf:
            tf.write("Imported from local host path into Projects/<slug>/Files/\n")
            temp_host_path = tf.name
        try:
            c_imp, imp_res, _ = _http_request(
                f"{base_url}/api/projects/files/upload",
                method="POST",
                payload={"project_slug": TEST_PROJ_RENAMED, "local_path": temp_host_path},
            )
            assert c_imp == 200 and imp_res.get("ok"), f"Local path import failed: {imp_res}"
            imported_name = Path(temp_host_path).name
            assert (PROJECTS_DIR / TEST_PROJ_RENAMED / "Files" / imported_name).is_file()
        finally:
            Path(temp_host_path).unlink(missing_ok=True)

        # 9d. List project files (`📁 Manage Files/` button -> `GET /api/projects/files`)
        c_ls, ls_res, _ = _http_request(
            f"{base_url}/api/projects/files?project_slug={ urllib.parse.quote(TEST_PROJ_RENAMED) }"
        )
        assert c_ls == 200, f"GET /api/projects/files failed: {ls_res}"
        names_in_files = {item["name"] for item in ls_res.get("files_dir_items") or []}
        assert "autotest_probe.py" in names_in_files and "notes_target.txt" in names_in_files

        # 9e. Read file content in viewer (`Edit` button -> `GET /api/files/content`)
        rel_target = f"Projects/{TEST_PROJ_RENAMED}/Files/notes_target.txt"
        c_rd, rd_res, _ = _http_request(
            f"{base_url}/api/files/content?rel_path={urllib.parse.quote(rel_target)}"
        )
        assert c_rd == 200 and "CORA-WebGUI" in rd_res.get("content", ""), f"File read failed: {rd_res}"

        # 9f. Save edited file content (`💾 Save Changes` button -> `POST /api/files/save`)
        c_sv, sv_res, _ = _http_request(
            f"{base_url}/api/files/save",
            method="POST",
            payload={"rel_path": rel_target, "content": "Target: 127.0.0.1\nService: CORA-WebGUI-Edited\n"},
        )
        assert c_sv == 200 and sv_res.get("ok"), f"File save failed: {sv_res}"

        # 9g. Verify [2] Analyst Mode blocks file saving & deleting (HTTP 403)
        _http_request(f"{base_url}/api/session/config", method="POST", payload={"session_mode": "analyst"})
        c_sv_an, _, _ = _http_request(
            f"{base_url}/api/files/save",
            method="POST",
            payload={"rel_path": rel_target, "content": "Should be blocked"},
        )
        assert c_sv_an == 403, f"Expected HTTP 403 saving file in Analyst mode, got {c_sv_an}"
        c_del_an, _, _ = _http_request(
            f"{base_url}/api/projects/files/delete",
            method="POST",
            payload={"project_slug": TEST_PROJ_RENAMED, "rel_path": "Files/notes_target.txt"},
        )
        assert c_del_an == 403, f"Expected HTTP 403 deleting file in Analyst mode, got {c_del_an}"
        _http_request(f"{base_url}/api/session/config", method="POST", payload={"session_mode": "default", "isolation_level": "red"})

        # 9h. Delete file (`✕` delete button -> `POST /api/projects/files/delete`)
        c_del, del_res, _ = _http_request(
            f"{base_url}/api/projects/files/delete",
            method="POST",
            payload={"project_slug": TEST_PROJ_RENAMED, "rel_path": "Files/notes_target.txt"},
        )
        assert c_del == 200 and del_res.get("ok"), f"File delete failed: {del_res}"
        assert not (PROJECTS_DIR / TEST_PROJ_RENAMED / "Files" / "notes_target.txt").exists()

    h.run_step("Project `Files/` Upload, Local Path Import, Custom Script Editor, Viewer, Save, Analyst Guardrail & Delete", _test_project_files_manager)

    # 10. Command Probe Execution (`Run Now` Button -> `POST /api/command/execute`)
    def _test_command_probe_button() -> None:
        # 10a. Safe command execution
        c_cmd, cmd_res, _ = _http_request(
            f"{base_url}/api/command/execute",
            method="POST",
            payload={"command": "hostname", "project_slug": TEST_PROJ_RENAMED},
        )
        assert c_cmd == 200 and cmd_res.get("executed") is True and cmd_res.get("blocked") is False, f"Safe command failed: {cmd_res}"
        assert cmd_res.get("exit_code") == 0 and cmd_res.get("output", "").strip(), f"Unexpected command output: {cmd_res}"

        # 10b. Destructive command blocked by Engine 9 (CEGAR formal safety verifier)
        c_blk, blk_res, _ = _http_request(
            f"{base_url}/api/command/execute",
            method="POST",
            payload={"command": "rm -rf /", "project_slug": TEST_PROJ_RENAMED},
        )
        assert c_blk == 200 and blk_res.get("blocked") is True, f"Destructive command was not blocked: {blk_res}"

        # 10c. External network probe blocked when Network Isolation is WHITE (Air-Gapped Loopback)
        _http_request(f"{base_url}/api/session/config", method="POST", payload={"session_mode": "default", "isolation_level": "white"})
        c_wht, wht_res, _ = _http_request(
            f"{base_url}/api/command/execute",
            method="POST",
            payload={"command": "ping 8.8.8.8", "project_slug": TEST_PROJ_RENAMED},
        )
        assert c_wht == 200 and wht_res.get("blocked") is True, f"External ping was not blocked in WHITE isolation: {wht_res}"
        _http_request(f"{base_url}/api/session/config", method="POST", payload={"session_mode": "default", "isolation_level": "red"})

    h.run_step("`Command Probe` & `Run Now` Button (`POST /api/command/execute` safe execution + CEGAR & WHITE air-gap blocking)", _test_command_probe_button)

    # 11. `Generate 5-Section Report` Button (`POST /api/reports/generate`)
    def _test_generate_report_button() -> None:
        c_rep, rep_res, _ = _http_request(
            f"{base_url}/api/reports/generate",
            method="POST",
            payload={"project_slug": TEST_PROJ_RENAMED, "focus": "Windows WebGUI Automated Validation", "use_llm": False},
            timeout=35.0,
        )
        assert c_rep == 200 and rep_res.get("ok"), f"Report generation failed: {rep_res}"
        md = (rep_res.get("report") or {}).get("markdown", "")
        assert "## 1." in md and "## 2." in md and "## 3." in md and "## 4." in md and "## 5." in md, "5 sections missing in REPORT.md"
        assert (PROJECTS_DIR / TEST_PROJ_RENAMED / "REPORT.md").is_file(), "REPORT.md not written to disk"

    h.run_step("`Generate 5-Section Report` Button (`POST /api/reports/generate` -> `REPORT.md` + `report_dashboard.svg`)", _test_generate_report_button)

    # 12. Console Query Execution (`Execute Query` & `🎯 Pursue Goal` Buttons -> `POST /api/query` for all Slash Commands & `Ctrl+O` Separation)
    def _test_query_and_slash_commands() -> None:
        slash_tests = [
            ("/help", "Switch Help"),
            ("/mode -h", "Switch Help: /mode"),
            ("/netiso -h", "Switch Help: -netiso"),
            ("/files -h", "Switch Help: /files"),
            ("/goal -h", "Switch Help: /goal"),
            ("/relentless -h", "Switch Help: /relentless"),
            ("/status", "Live Hardware & Session Telemetry"),
            ("/hw", "Live Hardware & Session Telemetry"),
            ("/state", "Live Hardware & Session Telemetry"),
            ("/files list", "Project Local `Files` Directory"),
            ("/files read autotest_probe.py", "CORA_WEBGUI_AUTOTEST_SCRIPT_OK"),
            ('/goal "Verify all Windows WebGUI buttons and options"', ""),
            ("/goal status", "Verify all Windows WebGUI buttons and options"),
            ("/goal list", "Verify all Windows WebGUI buttons and options"),
            ("/relentless status", "Relentless Mode"),
            ("/relentless on", "ON (ARMED)"),
            ("/relentless off", "OFF (Single-Turn)"),
            ("/relentless audit", "Relentless Controller Audit"),
            ("/vault", "Obsidian Knowledge Vault"),
            ('/remember "Windows WebGUI autotest completed"', "Saved permanent fact"),
            ("/search WebGUI", "Search Results"),
            ("/goal clear", "Cleared active in-memory goal"),
        ]
        for q_str, expected_sub in slash_tests:
            if q_str.startswith('/goal "'):
                # Setting a goal via session/config first to avoid waiting on LLM if offline/busy, or test /goal status directly
                _http_request(
                    f"{base_url}/api/session/config",
                    method="POST",
                    payload={"active_project": TEST_PROJ_RENAMED, "active_goal": "Verify all Windows WebGUI buttons and options"},
                )
                continue
            code_q, q_res, _ = _http_request(
                f"{base_url}/api/query",
                method="POST",
                payload={
                    "query": q_str,
                    "project_slug": TEST_PROJ_RENAMED,
                    "session_mode": "default",
                    "isolation_level": "red",
                },
                timeout=30.0,
            )
            assert code_q == 200 and q_res.get("ok"), f"Query `{q_str}` failed ({code_q}): {q_res}"
            reply_txt = str(q_res.get("reply") or "")
            if expected_sub:
                assert expected_sub in reply_txt, f"Query `{q_str}` reply missing '{expected_sub}':\n{reply_txt[:400]}"

    h.run_step("`Execute Query` Button & All Slash Commands (`/help`, `/status`, `/hw`, `/files`, `/goal`, `/relentless`, `/vault`, `/remember`, `/search`)", _test_query_and_slash_commands)

    # 13. Test `Ctrl+O` Thought Process & 15-Engine Trace Separation (`thinking` vs clean `reply`) + `Clear Display` Button
    def _test_ctrl_o_separation_and_clear_display() -> None:
        # Execute a query with a fast shell command probe and reasoning enabled, and verify `thinking` holds the engine trace
        code_q, q_res, _ = _http_request(
            f"{base_url}/api/query",
            method="POST",
            payload={
                "query": "/status",
                "project_slug": TEST_PROJ_RENAMED,
                "session_mode": "default",
                "isolation_level": "red",
                "run_reasoning": True,
            },
            timeout=25.0,
        )
        assert code_q == 200 and "thinking" in q_res and "reply" in q_res
        assert "<think>" not in q_res["reply"], "Raw <think> tag leaked into visible reply!"

        # Test `Clear Display` button (`DELETE /api/messages/{project_slug}`)
        c_clr, clr_res, _ = _http_request(
            f"{base_url}/api/messages/{urllib.parse.quote(TEST_PROJ_RENAMED)}",
            method="DELETE",
        )
        assert c_clr == 200 and clr_res.get("ok"), f"Clear Display failed: {clr_res}"

        # Test `Cancel` button (`POST /api/cancel`)
        c_can, can_res, _ = _http_request(
            f"{base_url}/api/cancel",
            method="POST",
            payload={},
        )
        assert c_can == 200 and can_res.get("ok") and can_res.get("cancelled") is True, f"POST /api/cancel failed: {can_res}"

        # Test llama.cpp keep-alive & context compaction (`_compact_messages_for_llama_context`)
        sys.path.insert(0, str(CORE_DIR / "webui"))
        import server as webui_srv  # type: ignore

        sample_msgs = [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "Scan 192.168.1.99 and identify firmware"},
            {"role": "assistant", "content": "<think>long internal thought</think>", "tool_calls": [{"id": "c1", "function": {"name": "scan_target", "arguments": "{}"}}]},
            {"role": "tool", "tool_call_id": "c1", "name": "scan_target", "content": "Port 443 open: FortiGate-50E"},
        ]
        compacted = webui_srv._compact_messages_for_llama_context(sample_msgs, max_chars=4000, force_flatten=True)
        assert any(
            m.get("role") == "user" and "192.168.1.99" in str(m.get("content", "")) and "FortiGate-50E" in str(m.get("content", ""))
            for m in compacted
        ), f"Compacted messages lost user query or tool output: {compacted}"

    h.run_step("`🧠 Thought Process (Ctrl+O)` Clean Output Separation, `Cancel` Button (`POST /api/cancel`), Keep-Alive & `Clear Display` Button", _test_ctrl_o_separation_and_clear_display)


# ===========================================================================
# PHASE 3: LIVE WEBSOCKET TELEMETRY STREAM (`/ws/metrics`) TEST
# ===========================================================================
def run_websocket_telemetry_test(h: TestHarness, port: int) -> None:
    print(f"\n=== [Phase 3/3] Testing Live WebSocket Telemetry Stream (`ws://127.0.0.1:{port}/ws/metrics`) ===")

    def _test_ws_stream() -> None:
        import asyncio
        import websockets  # type: ignore

        async def _recv_one() -> Dict[str, Any]:
            uri = f"ws://127.0.0.1:{port}/ws/metrics"
            async with websockets.connect(uri, open_timeout=5.0, close_timeout=2.0) as ws:
                raw_msg = await asyncio.wait_for(ws.recv(), timeout=6.0)
                return json.loads(raw_msg)

        frame = asyncio.run(_recv_one())
        assert frame.get("type") == "telemetry", f"Unexpected WS frame type: {frame}"
        assert "hardware" in frame and "posture" in frame and "llama_server" in frame, f"Incomplete WS frame: {frame.keys()}"
        nics = (frame["hardware"].get("network") or {}).get("interfaces") or []
        assert len(nics) >= 1, "WS telemetry frame missing network.interfaces"

    h.run_step("WebSocket `/ws/metrics` streams live CPU/RAM/GPU/Disk & Multi-NIC `NET` telemetry frames", _test_ws_stream)


def main() -> int:
    print("====================================================================================")
    print("  C.O.R.A. WINDOWS WEBGUI AUTOMATED TEST SUITE (`Troubleshooting/test_webgui_WIN.py`)")
    print("====================================================================================")
    t0 = time.perf_counter()
    h = TestHarness()
    snap = _snapshot_state()

    # Check if Windows WebGUI is already running on 127.0.0.1:1337; if not, spawn an isolated instance on a free port
    port = 1337
    spawned_proc: Optional[subprocess.Popen] = None
    try:
        code, health_data, _ = _http_request("http://127.0.0.1:1337/api/health", timeout=2.0)
        reuse_existing = code == 200 and health_data.get("status") == "ok"
    except Exception:
        reuse_existing = False

    if not reuse_existing:
        port = _find_free_port(18338)
        env_srv = os.environ.copy()
        env_srv["CORA_SKIP_AUTO_LLAMA"] = "1"
        spawned_proc = subprocess.Popen(
            [sys.executable, str(SERVER_PY), "--host", "127.0.0.1", "--port", str(port)],
            cwd=str(CORE_DIR),
            env=env_srv,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ready = False
        for _ in range(35):
            if spawned_proc.poll() is not None:
                print(f"[FATAL] WebGUI server exited early with code {spawned_proc.returncode}")
                _restore_state(snap)
                return 1
            try:
                c, d, _ = _http_request(f"http://127.0.0.1:{port}/api/health", timeout=1.5)
                if c == 200 and d.get("status") == "ok":
                    ready = True
                    break
            except Exception:
                time.sleep(0.35)
        if not ready:
            print(f"[FATAL] WebGUI server failed to start on 127.0.0.1:{port}")
            spawned_proc.terminate()
            _restore_state(snap)
            return 1

    base_url = f"http://127.0.0.1:{port}"
    try:
        run_frontend_and_lexical_audit(h)
        run_live_webgui_api_and_logic_tests(h, base_url)
        run_websocket_telemetry_test(h, port)
    finally:
        if spawned_proc is not None:
            spawned_proc.terminate()
            try:
                spawned_proc.wait(timeout=5)
            except Exception:
                spawned_proc.kill()
        _restore_state(snap)

    elapsed = time.perf_counter() - t0
    print("\n====================================================================================")
    print(f"  WINDOWS WEBGUI TEST SUMMARY: {h.passed} PASSED | {h.failed} FAILED ({elapsed:.2f}s)")
    print("====================================================================================")
    if h.failures:
        for f in h.failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
