---
title: "Trained Knowledge & Topology: MobileHacking_with_SDR-3Gand5G.pdf"
tags:
  - adb
  - cve-2012-6636
  - cve-2013-4710
  - enumeration
  - http
  - https
  - mdp
  - passive_enum
  - pdf
  - serial
  - tls
  - trained
  - ttyusb1
source_file: MobileHacking_with_SDR-3Gand5G.pdf
doc_type: pdf
updated: 2026-10-25 00:59:18
---

# Trained Knowledge & Architecture: `MobileHacking_with_SDR-3Gand5G.pdf`

- **Source Path:** `~/Projects/CORA/Training/MobileHacking_with_SDR-3Gand5G.pdf` (`pdf`)
- **Extracted Technical Entities:** `adb, cve-2012-6636, cve-2013-4710, http, https, serial, tls, ttyusb1`
- **Extracted IPs / Subnets:** `127.0.1.1, 127.0.1.100, 127.0.1.200, 172.16.0.2`
- **Extracted Interfaces:** `ttyUSB1, ttyUSB2`
- **Linked Command Playbook:** [[commands/trained_mobilehacking_with_sdr-3gand5g]] (`3` CEGAR-verified commands | `3` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `3` (full executable list in [[commands/trained_mobilehacking_with_sdr-3gand5g]])
- **Tactic Distribution:** `Enumeration` (2), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `lte` (1), `nr` (1), `type` (1)

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-3Gand5G.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[penthertz]`
  2. `[Mobile Hacking with]`
  3. `[SDR | 3G - 5G]`

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-3Gand5G.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[3G Radio]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
*   **Modulation Selection Workflow:** Select modulation schemes based on channel quality and network generation:
    *   **3G (UMTS):** Default QPSK; upgrade to 16QAM (HSDPA) or 64QAM (HSDPA+) for high-speed data in good conditions.
    *   **4G (LTE):** Adaptive selection from QPSK to 1024QAM (Rel. 15) based on signal measurement.
    *   **5G (NR):** Supports QPSK through 1024QAM (Rel. 17); choose between CP-OFDM (general use) and DFT-s-OFDM (uplink/low PAPR).
*   **Multiplexing Strategy:**
    *   **Downlink:** Use OFDMA (4G) or CP-OFDM (5G) for high throughput.
    *   **Uplink:** Use SC-FDMA (4G) or DFT-s-OFDM (5G) to reduce Peak-to-Average Power Ratio (PAPR).
*   **Network Architecture Decision:**
    *   **5G NSA (Non-Standalone):** Retain existing EPC core for compatibility.
    *   **5G SA (Standalone):** Deploy SDN-based CUPS architecture for flexible service instantiation and reduced OPEX.
*   **Security Assessment Workflow:** Evaluate cipher strength before interception:
    *   **3G (UMTS):** Check for A5/0 (none), A5/1 (vulnerable), A5/2 (broken/export), or A5/3 (KASUMI/128-bit).
    *   **2G/2.5G:** Check for GEA0 (none) or GEA1/GEA2 (LFSR-based, often broken).

### Critical Command Patterns & Concepts
*   **Spread Spectrum Decoding:** Apply OVSF (Orthogonal Variable Spreading Factor) tree logic to separate user codes in WCDMA.
*   **Resource Block Calculation:** For LTE, calculate Physical Resource Blocks (PRB) using 12 sub-carriers and 7 symbols (normal CP).
*   **Bandwidth Aggregation:** Configure carrier aggregation up to 640 MHz (3GPP Rel. 13) for 4G or 25 MHz FDMA+TDMA for 5G.

### Network Topology & Service Relationships
*   **3G Topology:** UMTS (Europe) / CDMA-2000 (US); typically 5–20 MHz bandwidth using WCDMA.
*   **4G Topology:** LTE/E-UTRA with FDD (paired spectrum requiring diplexers) or TDD (shared timeslot).
*   **5G Core Functions:**
    *   **UPF:** Handles UE-to-Internet connectivity and IP allocation.
    *   **SMF:** Manages sessions between UPF and PCF.
    *   **PCF/UDR:** Enforces policies and stores subscriber data.
    *   **AMF:** Handles registration and NAS signaling on N1.
*   **Open RAN:** Utilizes open-source software

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-3Gand5G.pdf#page1`)
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-3Gand5G.pdf#page2`)
- eNB
- gNB
- echo -e 'AT+QLINUXCMD="/sbin/getty -L ttyGS0 115200
- microcom /dev/ttyUSB1

