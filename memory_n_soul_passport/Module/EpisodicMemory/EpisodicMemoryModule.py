from typing import Dict, Any, Optional, List
from .Node.JournalNode import JournalNode
from datetime import datetime

class EpisodicMemoryModule:
    """
    Subconscious module that manages the lifecycle of episodic memories.
    Handles speaker identification and multi-format consolidation.
    """
    
    def __init__(self, config: Dict[str, Any], sensory_module: Any = None):
        self.config = config
        self.journal = JournalNode(config)
        self.sensory_module = sensory_module
        
        # Resolve Module Parameters
        mod_cfg = config.get("module_definitions", {}).get("episodic_memory_module", {})
        self.params = mod_cfg.get("parameters", {})
        
        self.speaker_id_active = self.params.get("speaker_id_enabled", True)
        self.default_ri = self.params.get("default_resonance", 0.5)
        
    def consolidate_interaction(self, episode_data: Dict[str, Any], system_meta: Dict[str, Any], user_registry: Any) -> str:
        """
        Standard v9.4.0 consolidation flow.
        """
        episode_id = episode_data.get("episode_id")
        timestamp = episode_data.get("timestamp") or datetime.now().isoformat()
        
        # 1. Speaker Identification
        turn_user = episode_data.get("turn_user") or episode_data.get("turn_1", {})
        
        if self.speaker_id_active and user_registry:
            speaker_info = user_registry.identify_speaker(turn_user.get("raw_text", ""))
            
            if not turn_user.get("user_id") or turn_user.get("user_id") == "unknown":
                turn_user["user_id"] = speaker_info["user_id"]
                turn_user["username"] = speaker_info["username"]
            
            if speaker_info["user_id"] != "unknown":
                user_registry.increment_interaction(speaker_info["user_id"])

        # 2. Construction
        full_episode = {
            "episode_id": episode_id,
            "timestamp": timestamp,
            "session_id": episode_data.get("session_id"),
            "compression_meta": system_meta.get("compression_meta", {}),
            "situation_context": episode_data.get("situation_context"),
            "turn_user": turn_user,
            "turn_llm": episode_data.get("turn_llm") or episode_data.get("turn_ai", {}),
            "state_snapshot": episode_data.get("state_snapshot", {})
        }
        
        # RAG-Optimized User Version
        user_episode = {
            "episode_id": episode_id,
            "timestamp": timestamp,
            "turn_user": turn_user,
            "metrics": {
                "resonance_index": full_episode["state_snapshot"].get("Resonance_index", self.default_ri)
            }
        }
        
        # Audit-Optimized LLM Version
        llm_episode = {
             "episode_id": episode_id,
             "timestamp": timestamp,
             "turn_llm": full_episode["turn_llm"],
             "confidence": full_episode["turn_llm"].get("confidence", 0.0)
        }

        # 3. Persistence
        self.journal.write_split_episodes(episode_id, full_episode, user_episode, llm_episode)
        
        # 3.5 Sensory Sidecar (Refactored)
        if self.sensory_module:
            qualia = full_episode["state_snapshot"].get("qualia")
            if qualia:
                self.sensory_module.record_perception(qualia, episode_id)
        
        # 4. Logging
        summary = {
            "episode_id": episode_id,
            "timestamp": timestamp,
            "summary": episode_data.get("summary", ""),
            "ri": user_episode["metrics"]["resonance_index"]
        }
        self.journal.append_to_log(summary)
        
        return episode_id
