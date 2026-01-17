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

from capabilities.tools.logger import safe_print

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Resonance Bus Interface
from operation_system.resonance_bus import bus

# Biological & Psychological Systems
from physio_core.physio_core import PhysioCore
from eva_matrix.eva_matrix import EVAMatrixSystem
from artifact_qualia.artifact_qualia import ArtifactQualiaSystem
from orchestrator.cim.prompt_rule.prompt_rule_node import PromptRuleNode

# Cognitive & Memory
from orchestrator.cim.cim import ContextInjectionModule
from services.agentic_rag.agentic_rag_engine import AgenticRAG
from memory_n_soul_passport.memory_n_soul_passport_engine import MSP
from operation_system.llm_bridge.llm_bridge import LLMBridge, SYNC_BIOCOGNITIVE_STATE_TOOL, PROPOSE_EPISODIC_MEMORY_TOOL
from operation_system.llm_bridge.ollama_bridge import OllamaBridge

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

        safe_print(f"  - Mode: {self.llm_backend.upper()}, Physio: {self.enable_physio}")

        # --------------------------------------------------
        # 1. Initialize Resonance Bus
        # --------------------------------------------------
        self.bus = bus
        self.bus.initialize_session(self._generate_session_id())
        self.bus_log = []
        
        # Monitor all core channels
        for channel in ["bus:physical", "bus:psychological", "bus:phenomenological", "bus:knowledge"]:
            self.bus.subscribe(channel, lambda p, c=channel: self.bus_log.append((c, p)))

        # --------------------------------------------------
        # 2. Initialize Memory & RAG
        # --------------------------------------------------
        safe_print("  - Initializing MSP Engine...")
        self.msp = MSP()

        # Load last session if possible
        last_context = self.msp.load_turn_context()
        self.turn_count = last_context.get("turn_index", 0) + 1
        self.current_context_id = last_context.get("context_id", self._generate_context_id())

        safe_print("  - Initializing AgenticRAG...")
        self.agentic_rag = AgenticRAG(msp_client=self.msp)

        # --------------------------------------------------
        # 3. Initialize Biological & Psychological Mind (The Gap)
        # --------------------------------------------------
        if self.enable_physio:
            safe_print("  - Initializing PhysioCore (v9.1.0-C1)...")
            base_physio = Path(__file__).parent.parent / "eva" / "physio_core" / "configs"
            self.physio = PhysioCore(
                endocrine_cfg_path=str(base_physio / "hormone_spec_ml.yaml"),
                endocrine_reg_cfg_path=str(base_physio / "endocrine_regulation.yaml"),
                blood_cfg_path=str(base_physio / "blood_physiology.yaml"),
                receptor_cfg_path=str(base_physio / "receptor_configs.yaml"),
                reflex_cfg_path=str(base_physio / "receptor_configs.yaml"), # Reusing receptor for reflex if no separate spec
                autonomic_cfg_path=str(base_physio / "autonomic_response.yaml"),
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
        # 4. Initialize Cognitive Layer (CIM)
        # --------------------------------------------------
        print("  - Initializing CIM (Context Injection Module)...")
        root_path = Path(__file__).parent.parent
        self.cim = ContextInjectionModule(
            physio_controller=self.physio,
            msp_client=self.msp,
            hept_stream_rag=self.agentic_rag,
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
        self.session_id = self.bus.session_id
        if hasattr(self.bus, 'current_session_id') and self.bus.current_session_id:
             self.session_id = self.bus.current_session_id
             
        self.turn_count = 0
        self.recording_active = False # Default: OFF (Requiring explicit start)
        self.pending_session_end = False # For confirmation flow
        self.last_interaction = datetime.now()
        self.session_start_time = datetime.now()

        print(f"✅ EVA 9.1.0 ready! (Session: {self.session_id})\n")

    def _execute_the_gap(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute The Gap: Biological processing without LLM.
        
        Args:
            stimulus: Extracted from sync_biocognitive_state() call
            
        Returns:
            Rich bio state to feed back to LLM for embodied reasoning
        """
        safe_print("\n⚡ STEP 2: The Gap - Bio-Digital Sync")
        
        # 1. Physio Core Processing
        safe_print("  - [Process A] Physio Core: Chunking hormonal response...")
        physio_result = self.physio.step(
            eva_stimuli=[stimulus],
            zeitgebers={"active": 0.5},
            dt=60.0
        )
        safe_print(f"  - Chunk 1/1: {stimulus.get('salience_anchor', 'N/A')}")
        
        # 2. Matrix Update
        safe_print("  - [Process B] EVA Matrix: Recalculating psychological state...")
        matrix_result = self.matrix.process_signals(physio_result.get("blood", {}))
        
        # 3. Qualia Generation
        qualia_snap = self.qualia.process_experience()
        qualitative_exp = f"Intensity: {qualia_snap.get('intensity', 0.8):.2f}, Tone: {qualia_snap.get('tone', 'neutral')}"
        safe_print(f"  - Qualia Color: {qualia_snap.get('tone', 'neutral')} | Experience: {qualitative_exp}")
        
        # 4. Two-Stage RAG
        safe_print("  - [Process C] Two-Stage RAG: Quick Recall (parallel) + Deep Recall...")
        memory_matches = self.agentic_rag.two_stage_recall({
            "semantic_tags": stimulus.get("tags", []),
            "emotion_query": matrix_result.get("emotion_label", "neutral"),
            "ans_state": physio_result.get("autonomic", {}),
            "blood_levels": physio_result.get("blood", {})
        })
        
        quick_count = len(memory_matches.get("quick", []))
        deep_count = len(memory_matches.get("deep", []))
        safe_print(f"  - Quick Recall: {quick_count} matches")
        safe_print(f"  - Deep Recall: {deep_count} matches")
        
        # Merge memories
        all_memories = list(memory_matches.get("quick", [])) + list(memory_matches.get("deep", []))
        unique_memories = {m.episode_id: m for m in all_memories}.values()
        safe_print(f"  - Merged: {len(unique_memories)} unique episodes")
        
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
                safe_print(f"\nzzz [STOP] SESSION ENDED: {self.session_id}")
                return {"final_response": "Session Closed. Recording Stopped.", "emotion_label": "Calm", "resonance_hash": "END"}
            else:
                self.pending_session_end = False
                safe_print(f"\n🔄 [RESUME] Stop cancelled. Recording continues.")
                return {"final_response": "Session Continuation Confirmed.", "emotion_label": "Alert", "resonance_hash": "RESUME"}

        # Command Keywords
        start_keywords = ["/start", "เริ่ม", "อัด", "rec", "start session"]
        stop_keywords = ["/stop", "/end", "พอ", "หยุด", "จบ", "ปิดเซสชั่น", "quit session"]

        if any(word in cmd for word in start_keywords):
            self.recording_active = True
            self.session_id = self.bus._generate_session_id() # New Session ID
            self.bus.current_session_id = self.session_id
            self.turn_count = 0
            self.session_start_time = datetime.now()
            safe_print(f"\n🔴 [REC] SESSION STARTED: {self.session_id}")
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
        time_diff = (datetime.now() - self.last_interaction).total_seconds()
        if self.recording_active and time_diff > 1800: # 30 mins
             self.recording_active = False
             safe_print(f"\n⚠️ [TIMEOUT] Session auto-closed due to inactivity.")
        self.last_interaction = datetime.now()

        # Status Indicator
        status_icon = "🔴" if self.recording_active else "⚪"
        wait_icon = "⏳" if self.pending_session_end else ""
        safe_print(f"Status: {status_icon}{wait_icon} Rec: {'ON' if self.recording_active else 'OFF'}")

        self.turn_count += 1
        self.bus_log = [] # Clear log for fresh monitoring
        print(f"\n{'='*60}")
        print(f"🎯 Turn {self.turn_count} (Resonance Exchange)")
        print(f"{'='*60}")

        context_id = self._generate_context_id()
        
        # --- PHASE 1: Perception ---
        safe_print("🧠 STEP 1: Phase 1 - Perception")
        
        # Capture live physio snapshot (Background state)
        live_physio = None
        if self.enable_physio:
            live_physio = self.physio.get_state()
            safe_print("  - Captured live physio snapshot.")

        phase1_context = self.cim.inject_phase_1(user_input, live_physio=live_physio)
        safe_print("[DEBUG] Phase 1 context injected, building prompt...")
        phase1_prompt = self.cim.build_phase_1_prompt(phase1_context)
        safe_print(f"[DEBUG] Prompt built ({len(phase1_prompt)} chars), saving context...")
        self.cim.save_phase_context("phase1", phase1_context) # Granular Persistence

        safe_print(f"  - Calling {self.llm_backend.upper()} to extract stimulus...")
        safe_print("[DEBUG] About to call llm.generate()...")
        llm_response = self.llm.generate(
            phase1_prompt,
            tools=[SYNC_BIOCOGNITIVE_STATE_TOOL],
            temperature=0.7
        )
        safe_print("[DEBUG] llm.generate() returned!")

        # Handle tool call with Cognitive Firewall
        if not llm_response.tool_calls:
            safe_print("  ⚠️ Warning: LLM skipped Phase 1 extraction.")
            stimulus_chunks = self.cim.normalize_stimulus({"valence": 0.5, "arousal": 0.3, "intensity": 0.3})
        else:
            tool_call = llm_response.tool_calls[0]
            safe_print(f"  🛡️ Routing extraction and resonance analysis through CIM Firewall...")
            
            # 1. LOG: Extract AI's raw perception (What did the AI see?)
            raw_ai_perception = tool_call.args
            salience_anchor_phrase = raw_ai_perception.get("salience_anchor", "unknown")
            safe_print(f"  ✓ AI Identified Salience Anchor: '{salience_anchor_phrase}'")

            # 2. RIM Calculation (AI Perception & System Authority)
            # Use explicit rim_impact if provided by LLM, otherwise derive from arousal
            rim_score = raw_ai_perception.get("rim_impact")
            if rim_score is None:
                rim_score = raw_ai_perception.get("stimulus_vector", {}).get("arousal", 0.5)
            
            safe_print(f"  ✓ Resonance Impact (RIM) identified: {rim_score:.2f}")

            # 3. PARTIAL WRITE: Hydrate user_turn fragment immediately
            self.current_turn_user_fragment = {
                "speaker": "user",
                "raw_text": user_input, # Original input
                "salience_anchor": { # AI's analysis
                    "phrase": salience_anchor_phrase,
                    "Resonance_impact": rim_score
                },
                "semantic_frames": raw_ai_perception.get("tags", [])
            }
            safe_print(f"  💾 Partial Write: Buffered turn_user fragment.")

            stimulus_chunks = self.cim.normalize_stimulus(raw_ai_perception)
            safe_print(f"  ✓ Extracted {len(stimulus_chunks)} sensory chunks for Physio Core.")

        # --- THE GAP: Bio-Digital Synchronization ---
        safe_print("\n⚡ STEP 2: The Gap - Bio-Digital Sync & Chunking")
        
        ans_state = {"sympathetic": 0.4, "parasympathetic": 0.6}
        blood_levels = {"cortisol": 0.3, "oxytocin": 0.5}
        qualitative_experience = "Feeling stable."

        if self.enable_physio:
            # 1. Physio Chunking (Simulating Human Perception Time)
            safe_print("  - [Process A] Physio Core: Chunking hormonal response...")
            physio_result = self.physio.step(
                eva_stimuli=stimulus_chunks,
                zeitgebers={"active": 0.5},
                dt=60.0
            )
            ans_state = physio_result.get("autonomic", {})
            blood_levels = physio_result.get("blood", {})

            # 2. Matrix processing (Psychological shift based on new hormones)
            safe_print("  - [Process B] EVA Matrix: Recalculating psychological state...")
            matrix_result = self.matrix.process_signals(blood_levels)
            
            # 3. Qualia generation (Phenomenological texture)
            qualia_snap = self.qualia.process_experience()
            qualitative_experience = self._format_qualia_for_llm(qualia_snap)
            memory_color = qualia_snap.get("tone", "neutral")
            safe_print(f"  - Qualia Color: {memory_color} | Experience: {qualitative_experience}")

        # 4. TWO-STAGE RETRIEVAL (Optimized for Parallel Processing)
        safe_print("  - [Process C] Two-Stage RAG: Quick Recall (parallel) + Deep Recall...")
        
        # Stage 1: Quick Recall (runs parallel with Physio above - simulated here as sequential for now)
        quick_query_ctx = {
            "tags": stimulus_chunks[0].get("tags", []),
            "context_id": context_id
        }
        quick_matches = self.agentic_rag.retrieve_fast(quick_query_ctx)
        safe_print(f"  - Quick Recall: {len(quick_matches)} matches (Narrative, Intuition, Reflection)")
        
        # Stage 2: Deep Recall (requires complete bio state)
        deep_query_ctx = {
            "tags": stimulus_chunks[0].get("tags", []),
            "ans_state": ans_state,
            "blood_levels": blood_levels,
            "qualia_texture": qualia_snap if self.enable_physio else {},
            "context_id": context_id
        }
        deep_matches = self.agentic_rag.retrieve_deep(deep_query_ctx)
        safe_print(f"  - Deep Recall: {len(deep_matches)} matches (Emotion, Salience, Sensory, Temporal)")
        
        # Merge and deduplicate
        memory_matches = self.agentic_rag.merge_results(quick_matches, deep_matches)
        safe_print(f"  - Merged: {len(memory_matches)} unique episodes")
        
        # 4b. RMS Color Match (Resonance-based Recall)
        # TODO: self.msp.query_by_color(memory_color)
        safe_print(f"  - RMS: Scanning for '{memory_color}' resonance chains...")
        
        # Serialize matches
        memory_list = []
        for m in (memory_matches.values() if isinstance(memory_matches, dict) else memory_matches):
            if isinstance(m, list): memory_list.extend([vars(x) if hasattr(x, '__dict__') else x for x in m])
            else: memory_list.append(vars(m) if hasattr(m, '__dict__') else m)

        # --- Meta-Evaluation ---
        cognitive_load = 0.0 # Will be calculated based on emotional state vs intended action
        
        physio_impact = ans_state.get("sympathetic", 0.5)
        unified_impact = (0.4 * stimulus_chunks[0].get("intensity", 0.5)) + (0.6 * physio_impact)
        meta_intent = "Proceeding with stabilization." if unified_impact > 0.8 else "Normal engagement."

        # --- PHASE 2: Reasoning ---
        safe_print("\n💭 STEP 3: Phase 2 - Reasoning (40/60 Weighting)")
        phase2_context = self.cim.inject_phase_2(
            stimulus_vector=stimulus_chunks[0],
            tags=stimulus_chunks[0].get("tags", []),
            updated_physio=physio_result if self.enable_physio else {},
            memory_matches=memory_list,
            cognitive_load=cognitive_load # Pass cognitive load
        )
        phase2_context["embodied_sensation"] = qualitative_experience
        phase2_context["meta_evaluation"] = {"unified_impact": unified_impact, "recommended_intent": meta_intent}

        phase2_result = self.cim.build_phase_2_prompt(phase2_context)
        self.cim.save_phase_context("phase2", phase2_context) # Granular Persistence
        weighting_directive = f"\n### Transcription Point: 60% Physio (Impact: {unified_impact:.2f}) / 40% Persona\n"
        final_prompt = weighting_directive + phase2_result["function_result_text"]

        safe_print(f"  - Generating Final Response & Memory Proposal...")
        final_llm_response = self.llm.generate(
            final_prompt,
            tools=[PROPOSE_EPISODIC_MEMORY_TOOL],
            temperature=0.7
        )
        final_text = final_llm_response.text
        
        # Extract Memory Proposal if present
        self.last_memory_proposal = {}
        if final_llm_response.tool_calls:
            for tool in final_llm_response.tool_calls:
                if tool.name == "propose_episodic_memory":
                    self.last_memory_proposal = tool.args
                    safe_print(f"  ✓ Captured episodic memory proposal.")

        # --- PHASE 3: Prediction & Summary ---
        safe_print("\n🔮 STEP 4: Phase 3 - Prediction & Summary")
        phase3_context = self.cim.inject_phase_3(final_text, context_id)
        phase3_prompt = self.cim.build_phase_3_prompt(phase3_context)
        self.cim.save_phase_context("phase3", phase3_context) # Granular Persistence
        
        safe_print("  - Analyzing turn for next episode...")
        prediction_response = self.llm.generate(phase3_prompt, temperature=0.3)
        try:
            # Parse JSON from Prediction
            import json
            import re
            
            clean_text = prediction_response.text.strip()
            if not clean_text:
                raise ValueError("Empty response from LLM")
                
            # Try to find JSON block
            json_match = re.search(r'(\{.*\})', clean_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                prediction_data = json.loads(json_str)
                self.cim.update_previous_turn_data(prediction_data)
                safe_print(f"  ✓ Context Summary: {prediction_data.get('context_summary', 'None')[:50]}...")
                safe_print(f"  ✓ Prediction: {prediction_data.get('user_action_prediction', 'None')}")
            else:
                # If no braces found, maybe it's just raw JSON?
                try:
                    prediction_data = json.loads(clean_text)
                    self.cim.update_previous_turn_data(prediction_data)
                    safe_print(f"  ✓ Context Summary: {prediction_data.get('context_summary', 'None')[:50]}...")
                except:
                    safe_print("  ⚠️ Prediction output was not valid JSON.")
        except Exception as e:
            safe_print(f"  ⚠️ Error parsing prediction: {e}")

        # --- Resonance Transfer Report ---
        self._print_resonance_report()

        # --- Persistence ---
        safe_print("\n💾 STEP 5: Archiving turn to MSP (Propelled Hydration)")
        
        # 1. Authoritative Bio-Cognitive Snapshot (The Truth)
        # Calculate Final Resonance Index (RI) = Blend of Input (Bio) + Output (AI)
        # AI Contribution: Confidence * Epistemic Weight
        # (Assert=1.0, Hypothesize=0.8, Reflect=0.7, Explore=0.5, Caution=0.4)
        epistemic_map = {"assert": 1.0, "hypothesize": 0.8, "reflect": 0.7, "explore": 0.5, "caution": 0.4}
        ai_mode = proposal.get("ai_fragment_proposal", {}).get("turn_ai", {}).get("epistemic_mode", "reflect")
        ai_conf = proposal.get("ai_fragment_proposal", {}).get("turn_ai", {}).get("confidence", 0.5)
        
        ai_ri_contribution = ai_conf * epistemic_map.get(ai_mode, 0.7)
        final_ri = (unified_impact * 0.6) + (ai_ri_contribution * 0.4) # 60% Body, 40% Mind
        
        safe_print(f"  ✓ Resonance Index (RI): {final_ri:.2f} (Bio: {unified_impact:.2f}, AI: {ai_ri_contribution:.2f})")

        impact_level = "high" if final_ri > 0.7 else ("medium" if final_ri > 0.4 else "low")
        resonance_snapshot = self.msp.process_resonance(
            eva_matrix=matrix_result if self.enable_physio else {},
            rim_output={"impact_level": impact_level, "impact_trend": "stable", "unified_impact": final_ri},
            reflex_state=physio_result.get("signals", {}) if self.enable_physio else {},
            ri_total=final_ri
        )

        # 2. Hydrate Proposal with System Authority
        # Merge proposal from AI with System Truths
        proposal = self.last_memory_proposal or {}
        
        # Hydrate User Fragment & Recalculate RIM (First Impression vs Deep Resonance)
        user_frag = proposal.get("user_fragment_proposal", {}).get("turn_user", {})
        
        # Recalculate deep RIM for User Anchor based on final state
        # (Assuming arousal was main driver in Phase 1)
        initial_rim = self.current_turn_user_fragment.get("salience_anchor", {}).get("Resonance_impact", 0.5)
        deep_rim = unified_impact # The final biological state is the "deep" resonance
        rim_diff = deep_rim - initial_rim
        
        user_frag.update({
            "speaker": "user",
            "raw_text": user_input,
            "salience_anchor": {
                "phrase": self.current_turn_user_fragment.get("salience_anchor", {}).get("phrase", "unknown"),
                "Resonance_impact": deep_rim,
                "rim_diff": rim_diff
            }
        })
        
        # Hydrate AI Fragment
        ai_frag = proposal.get("ai_fragment_proposal", {}).get("turn_ai", {})
        
        # Calculate AI-side RIM (System Authority) derived from AI's Confidence + System Impact
        # Logic: High confidence + High system arousal = High Resonance
        ai_confidence = ai_frag.get("confidence", 0.5)
        ai_rim_score = (ai_confidence * 0.4) + (unified_impact * 0.6)
        
        ai_frag.update({
            "speaker": "ai",
            "text_excerpt": final_text[:200], # System extracts excerpt
            "salience_anchor": {
                 "phrase": ai_frag.get("salience_anchor", {}).get("phrase", "unknown"),
                 "Resonance_impact": ai_rim_score # System-calculated RIM
            }
        })

        # Final Episode Body (SYSTEM-HYDRATED)
        episode_data = {
            "context_id": context_id,
            "turn_index": self.turn_count,
            "timestamp": datetime.now().isoformat(),
            "episode_type": proposal.get("context_proposal", {}).get("episode_type", "interaction"),
            "episode_tag": proposal.get("context_proposal", {}).get("episode_tag", "unlabeled"),
            "turn_1": user_frag,
            "turn_ai": ai_frag,
            "state_snapshot": resonance_snapshot,
            "session_id": self.session_id,
            "crosslinks": proposal.get("ai_fragment_proposal", {}).get("crosslinks", {})
        }

        # 3. Write to MSP
        self.msp.write_episode(episode_data, persist=self.recording_active)

        # 4. Sync Full Context Persistence (Digital Twin Cache)
        # Gather active snapshots from all systems
        full_turn_state = {
            "physio": resonance_snapshot.get("physio_state", {}),
            "matrix": resonance_snapshot.get("eva_matrix_state", {}),
            "qualia": resonance_snapshot.get("qualia_state", {}),
            "cognitive": {
                "previous_turn_data": {
                    "context_summary": prediction_data.get("context_summary"),
                    "user_action_prediction": prediction_data.get("user_action_prediction"),
                    "action_plan": prediction_data.get("action_plan")
                }
            },
            "user_input": user_input,
            "final_response": final_text,
            "salience_anchor": ai_frag.get("salience_anchor", {}).get("phrase", "unknown"),
            "user_summary": prediction_data.get("context_summary"), # Using context summary as user summary if long
            "self_note": prediction_data.get("self_note", "") # Capture self-note from LLM
        }
        self.cim.update_turn_state(full_turn_state)

        self.turn_count += 1

        return {
            "final_response": final_text,
            "emotion_label": self.matrix.emotion_label if self.enable_physio else "Neutral",
            "resonance_hash": self.bus.generate_state_hash()
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
                "physical": "PhysioController", 
                "psychological": "EVA_Matrix", 
                "phenomenological": "Artifact_Qualia", 
                "knowledge": "PMT"
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

    def _generate_context_id(self): return f"ctx_{datetime.now().strftime('%y%m%d_%H%M%S')}"

    def _generate_session_id(self): return os.urandom(4).hex()


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
