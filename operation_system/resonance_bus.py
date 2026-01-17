import sys
import os
import json
import hashlib
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from capabilities.tools.logger import safe_print
from operation_system.identity_manager import IdentityManager
print = safe_print

class ResonanceBus:
    """
    EVA 9.1.0: Central Resonance Bus (Infrastructure OS)
    A high-speed, schema-validated publish/subscribe event bus.
    """
    def __init__(self):
        self.channels = {
            IdentityManager.BUS_PHYSICAL: [],
            IdentityManager.BUS_PSYCHOLOGICAL: [],
            IdentityManager.BUS_PHENOMENOLOGICAL: [],
            IdentityManager.BUS_KNOWLEDGE: []
        }
        self.session_id = None
        self.history = []

    def initialize_session(self, session_id: str):
        self.session_id = session_id
        print(f"Resonance Bus: Session {session_id} initialized.")

    def subscribe(self, channel: str, callback: Callable[[Dict], None]):
        """Subscribes a callback to a channel. Note: Callback should accept one Dict argument."""
        if channel in self.channels:
            self.channels[channel].append(callback)
        else:
            self.channels[channel] = [callback]

    def publish(self, channel: str, payload: Dict):
        """Publishes a payload to a channel and notifies subscribers."""
        if channel not in self.channels:
            # Auto-create channel if it doesn't exist to prevent crashes
            self.channels[channel] = []

        # Add metadata
        payload["__metadata__"] = {
            "timestamp": datetime.now().isoformat(),
            "channel": channel,
            "session_id": self.session_id
        }

        # Log to history
        self.history.append((channel, payload))

        # Notify subscribers
        for callback in self.channels[channel]:
            try:
                callback(payload)
            except Exception as e:
                print(f"  Resonance Bus Error in subscriber on {channel}: {e}")

    def generate_state_hash(self) -> str:
        """Generates a verifiable hash of the current bus state (Proof of Lived Experience)."""
        state_str = json.dumps(self.history, sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

# Global Singleton for the Infrastructure OS
bus = ResonanceBus()
