"""
EVA CNS - Master Flow Engine (v1.0.0)
Specialized Execution Slot for core orchestration logic.
"""

import yaml
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from operation_system.identity_manager import IdentityManager
from capabilities.services.slm_bridge.slm_bridge import slm
from operation_system.llm_bridge.llm_bridge import LLMBridge
from operation_system.llm_bridge.llm_bridge import (
    SYNC_BIOCOGNITIVE_STATE_TOOL,
    PROPOSE_EPISODIC_MEMORY_TOOL
)

def safe_print(msg: str):
    print(msg, flush=True)

class MasterFlowEngine:
    """
    Directs the multi-phase cognitive cycle for the Orchestrator CNS.
    Separates execution logic from system management.
    """

    def __init__(self, orchestrator: Any):
        self.orch = orchestrator

    def run_turn(self, user_input: str) -> Dict[str, Any]:
        """
        Executes a complete cognitive turn: Perception -> Gap -> Reasoning -> Persistence.
        """
        self.orch.turn_count += 1
        self.orch.bus_log = [] 
        
        # Start trajectory capture
        self.orch.trajectory.start_turn(self.orch.session_id, self.orch.turn_count)
        
        safe_print(f"\n{'='*60}")
        safe_print(f"🎯 Turn {self.orch.turn_count} (CNS Master Flow)")
        safe_print(f"{'='*60}")

        # Trigger CIM to start a new turn context
        self.orch.cim.start_new_turn_context()
        context_id = self.orch.cim.current_context_id
        
        # --- Phase 1: Perception ---
        stimulus, slm_result, current_speaker_profile, engram_hit, phase1_text = self._phase_1_perception(user_input)
        
        # --- Step 2: The Gap (Bio Processing) ---
        bio_state = self._step_2_the_gap(stimulus, user_input)
        
        # --- Phase 2: Reasoning & Continuation ---
        final_text, memory_proposal = self._phase_2_reasoning(bio_state, phase1_text)
        
        # --- Phase 3: Persistence & Learning ---
        result = self._phase_3_persistence(
            user_input, 
            final_text, 
            stimulus, 
            slm_result, 
            bio_state, 
            memory_proposal, 
            context_id
        )
        
        return result

    def _phase_1_perception(self, user_input: str):
        safe_print("🧠 PHASE 1: Perception")
        
        # Engram Reflex
        engram_hit = self.orch.engram.lookup(user_input)
        if engram_hit:
            safe_print(f"  ⚡ [Engram] Match found. Passing to LLM for verification.")

        # User Identification
        current_speaker_profile = None
        try:
            speaker_info = self.orch.msp.user_registry.identify_speaker(user_input)
            user_id = speaker_info.get("user_id", "unknown")
            if user_id != "unknown":
                current_speaker_profile = self.orch.msp.user_registry.get_user_profile(user_id)
                self.orch.msp.user_registry.increment_interaction(user_id)
            safe_print(f"  👤 Speaker: {speaker_info.get('username')} ({user_id})")
        except Exception as e:
            safe_print(f"  ⚠️ Identification Failed: {e}")

        # SLM Intent & Fast Recall
        try:
            slm_result = slm.extract_intent(user_input)
            # [SIMPLIFIED] Direct SLM -> RIM (No L2/L3)
            # Default to basic intensity if available
            slm_result["r_impact_score"] = slm_result.get("intensity", 0.5)
            fast_mems = self.orch.vector_db.query_memory(user_input, n_results=3)
        except Exception as e:
            safe_print(f"  ⚠️ Gateway Error: {e}")
            slm_result = {"intent": "unknown", "gut_vector": {}}
            fast_mems = []

        # Build Context & Prompt
        live_physio = self.orch.physio.get_state() if self.orch.enable_physio else None
        phase1_context = self.orch.cim.inject_phase_1(
            user_input, 
            live_physio=live_physio,
            slm_data=slm_result,
            long_term_memory=fast_mems,
            user_profile=current_speaker_profile,
            engram_hit=engram_hit
        )
        phase1_prompt = self.orch.cim.build_phase_1_prompt(phase1_context)
        self.orch.cim.save_markdown_context("step1_perception", phase1_prompt)

        # Call LLM
        llm_response = self.orch.llm.generate(
            phase1_prompt,
            tools=[SYNC_BIOCOGNITIVE_STATE_TOOL, PROPOSE_EPISODIC_MEMORY_TOOL]
        )

        # Extract Stimulus
        stimulus = self._extract_stimulus(llm_response, slm_result, user_input)
        # Preserve Phase 1 text — this is EVA's authentic pre-tool response
        phase1_text = llm_response.text.strip()

        return stimulus, slm_result, current_speaker_profile, engram_hit, phase1_text

    def _extract_stimulus(self, llm_response, slm_result, user_input):
        if not llm_response.tool_calls:
            return {"valence": 0.5, "arousal": 0.3, "intensity": 0.3, "tags": ["greeting"], "salience_anchor": "N/A"}
        
        tool_call = llm_response.tool_calls[0]
        if tool_call.name != "sync_biocognitive_state":
            return {"valence": 0.5, "arousal": 0.3, "intensity": 0.3, "tags": ["unknown"], "salience_anchor": "N/A"}
        
        stimulus = tool_call.args
        confidence = stimulus.get('confidence_score', 0.5)
        
        # Perception Delegation logic
        if not stimulus.get("stimulus_vector") or confidence > 0.9:
            stimulus["stimulus_vector"] = slm_result.get("gut_vector", {})
        
        # Buffer user fragment (Authoritative State)
        self.orch.current_turn_user_fragment = {
            "speaker": "user",
            "raw_text": user_input,
            "salience_anchor": {
                "phrase": stimulus.get("salience_anchor", "unknown"),
                "Resonance_impact": stimulus.get("r_impact_score", 0.5)
            },
            "semantic_frames": stimulus.get("tags", []),
            "affective_inference": {
                "intent": stimulus.get("intent", "unknown"),
                "emotion_signal": stimulus.get("emotional_signal", "neutral"),
                "confidence": confidence
            }
        }
        
        # Log to MSP
        if self.orch.msp:
            stimulus_data = {
                "turn_id": IdentityManager.generate_turn_id(self.orch.session_id, (self.orch.turn_count * 2) - 1),
                "eva_stimuli": stimulus.get("stimulus_vector", {}),
                "timestamp": datetime.now().isoformat()
            }
            self.orch.msp.log_stimulus_output(stimulus_data)
        
        return stimulus

    def _step_2_the_gap(self, stimulus, user_input):
        safe_print("\n⚡ STEP 2: The Gap")
        if not self.orch.enable_physio:
            return {
                "biological_state": {"hormones": {}, "autonomic": {}},
                "psychological_state": {},
                "emotion_label": "neutral",
                "embodied_sensation": "Baseline state",
                "retrieved_memories": [],
                "instruction": "Baseline response."
            }

        # Original execute_the_gap logic: Signal Driven
        # Strip protobuf objects (Gemini tool call args) before publishing to bus
        clean_stimulus = LLMBridge.deep_clean(stimulus)
        signal_payload = {
            "event_type": "STIMULUS_PERCEIVED",
            "stimulus": clean_stimulus,
            "query_text": user_input,
            "timestamp": datetime.now().isoformat()
        }
        self.orch.bus.publish(IdentityManager.BUS_PHYSICAL, signal_payload)
        self.orch.bus.publish(IdentityManager.BUS_KNOWLEDGE, signal_payload)
        
        physio_snap = self.orch.physio.get_snapshot()
        matrix_snap = self.orch.matrix.axes_9d
        emotion_label = self.orch.matrix.emotion_label
        qualia_snap = self.orch.qualia.last_qualia
        
        unique_memories = self.orch.agentic_rag.state.get("last_retrieval", [])
        
        # RMS Coloring
        try:
            rms_out = self.orch.rms.process(
                eva_matrix=matrix_snap,
                rim_output={"impact_level": "medium"},
                reflex_state=physio_snap.get("autonomic", {}),
                ri_total=0.5
            )
        except: pass

        bio_state = {
            "biological_state": {
                "hormones": {k: round(v, 4) for k, v in physio_snap.get("blood", {}).items()},
                "vitals": physio_snap.get("vitals", {})
            },
            "psychological_state": matrix_snap,
            "emotion_label": emotion_label,
            "embodied_sensation": f"Intensity: {qualia_snap.intensity:.2f}, Tone: {emotion_label}" if qualia_snap else f"Tone: {emotion_label}",
            "retrieved_memories": [
                {"content": m.content[:150] + "...", "emotion": getattr(m, "emotion_label", "N/A")}
                for m in list(unique_memories)[:3]
            ]
        }
        
        # Strategic Guidance (NexusMind)
        # [SIMPLIFIED] No NexusMind Strategy
        # Nexus logic removed per user revert
        pass

        self.orch.cim.save_markdown_context("step2_processing", yaml.dump(bio_state))
        return bio_state

    def _phase_2_reasoning(self, bio_state, phase1_text: str = ""):
        safe_print("\n💭 PHASE 2: Reasoning")
        # Send minimal result so Gemini continues as EVA, not as a data reporter
        minimal_result = {
            "status": "synchronized",
            "emotion": bio_state.get("emotion_label", "neutral"),
            "sensation": bio_state.get("embodied_sensation", "baseline")
        }
        final_response = self.orch.llm.continue_with_result(
            function_result=minimal_result,
            function_name="sync_biocognitive_state"
        )
        
        phase2_text = final_response.text.strip()
        # Phase 1 already contains EVA's authentic response (before tool call).
        # Use Phase 2 text only if it is a real response, not empty/meta/tool explanation.
        meta_markers = [
            # tool/function meta patterns
            "i have called", "the function", "sync_biocognitive_state",
            "the output shows", "[empty response]", "error extracting",
            "function result", "function call", "function response",
            # SLM/analysis reporting patterns (Gemini describing data instead of responding as EVA)
            "the user said", "the user input", "the user's message",
            "the slm", "slm's interpretation", "slm interpretation",
            "translates to", "is gibberish", "intent detection",
            "user message is", "the input is", "this is gibberish",
            # Generic analysis/report patterns
            "based on the", "the system", "i have processed",
        ]
        is_empty = (not phase2_text
                    or phase2_text.startswith("[Empty Response]")
                    or phase2_text.startswith("[System Error")
                    or phase2_text.startswith("[Error"))
        is_meta  = any(m in phase2_text.lower() for m in meta_markers)
        use_phase2 = not is_empty and not is_meta

        # Also check if phase1_text is usable (non-empty, non-meta)
        is_phase1_meta = any(m in phase1_text.lower() for m in meta_markers) if phase1_text else False
        is_phase1_usable = bool(phase1_text) and not is_phase1_meta

        if use_phase2:
            final_text = phase2_text
        elif is_phase1_usable:
            final_text = phase1_text
        else:
            # Both phases failed — send correction to guide EVA back to natural response
            safe_print("[Phase2] Both phases produced meta/empty text — attempting recovery...")
            try:
                recovery = self.orch.llm.send_correction(
                    "You are EVA. Respond naturally and conversationally to the user. "
                    "Do not analyze, report, or describe data — just respond as yourself."
                )
                rec_text = recovery.text.strip() if recovery.text else ""
                final_text = rec_text if (rec_text and not rec_text.startswith("[")) else (phase1_text or phase2_text or "...")
            except Exception as rec_err:
                safe_print(f"[Phase2] Recovery failed: {rec_err}")
                final_text = phase1_text or phase2_text or "..."
        memory_proposal = {}
        if final_response.tool_calls:
            for tool_call in final_response.tool_calls:
                if tool_call.name == "propose_episodic_memory":
                    memory_proposal = tool_call.args
                    break
        
        self.orch.cim.save_markdown_context("step3_reasoning", final_text)
        return final_text, memory_proposal

    def _phase_3_persistence(self, user_input, final_text, stimulus, slm_result, bio_state, memory_proposal, context_id):
        safe_print("\n💾 PHASE 3: Persistence")
        
        # Final Resonance
        # Final Resonance (Tool Evaluation)
        # Using simplified RIM logic (placeholder delta for now)
        try:
             res_result = self.orch.resonance.evaluate({}, {}, 0.0, 1.0) # Dummy inputs for stability
             final_ri = res_result["rim_value"]
        except:
             final_ri = 0.5
        
        # Generate Turn IDs
        user_turn_id = IdentityManager.generate_turn_id(self.orch.session_id, (self.orch.turn_count * 2) - 1)
        llm_turn_id = IdentityManager.generate_turn_id(self.orch.session_id, (self.orch.turn_count * 2))

        user_frag = getattr(self.orch, 'current_turn_user_fragment', None) or {"raw_text": user_input}
        user_frag["turn_id"] = user_turn_id
        
        ai_confidence = slm_result.get("confidence", 0.85)
        llm_frag = {
            "turn_id": llm_turn_id,
            "speaker": "llm",
            "raw_text": final_text,
            "confidence": ai_confidence
        }

        # Build Episode
        episode_data = {
            "context_id": context_id,
            "turn_index": self.orch.turn_count,
            "timestamp": datetime.now().isoformat(),
            "turn_1": user_frag,
            "turn_llm": llm_frag,
            "state_snapshot": {
                "physio_state": bio_state.get("biological_state", {}),
                "eva_matrix_state": bio_state.get("psychological_state", {}),
                "emotion_label": bio_state.get("emotion_label", "neutral"),
                "Resonance_index": final_ri 
            },
            "session_id": self.orch.session_id
        }
        
        # Write to MSP & Vector DB
        episode_data = LLMBridge.deep_clean(episode_data)
        self.orch.msp.write_episode(episode_data)
        
        if self.orch.recording_active and hasattr(self.orch, 'vector_db'):
            self.orch.vector_db.add_memory(text=user_input, metadata={"intent": stimulus.get("intent")}, memory_id=context_id)
            if ai_confidence > self.orch.engram.min_conf:
                self.orch.engram.memorize(text=user_input, context_data={"intent": stimulus.get("intent")}, confidence=ai_confidence)

        # Update State
        self.orch.turn_count += 2
        self.orch.cim.update_turn_state({"turn_index": self.orch.turn_count})
        self.orch.msp.save_turn_context({"turn_index": self.orch.turn_count, "context_id": context_id})
        
        return {
            "final_response": final_text,
            "emotion_label": bio_state.get("emotion_label", "neutral"),
            "resonance_hash": self.orch.bus.generate_state_hash(),
            "resonance_index": final_ri
        }

