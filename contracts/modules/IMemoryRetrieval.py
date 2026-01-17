from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class IMemoryRetrieval(ABC):
    """
    Interface for Memory Retrieval capabilities.
    Defines how the organism retrieves information from its subconscious.
    """

    @abstractmethod
    def retrieve_by_tags(self, tags: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieves memories matched against semantic tags."""
        pass

    @abstractmethod
    def retrieve_by_resonance(self, min_ri: float, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieves memories based on salience (Resonance Index)."""
        pass

    @abstractmethod
    def retrieve_by_state_similarity(self, state_snapshot: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """Retrieves memories that culturally/biologically match a given state."""
        pass
