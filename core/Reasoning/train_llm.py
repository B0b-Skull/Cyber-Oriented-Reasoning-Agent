#!/usr/bin/env python3
"""
CORA 4-Phase Multi-Modal Document, OCR & Network Diagram Training Engine (`train_llm.py`)
============================================================================================
Reads local documentation, playbooks, PDFs, Office docs, and network diagram images from
`Training/` (or any specified folder/file), extracts actionable commands, processes,
techniques, and visual network topologies, verifies every command through Engine 12 (CEGAR),
and stores structured intelligence into:
  1. Tier-2 Obsidian Vault (`ObsidianVault/commands/trained_*.md`, `ObsidianVault/knowledge/trained_*.md`,
     and `ObsidianVault/00_TRAINED_INDEX.md`) — with only a single compact pointer in `00_MEMORY_INDEX.md`
     so the LLM context window is NEVER overloaded.
  2. Symbolic Reasoning Engine Rules (`Reasoning/data/trained_rules.json`) — dynamically loaded by
     Engine 1 (Associative Vault Graph), Engine 2 (Geometric/Z3), Engine 6 (Analogy),
     Engine 11 (Case-Based Fingerprints), and Engine 14 (Evolutionary MAP-Elites).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REASONING_DIR = Path(__file__).resolve().parent
CORA_CORE_DIR = REASONING_DIR.parent
CORA_ROOT = CORA_CORE_DIR.parent if CORA_CORE_DIR.name.lower() == "core" else CORA_CORE_DIR
if str(CORA_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORA_CORE_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from Reasoning.engines.cegar_verifier import verify_command_cegar
from Reasoning.engines.mdp_tactical import (
    classify_tactic_category,
    load_or_init_mdp_store,
    merge_trained_mdp_transitions,
)
from Reasoning.engines.vault_bridge import (
    DATA_DIR,
    VAULT_DIR,
    _atomic_write_text,
    ensure_directories,
    save_json_state,
)

DEFAULT_TRAINING_DIR = Path(os.environ.get("CORA_TRAINING_DIR") or str(CORA_ROOT / "Training")).resolve()
LOG_DIR = CORA_CORE_DIR / "Log"
TRAINING_LOG_FILE = LOG_DIR / "training.log"
MANIFEST_FILE = DATA_DIR / "training_manifest.json"
TRAINED_RULES_FILE = DATA_DIR / "trained_rules.json"
TRAINED_INDEX_FILE = VAULT_DIR / "00_TRAINED_INDEX.md"
MEMORY_INDEX_FILE = VAULT_DIR / "00_MEMORY_INDEX.md"

API_URL = os.environ.get("LLAMA_API_URL", "http://127.0.0.1:8080/v1/chat/completions")
CHUNK_MAX_CHARS = 6000

SUPPORTED_TEXT_EXTS = {
    ".md", ".txt", ".rst", ".sh", ".bash", ".zsh", ".ps1", ".py",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".csv", ".tsv", ".xml", ".log", ".sql", ".lua",
}
SUPPORTED_HTML_EXTS = {".html", ".htm"}
SUPPORTED_DOC_EXTS = {".pdf", ".docx"}
SUPPORTED_VECTOR_EXTS = {".svg", ".drawio", ".mmd", ".dot"}
SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}
ALL_SUPPORTED_EXTS = (
    SUPPORTED_TEXT_EXTS
    | SUPPORTED_HTML_EXTS
    | SUPPORTED_DOC_EXTS
    | SUPPORTED_VECTOR_EXTS
    | SUPPORTED_IMAGE_EXTS
)

_OCR_ENGINE_INSTANCE: Any = None


def _log_training(msg: str) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(LOG_DIR, 0o775)
        except OSError:
            pass
        ts = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
        with open(TRAINING_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
        try:
            os.chmod(TRAINING_LOG_FILE, 0o664)
        except OSError:
            pass
    except Exception:
        pass


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", text.strip().lower()).strip("_")
    return s[:64] or "doc"


def _portable_path(p: Path | str) -> str:
    try:
        rel = Path(p).resolve().relative_to(CORA_ROOT.resolve())
        return f"~/Projects/CORA/{rel.as_posix()}"
    except Exception:
        pass
    try:
        rel = Path(p).resolve().relative_to(CORA_CORE_DIR.resolve())
        return f"~/Projects/CORA/core/{rel.as_posix()}"
    except Exception:
        pass
    s = str(p)
    home_s = str(Path.home())
    if home_s and s.startswith(home_s):
        return ("~" + s[len(home_s) :]).replace("\\", "/")
    return s.replace("\\", "/")


def resolve_training_target(target_path: Optional[Path | str] = None) -> Path:
    """
    Resolve a training folder or file path relative to CWD, CORA_ROOT, or DEFAULT_TRAINING_DIR.
    Aliases legacy `TrainingDocuments` to `DEFAULT_TRAINING_DIR` (`CORA/Training`).
    """
    if not target_path:
        return DEFAULT_TRAINING_DIR
    raw_s = str(target_path).strip()
    norm_s = raw_s.strip("./\\").lower()
    if not raw_s or norm_s in ("training", "trainingdocuments"):
        return DEFAULT_TRAINING_DIR
    p_cand = Path(raw_s).expanduser()
    if p_cand.exists():
        return p_cand.resolve()
    for base in (CORA_ROOT, DEFAULT_TRAINING_DIR, CORA_CORE_DIR):
        alt = base / raw_s
        if alt.exists():
            return alt.resolve()
    return p_cand.resolve()


def check_and_install_dependencies(auto_install: bool = True) -> Dict[str, Any]:
    """
    Verify (and optionally auto-install) Python packages required for PDF, DOCX, HTML,
    Image Processing, and Neural OCR (`rapidocr_onnxruntime` / `pytesseract`).
    """
    module_map = {
        "PIL": "pillow",
        "pypdf": "pypdf",
        "pymupdf": "pymupdf",
        "docx": "python-docx",
        "bs4": "beautifulsoup4",
        "rapidocr_onnxruntime": "rapidocr-onnxruntime",
        "pytesseract": "pytesseract",
    }
    status: Dict[str, bool] = {}
    missing_pkgs: List[str] = []

    for mod_name, pip_pkg in module_map.items():
        try:
            __import__(mod_name)
            status[mod_name] = True
        except ImportError:
            status[mod_name] = False
            missing_pkgs.append(pip_pkg)

    iso_white = os.environ.get("LLM_ISOLATION_MODE", "").strip().lower() == "white"
    mode_analyst = os.environ.get("CORA_PERSONALITY_MODE", "").strip().upper() == "ANALYST"
    if missing_pkgs and auto_install and not iso_white and not mode_analyst:
        print(f"  [Auto-Installer] Installing missing extraction/OCR packages: {', '.join(missing_pkgs)} ...", flush=True)
        in_venv = (sys.prefix != getattr(sys, "base_prefix", sys.prefix)) or bool(os.environ.get("VIRTUAL_ENV"))
        flag_sets = ([], ["--break-system-packages"]) if in_venv else ([], ["--user"], ["--break-system-packages"], ["--user", "--break-system-packages"])
        install_args = [*missing_pkgs, "numpy<2"]
        installed_batch = False
        for flags in flag_sets:
            try:
                proc = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--quiet", *flags, *install_args],
                    capture_output=True,
                    text=True,
                    timeout=240,
                    check=False,
                )
                if proc.returncode == 0:
                    installed_batch = True
                    break
            except Exception:
                pass
        if not installed_batch:
            for pkg in missing_pkgs:
                for flags in flag_sets:
                    try:
                        proc = subprocess.run(
                            [sys.executable, "-m", "pip", "install", "--quiet", *flags, pkg],
                            capture_output=True,
                            text=True,
                            timeout=180,
                            check=False,
                        )
                        if proc.returncode == 0:
                            break
                    except Exception:
                        pass
        try:
            import importlib
            import site

            importlib.invalidate_caches()
            site.main()
        except Exception:
            pass
        # Re-check after installation attempt
        for mod_name in module_map:
            try:
                __import__(mod_name)
                status[mod_name] = True
            except ImportError:
                status[mod_name] = False

    tesseract_bin = shutil.which("tesseract") is not None
    pdftotext_bin = shutil.which("pdftotext") is not None
    return {
        "python_modules": status,
        "ocr_ready": bool(status.get("rapidocr_onnxruntime") or (status.get("pytesseract") and tesseract_bin)),
        "pdf_ready": bool(status.get("pymupdf") or status.get("pypdf") or pdftotext_bin),
        "docx_ready": bool(status.get("docx")),
        "html_ready": bool(status.get("bs4")),
        "tesseract_binary": tesseract_bin,
        "pdftotext_binary": pdftotext_bin,
    }


def _get_ocr_engine() -> Any:
    """Lazy-initialize the CPU ONNX RapidOCR engine (`0 MB GPU VRAM`)."""
    global _OCR_ENGINE_INSTANCE
    if _OCR_ENGINE_INSTANCE is not None:
        return _OCR_ENGINE_INSTANCE
    try:
        from rapidocr_onnxruntime import RapidOCR

        _OCR_ENGINE_INSTANCE = RapidOCR()
        return _OCR_ENGINE_INSTANCE
    except Exception:
        return None


# ---------------------------------------------------------------------------
# PHASE 1: Multi-Modal Document, PDF, Image OCR & Network Diagram Extractor
# ---------------------------------------------------------------------------
def _extract_image_ocr_and_topology(image_path_or_bytes: Any, source_label: str = "diagram") -> Dict[str, Any]:
    """
    Runs Neural OCR (`RapidOCR` ONNX CPU or `pytesseract`) on an image (`.png`, `.jpg`, `.webp`,
    or embedded PDF diagram) and reconstructs spatial network diagram clusters (hosts, IPs,
    subnets, interfaces, ports, and links).
    """
    ocr_boxes: List[Dict[str, Any]] = []
    raw_lines: List[str] = []

    engine = _get_ocr_engine()
    if engine is not None:
        try:
            result, _ = engine(image_path_or_bytes)
            if result:
                for item in result:
                    box, text, score = item[0], str(item[1]).strip(), float(item[2])
                    if not text or score < 0.35:
                        continue
                    xs = [ float(pt[0]) for pt in box ]
                    ys = [ float(pt[1]) for pt in box ]
                    cx = sum(xs) / len(xs)
                    cy = sum(ys) / len(ys)
                    ocr_boxes.append({"cx": cx, "cy": cy, "text": text, "score": round(score, 3)})
        except Exception:
            pass

    if not ocr_boxes:
        # Fallback to pytesseract if installed
        try:
            import pytesseract
            from PIL import Image

            img = Image.open(image_path_or_bytes) if isinstance(image_path_or_bytes, (str, Path)) else None
            if img is not None:
                txt = pytesseract.image_to_string(img)
                for idx, ln in enumerate(txt.splitlines()):
                    if ln.strip():
                        ocr_boxes.append({"cx": 100.0, "cy": float(idx * 25), "text": ln.strip(), "score": 0.8})
        except Exception:
            pass

    # Sort OCR boxes top-to-bottom, left-to-right for natural reading order
    ocr_boxes.sort(key=lambda b: (round(b["cy"] / 24.0), b["cx"]))
    raw_lines = [b["text"] for b in ocr_boxes]

    # Spatial Network Diagram Topology Clustering:
    # Group nearby labels (within Euclidean distance <= 190 px) into visual diagram nodes
    clusters: List[List[str]] = []
    visited = [False] * len(ocr_boxes)
    for i, b1 in enumerate(ocr_boxes):
        if visited[i]:
            continue
        visited[i] = True
        cluster_texts = [b1["text"]]
        for j, b2 in enumerate(ocr_boxes):
            if not visited[j]:
                dist = math.hypot(b1["cx"] - b2["cx"], b1["cy"] - b2["cy"])
                if dist <= 185.0:
                    visited[j] = True
                    cluster_texts.append(b2["text"])
        clusters.append(cluster_texts)

    full_ocr_text = "\n".join(raw_lines)
    ips = sorted(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b", full_ocr_text)))
    ifaces = sorted(
        set(
            re.findall(
                r"\b(?:eth\d+|wlan\d+|enp\d+s\d+|ens\d+|lo|br-[a-z0-9]+|docker\d+|veth[a-z0-9]+|/dev/ttyUSB\d+|ttyUSB\d+|ttyACM\d+|vlan\d+|tun\d+|tap\d+)\b",
                full_ocr_text,
                flags=re.I,
            )
        )
    )
    ports = sorted(set(re.findall(r"\b(?:port\s+\d{2,5}|:\d{2,5}|80|443|8080|8443|22|53|3000|514)\b", full_ocr_text, flags=re.I)))

    topo_lines = [f"### Visual & Network Diagram Intelligence (`{source_label}`)"]
    if ips:
        topo_lines.append(f"- **Diagram IPv4 / Subnets:** `{', '.join(ips)}`")
    if ifaces:
        topo_lines.append(f"- **Diagram Interfaces / Serial Ports:** `{', '.join(ifaces)}`")
    if ports:
        topo_lines.append(f"- **Diagram Ports / Services:** `{', '.join(ports[:15])}`")
    if clusters:
        topo_lines.append("- **Spatially Grouped Diagram Nodes (Box/Component Clusters):**")
        for idx, cl in enumerate(clusters[:18], 1):
            joined = " | ".join(cl)
            topo_lines.append(f"  {idx}. `[{joined}]`")

    return {
        "ocr_text": full_ocr_text,
        "topology_markdown": "\n".join(topo_lines),
        "ips": ips,
        "interfaces": ifaces,
        "ports": ports,
        "box_count": len(ocr_boxes),
    }


def _extract_svg_topology(svg_path: Path) -> Dict[str, Any]:
    """Extracts text nodes, boxes, and network topology entities from an `.svg` or `.drawio` vector diagram."""
    raw = svg_path.read_text(encoding="utf-8", errors="replace")
    texts: List[str] = []
    try:
        root = ET.fromstring(raw)
        for elem in root.iter():
            if elem.text and elem.text.strip():
                t = elem.text.strip()
                if len(t) > 1 and not t.startswith("#"):
                    texts.append(t)
    except Exception:
        texts = re.findall(r">([^<>]{2,200})<", raw)

    dedup_texts: List[str] = []
    for t in texts:
        if t not in dedup_texts:
            dedup_texts.append(t)

    joined = "\n".join(dedup_texts)
    ips = sorted(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b", joined)))
    ifaces = sorted(
        set(
            re.findall(
                r"\b(?:eth\d+|wlan\d+|lo|/dev/ttyUSB\d+|ttyUSB\d+|vlan\d+|tun\d+)\b",
                joined,
                flags=re.I,
            )
        )
    )
    return {
        "text": joined,
        "topology_markdown": (
            f"### Vector Diagram Intelligence (`{svg_path.name}`)\n"
            f"- **Extracted Diagram Labels:** {len(dedup_texts)} nodes/edges\n"
            + (f"- **Diagram IPs/Subnets:** `{', '.join(ips)}`\n" if ips else "")
            + (f"- **Diagram Interfaces:** `{', '.join(ifaces)}`\n" if ifaces else "")
        ),
        "ips": ips,
        "interfaces": ifaces,
    }


def extract_file_content(file_path: Path) -> Dict[str, Any]:
    """
    Phase 1 Multi-Modal Extractor:
    Extracts text, code blocks, and visual/diagram topology from `.md`, `.txt`, `.pdf`,
    `.docx`, `.html`, `.svg`, and raster images (`.png`, `.jpg`, `.webp`, `.bmp`, `.tiff`).
    """
    ext = file_path.suffix.lower()
    text_parts: List[str] = []
    topo_parts: List[str] = []
    ips: List[str] = []
    ifaces: List[str] = []
    doc_type = "text"

    if ext in SUPPORTED_IMAGE_EXTS:
        doc_type = "image_diagram"
        img_res = _extract_image_ocr_and_topology(str(file_path), source_label=file_path.name)
        if img_res["topology_markdown"]:
            topo_parts.append(img_res["topology_markdown"])
        if img_res["ocr_text"]:
            text_parts.append(img_res["ocr_text"])
        ips.extend(img_res["ips"])
        ifaces.extend(img_res["interfaces"])

    elif ext in SUPPORTED_VECTOR_EXTS:
        doc_type = "vector_diagram"
        vec_res = _extract_svg_topology(file_path)
        topo_parts.append(vec_res["topology_markdown"])
        text_parts.append(vec_res["text"])
        ips.extend(vec_res["ips"])
        ifaces.extend(vec_res["interfaces"])

    elif ext == ".pdf":
        doc_type = "pdf"
        extracted_pdf = False
        try:
            import pymupdf

            try:
                pymupdf.TOOLS.mupdf_display_errors(False)
                pymupdf.TOOLS.mupdf_display_warnings(False)
            except Exception:
                pass

            doc = pymupdf.open(str(file_path))
            ocr_pages_run = 0
            for page_idx, page in enumerate(doc):
                p_txt = page.get_text("text").strip()
                if p_txt:
                    text_parts.append(f"--- [Page {page_idx + 1}] ---\n{p_txt}")
                # Only run full-page Neural OCR on scanned/diagram pages with <160 chars of digital text (max 3 pages per PDF)
                img_list = page.get_images(full=True)
                if ocr_pages_run < 3 and len(p_txt) < 160 and (len(p_txt) < 80 or img_list):
                    try:
                        ocr_pages_run += 1
                        pix = page.get_pixmap(dpi=150)
                        png_bytes = pix.tobytes("png")
                        ocr_res = _extract_image_ocr_and_topology(
                            png_bytes, source_label=f"{file_path.name}#page{page_idx + 1}"
                        )
                        if ocr_res["ips"] or ocr_res["interfaces"] or len(p_txt) < 80:
                            topo_parts.append(ocr_res["topology_markdown"])
                            if len(p_txt) < 80 and ocr_res["ocr_text"]:
                                text_parts.append(ocr_res["ocr_text"])
                            ips.extend(ocr_res["ips"])
                            ifaces.extend(ocr_res["interfaces"])
                    except Exception:
                        pass
            extracted_pdf = True
        except Exception:
            pass

        if not extracted_pdf:
            try:
                from pypdf import PdfReader

                reader = PdfReader(str(file_path))
                for idx, page in enumerate(reader.pages):
                    t = (page.extract_text() or "").strip()
                    if t:
                        text_parts.append(f"--- [Page {idx + 1}] ---\n{t}")
                extracted_pdf = True
            except Exception:
                pass

        if not extracted_pdf and shutil.which("pdftotext"):
            try:
                proc = subprocess.run(
                    ["pdftotext", str(file_path), "-"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                if proc.stdout.strip():
                    text_parts.append(proc.stdout.strip())
            except Exception:
                pass

    elif ext == ".docx":
        doc_type = "docx"
        try:
            import docx

            d = docx.Document(str(file_path))
            for p in d.paragraphs:
                if p.text.strip():
                    text_parts.append(p.text.strip())
            for tbl in d.tables:
                for row in tbl.rows:
                    cells = [c.text.strip() for c in row.cells if c.text.strip()]
                    if cells:
                        text_parts.append(" | ".join(cells))
        except Exception as exc:
            text_parts.append(f"[DOCX read error: {exc}]")

    elif ext in SUPPORTED_HTML_EXTS:
        doc_type = "html"
        raw = file_path.read_text(encoding="utf-8", errors="replace")
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(raw, "html.parser")
            for code in soup.find_all(["pre", "code"]):
                c_txt = code.get_text().strip()
                if c_txt:
                    text_parts.append(f"```bash\n{c_txt}\n```")
            text_parts.append(soup.get_text(separator="\n"))
        except Exception:
            text_parts.append(re.sub(r"<[^>]+>", " ", raw))

    else:
        raw = file_path.read_text(encoding="utf-8", errors="replace")
        text_parts.append(raw)

    combined_text = "\n\n".join(text_parts).strip()
    all_ips = sorted(set(ips + re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b", combined_text)))
    all_ifaces = sorted(
        set(
            ifaces
            + re.findall(
                r"\b(?:eth\d+|wlan\d+|enp\d+s\d+|ens\d+|lo|/dev/ttyUSB\d+|ttyUSB\d+|ttyACM\d+|vlan\d+|tun\d+)\b",
                combined_text,
                flags=re.I,
            )
        )
    )
    return {
        "file_path": str(file_path),
        "file_name": file_path.name,
        "doc_type": doc_type,
        "text": combined_text,
        "topology_markdown": "\n\n".join(topo_parts).strip(),
        "ips": all_ips,
        "interfaces": all_ifaces,
    }


# ---------------------------------------------------------------------------
# PHASE 2 & 3: 3-Bucket Distillation + Engine 12 (CEGAR) Verification Gatekeeper
# ---------------------------------------------------------------------------
_KNOWN_CLI_PREFIXES = (
    # Linux / Unix / Network & Security CLI
    "curl ", "wget ", "tio ", "ip ", "ifconfig ", "iwconfig ", "iwlist ", "iw ", "nmcli ", "wpa_supplicant ",
    "macchanger ", "sudo ", "su -", "nmap ", "masscan ", "ss ", "netstat ", "ping ", "socat ", "ssh ",
    "ssh-keygen ", "ssh-copy-id ", "ssh-add ", "ssh-agent ", "scp ", "sftp ", "rsync ", "iptables ",
    "ip6tables ", "nft ", "ufw ", "firewall-cmd ", "tcpdump ", "tshark ", "wireshark ", "dumpcap ",
    "editcap ", "mergecap ", "capinfos ", "p0f ", "snort ", "zeek ", "suricata ", "arp ", "arping ",
    "ethtool ", "dladm ", "ndd ", "ipfstat ", "ipf ", "systemctl ", "journalctl ", "service ",
    "chkconfig ", "svcs ", "svcadm ", "inetadm ", "prtconf ", "prtdiag ", "psrinfo ", "modinfo ",
    "lsmod ", "modprobe ", "insmod ", "rmmod ", "sysdef ", "vmstat ", "iostat ", "dmesg ", "uname ",
    "uptime ", "lsof ", "fuser ", "pfiles ", "ptree ", "pwdx ", "pmap ", "strace ", "ltrace ", "truss ",
    "sestatus ", "getenforce ", "setenforce ", "ausearch ", "aureport ", "auditctl ", "logger ",
    "last ", "lastlog ", "who ", "w -", "id ", "groups ", "crontab ", "run-parts ", "runlevel ",
    "ps ", "pgrep ", "pkill ", "kill ", "killall ", "grep ", "egrep ", "fgrep ", "find ", "locate ",
    "which ", "whereis ", "type -", "file /", "stat /", "strings ", "objdump ", "readelf ", "ldd ",
    "gdb ", "r2 ", "radare2 ", "binwalk ", "exiftool ", "xxd ", "hexdump ", "base64 ", "ls ", "cat ",
    "head ", "tail ", "awk ", "sed ", "cut ", "sort -", "uniq ", "wc ", "xargs ", "tee ", "echo ",
    "printf ", "export ", "unset ", "history ", "script ", "chmod ", "chown ", "chgrp ", "cp -", "cp /",
    "mv ", "rm -", "rm /", "ln -", "mkdir ", "tar ", "gzip ", "gunzip ", "zip ", "unzip ", "dd ",
    "df ", "du -", "mount ", "umount ", "fdisk ", "lsblk ", "blkid ", "mkfifo ", "openssl ",
    "nc ", "netcat ", "ncat ", "dig ", "nslookup ", "host ", "whois ", "traceroute ", "tracepath ",
    "mtr ", "rpcinfo ", "showmount ", "smbclient ", "rpcclient ", "enum4linux ", "nmblookup ",
    "nbtscan ", "onesixtyone ", "snmpwalk ", "snmpget ", "ldapsearch ", "dns-sd ", "sqlmap ",
    "hydra ", "medusa ", "ncrack ", "crowbar ", "crowbar.py ",
    "john ", "unshadow ", "zip2john ", "rar2john ", "ssh2john ", "keepass2john ", "hashcat ",
    "mdxfind ", "mdxsplit ", "cewl ", "crunch ", "gobuster ", "feroxbuster ", "wfuzz ", "ffuf ",
    "dirb ", "dirsearch ", "nikto ", "wpscan ", "msfvenom ", "msfconsole ", "msfdb ", "searchsploit ",
    "responder ", "impacket-", "getnpusers.py ", "getuserspns.py ", "secretsdump.py ", "psexec.py ",
    "smbexec.py ", "wmiexec.py ", "atexec.py ", "dcomexec.py ", "ntlmrelayx.py ", "ticketer.py ",
    "getst.py ", "gettgt.py ", "lookupsid.py ", "samrdump.py ", "rpcdump.py ", "smbclient.py ",
    "mssqlclient.py ", "crackmapexec ", "netexec ", "nxc ", "certipy ", "rubeus ", "sharphound ",
    "bifrost ", "bitfrost ", "nimbostratus ",
    "mimikatz ", "privilege::", "sekurlsa::", "lsadump::", "kerberos::", "crypto::", "token::",
    "vault::", "dpapi::", "sid::", "iis::", "misc::", "process::", "service::", "ts::", "event::",
    "airmon-ng ", "airodump-ng ", "aireplay-ng ", "aircrack-ng ", "airdecap-ng ", "packetforge-ng ",
    "wash ", "reaver ", "hcxdumptool ", "hcxpcaptool ", "kismet ", "bettercap ", "ettercap ",
    "hciconfig ", "hcitool ", "l2ping ", "chisel ", "proxychains ", "proxychains4 ", "sshuttle ",
    "ligolo ", "plink ", "sshpass ", "xfreerdp ",
    # Cloud, Containers, DevOps, Forensics, Mobile, SIEM & Databases
    "aws ", "az ", "gcloud ", "gsutil ", "bq ", "docker ", "docker-compose ", "kubectl ", "kubeadm ",
    "minikube ", "helm ", "ansible ", "ansible-playbook ", "ansible-galaxy ", "ansible-vault ",
    "puppet ", "terraform ", "git ", "gh ", "jq ", "tmux ", "screen ", "vim ", "vi ", "adb ", "fastboot ",
    "frida ", "frida-ps ", "frida-trace ", "frida-ls-devices ", "objection ", "volatility ",
    "vol.py ", "osqueryi ", "osqueryd ", "yara ", "yarac ", "splunk ", "shodan ", "greynoise ",
    "utmpdump ", "gcc ", "go get ", "go build ", "go run ",
    "mysql ", "mysqldump ", "psql ", "sqlite3 ", "mongo ", "redis-cli ", "sqlcmd ",
    "apt ", "apt-get ", "apt-cache ", "dpkg ", "yum ", "dnf ", "rpm ", "pacman ", "zypper ",
    "brew ", "pip ", "pip3 ", "npm ", "gem ",
    # macOS Administration & Security CLI
    "launchctl ", "defaults ", "dscl ", "dscacheutil ", "dsconfigad ", "otool ", "scutil ",
    "systemsetup ", "networksetup ", "security ", "codesign ", "spctl ", "pkgutil ", "hdiutil ",
    "osascript ", "plutil ", "dtrace ", "csrutil ", "nvram ", "diskutil ", "softwareupdate ", "xcode-select ",
    "python3 ", "python ", "perl ", "php -r ", "ruby -r", "bash ", "sh -", "zsh ", "stty ", "./",
    "network_isolation/",
    # Windows CMD, Active Directory, Registry, Firewall, LOLBins & Triage CLI
    "wmic ", "icacls ", "cacls ", "takeown ", "bcdedit ", "sfc ", "attrib ", "auditpol ",
    "wevtutil ", "wevutil ", "reg query", "reg add", "reg delete", "reg save", "reg export", "reg import",
    "reg copy", "reg restore", "reg unload", "reg load", "reg compare", "reg flags", "regedit ",
    "net user", "net users", "net localgroup", "net group", "net share", "net use", "net view",
    "net start", "net stop", "net session", "net statistics", "net accounts", "net config",
    "net time", "net file", "net computer", "net continue", "net pause", "net help", "net1 ",
    "netsh ", "ipconfig ", "nbtstat ", "route print", "route add", "route delete", "route change",
    "route -", "tracert ", "pathping ", "telnet ", "tasklist ", "taskkill ", "systeminfo ",
    "sc query", "sc qc", "sc config", "sc start", "sc stop", "sc create", "sc delete",
    "sc description", "sc sdshow", "sc sdset", "sc enumdepend", "sc failure", "sc triggerinfo",
    "sc \\\\", "schtasks ", "at ", "runas ", "whoami ", "hostname ", "ver ", "date /t", "time /t",
    "time/t", "prompt ", "setx ", "gpresult ", "gpupdate ", "nltest ", "dsquery ", "dsget ",
    "dsmod ", "dsadd ", "dsrm ", "csvde ", "ldifde ", "dnscmd ", "ntdsutil ", "certutil ",
    "certreq ", "bitsadmin ", "vssadmin ", "wbadmin ", "dism ", "pktmon ", "fport ", "driverquery ",
    "fltmc ", "fsutil ", "openfiles ", "qwinsta ", "rwinsta ", "quser ", "klist ", "vaultcmd ",
    "cmdkey ", "forfiles ", "findstr ", "dir ", "copy ", "xcopy ", "robocopy ", "del ", "erase ",
    "ren ", "rename ", "md ", "rd ", "rmdir ", "type ", "cmd /c", "cmd /k", "pushd ", "popd ",
    "start \\\\", "rpcping ", "rundll32 ", "regsvr32 ", "mshta ", "msiexec ", "makecab ", "expand ",
    "esentutl ", "cmstp ", "odbcconf ", "pcalua ", "regasm ", "regsvcs ", "wscript ", "cscript ",
    "csc ", "jsc ", "for /f ", "for /l ", "for /r ", "for /d ",
    # Sysinternals Utilities
    "pslist ", "psloggedon ", "psloglist ", "psservice ", "psexec ", "pskill ", "psinfo ",
    "psfile ", "psgetsid ", "pspasswd ", "psping ", "autorunsc ", "autoruns ", "sigcheck ",
    "sigcheck\\", "handle ", "listdlls ", "tcpvcon ", "accesschk ", "accessenum ", "procdump ",
    "procmon ", "sysmon ", "sdelete ", "logonsessions ", "pipelist ", "portmon ", "movefile ",
    "movelatr ", "movelatr.exe ", "pechksum ", "pechksum.exe ",
    # PowerShell Cmdlets & Aliases
    "powershell ", "pwsh ", "import-module ", "invoke-", "get-", "set-", "new-", "remove-",
    "write-", "install-", "uninstall-", "restore-", "find-", "select-", "where-", "sort-",
    "format-", "out-", "export-", "import-", "start-", "stop-", "restart-", "enable-",
    "disable-", "test-", "enter-", "exit-", "register-", "unregister-", "update-", "clear-",
    "copy-", "move-", "rename-", "measure-", "compare-", "group-", "tee-", "resolve-",
    "resume-", "suspend-", "wait-",
    "gcm ", "gci ", "gwmi ", "gcim ", "iex ", "iwr ", "irm ", "$psversiontable",
    # Cisco IOS / Network Appliance CLI
    "ip flow-", "interface gigabitethernet", "interface fastethernet", "interface serial",
    "interface vlan", "interface loopback", "interface tunnel", "show ip ", "show interfaces",
    "show running-config", "show arp", "show mac ", "show vlan",
)

_KNOWN_CLI_PREFIXES_LOWER = tuple(p.lower() for p in _KNOWN_CLI_PREFIXES)

_STANDALONE_CLI_COMMANDS = {
    "systeminfo", "tasklist", "ipconfig", "listdlls", "psloggedon", "fport", "ver",
    "whoami", "hostname", "uname", "uptime", "vmstat", "lsmod", "lsof", "dmesg",
    "sestatus", "getenforce", "aureport", "history", "w", "last", "who", "id",
    "groups", "mount", "run-parts", "runlevel", "inetadm", "svcs", "prtconf",
    "prtdiag", "psrinfo", "sysdef", "hostid", "date", "$psversiontable", "klist",
    "driverquery", "fltmc", "qwinsta", "quser", "privilege::debug", "sekurlsa::logonpasswords",
    "lsadump::sam", "lsadump::secrets", "lsadump::cache", "token::elevate", "token::revert",
    "vault::cred", "vault::list", "crypto::capi", "crypto::cng",
}


def _clean_and_split_candidate_line(raw_ln: str) -> List[str]:
    """
    Normalizes whitespace/quotes, strips trailing inline cheat-sheet comments
    (e.g. `<--- comment`, `-> comment`, and tab- or multi-space-indented `:Description` suffixes),
    strips shell/router/PowerShell prompts and Unicode bullet markers, repairs PDF broken
    en-dash flags, rejects Table-of-Contents leader lines, and splits uppercase `OR` alternatives.
    """
    if not raw_ln:
        return []
    ln = (
        raw_ln.replace("\xa0", " ")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace(" \u2013", " -")
        .replace(" \u2014", " -")
        .strip()
    )
    # Repair PDF broken en-dash flag character `\ufffd` when preceded by space and followed by flag letters
    ln = re.sub(r"(?<=\s)\ufffd(?=[a-zA-Z0-9])", "-", ln)

    if not ln or ln.startswith((";", "//", "===", "---", "***", "http://", "https://")):
        return []
    if re.match(r"^(?:URL|LOOKUP\s+IP|Output|Process|NOTES?)\s*:", ln, flags=re.I):
        return []
    # Reject Table-of-Contents dotted/dashed leader lines (e.g. `NMAP --------- 223` or `Section ..... 42`)
    if re.search(r"[-._]{4,}\s*\d+\s*$", ln):
        return []

    # 1. Strip trailing arrow comments (`<---...`, `<--...`, `<-...`, and `   -> ...`)
    ln = re.sub(r"(?<!<)\s*<+-+.*$", "", ln).strip()
    ln = re.sub(r"(?:\t+\s*|\s{2,})-+>\s+.*$", "", ln).strip()

    # 2. Strip tab-indented or multi-space-indented `:Description` cheat-sheet suffixes
    ln = re.sub(r"(?:\t+\s*|\s{2,}):\s*.*$", "", ln).strip()

    # 3. Strip inline `# comment` when preceded by 2+ spaces or tabs
    ln = re.sub(r"(?:\t+\s*|\s{2,})#\s+.*$", "", ln).strip()

    # 4. Strip trailing OS notes in parentheses like `(Linux only)` or `(SOLARIS)`
    ln = re.sub(r"\s+\((?:Linux|Solaris|Windows|XP|Vista|Win7|newer Linux)[^)]*\)\s*$", "", ln, flags=re.I).strip()

    # 5. Strip hanging trailing `&` from wrapped Windows batch lines (not `&&`)
    if ln.endswith("&") and not ln.endswith("&&") and ("\\" in ln or "%" in ln):
        ln = ln[:-1].rstrip()

    if not ln:
        return []

    # 6. Split `cmd1   OR   cmd2` alternatives on the same line
    parts = re.split(r"\s+OR\s+", ln)
    cleaned_parts: List[str] = []
    for part in parts:
        p = part.strip()
        if not p:
            continue
        # Strip leading step/command labels and ASCII/Unicode bullet markers (`*`, `•`, `●`, `▪`, `▸`, `►`)
        p = re.sub(r"^(?:CMD\d*|Command\s*\d*|Step\s*\d*|Run)\s*:\s*", "", p, flags=re.I).strip()
        p = re.sub(r"^[\*\u2022\u25cf\u25aa\u25b8\u25ba\ufffd]+\s+", "", p).strip()
        # Strip trailing colon or `: Description` from Active Directory `DSQUERY/DSGET/DSADD/DSMOD <OBJECT>:` cheat-sheet entries
        p = re.sub(
            r"^((?:dsquery|dsget|dsadd|dsmod|dsmove|dsrm)\s+(?:computer|contact|subnet|group|ou|site|server|user|quota|partition|\*))\s*:\s*.*$",
            r"\1",
            p,
            flags=re.I,
        ).strip()
        # Strip Windows, PowerShell, Linux, Beacon, and Cisco IOS prompts
        p = re.sub(
            r"^(?:PS\s+[A-Za-z]:\\[^>]*>|[A-Za-z]:\\[^>]*>|beacon>|"
            r"(?:root|www-data|[a-zA-Z0-9_.\-]+)@[^\s#$]+[#\$]\s*|"
            r"(?:Router|Switch)(?:\([^\)]+\))?[#>]\s*)",
            "",
            p,
            flags=re.I,
        ).strip()
        if p.startswith("$ "):
            p = p[2:].strip()
        elif p.startswith("# "):
            # In Linux PDFs (e.g., `# netstat -a | more`), `# ` is often the root shell prompt
            after_hash = p[2:].strip()
            if _is_known_cli_command(after_hash):
                p = after_hash
        if p:
            cleaned_parts.append(p)
    return cleaned_parts


def _is_known_cli_command(cmd: str) -> bool:
    """
    Case-insensitively checks whether `cmd` is a known CLI command (Linux, Solaris, Windows CMD,
    Sysinternals, Active Directory, PowerShell, Cloud, or network appliance) while rejecting
    English prose sentences, Table-of-Contents lines, and truncated multi-line fragments.
    """
    s = (cmd or "").strip()
    if not s or len(s) > 360:
        return False
    # Reject Table-of-Contents leader lines, lines ending with a colon or hanging flag dash, or unbalanced quotes/parens/placeholders
    if s.endswith((":", " -", " --")) or re.search(r"[-._]{4,}\s*\d+\s*$", s) or re.search(r"<[a-zA-Z0-9_\-]*$", s):
        return False
    if s.count('"') % 2 != 0 or s.count("'") % 2 != 0 or s.count("(") != s.count(")"):
        return False

    low = s.lower()
    # Normalize `.exe` on the leading binary token (`rundll32.exe ...` -> `rundll32 ...`, `at.exe` -> `at`)
    low_norm = re.sub(r"^([a-z0-9_\-]+)\.exe(?=\s|$)", r"\1", low)

    # Reject truncated `reg add` / `reg query` lines ending with a bare value/type switch (`/v`, `/t`, `/d`) or `Regedit Last Key`
    if re.search(r"^reg\s+(?:add|query|delete)\b.*\s+/[vtd]\s*$", low_norm):
        return False
    if low_norm.startswith("regedit") and not re.search(r"^regedit(?:\s+(?:/[se]\b|[^\s]+\.reg\b|[a-zA-Z]:\\))?$", low_norm):
        return False

    # Reject ALL-CAPS multi-word PDF section headers (`ADB BASICS`, `DOCKER CONTAINERS`, `SSH SESSIONS`)
    # unless they contain CLI flags/paths/digits or are known 2-word Windows/Linux/AD status commands
    if (
        s.isupper()
        and " " in s
        and not re.search(r"[-/\\.$%~|><=\"'`:\[\]0-9*]", s)
        and not re.match(
            r"^(?:net\s+(?:view|start|share|session|use|users?|accounts|config|statistics|localgroup|group|time)|"
            r"(?:dsquery|dsget|dsadd|dsmod)\s+(?:computer|contact|subnet|group|ou|site|server|user|quota|partition)|"
            r"sc\s+query|wevtutil\s+el|ip\s+(?:addr|route|link|neigh))\b",
            low_norm,
        )
    ):
        return False

    if low in _STANDALONE_CLI_COMMANDS or low_norm in _STANDALONE_CLI_COMMANDS:
        # Reject capitalized English headings (`Mount`, `Date`, `History`, `Who`, `Groups`) for single-word Unix commands
        if not s.islower() and low_norm not in ("systeminfo", "tasklist", "ipconfig", "ver", "driverquery", "fltmc", "klist", "$psversiontable"):
            return False
        return True

    # PowerShell variable assignment to a cmdlet (`$c = Get-Credential`, `$FindDate=Get-Date ...`)
    # or parenthesized PowerShell expression (`(Get-WmiObject ...).Uninstall()`, `(gcm Get-Command).definition`)
    if re.match(r"^\$[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*(?:get-|set-|new-|invoke-|select-|where-|\(?\s*netsh\b)", low):
        return True
    if re.match(r"^\(\s*(?:get-|gcm\s|gwmi\s|gci\s)", low):
        return True

    # Check if command starts with any known CLI prefix (case-insensitive, with or without `.exe`)
    if not (
        any(low.startswith(p) for p in _KNOWN_CLI_PREFIXES_LOWER)
        or any(low_norm.startswith(p) for p in _KNOWN_CLI_PREFIXES_LOWER)
    ):
        return False

    # Guard against English prose sentences & table descriptions in PDFs starting with command words
    raw_first = s.split()[0].rstrip(":")
    first_word = low_norm.split()[0].rstrip(":")

    # Reject `Tool - Description` cheat-sheet lines (where ` - ` has spaces on both sides, not a `-flag`)
    if re.match(r"^[a-zA-Z0-9_.\-]+\s+-\s+[a-zA-Z]{2,}\b", s):
        return False

    # Reject unquoted natural-language prose clauses mixed with command prefixes
    unquoted_s = re.sub(r'"[^"]*"|\'[^\']*\'', "", low_norm)
    if re.search(
        r"\b(?:within\s+the\s+organization|at\s+which\s+it\s+is|is\s+developed|we\s+are\s+running\s+as|"
        r"module\s+which\s+extracts|to\s+extract\s+the\s+hash|script\s+from\s+the\s+control\s+server|"
        r"imported\s+from\s+above|connection\s+request\s+was|a\s+tool\s+to\s+parse)\b",
        unquoted_s,
    ):
        return False

    # Unix/Cloud/Container/Security tools whose binary token in real CLI invocations is lowercase
    # (filters out PDF table descriptions like `Docker push a tagged`, `SSH connect to host`, `Mount Windows C share`)
    _LOWERCASE_BINARY_TOOLS = {
        "adb", "fastboot", "ansible", "ansible-playbook", "ansible-galaxy", "ansible-vault",
        "aws", "az", "gcloud", "gsutil", "bq", "docker", "docker-compose", "kubectl", "kubeadm",
        "helm", "terraform", "git", "gh", "frida", "frida-ps", "frida-trace", "objection",
        "volatility", "vol.py", "yara", "yarac", "osqueryi", "osqueryd", "splunk", "shodan",
        "greynoise", "hashcat", "john", "hydra", "medusa", "ncrack", "crowbar", "sqlmap",
        "msfvenom", "msfconsole", "searchsploit", "tcpdump", "tshark", "wireshark", "ssh",
        "scp", "sftp", "ssh-keygen", "ssh-copy-id", "smbclient", "rpcclient", "enum4linux",
        "gobuster", "ffuf", "feroxbuster", "wfuzz", "wpscan", "nikto", "curl", "wget",
        "openssl", "socat", "nc", "ncat", "netcat", "chisel", "proxychains", "proxychains4",
        "tmux", "screen", "vim", "nano", "tar", "gzip", "gunzip", "zip", "unzip", "chmod",
        "chown", "chgrp", "mkdir", "rm", "cp", "mv", "ln", "mount", "umount", "export",
        "alias", "source", "kill", "killall", "pkill", "ps", "top", "htop", "lsof", "lsmod",
        "modprobe", "insmod", "rmmod", "sysctl", "systemctl", "journalctl", "service",
        "chkconfig", "apt", "apt-get", "yum", "dnf", "rpm", "dpkg", "pip", "pip3",
        "security", "defaults", "launchctl", "diskutil", "hdiutil", "scutil",
        "cut", "script", "who", "groups", "id", "w", "last", "history", "uname", "uptime",
        "vmstat", "dmesg", "which", "whereis", "host", "dig", "nslookup", "whois", "arping",
        "ping", "traceroute", "nmap", "masscan",
    }
    if s.startswith("./"):
        non_exec_exts = (
            ".txt", ".log", ".md", ".json", ".xml", ".csv", ".yml", ".yaml", ".ini", ".cfg",
            ".conf", ".pdf", ".docx", ".html", ".htm", ".db", ".sqlite", ".sqlite3", ".mdb", ".bak",
        )
        first_path = s.split()[0].lower()
        if first_path.endswith(non_exec_exts):
            return False

    if first_word in _LOWERCASE_BINARY_TOOLS and not raw_first.islower():
        return False

    if first_word == "ip":
        # Must be `ip` followed by a valid iproute2 or Cisco IOS subcommand/flag (never `IP Header`, `IP Statistics`, `IP Source Address`, `IP address for which...`)
        if not re.match(
            r"^ip\s+(?:-[46brsdojc]+|addr(?:ess)?(?:\s+(?:show|add|del|flush|change|replace))?\s*$|addr(?:ess)?\s+(?:show|add|del|flush|change|replace)\b|route\b|link\b|neigh\b|rule\b|netns\b|tunnel\b|tuntap\b|maddr\b|monitor\b|flow-|cef\b|nat\b|access-list\b|dhcp\b|helper-address\b)",
            low_norm,
        ):
            return False

    if first_word == "arp":
        # Must be `arp` with `-`/`/` flags (e.g. `arp -a`, `arp -an`), never `ARP Packet`, `ARP Request`, `ARP Table`
        if not re.match(r"^arp(?:\s+[-/][a-z0-9]+|\s+\d+\.\d+\.\d+\.\d+)\b", low_norm):
            return False

    if first_word == "service":
        # Must be `service --status-all` or `service <svc_name> <action>` (never `service for...`, `service that...`, `Service Cluster...`)
        if not re.match(
            r"^service\s+(?:--status-all|[a-z0-9_.\-]+\s+(?:start|stop|restart|reload|status|condrestart|try-restart|force-reload))\b",
            low_norm,
        ):
            return False

    if first_word == "security":
        # macOS `security` CLI tool subcommands (never `Security Group Configurations`)
        if not re.match(
            r"^security\s+(?:find-|dump-|unlock-|show-|list-|delete-|create-|import|export|authorize|leaks)\b",
            low_norm,
        ):
            return False

    if first_word == "screen":
        # GNU `screen` requires a `-` flag (`screen -S`, `screen -r`, `screen -ls`, `screen -x`)
        if not re.match(r"^screen\s+-[a-zA-Z0-9]", s):
            return False

    if first_word == "export":
        # Shell `export` requires `=` or `-p`/`-f`/`-n` flag
        if not re.search(r"^export\s+(?:-[pfn]\b|[a-zA-Z_][a-zA-Z0-9_]*=)", s):
            return False

    if first_word in ("mount", "umount"):
        if not re.search(r"[-/\\:$]", s):
            return False

    if first_word == "kill":
        if not re.match(r"^kill\s+(?:-[a-zA-Z0-9]+|%\d+|\d+|\$[a-zA-Z0-9_{}]+)\b", s):
            return False

    if first_word == "cut":
        if not re.search(r"\s-(?:[dfcb]|-)", s):
            return False

    if first_word == "mimikatz":
        if re.match(r"^mimikatz\s+(?:execution|is|can|to|from|module|command|tool)\b", low_norm):
            return False

    if first_word.startswith(("sekurlsa::", "lsadump::", "privilege::", "token::", "vault::", "crypto::")):
        if re.search(r"\b(?:module|which|extracts?|from\s+the|to\s+extract|is\s+used)\b", low_norm):
            return False

    if first_word == "wmic":
        # Must have a WMIC verb/switch or >= 3 tokens (never 2-word heading `WMIC Process`)
        if len(s.split()) < 3 and not re.search(r"^(?:wmic\s+(?:qfe|bios|os|cpu|logicaldisk|nic|product|startup|share|useraccount))\s*$", low_norm):
            return False

    if first_word in ("gcloud", "kubectl", "docker", "aws", "az", "john"):
        if re.match(
            r"^(?:gcloud\s+(?:cli|doc)\b|kubectl\s+commands\b|docker\s+(?:files|for|secrets)\b|aws\s+best\b|john\s+the\s+ripper\b)",
            low_norm,
        ):
            return False

    if first_word in ("powershell", "pwsh"):
        # Must be followed by `-flag`, `/flag`, `$var`, `(`, `.`, or `.ps1` (never `PowerShell Azure Modules Installed`)
        if not re.search(r"^p(?:owershell|wsh)(?:\.exe)?\s+(?:[-/$@.(]|[^\s]+\.ps1\b)", low):
            return False

    if first_word in ("python", "python3", "perl", "bash", "sh", "cmd"):
        # Must be followed by `-c`/`-m`/`/c`/`/k` flag, script file, redirection, or variable
        if not re.search(r"^(?:python3?|perl|bash|sh|cmd)(?:\.exe)?\s+(?:[-/$<(\"]|[^\s]+\.(?:py|pl|sh|bat|cmd)\b)", low):
            return False

    if first_word == "at":
        # Must be `at` with `\\computer`, time `HH:MM`, `/delete`, `/yes`, or `-f` (never English `at the...`)
        if not re.search(r"^at(?:\.exe)?\s+(?:\\\\|\d{1,2}:\d{2}|/[a-z]+|-[a-z]+)", low):
            return False

    if first_word == "expand":
        if not re.search(r"^expand(?:\.exe)?\s+(?:[-/\\]|[a-zA-Z]:\\|[^\s]+\.cab\b)", low):
            return False

    if first_word in ("netstat", "nbtstat", "ss", "ifconfig", "ipconfig", "tcpdump", "tshark", "nmap", "masscan"):
        rest = low_norm[len(first_word) :].strip()
        if rest and not re.match(r"^(?:[-/|><]|&&|;|\d+|eth\d+|wlan\d+|enp\d+|ens\d+|lo\b|any\b|\d+\.\d+\.\d+\.\d+)", rest, flags=re.I):
            return False

    if first_word == "ps":
        if not re.match(r"^ps\s+(?:-[a-zA-Z0-9]+|aux\b|awx\b|ef\b)", s):
            return False

    if first_word in ("which", "whereis"):
        if not re.match(r"^(?:which|whereis)\s+(?:-[a-z]+\s+)?[a-zA-Z0-9_.\-/]{1,40}$", s):
            return False

    if first_word == ".":
        # Reject PDF bibliography citations like `. update-the-cyber-kill-chain... [Accessed: ...]`
        if "[accessed:" in low_norm or not re.match(r"^\.\s+(?:\./|/|[a-zA-Z0-9_\-]+\.sh\b)", s):
            return False

    if first_word == "echo":
        if (
            re.match(r"^echo\s+(?:request|requests|reply|replies|or\s+echo|command\b|\d+$)", low_norm)
            or ("|" not in s and ">" not in s and "/proc/" not in low_norm and "/sys/" not in low_norm)
        ):
            return False

    if first_word == "script":
        if re.match(r"^script\s+(?:to|for|that|which|is|in|imported|from|using|with|the|a|an)\b", low_norm) or s.endswith(":") or len(s.split()) > 5:
            return False

    if first_word == "host":
        if not re.match(r"^host\s+(?:-[a-zA-Z0-9]+\s+)*(?:[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_.\-]+|\d+\.\d+\.\d+\.\d+)$", s):
            return False

    if first_word in ("cat", "ls", "head", "tail", "stat", "file"):
        if not re.search(r"[-/\\.$~*|`><]", s):
            return False

    if first_word == "copy":
        # Real `copy` commands have flags (`/y`, `/b`), drive/UNC paths (`\`, `:`), wildcards (`*`), or file extensions (`.ext`)
        if not re.search(r"(?:\\[a-zA-Z0-9_.\-*]+|[a-zA-Z]:\\|/[yba]\b|\.[a-zA-Z0-9]{1,5}\b|%[a-zA-Z0-9_]+%)", s):
            return False
        if re.match(r"^copy\s+(?:the|of|a|an|from|to|file|files|dir|directory|all)\b", low_norm):
            return False

    if first_word in ("find", "where", "type", "del", "dir", "ren", "rename", "md", "rd", "date", "time", "handle", "strings"):
        # Real commands with these verbs contain flags (`-`, `/`), paths (`\`, `/`, `.`, `~`),
        # env vars (`%`, `$`), quotes (`"`, `'`), pipes (`|`, `>`), or known process/target tokens
        if not re.search(r"[-/\\.$%~|><=\"'`:\[\]]|\b(?:notepad|cmd|conhost|lsass|explorer|boot\.ini)\b", s, flags=re.I):
            return False
        # Reject natural-language phrases like `Find files with...`, `Where the...`, `Type of...`, `Date and time...`
        if re.match(
            r"^(?:find\s+(?:the|all|a|an|out|files|user|users|sudo|non-supportive)\b|"
            r"where\s+(?:the|a|an|is|are|to|possible)\b|"
            r"type\s+(?:the|of|a|an|in|is|to|for|from|that|which)\b|"
            r"date\s+(?:and|of|to|range|stamps?)\b|"
            r"time\s+(?:to|of|review|stamps?|between|range)\b|"
            r"handle\s+(?:the|a|an|all|errors?|requests?|packets?)\b)",
            low_norm,
        ):
            return False

    if first_word == "groups":
        if len(s.split()) > 3 or re.match(r"^groups\s+(?:definitions?|and|of|in|for|to|are|is|that|with|within|the|from|can)\b", low_norm):
            return False

    if first_word in ("who", "last", "w", "id", "history", "uname", "uptime", "vmstat", "lsmod", "lsof", "dmesg"):
        # Must be followed by a flag (`-`), pipe (`|`), redirection (`>`), or a single identifier/path
        rest = low_norm[len(first_word) :].strip()
        if rest and not re.match(r"^(?:[-/|>;]|&&|[a-zA-Z0-9_.\-/]{1,24}$)", rest):
            return False

    return True


def _normalize_placeholder_for_cegar(cmd: str) -> str:
    """Replace template placeholders like `<target_ip>` or `<ip>` with an RFC 5737 test IP solely for CEGAR syntax validation."""
    s = re.sub(r"<(?:target_?ip|ip|host|gateway)>", "198.51.100.10", cmd, flags=re.I)
    s = re.sub(r"<(?:iface|interface)>", "eth0", s, flags=re.I)
    s = re.sub(r"<(?:port)>", "8080", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "placeholder_val", s)
    return s


def _join_wrapped_cli_lines(raw_lines: List[str]) -> List[str]:
    """
    Reconstructs multi-line CLI commands that wrapped across 2-3 PDF lines due to column width
    (e.g., lines ending with `\\`, ` -`, ` --`, `|`, `&&`, unclosed quotes `"`/`'`, or unclosed `<placeholder`).
    """
    joined: List[str] = []
    i = 0
    n = len(raw_lines)
    while i < n:
        cur = raw_lines[i].strip()
        if not cur:
            i += 1
            continue
        low = cur.lower()
        starts_cmd = any(low.startswith(p) for p in _KNOWN_CLI_PREFIXES_LOWER)
        if starts_cmd:
            merges = 0
            while merges < 2 and (i + 1) < n:
                nxt = raw_lines[i + 1].strip()
                if not nxt or nxt.startswith(("---", "#", "http://", "https://")) or re.search(r"[-._]{4,}\s*\d+\s*$", nxt):
                    break
                needs_cont = (
                    cur.endswith(("\\", " -", " --", "|", "&&"))
                    or (cur.count('"') % 2 != 0)
                    or (cur.count("'") % 2 != 0)
                    or bool(re.search(r"<[a-zA-Z0-9_\-]*$", cur))
                )
                next_is_flag = bool(
                    re.match(
                        r"^(?:--?[a-zA-Z][a-zA-Z0-9\-]*\b|[a-zA-Z0-9_.\-]+/[a-zA-Z0-9_.\-]+:[^\s]+@\d+\.\d+\.\d+\.\d+)",
                        nxt,
                    )
                )
                if not (needs_cont or next_is_flag):
                    break
                if cur.endswith("\\"):
                    cur = cur[:-1].rstrip() + " " + nxt
                elif cur.endswith((" -", " --")) and not nxt.startswith("-"):
                    # Wrapped inside a flag name (e.g., `--` + `protocol tcp` -> `--protocol tcp`)
                    cur = cur + nxt
                elif re.search(r"<[a-zA-Z0-9_\-]*-$", cur):
                    # Wrapped inside a `<placeholder-` token
                    cur = cur + nxt
                else:
                    cur = cur + " " + nxt
                i += 1
                merges += 1
        joined.append(cur)
        i += 1
    return joined


def _extract_and_verify_commands_deterministic(text: str) -> Tuple[List[Dict[str, Any]], int]:
    """
    Deterministically extracts shell, Windows CMD, Sysinternals, Active Directory, PowerShell,
    Cloud, and network appliance commands from fenced code blocks and document lines, reconstructs
    wrapped PDF lines, strips trailing cheat-sheet comments, and validates each one through Engine 12
    (`verify_command_cegar`). Returns `(verified_commands, quarantined_count)` with no artificial cap.
    """
    candidates: List[str] = []

    # 1. Extract from fenced code blocks ```bash / ```sh / ```powershell / ```cmd / ```
    for m_block in re.finditer(
        r"```(?:bash|sh|zsh|shell|console|cmd|batch|dos|powershell|ps1|text|)\n(.*?)```",
        text,
        flags=re.S | re.I,
    ):
        block = m_block.group(1)
        for raw_ln in _join_wrapped_cli_lines(block.splitlines()):
            for cand in _clean_and_split_candidate_line(raw_ln):
                if _is_known_cli_command(cand):
                    candidates.append(cand)

    # 2. Extract inline commands (including Windows/Linux/PowerShell cheat sheets & router transcripts)
    for raw_ln in _join_wrapped_cli_lines(text.splitlines()):
        for cand in _clean_and_split_candidate_line(raw_ln):
            if _is_known_cli_command(cand):
                candidates.append(cand)

    verified: List[Dict[str, Any]] = []
    seen = set()
    quarantined = 0

    prose_re = re.compile(
        r"(?:^[a-z0-9_.\-/]+\s+(?:is|are|was|were|can|will|should|allows|provides|uses|works|supports|helps|means|has|have|"
        r"displays|shows|lists|prints|returns|checks|enables|disables|configures|creates|deletes|modifies|requires|contains|"
        r"represents|indicates|specifies|determines|describes|defines|monitors|captures|filters|searches)\b|"
        r"\b(?:option\s+can\s+be|can\s+be\s+combined|can\s+be\s+used|is\s+used\s+to|will\s+display|will\s+add)\b)",
        re.I,
    )
    for cmd in candidates:
        cmd_clean = cmd.strip()
        if not cmd_clean or cmd_clean in seen or len(cmd_clean) < 3:
            continue
        # Strip quoted strings before testing `prose_re` so commands like `echo "@file is a batch file"` are not rejected
        cmd_unquoted = re.sub(r"\"[^\"]*\"|'[^']*'", '""', cmd_clean)
        if prose_re.search(cmd_unquoted):
            continue
        seen.add(cmd_clean)

        # Auto-heal unbounded `ping <ip>` in training docs by adding `-c 3` before CEGAR check
        if re.match(r"^ping\s+(?![-/][cwn]\b)", cmd_clean, flags=re.I):
            cmd_clean = re.sub(r"^ping\s+", "ping -c 3 ", cmd_clean, count=1, flags=re.I)

        test_cmd = _normalize_placeholder_for_cegar(cmd_clean)
        cegar_res = verify_command_cegar(test_cmd)
        if cegar_res.get("blocked"):
            quarantined += 1
            continue

        layer = _classify_command_layer(cmd_clean)
        verified.append(
            {
                "command": cmd_clean,
                "layer": layer,
                "cegar_verified": True,
            }
        )

    # Return 100% of verified commands with no artificial ceiling
    return verified, quarantined


def _classify_command_layer(cmd: str) -> str:
    low = cmd.strip().lower()
    if re.search(r"\b(?:tio|ttyusb\d*|ttyacm\d*|stty|minicom)\b", low):
        return "L1_Serial_OOB"
    if re.search(r"^(?:arp|arping|ethtool|dladm|airmon-ng|airodump-ng|aireplay-ng|aircrack-ng|iwconfig|iwlist)\b|\bip\s+(?:neigh|link)\b|\b(?:bridge|vlan)\b", low):
        return "L2_ARP_Link"
    if re.search(
        r"^(?:ip\s+(?:-[46brsdojc]+\s+)*(?:route|addr|address|rule|netns|flow-)|ifconfig|ipconfig|route|iptables|ip6tables|"
        r"nft|ufw|firewall-cmd|netsh|ipfstat|ipf|ping|traceroute|tracepath|tracert|pathping|mtr)\b",
        low,
    ):
        return "L3_Routing_NAT"
    if re.search(
        r"^(?:nmap|masscan|ss|netstat|nbtstat|fport|tcpvcon|socat|nc|netcat|ncat|tcpdump|tshark|wireshark|p0f|snort|zeek|suricata|rpcinfo|rpcping|telnet|ssh|scp|sftp|chisel|proxychains)\b",
        low,
    ):
        return "L4_Port_Service"
    if re.search(
        r"^(?:curl|wget|openssl|invoke-webrequest|iwr|irm|sqlmap|nikto|gobuster|ffuf|dirb|feroxbuster|wfuzz|wpscan|aws|az|gcloud|gsutil|kubectl|docker|helm)\b|https?://",
        low,
    ):
        return "L7_HTTP_Web"
    return "General_System"


def _extract_workflows_and_rules_deterministic(text: str, source_name: str) -> Dict[str, Any]:
    """Extracts PDF Table-of-Contents/chapter headings, Markdown headings, numbered steps, error->fix pairs, and capability tags."""
    headings: List[str] = []

    # 1. Extract PDF Table-of-Contents chapter/section titles (`CHAPTER NAME -------- 42`) first
    for m_toc in re.finditer(r"^([A-Z][A-Za-z0-9_ /()&.\-]{2,60}?)\s+[-.]{4,}\s*(\d+)\s*$", text, flags=re.M):
        sec_title = m_toc.group(1).strip()
        page_num = m_toc.group(2).strip()
        entry = f"{sec_title} (p. {page_num})"
        if entry not in headings:
            headings.append(entry)

    # 2. Extract Markdown headings (`# Heading`) while excluding shell/Python comments inside code blocks
    raw_headings = [m.group(1).strip() for m in re.finditer(r"^#{1,3}\s+(.+)$", text, flags=re.M)]
    for h in raw_headings:
        if (
            not _is_known_cli_command(h)
            and not h.startswith(("-", "#", "Usage:", "def ", "from ", "import "))
            and not re.match(
                r"^(?:git|docker|kubectl|aws|az|gcloud|sudo|apt|yum|pip|npm|make|cd|mkdir|rm|cp|mv|chmod|chown|tcpdump|greynoise|easy_install)\b",
                h,
                flags=re.I,
            )
            and h not in headings
        ):
            headings.append(h)

    headings = headings[:120]
    steps = [
        m.group(0).strip()
        for m in re.finditer(r"^(?:(?:\d+\.|Step\s+\d+[:.]|- \[[ xX]\])\s+.+)$", text, flags=re.M)
    ][:45]

    # Extract canonical technical tags for Engine 1 Bipartite Graph
    tech_tokens = sorted(
        set(
            re.findall(
                r"\b(?:curl|tio|socat|nmap|masscan|iptables|netsh|netstat|ipconfig|wmic|icacls|cacls|bcdedit|auditpol|wevtutil|"
                r"powershell|sysinternals|pslist|listdlls|autorunsc|dsquery|mimikatz|impacket|hashcat|john|sqlmap|msfvenom|"
                r"bloodhound|responder|kerberos|volatility|yara|osquery|splunk|aws|gcloud|docker|kubectl|adb|frida|"
                r"tshark|tcpdump|wireshark|p0f|snort|netns|vlan|arp|mtls|tls|ssl|ssh|http|https|serial|ttyusb0|ttyusb1|"
                r"eth0|eth1|eth2|z3|clingo|pagerank|cegar|sygus|cve-\d{4}-\d+)\b",
                text.lower(),
            )
        )
    )

    # Extract Error -> Fix pairs if present in text
    cbr_rules: List[Dict[str, str]] = []
    for m_fix in re.finditer(
        r"(?:error|symptom|failure|issue)[:\s]+([^\n]{5,120})[\s\n]+(?:fix|solution|resolution|remediation)[:\s]+`?([^\n`]{5,160})`?",
        text,
        flags=re.I,
    ):
        cbr_rules.append(
            {
                "symptom": m_fix.group(1).strip(),
                "verified_fix": m_fix.group(2).strip(),
                "source_doc": source_name,
            }
        )

    return {
        "headings": headings,
        "steps": steps,
        "tech_tags": tech_tokens[:30],
        "cbr_rules": cbr_rules[:20],
    }


def chunk_document_with_breadcrumbs(text: str, doc_name: str, chunk_size: int = 2500) -> List[Dict[str, str]]:
    """
    Splits large books, PDFs, and manuals into semantic chunks prefixed with their
    Chapter / Section heading breadcrumb so multi-step procedures never lose context.
    """
    chunks: List[Dict[str, str]] = []
    cur_h1 = "Overview"
    cur_h2 = ""
    buf: List[str] = []
    buf_len = 0

    for ln in text.splitlines():
        m_h1 = re.match(r"^(?:#\s+|Chapter\s+\d+[:.\s]+|--- Page \d+ ---)(.+)?$", ln.strip(), flags=re.I)
        m_h2 = re.match(r"^(?:##+\s+|\d+\.\d+\s+)(.+)$", ln.strip())
        if m_h1:
            if buf:
                bc = f"[Book/Doc: {doc_name} > {cur_h1}" + (f" > {cur_h2}]" if cur_h2 else "]")
                chunks.append({"breadcrumb": bc, "text": bc + "\n" + "\n".join(buf)})
                buf, buf_len = [], 0
            cur_h1 = ln.strip().lstrip("#").strip()[:80]
            cur_h2 = ""
        elif m_h2:
            cur_h2 = m_h2.group(1).strip()[:80]

        buf.append(ln)
        buf_len += len(ln) + 1
        if buf_len >= chunk_size:
            bc = f"[Book/Doc: {doc_name} > {cur_h1}" + (f" > {cur_h2}]" if cur_h2 else "]")
            chunks.append({"breadcrumb": bc, "text": bc + "\n" + "\n".join(buf)})
            # Keep last 3 lines as overlap for sequential continuity
            overlap = buf[-3:]
            buf = list(overlap)
            buf_len = sum(len(x) + 1 for x in buf)

    if buf:
        bc = f"[Book/Doc: {doc_name} > {cur_h1}" + (f" > {cur_h2}]" if cur_h2 else "]")
        chunks.append({"breadcrumb": bc, "text": bc + "\n" + "\n".join(buf)})
    return chunks


_TACTIC_STATE_CHAIN: Dict[str, Tuple[str, str]] = {
    "Passive_Enum": ("s_init_unknown", "s_passive_topology_mapped"),
    "Reconnaissance": ("s_init_unknown", "s_passive_topology_mapped"),
    "Active_Enum": ("s_passive_topology_mapped", "s_active_services_enumerated"),
    "Enumeration": ("s_l2_l3_verified", "s_active_services_enumerated"),
    "Out-of-Band_Access": ("s_l2_l3_verified", "s_oob_serial_enumerated"),
    "Defense_Evasion_Firewall": ("s_oob_serial_enumerated", "s_firewall_or_acl_unlocked"),
    "Credential_Access": ("s_active_services_enumerated", "s_credentials_or_certs_acquired"),
    "Protocol_Chaining": ("s_credentials_or_certs_acquired", "s_protocol_chain_established"),
    "Covert_Infil": ("s_protocol_chain_established", "s_covert_infil_channel_ready"),
    "Initial_Access_Exploitation": ("s_active_services_enumerated", "s_initial_shell_or_api_access"),
    "Privilege_Escalation": ("s_initial_shell_or_api_access", "s_interactive_tty_or_priv_escalated"),
    "Lateral_Movement_Routing_Pivot": ("s_firewall_or_acl_unlocked", "s_cross_subnet_pivot_routed"),
    "Covert_Exfil": ("s_interactive_tty_or_priv_escalated", "s_covert_exfil_verified"),
    "Post_Exploitation_Verification": ("s_cross_subnet_pivot_routed", "s_goal_verified_complete"),
}


def _extract_mdp_transitions_from_doc(
    text: str,
    verified_cmds: List[Dict[str, Any]],
    doc_name: str,
    slug: str,
) -> List[Dict[str, Any]]:
    """
    Build 4-level Hierarchical MDP transitions (`Tactic -> Technique -> Tool -> Command`)
    with `(pre_state, post_state_success, alpha_success, alpha_fail)` from a document's
    CEGAR-verified commands and surrounding context.
    Classifies 100% of verified commands with no artificial ceiling, ordering them round-robin
    across all discovered Tactic Categories so the top of the table highlights diverse tactics.
    """
    by_tactic: Dict[str, List[Dict[str, Any]]] = {}
    for item in verified_cmds:
        cmd_str = item["command"]
        pos = text.find(cmd_str[:30])
        ctx_window = text[max(0, pos - 300) : pos + 300] if pos >= 0 else text[:600]
        tactic, technique, tool_bin = classify_tactic_category(ctx_window, cmd_str)
        item["tactic"] = tactic
        item["technique"] = technique
        item["tool"] = tool_bin
        by_tactic.setdefault(tactic, []).append(item)

    # Interleave across discovered tactics so every tactic category is represented from the start,
    # while retaining 100% of all verified commands as MDP transitions
    selected_items: List[Dict[str, Any]] = []
    tactic_keys = list(by_tactic.keys())
    round_idx = 0
    while tactic_keys:
        progressed = False
        for tk in tactic_keys:
            bucket = by_tactic[tk]
            if round_idx < len(bucket):
                selected_items.append(bucket[round_idx])
                progressed = True
        if not progressed:
            break
        round_idx += 1

    transitions: List[Dict[str, Any]] = []
    for idx, item in enumerate(selected_items, 1):
        cmd_str = item["command"]
        tactic = item["tactic"]
        technique = item["technique"]
        tool_bin = item["tool"]
        pre_s, post_s = _TACTIC_STATE_CHAIN.get(
            tactic, ("s_l2_l3_verified", "s_active_services_enumerated")
        )
        transitions.append(
            {
                "id": f"MDP_TRN_{slug.upper()}_{idx}",
                "pre_state": pre_s,
                "tactic": tactic,
                "technique": technique,
                "tool": tool_bin,
                "command_template": cmd_str,
                "post_state_success": post_s,
                "post_state_fail": pre_s,
                "alpha_success": 12.0,
                "alpha_fail": 1.5,
                "step_cost": 1.5,
                "source": doc_name,
            }
        )
    return transitions


def _select_substantive_chunks_for_llm(
    chunks: List[Dict[str, str]],
    wf_info: Dict[str, Any],
    verified_cmds: List[Dict[str, Any]],
) -> str:
    """
    Builds a high-signal context window for LLM distillation that skips PDF front-matter
    (copyright pages, ISBN blocks, and Twitter/social handle acknowledgement lists) and
    includes the document's Table-of-Contents headings + representative command & technical chunks.
    """
    parts: List[str] = []
    if wf_info.get("headings"):
        parts.append("DOCUMENT SECTIONS / CHAPTERS:\n" + ", ".join(wf_info["headings"][:60]))
    if verified_cmds:
        sample_cmds = [c["command"] for c in verified_cmds[:25]]
        parts.append("SAMPLE EXTRACTED COMMANDS:\n" + "\n".join(sample_cmds))

    substantive_texts: List[str] = []
    for c in chunks:
        txt = c["text"]
        low = txt.lower()
        # Skip front-matter copyright / acknowledgements / social-handle lists
        if "all rights reserved" in low or "infosec twitter" in low or txt.count("@") > 12:
            continue
        substantive_texts.append(txt)
        if len(substantive_texts) >= 2:
            break

    if not substantive_texts and chunks:
        substantive_texts = [c["text"] for c in chunks[:2]]

    parts.extend(substantive_texts)
    return "\n\n".join(parts)[:CHUNK_MAX_CHARS]


def _distill_with_cora_if_online(chunk_text: str, doc_name: str) -> Optional[str]:
    """
    If `llama-server` on 127.0.0.1:8080 is online, runs a fast, isolated single-chunk
    distillation pass (`max_tokens: 700`) to summarize key operational techniques & workflows.
    Never modifies or bloats the main CLI conversation history.
    """
    health_url = API_URL.split("/v1/")[0].rstrip("/") + "/health"
    try:
        with urllib.request.urlopen(health_url, timeout=1.2) as r:
            if r.status != 200:
                return None
    except Exception:
        return None

    prompt = (
        f"You are distilling a technical training document (`{doc_name}`) into a compact Obsidian Vault playbook.\n"
        "Extract ONLY:\n"
        "1. Key operational techniques & decision workflows (bulleted).\n"
        "2. Critical command patterns and required flags.\n"
        "3. Any network topology, IP/subnet, serial, or service relationships.\n"
        "Keep your response under 350 words in clean Markdown.\n\n"
        f"--- DOCUMENT CHUNK ---\n{chunk_text[:CHUNK_MAX_CHARS]}"
    )
    payload = {
        "messages": [
            {"role": "system", "content": "You are a precise technical knowledge distillation engine."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 700,
        "stream": False,
    }
    try:
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            choices = data.get("choices") or []
            if choices:
                content = (choices[0].get("message") or {}).get("content") or ""
                # Strip any <think>...</think> blocks if present
                content = re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()
                return content
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# PHASE 4: Tier-2 Obsidian Vault Storage & 14-Engine Symbolic Rule Injection
# ---------------------------------------------------------------------------
def train_on_single_file(file_path: Path, use_llm: bool = True) -> Dict[str, Any]:
    """Run all 4 phases on a single document or diagram image."""
    t0 = time.perf_counter()
    extracted = extract_file_content(file_path)
    raw_text = extracted["text"]
    topo_md = extracted["topology_markdown"]
    combined_source = (topo_md + "\n\n" + raw_text).strip()

    verified_cmds, quarantined_cmds = _extract_and_verify_commands_deterministic(combined_source)
    wf_info = _extract_workflows_and_rules_deterministic(combined_source, file_path.name)
    slug = f"trained_{_slugify(file_path.stem)}"
    mdp_transitions = _extract_mdp_transitions_from_doc(combined_source, verified_cmds, file_path.name, slug)
    chunks = chunk_document_with_breadcrumbs(combined_source, file_path.name, chunk_size=CHUNK_MAX_CHARS)

    know_path = VAULT_DIR / "knowledge" / f"{slug}.md"
    llm_summary = None
    if know_path.is_file():
        try:
            existing_know = know_path.read_text(encoding="utf-8", errors="replace")
            m_sum = re.search(
                r"^## LLM Distilled Operational Summary\s*\n(.*?)(?=\n## (?:Document Structure|Command & Tactic|Extracted Operational|Extracted Reference)|\Z)",
                existing_know,
                flags=re.M | re.S,
            )
            if m_sum and m_sum.group(1).strip():
                candidate_sum = m_sum.group(1).strip()
                # Invalidate old front-matter-only or truncated summaries
                if (
                    len(candidate_sum) >= 100
                    and "infosec twitter" not in candidate_sum.lower()
                    and "(pages 1–4)" not in candidate_sum.lower()
                ):
                    llm_summary = candidate_sum
        except Exception:
            pass
    if not llm_summary and use_llm and chunks:
        sample_chunk = _select_substantive_chunks_for_llm(chunks, wf_info, verified_cmds)
        llm_summary = _distill_with_cora_if_online(sample_chunk, file_path.name)

    tactic_tags = sorted({item.get("tactic", "").lower() for item in verified_cmds if item.get("tactic")})
    tags = sorted(set(["trained", "mdp", extracted["doc_type"]] + tactic_tags[:8] + wf_info["tech_tags"][:12]))
    tags_yaml = "\n".join(f"  - {t}" for t in tags)
    now_str = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")

    # 1. If executable commands were extracted, write `ObsidianVault/commands/trained_<slug>.md`
    cmd_note_rel = ""
    if verified_cmds:
        cmd_lines = [
            "---",
            f'title: "Trained Command Playbook: {file_path.name}"',
            "tags:",
            tags_yaml,
            f"source_file: {file_path.name}",
            f"updated: {now_str}",
            "---",
            "",
            f"# Trained Command Playbook: `{file_path.name}`",
            "",
            f"- **Source Document:** `{_portable_path(file_path)}`",
            f"- **CEGAR Verified Commands:** `{len(verified_cmds)}` (`{quarantined_cmds}` malformed/unsafe snippets filtered)",
            f"- **MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`):** `{len(mdp_transitions)}`",
            f"- **Discovered IPs/Subnets:** `{', '.join(extracted['ips']) or 'None'}`",
            f"- **Discovered Interfaces:** `{', '.join(extracted['interfaces']) or 'None'}`",
            f"- **Related Knowledge Note:** [[knowledge/{slug}]]",
            "",
        ]
        if mdp_transitions:
            cmd_lines.extend(
                [
                    "## Distilled MDP Tactical Transitions (`Tactic -> Technique -> Tool -> Command`)",
                    "| Pre-State ($s$) | Tactic ($\\tau$) | Technique ($k$) | Tool ($u$) | Post-State ($s'$) | Verified Command ($c$) |",
                    "| :--- | :--- | :--- | :--- | :--- | :--- |",
                ]
            )
            for tr in mdp_transitions[:40]:
                cmd_safe = tr["command_template"].replace("|", "\\|")
                cmd_lines.append(
                    f"| `{tr['pre_state']}` | **`{tr['tactic']}`** | {tr['technique']} | `{tr['tool']}` | `{tr['post_state_success']}` | `{cmd_safe}` |"
                )
            cmd_lines.append("")

        cmd_lines.extend(
            [
                "## Verified Executable Commands (Grouped by Capability Layer)",
                "",
            ]
        )
        by_layer: Dict[str, List[str]] = {}
        for item in verified_cmds:
            by_layer.setdefault(item["layer"], []).append(item["command"])
        for layer_name, cmds in sorted(by_layer.items()):
            cmd_lines.append(f"### {layer_name} ({len(cmds)} commands)")
            cmd_lines.append("```bash")
            for c in cmds:
                cmd_lines.append(c)
            cmd_lines.append("```\n")

        cmd_path = VAULT_DIR / "commands" / f"{slug}.md"
        _atomic_write_text(cmd_path, "\n".join(cmd_lines) + "\n")
        cmd_note_rel = f"commands/{slug}"

    # 2. Always write `ObsidianVault/knowledge/trained_<slug>.md` with workflows, command coverage, topology & concepts
    know_lines = [
        "---",
        f'title: "Trained Knowledge & Topology: {file_path.name}"',
        "tags:",
        tags_yaml,
        f"source_file: {file_path.name}",
        f"doc_type: {extracted['doc_type']}",
        f"updated: {now_str}",
        "---",
        "",
        f"# Trained Knowledge & Architecture: `{file_path.name}`",
        "",
        f"- **Source Path:** `{_portable_path(file_path)}` (`{extracted['doc_type']}`)",
        f"- **Extracted Technical Entities:** `{', '.join(wf_info['tech_tags']) or 'general'}`",
        f"- **Extracted IPs / Subnets:** `{', '.join(extracted['ips']) or 'None'}`",
        f"- **Extracted Interfaces:** `{', '.join(extracted['interfaces']) or 'None'}`",
    ]
    if cmd_note_rel:
        know_lines.append(
            f"- **Linked Command Playbook:** [[{cmd_note_rel}]] (`{len(verified_cmds)}` CEGAR-verified commands | `{len(mdp_transitions)}` MDP transitions)"
        )
    know_lines.append("")

    if verified_cmds:
        tactic_counts: Dict[str, int] = {}
        tool_counts: Dict[str, int] = {}
        for item in verified_cmds:
            tc = item.get("tactic") or "Enumeration"
            tl = item.get("tool") or "shell"
            tactic_counts[tc] = tactic_counts.get(tc, 0) + 1
            tool_counts[tl] = tool_counts.get(tl, 0) + 1
        top_tactics = ", ".join(
            f"`{k}` ({v})" for k, v in sorted(tactic_counts.items(), key=lambda x: (-x[1], x[0]))[:10]
        )
        top_tools = ", ".join(
            f"`{k}` ({v})" for k, v in sorted(tool_counts.items(), key=lambda x: (-x[1], x[0]))[:25]
        )
        know_lines.extend(
            [
                "## Command & Tactic Coverage Summary",
                f"- **Total CEGAR-Verified Commands:** `{len(verified_cmds)}` (full executable list in [[{cmd_note_rel}]])",
                f"- **Tactic Distribution:** {top_tactics}",
                f"- **Top Extracted CLI Tools:** {top_tools}",
                "",
            ]
        )

    if topo_md:
        know_lines.append(topo_md)
        know_lines.append("")

    if llm_summary:
        know_lines.append("## LLM Distilled Operational Summary")
        know_lines.append(llm_summary)
        know_lines.append("")

    if wf_info["headings"]:
        know_lines.append("## Document Structure & Key Topics")
        for h in wf_info["headings"]:
            know_lines.append(f"- {h}")
        know_lines.append("")

    if wf_info["steps"]:
        know_lines.append("## Extracted Operational Steps & Workflows")
        for st in wf_info["steps"]:
            know_lines.append(f"- {st}")
        know_lines.append("")

    if not llm_summary and raw_text:
        know_lines.append("## Extracted Reference Excerpt")
        know_lines.append(raw_text[:2800])
        know_lines.append("")

    know_path = VAULT_DIR / "knowledge" / f"{slug}.md"
    _atomic_write_text(know_path, "\n".join(know_lines) + "\n")
    know_note_rel = f"knowledge/{slug}"

    dt_ms = round((time.perf_counter() - t0) * 1000, 2)
    return {
        "file_path": _portable_path(file_path),
        "file_name": file_path.name,
        "slug": slug,
        "doc_type": extracted["doc_type"],
        "chunks_count": len(chunks),
        "verified_commands": verified_cmds,
        "quarantined_commands": quarantined_cmds,
        "mdp_transitions": mdp_transitions,
        "cbr_rules": wf_info["cbr_rules"],
        "ips": extracted["ips"],
        "interfaces": extracted["interfaces"],
        "tech_tags": wf_info["tech_tags"],
        "cmd_note": cmd_note_rel,
        "knowledge_note": know_note_rel,
        "llm_distilled": bool(llm_summary),
        "elapsed_ms": dt_ms,
    }


def _update_trained_rules_and_indexes(results: List[Dict[str, Any]], manifest: Dict[str, Any]) -> None:
    """
    Merges newly trained commands, CBR error->fix rules, and evolutionary capability primitives
    into `Reasoning/data/trained_rules.json` and updates `ObsidianVault/00_TRAINED_INDEX.md` +
    `ObsidianVault/00_MEMORY_INDEX.md`.
    """
    existing_rules: Dict[str, Any] = {
        "updated_at": "",
        "trained_documents_count": 0,
        "cbr_fingerprints": [],
        "evolutionary_primitives": [],
        "discovered_topologies": [],
    }
    if TRAINED_RULES_FILE.is_file():
        try:
            loaded = json.loads(TRAINED_RULES_FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                existing_rules.update(loaded)
        except Exception:
            pass

    cbr_list: List[Dict[str, Any]] = existing_rules.get("cbr_fingerprints", [])
    evo_list: List[Dict[str, Any]] = existing_rules.get("evolutionary_primitives", [])
    topo_list: List[Dict[str, Any]] = existing_rules.get("discovered_topologies", [])

    seen_cmds = {p.get("command_template") for p in evo_list}
    seen_symptoms = {c.get("symptom") for c in cbr_list}
    all_new_mdp_transitions: List[Dict[str, Any]] = []

    for res in results:
        all_new_mdp_transitions.extend(res.get("mdp_transitions", []))
        for idx_cbr, cbr in enumerate(res.get("cbr_rules", []), 1):
            if cbr["symptom"] not in seen_symptoms:
                seen_symptoms.add(cbr["symptom"])
                pat_clean = re.sub(r"[`*_]+", "", cbr["symptom"].split("`")[0]).strip()[:80]
                cbr_entry = dict(cbr)
                cbr_entry.setdefault("case_id", f"CBR-TRN-{len(cbr_list) + 1:03d}")
                cbr_entry.setdefault("binary", "any")
                cbr_entry.setdefault("exit_code", 1)
                cbr_entry.setdefault("error_pattern", re.escape(pat_clean) if pat_clean else "error")
                cbr_list.append(cbr_entry)

        for idx, cmd_item in enumerate(res.get("verified_commands", [])):
            cmd_str = cmd_item["command"]
            if cmd_str not in seen_cmds:
                seen_cmds.add(cmd_str)
                evo_list.append(
                    {
                        "id": f"P_TRAINED_{res['slug'].upper()}_{idx + 1}",
                        "name": f"trained_{res['slug']}_{idx + 1}",
                        "layer": cmd_item["layer"],
                        "risk": "State-Mutating-Pivot" if "sudo " in cmd_str else "Ephemeral-Probe",
                        "cmd": cmd_str,
                        "command_template": cmd_str,
                        "source_doc": res["file_name"],
                        "pre": [],
                        "post": [f"executed_{cmd_item['layer'].lower()}"],
                        "preconditions": ["host_shell_ready"],
                        "postconditions": [f"executed_{cmd_item['layer'].lower()}"],
                        "utility": 0.88,
                    }
                )

        if res.get("ips") or res.get("interfaces"):
            topo_list.append(
                {
                    "source_doc": res["file_name"],
                    "doc_type": res["doc_type"],
                    "ips": res["ips"],
                    "interfaces": res["interfaces"],
                }
            )

    now_iso = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")
    mdp_merged_count = merge_trained_mdp_transitions(all_new_mdp_transitions)
    existing_rules["updated_at"] = now_iso
    existing_rules["trained_documents_count"] = len(manifest.get("files", {}))
    existing_rules["mdp_transitions_merged"] = mdp_merged_count
    existing_rules["cbr_fingerprints"] = cbr_list
    existing_rules["evolutionary_primitives"] = evo_list
    existing_rules["discovered_topologies"] = topo_list
    save_json_state(TRAINED_RULES_FILE, existing_rules)

    # Update `ObsidianVault/00_TRAINED_INDEX.md`
    idx_lines = [
        "# Trained Documentation, Playbooks & Network Diagrams Index (`00_TRAINED_INDEX.md`)",
        "",
        f"- **Last Updated:** `{now_iso}`",
        f"- **Total Trained Documents & Diagrams:** `{len(manifest.get('files', {}))}`",
        f"- **Active Evolutionary Command Primitives:** `{len(existing_rules['evolutionary_primitives'])}`",
        f"- **Active CBR Failure Fingerprints:** `{len(existing_rules['cbr_fingerprints'])}`",
        "",
        "| Source Document | Type | Knowledge Note | Command Playbook | Verified Cmds | IPs / Interfaces |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for fpath, meta in sorted(manifest.get("files", {}).items(), key=lambda x: x[1].get("file_name", "")):
        k_link = f"[[{meta['knowledge_note']}]]" if meta.get("knowledge_note") else "-"
        c_link = f"[[{meta['cmd_note']}]]" if meta.get("cmd_note") else "-"
        ip_if = ", ".join((meta.get("ips") or [])[:3] + (meta.get("interfaces") or [])[:3]) or "-"
        idx_lines.append(
            f"| `{meta.get('file_name')}` | `{meta.get('doc_type')}` | {k_link} | {c_link} | "
            f"`{meta.get('verified_cmd_count', 0)}` | `{ip_if}` |"
        )
    _atomic_write_text(TRAINED_INDEX_FILE, "\n".join(idx_lines) + "\n")

    # Ensure `00_MEMORY_INDEX.md` has a single compact 1-line link to `[[00_TRAINED_INDEX]]`
    if MEMORY_INDEX_FILE.is_file():
        mem_txt = MEMORY_INDEX_FILE.read_text(encoding="utf-8", errors="replace")
        if "[[00_TRAINED_INDEX]]" not in mem_txt:
            mem_txt = (
                mem_txt.rstrip()
                + "\n- [[00_TRAINED_INDEX]] — Master Index of Trained Documentation, Command Playbooks & Network Diagrams\n"
            )
            _atomic_write_text(MEMORY_INDEX_FILE, mem_txt)

    # Invalidate Engine 1 in-memory graph cache so newly trained notes are indexed immediately
    try:
        from Reasoning.engines import associative

        associative._GRAPH_CACHE["signature"] = None
    except Exception:
        pass


def run_training_pipeline(
    target_path: Optional[Path] = None,
    force: bool = False,
    use_llm: bool = True,
    auto_install_deps: bool = True,
    quiet: bool = False,
) -> Dict[str, Any]:
    """
    Discover all supported documents, PDFs, and diagram images in `target_path`
    (defaults to `~/Projects/CORA/Training`), run the 4-Phase
    Distillation & CEGAR Verification Pipeline, and update `ObsidianVault/` and `Reasoning/data/`.
    """
    ensure_directories()
    DEFAULT_TRAINING_DIR.mkdir(parents=True, exist_ok=True)
    dep_status = check_and_install_dependencies(auto_install=auto_install_deps)

    target = resolve_training_target(target_path)
    if not target.exists():
        raise FileNotFoundError(f"Training path does not exist: {target}")

    manifest: Dict[str, Any] = {"files": {}}
    if MANIFEST_FILE.is_file():
        try:
            m_loaded = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
            if isinstance(m_loaded, dict) and isinstance(m_loaded.get("files"), dict):
                manifest = m_loaded
        except Exception:
            pass

    candidate_files: List[Path] = []
    if target.is_file():
        if target.suffix.lower() in ALL_SUPPORTED_EXTS:
            candidate_files.append(target)
    else:
        for p in sorted(target.rglob("*")):
            if p.is_file() and p.suffix.lower() in ALL_SUPPORTED_EXTS:
                # Skip the runner scripts (train_llm_NIX.sh / train_llm_WIN.ps1) and instructional README.md in Training/
                if p.parent == DEFAULT_TRAINING_DIR and p.name in ("train_llm_NIX.sh", "train_llm_WIN.ps1"):
                    continue
                if p.parent == DEFAULT_TRAINING_DIR and p.name == "README.md" and not force:
                    continue
                candidate_files.append(p)

    trained_results: List[Dict[str, Any]] = []
    skipped_unchanged = 0

    print("\033[1;36m==============================================================================\033[0m")
    print("\033[1;37m  CORA 4-PHASE DOCUMENT, OCR & NETWORK DIAGRAM TRAINING PIPELINE\033[0m")
    print("\033[1;36m==============================================================================\033[0m")
    print(f"  Target Path:     `{target}`")
    print(
        f"  Extractors:      PDF=`{dep_status['pdf_ready']}` | Neural OCR=`{dep_status['ocr_ready']}` | "
        f"DOCX=`{dep_status['docx_ready']}` | HTML=`{dep_status['html_ready']}`"
    )
    print(f"  Discovered Docs: {len(candidate_files)} supported file(s)")

    for fpath in candidate_files:
        try:
            raw_bytes = fpath.read_bytes()
            sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
        except Exception as exc:
            print(f"  \033[1;31m[SKIP]\033[0m Could not read `{fpath.name}`: {exc}")
            continue

        port_key = _portable_path(fpath)
        prev_entry = manifest["files"].get(port_key) or manifest["files"].get(str(fpath))
        if not prev_entry:
            for existing_entry in manifest["files"].values():
                if (
                    isinstance(existing_entry, dict)
                    and existing_entry.get("sha256") == sha256_hex
                    and existing_entry.get("extractor_v2")
                ):
                    prev_entry = existing_entry
                    break
        if (
            not force
            and prev_entry
            and prev_entry.get("sha256") == sha256_hex
            and prev_entry.get("extractor_v2")
        ):
            # Verify its Vault note still exists before skipping
            k_note = VAULT_DIR / f"{prev_entry.get('knowledge_note', '')}.md"
            if k_note.is_file():
                if str(fpath) in manifest["files"] and port_key != str(fpath):
                    manifest["files"][port_key] = manifest["files"].pop(str(fpath))
                skipped_unchanged += 1
                print(f"  \033[1;34m[CACHED]\033[0m `{fpath.name}` (SHA-256 unchanged -> `[[{prev_entry.get('knowledge_note')}]]`)")
                continue

        print(f"  \033[1;33m[TRAINING]\033[0m Processing `{fpath.name}` ...", end="", flush=True)
        res = train_on_single_file(fpath, use_llm=use_llm)
        trained_results.append(res)

        manifest["files"].pop(str(fpath), None)
        manifest["files"][port_key] = {
            "file_name": fpath.name,
            "sha256": sha256_hex,
            "doc_type": res["doc_type"],
            "knowledge_note": res["knowledge_note"],
            "cmd_note": res["cmd_note"],
            "verified_cmd_count": len(res["verified_commands"]),
            "quarantined_cmd_count": res["quarantined_commands"],
            "extractor_v2": True,
            "ips": res["ips"],
            "interfaces": res["interfaces"],
            "trained_at": datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds"),
        }
        save_json_state(MANIFEST_FILE, manifest)
        print(
            f" \033[1;32mDONE\033[0m ({res['elapsed_ms']} ms | "
            f"{len(res['verified_commands'])} CEGAR-verified cmds | "
            f"{len(res.get('mdp_transitions', []))} MDP transitions | "
            f"IPs={len(res['ips'])} | -> `[[{res['knowledge_note']}]]`)"
        )
        _log_training(
            f"TRAINED file={fpath.name} type={res['doc_type']} verified_cmds={len(res['verified_commands'])} "
            f"ips={res['ips']} note={res['knowledge_note']}"
        )

    save_json_state(MANIFEST_FILE, manifest)
    _update_trained_rules_and_indexes(trained_results, manifest)

    if trained_results:
        try:
            ver_file = LOG_DIR / "cora_version.json"
            if ver_file.is_file():
                v_data = json.loads(ver_file.read_text(encoding="utf-8", errors="replace"))
                v_data["patch_rev"] = int(v_data.get("patch_rev", 12)) + 1
                v_data["version"] = f"{v_data.get('major_cli', 5)}.{v_data.get('engine_rev', 15)}.{v_data['patch_rev']}"
                v_data["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                v_data["patch_tree_sha256"] = ""
                v_data["last_update_reason"] = f"Retrained on {len(trained_results)} document(s) via train_llm.py"
                ver_file.write_text(json.dumps(v_data, indent=2) + "\n", encoding="utf-8")
        except Exception:
            pass

    total_cmds = sum(len(r["verified_commands"]) for r in trained_results)
    summary = {
        "target_path": str(target),
        "discovered_files": len(candidate_files),
        "newly_trained_files": len(trained_results),
        "skipped_cached_files": skipped_unchanged,
        "total_manifest_files": len(manifest["files"]),
        "newly_verified_commands": total_cmds,
        "trained_index_note": str(TRAINED_INDEX_FILE),
        "trained_rules_file": str(TRAINED_RULES_FILE),
        "extractors": dep_status,
    }
    print("\033[1;36m------------------------------------------------------------------------------\033[0m")
    print(
        f"  \033[1;32m[TRAINING COMPLETE]\033[0m Newly trained: `{len(trained_results)}` | "
        f"Cached: `{skipped_unchanged}` | Total in Vault: `{len(manifest['files'])}`"
    )
    print(f"  Obsidian Index:  `{TRAINED_INDEX_FILE}` (`[[00_TRAINED_INDEX]]`)")
    print(f"  Symbolic Rules:  `{TRAINED_RULES_FILE}`")
    print("\033[1;36m==============================================================================\033[0m")
    return summary


def get_training_status() -> Dict[str, Any]:
    dep_status = check_and_install_dependencies(auto_install=False)
    manifest_count = 0
    if MANIFEST_FILE.is_file():
        try:
            m = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
            manifest_count = len(m.get("files", {}))
        except Exception:
            pass
    rules_summary = {"cbr_fingerprints": 0, "evolutionary_primitives": 0, "discovered_topologies": 0}
    if TRAINED_RULES_FILE.is_file():
        try:
            r = json.loads(TRAINED_RULES_FILE.read_text(encoding="utf-8"))
            rules_summary = {
                "cbr_fingerprints": len(r.get("cbr_fingerprints", [])),
                "evolutionary_primitives": len(r.get("evolutionary_primitives", [])),
                "discovered_topologies": len(r.get("discovered_topologies", [])),
            }
        except Exception:
            pass
    mdp_store = load_or_init_mdp_store()
    return {
        "default_training_dir": _portable_path(DEFAULT_TRAINING_DIR),
        "trained_documents_count": manifest_count,
        "trained_rules": rules_summary,
        "mdp_transitions_total": len(mdp_store.get("transitions", [])),
        "mdp_tactic_categories": mdp_store.get("tactic_categories", []),
        "trained_index_exists": TRAINED_INDEX_FILE.is_file(),
        "extractors": dep_status,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CORA 4-Phase Multi-Modal Document, PDF, Image OCR & Network Diagram Trainer"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_TRAINING_DIR),
        help="Folder or file to train on (defaults to Training/)",
    )
    parser.add_argument("--force", "-f", action="store_true", help="Force re-training even if SHA-256 matches manifest")
    parser.add_argument("--no-llm", action="store_true", help="Use fast deterministic CPU + OCR + SyGuS extraction only")
    parser.add_argument("--status", action="store_true", help="Show training status, extractor readiness, and rule counts")
    parser.add_argument(
        "--install-deps",
        "--check-deps",
        dest="install_deps",
        action="store_true",
        help="Verify and auto-install PDF, DOCX, and Neural OCR dependencies",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output")

    args = parser.parse_args()

    if args.install_deps:
        res = check_and_install_dependencies(auto_install=True)
        print(json.dumps(res, indent=2))
        return

    if args.status:
        st = get_training_status()
        print(json.dumps(st, indent=2))
        return

    summary = run_training_pipeline(
        target_path=Path(args.path),
        force=args.force,
        use_llm=not args.no_llm,
        auto_install_deps=True,
    )
    if args.json:
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
