# CORA Centralized `Log/` Directory (`core/Log/README.md`)

**Author:** CROW Innovations  

All runtime server logs, process state files, console security posture logs, SQLite WebUI storage, and the master version control & historical fix analysis document are stored in `~/Projects/CORA/core/Log/`:

| File in `core/Log/` | Purpose |
| :--- | :--- |
| [`VERSION_HISTORY_AND_CHANGELOG.md`](./VERSION_HISTORY_AND_CHANGELOG.md) | Master version control log, architectural changelog (`v1.0.0` $\rightarrow$ `v5.15.12`), and root-cause incident analyses |
| [`cora_version.json`](./cora_version.json) | Machine-readable semantic version (`5.15.12`) and SHA-256 integrity hashes for the 15-Engine core and training corpus |
| `cora_webui.db` | Local SQLite database storing Custom WebUI settings, project metadata, and conversation/reasoning history |
| `active-project.txt` | Currently selected isolated project workspace slug under `CORA/Projects/` |
| `active_session_mode.env` | Synchronized session environment state (`CORA_ACTIVE_PROJECT`, `CORA_PERSONALITY_MODE`, `LLM_ISOLATION_MODE`, `LLM_ALLOWED_IFACES`) shared between CLI, launchers, and WebUI |
| `llama-server.log` | Live and historical `llama-server` stderr/diagnostic output (`./run_cora_NIX.sh logs` or `.\run_cora_WIN.ps1 logs`) |
| `llama-server.stdout.log` | Windows `llama-server.exe` standard output log |
| `llama-server.pid` | Active `llama-server` process ID |
| `llama-server.model` | Currently loaded GGUF model filename |
| `webui.pid` / `webui.log` | Active Custom CORA WebUI FastAPI server process ID and log |
| `console_posture.log` | Timestamped audit log of detected console security postures (`UNRESTRICTED`, `ISOLATED_LAN_USB`, `AIR_GAPPED_NETNS`) |
