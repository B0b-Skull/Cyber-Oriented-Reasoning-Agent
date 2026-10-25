---
title: "Trained Knowledge & Topology: BCF_Autopsy Internet Artifacts.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: BCF_Autopsy Internet Artifacts.pdf
doc_type: pdf
updated: 2026-10-25 00:56:22
---

# Trained Knowledge & Architecture: `BCF_Autopsy Internet Artifacts.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_Autopsy Internet Artifacts.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Internet and Browser]`
  2. `[Artifacts]`
  3. `[OVERVIEW]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Browser Artifact Analysis Workflow:**
    *   Identify the target operating system (Windows XP, Vista, 7) to determine the correct registry path or user profile structure.
    *   Locate specific artifact types: Cache (content), History (URLs), Cookies (session data), and Download files.
    *   Use specialized external viewers for visualization: `IECacheView` for Internet Explorer and `Firefox`'s `places.sqlite` for Mozilla Firefox.
    *   Export artifacts when possible to preserve state, as cached webmail messages are often overwritten quickly.
*   **Spatial Grouping Strategy:**
    *   Cluster findings by browser type (Internet Explorer, Firefox, Chrome) and then by OS version to normalize path discrepancies.
    *   Distinguish between "Local Settings" (XP) and "AppData" (Vista/7) directory structures.

### Critical Command Patterns & Required Flags
*   **Path Resolution Variables:**
    *   `%systemdir%`: System root directory.
    *   `%root%`: Root drive letter (e.g., `C:`).
    *   `%username%` / `%userprofile%`: Current user's profile name.
    *   `%PROFILE%`: Firefox-specific profile identifier.
*   **Key File Formats:**
    *   Firefox: `places.sqlite` (SQLite database format).
    *   IE/Chrome: Folder-based storage (`.ie5`, `.cache`, `.default`).

### Network Topology & Service Relationships
*   **Internet Explorer (IE):**
    *   **XP Path:** `%systemdir%\Documents and Settings\%username%\Local Settings\Temporary Internet Files\Content.ie5` and `Cookies`.
    *   **Vista/7 Path:** `%systemdir%\Users\%username%\AppData\Local\Microsoft\Windows\Temporary Internet Files\` (including `Low` subfolder) and `History`.
*   **Mozilla Firefox:**
    *   **XP Path:** `%root%/Documents and Settings/%userprofile%/Local Settings/Application Data/Mozilla/Firefox/Profiles/*.default/Cache`.
    *   **Vista/7 Path:** `C:\Users\%userprofile%\AppData\Local\Mozilla\Firefox\Profiles\%PROFILE%.default\Cache` and `Roaming` profile.
*   **Google Chrome:**
    *   **XP Path:** `%root%/Documents and Settings/%userprofile%/Local Settings/Application Data/Google/Chrome/User Data/Default/Cache`.
    *   **Vista/7 Path:** `%root%/Users\%username%\AppData\Local\Google\Chrome\User Data\Default\Preference`.
*   **Data Characteristics:**
    *   **Cached Browsing:** Contains actual page content and "read-only" webmail messages.
    *   **Volatility:** Cache data is overwritten rapidly; export is recommended for evidence preservation.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_Autopsy Internet Artifacts.pdf#page2`)

