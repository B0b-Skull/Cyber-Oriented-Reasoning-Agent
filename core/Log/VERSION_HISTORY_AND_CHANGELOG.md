# C.O.R.A. Master Version History & Architectural Changelog (`core/Log/VERSION_HISTORY_AND_CHANGELOG.md`)

**Author:** CROW Innovations  
**Current Semantic Version:** `5.15.12` ([`cora_version.json`](./cora_version.json))  

---

## 1. Semantic Versioning Specification (`MAJOR.ENGINE_REV.PATCH_REV`)

`C.O.R.A.` tracks its version deterministically in [`core/Log/cora_version.json`](./cora_version.json):
- **`major_cli` (`5`)**: Major CLI, Custom WebUI, and Two-Tier Project/Vault Architecture generation.
- **`engine_rev` (`15`)**: Active Neuro-Symbolic Reasoning Engine count (`15-Engine Streamlined Core` verified via SHA-256 tree hash `engine_tree_sha256`).
- **`patch_rev` (`12`)**: Incremental patch & training corpus revision (`patch_tree_sha256`).

---

## 2. Release History & Root-Cause Fix Ledger

### `v5.15.12` — Custom Svelte/FastAPI WebUI, Cross-Platform Parity & 15-Engine Audit Fixes
- **Custom Local WebUI (`core/webui/`)**:
  - Replaced third-party Docker `open-webui` container with a native **Svelte + TypeScript + Tailwind CSS** dashboard and **Python + FastAPI + WebSockets + SQLite + `psutil` + NVIDIA `NVML`** local backend (`core/webui/server.py`).
  - Added CLI-equivalent dropdown selectors (`Projects/<slug>/` with Create & Rename, `Personality Mode [1-4]`, `Network Isolation [Red/Blue/White]`, `Model Selector [llama-server & Ollama]`, `Thinking`, `Permissions`), with the **Results Display Window** positioned directly above the **Input Window & Select Options**.
  - Added real-time WebSocket hardware monitoring (`/ws/metrics`) for CPU, RAM, Disk, Network throughput/NICs (`psutil`), and NVIDIA GPU utilization, VRAM, temperature, and power draw (`pynvml`).
- **Log & Reasoning Engine Bug Fixes**:
  - Fixed `/train` `TypeError` in `core/agent-cli.py` where `run_training_pipeline()` was passed an unsupported `quiet=False` keyword argument.
  - Fixed `/reason -engine:<name>` in `core/agent-cli.py` so all 15 individual reasoning engines can be invoked directly instead of only 5.
  - Unified `shadow_archive` path inspection across `context_vm.py`, `agent-cli.py` (`/state`), and `Troubleshooting/troubleshoot_core.py` so project-scoped `Projects/<project>/shadow_archive/sha256_*.log` files and global `Reasoning/data/shadow_archive/` files are both counted and reported accurately.
  - Fixed `vault_bridge.load_json_state()` in-memory cache shallow reference mutation bug and removed `len(str(cached[1]))` serialization overhead.
  - Fixed `train_llm.py` version bump logic so `cora_version.json` updates `patch_tree_sha256` cleanly without causing a double patch increment on the next CLI launch.
  - Fixed Windows `ping` auto-repair in `cegar_verifier.py` (`ping -n 3 -w 2000` on Windows vs `ping -c 3 -W 2` on POSIX) and cross-platform fallback commands in `pipeline.py`, `cegar_verifier.py`, `mdp_tactical.py`, and `rl_network_policy.py`.
  - Fixed `active-model.txt` $\rightarrow$ `llama-server.model` cleanup in `core/agent-cli.py` and `export KEY="VAL"` parsing of `active_session_mode.env` in `run_cora_WIN.ps1`.
  - Fixed `./run_cora_NIX.sh troubleshoot` argument parsing and `-c` / `--continue` restoration of `isolation_mode` and `allowed_interfaces`.

### `v5.14.11` — 80/20 Pareto Streamlining (20 Engines $\rightarrow$ 15 Core Engines)
- Removed 5 redundant/high-latency engines (`fca.py`, `analogy.py`, `planner_asp.py`, `evolutionary_leap.py`, `ablation_discovery_engine.py`), cutting cold-start pipeline latency by **85.9%** while preserving 100% of root-cause, tactical Bellman H-MDP, `TD(λ)` RL, CEGAR safety, and META-MIND calibration accuracy.
- Standardized VSA hyperdimensional vectors in `vault_bridge.py` and `vsa.py` to `1,024-D` (`1.64x` speedup with zero cosine rank loss).

### `v5.12.10` — Two-Tier Project Workspace Isolation (`Projects/<project>/`)
- Isolated all runtime target scans, downloads, temporary scripts, and `memory.md` / `goals.md` / `REPORT.md` inside `CORA/Projects/<project>/` while keeping `core/ObsidianVault/` clean and universal through IP-abstracted `<TARGET_IP>` parameterization.
