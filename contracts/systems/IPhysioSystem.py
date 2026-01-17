from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IPhysioSystem(ABC):
    """Contract for the Physiological Core System"""
    
    @abstractmethod
    def step(self, eva_stimuli: list, zeitgebers: Dict, dt: float) -> Dict[str, Any]:
        """Advance physiological simulation by dt seconds."""
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Retrieve current full biological state."""
        pass
