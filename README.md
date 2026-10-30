<div align="center">
  <a href="https://CROWinnovations.com">
    <img src="core/Explained/assets/CROW_Logo-NoWords_Transparent_Glow-NoBackground.png" alt="CROW Innovations Emblem" width="220" />
  </a>

  # C.O.R.A. — Cyber Oriented Reasoning Agent

  **Version:** `5.15.12` ([`core/Log/cora_version.json`](./core/Log/cora_version.json)) &nbsp;|&nbsp; **Developed by:** [CROWinnovations.com](https://CROWinnovations.com) &nbsp;|&nbsp; **License:** [GNU GPL v3.0 (`core/LICENSE`)](./core/LICENSE)
</div>

![C.O.R.A. Splash & Architecture Banner](core/Explained/assets/cora_splash_and_versioning_guide.svg)

**C.O.R.A. (`Cyber Oriented Reasoning Agent`)** is a local, hardware-tuned AI and neuro-symbolic reasoning workstation built for Red, Blue, and Hunt Teams. It pairs local uncensored GGUF LLMs (`Qwen3.8-27B` default, `Qwen3.5-9B` fast, and `Qwen3.8-27B Turbo MTP`) via `llama-server` (CUDA/CPU) or `Ollama` with a **Custom Svelte + TypeScript + Tailwind CSS + FastAPI WebUI Dashboard** ([`core/webui/`](./core/webui)), a **15-Engine CPU Neuro-Symbolic Reasoning Suite** (`0 MB GPU VRAM`, `~9.1 ms` pipeline), **Two-Tier Memory Isolation** ([`core/ObsidianVault/`](./core/ObsidianVault) + per-project [`Projects/`](./Projects)), **Red/White/Blue Network Isolation**, and a **4-Mode Session Personality & Logic Enforcer** (`Default`, `Analyst`, `Berserker`, `Ninja`).

---

## 1. Installation & Setup Commands

Clone the repository and run the automated 7-phase installer for your operating system. The setup script probes your CPU, RAM, and NVIDIA GPU VRAM, downloads `llama.cpp` binaries and matching GGUF models with automatic byte-level resume, seeds all 15 CPU reasoning engines, and runs the 5-layer self-test suite.

### Linux (`setup_cora_NIX.sh`)
```bash
git clone https://github.com/B0b-Skull/Cyber-Oriented-Reasoning-Agent.git CORA
cd CORA

# Full automatic setup (detects GPU/RAM and downloads matching models + 15-Engine suite):
bash setup_cora_NIX.sh

# Optional installer flags:
bash setup_cora_NIX.sh --all-models       # Download all 5 GGUF models (3.5, 3.8, Turbo MTP Q4/Q6/Q8)
bash setup_cora_NIX.sh --only-3.5         # Download only fast Qwen3.5-9B (5.24 GiB)
bash setup_cora_NIX.sh --only-3.8         # Download only default Qwen3.8-27B (12.40 GiB)
bash setup_cora_NIX.sh --skip-models      # Install binaries, Python deps & 15-Engine suite only
```

### Windows PowerShell (`setup_cora_WIN.ps1`)
```powershell
git clone https://github.com/B0b-Skull/Cyber-Oriented-Reasoning-Agent.git CORA
cd CORA

# Full automatic setup (detects GPU/RAM and downloads Windows CUDA/CPU binaries + models):
.\setup_cora_WIN.ps1

# Optional installer flags:
.\setup_cora_WIN.ps1 -AllModels           # Download all 5 GGUF models (3.5, 3.8, Turbo MTP Q4/Q6/Q8)
.\setup_cora_WIN.ps1 -Only35              # Download only fast Qwen3.5-9B (5.24 GiB)
.\setup_cora_WIN.ps1 -Only38              # Download only default Qwen3.8-27B (12.40 GiB)
.\setup_cora_WIN.ps1 -SkipModels          # Install binaries, Python deps & 15-Engine suite only
```

---

## 2. Quick Start & Run Commands

### Linux (`run_cora_NIX.sh`)
```bash
./run_cora_NIX.sh                                       # Launch interactive C.O.R.A. CLI (default Qwen3.8-27B)
./run_cora_NIX.sh webgui                                # Launch Custom CORA WebUI Dashboard (http://127.0.0.1:1337)
./run_cora_NIX.sh cli -m 3.5                            # Launch with fast Qwen3.5-9B model
./run_cora_NIX.sh cli -m 3.8 --dangerously-skip-permissions  # Launch with auto-run enabled
./run_cora_NIX.sh cli -m 3.8 -netiso blue eth0,eth1     # Launch locked to specific network interfaces
./run_cora_NIX.sh -train                                # Train Vault & 15 Engines on docs/images in ./Training/
./run_cora_NIX.sh status                                # Check server status, active model & hardware profile
./run_cora_NIX.sh troubleshoot                          # Run 5-Layer diagnostics & auto-repair check
./run_cora_NIX.sh stop                                  # Stop background llama-server and free RAM/VRAM
```

### Windows PowerShell (`run_cora_WIN.ps1`)
```powershell
.\run_cora_WIN.ps1                                      # Launch interactive C.O.R.A. CLI (default Qwen3.8-27B)
.\run_cora_WIN.ps1 webgui                               # Launch Custom CORA WebUI Dashboard (http://127.0.0.1:1337)
.\run_cora_WIN.ps1 cli -m 3.5                           # Launch with fast Qwen3.5-9B model
.\run_cora_WIN.ps1 cli -m 3.8 --dangerously-skip-permissions # Launch with auto-run enabled
.\run_cora_WIN.ps1 -train                               # Train Vault & 15 Engines on docs/images in .\Training\
.\run_cora_WIN.ps1 status                               # Check server status, active model & hardware profile
.\run_cora_WIN.ps1 troubleshoot                         # Run 5-Layer diagnostics & auto-repair check
.\run_cora_WIN.ps1 stop                                 # Stop background llama-server and free RAM/VRAM
```

---

## 3. Enterprise WebGUI Dashboard, Commands & Keyboard Shortcuts (`http://127.0.0.1:1337`)

Launch the native Svelte + TypeScript + Tailwind CSS + FastAPI WebGUI Dashboard with `./run_cora_NIX.sh webgui` (Linux) or `.\run_cora_WIN.ps1 webgui` (Windows PowerShell).

### Key WebGUI Capabilities & Controls
- **High-Contrast Lighter C.O.R.A. Output Surface:** Visually separates **`👤 OPERATOR QUERY`**, **`🤖 C.O.R.A. OUTPUT`** (rendered on a lighter, high-contrast slate/white reading surface), and **`⚡ COMMAND PROBE OUTPUT`** so responses are effortless to scan.
- **Antigravity-Style `Ctrl+O` Thought Process & Engine Trace Toggle (Hidden by Default):**
  - Internal LLM chain-of-thought (`<think>...</think>`), executed tool probes, and 15-Engine neuro-symbolic diagnostics are **hidden by default** so the main output pane stays clean and focused.
  - While C.O.R.A. is actively processing, a live status card appears in the output pane: **`🧠 C.O.R.A. THINKING / PROCESSING — Press Ctrl+O to expand thought process ▸`**.
  - Press **`Ctrl+O`** (or click the **`🧠 Thought Process (Ctrl+O)`** header button / message thought bar) at any time during or after execution to expand or collapse the full internal reasoning trace.
- **Stacked & Scrollable Multi-NIC `NET` Header Display:**
  - Displays live per-interface network telemetry in the top header formatted as **`Interface name | IP/mask | ↑upload ↓download`**.
  - When multiple network interfaces or IP/CIDR addresses are active on the host, rows are stacked vertically inside the header with an interactive scrollbar (`↕`).
- **`⚙️ Settings` Display & Font Customization Modal:**
  - Located to the right of the **`SYSINTERNALS: INSTALLED`** / **`SYS TOOLS: INSTALLED`** badge in the top header.
  - Customize **Font Style** (JetBrains Mono, Fira Code, Cascadia Code, Inter, IBM Plex Sans, Classic Terminal), **Font Size** (`11px`–`20px`), **Font Color** (8 tactical presets + custom hex color picker), **Line Spacing**, **Workspace Layout** (`Flush` edge-to-edge zero-gap vs `Framed`), and **Theme Mode** (`🌙 Dark` / `☀️ Light`).
- **Mandatory Project Workspace & Per-Project `Projects/<project>/Files/` Directory:**
  - Requires selecting an existing project or creating a new project in `Projects/<project>/` (never creates a dummy `active_session` or `default` project).
  - Every project automatically includes **`Projects/<project>/Files/`**. Use **`📤 + Upload / Add File`**, **`📁 Manage Files/`**, drag-and-drop onto the console, or `/upload <path>` to place custom scripts, logs, or configs directly into `Projects/<project>/Files/` where the LLM can automatically inspect, read, edit, and execute them.

### WebGUI & CLI Slash Commands & Keyboard Shortcuts

| Shortcut / Command | Scope | Description |
| :--- | :--- | :--- |
| **`Ctrl+O`** | WebGUI & CLI | Expand or collapse C.O.R.A.'s internal LLM `<think>` thought process & 15-Engine trace (hidden by default). |
| **`↑` / `↓` Arrows** | WebGUI & CLI | Scroll backward and forward through saved Query History and Command Probe History. |
| **`Tab ↹`** *(or `Shift+Tab`)* | WebGUI & CLI | Accept (or cycle) inline shaded ghost-text word & command autocomplete. |
| **`/files`** *(or `/files list`)* | WebGUI & CLI | List all files inside the active project's `Projects/<project>/Files/` directory. |
| **`/upload <path>`** *(or `/add <path>`)* | WebGUI & CLI | Copy/import a local file or directory into `Projects/<project>/Files/` for immediate LLM interaction. |
| **`/files read <name>`** / **`/files rm <name>`** | WebGUI & CLI | View or delete a file inside `Projects/<project>/Files/`. |
| **`/goal "<objective>"`** | WebGUI & CLI | Lock a project objective into `Projects/<project>/goals.md` and pursue it with the LLM. |
| **`/relentless "<objective>" [-max:<#>]`** | WebGUI & CLI | Engage multi-wave autonomous execution until `[GOAL_ACHIEVED]` (`-max:0` = unlimited waves). |
| **`/generate-report`** *(or `/report`)* | WebGUI & CLI | Generate a 5-Section Executive & Technical Markdown Report (`Projects/<project>/REPORT.md`). |
| **`/project`** | WebGUI & CLI | List, switch (`-load:<name>`), create (`-new:<name>`), or rename (`-rename:<old>:<new>`) projects. |
| **`/mode`** | WebGUI & CLI | View or switch Session Personality Mode (`[1] Default`, `[2] Analyst`, `[3] Berserker`, `[4] Ninja`). |
| **`/netiso <red\|blue\|white> [ifaces]`** | WebGUI & CLI | Inspect or switch Network Isolation posture (`Red` unrestricted, `Blue` NIC-locked, `White` loopback). |
| **`/reason`** / **`/rl`** / **`/pca`** / **`/continual`** | WebGUI & CLI | Run on-demand 15-Engine Neuro-Symbolic, Trajectory RL, Spectral PCA/K-Means++, or Continual Learning passes. |
| **`/train [-path:<dir>] [-mode:force]`** | WebGUI & CLI | Run 4-Phase Multi-Modal & CPU Neural OCR training on documents/images in `Training/`. |
| **`/scan -target:<ip_or_url>`** | WebGUI & CLI | Scan a target (blocked in `Analyst` / `WHITE` isolation) and save findings to the project workspace. |
| **`/vault`** / **`/search <q>`** / **`/remember <fact>`** | WebGUI & CLI | Inspect, search, or persist universal long-term knowledge in `core/ObsidianVault/`. |
| **`/state`** / **`/hw`** / **`/status`** / **`/clear`** / **`/help`** | WebGUI & CLI | Inspect Context VM & L1 state, live CPU/RAM/GPU/NIC hardware telemetry, service status, clear display, or view help. |

---

## 4. Repository Structure & Documentation

```text
CORA/
├── setup_cora_NIX.sh       # Linux Automated Setup & 7-Phase Installer
├── setup_cora_WIN.ps1      # Windows PowerShell Automated Setup & 7-Phase Installer
├── run_cora_NIX.sh         # Linux Service Manager, Hardware Auto-Tuner, WebGUI & CLI Launcher
├── run_cora_WIN.ps1        # Windows PowerShell Service Manager, Hardware Auto-Tuner, WebGUI & CLI Launcher
├── core/                   # Core Agent CLI (agent-cli.py), Custom WebUI (core/webui), ObsidianVault & 15 Engines
├── models/                 # Local Uncensored GGUF Model Weights (Qwen3.8-27B, Qwen3.5-9B, Turbo MTP)
├── Projects/               # Tier-2 Isolated Per-Project Workspaces (Files/, downloads/, targets/, memory.md, goals.md)
├── Training/               # Multi-Modal & CPU Neural OCR Training Pipeline (train_llm_NIX.sh / train_llm_WIN.ps1)
└── Troubleshooting/        # 5-Layer Diagnostic & Auto-Repair Suite (troubleshoot_llm_NIX.sh / troubleshoot_llm_WIN.ps1)
```

- **Complete Command & Switch Reference:** [`core/CORA_RunCMDs.md`](./core/CORA_RunCMDs.md)
- **Custom Svelte/FastAPI WebUI Guide:** [`core/webui/README.md`](./core/webui/README.md)
- **Architecture & Setup Deep-Dive:** [`core/SetupHowItWorks.md`](./core/SetupHowItWorks.md)
- **Multi-Modal & OCR Training Guide:** [`Training/README.md`](./Training/README.md)
- **5-Layer Troubleshooting Suite:** [`Troubleshooting/README.md`](./Troubleshooting/README.md)
- **Version History & Changelog:** [`core/Log/VERSION_HISTORY_AND_CHANGELOG.md`](./core/Log/VERSION_HISTORY_AND_CHANGELOG.md)

---

## 5. Open-Source License & Attribution (`GPL-3.0`)

C.O.R.A. is licensed under the **GNU General Public License v3.0 ([`core/LICENSE`](./core/LICENSE))**. Redistribution, modification, or operational deployment is permitted under the terms of the GPL-3.0 provided that clear attribution and development credit to **[https://CROWinnovations.com](https://CROWinnovations.com)** are retained in all copies and derivative works. C.O.R.A. is provided `"AS IS"` without warranty of any kind for authorized cybersecurity testing, defense, and research only.
