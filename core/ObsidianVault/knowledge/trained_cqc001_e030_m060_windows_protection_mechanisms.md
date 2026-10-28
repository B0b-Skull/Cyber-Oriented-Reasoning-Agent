---
title: "Trained Knowledge & Topology: CQC001_E030_M060_Windows_Protection_Mechanisms.pdf"
tags:
  - http
  - https
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M060_Windows_Protection_Mechanisms.pdf
doc_type: pdf
updated: 2026-10-24 00:57:39
---

# Trained Knowledge & Architecture: `CQC001_E030_M060_Windows_Protection_Mechanisms.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M060_Windows_Protection_Mechanisms.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **SFC (System File Checker) Execution Strategy**:
    *   Use `/SCANNOW` for immediate scanning and repair of all protected system files.
    *   Use `/FILESONLY` to restrict verification/repair to files only, excluding registry keys (note: unsupported on Windows XP).
    *   Use `/VERIFYFILE` or `/VERIFYONLY` for path-specific verification or full-system scan without repair.
    *   Use `/OFFBOOTDIR` and `/OFFWINDIR` for offline repair scenarios on Windows Server 2003/XP.
    *   Use `/PURGECACHE` to clear the file cache and force a full scan of protected system files (Server 2003/XP).
    *   Use `/SCANBOOT` to schedule a scan at the next boot (Server 2003/XP).

*   **DEP (Data Execution Prevention) Configuration Workflow**:
    *   **OptIn (Default)**: Enables DEP for limited system binaries; suitable for standard setups.
    *   **OptOut**: Enables DEP for all processes by default; allows manual exemption of specific programs via Control Panel or Application Compatibility Toolkit. Recommended for general compatibility needs.
    *   **AlwaysOn**: Provides full DEP coverage for the entire system without an exceptions list; overrides shims. Best for high-security environments.
    *   **AlwaysOff**: Disables DEP entirely; disables PAE mode unless explicitly enabled via Boot.ini.

### Critical Command Patterns & Required Flags

*   **SFC Commands**:
    *   `sfc /SCANNOW` (Immediate repair)
    *   `sfc /FILESONLY` (File-only repair)
    *   `sfc /VERIFYFILE <path>` (Verify specific file)
    *   `sfc /OFFBOOTDIR <dir>` (Offline boot directory)
    *   `sfc /OFFWINDIR <dir>` (Offline Windows directory)
    *   `sfc /PURGECACHE` (Clear cache and scan)

*   **DEP Configuration**:
    *   Managed via **System Properties** > **Advanced** > **Performance Settings** > **Data Execution Prevention** tab.
    *   Options: OptIn, OptOut, AlwaysOn, AlwaysOff.

### Network Topology & Service Relationships

*   **OS Version Dependencies**:
    *   **Windows Server 2003 / Windows XP**: Support `/OFFBOOTDIR`, `/OFFWINDIR`, `/PURGECACHE`, `/SCANBOOT`, `/SCANONCE`, `/FILESONLY`.
    *   **Windows Server 2008 / Windows Vista**: Do not support `/REVERT` or `/SCANONCE`.
*   **Hardware Dependency**:
    *   DEP hardware enforcement requires compatible processors.
    *   `AlwaysOff` configuration disables Physical Address Extension (PAE) mode unless `/PAE` is present in `Boot.ini`.

