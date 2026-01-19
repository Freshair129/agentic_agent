from typing import Dict, Any, Optional
from .Module.encoding_module.encoding_module import ResonanceEncodingModule
from .Module.latching_module.latching_module import LatchingModule

class ResonanceMemorySystem:
    """
    System: ResonanceMemorySystem (RMS)
    Version: 2.5.0 (V9 Alignment)
    Role: Orchestrates Affective Encoding and State Latching
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.encoding_module = ResonanceEncodingModule(self.config)
        self.latching_module = LatchingModule(self.config)

    def step(self, 
             eva_matrix: Dict[str, Any], 
             rim_output: Dict[str, Any], 
             reflex_state: Dict[str, float], 
             ri_total: float = 0.0) -> Dict[str, Any]:
        """
        Executes one cognitive resonance cycle.
        """
        # 1. Encoding Phase
        encoded = self.encoding_module.encode(eva_matrix, rim_output, reflex_state)
        
        # 2. Latching & Packaging Phase
        snapshot = self.latching_module.process_latch(
            eva_matrix=eva_matrix,
            intensity=encoded["intensity"],
            color_axes=encoded["color_axes"],
            ri=ri_total,
            threat=encoded["threat_level"],
            trauma=encoded["trauma_flag"]
        )
        
        return snapshot

    def get_full_state(self) -> Dict[str, Any]:
        return self.latching_module.export_state()

    def load_state(self, state_dict: Dict[str, Any]):
        self.latching_module.import_state(state_dict)
