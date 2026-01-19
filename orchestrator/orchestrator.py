"""
EVA Orchestrator (Independent Version: 1.3.0)
Architecture:
    User Input
        ↓
    Phase 1: Perception (CIM + LLM extract stimulus)
        ↓
    The Gap: PhysioController + EVA Matrix + Artifact Qualia + PRN (Connected via Resonance Bus)
        ↓
    Phase 2: Reasoning (CIM + LLM generate RESPONSE with 40/60 weighting)
        ↓
    Write to MSP (Episodic Memory)
"""

import sys
import os
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import yaml

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from capabilities.tools.logger import safe_print
from operation_system.identity_manager import IdentityManager
import time

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Resonance Bus Interface
from operation_system.resonance_bus import bus

# Biological & Psychological Systems
from physio_core.physio_core import PhysioCore
from eva_matrix.eva_matrix import EVAMatrixSystem
from artifact_qualia.artifact_qualia import ArtifactQualiaSystem
from orchestrator.Module.CIM.Node.prompt_rule.prompt_rule_node import PromptRuleNode

# Cognitive & Memory
from orchestrator.Module.CIM.cim_module import CIMModule as ContextInjectionModule
from capabilities.services.agentic_rag.agentic_rag_engine import AgenticRAG
from memory_n_soul_passport.memory_n_soul_passport_engine import MSP
from operation_system.llm_bridge.llm_bridge import LLMBridge, SYNC_BIOCOGNITIVE_STATE_TOOL, PROPOSE_EPISODIC_MEMORY_TOOL
from operation_system.llm_bridge.ollama_bridge import OllamaBridge
# [NEW] Bridges
from capabilities.services.slm_bridge.slm_bridge import slm
from capabilities.services.vector_bridge.chroma_bridge import ChromaVectorBridge
from operation_system.rim.rim_engine import rim_calc
from operation_system.resonance_engine.resonance_engine import ResonanceEngine
from genesis_knowledge_system.gks_interface import gks_interface  # [NEW] V9.3.0G
from resonance_memory_system.rms import RMSEngineV6
# [NEW] Engram System (Conditional Memory)
from capabilities.services.engram_system.engram_engine import EngramEngine
# [NEW] Session Manager
from orchestrator.Node.session_node import SessionNode as SessionManager
# [NEW] Trajectory System
from operation_system.trajectory.trajectory_manager import TrajectoryManager
# [NEW] Execution Engine
from orchestrator.Execution.CognitiveFlow.master_flow_engine import MasterFlowEngine

