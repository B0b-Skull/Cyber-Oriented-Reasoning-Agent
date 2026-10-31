---
title: reverse_engineering_strategy_playbook
category: reasoning
engine: team_strategy_arbiter
team_role: reverse_engineering
os_platform: cross-platform
domain_hub: "[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]"
primary_tactic: Passive_Enum
summary: "Reverse Engineering & RevEng.AI Binary Intelligence Strategy Playbook: setup and installation of RevEngAI repositories (reait, sdk-python, creait, plugin-ghidra, plugin-ida, plugin-binary-ninja, reai-r2, reai-rz), AI symbol recovery (auto-unstripping), BinNet function embeddings, binary similarity, and static/dynamic PE/ELF/firmware analysis across Windows and Linux."
when_to_apply: "Apply when the operator or goal involves reverse engineering binaries (Windows PE .exe/.dll/.sys, Linux ELF, macOS Mach-O, or firmware), recovering stripped symbols, computing function similarity or BinNet embeddings, generating YARA/SBOM signatures, running headless Ghidra/IDA/Radare2/Rizin analysis, or installing, configuring, and using the RevEng.AI toolset (https://github.com/orgs/RevEngAI/repositories)."
tags: [reasoning, reverse_engineering, reverse-engineering, revengai, reait, sdk-python, creait, ghidra, ida, binary-ninja, radare2, rizin, cutter, pe, elf, decompilation, binary-similarity, embeddings, yara, sbom, malware-analysis, windows, linux]
updated: 2026-10-31 00:05:00
---
# Reverse Engineering & RevEng.AI Binary Intelligence Playbook (`reverse_engineering_strategy_playbook`)

