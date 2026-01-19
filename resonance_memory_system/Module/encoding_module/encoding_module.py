from typing import Dict, Any
from .Node.color_node import ColorGenerationNode
from .Node.intensity_node import IntensityCalculationNode
from .Node.trauma_node import TraumaProtectionNode

class ResonanceEncodingModule:
    """
    Module: ResonanceEncodingModule
    Role: Transforms Matrix state into affective encoding parameters
    """
    def __init__(self, config: Dict[str, Any]):
        logic = config.get("logic", {})
        self.trauma_node = TraumaProtectionNode(logic.get("trauma_threshold", 0.85))
        self.color_node = ColorGenerationNode()
        self.intensity_node = IntensityCalculationNode()
        
        protection = logic.get("trauma_protection", {})
        self.dim_factor = protection.get("color_dim_factor", 0.55)
        self.reduction = protection.get("intensity_reduction", 0.50)

    def encode(self, eva_matrix: Dict[str, Any], rim_output: Dict[str, Any], reflex_state: Dict[str, float]) -> Dict[str, Any]:
        axes_9d = eva_matrix.get("axes_9d", {})
        threat = reflex_state.get("threat_level", 0.0)
        
        # 1. Trauma Detection
        trauma_flag = self.trauma_node.evaluate(threat)
        
        # 2. Base Calculation
        raw_color_axes = self.color_node.generate_color_axes(axes_9d)
        raw_intensity = self.intensity_node.compute(axes_9d, rim_output)
        
        # 3. Shielding
        if trauma_flag:
            raw_color_axes, raw_intensity = self.trauma_node.apply_shield(
                raw_color_axes, raw_intensity, self.dim_factor, self.reduction
            )
            
        return {
            "color_axes": raw_color_axes,
            "intensity": raw_intensity,
            "trauma_flag": trauma_flag,
            "threat_level": threat
        }
