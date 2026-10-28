"""
Neuro-Symbolic Reasoning Engines for CORA (Qwen3.5-9B & Qwen3.8-27B).
All modules are lazy-loaded and execute strictly on CPU (0 MB GPU VRAM).
"""
from pathlib import Path

REASONING_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = REASONING_DIR / "data"
CORA_CORE_DIR = REASONING_DIR.parent
VAULT_DIR = CORA_CORE_DIR / "ObsidianVault"

__all__ = ["REASONING_DIR", "DATA_DIR", "CORA_CORE_DIR", "VAULT_DIR"]
