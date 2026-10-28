---
title: "Trained Knowledge & Topology: _OS Internals__Kernel & Hardware.pdf"
tags:
  - mdp
  - passive_enum
  - pdf
  - serial
  - trained
source_file: _OS Internals__Kernel & Hardware.pdf
doc_type: pdf
updated: 2026-10-24 00:56:06
---

# Trained Knowledge & Architecture: `_OS Internals__Kernel & Hardware.pdf`

- **Source Path:** `~/Projects/CORA/Training/_OS Internals__Kernel & Hardware.pdf` (`pdf`)
- **Extracted Technical Entities:** `serial`
- **Extracted IPs / Subnets:** `0.0.1.33, 0.0.100.4, 0.15.0.2`
- **Extracted Interfaces:** `None`
- **Linked Command Playbook:** [[commands/trained_os_internals__kernel_hardware]] (`1` CEGAR-verified commands | `1` MDP transitions)

## Command & Tactic Coverage Summary
- **Total CEGAR-Verified Commands:** `1` (full executable list in [[commands/trained_os_internals__kernel_hardware]])
- **Tactic Distribution:** `Passive_Enum` (1)
- **Top Extracted CLI Tools:** `openssl` (1)

## LLM Distilled Operational Summary
### 1. Key Operational Techniques & Decision Workflows

*   **Boot Chain Execution Flow**: The application processor executes a sequential chain starting with the **SecureROM** image, followed by **LLB** (Low Level Boot), **iBSS** (Second Stage Boot), and finally **iBoot**, which loads the **kernelcache**. Failure at any stage transitions the device into **Recovery Mode** ("Connect to iTunes") or **USB-DFU** mode.
*   **Code Rebase Loop**: Upon loading, components check if the binary resides at a predefined address (e.g., `0x100000000` for A12 SecureROM). If not, the code is dynamically moved to the correct location before execution proceeds.
*   **Common Code Initialization**: All boot components share core initialization routines including CPU setup, Vector Base Address Register (VBAR) configuration, MMU setup, ARM MSRs, and task management for multithreading.
*   **Certificate-Based Verification**: Trust is established via a hard-coded root certificate burned into ROM. This certificate verifies the integrity of subsequent iBoot components and the kernelcache via digital signatures and APTicket entries.
*   **Image Format Handling**: 32-bit devices utilize **IMG3**, while 64-bit devices (and watches) use **IMG4** (DER format) to encode binaries and graphics.

### 2. Critical Command Patterns & Required Flags

*   **SecureROM Certificate Extraction**: Locate the Apple Secure Boot CA by searching for the specific DER encoding sequence `30 82 05 5a` (representing a SEQUENCE of 1,370 bytes) within a ROM dump or decrypted image.
*   **Decryption Keys**: For 64-bit iBoot images (iOS 10+), decryption requires device-specific **GID keys** and **IVs** (Initialization Vectors). These are often sourced from public repositories like the iPhone Wiki or NewOSXBook.com forums.
*   **Source Identification**: While exact versioning is obscured by external `#define` macros, board support files (e.g., `t8010`) and copyright dates (e.g., 2015) help correlate leaked sources (GitHub/Reddit) to specific hardware generations (e.g., iPhone 6S).

### 3. Network Topology & Service Relationships

*   **Firmware Partitioning**: Updatable boot components are extracted from the `.ipsw` file (specifically the `firmware/all_flash` directory) and copied to the device's **boot partition**.
*   **Component Evolution**: On A10 and later devices, the four distinct images (LLB, iBoot, iBEC, iBSS) have converged into a single unified iBoot image that handles all boot phases, though the image may still be tagged as `'illb'` rather than `'ibot'`.
*   **Security Architecture**: The chain of trust relies on the immutability of the ROM certificate. Once verified, this root of trust cascades through the boot stages to validate the kernelcache, forming the foundation for *OS security and runtime integrity.

## Document Structure & Key Topics
- Using openssl, parse the imag4 containers in the boot NVMe namespace,
- looking for the tags following the IM4P magic, but removing the magic
- and compare to fixed address (stored at 0x318, here 0x19c030000).
- _start:

