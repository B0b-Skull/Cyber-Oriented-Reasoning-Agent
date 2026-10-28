#!/usr/bin/env python3
"""
Cross-Platform Installer, Hardware-Adaptive Parameter Profiler & Maintenance Script for the
CORA 15-Engine Neuro-Symbolic, Somatic, Forecasting, Continual, Meta-Learning, Trajectory RL
& Spectral PCA/K-Means++ Reasoning Suite + 80/20 Pareto Gating + Zero-Loss Context VM +
Uncapped Cross-Platform Training Pipeline (`v4.5.0-15Engine-Core`).
Works natively on both Linux and Windows (Python 3.9+, 0 MB GPU VRAM).

Usage:
  python3 Reasoning/install_reasoning.py --all
  python3 Reasoning/install_reasoning.py --check-compat
  python3 Reasoning/install_reasoning.py --install-deps
  python3 Reasoning/install_reasoning.py --seed
  python3 Reasoning/install_reasoning.py --test
  python3 Reasoning/install_reasoning.py --status
  python3 Reasoning/install_reasoning.py --download-wheels
"""

import argparse
import json
import os
import platform
import py_compile
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
REASONING_DIR = _SCRIPT_DIR
CORA_CORE_DIR = REASONING_DIR.parent
REQ_FILE = REASONING_DIR / "requirements.txt"
WHEELHOUSE_DIR = REASONING_DIR / "wheelhouse"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REQUIRED_MODULES: List[Tuple[str, str, bool]] = [
    ("numpy", "numpy>=1.24.0", True),
    ("scipy", "scipy>=1.10.0", True),
    ("networkx", "networkx>=3.0", True),
    ("sympy", "sympy>=1.12", True),
    ("z3", "z3-solver>=4.12.0", False),
    ("shapely", "shapely>=2.0.0", False),
]

MIN_RAM_MIB = 2048
MIN_FREE_RAM_MIB = 512
MIN_DISK_FREE_MIB = 250


def banner(msg: str) -> None:
    print(f"\n=== {msg} ===", flush=True)


