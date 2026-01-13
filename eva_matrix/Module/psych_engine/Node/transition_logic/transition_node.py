from typing import Dict, Any, List

class TransitionNode:
    """
    Node: TransitionNode
    Role: Logic Provider for 5+2+2 Dimensional Model
    Responsibility: Pure logic calculation for state transitions. No state ownership.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def calculate_transition(self, current_axes: Dict[str, float], current_momentum: Dict[str, float], signals: Dict[str, float]) -> Dict[str, Any]:
        """
        Implements the 5+2+2 dimensional logic.
        """
        dynamics = self.config.get("mood_dynamics", {})
        inertia = dynamics.get("state_inertia", 0.7)
        learning_rate = dynamics.get("learning_rate", 0.3)
        
        new_axes = {}
        structure = self.config.get("axes_structure", {})

        # A. 5 Core Affective Axes
        core_5d = structure.get("core_5d", {})
        for axis_name, spec in core_5d.items():
            pos_sum = sum(signals.get(h, 0.0) for h in spec.get("positive_factors", []))
            neg_sum = sum(signals.get(h, 0.0) for h in spec.get("negative_factors", []))
            
            raw_influence = max(0.0, min(1.0, pos_sum - neg_sum))
            prev_val = current_axes.get(axis_name, 0.5)
            
            # Apply momentum/inertia logic
            new_val = (raw_influence * learning_rate) + (prev_val * inertia)
            new_axes[axis_name] = round(max(0.0, min(1.0, new_val)), 3)

        # B. 2 Meta-Directional Axes (Directions)
        # stability logic (formula simplified)
        gaba = signals.get("ESC_N05_GABA", 0.0)
        ad = signals.get("ESC_H01_ADRENALINE", 0.0)
        new_axes["stability"] = round(max(0.0, min(1.0, 0.5 + (gaba - ad))), 3)
        
        # orientation logic
        ox = signals.get("ESC_H04_OXYTOCIN", 0.0)
        cor = signals.get("ESC_H02_CORTISOL", 0.0)
        new_axes["orientation"] = round(max(0.0, min(1.0, 0.5 + (ox - cor))), 3)

        # C. 2 Categorical Axes (Pointers)
        sorted_cores = sorted(core_5d.keys(), key=lambda x: new_axes[x], reverse=True)
        new_axes["primary"] = sorted_cores[0] if sorted_cores else "None"
        new_axes["secondary"] = sorted_cores[1] if len(sorted_cores) > 1 else "None"

        # D. Emotion Labeling (7D categorization)
        label = self._map_emotion_label(new_axes)

        # E. Momentum & Reflex Directives
        decay = dynamics.get("momentum_decay", 0.15)
        prev_momentum_val = current_momentum.get("intensity", 0.1)
        new_momentum_val = (prev_momentum_val * (1.0 - decay)) + (sum(new_axes[a] for a in core_5d) / 5.0 * decay)
        
        threshold = self.config.get("runtime_hook", {}).get("reflex_thresholds", {}).get("high_stress", 0.85)
        urgency = 0.8 if new_axes["stress"] > threshold else 0.2

        return {
            "axes_9d": new_axes,
            "emotion_label": label,
            "momentum": {"intensity": round(new_momentum_val, 3)},
            "reflex_directives": {"urgency": urgency, "concise": urgency > 0.5}
        }

    def _map_emotion_label(self, axes: Dict[str, Any]) -> str:
        """Categorizes 9D state into human label."""
        categories = self.config.get("emotion_categories", {})
        
        for label, spec in categories.items():
            cond = spec.get("condition", "")
            if cond == "default": continue
            
            try:
                # Replace axis names with values for eval
                safe_cond = cond
                for axis in ["stress", "warmth", "drive", "clarity", "joy"]:
                    safe_cond = safe_cond.replace(axis, str(axes.get(axis, 0.0)))
                
                if eval(safe_cond):
                    return label
            except:
                continue
                
        return "Calm"
