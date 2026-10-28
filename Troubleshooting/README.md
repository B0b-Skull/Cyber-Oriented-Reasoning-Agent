# C.O.R.A. & 15-Engine Layered Reasoning Troubleshooting Suite (`~/Projects/CORA/Troubleshooting`) — `v5.12.10`

**Author:** https://CROWinnovations.com  

> **Version Control & Historical Fix Analysis:** See [`../core/Log/VERSION_HISTORY_AND_CHANGELOG.md`](../core/Log/VERSION_HISTORY_AND_CHANGELOG.md).

## 1. Purpose

Because the C.O.R.A. system uses a **multi-layered Neuro-Symbolic architecture** (pre-execution command & target verification, post-execution fact extraction & failure fingerprinting, zero-loss shadow archiving, temporal state tracking, and a 15-engine Consensus Arbiter), this directory provides automated diagnostic and fault-isolation scripts for **both Linux and Windows** to immediately identify:
1. **Host & Server Concerns:** RAM/VRAM/Disk pressure, serial port (`/dev/ttyUSB*`) permission issues, `llama-server` health/context size (`n_ctx`), or recent CUDA OOM / HTTP 500 log errors.
2. **State Store & Vault Concerns:** Corrupted `.json` files in `core/Reasoning/data/`, stale truncated-IP artifacts, broken `[[WikiLinks]]` in `core/ObsidianVault/00_MEMORY_INDEX.md`, or stuck `STALE_INVALIDATED` temporal fluents in `live_fluents.json`.
3. **Guardrail Regressions:** Verifies all 6 Guardrails (CEGAR non-blocking route checks vs. fatal syntax/hang/truncated-IP blocks, SyGuS raw output preservation $\le$ threshold, and Shadow Archive rotation).
4. **Per-Engine Fault & Latency Isolation:** Runs each of the **15 Reasoning Engines** individually in isolation, measuring exact execution latency in milliseconds and capturing any exception or slow stage.
5. **Interactive Command & Arbiter Tracing:** Simulates how any bash command or problem statement flows through every reasoning layer.

---

## 2. Quick-Start Commands & Switches

### Linux (`./run_cora_NIX.sh troubleshoot` or `troubleshoot_llm_NIX.sh`)
```bash
cd ~/Projects/CORA

# 1. Run full 5-layer diagnostic & 15-engine fault-isolation audit:
./run_cora_NIX.sh troubleshoot
bash Troubleshooting/troubleshoot_llm_NIX.sh

# 2. Auto-repair corrupted JSON stores, purge stale truncated-IP files, clear stale fluents, and re-seed models:
./run_cora_NIX.sh troubleshoot --fix
bash Troubleshooting/troubleshoot_llm_NIX.sh --fix

# 3. Quick check (Layers A–C only, skipping full 15-engine benchmark):
python3 Troubleshooting/troubleshoot_core.py --quick

# 4. Trace why a specific shell command was blocked, modified, or flagged by CEGAR / CBR / SyGuS:
bash Troubleshooting/troubleshoot_llm_NIX.sh --diagnose-cmd "tio /dev/ttyUSB0"
bash Troubleshooting/troubleshoot_llm_NIX.sh --diagnose-cmd "curl -sS -m 5 -i http://172.24"
bash Troubleshooting/troubleshoot_llm_NIX.sh --diagnose-cmd "sudo ip route add <REMOTE_SUBNET> via <TARGET_IP>" --sim-output "RTNETLINK answers: File exists" --sim-exit 2

# 5. Explain why the 15-Engine Consensus Arbiter chose its recommended action for a problem:
bash Troubleshooting/troubleshoot_llm_NIX.sh --explain-arbiter "curl exit 7 on <TARGET_IP> with /dev/ttyUSB0 attached"

# 6. Append machine-readable JSON diagnostic report:
bash Troubleshooting/troubleshoot_llm_NIX.sh --json
```

### Windows PowerShell (`.\run_cora_WIN.ps1 troubleshoot` or `troubleshoot_llm_WIN.ps1`)
```powershell
# 1. Run full diagnostic & 15-engine fault-isolation audit:
.\run_cora_WIN.ps1 troubleshoot
.\Troubleshooting\troubleshoot_llm_WIN.ps1

# 2. Auto-repair corrupted JSON stores, purge stale artifacts & clear stale temporal fluents:
.\Troubleshooting\troubleshoot_llm_WIN.ps1 -Fix

# 3. Trace how a specific command is handled across all reasoning layers:
.\Troubleshooting\troubleshoot_llm_WIN.ps1 -DiagnoseCmd "ping <TARGET_IP>"

# 4. Explain the 15-Engine Consensus Arbiter decision:
.\Troubleshooting\troubleshoot_llm_WIN.ps1 -ExplainArbiter "curl exit 7 on <TARGET_IP>"

# 5. Append JSON diagnostic summary or disable ANSI colors:
.\Troubleshooting\troubleshoot_llm_WIN.ps1 -Json -NoColor
```

