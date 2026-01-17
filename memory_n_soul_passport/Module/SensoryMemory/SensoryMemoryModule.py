from typing import Dict, Any, List
from .Node.QualiaStorageNode import QualiaStorageNode
import sys
from pathlib import Path

# Add contracts path for import
sys.path.append(str(Path(__file__).parent.parent.parent.parent.resolve()))
from contracts.modules.IMemoryRetrieval import IMemoryRetrieval
from contracts.modules.IMemoryStorage import IMemoryStorage

class SensoryMemoryModule(IMemoryRetrieval, IMemoryStorage):
    """
    Subconscious module that records raw sensory evidence from Artifact Qualia.
    Provides the ground-truth perceptual link for memories.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.storage = QualiaStorageNode(config)
        
    def record_perception(self, perception_data: Dict[str, Any], episode_id: str):
        """
        Records a perception snapshot linked to an episode.
        """
        perception_data["episode_id"] = episode_id
        self.storage.write_sensory_record(perception_data)

    # --- IMemoryRetrieval Implementation ---

    def retrieve_by_tags(self, tags: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """Sensory data doesn't use tags directly, but can cross-reference with Episodic."""
        return []

    def retrieve_by_resonance(self, min_ri: float, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieves sensory records with high intensity (Qualia-based)."""
        records = self.storage.read_sensory_log()
        matches = []
        
        # Qualia intensity is treated as sensory RI
        sorted_records = sorted(records, key=lambda x: x.get("intensity", 0.0), reverse=True)
        
        for rec in sorted_records:
            if rec.get("intensity", 0.0) >= min_ri:
                matches.append(rec)
            if len(matches) >= limit:
                break
        return matches

    def retrieve_by_state_similarity(self, state_snapshot: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """Retrieves sensory records matching a biological state."""
        # This would require complex mapping, returning empty for now
        return []

    # --- IMemoryStorage Implementation ---

    def store_episode(self, episode_data: Dict[str, Any]) -> bool:
        """
        Extracts and records sensory qualia from an episode.
        """
        qualia = episode_data.get("state_snapshot", {}).get("qualia")
        episode_id = episode_data.get("episode_id")
        if qualia and episode_id:
            self.record_perception(qualia, episode_id)
            return True
        return False

    def update_semantic_node(self, node_id: str, updates: Dict[str, Any]) -> bool:
        """Not applicable to Sensory Module."""
        return False

    def archive_session(self, session_id: str) -> str:
        return f"SEN_ARCHIVE_{session_id}"
