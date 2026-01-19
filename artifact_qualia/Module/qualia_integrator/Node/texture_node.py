from typing import Dict, Any, List, Optional

class TextureNode:
    """
    Node: TextureNode
    Role: Logic Provider for Qualia Calculation
    Responsibility: Pure logic for Intensity, Tone, Coherence, Depth, and Texture.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        dynamics = self.config.get("dynamics", {})
        
        # Alphas for EMA
        self.alphas = dynamics.get("temporal_smoothing", {
            "intensity_alpha": 0.65,
            "coherence_alpha": 0.70,
            "depth_alpha": 0.85
        })
        
        # Texture Modulation
        self.modulation = dynamics.get("texture_modulation", {
            "impact_boost": 1.15,
            "clamping": [0.0, 1.0]
        })
        
        # Thresholds
        self.thresholds = dynamics.get("thresholds", {
            "quiet_groundedness": 0.6,
            "charged_stress": 0.7,
            "perception_min": 0.05
        })

    def compute_metrics(self, eva: Dict[str, float], rim: Any, last_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Computes all qualia metrics based on current input and last state.
        """
        intensity = self._compute_intensity(eva, rim, last_state.get("intensity", 0.3))
        coherence = self._compute_coherence(eva, rim, last_state.get("coherence", 0.6))
        depth = self._compute_depth(eva, intensity)
        tone = self._derive_tone(eva, rim)
        texture = self._build_texture(eva, rim)

        return {
            "intensity": intensity,
            "coherence": coherence,
            "depth": depth,
            "tone": tone,
            "texture": texture
        }

    def _compute_intensity(self, eva: Dict[str, float], rim: Any, last_intensity: float) -> float:
        base = max(0.0, min(1.0, eva.get("baseline_arousal", 0.0) + eva.get("emotional_tension", 0.0)))
        impact_boost = {"low": 0.0, "medium": 0.1, "high": 0.25}.get(rim.impact_level, 0.0)
        trend_mod = {"rising": 1.1, "stable": 1.0, "fading": 0.85}.get(rim.impact_trend, 1.0)
        raw = max(0.0, min(1.0, (base + impact_boost) * trend_mod))
        
        alpha = self.alphas.get("intensity_alpha", 0.65)
        return (alpha * last_intensity) + ((1.0 - alpha) * raw)

    def _compute_coherence(self, eva: Dict[str, float], rim: Any, last_coherence: float) -> float:
        stability = eva.get("coherence", 0.5)
        momentum = eva.get("momentum", 0.5)
        disruption = {"low": 0.05, "medium": 0.15, "high": 0.30}.get(rim.impact_level, 0.1)
        raw = max(0.0, min(1.0, stability + momentum - disruption))
        
        alpha = self.alphas.get("coherence_alpha", 0.70)
        return (alpha * last_coherence) + ((1.0 - alpha) * raw)

    def _compute_depth(self, eva: Dict[str, float], intensity: float) -> float:
        # slow immersion depth logic
        target = max(0.0, min(1.0, eva.get("calm_depth", 0.0) * 0.6 + eva.get("emotional_tension", 0.0) * 0.4))
        return target 

    def _derive_tone(self, eva: Dict[str, float], rim: Any) -> str:
        if eva.get("calm_depth", 0.0) > self.thresholds.get("quiet_groundedness", 0.6): return "quiet"
        if eva.get("emotional_tension", 0.0) > self.thresholds.get("charged_stress", 0.7): return "charged"
        if rim.impact_trend == "fading": return "settling"
        return "neutral"

    def _get_clamped(self, val: float) -> float:
        c = self.modulation.get("clamping", [0.0, 1.0])
        return max(c[0], min(c[1], val))

    def _build_texture(self, eva: Dict[str, float], rim: Any) -> Dict[str, float]:
        texture = {
            "emotional": eva.get("emotional_tension", 0.0),
            "relational": eva.get("baseline_arousal", 0.0),
            "identity": eva.get("coherence", 0.0),
            "ambient": eva.get("momentum", 0.0),
        }
        boost = self.modulation.get("impact_boost", 1.15)
        for d in rim.affected_domains:
            if d in texture: texture[d] = self._get_clamped(texture[d] * boost)
        return texture
