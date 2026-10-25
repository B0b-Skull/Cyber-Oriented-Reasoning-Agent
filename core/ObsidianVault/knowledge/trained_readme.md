---
title: "Trained Knowledge & Topology: README.md"
tags:
  - cegar
  - enumeration
  - mdp
  - powershell
  - sysinternals
  - text
  - trained
source_file: README.md
doc_type: text
updated: 2026-10-25 01:00:16
---

# Trained Knowledge & Architecture: `README.md`

- **Source Path:** `~/Projects/CORA/Training/README.md` (`text`)
- **Extracted Technical Entities:** `cegar, powershell, sysinternals`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_readme]] (`2` CEGAR-verified commands | `2` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `2` (full executable list in [[commands/trained_readme]])
- **Tactic Distribution:** `Enumeration` (2)
- **Top Extracted CLI Tools:** `run_cora_NIX.sh` (1), `train_llm_NIX.sh` (1)

## LLM Distilled Operational Summary
# CORA Training Corpus (`v3.6.1`)

## Operational Techniques & Workflows
*   **Ingestion Workflow**: Drop any technical documentation, runbooks, cheat sheets, scripts, PDFs, Word documents, or network architecture diagrams into the `Training/` folder (or its subfolders).
*   **Execution Trigger**: Run the specific management script to initiate training based on the operating system.

## Critical Command Patterns
*   **Linux Execution**:
    ```bash
    ./run_cora_NIX.sh -train Training
    ```
*   **Windows Execution**:
    ```powershell
    .\run_cora_WIN.ps1 -train Training
    ```

## Network Topology & Service Relationships
*   **Primary Script**: `run_cora_NIX.sh` (Linux) or `run_cora_WIN.ps1` (Windows).
*   **Input Directory**: `Training/` (supports recursive subfolders).
*   **Supported File Types**: `.md`, `.txt`, `.pdf`, `.docx`, `.sh`, `.ps1`, `.py`, `.json`, `.yaml`, `.xml`, `.png`, `.jpg`, `.svg`.
*   **Default Output**: `CORA/` (contains the trained playbooks, rules, and metadata).

## Document Structure & Key Topics
- CORA Training Corpus (`v3.6.1`)
- Option 1: Via run_cora_NIX.sh (Linux) or run_cora_WIN.ps1 (Windows)
- Option 2: Standalone Linux / Windows script
- Option 3: Inside the interactive You> CLI
- Supported File Formats & Multi-Modal Extraction
- How the 4-Phase Distillation & Verification Pipeline Protects Reasoning Integrity

## Extracted Operational Steps & Workflows
- 1. **Zero Context Window Bloat**: Raw documents are never dumped into the live chat prompt. Instead, they are distilled into atomic, frontmatter-indexed notes inside `ObsidianVault/knowledge/trained_*.md` and `ObsidianVault/commands/trained_*.md`.
- 2. **Cross-Platform Engine 12 CEGAR Gatekeeper**: Every extracted command is verified against **Engine 12 (`cegar_verifier.py`)** before being stored (`bash -n` for Linux/POSIX commands; balanced-parenthesis and `-n` ping flag verification for Windows CMD, Sysinternals, Active Directory, and PowerShell commands). Dangerous, syntax-broken, or hallucinated commands are quarantined and never reach the active playbook library.
- 3. **Per-File SHA-256 + `extractor_v2` Manifest & Cached LLM Summary Reuse**: `Reasoning/data/training_manifest.json` checkpoints the SHA-256 hash and `extractor_v2` flag after every single file in `Training/`. Re-running `./run_cora_NIX.sh -train` only processes new or modified files, and when upgrading previously trained files to a newer extractor version, it reuses the cached `## LLM Distilled Operational Summary` from `ObsidianVault/knowledge/trained_*.md` so upgrades finish in milliseconds per file (use `--force` to re-run LLM summaries from scratch).
- 4. **Structured 15-Engine Reasoning & Tactical MDP Sync**: Verified troubleshooting signatures, multi-step command primitives, and hierarchical `(State -> Tactic -> Technique -> Tool -> Command -> Next State)` transitions are automatically merged into `Reasoning/data/trained_rules.json` (**Engine 11 CBR** & **Engine 14 MAP-Elites**) and `Reasoning/data/mdp_transitions.json` (**Engine 15 Hierarchical Tactical MDP**).
