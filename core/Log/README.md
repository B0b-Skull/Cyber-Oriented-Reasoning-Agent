# CORA Centralized `Log/` Directory (`core/Log/README.md`)

**Author:** CROW Innovations  

All runtime server logs, process state files, console security posture logs, and the master version control & historical fix analysis document are stored in `~/Projects/CORA/core/Log/`:

| File in `core/Log/` | Purpose |
| :--- | :--- |
| [`VERSION_HISTORY_AND_CHANGELOG.md`](./VERSION_HISTORY_AND_CHANGELOG.md) | Master version control log, architectural changelog (`v1.0.0` $\rightarrow$ `v5.12.10`), and root-cause incident analyses |
| `llama-server.log` | Live and historical `llama-server` output (`./run_cora_NIX.sh logs` or `tail -f core/Log/llama-server.log`) |
| `llama-server.pid` | Active `llama-server` process ID |
| `llama-server.model` | Currently loaded GGUF model filename |
| `console_posture.log` | Timestamped audit log of detected console security postures (`UNRESTRICTED`, `ISOLATED_LAN_USB`, `AIR_GAPPED_NETNS`) |