def analyze_system_resources_and_compatibility() -> Dict[str, Any]:
    """
    Analyze OS, Python version, CPU threads, System RAM, Disk space, GPU VRAM isolation,
    and dynamically compute Hardware-Adaptive Reasoning Limits (`EXTREME_WORKSTATION`,
    `HIGH_PERFORMANCE`, or `PORTABLE_CONSERVATIVE`).
    """
    banner("Analyzing System Compatibility, Hardware Resources & Adaptive Reasoning Limits")
    os_name = platform.system()
    os_release = platform.release()
    arch = platform.machine()
    py_ver = sys.version_info
    py_ok = (py_ver.major, py_ver.minor) >= (3, 9)

    cpu_threads = os.cpu_count() or 2

    total_ram_mib = 8192
    avail_ram_mib = 4096
    try:
        if os_name == "Linux" and Path("/proc/meminfo").is_file():
            mem_txt = Path("/proc/meminfo").read_text(encoding="utf-8", errors="replace")
            for ln in mem_txt.splitlines():
                if ln.startswith("MemTotal:"):
                    total_ram_mib = int(ln.split()[1]) // 1024
                elif ln.startswith("MemAvailable:"):
                    avail_ram_mib = int(ln.split()[1]) // 1024
        elif os_name == "Windows":
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                total_ram_mib = int(stat.ullTotalPhys // (1024 * 1024))
                avail_ram_mib = int(stat.ullAvailPhys // (1024 * 1024))
    except Exception:
        pass

    disk_free_mib = 10240
    try:
        du = shutil.disk_usage(str(REASONING_DIR))
        disk_free_mib = int(du.free // (1024 * 1024))
    except Exception:
        pass

    gpu_info = "None detected (CPU-only)"
    try:
        nvsmi = shutil.which("nvidia-smi")
        if nvsmi:
            out = subprocess.check_output(
                [nvsmi, "--query-gpu=name,memory.used,memory.free,memory.total", "--format=csv,noheader"],
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=5,
            ).strip()
            if out:
                gpu_info = out.splitlines()[0]
    except Exception:
        pass

    if str(CORA_CORE_DIR) not in sys.path:
        sys.path.insert(0, str(CORA_CORE_DIR))
    from Reasoning.engines.vault_bridge import get_hardware_reasoning_limits

    hw_limits = get_hardware_reasoning_limits()

    ram_ok = total_ram_mib >= MIN_RAM_MIB and avail_ram_mib >= MIN_FREE_RAM_MIB
    disk_ok = disk_free_mib >= MIN_DISK_FREE_MIB
    compatible = py_ok and ram_ok and disk_ok

    report = {
        "compatible": compatible,
        "os": f"{os_name} {os_release} ({arch})",
        "python_version": f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}",
        "python_ok": py_ok,
        "cpu_logical_threads": cpu_threads,
        "system_ram_total_mib": total_ram_mib,
        "system_ram_available_mib": avail_ram_mib,
        "ram_ok": ram_ok,
        "disk_free_mib": disk_free_mib,
        "disk_ok": disk_ok,
        "gpu_detected": gpu_info,
        "reasoning_gpu_vram_required_mb": 0,
        "hardware_reasoning_limits": hw_limits,
    }

    print(f"  OS / Architecture:    {report['os']}")
    print(f"  Python Runtime:       Python {report['python_version']} ({'OK' if py_ok else 'FAIL: requires >= 3.9'})")
    print(f"  CPU Topology:         {hw_limits.get('cpu_physical_cores', cpu_threads // 2)} physical cores / {cpu_threads} logical threads ({hw_limits.get('numa_nodes', 1)} NUMA node(s))")
    print(f"  System RAM:           {total_ram_mib} MiB total, {avail_ram_mib} MiB available ({'OK' if ram_ok else 'LOW RAM'})")
    print(f"  Free Disk Space:      {disk_free_mib} MiB available ({'OK' if disk_ok else 'LOW DISK'})")
    print(f"  GPU Status:           {gpu_info}")
    print(
        f"  Hardware Tier:        {hw_limits.get('tier')} (All 15 Core Engines Hardware-Scaled)\n"
        f"    - L1 Safety/Sensing:  Z3 timeout={hw_limits.get('z3_timeout_ms')}ms, CEGAR loops={hw_limits.get('cegar_max_refinement_loops')}, PCA/K-Means++={hw_limits.get('kmeans_n_init')} iters (buf={hw_limits.get('pca_history_buffer_size')})\n"
        f"    - L2 Abduct/Graph:    PageRank={hw_limits.get('pagerank_max_iter')} iters, EIG depth={hw_limits.get('eig_lookahead_depth')}, DST samples={hw_limits.get('dst_monte_carlo_samples')}\n"
        f"    - L3 Causal/VSA:      Causal paths={hw_limits.get('causal_counterfactual_paths')}, VSA={hw_limits.get('vsa_hypervector_dim')}-D\n"
        f"    - L4 Tactical/RL/MDP: MDP sweeps={hw_limits.get('mdp_bellman_sweeps')}, RL={hw_limits.get('rl_train_episodes')} eps\n"
        f"    - L5 Meta/Continual:  Pass-2 cands={hw_limits.get('continual_pass2_max_candidates')}, Hedge bins={hw_limits.get('meta_calibration_bins')}, Shadow Archive={hw_limits.get('shadow_archive_max_files')} files"
    )
    print("  Reasoning VRAM Usage: 0 MB (100% CPU-isolated; preserves all GPU VRAM for LLM weights & KV cache)")
    if not compatible:
        print("  [ERROR] System does not meet minimum requirements for the 15-engine reasoning suite.", file=sys.stderr)
    else:
        print("  [OK] Hardware resources verified capable of supporting all 15 Neuro-Symbolic, Somatic, Forecasting, Continual, Meta-Learning, Trajectory RL & Spectral PCA/K-Means++ engines.")
    return report


def check_missing_modules() -> List[Tuple[str, str, bool]]:
    missing = []
    for mod_name, pkg_spec, is_core in REQUIRED_MODULES:
        try:
            __import__(mod_name)
        except ImportError:
            missing.append((mod_name, pkg_spec, is_core))
    return missing


def install_dependencies(offline: bool = False) -> bool:
    banner(f"Checking & Installing 15-Engine Python Dependencies ({platform.system()} {platform.release()})")
    missing = check_missing_modules()
    if not missing:
        print("  [OK] All 6 packages (numpy, scipy, networkx, sympy, z3-solver, shapely) are installed.")
        return True

    pkgs = [spec for _, spec, _ in missing]
    print(f"  Installing missing packages: {', '.join(pkgs)}")

    pip_base = [sys.executable, "-m", "pip", "install"]
    if offline:
        if not WHEELHOUSE_DIR.is_dir() or not list(WHEELHOUSE_DIR.glob("*.whl")):
            print(f"  [ERROR] Offline mode requested but no wheels found in {WHEELHOUSE_DIR}", file=sys.stderr)
            return False
        pip_base.extend(["--no-index", "--find-links", str(WHEELHOUSE_DIR)])

    in_venv = (sys.prefix != getattr(sys, "base_prefix", sys.prefix)) or bool(os.environ.get("VIRTUAL_ENV"))
    if in_venv:
        attempts = [
            pip_base + ["--quiet"] + pkgs,
            pip_base + ["--break-system-packages", "--quiet"] + pkgs,
        ]
    else:
        attempts = [
            pip_base + ["--user", "--quiet"] + pkgs,
            pip_base + ["--user", "--break-system-packages", "--quiet"] + pkgs,
            pip_base + ["--break-system-packages", "--quiet"] + pkgs,
            pip_base + ["--quiet"] + pkgs,
        ]
    for cmd in attempts:
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
            if res.returncode == 0:
                import importlib
                import site

                importlib.invalidate_caches()
                try:
                    site.main()
                except Exception:
                    pass
                break
        except Exception:
            continue

    still_missing = check_missing_modules()
    # Fail-safe fallback on Debian/Ubuntu/Kali if pip was blocked, missing, or offline
    if still_missing and platform.system() == "Linux" and shutil.which("apt-get") and not offline:
        apt_map = {
            "numpy": "python3-numpy",
            "scipy": "python3-scipy",
            "networkx": "python3-networkx",
            "sympy": "python3-sympy",
            "z3": "python3-z3",
            "shapely": "python3-shapely",
        }
        # Install each available apt package individually so an unavailable optional package
        # (like python3-clingo on Debian 12) never aborts the core packages, and ensure python3-pip is present.
        apt_candidates = ["python3-pip"] + [apt_map[m] for m, _, _ in still_missing if m in apt_map]
        for apt_pkg in apt_candidates:
            try:
                subprocess.run(
                    ["sudo", "-n", "apt-get", "install", "-y", apt_pkg],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                    timeout=120,
                )
            except Exception:
                pass
        import importlib
        import site

        importlib.invalidate_caches()
        try:
            site.main()
        except Exception:
            pass
        still_missing = check_missing_modules()
        # Retry pip for any remaining packages (e.g. clingo) now that python3-pip is available
        if still_missing:
            rem_pkgs = [spec for _, spec, _ in still_missing]
            for retry_cmd in (
                [sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "--quiet"] + rem_pkgs,
                [sys.executable, "-m", "pip", "install", "--break-system-packages", "--quiet"] + rem_pkgs,
                [sys.executable, "-m", "pip", "install", "--user", "--quiet"] + rem_pkgs,
            ):
                try:
                    r2 = subprocess.run(retry_cmd, capture_output=True, text=True, timeout=180)
                    if r2.returncode == 0:
                        importlib.invalidate_caches()
                        try:
                            site.main()
                        except Exception:
                            pass
                        break
                except Exception:
                    continue
            still_missing = check_missing_modules()

    core_missing = [m for m, _, is_core in still_missing if is_core]
    opt_missing = [m for m, _, is_core in still_missing if not is_core]

    if core_missing:
        print(f"  [ERROR] Core packages failed to install: {core_missing}", file=sys.stderr)
        return False
    if opt_missing:
        print(f"  [WARN] Optional solver packages missing (fallback solvers active): {opt_missing}")
    else:
        print("  [OK] All 15-engine packages (including Z3 SMT & Shapely solvers) verified.")
    return True


def verify_bytecode_syntax() -> bool:
    """Compile-checks all Python modules in Reasoning/ to guarantee zero syntax regressions."""
    banner("Verifying Bytecode Compilation Across All 15 Engine Modules + Uncapped train_llm.py")
    py_files = sorted(REASONING_DIR.rglob("*.py"))
    for pf in py_files:
        py_compile.compile(str(pf), doraise=True)
    print(f"  [OK] Verified {len(py_files)} Python modules in {REASONING_DIR} with zero syntax errors.")
    return True


def download_offline_wheels() -> bool:
    banner(f"Downloading Offline Wheelhouse to {WHEELHOUSE_DIR}")
    try:
        WHEELHOUSE_DIR.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "download",
            "-r",
            str(REQ_FILE),
            "-d",
            str(WHEELHOUSE_DIR),
        ]
        res = subprocess.run(cmd, check=False)
        if res.returncode == 0:
            print(f"  [OK] Offline wheels stored in {WHEELHOUSE_DIR}")
            return True
        print(f"  [WARN] pip download exited with code {res.returncode}", file=sys.stderr)
        return False
    except Exception as exc:
        print(f"  [ERROR] Failed to download offline wheels: {exc}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install, profile hardware limits, and maintain the CORA 15-Engine Neuro-Symbolic Reasoning Suite (v4.5.0-15Engine-Core)"
    )
    parser.add_argument("--all", action="store_true", help="Verify compatibility, install dependencies, seed data/Vault, and run 15-engine self-tests")
    parser.add_argument("--check-compat", action="store_true", help="Analyze and verify system compatibility and hardware scaling limits")
    parser.add_argument("--install-deps", action="store_true", help="Install required Python packages")
    parser.add_argument("--offline", action="store_true", help="Install from Reasoning/wheelhouse without internet")
    parser.add_argument("--download-wheels", action="store_true", help="Download wheels into Reasoning/wheelhouse for offline replication")
    parser.add_argument("--seed", action="store_true", help="Initialize Reasoning/data/ and seed ObsidianVault/reasoning/")
    parser.add_argument("--test", action="store_true", help="Run deterministic self-tests across all 15 engines + 10 guardrails + uncapped extractor")
    parser.add_argument("--status", action="store_true", help="Show environment, hardware scaling limits, Bipartite Vault Graph, and reasoning status")

    args = parser.parse_args()
    if not any([args.all, args.check_compat, args.install_deps, args.download_wheels, args.seed, args.test, args.status]):
        args.all = True

    if str(CORA_CORE_DIR) not in sys.path:
        sys.path.insert(0, str(CORA_CORE_DIR))

    try:
        if args.all or args.check_compat:
            compat = analyze_system_resources_and_compatibility()
            if not compat["compatible"]:
                sys.exit(1)
            verify_bytecode_syntax()

        if args.download_wheels:
            download_offline_wheels()

        if args.all or args.install_deps:
            if not install_dependencies(offline=args.offline):
                sys.exit(1)

        from Reasoning.reasoning_cli import check_environment_status, run_self_tests, seed_all_data_and_vault

        if args.all or args.seed:
            banner("Seeding 15-Engine Reasoning/data/ and ObsidianVault/")
            print(seed_all_data_and_vault())

        if args.all or args.test:
            banner("Running 15-Engine + 10-Guardrail + Uncapped CLI Extractor Self-Test Suite")
            test_res = run_self_tests()
            print(json.dumps(test_res, indent=2))
            if not test_res.get("all_passed"):
                sys.exit(1)

        if args.all or args.status:
            banner("15-Engine Neuro-Symbolic, Somatic, Forecasting, Continual, Meta-Learning, RL & PCA/K-Means++ Status")
            status_res = check_environment_status()
            print(json.dumps(status_res, indent=2))

    except KeyboardInterrupt:
        print("\n[Interrupted by user]", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:
        print(f"\n[FATAL INSTALLER ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
