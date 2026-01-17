from abc import ABC, abstractmethod
from typing import Dict, List, Any

class IMemoryStorage(ABC):
    """
    Interface for Memory Storage operations.
    Standardizes how memories are written to the persistent layer.
    """

    @abstractmethod
    def store_episode(self, episode_data: Dict[str, Any]) -> bool:
        """Persists a full episodic record."""
        pass

    @abstractmethod
    def update_semantic_node(self, node_id: str, updates: Dict[str, Any]) -> bool:
        """Updates or reinforces a semantic concept."""
        pass

    @abstractmethod
    def archive_session(self, session_id: str) -> str:
        """Freezes and archives a complete session."""
        pass
