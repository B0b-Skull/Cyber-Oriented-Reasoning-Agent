# C.O.R.A. Custom Web Interface (`core/webui/`)

**Author:** CROW Innovations  
**Version:** `5.15.12`  

Replaces the third-party Docker `open-webui` container with a native, zero-Docker **Svelte + TypeScript + Tailwind CSS** dashboard backed by a local **Python + FastAPI + WebSockets + SQLite + psutil + NVIDIA NVML** service (`core/webui/server.py`).

---

## 1. Component & Technology Architecture

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Interface (`frontend/`)** | **Svelte 4 + TypeScript + Tailwind CSS + Vite** | Full-bleed edge-to-edge Enterprise Dashboard (`p-0 gap-0`), lighter high-contrast **`🤖 C.O.R.A. OUTPUT`** surface vs **`👤 OPERATOR QUERY`**, Antigravity-style **`Ctrl+O` Thought Process & Engine Trace toggle** (hidden by default with live `Thinking / Processing... Press Ctrl+O to expand` indicator), **`⚙️ Settings` customization modal** (Font Style, Font Color, Font Size, Line Spacing, Layout Density), **stacked/scrollable multi-NIC `NET` header display** (`Interface name \| IP/mask \| ↑upload ↓download`), **Console File Uploader & Project `Files/` Manager (`Projects/<project>/Files/`)**, and CLI-equivalent selectors (`Projects`, `Personality Mode`, `Network Isolation`, `Model`). |
| **Local Backend (`server.py`)** | **Python + FastAPI + WebSockets** | Connects the interface to `CORA/Projects/` (including automatic creation & LLM indexing of `Projects/<project>/Files/`), `core/ObsidianVault/`, hardware telemetry, the 15-Engine Neuro-Symbolic Reasoning Pipeline (`core/Reasoning/`), Engine 9 CEGAR pre-verification, and local inference APIs. |
| **Hardware Monitoring** | **`psutil` + NVIDIA `pynvml` (`nvidia-smi` fallback)** | Streams real-time CPU %, per-core load, RAM GB/%, Disk GB & I/O MB/s, Network RX/TX KB/s & NICs, and NVIDIA GPU utilization %, VRAM used/total GB, temperature °C, and power draw over `/ws/metrics`. |
| **Model Connections** | **Local Inference APIs (`llama-server` & `Ollama`)** | Discovers installed GGUF models in `core/Models/` (`3.8`, `3.5`, `turbo`, `turbo-q6`, `turbo-q8`), probes `llama-server` (`127.0.0.1:8080/v1`) and `Ollama` (`127.0.0.1:11434`), and routes conversations to the selected model. |
| **Local Storage** | **SQLite (`core/Log/cora_webui.db`)** | Persists operator settings, project metadata, and per-project conversation & 15-Engine reasoning history while synchronizing `core/Log/active-project.txt` and `core/Log/active_session_mode.env` with the CLI. |
| **Desktop Window (Optional)** | **Tauri (`frontend/src-tauri/tauri.conf.json`)** | Optional desktop window wrapper pointing at the local service or compiled `frontend/dist` bundle. |

---

## 2. Quick Start

### Launch via CORA Startup Scripts (Recommended)
```powershell
# Windows PowerShell (starts & opens the Custom CORA WebUI on http://127.0.0.1:1337, fallback: 31337)
.\run_cora_WIN.ps1 webgui
# (or .\run_cora_WIN.ps1 webui  /  .\run_cora_WIN.ps1 start)

# Or launch directly via Python on port 1337 (or 31337):
python core\webui\server.py --host 127.0.0.1 --port 1337
```

```bash
# Linux / macOS
./run_cora_NIX.sh webgui
# (or ./run_cora_NIX.sh webui  /  ./run_cora_NIX.sh start)

# Or launch directly via Python on port 1337 (or 31337):
python3 core/webui/server.py --host 127.0.0.1 --port 1337
```

### Frontend Development & Rebuild
```bash
cd core/webui/frontend
npm install
npm run check   # Verify TypeScript & Svelte types (0 errors, 0 warnings)
npm run build   # Compile production bundle into core/webui/frontend/dist/
npm run dev     # Optional Vite dev server on http://127.0.0.1:5173 (proxies /api and /ws to :1337)
```
