"""
Semantic Memory Buffer
Temporary session-scoped knowledge storage for conflict detection
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class SemanticMemoryBuffer:
    """
    Session-scoped temporary knowledge store.
    Holds unverified discoveries until end-of-session commit or conflict resolution.
    """
    
    def __init__(self, user_id: str, session_id: str):
        """
        Initialize buffer for a specific user and session
        
        Args:
            user_id: User ID (e.g., U_001)
            session_id: Current session ID
        """
        self.user_id = user_id
        self.session_id = session_id
        self.discoveries: List[Dict] = []
        self.verified_facts: List[str] = []  # fact_ids that passed conflict check
    
    def add_discovery(
        self, 
        statement: str, 
        category: str,
        confidence: float,
        turn_id: str,
        evidence_text: str = ""
    ):
        """
        Add unverified discovery from current session
        
        Args:
            statement: The fact discovered (e.g., "อยากกินกุ้งเผา")
            category: Category (health, preference, memory, skill, etc.)
            confidence: LLM confidence in this fact (0.0-1.0)
            turn_id: Turn where this was discovered
            evidence_text: Supporting text snippet
        """
        discovery = {
            "statement": statement,
            "category": category,
            "confidence": confidence,
            "turn_id": turn_id,
            "evidence_text": evidence_text,
            "timestamp": datetime.now().isoformat(),
            "status": "unverified",  # unverified, verified, conflicted
            "conflict_resolution": None
        }
        self.discoveries.append(discovery)
    
    def get_discoveries_by_category(self, category: str) -> List[Dict]:
        """Get all discoveries in a category"""
        return [d for d in self.discoveries if d["category"] == category]
    
    def get_all_discoveries(self) -> List[Dict]:
        """Get all discoveries from current session"""
        return self.discoveries.copy()
    
    def mark_as_verified(self, statement: str):
        """Mark a discovery as verified (no conflict)"""
        for discovery in self.discoveries:
            if discovery["statement"] == statement:
                discovery["status"] = "verified"
                self.verified_facts.append(discovery["turn_id"])
    
    def mark_as_conflicted(self, statement: str, resolution: str):
        """Mark a discovery as conflicted with resolution note"""
        for discovery in self.discoveries:
            if discovery["statement"] == statement:
                discovery["status"] = "conflicted"
                discovery["conflict_resolution"] = resolution
    
    def clear(self):
        """Clear buffer (e.g., at session end)"""
        self.discoveries = []
        self.verified_facts = []
    
    def to_dict(self) -> Dict:
        """Export buffer state"""
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "discovery_count": len(self.discoveries),
            "discoveries": self.discoveries,
            "verified_facts": self.verified_facts
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SemanticMemoryBuffer':
        """Restore buffer from saved state"""
        buffer = cls(data["user_id"], data["session_id"])
        buffer.discoveries = data.get("discoveries", [])
        buffer.verified_facts = data.get("verified_facts", [])
        return buffer
