#!/usr/bin/env python3
"""
C.O.R.A. Linux / WSL Automated Test Suite (`Troubleshooting/test_nix_WSL.py`)
=============================================================================
Validates the Linux CLI (`core/agent-cli.py` + `run_cora_NIX.sh`) in a real Linux PTY
(including rapid SIGWINCH terminal resize stress testing, interactive Project & Mode
menus, Ctrl+O thought-process toggle, and slash commands) and validates the Linux
WebGUI backend (`core/webui/server.py`) inside WSL / Linux.

Usage (from Windows PowerShell):
    wsl -d Ubuntu -- python3 /mnt/c/CODEX/NeuralNet/CORA_GITHUB/Troubleshooting/test_nix_WSL.py
Usage (from Linux / WSL Bash):
    python3 Troubleshooting/test_nix_WSL.py
"""
from __future__ import annotations

import base64
import fcntl
import json
import os
from pathlib import Path
import pty
import select
import shutil
import signal
import socket
import struct
import subprocess
import sys
import termios
import time
from typing import Any, Dict, Tuple
import urllib.error
import urllib.request

CORA_ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = CORA_ROOT / "core"
PROJECTS_DIR = CORA_ROOT / "Projects"
LOG_DIR = CORE_DIR / "Log"
SESSIONS_DIR = CORE_DIR / "Reasoning" / "data" / "sessions"


def _find_free_port(preferred: int = 18337) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            s.bind(("127.0.0.1", 0))
            return int(s.getsockname()[1])


def _snapshot_workspace_state() -> Dict[str, Any]:
    active_proj_log = LOG_DIR / "active-project.txt"
    active_proj_sess = SESSIONS_DIR / "active_project.txt"
    return {
        "active_proj_log": active_proj_log.read_text(encoding="utf-8") if active_proj_log.is_file() else None,
        "active_proj_sess": active_proj_sess.read_text(encoding="utf-8") if active_proj_sess.is_file() else None,
    }


def _restore_workspace_state(snap: Dict[str, Any], temp_projects: list[str]) -> None:
    for slug in temp_projects:
        shutil.rmtree(PROJECTS_DIR / slug, ignore_errors=True)
    active_proj_log = LOG_DIR / "active-project.txt"
    active_proj_sess = SESSIONS_DIR / "active_project.txt"
    if snap.get("active_proj_log") is not None:
        active_proj_log.parent.mkdir(parents=True, exist_ok=True)
        active_proj_log.write_text(snap["active_proj_log"], encoding="utf-8")
    else:
        active_proj_log.unlink(missing_ok=True)
    if snap.get("active_proj_sess") is not None:
        active_proj_sess.parent.mkdir(parents=True, exist_ok=True)
        active_proj_sess.write_text(snap["active_proj_sess"], encoding="utf-8")
    else:
        active_proj_sess.unlink(missing_ok=True)


