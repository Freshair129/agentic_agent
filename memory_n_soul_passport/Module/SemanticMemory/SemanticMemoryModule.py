from typing import Dict, Any, Optional, List
from .Node.GroundingNode import GroundingNode
import sys
from pathlib import Path

# Add contracts path for import
sys.path.append(str(Path(__file__).parent.parent.parent.parent.resolve()))
from contracts.modules.IMemoryStorage import IMemoryStorage

class SemanticMemoryModule(IMemoryStorage):
    """
    Manages situational knowledge and validates it against historical truths.
    Implements the "Situation Grounding" buffer.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.grounding = GroundingNode(config)
        
        # Resolve Module Parameters
        mod_cfg = config.get("module_definitions", {}).get("semantic_memory_module", {})
        self.params = mod_cfg.get("parameters", {})
        
        self.buffer_size = self.params.get("situation_grounding_buffer", 5)
        
    def process_new_knowledge(self, knowledge_proposals: List[Dict[str, Any]], user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validates proposed facts against user profile.
        Returns a list of verified or flagged facts.
        """
        results = []
        for fact in knowledge_proposals:
            conflict = self.grounding.check_conflict(fact, user_profile)
            fact["grounding_status"] = "conflicted" if conflict["has_conflict"] else "stable"
            fact["conflict_details"] = conflict
            results.append(fact)
        return results

    # --- IMemoryStorage Implementation ---

    def store_episode(self, episode_data: Dict[str, Any]) -> bool:
        """Extracts and stores semantic facts from an episode."""
        proposals = episode_data.get("situation_context", {}).get("knowledge_proposals", [])
        if proposals:
            self.process_new_knowledge(proposals, {})
            # Actually store them in GroundingNode/SemanticDB
            for prop in proposals:
                self.grounding.persist_fact(prop)
            return True
        return False

    def update_semantic_node(self, node_id: str, updates: Dict[str, Any]) -> bool:
        """Reinforces or updates a specific semantic node."""
        return self.grounding.update_fact(node_id, updates)

    def archive_session(self, session_id: str) -> str:
        return f"SEM_ARCHIVE_{session_id}"
