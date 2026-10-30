"""
Bi-directional storage bridge between `Reasoning/data/` (machine-readable JSON state)
and `ObsidianVault/reasoning/` + `00_MEMORY_INDEX.md` (human + LLM readable Markdown notes).
"""
from datetime import datetime
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import threading
from typing import Any, Dict, List, Optional, Tuple

_VAULT_IO_LOCK = threading.RLock()

REASONING_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = REASONING_DIR / "data"
CBR_DIR = str(DATA_DIR / "cbr_cases")
SHADOW_ARCHIVE_DIR = str(DATA_DIR / "shadow_archive")
CORA_CORE_DIR = REASONING_DIR.parent
CORA_ROOT = CORA_CORE_DIR.parent if CORA_CORE_DIR.name.lower() == "core" else CORA_CORE_DIR
VAULT_DIR = Path(os.environ.get("OBSIDIAN_VAULT_DIR", str(CORA_CORE_DIR / "ObsidianVault"))).resolve()
PROJECTS_DIR = Path(
    os.environ.get("CORA_PROJECTS_DIR")
    or str(CORA_ROOT / "Projects")
).resolve()
INDEX_FILE = VAULT_DIR / "00_MEMORY_INDEX.md"


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_\-]+", "_", str(name).strip()).strip("_").lower()
    s = s[:64].strip("_")
    if not re.search(r"(?:192|10|172)(?:_\d{1,3}){3}$", s):
        s = re.sub(r"(?:^|_)(?:192|10|172)(?:_\d{1,3}){0,2}$", "", s).strip("_")
    return s or "reasoning_note"


_PARAM_IPV4_RE = re.compile(
    r"\b(?!127\.0\.0\.1\b|0\.0\.0\.0\b|255\.255\.255\.\d+\b)"
    r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b"
)


