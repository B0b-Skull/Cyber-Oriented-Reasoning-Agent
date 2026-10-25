---
title: "Trained Command Playbook: Address_Space_Layout_Randomization.pdf"
tags:
  - enumeration
  - http
  - mdp
  - pdf
  - trained
source_file: Address_Space_Layout_Randomization.pdf
updated: 2026-10-25 00:56:07
---

# Trained Command Playbook: `Address_Space_Layout_Randomization.pdf`

- **Source Document:** `~/Projects/CORA/Training/Address_Space_Layout_Randomization.pdf`
- **CEGAR Verified Commands:** `30` (`0` malformed/unsafe snippets filtered)
- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `30`
- **Discovered IPs/Subnets:** `None`
- **Discovered Interfaces:** `None`
- **Related Knowledge Note:** [[knowledge/trained_address_space_layout_randomization]]

## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)
| Pre-State ($s$) | Tactic ($\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-1.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-2.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-3.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-4.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-5.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-6.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-7.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-8.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-9.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-A.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-B.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-C.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-D.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-E.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `copy` | `s_active_services_enumerated` | `Copy /Y ASLR.exe ASLR-F.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-1.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-2.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-3.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-4.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-5.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-6.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-7.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-8.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-9.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-A.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-B.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-C.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-D.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-E.exe` |
| `s_l2_l3_verified` | **`Enumeration`** | General System & Service Enumeration | `del` | `s_active_services_enumerated` | `Del ASLR-F.exe` |

## Verified Executable Commands (Grouped by Capability Layer)

### General_System (30 commands)
```bash
Copy /Y ASLR.exe ASLR-1.exe
Copy /Y ASLR.exe ASLR-2.exe
Copy /Y ASLR.exe ASLR-3.exe
Copy /Y ASLR.exe ASLR-4.exe
Copy /Y ASLR.exe ASLR-5.exe
Copy /Y ASLR.exe ASLR-6.exe
Copy /Y ASLR.exe ASLR-7.exe
Copy /Y ASLR.exe ASLR-8.exe
Copy /Y ASLR.exe ASLR-9.exe
Copy /Y ASLR.exe ASLR-A.exe
Copy /Y ASLR.exe ASLR-B.exe
Copy /Y ASLR.exe ASLR-C.exe
Copy /Y ASLR.exe ASLR-D.exe
Copy /Y ASLR.exe ASLR-E.exe
Copy /Y ASLR.exe ASLR-F.exe
Del ASLR-1.exe
Del ASLR-2.exe
Del ASLR-3.exe
Del ASLR-4.exe
Del ASLR-5.exe
Del ASLR-6.exe
Del ASLR-7.exe
Del ASLR-8.exe
Del ASLR-9.exe
Del ASLR-A.exe
Del ASLR-B.exe
Del ASLR-C.exe
Del ASLR-D.exe
Del ASLR-E.exe
Del ASLR-F.exe
```

