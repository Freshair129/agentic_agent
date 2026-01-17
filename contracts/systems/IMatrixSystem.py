from abc import ABC, abstractmethod
from typing import Dict, Any

class IMatrixSystem(ABC):
    """Contract for the Psychological Matrix System"""
    
    @abstractmethod
    def step(self, physio_state: Dict, qualia_snapshot: Dict) -> Dict[str, Any]:
        """Update psychological axes based on bio-input."""
        pass
    
    @property
    @abstractmethod
    def axes_9d(self) -> Dict[str, float]:
        """Return the 9D emotional axes."""
        pass
