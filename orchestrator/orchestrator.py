"""
EVA 8.2.0-R1: Main Orchestrator (Resonance Edition)
Refactor Date: 2026-01-04

Architecture:
    User Input
        ↓
    Phase 1: Perception (CIM + LLM extract stimulus)
        ↓
    The Gap: PhysioController + EVA Matrix + Artifact Qualia + PMT (Connected via Resonance Bus)
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

from tools.logger import safe_print
from operation_system.identity_manager import IdentityManager
import time

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Resonance Bus Interface
from operation_system.resonance_bus import bus

# Biological & Psychological Systems
from eva.physio_core.physio_core import PhysioCore
from eva.eva_matrix.eva_matrix import EVAMatrixSystem
from eva.artifact_qualia.artifact_qualia import ArtifactQualiaSystem
from orchestrator.cim.prompt_rule.prompt_rule_node import PromptRuleNode

# Cognitive & Memory
from orchestrator.cim.cim import ContextInjectionModule
from services.agentic_rag.agentic_rag_engine import AgenticRAG
from eva.memory_n_soul_passport.memory_n_soul_passport_engine import MSP
from operation_system.llm_bridge.llm_bridge import LLMBridge, SYNC_BIOCOGNITIVE_STATE_TOOL, PROPOSE_EPISODIC_MEMORY_TOOL
from operation_system.llm_bridge.ollama_bridge import OllamaBridge
# [NEW] Bridges
from services.slm_bridge.slm_bridge import slm
from services.vector_bridge.chroma_bridge import ChromaVectorBridge
from services.vector_bridge.chroma_bridge import ChromaVectorBridge
from operation_system.rim_calculator import rim_calc
from eva.genesis_knowledge_system.gks_interface import gks_interface  # [NEW] V9.3.0G

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
        safe_print(f"🚀 Initializing EVA 9.1.0 Orchestrator (Resonance Edition)...")

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
        self.agentic_rag = AgenticRAG(msp_client=self.msp)

        # --------------------------------------------------
        # 3. Initialize Biological & Psychological Mind (The Gap)
        # --------------------------------------------------
        if self.enable_physio:
            safe_print("  - Initializing PhysioCore (v9.1.0-C1)...")
            base_physio = Path(__file__).parent.parent / "eva" / "physio_core" / "configs"
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
        # 3.5 Initialize Vector Store (Long-Term Memory)
        # --------------------------------------------------
        # Initialize AFTER basic setup but BEFORE CIM
        self.vector_db = ChromaVectorBridge()

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
        if self.llm_backend.lower() == "ollama":
            ollama_ctx = orch_params.get("ollama_context_window", 32768)
            self.llm = OllamaBridge(model=ollama_model, context_window=ollama_ctx)
        else:
            self.llm = LLMBridge()

        # Session state
        # Fix: Load persistent session if available, else new
        if hasattr(self.bus, 'current_session_id') and self.bus.current_session_id:
             self.session_id = self.bus.current_session_id
             
        self.pending_session_end = False # For confirmation flow
        self.last_interaction = datetime.now()
        self.session_start_time = datetime.now()

        # [NEW] Sync with CIM Context Store (Store-Centric)
        self.current_context_id = self.cim.current_context_id
        # Turn count still managed by MSP for history, but synced via CIM
        last_context = self.msp.load_turn_context()
        self.turn_count = last_context.get("turn_index", 0) + 1

        self.current_turn_user_fragment: Optional[Dict] = None

        print(f"✅ EVA 9.1.0 ready! (Session: {self.session_id})\n")

    def _execute_the_gap(self, stimulus: Dict[str, Any], query_text: str = "") -> Dict[str, Any]:
        """
        Execute The Gap: Biological processing without LLM.
        
        Args:
            stimulus: Extracted from sync_biocognitive_state() call
            query_text: Raw user input for re-ranking
            
        Returns:
            Rich bio state to feed back to LLM for embodied reasoning
        """
        safe_print("\n⚡ STEP 2: The Gap - Bio-Digital Sync")
        
        # [NEW] Configuration Binding: Chunking Protocol
        chunk_cfg = self.config_data.get("chunking_protocol", {})
        max_chunks = chunk_cfg.get("max_chunks", 1)
        delay_ms = chunk_cfg.get("digestion_delay_ms", 0)
        
        # 1. Physio Core Processing (with Chunking Simulation)
        safe_print(f"  - [Process A] Physio Core: Chunking hormonal response (Max: {max_chunks})...")
        
        physio_result = {}
        for i in range(max_chunks):
            # Split processing if needed, for now we run master step and simulate chunks
            physio_result = self.physio.step(
                eva_stimuli=[stimulus] if i == 0 else [], # Apply stimulus on first chunk
                zeitgebers={"active": 0.5},
                dt=60.0 / max_chunks
            )
            safe_print(f"    [Chunk {i+1}/{max_chunks}] Processing signal: {stimulus.get('salience_anchor', 'N/A')}")
            
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)

        safe_print(f"  - [Sync Complete] Physiological state updated.")
        
        # 2. Matrix Update
        safe_print("  - [Process B] EVA Matrix: Recalculating psychological state...")
        matrix_result = self.matrix.process_signals(physio_result.get("blood", {}))
        
        # 3. Qualia Generation
        qualia_snap = self.qualia.process_experience()
        qualitative_exp = f"Intensity: {qualia_snap.get('intensity', 0.8):.2f}, Tone: {qualia_snap.get('tone', 'neutral')}"
        safe_print(f"  - Qualia Color: {qualia_snap.get('tone', 'neutral')} | Experience: {qualitative_exp}")
        
        # 4. Two-Stage RAG
        # 4. Two-Stage RAG: Correctly call Fast + Deep retrieval
        safe_print("  - [Process C] Two-Stage RAG: Quick Recall (parallel) + Deep Recall...")
        
        # Stage 1: Quick Recall
        quick_query = {
            "tags": stimulus.get("tags", []),
            "context_id": "auto"
        }
        quick_matches = self.agentic_rag.retrieve_fast(quick_query)
        safe_print(f"  - Quick Recall: {len(quick_matches)} matches")

        # Stage 2: Deep Recall
        deep_query = {
            "tags": stimulus.get("tags", []),
            "ans_state": physio_result.get("autonomic", {}),
            "blood_levels": physio_result.get("blood", {}),
            "qualia_texture": qualia_snap
        }
        deep_matches = self.agentic_rag.retrieve_deep(deep_query)
        safe_print(f"  - Deep Recall: {len(deep_matches)} matches")

        # Merge results with Cross-Encoder Reranking
        unique_memories = self.agentic_rag.merge_results(quick_matches, deep_matches, user_query=query_text)
        safe_print(f"  - Merged & Reranked: {len(unique_memories)} highly relevant episodes")
        
        # 5. RMS scan
        safe_print(f"  - RMS: Scanning for '{matrix_result.get('emotion_label', 'neutral')}' resonance chains...")
        
        # 6. Format for LLM Continuation
        return {
            "biological_state": {
                "hormones": {k: round(v, 4) for k, v in physio_result.get("blood", {}).items()},
                "autonomic": physio_result.get("autonomic", {})
            },
            "psychological_state": matrix_result.get("axes_9d", {}),
            "emotion_label": matrix_result.get("emotion_label", "neutral"),
            "embodied_sensation": qualitative_exp,
            "qualia_tone": qualia_snap.get("tone", "neutral"),
            "retrieved_memories": [
                {"content": m.content[:150] + "...", "emotion": getattr(m, "emotion_label", "N/A")}
                for m in list(unique_memories)[:3]
            ],
            "instruction": "Use this biological and psychological state to formulate an embodied response. Your response should reflect the current emotional state."
        }

    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Main entry point: Dual-Phase One-Inference Flow (Resonance Aware)
        """
        # --- Session Control Commands ---
        cmd = user_input.strip().lower()

        # 1. Handle Pending Confirmation
        if self.pending_session_end:
            if any(word in cmd for word in ["y", "yes", "confirm", "ok", "ยืนยัน", "ครับ", "ค่ะ"]):
                self.recording_active = False
                self.pending_session_end = False
                
                # Perform Session Analysis (LLM-based) with closure reason
                session_analysis = self._analyze_session_completion(self.session_id, closure_reason="user_command")
                
                # Finalize Session in MSP with analysis
                digest = self.msp.end_session(self.session_id, session_analysis=session_analysis)
                
                # --- ARCHIVAL WORKFLOW ---
                # 1. Collect referenced episodes (quotes + events)
                referenced_eps = []
                if digest:
                    # Quotes
                    referenced_eps.extend([q.get("episode_id") for q in digest.get("memorable_quotes", []) if q.get("episode_id")])
                    # Events
                    for evt in digest.get("event_classification", []):
                        referenced_eps.extend(evt.get("episode_range", []))
                
                # 2. Trigger MSP Archival
                archive_stats = self.msp.archive_processed_episodes(self.session_id, list(set(referenced_eps)))
                safe_print(f"  ✓ Archival: {archive_stats.get('archived_count',0)} episodes moved to cold storage.")

                safe_print(f"\nzzz [STOP] SESSION ENDED: {self.session_id}")
                return {"final_response": "Session Closed. Recording Stopped, Compressed, and Archived.", "emotion_label": "Calm", "resonance_hash": "END"}
            else:
                self.pending_session_end = False
                safe_print(f"\n🔄 [RESUME] Stop cancelled. Recording continues.")
                return {"final_response": "Session Continuation Confirmed.", "emotion_label": "Alert", "resonance_hash": "RESUME"}

        # Command Keywords
        start_keywords = ["/start", "เริ่ม", "อัด", "rec", "start session"]
        stop_keywords = ["/stop", "/end", "พอ", "หยุด", "จบ", "ปิดเซสชั่น", "quit session"]

        if any(word in cmd for word in start_keywords):
            self.recording_active = True
            
            # Start new session in MSP (Increments counters)
            new_counters = self.msp.start_new_session()
            
            # Generate new session ID from updated counters
            self.session_id = self._generate_session_id()
            self.bus.current_session_id = self.session_id
            
            self.turn_count = 0
            self.session_start_time = datetime.now()
            safe_print(f"\n🔴 [REC] SESSION STARTED: {self.session_id}")
            safe_print(f"  - Counters: Session {new_counters.get('session_seq')}, Core {new_counters.get('core_seq')}")
            return {"final_response": f"Session Started. Recording Active. (ID: {self.session_id})", "emotion_label": "Alert", "resonance_hash": "INIT"}
            
        elif any(word in cmd for word in stop_keywords):
            if not self.recording_active:
                return {"final_response": "Recording is already OFF.", "emotion_label": "Neutral", "resonance_hash": "INFO"}
            
            # Generate Summary (ENRICHED)
            now = datetime.now()
            duration = now - getattr(self, 'session_start_time', now)
            duration_minutes = duration.total_seconds() / 60
            
            summary = f"""
            📝 SESSION SUMMARY ({self.session_id})
            - Duration: {duration_minutes:.1f} minutes
            - Episodes (Turns): {self.turn_count}
            - Last Resonance Index: {self.bus.get_last_state_hash()[:8]}
            - Semantic Events: {len(self.bus_log)} signals processed in last turn
            """
            safe_print(Text(summary, style="bold cyan"))
            safe_print("\n⚠️  CONFIRM END SESSION? (y/n / ยืนยัน)")
            
            self.pending_session_end = True
            return {"final_response": f"Session Summary Generated. Please confirm end of session (y/n).", "emotion_label": "Waiting", "resonance_hash": "WAIT"}

        # --- Timeout Logic (e.g., 30 mins) ---
        # --- Timeout Logic (Configurable) ---
        time_diff = (datetime.now() - self.last_interaction).total_seconds()
        if self.recording_active and time_diff > self.session_timeout:
             self.recording_active = False
             
             # Finalize Session on Timeout
             if hasattr(self, 'session_id') and self.session_id:
                 try:
                     analysis = self._analyze_session_completion(self.session_id, closure_reason="timeout")
                     digest = self.msp.end_session(self.session_id, session_analysis=analysis)
                     
                     # Trigger Archival for Timeout
                     referenced_eps = []
                     if digest:
                         referenced_eps.extend([q.get("episode_id") for q in digest.get("memorable_quotes", []) if q.get("episode_id")])
                         for evt in digest.get("event_classification", []):
                             referenced_eps.extend(evt.get("episode_range", []))
                     
                     self.msp.archive_processed_episodes(self.session_id, list(set(referenced_eps)))
                 except Exception as e:
                     print(f"  ⚠️ Timeout archival failed: {e}")
                     self.msp.end_session(self.session_id)
                 
             safe_print(f"\n⚠️ [TIMEOUT] Session auto-closed due to inactivity (30m). Data compressed.")
        self.last_interaction = datetime.now()

        # Status Indicator
        status_icon = "🔴" if self.recording_active else "⚪"
        wait_icon = "⏳" if self.pending_session_end else ""
        safe_print(f"Status: {status_icon}{wait_icon} Rec: {'ON' if self.recording_active else 'OFF'}")
        
        # Guard: If recording is OFF, don't process.
        if not self.recording_active:
             msg = "เซสชั่นเก่าปิดไปแล้วครับ 🔒 หากต้องการคุยต่อ กรุณาพิมพ์ /start เพื่อเริ่มเซสชั่นใหม่ (Previous session ended. Type /start to begin a new one.)"
             return {"final_response": msg, "emotion_label": "Neutral", "resonance_hash": "OFF"}

        self.turn_count += 1
        self.bus_log = [] # Clear log for fresh monitoring
        print(f"\n{'='*60}")
        print(f"🎯 Turn {self.turn_count} (Resonance Exchange)")
        print(f"{'='*60}")

        # Trigger CIM to start a new turn context (Store-Centric)
        self.cim.start_new_turn_context()
        context_id = self.cim.current_context_id
        
        
        # ============================================================
        # SINGLE LLM SESSION: PHASE 1 - Initial Call & Stimulus Extraction
        # ============================================================
        safe_print("🧠 STEP 1: Single-Session Orchestration - Perception")
        
        # [NEW] Phase 2: User Identification
        current_speaker_profile = None
        try:
            # 1. Identify Speaker
            speaker_info = self.msp.user_registry.identify_speaker(user_input)
            user_id = speaker_info.get("user_id", "unknown")
            confidence = speaker_info.get("confidence", 0.0)
            
            safe_print(f"  - 👤 Speaker Identified: {speaker_info.get('username')} (ID: {user_id}, Conf: {confidence:.2f})")
            
            # 2. Get Full Profile (Grounding Facts)
            if user_id != "unknown":
                current_speaker_profile = self.msp.user_registry.get_user_profile(user_id)
                
            # 3. Update Interaction Count
            if user_id != "unknown":
                self.msp.user_registry.increment_interaction(user_id)
                
        except Exception as e:
            safe_print(f"  ⚠️ User Identification Failed: {e}")

        
        # Capture live physio snapshot (Background state)
        live_physio = None
        if self.enable_physio:
            live_physio = self.physio.get_state()
            safe_print("  - Captured live physio snapshot.")

        # [NEW] Pre-Inference: Intent & Fast Recall
        safe_print("  - [Cognitive Gateway] Extracting intent (SLM) & retrieving fast memories...")
        try:
            slm_result = slm.extract_intent(user_input)
            
            # Use RIM Calculator for instinctual impact
            slm_impact = rim_calc.calculate_impact(
                slm_result.get("emotional_signal", "neutral"),
                slm_result.get("salience_anchor", "None")
            )
            slm_result["rim_impact"] = slm_impact
            
            safe_print(f"    > Intent: {slm_result.get('intent')}")
            safe_print(f"    > Instinctual Signal: {slm_result.get('emotional_signal')} (Impact: {slm_impact:.2f})")
            safe_print(f"    > Salience Anchor: {slm_result.get('salience_anchor')}")
            
            fast_mems = self.vector_db.query_memory(user_input, n_results=3)
            safe_print(f"    > Fast Recall: Found {len(fast_mems)} memories")
        except Exception as e:
            safe_print(f"    > ⚠️ Gateway Error: {e}")
            slm_result = {"intent": "unknown", "emotional_signal": "neutral", "salience_anchor": "None", "rim_impact": 0.0}
            fast_mems = []

        # Build initial context for perception
        phase1_context = self.cim.inject_phase_1(
            user_input, 
            live_physio=live_physio,
            slm_data=slm_result,
            long_term_memory=fast_mems,
            user_profile=current_speaker_profile  # [NEW] Pass Profile
        )
        phase1_prompt = self.cim.build_phase_1_prompt(phase1_context)
        self.cim.save_markdown_context("step1_perception", phase1_prompt)

        # Initial LLM call with both tools available
        safe_print(f"  - Calling {self.llm_backend.upper()} (Session Start) with tools: sync + propose...")
        llm_response = self.llm.generate(
            phase1_prompt,
            tools=[SYNC_BIOCOGNITIVE_STATE_TOOL, PROPOSE_EPISODIC_MEMORY_TOOL],
            temperature=0.7
        )

        # Extract stimulus from function call
        if not llm_response.tool_calls:
            safe_print("  ⚠️ Warning: LLM skipped stimulus extraction")
            stimulus = {"valence": 0.5, "arousal": 0.3, "intensity": 0.3, "tags": ["greeting"], "salience_anchor": "N/A"}
        else:
            tool_call = llm_response.tool_calls[0]
            if tool_call.name != "sync_biocognitive_state":
                safe_print(f"  ⚠️ Unexpected tool call: {tool_call.name}")
                stimulus = {"valence": 0.5, "arousal": 0.3, "intensity": 0.3, "tags": ["unknown"], "salience_anchor": "N/A"}
            else:
                stimulus = tool_call.args
                confidence = stimulus.get('confidence_score', 0.5)
                
                # [NEW] Perception Delegation Logic
                # If LLM is confident (>0.9) and didn't provide a vector, use SLM gut vector
                if not stimulus.get("stimulus_vector") and confidence > 0.9:
                    safe_print(f"  ✓ High Confidence ({confidence:.2f}): Accepting SLM Gut Instinct vector.")
                    stimulus["stimulus_vector"] = slm_result.get("gut_vector", {})
                elif not stimulus.get("stimulus_vector"):
                     safe_print(f"  ⚠️ Low Confidence ({confidence:.2f}) but no vector provided. Using SLM fallback.")
                     stimulus["stimulus_vector"] = slm_result.get("gut_vector", {})
                else:
                    safe_print(f"  ✓ Reflection: LLM provided refined stimulus vector (Confidence: {confidence:.2f})")
                
                safe_print(f"  ✓ Stimulus extracted: '{stimulus.get('salience_anchor', 'N/A')}'")
                safe_print(f"  ✓ RIM Impact: {stimulus.get('rim_impact', 0.5):.2f}")
                
                # Partial write: Buffer user fragment
                self.current_turn_user_fragment = {
                    "speaker": "user",
                    "raw_text": user_input,
                    "salience_anchor": {
                        "phrase": stimulus.get("salience_anchor", "unknown"),
                        "Resonance_impact": stimulus.get("rim_impact", 0.5)
                    },
                    "semantic_frames": stimulus.get("tags", []),
                    "affective_inference": {
                        "intent": stimulus.get("intent", "unknown"),
                        "emotion_signal": stimulus.get("emotional_signal", "neutral"),
                        "confidence": confidence,
                        "slm_gut_vector": slm_result.get("gut_vector", {})
                    }
                }
                safe_print(f"  💾 Partial Write: Buffered turn_user fragment.")

        stimulus_chunks = self.cim.normalize_stimulus(stimulus)
        safe_print(f"  ✓ Normalized {len(stimulus_chunks)} stimulus chunk(s).")


        # ============================================================
        # STEP 2: THE GAP - Bio Processing (Function Execution)
        # ============================================================
        
        if self.enable_physio:
            bio_state = self._execute_the_gap(stimulus, query_text=user_input)
            
            # [NEW] NexusMind Strategic Guidance (DeepThink) in The Gap
            if self.nexus_mode:
                safe_print(f"  - [NexusMind] Executing Strategic Decision Matrix...")
                try:
                    strategy = gks_interface.get_strategic_guidance({
                        "stress": bio_state.get('matrix_state', {}).get('stress', 0)/1000.0,
                        "confidence": stimulus.get('confidence_score', 1.0)
                    })
                    # Add strategic guidance to bio_state for LLM consumption
                    bio_state['strategic_guidance'] = strategy
                    safe_print(f"    ✓ Strategic guidance injected.")
                except Exception as e:
                    safe_print(f"    ⚠️ Strategy generation failed: {e}")
                    
        else:
            # Fallback: minimal state
            safe_print("\n⚡ STEP 2: The Gap - Skipped (Physio disabled)")
            bio_state = {
                "biological_state": {"hormones": {}, "autonomic": {}},
                "psychological_state": {},
                "emotion_label": "neutral",
                "embodied_sensation": "Baseline state",
                "retrieved_memories": [],
                "instruction": "Generate a response based on baseline state."
            }

        # [NEW] Persist Step 2 result (Markdown)
        step2_md = f"# [STEP 2: GAP PROCESSING]\n\n## 🧬 BIOLOGICAL STATE\n{yaml.dump(bio_state.get('biological_state', {}), allow_unicode=True)}\n\n## 🧠 PSYCHOLOGICAL STATE\n{yaml.dump(bio_state.get('psychological_state', {}), allow_unicode=True)}\n\n## 🌈 QUALIA\n{bio_state.get('embodied_sensation', 'N/A')}\n\n## 📑 RETRIEVED MEMORIES\n"
        for m in bio_state.get('retrieved_memories', []):
            step2_md += f"- {m.get('content')} (Emotion: {m.get('emotion')})\n"
            
        self.cim.save_markdown_context("step2_processing", step2_md)


        # ============================================================
        # STEP 3: CONTINUATION - Embodied Response Generation
        # ============================================================
        safe_print("\n💭 STEP 3: Continuation - Embodied Reasoning")
        safe_print("  - Sending bio state back to LLM...")
        
        # Continue LLM session with bio state
        final_response = self.llm.continue_with_result(
            function_result=bio_state,
            function_name="sync_biocognitive_state"
        )
        
        # Extract final text
        final_text = final_response.text
        safe_print(f"  ✓ Generated response ({len(final_text)} chars)")
        
        # Extract memory proposal (if LLM called it)
        memory_proposal = {}
        if final_response.tool_calls:
            for tool_call in final_response.tool_calls:
                if tool_call.name == "propose_episodic_memory":
                    memory_proposal = tool_call.args
                    safe_print(f"  ✓ Captured episodic memory proposal")
                    break
        else:
            safe_print("  ⚠️ No memory proposal generated")

        # [NEW] Persist Step 3 result (Markdown)
        step3_md = f"# [STEP 3: REASONING]\n\n## 🤖 FINAL RESPONSE\n{final_text}\n\n## 🧠 MEMORY PROPOSAL\n{yaml.dump(memory_proposal, allow_unicode=True)}"
        self.cim.save_markdown_context("step3_reasoning", step3_md)


        # ============================================================
        # STEP 4: PERSISTENCE - Archive to MSP
        # ============================================================
        safe_print("\n💾 STEP 4: Archiving turn to MSP")
        
        # Final RI Calculation (Resonance Edition logic)
        # Formula: (Bio_Impact * 0.6) + (AI_Confidence * 0.4)
        bio_impact = bio_state.get("Resonance_index", 0.5) 
        ai_confidence = stimulus.get("confidence_score", 0.5)
        final_ri = (bio_impact * 0.6) + (ai_confidence * 0.4)
        safe_print(f"  ✓ Calculated Final RI: {final_ri:.2f} (Bio: {bio_impact:.2f} ‖ AI: {ai_confidence:.2f})")

        # [NEW] Generate Sequential Turn IDs via IdentityManager
        user_turn_num = (self.turn_count * 2) - 1
        llm_turn_num = (self.turn_count * 2)
        user_turn_id = IdentityManager.generate_turn_id(self.session_id, user_turn_num)
        llm_turn_id = IdentityManager.generate_turn_id(self.session_id, llm_turn_num)

        # Prepare fragments with IDs
        user_frag = getattr(self, 'current_turn_user_fragment', None) or {
             "speaker": "user",
             "raw_text": user_input,
             "salience_anchor": {"phrase": "unknown", "Resonance_impact": 0.5},
             "semantic_frames": []
        }
        user_frag["turn_id"] = user_turn_id

        llm_frag = {
            "turn_id": llm_turn_id,
            "speaker": "llm",
            "raw_text": final_text,
            "salience_anchor": {
                "phrase": memory_proposal.get("llm_fragment_proposal", {}).get("turn_llm", {}).get("salience_anchor", {}).get("phrase", "N/A"),
                "Resonance_impact": stimulus.get("rim_impact", 0.5)
            },
            "epistemic_mode": memory_proposal.get("llm_fragment_proposal", {}).get("turn_llm", {}).get("epistemic_mode", "reflect"),
            "confidence": ai_confidence
        }

        # Build episode data
        episode_data = {
            "context_id": context_id,
            "turn_index": self.turn_count,
            "timestamp": datetime.now().isoformat(),
            "episode_type": memory_proposal.get("context_proposal", {}).get("episode_type", "interaction"),
            "episode_tag": memory_proposal.get("context_proposal", {}).get("episode_tag", "unlabeled"),
            "intent": stimulus.get("intent", "unknown"),
            "confidence_score": ai_confidence,
            "turn_id": user_turn_id,  # Root turn_id usually matches initial user turn? Or episode ID? Schema requires it.
            "turn_1": user_frag,
            "turn_llm": llm_frag,
            "state_snapshot": {
                "physio_state": bio_state.get("biological_state", {}),
                "eva_matrix_state": bio_state.get("psychological_state", {}),
                "emotion_label": bio_state.get("emotion_label", "neutral"),
                "qualia": self.msp.get_active_state("qualia_state"), # Capture phenomenology
                "Resonance_index": final_ri  # The authoritative combined score
            },
            "session_id": self.session_id,
            "crosslinks": memory_proposal.get("llm_fragment_proposal", {}).get("crosslinks", {})
        }
        
        # FINAL SANITIZATION: Remove Protobuf/SDK objects before persistence
        from operation_system.llm_bridge.llm_bridge import LLMBridge
        episode_data = LLMBridge.deep_clean(episode_data)
        
        # Write to MSP
        self.msp.write_episode(episode_data, persist=self.recording_active)
        self.msp.log_state_history() # Finalize state history for this turn
        
        # [NEW] Add to Vector DB (Cognitive Learning Loop)
        # We index the raw user input with the REFINED metadata from Step 1
        if self.recording_active and hasattr(self, 'vector_db'):
            safe_print("  - [Learning] Indexing interaction in Vector DB with refined metadata...")
            self.vector_db.add_memory(
                text=user_input,
                metadata={
                    "intent": stimulus.get("intent", "unknown"),
                    "emotional_signal": stimulus.get("emotional_signal", "neutral"),
                    "tags": stimulus.get("tags", []),
                    "salience_anchor": stimulus.get("salience_anchor", "None"),
                    "resonance_index": final_ri,
                    "confidence": ai_confidence,
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat()
                },
                memory_id=context_id
            )

        safe_print(f"  ✓ Episode archived (ID: {context_id[:8]}...)")
        
        # Increment turn counter (2 per interaction: user + llm)
        self.turn_count += 2
        
        # Update CIM turn state and persist turn_index
        self.cim.update_turn_state({
            "user_input": user_input,
            "final_response": final_text,
            "emotion_label": bio_state.get("emotion_label", "neutral"),
            "salience_anchor": stimulus.get("salience_anchor", "unknown"),
            "turn_index": self.turn_count
        })
        
        # Persist turn count for session continuity
        self.msp.save_turn_context({
            "turn_index": self.turn_count,
            "context_id": context_id,
            "session_id": self.session_id
        })
        
        # Resonance Report
        self._print_resonance_report()

        return {
            "final_response": final_text,
            "emotion_label": bio_state.get("emotion_label", "neutral"),
            "resonance_hash": self.bus.generate_state_hash(),
            "confidence_score": ai_confidence,
            "salience_anchor": stimulus.get("salience_anchor", "None"),
            "resonance_index": final_ri,
            "state_snapshot": episode_data.get("state_snapshot", {})
        }

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
            comp = comp_map.get(clean_channel, "Unknown")
            
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
    parser = argparse.ArgumentParser(description="EVA 9.1.0 Orchestrator")
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
