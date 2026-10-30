export interface SessionMode {
  number: string;
  key: 'default' | 'analyst' | 'berserker' | 'ninja';
  label: string;
  badge: string;
  allowed_isolation: string[];
  forced_isolation: string | null;
  default_permission: 'confirm' | 'auto';
  read_only: boolean;
  summary: string;
  system_directive: string;
}

export interface PostureInfo {
  mode: string;
  color_level: 'RED' | 'BLUE' | 'WHITE';
  short_tag: string;
  hud_badge: string;
  banner_badge: string;
  description: string;
  bg_hex: string;
  fg_hex: string;
  cursor_hex: string;
  window_title: string;
  active_interfaces: string[];
  allowed_interfaces?: string[];
  effective_group: string;
  netns: string;
  detected_by: string;
}

export interface ProjectItem {
  menu_number: number;
  slug: string;
  path: string;
  files_dir?: string;
  custom_files_count?: number;
  has_report: boolean;
  last_goal: string;
  tasks_completed: number;
  tasks_pending: number;
  file_count: number;
  updated_at: string;
}

export interface WorkspaceFile {
  name: string;
  rel_path: string;
  project_rel?: string;
  category: string;
  ext: string;
  size_bytes: number;
  modified_at: string;
}

export interface ProjectFilesPayload {
  project_slug: string;
  files_dir: string;
  files_dir_rel: string;
  files_dir_items: WorkspaceFile[];
  project_files: WorkspaceFile[];
  system_scripts: WorkspaceFile[];
}

export interface ModelItem {
  id: string;
  name: string;
  filename: string;
  provider: 'llama-server' | 'ollama';
  role: string;
  vram_est: string;
  installed_on_disk: boolean;
  size_gb?: number;
}

export interface GpuMetric {
  index: number;
  name: string;
  utilization_pct: number;
  vram_used_mb: number;
  vram_total_mb: number;
  vram_pct: number;
  temperature_c: number;
  power_w: number;
  power_limit_w: number;
  fan_speed_pct: number;
  source: string;
}

export interface HardwareMetrics {
  timestamp: string;
  os: string;
  cpu: {
    utilization_pct: number;
    per_core_pct: number[];
    cores_physical: number;
    cores_logical: number;
    frequency_mhz: number;
    temperature_c: number | null;
  };
  ram: {
    used_gb: number;
    total_gb: number;
    utilization_pct: number;
    swap_pct: number;
  };
  disk: {
    mount: string;
    used_gb: number;
    total_gb: number;
    utilization_pct: number;
    read_mb_s: number;
    write_mb_s: number;
  };
  network: {
    tx_kb_s: number;
    rx_kb_s: number;
    total_sent_mb: number;
    total_recv_mb: number;
    interfaces: Array<{
      name: string;
      ipv4: string[];
      ip_cidr?: string[];
      primary_ip_cidr?: string;
      tx_kb_s?: number;
      rx_kb_s?: number;
      speed_mbps: number;
      is_loopback?: boolean;
      is_virtual?: boolean;
    }>;
  };
  gpus: GpuMetric[];
  cora_hw_tier?: Record<string, unknown>;
}

export interface CompactReasoning {
  pipeline_latency_ms?: number;
  consensus_immediate_action?: string;
  cegar_verification?: {
    blocked?: boolean;
    counterexample_reason?: string;
    auto_repaired_command?: string;
  };
  bayesian_top?: {
    cause?: string;
    posterior?: number;
  };
  dempster_shafer?: {
    top_hypothesis?: string;
    top_belief?: number;
    top_plausibility?: number;
    conflict_mass_K?: number;
  };
  mdp_policy?: {
    recommended_tactic_category?: string;
    recommended_tool?: string;
    bellman_q_star?: number;
    optimal_stopping_decision?: string;
  };
  rl_network_policy?: {
    stage?: string;
    immediate_action?: string;
    immediate_q_value?: number;
  };
  spectral_pca_kmeans?: {
    assigned_cluster_label?: string;
    silhouette_score?: number;
    cumulative_top3_variance_pct?: number;
  };
  vsa_top?: {
    archetype?: string;
    cosine_similarity?: number;
    somatic_valence?: number;
  };
  meta_calibration?: {
    rolling_brier_score?: number;
    expected_calibration_error_pct?: number;
  };
  vault_note_saved?: string;
}

export interface ChatMessage {
  id?: number;
  conversation_id: string;
  project_slug: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  thinking?: string;
  command_executed?: string;
  command_output?: string;
  reasoning?: CompactReasoning;
  posture_level: string;
  mode_key: string;
  model_used: string;
  latency_ms: number;
  created_at: string;
}

export interface SystemToolItem {
  id: string;
  name: string;
  binary: string;
  os: 'windows' | 'linux';
  team: 'red' | 'blue' | 'hunt';
  team_label: string;
  focus_area: string;
  source_type: string;
  description: string;
  example_command: string;
  safe_demo_command: string;
  live_smb_path: string;
  live_smb_example: string;
  download_url: string;
  installed: boolean;
  installed_path: string;
  status: string;
  status_label: string;
  resolved_command: string;
  resolved_safe_command: string;
}

export interface SystemToolsInventory {
  host_os: 'windows' | 'linux';
  host_os_label: string;
  shell_label: string;
  tools_dir: string;
  sysinternals_smb_share: string;
  total_count: number;
  installed_count: number;
  live_smb_count: number;
  missing_downloadable_ids: string[];
  tools: SystemToolItem[];
}

export interface HostInterfaceItem {
  name: string;
  subnets: string[];
  label: string;
  is_virtual: boolean;
}

export interface CliBannerInfo {
  version: string;
  developed_by: string;
  repository: string;
  license_name: string;
  license_path: string;
  crow_ascii_lines: string[];
  cora_banner_lines: string[];
  combined_splash_lines: string[];
  description_lines: string[];
  disclaimer_lines: string[];
  license_header_lines: string[];
  full_license_text: string;
  vault_dir: string;
  projects_dir: string;
  working_dir: string;
}


