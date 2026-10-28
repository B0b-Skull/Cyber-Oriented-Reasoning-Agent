<div align="center">
  <a href="https://CROWinnovations.com">
    <img src="core/Explained/assets/CROW_Logo-NoWords_Transparent_Glow-NoBackground.png" alt="CROW Innovations Emblem" width="220" />
  </a>

  # C.O.R.A. — Cyber Oriented Reasoning Agent

  **Version:** `5.14.11` ([`core/Log/cora_version.json`](./core/Log/cora_version.json)) &nbsp;|&nbsp; **Developed by:** [CROWinnovations.com](https://CROWinnovations.com) &nbsp;|&nbsp; **License:** [GNU GPL v3.0 (`core/LICENSE`)](./core/LICENSE)
</div>

![C.O.R.A. Splash & Architecture Banner](core/Explained/assets/cora_splash_and_versioning_guide.svg)

**C.O.R.A. (`Cyber Oriented Reasoning Agent`)** is a local, hardware-tuned AI and neuro-symbolic reasoning workstation built for Red, Blue, and Hunt Teams. It pairs local uncensored GGUF LLMs (`Qwen3.8-27B` default, `Qwen3.5-9B` fast, and `Qwen3.8-27B Turbo MTP`) via `llama-server` (CUDA/CPU) with a **15-Engine CPU Neuro-Symbolic Reasoning Suite** (`0 MB GPU VRAM`, `~9.1 ms` pipeline), **Two-Tier Memory Isolation** ([`core/ObsidianVault/`](./core/ObsidianVault) + per-project [`Projects/`](./Projects)), **Red/White/Blue Network Isolation**, and a **4-Mode Session Personality & Logic Enforcer** (`Default`, `Analyst`, `Berserker`, `Ninja`).

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
.\run_cora_WIN.ps1 cli -m 3.5                           # Launch with fast Qwen3.5-9B model
.\run_cora_WIN.ps1 cli -m 3.8 --dangerously-skip-permissions # Launch with auto-run enabled
.\run_cora_WIN.ps1 -train                               # Train Vault & 15 Engines on docs/images in .\Training\
.\run_cora_WIN.ps1 status                               # Check server status, active model & hardware profile
.\run_cora_WIN.ps1 troubleshoot                         # Run 5-Layer diagnostics & auto-repair check
.\run_cora_WIN.ps1 stop                                 # Stop background llama-server and free RAM/VRAM
```

---

## 3. Repository Structure & Documentation

```text
CORA/
├── setup_cora_NIX.sh       # Linux Automated Setup & 7-Phase Installer
├── setup_cora_WIN.ps1      # Windows PowerShell Automated Setup & 7-Phase Installer
├── run_cora_NIX.sh         # Linux Service Manager, Hardware Auto-Tuner & CLI Launcher
├── run_cora_WIN.ps1        # Windows PowerShell Service Manager, Hardware Auto-Tuner & CLI Launcher
├── core/                   # Core Agent CLI (agent-cli.py), ObsidianVault, 15 Reasoning Engines & LICENSE
├── models/                 # Local Uncensored GGUF Model Weights (Qwen3.8-27B, Qwen3.5-9B, Turbo MTP)
├── Projects/               # Tier-2 Isolated Per-Project Workspaces (downloads, scans, memory.md, goals.md)
├── Training/               # Multi-Modal & CPU Neural OCR Training Pipeline (train_llm_NIX.sh / train_llm_WIN.ps1)
└── Troubleshooting/        # 5-Layer Diagnostic & Auto-Repair Suite (troubleshoot_llm_NIX.sh / troubleshoot_llm_WIN.ps1)
```

- **Complete Command & Switch Reference:** [`core/CORA_RunCMDs.md`](./core/CORA_RunCMDs.md)
- **Architecture & Setup Deep-Dive:** [`core/SetupHowItWorks.md`](./core/SetupHowItWorks.md)
- **Multi-Modal & OCR Training Guide:** [`Training/README.md`](./Training/README.md)
- **5-Layer Troubleshooting Suite:** [`Troubleshooting/README.md`](./Troubleshooting/README.md)
- **Version History & Changelog:** [`core/Log/VERSION_HISTORY_AND_CHANGELOG.md`](./core/Log/VERSION_HISTORY_AND_CHANGELOG.md)

---

## 4. Open-Source License & Attribution (`GPL-3.0`)

C.O.R.A. is licensed under the **GNU General Public License v3.0 ([`core/LICENSE`](./core/LICENSE))**. Redistribution, modification, or operational deployment is permitted under the terms of the GPL-3.0 provided that clear attribution and development credit to **[https://CROWinnovations.com](https://CROWinnovations.com)** are retained in all copies and derivative works. C.O.R.A. is provided `"AS IS"` without warranty of any kind for authorized cybersecurity testing, defense, and research only.
