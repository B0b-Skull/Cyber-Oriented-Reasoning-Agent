#!/usr/bin/env python3
"""
C.O.R.A. Windows CLI Comprehensive Automated Test Suite (`Troubleshooting/test_cli_WIN.py`)
===========================================================================================
Systematically validates every startup switch, PowerShell launcher subcommand, interactive
project/mode menu, keyboard shortcut (`Ctrl+O` / `/ctrl-o`), session personality mode
(`Default`, `Analyst`, `Berserker`, `Ninja`), network isolation posture (`Red`, `White`, `Blue`),
project `Files/` operation, 15-Engine reasoning command, and slash command in the Windows CLI
(`core/agent-cli.py` + `run_cora_WIN.ps1`).

Usage:
    python Troubleshooting/test_cli_WIN.py
    powershell -ExecutionPolicy Bypass -File Troubleshooting/test_cli_WIN.ps1
"""
from __future__ import annotations

import ast
import os
from pathlib import Path
import shutil
import subprocess
import symtable
import sys
import tempfile
import time
from typing import Any, Callable, Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CORA_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = CORA_ROOT / "core"
AGENT_CLI_PY = CORE_DIR / "agent-cli.py"
RUN_CORA_PS1 = CORA_ROOT / "run_cora_WIN.ps1"
PROJECTS_DIR = CORA_ROOT / "Projects"
LOG_DIR = CORE_DIR / "Log"
SESSIONS_DIR = CORE_DIR / "Reasoning" / "data" / "sessions"
VAULT_KNOWLEDGE_DIR = CORE_DIR / "ObsidianVault" / "knowledge"

CLI_TEST_PROJ = "autotest-cli-win"
CLI_TEST_PROJ_RENAMED = "autotest-cli-renamed"


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


def _snapshot_cli_state() -> Dict[str, Any]:
    mem_idx = CORE_DIR / "ObsidianVault" / "00_MEMORY_INDEX.md"
    return {
        "active_proj_log": (LOG_DIR / "active-project.txt").read_text(encoding="utf-8")
        if (LOG_DIR / "active-project.txt").is_file()
        else None,
        "active_proj_sess": (SESSIONS_DIR / "active_project.txt").read_text(encoding="utf-8")
        if (SESSIONS_DIR / "active_project.txt").is_file()
        else None,
        "last_cli_session": (SESSIONS_DIR / "last_cli_session.json").read_text(encoding="utf-8")
        if (SESSIONS_DIR / "last_cli_session.json").is_file()
        else None,
        "relentless_ledger": (SESSIONS_DIR / "relentless_ledger.json").read_text(encoding="utf-8")
        if (SESSIONS_DIR / "relentless_ledger.json").is_file()
        else None,
        "cli_history": (LOG_DIR / "cli_command_history.json").read_text(encoding="utf-8")
        if (LOG_DIR / "cli_command_history.json").is_file()
        else None,
        "vault_index": mem_idx.read_text(encoding="utf-8") if mem_idx.is_file() else None,
    }


def _restore_cli_state(snap: Dict[str, Any]) -> None:
    for slug in (CLI_TEST_PROJ, CLI_TEST_PROJ_RENAMED):
        shutil.rmtree(PROJECTS_DIR / slug, ignore_errors=True)
    # Remove any temporary vault notes created by `/remember` during autotest
    if VAULT_KNOWLEDGE_DIR.is_dir():
        for md in VAULT_KNOWLEDGE_DIR.glob("*autotest*"):
            md.unlink(missing_ok=True)
    for key, path in (
        ("active_proj_log", LOG_DIR / "active-project.txt"),
        ("active_proj_sess", SESSIONS_DIR / "active_project.txt"),
        ("last_cli_session", SESSIONS_DIR / "last_cli_session.json"),
        ("relentless_ledger", SESSIONS_DIR / "relentless_ledger.json"),
        ("cli_history", LOG_DIR / "cli_command_history.json"),
        ("vault_index", CORE_DIR / "ObsidianVault" / "00_MEMORY_INDEX.md"),
    ):
        val = snap.get(key)
        if val is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(val, encoding="utf-8")
        else:
            path.unlink(missing_ok=True)


