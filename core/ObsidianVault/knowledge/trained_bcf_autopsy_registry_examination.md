---
title: "Trained Knowledge & Topology: BCF_Autopsy Registry_Examination.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: BCF_Autopsy Registry_Examination.pdf
doc_type: pdf
updated: 2026-10-24 00:56:28
---

# Trained Knowledge & Architecture: `BCF_Autopsy Registry_Examination.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Autopsy Registry_Examination.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Registry_Examination.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018]`
  3. `[DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Registry_Examination.pdf#page5`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Registry Hive Extraction:** Identify the target hive file within the `C:\Windows\System32\config` directory (specifically `Software`, `Security`, `System`, or `SAM`).
*   **Tool Selection:** Utilize **AccessData Registry Viewer** (also referred to as AD Reg Viewer) for analysis.
*   **Workflow Execution:**
    1.  Import the target image into **Autopsy**.
    2.  Execute the registry examination plugin/module within Autopsy to export the specific hive file.
    3.  Navigate to the Autopsy export folder.
    4.  Launch **AccessData Registry Viewer** and open the extracted `.hve` or `.reg` file directly from the export directory.

### Critical Command Patterns & Required Flags
*   **Autopsy Plugin Execution:** While specific CLI flags vary by version, the core action involves selecting the "Registry Examination" plugin within the Autopsy interface to target a specific hive path.
*   **File Path Pattern:** `C:\Windows\System32\config\[Software|Security|System|SAM]`
*   **Viewer Launch Command (Conceptual):** `AccessData_Registry_Viewer.exe [Path_to_Exported_Hive_File]`

### Network Topology & Service Relationships
*   **Primary Software Ecosystem:** The workflow relies on the **Autopsy** platform (specifically the DCIP/ICHIRON or WCHIRON training modules) integrated with **AccessData** proprietary tools.
*   **Service Relationship:** The `AccessData Registry Viewer` acts as a secondary visualization layer for data extracted by Autopsy, enabling deep inspection of Windows registry structures without requiring a live OS mount.
*   **Training Context:** The procedures are part of the **Discovery and Counter-Infiltration Professional (DCIP)** curriculum, focusing on forensic artifact recovery from standard Windows system hives.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Autopsy Registry_Examination.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Autopsy Registry_Examination.pdf#page5`)

