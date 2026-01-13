"""
PhysioCore: Endocrine Controller
Version: v9.1

Role:
- Orchestrate endocrine glands
- Maintain gland states
- Convert stimuli -> hormone mass output (pg)
- Support Vagus Inhibition feedback
"""

from typing import Dict, Any
from .glands import EndocrineGland

class EndocrineController:
    """
    Endocrine = production + regulation layer
    """

    def __init__(self, glands: Dict[str, EndocrineGland]):
        """
        glands:
            {
              hormone_id: EndocrineGland(...)
            }
        """
        self.glands: Dict[str, EndocrineGland] = glands

        # Internal gland states (pure endocrine state)
        self.states: Dict[str, dict] = {
            h_id: gland.create_initial_state()
            for h_id, gland in glands.items()
        }

    def step(
        self,
        stimuli: Dict[str, float],
        dt: float,
        inhibition: float = 0.0
    ) -> Dict[str, Any]:
        """
        Run one endocrine step.
        """
        released_pg: Dict[str, float] = {}

        for h_id, gland in self.glands.items():
            stimulus = float(stimuli.get(h_id, 0.0))
            state = self.states[h_id]

            # ---- Acute response (nerve surge) ----
            surge_pg, state = gland.trigger_nerve_surge(
                state=state,
                stimulus_intensity=stimulus
            )

            # ---- Normal tonic secretion ----
            # Pass inhibition factor (e.g., from Vagus Nerve)
            flux_pg, state = gland.process_step(
                state=state,
                stimulus=stimulus,
                dt=dt,
                inhibition=inhibition
            )

            total_pg = surge_pg + flux_pg
            if total_pg > 0.0:
                released_pg[h_id] = total_pg

            # persist updated state
            self.states[h_id] = state

        return {
            "released_pg": released_pg,
            "gland_state": self.states
        }

    def get_gland_state(self, hormone_id: str) -> dict:
        return self.states.get(hormone_id, {}).copy()

    def get_all_states(self) -> Dict[str, dict]:
        return {
            h_id: state.copy()
            for h_id, state in self.states.items()
        }

    def load_states(self, state_map: Dict[str, dict]):
        for h_id, state in state_map.items():
            if h_id in self.states:
                self.states[h_id] = state.copy()

    def export_states(self) -> Dict[str, dict]:
        return {
            h_id: state.copy()
            for h_id, state in self.states.items()
        }

    def get_status_report(self) -> Dict[str, dict]:
        report = {}
        for h_id, gland in self.glands.items():
            report[h_id] = gland.get_status(self.states[h_id])
        return report
