from typing import Dict, Any

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

class ColorGenerationNode:
    """
    Node: ColorGenerationNode
    Role: Mappings 9D Psychological Matrix -> 5D Encoding Colors
    """
    def generate_color_axes(self, axes_9d: Dict[str, float]) -> Dict[str, float]:
        return {
            "stress": clamp(axes_9d.get("stress", 0.0)),
            "warmth": clamp(axes_9d.get("valence", 0.5)),
            "clarity": clamp(axes_9d.get("clarity", 0.5)),
            "drive": clamp(axes_9d.get("arousal", 0.3)),
            "calm": clamp(axes_9d.get("groundedness", 0.5))
        }

    def compute_hex(self, intensity: float, color_axes: Dict[str, float]) -> str:
        r_val = color_axes.get("stress", 0.0) * 255
        g_val = color_axes.get("calm", 0.0) * 200 + color_axes.get("clarity", 0.0) * 55
        b_val = color_axes.get("warmth", 0.0) * 150 + color_axes.get("calm", 0.0) * 100
        r_val += color_axes.get("warmth", 0.0) * 50
        
        multiplier = (intensity * 0.5) + (color_axes.get("clarity", 0.5) * 0.5)
        
        final_r = int(max(0, min(255, r_val * multiplier)))
        final_g = int(max(0, min(255, g_val * multiplier)))
        final_b = int(max(0, min(255, b_val * multiplier)))
        return f"#{final_r:02x}{final_g:02x}{final_b:02x}"
