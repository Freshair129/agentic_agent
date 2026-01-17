# =============================================================================
# RMS ENGINE v6.2 (Merged & Standardized)
# Resonance Memory System (EVA_Matrix–based)
# =============================================================================

import math
from typing import Dict, Any, List, Optional
from datetime import datetime

# -----------------------------------------------------------------------------
# Utils
# -----------------------------------------------------------------------------

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def smooth(prev: float, now: float, alpha: float = 0.7) -> float:
    return (alpha * prev) + ((1.0 - alpha) * now)

# -----------------------------------------------------------------------------
# RMS Engine
# -----------------------------------------------------------------------------

class RMSEngineV6:
    """
    Resonance Memory System v6.2
    - Merged with logicupdate.py
    - Output aligned with Episodic Memory Schema
    - Aligned with 9D Axes
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # 1. Load Logic Configuration
        self.config = config or {}
        logic = self.config.get("logic", {})
        
        # Encoding Parameters
        self.trauma_threshold = logic.get("trauma_threshold", 0.85)
        
        # Temporal Smoothing Alphas
        smoothing = logic.get("smoothing", {})
        self.color_alpha = smoothing.get("color_axes_alpha", 0.65)
        self.intensity_alpha = smoothing.get("intensity_alpha", 0.70)
        
        # Trauma Protection
        protection = logic.get("trauma_protection", {})
        self.trauma_dim_factor = protection.get("color_dim_factor", 0.55)
        self.trauma_intensity_reduction = protection.get("intensity_reduction", 0.50)

        # Internal smoothing memory
        self._last_color_axes = {
            "stress": 0.2,
            "warmth": 0.5,
            "clarity": 0.5,
            "drive": 0.3,
            "calm": 0.4,
        }
        self._last_intensity = 0.3

    def process(
        self,
        eva_matrix: Dict[str, Any],
        rim_output: Dict[str, Any],
        reflex_state: Dict[str, float],
        ri_total: float = 0.0
    ) -> Dict[str, Any]:
        """
        Process internal states into a memory-ready snapshot.
        """
        # 1. Trauma Detection
        threat = reflex_state.get("threat_level", 0.0)
        trauma_flag = threat > self.trauma_threshold

        # 2. Color Generation
        raw_color_axes = self._generate_color_axes(eva_matrix)
        
        # 3. Intensity Calculation
        raw_intensity = self._compute_intensity(eva_matrix, rim_output)

        # 4. Trauma Protection
        if trauma_flag:
            raw_color_axes = {k: v * self.trauma_dim_factor for k, v in raw_color_axes.items()}
            raw_intensity *= self.trauma_intensity_reduction

        # 5. Smoothing
        color_axes = {
            k: smooth(self._last_color_axes[k], v, alpha=self.color_alpha)
            for k, v in raw_color_axes.items()
        }
        intensity = smooth(self._last_intensity, raw_intensity, alpha=self.intensity_alpha)

        # Update last state
        self._last_color_axes = color_axes
        self._last_intensity = intensity

        # 6. Formatting
        return self._package_output(eva_matrix, ri_total, intensity, color_axes, threat, trauma_flag)

    def _generate_color_axes(self, eva: Dict[str, Any]) -> Dict[str, float]:
        """Mapping 9D Axes -> 5 RMS Color Axes"""
        axes = eva.get("axes_9d", {})
        return {
            "stress": clamp(axes.get("stress", 0.0)),
            "warmth": clamp(axes.get("valence", 0.5)),
            "clarity": clamp(axes.get("clarity", 0.5)),
            "drive": clamp(axes.get("arousal", 0.3)),
            "calm": clamp(axes.get("groundedness", 0.5))
        }

    def _compute_intensity(self, eva: Dict[str, Any], rim: Dict[str, Any]) -> float:
        """Overall affective intensity based on load and resonance impact"""
        axes = eva.get("axes_9d", {})
        base = clamp(axes.get("arousal", 0.5) * 0.6 + axes.get("stress", 0.3) * 0.4)
        
        impact_boost = {"low": 0.0, "medium": 0.1, "high": 0.25}.get(rim.get("impact_level", "low"), 0.0)
        trend_mod = {"rising": 1.1, "stable": 1.0, "fading": 0.85}.get(rim.get("impact_trend", "stable"), 1.0)

        raw = clamp((base + impact_boost) * trend_mod)
        return raw

    def _package_output(self, 
                       eva: Dict[str, Any], 
                       ri: float, 
                       intensity: float, 
                       color_axes: Dict[str, float], 
                       threat: float,
                       trauma: bool) -> Dict[str, Any]:
        """Aligns output with episodic_memory_spec.yaml state_snapshot structure"""
        
        thresholds = self.config.get("logic", {}).get("thresholds", {})
        high = thresholds.get("high_resonance", 0.85)
        med = thresholds.get("medium_resonance", 0.65)
        low = thresholds.get("low_resonance", 0.40)

        if trauma:
            level = self.config.get("logic", {}).get("trauma_protection", {}).get("force_level", "L4_trauma")
        elif intensity < low:
            level = "L0_trace"
        elif intensity < med:
            level = "L1_light"
        elif intensity < high:
            level = "L2_standard"
        else:
            level = "L3_deep"

        r_val = color_axes.get("stress", 0.0) * 255
        g_val = color_axes.get("calm", 0.0) * 200 + color_axes.get("clarity", 0.0) * 55
        b_val = color_axes.get("warmth", 0.0) * 150 + color_axes.get("calm", 0.0) * 100
        r_val += color_axes.get("warmth", 0.0) * 50
        
        multiplier = (intensity * 0.5) + (color_axes.get("clarity", 0.5) * 0.5)
        
        final_r = int(max(0, min(255, r_val * multiplier)))
        final_g = int(max(0, min(255, g_val * multiplier)))
        final_b = int(max(0, min(255, b_val * multiplier)))
        hex_color = f"#{final_r:02x}{final_g:02x}{final_b:02x}"

        return {
            "matrix_snapshot": eva,
            "Resonance_index": float(ri),
            "memory_encoding_level": level,
            "memory_color": hex_color,
            "resonance_texture": {k: float(v) for k, v in color_axes.items()},
            "qualia": {
                "intensity": float(intensity)
            },
            "reflex": {
                "threat_level": float(threat)
            },
            "trauma_flag": trauma,
            "timestamp": datetime.now().isoformat()
        }

    def get_full_state(self) -> Dict[str, Any]:
        return {
            "last_color_axes": {k: float(v) for k, v in self._last_color_axes.items()},
            "last_intensity": float(self._last_intensity)
        }

    def load_state(self, state_dict: Dict[str, Any]):
        if "last_color_axes" in state_dict:
            self._last_color_axes.update(state_dict["last_color_axes"])
        self._last_intensity = state_dict.get("last_intensity", 0.3)
