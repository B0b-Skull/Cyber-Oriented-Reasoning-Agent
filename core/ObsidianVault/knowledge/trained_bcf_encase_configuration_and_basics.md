---
title: "Trained Knowledge & Topology: BCF_EnCase Configuration and Basics.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: BCF_EnCase Configuration and Basics.pdf
doc_type: pdf
updated: 2026-10-24 00:56:35
---

# Trained Knowledge & Architecture: `BCF_EnCase Configuration and Basics.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_EnCase Configuration and Basics.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[EnCase | Configuration]`
  2. `[OVERVIEW]`
  3. `[Adding Images | Pane Properties]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page3`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[Starting EnCase - Need Dongle]`
  3. `[F | EnCase Acquisition | File Edit View Tools Help | 港 New | Open]`
  4. `[EnCase Law Enforcement | File Edit  View Toos  Help | New  Open  Refresh]`
  5. `[Refresh]`
  6. `[Report | Code]`
  7. `[DISCOVERYANDCOUNTER-INFILTRATION | PROFESSIONALTM(DCIP)TM | @ 2016 CHIRON TECHNOLOGY SERVICES, INC.]`
  8. `[Basic Computer Forensics | Any unauthorized use or disclosure of this material is strictly prohibited.]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows

*   **Case Initialization:** Create a new case via `File > New`, defining the Case Name, Examiner Name, and file paths.
*   **Image Ingestion:**
    *   Navigate to `File > Add Raw Image`.
    *   Select all `.img` files (exclude `.txt` logs) and drag them into the "Component Files" window.
    *   Reorder images by highlighting them in reverse sequence to match the physical disk layout.
    *   Alternatively, use the "Add Device" tab for previously acquired hardware.
*   **File Viewer Configuration:**
    *   Access `View > File Viewers > New` to create custom viewers.
    *   Assign application paths (e.g., IrfanView for images, Firefox/Chrome for HTML).
    *   Configure `View > File Types` to override default OS rendering (e.g., set HTML to use Mozilla Firefox).
*   **Global Options Setup:**
    *   Enable "Auto Save" and configure "Picture Viewer" settings (ART Image, Timeout, Corrupted Image handling).
    *   Set "Show True/False" conditions to display "yes/no" values for clarity.
*   **Table Pane Optimization:**
    *   Right-click column headers to hide unnecessary columns, reorder, or lock specific columns.
    *   Utilize "Green Homeplate" in the Tree pane to expand/collapse directory structures.
    *   Use blue checkmarks in the Table pane to select files for bulk operations.

### Critical Command Patterns & Required Flags

*   **Menu Path for Images:** `File` → `Add Raw Image`
*   **Menu Path for Viewers:** `View` → `File Viewers` → `New`
*   **Menu Path for File Types:** `View` → `File Types`
*   **Menu Path for Global Settings:** `Options` → `Global` Tab
*   **Column Management:** Right-click column header → `Show Columns` (Uncheck desired)
*   **Selection Logic:** Highlight files in reverse order when adding multiple images to ensure correct chronological/physical sequence.

### Network Topology & Service Relationships

*   **Default Rendering Services:** EnCase defaults to the Windows OS application for rendering webpages and documents unless explicitly overridden via the `File Types` configuration.
*   **Recommended External Viewers:**
    *   **HTML:** Mozilla Firefox or Google Chrome.
    *   **Images (bmp, jpg, gif):** IrfanView.
    *   **Advanced Graphics (psd):** Adobe Photoshop or GIMP.
*   **Dongle Dependency:** The software requires a physical dongle to start the acquisition process.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page2`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Configuration and Basics.pdf#page3`)

