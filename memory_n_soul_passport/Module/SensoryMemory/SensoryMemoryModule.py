from typing import Dict, Any
from .Node.QualiaStorageNode import QualiaStorageNode

class SensoryMemoryModule:
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