class EVAOrchestrator:
    """
    EVA 8.2.0: Main Orchestrator (Resonance Edition)
    """

    def __init__(
        self,
        mock_mode: Optional[bool] = None,
        enable_physio: Optional[bool] = None,
        llm_backend: Optional[str] = None,  # "gemini" or "ollama"
        ollama_model: Optional[str] = None
    ):
        safe_print(f"🚀 Initializing EVA Orchestrator (v1.2.0)...")

        # --------------------------------------------------
        # 0. Load Unified Configuration
        # --------------------------------------------------
        self.config_path = Path(__file__).parent / "configs" / "orchestrator_configs.yaml"
        self.config_data = {}
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = yaml.safe_load(f)
                safe_print(f"  - Loaded unified config from {self.config_path.name}")
            except Exception as e:
                safe_print(f"  ⚠️ Error loading unified config: {e}")
        
        # Override with parameters or config defaults
        orch_params = self.config_data.get("orchestrator", {}).get("parameters", {})
        self.mock_mode = mock_mode if mock_mode is not None else orch_params.get("mock_mode", False)
        self.enable_physio = enable_physio if enable_physio is not None else orch_params.get("enable_physio", True)
        self.llm_backend = llm_backend if llm_backend is not None else orch_params.get("llm_backend", "gemini")
        ollama_model = ollama_model if ollama_model is not None else orch_params.get("ollama_model", "llama3.2:3b")
        self.recording_active = orch_params.get("recording_active", True) # Default: ON for Resonance Edition
        
        # [NEW] Cognitive Strategy
        self.gks_enabled = orch_params.get("gks_enabled", True)
        self.nexus_mode = orch_params.get("nexus_mode", False)
        safe_print(f"  - Cognition: GKS={'ON' if self.gks_enabled else 'OFF'}, NexusMode={'ON' if self.nexus_mode else 'OFF'}")

        # Runtime Settings
        runtime_cfg = self.config_data.get("orchestrator", {}).get("runtime", {})
        self.session_timeout = runtime_cfg.get("session_timeout", 1800)

        safe_print(f"  - Mode: {self.llm_backend.upper()}, Physio: {self.enable_physio}")

        safe_print("  - Initializing MSP Engine...")
        self.msp = MSP()

        # [NEW] Configuration Binding: Execution Protocol
        exec_cfg = self.config_data.get("execution_protocol", {})
        exec_status = exec_cfg.get("status", "Unknown")
        safe_print(f"  - Execution Protocol: {exec_status} (Flow: Unified 3-Phase)")

        # --------------------------------------------------
        # 1. Initialize Resonance Bus
        # --------------------------------------------------
        self.bus = bus
        self.session_id = self._generate_session_id()
        self.bus.initialize_session(self.session_id)
        self.bus_log = []
        
        # Monitor all core channels
        for channel in [
            IdentityManager.BUS_PHYSICAL,
            IdentityManager.BUS_PSYCHOLOGICAL,
            IdentityManager.BUS_PHENOMENOLOGICAL,
            IdentityManager.BUS_KNOWLEDGE
        ]:
            self.bus.subscribe(channel, lambda p, c=channel: self.bus_log.append((c, p)))

        # Memory & RAG handles follow initialization

        safe_print("  - Initializing AgenticRAG...")
        self.agentic_rag = AgenticRAG(msp_client=self.msp, bus=self.bus)

        # --------------------------------------------------
        # 3. Initialize Biological & Psychological Mind (The Gap)
        # --------------------------------------------------
        if self.enable_physio:
            safe_print("  - Initializing PhysioCore (v2.4.3)...")
            base_physio = Path(__file__).parent.parent / "physio_core" / "configs"
            self.physio = PhysioCore(
                config_path=str(base_physio / "PhysioCore_configs.yaml"),
                msp=self.msp,
                bus=self.bus
            )
            # Inject unified config for component-specific settings (Digestion Delay, etc.)
            self.physio.config = self.config_data
            
            safe_print("  - Initializing EVA Matrix (Psyche Core)...")
            project_root = Path(__file__).parent.parent
            self.matrix = EVAMatrixSystem(base_path=project_root, msp=self.msp, bus=self.bus)
            
            safe_print("  - Initializing Artifact Qualia (Phenomenology Core)...")
            self.qualia = ArtifactQualiaSystem(base_path=project_root, msp=self.msp, bus=self.bus)
            
            safe_print("  - Initializing PRN (Prompt Rule Node)...")
            # PRN will auto-detect the unified config path if we update its engine
            self.prn = PromptRuleNode(msp=self.msp, bus=self.bus)
        else:
            self.physio = self.matrix = self.qualia = self.prn = None

        # --------------------------------------------------
        # 3.5 Initialize Vector Store & Engram (Long-Term Memory)
        # --------------------------------------------------
        # Initialize AFTER basic setup but BEFORE CIM
        self.vector_db = ChromaVectorBridge()
        
        safe_print("  - Initializing Engram System (O(1) Memory)...")
        self.engram = EngramEngine()

        # --------------------------------------------------
        # 4. Initialize Cognitive Layer (CIM)
        # --------------------------------------------------
        safe_print("  - Initializing CIM (Context Injection Module)...")
        root_path = Path(__file__).parent.parent
        self.cim = ContextInjectionModule(
            physio_controller=self.physio,
            msp_client=self.msp,
            hept_stream_rag=self.agentic_rag,
            eva_persona_governor=self.prn, # [NEW] PRN provides identity suite
            base_path=root_path
        )

        print(f"  - Initializing LLM Bridge ({self.llm_backend.upper()})...")
        if self.mock_mode:
            from tests.mock_llm import MockLLM
            self.llm = MockLLM()
            safe_print("  ⚠️ [MOCK MODE] LLM Bridge replaced with MockLLM.")
        elif self.llm_backend.lower() == "ollama":
            ollama_ctx = orch_params.get("ollama_context_window", 32768)
            self.llm = OllamaBridge(model=ollama_model, context_window=ollama_ctx)
        else:
            self.llm = LLMBridge()

        # Session state
        # Fix: Load persistent session if available, else new
        if hasattr(self.bus, 'current_session_id') and self.bus.current_session_id:
             self.session_id = self.bus.current_session_id
             
        # [NEW] Session Manager (Delegate Lifecycle)
        self.session_manager = SessionManager(
            msp_engine=self.msp,
            bus_system=self.bus,
            gks_interface=gks_interface
        )
        
        # [NEW] Trajectory Manager (Execution Trace Logger)
        safe_print("  - Initializing Trajectory Manager (Trace Logger)...")
        self.trajectory = TrajectoryManager()
        
        # [NEW] Resonance Engine (4-Layer Resonance)
        safe_print("  - Initializing Resonance Engine (4-Layer Pipeline)...")
        self.resonance = ResonanceEngine()
        # [NEW] RMS Activation (V9.4.3)
        safe_print("  - Initializing RMS (Resonance Memory System v6.2.0)...")
        self.rms = RMSEngineV6(config=self.config_data.get("rms", {}))

        
        self.pending_session_end = False # For confirmation flow
        self.last_interaction = datetime.now()
        self.session_start_time = datetime.now()

        # [NEW] Sync with CIM Context Store (Store-Centric)
        self.current_context_id = self.cim.current_context_id
        # Turn count still managed by MSP for history, but synced via CIM
        last_context = self.msp.load_turn_context()
        self.turn_count = last_context.get("turn_index", 0) + 1

        self.current_turn_user_fragment: Optional[Dict] = None

        # [AUTO-START] Ensure session is active by default for API usage
        if not self.session_manager.recording_active:
             self.session_manager._start_new_session()

        # [NEW] Master Flow Engine (Logic Delegation)
        self.master_flow = MasterFlowEngine(self)

        print(f"✅ EVA Orchestrator ready! (Session: {self.session_id})\n")


    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Main entry point: Dual-Phase One-Inference Flow (Resonance Aware)
        """
        # --- [NEW] Session Control Delegation ---
        session_response = self.session_manager.process_command(user_input)
        if session_response:
             # If SessionManager handled it (Start/Stop/Confirm), return immediately
             return session_response
        
        # --- Timeout Check (Auto-Close) ---
        if hasattr(self, 'last_interaction'):
             timeout_response = self.session_manager.check_timeout(self.last_interaction)
             if timeout_response:
                 return timeout_response

        # --- Standard Orchestration Flow (Only if Recording Active) ---
        if not self.session_manager.recording_active:
             return {"final_response": "Recording Paused. Type '/start' to begin.", "emotion_label": "Neutral", "resonance_hash": "IDLE"}
             
        self.session_id = self.session_manager.session_id
        self.last_interaction = datetime.now()

        # Status Indicator
        status_icon = "🔴" if self.recording_active else "⚪"
        wait_icon = "⏳" if self.pending_session_end else ""
        safe_print(f"Status: {status_icon}{wait_icon} Rec: {'ON' if self.recording_active else 'OFF'}")
        
        # Guard: If recording is OFF, don't process.
        if not self.recording_active:
             msg = "เซสชั่นเก่าปิดไปแล้วครับ 🔒 หากต้องการคุยต่อ กรุณาพิมพ์ /start เพื่อเริ่มเซสชั่นใหม่ (Previous session ended. Type /start to begin a new one.)"
             return {"final_response": msg, "emotion_label": "Neutral", "resonance_hash": "OFF"}

        # --------------------------------------------------
        # DELEGATION: CNS Master Flow Engine (The Brain)
        # --------------------------------------------------
        result = self.master_flow.run_turn(user_input)
        
        # Resonance Report
        self._print_resonance_report()

        return result

    def _print_resonance_report(self):
        """Displays chronological signal propagation on the Resonance Bus."""
        safe_print(f"\n📡 [RESONANCE TRANSFER REPORT - CYCLE {self.turn_count}]")
        safe_print("=" * 60)
        if not self.bus_log:
            safe_print("  ∅ No bus activity detected.")
            return

        for i, (channel, payload) in enumerate(self.bus_log):
            # Normalize channel name (handle BUS: prefix)
            clean_channel = channel.lower().replace("bus:", "").strip()
            
            comp_map = {
                IdentityManager.BUS_PHYSICAL: IdentityManager.SYSTEM_PHYSIO,
                IdentityManager.BUS_PSYCHOLOGICAL: IdentityManager.SYSTEM_MATRIX,
                IdentityManager.BUS_PHENOMENOLOGICAL: IdentityManager.SYSTEM_QUALIA,
                IdentityManager.BUS_KNOWLEDGE: IdentityManager.SYSTEM_PRN
            }
            comp = comp_map.get(channel, "Unknown")
            
            summary = ""
            if clean_channel == "physical":
                ans = payload.get('ans_state',{})
                summary = f"ANS: S={ans.get('sympathetic',0):.2f}/P={ans.get('parasympathetic',0):.2f}"
            elif clean_channel == "psychological":
                summary = f"Emotion: {payload.get('matrix_state', {}).get('emotion_label')}"
            elif clean_channel == "phenomenological":
                summary = f"Tone: {payload.get('qualia_snapshot', {}).get('tone')}, Intensity: {payload.get('qualia_snapshot', {}).get('intensity', 0):.2f}"
            elif clean_channel == "knowledge":
                summary = f"Policies Injected: {len(payload.get('behavior_policy', []))}"
            else:
                 # Debug: Show keys if unknown
                 summary = f"Keys: {list(payload.keys())[:3]}"

            safe_print(f"  {i+1:02d} | [{channel:<16}] | {comp:<18} | {summary}")

        safe_print("-" * 60)
        safe_print(f"  🔑 StateHash_S1: {self.bus.generate_state_hash()}")
        safe_print("=" * 60)

    def _format_qualia_for_llm(self, qualia: Any) -> str:
        if isinstance(qualia, dict): return f"Intensity: {qualia.get('intensity',0):.2f}, Tone: {qualia.get('tone')}"
        return f"Intensity: {qualia.intensity:.2f}, Tone: {qualia.tone}"

    def _analyze_session_completion(self, session_id: str, closure_reason: str = "unknown") -> Dict[str, Any]:
        """
        Analyze session history using LLM to generate semantic event segmentation.
        Includes closure tracking and memorable quotes extraction.
        """
        safe_print(f"\n🔍 Analyzing Session for Compression (Reason: {closure_reason})...")
        
        # 1. Retrieve raw episodes
        all_eps = self.msp._read_all_episodes_from_log()
        session_eps = [ep for ep in all_eps if ep.get("session_id") == session_id]
        
        if not session_eps:
            return {}

        # Sort
        session_eps.sort(key=lambda x: x.get("timestamp", ""))
        
        # 2. Pre-extract Memorable Quotes (High RIM)
        raw_quotes = self.msp.extract_memorable_quotes(session_id, min_rim=0.8, limit=10)
        quotes_context = ""
        for i, q in enumerate(raw_quotes):
             quotes_context += f"[{i+1}] EP: {q['episode_id']} | RIM: {q['rim_score']} | Context: {q['context']}\n"
        
        # 3. Prepare Episode Summaries for Segmentation
        ep_summaries = []
        for ep in session_eps:
             eid = ep.get("episode_id")
             intent = ep.get("intent", "unknown")
             summ = "N/A"
             if "turn_llm" in ep:
                 summ = ep.get("turn_llm", {}).get("salience_anchor", {}).get("phrase", "N/A")
             elif "turn_1" in ep:
                 summ = ep.get("turn_1", {}).get("raw_text", "")[:50]
             
             ep_summaries.append(f"- {eid}: {intent} | {summ}...")

        context_str = "\n".join(ep_summaries)
        
        # 4. Prompt LLM
        prompt = f"""
        You are the Cognitive Cortex of EVA 9.1.0. Analyze this session history and segment it into Semantic Events.
        
        SESSION METADATA:
        Session ID: {session_id}
        Closure Reason: {closure_reason}
        
        POTENTIAL MEMORABLE QUOTES (RIM >= 0.8):
        {quotes_context if quotes_context else "None identified."}

        SESSION HISTORY:
        {context_str}
        
        INSTRUCTIONS:
        1. Identify the Overarching Objective of this session.
        2. Determine the Session Status (Success, Failed, or Continuous).
        3. Extract a Motto or Key Phrase that captures the essence of the session.
        4. Group consecutive episodes into logical "Events".
        5. Select the TOP 3 most impactful Memorable Quotes from the provided list or the history.
           Ensure each quote has its episode_id, rim_score, and a short context.
        6. Provide a high-level Knowledge Synthesis (session_summary).
        7. Return JSON format strictly.
        
        FORMAT:
        {{
            "session_objective": "...",
            "session_status": "...",
            "session_motto": "...",
            "closure_reason": "{closure_reason}",
            "memorable_quotes": [
                {{"quote": "...", "rim_score": 0.9, "episode_id": "EVA_EPxx", "context": "..."}}
            ],
            "events": [
                {{"label": "...", "summary": "...", "start_episode_id": "...", "end_episode_id": "..."}}
            ],
            "session_summary": "..."
        }}
        """
        
        try:
             # Use simple generation (no tools needed for this internal thought)
             response = self.llm.generate(prompt, temperature=0.3)
             text = response.text
             
             # Clean markdown json
             if "```json" in text:
                 text = text.split("```json")[1].split("```")[0].strip()
             elif "```" in text:
                 text = text.split("```")[1].split("```")[0].strip()
                 
             analysis = json.loads(text)
             safe_print("  ✓ Session segmentation complete.")
             return analysis
             
        except Exception as e:
             safe_print(f"  ⚠️ Session analysis failed: {e}")
             return {}

    @property
    def umbrella_active(self) -> bool:
        """Check if Umbrella (Transcendent Layer) is active."""
        if hasattr(self, 'resonance') and self.resonance:
            return self.resonance.umbrella_active
        return False

    def _generate_session_id(self): 
        """Generate session ID aligned with session memory naming"""
        dev_id = self.msp.identity_config.get("instance", {}).get("developer_id", "THA-06")
        counters = self.msp.system_registry.get("counters", {})
        return IdentityManager.generate_session_id(
            dev_id=dev_id,
            sphere=counters.get("sphere_seq", 0),
            core=counters.get("core_seq", 0),
            session=counters.get("session_seq", 0)
        )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="EVA Orchestrator (v1.2.0)")
    parser.add_argument("--ollama", action="store_true", help="Use Ollama backend")
    parser.add_argument("--model", type=str, default="llama3.2:3b", help="Ollama model name")
    args = parser.parse_args()

    # Initialize Orchestrator
    llm_backend = "ollama" if args.ollama else "gemini"
    orch = EVAOrchestrator(llm_backend=llm_backend, ollama_model=args.model)

    safe_print("\n" + "="*60)
    safe_print("🧘 EVA 9.1.0 (Resonance Edition) - Living Sandbox")
    safe_print("="*60)
    safe_print("Type 'exit' to end session or 'reset' to clear context.")
    safe_print("-" * 60)

    try:
        while True:
            # Use input() but encode/decode safely if needed
            try:
                user_input = input("\n👤 YOU: ").strip()
            except EOFError:
                break
                
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "bye"]:
                safe_print("\n[SYSTEM] Terminating organism loop. Saving state...")
                break
            if user_input.lower() == "reset":
                orch.msp.save_turn_context({})
                safe_print("\n[SYSTEM] Context cleared.")
                continue

            # Process turn
            try:
                result = orch.process_user_input(user_input)
                safe_print(f"\n✨ EVA: {result['final_response']}")
                safe_print(f"📊 State Hash: {result['resonance_hash']}")
            except Exception as e:
                safe_print(f"\n❌ CRITICAL ERROR: {e}")
                import traceback
                traceback.print_exc()

    except KeyboardInterrupt:
        safe_print("\n[SYSTEM] Interrupted by user.")
    
    safe_print("\nSession ended. Goodbye.")

from resonance_memory_system.rms import RMSEngineV6