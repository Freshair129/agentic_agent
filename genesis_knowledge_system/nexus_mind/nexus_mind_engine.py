"""
EVA NexusMind Engine v9.3.4
The Strategic Brain of the Organism (ERD Aligned).
Responsible for:
1. Insecurity Checks (Pre-Inference)
2. Decision Matrix Logic (The Gap)
3. Final Synthesis (Post-Inference)
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path

# V9.2.0 Core Imports
from operation_system.identity_manager import IdentityManager
from operation_system.llm_bridge.llm_bridge import LLMBridge
from eva.genesis_knowledge_system.gks_loader import GKSLoader
import logging

try:
    from eva.genesis_knowledge_system.archetypal_projection.apm_engine import ArchetypalProjectionModule
    from eva.genesis_knowledge_system.meta_learning_loop.mll_engine import MetaLearningLoop
    from orchestrator.temporal.temporal_engine import TemporalEngine
except ImportError:
    # Build fallback stubs if files missing during migration
    class ArchetypalProjectionModule:
        def __init__(self, gks): pass
        def project_archetype(self, ctx): return {"archetype_projection": ""}

    class MetaLearningLoop:
        def __init__(self, gks): pass
        def process_learning(self, fb, ctx): return {"status": "inactive"}

    class TemporalEngine:
        def __init__(self, gks): pass
        def process_temporal_sot(self, ctx): return ""
        def get_narrative_pulse(self, score): return ""

class NexusMindEngine:
    """
    EVA NexusMind Engine (v9.3.3)
    Orchestrates GKS knowledge, APM archetypes, and MLL learning (ERD Aligned).
    """
    def __init__(self, mock_mode: bool = False):
        
        # 1. Load Static Knowledge (GKS)
        self.gks_loader = GKSLoader()
        
        # Initialize Expansion Modules with Loader
        self.apm = ArchetypalProjectionModule(self.gks_loader)
        self.mll = MetaLearningLoop(self.gks_loader)
        self.temporal = TemporalEngine(self.gks_loader)
        
        # Load Knowledge Blocks
        if not mock_mode:
            self.gks_loader.load_all()
            
        logging.info("[NexusMind] 🧠 Expansion Modules (APM/MLL) Online")
            
        # 2. Connect to External Brain (Thinking)
        # Using LLMBridge for "Talk-to-Self" capabilities
        self.brain = LLMBridge()
        
        # 3. Decision Matrix State
        self.decision_matrix: List[Dict[str, Any]] = []
        self.current_risk_score = 0.0

    def process_insecurity_check(self, context_data: dict) -> Dict[str, Any]:
        """
        Task 4.0 & 4.1: Master/Safety Block Insecurity Check
        Checks if User Input violates 'Core Insecurities' or 'Safety Protocols'.
        STRICTLY DATA-DRIVEN: No hardcoded heuristics.
        """
        user_input = context_data.get("user_input", "").lower()
        
        triggered = []
        reasons = []
        
        # 1. Check Safety Protocols (Safety Block) - Use key_trigger from block
        safety = self.gks_loader.get_safety_block().get("Safety_Block", {})
        protocols = safety.get("protocols", [])
        for proto in protocols:
            trigger = proto.get("key_trigger", "").lower()
            if trigger and trigger in user_input:
                triggered.append(proto["id"])
                reasons.append(f"Safety Protocol Violation: {proto['name']}")

        # 2. Check Activation Triggers (Master Block)
        # Note: Master Block defines 'High-Level Intuition'. 
        # Integration logic searches for specific Block_ID triggers if applicable.
        # For v9.3.3, we focus on Safety and Protocol-level blocking.
                    
        return {
            "is_insecure": len(triggered) > 0,
            "triggered_insecurities": triggered,
            "insecurity_reasons": reasons
        }

    def formulate_strategic_guidance(self, context_data: dict) -> str:
        """
        Generates high-level strategic guidance based on GKS + APM.
        """
        # 1. Base Strategy from Algorithm Block
        algo_root = self.gks_loader.get_genesis_block("algorithm").get("genesis_block", {})
        algorithms = algo_root.get("algorithms", [])
        
        relevant_algos = []
        user_input_lower = context_data.get("user_input", "").lower()
        
        for algo in algorithms:
            trigger = algo.get("key_trigger", "").lower()
            if trigger and trigger in user_input_lower:
                relevant_algos.append(algo)
            # Tag fallback
            for tag in algo.get("tags", []):
                if tag.lower() in context_data.get("tags", []):
                    relevant_algos.append(algo)
                    break
                
        # 2. Archetypal Projection (APM) - v9.3.1GEM
        apm_result = self.apm.project_archetype(context_data)
        projection_text = apm_result.get("archetype_projection", "")
        
        # 3. Construct Guidance
        guidance = "## 🛡️ NEXUSMIND STRATEGIC GUIDANCE\n"
        
        if relevant_algos:
            guidance += "Apply these GKS Algorithms:\n"
            for algo in relevant_algos[:2]:
                guidance += f"- **{algo['name']}**: {algo['core_instruction']}\n"
        else:
            guidance += "No specific algorithm triggered. Maintain standard protocol.\n"
            
        if projection_text:
            guidance += f"\n{projection_text}\n"
            
        return guidance

    def execute_decision_matrix(self, stimulus_vector: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Task 4.2: Parallel Evaluation (The Gap)
        Consults GKS blocks based on stimulus.
        STRICTLY DATA-DRIVEN: Matches stress levels to safety mechanisms.
        """
        matrix_results = []
        
        # 1. Consult Master Block (Instinct) - Placeholder for v9.3.3
        # In full production, this would match 16D vectors.
        
        # 2. Consult Genesis Protocols (Process)
        # Check for system control protocols that might apply to current state
        proto_root = self.gks_loader.get_genesis_block('protocol').get("genesis_block", {})
        protocols = proto_root.get("protocols", [])
        for proto in protocols:
            # If stress is high and protocol is safety-related, inject advice
            # Use partial match for 'integrity' to catch 'data_integrity' etc.
            tags = [t.lower() for t in proto.get("tags", [])]
            if stimulus_vector.get('stress', 0) > 0.8 and any("integrity" in t for t in tags):
                matrix_results.append({
                    "source": proto["id"],
                    "advice": proto["core_definition"],
                    "weight": 1.0
                })

        self.decision_matrix = matrix_results
        return matrix_results

        for item in self.decision_matrix:
            synthesis += f"- **{item['source']}**: {item['advice']} (Weight: {item['weight']})\n"
            
        return synthesis

# Lifecycle Hook for Orchestrator
def get_engine():
    return NexusMindEngine()