> **Team Role:** `REVERSE_ENGINEERING` (Binary Intelligence, Symbol Recovery, Decompilation & Malware Triage)  
> **Official Repository Hub:** `https://github.com/orgs/RevEngAI/repositories` (`https://github.com/RevEngAI`)  
> **Primary H-MDP Tactics:** `Passive_Enum` (Static Triage) $\to$ `Enumeration` (Embeddings, Decompilation & Similarity) $\to$ `Post_Exploitation_Verification` (Signature & Capability Verification)  
> **Recommended Console Posture:** `WHITE` (Air-Gapped Namespace for Offline Static/Dynamic Analysis) or `BLUE`/`RED` (When querying `https://api.reveng.ai`) | **Modes:** `Analyst` (Read-Only Safe Triage) / `Standard`  
> **Backlinks:** [[00_MEMORY_INDEX]] | [[commands/revengai_and_binary_reversing_playbook]] | [[commands/windows_master_command_playbook]] | [[commands/linux_master_command_playbook]] | [[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]

---

## 1. When Engines & LLM Must Activate This Playbook
Activate `[[reasoning/reverse_engineering_strategy_playbook]]` and `[[commands/revengai_and_binary_reversing_playbook]]` whenever the query, goal, or attached project file in `Projects/<project>/Files/` involves:
- **RevEng.AI Installation, Setup & CLI/SDK Automation:** Installing or configuring any repository from `https://github.com/orgs/RevEngAI/repositories` (`reait`, `sdk-python`, `creait`, `plugin-ghidra`, `plugin-ida`, `plugin-binary-ninja`, `reai-r2`, `reai-rz`).
- **Stripped Binary Analysis & Auto-Unstripping:** Recovering stripped function names, types, and library attributions from compiled C/C++/Rust/Go binaries using RevEng.AI BinNet embeddings (`reait -b <bin> -M`).
- **Cross-Binary Similarity, Malware Triage & SBOM Generation:** Comparing unknown binaries against known malware families, open-source libraries, or vulnerable firmware versions (`reait -b <bin> -x`, `-s`).
- **PE / ELF / Firmware Static & Headless Disassembly:** Inspecting headers, imports/exports, sections, entropy, strings, authenticode signatures, TLS callbacks, or running headless Ghidra / Radare2 / Rizin / `objdump` / `dumpbin` decompilation.

---

## 2. Official RevEng.AI GitHub Repositories (`https://github.com/orgs/RevEngAI/repositories`)
| Repository Name | Official GitHub URL | Language / Type | Core Purpose & When to Use |
| :--- | :--- | :--- | :--- |
| **RevEngAI Org Hub** | `https://github.com/orgs/RevEngAI/repositories` | Organization Index | Master catalog of all official RevEng.AI SDKs, CLI toolkits, C libraries, and disassembler plugins. |
| **`RevEngAI/reait`** | `https://github.com/RevEngAI/reait` | Python (`CLI` + API) | **Primary CLI & Python Toolkit (`reait`)**: Upload binaries (`-a`), extract BinNet function embeddings (`-x`), auto-unstrip/match similar functions (`-M`), and query collections. |
| **`RevEngAI/sdk-python`** | `https://github.com/RevEngAI/sdk-python` | Python (`revengai`) | **Official Python SDK**: Programmatic REST client for batch binary submission, CI/CD pipelines, AI decompilation polling, and custom agent workflows. |
| **`RevEngAI/creait`** | `https://github.com/RevEngAI/creait` | C (`libcreait`) | **Native C Toolkit & Config Engine**: Lightweight C library for interacting with the RevEng.AI API and managing `~/.creait` credentials for `reai-r2` / `reai-rz`. |
| **`RevEngAI/plugin-ghidra`** | `https://github.com/RevEngAI/plugin-ghidra` | Java (Ghidra 11.x+) | **Ghidra Extension**: Integrates RevEng.AI binary upload, function similarity matching, auto-unstripping, AI decompilation, and AI chat directly into Ghidra. |
| **`RevEngAI/plugin-ida`** | `https://github.com/RevEngAI/plugin-ida` | Python 3 (IDA Pro) | **IDA Pro Plugin**: Adds AI function renaming, similarity search across global collections, AI decompilation, and symbol propagation inside IDA Pro. |
| **`RevEngAI/plugin-binary-ninja`** | `https://github.com/RevEngAI/plugin-binary-ninja` | Python 3 (Binja 3.0+) | **Binary Ninja Plugin**: Embeds semantic function matching, binary upload, and automated symbol recovery into Binary Ninja. |
| **`RevEngAI/reai-r2`** | `https://github.com/RevEngAI/reai-r2` | C (Radare2 Plugin) | **Radare2 Plugin**: Executes RevEng.AI binary analysis, function similarity searches, and auto-renaming directly inside the `r2` CLI shell. |
| **`RevEngAI/reai-rz`** | `https://github.com/RevEngAI/reai-rz` | C (Rizin / Cutter) | **Rizin & Cutter Plugin**: Brings RevEng.AI function similarity and AI symbol recovery to the Rizin CLI (`rizin`) and Cutter GUI. |

---

## 3. Setup, Installation & Configuration Process for RevEng.AI (Windows & Linux)

### Step 3.1: Verify Existing Installation (Run First Before Installing)
- **Windows (`PowerShell`):**
  ```powershell
  python -m pip show reait revengai 2>$null; Get-Command reait -ErrorAction SilentlyContinue
  ```
- **Linux (`Bash`):**
  ```bash
  python3 -m pip show reait revengai 2>/dev/null; command -v reait
  ```

### Step 3.2: Install `reait` CLI Toolkit & `sdk-python` (`revengai`)
Always install inside the active Python virtual environment (`venv`) or user site-packages:
- **Install from PyPI (Fastest Recommended Method — Windows & Linux):**
  ```bash
  python -m pip install --upgrade reait revengai
  ```
- **Install Latest Development Version Directly from GitHub (`https://github.com/orgs/RevEngAI/repositories`):**
  ```bash
  git clone https://github.com/RevEngAI/reait.git
  python -m pip install -e ./reait
  git clone https://github.com/RevEngAI/sdk-python.git
  python -m pip install -e ./sdk-python
  ```

### Step 3.3: Configure RevEng.AI API Key & Endpoint (`https://api.reveng.ai`)
1. Obtain an API key from the RevEng.AI Portal (`https://portal.reveng.ai` $\to$ **Settings** $\to$ **API Keys**).
2. Configure via Environment Variables or the `~/.creait` (`%USERPROFILE%\.creait`) config file:
   - **Windows (`PowerShell`):**
     ```powershell
     $env:REVENGAI_API_KEY = "<YOUR_API_KEY>"
     $env:REVENGAI_HOST = "https://api.reveng.ai"
     Set-Content -Path "$env:USERPROFILE\.creait" -Value "api_key = <YOUR_API_KEY>`nhost = https://api.reveng.ai"
     ```
   - **Linux (`Bash`):**
     ```bash
     export REVENGAI_API_KEY="<YOUR_API_KEY>"
     export REVENGAI_HOST="https://api.reveng.ai"
     printf "api_key = %s\nhost = https://api.reveng.ai\n" "$REVENGAI_API_KEY" > ~/.creait && chmod 600 ~/.creait
     ```

### Step 3.4: Install Disassembler Plugins (Ghidra, IDA Pro, Binary Ninja, Radare2, Rizin)
| Disassembler | Installation & Setup Procedure |
| :--- | :--- |
| **Ghidra (`plugin-ghidra`)** | 1. Download the release `.zip` matching your Ghidra version from `https://github.com/RevEngAI/plugin-ghidra/releases` (requires Ghidra 11.x+ & Java 21).<br>2. In Ghidra: **File $\to$ Install Extensions...** $\to$ click **`+`** $\to$ select the `.zip` $\to$ restart Ghidra.<br>3. In CodeBrowser: **Window $\to$ RevEng.AI** $\to$ enter API Key & `https://api.reveng.ai`. |
| **IDA Pro (`plugin-ida`)** | 1. Clone `https://github.com/RevEngAI/plugin-ida.git` or download the latest release.<br>2. Copy the plugin into `%APPDATA%\Hex-Rays\IDA Pro\plugins\` (Windows) or `~/.idapro/plugins/` (Linux) and run `pip install -r requirements.txt` using IDA's Python interpreter.<br>3. In IDA Pro: **Edit $\to$ Plugins $\to$ RevEng.AI** $\to$ configure API Key. |
| **Binary Ninja (`plugin-binary-ninja`)** | 1. Download the latest release from `https://github.com/RevEngAI/plugin-binary-ninja/releases`.<br>2. Extract into `%APPDATA%\Binary Ninja\plugins\` (Windows) or `~/.binaryninja/plugins/` (Linux) (*Tools $\to$ Plugins $\to$ Open Plugin Folder*). |
| **Radare2 / Rizin (`reai-r2` / `reai-rz`)** | 1. Build & install `https://github.com/RevEngAI/creait` (`cmake -B build && cmake --build build --target install`).<br>2. Install `reai-r2` (`https://github.com/RevEngAI/reai-r2`) via `r2pm -ci reai-r2` or CMake; install `reai-rz` (`https://github.com/RevEngAI/reai-rz`) for Rizin/Cutter. |

---

## 4. 15-Engine Neuro-Symbolic Alignment for Reverse Engineering
| Engine Layer | Engine Name | Reverse Engineering Role & Decision Rule |
| :--- | :--- | :--- |
| **Layer 0** | **Engine 1 (`associative`) & Engine 13 (`sygus_extractor`)** | Activate `[[reasoning/reverse_engineering_strategy_playbook]]`, `[[commands/revengai_and_binary_reversing_playbook]]`, and `[[knowledge/10_digital_forensics_pe_reversing_and_threat_intel]]`; extract hashes, section names, imports, and function addresses from CLI output. |
| **Layer 1** | **Engine 2 (`geometric`) & Engine 12 (`cegar_verifier`)** | Check PE/ELF section virtual-to-raw size ratios and Shannon entropy ($H > 7.2$ bits/byte indicates packing/encryption); CEGAR enforces non-execution of untrusted binaries outside an isolated sandbox. |
| **Layer 2** | **Engine 4 (`bayesian`), Engine 7 (`vsa`) & Engine 10 (`dempster_shafer`)** | Combine import table indicators, section entropy, and RevEng.AI BinNet cosine similarity scores to rank binary capabilities and detect packed/spoofed headers (high DST conflict $K$). |
| **Layer 3/4** | **Engine 15 (`mdp_tactical`) & Engine 20 (`spectral_manifold_pca`)** | Follow strict static-first progression (`File/Hash/Headers` $\to$ `Strings/Imports/Entropy` $\to$ `RevEng.AI Embeddings & Unstrip` $\to$ `Headless Decompilation`); project high-dimensional BinNet function embeddings into PCA/K-Means++ clusters to isolate outlier/custom functions from standard runtime library code. |

---

## 5. Concise 5-Phase Reverse Engineering Operational Playbook

### Phase 1: Static Identification, Hashing, Headers & Signatures (`Passive_Enum`)
| Task | Windows Command (`PowerShell` / `Sysinternals` / `MSVC`) | Linux Command (`Bash` / `Binutils`) | Analytical Purpose |
| :--- | :--- | :--- | :--- |
| **Compute SHA-256 Hash & File Type** | `powershell -NoProfile -Command "Get-FileHash -Algorithm SHA256 '<BINARY>'; Get-Item '<BINARY>' \| Select-Object Name,Length,CreationTime,LastWriteTime"` | `sha256sum '<BINARY>' && file '<BINARY>' && stat '<BINARY>'` | Generate canonical SHA-256 lookup hash (for RevEng.AI & threat intel) and identify architecture (x86/x64/ARM, PE/ELF, stripped vs not stripped). |
| **Verify Authenticode / Headers & Mitigations** | `sigcheck64.exe -a -h -i -m -nobanner "<BINARY>"` *(or)* `dumpbin /headers "<BINARY>"` | `readelf -h -S -l '<BINARY>'` *(or)* `checksec --file='<BINARY>'` | Check digital signature validity, compile timestamp, entry point, ASLR/PIE, DEP/NX, stack canaries, and section permissions (`RWX`). |

### Phase 2: Imports, Exports, Strings & Section Entropy Analysis (`Passive_Enum`)
| Task | Windows Command (`PowerShell` / `Sysinternals`) | Linux Command (`Bash` / `Radare2`) | Analytical Purpose |
| :--- | :--- | :--- | :--- |
| **Inspect Imported & Exported APIs** | `dumpbin /imports /exports "<BINARY>"` *(or)* `powershell -NoProfile -Command "strings64.exe -accepteula -n 6 '<BINARY>' \| Select-String -Pattern 'VirtualAlloc\|WriteProcessMemory\|CreateRemoteThread\|WinHttp\|Crypt\|RegSetValue'"` | `nm -D '<BINARY>' 2>/dev/null; objdump -T -p '<BINARY>'; rabin2 -i -E '<BINARY>'` | Identify process injection (`VirtualAllocEx`, `WriteProcessMemory`), crypto, network (`socket`, `connect`, `WinInet`), or anti-debug APIs (`IsDebuggerPresent`, `ptrace`). |
| **Extract ASCII & UTF-16LE Strings** | `strings64.exe -a -u -n 6 -nobanner "<BINARY>"` | `strings -a -n 6 '<BINARY>' && strings -a -e l -n 6 '<BINARY>'` | Extract embedded URLs, IPs, C2 domains, registry keys, file paths, mutex names, format strings, and compiler build paths (`PDB`). |
| **Detect Packing / High Section Entropy** | `powershell -NoProfile -Command "$b=[IO.File]::ReadAllBytes('<BINARY>'); $f=@{}; foreach($x in $b){$f[$x]++}; $h=0.0; foreach($c in $f.Values){$p=$c/$b.Length; $h-=$p*[Math]::Log($p,2)}; Write-Output ('Shannon_Entropy_BitsPerByte: {0:N4}' -f $h)"` | `rabin2 -S '<BINARY>'` *(or)* `python3 -c "import math,collections,sys; b=open(sys.argv[1],'rb').read(); c=collections.Counter(b); print(f'Entropy: {-sum((v/len(b))*math.log2(v/len(b)) for v in c.values()):.4f} bits/B')" '<BINARY>'` | Entropy $> 7.2$ bits/byte or missing import tables (`LoadLibraryA` + `GetProcAddress` only) indicates UPX/custom packing or encrypted payloads; unpack (`upx -d`) before decompiling. |

### Phase 3: RevEng.AI Binary Intelligence, Embeddings & Auto-Unstripping (`Enumeration`)
| Task | `reait` CLI / Python Command (Cross-Platform Windows & Linux) | What It Accomplishes |
| :--- | :--- | :--- |
| **Upload Binary for AI Analysis** | `reait -b "<BINARY>" -a` | Uploads the binary to RevEng.AI (`https://api.reveng.ai`) and triggers disassembly, control-flow graph (CFG) extraction, and BinNet AI model analysis. |
| **Auto-Unstrip Symbols via Similarity Match** | `reait -b "<BINARY>" -M` | Queries RevEng.AI's global symbol corpus using BinNet embeddings to automatically rename stripped functions (`FUN_00401000` $\to$ `mbedtls_aes_crypt_cbc`) above confidence threshold. |
| **Extract Function Embeddings Vector JSON** | `reait -b "<BINARY>" -x` | Downloads numerical BinNet function embedding vectors for every function in `<BINARY>` for downstream cosine similarity or Engine 20 PCA/K-Means++ clustering. |
| **Download Logs / Delete / Check Analysis** | `reait -b "<BINARY>" -l` *(logs)* \| `reait -h` *(full CLI options)* | Retrieves remote analysis progress logs or inspects available model/collection flags. |
| **Programmatic Python SDK Triage (`sdk-python`)** | `python -c "import os, revengai; print('RevEngAI SDK Ready:', getattr(revengai, '__file__', 'installed'))"` | Verifies the `revengai` Python SDK (`https://github.com/RevEngAI/sdk-python`) for custom batch automation scripts inside `Projects/<project>/Files/`. |

### Phase 4: Headless Disassembly & Decompilation (`Ghidra`, `Radare2`, `Rizin`, `objdump`)
| Task | Windows Command (`CMD` / `PowerShell`) | Linux Command (`Bash`) | Analytical Purpose |
| :--- | :--- | :--- | :--- |
| **Radare2 / Rizin Non-Interactive Function & CFG Audit** | `r2 -q -c "aaa; afl; iI; iz" "<BINARY>"` | `r2 -q -c 'aaa; afl; iI; iz' '<BINARY>'` *(or)* `rizin -q -c 'aaa; afl; iI; iz' '<BINARY>'` | Performs automated function analysis (`aaa`), lists all discovered functions (`afl`), binary info (`iI`), and strings (`iz`) without hanging interactively. |
| **Disassemble Specific Function (`main` / Entry)** | `r2 -q -c "aaa; pdf @ main" "<BINARY>"` *(or)* `dumpbin /disasm:nobytes "<BINARY>"` | `objdump -d -M intel '<BINARY>' \| head -n 120` *(or)* `r2 -q -c 'aaa; pdf @ main' '<BINARY>'` | Inspects exact x86/x64/ARM assembly instructions, calling conventions, and cross-references (`axf` / `axt`). |
| **Ghidra Headless Batch Analysis** | `analyzeHeadless.bat C:\Temp\GhidraProj ReProj -import "<BINARY>" -overwrite` | `analyzeHeadless /tmp/GhidraProj ReProj -import '<BINARY>' -overwrite` | Imports and analyzes the binary headlessly in Ghidra so `plugin-ghidra` or post-scripts can export decompiled C pseudocode. |

### Phase 5: Controlled Dynamic Behavioral & Memory Inspection (Isolated Sandbox Only)
| Task | Windows Command (`Sysinternals` / `PowerShell`) | Linux Command (`Bash`) | Safety & Analytical Purpose |
| :--- | :--- | :--- | :--- |
| **Trace System & Library Calls (Non-Networked)** | `procmon64.exe /AcceptEula /Quiet /Minimized /BackingFile C:\Temp\trace.pml` | `strace -f -s 256 -o /tmp/strace.log '<BINARY>'` & `ltrace -f -s 256 -o /tmp/ltrace.log '<BINARY>'` | **Execute ONLY in an isolated `WHITE` air-gapped environment:** Captures runtime file, registry, socket, and library calls (e.g., `strcmp`, `memcpy`, decrypted buffers). |
| **Dump Unpacked Process Memory from RAM** | `procdump64.exe -ma <PID> C:\Temp\unpacked_<PID>.dmp /accepteula` | `gdb -batch -ex "attach <PID>" -ex "generate-core-file /tmp/unpacked.core" -ex "detach"` | Bypass static packers/crypters by dumping the process memory image after the original entry point (OEP) has unpacked in RAM, then feed the dump into `reait -b` / Ghidra. |
