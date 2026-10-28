---
title: "Trained Knowledge & Topology: MobileHacking_with_SDR-2G-part.pdf"
tags:
  - cve-2012-6636
  - cve-2013-4710
  - docker
  - enumeration
  - https
  - mdp
  - pdf
  - trained
  - wireshark
source_file: MobileHacking_with_SDR-2G-part.pdf
doc_type: pdf
updated: 2026-10-24 00:59:14
---

# Trained Knowledge & Architecture: `MobileHacking_with_SDR-2G-part.pdf`

- **Source Path:** `~/Projects/CORA/Training/MobileHacking_with_SDR-2G-part.pdf` (`pdf`)
- **Extracted Technical Entities:** `cve-2012-6636, cve-2013-4710, docker, https, wireshark`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_mobilehacking_with_sdr-2g-part]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_mobilehacking_with_sdr-2g-part]])
- **Tactic Distribution:** `Enumeration` (1)
- **Top Extracted CLI Tools:** `python` (1)

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[penthertz]`
  2. `[Mobile Hacking | 2G part]`

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page4`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Introduction]`

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page8`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[Introduction | Evolution]`
  2. `[Mobile network → more than 40 years]`
  3. `[1G-TACS/AMPS]`
  4. `[2G-GSM/GPRS/EDGE | 3G-WCDMA/UMTS/HSPA/HSPA+]`
  5. `[4G-LTE/LTEAdvanced/LTEAdvancedPro | 2010]`
  6. `[Research | Industry | 1980]`
  7. `[5G-LTE/5G-NR | 2020 | 2030]`
  8. `[1990 | 2000]`
  9. `[penthertz.com]`
  10. `[penthertz 1 8]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Threat Modeling**: Identify risks associated with Over-The-Air (OTA) attacks including eavesdropping, replay, injection, relay, jamming, and Denial-of-Service (DoS) via high-amplitude transmission.
- **Target Scope Definition**: Focus on access controls, mobile phones, navigation systems, autonomous vehicles, and industrial IoT components.
- **Regulatory Compliance Check**: Verify frequency band licensing requirements (e.g., ANFR, FCC) before deploying transmitters, noting exemptions for specific equipment like Wi-Fi or telemetry.
- **Technology Selection**: Choose between circuit-switched (GSM) and packet-switched (GPRS/EDGE) networks based on the target's service type, acknowledging that radio physics remain similar across 2G variants.

### Critical Command Patterns & Concepts
- **Modulation & Multiplexing**: Utilize GMSK modulation for standard 2G/2.5G and 8PSK for EDGE. Apply Frequency Division Multiple Access (FDMA) combined with Time-Division Multiple Access (TDMA) within 25 MHz bandwidths.
- **TDMA Frame Structure**: Configure signals into frames of 8 timeslots, where each time-slot contains 156.25 symbols at a transmission rate of 270.83 kbits/s.
- **Logical Channel Interactions**:
  - *Broadcast Channels*: Use FCCH for oscillator tuning, SCH for frame synchronization (BSIC), and BCCH for network identity (MCC/MNC/CGI) verification against SIM data.
  - *Common Control Channels*: Monitor PCH for incoming calls, RACH for mobile-originated requests, AGCH for access grants, and CBCH for cell broadcast messages.
  - *Dedicated Control Channels*: Leverage SDCCH for call setup and SACCH for control/supervisory signaling.

### Network Topology & Relationships
- **Global vs. Regional Standards**: While GSM/GPRS/EDGE/EGPRS are worldwide, the US utilizes CDMA. European implementations specifically use GMSK modulation and FDMA/TDMA multiplexing.
- **Evolutionary Timeline**: The mobile network has evolved from 1G (TACS/AMPS) through 2G (GSM), 3G (WCDMA/UMTS), 4G (LTE), to 5G (NR), spanning from the 1980s to the 2030s.
- **Device-Network Interaction**: The Mobile Station (MS) must successfully tune to the RF carrier (via FCCH), synchronize to the physical slot (via SCH), and verify network identity (via BCCH/SIM comparison) before establishing a connection.

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page1`)
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page4`)
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-2G-part.pdf#page8`)
- associating attacker IMSI with a resident number

## Extracted Operational Steps & Workflows
- 1. Get the TMSI of the victim
- 2. Analyze the cell you and the victim are camping on
- 3. Capture traffic and use the results of your analysis to construct
- 4. Use Kraken to crack the key
- 5. Use the key to decode the data you captured

