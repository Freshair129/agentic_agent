from abc import ABC, abstractmethod
from typing import Dict, Any

class ICognitiveGateway(ABC):
    """Contract for SLM (Small Language Model) Bridge"""
    
    @abstractmethod
    def extract_intent(self, user_input: str) -> Dict[str, Any]:
        """Extract intent, emotional signal, and salience anchor."""
        pass