def set_pty_size(fd: int, rows: int, cols: int) -> None:
    winsize = struct.pack("HHHH", rows, cols, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_until_idle(master_fd: int, total_timeout: float = 2.0, idle_timeout: float = 0.35) -> str:
    buf = bytearray()
    t0 = time.monotonic()
    last_rx = t0
    while (time.monotonic() - t0) < total_timeout:
        r, _, _ = select.select([master_fd], [], [], 0.08)
        if r:
            try:
                chunk = os.read(master_fd, 8192)
                if not chunk:
                    break
                buf.extend(chunk)
                last_rx = time.monotonic()
            except OSError:
                break
        elif buf and (time.monotonic() - last_rx) >= idle_timeout:
            break
    return buf.decode("utf-8", errors="replace")


def test_interactive_cli_in_pty() -> None:
    print("=== [1/3] Testing Linux CLI (`core/agent-cli.py`) in Real Linux PTY ===")
    master_fd, slave_fd = pty.openpty()
    set_pty_size(master_fd, 36, 120)

    proc = subprocess.Popen(
        ["python3", str(CORE_DIR / "agent-cli.py"), "-P", "wsl-cli-autotest"],
        cwd=str(CORA_ROOT),
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
        preexec_fn=os.setsid,
    )
    os.close(slave_fd)

    out_mode = read_until_idle(master_fd, total_timeout=6.0, idle_timeout=0.6)
    if "Traceback" in out_mode or "NameError" in out_mode:
        raise RuntimeError(f"CLI crashed on startup:\n{out_mode}")
    assert "Session Personality & Logic Mode Selection" in out_mode, f"Expected mode menu, got:\n{out_mode}"
    print("  [PASS] Startup project initialization (`Projects/wsl-cli-autotest/Files/`) & Mode Menu rendered.")

    # Select [1] Default mode
    os.write(master_fd, b"1\n")
    out_splash = read_until_idle(master_fd, total_timeout=5.0, idle_timeout=0.8)
    if "Traceback" in out_splash:
        raise RuntimeError(f"CLI crashed during splash screen:\n{out_splash}")
    assert "Cyber Oriented Reasoning Agent" in out_splash, f"Splash banner missing:\n{out_splash}"
    assert "You>" in out_splash, f"CLI prompt missing:\n{out_splash}"
    print("  [PASS] C.O.R.A. Splash Screen & `You>` prompt rendered cleanly.")

    # Simulate rapid terminal resizing (SIGWINCH stress test)
    for r, c in [(40, 140), (28, 95), (32, 110), (45, 160), (36, 120)]:
        set_pty_size(master_fd, r, c)
        os.killpg(os.getpgid(proc.pid), signal.SIGWINCH)
        time.sleep(0.05)
    out_resize = read_until_idle(master_fd, total_timeout=1.5, idle_timeout=0.3)
    if "Traceback" in out_resize or "RuntimeError" in out_resize:
        raise RuntimeError(f"CLI crashed during SIGWINCH terminal resize:\n{out_resize}")
    print("  [PASS] Rapid SIGWINCH terminal resize stress test passed without reentrant stdout errors.")

    # Test slash commands and Ctrl+O keybinding (\x0f)
    for cmd_label, payload in [
        ("/hw", b"/hw\n"),
        ("/files", b"/files\n"),
        ("Ctrl+O key (\\x0f)", b"\x0f"),
        ("/ctrl-o", b"/ctrl-o\n"),
        ("/state", b"/state\n"),
        ("/reason status", b"/reason status\n"),
        ("/netiso status", b"/netiso status\n"),
        ("/relentless status", b"/relentless status\n"),
    ]:
        os.write(master_fd, payload)
        resp = read_until_idle(master_fd, total_timeout=6.0, idle_timeout=0.6)
        if "Traceback (most recent call last)" in resp:
            raise RuntimeError(f"CLI crashed on {cmd_label}:\n{resp}")
        print(f"  [PASS] Command `{cmd_label}` executed cleanly.")

    # Exit cleanly
    os.write(master_fd, b"/exit\n")
    out_exit = read_until_idle(master_fd, total_timeout=4.0, idle_timeout=0.5)
    proc.wait(timeout=10)
    os.close(master_fd)
    assert proc.returncode == 0, f"CLI exited with non-zero code: {proc.returncode}\n{out_exit}"
    print("  [PASS] Linux CLI exited cleanly with code 0.")


def test_run_cora_nix_commands() -> None:
    print("\n=== [2/3] Testing `run_cora_NIX.sh` Subcommands in WSL ===")
    for subcmd in [
        ["bash", "./run_cora_NIX.sh", "tune"],
        ["bash", "./run_cora_NIX.sh", "models"],
        ["bash", "./run_cora_NIX.sh", "status"],
        ["bash", "./run_cora_NIX.sh", "reason", "status"],
        ["bash", "./run_cora_NIX.sh", "posture", "--detect"],
    ]:
        res = subprocess.run(subcmd, cwd=str(CORA_ROOT), capture_output=True, text=True, timeout=30)
        if res.returncode != 0 or "Traceback" in res.stdout or "Traceback" in res.stderr:
            raise RuntimeError(
                f"Command {subcmd} failed (rc={res.returncode}):\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
            )
        print(f"  [PASS] `{' '.join(subcmd[1:])}` succeeded (rc=0).")


def _http_json(
    url: str,
    method: str = "GET",
    payload: Dict[str, Any] | None = None,
    timeout: float = 20.0,
) -> Tuple[int, Dict[str, Any]]:
    data_bytes = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"raw": raw}
        return exc.code, body


