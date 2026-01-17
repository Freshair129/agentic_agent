from typing import Dict, Any, Optional, List
from .Node.GroundingNode import GroundingNode

class SemanticMemoryModule:
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
