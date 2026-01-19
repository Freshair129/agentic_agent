from typing import Dict, Any
from .Node.smoothing_node import TemporalSmoothingNode
from .Node.packaging_node import OutputPackagingNode

class LatchingModule:
    """
    Module: LatchingModule
    Role: Manages temporal smoothing and memory snapshot formatting
    """
    def __init__(self, config: Dict[str, Any]):
        logic = config.get("logic", {})
        smoothing = logic.get("smoothing", {})
        self.smoothing_node = TemporalSmoothingNode(
            color_alpha=smoothing.get("color_axes_alpha", 0.65),
            intensity_alpha=smoothing.get("intensity_alpha", 0.70)
        )
        self.packaging_node = OutputPackagingNode()
        
        self.thresholds = logic.get("thresholds", {})
        self._last_color_axes = {
            "stress": 0.2, "warmth": 0.5, "clarity": 0.5, "drive": 0.3, "calm": 0.4
        }
        self._last_intensity = 0.3

    def process_latch(self, 
                      eva_matrix: Dict[str, Any], 
                      intensity: float, 
                      color_axes: Dict[str, float], 
                      ri: float,
                      threat: float, 
                      trauma: bool) -> Dict[str, Any]:
        
        # 1. Smoothing
        smoothed_colors = self.smoothing_node.smooth_color(self._last_color_axes, color_axes)
        smoothed_intensity = self.smoothing_node.smooth_intensity(self._last_intensity, intensity)
        
        # Update state
        self._last_color_axes = smoothed_colors
        self._last_intensity = smoothed_intensity
        
        # 2. Determine Level
        level = self._determine_level(smoothed_intensity, trauma)
        
        # 3. Generate Hex Color (Simplified call to package)
        hex_color = self._generate_hex(smoothed_intensity, smoothed_colors)
        
        return self.packaging_node.package(
            eva_matrix, ri, smoothed_intensity, smoothed_colors, hex_color, level, threat, trauma
        )

    def _determine_level(self, intensity: float, trauma: bool) -> str:
        high = self.thresholds.get("high_resonance", 0.85)
        med = self.thresholds.get("medium_resonance", 0.65)
        low = self.thresholds.get("low_resonance", 0.40)

        if trauma: return "L4_trauma"
        if intensity < low: return "L0_trace"
        if intensity < med: return "L1_light"
        if intensity < high: return "L2_standard"
        return "L3_deep"

    def _generate_hex(self, intensity: float, color_axes: Dict[str, float]) -> str:
        # Re-using logic from color node spec (Virtual call)
        r_val = (color_axes.get("stress", 0.0) * 255) + (color_axes.get("warmth", 0.0) * 50)
        g_val = (color_axes.get("calm", 0.0) * 200) + (color_axes.get("clarity", 0.0) * 55)
        b_val = (color_axes.get("warmth", 0.0) * 150) + (color_axes.get("calm", 0.0) * 100)
        
        multiplier = (intensity * 0.5) + (color_axes.get("clarity", 0.5) * 0.5)
        fr = int(max(0, min(255, r_val * multiplier)))
        fg = int(max(0, min(255, g_val * multiplier)))
        fb = int(max(0, min(255, b_val * multiplier)))
        return f"#{fr:02x}{fg:02x}{fb:02x}"

    def export_state(self) -> Dict[str, Any]:
        return {
            "last_color_axes": self._last_color_axes,
            "last_intensity": self._last_intensity
        }

    def import_state(self, state: Dict[str, Any]):
        self._last_color_axes = state.get("last_color_axes", self._last_color_axes)
        self._last_intensity = state.get("last_intensity", self._last_intensity)
