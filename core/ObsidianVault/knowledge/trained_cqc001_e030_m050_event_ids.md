---
title: "Trained Knowledge & Topology: CQC001_E030_M050_Event_IDs.pdf"
tags:
  - https
  - mdp
  - pdf
  - trained
source_file: CQC001_E030_M050_Event_IDs.pdf
doc_type: pdf
updated: 2026-10-24 00:57:38
---

# Trained Knowledge & Architecture: `CQC001_E030_M050_Event_IDs.pdf`

- **Source Path:** `~/Projects/CORA/Training/CQC001_E030_M050_Event_IDs.pdf` (`pdf`)
- **Extracted Technical Entities:** `https`
- **Extracted IPs / Subnets:** `None`
- **Extracted Interfaces:** `None`

## LLM Distilled Operational Summary
### Key Operational Techniques & Decision Workflows
*   **Logon Failure Analysis**: Differentiate between authentication failures (Event 529: unknown user/bad password), policy violations (530: time restriction, 534: logon type), and account state issues (531: disabled, 532: expired, 535: password expired, 539: locked out).
*   **Successful Authentication Verification**: Confirm valid logons via Event 4624 (account) or 528 (interactive), and network logons via Event 540.
*   **Privilege & Service Monitoring**: Detect when privileged services are called (Event 577) or when the Windows Firewall service stops (5025) or changes settings (4950).
*   **Registry & Group Management**: Track registry modifications (4657) and security group changes, specifically adding members to enabled local groups (4732) or deleting disabled universal groups (4763).
*   **Firewall Traffic Control**: Monitor the Windows Filtering Platform permitting inbound connections (5154) and applications blocked from accepting traffic (5031).

### Critical Command Patterns and Required Flags
*   **Event ID Filtering**: Use `Event ID` filters in SIEM tools or PowerShell (`Get-WinEvent -FilterHashtable @{LogName='Security';Id=4624}`) to isolate specific security events.
*   **Credential Context**: Always cross-reference Event 529 (Failure) with Event 528/4624 (Success) to determine if a brute-force attack or a successful breach occurred.
*   **Firewall State Checks**: Correlate Event 5025 (Service Stopped) with Event 5031 (Blocked Application) to identify potential post-exploitation attempts to disable defenses.

### Network Topology & Service Relationships
*   **Service Dependency**: The **Windows Firewall Service** (Event 5025/5031) relies on the **Windows Filtering Platform** (Event 5154) to manage inbound connection permissions for applications and services.
*   **Domain Controller Interaction**: **NetLogon** component status (Event 536) indicates the health of domain trust relationships; failure here blocks logons even if credentials are correct.
*   **Local vs. Universal Groups**: Distinguish between **Security-Enabled Local Groups** (Event 4732) used for local machine access control and **Universal Groups** (Event 4763) often used in multi-domain environments.
*   **Registry Integrity**: The **Registry** (Event 4657) serves as the configuration store for many services, including Firewall rules and audit policies (Event 612).