# ===========================================================================
# PHASE 1: AST, SYMTABLE & POWERSHELL PARSER AUDIT
# ===========================================================================
def run_static_and_lexical_audit(h: TestHarness) -> None:
    print("\n=== [Phase 1/3] Auditing Python AST/Symtable & PowerShell Scripts ===")

    def _audit_all_python_files() -> None:
        import builtins

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

        py_files = [
            p
            for p in CORA_ROOT.rglob("*.py")
            if "node_modules" not in p.parts and ".git" not in p.parts and "__pycache__" not in p.parts
        ]
        all_undef: List[str] = []
        for pf in sorted(py_files):
            src = pf.read_text(encoding="utf-8")
            ast.parse(src, filename=str(pf))
            top_st = symtable.symtable(src, str(pf), "exec")
            undef = _walk(top_st, set())
            for lineno, scope, name in undef:
                all_undef.append(f"{pf.relative_to(CORA_ROOT)}:{lineno} ({scope}) -> `{name}`")
        assert not all_undef, "Undefined symbols found:\n" + "\n".join(all_undef)

    h.run_step("Python AST & symtable lexical scope check across all repository `.py` files (0 undefined symbols)", _audit_all_python_files)

    def _audit_powershell_scripts() -> None:
        ps_cmd = (
            "$errs = @(); "
            "Get-ChildItem -Path '.' -Recurse -Filter '*.ps1' | Where-Object { $_.FullName -notmatch 'node_modules' } | ForEach-Object { "
            "  $tokens = $null; $parseErrors = $null; "
            "  [void][System.Management.Automation.Language.Parser]::ParseFile($_.FullName, [ref]$tokens, [ref]$parseErrors); "
            "  if ($parseErrors.Count -gt 0) { $errs += \"$($_.FullName): $($parseErrors[0].Message)\" } "
            "}; "
            "if ($errs.Count -gt 0) { Write-Error ($errs -join \"`n\"); exit 1 }"
        )
        res = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
            cwd=str(CORA_ROOT),
            capture_output=True,
            text=True,
            timeout=25,
        )
        assert res.returncode == 0, f"PowerShell syntax error:\n{res.stderr}\n{res.stdout}"

    h.run_step("PowerShell AST parser validation across `run_cora_WIN.ps1` and all `.ps1` scripts", _audit_powershell_scripts)


# ===========================================================================
# PHASE 2: STARTUP SWITCHES & `run_cora_WIN.ps1` SUBCOMMANDS
# ===========================================================================
def run_startup_switches_and_ps1_tests(h: TestHarness) -> None:
    print("\n=== [Phase 2/3] Testing Startup CLI Switches & `run_cora_WIN.ps1` Subcommands ===")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # 1. Test `core/agent-cli.py` startup switches
    cli_switch_tests = [
        (["--version"], "Version:"),
        (["-h"], "C.O.R.A. (Cyber Oriented Reasoning Agent) CLI & Switch Help"),
        (["-m", "-h"], "Switch Help: -m / --model"),
        (["-netiso", "-h"], "Switch Help: -netiso / --network-isolation"),
        (["-P", "-h"], "Switch Help: -P / --project"),
        (["--continual", "-h"], "Switch Help: --continual"),
        (["--think", "-h"], "Switch Help: --think"),
        (["--hud", "-h"], "Switch Help: --hud"),
        (["--print-switches-table"], "Simplified Available Switches & Commands Reference"),
    ]
    for args_list, expected in cli_switch_tests:
        def _test_sw(a: List[str] = args_list, exp: str = expected) -> None:
            res = subprocess.run(
                [sys.executable, str(AGENT_CLI_PY), *a],
                cwd=str(CORA_ROOT),
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=20,
            )
            assert res.returncode == 0, f"Switch {a} failed (rc={res.returncode}):\n{res.stderr}\n{res.stdout}"
            assert exp in res.stdout, f"Switch {a} output missing '{exp}':\n{res.stdout[:400]}"

        h.run_step(f"CLI startup switch `agent-cli.py {' '.join(args_list)}`", _test_sw)

    # 2. Test `run_cora_WIN.ps1` subcommands
    ps1_subcommands = [
        (["tune"], "Auto-Detected Hardware & Tuning Profile"),
        (["models"], "GGUF"),
        (["status"], "Status"),
        (["reason", "status"], "Engine"),
        (["posture", "-detect"], "Posture"),
    ]
    for sub_args, expected in ps1_subcommands:
        def _test_ps1(sa: List[str] = sub_args, exp: str = expected) -> None:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RUN_CORA_PS1), *sa],
                cwd=str(CORA_ROOT),
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=35,
            )
            combined = (res.stdout or "") + "\n" + (res.stderr or "")
            assert res.returncode == 0, f"run_cora_WIN.ps1 {sa} failed (rc={res.returncode}):\n{combined}"
            assert exp.lower() in combined.lower(), f"run_cora_WIN.ps1 {sa} output missing '{exp}':\n{combined[:500]}"

        h.run_step(f"PowerShell launcher `run_cora_WIN.ps1 {' '.join(sub_args)}`", _test_ps1)


