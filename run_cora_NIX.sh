#!/usr/bin/env bash
# run_cora_NIX.sh — Manage the CORA server (llama.cpp CUDA/CPU) + Custom CORA WebUI + CORA Agent CLI.
# Supports switching between:
#   - qwen3.8 (DEFAULT):  Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.4 GiB)
#   - qwen3.5 (FAST):     Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.2 GiB, HauhauCS-Aggressive)
#   - turbo   (MTP-Q4):   Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.2 GiB, Multiple Token Prediction)
#   - turbo-q6 (MTP-Q6):  Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.4 GiB, Multiple Token Prediction)
#   - turbo-q8 (MTP-Q8):  Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.2 GiB, Multiple Token Prediction)
# Dynamically auto-detects CPU topology (hybrid P/E cores), system RAM, and GPU VRAM
# to configure llama-server / Agent CLI for peak efficiency.
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")" && pwd -P)
if [[ "$(basename "$SCRIPT_DIR")" == "core" ]]; then
  CORA_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd -P)
else
  CORA_ROOT="$SCRIPT_DIR"
fi
if [[ -d "$CORA_ROOT/core" ]]; then
  BASE_DIR="$CORA_ROOT/core"
else
  BASE_DIR="$CORA_ROOT"
fi
BIN_DIR="$BASE_DIR/bin"
MODELS_DIR="${CORA_MODELS_DIR:-$CORA_ROOT/models}"
LOG_DIR="$BASE_DIR/Log"
PROJECTS_DIR="${CORA_PROJECTS_DIR:-$CORA_ROOT/Projects}"
TRAINING_DIR="${CORA_TRAINING_DIR:-$CORA_ROOT/Training}"
export CORA_ROOT CORA_CORE_DIR="$BASE_DIR" CORA_MODELS_DIR="$MODELS_DIR" CORA_PROJECTS_DIR="$PROJECTS_DIR" CORA_TRAINING_DIR="$TRAINING_DIR" OBSIDIAN_VAULT_DIR="$BASE_DIR/ObsidianVault"
mkdir -p "$LOG_DIR" "$PROJECTS_DIR" "$MODELS_DIR" "$TRAINING_DIR"
chmod 775 "$LOG_DIR" "$PROJECTS_DIR" 2>/dev/null || true
# Ensure every existing project in Projects/ has a Files/ subdirectory
for _pdir in "$PROJECTS_DIR"/*/; do
  if [[ -d "$_pdir" ]]; then
    mkdir -p "${_pdir%/}/Files" 2>/dev/null || true
  fi
done
# Automatically migrate any legacy root-level pid/model/log files into Log/
for _legacy in llama-server.pid llama-server.model llama-server.log; do
  if [[ -f "$BASE_DIR/$_legacy" && ! -f "$LOG_DIR/$_legacy" ]]; then
    mv -f "$BASE_DIR/$_legacy" "$LOG_DIR/$_legacy" 2>/dev/null || true
  fi
done
PID_FILE="$LOG_DIR/llama-server.pid"
ACTIVE_MODEL_FILE="$LOG_DIR/llama-server.model"
LOG_FILE="$LOG_DIR/llama-server.log"
WEBUI_PID_FILE="$LOG_DIR/webui.pid"
WEBUI_LOG_FILE="$LOG_DIR/webui.log"

HOST="${HOST:-127.0.0.1}"
LLAMA_PORT="${LLAMA_PORT:-8080}"
WEBUI_PORT="${WEBUI_PORT:-1337}"

QWEN38_URL="https://huggingface.co/0bserverx/Qwen3.8-27B-Heretic-Abliterated-Uncensored-GGUF/resolve/main/RVN-Q3_K_M-multilingual.gguf"
QWEN38_FILE="Qwen3.8-27B-Uncensored-Q3_K_M.gguf"
QWEN38_MIN_BYTES=13000000000

QWEN35_URL="https://huggingface.co/HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive/resolve/main/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
QWEN35_FILE="Qwen3.5-9B-Uncensored-Q4_K_M.gguf"
QWEN35_MIN_BYTES=5500000000

QWEN38_TURBO_HF_BASE="https://huggingface.co/DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF/resolve/main"
QWEN38_TURBO_Q4_URL="${QWEN38_TURBO_HF_BASE}/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q4_K_M.gguf"
QWEN38_TURBO_Q4_FILE="Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf"
QWEN38_TURBO_Q4_HF_FILE="Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q4_K_M.gguf"
QWEN38_TURBO_Q4_MIN_BYTES=18000000000

QWEN38_TURBO_Q6_URL="${QWEN38_TURBO_HF_BASE}/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q6_K.gguf"
QWEN38_TURBO_Q6_FILE="Qwen3.8-27B-Turbo-MTP-Q6_K.gguf"
QWEN38_TURBO_Q6_HF_FILE="Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q6_K.gguf"
QWEN38_TURBO_Q6_MIN_BYTES=23500000000

QWEN38_TURBO_Q8_URL="${QWEN38_TURBO_HF_BASE}/Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q8_0.gguf"
QWEN38_TURBO_Q8_FILE="Qwen3.8-27B-Turbo-MTP-Q8_0.gguf"
QWEN38_TURBO_Q8_HF_FILE="Qwen3.8-27B-TurboFCFusion-735-882-Here-Uncen-NEO-CODER-MAX-MTP-Q8_0.gguf"
QWEN38_TURBO_Q8_MIN_BYTES=29500000000

# Default model selection (defaults to qwen3.8 when not specified)
MODEL_SELECT="${MODEL:-qwen3.8}"
AGENT_MODE="${AGENT_MODE:-on}"
# Disable ngram-mod speculative drafting by default (causes <2% acceptance overhead on tool JSONs)
SPEC_TYPE="${SPEC_TYPE:-none}"
# Default REASONING to 'off' so Qwen3.5/3.8 answers immediately instead of spending
# hundreds of tokens debating with itself in <think>...</think> blocks.
REASONING_MODE="${REASONING:-off}"
SKIP_PERMISSIONS="${SKIP_PERMISSIONS:-0}"
NETISO_CONFIG_FILE="$BASE_DIR/Network_Isolation/network_isolation.conf"
NETISO_LEVEL="${LLM_ISOLATION_MODE:-}"
NETISO_IFACES="${LLM_ALLOWED_IFACES:-}"
CONTINUE_SESSION="${LLM_CONTINUE_SESSION:-0}"

usage() {
  cat <<'EOT'
Usage: ./run_cora_NIX.sh {start|stop|restart|status|webui|webgui|models|download|tune|cli|continue|reason|train|posture|troubleshoot|logs} [-m MODEL] [options...]

Commands:
  start        Start llama-server (with Agent tools + auto-detected tuning) and Custom CORA WebUI (port 1337)
  stop         Stop llama-server and Custom CORA WebUI
  restart      Restart both services (optionally switching models with -m)
  status       Show service status, active model, auto-detected hardware profile, and GPU VRAM usage
  webui|webgui Start & open the Custom CORA WebUI Dashboard (http://127.0.0.1:1337)
  models       List installed & available models and show which model is active / default
  download     Download/verify a specific model (-m turbo | -m turbo-q6 | -m turbo-q8 | -m all-turbo | -m all)
  tune         Display the auto-detected hardware profile and exact flags without starting
  cli          Launch the interactive CORA Agent CLI with shell & file tools
  continue     Launch CORA Agent CLI and resume directly from the last saved session (alias for `cli --continue`)
  reason       Run CPU-based Neuro-Symbolic Reasoning Engine (status|test|seed|pipeline)
  train        Distill Training/ (or custom folder/file) + OCR diagrams into ObsidianVault & Reasoning (-train / --train)
  posture      Detect & apply console security posture theme (--detect|--apply|--demo|--reset)
  troubleshoot Run the 8-Layer CORA Troubleshooting & Diagnostics Suite
  logs         Tail llama-server logs (stored in core/Log/llama-server.log)

Model Selection Switch (-m / --model or MODEL=...):
  -m qwen3.8 | 3.8 | 27b | q3              Use Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.4 GiB) [DEFAULT]
  -m qwen3.5 | 3.5 | 9b | fast             Use Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.2 GiB, HauhauCS-Aggressive)
  -m turbo | mtp | turbo-q4 | mtp-q4 | q4  Use Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.2 GiB, Multiple Token Prediction)
  -m turbo-q6 | mtp-q6 | 3.8-q6 | q6       Use Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.4 GiB, Multiple Token Prediction)
  -m turbo-q8 | mtp-q8 | 3.8-q8 | q8       Use Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.2 GiB, Multiple Token Prediction)
  -m /path/to/model.gguf                   Use a custom GGUF model file

Session Continuation Switch (Agent CLI):
  -c, --continue, --resume                 Continue from the last CLI session (restores active project, goal,
                                           attempt ledger, and conversation history)

Network Isolation Switch (--network-isolation / -netiso <Red|White|Blue> [ifaces]):
  -netiso red   | --network-isolation red             Full network stack access (RED posture; all NICs & WAN open)
  -netiso white | --network-isolation white           Isolated by Linux network namespace (WHITE posture; loopback `lo` only)
  -netiso blue  | --network-isolation blue            Interface-locked isolation using static `BLUE_ALLOWED_IFACES`
                                                      from `core/Network_Isolation/network_isolation.conf`
  -netiso blue eth0,eth1                              Override config file and lock CLI strictly to `eth0` and `eth1`
  Shorthand aliases: -red | -white | -blue [eth0,eth1] | -netiso blue:eth0,eth1

Reasoning / Thinking Switch:
  --no-think                       Disable internal <think> monologue for instant answers [DEFAULT]
  --think                          Enable step-by-step <think> chain-of-thought reasoning

Permissions / Confirmation & Project Switches (Agent CLI):
  --confirm                              Prompt [y/N/a] before running shell commands or file writes [DEFAULT]
  --dangerously-skip-permissions         Auto-run all shell commands and file writes without confirming
  -P, --project <doc_path_or_dir> [name] Ingest documentation file/folder, verify data with user, and create/track
                                         an isolated project workspace in Projects/<name>/ (memory.md & downloads/)

Environment Overrides (optional — auto-detected when omitted):
  MODEL          Model selector ('qwen3.8' [default], 'qwen3.5', 'turbo', 'turbo-q6', or 'turbo-q8')
  CTX_SIZE       Context window size in tokens (e.g. CTX_SIZE=32768)
  AGENT_MODE     Enable built-in system tools (write_file, edit_file, exec_shell_command, etc.): 'on' (default) or 'off'
  REASONING      Thinking mode: 'off' (default, instant output), 'on' (chain-of-thought), or 'auto'
  SPEC_TYPE      Speculative decoding mode (default: 'none')
  THREADS        Generation (decode) thread count
  THREADS_BATCH  Prompt processing (prefill) thread count
  FIT_TARGET     VRAM safety headroom in MiB per GPU (e.g. FIT_TARGET=384)

Examples:
  ./run_cora_NIX.sh cli -m 3.8 -c                                   # Continue from the last session with Qwen3.8-27B
  ./run_cora_NIX.sh cli -m 3.8 -netiso red                          # Full network stack access (Red posture)
  ./run_cora_NIX.sh cli -m 3.8 --network-isolation white            # Isolated by network namespace (White posture, lo only)
  ./run_cora_NIX.sh cli -m 3.8 -netiso blue                         # Locked to static interfaces in network_isolation.conf
  ./run_cora_NIX.sh cli -m 3.8 -netiso blue eth0,eth1               # Override config and lock strictly to eth0 and eth1
  ./run_cora_NIX.sh cli -m 3.8 -c -netiso blue eth0,eth1            # Continue last session + lock to eth0,eth1
  ./run_cora_NIX.sh cli -m 3.5 --dangerously-skip-permissions       # Agent CLI with Qwen3.5-9B (auto-run all commands)
  ./run_cora_NIX.sh cli -m turbo --dangerously-skip-permissions     # Agent CLI with Qwen3.8-27B Turbo MTP Q4_K_M
  ./run_cora_NIX.sh download -m all-turbo                           # Download all 3 Qwen3.8-27B Turbo MTP models (Q4_K_M, Q6_K, Q8_0)
  ./run_cora_NIX.sh -train                                          # Train CORA & Reasoning on Training/ (MD/PDF/OCR/Diagrams)
  ./run_cora_NIX.sh models                                          # List installed & available models
EOT
}

show_switch_help() {
  local sw="${1:-}"
  sw="${sw#-}"
  sw="${sw#-}"
  sw="${sw,,}"
  case "$sw" in
    m|model)
      cat <<'EOT'
=== Switch Help: -m / --model ===
  Select the active GGUF CORA model to run on llama-server (127.0.0.1:8080):
    -m qwen3.8 | 3.8 | 27b | q3              Use Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.4 GiB) [DEFAULT]
    -m qwen3.5 | 3.5 | 9b | fast             Use Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.2 GiB, HauhauCS-Aggressive)
    -m turbo   | mtp | turbo-q4 | q4         Use Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.2 GiB, Multiple Token Prediction)
    -m turbo-q6| mtp-q6 | 3.8-q6 | q6        Use Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.4 GiB, Multiple Token Prediction)
    -m turbo-q8| mtp-q8 | 3.8-q8 | q8        Use Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.2 GiB, Multiple Token Prediction)
    -m /path/to/model.gguf                   Use a custom GGUF model file
EOT
      ;;
    netiso|network-isolation|n|posture|red|white|blue)
      cat <<'EOT'
=== Switch Help: --network-isolation / -netiso / posture ===
  Configure C.O.R.A. Network Isolation & Security Posture (Red / White / Blue):
    -netiso red   | --network-isolation red             Full network stack access (RED posture; all NICs & WAN open)
    -netiso white | --network-isolation white           Isolated by Linux network namespace (WHITE posture; loopback `lo` only)
    -netiso blue  | --network-isolation blue            Interface-locked isolation using static `BLUE_ALLOWED_IFACES`
                                                        from `core/Network_Isolation/network_isolation.conf`
    -netiso blue eth0,eth1                              Override config file and lock CLI strictly to `eth0` and `eth1`
    Shorthand aliases: -red | -white | -blue [eth0,eth1] | -netiso blue:eth0,eth1
EOT
      ;;
    c|continue|resume)
      cat <<'EOT'
=== Switch Help: -c / --continue / continue ===
  Restore and continue from the last saved C.O.R.A. CLI session (`last_cli_session.json` + `relentless_ledger.json`):
    ./run_cora_NIX.sh cli -m 3.8 -c         Launch CLI and immediately restore previous project, goal, wave, and messages
    ./run_cora_NIX.sh cli -m 3.8 --continue Same as `-c`
    ./run_cora_NIX.sh continue -m 3.8       Shorthand command alias for `cli --continue`
EOT
      ;;
    p|project|projects)
      cat <<'EOT'
=== Switch Help: -P / --project / /project ===
  Manage isolated project workspaces inside `CORA/Projects/<project-name>/`:
  (All spaces and special characters in project names are automatically converted to dashes `-`; parameters require a leading `-`)
    -P:<project_name> | -P <project_name>           Select or create `Projects/<project_name>/` at CLI startup
    -P <doc_path_or_dir> [project_name]             Ingest documentation file/folder into `Projects/<project_name>/memory.md`
    In-CLI `/project` options:
      /project | /project -mode:menu                Open the interactive numbered Project Selection / Rename / Create menu
      /project list | /project -mode:list           List all current projects in `Projects/`
      /project -new:<name>  (or /project new)       Create a new project in `Projects/<name>/` (spaces/special chars -> `-`)
      /project -rename:<old>:<new> (or /project rename) Rename an existing project in `Projects/`
      /project -load:<name> ["<task>"]              Switch active project to `Projects/<name>/`
      -P -h | --project --help | /project -h | /project --help : Show this help message
EOT
      ;;
    start|restart|stop|status|models|download|pull|tune|detect|logs)
      cat <<'EOT'
=== Switch Help: Service & Model Management Commands ===
  ./run_cora_NIX.sh start   [-m MODEL] [-netiso LEVEL] : Start llama-server + WebUI (prompts for active project selection)
  ./run_cora_NIX.sh stop                               : Stop llama-server and Open WebUI
  ./run_cora_NIX.sh restart [-m MODEL]                 : Restart services (optionally switching models)
  ./run_cora_NIX.sh status                             : Show service status, active model, hardware profile, and VRAM
  ./run_cora_NIX.sh models                             : List installed & available GGUF models
  ./run_cora_NIX.sh download -m:<3.8|3.5|turbo|all>    : Download/verify GGUF model files
  ./run_cora_NIX.sh tune                               : Print auto-detected hardware tuning profile without starting
  ./run_cora_NIX.sh logs                               : Tail `core/Log/llama-server.log`
  Pass `-h` or `--help` after any command or switch to view its options.
EOT
      ;;
    cli)
      python3 "$BASE_DIR/agent-cli.py" -h
      ;;
    *)
      python3 "$BASE_DIR/agent-cli.py" "$sw" -h
      ;;
  esac
}

# Check for `<switch> -h` or `<switch> --help` (or `<switch>:-h` / `<switch>:--help`) anywhere in arguments before starting services
_prev_arg=""
for _arg in "$@"; do
  if [[ "$_arg" == *":-h" || "$_arg" == *":--help" ]]; then
    show_switch_help "${_arg%%:*}"
    exit 0
  elif [[ "$_arg" == "-h" || "$_arg" == "--help" || "$_arg" == "-?" ]]; then
    if [[ -n "$_prev_arg" ]]; then
      show_switch_help "$_prev_arg"
      exit 0
    fi
  elif [[ "$_prev_arg" == "-h" || "$_prev_arg" == "--help" || "$_prev_arg" == "help" ]]; then
    show_switch_help "$_arg"
    exit 0
  fi
  _prev_arg="$_arg"
done

ACTION="status"
ACTION_SET=0
EXTRA_ARGS=()

is_action_keyword() {
  case "$1" in
    start|stop|restart|status|webui|webgui|-webui|--webui|-webgui|--webgui|gui|ui|dashboard|models|download|pull|tune|detect|cli|continue|resume|reason|reasoning|train|-train|--train|posture|troubleshoot|diag|diagnostics|logs|-h|--help|help)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    start|stop|restart|status|webui|webgui|-webui|--webui|-webgui|--webgui|gui|ui|dashboard|models|download|pull|tune|detect|cli|continue|resume|reason|reasoning|train|-train|--train|posture|troubleshoot|diag|diagnostics|logs|-h|--help|help)
      if (( ACTION_SET == 0 )); then
        if [[ "$1" == "-train" || "$1" == "--train" ]]; then
          ACTION="train"
        elif [[ "$1" == "webui" || "$1" == "webgui" || "$1" == "-webui" || "$1" == "--webui" || "$1" == "-webgui" || "$1" == "--webgui" || "$1" == "gui" || "$1" == "ui" || "$1" == "dashboard" ]]; then
          ACTION="webui"
        elif [[ "$1" == "pull" ]]; then
          ACTION="download"
        elif [[ "$1" == "continue" || "$1" == "resume" ]]; then
          ACTION="cli"
          CONTINUE_SESSION="1"
          EXTRA_ARGS+=("--continue")
        else
          ACTION="$1"
        fi
        ACTION_SET=1
      else
        if [[ "$1" == "continue" || "$1" == "resume" ]]; then
          CONTINUE_SESSION="1"
          EXTRA_ARGS+=("--continue")
        else
          EXTRA_ARGS+=("$1")
        fi
      fi
      shift
      ;;
    -c|--continue|-continue|--resume|-resume)
      CONTINUE_SESSION="1"
      EXTRA_ARGS+=("--continue")
      shift
      ;;
    -netiso|--netiso|--network-isolation|-n)
      if [[ $# -lt 2 ]]; then
        printf 'Error: %s requires a color level: red, white, or blue [ifaces]\n' "$1" >&2
        exit 2
      fi
      NETISO_LEVEL="$2"
      shift 2
      if [[ "${NETISO_LEVEL,,}" == blue:* || "${NETISO_LEVEL,,}" == blue=* ]]; then
        NETISO_IFACES="${NETISO_LEVEL#*:}"
        NETISO_IFACES="${NETISO_IFACES#*=}"
        NETISO_LEVEL="blue"
      elif [[ "${NETISO_LEVEL,,}" == "blue" ]]; then
        if [[ $# -gt 0 && "$1" != -* ]] && ! is_action_keyword "$1"; then
          NETISO_IFACES="$1"
          shift
        fi
      fi
      ;;
    --network-isolation=*|-netiso=*|--netiso=*|--network-isolation:*|-netiso:*|--netiso:*)
      NETISO_LEVEL="${1#*=}"
      if [[ "$NETISO_LEVEL" == "$1" ]]; then
        NETISO_LEVEL="${1#*:}"
      fi
      shift
      if [[ "${NETISO_LEVEL,,}" == blue:* || "${NETISO_LEVEL,,}" == blue=* ]]; then
        NETISO_IFACES="${NETISO_LEVEL#*:}"
        NETISO_IFACES="${NETISO_IFACES#*=}"
        NETISO_LEVEL="blue"
      elif [[ "${NETISO_LEVEL,,}" == "blue" ]]; then
        if [[ $# -gt 0 && "$1" != -* ]] && ! is_action_keyword "$1"; then
          NETISO_IFACES="$1"
          shift
        fi
      fi
      ;;
    -red|--red)
      NETISO_LEVEL="red"
      NETISO_IFACES=""
      shift
      ;;
    -white|--white)
      NETISO_LEVEL="white"
      NETISO_IFACES="lo"
      shift
      ;;
    -blue|--blue)
      NETISO_LEVEL="blue"
      shift
      if [[ $# -gt 0 && "$1" != -* ]] && ! is_action_keyword "$1"; then
        NETISO_IFACES="$1"
        shift
      fi
      ;;
    -blue=*|--blue=*|-blue:*|--blue:*)
      NETISO_LEVEL="blue"
      NETISO_IFACES="${1#*=}"
      NETISO_IFACES="${NETISO_IFACES#*:}"
      shift
      ;;
    -m|--model)
      if [[ $# -lt 2 ]]; then
        printf 'Error: %s requires a model argument (e.g. qwen3.8, qwen3.5, turbo, turbo-q6, or turbo-q8)\n' "$1" >&2
        exit 2
      fi
      MODEL_SELECT="$2"
      shift 2
      ;;
    --model=*|--model:*|-m:*|-m=*)
      MODEL_SELECT="${1#*=}"
      if [[ "$MODEL_SELECT" == "$1" ]]; then
        MODEL_SELECT="${1#*:}"
      fi
      shift
      ;;
    --think)
      REASONING_MODE="on"
      shift
      ;;
    --no-think)
      REASONING_MODE="off"
      shift
      ;;
    --dangerously-skip-permissions)
      SKIP_PERMISSIONS="1"
      shift
      ;;
    --confirm)
      SKIP_PERMISSIONS="0"
      shift
      ;;
    *)
      EXTRA_ARGS+=("$1")
      shift
      ;;
  esac
done

configure_network_isolation() {
  local raw_lvl="${NETISO_LEVEL:-}"
  local raw_ifaces="${NETISO_IFACES:-}"
  local cfg_default_lvl="red"
  local cfg_blue_ifaces="eth0,eth1"

  if [[ -f "$NETISO_CONFIG_FILE" ]]; then
    # Safely read static defaults from Network_Isolation/network_isolation.conf
    local line key val
    while IFS= read -r line || [[ -n "$line" ]]; do
      line="${line%%#*}"
      line="${line#"${line%%[![:space:]]*}"}"
      line="${line%"${line##*[![:space:]]}"}"
      [[ -z "$line" || "$line" != *=* ]] && continue
      key="${line%%=*}"
      val="${line#*=}"
      val="${val#\"}"
      val="${val%\"}"
      val="${val#\'}"
      val="${val%\'}"
      case "$key" in
        DEFAULT_ISOLATION_LEVEL) cfg_default_lvl="$val" ;;
        BLUE_ALLOWED_IFACES)     cfg_blue_ifaces="$val" ;;
      esac
    done < "$NETISO_CONFIG_FILE"
  fi

  if [[ -z "$raw_lvl" ]]; then
    raw_lvl="$cfg_default_lvl"
  fi

  local lvl_lower
  lvl_lower=$(printf '%s' "$raw_lvl" | tr '[:upper:]' '[:lower:]')
  case "$lvl_lower" in
    white|netns|namespace|airgap|airgapped|air_gapped_netns)
      export LLM_ISOLATION_MODE="WHITE"
      export LLM_POSTURE_OVERRIDE="WHITE"
      export LLM_ALLOWED_IFACES="lo"
      EXTRA_ARGS+=("-netiso" "white")
      ;;
    blue|lan|usb|isolated|isolated_lan_usb)
      local eff_ifaces="$raw_ifaces"
      if [[ -z "$eff_ifaces" ]]; then
        eff_ifaces="$cfg_blue_ifaces"
      fi
      # Normalize spaces to commas
      eff_ifaces=$(printf '%s' "$eff_ifaces" | tr ' ' ',' | sed 's/,,*/,/g; s/^,//; s/,$//')
      [[ -z "$eff_ifaces" ]] && eff_ifaces="eth0,eth1"
      if [[ -n "$raw_ifaces" ]]; then
        export LLM_CLI_BLUE_IFACES="$eff_ifaces"
      fi
      export LLM_ISOLATION_MODE="BLUE"
      export LLM_POSTURE_OVERRIDE="BLUE"
      export LLM_ALLOWED_IFACES="$eff_ifaces"
      EXTRA_ARGS+=("-netiso" "blue" "$eff_ifaces")
      ;;
    red|unrestricted|full|default|*)
      export LLM_ISOLATION_MODE="RED"
      export LLM_POSTURE_OVERRIDE="RED"
      unset LLM_ALLOWED_IFACES 2>/dev/null || true
      if [[ -n "${NETISO_LEVEL:-}" ]]; then
        EXTRA_ARGS+=("-netiso" "red")
      fi
      ;;
  esac

  if [[ "$CONTINUE_SESSION" == "1" ]]; then
    export LLM_CONTINUE_SESSION="1"
  fi
}

