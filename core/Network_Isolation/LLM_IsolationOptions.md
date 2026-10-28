# CORA Network Isolation Options (`LLM_IsolationOptions.md`)

To guarantee that your CORA setup (`llama-server`, `agent-cli.py`, and Open WebUI) can never send or receive data over the broader internet once installed—while still functioning normally on your local machine or an isolated lab network—you can enforce isolation at four different layers of the Linux operating system.

---

## 1. Loopback-Only Binding (Inbound Protection)
* **How it works:** The LLM server (`127.0.0.1:8080`) and Open WebUI (`127.0.0.1:3000`) are bound strictly to the local loopback address (`127.0.0.1`) rather than all interfaces (`0.0.0.0`).
* **What it prevents:** The Linux kernel will only accept connections originating from inside your own laptop. Nothing on your Wi-Fi, LAN, or the internet can connect inward to those ports.
* **Limitation:** Binding to `127.0.0.1` stops *inbound* connections, but by itself it does not stop a local process (or a shell command triggered by the agent) from initiating an *outbound* connection to the internet. For outbound guarantees, use one of the kernel-level controls below.

---

## 2. Linux Network Namespaces (Total Air-Gap for the Process)
* **Implemented by:** [`LLM_NetworkNamespaceSetup_NIX.sh`](./LLM_NetworkNamespaceSetup_NIX.sh)
* **How it works:** Linux allows you to start the LLM server and CLI inside a private **network namespace** (`ip netns` / `unshare`). Inside this namespace, the only network adapter that exists by default is a virtual loopback interface (`lo` / `127.0.0.1`)—your Wi-Fi card, WAN interfaces, and default internet gateway are completely invisible to the LLM and any child shell commands it spawns.
* **Why it is ideal for CORA:**
  * The CLI and `llama-server` can still communicate with each other over `127.0.0.1:8080`.
  * The LLM still has full access to your local filesystem, Obsidian Vault, USB serial consoles (`/dev/ttyUSB0`, `/dev/ttyUSB1`), CPU, and NVIDIA GPU (since GPU access happens through `/dev/nvidia*` device files, not the network stack).
  * Even if the LLM attempts to run `curl`, `wget`, or a Python script to reach an external IP address or DNS server, the kernel immediately returns `Network is unreachable` because no route to the internet exists in that namespace.

---

## 3. Host Firewall Filtering by Group & Interface (`iptables` / `ip6tables`)
* **Implemented by:** [`LLM_NetworkIsolationSetup_NIX.sh`](./LLM_NetworkIsolationSetup_NIX.sh)
* **How it works:** If you want the LLM Agent CLI to communicate **only** over specific local lab interfaces (`eth0`, `eth1`, `eth2`), local loopback (`lo`), and local USB serial consoles (`/dev/ttyUSB0`, `/dev/ttyUSB1` / `/dev/tty/usb0`, `/dev/tty/usb1`) while strictly blocking all internet-facing interfaces (such as Wi-Fi `wlan0`, WAN gateways, or VPN/tunnel interfaces):
  * **Group-Based Firewalling (`-m owner --gid-owner llm-local`):** A dedicated Linux group (`llm-local`) is created, and the LLM processes are launched under that primary group (`sg llm-local -c ...`).
  * **Strict Interface Whitelist:** In the Linux kernel firewall (`OUTPUT` chain), packets originating from `--gid-owner llm-local` are explicitly allowed **only** on `lo`, `eth0`, `eth1`, and `eth2`, and **rejected/dropped on all other interfaces** (both IPv4 and IPv6).
  * **USB Console Access:** The script also grants read/write ACLs on `/dev/ttyUSB0`, `/dev/ttyUSB1`, `/dev/tty/usb0`, and `/dev/tty/usb1` to the `llm-local` group so the LLM can interact with local serial consoles while remaining blocked from the internet.

---

## 4. Systemd Cgroup IP Sandboxing (`IPAddressDeny`)
* **How it works:** If you run the LLM service under `systemd`, `systemd` can attach a kernel eBPF socket filter to the service's control group (cgroup).
* **Configuration concept:** You set the service policy to **Deny All IP Addresses** (`IPAddressDeny=any`) and explicitly **Allow Only `localhost`** (and optionally your local lab subnet).
* **What it guarantees:** Every process inside that service—including `llama-server`, `agent-cli.py`, and any bash command spawned by the agent—is governed by the same cgroup filter. Any attempt to open a socket to a public internet IP is blocked inside the kernel before a single packet can be transmitted.

---

## Summary: Which Isolation Switch or Script to Use

| Switch / Script | Best Use Case | What Is Allowed | What Is Blocked |
| :--- | :--- | :--- | :--- |
| **`./run_cora_NIX.sh cli -m 3.8 -netiso red`**<br>*(or `--network-isolation red` / `-red`)* | Full network stack access (`RED` posture) | All host NICs, subnets, routes, and WAN | Nothing blocked |
| **`./run_cora_NIX.sh cli -m 3.8 -netiso white`**<br>*(or `--network-isolation white` / `-white`)* | Complete network namespace isolation (`WHITE` posture via `unshare -r -n`) | `lo` (`127.0.0.1`), local `llama-server`, local files, GPU, and `/dev/ttyUSB*` | **All** external network interfaces (`Network is unreachable`) |
| **`./run_cora_NIX.sh cli -m 3.8 -netiso blue [eth0,eth1]`**<br>*(or `--network-isolation blue` / `-blue`)* | Interface-locked isolation (`BLUE` posture; uses `network_isolation.conf` or CLI override `eth0,eth1`) | `lo` (`127.0.0.1`) + ONLY the specified interfaces (e.g. `eth0,eth1`), `/dev/ttyUSB*`, local files & GPU | All other host interfaces (e.g. `eth2`, `docker0`, `br-*`, `wlan0`) and their subnets |
| **[`LLM_NetworkIsolationSetup_NIX.sh`](./LLM_NetworkIsolationSetup_NIX.sh)** | Persistent host `iptables`/`ip6tables` group (`llm-local`) + `udev` rules (`--ifaces eth0,eth1`) | `lo` + configured `BLUE_ALLOWED_IFACES` (`eth0,eth1`), `/dev/ttyUSB0..1` | All non-whitelisted NICs in the kernel `OUTPUT` chain |
| **[`LLM_NetworkNamespaceSetup_NIX.sh`](./LLM_NetworkNamespaceSetup_NIX.sh)** | Persistent named `ip netns` (`llm-isolated`) or rootless `--unshare` wrapper | `lo` (`127.0.0.1`), local files, GPU, and `/dev/*` devices | **All** external network interfaces (`Network is unreachable`) |