def parameterize_tactical_template(text: str) -> str:
    """
    Replace concrete target IPv4 addresses (`-> <TARGET_IP>`) and local user/project directory paths
    (`-> $PROJECT_DIR`) so online tactical stores (`somatic_markers.json`, `rl_policy_table.json`,
    `learned_cbr_cases.json`, `cbr_library.json`) learn reusable tactical patterns without storing
    dirty local IPs, usernames, or paths.
    """
    if not text:
        return ""
    s = _PARAM_IPV4_RE.sub("<TARGET_IP>", str(text))
    s = re.sub(r"(?:~|/home/[^/\s'\"]+|[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s'\"]+)[\\/]+Projects[\\/]+CORA[\\/]+Projects[\\/]+[^\\/\s'\"]+", "$PROJECT_DIR", s)
    s = re.sub(r"(?:~|/home/[^/\s'\"]+|[A-Za-z]:[\\/]+[^\s'\"]+)[\\/]+Projects[\\/]+[^\\/\s'\"]+", "$PROJECT_DIR", s)
    s = re.sub(r"/home/[^/\s'\"]+", "~", s)
    s = re.sub(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s'\"]+", "~", s)
    curr_user = os.environ.get("USER") or os.environ.get("USERNAME") or ""
    if curr_user and len(curr_user) >= 3:
        s = re.sub(rf"\b{re.escape(curr_user)}\b", "$USER", s)
    return s


def _atomic_write_text(path: Path, content: str) -> None:
    """
    Atomically write text to `path` via a PID+Thread-scoped temporary file + `os.replace()`,
    preventing partial-write JSON corruption when background `SpeculativeLookaheadCache`,
    parallel Layer-2 `ThreadPoolExecutor` workers, and the foreground CLI write concurrently.
    Also handles multi-group (`llm-local` / `sudo`) permission recovery if an older file was
    created by root in a writable directory.
    """
    with _VAULT_IO_LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.parent / f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp"
        try:
            tmp_path.write_text(content, encoding="utf-8")
            if os.name == "posix":
                try:
                    os.chmod(tmp_path, 0o664)
                except Exception:
                    pass
            try:
                os.replace(tmp_path, path)
            except PermissionError:
                try:
                    path.unlink(missing_ok=True)
                except Exception:
                    pass
                os.replace(tmp_path, path)
        except Exception:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass
            try:
                path.write_text(content, encoding="utf-8")
            except PermissionError:
                try:
                    path.unlink(missing_ok=True)
                    path.write_text(content, encoding="utf-8")
                except Exception:
                    pass


EPHEMERAL_ROTATED_SUBDIRS = {
    "associative_graphs",
    "vsa_spaces",
    "temporal_fluents",
    "dempster_shafer",
    "mdp_policies",
    "sessions",
}
_cached_max_files = 100
_HW_LIMITS_RAM_CACHE: Optional[Dict[str, Any]] = None
_DIRS_ENSURED: bool = False
_JSON_STATE_RAM_CACHE: Dict[str, Tuple[float, Any]] = {}


def ensure_directories() -> None:
    global _DIRS_ENSURED
    if _DIRS_ENSURED and DATA_DIR.is_dir() and VAULT_DIR.is_dir() and PROJECTS_DIR.is_dir():
        return
    for sub in (
        "causal_dags",
        "geometric_models",
        "associative_graphs",
        "vsa_spaces",
        "temporal_fluents",
        "dempster_shafer",
        "cbr_cases",
        "mdp_policies",
        "shadow_archive",
        "sessions",
    ):
        (DATA_DIR / sub).mkdir(parents=True, exist_ok=True)
    for sub in (".obsidian", "targets", "commands", "projects", "knowledge", "reasoning", "SuggestedImprovements"):
        (VAULT_DIR / sub).mkdir(parents=True, exist_ok=True)
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    _DIRS_ENSURED = True


_INVALID_PROJECT_NAMES = {"active_session", "active-session", "default", "default-project", "default_session"}


def slugify_project_name(name: str) -> str:
    """
    Sanitize a project directory name in `Projects/<project_name>/`:
    Spaces and any special/strange characters are automatically converted to dashes (`-`).
    If an existing directory with that exact name already exists on disk,
    preserve its exact directory name.
    """
    raw = str(name or "").strip()
    if not raw or raw.lower() in _INVALID_PROJECT_NAMES:
        return ""
    if (PROJECTS_DIR / raw).is_dir() and re.match(r"^[a-zA-Z0-9_\-]+$", raw):
        return raw
    s = re.sub(r"[^a-zA-Z0-9\-]+", "-", raw).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    clean = s[:64].strip("-")
    return "" if clean.lower() in _INVALID_PROJECT_NAMES else clean


def _resolve_existing_project_slug(candidate: str = "") -> str:
    """Resolve an active project slug from candidate, env, state files, or existing `Projects/` folders."""
    for raw in (
        candidate,
        os.environ.get("CORA_ACTIVE_PROJECT", ""),
    ):
        slug = slugify_project_name(raw)
        if slug and (PROJECTS_DIR / slug).is_dir():
            return slug

    for state_file in (
        CORE_DIR / "Log" / "active-project.txt",
        DATA_DIR / "sessions" / "active_project.txt",
    ):
        if state_file.is_file():
            try:
                saved = slugify_project_name(state_file.read_text(encoding="utf-8", errors="replace").strip())
                if saved and (PROJECTS_DIR / saved).is_dir():
                    return saved
            except Exception:
                pass

    if PROJECTS_DIR.is_dir():
        existing = [
            d.name
            for d in sorted(PROJECTS_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
            if d.is_dir() and not d.name.startswith(".") and d.name.lower() not in _INVALID_PROJECT_NAMES
        ]
        if existing:
            return existing[0]

    # If the caller explicitly provided a new valid project name, allow creating it
    explicit_slug = slugify_project_name(candidate) or slugify_project_name(os.environ.get("CORA_ACTIVE_PROJECT", ""))
    return explicit_slug


def get_active_project_dir(project_name: str = "") -> Path:
    """
    Resolve and initialize the isolated project workspace inside `CORA/Projects/<project_slug>/`.
    Never creates a dummy `active_session` or `default` project in `Projects/`.
    Creates `Files/`, `downloads/`, `artifacts/`, `targets/`, `notes/`, `reasoning/`, and `memory.md`.
    """
    ensure_directories()
    slug = _resolve_existing_project_slug(project_name)
    if slug:
        proj_dir = PROJECTS_DIR / slug
    else:
        # No user project selected or created yet; keep scratch state outside `Projects/`
        slug = "unassigned"
        proj_dir = DATA_DIR / "sessions" / "_unassigned_workspace"
    for sub in ("Files", "downloads", "artifacts", "targets", "notes", "reasoning", "shadow_archive"):
        (proj_dir / sub).mkdir(parents=True, exist_ok=True)
    mem_file = proj_dir / "memory.md"
    if not mem_file.exists():
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _atomic_write_text(
            mem_file,
            "---\n"
            f"title: Project Memory ({slug})\n"
            "category: project_workspace\n"
            f"project: {slug}\n"
            f"summary: Isolated project memory, downloaded artifacts, target scans & test state for {slug}\n"
            f"updated: {now_str}\n"
            "---\n"
            f"# Project Workspace Memory (`Projects/{slug}/memory.md`)\n\n"
            "> **Two-Tier Memory Isolation:** Ephemeral test data, target scans, downloaded files (`downloads/`), "
            "and session notes for this project are isolated here so long-term universal knowledge in `ObsidianVault/` is never polluted.\n\n"
            "## 1. Verified Data & Architecture\n"
            "- Workspace initialized at `Projects/" + slug + "/`\n"
            "- Downloaded files directory: `Projects/" + slug + "/downloads/`\n\n"
            "## 2. Open Verification Questions\n"
            "- None\n\n"
            "## 3. Project Plan & Task Tracking\n"
            "- [ ] Initial project / test workspace ready\n\n"
            "## 4. Indexed Project Notes, Target Scans & Downloads\n"
            "<!-- PROJECT-INDEX-START -->\n"
            "<!-- PROJECT-INDEX-END -->\n",
        )
    return proj_dir


def update_project_memory_index(proj_dir: Path, rel_link: str, summary: str, tags: Optional[List[str]] = None) -> Path:
    """Update the `<!-- PROJECT-INDEX-START -->` section inside `Projects/<slug>/memory.md`."""
    mem_file = proj_dir / "memory.md"
    if not mem_file.exists():
        get_active_project_dir(proj_dir.name)
    text = mem_file.read_text(encoding="utf-8", errors="replace")
    tag_str = " ".join(f"#{str(t).lstrip('#')}" for t in (tags or []) if str(t).strip())
    entry_line = f"- [[{rel_link}]] — {summary.strip()}" + (f" ({tag_str})" if tag_str else "")
    start_marker = "<!-- PROJECT-INDEX-START -->"
    end_marker = "<!-- PROJECT-INDEX-END -->"
    if start_marker in text and end_marker in text:
        before, rest = text.split(start_marker, 1)
        middle, after = rest.split(end_marker, 1)
        lines = [ln for ln in middle.strip().splitlines() if ln.strip()]
        updated = False
        for idx, ln in enumerate(lines):
            if f"[[{rel_link}]]" in ln:
                lines[idx] = entry_line
                updated = True
                break
        if not updated:
            lines.append(entry_line)
        lines = lines[-50:]
        new_text = f"{before}{start_marker}\n" + "\n".join(lines) + f"\n{end_marker}{after}"
    else:
        new_text = text.rstrip() + f"\n\n## 4. Indexed Project Notes, Target Scans & Downloads\n{start_marker}\n{entry_line}\n{end_marker}\n"
    _atomic_write_text(mem_file, new_text)
    return mem_file


def get_hardware_reasoning_limits() -> Dict[str, Any]:
    """
    Dynamically compute hardware-adaptive reasoning parameters for all 20 symbolic/statistical
    engines and the 5-Layer Lexical Priority Cascade based on the local machine's CPU physical
    cores, logical threads, NUMA topology, System RAM, and GPU VRAM.
    Automatically detects if the project was moved to a different machine (e.g., from a laptop
    to a Dual Xeon + 512 GB RAM + 48 GB RTX A6000 server) and re-profiles automatically.
    """
    global _cached_max_files, _HW_LIMITS_RAM_CACHE
    if _HW_LIMITS_RAM_CACHE is not None:
        return _HW_LIMITS_RAM_CACHE
    ensure_directories()
    prof_path = DATA_DIR / "hardware_profile.json"

    cpu_threads = os.cpu_count() or 4
    cpu_physical_cores = max(1, cpu_threads // 2)
    numa_nodes = 1
    total_ram_mib = 8192
    try:
        if Path("/proc/cpuinfo").is_file():
            phys_ids = set()
            core_pairs = set()
            cur_phys = "0"
            for ln in Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace").splitlines():
                if ln.startswith("physical id"):
                    cur_phys = ln.split(":", 1)[1].strip()
                    phys_ids.add(cur_phys)
                elif ln.startswith("core id"):
                    core_pairs.add((cur_phys, ln.split(":", 1)[1].strip()))
            if core_pairs:
                cpu_physical_cores = len(core_pairs)
            if phys_ids:
                numa_nodes = max(1, len(phys_ids))
        node_dirs = list(Path("/sys/devices/system/node").glob("node[0-9]*")) if Path("/sys/devices/system/node").is_dir() else []
        if node_dirs:
            numa_nodes = max(numa_nodes, len(node_dirs))
    except Exception:
        pass

    try:
        if Path("/proc/meminfo").is_file():
            for ln in Path("/proc/meminfo").read_text(encoding="utf-8", errors="replace").splitlines():
                if ln.startswith("MemTotal:"):
                    total_ram_mib = int(ln.split()[1]) // 1024
                    break
        elif os.name == "nt":
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                total_ram_mib = int(stat.ullTotalPhys // (1024 * 1024))
    except Exception:
        pass

    detected_gpu_vram_mib = 0
    gpu_count = 0
    try:
        nvsmi = shutil.which("nvidia-smi")
        if nvsmi:
            out = subprocess.check_output(
                [nvsmi, "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=3,
            ).strip()
            if out:
                vram_list = [int(x.strip()) for x in out.splitlines() if x.strip().isdigit()]
                if vram_list:
                    detected_gpu_vram_mib = max(vram_list)
                    gpu_count = len(vram_list)
    except Exception:
        pass

    if prof_path.is_file():
        try:
            cached = json.loads(prof_path.read_text(encoding="utf-8"))
            if (
                cached.get("cpu_threads") == cpu_threads
                and abs(cached.get("total_ram_mib", 0) - total_ram_mib) < 1024
                and cached.get("detected_gpu_vram_mib", 0) == detected_gpu_vram_mib
                and cached.get("vsa_hypervector_dim") == 1024
                and "rl_train_episodes" in cached
                and "kmeans_n_init" in cached
                and "z3_timeout_ms" in cached
            ):
                if "tier" not in cached and "hardware_tier" in cached:
                    cached["tier"] = cached["hardware_tier"]
                _cached_max_files = int(cached.get("shadow_archive_max_files", 100))
                _HW_LIMITS_RAM_CACHE = cached
                return cached
        except Exception:
            pass

    if total_ram_mib >= 120000 or detected_gpu_vram_mib >= 24000 or cpu_threads >= 36:
        tier = "ULTRA_SERVER_DATACENTER"
        vsa_dim = 1024
        evo_generations = 800
        evo_beam_width = 64
        pagerank_max_iter = 400
        spreading_hops = 4
        top_k_notes = 12
        max_hot_notes = 2500
        z3_timeout_ms = 5000
        max_cidr_rects = 512
        fca_max_concepts = 512
        eig_depth = 4
        max_hypotheses = 32
        causal_paths = 64
        causal_steps = 20
        analogy_candidates = 128
        analogy_beam = 32
        somatic_cap = 2000
        asp_horizon = 16
        ao_star_exp = 512
        fluent_history = 1000
        schmitt_window = 8
        dst_focal_limit = 256
        dst_mc_samples = 2000
        cbr_max_cases = 2000
        cbr_top_k = 8
        cegar_loops = 12
        cegar_ast_depth = 64
        sygus_lines = 5000
        sygus_beam = 32
        mdp_sweeps = 160
        mdp_horizon = 12
        speculative_branches = 8
        continual_candidates = 16
        continual_window = 500
        meta_bins = 20
        meta_window = 1000
        shapley_coalitions = 256
        ablation_max_entries = 500
        rl_episodes = 1200
        rl_horizon = 8
        rl_sweeps = 64
        kmeans_n_init = 32
        kmeans_max_iter = 300
        pca_buffer_size = 2000
        shadow_max_files = 500
        raw_preserve_chars = 12000
        max_tool_chars = 16000
        max_history_chars = 180000
    elif total_ram_mib >= 24000 and cpu_threads >= 16:
        tier = "EXTREME_WORKSTATION"
        vsa_dim = 1024
        evo_generations = 320
        evo_beam_width = 36
        pagerank_max_iter = 200
        spreading_hops = 3
        top_k_notes = 8
        max_hot_notes = 1200
        z3_timeout_ms = 2500
        max_cidr_rects = 256
        fca_max_concepts = 256
        eig_depth = 3
        max_hypotheses = 16
        causal_paths = 32
        causal_steps = 12
        analogy_candidates = 64
        analogy_beam = 16
        somatic_cap = 1000
        asp_horizon = 12
        ao_star_exp = 256
        fluent_history = 500
        schmitt_window = 5
        dst_focal_limit = 128
        dst_mc_samples = 1000
        cbr_max_cases = 1000
        cbr_top_k = 5
        cegar_loops = 8
        cegar_ast_depth = 48
        sygus_lines = 2500
        sygus_beam = 16
        mdp_sweeps = 80
        mdp_horizon = 8
        speculative_branches = 4
        continual_candidates = 8
        continual_window = 250
        meta_bins = 15
        meta_window = 500
        shapley_coalitions = 128
        ablation_max_entries = 250
        rl_episodes = 600
        rl_horizon = 6
        rl_sweeps = 32
        kmeans_n_init = 20
        kmeans_max_iter = 200
        pca_buffer_size = 1000
        shadow_max_files = 100
        raw_preserve_chars = 2500
        max_tool_chars = 3500
        max_history_chars = 24000
    elif total_ram_mib >= 12000 and cpu_threads >= 8:
        tier = "HIGH_PERFORMANCE"
        vsa_dim = 1024
        evo_generations = 200
        evo_beam_width = 24
        pagerank_max_iter = 150
        spreading_hops = 3
        top_k_notes = 6
        max_hot_notes = 600
        z3_timeout_ms = 1500
        max_cidr_rects = 128
        fca_max_concepts = 128
        eig_depth = 2
        max_hypotheses = 12
        causal_paths = 16
        causal_steps = 8
        analogy_candidates = 32
        analogy_beam = 12
        somatic_cap = 500
        asp_horizon = 8
        ao_star_exp = 128
        fluent_history = 250
        schmitt_window = 4
        dst_focal_limit = 64
        dst_mc_samples = 500
        cbr_max_cases = 500
        cbr_top_k = 4
        cegar_loops = 5
        cegar_ast_depth = 32
        sygus_lines = 1500
        sygus_beam = 12
        mdp_sweeps = 50
        mdp_horizon = 6
        speculative_branches = 3
        continual_candidates = 6
        continual_window = 120
        meta_bins = 10
        meta_window = 250
        shapley_coalitions = 64
        ablation_max_entries = 120
        rl_episodes = 400
        rl_horizon = 5
        rl_sweeps = 20
        kmeans_n_init = 12
        kmeans_max_iter = 150
        pca_buffer_size = 500
        shadow_max_files = 60
        raw_preserve_chars = 2500
        max_tool_chars = 3500
        max_history_chars = 24000
    else:
        tier = "PORTABLE_CONSERVATIVE"
        vsa_dim = 1024
        evo_generations = 100
        evo_beam_width = 12
        pagerank_max_iter = 100
        spreading_hops = 2
        top_k_notes = 4
        max_hot_notes = 300
        z3_timeout_ms = 800
        max_cidr_rects = 64
        fca_max_concepts = 64
        eig_depth = 2
        max_hypotheses = 8
        causal_paths = 8
        causal_steps = 5
        analogy_candidates = 16
        analogy_beam = 8
        somatic_cap = 250
        asp_horizon = 6
        ao_star_exp = 64
        fluent_history = 100
        schmitt_window = 3
        dst_focal_limit = 32
        dst_mc_samples = 200
        cbr_max_cases = 200
        cbr_top_k = 3
        cegar_loops = 3
        cegar_ast_depth = 24
        sygus_lines = 800
        sygus_beam = 8
        mdp_sweeps = 30
        mdp_horizon = 4
        speculative_branches = 2
        continual_candidates = 4
        continual_window = 60
        meta_bins = 10
        meta_window = 100
        shapley_coalitions = 32
        ablation_max_entries = 60
        rl_episodes = 200
        rl_horizon = 4
        rl_sweeps = 12
        kmeans_n_init = 8
        kmeans_max_iter = 100
        pca_buffer_size = 250
        shadow_max_files = 30
        raw_preserve_chars = 2000
        max_tool_chars = 3000
        max_history_chars = 16000

    clingo_threads = min(8, max(1, cpu_physical_cores // 2))
    layer2_workers = min(8, max(2, cpu_threads // 4))

    _cached_max_files = shadow_max_files
    profile = {
        "tier": tier,
        "hardware_tier": tier,
        "cpu_threads": cpu_threads,
        "cpu_physical_cores": cpu_physical_cores,
        "numa_nodes": numa_nodes,
        "total_ram_mib": total_ram_mib,
        "detected_gpu_vram_mib": detected_gpu_vram_mib,
        "gpu_count": gpu_count,
        "engines_configured": 15,
        # Engine 1: Associative Graph & PageRank
        "pagerank_max_iter": pagerank_max_iter,
        "spreading_activation_hops": spreading_hops,
        "top_k_activated_notes": top_k_notes,
        "max_hot_vault_notes": max_hot_notes,
        # Engine 2: Geometric Z3 & CIDR Polytope
        "z3_timeout_ms": z3_timeout_ms,
        "max_cidr_hyperrectangles": max_cidr_rects,
        # Engine 3: Formal Concept Analysis (FCA)
        "fca_max_concepts": fca_max_concepts,
        # Engine 4: Bayesian Abductive & Shannon EIG
        "eig_lookahead_depth": eig_depth,
        "max_abductive_hypotheses": max_hypotheses,
        # Engine 5: Pearl Structural Causal Models
        "causal_counterfactual_paths": causal_paths,
        "causal_sensitivity_steps": causal_steps,
        # Engine 6: VF2 Structural Analogy
        "analogy_vf2_max_candidates": analogy_candidates,
        "analogy_beam_width": analogy_beam,
        # Engine 7: Hyperdimensional VSA & Damasio Somatic Markers
        "vsa_hypervector_dim": vsa_dim,
        "somatic_memory_capacity": somatic_cap,
        # Engine 8: Clingo Non-Monotonic ASP & AO* Contingent Planner
        "asp_max_horizon_steps": asp_horizon,
        "ao_star_max_expansions": ao_star_exp,
        "clingo_parallel_threads": clingo_threads,
        # Engine 9: Event Calculus Temporal Fluents & Schmitt Trigger
        "fluent_event_history_limit": fluent_history,
        "schmitt_hysteresis_window": schmitt_window,
        # Engine 10: Dempster-Shafer Evidential Sensor Fusion
        "dst_focal_set_limit": dst_focal_limit,
        "dst_monte_carlo_samples": dst_mc_samples,
        # Engine 11: Case-Based Reasoning (CBR) Fingerprints
        "cbr_max_library_cases": cbr_max_cases,
        "cbr_top_k_retrievals": cbr_top_k,
        # Engine 12: CEGAR Pre-Execution Safety Verifier
        "cegar_max_refinement_loops": cegar_loops,
        "cegar_ast_depth_limit": cegar_ast_depth,
        # Engine 13: SyGuS Execution-Guided Output Extractor
        "sygus_max_parse_lines": sygus_lines,
        "sygus_synthesis_beam": sygus_beam,
        # Engine 14: Evolutionary MAP-Elites & Creative Leap
        "evolutionary_generations": evo_generations,
        "evolutionary_beam_width": evo_beam_width,
        # Engine 15: Hierarchical Tactical MDP & Optimal Stopping
        "mdp_bellman_sweeps": mdp_sweeps,
        "mdp_horizon_depth": mdp_horizon,
        "speculative_lookahead_branches": speculative_branches,
        # Engine 16: Continual Reasoning & Learning Loop Controller
        "continual_pass2_max_candidates": continual_candidates,
        "continual_audit_window": continual_window,
        # Engine 17: Multiplicative-Weights Hedge Meta-Arbiter
        "meta_calibration_bins": meta_bins,
        "meta_history_window": meta_window,
        # Engine 18: Counterfactual Shapley Command-Chain Ablation
        "shapley_max_coalitions": shapley_coalitions,
        "ablation_ledger_max_entries": ablation_max_entries,
        # Engine 19: Dual-Mode Pessimistic Q_LCB Trajectory RL & Network World-Model
        "rl_train_episodes": rl_episodes,
        "rl_rollout_horizon": rl_horizon,
        "rl_td_sweeps": rl_sweeps,
        # Engine 20: Spectral PCA, K-Means++ Clustering & Graph Laplacian
        "kmeans_n_init": kmeans_n_init,
        "kmeans_max_iter": kmeans_max_iter,
        "pca_history_buffer_size": pca_buffer_size,
        # Pipeline & Zero-Loss Context VM
        "layer2_parallel_workers": layer2_workers,
        "shadow_archive_max_files": shadow_max_files,
        "raw_preserve_threshold_chars": raw_preserve_chars,
        "max_tool_output_chars": max_tool_chars,
        "max_history_chars": max_history_chars,
        "gpu_vram_mb": 0,
    }
    try:
        _atomic_write_text(prof_path, json.dumps(profile, indent=2) + "\n")
    except Exception:
        pass
    _HW_LIMITS_RAM_CACHE = profile
    return profile


def _rotate_subdir_files(out_dir: Path, max_files: int) -> None:
    """FIFO file rotation for ephemeral snapshot subdirectories so disk usage stays bounded."""
    try:
        files = sorted(
            (f for f in out_dir.glob("*.json") if not f.name.startswith(".")),
            key=lambda p: p.stat().st_mtime,
        )
        if len(files) > max_files:
            for old_f in files[: len(files) - max_files]:
                try:
                    old_f.unlink(missing_ok=True)
                except Exception:
                    pass
    except Exception:
        pass


def save_json_data(subdir: str, name: str, payload: Dict[str, Any]) -> Path:
    ensure_directories()
    slug = slugify(name)
    out_dir = DATA_DIR / subdir if subdir else DATA_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{slug}.json"
    payload_with_meta = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **payload,
    }
    _atomic_write_text(path, json.dumps(payload_with_meta, indent=2) + "\n")
    if subdir in EPHEMERAL_ROTATED_SUBDIRS:
        _rotate_subdir_files(out_dir, max(30, _cached_max_files))
    return path


def load_json_data(subdir: str, name: str) -> Optional[Dict[str, Any]]:
    ensure_directories()
    slug = slugify(name)
    base = DATA_DIR / subdir if subdir else DATA_DIR
    candidates = [
        base / f"{slug}.json",
        base / name,
        base / f"{name}.json",
    ]
    for cand in candidates:
        if cand.is_file():
            try:
                return json.loads(cand.read_text(encoding="utf-8"))
            except Exception:
                return None
    return None


def list_json_data(subdir: str) -> List[Path]:
    ensure_directories()
    base = DATA_DIR / subdir if subdir else DATA_DIR
    if not base.is_dir():
        return []
    return sorted(base.glob("*.json"))


def update_vault_index(wiki_link: str, summary: str, tags: List[str]) -> None:
    ensure_directories()
    if not INDEX_FILE.exists():
        _atomic_write_text(
            INDEX_FILE,
            "# LLM Knowledge & Memory Index (`00_MEMORY_INDEX`)\n\n"
            "> **Tier-1 Hot Memory:** Automatically loaded into Qwen 3.8 / 3.5 on every session.\n\n"
            "## Indexed Vault Notes\n"
            "<!-- AUTO-INDEX-START -->\n"
            "<!-- AUTO-INDEX-END -->\n",
        )
    text = INDEX_FILE.read_text(encoding="utf-8", errors="replace")
    tag_str = " ".join(f"#{t.lstrip('#')}" for t in tags if str(t).strip())
    entry_line = f"- [[{wiki_link}]] — {summary.strip()}" + (f" ({tag_str})" if tag_str else "")

    start_marker = "<!-- AUTO-INDEX-START -->"
    end_marker = "<!-- AUTO-INDEX-END -->"
    if start_marker in text and end_marker in text:
        before, rest = text.split(start_marker, 1)
        middle, after = rest.split(end_marker, 1)
        lines = [ln for ln in middle.strip().splitlines() if ln.strip()]
        updated = False
        for idx, ln in enumerate(lines):
            if f"[[{wiki_link}]]" in ln:
                lines[idx] = entry_line
                updated = True
                break
        if not updated:
            lines.append(entry_line)
        lines = lines[-35:]
        new_text = f"{before}{start_marker}\n" + "\n".join(lines) + f"\n{end_marker}{after}"
    else:
        new_text = text.rstrip() + f"\n\n## Indexed Vault Notes\n{start_marker}\n{entry_line}\n{end_marker}\n"

    _atomic_write_text(INDEX_FILE, new_text)


def _rotate_reasoning_vault_notes(max_hot_notes: int = 60) -> int:
    """
    Episodic Vault Compaction (Improvement #6):
    Preserves 100% of `commands/`, `targets/`, `projects/`, `knowledge/`, `SuggestedImprovements/`,
    and canonical engine playbooks (`rl_network_policy_playbooks.md`, `spectral_pca_kmeans_manifold.md`),
    while archiving older auto-generated `ObsidianVault/reasoning/pipeline15_*` episodic session notes
    beyond `max_hot_notes` into `ObsidianVault/archive/reasoning/` so the hot Bipartite Vault Graph stays fast.
    """
    reasoning_dir = VAULT_DIR / "reasoning"
    if not reasoning_dir.is_dir():
        return 0
    protected_stems = {
        "rl_network_policy_playbooks",
        "spectral_pca_kmeans_manifold",
        "meta_learning_audit",
    }
    try:
        session_files = sorted(
            (
                f
                for f in reasoning_dir.glob("*.md")
                if not f.name.startswith(".") and f.stem not in protected_stems
            ),
            key=lambda p: p.stat().st_mtime,
        )
        if len(session_files) <= max_hot_notes:
            return 0
        archive_dir = VAULT_DIR / "archive" / "reasoning"
        archive_dir.mkdir(parents=True, exist_ok=True)
        moved = 0
        for old_f in session_files[: len(session_files) - max_hot_notes]:
            try:
                shutil.move(str(old_f), str(archive_dir / old_f.name))
                moved += 1
            except Exception:
                pass
        return moved
    except Exception:
        return 0


def save_reasoning_to_vault(
    title: str,
    summary: str,
    markdown_body: str,
    engine_type: str,
    tags: Optional[List[str]] = None,
    persist_long_term: bool = False,
) -> str:
    """
    Save a Markdown reasoning report.
    - Canonical universal playbooks (`rl_network_policy_playbooks`, `spectral_pca_kmeans_manifold`, `meta_learning_audit`)
      or explicit `persist_long_term=True` reports are saved to `ObsidianVault/reasoning/<slug>.md` and indexed in `00_MEMORY_INDEX.md`.
    - Session/project-specific diagnostic runs (e.g. `pipeline15_*`, target-specific probes) are isolated inside
      `Projects/<active_project>/reasoning/<slug>.md` and indexed in `Projects/<active_project>/memory.md` so internal/test
      network data never pollutes the long-term `ObsidianVault/`.
    """
    ensure_directories()
    slug = slugify(title)
    canonical_long_term_stems = {
        "rl_network_policy_playbooks",
        "spectral_pca_kmeans_manifold",
        "meta_learning_audit",
    }
    is_long_term = persist_long_term or (slug in canonical_long_term_stems)

    all_tags = ["reasoning", engine_type.lower()] + (tags or [])
    clean_tags = []
    for t in all_tags:
        ct = re.sub(r"[^a-zA-Z0-9_\-]", "", str(t).lstrip("#")).lower()
        if ct and ct not in clean_tags:
            clean_tags.append(ct)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    frontmatter = (
        "---\n"
        f"title: {title}\n"
        "category: reasoning\n"
        f"engine: {engine_type}\n"
        f"summary: {summary}\n"
        f"tags: [{', '.join(clean_tags)}]\n"
        f"updated: {now_str}\n"
        "---\n"
    )
    backlink_ref = "[[00_MEMORY_INDEX]]" if is_long_term else "[[memory]]"
    body = (
        f"# {title}\n\n"
        f"> **Engine:** `{engine_type}` | **Summary:** {summary}  \n"
        f"> **Backlink:** {backlink_ref} | **Updated:** `{now_str}`\n\n"
        f"{markdown_body.strip()}\n"
    )
    if is_long_term:
        note_path = VAULT_DIR / "reasoning" / f"{slug}.md"
        _atomic_write_text(note_path, frontmatter + body)
        _rotate_reasoning_vault_notes(max_hot_notes=60)
        wiki_link = f"reasoning/{slug}"
        update_vault_index(wiki_link, summary, clean_tags)
    else:
        proj_dir = get_active_project_dir()
        note_path = proj_dir / "reasoning" / f"{slug}.md"
        _atomic_write_text(note_path, frontmatter + body)
        wiki_link = f"Projects/{proj_dir.name}/reasoning/{slug}"
        update_project_memory_index(proj_dir, f"reasoning/{slug}", summary, clean_tags)
    home_s = str(Path.home())
    disp_path = ("~" + str(note_path)[len(home_s):]) if (home_s and str(note_path).startswith(home_s)) else str(note_path)
    return f"[[{wiki_link}]] ({disp_path})"


def load_json_state(filepath: str, default: Any = None) -> Any:
    """Convenience loader for direct file path JSON state with mtime-checked RAM cache."""
    import copy

    ensure_directories()
    key = str(filepath)
    p = Path(key)
    if p.is_file():
        try:
            mtime = p.stat().st_mtime
            cached = _JSON_STATE_RAM_CACHE.get(key)
            if cached is not None and cached[0] == mtime:
                return copy.deepcopy(cached[1])
            data = json.loads(p.read_text(encoding="utf-8"))
            _JSON_STATE_RAM_CACHE[key] = (mtime, copy.deepcopy(data))
            return data
        except Exception:
            pass
    return default if default is not None else {}


def save_json_state(filepath: str, data: Any) -> None:
    """Convenience saver for direct file path JSON state."""
    ensure_directories()
    key = str(filepath)
    p = Path(key)
    _atomic_write_text(p, json.dumps(data, indent=2) + "\n")
    try:
        _JSON_STATE_RAM_CACHE[key] = (p.stat().st_mtime, data)
    except Exception:
        _JSON_STATE_RAM_CACHE.pop(key, None)


def write_reasoning_note(
    title: str,
    engine: str,
    content_md: str,
    tags: Optional[List[str]] = None,
) -> str:
    """Alias wrapper around `save_reasoning_to_vault` for Engines 9-14."""
    return save_reasoning_to_vault(
        title=title,
        summary=f"{engine}: {title}",
        markdown_body=content_md,
        engine_type=engine,
        tags=tags,
    )


def scan_vault_notes() -> List[Dict[str, str]]:
    """Returns a list of markdown notes in `ObsidianVault/` for Context VM Bipartite Page-In."""
    ensure_directories()
    notes: List[Dict[str, str]] = []
    if not VAULT_DIR.is_dir():
        return notes
    for md_file in sorted(VAULT_DIR.rglob("*.md")):
        if md_file.name.startswith(".") or "archive" in md_file.parts:
            continue
        rel = str(md_file.relative_to(VAULT_DIR))
        notes.append({"title": md_file.stem, "rel_path": rel, "abs_path": str(md_file)})
    return notes


_HOST_NET_CACHE: Optional[Dict[str, Any]] = None
_HOST_NET_CACHE_TS: float = 0.0
_IPV4_FULL_RE = re.compile(
    r"\b((?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})(?:/([1-9]|[12]\d|3[0-2]))?\b"
)


def _netmask_to_prefixlen(mask: str) -> int:
    try:
        import ipaddress

        return ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False).prefixlen
    except Exception:
        return 24


def _parse_iface_tokens(raw_if: str) -> List[str]:
    s = (raw_if or "").strip().strip("\"'")
    if not s:
        return []
    if "," in s:
        parts = [x.strip() for x in s.split(",")]
    elif re.search(r"\b(?:vEthernet|Adapter|Connection|Loopback)\b", s, re.I):
        parts = [s]
    else:
        parts = [x.strip() for x in s.split()]
    return [p for p in parts if p and p.lower() != "lo"]


def _get_isolation_filter() -> Tuple[str, List[str]]:
    """Return `(isolation_level, allowed_interfaces)` for RED / WHITE / BLUE network isolation."""
    if os.environ.get("CORA_PERSONALITY_MODE", "").strip().upper() == "ANALYST":
        return "white", ["lo"]
    mode_raw = os.environ.get("LLM_ISOLATION_MODE", "").strip()
    override_raw = os.environ.get("LLM_POSTURE_OVERRIDE", "").strip()
    eff_raw = override_raw or mode_raw
    eff = eff_raw.lower()
    if eff in ("white", "airgap", "air-gap", "netns", "namespace", "air_gapped_netns", "llm-isolated", "green"):
        return "white", ["lo"]
    if eff in ("blue", "lan_usb", "lan", "isolated_lan_usb", "group", "llm-local", "restricted") or eff.startswith(("blue:", "blue=")):
        raw_if = os.environ.get("LLM_ALLOWED_IFACES", "").strip()
        if not raw_if and eff.startswith(("blue:", "blue=")):
            raw_if = eff_raw.split(":", 1)[1] if ":" in eff_raw else eff_raw.split("=", 1)[1]
        if not raw_if:
            try:
                from Network_Isolation.console_posture import load_network_isolation_config

                cfg = load_network_isolation_config()
                return "blue", list(cfg.get("blue_allowed_ifaces") or ["eth0", "eth1"])
            except Exception:
                return "blue", ["eth0", "eth1"]
        parsed = _parse_iface_tokens(raw_if)
        if os.name == "nt" and parsed == ["eth0", "eth1"]:
            try:
                from Network_Isolation.console_posture import _get_windows_active_interfaces

                win_ifaces = _get_windows_active_interfaces()
                if win_ifaces and not any(i.lower() in ("eth0", "eth1") for i in win_ifaces):
                    preferred = [i for i in win_ifaces if not i.lower().startswith("vethernet")]
                    return "blue", (preferred[:2] if preferred else win_ifaces[:2])
            except Exception:
                pass
        return "blue", (parsed or ["eth0", "eth1"])
    return "red", []


def detect_host_network_context(force_refresh: bool = False) -> Dict[str, Any]:
    """
    Cross-platform (Linux & Windows) live host network & serial device discovery.
    Honors RED (unrestricted), WHITE (namespace lo-only), and BLUE (interface-locked) isolation.
    Never uses hardcoded profile IPs. Cached for 30 seconds for < 1 ms latency.
    """
    global _HOST_NET_CACHE, _HOST_NET_CACHE_TS
    import ipaddress
    import time

    iso_level, blue_ifaces = _get_isolation_filter()
    cache_sig = f"{iso_level}:{','.join(blue_ifaces)}"
    now = time.monotonic()
    if (
        not force_refresh
        and _HOST_NET_CACHE is not None
        and _HOST_NET_CACHE.get("_iso_sig") == cache_sig
        and (now - _HOST_NET_CACHE_TS) < 30.0
    ):
        return dict(_HOST_NET_CACHE)

    os_family = "windows" if os.name == "nt" or platform.system().lower() == "windows" else "linux"
    local_subnets: List[str] = []
    local_ips: List[str] = []
    interfaces: List[str] = []
    serial_ports: List[str] = []

    if os_family == "linux":
        if iso_level != "white":
            try:
                proc = subprocess.run(
                    ["ip", "-o", "-4", "addr", "show"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=1.5,
                    check=False,
                )
                if proc.returncode == 0 and proc.stdout:
                    for ln in proc.stdout.splitlines():
                        parts = ln.split()
                        if len(parts) >= 4:
                            iface = parts[1].split("@")[0]
                            if iface == "lo":
                                continue
                            if iso_level == "blue" and blue_ifaces and iface not in blue_ifaces:
                                continue
                            if iface not in interfaces:
                                interfaces.append(iface)
                            for tok in parts[2:]:
                                if "/" in tok and re.match(r"^\d+\.\d+\.\d+\.\d+/\d+$", tok):
                                    ip_str = tok.split("/")[0]
                                    if not ip_str.startswith("127."):
                                        if ip_str not in local_ips:
                                            local_ips.append(ip_str)
                                        try:
                                            net_str = str(ipaddress.ip_network(tok, strict=False))
                                            if net_str not in local_subnets:
                                                local_subnets.append(net_str)
                                        except Exception:
                                            pass
            except Exception:
                pass
            if iso_level == "blue" and blue_ifaces:
                for bi in blue_ifaces:
                    if bi not in interfaces:
                        interfaces.append(bi)
        else:
            interfaces = ["lo"]
        for pattern in ("/dev/ttyUSB*", "/dev/ttyACM*"):
            for p in sorted(Path("/dev").glob(pattern.replace("/dev/", ""))):
                sp = str(p)
                if sp not in serial_ports:
                    serial_ports.append(sp)
    else:
        # Windows native discovery via ipconfig (respecting WHITE / BLUE isolation)
        if iso_level == "white":
            interfaces = ["lo"]
        else:
            try:
                proc = subprocess.run(
                    ["ipconfig"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=2.0,
                    check=False,
                )
                if proc.returncode == 0 and proc.stdout:
                    cur_ip = ""
                    cur_adapter = ""
                    blue_low = {b.lower() for b in blue_ifaces}

                    def _win_adapter_allowed(name: str) -> bool:
                        if iso_level != "blue" or not blue_low:
                            return True
                        nl = name.lower()
                        if nl in blue_low:
                            return True
                        return any(len(b) >= 3 and (b in nl or nl in b) for b in blue_low)

                    for ln in proc.stdout.splitlines():
                        s = ln.strip()
                        if s.endswith(":") and "adapter" in s.lower():
                            cur_adapter = re.sub(r"(?i)^.*adapter\s+", "", s[:-1]).strip()
                            if cur_adapter and _win_adapter_allowed(cur_adapter):
                                if cur_adapter not in interfaces:
                                    interfaces.append(cur_adapter)
                        elif "IPv4 Address" in s or "IP Address" in s:
                            if cur_adapter and not _win_adapter_allowed(cur_adapter):
                                cur_ip = ""
                                continue
                            m = re.search(r"(\d+\.\d+\.\d+\.\d+)", s)
                            if m and not m.group(1).startswith("127."):
                                cur_ip = m.group(1)
                                if cur_ip not in local_ips:
                                    local_ips.append(cur_ip)
                        elif "Subnet Mask" in s and cur_ip:
                            m = re.search(r"(\d+\.\d+\.\d+\.\d+)", s)
                            plen = _netmask_to_prefixlen(m.group(1)) if m else 24
                            try:
                                net_str = str(ipaddress.ip_network(f"{cur_ip}/{plen}", strict=False))
                                if net_str not in local_subnets:
                                    local_subnets.append(net_str)
                            except Exception:
                                pass
                            cur_ip = ""
            except Exception:
                pass
            if iso_level == "blue" and blue_ifaces:
                for bi in blue_ifaces:
                    if bi not in interfaces:
                        interfaces.append(bi)
            try:
                proc_com = subprocess.run(
                    ["reg", "query", r"HKLM\HARDWARE\DEVICEMAP\SERIALCOMM"],
                    capture_output=True,
                    text=True,
                    timeout=1.5,
                    check=False,
                )
                if proc_com.returncode == 0 and proc_com.stdout:
                    for cm in re.findall(r"\bCOM\d+\b", proc_com.stdout, flags=re.I):
                        cm_up = cm.upper()
                        if cm_up not in serial_ports:
                            serial_ports.append(cm_up)
            except Exception:
                pass

    _HOST_NET_CACHE = {
        "_iso_sig": cache_sig,
        "isolation_level": iso_level,
        "allowed_interfaces": blue_ifaces if iso_level == "blue" else (["lo"] if iso_level == "white" else interfaces),
        "os_family": os_family,
        "local_subnets": local_subnets,
        "local_ips": local_ips,
        "interfaces": interfaces,
        "primary_interface": interfaces[0] if interfaces else ("Ethernet" if os_family == "windows" else "eth0"),
        "serial_ports": serial_ports,
        "primary_serial": serial_ports[0] if serial_ports else ("COM1" if os_family == "windows" else "/dev/ttyUSB0"),
    }
    _HOST_NET_CACHE_TS = now
    return dict(_HOST_NET_CACHE)


def resolve_problem_targets(
    problem_text: str = "",
    target_ip: str = "",
    secondary_ip: str = "",
    local_subnets: Optional[List[str]] = None,
    *,
    problem: str = "",
    explicit_target: str = "",
    explicit_secondary: str = "",
    secondary_target_ip: str = "",
    explicit_local_subnets: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Dynamically resolves target IPs, secondary/remote hosts, CIDR subnets, interfaces, and
    OS family from explicit arguments, problem text, and active holding fluents.
    NEVER injects hardcoded profile IPs; uses symbolic placeholders (`<TARGET_IP>`,
    `<REMOTE_HOST>`, `<REMOTE_SUBNET>`) when no concrete IP is present in the user's context.
    """
    import ipaddress

    problem_text = problem_text or problem or ""
    target_ip = target_ip or explicit_target or ""
    secondary_ip = secondary_ip or explicit_secondary or secondary_target_ip or ""
    local_subnets = local_subnets or explicit_local_subnets

    host_ctx = detect_host_network_context()
    os_family = host_ctx["os_family"]
    prob_low = (problem_text or "").lower()
    if any(
        w in prob_low
        for w in (
            "powershell",
            "get-net",
            "test-netconnection",
            "ipconfig",
            "netsh",
            "cmd.exe",
            "c:\\",
            "active directory",
            "impacket",
            "wmic",
            "tasklist",
            "reg query",
            "winrm",
        )
    ):
        target_os = "windows"
    elif any(
        w in prob_low
        for w in (
            "/dev/tty",
            "ip route",
            "ip addr",
            "ip neigh",
            "iptables",
            "nft",
            "systemctl",
            "tio ",
            "ss -",
            "linux",
            "eth0",
            "wlan0",
            "sudo ",
            "curl ",
        )
    ):
        target_os = "linux"
    else:
        target_os = os_family

    discovered_ips: List[str] = []
    discovered_subnets: List[str] = []
    local_iface_ips_in_prompt: set[str] = set()
    explicit_target_ips_in_prompt: List[str] = []
    via_gateway_ips_in_prompt: List[str] = []
    dest_ips_in_prompt: List[str] = []

    def _collect_from_text(txt: str, is_problem_body: bool = False) -> None:
        if not txt:
            return
        for m in _IPV4_FULL_RE.finditer(txt):
            ip_val, prefix_val = m.group(1), m.group(2)
            if ip_val in ("0.0.0.0", "127.0.0.1", "255.255.255.255", "255.255.255.0", "255.255.0.0"):
                continue
            before_ctx = txt[max(0, m.start() - 55) : m.start()].lower() if is_problem_body else ""
            is_local_iface_decl = bool(
                is_problem_body
                and (
                    (
                        prefix_val
                        and re.search(r"\b(?:local\s+interface|eth\d+|wlan\d+|enp\d+s\d+|ens\d+|local\s+ip)\b", before_ctx)
                    )
                    or re.search(r"\b(?:from|source|src|management\s+ip|local\s+ip)\b[^,.;]*$", before_ctx)
                )
            )
            is_via_gw_decl = bool(
                is_problem_body
                and not prefix_val
                and re.search(r"\b(?:via|gateway|next[\s\-]?hop|router)\b[^,.;]*$", before_ctx)
            )
            is_dest_decl = bool(
                is_problem_body
                and not prefix_val
                and not is_via_gw_decl
                and re.search(r"\b(?:to|towards|destination)\b[^,.;]*$", before_ctx)
            )
            is_explicit_target_decl = bool(
                is_problem_body
                and not prefix_val
                and (
                    is_via_gw_decl
                    or is_dest_decl
                    or re.search(
                        r"(?:\b(?:target|host|destination|device|gateway|router|server|endpoint|to|at|via|towards|reach)\b[\s:a-z0-9_\-]*$|https?://\s*$)",
                        before_ctx,
                    )
                )
            )
            if is_local_iface_decl:
                local_iface_ips_in_prompt.add(ip_val)
            else:
                if is_via_gw_decl and ip_val not in via_gateway_ips_in_prompt:
                    via_gateway_ips_in_prompt.append(ip_val)
                if is_dest_decl and ip_val not in dest_ips_in_prompt:
                    dest_ips_in_prompt.append(ip_val)
                if is_explicit_target_decl and ip_val not in explicit_target_ips_in_prompt:
                    explicit_target_ips_in_prompt.append(ip_val)
            if prefix_val:
                try:
                    net_obj = ipaddress.ip_network(f"{ip_val}/{prefix_val}", strict=False)
                    net_s = str(net_obj)
                    if net_s not in discovered_subnets:
                        discovered_subnets.append(net_s)
                    # If the IP itself is a host address (not network address), also record it as a host IP
                    if str(net_obj.network_address) != ip_val and ip_val not in discovered_ips:
                        discovered_ips.append(ip_val)
                except Exception:
                    pass
            else:
                if ip_val not in discovered_ips:
                    discovered_ips.append(ip_val)

    _collect_from_text(target_ip)
    _collect_from_text(secondary_ip)
    _collect_from_text(problem_text, is_problem_body=True)
    had_explicit_or_prompt_ips = len(discovered_ips) >= 2 or bool((secondary_ip or "").strip())

    # If no explicit IP was in the prompt, check Active Project memory.md and relentless_ledger.json first
    if not discovered_ips:
        active_proj = os.environ.get("CORA_ACTIVE_PROJECT", "").strip()
        ledger_file = DATA_DIR / "sessions" / "relentless_ledger.json"
        if ledger_file.is_file():
            try:
                ldata = json.loads(ledger_file.read_text(encoding="utf-8"))
                if not active_proj:
                    active_proj = str(ldata.get("active_project") or "").strip()
                _collect_from_text(str(ldata.get("active_goal") or ""))
                for att in reversed(ldata.get("attempts") or []):
                    _collect_from_text(str(att.get("target_or_cmd") or ""))
            except Exception:
                pass
        if active_proj:
            proj_mem = PROJECTS_DIR / active_proj / "memory.md"
            if proj_mem.is_file():
                try:
                    _collect_from_text(proj_mem.read_text(encoding="utf-8", errors="replace")[:4000])
                except Exception:
                    pass

    # Next inspect active holding fluents in live_fluents.json sorted by most recent turn first
    if not discovered_ips:
        fluent_file = DATA_DIR / "temporal_fluents" / "live_fluents.json"
        if fluent_file.is_file():
            try:
                fdata = json.loads(fluent_file.read_text(encoding="utf-8"))
                fluent_items = [
                    (fk, fv)
                    for fk, fv in (fdata.get("fluents") or {}).items()
                    if isinstance(fv, dict) and fv.get("status") in ("ACTIVE", "HOLDING")
                ]
                fluent_items.sort(key=lambda kv: -int(kv[1].get("updated_turn", 0)))
                for fk, fv in fluent_items:
                    _collect_from_text(f"{fk} {fv.get('fluent', '')}")
            except Exception:
                pass

    eff_local_subnets = list(local_subnets) if local_subnets else list(host_ctx["local_subnets"])
    # Do not strip an IP as "self" if the prompt explicitly designated it as a target/destination/gateway
    # (e.g. dual-homed / cross-NIC transit test from eth0 to eth1 via external appliance)
    host_local_ips = (set(host_ctx["local_ips"]) - set(explicit_target_ips_in_prompt)) | local_iface_ips_in_prompt
    non_self_ips = [ip for ip in discovered_ips if ip not in host_local_ips] or discovered_ips
    if explicit_target_ips_in_prompt:
        # When both a `via <GW_IP>` and `to <DST_IP>` are specified in the prompt, place the next-hop gateway first
        # (`primary`/`target_ip`) and the destination behind it second (`secondary_ip`/`secondary_target_ip`)
        if via_gateway_ips_in_prompt and dest_ips_in_prompt:
            ordered_explicit = list(via_gateway_ips_in_prompt) + [
                ip for ip in dest_ips_in_prompt if ip not in via_gateway_ips_in_prompt
            ] + [
                ip for ip in explicit_target_ips_in_prompt
                if ip not in via_gateway_ips_in_prompt and ip not in dest_ips_in_prompt
            ]
        else:
            ordered_explicit = explicit_target_ips_in_prompt
        prioritized = [ip for ip in ordered_explicit if ip in non_self_ips]
        non_self_ips = prioritized + [ip for ip in non_self_ips if ip not in prioritized]
    # Deprioritize RFC 5737 test/documentation IPs (198.51.100.x, 203.0.113.x, 192.0.2.x) if real target IPs exist
    real_target_ips = [
        ip for ip in non_self_ips if not ip.startswith(("198.51.100.", "203.0.113.", "192.0.2."))
    ]
    if real_target_ips and not any(
        d in (problem_text or "") for d in ("198.51.100.", "203.0.113.", "192.0.2.")
    ):
        non_self_ips = real_target_ips + [ip for ip in non_self_ips if ip not in real_target_ips]

    primary = (target_ip or "").strip()
    if not primary or not _IPV4_FULL_RE.search(primary):
        primary = non_self_ips[0] if non_self_ips else "<TARGET_IP>"
    else:
        primary = _IPV4_FULL_RE.search(primary).group(1)  # type: ignore[union-attr]

    secondary = (secondary_ip or "").strip()
    if not secondary or not _IPV4_FULL_RE.search(secondary):
        if had_explicit_or_prompt_ips:
            rem_candidates = [ip for ip in non_self_ips if ip != primary]
            secondary = rem_candidates[0] if rem_candidates else "<REMOTE_HOST>"
        else:
            secondary = "<REMOTE_HOST>"
    else:
        secondary = _IPV4_FULL_RE.search(secondary).group(1)  # type: ignore[union-attr]

    non_local_subnets = [s for s in discovered_subnets if s not in eff_local_subnets]
    if non_local_subnets:
        remote_subnet = non_local_subnets[0]
    elif secondary != "<REMOTE_HOST>":
        try:
            remote_subnet = str(ipaddress.ip_network(f"{secondary}/24", strict=False))
        except Exception:
            remote_subnet = "<REMOTE_SUBNET>"
    elif primary != "<TARGET_IP>":
        try:
            cand_net = str(ipaddress.ip_network(f"{primary}/24", strict=False))
            remote_subnet = cand_net if cand_net not in eff_local_subnets else "<REMOTE_SUBNET>"
        except Exception:
            remote_subnet = "<REMOTE_SUBNET>"
    else:
        remote_subnet = "<REMOTE_SUBNET>"

    local_subnet_str = eff_local_subnets[0] if eff_local_subnets else "<LOCAL_SUBNET>"
    serial_match = re.search(r"(/dev/tty(?:USB|ACM|S)\d+|\bCOM\d+\b)", problem_text or "", re.I)
    serial_port = serial_match.group(1) if serial_match else host_ctx["primary_serial"]
    explicit_serial_intent = bool(
        serial_match
        or re.search(
            r"\b(?:ttyusb\d*|ttyacm\d*|serial|tio|uart|oob|out-of-band|baud|console)\b|exit 7|connection refused",
            prob_low,
        )
    )
    non_serial_domain_intent = bool(
        any(
            k in prob_low
            for k in (
                "mtls", "client.crt", "https://", "http://", "injection", "endpoint", "rest api",
                "graphql", "cookie", "jwt", "network is unreachable", "no route to host",
                "cross-subnet", "active directory", "ldap", "smb", "suid", "sudoers", "capabilities",
                "privesc", "privilege escalation", "www-data",
            )
        )
        and not explicit_serial_intent
    )
    has_serial = bool(explicit_serial_intent or (host_ctx["serial_ports"] and not non_serial_domain_intent))

    return {
        "os_family": os_family,
        "target_os": target_os,
        "primary_ip": primary,
        "target_ip": primary,
        "secondary_ip": secondary,
        "secondary_target_ip": secondary if secondary != "<REMOTE_HOST>" else "",
        "gateway_ip": primary if primary != "<TARGET_IP>" else "<GATEWAY_IP>",
        "remote_subnet": remote_subnet,
        "local_subnets": eff_local_subnets,
        "local_subnet": local_subnet_str,
        "discovered_ips": non_self_ips,
        "discovered_subnets": discovered_subnets,
        "primary_interface": host_ctx["primary_interface"],
        "serial_port": serial_port,
        "serial_device": serial_port,
        "has_serial_oob": has_serial,
        "has_concrete_primary_ip": primary != "<TARGET_IP>",
        "has_concrete_secondary_ip": secondary != "<REMOTE_HOST>",
    }


def render_command_template(template: str, ctx: Optional[Dict[str, Any]] = None) -> str:
    """Substitute dynamic runtime target/network placeholders into an engine command template."""
    if not template:
        return ""
    c = ctx or resolve_problem_targets()
    sec_ip = str(c.get("secondary_ip") if c.get("secondary_ip") not in ("", None) else "<REMOTE_HOST>")
    prim_ip = str(c.get("primary_ip") or c.get("target_ip") or "<TARGET_IP>")
    rem_ip = sec_ip if sec_ip != "<REMOTE_HOST>" else prim_ip
    gw_ip = str(c.get("gateway_ip", "<GATEWAY_IP>"))
    rem_sub = str(c.get("remote_subnet", "<REMOTE_SUBNET>"))
    loc_sub = str(c.get("local_subnet", "<LOCAL_SUBNET>"))
    iface = str(c.get("primary_interface", "eth0"))
    ser = str(c.get("serial_device") or c.get("serial_port") or "/dev/ttyUSB0")
    replacements = {
        "{target_ip}": prim_ip,
        "{target}": prim_ip,
        "{primary_ip}": prim_ip,
        "{secondary_ip}": sec_ip,
        "{secondary_target_ip}": rem_ip,
        "{remote_ip}": rem_ip,
        "{gateway_ip}": gw_ip,
        "{remote_subnet}": rem_sub,
        "{local_subnet}": loc_sub,
        "{iface}": iface,
        "{serial_port}": ser,
        "{serial_device}": ser,
        "<TARGET_IP>": prim_ip,
        "<target_ip>": prim_ip,
        "<target>": prim_ip,
        "<PRIMARY_IP>": prim_ip,
        "<REMOTE_HOST>": rem_ip,
        "<SECONDARY_IP>": sec_ip,
        "<GATEWAY_IP>": gw_ip,
        "<REMOTE_SUBNET>": rem_sub,
        "<LOCAL_SUBNET>": loc_sub,
        "<IFACE>": iface,
        "<SERIAL_PORT>": ser,
    }
    out = template
    for k, v in replacements.items():
        out = out.replace(k, v)
    if os.name == "nt" and "tio " not in out and "/dev/tty" not in out:
        out = out.replace("ip -4 -br addr show; ip route show; ip neigh show", "ipconfig /all & route print -4 & arp -a")
        out = out.replace("ss -tulpn; ip -d link show", "netstat -ano & ipconfig /all")
        out = re.sub(r"\bip\s+neigh\s+show\b", "arp -a", out)
        out = re.sub(r"\bip\s+route\s+get\s+(\S+)\s*;\s*", "", out)
        out = re.sub(r"\bping\s+-c\s+(\d+)\s+-W\s+\d+\b", r"ping -n \1 -w 1200", out)
        out = re.sub(r"\bping\s+-c\s+(\d+)\b", r"ping -n \1", out)
    return out
