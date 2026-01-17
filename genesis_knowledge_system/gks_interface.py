"""
GKS Interface Module
Unified API for accessing Genesis Knowledge System and NexusMind Engine.
"""

from typing import Dict, Any, Optional, List
from genesis_knowledge_system.gks_loader import GKSLoader
from genesis_knowledge_system.nexus_mind.nexus_mind_engine import NexusMindEngine

class GKSInterface:
    def __init__(self):
        self.loader = GKSLoader()
        self.loader.load_all()
        self.nexus = NexusMindEngine()

    # --- Knowledge Access (Static) ---
    def query_master(self) -> Dict[str, Any]:
        """Get Master Block rules."""
        return self.loader.get_master_block()

    def query_genesis(self, category: str) -> Optional[Dict[str, Any]]:
        """Get specific Genesis Block (algorithm, concept, etc.)."""
        return self.loader.get_genesis_block(category)

    # --- Cognitive Strategy (Dynamic) ---
    def check_insecurity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run NexusMind insecurity check (Pre-Inference)."""
        return self.nexus.process_insecurity_check(context)

    def get_strategic_guidance(self, stimulus_vector: Dict[str, float]) -> str:
        """Get guidance for The Gap phase."""
        results = self.nexus.execute_decision_matrix(stimulus_vector)
        return self.nexus.synthesize_final_view({"decision_matrix": results})

# Singleton instance
gks_interface = GKSInterface()
