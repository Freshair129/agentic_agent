from abc import ABC, abstractmethod
from typing import Dict, Any, Callable

class IResonanceBus(ABC):
    """
    Interface for the Resonance Bus.
    Manages high-speed communication between system components.
    """

    @abstractmethod
    def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribes to a channel."""
        pass

    @abstractmethod
    def publish(self, channel: str, payload: Dict[str, Any]) -> None:
        """Publishes a payload to a channel."""
        pass

    @abstractmethod
    def initialize_session(self, session_id: str) -> None:
        """Initializes the bus for a new session."""
        pass