configure_network_isolation

MODEL_DOWNLOAD_URL=""
MODEL_MIN_BYTES=0
MODEL_HF_SYMLINK=""
MODEL_EXPECTED_MIB=5366

resolve_model() {
  local sel="${1:-$MODEL_SELECT}"
  local sel_lower
  sel_lower=$(printf '%s' "$sel" | tr '[:upper:]' '[:lower:]')
  MODEL_DOWNLOAD_URL=""
  MODEL_MIN_BYTES=0
  MODEL_HF_SYMLINK=""
  MODEL_EXPECTED_MIB=5366

  case "$sel_lower" in
    qwen3.8|3.8|27b|qwen38|q3|q3_k_m|default|"")
      if [[ -f "$MODELS_DIR/$QWEN38_FILE" || ! -f "$MODELS_DIR/$QWEN35_FILE" || "$sel_lower" != "" ]]; then
        MODEL_KEY="qwen3.8"
        MODEL_ALIAS="Qwen3.8-27B-Uncensored-Q3_K_M"
        MODEL_PATH="${MODEL_PATH_OVERRIDE:-$MODELS_DIR/$QWEN38_FILE}"
        MODEL_DOWNLOAD_URL="$QWEN38_URL"
        MODEL_MIN_BYTES="$QWEN38_MIN_BYTES"
        MODEL_EXPECTED_MIB=12689
      else
        # Fallback to 3.5 if only 3.5 is installed on a smaller laptop and no explicit selector was given
        MODEL_KEY="qwen3.5"
        MODEL_ALIAS="Qwen3.5-9B-Uncensored-Q4_K_M"
        MODEL_PATH="$MODELS_DIR/$QWEN35_FILE"
        MODEL_DOWNLOAD_URL="$QWEN35_URL"
        MODEL_MIN_BYTES="$QWEN35_MIN_BYTES"
        MODEL_EXPECTED_MIB=5366
      fi
      ;;
    qwen3.5|3.5|9b|qwen35|fast|hauhaucs)
      MODEL_KEY="qwen3.5"
      MODEL_ALIAS="Qwen3.5-9B-Uncensored-Q4_K_M"
      MODEL_DOWNLOAD_URL="$QWEN35_URL"
      MODEL_MIN_BYTES="$QWEN35_MIN_BYTES"
      MODEL_HF_SYMLINK="Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
      MODEL_EXPECTED_MIB=5366
      if [[ -f "$MODELS_DIR/$QWEN35_FILE" ]]; then
        MODEL_PATH="$MODELS_DIR/$QWEN35_FILE"
      elif [[ -f "$MODELS_DIR/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf" ]]; then
        MODEL_PATH="$MODELS_DIR/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
      else
        MODEL_PATH="$MODELS_DIR/$QWEN35_FILE"
      fi
      ;;
    turbo|mtp|turbo-q4|mtp-q4|q4|q4_k_m|3.8-turbo|3.8-mtp|3.8-q4|3.8-turbo-q4|3.8-mtp-q4|qwen3.8-turbo|qwen3.8-mtp|qwen3.8-turbo-q4|qwen3.8-mtp-q4|27b-turbo|27b-mtp|27b-q4)
      MODEL_KEY="turbo-q4"
      MODEL_ALIAS="Qwen3.8-27B-Turbo-MTP-Q4_K_M"
      MODEL_DOWNLOAD_URL="$QWEN38_TURBO_Q4_URL"
      MODEL_MIN_BYTES="$QWEN38_TURBO_Q4_MIN_BYTES"
      MODEL_HF_SYMLINK="$QWEN38_TURBO_Q4_HF_FILE"
      MODEL_EXPECTED_MIB=17642
      if [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q4_FILE" ]]; then
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q4_FILE"
      elif [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q4_HF_FILE" ]]; then
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q4_HF_FILE"
      else
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q4_FILE"
      fi
      ;;
    turbo-q6|mtp-q6|q6|q6_k|3.8-turbo-q6|3.8-mtp-q6|3.8-q6|qwen3.8-turbo-q6|qwen3.8-mtp-q6|27b-turbo-q6|27b-mtp-q6|27b-q6)
      MODEL_KEY="turbo-q6"
      MODEL_ALIAS="Qwen3.8-27B-Turbo-MTP-Q6_K"
      MODEL_DOWNLOAD_URL="$QWEN38_TURBO_Q6_URL"
      MODEL_MIN_BYTES="$QWEN38_TURBO_Q6_MIN_BYTES"
      MODEL_HF_SYMLINK="$QWEN38_TURBO_Q6_HF_FILE"
      MODEL_EXPECTED_MIB=22920
      if [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q6_FILE" ]]; then
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q6_FILE"
      elif [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q6_HF_FILE" ]]; then
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q6_HF_FILE"
      else
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q6_FILE"
      fi
      ;;
    turbo-q8|mtp-q8|q8|q8_0|3.8-turbo-q8|3.8-mtp-q8|3.8-q8|qwen3.8-turbo-q8|qwen3.8-mtp-q8|27b-turbo-q8|27b-mtp-q8|27b-q8)
      MODEL_KEY="turbo-q8"
      MODEL_ALIAS="Qwen3.8-27B-Turbo-MTP-Q8_0"
      MODEL_DOWNLOAD_URL="$QWEN38_TURBO_Q8_URL"
      MODEL_MIN_BYTES="$QWEN38_TURBO_Q8_MIN_BYTES"
      MODEL_HF_SYMLINK="$QWEN38_TURBO_Q8_HF_FILE"
      MODEL_EXPECTED_MIB=28838
      if [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q8_FILE" ]]; then
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q8_FILE"
      elif [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q8_HF_FILE" ]]; then
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q8_HF_FILE"
      else
        MODEL_PATH="$MODELS_DIR/$QWEN38_TURBO_Q8_FILE"
      fi
      ;;
    *)
      if [[ -f "$sel" ]]; then
        MODEL_PATH=$(readlink -f "$sel")
      elif [[ -f "$MODELS_DIR/$sel" ]]; then
        MODEL_PATH=$(readlink -f "$MODELS_DIR/$sel")
      else
        printf 'Error: Unknown model selector "%s". Use -m qwen3.8 (default), -m qwen3.5, -m turbo (MTP Q4_K_M), -m turbo-q6 (MTP Q6_K), or -m turbo-q8 (MTP Q8_0).\n' "$sel" >&2
        exit 2
      fi
      MODEL_ALIAS=$(basename "$MODEL_PATH" .gguf)
      MODEL_KEY="$MODEL_ALIAS"
      ;;
  esac
}

download_gguf_model() {
  local label="$1"
  local url="$2"
  local dest="$3"
  local min_bytes="$4"
  local hf_symlink="${5:-}"

  mkdir -p "$MODELS_DIR"
  if [[ -f "$dest" ]]; then
    local actual_bytes
    actual_bytes=$(stat -Lc%s "$dest" 2>/dev/null || echo 0)
    if (( actual_bytes >= min_bytes )); then
      printf '  -> %s already installed and verified (%d MiB).\n' "$label" "$(( actual_bytes / 1048576 ))"
      if [[ -n "$hf_symlink" && ! -e "$MODELS_DIR/$hf_symlink" ]]; then
        ln -sf "$(basename "$dest")" "$MODELS_DIR/$hf_symlink" 2>/dev/null || true
      fi
      return 0
    fi
    printf '  -> %s is incomplete (%d MiB < %d MiB); resuming download...\n' "$label" "$(( actual_bytes / 1048576 ))" "$(( min_bytes / 1048576 ))"
  else
    local avail_mb needed_mb
    avail_mb=$(df -Pm "$MODELS_DIR" | awk 'NR==2 {print $4}' 2>/dev/null || echo 999999)
    needed_mb=$(( min_bytes / 1048576 + 512 ))
    if (( avail_mb < needed_mb )); then
      printf 'Error: Insufficient disk space in %s (%d MiB free, need at least %d MiB for %s).\n' \
        "$MODELS_DIR" "$avail_mb" "$needed_mb" "$label" >&2
      exit 1
    fi
    printf '  -> Downloading %s from Hugging Face ...\n' "$label"
  fi

  if command -v wget >/dev/null 2>&1; then
    wget -c --tries=5 --timeout=30 --progress=bar:force:noscroll -O "$dest" "$url"
  else
    curl -fL --retry 5 --retry-delay 3 -C - -o "$dest" "$url"
  fi

  local final_bytes
  final_bytes=$(stat -Lc%s "$dest" 2>/dev/null || echo 0)
  if (( final_bytes < min_bytes )); then
    printf 'Error: Downloaded file %s is smaller than expected (%d bytes < %d bytes). Re-run command to resume.\n' \
      "$dest" "$final_bytes" "$min_bytes" >&2
    exit 1
  fi
  if [[ -n "$hf_symlink" && ! -e "$MODELS_DIR/$hf_symlink" ]]; then
    ln -sf "$(basename "$dest")" "$MODELS_DIR/$hf_symlink" 2>/dev/null || true
  fi
  printf '  -> Verified %s (%d MiB).\n' "$label" "$(( final_bytes / 1048576 ))"
}

ensure_selected_model_downloaded() {
  if [[ -f "$MODEL_PATH" ]]; then
    local actual_bytes
    actual_bytes=$(stat -Lc%s "$MODEL_PATH" 2>/dev/null || echo 0)
    if (( MODEL_MIN_BYTES == 0 || actual_bytes >= MODEL_MIN_BYTES )); then
      return 0
    fi
  fi
  if [[ -n "${MODEL_DOWNLOAD_URL:-}" && "${OFFLINE:-0}" != "1" ]]; then
    printf 'Model %s (%s) is not yet present in %s; auto-downloading now...\n' \
      "$MODEL_ALIAS" "$(basename "$MODEL_PATH")" "$MODELS_DIR"
    download_gguf_model "$MODEL_ALIAS ($(basename "$MODEL_PATH"))" \
      "$MODEL_DOWNLOAD_URL" "$MODEL_PATH" "$MODEL_MIN_BYTES" "$MODEL_HF_SYMLINK"
    MODEL_SIZE_MIB=$(( $(stat -Lc%s "$MODEL_PATH" 2>/dev/null || echo 0) / 1048576 ))
  fi
}

cmd_download_models() {
  local sel="${1:-$MODEL_SELECT}"
  local sel_lower
  sel_lower=$(printf '%s' "$sel" | tr '[:upper:]' '[:lower:]')
  case "$sel_lower" in
    all)
      download_gguf_model "Qwen3.5-9B-Uncensored-Q4_K_M.gguf (5.24 GiB)" "$QWEN35_URL" "$MODELS_DIR/$QWEN35_FILE" "$QWEN35_MIN_BYTES" "Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"
      download_gguf_model "Qwen3.8-27B-Uncensored-Q3_K_M.gguf (12.40 GiB)" "$QWEN38_URL" "$MODELS_DIR/$QWEN38_FILE" "$QWEN38_MIN_BYTES" ""
      download_gguf_model "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB MTP)" "$QWEN38_TURBO_Q4_URL" "$MODELS_DIR/$QWEN38_TURBO_Q4_FILE" "$QWEN38_TURBO_Q4_MIN_BYTES" "$QWEN38_TURBO_Q4_HF_FILE"
      download_gguf_model "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.38 GiB MTP)" "$QWEN38_TURBO_Q6_URL" "$MODELS_DIR/$QWEN38_TURBO_Q6_FILE" "$QWEN38_TURBO_Q6_MIN_BYTES" "$QWEN38_TURBO_Q6_HF_FILE"
      download_gguf_model "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.16 GiB MTP)" "$QWEN38_TURBO_Q8_URL" "$MODELS_DIR/$QWEN38_TURBO_Q8_FILE" "$QWEN38_TURBO_Q8_MIN_BYTES" "$QWEN38_TURBO_Q8_HF_FILE"
      ;;
    all-turbo|turbo-all|mtp-all|all-mtp)
      download_gguf_model "Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (17.23 GiB MTP)" "$QWEN38_TURBO_Q4_URL" "$MODELS_DIR/$QWEN38_TURBO_Q4_FILE" "$QWEN38_TURBO_Q4_MIN_BYTES" "$QWEN38_TURBO_Q4_HF_FILE"
      download_gguf_model "Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (22.38 GiB MTP)" "$QWEN38_TURBO_Q6_URL" "$MODELS_DIR/$QWEN38_TURBO_Q6_FILE" "$QWEN38_TURBO_Q6_MIN_BYTES" "$QWEN38_TURBO_Q6_HF_FILE"
      download_gguf_model "Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (28.16 GiB MTP)" "$QWEN38_TURBO_Q8_URL" "$MODELS_DIR/$QWEN38_TURBO_Q8_FILE" "$QWEN38_TURBO_Q8_MIN_BYTES" "$QWEN38_TURBO_Q8_HF_FILE"
      ;;
    *)
      resolve_model "$sel"
      if [[ -z "${MODEL_DOWNLOAD_URL:-}" ]]; then
        printf 'Error: No remote download URL configured for model selector "%s".\n' "$sel" >&2
        exit 2
      fi
      download_gguf_model "$MODEL_ALIAS ($(basename "$MODEL_PATH"))" \
        "$MODEL_DOWNLOAD_URL" "$MODEL_PATH" "$MODEL_MIN_BYTES" "$MODEL_HF_SYMLINK"
      ;;
  esac
}

