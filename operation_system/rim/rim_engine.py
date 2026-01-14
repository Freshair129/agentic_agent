import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class RIMCalculator:
    """
    RIM Calculator Utility
    Maps SLM emotional signals and salience anchors to numerical Resonance Impact (RIM) scores.
    """
    def __init__(self, config_path: Optional[str] = None):
        self.base_path = Path(__file__).parent
        self.config_path = Path(config_path) if config_path else self.base_path / "configs/RIM_configs.yaml"
        self.config = self._load_config()
        self.emotion_map = self.config.get("emotion_map", {})
        self.anchor_settings = self.config.get("anchor_settings", {})
        self.constraints = self.config.get("constraints", {})

    def _load_config(self) -> Dict[str, Any]:
        """Loads YAML configuration."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def calculate_impact(self, signal: str, anchor: str) -> float:
        """
        Calculate a raw impact score based on signal and anchor characteristics.
        """
        base_score = self.emotion_map.get(signal.lower(), 0.0)
        
        # Apply anchor multipliers from config
        multiplier = self.anchor_settings.get("default_multiplier", 1.0)
        if anchor and anchor != "None":
            length_settings = self.anchor_settings.get("length_multipliers", {})
            if len(anchor) > length_settings.get("long_threshold", 10):
                multiplier = length_settings.get("long_multiplier", 1.2)
            elif len(anchor) < length_settings.get("short_threshold", 3):
                multiplier = length_settings.get("short_multiplier", 0.8)
        
        final_score = base_score * multiplier
        
        # Clamp based on config constraints
        min_s = self.constraints.get("min_score", -1.0)
        max_s = self.constraints.get("max_score", 1.0)
        return max(min_s, min(max_s, final_score))

# Singleton for easy access (initialized with default config)
rim_calc = RIMCalculator()
