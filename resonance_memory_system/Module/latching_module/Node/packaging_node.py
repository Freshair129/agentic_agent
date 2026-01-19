from typing import Dict, Any
from datetime import datetime

class OutputPackagingNode:
    """
    Node: OutputPackagingNode
    Role: Aligning output with episodic/sensory memory schemas
    """
    def package(self, 
                eva_matrix: Dict[str, Any], 
                ri: float, 
                intensity: float, 
                color_axes: Dict[str, float], 
                hex_color: str,
                level: str,
                threat: float, 
                trauma: bool) -> Dict[str, Any]:
        return {
            "matrix_snapshot": eva_matrix,
            "Resonance_index": ri,
            "memory_encoding_level": level,
            "memory_color": hex_color,
            "resonance_texture": color_axes,
            "qualia": {"intensity": intensity},
            "reflex": {"threat_level": threat},
            "trauma_flag": trauma,
            "timestamp": datetime.now().isoformat()
        }
