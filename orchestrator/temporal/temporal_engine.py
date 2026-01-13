from typing import Dict, Any, Optional
import datetime

class TemporalEngine:
    """
    Temporal Engine (v9.3.2GT)
    Manages Time Perception (SOT) and Narrative Logic (Pulsing).
    Now integrated with GKS 'Time' Block.
    """
    def __init__(self, gks_loader=None):
        self.loader = gks_loader
        self.version = "9.3.2GT"

    def process_temporal_sot(self, context_data: Dict[str, Any]) -> str:
        """
        Node SOT: Returns standard time anchor string.
        """
        # 1. Get Policy
        policy_text = "Standard Time"
        if self.loader:
            block = self.loader.get_genesis_block('time')
            if block:
                sot_config = block.get('genesis_block', {}).get('node_sot', {})
                policies = sot_config.get('policies', [])
                if policies:
                    policy_text = policies[0].get('rule', 'Standard Time')

        # 2. Calculate Current Time
        # In a real system, this would handle complex offsets.
        now = datetime.datetime.now().isoformat()
        return f"[TIME_SOT: {now} | Policy: {policy_text}]"

    def get_narrative_pulse(self, sentiment_score: float) -> str:
        """
        Determines the 'beat' of the conversation based on sentiment/energy.
        """
        if not self.loader:
            return "Pulse: Neutral"
            
        block = self.loader.get_genesis_block('time')
        if not block:
             return "Pulse: Neutral (No Block)"
             
        beats = block.get('genesis_block', {}).get('narrative_pulsing', {}).get('beats', [])
        
        # Simple Logic Mapping
        selected_beat = None
        if sentiment_score > 0.5:
             selected_beat = next((b for b in beats if b['name'] == 'Upbeat'), None)
        elif sentiment_score < -0.5:
             selected_beat = next((b for b in beats if b['name'] == 'Downbeat'), None)
        else:
             selected_beat = next((b for b in beats if b['name'] == 'Steady'), None)
             
        if selected_beat:
            return f"Pulse: {selected_beat['name']} ({selected_beat['action']})"
            
        return "Pulse: Steady"