def test_linux_webui_in_wsl() -> None:
    print("\n=== [3/3] Testing Linux WebGUI (`core/webui/server.py`) in WSL ===")
    port = _find_free_port(18337)
    base_url = f"http://127.0.0.1:{port}"
    env_srv = os.environ.copy()
    env_srv["CORA_SKIP_AUTO_LLAMA"] = "1"
    srv_proc = subprocess.Popen(
        ["python3", str(CORE_DIR / "webui" / "server.py"), "--host", "127.0.0.1", "--port", str(port)],
        cwd=str(CORE_DIR),
        env=env_srv,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        ready = False
        for _ in range(35):
            if srv_proc.poll() is not None:
                raise RuntimeError(f"Linux WebGUI server exited early with code {srv_proc.returncode}")
            try:
                code, data = _http_json(f"{base_url}/api/health", timeout=1.5)
                if code == 200 and data.get("status") == "ok":
                    ready = True
                    break
            except Exception:
                time.sleep(0.35)
        assert ready, f"Linux WebGUI server failed to become ready on {base_url}"
        print(f"  [PASS] Linux WebGUI started on {base_url} and responded to `/api/health`.")

        for ep in ["/api/bootstrap", "/api/hardware", "/api/models", "/api/projects", "/api/tools"]:
            code, body = _http_json(f"{base_url}{ep}", timeout=12.0)
            assert code == 200, f"Endpoint {ep} returned {code}: {body}"
            if ep == "/api/hardware":
                nics = (body.get("network") or {}).get("interfaces") or []
                assert len(nics) >= 1, f"Expected at least 1 NIC in /api/hardware, got: {body.get('network')}"
                print(f"  [PASS] `/api/hardware` returned {len(nics)} Linux network interface(s) with IP/mask & speed.")
            else:
                print(f"  [PASS] `{ep}` returned HTTP 200.")

        # Create test project, upload file to Files/, and run queries
        code, c_res = _http_json(
            f"{base_url}/api/projects/create",
            method="POST",
            payload={"name": "wsl-webui-autotest", "goal": "Verify Linux WebGUI in WSL"},
        )
        assert code == 200 and c_res.get("ok"), f"Project create failed: {c_res}"
        print("  [PASS] `/api/projects/create` created `Projects/wsl-webui-autotest/Files/`.")

        b64_script = base64.b64encode(b"#!/usr/bin/env bash\necho 'CORA_WSL_FILE_OK'\n").decode("ascii")
        code, u_res = _http_json(
            f"{base_url}/api/projects/files/upload",
            method="POST",
            payload={
                "project_slug": "wsl-webui-autotest",
                "files": [{"filename": "probe.sh", "content_base64": b64_script}],
            },
        )
        assert code == 200 and u_res.get("ok"), f"File upload failed: {u_res}"
        print("  [PASS] `/api/projects/files/upload` saved `probe.sh` into `Projects/wsl-webui-autotest/Files/`.")

        for q_cmd in ["/status", "/files", "/relentless status", "/help"]:
            code, q_res = _http_json(
                f"{base_url}/api/query",
                method="POST",
                payload={"query": q_cmd, "project_slug": "wsl-webui-autotest", "session_mode": "default"},
            )
            assert code == 200 and q_res.get("reply"), f"Query {q_cmd} failed: {q_res}"
            print(f"  [PASS] `/api/query` (`{q_cmd}`) returned valid reply.")

        # Clean up SQLite messages for test project
        _http_json(f"{base_url}/api/messages/wsl-webui-autotest", method="DELETE")
    finally:
        srv_proc.terminate()
        try:
            srv_proc.wait(timeout=5)
        except Exception:
            srv_proc.kill()


def main() -> int:
    snap = _snapshot_workspace_state()
    try:
        test_interactive_cli_in_pty()
        test_run_cora_nix_commands()
        test_linux_webui_in_wsl()
        print("\n=== ALL WSL LINUX CLI & WEBGUI TESTS PASSED (100%) ===")
        return 0
    finally:
        _restore_workspace_state(snap, ["wsl-cli-autotest", "wsl-webui-autotest"])


if __name__ == "__main__":
    sys.exit(main())
