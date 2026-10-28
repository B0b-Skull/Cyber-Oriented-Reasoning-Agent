# CORA Isolated Project Workspaces & Continual Tactical Growth (`Projects/`)

![Two-Tier Memory Isolation & Continual Tactical Growth](../core/Explained/assets/two_tier_memory_and_tactical_growth.svg)

---

## 1. Architectural Purpose: Isolating Local Network Data While Growing Global Tactics

`CORA` separates **environment-specific project data** from **universal long-term knowledge and tactical policy learning** so that:
1. **Zero Dirty Knowledge Leakage:** Local host IPs, MAC addresses, ARP tables, downloaded payloads, temporary test scripts, and target scan reports are trapped inside `CORA/Projects/<project_name>/` and **never** pollute `core/ObsidianVault/` (`00_MEMORY_INDEX.md`, `00_TRAINED_INDEX.md`, `commands/`, `knowledge/`).
2. **Continuous Tactical & Process Improvement:** Every command executed during a project still updates the 15-Engine Reasoning Suite's mathematical policies (`core/Reasoning/data/`) using **symbolic, IP-abstracted templates (`<TARGET_IP>`, `<REMOTE_SUBNET>`, `$PROJECT_DIR`)** — so the LLM continuously improves *how* it approaches questions and multi-step testing without remembering dirty local IPs.

