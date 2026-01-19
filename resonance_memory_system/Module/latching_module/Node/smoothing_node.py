from typing import Dict

def smooth(prev: float, now: float, alpha: float = 0.7) -> float:
    return (alpha * prev) + ((1.0 - alpha) * now)

class TemporalSmoothingNode:
    """
    Node: TemporalSmoothingNode
    Role: State persistence and recursive filtering
    """
    def __init__(self, color_alpha: float = 0.65, intensity_alpha: float = 0.70):
        self.color_alpha = color_alpha
        self.intensity_alpha = intensity_alpha

    def smooth_color(self, last_color: Dict[str, float], new_color: Dict[str, float]) -> Dict[str, float]:
        return {
            k: smooth(last_color.get(k, 0.5), v, alpha=self.color_alpha)
            for k, v in new_color.items()
        }

    def smooth_intensity(self, last_intensity: float, new_intensity: float) -> float:
        return smooth(last_intensity, new_intensity, alpha=self.intensity_alpha)