ensure_bin_runtime_health() {
  # Auto-repair any 0-byte .so symlinks or missing +x bits caused by cross-filesystem copies
  if [[ -d "$BIN_DIR" ]]; then
    local pair src dst
    for pair in \
      "libggml-base.so.0.27.0:libggml-base.so.0" \
      "libggml-base.so.0:libggml-base.so" \
      "libggml.so.0.27.0:libggml.so.0" \
      "libggml.so.0:libggml.so" \
      "libllama-common.so.0.7.0:libllama-common.so.0" \
      "libllama-common.so.0:libllama-common.so" \
      "libllama.so.0.7.0:libllama.so.0" \
      "libllama.so.0:libllama.so" \
      "libmtmd.so.0.7.0:libmtmd.so.0" \
      "libmtmd.so.0:libmtmd.so"; do
      src="${pair%%:*}"
      dst="${pair##*:}"
      if [[ -f "$BIN_DIR/$src" ]] && [[ ! -L "$BIN_DIR/$dst" && ! -s "$BIN_DIR/$dst" ]]; then
        ln -sf "$src" "$BIN_DIR/$dst" 2>/dev/null || true
      fi
    done
    if [[ -f "$BIN_DIR/llama-server" && ! -x "$BIN_DIR/llama-server" ]]; then
      chmod +x "$BIN_DIR"/llama* "$BIN_DIR"/ggml* "$BIN_DIR"/*.so* 2>/dev/null || true
    fi
  fi
  for _cuda_compat in "/usr/local/lib/ollama/cuda_v12" "/usr/local/cuda/compat"; do
    if [[ -d "$_cuda_compat" && ":${LD_LIBRARY_PATH:-}:" != *":$_cuda_compat:"* ]]; then
      export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$_cuda_compat"
    fi
  done
  if [[ ":${LD_LIBRARY_PATH:-}:" != *":$BIN_DIR:"* ]]; then
    export LD_LIBRARY_PATH="$BIN_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  fi
}

HW_TUNED_DONE=0
KEEP_SRV_ON_EXIT=0

detect_hardware_and_tune() {
  if (( HW_TUNED_DONE == 1 )); then
    return 0
  fi
  HW_TUNED_DONE=1
  ensure_bin_runtime_health
  resolve_model "$MODEL_SELECT"

  CPU_NAME=$(LC_ALL=C lscpu 2>/dev/null | awk -F: '/Model name:/ {gsub(/^[ \t]+/, "", $2); print $2; exit}')
  CPU_NAME="${CPU_NAME:-Unknown CPU}"
  LOGICAL_CPUS=$(nproc --all 2>/dev/null || echo 4)
  NUMA_NODES=$(LC_ALL=C lscpu 2>/dev/null | awk -F: '/NUMA node\(s\):/ {gsub(/^[ \t]+/, "", $2); print int($2); exit}')
  NUMA_NODES="${NUMA_NODES:-1}"
  (( NUMA_NODES < 1 )) && NUMA_NODES=1

  if command -v lscpu >/dev/null 2>&1; then
    PHYSICAL_CORES=$(LC_ALL=C lscpu -p=SOCKET,CORE 2>/dev/null | grep -v '^#' | sort -u | wc -l)
    P_CORES=$(LC_ALL=C lscpu -p=SOCKET,CORE 2>/dev/null | grep -v '^#' | sort | uniq -c | awk '$1 > 1 {c++} END {print c+0}')
    E_CORES=$(( PHYSICAL_CORES - P_CORES ))
  else
    PHYSICAL_CORES=$(( LOGICAL_CPUS / 2 ))
    (( PHYSICAL_CORES < 1 )) && PHYSICAL_CORES=1
    P_CORES=$PHYSICAL_CORES
    E_CORES=0
  fi

  if (( P_CORES > 0 && E_CORES > 0 )); then
    AUTO_THREADS=$(( P_CORES + (E_CORES / 2) ))
  else
    AUTO_THREADS=$(( (PHYSICAL_CORES * 4 + 4) / 5 ))
  fi
  (( AUTO_THREADS < 1 )) && AUTO_THREADS=1
  AUTO_THREADS_BATCH=$PHYSICAL_CORES

  THREADS="${THREADS:-$AUTO_THREADS}"
  THREADS_BATCH="${THREADS_BATCH:-$AUTO_THREADS_BATCH}"

  TOTAL_RAM_MIB=$(awk '/MemTotal:/ {printf "%d", $2/1024}' /proc/meminfo 2>/dev/null || echo 8192)
  AVAIL_RAM_MIB=$(awk '/MemAvailable:/ {printf "%d", $2/1024}' /proc/meminfo 2>/dev/null || echo 4096)
  if [[ -f "$MODEL_PATH" ]]; then
    MODEL_SIZE_MIB=$(( $(stat -Lc%s "$MODEL_PATH" 2>/dev/null || echo 0) / 1048576 ))
  else
    MODEL_SIZE_MIB="${MODEL_EXPECTED_MIB:-5366}"
  fi

  GPU_DETECTED=0
  GPU_COUNT=0
  GPU_NAME="None (CPU-only mode)"
  GPU_TOTAL_MIB=0
  GPU_FREE_MIB=0

  if command -v nvidia-smi >/dev/null 2>&1; then
    local gpu_lines gpu_line
    gpu_lines=$(env -u LD_LIBRARY_PATH nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader,nounits 2>/dev/null || true)
    if [[ -n "$gpu_lines" && "$gpu_lines" != *"Failed"* ]]; then
      GPU_COUNT=$(printf '%s\n' "$gpu_lines" | grep -c '[^[:space:]]' || echo 0)
      gpu_line=$(printf '%s\n' "$gpu_lines" | head -n1)
      GPU_DETECTED=1
      GPU_NAME=$(printf '%s' "$gpu_line" | awk -F', ' '{print $1}')
      GPU_TOTAL_MIB=$(printf '%s' "$gpu_line" | awk -F', ' '{print int($2)}')
      GPU_FREE_MIB=$(printf '%s' "$gpu_line" | awk -F', ' '{print int($3)}')
      # Validate CUDA_VISIBLE_DEVICES against actual GPU count so out-of-range index (e.g. 1 on a 1-GPU system) never hides GPU 0
      if [[ -n "${CUDA_VISIBLE_DEVICES:-}" && "${CUDA_VISIBLE_DEVICES}" =~ ^[0-9]+$ ]]; then
        if (( CUDA_VISIBLE_DEVICES >= GPU_COUNT )); then
          export CUDA_VISIBLE_DEVICES=0
        fi
      fi
    fi
  fi

  GPU_HEADROOM_MIB=$(( GPU_TOTAL_MIB - MODEL_SIZE_MIB ))
  if (( GPU_DETECTED == 1 && GPU_TOTAL_MIB >= 24000 && GPU_HEADROOM_MIB >= 10000 )); then
    KV_CACHE_TYPE="${KV_CACHE_TYPE:-f16}"
  else
    KV_CACHE_TYPE="${KV_CACHE_TYPE:-q8_0}"
  fi
  GPU_ARGS=()

  if (( GPU_DETECTED == 1 && GPU_TOTAL_MIB > 0 )); then
    if (( MODEL_SIZE_MIB <= GPU_TOTAL_MIB )); then
      AUTO_FIT_TARGET=256
    elif (( GPU_TOTAL_MIB <= 8192 )); then
      AUTO_FIT_TARGET=384
    elif (( GPU_TOTAL_MIB <= 16384 )); then
      AUTO_FIT_TARGET=512
    else
      AUTO_FIT_TARGET=768
    fi
    FIT_TARGET="${FIT_TARGET:-$AUTO_FIT_TARGET}"
    if (( GPU_TOTAL_MIB >= 24000 )); then
      BATCH_SIZE="${BATCH_SIZE:-4096}"
      UBATCH_SIZE="${UBATCH_SIZE:-2048}"
    else
      BATCH_SIZE="${BATCH_SIZE:-2048}"
      UBATCH_SIZE="${UBATCH_SIZE:-512}"
    fi
    GPU_ARGS=(
      --fit on
      --fit-target "$FIT_TARGET"
      --flash-attn on
      --cache-type-k "$KV_CACHE_TYPE"
      --cache-type-v "$KV_CACHE_TYPE"
    )
    if (( GPU_HEADROOM_MIB >= 4096 )); then
      GPU_ARGS+=(--n-gpu-layers 999)
    fi
  else
    FIT_TARGET="N/A"
    BATCH_SIZE="${BATCH_SIZE:-1024}"
    UBATCH_SIZE="${UBATCH_SIZE:-256}"
    GPU_ARGS=(
      --n-gpu-layers 0
      --flash-attn on
      --cache-type-k "$KV_CACHE_TYPE"
      --cache-type-v "$KV_CACHE_TYPE"
    )
  fi

  TOTAL_POOL_MIB=$(( TOTAL_RAM_MIB + GPU_TOTAL_MIB ))
  HEADROOM_MIB=$(( TOTAL_POOL_MIB - MODEL_SIZE_MIB ))
  if (( GPU_DETECTED == 1 && MODEL_SIZE_MIB <= GPU_TOTAL_MIB )); then
    if (( GPU_HEADROOM_MIB >= 24000 )); then
      AUTO_CTX_SIZE=65536
    elif (( GPU_HEADROOM_MIB >= 10000 )); then
      AUTO_CTX_SIZE=32768
    elif (( GPU_HEADROOM_MIB >= 4000 )); then
      AUTO_CTX_SIZE=16384
    else
      AUTO_CTX_SIZE=8192
    fi
  elif (( HEADROOM_MIB >= 64000 )); then
    AUTO_CTX_SIZE=32768
  elif (( HEADROOM_MIB >= 18000 )); then
    AUTO_CTX_SIZE=16384
  elif (( HEADROOM_MIB >= 10000 )); then
    AUTO_CTX_SIZE=8192
  else
    AUTO_CTX_SIZE=4096
  fi
  CTX_SIZE="${CTX_SIZE:-$AUTO_CTX_SIZE}"

  FEATURE_ARGS=()
  if [[ "$SPEC_TYPE" != "none" && -n "$SPEC_TYPE" ]]; then
    FEATURE_ARGS+=(--spec-type "$SPEC_TYPE")
  fi
  if [[ "$REASONING_MODE" != "auto" && -n "$REASONING_MODE" ]]; then
    FEATURE_ARGS+=(--reasoning "$REASONING_MODE")
  fi
  if (( NUMA_NODES > 1 )); then
    FEATURE_ARGS+=(--numa distribute)
  fi

  if (( TOTAL_RAM_MIB >= 120000 || GPU_TOTAL_MIB >= 24000 || LOGICAL_CPUS >= 36 )); then
    REASONING_HW_TIER="ULTRA_SERVER_DATACENTER (15 Core Engines: 1,024-D VSA, 80x H-MDP, 1,200 RL eps, 32x K-Means++)"
  elif (( TOTAL_RAM_MIB >= 24000 && LOGICAL_CPUS >= 16 )); then
    REASONING_HW_TIER="EXTREME_WORKSTATION (15 Core Engines: 1,024-D VSA, 80x H-MDP, 600 RL eps, 20x K-Means++)"
  elif (( TOTAL_RAM_MIB >= 12000 && LOGICAL_CPUS >= 8 )); then
    REASONING_HW_TIER="HIGH_PERFORMANCE (15 Core Engines: 1,024-D VSA, 60x H-MDP, 400 RL eps, 12x K-Means++)"
  else
    REASONING_HW_TIER="PORTABLE_CONSERVATIVE (15 Core Engines: 1,024-D VSA, 40x H-MDP, 200 RL eps, 8x K-Means++)"
  fi

  SERVER_AGENT_ARGS=()
  if [[ "$AGENT_MODE" == "on" || "$AGENT_MODE" == "true" || "$AGENT_MODE" == "1" ]]; then
    SERVER_AGENT_ARGS+=(--agent --tools all)
  fi

  # NOTE: Do NOT enable DRY (--dry-multiplier) or high repeat-penalty by default for tool-calling agents!
  # DRY penalizes repeating n-grams from the prompt (like IP addresses `<TARGET_IP>` or file paths),
  # which forces the sampler to close JSON string quotes mid-IP (`http://172.24`, `http://192.16`, `192.1`).
  SAMPLING_GUARD_ARGS=(
    --repeat-penalty "${REPEAT_PENALTY:-1.02}"
    --repeat-last-n "${REPEAT_LAST_N:-64}"
  )
  if [[ -n "${DRY_MULTIPLIER:-}" && "${DRY_MULTIPLIER:-0}" != "0" ]]; then
    SAMPLING_GUARD_ARGS+=(
      --dry-multiplier "$DRY_MULTIPLIER"
      --dry-base "${DRY_BASE:-1.75}"
      --dry-allowed-length "${DRY_ALLOWED_LENGTH:-4}"
      --dry-penalty-last-n "${DRY_PENALTY_LAST_N:-256}"
    )
  fi
}

print_hardware_profile() {
  detect_hardware_and_tune
  printf '=== Auto-Detected Hardware & Tuning Profile ===\n'
  if (( P_CORES > 0 && E_CORES > 0 )); then
    printf '  CPU:            %s (%d physical cores: %d P-cores + %d E-cores, %d threads, %d NUMA node(s))\n' \
      "$CPU_NAME" "$PHYSICAL_CORES" "$P_CORES" "$E_CORES" "$LOGICAL_CPUS" "$NUMA_NODES"
  else
    printf '  CPU:            %s (%d physical cores, %d threads, %d NUMA node(s))\n' \
      "$CPU_NAME" "$PHYSICAL_CORES" "$LOGICAL_CPUS" "$NUMA_NODES"
  fi
  printf '  System RAM:     %d MiB total (%d MiB available)\n' "$TOTAL_RAM_MIB" "$AVAIL_RAM_MIB"
  if (( GPU_DETECTED == 1 )); then
    printf '  GPU:            %s (%d MiB total, %d MiB free, %d GPU(s) visible)\n' "$GPU_NAME" "$GPU_TOTAL_MIB" "$GPU_FREE_MIB" "$GPU_COUNT"
  else
    printf '  GPU:            %s\n' "$GPU_NAME"
  fi
  printf '  15-Engine Tier: %s\n' "$REASONING_HW_TIER"
  printf '  Selected Model: %s (%d MiB -> %s)\n' "$MODEL_ALIAS" "$MODEL_SIZE_MIB" "$(basename "$MODEL_PATH")"
  printf '  Reasoning Mode: %s (default: off for instant answers; pass --think to enable <think>)\n' "$REASONING_MODE"
  printf '  Agent Tools:    %s (read_file, write_file, edit_file, exec_shell_command, grep_search, ...)\n' "$AGENT_MODE"
  printf '  Tuned Settings: --ctx-size %s --reasoning %s --threads %s --threads-batch %s --batch-size %s --ubatch-size %s --spec-type %s' \
    "$CTX_SIZE" "$REASONING_MODE" "$THREADS" "$THREADS_BATCH" "$BATCH_SIZE" "$UBATCH_SIZE" "$SPEC_TYPE"
  if (( NUMA_NODES > 1 )); then
    printf ' --numa distribute'
  fi
  if (( GPU_DETECTED == 1 )); then
    printf ' --fit on --fit-target %s --flash-attn on -ctk %s -ctv %s\n' \
      "$FIT_TARGET" "$KV_CACHE_TYPE" "$KV_CACHE_TYPE"
  else
    printf ' --n-gpu-layers 0 --flash-attn on -ctk %s -ctv %s\n' \
      "$KV_CACHE_TYPE" "$KV_CACHE_TYPE"
  fi
  printf '===============================================\n'
}

is_llama_running() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid=$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || true)
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
  fi
  local live_pid
  live_pid=$(pgrep -f "$BIN_DIR/llama-server" 2>/dev/null | head -n 1 || true)
  if [[ -n "$live_pid" ]] && kill -0 "$live_pid" 2>/dev/null; then
    echo "$live_pid" > "$PID_FILE"
    if [[ ! -f "$ACTIVE_MODEL_FILE" ]]; then
      local cmdline
      cmdline=$(tr '\0' ' ' < "/proc/$live_pid/cmdline" 2>/dev/null || true)
      if [[ "$cmdline" == *"Qwen3.5"* ]]; then
        echo "Qwen3.5-9B-Uncensored-Q4_K_M (Qwen3.5-9B-Uncensored-Q4_K_M.gguf)" > "$ACTIVE_MODEL_FILE"
      elif [[ "$cmdline" == *"MTP-Q8_0"* || "$cmdline" == *"Turbo-MTP-Q8_0"* ]]; then
        echo "Qwen3.8-27B-Turbo-MTP-Q8_0 (Qwen3.8-27B-Turbo-MTP-Q8_0.gguf)" > "$ACTIVE_MODEL_FILE"
      elif [[ "$cmdline" == *"MTP-Q6_K"* || "$cmdline" == *"Turbo-MTP-Q6_K"* ]]; then
        echo "Qwen3.8-27B-Turbo-MTP-Q6_K (Qwen3.8-27B-Turbo-MTP-Q6_K.gguf)" > "$ACTIVE_MODEL_FILE"
      elif [[ "$cmdline" == *"MTP-Q4_K_M"* || "$cmdline" == *"Turbo-MTP-Q4_K_M"* ]]; then
        echo "Qwen3.8-27B-Turbo-MTP-Q4_K_M (Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf)" > "$ACTIVE_MODEL_FILE"
      elif [[ "$cmdline" == *"Qwen3.8"* ]]; then
        echo "Qwen3.8-27B-Uncensored-Q3_K_M (Qwen3.8-27B-Uncensored-Q3_K_M.gguf)" > "$ACTIVE_MODEL_FILE"
      fi
    fi
    return 0
  fi
  return 1
}

list_models() {
  resolve_model "$MODEL_SELECT"
  local running_model="NONE (stopped)"
  if is_llama_running && [[ -f "$ACTIVE_MODEL_FILE" ]]; then
    running_model=$(<"$ACTIVE_MODEL_FILE")
  fi
  printf '=== Installed & Available CORA Models ===\n'
  printf '  1. [DEFAULT]  qwen3.8 (-m 3.8 | 27b | q3)            -> Qwen3.8-27B-Uncensored-Q3_K_M.gguf (~12.4 GiB)\n'
  if [[ -f "$MODELS_DIR/$QWEN38_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN38_FILE" | awk '{print $1}')"
  else
    printf '     Status: Not downloaded yet (auto-downloads with: ./run_cora_NIX.sh download -m 3.8)\n'
  fi
  printf '  2. [FAST]     qwen3.5 (-m 3.5 | 9b | fast)           -> Qwen3.5-9B-Uncensored-Q4_K_M.gguf (~5.2 GiB, HauhauCS-Aggressive)\n'
  if [[ -f "$MODELS_DIR/$QWEN35_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN35_FILE" | awk '{print $1}')"
  else
    printf '     Status: Not downloaded yet (auto-downloads with: ./run_cora_NIX.sh download -m 3.5)\n'
  fi
  printf '  3. [MTP-Q4]   turbo (-m turbo | mtp | turbo-q4 | q4) -> Qwen3.8-27B-Turbo-MTP-Q4_K_M.gguf (~17.2 GiB, Multiple Token Prediction)\n'
  if [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q4_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN38_TURBO_Q4_FILE" | awk '{print $1}')"
  elif [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q4_HF_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN38_TURBO_Q4_HF_FILE" | awk '{print $1}')"
  else
    printf '     Status: Available for auto-download (./run_cora_NIX.sh download -m turbo  OR  ./run_cora_NIX.sh cli -m turbo)\n'
  fi
  printf '  4. [MTP-Q6]   turbo-q6 (-m turbo-q6 | mtp-q6 | q6)   -> Qwen3.8-27B-Turbo-MTP-Q6_K.gguf (~22.4 GiB, Multiple Token Prediction)\n'
  if [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q6_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN38_TURBO_Q6_FILE" | awk '{print $1}')"
  elif [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q6_HF_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN38_TURBO_Q6_HF_FILE" | awk '{print $1}')"
  else
    printf '     Status: Available for auto-download (./run_cora_NIX.sh download -m turbo-q6  OR  ./run_cora_NIX.sh cli -m turbo-q6)\n'
  fi
  printf '  5. [MTP-Q8]   turbo-q8 (-m turbo-q8 | mtp-q8 | q8)   -> Qwen3.8-27B-Turbo-MTP-Q8_0.gguf (~28.2 GiB, Multiple Token Prediction)\n'
  if [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q8_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN38_TURBO_Q8_FILE" | awk '{print $1}')"
  elif [[ -f "$MODELS_DIR/$QWEN38_TURBO_Q8_HF_FILE" ]]; then
    printf '     Status: Installed (%s)\n' "$(du -Lh "$MODELS_DIR/$QWEN38_TURBO_Q8_HF_FILE" | awk '{print $1}')"
  else
    printf '     Status: Available for auto-download (./run_cora_NIX.sh download -m turbo-q8  OR  ./run_cora_NIX.sh cli -m turbo-q8)\n'
  fi
  printf '\n  Currently Running: %s\n' "$running_model"
  printf '==============================================\n'
}

is_webui_running() {
  if curl -sS -m 2 "http://${HOST}:${WEBUI_PORT}/api/health" 2>/dev/null | grep -q '"cora-webui"'; then
    return 0
  fi
  if [[ -f "$WEBUI_PID_FILE" ]]; then
    local wpid
    wpid=$(tr -d '[:space:]' < "$WEBUI_PID_FILE" 2>/dev/null || true)
    if [[ -n "$wpid" ]] && kill -0 "$wpid" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

ensure_webui_python_deps() {
  if ! python3 -c "import fastapi, uvicorn, psutil, pydantic" >/dev/null 2>&1; then
    if [[ -f "$BASE_DIR/webui/requirements.txt" ]]; then
      printf 'Installing CORA WebUI Python dependencies (%s/webui/requirements.txt)...\n' "$BASE_DIR"
      python3 -m pip install -q -r "$BASE_DIR/webui/requirements.txt" 2>/dev/null || \
        python3 -m pip install --break-system-packages -q -r "$BASE_DIR/webui/requirements.txt" 2>/dev/null || true
    fi
  fi
}

start_cora_webui() {
  local open_browser="${1:-1}"
  if [[ ! -f "$BASE_DIR/webui/server.py" ]]; then
    printf 'Warning: Custom CORA WebUI server not found at %s\n' "$BASE_DIR/webui/server.py" >&2
    return 0
  fi
  local no_browser=0
  local arg
  for arg in "${EXTRA_ARGS[@]:-}"; do
    if [[ "$arg" == "--no-browser" || "$arg" == "-no-browser" ]]; then
      no_browser=1
    fi
  done
  local url="http://${HOST}:${WEBUI_PORT}"

  ensure_webui_python_deps
  if [[ -n "${CORA_ACTIVE_PROJECT:-}" && "${CORA_ACTIVE_PROJECT,,}" != "active_session" && "${CORA_ACTIVE_PROJECT,,}" != "default" ]]; then
    mkdir -p "$PROJECTS_DIR/${CORA_ACTIVE_PROJECT}/Files" 2>/dev/null || true
  fi

  if ! is_llama_running; then
    resolve_model "$MODEL_SELECT"
    HW_TUNED_DONE=0
    detect_hardware_and_tune
    if [[ -f "$MODEL_PATH" && -x "$BIN_DIR/llama-server" ]]; then
      printf 'Starting llama-server (%s) on http://%s:%s ...\n' "$MODEL_ALIAS" "$HOST" "$LLAMA_PORT"
      export LD_LIBRARY_PATH="$BIN_DIR:${LD_LIBRARY_PATH:-}"
      nohup "$BIN_DIR/llama-server" \
        --model "$MODEL_PATH" \
        --alias "$MODEL_ALIAS" \
        --host "$HOST" \
        --port "$LLAMA_PORT" \
        --ctx-size "$CTX_SIZE" \
        --parallel 1 \
        --context-shift \
        --no-reasoning-preserve \
        "${GPU_ARGS[@]}" \
        "${FEATURE_ARGS[@]}" \
        "${SAMPLING_GUARD_ARGS[@]}" \
        --threads "$THREADS" \
        --threads-batch "$THREADS_BATCH" \
        --batch-size "$BATCH_SIZE" \
        --ubatch-size "$UBATCH_SIZE" \
        --cont-batching \
        --no-webui \
        > "$LOG_FILE" 2>&1 &
      echo $! > "$PID_FILE"
      echo "$MODEL_ALIAS ($(basename "$MODEL_PATH"))" > "$ACTIVE_MODEL_FILE"
    fi
  fi
  if is_webui_running; then
    local wpid="active"
    [[ -f "$WEBUI_PID_FILE" ]] && wpid=$(tr -d '[:space:]' < "$WEBUI_PID_FILE" 2>/dev/null || echo "active")
    printf 'Custom CORA WebUI is already running (PID %s) -> %s\n' "$wpid" "$url"
    printf 'Verifying local LLM (llama-server) readiness...'
    if curl -sS -m 90 -X POST "${url}/api/models/start" -H "Content-Type: application/json" -d '{"force_restart":false}' 2>/dev/null | grep -q '"ok":true'; then
      printf ' ONLINE\n'
    else
      printf ' Loading in background...\n'
    fi
    if (( open_browser == 1 && no_browser == 0 )) && [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && command -v xdg-open >/dev/null 2>&1; then
      xdg-open "$url" >/dev/null 2>&1 &
    fi
    return 0
  fi

  # Ensure no stale process is holding port 1337 before starting the single WebUI instance
  if command -v fuser >/dev/null 2>&1; then
    fuser -k "${WEBUI_PORT}/tcp" >/dev/null 2>&1 || true
  fi
  pkill -f "webui/server.py" >/dev/null 2>&1 || true

  printf 'Starting Custom CORA WebUI (Svelte + FastAPI + 15-Engine Dashboard + Project Files/) on %s ' "$url"
  nohup python3 "$BASE_DIR/webui/server.py" --host "$HOST" --port "$WEBUI_PORT" > "$WEBUI_LOG_FILE" 2>&1 &
  local wproc_pid=$!
  echo "$wproc_pid" > "$WEBUI_PID_FILE"
  local ready=0
  for _ in {1..25}; do
    if ! kill -0 "$wproc_pid" 2>/dev/null; then
      printf '\nError: Custom CORA WebUI exited during startup. Log output:\n' >&2
      tail -n 25 "$WEBUI_LOG_FILE" >&2 2>/dev/null || true
      return 1
    fi
    if curl -sS -m 1 "${url}/api/health" 2>/dev/null | grep -q '"ok"'; then
      ready=1
      break
    fi
    printf '.'
    sleep 0.4
  done
  printf '\n'
  if (( ready == 1 )); then
    printf 'Custom CORA WebUI is LIVE (PID %s) -> %s\n' "$wproc_pid" "$url"
    printf 'Ensuring local LLM (llama-server) is ONLINE and ready...'
    if curl -sS -m 90 -X POST "${url}/api/models/start" -H "Content-Type: application/json" -d '{"force_restart":false}' 2>/dev/null | grep -q '"ok":true'; then
      printf ' ONLINE\n'
    else
      printf ' Loading in background...\n'
    fi
    if (( open_browser == 1 && no_browser == 0 )) && [[ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]] && command -v xdg-open >/dev/null 2>&1; then
      printf 'Opening %s in your default browser...\n' "$url"
      xdg-open "$url" >/dev/null 2>&1 &
    fi
  else
    printf 'Custom CORA WebUI process started (PID %s) -> %s\n' "$wproc_pid" "$url"
  fi
}

stop_cora_webui() {
  local stopped_any=0
  if [[ -f "$WEBUI_PID_FILE" ]]; then
    local wpid
    wpid=$(tr -d '[:space:]' < "$WEBUI_PID_FILE" 2>/dev/null || true)
    if [[ -n "$wpid" ]] && kill -0 "$wpid" 2>/dev/null; then
      printf 'Stopping Custom CORA WebUI (PID %s)...\n' "$wpid"
      kill "$wpid" 2>/dev/null || true
      stopped_any=1
    fi
  fi
  if pgrep -f "webui/server.py" >/dev/null 2>&1; then
    (( stopped_any == 0 )) && printf 'Stopping Custom CORA WebUI process on port %s...\n' "$WEBUI_PORT"
    pkill -f "webui/server.py" >/dev/null 2>&1 || true
  fi
  if command -v fuser >/dev/null 2>&1; then
    fuser -k "${WEBUI_PORT}/tcp" >/dev/null 2>&1 || true
  fi
  rm -f "$WEBUI_PID_FILE" 2>/dev/null || true
}

start_services() {
  resolve_model "$MODEL_SELECT"
  ensure_selected_model_downloaded
  HW_TUNED_DONE=0
  detect_hardware_and_tune

  if [[ ! -f "$MODEL_PATH" ]]; then
    printf 'Error: Model file not found at %s\n' "$MODEL_PATH" >&2
    exit 1
  fi

  # When starting the Web Interface interactively, display the C.O.R.A. splash screen
  # and require selecting or creating a project in /Projects and choosing a Session Personality Mode
  # before interacting with the LLM.
  local has_no_browser=0
  local _ea
  for _ea in "${EXTRA_ARGS[@]:-}"; do
    if [[ "$_ea" == "--no-browser" || "$_ea" == "-no-browser" ]]; then
      has_no_browser=1
    fi
  done
  rm -f "$BASE_DIR/Log/active_session_mode.env" 2>/dev/null || true
  if [[ -t 0 && -t 1 && "${CORA_NON_INTERACTIVE:-0}" != "1" && -z "${CORA_ACTIVE_PROJECT:-}" && "$has_no_browser" == "0" ]]; then
    python3 "$BASE_DIR/agent-cli.py" --select-project-only
  fi
  if [[ -f "$BASE_DIR/Log/active_session_mode.env" ]]; then
    # shellcheck disable=SC1090
    source "$BASE_DIR/Log/active_session_mode.env"
  fi
  if [[ -z "${CORA_ACTIVE_PROJECT:-}" && -f "$BASE_DIR/Reasoning/data/sessions/active_project.txt" ]]; then
    export CORA_ACTIVE_PROJECT
    CORA_ACTIVE_PROJECT=$(head -n 1 "$BASE_DIR/Reasoning/data/sessions/active_project.txt" | tr -d '\r\n')
  fi
  export CORA_ACTIVE_PROJECT="${CORA_ACTIVE_PROJECT:-}"
  export CORA_PERSONALITY_MODE="${CORA_PERSONALITY_MODE:-DEFAULT}"

  # Enforce Analyst Mode network isolation & external scan/egress block in WebGUI / llama-server
  if [[ "${CORA_PERSONALITY_MODE}" == "ANALYST" ]]; then
    export LLM_ISOLATION_MODE="WHITE"
    export LLM_POSTURE_OVERRIDE="WHITE"
    export LLM_ALLOWED_IFACES="lo"
    HOST="127.0.0.1"
    SERVER_AGENT_ARGS=()
    printf '  [ANALYST MODE ENFORCED] WebGUI / llama-server locked to WHITE isolation (127.0.0.1 loopback only; external network scanning & agent shell tools disabled).\n'
  fi

  print_hardware_profile

  local srv_extra_args=()
  local skip_next=0
  for ((i=0; i<${#EXTRA_ARGS[@]}; i++)); do
    if (( skip_next > 0 )); then
      ((skip_next--))
      continue
    fi
    case "${EXTRA_ARGS[$i]}" in
      -netiso|--network-isolation)
        if [[ "${EXTRA_ARGS[$((i+1))]:-}" == "blue" && -n "${EXTRA_ARGS[$((i+2))]:-}" && "${EXTRA_ARGS[$((i+2))]}" != -* ]]; then
          skip_next=2
        else
          skip_next=1
        fi
        ;;
      -P|--project)
        skip_next=1
        ;;
      --continue|-c|--no-browser|-no-browser|--hud|--no-hud|--keep-server|--keep-alive|-P:*|--project:*|-P=*|--project=*)
        ;;
      *)
        srv_extra_args+=("${EXTRA_ARGS[$i]}")
        ;;
    esac
  done

  if is_llama_running; then
    printf 'llama-server is already running (PID %s, Model: %s). Use "./run_cora_NIX.sh restart -m %s" to switch models.\n' \
      "$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || echo active)" "$(tr -d '\r\n' < "$ACTIVE_MODEL_FILE" 2>/dev/null || echo unknown)" "$MODEL_KEY"
  else
    printf 'Starting llama-server (%s) on http://%s:%s (Active Project: %s) ...\n' \
      "$MODEL_ALIAS" "$HOST" "$LLAMA_PORT" "${CORA_ACTIVE_PROJECT:-select-in-webui}"
    export LD_LIBRARY_PATH="$BIN_DIR:${LD_LIBRARY_PATH:-}"
    nohup "$BIN_DIR/llama-server" \
      --model "$MODEL_PATH" \
      --alias "$MODEL_ALIAS" \
      --host "$HOST" \
      --port "$LLAMA_PORT" \
      --ctx-size "$CTX_SIZE" \
      --parallel 1 \
      --context-shift \
      --no-reasoning-preserve \
      "${GPU_ARGS[@]}" \
      "${FEATURE_ARGS[@]}" \
      "${SERVER_AGENT_ARGS[@]}" \
      "${SAMPLING_GUARD_ARGS[@]}" \
      --threads "$THREADS" \
      --threads-batch "$THREADS_BATCH" \
      --batch-size "$BATCH_SIZE" \
      --ubatch-size "$UBATCH_SIZE" \
      --cont-batching \
      --no-webui \
      ${srv_extra_args[@]+"${srv_extra_args[@]}"} \
      > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "$MODEL_ALIAS ($(basename "$MODEL_PATH"))" > "$ACTIVE_MODEL_FILE"
    printf 'llama-server started (PID %s, Model: %s). Waiting for model load...\n' "$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || echo active)" "$MODEL_ALIAS"
  fi

  start_cora_webui
}

run_cli() {
  resolve_model "$MODEL_SELECT"
  ensure_selected_model_downloaded
  HW_TUNED_DONE=0
  detect_hardware_and_tune
  if [[ ! -f "$MODEL_PATH" ]]; then
    printf 'Error: Model file not found at %s\n' "$MODEL_PATH" >&2
    exit 1
  fi

  pkill -f "$BIN_DIR/llama-cli" 2>/dev/null || true

  local running_now=0
  if is_llama_running; then
    running_now=1
  fi
  local current_active=""
  if [[ -f "$ACTIVE_MODEL_FILE" ]]; then
    current_active=$(tr -d '\r\n' < "$ACTIVE_MODEL_FILE" 2>/dev/null || true)
  fi

  if (( running_now == 0 )) || [[ "$current_active" != "$MODEL_ALIAS"* ]]; then
    if (( running_now == 1 )); then
      printf 'Switching running llama-server to %s ...\n' "$MODEL_ALIAS"
      kill "$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || true)" 2>/dev/null || true
      rm -f "$PID_FILE" "$ACTIVE_MODEL_FILE"
      sleep 1
    fi
    print_hardware_profile
    printf 'Starting local llama-server backend (%s) on http://%s:%s ...\n' "$MODEL_ALIAS" "$HOST" "$LLAMA_PORT"
    export LD_LIBRARY_PATH="$BIN_DIR:${LD_LIBRARY_PATH:-}"
    nohup "$BIN_DIR/llama-server" \
      --model "$MODEL_PATH" \
      --alias "$MODEL_ALIAS" \
      --host "$HOST" \
      --port "$LLAMA_PORT" \
      --ctx-size "$CTX_SIZE" \
      --parallel 1 \
      --context-shift \
      --no-reasoning-preserve \
      "${GPU_ARGS[@]}" \
      "${FEATURE_ARGS[@]}" \
      "${SAMPLING_GUARD_ARGS[@]}" \
      --threads "$THREADS" \
      --threads-batch "$THREADS_BATCH" \
      --batch-size "$BATCH_SIZE" \
      --ubatch-size "$UBATCH_SIZE" \
      --cont-batching \
      --no-webui \
      > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "$MODEL_ALIAS ($(basename "$MODEL_PATH"))" > "$ACTIVE_MODEL_FILE"
  else
    print_hardware_profile
  fi

  printf 'Waiting for %s backend to become ready ' "$MODEL_ALIAS"
  local ready=0
  for _ in {1..90}; do
    if ! is_llama_running; then
      printf '\nError: llama-server exited during startup. Last log lines:\n' >&2
      tail -n 20 "$LOG_FILE" >&2
      exit 1
    fi
    if curl -sf "http://$HOST:$LLAMA_PORT/health" 2>/dev/null | grep -q '"ok"'; then
      ready=1
      break
    fi
    printf '.'
    sleep 1
  done
  printf '\n'
  if (( ready == 0 )); then
    printf 'Error: Timed out waiting for llama-server on http://%s:%s\n' "$HOST" "$LLAMA_PORT" >&2
    exit 1
  fi

  export LLAMA_API_URL="http://$HOST:$LLAMA_PORT/v1/chat/completions"
  export MODEL_ALIAS="$MODEL_ALIAS"
  export SKIP_PERMISSIONS="$SKIP_PERMISSIONS"
  export REASONING_MODE="$REASONING_MODE"

  KEEP_SRV_ON_EXIT=0
  for arg in "${EXTRA_ARGS[@]:-}"; do
    if [[ "$arg" == "--keep-server" || "$arg" == "--keep-alive" ]]; then
      KEEP_SRV_ON_EXIT=1
      export KEEP_SERVER_ON_EXIT=1
    fi
  done

  cleanup_cli_session() {
    rm -f "$BASE_DIR/Log/active_session_mode.env" 2>/dev/null || true
    if (( ${KEEP_SRV_ON_EXIT:-0} == 0 )) && [[ -f "$PID_FILE" ]]; then
      local srv_pid
      srv_pid=$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || true)
      if [[ -n "$srv_pid" ]] && kill -0 "$srv_pid" 2>/dev/null; then
        kill "$srv_pid" 2>/dev/null || true
      fi
      rm -f "$PID_FILE" "$ACTIVE_MODEL_FILE"
    fi
  }
  trap cleanup_cli_session EXIT INT TERM HUP

  python3 "$BASE_DIR/agent-cli.py" ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}
}

stop_services() {
  rm -f "$BASE_DIR/Log/active_session_mode.env" 2>/dev/null || true
  if is_llama_running; then
    local pid
    pid=$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || true)
    printf 'Stopping llama-server (PID %s)...\n' "$pid"
    kill "$pid" 2>/dev/null || true
    rm -f "$PID_FILE" "$ACTIVE_MODEL_FILE"
  else
    printf 'llama-server is not running.\n'
    rm -f "$PID_FILE" "$ACTIVE_MODEL_FILE"
  fi

  stop_cora_webui
}

status_services() {
  print_hardware_profile
  printf '\nService Status:\n'
  if is_llama_running; then
    local active_mod
    active_mod=$(tr -d '\r\n' < "$ACTIVE_MODEL_FILE" 2>/dev/null || echo "$MODEL_ALIAS")
    printf '  llama-server: RUNNING (PID %s)\n' "$(tr -d '[:space:]' < "$PID_FILE" 2>/dev/null || echo active)"
    printf '  Active Model: %s\n' "$active_mod"
    printf '  Llama API:    http://%s:%s (OpenAI-compatible API & llama.cpp server)\n' "$HOST" "$LLAMA_PORT"
  else
    printf '  llama-server: STOPPED\n'
  fi
  if is_webui_running; then
    printf '  CORA WebUI:   RUNNING (PID %s) -> http://%s:%s (Custom Svelte/FastAPI Dashboard)\n' "$(tr -d '[:space:]' < "$WEBUI_PID_FILE" 2>/dev/null || echo active)" "$HOST" "$WEBUI_PORT"
  else
    printf '  CORA WebUI:   STOPPED (Start with: ./run_cora_NIX.sh webui  or  ./run_cora_NIX.sh start)\n'
  fi
  if command -v nvidia-smi >/dev/null 2>&1; then
    printf '\nGPU Memory Usage:\n'
    nvidia-smi --query-gpu=name,memory.used,memory.free,memory.total,utilization.gpu --format=csv
  fi
}

case "$ACTION" in
  start)          start_services ;;
  stop)           stop_services ;;
  restart)        stop_services; sleep 1; start_services ;;
  status)         status_services ;;
  webui)          start_cora_webui ;;
  models)         list_models ;;
  download)       cmd_download_models "${EXTRA_ARGS[0]:-$MODEL_SELECT}" ;;
  tune|detect)    print_hardware_profile ;;
  cli)            run_cli ;;
  reason|reasoning) exec python3 "$BASE_DIR/Reasoning/reasoning_cli.py" ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"} ;;
  train)          exec bash "$TRAINING_DIR/train_llm_NIX.sh" ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"} ;;
  posture)        exec bash "$BASE_DIR/Network_Isolation/ConsolePostureDetection_NIX.sh" ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"} ;;
  troubleshoot|diag|diagnostics) exec bash "$CORA_ROOT/Troubleshooting/troubleshoot_llm_NIX.sh" ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"} ;;
  logs)           tail -n 50 -f "$LOG_FILE" ;;
  -h|--help|help) usage ;;
  *)              usage >&2; exit 2 ;;
esac
