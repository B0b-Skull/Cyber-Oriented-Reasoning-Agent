# C.O.R.A. Training Corpus (`CORA/Training/` — `v5.12.10`)

**Author:** https://CROWinnovations.com  

Drop any technical documentation, runbooks, cheat sheets, scripts, PDFs, Word documents, or network architecture diagrams into this folder (`Training/` or subfolders) and run:

```bash
# Option 1: Via root runner scripts (Linux or Windows)
./run_cora_NIX.sh -train
.\run_cora_WIN.ps1 -train

# Option 2: Standalone Linux / Windows script inside Training/
./Training/train_llm_NIX.sh
.\Training\train_llm_WIN.ps1

# Option 3: Inside the interactive You> CLI
/train Training
```

---

## Supported File Formats & Multi-Modal Extraction

| Category | Extensions | Extraction & Reasoning Distillation Method |
| :--- | :--- | :--- |
| **Markdown, Text & Cheat Sheets** | `.md`, `.txt`, `.rst`, `.log`, `.csv` | Heading-aware section breadcrumb chunking, cross-platform CLI command extraction (Linux, Windows CMD, Sysinternals, Active Directory, PowerShell `Verb-Noun`, Solaris, Cisco IOS), automatic inline comment stripping (`<---...`, `\t:Description`, `(Linux only)`, `OR` splitting), topology entity parsing |
| **Scripts & Configs** | `.sh`, `.bash`, `.ps1`, `.py`, `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.conf` | Command syntax extraction, cross-platform Engine 12 CEGAR verification, CBR failure rule synthesis & MDP state-action transition mapping |
| **PDF Documents** | `.pdf` | `pymupdf` (`fitz`) + `pypdf` text extraction **plus embedded page image/diagram OCR** + automatic non-breaking space (`\xa0`) normalization |
| **Office & Web Docs** | `.docx`, `.html`, `.htm` | `python-docx` paragraphs/tables & `BeautifulSoup4` DOM extraction |
| **Vector Diagrams** | `.svg` | XML `<text>` / `<tspan>` coordinate clustering & arrow/edge topology reconstruction |
| **Raster Diagrams & Screenshots** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff` | **100% CPU ONNX Neural OCR (`rapidocr-onnxruntime`)** + `pytesseract` fallback + spatial bounding-box clustering (`<= 185 px`) into Network Nodes, IPv4/CIDR Subnets, Interfaces, and Ports |

---

## How the 4-Phase Distillation & Verification Pipeline Protects Reasoning Integrity

1. **Zero Context Window Bloat**: Raw documents are never dumped into the live chat prompt. Instead, they are distilled into atomic, frontmatter-indexed notes inside `core/ObsidianVault/knowledge/trained_*.md` and `core/ObsidianVault/commands/trained_*.md`.
2. **Cross-Platform Engine 12 CEGAR Gatekeeper**: Every extracted command is verified against **Engine 12 (`core/Reasoning/engines/cegar_verifier.py`)** before being stored (`bash -n` for Linux/POSIX commands; balanced-parenthesis and `-n` ping flag verification for Windows CMD, Sysinternals, Active Directory, and PowerShell commands). Dangerous, syntax-broken, or hallucinated commands are quarantined and never reach the active playbook library.
3. **Per-File SHA-256 + `extractor_v2` Manifest & Cached LLM Summary Reuse**: `core/Reasoning/data/training_manifest.json` checkpoints the SHA-256 hash and `extractor_v2` flag after every single file in `Training/`. Re-running `./run_cora_NIX.sh -train` or `./Training/train_llm_NIX.sh` only processes new or modified files, and when upgrading previously trained files to a newer extractor version, it reuses the cached `## LLM Distilled Operational Summary` from `core/ObsidianVault/knowledge/trained_*.md` so upgrades finish in milliseconds per file (use `--force` to re-run LLM summaries from scratch).
4. **Structured 15-Engine Reasoning & Tactical MDP Sync**: Verified troubleshooting signatures, multi-step command primitives, and hierarchical `(State -> Tactic -> Technique -> Tool -> Command -> Next State)` transitions are automatically merged into `core/Reasoning/data/trained_rules.json` (**Engine 7 CBR** & **Engine 12 Continual Learner**) and `core/Reasoning/data/mdp_transitions.json` (**Engine 11 Hierarchical Tactical MDP**).
