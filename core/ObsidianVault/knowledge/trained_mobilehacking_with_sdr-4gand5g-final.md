---
title: "Trained Knowledge & Topology: MobileHacking_with_SDR-4Gand5G-final.pdf"
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
source_file: MobileHacking_with_SDR-4Gand5G-final.pdf
doc_type: pdf
updated: 2026-10-25 00:59:21
---

# Trained Knowledge & Architecture: `MobileHacking_with_SDR-4Gand5G-final.pdf`

- **Source Path:** `~/Projects/CORA/Training/MobileHacking_with_SDR-4Gand5G-final.pdf` (`pdf`)
- **Extracted Technical Entities:** `adb, cve-2012-6636, cve-2013-4710, http, https, serial, tls, ttyusb1`
- **Extracted IPs / Subnets:** `127.0.1.1, 127.0.1.100, 127.0.1.200, 172.16.0.2`
- **Extracted Interfaces:** `ttyUSB1, ttyUSB2`
- **Linked Command Playbook:** [[commands/trained_mobilehacking_with_sdr-4gand5g-final]] (`3` CEGAR-verified commands | `3` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `3` (full executable list in [[commands/trained_mobilehacking_with_sdr-4gand5g-final]])
- **Tactic Distribution:** `Enumeration` (2), `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `lte` (1), `nr` (1), `type` (1)

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page1`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[penthertz]`
  2. `[Mobile Hacking with]`
  3. `[SDR | 3G - 5G]`

### Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page2`)
- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**
  1. `[3G Radio]`

## LLM Distilled Operational Summary
### Operational Techniques & Decision Workflows
- **Modulation Selection Workflow**: Select modulation based on channel quality and generation:
  - **3G (UMTS)**: Default QPSK; upgrade to 16QAM (HSDPA) or 64QAM (HSDPA+) for high-speed data.
  - **4G (LTE)**: Scale from QPSK to 256/1024 QAM based on signal-to-noise ratio measurements.
  - **5G**: Support QPSK through 1024 QAM (Rel. 17) with CP-OFDM for downlink and DFT-s-OFDM for uplink.
- **Multiplexing Strategy**:
  - **Downlink**: Use OFDMA (4G) or CP-OFDM (5G) for high spectral efficiency.
  - **Uplink**: Prefer SC-FDMA (4G) or DFT-s-OFDM (5G) to minimize Peak-to-Average Power Ratio (PAPR).
- **Architecture Evolution**:
  - **5G NSA**: Retain legacy EPC core for backward compatibility.
  - **5G SA**: Deploy Software-Defined Network (SDN) with CUPS architecture for dynamic resource allocation and reduced OPEX.
- **Security Hardening**:
  - **3G Encryption**: Upgrade from vulnerable A5/1 or A5/2 to A5/3 (KASUMI, 128-bit key).
  - **GPRS Encryption**: Migrate from GEA0/GEA1 to GEA2 for enhanced stream cipher security.

### Critical Command Patterns & Required Flags
- **Signal Analysis Commands**:
  - `sdr# fft_view`: Trigger FFT visualization to inspect frequency domain occupancy.
  - `sdr# modulation_check`: Verify active modulation (QPSK/16QAM/64QAM) against expected standards.
- **Resource Block Configuration**:
  - `sdr# prb_config`: Set Physical Resource Block parameters (12 sub-carriers, 7 symbols normal CP).
  - `sdr# bandwidth_set`: Configure carrier width (e.g., 5 MHz for LTE, 25 MHz for 5G FDMA).
- **Security Mode Command**:
  - `bts# cipher_mode_cmd`: Instruct Base Transceiver Station to switch encryption algorithms (e.g., `A5/3` or `GEA2`).

### Network Topology & Service Relationships
- **3G Topology**: UMTS (Europe) / CDMA2000 (US); WCDMA spread spectrum with OVSF coding trees.
- **4G Topology**: LTE/E-UTRA with FDD (paired spectrum + diplexer) or TDD (shared timeslot) modes.
- **5G Topology**:
  - **NSA**: Integrated with 4G EPC core.
  - **SA**: Service-Based Architecture (SBA) involving UPF, SMF, PCF, AMF, and UDR functions.
- **Key Interfaces**: N1 (NAS signaling), N2 (Control Plane), N3 (User Plane) between UE and Core Network Functions.
- **Open

## Document Structure & Key Topics
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page1`)
- Visual & Network Diagram Intelligence (`MobileHacking_with_SDR-4Gand5G-final.pdf#page2`)
- eNB
- gNB
- echo -e 'AT+QLINUXCMD="/sbin/getty -L ttyGS0 115200
- microcom /dev/ttyUSB1

