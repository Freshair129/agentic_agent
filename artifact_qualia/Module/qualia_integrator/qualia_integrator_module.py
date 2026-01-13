from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .Node.texture_logic.texture_node import TextureNode

@dataclass
class QualiaSnapshot:
    """
    Lived phenomenological snapshot.
    """
    intensity: float
    tone: str
    coherence: float
    depth: float
    texture: Dict[str, float]

class QualiaIntegratorModule:
    """
    Module: QualiaIntegratorModule
    Role: Functional Integrator for Phenomenological Experience
    Responsibility: Orchestrates qualia integration flow using TextureNode.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.texture_node = TextureNode(config)
        self.last_intensity: float = 0.3
        self.last_coherence: float = 0.6

    def set_state(self, last_intensity: float, last_coherence: float):
        """Injects state from System (Persistence Layer)."""
        self.last_intensity = last_intensity
        self.last_coherence = last_coherence

    def get_internal_state(self) -> Dict[str, float]:
        """Returns internal state for System persistence."""
        return {
            "last_intensity": self.last_intensity,
            "last_coherence": self.last_coherence
        }

    def integrate(self, eva_state: Dict[str, float], rim_semantic: Any) -> QualiaSnapshot:
        """
        Orchestrates integration flow.
        """
        # Prepare context
        last_state = {
            "intensity": self.last_intensity,
            "coherence": self.last_coherence
        }

        # Delegate to Node
        metrics = self.texture_node.compute_metrics(eva_state, rim_semantic, last_state)

        # Update Internal State (Transient)
        self.last_intensity = metrics["intensity"]
        self.last_coherence = metrics["coherence"]

        return QualiaSnapshot(
            intensity=metrics["intensity"],
            tone=metrics["tone"],
            coherence=metrics["coherence"],
            depth=metrics["depth"],
            texture=metrics["texture"]
        )
