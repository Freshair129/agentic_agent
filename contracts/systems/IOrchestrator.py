from abc import ABC, abstractmethod
from typing import Dict, Any

class IOrchestrator(ABC):
    """Contract for the Main EVA Orchestrator"""
    
    @abstractmethod
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Main entry point for user interaction."""
        pass