```mermaid
flowchart LR
    subgraph CLI["🧠 CORA Agent CLI (`core/agent-cli.py`)"]
        Exec["Tool Execution\n`run_shell_command` | `scan_target`\n`project_tracker` | `vault_save_note` | `write_file`"]
    end

    subgraph Tier2["📁 Tier-2: Isolated Project Workspace (`Projects/<project_name>/`)"]
        Mem["`memory.md`\nProject Plan, Verified Data,\n`/goal` Attempt Ledger & Index"]
        DL["`downloads/` & `artifacts/`\n`curl -o`, `wget -O`, `/tmp/*` redirects\n& temporary test scripts"]
        Tgt["`targets/`\n`scan_target` reports & live host\n`local_network_topology.md`"]
        Notes["`notes/` & `reasoning/`\nSession `vault_save_note` & `pipeline15_*`"]
    end

    subgraph Gate["🛡️ Symbolic Parameterization Gate"]
        Param["`_parameterize_tactical_template()`\n`172.24.x.y` -> `<TARGET_IP>`\n`/home/...` -> `$PROJECT_DIR`\n12-Bit Symbolic OSI State `S_<Cluster>::<Stage>`"]
    end

    subgraph Tier1["🗂️ Tier-1: Universal Long-Term Memory & Tactical Policies"]
        Vault["`ObsidianVault/` (Clean & Portable)\nUpdated ONLY by `/train` & `/remember`\n208 Trained Handbooks / 346 Notes"]
        MDP["Engine 11 H-MDP (`mdp_transitions.json`)\nDirichlet `α_success / α_fail` & Bellman `Q*(s,a)`\nacross 5,039 abstract tactical transitions"]
        RL["Engine 14 Trajectory RL (`rl_policy_table.json`)\nOnline `TD(λ)` Pessimistic `Q_LCB` across\n12-bit OSI stages (`L1 -> L2 -> L3 -> L4 -> L7`)"]
        CBR["Engine 12 Continual CBR (`learned_cbr_cases.json`)\nAuto-synthesized `<TARGET_IP>`\nFailure -> Fix remediation rules"]
        Meta["Engines 5 & 13 (`somatic_markers` & `meta_weights`)\nDamasio Somatic Valence & Hedge Engine Trust"]
    end

    Exec -->|"Raw Target Scans, Downloads,\nHost Topology & Project Notes"| Tier2
    Exec -->|"Command Exit Code,\nSyGuS Facts & State Delta"| Gate
    Gate -->|"IP-Abstracted Templates\n& Symbolic OSI Transitions"| MDP
    Gate --> RL
    Gate --> CBR
    Gate --> Meta
    Train["📚 `/train` & `/remember`"] -->|"Universal Playbooks & Rules"| Vault
```

---

## 2. Mandatory Startup Project Selection, Rename & Creation Menu (`Projects/<project-name>/`)

When starting the **C.O.R.A. (Cyber Oriented Reasoning Agent)** CLI (`./run_cora_NIX.sh` or `.\run_cora_WIN.ps1`) or Web Interface (`./run_cora_NIX.sh start` or `.\run_cora_WIN.ps1 start`), C.O.R.A. requires a project in `CORA/Projects/` to be selected or created and a session Personality Mode (`Default`, `Analyst`, `Berserker`, or `Ninja`) to be chosen before displaying the main C.O.R.A. login banner (`core/Explained/assets/CROW_Logo-NoWords_Transparent_Glow-NoBackground.png`) and interacting with the LLM:

1. **`[1 .. N]` Existing Projects:** Lists every project directory currently inside `CORA/Projects/` assigned a number.
2. **`[N + 1] Rename Current Project`:** Placed directly above `CREATE NEW PROJECT`. Opens a secondary screen where you select the number of the project to rename (with `[B] Go Back` and `[C] CANCEL` options) and enter the new project name.
3. **`[N + 2] CREATE NEW PROJECT`:** Always the very last numbered item on the list. Prompts for a new project name (with `[B] Go Back` and `[C] CANCEL` options), automatically converts any spaces, strange characters, or special characters to dashes (`-`), creates `CORA/Projects/<new-project-name>/`, and locks all files, target scans, downloads, and `memory.md` to that workspace.

You can also open this interactive menu at any time inside the CLI with `/project` (or `/project menu`), or pass `-h` to any switch (`/project -h`) to view all options.

Whenever `CORA` works on a project (`/project <doc_or_dir> [name]` or `project_tracker`) or runs an active test session (`Projects/active_session/`), [`ensure_project_workspace()`](../core/agent-cli.py) automatically creates:

```text
CORA/Projects/<project_name>/
├── memory.md        # Project-specific memory, verified architecture, open questions, task checklist & note index
├── goals.md         # Chronological project goals file (every new /goal is appended; /goal displays the very last goal)
├── REPORT.md        # 5-Section Status & Findings Report (Executive Summary, High-School Overview, SVG/Mermaid & Technical Write-Up)
├── assets/          # Auto-generated standalone SVG dashboards (report_dashboard.svg)
├── reports/         # Dated historical snapshots of generated project reports (<date>_<project>_Status_Report.md)
├── downloads/       # All files downloaded via curl -o, wget -O, or redirected from /tmp/<filename>
├── targets/         # Target HTTP/API scan reports (scan_target) & live host local_network_topology.md
├── notes/           # Session/project findings saved via vault_save_note
├── reasoning/       # Session-specific 15-Engine Neuro-Symbolic diagnostic reports (pipeline15_*)
└── artifacts/       # Temporary scripts or test files created for the current project
```

When a goal is set inside a project (`/goal "<objective>"` or `/relentless "<objective>" -max:100`), it is automatically appended chronologically to `CORA/Projects/<project_name>/goals.md` (`### Goal #N — <timestamp>`). Running `/goal` (or `/goal status`) displays the **very last goal** from that project's `goals.md` file, while `/goal list` displays all historical goals for the project.

To generate or refresh a project's report at any time inside the CLI, type:
```text
You> /generate-report
You> /generate-report <project_name_or_focus>
You> /generate-report fast
```

---

## 3. How Tactical & Process Growth Works Without Dirty Knowledge

| Learning Mechanism | File Updated in `Reasoning/data/` | What It Learns From Every Test / Project | Why Zero Dirty IPs Are Stored |
| :--- | :--- | :--- | :--- |
| **1. Hierarchical Tactical MDP (`Engine 11`)** | `mdp_transitions.json` (`5,039` transitions across 14 tactics) | Updates Dirichlet $\alpha_{\text{success}}$ / $\alpha_{\text{fail}}$ and Bellman $Q^*(s,a)$ values based on which tactic/tool succeeded or failed. | Transitions are keyed by abstract tactic (`Out-of-Band_Access -> tio`, `Reconnaissance -> nmap -Pn <TARGET_IP>`), never concrete IPs. |
| **2. Multi-Step Trajectory RL (`Engine 14`)** | `rl_policy_table.json` | Learns multi-step OSI troubleshooting sequences (`L1 -> L2 -> L3 -> L4 -> L7`) via `TD(λ)` eligibility traces and Pessimistic $Q_{\text{LCB}}$. | States are encoded as 12-bit topology-invariant OSI vectors (`S_<Cluster>::<Stage>`). |
| **3. Autonomous Failure $\rightarrow$ Fix CBR (`Engine 12`)** | `learned_cbr_cases.json` | When a failed command is followed by a working remediation command, synthesizes a reusable `CBR-AUTO-*` rule. | [`_parameterize_tactical_template()`](../Reasoning/engines/continual_learner.py) replaces all concrete IPv4 addresses with `<TARGET_IP>` and local paths with `$PROJECT_DIR`. |
| **4. Somatic Intuition & Hedge Calibration (`Engines 5 & 13`)** | `somatic_markers.json` & `meta_weights.json` | Penalizes rabbit-hole command loops (Damasio Somatic Valence) and increases voting weight for the most accurate engines (Brier/ECE Hedge). | Tracks abstract command binaries, symptom tags, and per-engine Brier calibration scores. |
| **5. Universal Knowledge Distillation (`/train` & `/remember`)** | `ObsidianVault/` (`00_TRAINED_INDEX.md`, `00_MEMORY_INDEX.md`) | Distills reference books, PDFs, cheat sheets, and explicit `/remember <fact>` commands into permanent Vault playbooks. | Explicitly curated universal knowledge; isolated from runtime project scans and temporary downloads. |