---

## 3. How to Identify Which Layer Is Causing an Issue

| Symptom Observed in CLI | Responsible Layer / Engine | How to Diagnose & Resolve |
| :--- | :--- | :--- |
| A command or scan refuses to run and prints `[CEGAR Pre-Verifier Blocked]` | **Layer C / Engine 12 (`cegar_verifier.py`)** | Run `bash Troubleshooting/troubleshoot_llm_NIX.sh --diagnose-cmd "<your_cmd>"`. CEGAR hard-blocks invalid `bash -n` syntax, interactive `tio` without `--script`, Python `import` inside `tio --script`, unbounded `ping` without `-c`, or truncated/malformed IPv4 targets (`http://172.24`, `ip route get 1`). |
| `[Auto-Healed Truncated IP]` appears before a tool executes | **Pre-Execution IP Healer (`agent-cli.py`)** | A tool argument contained a partial IP prefix (e.g. `172.24`) that uniquely matched a full 4-octet IPv4 address (`<TARGET_IP>`) from your prompt/project context and was automatically healed before execution. |
| Tool output has `[Temporal Event Calculus] State transition ... invalidated prior fluent(s)` | **Layer B / Engine 9 (`temporal_fluents.py`)** | A prior command restarted a service, flushed firewall rules, or bounced an interface. Run `bash Troubleshooting/troubleshoot_llm_NIX.sh --fix` to clear stale fluents in `core/Reasoning/data/temporal_fluents/live_fluents.json`. |
| Tool output has `[CBR Failure Match CBR-xxx]` prepended | **Layer C / Engine 11 (`cbr_fingerprints.py`)** | Triggered when a command exits with a non-zero return code or matches a known failure pattern in `core/Reasoning/data/cbr_cases/cbr_library.json`. |
| Long tool output (`> 2,500 chars` on laptop, `> 12,000 chars` on Ultra Server) shows `... [archived losslessly to shadow_archive/sha256_...] ...` | **Part 1 Context VM (`context_vm.py`)** | Normal zero-loss context protection. The 100% full raw log is stored at the printed path in `core/Reasoning/data/shadow_archive/`. |
| `/reason` or `neuro_symbolic_reason` is slow or fails on one engine | **Layer D (`Engines 1–15`)** | Run `bash Troubleshooting/troubleshoot_llm_NIX.sh` and check **LAYER D** — it prints the exact millisecond latency and status of all 15 engines individually. |
| LLM stops after a few tool calls or repeats failed commands | **Layer C (`Guardrail 7: /goal & /relentless`)** | Inside `./run_cora_NIX.sh cli`, lock your objective with `/goal <objective>` and run `/relentless` to engage the multi-wave loop, Obsidian Attempt Ledger (`Projects/<project>/memory.md`), and Anti-Repetition Guard. |
| `HTTP Error 500: Jinja Exception: No user query found in messages.` | **Layer C (`Guardrail 3 & 7: Context Compaction`)** | Fixed in `v3.3.0`: `trim_messages_to_fit()` and `sanitize_messages()` in `agent-cli.py` preserve the active `"role": "user"` anchor at `messages[1]` and trim `(assistant, tool)` pairs at index `2+` during deep multi-step tool chains. Restart any pre-`v3.3.0` CLI session (`./run_cora_NIX.sh cli`). |
| Console posture banner, HUD badge, and prompt colors change, but overall terminal window background/font colors do not change in **QTerminal** | **Console Posture Theme Engine (`console_posture.py` / QTerminal `libqtermwidget6`)** | Documented as a **Low-Priority Known Issue** in [`KNOWN_ISSUE_CONSOLE_POSTURE_BACKGROUND_COLOR.md`](KNOWN_ISSUE_CONSOLE_POSTURE_BACKGROUND_COLOR.md). QTerminal (`libqtermwidget6.so.2`) ignores XTerm `OSC 10`/`11`/`12` sequences while rendering ANSI/TrueColor SGR badges on the banner, prompt, and HUD bar. |
