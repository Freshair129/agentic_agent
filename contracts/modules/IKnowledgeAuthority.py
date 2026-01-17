from abc import ABC, abstractmethod
from typing import Dict, Any

class IKnowledgeAuthority(ABC):
    """Contract for Genesis Knowledge System (GKS)"""
    
    @abstractmethod
    def verify_truth(self, statement: str) -> Dict[str, Any]:
        """Check statement against Master Blocks."""
        pass
        
    @abstractmethod
    def get_strategic_guidance(self, context: Dict) -> str:
        """Get high-level strategy (NexusMode)."""
        pass
