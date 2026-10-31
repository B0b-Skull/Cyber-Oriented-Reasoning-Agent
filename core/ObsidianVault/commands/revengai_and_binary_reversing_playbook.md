---
title: revengai_and_binary_reversing_playbook
category: commands
os_platform: cross-platform
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
primary_tactic: Passive_Enum
summary: "Master CLI & SDK command playbook for RevEng.AI (https://github.com/orgs/RevEngAI/repositories — reait, sdk-python, creait, plugin-ghidra, plugin-ida, plugin-binary-ninja, reai-r2, reai-rz) and cross-platform Windows PE / Linux ELF reverse engineering."
when_to_apply: "Apply when installing, configuring, or running RevEng.AI CLI/SDK tools (reait, revengai, creait, reai-r2, reai-rz), recovering stripped binary symbols, extracting BinNet function embeddings, or disassembling and inspecting Windows PE and Linux ELF binaries."
tags: [commands, reverse_engineering, reverse-engineering, revengai, reait, sdk-python, creait, ghidra, ida, binary-ninja, radare2, rizin, pe, elf, sigcheck, strings, dumpbin, readelf, objdump, windows, linux]
updated: 2026-10-31 00:06:00
---
# RevEng.AI & Cross-Platform Binary Reverse Engineering Command Playbook (`revengai_and_binary_reversing_playbook`)

> **Official RevEng.AI GitHub Organization:** `https://github.com/orgs/RevEngAI/repositories`  
> **Strategy Playbook:** [[reasoning/reverse_engineering_strategy_playbook]]  
> **Domain Knowledge Hub:** [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]]

---

## 1. RevEng.AI Installation & Configuration Commands (`https://github.com/orgs/RevEngAI/repositories`)
| Command (`Windows PowerShell` / `Linux Bash`) | Flag & Parameter Breakdown | When to Apply (`H-MDP` / Engine Trigger) |
| :--- | :--- | :--- |
| `python -m pip install --upgrade reait revengai` | `--upgrade`: Installs or updates both the `reait` CLI toolkit (`https://github.com/RevEngAI/reait`) and `revengai` Python SDK (`https://github.com/RevEngAI/sdk-python`). | Run whenever `reait` or `revengai` is not yet installed on the host. |
| `git clone https://github.com/RevEngAI/reait.git && python -m pip install -e ./reait` | `-e ./reait`: Editable install directly from the official `RevEngAI/reait` GitHub repository. | Apply when building from source or testing the latest `RevEngAI` repository commits. |
| `git clone https://github.com/RevEngAI/creait.git && cmake -B creait/build -S creait && cmake --build creait/build` | `-B` build directory, `-S` source directory: Compiles the native C library (`libcreait`) required by `reai-r2` and `reai-rz`. | Apply before installing the Radare2 (`reai-r2`) or Rizin/Cutter (`reai-rz`) plugins. |
| `export REVENGAI_API_KEY="<KEY>" && printf "api_key = %s\nhost = https://api.reveng.ai\n" "$REVENGAI_API_KEY" > ~/.creait` | Writes `~/.creait` (Linux) or `%USERPROFILE%\.creait` (Windows) with `api_key` and `host = https://api.reveng.ai`. | Mandatory one-time credential setup before running `reait`, `reai-r2`, or `reai-rz`. |

---

## 2. `reait` CLI Binary Intelligence Commands (`RevEngAI/reait`)
| Verified Command | Flag & Parameter Breakdown | When to Apply (`H-MDP` / Engine Trigger) |
| :--- | :--- | :--- |
| `reait -b "<BINARY_PATH>" -a` | `-b`: Target binary path (PE, ELF, Mach-O, raw firmware). `-a`: Upload and start AI binary analysis on RevEng.AI. | First `RevEng.AI` step for any new unknown or stripped binary sample. |
| `reait -b "<BINARY_PATH>" -M` | `-b`: Target binary. `-M`: Match function embeddings against RevEng.AI's global corpus to auto-unstrip and recover original function symbol names. | Apply when reversing stripped C/C++/Rust/Go binaries to recover function names and library symbols. |
| `reait -b "<BINARY_PATH>" -x` | `-b`: Target binary. `-x`: Extract numerical BinNet function embedding vectors for all discovered functions in the binary. | Apply when feeding function feature vectors into Engine 20 (PCA / K-Means++) or custom similarity scripts. |
| `reait -b "<BINARY_PATH>" -l` | `-b`: Target binary. `-l`: Fetch analysis status and execution logs for the submitted binary hash. | Apply to check whether remote CFG extraction and BinNet embedding generation have completed. |

---

## 3. Cross-Platform Static & Dynamic Binary Reversing Command Matrix (Windows vs. Linux)
| Reversing Task | Windows Command (`PowerShell` / `Sysinternals` / `MSVC`) | Linux Command (`Bash` / `Binutils` / `Radare2`) | When to Apply |
| :--- | :--- | :--- | :--- |
| **File Hash, Architecture & Header Triage** | `sigcheck64.exe -a -h -i -m -nobanner "<BIN>"` | `sha256sum '<BIN>' && file '<BIN>' && readelf -h -S -l '<BIN>'` | Initial `Passive_Enum` triage (`s_init_unknown`) before any disassembly or upload. |
| **Import / Export & Capability Mapping** | `dumpbin /headers /imports /exports "<BIN>"` | `objdump -p -T '<BIN>' && rabin2 -i -E -S '<BIN>'` | Identify network sockets, cryptography, process injection, or dynamic resolver APIs (`GetProcAddress`/`dlsym`). |
| **ASCII + Wide Unicode String Extraction** | `strings64.exe -a -u -n 6 -nobanner "<BIN>"` | `strings -a -n 6 '<BIN>' && strings -a -e l -n 6 '<BIN>'` | Extract embedded C2 URLs, IP addresses, registry keys, file paths, mutexes, and error strings. |
| **UPX Unpacking (If Entropy $> 7.2$)** | `upx.exe -t "<BIN>" && upx.exe -d -o "<UNPACKED_BIN>" "<BIN>"` | `upx -t '<BIN>' && upx -d -o '<UNPACKED_BIN>' '<BIN>'` | Apply when section entropy is $> 7.2$ bits/byte or `UPX0`/`UPX1` sections are present. |
| **Non-Interactive Radare2 / Rizin Function & CFG Dump** | `r2 -q -c "aaa; afl; iI; iz" "<BIN>"` | `r2 -q -c 'aaa; afl; iI; iz' '<BIN>'` *(or `rizin -q -c ...`)* | Enumerate all functions, sizes, cyclomatic complexity, and strings without opening an interactive TUI. |
| **Ghidra Headless Batch Import & Analysis** | `analyzeHeadless.bat C:\Temp\GhidraProj ReProj -import "<BIN>" -overwrite` | `analyzeHeadless /tmp/GhidraProj ReProj -import '<BIN>' -overwrite` | Automate Ghidra project creation and decompilation prior to running `plugin-ghidra`. |
