---
title: "Trained Knowledge & Topology: BCF_EnCase Navigation.pdf"
tags:
  - mdp
  - pdf
  - trained
source_file: BCF_EnCase Navigation.pdf
doc_type: pdf
updated: 2026-10-25 00:56:38
---

# Trained Knowledge & Architecture: `BCF_EnCase Navigation.pdf`

- **Source Path:** `~/Projects/CORA/Training/BCF_EnCase Navigation.pdf` (`pdf`)
- **Extracted Technical Entities:** `general`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

### Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[ICHIRON | TRAINING]`
  2. `[Basic Computer Forensics | 26-28Mar2018 | DISCOVERYANDCOUNTER-INFILTRATIONPROFESSIONALTM(DCIP)TM]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[EnCase | Tool navigation]`
  2. `[OVERVIEW]`

### Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[WCHIRON | TRAINING]`
  2. `[Filter Pane | What is it looking for?]`
  3. `[Edit "MS Word" | Conditions | Filters | Source Code | Name | M | f) Main | if File Ext equal to [doc]]`
  4. `[Report | and NotFullPath find [\Microsoft Office, \Temporary Internet Files, \C\IWindows, I.] | and Logical Size greater than [0]]`
  5. `[OK | Cancel]`
  6. `[DISCOVERYANDCOUNTER-INFILTRATION | PROFESSIONALTM(DCIP)TM | 2016 CHIRON TECHNOLOGY SERVICES,INC]`
  7. `[Basic Computer Forensics | Any unauthorized use or disclosure of this material is strictly prohibited.]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Case Initialization & Device Verification**: Verify the physical device status in the "Devices" tab. A blue triangle indicates a live device, while a red triangle indicates a remote preview. Ensure the hard drive status is "green-homeplated" before running conditions to confirm readiness.
*   **Filter Construction Workflow**:
    1.  Navigate to the **Filter Pane** and select **Conditions**.
    2.  Define the target file type (e.g., Microsoft Office) by editing the `File Ext` condition.
    3.  Refine the search path using `NotFullPath` to exclude system directories like `\Microsoft Office`, `\Temporary Internet Files`, and `\C\IWindows`.
    4.  Apply a size constraint using `Logical Size greater than [0]` to filter out empty files.
    5.  Execute the query; confirm activation by checking for a green "+" next to "Query" in the pane header.
*   **Report Generation**: Utilize the **Report** function within the Filter Pane to generate outputs based on active queries, specifically targeting file extensions and logical sizes.
*   **Advanced Parsing & EnScripts**: Use **EnScripts** for custom case processing (e.g., converting `.E01` images to DD format). Leverage **File Parsers** (EXIF Viewer, IM Archive Parser) for compound file analysis, noting that parsing PST/DBX/EDB files is memory-intensive and relies on the `ParseCache` subfolder.
*   **Record & Email Analysis**: Access the **Records** tab to view parsed email data (messages, attachments) from mounted compound files like PST or DBX.

### Critical Command Patterns & Required Flags
*   **File Extension Filter**: `if File Ext equal to [doc]` (Update to include `docx` for comprehensive coverage).
*   **Path Exclusion Logic**: `and NotFullPath find [\Microsoft Office, \Temporary Internet Files, \C\IWindows, I.]`.
*   **Size Constraint**: `and Logical Size greater than [0]`.
*   **Query Activation**: Toggle the green "+" indicator next to "Query" to enable/disable the active condition.

### Network Topology & Service Relationships
*   **Remote Device Indicators**: A **red triangle** on a device icon signifies a **remote preview of a live device over the network**, establishing a relationship between the local EnCase instance and a remote physical source.
*   **Secure Storage Dependencies**: Accessing encrypted data in system files and the Registry requires the **EDS certificate**, linking the `Secure Storage` view to specific cryptographic credentials.
*   **Compound File Mounting**: The **Records** tab relies on a cache file located in the `EnCase 6` folder (specifically the `ParseCache` subfolder) to mount and parse compound files like PST, DBX, and EDB.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page1`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page2`)
- Visual & Network Diagram Intelligence (`BCF_EnCase Navigation.pdf#page8`)

