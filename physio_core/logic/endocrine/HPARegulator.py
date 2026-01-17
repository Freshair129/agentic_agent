"""
HPARegulator
Version: v9.0

Role:
- Model HPA axis (Stress → CRH → ACTH → Cortisol)
- Produce stimulus modifier for Cortisol gland ONLY
- Read-only access to plasma snapshot (optional)

NO:
- hormone production
- gland state mutation
- blood interaction
"""

import math
from typing import Dict, Any, Optional


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def sigmoid(x):
    # Protect against overflow
    if x < -50: return 0.0
    if x > 50: return 1.0
    return 1.0 / (1.0 + math.exp(-x))


class HPARegulator:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.hpa = cfg.get("HPA_axis", {})

        # Resilient config access
        self.alpha = cfg.get("global", {}).get("smoothing", {}).get("alpha", 0.05)
        if "dynamics" not in self.hpa:
             # Fallback to local default if hpa axis block is missing
             self.hpa["dynamics"] = {
                 "hypothalamus": {"input": {"stress_signal": 1.0}, "gain": 1.0, "baseline": 0.1},
                 "pituitary": {"gain": 0.9},
                 "adrenal": {"gain": 1.0}
             }

        # internal virtual hormone states
        self._crh = 0.0
        self._acth = 0.0

    # --------------------------------------------------
    # Main step
    # --------------------------------------------------

    def step(
        self,
        stress_inputs: Dict[str, float],
        plasma_snapshot: Optional[Dict[str, float]],
        dt: float
    ) -> Dict[str, float]:
        """
        Returns:
          { "COR": stimulus_modifier }
        """

        # -------------------------------
        # 1) Hypothalamus (Stress → CRH)
        # -------------------------------
        hypo_cfg = self.hpa["dynamics"]["hypothalamus"]

        drive = 0.0
        for k, w in hypo_cfg.get("input", {}).items():
            drive += stress_inputs.get(k, 0.0) * w

        target_crh = hypo_cfg.get("baseline", 0.1) + hypo_cfg.get("gain", 1.0) * drive
        self._crh = self._ema(self._crh, target_crh)

        # -------------------------------
        # 2) Pituitary (CRH → ACTH)
        # -------------------------------
        pit_cfg = self.hpa["dynamics"]["pituitary"]
        target_acth = self._crh * pit_cfg.get("gain", 0.9)
        self._acth = self._ema(self._acth, target_acth)

        # -------------------------------
        # 3) Adrenal drive (ACTH → COR)
        # -------------------------------
        adrenal_cfg = self.hpa["dynamics"]["adrenal"]
        cortisol_drive = self._acth * adrenal_cfg.get("gain", 1.0)

        # -------------------------------
        # 4) Negative feedback (COR ⟂ HPA)
        # -------------------------------
        if plasma_snapshot:
            # Safely get negative feedback config
            fb_cfg = self.hpa.get("negative_feedback", {}).get("cortisol_inhibition", {})
            if fb_cfg:
                cor_level = plasma_snapshot.get("COR", 0.0)
                threshold = fb_cfg.get("threshold", 1.0)
                strength = fb_cfg.get("strength", 0.7)
                inhibition = sigmoid((cor_level - threshold) * 5.0)
                cortisol_drive *= (1.0 - strength * inhibition)

        # Bound the output
        clamp_cfg = self.cfg.get("global", {}).get("clamp", {})
        min_v = clamp_cfg.get("stimulus_min", 0.0)
        max_v = clamp_cfg.get("stimulus_max", 5.0)
        
        cortisol_drive = clamp(cortisol_drive, min_v, max_v)

        return {"COR": cortisol_drive}

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _ema(self, prev, target):
        return (self.alpha * target) + ((1 - self.alpha) * prev)
