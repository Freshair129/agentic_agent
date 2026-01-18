from typing import Dict, Any, Optional, List
from .Node.JournalNode import JournalNode
from datetime import datetime
import sys
from pathlib import Path

# Add contracts path for import
sys.path.append(str(Path(__file__).parent.parent.parent.parent.resolve()))
from contracts.modules.IMemoryRetrieval import IMemoryRetrieval
from contracts.modules.IMemoryStorage import IMemoryStorage

class EpisodicMemoryModule(IMemoryRetrieval, IMemoryStorage):
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
        Original consolidation flow, now serving as the core of store_episode.
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
                "resonance_index": full_episode["state_snapshot"].get("resonance_index") or full_episode["state_snapshot"].get("Resonance_index", self.default_ri)
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

    # --- IMemoryStorage Implementation ---

    def store_episode(self, episode_data: Dict[str, Any]) -> bool:
        """
        Standard store operation. For v9.4.3, we expect consolidated data.
        """
        try:
            # For now, we reuse consolidate_interaction logic
            # In a full refactor, this would be the primary entry point
            self.consolidate_interaction(episode_data, {}, None)
            return True
        except Exception as e:
            print(f"[EpisodicModule] ❌ Store Error: {e}")
            return False

    def update_semantic_node(self, node_id: str, updates: Dict[str, Any]) -> bool:
        """Not applicable to Episodic Module."""
        return False

    def archive_session(self, session_id: str) -> str:
        """Logic for session archiving (to be implemented)."""
        return f"ARCHIVE_{session_id}"

    # --- IMemoryRetrieval Implementation ---

    def retrieve_by_tags(self, tags: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves episodes matching semantic tags from journal log.
        """
        summaries = self.journal.read_log()
        tags_lower = [t.lower() for t in tags]
        matches = []
        
        for summary in summaries:
            # We assume tags are stored in summary for fast lookup
            # If not, we'd need to load full episodes (slow)
            ep_tags = [t.lower() for t in summary.get("tags", [])]
            if any(tag in ep_tags for tag in tags_lower):
                full_ep = self.journal.read_full_episode(summary["episode_id"])
                if full_ep:
                    matches.append(full_ep)
            
            if len(matches) >= limit:
                break
        return matches

    def retrieve_by_resonance(self, min_ri: float, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves high-salience memories.
        """
        summaries = self.journal.read_log()
        matches = []
        
        # Sort log by RI descending
        sorted_summaries = sorted(summaries, key=lambda x: x.get("ri", 0.0), reverse=True)
        
        for summary in sorted_summaries:
            if summary.get("ri", 0.0) >= min_ri:
                full_ep = self.journal.read_full_episode(summary["episode_id"])
                if full_ep:
                    matches.append(full_ep)
            
            if len(matches) >= limit:
                break
        return matches

    def retrieve_by_state_similarity(self, state_snapshot: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves memories with similar biological/emotional states.
        Uses Phase 2 snapshot schema (Resonance, Qualia, Texture).
        """
        summaries = self.journal.read_log()
        
        target_ri = state_snapshot.get("resonance_index") or state_snapshot.get("Resonance_index", 0.5)
        target_int = state_snapshot.get("qualia", {}).get("intensity", 0.3)
        target_tex = state_snapshot.get("resonance_texture", {}) # Dict[str, float]
        
        scored_episodes = []

        for summary in summaries:
            full_ep = self.journal.read_full_episode(summary["episode_id"])
            if not full_ep: continue
            
            curr_snap = full_ep.get("state_snapshot", {})
            curr_ri = curr_snap.get("resonance_index") or curr_snap.get("Resonance_index", 0.5)
            curr_int = curr_snap.get("qualia", {}).get("intensity", 0.3)
            curr_tex = curr_snap.get("resonance_texture", {})

            # 1. Scalar Delta (RI + Intensity)
            delta_scalar = abs(target_ri - curr_ri) + abs(target_int - curr_int)
            
            # 2. Texture Distance (Manhattan)
            delta_tex = 0.0
            for k in ["stress", "warmth", "clarity", "drive", "calm"]:
                delta_tex += abs(target_tex.get(k, 0) - curr_tex.get(k, 0))
            
            # Total Score (Lower is better)
            total_score = delta_scalar + (delta_tex * 0.5)
            
            # Valid match candidate
            scored_episodes.append((total_score, full_ep))

        # Sort by score ascending (closest matches first)
        scored_episodes.sort(key=lambda x: x[0])
        
        return [x[1] for x in scored_episodes[:limit]]

