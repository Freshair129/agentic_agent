"""
CircadianController
Version: v9.0

Role:
- Circadian modulation of endocrine stimuli
- Light / activity driven
- Phase-based (24h)
- Output stimulus modifiers only

NO:
- hormone production
- blood / plasma mutation
- blood interaction
"""

import math
from datetime import datetime
from typing import Dict, Any, Optional


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


class CircadianController:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.circ = cfg.get("circadian", {})

    # --------------------------------------------------
    # Main step
    # --------------------------------------------------

    def step(
        self,
        zeitgeber_inputs: Dict[str, float],
        now: datetime
    ) -> Dict[str, float]:
        """
        Returns:
          { hormone_id: stimulus_modifier }
        """

        hour = now.hour + now.minute / 60.0
        outputs: Dict[str, float] = {}

        # -------------------------------
        # Zeitgeber aggregation
        # -------------------------------
        z_drive = 0.0

        zeitgebers = self.circ.get("zeitgebers", {})
        for group, signals in zeitgebers.items():
            if not isinstance(signals, dict): continue
            for k, w in signals.items():
                gain = w.get("gain", 1.0) if isinstance(w, dict) else w
                z_drive += zeitgeber_inputs.get(k, 0.0) * gain

        # -------------------------------
        # Hormone modulation
        # -------------------------------
        modulation = self.circ.get("hormone_modulation", {})
        for h_id, mod_cfg in modulation.items():
            value = 0.0

            # night / morning windows
            if isinstance(mod_cfg, dict):
                for window_name, win in mod_cfg.items():
                    if not isinstance(win, dict):
                        # Some might be direct gains
                        if window_name == "daylight_suppression" and zeitgeber_inputs.get("daylight"):
                            value += win
                        continue

                    if "start_hour" in win and "end_hour" in win:
                        if self._in_window(hour, win["start_hour"], win["end_hour"]):
                            value += win.get("amplitude", 0.0)

            value += z_drive
            
            # Resilient clamp
            output_cfg = self.circ.get("output", {})
            clamp_range = output_cfg.get("clamp", [0.0, 5.0])
            
            value = clamp(value, clamp_range[0], clamp_range[1])
            outputs[h_id] = value

        return outputs

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _in_window(self, hour, start, end):
        if start <= end:
            return start <= hour < end
        else:
            # wrap around midnight
            return hour >= start or hour < end
