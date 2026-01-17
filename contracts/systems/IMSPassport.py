from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class IMSPassport(ABC):
    """
    Interface for the Memory & Soul Passport (MSP) System.
    Ensures a unified contract for memory persistence and state management.
    """

    @abstractmethod
    def set_active_state(self, slot: str, data: Any) -> None:
        """Broadcasts and persists a system's active state."""
        pass

    @abstractmethod
    def get_active_state(self, slot: str) -> Optional[Dict[str, Any]]:
        """Retrieves a system's last known active state."""
        pass

    @abstractmethod
    def latch_state(self, bus_id: str, snapshot: Dict[str, Any]) -> None:
        """Latches state from the Resonance Bus for subsequent archival."""
        pass

    @abstractmethod
    def log_episodic_event(self, event_data: Dict[str, Any]) -> str:
        """Logs a single episodic event and returns its internal ID."""
        pass

    @abstractmethod
    def query_memories(self, query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Queries the collective memory pool based on provided parameters."""
        pass
