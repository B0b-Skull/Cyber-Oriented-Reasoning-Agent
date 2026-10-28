---
title: curl_playbook
category: commands
tags: [curl, http, api, scanning]
updated: 2026-10-22
---
# Valid `curl` Command Playbook

Backlink: [[00_MEMORY_INDEX]]

## Best-Practice `curl` Flags for Local Agent Execution
- Always include `-sS` (silent progress bar, but show errors), `-k` (allow self-signed lab certs), and `-L` (follow redirects).
- Use `--max-time 15` so unresponsive hosts never hang the agent.
- For headers only:
  ```bash
  curl -sS -k -L -I --max-time 15 "https://target/path"
  ```
- For JSON APIs (`GET`):
  ```bash
  curl -sS -k -L --max-time 15 -H "Accept: application/json" "https://target/api/v1/status"
  ```
- For JSON APIs (`POST`):
  ```bash
  curl -sS -k -L --max-time 15 -X POST -H "Content-Type: application/json" -d '{"key":"value"}' "https://target/api/v1/login"
  ```
- For Form Submissions (`application/x-www-form-urlencoded`):
  ```bash
  curl -sS -k -L --max-time 15 -X POST -d "username=admin&password=foo" "https://target/login"
  ```
