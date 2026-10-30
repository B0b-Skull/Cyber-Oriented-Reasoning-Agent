<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';
  import type {
    SessionMode,
    PostureInfo,
    ProjectItem,
    WorkspaceFile,
    ProjectFilesPayload,
    ModelItem,
    HardwareMetrics,
    ChatMessage,
    SystemToolsInventory,
    SystemToolItem,
    HostInterfaceItem,
    CliBannerInfo,
  } from './types';

  // --- Bootstrap & State ---
  let loading = true;
  let errorBanner = '';
  let statusToast = '';

  let versionStr = '5.15.12';
  let activeProject = '';
  let sessionMode: 'default' | 'analyst' | 'berserker' | 'ninja' = 'default';
  let isolationLevel: 'red' | 'blue' | 'white' = 'red';
  let allowedInterfaces = 'Wi-Fi';
  let selectedModel = '3.8';
  let inferenceProvider: 'llama-server' | 'ollama' = 'llama-server';
  let thinkingEnabled = false;
  let permissionMode: 'confirm' | 'auto' = 'confirm';
  let activeGoal = '';
  let runReasoningOnSubmit = true;

  // --- Dark / Light Theme State ---
  // Dark mode uses the White Crow Emblem (/api/assets/logo-dark)
  // Light mode uses the Dark/Glow Crow Emblem (/api/assets/logo-light)
  let themeMode: 'dark' | 'light' = 'dark';

  // --- Enterprise UI Customization & Settings Gear Modal State ---
  let showSettingsModal = false;
  let uiFontFamily = "'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace";
  let uiFontSize = 13; // px (11 - 20)
  let uiFontColor = ''; // '' = Theme Default Auto, or hex color e.g. '#e2e8f0'
  let uiLineHeight = '1.5'; // '1.35' | '1.5' | '1.7'
  let uiPanelDensity: 'flush' | 'framed' = 'flush'; // 'flush' = zero outer gap edge-to-edge enterprise layout
  let uiGlowIntensity = 'standard';

  const FONT_FAMILY_OPTIONS = [
    {
      label: 'JetBrains Mono / Cascadia Code (Default Tactical Mono)',
      value: "'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace",
    },
    {
      label: 'Cascadia Code / Consolas (Windows Terminal Mono)',
      value: "'Cascadia Code', 'Consolas', 'Lucida Console', monospace",
    },
    {
      label: 'IBM Plex Mono / Source Code Pro (Technical Mono)',
      value: "'IBM Plex Mono', 'Source Code Pro', 'Courier New', monospace",
    },
    {
      label: 'Inter / Segoe UI / System Sans (Enterprise Dashboard Sans)',
      value: "'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif",
    },
    {
      label: 'Roboto / Arial / Liberation Sans (Clean Corporate Sans)',
      value: "'Roboto', 'Helvetica Neue', Arial, sans-serif",
    },
    {
      label: 'Georgia / Cambria (Executive Report Serif)',
      value: "Georgia, Cambria, 'Times New Roman', serif",
    },
  ];

  const FONT_COLOR_PRESETS = [
    { label: 'Theme Default (Auto)', value: '', swatch: 'linear-gradient(135deg, #f8fafc 50%, #0f172a 50%)' },
    { label: 'Crisp White', value: '#f8fafc', swatch: '#f8fafc' },
    { label: 'Cyber Cyan', value: '#67e8f9', swatch: '#67e8f9' },
    { label: 'Matrix Emerald', value: '#6ee7b7', swatch: '#6ee7b7' },
    { label: 'Tactical Amber', value: '#fcd34d', swatch: '#fcd34d' },
    { label: 'Phosphor Violet', value: '#d8b4fe', swatch: '#d8b4fe' },
    { label: 'Ice Blue', value: '#93c5fd', swatch: '#93c5fd' },
    { label: 'Deep Slate (Light Mode)', value: '#0f172a', swatch: '#0f172a' },
  ];

  let sessionModes: SessionMode[] = [];
  let activeModeInfo: SessionMode | null = null;
  let posture: PostureInfo | null = null;
  let projects: ProjectItem[] = [];
  let models: ModelItem[] = [];
  let llamaServerStatus: {
    online: boolean;
    state?: string;
    api_url: string;
    active_model: string;
    last_error?: string;
  } = { online: false, state: 'offline', api_url: 'http://127.0.0.1:8080/v1', active_model: '', last_error: '' };
  let startingLlm = false;
  let ollamaStatus = { online: false, api_url: 'http://127.0.0.1:11434', model_count: 0 };
  let hardware: HardwareMetrics | null = null;
  let messages: ChatMessage[] = [];
  let systemTools: SystemToolsInventory | null = null;
  let hostInterfaces: HostInterfaceItem[] = [];
  let cliBanner: CliBannerInfo | null = null;

  // --- CLI Banner, Disclaimer & Licensing Modal State (Opened by clicking the CROW Emblem) ---
  let showBannerModal = false;

  const FALLBACK_CORA_BANNER_LINES = [
    '  _____       ____       _____         ___       ',
    ' / ____|     / __ \\     |  __ \\       / _ \\      ',
    '| |         | |  | |    | |__) |     / /_\\ \\     ',
    '| |____  _  | |__| | _  |  _  /  _  / _____ \\  _ ',
    ' \\_____|(_)  \\____/ (_) |_| \\_\\ (_) /_/   \\_\\ (_)',
    '',
    '',
    '  Cyber Oriented Reasoning Agent',
    '  ------------------------------',
  ];

  const FALLBACK_DESCRIPTION_LINES = [
    'C.O.R.A. is a multi-layered reasoning agent that combines AI and a cybersecurity focused',
    'Super Intelligence system to support Red, Blue, and Hunt Teams. Its Analyst, Active, and',
    'Passive modes help teams analyze scan results and system data, identify potential',
    'weaknesses and threats, and create clear reports for technical teams and leadership.',
  ];

  const FALLBACK_DISCLAIMER_LINES = [
    '--- OPEN-SOURCE NOTICE, ATTRIBUTION & LIMITATION OF LIABILITY ---',
    'C.O.R.A. is open-source software under active development and continuous refinement.',
    'Redistribution, modification, or operational deployment is permitted provided that clear',
    'attribution and development credit to https://CROWinnovations.com are retained in all copies',
    'and derivative works. C.O.R.A. and its layered reasoning engines are provided "AS IS" without',
    'warranty of any kind. The developer assumes no liability or legal responsibility for any',
    'actions, damages, data loss, or legal consequences arising from the use of this system.',
  ];

  // --- System Tools UI State ---
  let selectedToolId = '';
  let useLiveSysinternalsSmb = false;
  let showToolsCatalogModal = false;
  let activeTeamFilter: 'all' | 'red' | 'blue' | 'hunt' = 'all';
  let syncingTools = false;

  // --- Project Action Dropdown State (Matches CLI `[1..N]`, `[N+1] Rename`, `[N+2] CREATE NEW`) ---
  let projectDropdownValue = '';
  let showCreateProjectModal = false;
  let newProjectNameInput = '';
  let newProjectGoalInput = '';
  let showRenameProjectModal = false;
  let renameProjectNewNameInput = '';

  // --- Project `Files/` Directory (`Projects/<project>/Files/`) & Console File Upload State ---
  let projectFilesPayload: ProjectFilesPayload | null = null;
  let attachedFiles: string[] = [];
  let uploadingFiles = false;
  let isDraggingFilesOverConsole = false;
  let consoleFileInputEl: HTMLInputElement;
  let showProjectFilesModal = false;
  let localFilePathInput = '';
  let newCustomScriptName = '';
  let newCustomScriptContent = '';
  let selectedProjectFileRel = '';
  let selectedProjectFileContent = '';
  let loadingProjectFileContent = false;
  let savingProjectFile = false;

  // --- Query & Command Execution State ---
  let queryInput = '';
  let commandToExecute = '';
  let submittingQuery = false;
  let executingCommand = false;
  let generatingReport = false;

  // --- Antigravity-Style "Ctrl+O" Thought Process & Engine Trace State (Hidden by Default) ---
  let showThinkingExpanded = false;
  let expandedMessageMap: Record<string, boolean> = {};
  let processingElapsedSec = 0;
  let processingTimerHandle: ReturnType<typeof setInterval> | null = null;
  let activeProcessingLabel = '';
  let activeProcessingDetail = '';

  function startProcessingTimer(label: string, detail = '') {
    activeProcessingLabel = label;
    activeProcessingDetail = detail;
    processingElapsedSec = 0;
    if (processingTimerHandle) clearInterval(processingTimerHandle);
    const startedAt = Date.now();
    processingTimerHandle = setInterval(() => {
      processingElapsedSec = (Date.now() - startedAt) / 1000;
    }, 100);
  }

  function stopProcessingTimer() {
    if (processingTimerHandle) {
      clearInterval(processingTimerHandle);
      processingTimerHandle = null;
    }
  }

  function toggleGlobalThinkingCtrlO() {
    showThinkingExpanded = !showThinkingExpanded;
    if (!showThinkingExpanded) {
      expandedMessageMap = {};
    }
    showToast(
      showThinkingExpanded
        ? '🧠 Thought Process & Engine Trace EXPANDED (Press Ctrl+O to collapse)'
        : '🧠 Thought Process & Engine Trace HIDDEN (Press Ctrl+O to expand)'
    );
  }

  function isMessageThinkingExpanded(msgKey: string, globalExpanded: boolean, mapState: Record<string, boolean>): boolean {
    if (msgKey in mapState) {
      return Boolean(mapState[msgKey]);
    }
    return globalExpanded;
  }

  function toggleSingleMessageThinking(msgKey: string) {
    const current = isMessageThinkingExpanded(msgKey, showThinkingExpanded, expandedMessageMap);
    expandedMessageMap = {
      ...expandedMessageMap,
      [msgKey]: !current,
    };
  }

  function extractCleanDisplayAndThinking(msg: ChatMessage): { cleanContent: string; combinedThinking: string } {
    let rawContent = String(msg.content || '');
    const extraThinkingParts: string[] = [];

    if (msg.thinking && msg.thinking.trim()) {
      extraThinkingParts.push(msg.thinking.trim());
    }

    // 1. Strip any inline <think>...</think> blocks from visible content into Ctrl+O trace
    const thinkRegex = /<think>([\s\S]*?)<\/think>/gi;
    let match: RegExpExecArray | null;
    while ((match = thinkRegex.exec(rawContent)) !== null) {
      const captured = (match[1] || '').trim();
      if (captured && !extraThinkingParts.some((p) => p.includes(captured))) {
        extraThinkingParts.push(`=== LLM CHAIN-OF-THOUGHT (<think>) ===\n${captured}`);
      }
    }
    rawContent = rawContent.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();

    // 2. Strip any legacy inline 15-Engine or Tool Trace sections from visible content into Ctrl+O trace
    const legacyEngineHeaderIdx = rawContent.search(/###\s*(?:15-Engine Neuro-Symbolic|Executed Tactical Probes & Tool Calls)/i);
    if (legacyEngineHeaderIdx > 0) {
      const legacyTrace = rawContent.slice(legacyEngineHeaderIdx).trim();
      rawContent = rawContent.slice(0, legacyEngineHeaderIdx).trim();
      if (legacyTrace && !extraThinkingParts.some((p) => p.includes(legacyTrace))) {
        extraThinkingParts.push(legacyTrace);
      }
    }

    // 3. Remove noisy fallback header prefix if present so CORA output is clean and direct
    rawContent = rawContent.replace(
      /^###\s*C\.O\.R\.A\.\s*15-Engine Neuro-Symbolic Synthesis\s*\([^)]*\)\s*/i,
      '### C.O.R.A. Tactical Assessment\n\n'
    );

    // 4. If reasoning metadata exists on the message and isn't already in combinedThinking, format it for Ctrl+O
    if (msg.reasoning && Object.keys(msg.reasoning).length > 0 && extraThinkingParts.length === 0) {
      const r = msg.reasoning;
      const traceLines: string[] = [
        '=== 15-ENGINE NEURO-SYMBOLIC TRACE (Hidden by Default — Expanded via Ctrl+O) ===',
      ];
      if (r.consensus_immediate_action) {
        traceLines.push(`• Consensus Immediate Action : ${r.consensus_immediate_action}`);
      }
      if (r.engine_9_cegar_proof) {
        traceLines.push(
          `• Engine 9 (CEGAR Proof)     : status=${r.engine_9_cegar_proof.status || 'VERIFIED'} | safe=${r.engine_9_cegar_proof.safe}`
        );
      }
      if (r.engine_11_hmdp_plan) {
        traceLines.push(
          `• Engine 11 (H-MDP Planner)  : action=${r.engine_11_hmdp_plan.recommended_action || 'N/A'} | Q*=${r.engine_11_hmdp_plan.q_star ?? 'N/A'}`
        );
      }
      if (r.engine_14_rl_policy) {
        traceLines.push(
          `• Engine 14 (Trajectory RL)  : best_action=${r.engine_14_rl_policy.best_action || 'N/A'} | advantage=${r.engine_14_rl_policy.advantage ?? 'N/A'}`
        );
      }
      if (r.engine_3_bayesian_top_hypotheses && r.engine_3_bayesian_top_hypotheses.length > 0) {
        const topBayes = r.engine_3_bayesian_top_hypotheses
          .slice(0, 3)
          .map((h) => `${h.hypothesis}=${(Number(h.posterior || 0) * 100).toFixed(1)}%`)
          .join(', ');
        traceLines.push(`• Engine 3 (Bayesian Post.)  : ${topBayes}`);
      }
      if (r.engine_13_meta_mind) {
        traceLines.push(
          `• Engine 13 (META-MIND)      : route=${r.engine_13_meta_mind.selected_route || 'N/A'} | confidence=${((Number(r.engine_13_meta_mind.confidence || 0)) * 100).toFixed(1)}%`
        );
      }
      extraThinkingParts.push(traceLines.join('\n'));
    }

    return {
      cleanContent: rawContent || String(msg.content || ''),
      combinedThinking: extraThinkingParts.join('\n\n'),
    };
  }

  // --- Command & Query History (Up/Down Arrow Scroll) + Shaded Tab Autocomplete State ---
  let queryHistory: string[] = [];
  let queryHistoryCursor = -1; // -1 = live draft, 0..N-1 = index in queryHistory
  let queryDraftBeforeHistory = '';
  let queryCycleIndex = 0;
  let queryAutocompleteDismissed = false;

  let commandHistory: string[] = [];
  let cmdHistoryCursor = -1; // -1 = live draft, 0..N-1 = index in commandHistory
  let cmdDraftBeforeHistory = '';
  let cmdCycleIndex = 0;
  let cmdAutocompleteDismissed = false;

  let queryTextareaEl: HTMLTextAreaElement;
  let queryMirrorEl: HTMLDivElement;
  let cmdInputEl: HTMLInputElement;

  const BASE_AUTOCOMPLETE_WORDS: string[] = [
    '/relentless',
    '/goal',
    '/files',
    '/file',
    '/upload',
    '/add',
    '/generate-report',
    '/report',
    '/mode',
    '/netiso',
    '/project',
    '/rl',
    '/pca',
    '/continual',
    '/train',
    '/reason',
    '/scan',
    '/vault',
    '/remember',
    '/search',
    '/state',
    '/hw',
    '/status',
    '/clear',
    '/help',
    'procdump.exe',
    'psexec.exe',
    'autorunsc.exe',
    'reg.exe',
    'sysmon.exe',
    'accesschk.exe',
    'wevtutil.exe',
    'Get-CimInstance',
    'pslist.exe',
    'handle.exe',
    'pipelist.exe',
    'netstat.exe',
    'tasklist.exe',
    '\\\\live.sysinternals.com\\tools\\',
    '-accepteula',
    'lsass.exe',
    'wininet.dll',
    'EventID=4624',
    'ipconfig',
    'powershell',
    'systeminfo',
    'whoami',
    'netsh',
    'nmap',
    'analyze',
    'analysis',
    'anomalies',
    'architecture',
    'artifacts',
    'assessment',
    'authentication',
    'authorization',
    'autoruns',
    'baseline',
    'beacon',
    'berserker',
    'boundaries',
    'capabilities',
    'certificates',
    'check',
    'command',
    'commands',
    'communications',
    'comparison',
    'configuration',
    'connections',
    'consensus',
    'containers',
    'controller',
    'credentials',
    'cybersecurity',
    'dashboard',
    'database',
    'defense',
    'defensive',
    'deployment',
    'detection',
    'diagnostics',
    'directory',
    'discovery',
    'domain',
    'download',
    'drivers',
    'elevated',
    'encryption',
    'endpoint',
    'enumerate',
    'enumeration',
    'environment',
    'escalation',
    'establish',
    'evasion',
    'execute',
    'execution',
    'exploitation',
    'exfiltration',
    'external',
    'firewall',
    'forensics',
    'gateway',
    'generate',
    'handles',
    'hardening',
    'hashes',
    'hierarchy',
    'hostname',
    'hunting',
    'hypothesis',
    'identify',
    'implications',
    'incident',
    'indicators',
    'infrastructure',
    'injection',
    'inspect',
    'inspection',
    'installed',
    'interface',
    'interfaces',
    'internal',
    'intrusion',
    'inventory',
    'investigate',
    'investigation',
    'isolation',
    'kernel',
    'lateral',
    'latency',
    'listening',
    'localhost',
    'loopback',
    'malicious',
    'malware',
    'memory',
    'mitigation',
    'modules',
    'monitoring',
    'movement',
    'named',
    'namespace',
    'network',
    'networking',
    'offensive',
    'operational',
    'orphaned',
    'outbound',
    'packets',
    'passive',
    'password',
    'pathway',
    'payload',
    'permissions',
    'persistence',
    'pipeline',
    'pivoting',
    'policy',
    'posture',
    'privilege',
    'privileges',
    'processes',
    'protocol',
    'reconnaissance',
    'remediation',
    'registry',
    'remote',
    'report',
    'resolution',
    'response',
    'restricted',
    'routing',
    'sandbox',
    'scanning',
    'scheduled',
    'security',
    'segmentation',
    'services',
    'session',
    'shares',
    'signature',
    'sockets',
    'software',
    'stealth',
    'subnet',
    'subnets',
    'summarize',
    'summary',
    'suspicious',
    'sysinternals',
    'tactical',
    'targets',
    'telemetry',
    'terminal',
    'threats',
    'threads',
    'timeline',
    'tokens',
    'topology',
    'traffic',
    'triage',
    'unauthorized',
    'unrestricted',
    'utilities',
    'validation',
    'vectors',
    'verification',
    'vulnerabilities',
    'vulnerability',
    'weaknesses',
    'windows',
    'workspace',
  ];

  let resultsContainerEl: HTMLElement;
  let ws: WebSocket | null = null;
  let wsConnected = false;

  function showToast(msg: string) {
    statusToast = msg;
    setTimeout(() => {
      if (statusToast === msg) statusToast = '';
    }, 4000);
  }

  function applyThemeToDocument(mode: 'dark' | 'light') {
    if (typeof document === 'undefined') return;
    const meta = document.querySelector('meta[name="color-scheme"]') as HTMLMetaElement | null;
    if (meta) {
      meta.content = mode;
    }
    const linkIcon = document.querySelector('link[rel="icon"]') as HTMLLinkElement | null;
    if (linkIcon) {
      linkIcon.href = mode === 'dark' ? '/api/assets/logo-dark' : '/api/assets/logo-light';
    }
    try {
      localStorage.setItem('color-scheme', mode);
    } catch {
      // ignore storage errors
    }
  }

  async function toggleThemeMode() {
    themeMode = themeMode === 'dark' ? 'light' : 'dark';
    applyThemeToDocument(themeMode);
    await syncSessionConfig();
  }

  function applyUiCustomization(persistLocal = true) {
    if (typeof document !== 'undefined') {
      const root = document.documentElement;
      root.style.setProperty('--cora-font-family', uiFontFamily);
      root.style.setProperty('--cora-font-size', `${uiFontSize}px`);
      root.style.setProperty('--cora-line-height', uiLineHeight);
    }
    if (persistLocal) {
      try {
        localStorage.setItem('cora_ui_font_family', uiFontFamily);
        localStorage.setItem('cora_ui_font_size', String(uiFontSize));
        localStorage.setItem('cora_ui_font_color', uiFontColor);
        localStorage.setItem('cora_ui_line_height', uiLineHeight);
        localStorage.setItem('cora_ui_panel_density', uiPanelDensity);
        localStorage.setItem('cora_ui_glow_intensity', uiGlowIntensity);
      } catch {
        // ignore storage errors
      }
    }
  }

  async function saveUiCustomizationSettings() {
    applyUiCustomization(true);
    await syncSessionConfig();
  }

  async function resetUiCustomization() {
    uiFontFamily = "'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace";
    uiFontSize = 13;
    uiFontColor = '';
    uiLineHeight = '1.5';
    uiPanelDensity = 'flush';
    uiGlowIntensity = 'standard';
    applyUiCustomization(true);
    await syncSessionConfig();
    showToast('Reset font & display customization to enterprise defaults.');
  }

  async function scrollToBottom() {
    await tick();
    if (resultsContainerEl) {
      resultsContainerEl.scrollTop = resultsContainerEl.scrollHeight;
    }
  }

  async function loadBootstrap() {
    loading = true;
    errorBanner = '';
    try {
      const res = await fetch('/api/bootstrap');
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
      const data = await res.json();

      versionStr = data.version?.version || '5.15.12';
      projects = data.projects || [];
      activeProject = data.settings?.active_project || (projects.length > 0 ? projects[0].slug : '');
      projectDropdownValue = activeProject;
      if (!activeProject || projects.length === 0) {
        showCreateProjectModal = true;
      }
      sessionMode = data.settings?.session_mode || 'default';
      isolationLevel = data.settings?.isolation_level || 'red';
      allowedInterfaces = data.settings?.allowed_interfaces || 'eth0,eth1';
      selectedModel = data.settings?.selected_model || '3.8';
      inferenceProvider = data.settings?.inference_provider || 'llama-server';
      thinkingEnabled = data.settings?.thinking_enabled === 'true' || data.settings?.thinking_enabled === true;
      permissionMode = data.settings?.permission_mode || 'confirm';
      activeGoal = data.settings?.active_goal || '';

      let savedTheme: 'dark' | 'light' = 'dark';
      try {
        const lsTheme = localStorage.getItem('color-scheme');
        if (lsTheme === 'light' || lsTheme === 'dark') {
          savedTheme = lsTheme;
        } else if (data.settings?.theme_mode === 'light' || data.settings?.theme_mode === 'dark') {
          savedTheme = data.settings.theme_mode;
        }
      } catch {
        savedTheme = data.settings?.theme_mode === 'light' ? 'light' : 'dark';
      }
      themeMode = savedTheme;
      applyThemeToDocument(themeMode);

      try {
        uiFontFamily =
          localStorage.getItem('cora_ui_font_family') ||
          data.settings?.ui_font_family ||
          "'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace";
        const rawSize = Number(localStorage.getItem('cora_ui_font_size') || data.settings?.ui_font_size || 13);
        uiFontSize = Number.isFinite(rawSize) ? Math.min(20, Math.max(11, rawSize)) : 13;
        const lsColor = localStorage.getItem('cora_ui_font_color');
        uiFontColor = lsColor !== null ? lsColor : data.settings?.ui_font_color || '';
        uiLineHeight = localStorage.getItem('cora_ui_line_height') || data.settings?.ui_line_height || '1.5';
        const rawDensity = localStorage.getItem('cora_ui_panel_density') || data.settings?.ui_panel_density || 'flush';
        uiPanelDensity = rawDensity === 'framed' ? 'framed' : 'flush';
        const rawGlow = localStorage.getItem('cora_ui_glow_intensity') || data.settings?.ui_glow_intensity || 'standard';
        uiGlowIntensity = rawGlow === 'subtle' || rawGlow === 'high' ? rawGlow : 'standard';
      } catch {
        // fallback defaults
      }
      applyUiCustomization(false);

      sessionModes = data.session_modes || [];
      activeModeInfo = data.active_mode || null;
      posture = data.posture || null;
      projectFilesPayload = data.files || null;
      models = data.models?.models || [];
      llamaServerStatus = data.models?.llama_server || llamaServerStatus;
      ollamaStatus = data.models?.ollama || ollamaStatus;
      hardware = data.hardware || null;
      systemTools = data.system_tools || null;
      hostInterfaces = data.host_interfaces || [];
      cliBanner = data.cli_banner || null;
      messages = data.messages || [];
      syncInputHistories(messages, data.system_tools);

      if (isolationLevel === 'white') {
        useLiveSysinternalsSmb = false;
      }

      if (inferenceProvider === 'llama-server' && llamaServerStatus?.state === 'offline') {
        handleStartOrRestartLlm(false);
      }

      await scrollToBottom();
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to load CORA dashboard bootstrap.';
    } finally {
      loading = false;
    }
  }

  function connectTelemetryWebSocket() {
    try {
      const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${proto}//${window.location.host}/ws/metrics`;
      ws = new WebSocket(wsUrl);
      ws.onopen = () => {
        wsConnected = true;
      };
      ws.onmessage = (evt) => {
        try {
          const payload = JSON.parse(evt.data);
          if (payload.type === 'telemetry') {
            hardware = payload.hardware;
            if (payload.posture) posture = payload.posture;
            if (payload.llama_server) llamaServerStatus = payload.llama_server;
          }
        } catch {
          // ignore malformed frame
        }
      };
      ws.onclose = () => {
        wsConnected = false;
        setTimeout(connectTelemetryWebSocket, 3000);
      };
    } catch {
      wsConnected = false;
    }
  }

  onMount(() => {
    loadBootstrap();
    connectTelemetryWebSocket();
  });

  onDestroy(() => {
    if (ws) ws.close();
    stopProcessingTimer();
  });

  // --- Handlers for CLI-Equivalent Dropdown Selectors ---
  async function handleProjectDropdownChange() {
    if (projectDropdownValue === '__CREATE_NEW__') {
      newProjectNameInput = '';
      newProjectGoalInput = '';
      showCreateProjectModal = true;
      projectDropdownValue = activeProject;
      return;
    }
    if (projectDropdownValue === '__RENAME_CURRENT__') {
      renameProjectNewNameInput = activeProject;
      showRenameProjectModal = true;
      projectDropdownValue = activeProject;
      return;
    }
    try {
      const res = await fetch('/api/projects/select', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug: projectDropdownValue }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      activeProject = data.active_project;
      projectDropdownValue = activeProject;
      projects = data.projects || projects;
      projectFilesPayload = data.files || projectFilesPayload;
      attachedFiles = [];
      messages = data.messages || [];
      syncInputHistories(messages, systemTools);
      const curProjObj = projects.find((p) => p.slug === activeProject);
      activeGoal = curProjObj?.last_goal || '';
      showToast(`Switched active workspace to Projects/${activeProject}/ (Files/ ready)`);
      await scrollToBottom();
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to switch project.';
    }
  }

  async function submitCreateProject() {
    if (!newProjectNameInput.trim()) return;
    try {
      const res = await fetch('/api/projects/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newProjectNameInput.trim(),
          goal: newProjectGoalInput.trim(),
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      activeProject = data.created_slug || data.active_project;
      projectDropdownValue = activeProject;
      projects = data.projects || projects;
      projectFilesPayload = data.files || projectFilesPayload;
      attachedFiles = [];
      messages = [];
      activeGoal = newProjectGoalInput.trim();
      showCreateProjectModal = false;
      showToast(`Created & activated Projects/${activeProject}/ (with Projects/${activeProject}/Files/)`);
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to create project.';
    }
  }

  async function submitRenameProject() {
    if (!renameProjectNewNameInput.trim() || renameProjectNewNameInput.trim() === activeProject) {
      showRenameProjectModal = false;
      return;
    }
    try {
      const res = await fetch('/api/projects/rename', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          old_slug: activeProject,
          new_name: renameProjectNewNameInput.trim(),
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      activeProject = data.new_slug;
      projectDropdownValue = activeProject;
      projects = data.projects || projects;
      projectFilesPayload = data.files || projectFilesPayload;
      showRenameProjectModal = false;
      showToast(`Renamed workspace to Projects/${activeProject}/`);
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to rename project.';
    }
  }

  async function refreshProjectFiles() {
    try {
      const res = await fetch(`/api/projects/files?project_slug=${encodeURIComponent(activeProject)}`);
      if (!res.ok) return;
      projectFilesPayload = await res.json();
    } catch {
      // ignore background refresh error
    }
  }

  function readFileAsBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const resStr = String(reader.result || '');
        const commaIdx = resStr.indexOf(',');
        resolve(commaIdx >= 0 ? resStr.slice(commaIdx + 1) : resStr);
      };
      reader.onerror = () => reject(reader.error || new Error(`Failed to read ${file.name}`));
      reader.readAsDataURL(file);
    });
  }

  function toggleAttachFile(projectRel: string) {
    const clean = (projectRel || '').trim();
    if (!clean) return;
    if (attachedFiles.includes(clean)) {
      attachedFiles = attachedFiles.filter((f) => f !== clean);
    } else {
      attachedFiles = [...attachedFiles, clean];
    }
  }

  async function handleBrowserFilesUpload(fileList: FileList | File[] | null, autoAttach = true) {
    if (!fileList || fileList.length === 0 || uploadingFiles) return;
    uploadingFiles = true;
    errorBanner = '';
    try {
      const arr = Array.from(fileList);
      const payloadFiles: Array<{ filename: string; content_base64: string }> = [];
      for (const f of arr) {
        const b64 = await readFileAsBase64(f);
        payloadFiles.push({ filename: f.name, content_base64: b64 });
      }
      const res = await fetch('/api/projects/files/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_slug: activeProject,
          files: payloadFiles,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      if (data.projects) projects = data.projects;
      if (data.files) projectFilesPayload = data.files;
      const uploadedList = data.uploaded || [];
      if (autoAttach && uploadedList.length > 0) {
        const nextAttached = new Set(attachedFiles);
        for (const u of uploadedList) {
          if (u.project_rel) nextAttached.add(u.project_rel);
        }
        attachedFiles = Array.from(nextAttached);
      }
      showToast(
        `Uploaded ${uploadedList.length} file(s) to Projects/${activeProject}/Files/ — ready for LLM interaction!`
      );
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to upload file(s) to Projects/Files/.';
    } finally {
      uploadingFiles = false;
      if (consoleFileInputEl) {
        consoleFileInputEl.value = '';
      }
    }
  }

  async function handleImportLocalPath(autoAttach = true) {
    if (!localFilePathInput.trim() || uploadingFiles) return;
    uploadingFiles = true;
    errorBanner = '';
    try {
      const res = await fetch('/api/projects/files/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_slug: activeProject,
          local_path: localFilePathInput.trim(),
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      if (data.projects) projects = data.projects;
      if (data.files) projectFilesPayload = data.files;
      const uploadedList = data.uploaded || [];
      if (autoAttach && uploadedList.length > 0) {
        const nextAttached = new Set(attachedFiles);
        for (const u of uploadedList) {
          if (u.project_rel) nextAttached.add(u.project_rel);
        }
        attachedFiles = Array.from(nextAttached);
      }
      localFilePathInput = '';
      showToast(`Imported ${uploadedList.length} file(s) into Projects/${activeProject}/Files/`);
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to import local path into Projects/Files/.';
    } finally {
      uploadingFiles = false;
    }
  }

  async function handleCreateNewCustomScript() {
    if (!newCustomScriptName.trim() || uploadingFiles) return;
    uploadingFiles = true;
    errorBanner = '';
    try {
      const res = await fetch('/api/projects/files/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_slug: activeProject,
          files: [
            {
              filename: newCustomScriptName.trim(),
              content_text: newCustomScriptContent,
            },
          ],
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      if (data.projects) projects = data.projects;
      if (data.files) projectFilesPayload = data.files;
      const created = (data.uploaded || [])[0];
      if (created?.project_rel && !attachedFiles.includes(created.project_rel)) {
        attachedFiles = [...attachedFiles, created.project_rel];
      }
      showToast(`Saved custom file Projects/${activeProject}/Files/${newCustomScriptName.trim()}`);
      newCustomScriptName = '';
      newCustomScriptContent = '';
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to create file in Projects/Files/.';
    } finally {
      uploadingFiles = false;
    }
  }

  async function openProjectFileInViewer(relPath: string) {
    if (!relPath) return;
    loadingProjectFileContent = true;
    selectedProjectFileRel = relPath;
    showProjectFilesModal = true;
    try {
      const res = await fetch(`/api/files/content?rel_path=${encodeURIComponent(relPath)}`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      selectedProjectFileContent = data.content || '';
    } catch (err: any) {
      errorBanner = err?.message || `Failed to read ${relPath}`;
    } finally {
      loadingProjectFileContent = false;
    }
  }

  async function saveEditedProjectFile() {
    if (!selectedProjectFileRel || savingProjectFile) return;
    savingProjectFile = true;
    errorBanner = '';
    try {
      const res = await fetch('/api/files/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rel_path: selectedProjectFileRel,
          content: selectedProjectFileContent,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      await refreshProjectFiles();
      showToast(`Saved ${selectedProjectFileRel}`);
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to save file.';
    } finally {
      savingProjectFile = false;
    }
  }

  async function deleteProjectFile(relPath: string) {
    if (!relPath) return;
    try {
      const res = await fetch('/api/projects/files/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_slug: activeProject,
          rel_path: relPath,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      if (data.projects) projects = data.projects;
      if (data.files) projectFilesPayload = data.files;
      attachedFiles = attachedFiles.filter((f) => f !== relPath && !relPath.endsWith(f));
      if (selectedProjectFileRel === relPath) {
        selectedProjectFileRel = '';
        selectedProjectFileContent = '';
      }
      showToast(`Removed ${relPath} from Projects/${activeProject}/Files/`);
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to delete file.';
    }
  }

  function promptLlmToUseProjectFile(fileItem: WorkspaceFile) {
    const pRel = fileItem.project_rel || `Files/${fileItem.name}`;
    if (!attachedFiles.includes(pRel)) {
      attachedFiles = [...attachedFiles, pRel];
    }
    const ext = (fileItem.ext || '').toLowerCase();
    if (['.py', '.sh', '.ps1', '.bat', '.cmd', '.pl', '.rb'].includes(ext)) {
      if (ext === '.py') {
        commandToExecute = `python "${fileItem.rel_path}"`;
      } else if (ext === '.ps1') {
        commandToExecute = `powershell -NoProfile -ExecutionPolicy Bypass -File "${fileItem.rel_path}"`;
      } else if (ext === '.sh') {
        commandToExecute = `bash "${fileItem.rel_path}"`;
      } else {
        commandToExecute = `"${fileItem.rel_path}"`;
      }
      if (!queryInput.trim()) {
        queryInput = `Go to the local Files directory (Projects/${activeProject}/Files/) and inspect and use ${fileItem.name}.`;
      }
    } else if (!queryInput.trim()) {
      queryInput = `Go to the local Files directory (Projects/${activeProject}/Files/) and analyze ${fileItem.name}.`;
    }
    showProjectFilesModal = false;
    showToast(`Attached ${pRel} to Console prompt`);
  }

  function handleConsoleDragOver(e: DragEvent) {
    e.preventDefault();
    if (e.dataTransfer?.types?.includes('Files')) {
      isDraggingFilesOverConsole = true;
    }
  }

  function handleConsoleDragLeave(e: DragEvent) {
    e.preventDefault();
    isDraggingFilesOverConsole = false;
  }

  async function handleConsoleDrop(e: DragEvent) {
    e.preventDefault();
    isDraggingFilesOverConsole = false;
    const dropped = e.dataTransfer?.files;
    if (dropped && dropped.length > 0) {
      await handleBrowserFilesUpload(dropped, true);
    }
  }

  function isInterfaceSelectedInBlue(ifaceName: string): boolean {
    const parts = allowedInterfaces
      .split(',')
      .map((s) => s.trim().toLowerCase())
      .filter(Boolean);
    const ilow = ifaceName.trim().toLowerCase();
    return parts.some((p) => p === ilow || (p.length >= 3 && (ilow.includes(p) || p.includes(ilow))));
  }

  async function toggleBlueInterfaceChip(ifaceName: string) {
    const rawParts = allowedInterfaces
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    const ilow = ifaceName.trim().toLowerCase();
    const existsIdx = rawParts.findIndex((p) => p.toLowerCase() === ilow);
    let nextParts: string[];
    if (existsIdx >= 0) {
      if (rawParts.length <= 1) {
        showToast('BLUE isolation requires at least one allowed interface.');
        return;
      }
      nextParts = rawParts.filter((_, idx) => idx !== existsIdx);
    } else {
      nextParts = [...rawParts, ifaceName.trim()];
    }
    allowedInterfaces = nextParts.join(',');
    await syncSessionConfig();
  }

  async function syncSessionConfig() {
    const modeObj = sessionModes.find((m) => m.key === sessionMode);
    if (modeObj) {
      if (modeObj.forced_isolation) {
        isolationLevel = modeObj.forced_isolation as 'white';
      } else if (!modeObj.allowed_isolation.includes(isolationLevel)) {
        isolationLevel = modeObj.allowed_isolation[0] as 'red' | 'blue';
      }
    }
    if (isolationLevel === 'white') {
      // WHITE air-gap blocks remote SMB shares
      useLiveSysinternalsSmb = false;
    }
    const modelObj = models.find((m) => m.id === selectedModel);
    if (modelObj) {
      inferenceProvider = modelObj.provider;
    }
    try {
      const res = await fetch('/api/session/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          active_project: activeProject,
          session_mode: sessionMode,
          isolation_level: isolationLevel,
          allowed_interfaces: allowedInterfaces,
          selected_model: selectedModel,
          inference_provider: inferenceProvider,
          thinking_enabled: thinkingEnabled,
          permission_mode: permissionMode,
          active_goal: activeGoal,
          theme_mode: themeMode,
          ui_font_family: uiFontFamily,
          ui_font_size: String(uiFontSize),
          ui_font_color: uiFontColor,
          ui_line_height: uiLineHeight,
          ui_panel_density: uiPanelDensity,
          ui_glow_intensity: uiGlowIntensity,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      activeModeInfo = data.active_mode;
      posture = data.posture;
      if (data.llama_server) llamaServerStatus = data.llama_server;
      showToast(
        `Synced: Theme=${themeMode.toUpperCase()} | Mode=${sessionMode.toUpperCase()} | NetIso=${isolationLevel.toUpperCase()}${
          isolationLevel === 'blue' ? `(${allowedInterfaces})` : ''
        }`
      );
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to update session configuration.';
    }
  }

  async function handleStartOrRestartLlm(forceRestart = false) {
    if (startingLlm) return;
    startingLlm = true;
    errorBanner = '';
    showToast(`Starting local LLM (${selectedModel})...`);
    try {
      const res = await fetch('/api/models/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_id: selectedModel, force_restart: forceRestart }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      if (data.models?.llama_server) {
        llamaServerStatus = data.models.llama_server;
      }
      if (data.ok) {
        showToast(`LLM (${llamaServerStatus.active_model || selectedModel}) is ONLINE and ready!`);
      } else if (data.result?.error) {
        errorBanner = data.result.error;
      }
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to start local LLM.';
    } finally {
      startingLlm = false;
    }
  }

  function buildToolCommand(tool: SystemToolItem, useSafeDemo = false): string {
    if (useLiveSysinternalsSmb && tool.live_smb_path && isolationLevel !== 'white') {
      if (useSafeDemo) {
        const parts = tool.safe_demo_command.split(' ');
        return `${tool.live_smb_path} ${parts.slice(1).join(' ')}`.trim();
      }
      return tool.live_smb_example || `${tool.live_smb_path} -accepteula`;
    }
    return useSafeDemo ? tool.resolved_safe_command : tool.resolved_command;
  }

  function handleToolDropdownSelect() {
    if (!selectedToolId || !systemTools) return;
    const tool = systemTools.tools.find((t) => t.id === selectedToolId);
    if (!tool) return;
    const cmd = buildToolCommand(tool, false);
    commandToExecute = cmd;
    if (!queryInput.trim()) {
      queryInput = `Analyze output and tactical implications of ${tool.name} (${tool.focus_area}): \`${cmd}\``;
    }
    showToast(
      `Loaded ${tool.name} (${useLiveSysinternalsSmb && tool.live_smb_path && isolationLevel !== 'white' ? 'Live SMB Share' : tool.status_label}) into Command Probe`
    );
  }

  function selectToolCard(tool: SystemToolItem, runSafeImmediately = false) {
    selectedToolId = tool.id;
    const cmd = buildToolCommand(tool, runSafeImmediately);
    commandToExecute = cmd;
    queryInput = `Execute and analyze ${tool.name} (${tool.team_label} - ${tool.focus_area}): \`${cmd}\``;
    showToolsCatalogModal = false;
    if (runSafeImmediately) {
      runQuickCommand(cmd);
    } else {
      showToast(`Prepared ${tool.name}: ${cmd}`);
    }
  }

  async function handleVerifyAndDownloadTools() {
    if (syncingTools) return;
    syncingTools = true;
    errorBanner = '';
    try {
      const res = await fetch('/api/tools/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      systemTools = data.inventory || systemTools;
      const dlCount = (data.downloaded || []).length;
      if (dlCount > 0) {
        showToast(`Verified & downloaded ${dlCount} tool(s) into ${systemTools?.tools_dir}`);
      } else {
        showToast(`All ${systemTools?.installed_count}/${systemTools?.total_count} system tools verified & installed!`);
      }
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to verify/download system tools.';
    } finally {
      syncingTools = false;
    }
  }

  async function handlePursueGoal() {
    if (!activeGoal.trim() || submittingQuery) return;
    await syncSessionConfig();
    queryInput = `/goal ${activeGoal.trim()}`;
    await handleQuerySubmit();
  }

  async function handleQuerySubmit() {
    if ((!queryInput.trim() && !commandToExecute.trim() && !activeGoal.trim() && attachedFiles.length === 0) || submittingQuery) return;
    submittingQuery = true;
    errorBanner = '';

    const submittedAttached = [...attachedFiles];
    const submittedText =
      queryInput.trim() ||
      (commandToExecute.trim()
        ? `Execute & analyze: ${commandToExecute.trim()}`
        : submittedAttached.length > 0
        ? `Go to the local Files directory (Projects/${activeProject}/Files/) and inspect and analyze: ${submittedAttached.join(', ')}`
        : `/goal ${activeGoal.trim()}`);
    const isSlashInfoCmd =
      submittedText.startsWith('/') &&
      (/\s(-h|--help|help|status|list|audit|clear|off)\b/i.test(submittedText) ||
        /^\/(help|status|clear|hw|vault|state|context|permissions|hud|files|file|upload|add|exit|quit)\b/i.test(submittedText));
    const submittedCmd = isSlashInfoCmd ? '' : commandToExecute.trim();

    startProcessingTimer(
      'C.O.R.A. is thinking & processing...',
      `Model: ${selectedModel} (${inferenceProvider}) • Project: Projects/${activeProject}/ • Query: "${submittedText.slice(0, 100)}"${
        submittedCmd ? ` • Probe: ${submittedCmd}` : ''
      }`
    );

    if (queryInput.trim()) {
      pushQueryHistory(queryInput.trim());
    }
    if (submittedCmd) {
      pushCommandHistory(submittedCmd);
    }

    // Optimistically append user message to the Results Display Window above
    const attachedBadgeStr =
      submittedAttached.length > 0
        ? `\n\n\`[Attached from Projects/${activeProject}/Files/]: ${submittedAttached.join(', ')}\``
        : '';
    const tempUserMsg: ChatMessage = {
      conversation_id: `conv-${activeProject}`,
      project_slug: activeProject,
      role: 'user',
      content:
        submittedText +
        attachedBadgeStr +
        (submittedCmd ? `\n\n\`[Shell Probe]: ${submittedCmd}\`` : ''),
      posture_level: posture?.color_level || isolationLevel.toUpperCase(),
      mode_key: sessionMode,
      model_used: selectedModel,
      latency_ms: 0,
      created_at: new Date().toLocaleTimeString(),
    };
    messages = [...messages, tempUserMsg];
    queryInput = '';
    commandToExecute = '';
    attachedFiles = [];
    queryHistoryCursor = -1;
    cmdHistoryCursor = -1;
    queryDraftBeforeHistory = '';
    cmdDraftBeforeHistory = '';
    await scrollToBottom();

    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: submittedText,
          project_slug: activeProject,
          session_mode: sessionMode,
          isolation_level: isolationLevel,
          allowed_interfaces: allowedInterfaces,
          selected_model: selectedModel,
          thinking_enabled: thinkingEnabled,
          permission_mode: permissionMode,
          run_reasoning: runReasoningOnSubmit,
          execute_command: submittedCmd || null,
          attached_files: submittedAttached,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();

      const replyText = data.reply || data.assistant_message?.content || '';
      if (replyText) {
        const assistantMsg: ChatMessage = data.assistant_message || {
          id: data.message_id,
          conversation_id: data.conversation_id || `conv-${activeProject}`,
          project_slug: activeProject,
          role: 'assistant',
          content: replyText,
          thinking: data.thinking || '',
          command_executed: data.command_result?.command || '',
          command_output: data.command_result?.output || '',
          reasoning: data.reasoning || {},
          posture_level: data.posture?.color_level || isolationLevel.toUpperCase(),
          mode_key: sessionMode,
          model_used: data.model_used || selectedModel,
          latency_ms: data.latency_ms || 0,
          created_at: new Date().toLocaleTimeString(),
        };
        messages = [...messages, assistantMsg];
      }
      if (data.posture) posture = data.posture;
      if (data.active_mode) activeModeInfo = data.active_mode;
      if (data.llama_server) llamaServerStatus = data.llama_server;
      if (data.llm_online === false && data.llm_error) {
        errorBanner = `LLM Warning: ${data.llm_error}`;
      }
      await refreshProjectFiles();
      await scrollToBottom();
    } catch (err: any) {
      errorBanner = err?.message || 'Query execution failed.';
    } finally {
      stopProcessingTimer();
      submittingQuery = false;
    }
  }

  async function runQuickCommand(cmd: string) {
    if (!cmd.trim() || executingCommand) return;
    pushCommandHistory(cmd.trim());
    cmdHistoryCursor = -1;
    executingCommand = true;
    errorBanner = '';
    startProcessingTimer(
      'C.O.R.A. is executing host command probe...',
      `Command: ${cmd.trim()} • Posture: ${postureColor} (${isolationLevel.toUpperCase()})`
    );
    await scrollToBottom();
    try {
      const res = await fetch('/api/command/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          command: cmd.trim(),
          project_slug: activeProject,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      const internalTrace = data.sygus_facts
        ? `=== ENGINE 9 (CEGAR) & ENGINE 10 (SyGuS) VERIFICATION TRACE ===\nCommand: ${data.command}\nExit Code: ${data.exit_code}\nParsed Facts:\n${JSON.stringify(
            data.sygus_facts,
            null,
            2
          )}`
        : '';
      const sysMsg: ChatMessage = {
        conversation_id: `conv-${activeProject}`,
        project_slug: activeProject,
        role: 'assistant',
        content: data.blocked
          ? `### Command Blocked by Safety / Network Isolation Guardrail\n- **Command:** \`${cmd}\`\n- **Active Posture:** \`${postureColor}\` (${isolationLevel.toUpperCase()})\n- **Reason:** ${data.reason}`
          : `### Host Command Executed (\`exit=${data.exit_code}\`, \`${data.latency_ms} ms\`)\n- **Command:** \`${data.command}\`\n\n\`\`\`text\n${data.output || '(no stdout/stderr)'}\n\`\`\``,
        thinking: internalTrace,
        command_executed: data.command,
        command_output: data.output || '',
        posture_level: posture?.color_level || isolationLevel.toUpperCase(),
        mode_key: sessionMode,
        model_used: 'Host Shell Probe',
        latency_ms: data.latency_ms || 0,
        created_at: new Date().toLocaleTimeString(),
      };
      messages = [...messages, sysMsg];
      await scrollToBottom();
    } catch (err: any) {
      errorBanner = err?.message || 'Command execution failed.';
    } finally {
      stopProcessingTimer();
      executingCommand = false;
    }
  }

  async function handleGenerateReport() {
    generatingReport = true;
    startProcessingTimer(
      'C.O.R.A. is synthesizing 5-Section Project Report...',
      `Workspace: Projects/${activeProject}/REPORT.md • Focus: ${activeGoal || 'General Assessment'}`
    );
    await scrollToBottom();
    try {
      const res = await fetch('/api/reports/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_slug: activeProject,
          focus: activeGoal || '',
          use_llm: true,
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      showToast(`Generated 5-Section Report: Projects/${activeProject}/REPORT.md`);
      const repMsg: ChatMessage = {
        conversation_id: `conv-${activeProject}`,
        project_slug: activeProject,
        role: 'assistant',
        content: `### Generated 5-Section Project Report (\`Projects/${activeProject}/REPORT.md\`)\n\n${(data.report?.markdown || '').slice(0, 5000)}`,
        posture_level: posture?.color_level || isolationLevel.toUpperCase(),
        mode_key: sessionMode,
        model_used: 'CORA Report Generator',
        latency_ms: 0,
        created_at: new Date().toLocaleTimeString(),
      };
      messages = [...messages, repMsg];
      await scrollToBottom();
    } catch (err: any) {
      errorBanner = err?.message || 'Report generation failed.';
    } finally {
      stopProcessingTimer();
      generatingReport = false;
    }
  }

  async function handleClearHistory() {
    try {
      await fetch(`/api/messages/${encodeURIComponent(activeProject)}`, { method: 'DELETE' });
      messages = [];
      showToast(`Cleared conversation display for ${activeProject}`);
    } catch (err: any) {
      errorBanner = err?.message || 'Failed to clear history.';
    }
  }

  // --- Up/Down History Navigation & Shaded Word/Command Autocomplete Engine ---
  function syncInputHistories(msgs: ChatMessage[], toolsInv: SystemToolsInventory | null) {
    let savedQueries: string[] = [];
    let savedCmds: string[] = [];
    try {
      const rawQ = localStorage.getItem('cora_query_history');
      if (rawQ) savedQueries = JSON.parse(rawQ);
      const rawC = localStorage.getItem('cora_cmd_history');
      if (rawC) savedCmds = JSON.parse(rawC);
    } catch {
      // ignore storage errors
    }

    const msgQueries: string[] = [];
    const msgCmds: string[] = [];
    for (const m of msgs || []) {
      if (m.role === 'user' && m.content) {
        const cleanQ = m.content.split('\n\n`[Shell Probe]:')[0].trim();
        if (cleanQ) msgQueries.push(cleanQ);
      }
      if (m.command_executed && m.command_executed.trim()) {
        msgCmds.push(m.command_executed.trim());
      }
      if (m.reasoning?.consensus_immediate_action) {
        msgCmds.push(m.reasoning.consensus_immediate_action.trim());
      }
    }

    const defaultCmdSeeds = (toolsInv?.tools || []).slice(0, 6).map((t) => t.resolved_safe_command || t.resolved_command);

    const dedupeKeepRecent = (arr: string[], limit = 100): string[] => {
      const seen = new Set<string>();
      const out: string[] = [];
      for (let i = arr.length - 1; i >= 0; i--) {
        const item = (arr[i] || '').trim();
        if (!item) continue;
        const key = item.toLowerCase();
        if (!seen.has(key)) {
          seen.add(key);
          out.unshift(item);
          if (out.length >= limit) break;
        }
      }
      return out;
    };

    queryHistory = dedupeKeepRecent([...savedQueries, ...msgQueries], 100);
    commandHistory = dedupeKeepRecent(
      [...defaultCmdSeeds, ...savedCmds, ...msgCmds].map((c) => c.replace(/\barp\s+-accepteula\b/gi, 'arp -a')),
      100
    );
    queryHistoryCursor = -1;
    cmdHistoryCursor = -1;
  }

  function pushQueryHistory(q: string) {
    const clean = q.trim();
    if (!clean) return;
    queryHistory = [...queryHistory.filter((x) => x.toLowerCase() !== clean.toLowerCase()), clean].slice(-100);
    try {
      localStorage.setItem('cora_query_history', JSON.stringify(queryHistory));
    } catch {
      // ignore
    }
  }

  function pushCommandHistory(c: string) {
    const clean = c.trim();
    if (!clean) return;
    commandHistory = [...commandHistory.filter((x) => x.toLowerCase() !== clean.toLowerCase()), clean].slice(-100);
    try {
      localStorage.setItem('cora_cmd_history', JSON.stringify(commandHistory));
    } catch {
      // ignore
    }
  }

  function stepQueryHistory(direction: 'up' | 'down') {
    if (queryHistory.length === 0) return;
    if (direction === 'up') {
      if (queryHistoryCursor === -1) {
        queryDraftBeforeHistory = queryInput;
        queryHistoryCursor = queryHistory.length - 1;
      } else if (queryHistoryCursor > 0) {
        queryHistoryCursor -= 1;
      }
      queryInput = queryHistory[queryHistoryCursor] || '';
      queryAutocompleteDismissed = true;
    } else {
      if (queryHistoryCursor === -1) return;
      if (queryHistoryCursor < queryHistory.length - 1) {
        queryHistoryCursor += 1;
        queryInput = queryHistory[queryHistoryCursor] || '';
      } else {
        queryHistoryCursor = -1;
        queryInput = queryDraftBeforeHistory;
      }
      queryAutocompleteDismissed = true;
    }
  }

  function stepCommandHistory(direction: 'up' | 'down') {
    if (commandHistory.length === 0) return;
    if (direction === 'up') {
      if (cmdHistoryCursor === -1) {
        cmdDraftBeforeHistory = commandToExecute;
        cmdHistoryCursor = commandHistory.length - 1;
      } else if (cmdHistoryCursor > 0) {
        cmdHistoryCursor -= 1;
      }
      commandToExecute = commandHistory[cmdHistoryCursor] || '';
      cmdAutocompleteDismissed = true;
    } else {
      if (cmdHistoryCursor === -1) return;
      if (cmdHistoryCursor < commandHistory.length - 1) {
        cmdHistoryCursor += 1;
        commandToExecute = commandHistory[cmdHistoryCursor] || '';
      } else {
        cmdHistoryCursor = -1;
        commandToExecute = cmdDraftBeforeHistory;
      }
      cmdAutocompleteDismissed = true;
    }
  }

  // Build dynamic vocabulary combining history, tools, projects, interfaces, and tactical words
  $: dynamicVocabulary = (() => {
    const words: string[] = [];
    const seen = new Set<string>();
    const addToken = (tok: string) => {
      const clean = (tok || '').trim();
      if (clean.length < 3 && !clean.startsWith('/')) return;
      const low = clean.toLowerCase();
      if (!seen.has(low)) {
        seen.add(low);
        words.push(clean);
      }
    };

    // 1. Slash commands & OS tool binaries
    for (const w of BASE_AUTOCOMPLETE_WORDS) {
      if (w.startsWith('/')) addToken(w);
    }
    if (systemTools?.tools) {
      for (const t of systemTools.tools) {
        addToken(t.binary);
        addToken(t.binary.replace(/\.exe$/i, ''));
        addToken(t.id);
        addToken(t.focus_area);
      }
    }
    // 2. Active Projects & Host Interfaces
    for (const p of projects) addToken(p.slug);
    for (const h of hostInterfaces) {
      addToken(h.name);
      for (const sub of h.subnets || []) addToken(sub);
    }
    // 3. Words from recent query & command history (most recent first)
    for (let i = queryHistory.length - 1; i >= 0; i--) {
      for (const part of queryHistory[i].split(/\s+/)) {
        const cleanPart = part.replace(/^[,.;:()[\]"'`]+|[,.;:()[\]"'`]+$/g, '');
        if (cleanPart.length >= 3) addToken(cleanPart);
      }
    }
    for (let i = commandHistory.length - 1; i >= 0; i--) {
      for (const part of commandHistory[i].split(/\s+/)) {
        const cleanPart = part.replace(/^[,.;:()[\]"'`]+|[,.;:()[\]"'`]+$/g, '');
        if (cleanPart.length >= 3) addToken(cleanPart);
      }
    }
    // 4. Curated tactical & technical vocabulary
    for (const w of BASE_AUTOCOMPLETE_WORDS) {
      addToken(w);
    }
    return words;
  })();

  function computeAutocompleteState(
    rawInput: string,
    isCommandBox: boolean,
    cycleIdx: number,
    dismissed: boolean
  ): {
    suffix: string;
    activeCandidate: string;
    prefix: string;
    matches: string[];
    isFullLineMatch: boolean;
  } {
    if (dismissed || !rawInput) {
      return { suffix: '', activeCandidate: '', prefix: '', matches: [], isFullLineMatch: false };
    }

    const trimmedStart = rawInput.trimStart();
    if (!trimmedStart) {
      return { suffix: '', activeCandidate: '', prefix: '', matches: [], isFullLineMatch: false };
    }

    // 1. If in Command Probe box (or single-token start), check full-command history/tool templates first
    const fullCandidates: string[] = [];
    const seenFull = new Set<string>();
    const addFull = (s: string) => {
      const c = (s || '').trim();
      const low = c.toLowerCase();
      if (c && !seenFull.has(low)) {
        seenFull.add(low);
        fullCandidates.push(c);
      }
    };

    if (isCommandBox) {
      for (let i = commandHistory.length - 1; i >= 0; i--) addFull(commandHistory[i]);
      for (const t of systemTools?.tools || []) {
        addFull(t.resolved_safe_command);
        addFull(t.resolved_command);
        if (t.live_smb_example) addFull(t.live_smb_example);
      }
    } else {
      for (let i = queryHistory.length - 1; i >= 0; i--) addFull(queryHistory[i]);
    }

    // Extract current trailing word token being typed at the end of rawInput
    const wordMatch = rawInput.match(/([\/\\A-Za-z0-9_.\-=:]+)$/);
    if (wordMatch) {
      const prefix = wordMatch[1];
      const prefixLow = prefix.toLowerCase();
      // Require length >= 3 for '-' flags so standard short flags (-a, -n, -4, -h) never collide with -accepteula
      const minLen = prefix.startsWith('/') || prefix.startsWith('\\') ? 1 : prefix.startsWith('-') ? 3 : 2;
      const isSysinternalsLine = /(procdump|psexec|autorunsc|sysmon|accesschk|pslist|handle|pipelist|sysinternals)/i.test(
        rawInput
      );

      if (prefix.length >= minLen) {
        const wordMatches: string[] = [];
        const seenWord = new Set<string>();

        // If typing at the very beginning of the input, include full command/history matches too
        if (rawInput.trim().length === prefix.length && isCommandBox) {
          for (const fc of fullCandidates) {
            if (fc.toLowerCase().startsWith(prefixLow) && fc.length > prefix.length) {
              const low = fc.toLowerCase();
              if (!seenWord.has(low)) {
                seenWord.add(low);
                wordMatches.push(fc);
              }
            }
          }
        }

        for (const w of dynamicVocabulary) {
          if (w.toLowerCase() === '-accepteula' && !isSysinternalsLine) continue;
          if (w.toLowerCase().startsWith(prefixLow) && w.length > prefix.length) {
            // Preserve user's capitalization if they started with an uppercase letter
            const formatted =
              prefix[0] === prefix[0].toUpperCase() && prefix[0] !== prefix[0].toLowerCase()
                ? w[0].toUpperCase() + w.slice(1)
                : w;
            const low = formatted.toLowerCase();
            if (!seenWord.has(low)) {
              seenWord.add(low);
              wordMatches.push(formatted);
            }
          }
          if (wordMatches.length >= 8) break;
        }

        // Also check if the full line matches a recent history entry
        if (wordMatches.length === 0) {
          for (const fc of fullCandidates) {
            if (fc.toLowerCase().startsWith(rawInput.toLowerCase()) && fc.length > rawInput.length) {
              return {
                suffix: fc.slice(rawInput.length),
                activeCandidate: fc,
                prefix: rawInput,
                matches: [fc],
                isFullLineMatch: true,
              };
            }
          }
        }

        if (wordMatches.length > 0) {
          const chosen = wordMatches[((cycleIdx % wordMatches.length) + wordMatches.length) % wordMatches.length];
          return {
            suffix: chosen.slice(prefix.length),
            activeCandidate: chosen,
            prefix,
            matches: wordMatches,
            isFullLineMatch: false,
          };
        }
      }
    } else if (rawInput.endsWith(' ') && rawInput.trim().length >= 3) {
      // User just typed a space after a word: check if a recent history entry starts with rawInput
      for (const fc of fullCandidates) {
        if (fc.toLowerCase().startsWith(rawInput.toLowerCase()) && fc.length > rawInput.length) {
          const remainder = fc.slice(rawInput.length);
          const nextWord = remainder.split(/\s+/)[0] || remainder;
          return {
            suffix: nextWord,
            activeCandidate: nextWord,
            prefix: '',
            matches: [nextWord],
            isFullLineMatch: false,
          };
        }
      }
    }

    return { suffix: '', activeCandidate: '', prefix: '', matches: [], isFullLineMatch: false };
  }

  $: queryAutocomplete = computeAutocompleteState(queryInput, false, queryCycleIndex, queryAutocompleteDismissed);
  $: cmdAutocomplete = computeAutocompleteState(commandToExecute, true, cmdCycleIndex, cmdAutocompleteDismissed);

  function acceptQueryAutocomplete(explicitCandidate?: string) {
    if (explicitCandidate) {
      if (queryAutocomplete.isFullLineMatch || !queryAutocomplete.prefix) {
        queryInput = queryInput + explicitCandidate.slice(queryAutocomplete.prefix.length);
      } else {
        queryInput = queryInput.slice(0, queryInput.length - queryAutocomplete.prefix.length) + explicitCandidate;
      }
    } else if (queryAutocomplete.suffix) {
      queryInput = queryInput + queryAutocomplete.suffix;
    }
    queryCycleIndex = 0;
    if (queryTextareaEl) {
      queryTextareaEl.focus();
    }
  }

  function acceptCommandAutocomplete(explicitCandidate?: string) {
    if (explicitCandidate) {
      if (cmdAutocomplete.isFullLineMatch || !cmdAutocomplete.prefix) {
        commandToExecute = commandToExecute + explicitCandidate.slice(cmdAutocomplete.prefix.length);
      } else {
        commandToExecute = commandToExecute.slice(0, commandToExecute.length - cmdAutocomplete.prefix.length) + explicitCandidate;
      }
    } else if (cmdAutocomplete.suffix) {
      commandToExecute = commandToExecute + cmdAutocomplete.suffix;
    }
    cmdCycleIndex = 0;
    if (cmdInputEl) {
      cmdInputEl.focus();
    }
  }

  function handleQueryInputEvent() {
    queryAutocompleteDismissed = false;
    queryCycleIndex = 0;
    queryHistoryCursor = -1;
  }

  function handleCommandInputEvent() {
    cmdAutocompleteDismissed = false;
    cmdCycleIndex = 0;
    cmdHistoryCursor = -1;
  }

  function handleQueryTextareaScroll() {
    if (queryMirrorEl && queryTextareaEl) {
      queryMirrorEl.scrollTop = queryTextareaEl.scrollTop;
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Tab') {
      if (queryAutocomplete.suffix) {
        e.preventDefault();
        if (e.shiftKey && queryAutocomplete.matches.length > 1) {
          queryCycleIndex = (queryCycleIndex + 1) % queryAutocomplete.matches.length;
        } else {
          acceptQueryAutocomplete();
        }
        return;
      }
    }

    if (e.key === 'ArrowRight' && queryAutocomplete.suffix && queryTextareaEl) {
      if (queryTextareaEl.selectionStart === queryInput.length && queryTextareaEl.selectionEnd === queryInput.length) {
        e.preventDefault();
        acceptQueryAutocomplete();
        return;
      }
    }

    if (e.key === 'Escape' && queryAutocomplete.suffix) {
      e.preventDefault();
      queryAutocompleteDismissed = true;
      return;
    }

    if (e.key === 'ArrowUp' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
      const cursorAtFirstLine = !queryTextareaEl || !queryInput.slice(0, queryTextareaEl.selectionStart).includes('\n');
      if (cursorAtFirstLine || queryHistoryCursor !== -1) {
        e.preventDefault();
        stepQueryHistory('up');
        return;
      }
    }

    if (e.key === 'ArrowDown' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
      const cursorAtLastLine = !queryTextareaEl || !queryInput.slice(queryTextareaEl.selectionEnd).includes('\n');
      if (cursorAtLastLine && queryHistoryCursor !== -1) {
        e.preventDefault();
        stepQueryHistory('down');
        return;
      }
    }

    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleQuerySubmit();
    }
  }

  function handleCommandKeydown(e: KeyboardEvent) {
    if (e.key === 'Tab') {
      if (cmdAutocomplete.suffix) {
        e.preventDefault();
        if (e.shiftKey && cmdAutocomplete.matches.length > 1) {
          cmdCycleIndex = (cmdCycleIndex + 1) % cmdAutocomplete.matches.length;
        } else {
          acceptCommandAutocomplete();
        }
        return;
      }
    }

    if (e.key === 'ArrowRight' && cmdAutocomplete.suffix && cmdInputEl) {
      if (cmdInputEl.selectionStart === commandToExecute.length && cmdInputEl.selectionEnd === commandToExecute.length) {
        e.preventDefault();
        acceptCommandAutocomplete();
        return;
      }
    }

    if (e.key === 'Escape' && cmdAutocomplete.suffix) {
      e.preventDefault();
      cmdAutocompleteDismissed = true;
      return;
    }

    if (e.key === 'ArrowUp') {
      e.preventDefault();
      stepCommandHistory('up');
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      stepCommandHistory('down');
      return;
    }

    if (e.key === 'Enter') {
      e.preventDefault();
      if (commandToExecute.trim()) {
        const cmdToRun = commandToExecute;
        commandToExecute = '';
        runQuickCommand(cmdToRun);
      }
    }
  }

  function formatNetSpeed(kbPerSec: number | undefined | null): string {
    const val = Number(kbPerSec || 0);
    if (!Number.isFinite(val) || val < 0) return '0.0 KB/s';
    if (val >= 1024) {
      return `${(val / 1024).toFixed(1)} MB/s`;
    }
    return `${val.toFixed(1)} KB/s`;
  }

  // Build stacked header NET rows: "Interface name | IP/mask | ↑upload ↓download"
  // If an interface has multiple IP/mask addresses, or if multiple NICs exist, each is stacked as a row
  // inside the scrollable header NET display.
  $: headerNetRows = (() => {
    const rows: Array<{
      ifaceName: string;
      ipMask: string;
      txStr: string;
      rxStr: string;
      isAllowed: boolean;
      isLoopback: boolean;
    }> = [];

    const hwIfaces = hardware?.network?.interfaces || [];
    if (hwIfaces.length > 0) {
      for (const nic of hwIfaces) {
        const cidrs =
          nic.ip_cidr && nic.ip_cidr.length > 0
            ? nic.ip_cidr
            : nic.ipv4 && nic.ipv4.length > 0
            ? nic.ipv4.map((ip) => (ip.includes('/') ? ip : `${ip}/24`))
            : ['N/A'];
        const tx = nic.tx_kb_s !== undefined ? nic.tx_kb_s : hardware?.network?.tx_kb_s || 0;
        const rx = nic.rx_kb_s !== undefined ? nic.rx_kb_s : hardware?.network?.rx_kb_s || 0;
        const allowed =
          isolationLevel === 'red' ||
          (isolationLevel === 'white' && (nic.is_loopback || cidrs.some((c) => c.startsWith('127.')))) ||
          (isolationLevel === 'blue' && isInterfaceSelectedInBlue(nic.name));

        for (const cidr of cidrs) {
          rows.push({
            ifaceName: nic.name,
            ipMask: cidr,
            txStr: formatNetSpeed(tx),
            rxStr: formatNetSpeed(rx),
            isAllowed: Boolean(allowed),
            isLoopback: Boolean(nic.is_loopback),
          });
        }
      }
    } else if (hostInterfaces.length > 0) {
      for (const hif of hostInterfaces) {
        const cidrs =
          hif.subnets && hif.subnets.length > 0
            ? hif.subnets
            : hif.ipv4 && hif.ipv4.length > 0
            ? hif.ipv4.map((ip) => `${ip}/24`)
            : ['N/A'];
        for (const cidr of cidrs) {
          rows.push({
            ifaceName: hif.name,
            ipMask: cidr,
            txStr: formatNetSpeed(hardware?.network?.tx_kb_s || 0),
            rxStr: formatNetSpeed(hardware?.network?.rx_kb_s || 0),
            isAllowed: isolationLevel === 'red' || isInterfaceSelectedInBlue(hif.name),
            isLoopback: Boolean(hif.is_loopback),
          });
        }
      }
    } else if (hardware?.network) {
      rows.push({
        ifaceName: 'Host NIC',
        ipMask: '127.0.0.1/8',
        txStr: formatNetSpeed(hardware.network.tx_kb_s),
        rxStr: formatNetSpeed(hardware.network.rx_kb_s),
        isAllowed: true,
        isLoopback: true,
      });
    }

    return rows;
  })();

  // --- Reactive Theme & Network Isolation Color Engine ---
  // 1. Crow Emblem URL changes automatically with Dark / Light mode:
  //    - Dark Mode  -> White Crow Emblem (/api/assets/logo-dark -> CROW_Logo_White_TransparentBackground.png)
  //    - Light Mode -> Dark/Glow Crow Emblem (/api/assets/logo-light -> CROW_Logo-NoWords_Transparent_Glow-NoBackground.png)
  $: isDark = themeMode === 'dark';
  $: crowLogoUrl = isDark ? '/api/assets/logo-dark' : '/api/assets/logo-light';
  $: postureColor = (isolationLevel || posture?.color_level || 'RED').toUpperCase() as 'RED' | 'BLUE' | 'WHITE';
  $: isFlushLayout = uiPanelDensity === 'flush';
  $: customTextStyle = `font-family: ${uiFontFamily}; font-size: ${uiFontSize}px; line-height: ${uiLineHeight};${
    uiFontColor ? ` color: ${uiFontColor};` : ''
  }`;

  // 2. Dynamic Header & Outline Shades based on Network Isolation (RED, BLUE, WHITE) + Dark/Light Mode
  $: isoTheme = (() => {
    const glowScale = uiGlowIntensity === 'subtle' ? 0.12 : uiGlowIntensity === 'high' ? 0.42 : 0.24;
    if (postureColor === 'RED') {
      return isDark
        ? {
            outlineHex: '#ff3b5c',
            outlineGlow: `rgba(255, 59, 92, ${glowScale})`,
            viewportStyle:
              'background: radial-gradient(circle at 50% 0%, #22080e 0%, #080b12 75%); border: 1px solid rgba(255, 59, 92, 0.75);',
            headerStyle:
              'background: linear-gradient(90deg, #2d0911 0%, #1c070d 55%, #120509 100%); border-bottom: 1.5px solid #ff3b5c; box-shadow: 0 2px 12px rgba(255, 59, 92, 0.20);',
            resultsWindowStyle: isFlushLayout
              ? 'background: #161f30; border-left: 1px solid rgba(255, 59, 92, 0.45); border-right: 1px solid rgba(255, 59, 92, 0.45);'
              : 'background: #161f30; border: 1.5px solid rgba(255, 59, 92, 0.65); box-shadow: 0 0 14px rgba(255, 59, 92, 0.12);',
            controlDeckStyle:
              'background: linear-gradient(180deg, #18070c 0%, #0e0508 100%); border-top: 1.5px solid #ff3b5c; box-shadow: 0 -2px 14px rgba(255, 59, 92, 0.18);',
            cardOutlineStyle: 'border: 1px solid rgba(255, 59, 92, 0.50); box-shadow: 0 1px 8px rgba(255, 59, 92, 0.10);',
            badgeClass: 'bg-rose-950 text-rose-100 border-rose-400 font-bold',
            submitBtnClass:
              'bg-gradient-to-r from-rose-600 to-red-500 hover:from-rose-500 hover:to-red-400 text-white border border-rose-300/50 shadow-rose-900/40',
          }
        : {
            outlineHex: '#e11d48',
            outlineGlow: `rgba(225, 29, 72, ${glowScale})`,
            viewportStyle:
              'background: radial-gradient(circle at 50% 0%, #ffe4e8 0%, #f8fafc 75%); border: 1px solid #e11d48;',
            headerStyle:
              'background: linear-gradient(90deg, #fecdd3 0%, #ffe4e6 55%, #fff1f2 100%); border-bottom: 1.5px solid #e11d48; box-shadow: 0 2px 10px rgba(225, 29, 72, 0.14);',
            resultsWindowStyle: isFlushLayout
              ? 'background: rgba(255, 255, 255, 0.96); border-left: 1px solid rgba(225, 29, 72, 0.45); border-right: 1px solid rgba(225, 29, 72, 0.45);'
              : 'background: rgba(255, 255, 255, 0.94); border: 1.5px solid rgba(225, 29, 72, 0.65);',
            controlDeckStyle:
              'background: linear-gradient(180deg, #fff1f2 0%, #ffe4e6 100%); border-top: 1.5px solid #e11d48;',
            cardOutlineStyle: 'border: 1px solid rgba(225, 29, 72, 0.50); box-shadow: 0 1px 6px rgba(225, 29, 72, 0.08);',
            badgeClass: 'bg-rose-600 text-white border-rose-700 font-bold',
            submitBtnClass:
              'bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white border border-rose-700 shadow-rose-500/30',
          };
    }

    if (postureColor === 'BLUE') {
      return isDark
        ? {
            outlineHex: '#00d2ff',
            outlineGlow: `rgba(0, 210, 255, ${glowScale})`,
            viewportStyle:
              'background: radial-gradient(circle at 50% 0%, #071a36 0%, #060b16 75%); border: 1px solid rgba(0, 210, 255, 0.75);',
            headerStyle:
              'background: linear-gradient(90deg, #072042 0%, #071730 55%, #051022 100%); border-bottom: 1.5px solid #00d2ff; box-shadow: 0 2px 12px rgba(0, 210, 255, 0.20);',
            resultsWindowStyle: isFlushLayout
              ? 'background: #152033; border-left: 1px solid rgba(0, 210, 255, 0.45); border-right: 1px solid rgba(0, 210, 255, 0.45);'
              : 'background: #152033; border: 1.5px solid rgba(0, 210, 255, 0.65);',
            controlDeckStyle:
              'background: linear-gradient(180deg, #07162e 0%, #050e1f 100%); border-top: 1.5px solid #00d2ff; box-shadow: 0 -2px 14px rgba(0, 210, 255, 0.18);',
            cardOutlineStyle: 'border: 1px solid rgba(0, 210, 255, 0.50); box-shadow: 0 1px 8px rgba(0, 210, 255, 0.10);',
            badgeClass: 'bg-sky-950 text-sky-100 border-cyan-400 font-bold',
            submitBtnClass:
              'bg-gradient-to-r from-sky-600 to-cyan-500 hover:from-sky-500 hover:to-cyan-400 text-white border border-cyan-300/50 shadow-sky-900/40',
          }
        : {
            outlineHex: '#0284c7',
            outlineGlow: `rgba(2, 132, 199, ${glowScale})`,
            viewportStyle:
              'background: radial-gradient(circle at 50% 0%, #dbeafe 0%, #f8fafc 75%); border: 1px solid #0284c7;',
            headerStyle:
              'background: linear-gradient(90deg, #bae6fd 0%, #e0f2fe 55%, #f0f9ff 100%); border-bottom: 1.5px solid #0284c7;',
            resultsWindowStyle: isFlushLayout
              ? 'background: rgba(255, 255, 255, 0.96); border-left: 1px solid rgba(2, 132, 199, 0.45); border-right: 1px solid rgba(2, 132, 199, 0.45);'
              : 'background: rgba(255, 255, 255, 0.94); border: 1.5px solid rgba(2, 132, 199, 0.65);',
            controlDeckStyle:
              'background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%); border-top: 1.5px solid #0284c7;',
            cardOutlineStyle: 'border: 1px solid rgba(2, 132, 199, 0.50); box-shadow: 0 1px 6px rgba(2, 132, 199, 0.08);',
            badgeClass: 'bg-sky-600 text-white border-sky-700 font-bold',
            submitBtnClass:
              'bg-gradient-to-r from-sky-600 to-blue-600 hover:from-sky-500 hover:to-blue-500 text-white border border-sky-700 shadow-sky-500/30',
          };
    }

    // WHITE — Air-Gapped Loopback (lo / 127.0.0.1 only)
    return isDark
      ? {
          outlineHex: '#f8fafc',
          outlineGlow: `rgba(248, 250, 252, ${glowScale})`,
          viewportStyle:
            'background: radial-gradient(circle at 50% 0%, #202734 0%, #0b0f16 75%); border: 1px solid rgba(248, 250, 252, 0.85);',
          headerStyle:
            'background: linear-gradient(90deg, #252d3b 0%, #1a212e 55%, #131822 100%); border-bottom: 1.5px solid #ffffff;',
          resultsWindowStyle: isFlushLayout
            ? 'background: #182232; border-left: 1px solid rgba(248, 250, 252, 0.45); border-right: 1px solid rgba(248, 250, 252, 0.45);'
            : 'background: #182232; border: 1.5px solid rgba(248, 250, 252, 0.72);',
          controlDeckStyle:
            'background: linear-gradient(180deg, #1b2230 0%, #11161f 100%); border-top: 1.5px solid #ffffff;',
          cardOutlineStyle: 'border: 1px solid rgba(248, 250, 252, 0.55); box-shadow: 0 1px 8px rgba(255, 255, 255, 0.08);',
          badgeClass: 'bg-white text-slate-950 border-white font-bold',
          submitBtnClass:
            'bg-gradient-to-r from-slate-100 to-white hover:from-white hover:to-slate-200 text-slate-950 border border-white shadow-white/20',
        }
      : {
          outlineHex: '#475569',
          outlineGlow: `rgba(71, 85, 105, ${glowScale})`,
          viewportStyle:
            'background: radial-gradient(circle at 50% 0%, #ffffff 0%, #f1f5f9 75%); border: 1px solid #64748b;',
          headerStyle:
            'background: linear-gradient(90deg, #ffffff 0%, #f8fafc 55%, #f1f5f9 100%); border-bottom: 1.5px solid #475569;',
          resultsWindowStyle: isFlushLayout
            ? 'background: #ffffff; border-left: 1px solid #94a3b8; border-right: 1px solid #94a3b8;'
            : 'background: #ffffff; border: 1.5px solid #64748b;',
          controlDeckStyle:
            'background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%); border-top: 1.5px solid #475569;',
          cardOutlineStyle: 'border: 1px solid #64748b; box-shadow: 0 1px 6px rgba(15, 23, 42, 0.06);',
          badgeClass: 'bg-slate-800 text-white border-slate-900 font-bold',
          submitBtnClass:
            'bg-gradient-to-r from-slate-800 to-slate-900 hover:from-slate-700 hover:to-slate-800 text-white border border-slate-950 shadow-slate-500/30',
        };
  })();

  $: filteredTools = (systemTools?.tools || []).filter(
    (t) => activeTeamFilter === 'all' || t.team === activeTeamFilter
  );
</script>

<svelte:window
  on:keydown={(e) => {
    if ((e.ctrlKey || e.metaKey) && !e.altKey && e.key.toLowerCase() === 'o') {
      e.preventDefault();
      toggleGlobalThinkingCtrlO();
      return;
    }
    if (e.key === 'Escape') {
      if (showSettingsModal) showSettingsModal = false;
      else if (showBannerModal) showBannerModal = false;
      else if (showProjectFilesModal) showProjectFilesModal = false;
      else if (showRenameProjectModal) showRenameProjectModal = false;
      else if (showCreateProjectModal && activeProject) showCreateProjectModal = false;
    }
  }}
/>

<!-- Root Full-Viewport Container (100% Observable Width, Zero Outer Margin/Gap, Enterprise Dashboard Layout) -->
<div
  class="h-screen w-screen overflow-hidden flex flex-col select-none transition-colors duration-200 {isDark
    ? 'text-slate-100'
    : 'text-slate-900'}"
  style="{isoTheme.viewportStyle} {customTextStyle}"
>
  <!-- ===================================================================== -->
  <!-- 1. TOP BRAND, POSTURE, STACKED NET TELEMETRY & SETTINGS GEAR HEADER   -->
  <!--    - CROW Emblem stretches from BOTTOM of header to TOP of header     -->
  <!--    - NET displays: Interface name | IP/mask | upload/download speed   -->
  <!--      stacked in rows with scroll option when multiple NICs/IPs exist  -->
  <!--    - Settings Gear Button placed to the right of SYSINTERNALS badge   -->
  <!-- ===================================================================== -->
  <header
    class="w-full min-h-[62px] shrink-0 px-3 py-1 flex items-center justify-between gap-2.5 z-20 transition-all duration-200"
    style={isoTheme.headerStyle}
  >
    <!-- Left: Full-Header-Height CROW Emblem + Title + Version + Posture Badge -->
    <div class="flex items-center gap-3 h-full min-w-0 shrink-0">
      <!-- Logo Button: Spans 100% from bottom of header to top of header; click opens CLI Banner, Disclaimer & Licensing Modal -->
      <button
        type="button"
        on:click={() => (showBannerModal = true)}
        class="h-12 self-stretch flex items-center justify-center shrink-0 overflow-hidden cursor-pointer focus:outline-none hover:scale-105 active:scale-95 transition-transform duration-150"
        title="Click to view C.O.R.A. CLI Banner, Disclaimer & Licensing Information ({isDark
          ? 'Dark Mode — White Crow Emblem'
          : 'Light Mode — Dark/Glow Crow Emblem'})"
        aria-label="Open C.O.R.A. Banner, Disclaimer, and Licensing Information"
      >
        <img
          src={crowLogoUrl}
          alt="CROW Emblem"
          class="h-full w-auto max-h-12 object-contain block select-none transition-transform duration-200"
          style="filter: drop-shadow(0 0 8px {isoTheme.outlineGlow});"
        />
      </button>

      <div class="flex flex-col justify-center min-w-0">
        <div class="flex items-center gap-2 flex-wrap">
          <span class="font-extrabold tracking-wider text-sm sm:text-base {isDark ? 'text-white' : 'text-slate-950'}">
            C.O.R.A.
          </span>
          <span class="text-[11px] {isDark ? 'text-slate-300' : 'text-slate-600'} hidden xl:inline">
            Cyber Oriented Reasoning Agent
          </span>
          <span
            class="text-[10px] font-mono px-1.5 py-0.5 rounded border {isDark
              ? 'bg-slate-900/90 text-cyan-300 border-cyan-500/40'
              : 'bg-white/90 text-cyan-800 border-cyan-600/40 font-semibold'}"
          >
            v{versionStr}
          </span>
        </div>
        <div class="flex items-center gap-1.5 mt-0.5 flex-wrap">
          <span class="text-[10px] font-mono px-1.5 py-0.5 rounded border {isoTheme.badgeClass}">
            {posture?.hud_badge || `NET:${postureColor}`}
          </span>
          <span
            class="text-[10px] font-mono px-1.5 py-0.5 rounded border {isDark
              ? 'bg-slate-900/90 border-slate-700 text-amber-300'
              : 'bg-amber-50 border-amber-400 text-amber-900 font-semibold'}"
          >
            {activeModeInfo?.badge || `MODE:${sessionMode.toUpperCase()}`}
          </span>
          <span
            class="text-[10px] font-mono px-1.5 py-0.5 rounded border hidden sm:inline-block {isDark
              ? 'bg-slate-900/90 border-slate-700 text-emerald-300'
              : 'bg-emerald-50 border-emerald-400 text-emerald-900 font-semibold'}"
          >
            PROJECT: {activeProject || 'NONE'}
          </span>
        </div>
      </div>
    </div>

    <!-- Center: Live psutil + NVIDIA NVML + Stacked/Scrollable Per-Interface NET Telemetry Strip -->
    {#if hardware}
      <div class="hidden md:flex items-center gap-1.5 text-[11px] font-mono min-w-0 flex-1 justify-center">
        <!-- CPU -->
        <div
          class="px-2 py-1 rounded border flex items-center gap-1.5 shrink-0 {isDark
            ? 'bg-slate-950/90 border-slate-700/80'
            : 'bg-white/95 border-slate-300 shadow-sm'}"
        >
          <span class={isDark ? 'text-slate-400' : 'text-slate-600'}>CPU</span>
          <span
            class="font-semibold {hardware.cpu.utilization_pct > 80
              ? 'text-rose-500'
              : isDark
              ? 'text-cyan-300'
              : 'text-cyan-700'}"
          >
            {hardware.cpu.utilization_pct.toFixed(0)}%
          </span>
          <div class="w-8 h-1.5 {isDark ? 'bg-slate-800' : 'bg-slate-200'} rounded overflow-hidden hidden xl:block">
            <div class="h-full bg-cyan-500" style="width: {Math.min(100, hardware.cpu.utilization_pct)}%"></div>
          </div>
        </div>

        <!-- RAM -->
        <div
          class="px-2 py-1 rounded border flex items-center gap-1.5 shrink-0 {isDark
            ? 'bg-slate-950/90 border-slate-700/80'
            : 'bg-white/95 border-slate-300 shadow-sm'}"
        >
          <span class={isDark ? 'text-slate-400' : 'text-slate-600'}>RAM</span>
          <span class="font-semibold {isDark ? 'text-emerald-300' : 'text-emerald-700'}">
            {hardware.ram.used_gb.toFixed(1)}/{hardware.ram.total_gb.toFixed(0)}G
          </span>
          <span class="text-[10px] hidden xl:inline {isDark ? 'text-slate-400' : 'text-slate-500'}">
            ({hardware.ram.utilization_pct.toFixed(0)}%)
          </span>
        </div>

        <!-- NVIDIA GPU (NVML / nvidia-smi) -->
        {#if hardware.gpus && hardware.gpus.length > 0}
          {#each hardware.gpus as gpu}
            <div
              class="px-2 py-1 rounded border hidden lg:flex items-center gap-1.5 shrink-0 {isDark
                ? 'bg-slate-950/90 border-emerald-500/40'
                : 'bg-white/95 border-emerald-500/60 shadow-sm'}"
            >
              <span class="font-semibold {isDark ? 'text-emerald-400' : 'text-emerald-700'}" title="{gpu.name} ({gpu.source})">
                GPU{gpu.index}
              </span>
              <span class={isDark ? 'text-white' : 'text-slate-900 font-semibold'}>{gpu.utilization_pct.toFixed(0)}%</span>
              <span class={isDark ? 'text-amber-300' : 'text-amber-700 font-semibold'}>
                {(gpu.vram_used_mb / 1024).toFixed(1)}/{(gpu.vram_total_mb / 1024).toFixed(1)}G
              </span>
              <span class="text-[10px] {gpu.temperature_c > 80 ? 'text-rose-500' : isDark ? 'text-slate-400' : 'text-slate-600'}">
                {gpu.temperature_c}°C
              </span>
            </div>
          {/each}
        {/if}

        <!-- DISK -->
        <div
          class="px-2 py-1 rounded border hidden xl:flex items-center gap-1.5 shrink-0 {isDark
            ? 'bg-slate-950/90 border-slate-700/80'
            : 'bg-white/95 border-slate-300 shadow-sm'}"
        >
          <span class={isDark ? 'text-slate-400' : 'text-slate-600'}>DISK</span>
          <span class="font-semibold {isDark ? 'text-slate-200' : 'text-slate-800'}">
            {hardware.disk.utilization_pct.toFixed(0)}%
          </span>
        </div>

        <!-- NET Display: "Interface name | IP/mask | upload/download speed" -->
        <!-- Stacked in rows within the header with a vertical scroll option when multiple NICs/IPs exist -->
        <div
          class="px-2.5 py-1 rounded border flex items-center gap-2 min-w-0 max-w-[460px] {isDark
            ? 'bg-slate-950/95 border-cyan-500/45 shadow-inner'
            : 'bg-white/95 border-sky-400 shadow-sm'}"
          title="Active Host Network Interfaces (Interface name | IP/mask | Upload / Download Speed). Scroll to inspect all NICs & IPs."
        >
          <div class="flex flex-col items-center justify-center shrink-0 pr-1 border-r {isDark ? 'border-slate-800' : 'border-slate-200'}">
            <span class="text-[10px] font-bold tracking-wider {isDark ? 'text-cyan-400' : 'text-sky-700'}">NET</span>
            {#if headerNetRows.length > 1}
              <span class="text-[9px] leading-none {isDark ? 'text-slate-400' : 'text-slate-500'}" title="{headerNetRows.length} active NIC/IP rows (scrollable)">
                {headerNetRows.length}↕
              </span>
            {/if}
          </div>

          <div
            class="max-h-[46px] overflow-y-auto pr-1 space-y-0.5 select-text divide-y {isDark
              ? 'divide-slate-800/80'
              : 'divide-slate-200/80'}"
          >
            {#each headerNetRows as row}
              <div
                class="flex items-center gap-1.5 text-[10.5px] leading-tight whitespace-nowrap pt-0.5 first:pt-0 {row.isAllowed
                  ? ''
                  : 'opacity-55'}"
              >
                <span
                  class="font-bold truncate max-w-[140px] {row.isLoopback
                    ? isDark
                      ? 'text-slate-300'
                      : 'text-slate-700'
                    : isDark
                    ? 'text-cyan-300'
                    : 'text-sky-800'}"
                  title={row.ifaceName}
                >
                  {row.ifaceName}
                </span>
                <span class={isDark ? 'text-slate-500' : 'text-slate-400'}>|</span>
                <span class="font-semibold {isDark ? 'text-emerald-300' : 'text-emerald-700'}">
                  {row.ipMask}
                </span>
                <span class={isDark ? 'text-slate-500' : 'text-slate-400'}>|</span>
                <span class={isDark ? 'text-amber-300' : 'text-amber-700'} title="Upload Speed (TX)">
                  ↑{row.txStr}
                </span>
                <span class={isDark ? 'text-sky-300' : 'text-sky-700'} title="Download Speed (RX)">
                  ↓{row.rxStr}
                </span>
              </div>
            {/each}
          </div>
        </div>
      </div>
    {/if}

    <!-- Right: Dark/Light Mode Toggle + Model Server Badges + SYSINTERNALS Badge + Settings Gear Button -->
    <div class="flex items-center gap-1.5 text-xs shrink-0">
      <!-- Dark / Light Mode Toggle Button (Switches White vs Dark/Glow Crow Emblem) -->
      <button
        type="button"
        on:click={toggleThemeMode}
        class="px-2.5 py-1 rounded font-mono text-[11px] font-bold border transition-all flex items-center gap-1 {isDark
          ? 'bg-slate-900/95 border-slate-500/80 text-white hover:bg-slate-800 shadow-sm'
          : 'bg-white border-slate-400 text-slate-900 hover:bg-slate-100 shadow-sm'}"
        title="Toggle Dark / Light Mode (Switches between White Crow Emblem in Dark Mode and Glow Crow Emblem in Light Mode)"
      >
        <span>{isDark ? '🌙 Dark' : '☀️ Light'}</span>
      </button>

      <button
        type="button"
        on:click={() => handleStartOrRestartLlm(!llamaServerStatus.online)}
        disabled={startingLlm}
        class="hidden sm:inline-block px-2 py-1 rounded font-mono text-[11px] border transition-colors {llamaServerStatus.online
          ? isDark
            ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300 hover:bg-emerald-900/80'
            : 'bg-emerald-100 border-emerald-500 text-emerald-900 font-semibold hover:bg-emerald-200'
          : llamaServerStatus.state === 'loading' || startingLlm
          ? isDark
            ? 'bg-amber-950/80 border-amber-500/50 text-amber-300 animate-pulse'
            : 'bg-amber-100 border-amber-500 text-amber-900 font-semibold animate-pulse'
          : isDark
          ? 'bg-slate-900/90 border-slate-700 text-slate-400 hover:bg-slate-800'
          : 'bg-white/90 border-slate-300 text-slate-600 hover:bg-slate-100'}"
        title="llama-server ({llamaServerStatus.api_url}) — Active: {llamaServerStatus.active_model || selectedModel}. Click to start/reload."
      >
        llama.cpp: {llamaServerStatus.online
          ? 'ONLINE'
          : llamaServerStatus.state === 'loading' || startingLlm
          ? 'LOADING...'
          : 'STANDBY'}
      </button>

      <span
        class="hidden 2xl:inline-block px-2 py-1 rounded font-mono text-[11px] border {ollamaStatus.online
          ? isDark
            ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300'
            : 'bg-emerald-100 border-emerald-500 text-emerald-900 font-semibold'
          : isDark
          ? 'bg-slate-900/90 border-slate-700 text-slate-400'
          : 'bg-white/90 border-slate-300 text-slate-600'}"
        title="Ollama ({ollamaStatus.api_url})"
      >
        Ollama: {ollamaStatus.online ? `ONLINE (${ollamaStatus.model_count})` : 'OFFLINE'}
      </span>

      <span
        class="hidden sm:inline-block px-2.5 py-1 rounded font-mono text-[11px] font-semibold border {isDark
          ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300'
          : 'bg-emerald-100 border-emerald-500 text-emerald-900'}"
        title="{systemTools?.host_os === 'windows' ? 'Windows Sysinternals Suite installed and ready' : 'System Tactical Utilities installed and ready'}"
      >
        {systemTools?.host_os === 'linux' ? 'SYS TOOLS: INSTALLED' : 'SYSINTERNALS: INSTALLED'}
      </span>

      <!-- Settings Gear Button (Right of "SYSINTERNALS: INSTALLED") -->
      <button
        type="button"
        on:click={() => (showSettingsModal = true)}
        class="px-2.5 py-1 rounded font-mono text-xs font-bold border transition-all flex items-center gap-1 cursor-pointer {isDark
          ? 'bg-slate-900/95 hover:bg-slate-800 border-cyan-500/50 text-cyan-300 shadow-sm'
          : 'bg-white hover:bg-slate-100 border-sky-500 text-sky-900 shadow-sm'}"
        title="Open Dashboard Display & Font Customization Settings (Font Style, Color, Size & Workspace Layout)"
        aria-label="Open Dashboard Display and Font Customization Settings"
      >
        <span class="text-sm leading-none">⚙️</span>
        <span class="hidden xl:inline text-[11px]">Settings</span>
      </button>
    </div>
  </header>

  <!-- Toast / Error Notifications -->
  {#if errorBanner}
    <div
      class="w-full px-4 py-1.5 text-xs flex items-center justify-between border-b shrink-0 {isDark
        ? 'bg-rose-950/95 border-rose-500/60 text-rose-200'
        : 'bg-rose-100 border-rose-400 text-rose-900 font-medium'}"
    >
      <span><strong>Error:</strong> {errorBanner}</span>
      <button class="font-bold hover:opacity-75" on:click={() => (errorBanner = '')}>✕</button>
    </div>
  {/if}
  {#if statusToast}
    <div
      class="w-full px-4 py-1 text-xs flex items-center justify-between border-b shrink-0 {isDark
        ? 'bg-cyan-950/90 border-cyan-500/50 text-cyan-200'
        : 'bg-cyan-100 border-cyan-400 text-cyan-900 font-medium'}"
    >
      <span>✓ {statusToast}</span>
      <button class="hover:opacity-75" on:click={() => (statusToast = '')}>✕</button>
    </div>
  {/if}

  <!-- ===================================================================== -->
  <!-- 2. FULL-WIDTH ENTERPRISE WORKSPACE: RESULTS WINDOW + CONTROL DECK     -->
  <!--    - Zero outer margin/gap in Flush mode (docks edge-to-edge)         -->
  <!-- ===================================================================== -->
  <main
    class="flex-1 flex flex-col w-full min-h-0 overflow-hidden {isFlushLayout ? 'p-0 gap-0' : 'p-1.5 gap-1.5'}"
  >
    <!-- TOP DISPLAY WINDOW FOR RESULTS (100% Full Observable Width & Height, Docked Flush) -->
    <section
      bind:this={resultsContainerEl}
      class="flex-1 w-full flex flex-col overflow-y-auto select-text transition-all duration-200 {isFlushLayout
        ? 'rounded-none'
        : 'rounded-lg'}"
      style="{isoTheme.resultsWindowStyle} {customTextStyle}"
    >
      <!-- Sticky Enterprise Results Display Header Bar -->
      <div
        class="sticky top-0 z-10 w-full flex flex-wrap items-center justify-between gap-2 px-4 py-2 border-b backdrop-blur-md shrink-0 {isDark
          ? 'bg-slate-950/90'
          : 'bg-white/95'}"
        style="border-color: {isoTheme.outlineHex}55;"
      >
        <div class="flex items-center gap-2.5 flex-wrap">
          <span class="w-2.5 h-2.5 rounded-full {wsConnected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}"></span>
          <h2 class="text-xs font-bold uppercase tracking-wider {isDark ? 'text-slate-200' : 'text-slate-800'}">
            Results & Tactical Output Display Window —
            <span class={isDark ? 'text-cyan-400' : 'text-cyan-700'}>Projects/{activeProject || 'None'}</span>
          </h2>
          <span class="text-[11px] font-mono px-2 py-0.5 rounded border {isoTheme.badgeClass}">
            ISOLATION: {postureColor}
            {#if isolationLevel === 'blue'}
              ({allowedInterfaces})
            {:else if isolationLevel === 'white'}
              (127.0.0.1 / lo ONLY)
            {:else}
              (UNRESTRICTED)
            {/if}
          </span>
          {#if activeGoal}
            <span
              class="text-xs font-mono px-2.5 py-0.5 rounded border {isDark
                ? 'bg-amber-950/70 border-amber-500/40 text-amber-200'
                : 'bg-amber-100 border-amber-400 text-amber-900'}"
            >
              Goal: "{activeGoal}"
            </span>
          {/if}
        </div>
        <div class="flex items-center gap-2 flex-wrap">
          <button
            type="button"
            on:click={toggleGlobalThinkingCtrlO}
            class="text-xs px-2.5 py-1 rounded border font-mono transition-colors flex items-center gap-1.5 {showThinkingExpanded
              ? isDark
                ? 'bg-amber-950/90 hover:bg-amber-900 text-amber-200 border-amber-400 font-semibold shadow-sm'
                : 'bg-amber-500 hover:bg-amber-600 text-white border-amber-700 font-semibold shadow-sm'
              : isDark
              ? 'bg-slate-900 hover:bg-slate-800 text-slate-300 border-slate-700'
              : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-300'}"
            title="Toggle LLM Thought Process & 15-Engine Trace visibility (Keyboard shortcut: Ctrl+O)"
          >
            <span>🧠 Thought Process (Ctrl+O): {showThinkingExpanded ? 'EXPANDED ▾' : 'HIDDEN ▸'}</span>
          </button>
          <button
            class="text-xs px-3 py-1 rounded border transition-colors disabled:opacity-50 {isDark
              ? 'bg-slate-800 hover:bg-slate-700 text-cyan-300 border-cyan-500/40'
              : 'bg-cyan-50 hover:bg-cyan-100 text-cyan-900 border-cyan-500/50 font-medium'}"
            disabled={generatingReport || !activeProject}
            on:click={handleGenerateReport}
          >
            {generatingReport ? 'Generating...' : 'Generate 5-Section Report'}
          </button>
          <button
            class="text-xs px-3 py-1 rounded border transition-colors {isDark
              ? 'bg-slate-900 hover:bg-rose-950/70 text-slate-300 hover:text-rose-200 border-slate-700'
              : 'bg-slate-100 hover:bg-rose-100 text-slate-700 hover:text-rose-900 border-slate-300'}"
            on:click={handleClearHistory}
          >
            Clear Display
          </button>
        </div>
      </div>

      <!-- Results Body Container -->
      <div class="flex-1 flex flex-col px-4 py-3 space-y-3">
        {#if messages.length === 0 && !submittingQuery && !executingCommand && !generatingReport}
          <!-- Full-Height Enterprise Empty State Workspace (Fills window cleanly with zero awkward gap) -->
          <div
            class="flex-1 w-full rounded-lg p-5 flex flex-col justify-between gap-4 {isDark
              ? 'bg-slate-900/65'
              : 'bg-slate-50/90'}"
            style={isoTheme.cardOutlineStyle}
          >
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div class="flex items-center gap-4">
                <button
                  type="button"
                  on:click={() => (showBannerModal = true)}
                  class="shrink-0 cursor-pointer focus:outline-none hover:scale-105 active:scale-95 transition-transform duration-150"
                  title="Click to view C.O.R.A. CLI Banner, Disclaimer & Licensing Information"
                  aria-label="Open C.O.R.A. Banner, Disclaimer, and Licensing Information"
                >
                  <img src={crowLogoUrl} alt="CROW Emblem" class="h-14 w-auto object-contain shrink-0" />
                </button>
                <div>
                  <h3 class="text-base sm:text-lg font-bold {isDark ? 'text-white' : 'text-slate-900'}">
                    C.O.R.A. Enterprise Tactical Workstation Ready ({isDark ? 'Dark Mode' : 'Light Mode'} • {postureColor} Isolation)
                  </h3>
                  <p class="text-xs {isDark ? 'text-slate-300' : 'text-slate-600'} mt-0.5">
                    Results from operator queries, local LLM inference (<code>{selectedModel}</code>), and host shell probes for
                    <strong>{activeProject ? `Projects/${activeProject}/` : 'your selected project'}</strong> render directly in this workspace.
                    Press <kbd class="px-1.5 py-0.5 rounded border font-mono text-[11px] {isDark ? 'bg-slate-800 border-slate-600 text-amber-300' : 'bg-amber-50 border-amber-400 text-amber-900'}">Ctrl+O</kbd> anytime to expand or collapse C.O.R.A.'s internal thought process &amp; engine trace.
                  </p>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <button
                  type="button"
                  on:click={() => (showSettingsModal = true)}
                  class="px-3 py-1.5 rounded border text-xs font-mono font-semibold transition-colors {isDark
                    ? 'bg-slate-950/90 hover:bg-slate-800 border-cyan-500/40 text-cyan-300'
                    : 'bg-white hover:bg-slate-100 border-sky-400 text-sky-900'}"
                >
                  ⚙️ Customize Font &amp; Display
                </button>
              </div>
            </div>

            <!-- Live Enterprise Readiness Status Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 text-xs font-mono">
              <div
                class="p-3 rounded border {isDark
                  ? 'bg-slate-950/80 border-slate-800'
                  : 'bg-white border-slate-200 shadow-sm'}"
              >
                <div class="text-[10px] uppercase tracking-wider opacity-70">Active Project Vault</div>
                <div class="font-bold mt-0.5 truncate {isDark ? 'text-emerald-300' : 'text-emerald-700'}">
                  {activeProject ? `Projects/${activeProject}/` : 'Select or Create Project'}
                </div>
                <div class="text-[10px] opacity-75 mt-0.5">
                  Local <code>Files/</code>: {(projectFilesPayload?.files_dir_items || []).length} item(s) ready
                </div>
              </div>

              <div
                class="p-3 rounded border {isDark
                  ? 'bg-slate-950/80 border-slate-800'
                  : 'bg-white border-slate-200 shadow-sm'}"
              >
                <div class="text-[10px] uppercase tracking-wider opacity-70">Session Mode &amp; Posture</div>
                <div class="font-bold mt-0.5 {isDark ? 'text-amber-300' : 'text-amber-700'}">
                  {sessionMode.toUpperCase()} • {postureColor}
                </div>
                <div class="text-[10px] opacity-75 mt-0.5">
                  {isolationLevel === 'blue'
                    ? `Locked NICs: ${allowedInterfaces}`
                    : isolationLevel === 'white'
                    ? 'Air-Gapped Loopback Only'
                    : 'Full Host & Network Access'}
                </div>
              </div>

              <div
                class="p-3 rounded border {isDark
                  ? 'bg-slate-950/80 border-slate-800'
                  : 'bg-white border-slate-200 shadow-sm'}"
              >
                <div class="text-[10px] uppercase tracking-wider opacity-70">Inference Engine</div>
                <div class="font-bold mt-0.5 truncate {isDark ? 'text-cyan-300' : 'text-cyan-700'}">
                  {selectedModel} ({inferenceProvider})
                </div>
                <div class="text-[10px] opacity-75 mt-0.5">
                  Status: {llamaServerStatus.online || ollamaStatus.online ? 'ONLINE & READY' : 'STANDBY'}
                </div>
              </div>

              <div
                class="p-3 rounded border {isDark
                  ? 'bg-slate-950/80 border-slate-800'
                  : 'bg-white border-slate-200 shadow-sm'}"
              >
                <div class="text-[10px] uppercase tracking-wider opacity-70">Active Network Interfaces</div>
                <div class="font-bold mt-0.5 truncate {isDark ? 'text-sky-300' : 'text-sky-700'}">
                  {headerNetRows.length} Active NIC/IP {headerNetRows.length === 1 ? 'Row' : 'Rows'}
                </div>
                <div class="text-[10px] opacity-75 mt-0.5 truncate">
                  Primary: {headerNetRows[0] ? `${headerNetRows[0].ifaceName} (${headerNetRows[0].ipMask})` : 'Detecting...'}
                </div>
              </div>
            </div>
          </div>
        {:else}
          {#each messages as msg, msgIdx}
            {@const msgKey = String(msg.id || `${msg.created_at || ''}-${msgIdx}`)}
            {@const parsedMsg = msg.role === 'assistant' ? extractCleanDisplayAndThinking(msg) : { cleanContent: msg.content, combinedThinking: '' }}
            {@const msgThinkingExpanded = isMessageThinkingExpanded(msgKey, showThinkingExpanded, expandedMessageMap)}
            <div
              class="w-full rounded-lg p-3.5 space-y-2.5 transition-all"
              style={msg.role === 'user'
                ? isDark
                  ? 'background: #0d1526; border: 1.5px solid rgba(56, 189, 248, 0.50); border-left: 6px solid #38bdf8; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);'
                  : 'background: #e0f2fe; border: 1.5px solid #38bdf8; border-left: 6px solid #0284c7; box-shadow: 0 2px 8px rgba(2, 132, 199, 0.08);'
                : isDark
                ? 'background: linear-gradient(180deg, #334663 0%, #293952 100%); border: 1.5px solid rgba(52, 211, 153, 0.80); border-left: 6px solid #10b981; box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);'
                : 'background: #ffffff; border: 1.5px solid #10b981; border-left: 6px solid #059669; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);'}
            >
              <!-- Message Meta Header (High-Contrast Role Identification) -->
              <div
                class="flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono pb-2 border-b {msg.role === 'user'
                  ? isDark
                    ? 'text-slate-300 border-sky-500/30'
                    : 'text-slate-700 border-sky-300'
                  : isDark
                  ? 'text-slate-100 border-emerald-400/35'
                  : 'text-slate-800 border-emerald-200'}"
              >
                <div class="flex items-center gap-2 flex-wrap">
                  <span
                    class="px-2.5 py-0.5 rounded font-extrabold tracking-wide border shadow-sm {msg.role === 'user'
                      ? isDark
                        ? 'bg-sky-950 text-sky-200 border-sky-400'
                        : 'bg-sky-700 text-white border-sky-800'
                      : isDark
                      ? 'bg-emerald-500 text-slate-950 border-emerald-300'
                      : 'bg-emerald-600 text-white border-emerald-700'}"
                  >
                    {msg.role === 'user'
                      ? '👤 OPERATOR QUERY'
                      : msg.model_used === 'Host Shell Probe'
                      ? '⚡ COMMAND PROBE OUTPUT'
                      : '🤖 C.O.R.A. OUTPUT'}
                  </span>
                  <span class="font-semibold {isDark ? 'text-white' : 'text-slate-900'}">
                    Project: {msg.project_slug}
                  </span>
                  <span>•</span>
                  <span>Mode: {msg.mode_key?.toUpperCase()}</span>
                  <span>•</span>
                  <span>Posture: {msg.posture_level}</span>
                </div>
                <div class="flex items-center gap-2 flex-wrap">
                  {#if msg.model_used}
                    <span
                      class="px-2 py-0.5 rounded border text-[10px] font-semibold {isDark
                        ? 'bg-slate-900/75 text-cyan-200 border-cyan-400/40'
                        : 'bg-slate-100 text-cyan-900 border-slate-300'}"
                    >
                      {msg.model_used}
                    </span>
                  {/if}
                  {#if msg.latency_ms}
                    <span class="font-semibold {isDark ? 'text-emerald-300' : 'text-emerald-700'}">
                      {(msg.latency_ms / 1000).toFixed(2)}s
                    </span>
                  {/if}
                  <span class="opacity-85">{msg.created_at || ''}</span>
                </div>
              </div>

              <!-- Antigravity-Style "Ctrl+O" Collapsible Thought Process & Engine Trace Bar (Hidden by Default) -->
              {#if msg.role === 'assistant' && parsedMsg.combinedThinking}
                <div
                  class="rounded-md border overflow-hidden transition-all {isDark
                    ? 'bg-slate-900/75 border-amber-400/40'
                    : 'bg-amber-50/90 border-amber-300'}"
                >
                  <button
                    type="button"
                    on:click={() => toggleSingleMessageThinking(msgKey)}
                    class="w-full px-3 py-1.5 flex flex-wrap items-center justify-between gap-2 text-left text-xs font-mono cursor-pointer transition-colors {isDark
                      ? 'hover:bg-slate-800/80 text-amber-200'
                      : 'hover:bg-amber-100/80 text-amber-900'}"
                    title="Press Ctrl+O or click to expand/collapse C.O.R.A.'s internal thought process and 15-Engine verification trace"
                  >
                    <div class="flex items-center gap-2">
                      <span class="text-sm leading-none">{msgThinkingExpanded ? '▾' : '▸'}</span>
                      <span class="font-semibold">
                        🧠 Thought &amp; processed{msg.latency_ms ? ` for ${(msg.latency_ms / 1000).toFixed(1)}s` : ''}
                      </span>
                    </div>
                    <span
                      class="text-[10.5px] px-2 py-0.5 rounded border {isDark
                        ? 'bg-slate-950/90 border-amber-400/40 text-amber-300'
                        : 'bg-white border-amber-400 text-amber-900 font-semibold'}"
                    >
                      Press Ctrl+O to {msgThinkingExpanded ? 'collapse' : 'expand'} thought process
                    </span>
                  </button>

                  {#if msgThinkingExpanded}
                    <div
                      class="px-3 py-2.5 border-t {isDark
                        ? 'bg-slate-950/90 border-slate-800 text-slate-300'
                        : 'bg-white border-amber-200 text-slate-700'}"
                    >
                      <pre
                        class="whitespace-pre-wrap font-mono text-[11px] leading-relaxed overflow-x-auto select-text">{parsedMsg.combinedThinking}</pre>
                    </div>
                  {/if}
                </div>
              {/if}

              <!-- Main Message Content (Lighter Surface for C.O.R.A. Output + High Contrast Text) -->
              <div
                class="rounded-md px-3.5 py-2.5 whitespace-pre-wrap overflow-x-auto {msg.role === 'user'
                  ? isDark
                    ? 'bg-slate-950/60 text-sky-100'
                    : 'bg-white/90 text-slate-900'
                  : isDark
                  ? 'bg-slate-800/85 text-white border border-slate-500/40 shadow-inner'
                  : 'bg-slate-50 text-slate-950 border border-slate-200'}"
                style={customTextStyle}
              >
                {parsedMsg.cleanContent}
              </div>

              <!-- Actionable Consensus Command Pill (If present) -->
              {#if msg.reasoning && msg.reasoning.consensus_immediate_action}
                <div
                  class="mt-1 pt-2 border-t flex flex-wrap items-center justify-between gap-2 text-xs font-mono {isDark
                    ? 'border-slate-600/60'
                    : 'border-slate-200'}"
                >
                  <div class="flex items-center gap-2 min-w-0">
                    <span class="{isDark ? 'text-emerald-200 font-semibold' : 'text-slate-700 font-semibold'} shrink-0">
                      Recommended Next Probe:
                    </span>
                    <code
                      class="px-2 py-0.5 rounded border truncate {isDark
                        ? 'text-emerald-200 bg-slate-900/90 border-emerald-400/50'
                        : 'text-emerald-900 bg-emerald-50 border-emerald-400'}"
                    >
                      {msg.reasoning.consensus_immediate_action}
                    </code>
                  </div>
                  <div class="flex items-center gap-2 shrink-0">
                    <button
                      class="px-2.5 py-1 rounded border text-[11px] font-semibold {isDark
                        ? 'bg-slate-900 hover:bg-slate-800 text-cyan-200 border-cyan-400/50'
                        : 'bg-cyan-50 hover:bg-cyan-100 text-cyan-900 border-cyan-400'}"
                      on:click={() => {
                        commandToExecute = msg.reasoning?.consensus_immediate_action || '';
                      }}
                    >
                      Load into Probe
                    </button>
                    <button
                      class="px-2.5 py-1 rounded border text-[11px] font-semibold {isDark
                        ? 'bg-emerald-600 hover:bg-emerald-500 text-white border-emerald-400'
                        : 'bg-emerald-600 hover:bg-emerald-500 text-white border-emerald-700'}"
                      disabled={executingCommand || sessionMode === 'analyst'}
                      on:click={() => runQuickCommand(msg.reasoning?.consensus_immediate_action || '')}
                    >
                      Run Command Now
                    </button>
                  </div>
                </div>
              {/if}
            </div>
          {/each}
        {/if}

        <!-- Live Antigravity-Style Thinking / Processing Status Card in C.O.R.A. Output Pane -->
        {#if submittingQuery || executingCommand || generatingReport}
          <div
            class="w-full rounded-lg p-3.5 space-y-2.5 transition-all"
            style={isDark
              ? 'background: linear-gradient(180deg, #334663 0%, #293952 100%); border: 1.5px solid #f59e0b; border-left: 6px solid #f59e0b; box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);'
              : 'background: #fffbeb; border: 1.5px solid #f59e0b; border-left: 6px solid #d97706; box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);'}
          >
            <button
              type="button"
              on:click={toggleGlobalThinkingCtrlO}
              class="w-full flex flex-wrap items-center justify-between gap-2 text-left font-mono text-xs cursor-pointer"
              title="Press Ctrl+O or click to expand/collapse C.O.R.A.'s live thinking process"
            >
              <div class="flex items-center gap-2.5">
                <span
                  class="animate-spin h-4 w-4 border-2 border-amber-400 border-t-transparent rounded-full shrink-0"
                ></span>
                <span
                  class="px-2 py-0.5 rounded font-extrabold tracking-wide border {isDark
                    ? 'bg-amber-400 text-slate-950 border-amber-200'
                    : 'bg-amber-600 text-white border-amber-700'}"
                >
                  🧠 C.O.R.A. THINKING / PROCESSING
                </span>
                <span class="font-bold {isDark ? 'text-white' : 'text-slate-900'}">
                  {activeProcessingLabel || 'Thinking & processing...'} ({processingElapsedSec.toFixed(1)}s)
                </span>
              </div>

              <span
                class="px-2.5 py-1 rounded border text-[11px] font-bold {isDark
                  ? 'bg-slate-950/90 border-amber-400/60 text-amber-200'
                  : 'bg-white border-amber-500 text-amber-900'}"
              >
                Press Ctrl+O to {showThinkingExpanded ? 'collapse ▾' : 'expand thought process ▸'}
              </span>
            </button>

            {#if showThinkingExpanded}
              <div
                class="rounded-md p-3 border font-mono text-[11px] space-y-1.5 {isDark
                  ? 'bg-slate-950/90 border-slate-700 text-slate-200'
                  : 'bg-white border-amber-300 text-slate-800'}"
              >
                <div class="font-bold {isDark ? 'text-amber-300' : 'text-amber-800'}">
                  === LIVE THOUGHT PROCESS &amp; ENGINE PIPELINE (Ctrl+O Expanded) ===
                </div>
                {#if activeProcessingDetail}
                  <div>• {activeProcessingDetail}</div>
                {/if}
                <div>
                  • [Stage 1] Inspecting active workspace vault (<code>Projects/{activeProject}/</code> &amp; <code>Projects/{activeProject}/Files/</code>)
                </div>
                <div>
                  • [Stage 2] Verifying network isolation guardrails (<code>{postureColor}</code> posture • <code>{sessionMode.toUpperCase()}</code> mode)
                </div>
                <div>
                  • [Stage 3] Running local LLM chain-of-thought reasoning (<code>{selectedModel}</code> via <code>{inferenceProvider}</code>) &amp; background 15-Engine verification...
                </div>
              </div>
            {/if}
          </div>
        {/if}
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 3. BOTTOM ENTERPRISE CONTROL DECK (CLI SELECTORS + QUERY INPUT)     -->
    <!--    - Docked flush edge-to-edge with zero outer gap                  -->
    <!-- =================================================================== -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <section
      on:dragover={handleConsoleDragOver}
      on:dragleave={handleConsoleDragLeave}
      on:drop={handleConsoleDrop}
      class="w-full shrink-0 {isFlushLayout
        ? 'rounded-none px-4 py-2.5 space-y-2'
        : 'rounded-lg px-4 py-2.5 space-y-2'} z-10 transition-all duration-200 relative"
      style="{isoTheme.controlDeckStyle} {isDraggingFilesOverConsole ? 'border: 2px solid #22d3ee;' : ''}"
    >
      {#if isDraggingFilesOverConsole}
        <div
          class="absolute inset-0 z-40 rounded-xl bg-cyan-950/90 border-2 border-dashed border-cyan-400 flex flex-col items-center justify-center gap-1 text-cyan-100 pointer-events-none"
        >
          <div class="text-base font-bold font-mono">
            📥 Drop File(s) to Upload into <code>Projects/{activeProject}/Files/</code>
          </div>
          <div class="text-xs font-mono text-cyan-300">
            Dropped scripts, configs, and files are saved directly in <code>Projects/{activeProject}/Files/</code> for LLM inspection &amp; execution
          </div>
        </div>
      {/if}
      <!-- Row B: CLI-Equivalent Dropdown Selectors (Projects, Mode, Network Isolation, Model) -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 text-xs">
        <!-- 1. Project Selector Dropdown (`[1..N]`, `[N+1] Rename`, `[N+2] CREATE NEW`) -->
        <div class="flex flex-col gap-1">
          <label
            for="cora-project-select"
            class="text-[10px] font-mono uppercase tracking-wider flex justify-between {isDark
              ? 'text-slate-300'
              : 'text-slate-700 font-semibold'}"
          >
            <span>1. Project (<code>Projects/</code>)</span>
            <span class={isDark ? 'text-cyan-400' : 'text-cyan-700'}>{activeProject || 'Select / Create'}</span>
          </label>
          <select
            id="cora-project-select"
            bind:value={projectDropdownValue}
            on:change={handleProjectDropdownChange}
            class="w-full rounded-lg border px-2.5 py-1.5 text-xs font-mono focus:outline-none {isDark
              ? 'bg-slate-900 border-slate-700 text-white focus:border-cyan-400'
              : 'bg-white border-slate-300 text-slate-900 focus:border-cyan-600'}"
          >
            {#if !activeProject}
              <option value="" disabled>-- Select or Create a Project --</option>
            {/if}
            {#each projects as p}
              <option value={p.slug}>
                [{p.menu_number}] {p.slug}
              </option>
            {/each}
            {#if activeProject}
              <option value="__RENAME_CURRENT__">[{projects.length + 1}] Rename Current Project ({activeProject})...</option>
            {/if}
            <option value="__CREATE_NEW__">[{projects.length + (activeProject ? 2 : 1)}] + CREATE NEW PROJECT...</option>
          </select>
        </div>

        <!-- 2. Session Personality & Logic Mode (`[1] Default`, `[2] Analyst`, `[3] Berserker`, `[4] Ninja`) -->
        <div class="flex flex-col gap-1">
          <label
            for="cora-mode-select"
            class="text-[10px] font-mono uppercase tracking-wider flex justify-between {isDark
              ? 'text-slate-300'
              : 'text-slate-700 font-semibold'}"
          >
            <span>2. Personality & Logic Mode</span>
            <span class={isDark ? 'text-amber-300' : 'text-amber-700'}>{sessionMode.toUpperCase()}</span>
          </label>
          <select
            id="cora-mode-select"
            bind:value={sessionMode}
            on:change={syncSessionConfig}
            class="w-full rounded-lg border px-2.5 py-1.5 text-xs font-mono focus:outline-none {isDark
              ? 'bg-slate-900 border-slate-700 text-white focus:border-cyan-400'
              : 'bg-white border-slate-300 text-slate-900 focus:border-cyan-600'}"
          >
            {#each sessionModes as m}
              <option value={m.key}>[{m.number}] {m.label}</option>
            {/each}
          </select>
        </div>

        <!-- 3. Network Isolation Option (`Red`, `Blue` + Windows/Linux interfaces, `White` air-gapped) -->
        <div class="flex flex-col gap-1">
          <label
            for="cora-netiso-select"
            class="text-[10px] font-mono uppercase tracking-wider flex justify-between {isDark
              ? 'text-slate-300'
              : 'text-slate-700 font-semibold'}"
          >
            <span>3. Network Isolation (<code>-netiso</code>)</span>
            <span
              class="font-bold {isolationLevel === 'red'
                ? isDark
                  ? 'text-rose-400'
                  : 'text-rose-700'
                : isolationLevel === 'blue'
                ? isDark
                  ? 'text-sky-400'
                  : 'text-sky-700'
                : isDark
                ? 'text-white'
                : 'text-slate-900'}"
            >
              {isolationLevel.toUpperCase()}
            </span>
          </label>
          <div class="flex gap-1.5">
            <select
              id="cora-netiso-select"
              bind:value={isolationLevel}
              disabled={sessionMode === 'analyst'}
              on:change={syncSessionConfig}
              class="flex-1 rounded-lg border px-2.5 py-1.5 text-xs font-mono focus:outline-none disabled:opacity-60 {isDark
                ? 'bg-slate-900 border-slate-700 text-white'
                : 'bg-white border-slate-300 text-slate-900'}"
              style="border-color: {isoTheme.outlineHex};"
            >
              <option value="red" disabled={sessionMode === 'analyst'}>RED — Unrestricted (Full Host & WAN)</option>
              <option value="blue" disabled={sessionMode === 'analyst'}>BLUE — Interface-Locked (Subnets/NICs)</option>
              <option value="white" disabled={sessionMode === 'berserker' || sessionMode === 'ninja'}>
                WHITE — Air-Gapped Loopback (127.0.0.1 / lo)
              </option>
            </select>
            {#if isolationLevel === 'blue'}
              <input
                type="text"
                bind:value={allowedInterfaces}
                on:change={syncSessionConfig}
                placeholder="Wi-Fi,VMnet8"
                title="Allowed Blue Interfaces on Windows/Linux (comma-separated)"
                class="w-28 rounded-lg border px-2 py-1 text-xs font-mono focus:outline-none {isDark
                  ? 'bg-slate-900 border-sky-400 text-sky-200'
                  : 'bg-white border-sky-600 text-sky-900 font-semibold'}"
              />
            {/if}
          </div>
        </div>

        <!-- 4. Model Connection Selector (CORA GGUF Models + Ollama Models) -->
        <div class="flex flex-col gap-1">
          <label
            for="cora-model-select"
            class="text-[10px] font-mono uppercase tracking-wider flex justify-between {isDark
              ? 'text-slate-300'
              : 'text-slate-700 font-semibold'}"
          >
            <span>4. Model Connection (<code>-m</code>)</span>
            <span class={isDark ? 'text-emerald-400' : 'text-emerald-700'}>{inferenceProvider}</span>
          </label>
          <select
            id="cora-model-select"
            bind:value={selectedModel}
            on:change={syncSessionConfig}
            class="w-full rounded-lg border px-2.5 py-1.5 text-xs font-mono focus:outline-none {isDark
              ? 'bg-slate-900 border-slate-700 text-white focus:border-cyan-400'
              : 'bg-white border-slate-300 text-slate-900 focus:border-cyan-600'}"
          >
            {#each models as mod}
              <option value={mod.id}>
                {mod.name} [{mod.vram_est}] {mod.installed_on_disk ? '✓' : '(Download)'}
              </option>
            {/each}
          </select>
        </div>
      </div>

      <!-- Optional Row B2: Active Windows/Linux Host Interfaces Picker when BLUE Isolation is active -->
      {#if isolationLevel === 'blue' && hostInterfaces.length > 0}
        <div
          class="flex flex-wrap items-center gap-1.5 px-3 py-1.5 rounded-lg border text-[11px] font-mono {isDark
            ? 'bg-sky-950/40 border-sky-500/40 text-sky-200'
            : 'bg-sky-100/80 border-sky-400 text-sky-950'}"
        >
          <span class="font-bold mr-1">BLUE Allowed Host Interfaces (click to toggle):</span>
          {#each hostInterfaces as hif}
            {@const isAllowed = isInterfaceSelectedInBlue(hif.name)}
            <button
              type="button"
              on:click={() => toggleBlueInterfaceChip(hif.name)}
              class="px-2 py-0.5 rounded border transition-all flex items-center gap-1 {isAllowed
                ? isDark
                  ? 'bg-sky-500/30 border-cyan-300 text-white font-bold shadow-sm'
                  : 'bg-sky-600 border-sky-700 text-white font-bold shadow-sm'
                : isDark
                ? 'bg-slate-900/80 border-slate-700 text-slate-400 hover:text-slate-200'
                : 'bg-white/80 border-slate-300 text-slate-600 hover:text-slate-900'}"
              title="Toggle {hif.name} ({hif.subnets.join(', ')}) in BLUE Network Isolation"
            >
              <span>{isAllowed ? '🔒' : '○'}</span>
              <span>{hif.name}</span>
              {#if hif.subnets.length > 0}
                <span class="text-[10px] opacity-80">({hif.subnets[0]})</span>
              {/if}
            </button>
          {/each}
        </div>
      {/if}

      <!-- Row C: Secondary Switches (Goal, Command Probe, Auto-Run, Thinking) -->
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <div class="flex items-center gap-1.5 flex-1 min-w-[220px]">
          <span class="text-[11px] font-mono shrink-0 {isDark ? 'text-slate-400' : 'text-slate-600 font-semibold'}">
            /goal:
          </span>
          <input
            type="text"
            bind:value={activeGoal}
            on:change={syncSessionConfig}
            on:keydown={(e) => {
              if (e.key === 'Enter' && activeGoal.trim()) {
                e.preventDefault();
                handlePursueGoal();
              }
            }}
            placeholder="Set active project goal (Enter or click Pursue Goal to execute with LLM)..."
            class="w-full rounded border px-2.5 py-1 text-xs font-mono focus:outline-none {isDark
              ? 'bg-slate-900/90 border-slate-700 text-amber-200 focus:border-amber-400'
              : 'bg-white border-slate-300 text-amber-900 focus:border-amber-600'}"
          />
          {#if activeGoal.trim()}
            <button
              type="button"
              disabled={submittingQuery}
              on:click={handlePursueGoal}
              class="px-2.5 py-1 rounded text-[11px] font-mono border shrink-0 transition-colors disabled:opacity-50 {isDark
                ? 'bg-amber-950/90 border-amber-500/50 text-amber-200 hover:bg-amber-900'
                : 'bg-amber-500 border-amber-600 text-white font-semibold hover:bg-amber-600'}"
              title="Pursue Active Goal using LLM + 15-Engine Reasoning & Tactical Tools"
            >
              {submittingQuery ? 'Pursuing...' : '🎯 Pursue Goal'}
            </button>
          {/if}
        </div>

        <div class="flex items-center gap-1.5 flex-1 min-w-[260px] relative">
          <span class="text-[11px] font-mono shrink-0 {isDark ? 'text-slate-400' : 'text-slate-600 font-semibold'}">
            Command Probe:
          </span>

          <!-- Up/Down Command History Steppers -->
          <div class="flex items-center gap-0.5 shrink-0" title="Scroll previous commands (Up/Down Arrow)">
            <button
              type="button"
              disabled={commandHistory.length === 0 || sessionMode === 'analyst'}
              on:click={() => stepCommandHistory('up')}
              class="px-1.5 py-0.5 rounded text-[10px] font-mono border disabled:opacity-35 transition-colors {isDark
                ? 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
                : 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'}"
              title="Previous command (Up Arrow)"
            >
              ↑
            </button>
            <button
              type="button"
              disabled={cmdHistoryCursor === -1 || sessionMode === 'analyst'}
              on:click={() => stepCommandHistory('down')}
              class="px-1.5 py-0.5 rounded text-[10px] font-mono border disabled:opacity-35 transition-colors {isDark
                ? 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
                : 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'}"
              title="Next command (Down Arrow)"
            >
              ↓
            </button>
          </div>

          <div
            class="relative flex-1 rounded border overflow-hidden {isDark
              ? 'bg-slate-900/90 border-slate-700 focus-within:border-emerald-400'
              : 'bg-white border-slate-300 focus-within:border-emerald-600'}"
          >
            <!-- Shaded Inline Ghost-Text Autocomplete Backdrop for Command Probe -->
            {#if cmdAutocomplete.suffix && sessionMode !== 'analyst'}
              <div
                aria-hidden="true"
                class="absolute inset-0 px-2.5 py-1 text-xs font-mono whitespace-pre overflow-hidden pointer-events-none select-none flex items-center"
              >
                <span class="text-transparent">{commandToExecute}</span><span
                  class="rounded px-1 py-0.2 {isDark
                    ? 'bg-emerald-500/20 text-emerald-300/65 border border-emerald-500/35'
                    : 'bg-emerald-100 text-emerald-800/75 border border-emerald-300'}"
                >{cmdAutocomplete.suffix}</span><span
                  class="ml-1.5 text-[9px] px-1 py-0.2 rounded {isDark
                    ? 'bg-slate-800 text-slate-400 border border-slate-700'
                    : 'bg-slate-200 text-slate-600 border border-slate-300'}"
                >Tab ↹</span>
              </div>
            {/if}

            <input
              bind:this={cmdInputEl}
              type="text"
              bind:value={commandToExecute}
              on:input={handleCommandInputEvent}
              on:keydown={handleCommandKeydown}
              disabled={sessionMode === 'analyst'}
              placeholder={sessionMode === 'analyst'
                ? 'Disabled in Analyst (Read-Only) mode'
                : 'Optional host/Sysinternals command (↑/↓ history, Tab autocomplete)...'}
              class="relative z-10 w-full bg-transparent px-2.5 py-1 text-xs font-mono focus:outline-none disabled:opacity-50 {isDark
                ? 'text-emerald-300 placeholder-slate-500'
                : 'text-emerald-900 placeholder-slate-400'}"
            />
          </div>

          {#if cmdHistoryCursor >= 0}
            <span
              class="text-[10px] font-mono px-1.5 py-0.5 rounded shrink-0 {isDark
                ? 'bg-emerald-950/70 text-emerald-300 border border-emerald-500/30'
                : 'bg-emerald-50 text-emerald-800 border border-emerald-300'}"
            >
              Cmd {cmdHistoryCursor + 1}/{commandHistory.length}
            </span>
          {/if}

          {#if commandToExecute.trim() && sessionMode !== 'analyst'}
            <button
              type="button"
              class="px-2.5 py-1 rounded text-[11px] font-mono border shrink-0 {isDark
                ? 'bg-emerald-950 border-emerald-500/50 text-emerald-200 hover:bg-emerald-900'
                : 'bg-emerald-600 border-emerald-700 text-white hover:bg-emerald-500'}"
              disabled={executingCommand}
              on:click={() => runQuickCommand(commandToExecute)}
            >
              {executingCommand ? 'Running...' : 'Run Now'}
            </button>
          {/if}
        </div>

        <div class="flex items-center gap-2">
          <button
            type="button"
            class="px-2.5 py-1 rounded text-[11px] font-mono border {permissionMode === 'auto'
              ? isDark
                ? 'bg-rose-950/80 border-rose-500/60 text-rose-200'
                : 'bg-rose-600 border-rose-700 text-white font-semibold'
              : isDark
              ? 'bg-slate-900 border-slate-700 text-slate-300'
              : 'bg-white border-slate-300 text-slate-800'}"
            on:click={() => {
              permissionMode = permissionMode === 'auto' ? 'confirm' : 'auto';
              syncSessionConfig();
            }}
          >
            Tools: {permissionMode === 'auto' ? 'AUTO-RUN' : 'CONFIRM'}
          </button>

          <button
            type="button"
            class="px-2.5 py-1 rounded text-[11px] font-mono border {thinkingEnabled
              ? isDark
                ? 'bg-amber-950/80 border-amber-500/60 text-amber-200'
                : 'bg-amber-500 border-amber-600 text-white font-semibold'
              : isDark
              ? 'bg-slate-900 border-slate-700 text-slate-400'
              : 'bg-white border-slate-300 text-slate-600'}"
            on:click={() => {
              thinkingEnabled = !thinkingEnabled;
              syncSessionConfig();
            }}
          >
            --think: {thinkingEnabled ? 'ON' : 'OFF'}
          </button>
        </div>
      </div>

      <!-- Command Probe Shaded Autocomplete Pills (when typing in Command Probe) -->
      {#if cmdAutocomplete.matches.length > 0 && sessionMode !== 'analyst'}
        <div
          class="flex items-center gap-1.5 flex-wrap px-2.5 py-1 rounded-lg border text-[11px] font-mono {isDark
            ? 'bg-slate-900/90 border-emerald-500/30 text-slate-300'
            : 'bg-emerald-50/70 border-emerald-300 text-slate-700'}"
        >
          <span class="text-[10px] uppercase tracking-wider font-semibold {isDark ? 'text-emerald-400' : 'text-emerald-700'}">
            Cmd Autocomplete (Tab ↹):
          </span>
          {#each cmdAutocomplete.matches as match}
            <button
              type="button"
              on:click={() => acceptCommandAutocomplete(match)}
              class="px-2 py-0.5 rounded border transition-all text-xs font-mono {match === cmdAutocomplete.activeCandidate
                ? isDark
                  ? 'bg-emerald-950 border-emerald-400 text-emerald-200 shadow-sm'
                  : 'bg-emerald-600 border-emerald-700 text-white shadow-sm'
                : isDark
                ? 'bg-slate-800/80 border-slate-700 text-slate-300 hover:border-emerald-500/50'
                : 'bg-white border-slate-300 text-slate-700 hover:border-emerald-400'}"
            >
              <span>{match.slice(0, cmdAutocomplete.prefix.length)}</span><span
                class="opacity-70 underline decoration-dotted">{match.slice(cmdAutocomplete.prefix.length)}</span
              >
            </button>
          {/each}
        </div>
      {/if}

      <!-- Query Autocomplete & Command History Bar -->
      <div class="flex items-center justify-between gap-2 flex-wrap px-1">
        <div class="flex items-center gap-1.5 flex-wrap min-h-[22px]">
          {#if queryAutocomplete.matches.length > 0}
            <span class="text-[10px] font-mono uppercase tracking-wider font-semibold {isDark ? 'text-cyan-400' : 'text-sky-700'}">
              Autocomplete (Tab ↹ accept · Shift+Tab cycle):
            </span>
            {#each queryAutocomplete.matches as match}
              <button
                type="button"
                on:click={() => acceptQueryAutocomplete(match)}
                class="px-2 py-0.5 rounded border transition-all text-xs font-mono {match === queryAutocomplete.activeCandidate
                  ? isDark
                    ? 'bg-cyan-950/90 border-cyan-400 text-cyan-200 shadow-sm'
                    : 'bg-sky-600 border-sky-700 text-white shadow-sm'
                  : isDark
                  ? 'bg-slate-900/90 border-slate-700 text-slate-300 hover:border-cyan-500/50'
                  : 'bg-slate-100 border-slate-300 text-slate-700 hover:border-sky-400'}"
              >
                <span>{match.slice(0, queryAutocomplete.prefix.length)}</span><span
                  class="px-0.5 rounded {match === queryAutocomplete.activeCandidate
                    ? isDark
                      ? 'bg-cyan-400/25 text-cyan-100'
                      : 'bg-white/25 text-white'
                    : isDark
                    ? 'bg-slate-800 text-cyan-300/80'
                    : 'bg-sky-100 text-sky-900'}">{match.slice(queryAutocomplete.prefix.length)}</span
                >
              </button>
            {/each}
          {:else}
            <span class="text-[10px] font-mono {isDark ? 'text-slate-400' : 'text-slate-600'}">
              Tip: Press <kbd class="px-1 py-0.2 rounded border text-[9px] {isDark ? 'bg-slate-900 border-slate-700 text-amber-300' : 'bg-amber-50 border-amber-400 text-amber-900'}">Ctrl+O</kbd> to expand/collapse thought process · <kbd class="px-1 py-0.2 rounded border text-[9px] {isDark ? 'bg-slate-900 border-slate-700 text-slate-300' : 'bg-slate-100 border-slate-300 text-slate-700'}">↑</kbd>/<kbd class="px-1 py-0.2 rounded border text-[9px] {isDark ? 'bg-slate-900 border-slate-700 text-slate-300' : 'bg-slate-100 border-slate-300 text-slate-700'}">↓</kbd> history · <kbd class="px-1 py-0.2 rounded border text-[9px] {isDark ? 'bg-slate-900 border-slate-700 text-slate-300' : 'bg-slate-100 border-slate-300 text-slate-700'}">Tab ↹</kbd> autocomplete
            </span>
          {/if}
        </div>

        <!-- Query History Navigation Controls -->
        <div class="flex items-center gap-1.5 shrink-0">
          {#if queryHistoryCursor >= 0}
            <span
              class="text-[10px] font-mono px-2 py-0.5 rounded border {isDark
                ? 'bg-cyan-950/80 border-cyan-500/40 text-cyan-200'
                : 'bg-sky-100 border-sky-300 text-sky-900 font-semibold'}"
            >
              History {queryHistoryCursor + 1}/{queryHistory.length}
            </span>
          {:else if queryHistory.length > 0}
            <span class="text-[10px] font-mono {isDark ? 'text-slate-400' : 'text-slate-600'}">
              History: {queryHistory.length} saved
            </span>
          {/if}

          <button
            type="button"
            disabled={queryHistory.length === 0}
            on:click={() => stepQueryHistory('up')}
            class="px-2 py-0.5 rounded text-[10px] font-mono border disabled:opacity-35 transition-colors {isDark
              ? 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
              : 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'}"
            title="Scroll up to previous command/query (Up Arrow)"
          >
            ↑ Prev
          </button>
          <button
            type="button"
            disabled={queryHistoryCursor === -1}
            on:click={() => stepQueryHistory('down')}
            class="px-2 py-0.5 rounded text-[10px] font-mono border disabled:opacity-35 transition-colors {isDark
              ? 'bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800'
              : 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'}"
            title="Scroll down to newer command/query (Down Arrow)"
          >
            ↓ Next
          </button>
        </div>
      </div>

      <!-- Row C2: Project Local `Files/` Directory (`Projects/<project>/Files/`) & Console File Upload Bar -->
      <div
        class="flex flex-wrap items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg border text-xs font-mono {isDark
          ? 'bg-slate-900/85 border-slate-700/90 text-slate-200'
          : 'bg-slate-50 border-slate-300 text-slate-800'}"
      >
        <div class="flex flex-wrap items-center gap-1.5 min-w-0">
          <input
            bind:this={consoleFileInputEl}
            type="file"
            multiple
            class="hidden"
            on:change={(e) => handleBrowserFilesUpload(e.currentTarget.files, true)}
          />
          <span class="font-bold text-[11px] flex items-center gap-1 {isDark ? 'text-cyan-300' : 'text-cyan-800'}">
            <span>📂 Local Project Files (<code>Projects/{activeProject}/Files/</code>):</span>
          </span>

          <button
            type="button"
            disabled={uploadingFiles || !activeProject}
            on:click={() => consoleFileInputEl && consoleFileInputEl.click()}
            class="px-2.5 py-0.5 rounded border text-[11px] font-semibold transition-colors flex items-center gap-1 disabled:opacity-50 {isDark
              ? 'bg-cyan-950/90 hover:bg-cyan-900 border-cyan-500/50 text-cyan-200'
              : 'bg-cyan-600 hover:bg-cyan-500 border-cyan-700 text-white'}"
            title="Upload or add files/scripts from your computer into Projects/{activeProject}/Files/ so the LLM can inspect and use them"
          >
            <span>{uploadingFiles ? '⏳ Uploading...' : '📤 + Upload / Add File'}</span>
          </button>

          <button
            type="button"
            disabled={!activeProject}
            on:click={() => {
              refreshProjectFiles();
              showProjectFilesModal = true;
            }}
            class="px-2.5 py-0.5 rounded border text-[11px] transition-colors flex items-center gap-1 disabled:opacity-50 {isDark
              ? 'bg-slate-800 hover:bg-slate-700 border-slate-600 text-slate-200'
              : 'bg-white hover:bg-slate-100 border-slate-300 text-slate-800'}"
            title="Open Projects/{activeProject}/Files/ Manager, Local Path Importer, & Custom Script Editor"
          >
            <span>📁 Manage <code>Files/</code> ({(projectFilesPayload?.files_dir_items || []).length})</span>
          </button>
        </div>

        {#if attachedFiles.length > 0}
          <div class="flex items-center gap-1.5 shrink-0">
            <span
              class="px-2 py-0.5 rounded text-[10px] font-bold {isDark
                ? 'bg-emerald-950 text-emerald-300 border border-emerald-500/40'
                : 'bg-emerald-100 text-emerald-900 border border-emerald-400'}"
            >
              📎 {attachedFiles.length} attached to prompt
            </span>
            <button
              type="button"
              on:click={() => (attachedFiles = [])}
              class="text-[10px] underline opacity-80 hover:opacity-100"
            >
              Clear
            </button>
          </div>
        {/if}
      </div>

      <!-- Row D: Main Query Input Window & Submit Button -->
      <div class="flex items-end gap-2">
        <div
          class="flex-1 relative rounded-lg border overflow-hidden {isDark
            ? 'bg-slate-900 border-slate-700'
            : 'bg-white border-slate-300'}"
          style="border-color: {isoTheme.outlineHex}88;"
        >
          <!-- Shaded Inline Ghost-Text Autocomplete Backdrop for Main Query Input -->
          <div
            bind:this={queryMirrorEl}
            aria-hidden="true"
            class="absolute inset-0 px-3 py-2 whitespace-pre-wrap break-words overflow-hidden pointer-events-none select-none"
            style={customTextStyle}
          >
            {#if queryAutocomplete.suffix}
              <span class="text-transparent">{queryInput}</span><span
                class="rounded px-1 py-0.5 {isDark
                  ? 'bg-cyan-500/20 text-cyan-300/75 border border-cyan-400/40 shadow-sm'
                  : 'bg-sky-200/85 text-sky-900/80 border border-sky-400/60 shadow-sm'}"
              >{queryAutocomplete.suffix}</span><span
                class="ml-1.5 text-[10px] px-1.5 py-0.5 rounded align-middle {isDark
                  ? 'bg-slate-800/95 text-cyan-300 border border-slate-700'
                  : 'bg-slate-200/95 text-sky-900 border border-slate-300'}"
              >Tab ↹{queryAutocomplete.matches.length > 1 ? ` (${((queryCycleIndex % queryAutocomplete.matches.length) + queryAutocomplete.matches.length) % queryAutocomplete.matches.length + 1}/${queryAutocomplete.matches.length})` : ''}</span>
            {/if}
          </div>

          <textarea
            bind:this={queryTextareaEl}
            bind:value={queryInput}
            on:input={handleQueryInputEvent}
            on:scroll={handleQueryTextareaScroll}
            on:keydown={handleKeydown}
            rows="2"
            placeholder="Enter your tactical query, target IP/URL, or slash command (/generate-report)... Press ↑/↓ for command history, Tab ↹ for shaded word autocomplete, Enter to execute."
            class="relative z-10 w-full bg-transparent px-3 py-2 focus:outline-none resize-none {isDark
              ? 'text-white placeholder-slate-400'
              : 'text-slate-900 placeholder-slate-500'}"
            style={customTextStyle}
          ></textarea>
        </div>

        <button
          type="button"
          disabled={!activeProject || submittingQuery || (!queryInput.trim() && !commandToExecute.trim() && !activeGoal.trim() && attachedFiles.length === 0)}
          on:click={handleQuerySubmit}
          class="h-[54px] px-5 rounded-lg font-bold text-sm tracking-wide transition-all shadow-lg flex items-center gap-2 disabled:opacity-50 {isoTheme.submitBtnClass}"
        >
          {#if submittingQuery}
            <span class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full"></span>
            <span>Executing...</span>
          {:else if !queryInput.trim() && !commandToExecute.trim() && activeGoal.trim()}
            <span>🎯 Pursue Goal</span>
          {:else}
            <span>Execute Query</span>
          {/if}
        </button>
      </div>
    </section>
  </main>

  <!-- ===================================================================== -->
  <!-- MODAL 2: SELECT OR CREATE PROJECT                                     -->
  <!-- ===================================================================== -->
  {#if showCreateProjectModal}
    <div class="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center z-50 p-3">
      <div
        class="w-full max-w-md rounded-xl overflow-hidden shadow-2xl {isDark
          ? 'bg-slate-950 text-white'
          : 'bg-white text-slate-900'}"
        style="border: 1.5px solid {isoTheme.outlineHex};"
      >
        <div class="px-4 py-3 flex items-center justify-between border-b" style={isoTheme.headerStyle}>
          <h3 class="text-sm font-bold">
            {!activeProject ? 'Select Existing Project or Create New Project' : 'Create New Isolated Project'} (<code>Projects/&lt;name&gt;/</code>)
          </h3>
          {#if activeProject}
            <button
              class="text-xs px-2 py-0.5 rounded border {isDark
                ? 'bg-slate-900 border-slate-700 text-slate-300'
                : 'bg-white border-slate-300 text-slate-700'}"
              on:click={() => (showCreateProjectModal = false)}
            >
              ✕
            </button>
          {/if}
        </div>
        <div class="p-4 space-y-3.5">
          {#if projects.length > 0 && !activeProject}
            <div class="space-y-1.5 text-xs pb-2.5 border-b {isDark ? 'border-slate-800' : 'border-slate-200'}">
              <div class="font-mono font-semibold">Select an Existing Project:</div>
              <div class="flex flex-wrap gap-1.5">
                {#each projects as p}
                  <button
                    type="button"
                    on:click={() => {
                      projectDropdownValue = p.slug;
                      showCreateProjectModal = false;
                      handleProjectDropdownChange();
                    }}
                    class="px-3 py-1.5 rounded border font-mono text-xs font-bold {isDark
                      ? 'bg-cyan-950/90 hover:bg-cyan-900 border-cyan-500/50 text-cyan-200'
                      : 'bg-cyan-600 hover:bg-cyan-500 border-cyan-700 text-white'}"
                  >
                    [{p.menu_number}] {p.slug}
                  </button>
                {/each}
              </div>
            </div>
          {/if}
          <div class="space-y-2 text-xs">
            <label for="new-proj-name" class="block font-mono">New Project Name (spaces convert to hyphens):</label>
            <input
              id="new-proj-name"
              type="text"
              bind:value={newProjectNameInput}
              on:keydown={(e) => e.key === 'Enter' && submitCreateProject()}
              placeholder="e.g. RedTeam-Engagement-01"
              class="w-full rounded border px-3 py-2 font-mono focus:outline-none {isDark
                ? 'bg-slate-900 border-slate-700 text-white'
                : 'bg-slate-50 border-slate-300 text-slate-900'}"
            />
            <label for="new-proj-goal" class="block font-mono mt-2">Initial Project Goal (optional):</label>
            <input
              id="new-proj-goal"
              type="text"
              bind:value={newProjectGoalInput}
              on:keydown={(e) => e.key === 'Enter' && submitCreateProject()}
              placeholder="e.g. Enumerate target subnet and verify services"
              class="w-full rounded border px-3 py-2 font-mono focus:outline-none {isDark
                ? 'bg-slate-900 border-slate-700 text-white'
                : 'bg-slate-50 border-slate-300 text-slate-900'}"
            />
          </div>
          <div class="flex justify-end gap-2 pt-1">
            {#if activeProject}
              <button
                class="px-3.5 py-1.5 rounded text-xs border {isDark
                  ? 'bg-slate-800 border-slate-700 text-slate-300'
                  : 'bg-slate-100 border-slate-300 text-slate-700'}"
                on:click={() => (showCreateProjectModal = false)}
              >
                Cancel
              </button>
            {/if}
            <button
              disabled={!newProjectNameInput.trim()}
              class="px-4 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-xs font-bold text-white"
              on:click={submitCreateProject}
            >
              Create Project
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <!-- ===================================================================== -->
  <!-- MODAL 3: RENAME CURRENT PROJECT                                       -->
  <!-- ===================================================================== -->
  {#if showRenameProjectModal}
    <div class="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center z-50 p-3">
      <div
        class="w-full max-w-md rounded-xl overflow-hidden shadow-2xl {isDark
          ? 'bg-slate-950 text-white'
          : 'bg-white text-slate-900'}"
        style="border: 1.5px solid {isoTheme.outlineHex};"
      >
        <div class="px-4 py-3 flex items-center justify-between border-b" style={isoTheme.headerStyle}>
          <h3 class="text-sm font-bold">Rename Project (<code>Projects/{activeProject}/</code>)</h3>
          <button
            class="text-xs px-2 py-0.5 rounded border {isDark
              ? 'bg-slate-900 border-slate-700 text-slate-300'
              : 'bg-white border-slate-300 text-slate-700'}"
            on:click={() => (showRenameProjectModal = false)}
          >
            ✕
          </button>
        </div>
        <div class="p-4 space-y-3">
          <div class="space-y-1.5 text-xs">
            <label for="rename-proj-input" class="block font-mono">New Project Name:</label>
            <input
              id="rename-proj-input"
              type="text"
              bind:value={renameProjectNewNameInput}
              class="w-full rounded border px-3 py-2 font-mono focus:outline-none {isDark
                ? 'bg-slate-900 border-slate-700 text-white'
                : 'bg-slate-50 border-slate-300 text-slate-900'}"
            />
          </div>
          <div class="flex justify-end gap-2 pt-1">
            <button
              class="px-3.5 py-1.5 rounded text-xs border {isDark
                ? 'bg-slate-800 border-slate-700 text-slate-300'
                : 'bg-slate-100 border-slate-300 text-slate-700'}"
              on:click={() => (showRenameProjectModal = false)}
            >
              Cancel
            </button>
            <button
              class="px-4 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-xs font-bold text-white"
              on:click={submitRenameProject}
            >
              Rename Project
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <!-- ===================================================================== -->
  <!-- MODAL 4: C.O.R.A. CLI BANNER, DISCLAIMER & LICENSING POP-UP           -->
  <!--          (Opened by clicking the CROW Emblem in Dark or Light Mode)   -->
  <!-- ===================================================================== -->
  {#if showBannerModal}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div
      class="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center z-50 p-3 select-text"
      on:click|self={() => (showBannerModal = false)}
    >
      <div
        class="w-full max-w-4xl max-h-[92vh] rounded-xl shadow-2xl flex flex-col overflow-hidden {isDark
          ? 'bg-slate-950 text-slate-100'
          : 'bg-white text-slate-900'}"
        style="border: 1.5px solid {isoTheme.outlineHex}; box-shadow: 0 0 24px {isoTheme.outlineGlow};"
      >
        <!-- Modal Header (Shaded by Active Network Isolation & Dark/Light Mode) -->
        <div
          class="px-4 py-2.5 flex items-center justify-between gap-3 shrink-0"
          style={isoTheme.headerStyle}
        >
          <div class="flex items-center gap-3 min-w-0">
            <img
              src={crowLogoUrl}
              alt="CROW Emblem"
              class="h-9 w-auto object-contain shrink-0 select-none"
              style="filter: drop-shadow(0 0 8px {isoTheme.outlineGlow});"
            />
            <h3 class="text-sm sm:text-base font-extrabold tracking-wider {isDark ? 'text-white' : 'text-slate-950'}">
              C.O.R.A. — Cyber Oriented Reasoning Agent
            </h3>
          </div>

          <button
            type="button"
            class="px-3 py-1 rounded text-xs font-bold border transition-colors shrink-0 {isDark
              ? 'bg-slate-900 hover:bg-slate-800 border-slate-700 text-slate-200'
              : 'bg-white hover:bg-slate-100 border-slate-300 text-slate-800 shadow-sm'}"
            on:click={() => (showBannerModal = false)}
          >
            ✕ Close
          </button>
        </div>

        <!-- Scrollable Modal Body (Zero redundant outer gap) -->
        <div class="flex-1 overflow-y-auto p-4 space-y-3.5 {isDark ? 'bg-slate-950' : 'bg-white'}">
          <!-- Top "=" Border (Centered) -->
          <div
            class="w-full text-center font-mono text-[11px] tracking-tight overflow-x-auto whitespace-pre font-bold"
            style="color: {isoTheme.outlineHex};"
          >
            {'='.repeat(100)}
          </div>

          <!-- CROW Emblem + C.O.R.A. ASCII Banner Side-by-Side -->
          <div class="flex flex-col md:flex-row items-center justify-center gap-8 py-2">
            <div class="flex items-center justify-center shrink-0">
              <img
                src={crowLogoUrl}
                alt="CROW Emblem"
                class="h-32 w-auto object-contain select-none"
                style="filter: drop-shadow(0 0 12px {isoTheme.outlineGlow});"
              />
            </div>

            <pre
              class="font-mono text-xs sm:text-sm leading-snug overflow-x-auto font-bold {isDark
                ? 'text-white'
                : 'text-slate-900'}">{(cliBanner?.cora_banner_lines || FALLBACK_CORA_BANNER_LINES).join('\n')}</pre>
          </div>

          <!-- Centered Multi-Layered Reasoning Agent Description (_CORA_DESCRIPTION_LINES) -->
          <div class="text-center font-mono text-xs leading-relaxed px-2 {isDark ? 'text-slate-200' : 'text-slate-800'}">
            {#each cliBanner?.description_lines || FALLBACK_DESCRIPTION_LINES as descLine}
              <div>{descLine}</div>
            {/each}
          </div>

          <!-- Centered "=" Divider Between Description and Disclaimer -->
          <div
            class="w-full text-center font-mono text-[11px] tracking-tight overflow-x-auto whitespace-pre font-bold"
            style="color: {isoTheme.outlineHex};"
          >
            {'='.repeat(100)}
          </div>

          <!-- CLI Disclaimer & Open-Source Licensing Notice (_CORA_DISCLAIMER_LINES) -->
          <div class="text-center font-mono text-xs leading-relaxed space-y-1">
            {#each cliBanner?.disclaimer_lines || FALLBACK_DISCLAIMER_LINES as dLine, idx}
              {#if idx === 0}
                <div class="font-bold {isDark ? 'text-amber-300' : 'text-amber-700'}">{dLine}</div>
              {:else}
                <div class={isDark ? 'text-slate-300' : 'text-slate-700'}>{dLine}</div>
              {/if}
            {/each}
          </div>

          <!-- Version & "Developed by:" at the Very Bottom, Left-Aligned -->
          <div class="w-full text-left font-mono text-xs pt-2 border-t space-y-0.5 {isDark ? 'text-slate-400 border-slate-800' : 'text-slate-600 border-slate-200'}">
            <div>Version: <strong class={isDark ? 'text-slate-200' : 'text-slate-900'}>{cliBanner?.version || versionStr}</strong></div>
            <div>
              Developed by:
              <a
                href={cliBanner?.developed_by || 'https://CROWinnovations.com'}
                target="_blank"
                rel="noreferrer"
                class="underline {isDark ? 'text-cyan-300' : 'text-cyan-700'}"
              >
                {cliBanner?.developed_by || 'https://CROWinnovations.com'}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <!-- ===================================================================== -->
  <!-- MODAL 5: PROJECT `Files/` DIRECTORY MANAGER, UPLOADER & SCRIPT EDITOR -->
  <!-- ===================================================================== -->
  {#if showProjectFilesModal}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div
      class="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center z-50 p-3 select-text"
      on:click|self={() => (showProjectFilesModal = false)}
    >
      <div
        class="w-full max-w-5xl max-h-[92vh] rounded-xl shadow-2xl flex flex-col overflow-hidden {isDark
          ? 'bg-slate-950 text-slate-100'
          : 'bg-white text-slate-900'}"
        style="border: 1.5px solid {isoTheme.outlineHex};"
      >
        <!-- Modal Header -->
        <div
          class="px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 shrink-0"
          style={isoTheme.headerStyle}
        >
          <div>
            <h3 class="text-sm sm:text-base font-bold font-mono flex items-center gap-2 {isDark ? 'text-white' : 'text-slate-950'}">
              <span>📂 Project Local <code>Files</code> Directory — <code>Projects/{activeProject}/Files/</code></span>
            </h3>
            <p class="text-[11px] font-mono mt-0.5 {isDark ? 'text-slate-300' : 'text-slate-700'}">
              Host Path (<code>$PROJECT_FILES_DIR</code>): <code>{projectFilesPayload?.files_dir || `Projects/${activeProject}/Files`}</code>
              — Anything placed here is automatically visible &amp; executable by the LLM.
            </p>
          </div>
          <div class="flex items-center gap-2">
            <button
              type="button"
              on:click={() => consoleFileInputEl && consoleFileInputEl.click()}
              class="px-3 py-1 rounded text-xs font-mono font-bold border {isDark
                ? 'bg-cyan-950 hover:bg-cyan-900 border-cyan-500/50 text-cyan-200'
                : 'bg-cyan-600 hover:bg-cyan-500 border-cyan-700 text-white'}"
            >
              📤 Upload File(s) from Computer
            </button>
            <button
              type="button"
              on:click={() => (showProjectFilesModal = false)}
              class="px-3 py-1 rounded text-xs font-bold border {isDark
                ? 'bg-slate-900 hover:bg-slate-800 border-slate-700 text-slate-200'
                : 'bg-white hover:bg-slate-100 border-slate-300 text-slate-800'}"
            >
              ✕ Close
            </button>
          </div>
        </div>

        <!-- Modal Body -->
        <div class="flex-1 overflow-y-auto p-4 grid grid-cols-1 lg:grid-cols-2 gap-3.5">
          <!-- Left Column: Upload / Import Local Host Path + Files List -->
          <div class="space-y-3">
            <!-- 1. Import Local Host File or Directory Path -->
            <div
              class="rounded-lg p-3 border space-y-2 {isDark
                ? 'bg-slate-900/90 border-slate-800'
                : 'bg-slate-50 border-slate-200'}"
            >
              <div class="text-xs font-bold font-mono {isDark ? 'text-cyan-300' : 'text-cyan-800'}">
                1. Import Local Host File or Folder into <code>Projects/{activeProject}/Files/</code>
              </div>
              <div class="flex gap-2">
                <input
                  type="text"
                  bind:value={localFilePathInput}
                  on:keydown={(e) => e.key === 'Enter' && handleImportLocalPath(true)}
                  placeholder="e.g. C:\scripts\custom_scan.py or /home/user/tools/check.sh"
                  class="flex-1 rounded border px-3 py-1.5 text-xs font-mono focus:outline-none {isDark
                    ? 'bg-slate-950 border-slate-700 text-white'
                    : 'bg-white border-slate-300 text-slate-900'}"
                />
                <button
                  type="button"
                  disabled={!localFilePathInput.trim() || uploadingFiles}
                  on:click={() => handleImportLocalPath(true)}
                  class="px-3 py-1.5 rounded text-xs font-mono font-bold border disabled:opacity-50 {isDark
                    ? 'bg-emerald-950 hover:bg-emerald-900 border-emerald-500/50 text-emerald-200'
                    : 'bg-emerald-600 hover:bg-emerald-500 border-emerald-700 text-white'}"
                >
                  Import Path
                </button>
              </div>
              <div class="text-[11px] font-mono opacity-75">
                Tip: You can also run <code>/files add &lt;path&gt;</code> or <code>/upload &lt;path&gt;</code> in the Console or CLI.
              </div>
            </div>

            <!-- 2. Create New Custom Script / File Directly in Files/ -->
            <div
              class="rounded-lg p-3 border space-y-2 {isDark
                ? 'bg-slate-900/90 border-slate-800'
                : 'bg-slate-50 border-slate-200'}"
            >
              <div class="text-xs font-bold font-mono {isDark ? 'text-amber-300' : 'text-amber-800'}">
                2. Create New Custom Script or File in <code>Projects/{activeProject}/Files/</code>
              </div>
              <div class="flex gap-2">
                <input
                  type="text"
                  bind:value={newCustomScriptName}
                  placeholder="Filename (e.g. custom_probe.py, enum.ps1, check.sh, targets.txt)"
                  class="flex-1 rounded border px-3 py-1.5 text-xs font-mono focus:outline-none {isDark
                    ? 'bg-slate-950 border-slate-700 text-white'
                    : 'bg-white border-slate-300 text-slate-900'}"
                />
                <button
                  type="button"
                  disabled={!newCustomScriptName.trim() || uploadingFiles}
                  on:click={handleCreateNewCustomScript}
                  class="px-3 py-1.5 rounded text-xs font-mono font-bold border disabled:opacity-50 {isDark
                    ? 'bg-amber-950 hover:bg-amber-900 border-amber-500/50 text-amber-200'
                    : 'bg-amber-600 hover:bg-amber-500 border-amber-700 text-white'}"
                >
                  + Save to Files/
                </button>
              </div>
              <textarea
                bind:value={newCustomScriptContent}
                rows="4"
                placeholder="Paste script or file content here..."
                class="w-full rounded border px-3 py-2 text-xs font-mono focus:outline-none {isDark
                  ? 'bg-slate-950 border-slate-700 text-slate-100'
                  : 'bg-white border-slate-300 text-slate-900'}"
              ></textarea>
            </div>

            <!-- 3. Current Files in Projects/<activeProject>/Files/ -->
            <div
              class="rounded-lg p-3 border space-y-2 {isDark
                ? 'bg-slate-900/90 border-slate-800'
                : 'bg-slate-50 border-slate-200'}"
            >
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold font-mono {isDark ? 'text-emerald-300' : 'text-emerald-800'}">
                  3. Files in <code>Projects/{activeProject}/Files/</code> ({(projectFilesPayload?.files_dir_items || []).length})
                </span>
                <button
                  type="button"
                  on:click={refreshProjectFiles}
                  class="text-[11px] font-mono underline opacity-80 hover:opacity-100"
                >
                  ↻ Refresh
                </button>
              </div>

              {#if (projectFilesPayload?.files_dir_items || []).length === 0}
                <div class="text-xs font-mono py-4 text-center opacity-70">
                  No custom files in <code>Projects/{activeProject}/Files/</code> yet. Upload a file, drag &amp; drop onto the Console, or create a script above.
                </div>
              {:else}
                <div class="space-y-1.5 max-h-60 overflow-y-auto pr-1">
                  {#each projectFilesPayload?.files_dir_items || [] as fItem}
                    {@const pRel = fItem.project_rel || `Files/${fItem.name}`}
                    {@const isAttached = attachedFiles.includes(pRel)}
                    <div
                      class="flex items-center justify-between gap-2 px-2.5 py-1.5 rounded border text-xs font-mono {isDark
                        ? 'bg-slate-950 border-slate-800'
                        : 'bg-white border-slate-300'}"
                    >
                      <div class="min-w-0 truncate">
                        <div class="font-bold truncate">{fItem.name}</div>
                        <div class="text-[10px] opacity-70">
                          <code>{fItem.rel_path}</code> · {fItem.size_bytes} bytes
                        </div>
                      </div>
                      <div class="flex items-center gap-1 shrink-0">
                        <button
                          type="button"
                          on:click={() => toggleAttachFile(pRel)}
                          class="px-2 py-0.5 rounded border text-[10px] {isAttached
                            ? 'bg-emerald-600 border-emerald-500 text-white font-bold'
                            : isDark
                            ? 'bg-slate-900 border-slate-700 text-slate-300'
                            : 'bg-slate-100 border-slate-300 text-slate-700'}"
                        >
                          {isAttached ? '📎 Attached' : 'Attach'}
                        </button>
                        <button
                          type="button"
                          on:click={() => promptLlmToUseProjectFile(fItem)}
                          class="px-2 py-0.5 rounded border text-[10px] {isDark
                            ? 'bg-cyan-950 border-cyan-500/40 text-cyan-200'
                            : 'bg-cyan-100 border-cyan-400 text-cyan-900'}"
                        >
                          Use with LLM
                        </button>
                        <button
                          type="button"
                          on:click={() => openProjectFileInViewer(fItem.rel_path)}
                          class="px-2 py-0.5 rounded border text-[10px] {isDark
                            ? 'bg-slate-900 border-slate-700 text-slate-300'
                            : 'bg-slate-100 border-slate-300 text-slate-700'}"
                        >
                          Edit
                        </button>
                        {#if sessionMode !== 'analyst'}
                          <button
                            type="button"
                            on:click={() => deleteProjectFile(fItem.rel_path)}
                            class="px-2 py-0.5 rounded border text-[10px] {isDark
                              ? 'bg-rose-950/70 border-rose-500/40 text-rose-300'
                              : 'bg-rose-100 border-rose-300 text-rose-800'}"
                          >
                            ✕
                          </button>
                        {/if}
                      </div>
                    </div>
                  {/each}
                </div>
              {/if}
            </div>
          </div>

          <!-- Right Column: Live File Viewer & Editor -->
          <div
            class="rounded-lg p-3 border flex flex-col gap-2 {isDark
              ? 'bg-slate-900/90 border-slate-800'
              : 'bg-slate-50 border-slate-200'}"
          >
            <div class="flex items-center justify-between gap-2">
              <span class="text-xs font-bold font-mono truncate {isDark ? 'text-cyan-300' : 'text-cyan-800'}">
                {selectedProjectFileRel ? `Editing: ${selectedProjectFileRel}` : 'Select a file on the left to view or edit'}
              </span>
              {#if selectedProjectFileRel && sessionMode !== 'analyst'}
                <button
                  type="button"
                  disabled={savingProjectFile}
                  on:click={saveEditedProjectFile}
                  class="px-3 py-1 rounded text-xs font-mono font-bold border {isDark
                    ? 'bg-emerald-950 hover:bg-emerald-900 border-emerald-500/50 text-emerald-200'
                    : 'bg-emerald-600 hover:bg-emerald-500 border-emerald-700 text-white'}"
                >
                  {savingProjectFile ? 'Saving...' : '💾 Save Changes'}
                </button>
              {/if}
            </div>
            <textarea
              bind:value={selectedProjectFileContent}
              disabled={!selectedProjectFileRel || loadingProjectFileContent || sessionMode === 'analyst'}
              rows="18"
              placeholder={loadingProjectFileContent ? 'Loading file content...' : 'Click "Edit" on any file in Projects/' + activeProject + '/Files/ to inspect or modify its contents here.'}
              class="flex-1 w-full rounded border p-3 text-xs font-mono leading-relaxed focus:outline-none {isDark
                ? 'bg-slate-950 border-slate-700 text-slate-100'
                : 'bg-white border-slate-300 text-slate-900'}"
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <!-- ===================================================================== -->
  <!-- MODAL 6: ENTERPRISE DISPLAY, FONT & WORKSPACE CUSTOMIZATION SETTINGS  -->
  <!--          (Opened by the ⚙️ Settings Gear button next to SYSINTERNALS) -->
  <!-- ===================================================================== -->
  {#if showSettingsModal}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div
      class="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center z-50 p-3 select-text"
      on:click|self={() => (showSettingsModal = false)}
    >
      <div
        class="w-full max-w-3xl max-h-[92vh] rounded-xl shadow-2xl flex flex-col overflow-hidden {isDark
          ? 'bg-slate-950 text-slate-100'
          : 'bg-white text-slate-900'}"
        style="border: 1.5px solid {isoTheme.outlineHex}; box-shadow: 0 0 24px {isoTheme.outlineGlow};"
      >
        <!-- Modal Header -->
        <div
          class="px-4 py-2.5 flex items-center justify-between gap-3 shrink-0"
          style={isoTheme.headerStyle}
        >
          <div class="flex items-center gap-2.5">
            <span class="text-base">⚙️</span>
            <div>
              <h3 class="text-sm sm:text-base font-bold font-mono {isDark ? 'text-white' : 'text-slate-950'}">
                Enterprise Dashboard &amp; Typography Customization Settings
              </h3>
              <p class="text-[11px] font-mono {isDark ? 'text-slate-300' : 'text-slate-700'}">
                Configure Font Style, Font Color, Font Size, Layout Density, and Default Workstation Behavior
              </p>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <button
              type="button"
              on:click={resetUiCustomization}
              class="px-2.5 py-1 rounded text-xs font-mono border transition-colors {isDark
                ? 'bg-slate-900 hover:bg-rose-950/80 border-slate-700 text-slate-300 hover:text-rose-200'
                : 'bg-slate-100 hover:bg-rose-100 border-slate-300 text-slate-700 hover:text-rose-900'}"
              title="Reset all font and display settings to enterprise defaults"
            >
              ↺ Reset Defaults
            </button>
            <button
              type="button"
              on:click={() => (showSettingsModal = false)}
              class="px-3 py-1 rounded text-xs font-bold border transition-colors {isDark
                ? 'bg-slate-900 hover:bg-slate-800 border-slate-700 text-slate-200'
                : 'bg-white hover:bg-slate-100 border-slate-300 text-slate-800'}"
            >
              ✕ Close
            </button>
          </div>
        </div>

        <!-- Modal Body -->
        <div class="flex-1 overflow-y-auto p-4 space-y-4 text-xs">
          <!-- Section 1: Font Style (Family) & Font Size -->
          <div
            class="rounded-lg p-3.5 border space-y-3 {isDark
              ? 'bg-slate-900/90 border-slate-800'
              : 'bg-slate-50 border-slate-200'}"
          >
            <div class="font-bold font-mono uppercase tracking-wider {isDark ? 'text-cyan-300' : 'text-sky-800'}">
              1. Typography — Font Style, Size &amp; Line Spacing
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <!-- Font Style Selector -->
              <div class="space-y-1">
                <label for="settings-font-family" class="block font-mono font-semibold">Font Style (Font Family):</label>
                <select
                  id="settings-font-family"
                  bind:value={uiFontFamily}
                  on:change={saveUiCustomizationSettings}
                  class="w-full rounded border px-2.5 py-1.5 text-xs font-mono focus:outline-none {isDark
                    ? 'bg-slate-950 border-slate-700 text-white focus:border-cyan-400'
                    : 'bg-white border-slate-300 text-slate-900 focus:border-sky-600'}"
                >
                  {#each FONT_FAMILY_OPTIONS as fOpt}
                    <option value={fOpt.value}>{fOpt.label}</option>
                  {/each}
                </select>
              </div>

              <!-- Font Size Slider & Quick Presets -->
              <div class="space-y-1">
                <div class="flex items-center justify-between font-mono">
                  <label for="settings-font-size" class="font-semibold">Font Size:</label>
                  <span class="px-2 py-0.5 rounded font-bold {isDark ? 'bg-slate-950 text-cyan-300 border border-slate-800' : 'bg-white text-sky-800 border border-slate-300'}">
                    {uiFontSize}px
                  </span>
                </div>
                <input
                  id="settings-font-size"
                  type="range"
                  min="11"
                  max="20"
                  step="1"
                  bind:value={uiFontSize}
                  on:input={() => applyUiCustomization(true)}
                  on:change={saveUiCustomizationSettings}
                  class="w-full accent-cyan-500 cursor-pointer"
                />
                <div class="flex flex-wrap gap-1 pt-0.5">
                  {#each [12, 13, 14, 15, 16, 18] as sz}
                    <button
                      type="button"
                      on:click={() => {
                        uiFontSize = sz;
                        saveUiCustomizationSettings();
                      }}
                      class="px-2 py-0.5 rounded border font-mono text-[11px] {uiFontSize === sz
                        ? isDark
                          ? 'bg-cyan-950 border-cyan-400 text-cyan-200 font-bold'
                          : 'bg-sky-600 border-sky-700 text-white font-bold'
                        : isDark
                        ? 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
                        : 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100'}"
                    >
                      {sz}px
                    </button>
                  {/each}
                </div>
              </div>
            </div>

            <!-- Line Height / Spacing -->
            <div class="flex flex-wrap items-center justify-between gap-2 pt-1 border-t {isDark ? 'border-slate-800' : 'border-slate-200'}">
              <span class="font-mono font-semibold">Line Spacing (Line Height):</span>
              <div class="flex items-center gap-1.5">
                {#each [
                  { label: 'Compact (1.35)', value: '1.35' },
                  { label: 'Standard (1.5)', value: '1.5' },
                  { label: 'Relaxed (1.7)', value: '1.7' },
                ] as lh}
                  <button
                    type="button"
                    on:click={() => {
                      uiLineHeight = lh.value;
                      saveUiCustomizationSettings();
                    }}
                    class="px-2.5 py-1 rounded border font-mono text-[11px] {uiLineHeight === lh.value
                      ? isDark
                        ? 'bg-cyan-950 border-cyan-400 text-cyan-200 font-bold'
                        : 'bg-sky-600 border-sky-700 text-white font-bold'
                      : isDark
                      ? 'bg-slate-950 border-slate-800 text-slate-300'
                      : 'bg-white border-slate-300 text-slate-700'}"
                  >
                    {lh.label}
                  </button>
                {/each}
              </div>
            </div>
          </div>

          <!-- Section 2: Font Color Swatches & Custom Color Picker -->
          <div
            class="rounded-lg p-3.5 border space-y-3 {isDark
              ? 'bg-slate-900/90 border-slate-800'
              : 'bg-slate-50 border-slate-200'}"
          >
            <div class="flex flex-wrap items-center justify-between gap-2">
              <span class="font-bold font-mono uppercase tracking-wider {isDark ? 'text-emerald-300' : 'text-emerald-800'}">
                2. Font Color — Enterprise Presets &amp; Custom Color Picker
              </span>
              <span class="font-mono text-[11px] opacity-80">
                Active: <code>{uiFontColor || 'Theme Default (Auto)'}</code>
              </span>
            </div>

            <div class="flex flex-wrap gap-1.5">
              {#each FONT_COLOR_PRESETS as cPreset}
                <button
                  type="button"
                  on:click={() => {
                    uiFontColor = cPreset.value;
                    saveUiCustomizationSettings();
                  }}
                  class="px-2.5 py-1 rounded border font-mono text-[11px] flex items-center gap-1.5 transition-all {uiFontColor ===
                  cPreset.value
                    ? isDark
                      ? 'bg-slate-950 border-cyan-400 text-white font-bold shadow-sm'
                      : 'bg-sky-50 border-sky-600 text-slate-950 font-bold shadow-sm'
                    : isDark
                    ? 'bg-slate-950/80 border-slate-800 text-slate-300 hover:border-slate-600'
                    : 'bg-white border-slate-300 text-slate-700 hover:border-slate-400'}"
                >
                  <span
                    class="w-3.5 h-3.5 rounded-full border border-slate-500 shrink-0"
                    style="background: {cPreset.swatch};"
                  ></span>
                  <span>{cPreset.label}</span>
                </button>
              {/each}
            </div>

            <div class="flex flex-wrap items-center gap-2.5 pt-1 border-t {isDark ? 'border-slate-800' : 'border-slate-200'}">
              <label for="settings-custom-color" class="font-mono font-semibold">Custom Color Picker / Hex:</label>
              <input
                id="settings-custom-color"
                type="color"
                value={uiFontColor && uiFontColor.startsWith('#') && uiFontColor.length === 7 ? uiFontColor : isDark ? '#f8fafc' : '#0f172a'}
                on:input={(e) => {
                  uiFontColor = e.currentTarget.value;
                  applyUiCustomization(true);
                }}
                on:change={saveUiCustomizationSettings}
                class="h-7 w-10 rounded border cursor-pointer bg-transparent"
              />
              <input
                type="text"
                bind:value={uiFontColor}
                on:change={saveUiCustomizationSettings}
                placeholder="Theme Auto (or #67e8f9)"
                class="w-44 rounded border px-2.5 py-1 font-mono text-xs focus:outline-none {isDark
                  ? 'bg-slate-950 border-slate-700 text-white'
                  : 'bg-white border-slate-300 text-slate-900'}"
              />
              {#if uiFontColor}
                <button
                  type="button"
                  on:click={() => {
                    uiFontColor = '';
                    saveUiCustomizationSettings();
                  }}
                  class="px-2.5 py-1 rounded border font-mono text-[11px] {isDark
                    ? 'bg-slate-950 border-slate-700 text-slate-300 hover:text-white'
                    : 'bg-white border-slate-300 text-slate-700 hover:text-slate-950'}"
                >
                  Use Theme Auto Color
                </button>
              {/if}
            </div>
          </div>

          <!-- Section 3: Workspace Layout, Theme & Posture Border Intensity -->
          <div
            class="rounded-lg p-3.5 border space-y-3 {isDark
              ? 'bg-slate-900/90 border-slate-800'
              : 'bg-slate-50 border-slate-200'}"
          >
            <div class="font-bold font-mono uppercase tracking-wider {isDark ? 'text-amber-300' : 'text-amber-800'}">
              3. Enterprise Workspace Layout, Theme &amp; Execution Defaults
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 font-mono">
              <!-- Theme Mode -->
              <div class="p-2.5 rounded border space-y-1.5 {isDark ? 'bg-slate-950 border-slate-800' : 'bg-white border-slate-200'}">
                <div class="text-[11px] font-semibold">Theme Mode:</div>
                <div class="flex gap-1.5">
                  <button
                    type="button"
                    on:click={() => {
                      if (themeMode !== 'dark') toggleThemeMode();
                    }}
                    class="flex-1 py-1 rounded border text-[11px] {themeMode === 'dark'
                      ? 'bg-cyan-950 border-cyan-400 text-cyan-200 font-bold'
                      : 'bg-slate-100 border-slate-300 text-slate-700'}"
                  >
                    🌙 Dark
                  </button>
                  <button
                    type="button"
                    on:click={() => {
                      if (themeMode !== 'light') toggleThemeMode();
                    }}
                    class="flex-1 py-1 rounded border text-[11px] {themeMode === 'light'
                      ? 'bg-sky-600 border-sky-700 text-white font-bold'
                      : 'bg-slate-900 border-slate-700 text-slate-400'}"
                  >
                    ☀️ Light
                  </button>
                </div>
              </div>

              <!-- Window Layout Density -->
              <div class="p-2.5 rounded border space-y-1.5 {isDark ? 'bg-slate-950 border-slate-800' : 'bg-white border-slate-200'}">
                <div class="text-[11px] font-semibold">Window Layout Density:</div>
                <div class="flex gap-1.5">
                  <button
                    type="button"
                    on:click={() => {
                      uiPanelDensity = 'flush';
                      saveUiCustomizationSettings();
                    }}
                    class="flex-1 py-1 rounded border text-[11px] {uiPanelDensity === 'flush'
                      ? isDark
                        ? 'bg-cyan-950 border-cyan-400 text-cyan-200 font-bold'
                        : 'bg-sky-600 border-sky-700 text-white font-bold'
                      : isDark
                      ? 'bg-slate-900 border-slate-700 text-slate-400'
                      : 'bg-slate-100 border-slate-300 text-slate-700'}"
                    title="Zero gap around windows (Docked edge-to-edge enterprise layout)"
                  >
                    Flush (0px Gap)
                  </button>
                  <button
                    type="button"
                    on:click={() => {
                      uiPanelDensity = 'framed';
                      saveUiCustomizationSettings();
                    }}
                    class="flex-1 py-1 rounded border text-[11px] {uiPanelDensity === 'framed'
                      ? isDark
                        ? 'bg-cyan-950 border-cyan-400 text-cyan-200 font-bold'
                        : 'bg-sky-600 border-sky-700 text-white font-bold'
                      : isDark
                      ? 'bg-slate-900 border-slate-700 text-slate-400'
                      : 'bg-slate-100 border-slate-300 text-slate-700'}"
                  >
                    Framed
                  </button>
                </div>
              </div>

              <!-- Border / Glow Intensity -->
              <div class="p-2.5 rounded border space-y-1.5 {isDark ? 'bg-slate-950 border-slate-800' : 'bg-white border-slate-200'}">
                <div class="text-[11px] font-semibold">Posture Accent Glow:</div>
                <div class="flex gap-1">
                  {#each ['subtle', 'standard', 'high'] as gOpt}
                    <button
                      type="button"
                      on:click={() => {
                        uiGlowIntensity = gOpt;
                        saveUiCustomizationSettings();
                      }}
                      class="flex-1 py-1 rounded border text-[10px] uppercase {uiGlowIntensity === gOpt
                        ? isDark
                          ? 'bg-cyan-950 border-cyan-400 text-cyan-200 font-bold'
                          : 'bg-sky-600 border-sky-700 text-white font-bold'
                        : isDark
                        ? 'bg-slate-900 border-slate-700 text-slate-400'
                        : 'bg-slate-100 border-slate-300 text-slate-700'}"
                    >
                      {gOpt}
                    </button>
                  {/each}
                </div>
              </div>
            </div>

            <!-- Default Execution Toggles -->
            <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t font-mono {isDark ? 'border-slate-800' : 'border-slate-200'}">
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  bind:checked={runReasoningOnSubmit}
                  class="accent-cyan-500"
                />
                <span>Auto-Run 15-Engine Layered Reasoning on Query Submit</span>
              </label>

              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  bind:checked={thinkingEnabled}
                  on:change={syncSessionConfig}
                  class="accent-amber-500"
                />
                <span>Enable <code>--think</code> Chain-of-Thought Trace</span>
              </label>
            </div>
          </div>

          <!-- Section 4: Live Typography Preview -->
          <div
            class="rounded-lg p-3 border space-y-1.5 {isDark
              ? 'bg-slate-950 border-slate-800'
              : 'bg-white border-slate-300'}"
            style={customTextStyle}
          >
            <div class="text-[10px] font-mono uppercase tracking-wider opacity-70">
              Live Typography &amp; Color Preview ({uiFontSize}px • Line Height {uiLineHeight})
            </div>
            <div>
              [C.O.R.A. v{versionStr}] Active Project: <strong>Projects/{activeProject || 'RedTeam-01'}/Files/</strong> —
              {headerNetRows[0]
                ? `${headerNetRows[0].ifaceName} | ${headerNetRows[0].ipMask} | ↑${headerNetRows[0].txStr} ↓${headerNetRows[0].rxStr}`
                : 'eth0 | 10.0.0.10/24 | ↑0.0 KB/s ↓0.0 KB/s'}
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div
          class="px-4 py-2.5 border-t flex items-center justify-between gap-2 shrink-0 {isDark
            ? 'bg-slate-900/95 border-slate-800'
            : 'bg-slate-100 border-slate-200'}"
        >
          <span class="text-[11px] font-mono opacity-80">
            Settings are saved automatically to browser storage &amp; active session configuration.
          </span>
          <button
            type="button"
            on:click={() => (showSettingsModal = false)}
            class="px-4 py-1.5 rounded text-xs font-bold text-white bg-cyan-600 hover:bg-cyan-500"
          >
            ✓ Done
          </button>
        </div>
      </div>
    </div>
  {/if}
</div>
