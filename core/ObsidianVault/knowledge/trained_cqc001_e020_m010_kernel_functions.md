---
title: "Trained Knowledge & Topology: CQC001_E020_M010_Kernel_Functions.pdf"
tags:
  - http
  - https
  - mdp
  - pdf
  - trained
source_file: CQC001_E020_M010_Kernel_Functions.pdf
doc_type: pdf
updated: 2026-10-25 00:57:31
---

# Trained Knowledge & Architecture: `CQC001_E020_M010_Kernel_Functions.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E020_M010_Kernel_Functions.pdf` (`pdf`)
- **Extracted Technical Entities:** `http, https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows

*   **Memory Management & Allocation**:
    *   **Contiguous Memory**: Use `AllocPhysMem` (Kernel-only) for physically contiguous blocks; release via `FreePhysMem`.
    *   **Virtual Mapping**: Create static mappings (`CreateStaticMapping`) for physical-to-virtual address translation; remove with `DeleteStaticMapping`.
    *   **Shared Memory**: Allocate read/write memory for the caller and read-only for others using `CeVirtualSharedAlloc`.
    *   **Page Fault Control**: Lock specific virtual address regions with `LockPages` to prevent swapping; force swap-out of discardable pages with `ForcePageout`.
    *   **Module Swapping**: Use `PageOutModule` to swap out all pages of a specific process or DLL.

*   **Cache & Memory Attributes**:
    *   **Cache Operations**: Flush specific ranges with `CacheRangeFlush` or the entire cache with `CacheSync`. Retrieve cache info via `CeGetCacheInfo`.
    *   **Hardware Attributes**: Apply hardware-specific memory attributes using `CeSetMemoryAttributes`.

*   **Interrupt Handling Workflow**:
    *   **Initialization**: Initialize hardware interrupts via `InterruptInitialize` and register ISRs using `HookInterrupt`.
    *   **Inter-Processor**: Install IPI handlers with `HookIPI`.
    *   **State Management**: Enable/Disable specific interrupts (`InterruptDisable`, `InterruptMask`) or toggle all (`INTERRUPTS_ON`, `INTERRUPTS_OFF`, `INTERRUPTS_ENABLE`).
    *   **Completion**: Signal ISR completion with `InterruptDone` and obtain the exception program counter (EPC) via `GetEPC`.

*   **Error Reporting & Profiling**:
    *   **Watson Dumps**: Manage error reporting dumps by clearing (`DrWatsonClear`), flushing (`DrWatsonFlush`), resizing, reading, or writing data.
    *   **Profiling**: Record samples via `ProfilerHit` (kernel) or `ProfilerHitEx` (OAL/ISR layer). Query profiler status with `ProfileCaptureStatus`.

### Critical Command Patterns & Required Flags

*   **Kernel-Only Functions**: Most low-level operations (e.g., `AllocPhysMem`, `CacheSync`, `HookInterrupt`) require execution in **Kernel Mode**.
*   **User-Mode Accessible**: Higher-level or coordination functions (e.g., `CeCallUserProc`, `CreateAPIHandle`, `GetCallerVMProcessId`) can be called from User Mode.
*   **Interrupt Prototypes**:
    *   `ISRHandler`: Prototype for OEM/IHV installable interrupt handlers.
    *   `PFN_UIENTRYPOINT`: Prototype for the UI proxy device driver entry point.
    *   `PFNAPIERRHANDLER`: Prototype for the API error handler.

### Network Topology & Service Relationships

*   **Device Drivers**: `CeCallUserProc` loads the User Interface (UI) proxy device driver.
*   **Standard I/O**: `GetStdioPathW` retrieves the device driver name used for standard input/output/error operations.
*   **Inter-Process Communication**: `ForwardDeviceIoControl` allows drivers to forward I/O controls to other drivers without validation when the current driver lacks context, preserving direct caller information for downstream