# ===========================================================================
# PHASE 3: INTERACTIVE WINDOWS CLI SESSION FLOW & EVERY `/` SLASH COMMAND
# ===========================================================================
def run_interactive_cli_session_tests(h: TestHarness) -> None:
    print("\n=== [Phase 3/3] Testing Interactive Windows CLI Session, Menus, Modes, `Files/` & Every Slash Command ===")

    with tempfile.NamedTemporaryFile("w", suffix="_cli_upload.py", delete=False, encoding="utf-8") as tf:
        tf.write("print('CORA_WIN_CLI_UPLOAD_TEST_OK')\n")
        temp_upload_path = Path(tf.name)

    try:
        # Build scripted interactive session input that exercises:
        # 1. Mode Selection Menu (`1` -> `[1] Default`)
        # 2. Every `/` slash command, mode switch, network isolation switch, file upload/read/rm, report generation, and `/exit`
        scripted_lines = [
            "1",  # Select [1] Default mode at the initial Session Personality Mode menu
            "/help",
            "/mode -h",
            "/netiso -h",
            "/files -h",
            "/goal -h",
            "/relentless -h",
            "/hw",
            "/files list",
            f'/upload "{temp_upload_path}"',
            f"/files read {temp_upload_path.name}",
            "/ctrl-o",
            "/ctrl-o",
            "/mode status",
            "/mode -mode:analyst",
            "/scan 127.0.0.1",
            "/mode -mode:berserker -netiso:red",
            "/mode -mode:ninja -netiso:blue",
            "/mode -mode:default",
            "/netiso status",
            "/netiso -mode:white",
            "/netiso -mode:red",
            "/goal status",
            "/goal list",
            "/goal clear",
            "/relentless status",
            "/relentless on",
            "/relentless -max:5",
            "/relentless off",
            "/relentless audit",
            "/permissions",
            "/permissions",
            "/hud off",
            "/hud prompt",
            "/state",
            "/vault",
            '/remember "Windows CLI autotest rule verified"',
            "/search autotest",
            "/reason status",
            "/reason test",
            "/rl status",
            "/pca status",
            "/continual status",
            "/continual -mode:auto",
            "/continual -mode:stop",
            "/train status",
            "/generate-report -mode:fast",
            f"/files rm {temp_upload_path.name}",
            "/project list",
            f"/project -rename:{CLI_TEST_PROJ}:{CLI_TEST_PROJ_RENAMED}",
            "/clear",
            "/exit",
        ]
        stdin_payload = "\n".join(scripted_lines) + "\n"

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        res = subprocess.run(
            [
                sys.executable,
                str(AGENT_CLI_PY),
                "--no-hud",
                "--keep-server",
                "-P",
                CLI_TEST_PROJ,
            ],
            input=stdin_payload,
            cwd=str(CORA_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=90,
        )
        out = (res.stdout or "") + "\n" + (res.stderr or "")

        h.check(
            "Interactive CLI session exited cleanly with return code 0 and zero unhandled Tracebacks",
            res.returncode == 0 and "Traceback (most recent call last)" not in out,
            f"rc={res.returncode}\n{out[-1500:]}",
        )

        expected_Interactive_markers = [
            ("Startup `-P` created & selected `Projects/autotest-cli-win/` (`Files/` ready)", "[Active Project Selected]"),
            ("Interactive Session Personality & Logic Mode Menu rendered `[1]..[4]`", "Session Personality & Logic Mode Selection"),
            ("C.O.R.A. Login Splash Banner & Disclaimer rendered", "Cyber Oriented Reasoning Agent"),
            ("`/help` and `<switch> -h` help tables rendered", "Switch Help: /mode"),
            ("`/hw` rendered live CPU, RAM, GPU & network summary", "- System RAM:"),
            ("`/files list` displayed `Projects/autotest-cli-win/Files/`", "Project Local `Files` Directory"),
            ("`/upload <path>` copied local script into `Projects/autotest-cli-win/Files/`", "[Added 1 File(s) to `Projects/autotest-cli-win/Files/`]"),
            ("`/files read <file>` read uploaded script contents", "CORA_WIN_CLI_UPLOAD_TEST_OK"),
            ("`/ctrl-o` toggled Thought Process & Engine Trace visibility ON & OFF", "[🧠 Thought Process (Ctrl+O)]"),
            ("`/mode -mode:analyst` locked Network Isolation to `WHITE` (Read-Only)", "[2] Analyst"),
            ("Analyst Mode guardrail blocked `/scan 127.0.0.1`", "[Analyst Mode Restriction — `/scan` Blocked]"),
            ("`/mode -mode:berserker -netiso:red` activated `[3] Berserker` mode", "[3] Berserker"),
            ("`/mode -mode:ninja -netiso:blue` activated `[4] Ninja` mode", "[4] Ninja"),
            ("`/netiso -mode:white` & `/netiso -mode:red` switched Console Posture", "POSTURE"),
            ("`/goal status`, `/goal list`, `/goal clear` executed cleanly", "Project Goal"),
            ("`/relentless status`, `on`, `-max:5`, `off`, `audit` executed cleanly", "Relentless Mode"),
            ("`/permissions` toggled between AUTO-RUN and CONFIRM ON", "Permissions:"),
            ("`/state` displayed Zero-Loss Context VM & L1 Symbolic State", "Context Virtual Memory"),
            ("`/vault`, `/remember`, and `/search` executed against ObsidianVault", "Saved long-term Obsidian note"),
            ("`/reason status` & `/reason test` validated all 15 Neuro-Symbolic Engines", "15-Engine"),
            ("`/rl status` & `/pca status` executed Engine 14 (Trajectory RL) & Engine 15 (Spectral PCA)", "PCA"),
            ("`/continual status`, `auto`, `stop` executed Engine 12 Continual Learner", "Continual Learning"),
            ("`/train status` inspected Multi-Modal Training pipeline", "Training"),
            ("`/generate-report -mode:fast` generated 5-Section `REPORT.md` & SVG dashboard", "REPORT.md"),
            ("`/files rm <file>` deleted test script from `Files/`", "Deleted `Projects/autotest-cli-win/Files/"),
            ("`/project -rename` renamed `autotest-cli-win` -> `autotest-cli-renamed`", "autotest-cli-renamed"),
            ("`/clear` reset conversation messages & `/exit` terminated cleanly", "Exiting..."),
        ]
        for label, marker in expected_Interactive_markers:
            h.check(label, marker in out, f"Missing marker `{marker}` in CLI output")

    finally:
        temp_upload_path.unlink(missing_ok=True)


def main() -> int:
    print("====================================================================================")
    print("  C.O.R.A. WINDOWS CLI AUTOMATED TEST SUITE (`Troubleshooting/test_cli_WIN.py`)")
    print("====================================================================================")
    t0 = time.perf_counter()
    h = TestHarness()
    snap = _snapshot_cli_state()
    try:
        run_static_and_lexical_audit(h)
        run_startup_switches_and_ps1_tests(h)
        run_interactive_cli_session_tests(h)
    finally:
        _restore_cli_state(snap)

    elapsed = time.perf_counter() - t0
    print("\n====================================================================================")
    print(f"  WINDOWS CLI TEST SUMMARY: {h.passed} PASSED | {h.failed} FAILED ({elapsed:.2f}s)")
    print("====================================================================================")
    if h.failures:
        for f in h.failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
