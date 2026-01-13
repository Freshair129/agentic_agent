from typing import Dict, Any, List
from .Node.transition_logic.transition_node import TransitionNode

class MatrixPsychModule:
    """
    Module: MatrixPsychModule
    Role: Functional Integrator for Psychological State
    Responsibility: Orchestrates state transition flow using nodes. No direct state ownership (passed from System).
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.transition_node = TransitionNode(config)

    def process_signals(self, current_axes: Dict[str, float], current_momentum: Dict[str, float], signals: Dict[str, float]) -> Dict[str, Any]:
        """
        Orchestrates the signal processing flow.
        """
        # 1. Delegate calculation to Node
        result = self.transition_node.calculate_transition(current_axes, current_momentum, signals)
        
        return result
