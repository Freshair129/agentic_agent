from typing import Dict, Any

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

class IntensityCalculationNode:
    """
    Node: IntensityCalculationNode
    Role: Pure logic for affective load calculation
    """
    def compute(self, axes_9d: Dict[str, float], rim_output: Dict[str, Any]) -> float:
        base = clamp(axes_9d.get("arousal", 0.5) * 0.6 + axes_9d.get("stress", 0.3) * 0.4)
        
        impact_boost = {"low": 0.0, "medium": 0.1, "high": 0.25}.get(rim_output.get("impact_level", "low"), 0.0)
        trend_mod = {"rising": 1.1, "stable": 1.0, "fading": 0.85}.get(rim_output.get("impact_trend", "stable"), 1.0)

        return clamp((base + impact_boost) * trend_mod)
