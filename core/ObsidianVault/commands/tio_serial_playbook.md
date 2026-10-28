---
title: tio_serial_playbook
category: commands
summary: Non-interactive tio 3.9 Lua --script patterns for logging into and running commands on /dev/ttyUSB0 without Python scripts
tags: [tio, serial, ttyusb0, console, login]
updated: 2026-10-22
---
# `tio` Serial Console Playbook (`/dev/ttyUSB0`)

> **Summary:** Non-interactive `tio 3.9` Lua `--script` patterns for `/dev/ttyUSB0` & `/dev/ttyUSB1`  
> **Backlink:** [[00_MEMORY_INDEX]]

## Critical Rules for LLM Agent Execution
1. **NEVER write or run `python3` scripts for `/dev/ttyUSB0`.** Always use `tio`.
2. **Why plain `tio /dev/ttyUSB0` or `echo ... | tio /dev/ttyUSB0` fails in `run_shell_command`:**
   - When `stdin` is not a TTY, `tio 3.9` enters `Non-interactive mode` and exits **1 millisecond** after `stdin` hits `EOF`—before the serial device can send any reply.
3. **Solution — Always use `tio -b 115200 -o 15 -O 120 --mute --script-run once --script '<lua>' /dev/ttyUSB0`:**
   - `tio` runs the `--script` Lua commands (`write`, `expect`, `read`, `msleep`, `exit(0)`) synchronously while capturing all serial output to `stdout`, then exits cleanly when `exit(0)` is called.
4. **ANTI-DROP PACING RULE (Preventing UART FIFO Overrun & Console Disconnects):**
   - Embedded UART consoles have small 16–64 byte RX buffers. Bombarding `/dev/ttyUSB0` with chained commands (`cmd1; cmd2; cmd3`) or back-to-back `write()` calls without delay drops the console connection and returns 0 bytes!
   - **Always pass `-o 15 -O 120`** (15ms character delay, 120ms line delay) and **send ONLY 1 short command per `write()`** followed by `msleep(500)` and `while read(4096, 600) > 0 do end`.

---

## 1. Probe / Wake the Serial Console (See Current Prompt)
Check whether the console is at `login:`, `Password:`, or already logged in at a `#` / `>` / `$` prompt:
```bash
tio -b 115200 -o 15 -O 120 --mute --script-run once --script '
write("\r")
msleep(400)
while read(4096, 600) > 0 do end
exit(0)
' /dev/ttyUSB0
```

---

## 1b. Direct Password-Only Login + Single Paced Command (When Console Has No Traditional `login:` Prompt)
When the serial console only requires typing a password directly (without a `login:` prompt) to log in:
```bash
tio -b 115200 -o 15 -O 120 --mute --script-run once --script '
write("\r")
while read(4096, 400) > 0 do end
write("PASSWORD_HERE\r")
msleep(600)
while read(4096, 600) > 0 do end
write("id\r")
while read(4096, 600) > 0 do end
exit(0)
' /dev/ttyUSB0
```

---

## 2. Smart Auto-Login (Handles `login:`, Stuck `Password:`, or Already Logged In)
Note: Do **not** `expect("login:")` after sending the password, because the MOTD banner prints `Last login: ...` which contains `"login:"`. Wait for the shell prompt `(#|>|\\$)` instead:
```bash
tio -b 115200 -o 15 -O 120 --mute --script-run once --script '
write("\r")
local r, m = expect("([Ll]ogin:|[Uu]sername:|[Pp]assword:|#|>|\\$)", 3000)
if r == 1 and m and (string.find(m, "ogin") or string.find(m, "sername")) then
  write("USERNAME\r")
  r, m = expect("([Pp]assword:|#|>|\\$)", 3000)
end
if r == 1 and m and string.find(m, "assword") then
  write("PASSWORD\r")
  expect("(#|>|\\$)", 4000)
  while read(4096, 300) > 0 do end
end
exit(0)
' /dev/ttyUSB0
```

---

## 3. Run a Single Paced Command on an Already-Logged-In Console
Send ONE command (always terminate with `\r`), wait for output, and drain until quiet:
```bash
tio -b 115200 -o 15 -O 120 --mute --script-run once --script '
write("\r")
msleep(300)
write("id\r")
while read(4096, 600) > 0 do end
exit(0)
' /dev/ttyUSB0
```

---

## 4. Login + Run Command in One Step
```bash
tio -b 115200 --mute --script-run once --script '
write("\r")
local r, m = expect("([Ll]ogin:|[Uu]sername:|[Pp]assword:|#|>|\\$)", 3000)
if r == 1 and m and (string.find(m, "ogin") or string.find(m, "sername")) then
  write("USERNAME\r")
  r, m = expect("([Pp]assword:|#|>|\\$)", 3000)
end
if r == 1 and m and string.find(m, "assword") then
  write("PASSWORD\r")
  expect("(#|>|\\$)", 4000)
  while read(4096, 300) > 0 do end
end
write("COMMAND_HERE\r")
while read(4096, 500) > 0 do end
exit(0)
' /dev/ttyUSB0
```

---

## `tio 3.9` Lua Script API Reference
- `write("text\r")` — Send string to serial port (use `\r` for Enter on serial consoles).
- `expect("regex", timeout_ms)` — Wait up to `timeout_ms` for regex match. Returns `1, matched_str` on match, `0` on timeout.
- `read(max_bytes, timeout_ms)` — Read up to `max_bytes` within `timeout_ms` (all read bytes are printed to `stdout`).
- `msleep(ms)` / `sleep(sec)` — Pause execution.
- `exit(0)` — Cleanly disconnect `tio` and return output to shell.
