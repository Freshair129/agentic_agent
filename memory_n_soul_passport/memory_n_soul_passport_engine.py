"""

EVA 8.1.0: MSP (Memory & Soul Passport) Engine with Local Filesystem Persistence

Manages episodic memory using JSONL format + individual JSON files



Storage Structure:

    consciousness/

    ├── 01_Episodic_memory/

    │   ├── episodic_log.jsonl       # Append-only log (fast retrieval)

    │   ├── episodic_index.jsonl     # Index with metadata

    │   └── episodes/

    │       ├── ep_260101_abc123.json

    │       └── ep_260101_def456.json

    │

    ├── 02_Semantic_memory/

    │   └── semantic_concepts.json

    │

    └── 10_state/

        └── turn_cache.json



Advantages:

    - ✅ Persistent (survives program restart)

    - ✅ Fast (JSONL + in-memory cache)

    - ✅ Simple (no database required)

    - ✅ Human-readable (JSON format)

    - ✅ Upgradeable to MongoDB later

"""



import sys
from pathlib import Path

# Add root to path for tools and engines
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from capabilities.tools.logger import safe_print
from operation_system.identity_manager import IdentityManager
from resonance_memory_system.rms import RMSEngineV6
from memory_n_soul_passport.user_registry_manager import UserRegistryManager

import json
import hashlib
import yaml
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math
import re

# v9.4.0 Module Delegation
from .Module.EpisodicMemory import EpisodicMemoryModule
from .Module.SemanticMemory import SemanticMemoryModule
from .Module.SensoryMemory import SensoryMemoryModule

class MSP:

    """

    MSP (Memory & Soul Passport) Engine with Local Filesystem Persistence



    Provides persistent storage and retrieval for:

    - Episodic Memory (episodes, events, conversations)

    - Semantic Memory (concepts, relationships)

    - Turn Cache (recent conversation summaries)



    Storage Format:

    - episodic_log.jsonl: Append-only log (one episode per line)

    - episodes/*.json: Individual episode files (detailed storage)

    - In-memory cache: Recent episodes for fast access

    """



    def __init__(

        self,

        root_path: Optional[str] = None,

        cache_size: int = 50

    ):

        """

        Initialize MSP Engine (v9.4.0 Resonance Refactored)

        """

        # Resolve Root Path (Agent Root)

        # The engine file is at agent/memory_n_soul_passport/memory_n_soul_passport_engine.py
        # So parent.parent is agent/
        self.root_path = Path(__file__).parent.parent.resolve()
        
        # Load Configuration
        config_path = Path(__file__).parent / "configs" / "MSP_configs.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            safe_print(f"[MSP] ⚠️ Config Missing: {config_path}")
            self.config = {}

        # Initialize Delegation Modules
        self.sensory_module  = SensoryMemoryModule(self.config)
        self.episodic_module = EpisodicMemoryModule(self.config, self.sensory_module)
        self.semantic_module = SemanticMemoryModule(self.config)

        # Path Setup (Driven by Config)
        cfg_storage = self.config.get("storage_structure", {})
        self.episodic_dir = self.root_path / cfg_storage.get("episodic", {}).get("path", "consciousness/episodic_memory")
        self.semantic_dir = self.root_path / cfg_storage.get("semantic", {}).get("path", "consciousness/semantic_memory")
        self.sensory_dir  = self.root_path / cfg_storage.get("sensory", {}).get("path", "consciousness/sensory_memory")
        self.state_dir    = self.root_path / self.config.get("filesystem_structure", {}).get("system_state", {}).get("root", "system_state")
        self.context_dir  = self.root_path / cfg_storage.get("context", {}).get("context_storage", "memory/context_storage")

        # Create Core Structures
        for d in [self.episodic_dir, self.semantic_dir, self.sensory_dir, self.state_dir, self.context_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Legacy Support / Internal State
        self.cache_size = cache_size
        self._episode_cache: List[Dict] = []
        self._cache_loaded = False
        self._active_state_cache: Dict[str, Any] = {}
        
        # Identity and Registry
        self.identity_config_file = self.root_path / "consciousness/indexes/identity_config.json"
        self.system_registry_file = self.root_path / "consciousness/indexes/system_registry.json"
        
        self.identity_config = {}
        if self.identity_config_file.exists():
            try:
                with open(self.identity_config_file, 'r', encoding='utf-8') as f:
                    self.identity_config = json.load(f)
            except: pass
            
        self.system_registry = {}
        if self.system_registry_file.exists():
            try:
                with open(self.system_registry_file, 'r', encoding='utf-8') as f:
                    self.system_registry = json.load(f)
            except: pass
        
        # Registry Managers
        registry_path = self.root_path / "memory" / "user_registry.json"
        self.user_registry = UserRegistryManager(str(registry_path))
        
        # V9.1.0 RMS Bridge (Temporary till full refactor)
        self.rms = RMSEngineV6(config={}) # Will load from system later
        self.storage_path = self.context_dir / "context_storage.json"

        # Legacy filenames for compatibility with existing methods in this monolithic file
        ep_cfg = self.config.get("storage_structure", {}).get("episodic", {})
        ep_formats = ep_cfg.get("formats", {})
        log_name = ep_formats.get("stream_log", {}).get("filename", "episodic_log.jsonl")
        self.episodic_log = self.episodic_dir / log_name
        self.episodes_user_dir = self.episodic_dir / "episodes_user"
        self.episodes_llm_dir = self.episodic_dir / "episodes_ai"
        self.active_state_dir = self.state_dir / "active_state"
        
        # [NEW] Index & Counter Reference (Unified v9.4.0)
        self.memory_index_file = self.root_path / "consciousness/indexes/memory_index.json"
        self.consciousness_history = self.root_path / "consciousness/indexes/consciousness_history.jsonl"
        self.episode_counter_file = self.root_path / "consciousness/indexes/episode_counter.json"
        self.memory_index_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure subdirs exist
        self.episodes_user_dir.mkdir(parents=True, exist_ok=True)
        self.episodes_llm_dir.mkdir(parents=True, exist_ok=True)
        self.active_state_dir.mkdir(parents=True, exist_ok=True)

        safe_print(f"[MSP] ✅ Subconscious Facade Initialized (v9.4.0)")

    # ============================================================
    # 9.1.0 BRIDGE METHODS
    # ============================================================

    def process_resonance(self, eva_matrix: Dict, rim_output: Dict, reflex_state: Dict, ri_total: float = 0.0) -> Dict:
        """Generates an affective memory snapshot using RMSv6 logic."""
        # return self.rms.process(eva_matrix, rim_output, reflex_state, ri_total)
        pass # Placeholder

    def save_turn_context(self, context_data: Dict[str, Any]):
        """Persists turn-to-turn context for CIM continuity (9.1.0 style)."""
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(context_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # safe_print(f"  ⚠️ MSP Error saving context: {e}")
            print(f"  ⚠️ MSP Error saving context: {e}")

    def load_turn_context(self) -> Dict[str, Any]:
        """Loads the last turn-to-turn context (9.1.0 style)."""
        if not self.storage_path.exists():
            return {}
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"  ⚠️ MSP Error loading context: {e}")
            return {}

    def get_context_identity_params(self) -> Dict[str, Any]:
        """
        Returns parameters for generating a context_id:
        - session_seq: Current session sequence from registry
        - episodic_id: Predicted next episodic_id
        """
        counters = self.system_registry.get("counters", {})
        session_seq = counters.get("session_seq", 0)
        
        # Predict next episode number
        next_ep_num = counters.get("current_episode", 0) + 1
        persona_code = self.identity_config.get("persona", {}).get("persona_code", "EVA")
        
        # RIS UPDATE: Use Config-Driven Naming Pattern
        naming_cfg = self.config.get("naming_rules", {}).get("episode_id", {})
        ep_pattern = naming_cfg.get("pattern", "{PERSONA}_EP{number:02d}")
        
        predicted_ep_id = IdentityManager.generate_episode_id(persona_code, next_ep_num, pattern=ep_pattern)
        
        return {
            "session_seq": session_seq,
            "episodic_id": predicted_ep_id
        }

    def get_recent_turns(self, limit: int = 5, timeout_ms: int = 100) -> List[Dict]:
        """Alias for history retrieval as expected by CIM."""
        # Map to get_recent_history
        history = self.get_recent_history(max_turns=limit)
        return history

    def query_recent_episodes(self, limit: int = 5, **kwargs) -> List[Dict]:
        """Alias for RAG queries."""
        max_age = kwargs.get('within_days', 30)
        return self.query_recent(limit=limit, max_age_days=max_age)

    # AgenticRAG mapping (proxies to recent for MVP)
    def query_narrative_chain(self, tags: List[str], limit: int = 3) -> List[Dict]:
        return self.query_recent(limit=limit)

    def query_by_salience(self, tags: List[str], min_ri: float = 0.7, limit: int = 3) -> List[Dict]:
        return self.query_by_ri(min_ri=min_ri, max_results=limit)

    def query_sensory_memories(self, tags: List[str], min_qualia_intensity: float = 0.6, limit: int = 3) -> List[Dict]:
        return self.query_by_qualia(min_intensity=min_qualia_intensity, max_results=limit)

    def query_semantic_patterns(self, tags: List[str], pattern_type: str = "structural", limit: int = 3) -> List[Dict]:
        return self.query_by_tags(tags=tags, limit=limit)

    def query_reflections(self, tags: List[str], reflection_type: str = "self_understanding", limit: int = 3) -> List[Dict]:
        return self.query_recent(limit=limit)



    # ============================================================

    # EPISODIC MEMORY - READ OPERATIONS

    # ============================================================



    def _load_cache(self):

        """Load recent episodes into memory cache"""

        if self._cache_loaded:

            return



        episodes = self._read_all_episodes_from_log()

        self._episode_cache = episodes[-self.cache_size:]

        self._cache_loaded = True

        print(f"[MSP] Loaded {len(self._episode_cache)} episodes into cache")



    def _read_all_episodes_from_log(self) -> List[Dict]:

        """Read all episodes from JSONL log file"""

        if not self.episodic_log.exists():

            return []



        episodes = []
        with open(self.episodic_log, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        episode = json.loads(line)
                        if isinstance(episode, dict):
                            episodes.append(episode)
                        else:
                            print(f"[MSP] Warning: Skipped non-dict entry in episodic_log: {type(episode)}")
                    except json.JSONDecodeError as e:
                        print(f"[MSP] Warning: Failed to parse episode: {e}")
                        continue
        return episodes



    def _read_episode_file(self, episode_id: str) -> Optional[Dict]:

        """Read individual episode file (redirects to get_full_episode)"""

        # Use new split storage

        return self.get_full_episode(episode_id)



    def _read_user_episodes(self) -> List[Dict]:

        """

        Read all user episodes (lightweight, fast)

        Use this for RAG queries that don't need LLM responses

        """

        user_episodes = []

        for user_file in self.episodes_user_dir.glob("*_user.json"):

            try:

                with open(user_file, 'r', encoding='utf-8') as f:

                    user_episodes.append(json.load(f))

            except Exception as e:

                print(f"[MSP] Warning: Failed to parse user episode {user_file}: {e}")

        return user_episodes



    def query_by_tags(

        self,

        tags: List[str],

        limit: int = 5,

        min_ri: float = 0.0,

        **kwargs

    ) -> List[Dict]:

        """

        Query episodes by semantic tags



        Args:

            tags: List of tags to search for

            limit: Maximum number of results

            min_ri: Minimum Resonance Index threshold

        """

        max_results = limit

        self._load_cache()



        # Search in cache first (fast)

        matches = []

        tags_lower = [t.lower() for t in tags]



        for ep in self._episode_cache:

            # Schema V2: tags are in turn_1.semantic_frames

            # Legacy: tags are at root level

            if "turn_1" in ep:

                ep_tags = [t.lower() for t in ep.get("turn_1", {}).get("semantic_frames", [])]

            else:

                ep_tags = [t.lower() for t in ep.get("tags", [])]



            if any(tag in ep_tags for tag in tags_lower):

                # Schema V2: RI in state_snapshot.Resonance_index

                # Legacy: resonance_index at root

                if "state_snapshot" in ep:

                    ri = ep.get("state_snapshot", {}).get("Resonance_index", 0)

                else:

                    ri = ep.get("resonance_index", 0)



                if ri >= min_ri:

                    matches.append(ep)



        # If not enough matches, search user episodes (fast, no LLM data)

        if len(matches) < max_results:

            user_episodes = self._read_user_episodes()

            for ep in user_episodes:

                if ep in matches:

                    continue



                # Schema V2: tags in turn_1.semantic_frames

                ep_tags = [t.lower() for t in ep.get("turn_1", {}).get("semantic_frames", [])]



                if any(tag in ep_tags for tag in tags_lower):

                    # Schema V2: RI in state_snapshot.Resonance_index

                    ri = ep.get("state_snapshot", {}).get("Resonance_index", 0)



                    if ri >= min_ri:

                        matches.append(ep)



        # Sort by RI (descending)

        def get_ri(ep):

            if "state_snapshot" in ep:

                return ep.get("state_snapshot", {}).get("Resonance_index", 0)

            return ep.get("resonance_index", 0)



        matches.sort(key=get_ri, reverse=True)

        return matches[:max_results]



    def query_by_physio_state(

        self,

        physio_query: Dict[str, float],

        similarity_threshold: float = 0.7,

        limit: int = 3,

        **kwargs

    ) -> List[Dict]:

        """

        Query episodes by physiological similarity (Emotion Stream)



        Args:

            physio_query: Current physiological state

            similarity_threshold: Minimum cosine similarity (0.0-1.0)

            limit: Maximum number of results

        """

        max_results = limit

        self._load_cache()

        all_episodes = self._read_all_episodes_from_log()



        matches = []

        for ep in all_episodes:

            # Schema V2: physio state in state_snapshot.Endocrine

            # Legacy: physio_state at root

            if "state_snapshot" in ep:

                physio_state = ep.get("state_snapshot", {}).get("Endocrine", {})

            else:

                physio_state = ep.get("physio_state", {})



            if not physio_state:

                continue



            similarity = self._cosine_similarity(physio_query, physio_state)



            if similarity >= similarity_threshold:

                ep_copy = ep.copy()

                ep_copy["physio_similarity"] = similarity

                matches.append(ep_copy)



        # Sort by similarity (descending)

        matches.sort(key=lambda x: x["physio_similarity"], reverse=True)

        return matches[:max_results]



    def query_by_ri(

        self,

        min_ri: float = 0.70,

        max_results: int = 3

    ) -> List[Dict]:

        """

        Query high-salience episodes (Salience Stream)



        Args:

            min_ri: Minimum Resonance Index

            max_results: Maximum results



        Returns:

            High-impact episodes

        """

        self._load_cache()

        all_episodes = self._read_all_episodes_from_log()



        # Schema V2 or Legacy format

        def get_ri(ep):

            if "state_snapshot" in ep:

                return ep.get("state_snapshot", {}).get("Resonance_index", 0)

            return ep.get("resonance_index", 0)



        matches = [ep for ep in all_episodes if get_ri(ep) >= min_ri]

        matches.sort(key=get_ri, reverse=True)

        return matches[:max_results]



    def query_by_qualia(

        self,

        min_intensity: float = 0.6,

        max_results: int = 3

    ) -> List[Dict]:

        """

        Query sensory-rich episodes (Sensory Stream)



        Args:

            min_intensity: Minimum qualia intensity

            max_results: Maximum results



        Returns:

            Sensory-rich episodes

        """

        self._load_cache()

        all_episodes = self._read_all_episodes_from_log()



        # Schema V2 or Legacy format

        def get_qualia_intensity(ep):

            if "state_snapshot" in ep:

                return ep.get("state_snapshot", {}).get("qualia", {}).get("intensity", 0)

            return ep.get("qualia", {}).get("intensity", 0)



        matches = [

            ep for ep in all_episodes

            if get_qualia_intensity(ep) >= min_intensity

        ]

        matches.sort(key=get_qualia_intensity, reverse=True)

        return matches[:max_results]



    def query_recent(

        self,

        limit: int = 5,

        max_age_days: int = 30,

        **kwargs

    ) -> List[Dict]:

        """

        Query recent episodes (Temporal Stream)



        Args:

            limit: Maximum results

            max_age_days: Maximum age in days

        """

        max_results = limit

        self._load_cache()

        all_episodes = self._read_all_episodes_from_log()



        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        matches = []



        for ep in all_episodes:

            timestamp_str = ep.get("timestamp", "")

            if not timestamp_str:

                continue



            try:

                ep_date = datetime.fromisoformat(timestamp_str)

                if ep_date >= cutoff_date:

                    days_ago = (datetime.now() - ep_date).days

                    recency_score = self._exponential_decay(days_ago, halflife=30)



                    ep_copy = ep.copy()

                    ep_copy["recency_score"] = recency_score

                    matches.append(ep_copy)

            except:

                continue
        # Sort by recency
        matches.sort(key=lambda x: x.get("recency_score", 0), reverse=True)
        return matches[:max_results]

    # ============================================================
    # EPISODIC MEMORY - WRITE OPERATIONS
    # ============================================================

    def log_internal_thought(self, thought_data: Dict[str, Any]) -> bool:
        """
        Log an internal thought to episodic memory.

        Args:
            thought_data: Dict containing:
                - thought: str
                - timestamp: str (ISO format)
                - emotion: str
                - arousal: float
                - thought_number: int

        Returns:
            True if logged successfully
        """
        try:
            # Create thought entry
            entry = {
                "type": "internal_thought",
                "content": thought_data["thought"],
                "timestamp": thought_data["timestamp"],
                "metadata": {
                    "emotion": thought_data.get("emotion", "unknown"),
                    "arousal": thought_data.get("arousal", 0.5),
                    "thought_number": thought_data.get("thought_number", 0)
                }
            }

            # Log to internal thoughts file
            thoughts_file = self.episodic_dir / "internal_thoughts.jsonl"
            # Directory should already exist from __init__, but safe to ensure
            thoughts_file.parent.mkdir(parents=True, exist_ok=True)

            with open(thoughts_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')

            return True

        except Exception as e:
            print(f"[MSP] Error logging internal thought: {e}")
            return False

    def write_episode(
        self,
        episode_data: Dict[str, Any],
        persist: bool = True
    ) -> str:
        """
        Consolidates and writes a new episode by delegating to EpisodicMemoryModule.
        """
        if not persist:
            safe_print(f"[MSP] ⚠️ Transient Mode: Episode {episode_data.get('episode_id')} NOT written to disk.")
            return episode_data.get("episode_id", "EP_TRANSIENT")

        # 1. ID Generation (Keep in Facade/Identity Manager for global consistency)
        persona_code = self.identity_config.get("persona", {}).get("persona_code", "EVA")
        episode_num = self._increment_episode_counter()
        episode_id = IdentityManager.generate_episode_id(persona_code, episode_num)
        episode_data["episode_id"] = episode_id

        # 2. Metadata Preparation
        counters = self.system_registry.get("counters", {})
        system_meta = {
            "compression_meta": {
                "session_seq": counters.get("session_seq", 0),
                "core_seq": counters.get("core_seq", 0),
                "sphere_seq": counters.get("sphere_seq", 0)
            }
        }

        # 3. Delegate Consolidation & Persistence
        try:
            self.episodic_module.consolidate_interaction(episode_data, system_meta, self.user_registry)
        except Exception as e:
            safe_print(f"[MSP] ❌ Error delegating episode write: {e}")
            return episode_id

        # 4. Update Facade-level Indexes (for compatibility)
        full_ep = {**episode_data, "episode_id": episode_id} # Simplified for index
        self._episode_cache.append(full_ep)
        if len(self._episode_cache) > self.cache_size:
            self._episode_cache.pop(0)
            
        self._update_memory_index(full_ep)

        safe_print(f"[MSP] ✓ Episode Consolidated: {episode_id}")
        return episode_id



    def get_full_episode(self, episode_id: str) -> Optional[Dict]:

        """

        Get full episode by merging user + llm files



        Args:

            episode_id: Episode ID



        Returns:

            Full episode dict or None if not found

        """

        user_file = self.episodes_user_dir / f"{episode_id}_user.json"

        llm_file = self.episodes_llm_dir / f"{episode_id}_llm.json"



        if not user_file.exists():

            print(f"[MSP] Warning: User file not found for {episode_id}")

            return None



        try:

            # Load user data (always needed)

            with open(user_file, 'r', encoding='utf-8') as f:

                user_data = json.load(f)



            # Load LLM data (if exists)

            if llm_file.exists():

                with open(llm_file, 'r', encoding='utf-8') as f:

                    llm_data = json.load(f)



                # Merge state_snapshot

                if "state_snapshot" in llm_data:

                    if "state_snapshot" not in user_data:

                        user_data["state_snapshot"] = {}

                    user_data["state_snapshot"].update(llm_data["state_snapshot"])



                # Add turn_2

                user_data["turn_llm"] = llm_data.get("turn_llm") or llm_data.get("turn_2")



            return user_data



        except Exception as e:

            print(f"[MSP] Error loading full episode {episode_id}: {e}")

            return None



    # ============================================================

    # SEMANTIC MEMORY OPERATIONS

    # ============================================================



    def _load_semantic_concepts(self):
        """Delegates semantic loading to SemanticMemoryModule."""
        # For compatibility, initializing fallback if module fails
        if not hasattr(self, "_semantic_concepts"):
             self._semantic_concepts = {}
        pass

    def _save_semantic_concepts(self):
        """Delegates semantic saving to SemanticMemoryModule."""
        pass



    def get_semantic_concepts(

        self,

        tags: List[str]

    ) -> Dict[str, Any]:

        """

        Get related semantic concepts



        Args:

            tags: Input tags



        Returns:

            Related concepts

        """

        related = {}

        for tag in tags:

            if tag in self._semantic_concepts:

                related[tag] = self._semantic_concepts[tag]

        return related



    # ============================================================

    # COMPRESSION COUNTER OPERATIONS
    # SYSTEM REGISTRY (COUNTERS & DYNAMIC STATE)
    # ============================================================

    def _load_system_registry(self) -> Dict[str, Any]:
        """Load unified system registry from 09_state/system_registry.json"""
        if not self.system_registry_file.exists():
            persona_code = self._get_persona_code()
            default_registry = {
                "counters": {
                    "current_episode": 0,
                    "session_seq": 1,
                    "core_seq": 0,
                    "sphere_seq": 0,
                    "total_sessions": 1
                },
                "persona": {
                    "persona_code": persona_code
                },
                "last_update": datetime.now().isoformat()
            }
            self._save_system_registry(default_registry)
            return default_registry

        try:
            with open(self.system_registry_file, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except Exception as e:
            print(f"[MSP] Error loading system registry: {e}")
            return {
                "counters": {"current_episode": 0, "session_seq": 1, "core_seq": 0, "sphere_seq": 0, "total_sessions": 1},
                "persona": {"persona_code": "EVA"},
                "last_update": datetime.now().isoformat()
            }

    def _save_system_registry(self, registry: Dict[str, Any] = None):
        """Save system registry to file"""
        if registry is None:
            registry = self.system_registry
        try:
            registry["last_update"] = datetime.now().isoformat()
            with open(self.system_registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[MSP] Error saving system registry: {e}")

    def start_new_session(self) -> Dict[str, int]:
        """
        Manually start a new session (called by Orchestrator on /start).
        Increment compression counters according to hierarchy:
        - Increment session_seq
        - If session_seq reaches 8: Increment core_seq, reset session_seq
        """
        counters = self.system_registry.get("counters", {})
        session_seq = counters.get("session_seq", 0)
        core_seq = counters.get("core_seq", 0)
        sphere_seq = counters.get("sphere_seq", 0)
        total_sessions = counters.get("total_sessions", 0)

        # Increment session & total
        session_seq += 1
        total_sessions += 1

        # Check if we need to create a Core
        if session_seq >= 8:
            print(f"[MSP] Compression trigger: 8 sessions completed → Creating Core {core_seq}")
            core_seq += 1
            session_seq = 0

            # Check if we need to create a Sphere
            if core_seq >= 8:
                print(f"[MSP] Compression trigger: 8 cores completed → Creating Sphere {sphere_seq}")
                sphere_seq += 1
                core_seq = 0

        # Update registry
        counters["session_seq"] = session_seq
        counters["core_seq"] = core_seq
        counters["sphere_seq"] = sphere_seq
        counters["total_sessions"] = total_sessions
        
        self.system_registry["counters"] = counters
        self._save_system_registry()
        
        print(f"[MSP] Session {session_seq} (Total {total_sessions}) Init.")
        return counters

    def end_session(self, session_id: str, session_analysis: Dict = None) -> Dict[str, Any]:
        """
        Finalize session:
        1. Compile all turns/episodes within this session (from cache or log)
        2. Create Session Memory Snapshot (Digest)
        3. Clear Turn Cache (ready for next session)
        
        Args:
            session_id: Session ID
            session_analysis: Optional LLM-generated analysis (events, summary)
            
        Returns:
            Snapshot data for display
        """
        print(f"[MSP] Ending session: {session_id}...")
        
        # 1. Retrieve items belonging to this session
        all_episodes = self._read_all_episodes_from_log()
        session_episodes = [ep for ep in all_episodes if ep.get("session_id") == session_id]
        
        # Sort by timestamp/turn_index to ensure order
        def get_sort_key(ep):
             # Try turn_1.turn_id or fallback to timestamp
             tid = ep.get("turn_1", {}).get("turn_id", "")
             return tid if tid else ep.get("timestamp", "")
        session_episodes.sort(key=get_sort_key)

        print(f"[MSP] Found {len(session_episodes)} episodes for {session_id}")

        # 2. Compress Data (Digest Generation) - Pass analysis
        digest = self._compress_session_data(session_id, session_episodes, session_analysis)
        
        # 3. Write Digest to Disk
        self.write_session_memory(digest)
        
        # 4. Clear Cache for next session
        self.turn_cache = {}
        self._save_turn_cache()

        return digest

    def extract_memorable_quotes(self, session_id: str, min_rim: float = 0.8, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Extract memorable quotes (salience anchors) from session episodes.
        
        Args:
            session_id: Session ID to extract from
            min_rim: Minimum RIM threshold (default: 0.8)
            limit: Maximum number of quotes to return
            
        Returns:
            List of quote objects with full episode context
        """
        all_episodes = self._read_all_episodes_from_log()
        session_eps = [ep for ep in all_episodes if ep.get("session_id") == session_id]
        
        quotes = []
        for ep in session_eps:
            # Check RIM threshold
            rim = ep.get("state_snapshot", {}).get("Resonance_index", 0)
            if rim < min_rim:
                continue
            
            # Extract salience anchor from LLM turn
            turn_llm = ep.get("turn_llm", {})
            anchor = turn_llm.get("salience_anchor", {})
            
            if anchor and anchor.get("phrase"):
                quotes.append({
                    "quote": anchor.get("phrase"),
                    "rim_score": float(rim),
                    "episode_id": ep.get("episode_id"),
                    "speaker": turn_llm.get("speaker", "eva"),
                    "context": turn_llm.get("text_excerpt", "")[:150],
                    "full_episode": ep,  # Complete episode for deep retrieval
                    "related_event": None  # To be populated by LLM if needed
                })
        
        # Sort by RIM score (highest first)
        quotes.sort(key=lambda x: x["rim_score"], reverse=True)
        
        return quotes[:limit]

    def archive_processed_episodes(self, session_id: str, referenced_episode_ids: List[str]) -> Dict[str, Any]:
        """
        Move session episodes to archival storage after compression.
        Logic: Keep referenced episodes (quotes/events), archive the rest.
        """
        import shutil
        import os
        
        # 1. Determine archival path hierarchy
        # Format: archival_memory/sphere_{n}/core_{n}/session_{n}/
        # Using system_registry for sequences
        counters = self.system_registry.get("counters", {})
        archive_path = (
            self.archival_dir / 
            f"sphere_{counters.get('sphere_seq', 1)}" /
            f"core_{counters.get('core_seq', 1)}" /
            f"session_{counters.get('session_seq', 1)}"
        )
        archive_path.mkdir(parents=True, exist_ok=True)
        
        # 2. Get all episodes for this session
        all_episodes = self._read_all_episodes_from_log()
        session_eps = [ep for ep in all_episodes if ep.get("session_id") == session_id]
        
        referenced_set = set(referenced_episode_ids)
        archived_count = 0
        
        # 3. Process archival
        for ep in session_eps:
            ep_id = ep.get("episode_id")
            if ep_id in referenced_set:
                continue # Keep referenced ones
            
            # Move variants (Global, User, LLM)
            variants = [
                (self.episodes_dir, f"{session_id}_{ep_id}.json"),
                (self.episodes_user_dir, f"{session_id}_{ep_id}_U.json"),
                (self.episodes_llm_dir, f"{session_id}_{ep_id}_L.json")
            ]
            
            for src_dir, filename in variants:
                src_file = src_dir / filename
                if src_file.exists():
                    dst_file = archive_path / filename
                    try:
                        shutil.move(str(src_file), str(dst_file))
                        archived_count += 1
                    except Exception as e:
                        print(f"[MSP] Archival error for {ep_id}: {e}")
        
        return {
            "status": "success",
            "archived_count": archived_count,
            "archive_path": str(archive_path)
        }

    def _compress_session_data(self, session_id: str, episodes: List[Dict], analysis: Dict = None) -> Dict[str, Any]:
        """
        Compress explicit episodes into a session digest with event classification.
        Logic: Use LLM analysis for grouping if available, else fallback to chunks.
        """
        events = []
        
        # Calculate timeline
        start_time = episodes[0].get("timestamp") if episodes else datetime.now().isoformat()
        end_time = episodes[-1].get("timestamp") if episodes else datetime.now().isoformat()
        
        try:
           st = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
           et = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
           duration = int((et - st).total_seconds() / 60)
        except:
           duration = 0

        # --- EVENT SEGMENTATION LOGIC ---
        if analysis and "events" in analysis:
            # Plan A: LLM-based Segmentation
            print("[MSP] Using LLM-based event segmentation.")
            llm_events = analysis.get("events", [])
            for i, ev_def in enumerate(llm_events):
                event_id = f"EVT_{session_id}_{i+1:02d}"
                start_ep = ev_def.get("start_episode_id")
                end_ep = ev_def.get("end_episode_id")
                
                # Optimized Finder
                start_idx = -1
                end_idx = -1
                
                for idx, ep in enumerate(episodes):
                    eid = ep.get("episode_id")
                    if eid == start_ep: start_idx = idx
                    if eid == end_ep: end_idx = idx
                
                if start_idx != -1:
                    actual_end = end_idx if end_idx != -1 else len(episodes)-1
                    chunk = episodes[start_idx : actual_end+1]
                else:
                    print(f"  ⚠️ Warning: Could not map episode range {start_ep}-{end_ep}")
                    continue

                # Calculate RIM Stats
                rim_values = []
                for ep in chunk:
                    if "state_snapshot" in ep:
                         val = ep.get("state_snapshot", {}).get("Resonance_index")
                    else:
                         val = ep.get("resonance_index")
                    if val is not None: rim_values.append(float(val))

                rim_stats = {
                    "RIM_MAX": max(rim_values) if rim_values else 0.0,
                    "RIM_MEAN": round(sum(rim_values)/len(rim_values), 2) if rim_values else 0.0,
                    "RIM_MIN": min(rim_values) if rim_values else 0.0
                }
                
                ep_range = [chunk[0].get("episode_id"), chunk[-1].get("episode_id")] if chunk else []

                events.append({
                    "event_id": event_id,
                    "label": ev_def.get("label", "Unknown Event"),
                    "episode_range": ep_range,
                    "rim_stats": rim_stats,
                    "summary": ev_def.get("summary", "")
                })
        else:
            # Plan B: Fallback Chunking (If LLM fails or simple mode)
            print("[MSP] Fallback: Using fixed-size chunking (n=4).")
            chunk_size = 4
            for i in range(0, len(episodes), chunk_size):
                chunk = episodes[i:i+chunk_size]
                if not chunk: continue
                
                chunk_idx = (i // chunk_size) + 1
                event_id = f"EVT_{session_id}_{chunk_idx:02d}"
                
                ep_ids = [ep.get("episode_id") for ep in chunk]
                ep_range = [ep_ids[0], ep_ids[-1]] if ep_ids else []
                
                # Simple Label
                tags = []
                for ep in chunk:
                     t = ep.get("tags", [])
                     if not t and "turn_1" in ep:
                          t = ep.get("turn_1", {}).get("semantic_frames", [])
                     tags.extend(t)
                
                import collections
                common_tag = "General Interaction"
                if tags:
                    counter = collections.Counter(tags)
                    common_tag = counter.most_common(1)[0][0]

                rim_values = []
                for ep in chunk:
                    if "state_snapshot" in ep: val = ep.get("state_snapshot", {}).get("Resonance_index")
                    else: val = ep.get("resonance_index")
                    if val is not None: rim_values.append(float(val))
                
                rim_stats = {
                    "RIM_MAX": max(rim_values) if rim_values else 0.0,
                    "RIM_MEAN": round(sum(rim_values)/len(rim_values), 2) if rim_values else 0.0,
                    "RIM_MIN": min(rim_values) if rim_values else 0.0
                }

                events.append({
                    "event_id": event_id,
                    "label": common_tag.title(),
                    "episode_range": ep_range,
                    "rim_stats": rim_stats,
                    "summary": f"Discussion focused on {common_tag} involving episodes {len(chunk)} turns."
                })

        # Construct Digest
        digest_summary = {
            "knowledge_synthesis": "Session analysis complete.",
            "accumulated_turns": len(episodes),
            "session_objective": "N/A",
            "session_status": "Unknown",
            "session_motto": "N/A"
        }
        
        if analysis:
             if "session_summary" in analysis: digest_summary["knowledge_synthesis"] = analysis["session_summary"]
             if "session_objective" in analysis: digest_summary["session_objective"] = analysis["session_objective"]
             if "session_status" in analysis: digest_summary["session_status"] = analysis["session_status"]
             if "session_motto" in analysis: digest_summary["session_motto"] = analysis["session_motto"]
             if "closure_reason" in analysis: digest_summary["closure_reason"] = analysis["closure_reason"]
             
        # Extract Memorable Quotes if provided in analysis
        memorable_quotes = analysis.get("memorable_quotes", []) if analysis else []

        # Collect all Episode IDs for the list
        all_ep_ids = [ep.get("episode_id") for ep in episodes]

        digest = {
            "session_id": session_id,
            "session_title": f"Session Digest: {session_id}",
            "developer_id": self.identity_config.get("instance", {}).get("developer_id", "THA-06"),
            "timeline": {
                "start_time": start_time,
                "end_time": end_time,
                "total_duration_minutes": duration
            },
            "episode_list": all_ep_ids,
            "event_classification": events,
            "memorable_quotes": memorable_quotes,
            "digest_summary": digest_summary,
             "salience_anchor": {
                "summary": f"Session containing {len(events)} discrete events.",
                "anchor_phrase": "N/A"
            }
        }
        
        return digest


    def _increment_episode_counter(self) -> int:
        """Increment episode counter and return new episode number"""
        counters = self.system_registry.get("counters", {})
        current = counters.get("current_episode", 0)
        current += 1
        
        counters["current_episode"] = current
        self.system_registry["counters"] = counters
        self._save_system_registry()
        
        return current



    def _get_persona_code(self) -> str:

        """

        Get persona code from persona.yaml

        If name > 4 chars, abbreviate like airport codes



        Returns:

            Persona code (max 4 chars, uppercase)

        """

        try:

            if self.persona_file.exists():

                with open(self.persona_file, 'r', encoding='utf-8') as f:

                    persona_data = yaml.safe_load(f)

                    persona_name = persona_data.get('meta', {}).get('name', 'EVA')

            else:

                persona_name = 'EVA'

        except Exception as e:

            print(f"[MSP] Error loading persona: {e}, using default 'EVA'")

            persona_name = 'EVA'



        # Abbreviate if needed

        return self._abbreviate_persona_name(persona_name)



    def _abbreviate_persona_name(self, name: str) -> str:

        """

        Abbreviate persona name to max 4 characters (like airport codes)



        Rules:

        - If <= 4 chars: Use as-is

        - If > 4 chars: Take first 4 consonants/letters

        - Examples:

            EVA → EVA

            Alexander → ALEX

            Christopher → CHRS

            สมหญิง → สมหญ



        Args:

            name: Persona name



        Returns:

            Abbreviated code (max 4 chars, uppercase for English)

        """

        name = name.strip()



        # If already <= 4, use as-is

        if len(name) <= 4:

            return name.upper()



        # For English names: Extract consonants + vowels, prioritize first letters

        # Simple approach: Take first 4 characters and remove vowels if needed

        if re.match(r'^[A-Za-z]+$', name):

            # Remove vowels, keep consonants

            consonants = re.sub(r'[aeiouAEIOU]', '', name)

            if len(consonants) >= 4:

                return consonants[:4].upper()

            else:

                # Not enough consonants, use first 4 letters

                return name[:4].upper()

        else:

            # For Thai or other scripts: Just take first 4 characters

            return name[:4]



    # ============================================================
    # IDENTITY & LINEAGE (THA-06)
    # ============================================================

    def _generate_episode_id(self) -> str:
        """DEPRECATED: Use IdentityManager.generate_episode_id"""
        persona_code = self.identity_config.get("persona", {}).get("persona_code", "EVA")
        episode_num = self._increment_episode_counter()
        return IdentityManager.generate_episode_id(persona_code, episode_num)

    def _generate_session_memory_filename(self) -> str:
        """Generate session memory filename using IdentityManager"""
        dev_id = self.identity_config.get("instance", {}).get("developer_id", "THA-06")
        counters = self.system_registry.get("counters", {})
        
        session_id = IdentityManager.generate_session_memory_id(
            dev_id, 
            counters.get("sphere_seq", 0),
            counters.get("core_seq", 0),
            counters.get("session_seq", 0)
        )
        return f"{session_id}.json"

    def _generate_session_memory_id(self) -> str:
        """Generate session memory ID using IdentityManager"""
        dev_id = self.identity_config.get("instance", {}).get("developer_id", "THA-06")
        counters = self.system_registry.get("counters", {})
        
        return IdentityManager.generate_session_memory_id(
            dev_id, 
            counters.get("sphere_seq", 0),
            counters.get("core_seq", 0),
            counters.get("session_seq", 0)
        )




    # ============================================================
    # IDENTITY CONFIG (SSOT)
    # ============================================================

    def _load_identity_config(self) -> Dict[str, Any]:
        """Load unified identity config from 09_state/identity_config.json"""
        if not self.identity_config_file.exists():
             print("[MSP] ⚠️ identity_config.json not found! Using fallback defaults.")
             return {
                 "instance": {"developer_id": "THA-01-S003"},
                 "persona": {"persona_code": "EVA"}
             }

        try:
            with open(self.identity_config_file, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except Exception as e:
            print(f"[MSP] Error loading identity config: {e}")
            return {"instance": {"developer_id": "THA-01-S003"}, "persona": {"persona_code": "EVA"}}



    def _get_develop_id_from_soul(self) -> str:
        """
        Get develop_id from soul.md file

        Returns:
            Develop ID (e.g., "THA-01-S003")
        """
        soul_file = self.root_path.parent / "orchestrator" / "cim" / "prompt_rule" / "configs" / "identity" / "soul.md"

        try:
            if soul_file.exists():
                with open(soul_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if 'Deverlop_id' in line or 'develop_id' in line:
                            # Parse: Deverlop_id : "THA-01-S003"
                            parts = line.split(':', 1)
                            if len(parts) == 2:
                                value = parts[1].strip().strip('"').strip("'")
                                if value:
                                    return value
        except Exception as e:
            print(f"[MSP] Error reading soul.md: {e}")

        # Default fallback
        return "THA-01-S003"



    def write_session_memory(self, session_data: Dict[str, Any]) -> str:

        """
        Write compressed session memory (digest) to persistent storage as Markdown.
        Format: SES{seq}_{DevID}_{Sphere}{Core}.md
        """
        # Ensure session memory directory exists
        self.session_memory_dir.mkdir(parents=True, exist_ok=True)

        # Extract IDs
        session_id = session_data.get("session_id", "UNKNOWN")
        dev_id = session_data.get("developer_id", "THA-06")
        
        # Parse Session ID for parts (THA-06_SP1C1_SES1)
        # We need to construct SES{seq}_{DevID}_{Sphere}{Core}
        # Assuming session_id matches standard format
        try:
            # parts: [DevID, SPxCxx, SESx]
            parts = session_id.split("_")
            ses_part = parts[-1] # SES1
            sp_part = parts[-2]  # SP1C1
            # Adjust DevID if needed (or take from session_id prefix)
            
            filename = f"{ses_part}_{dev_id}_{sp_part}.md"
        except:
            filename = f"{session_id}.md"

        storage_path = self.session_memory_dir / filename

        # Add metadata if not present
        if "timestamp" not in session_data:
            session_data["timestamp"] = datetime.now().isoformat()

        # --- GENERATE MARKDOWN CONTENT ---
        md_content = []
        
        # 1. Header
        timestamp = session_data.get("timeline", {}).get("end_time", datetime.now().isoformat())
        md_content.append(f"# {session_data.get('session_title', 'Session Digest')}")
        md_content.append(f"**Date:** {timestamp} | **ID:** {session_id}")
        md_content.append("")
        
        # 2. Dashboard
        summary = session_data.get("digest_summary", {})
        md_content.append("## 📊 Dashboard")
        md_content.append(f"- **Objective:** {summary.get('session_objective', 'N/A')}")
        md_content.append(f"- **Status:** {summary.get('session_status', 'N/A')}")
        md_content.append(f"- **Motto:** \"{summary.get('session_motto', 'N/A')}\"")
        md_content.append(f"- **Total Episodes:** {summary.get('accumulated_turns', 0)}")
        md_content.append(f"- **Duration:** {session_data.get('timeline', {}).get('total_duration_minutes', 0)} mins")
        md_content.append("")
        
        # 3. Session Closure
        md_content.append("## 🔚 Session Closure")
        md_content.append(f"- **Ended By:** {summary.get('closure_reason', 'unknown')}")
        md_content.append("")

        # 4. Memorable Quotes
        md_content.append("## 💭 Memorable Quotes")
        quotes = session_data.get("memorable_quotes", [])
        if quotes:
            for i, q in enumerate(quotes[:3], 1):
                md_content.append(f"### Quote {i} (RIM: {q.get('rim_score', 'N/A')})")
                md_content.append(f"> \"{q.get('quote')}\"")
                md_content.append(f"*— Context: {q.get('context', 'N/A')} ({q.get('episode_id', 'N/A')})*")
                md_content.append("")
        else:
            md_content.append("No memorable quotes identified.")
        md_content.append("")
        
        # 5. Episode List
        md_content.append("## 📑 Episode List")
        ep_list = session_data.get("episode_list", [])
        if ep_list:
            # Group by 5 for cleaner look or just list
            md_content.append(", ".join(ep_list))
        else:
            md_content.append("No episodes recorded.")
        md_content.append("")
        
        # 6. Event Breakdown
        md_content.append("## 🧠 Event Breakdown")
        
        events = session_data.get("event_classification", [])
        for evt in events:
            md_content.append(f"### {evt.get('label', 'Event')} ({evt.get('event_id')})")
            md_content.append(f"**Episodes:** {evt.get('episode_range', ['?','?'])[0]} - {evt.get('episode_range', ['?','?'])[-1]}")
            md_content.append(f"**Summary:** {evt.get('summary', 'No summary')}")
            
            stats = evt.get('rim_stats', {})
            md_content.append(f"> **RIM Stats:** Max {stats.get('RIM_MAX', 0.0)} | Mean {stats.get('RIM_MEAN', 0.0)} | Min {stats.get('RIM_MIN', 0.0)}")
            md_content.append("")

        # 7. Knowledge Synthesis
        md_content.append("## 📝 Knowledge Synthesis")
        md_content.append(summary.get("knowledge_synthesis", "N/A"))
        md_content.append("")

        try:
            with open(storage_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(md_content))
            return str(storage_path)
            
        except Exception as e:
            print(f"[MSP] Error writing session markdown: {e}")
            return ""

            print(f"[MSP] Error writing session memory: {e}")

            raise e



    # ============================================================

    # TURN CACHE OPERATIONS

    # ============================================================



    def _load_turn_cache(self):

        """Load turn cache from file"""

        if not self.turn_cache_file.exists():

            self.turn_cache = {}

            return



        try:

            with open(self.turn_cache_file, 'r', encoding='utf-8') as f:

                self.turn_cache = json.load(f)

        except Exception as e:

            print(f"[MSP] Error loading turn cache: {e}")

            self.turn_cache = {}



    def _save_turn_cache(self):

        """Save turn cache to file"""

        try:

            with open(self.turn_cache_file, 'w', encoding='utf-8') as f:

                json.dump(self.turn_cache, f, ensure_ascii=False, indent=2)

        except Exception as e:

            print(f"[MSP] Error saving turn cache: {e}")



    def update_turn_cache(

        self,

        context_id: str,

        context_data: Any

    ):

        """

        Update turn cache for Phase 1 bootstrap (Supports rich dict or string)



        Args:

            context_id: Context ID

            context_data: Turn summary (string) or rich metadata (dict)

        """

        if isinstance(context_data, str):

            data = {

                "summary": context_data,

                "timestamp": datetime.now().isoformat()

            }

        elif isinstance(context_data, dict):

            data = {

                **context_data,

                "timestamp": datetime.now().isoformat()

            }

        else:

            data = {

                "summary": str(context_data),

                "timestamp": datetime.now().isoformat()

            }



        # 1. Update In-memory & JSON Turn Cache (Fast access)

        self.turn_cache[context_id] = data

        self._save_turn_cache()



        # 2. Append to Context Ledger (Long-term tracking)

        try:

            ledger_entry = {

                "context_id": context_id,

                **data

            }

            with open(self.context_ledger, 'a', encoding='utf-8') as f:

                f.write(json.dumps(ledger_entry, ensure_ascii=False) + '\n')

        except Exception as e:

            print(f"[MSP] Error writing to context ledger: {e}")



    def get_recent_history(

        self,

        max_turns: int = 5

    ) -> List[Dict]:

        """

        Get recent conversation history



        Args:

            max_turns: Maximum number of turns



        Returns:

            Recent turn summaries

        """

        # Sort by timestamp

        turns = sorted(

            self.turn_cache.items(),

            key=lambda x: x[1]["timestamp"],

            reverse=True

        )

        return [{"context_id": k, **v} for k, v in turns[:max_turns]]



    def get_recent_turns(

        self,

        limit: int = 5,

        timeout_ms: int = 100

    ) -> List[Dict]:

        """

        Get recent turn summaries from turn cache (for CIN Phase 1 bootstrap)



        Args:

            limit: Maximum number of turns to retrieve

            timeout_ms: Timeout in milliseconds (not used for filesystem - always fast)



        Returns:

            List of recent turn summaries

        """

        # Note: timeout_ms is ignored for filesystem-based implementation

        # Filesystem reads are always fast (<10ms typically)

        return self.get_recent_history(max_turns=limit)



    def get_recent_episodes(

        self,

        limit: int = 10

    ) -> List[Dict]:

        """

        Get recent episodes for conversation history (for CIN Phase 1)



        Args:

            limit: Maximum number of episodes to retrieve



        Returns:

            List of recent episodes (user-only data for speed)

        """

        # Use user episodes for speed (no LLM response data)

        user_episodes = self._read_user_episodes()



        # Sort by timestamp (descending - most recent first)

        user_episodes.sort(

            key=lambda ep: ep.get("timestamp", ""),

            reverse=True

        )



        # Return last N episodes

        return user_episodes[:limit]



    def get_episode_counter(self) -> Dict[str, Any]:
        """
        Get current episode counter data (for CIN episode ID generation)
        Returns:
            Episode counter dict with persona_code and current_episode
        """
        counters = self.system_registry.get("counters", {})
        persona = self.system_registry.get("persona", {})
        return {
            "current_episode": counters.get("current_episode", 0),
            "persona_code": persona.get("persona_code", "EVA"),
            "last_update": self.system_registry.get("last_update")
        }

    def get_compression_counters(self) -> Dict[str, Any]:
        """Get current compression counters"""
        return self.system_registry.get("counters", {}).copy()



    # ============================================================

    # SENSORY MEMORY OPERATIONS

    # ============================================================



    def write_sensory_log(
        self,
        episode_id: str,
        qualia_data: Dict[str, Any]
    ) -> str:
        """
        Write sensory memory sidecar for an episode (Supports JSONL + JSON)
        """
        sensory_file = self.root_path / "sensory_memory" / "sensory_memory.json"
        
        # 1. Load existing structured storage
        if sensory_file.exists():
            try:
                with open(sensory_file, 'r', encoding='utf-8') as f:
                    sensory_data = json.load(f)
            except:
                sensory_data = {"entries": []}
        else:
            sensory_data = {"entries": []}

        # 2. Create entry
        sensory_entry = {
            "sensory_id": f"sen_{datetime.now().strftime('%y%m%d')}_{self._hash_short(episode_id)}",
            "episode_id": episode_id,
            "timestamp": datetime.now().isoformat(),
            "qualia": qualia_data
        }
        
        # 3. Append to JSONL (9.1.0 Standard)
        try:
            with open(self.sensory_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(sensory_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"[MSP] Error appending to sensory_log.jsonl: {e}")

        # 4. Append to entries for legacy/structured view
        sensory_data["entries"].append(sensory_entry)

        # 5. Write back JSON
        try:
            with open(sensory_file, 'w', encoding='utf-8') as f:
                json.dump(sensory_data, f, ensure_ascii=False, indent=2)
            print(f"[MSP] ✓ Sensory qualitatively logged: {sensory_entry['sensory_id']}")
        except Exception as e:
            print(f"[MSP] Error writing sensory_memory.json: {e}")

        return sensory_entry["sensory_id"]



    def query_sensory_logs(

        self,

        episode_id: Optional[str] = None

    ) -> List[Dict]:

        """

        Query sensory memory logs



        Args:

            episode_id: Optional filter by episode



        Returns:

            List of sensory logs

        """

        sensory_file = self.root_path / "sensory_memory" / "sensory_memory.json"



        if not sensory_file.exists():

            return []



        try:

            with open(sensory_file, 'r', encoding='utf-8') as f:

                sensory_data = json.load(f)

        except:

            return []



        entries = sensory_data.get("entries", [])



        if episode_id:

            return [e for e in entries if e.get("episode_id") == episode_id]



        return entries



    # ============================================================

    # UTILITY METHODS

    # ============================================================



    def _cosine_similarity(

        self,

        vec1: Dict[str, float],

        vec2: Dict[str, float]

    ) -> float:

        """

        Calculate cosine similarity between two physio state vectors



        Args:

            vec1: First vector

            vec2: Second vector



        Returns:

            Similarity score (0.0-1.0)

        """

        # Get common keys

        common_keys = set(vec1.keys()) & set(vec2.keys())

        if not common_keys:

            return 0.0



        # Calculate dot product and magnitudes

        dot_product = sum(vec1[k] * vec2[k] for k in common_keys)

        mag1 = sum(vec1[k] ** 2 for k in common_keys) ** 0.5

        mag2 = sum(vec2[k] ** 2 for k in common_keys) ** 0.5



        if mag1 == 0 or mag2 == 0:

            return 0.0



        return dot_product / (mag1 * mag2)



    def _exponential_decay(

        self,

        days_ago: int,

        halflife: int = 30

    ) -> float:

        """

        Calculate exponential decay score



        Args:

            days_ago: Number of days ago

            halflife: Halflife in days



        Returns:

            Decay score (0.0-1.0)

        """

        return math.exp(-days_ago / halflife)



    def _update_memory_index(self, episode: Dict[str, Any]):

        """

        Update memory_index.json with lightweight episode metadata



        Args:

            episode: Full episode document

        """

        # Extract index fields according to MSP_Write_Policy.yaml:87-98

        index_entry = {

            "episode_id": episode.get("episode_id"),

            "timestamp": episode.get("timestamp"),

            "session_id": episode.get("session_id"),

            "event_label": episode.get("event_label"),

            "episode_tag": episode.get("episode_tag"),

        }



        # Schema V2 fields

        turn_1 = episode.get("turn_1")

        turn_2 = episode.get("turn_2")

        state = episode.get("state_snapshot")



        if turn_1:

            index_entry["summary_user"] = turn_1.get("summary")

            index_entry["tags"] = turn_1.get("semantic_frames", [])

            index_entry["salience_anchor"] = turn_1.get("salience_anchor")

            index_entry["speaker_1"] = turn_1.get("speaker")



        turn_llm = episode.get("turn_llm") or episode.get("turn_2")

        if turn_llm:

            index_entry["summary_eva"] = turn_llm.get("summary")

            index_entry["speaker_2"] = turn_llm.get("speaker")



        if state:

            index_entry["resonance_index"] = state.get("Resonance_index")

            eva_matrix = state.get("EVA_matrix", {})

            if eva_matrix:

                index_entry["emotion_label"] = eva_matrix.get("emotion_label")



        # Load existing index

        if self.memory_index_file.exists():

            try:

                with open(self.memory_index_file, 'r', encoding='utf-8') as f:

                    memory_index = json.load(f)

            except:

                memory_index = {"episodes": []}

        else:

            memory_index = {"episodes": []}



        # Append new entry

        memory_index["episodes"].append(index_entry)



        # Keep only last 1000 entries (prevent bloat)

        if len(memory_index["episodes"]) > 1000:

            memory_index["episodes"] = memory_index["episodes"][-1000:]



        # Write back

        try:

            with open(self.memory_index_file, 'w', encoding='utf-8') as f:

                json.dump(memory_index, f, ensure_ascii=False, indent=2)

        except Exception as e:

            print(f"[MSP] Error updating memory_index: {e}")



    def _hash_short(self, text: str) -> str:

        """Generate short hash (8 chars)"""

        return hashlib.md5(text.encode()).hexdigest()[:8]



    def get_stats(self) -> Dict[str, Any]:

        """Get storage statistics"""

        total_episodes = len(list(self.episodes_dir.glob("ep_*.json")))



        # Count lines in JSONL

        jsonl_count = 0

        if self.episodic_log.exists():

            with open(self.episodic_log, 'r', encoding='utf-8') as f:

                jsonl_count = sum(1 for line in f if line.strip())



        return {

            "total_episodes": total_episodes,

            "jsonl_episodes": jsonl_count,

            "cached_episodes": len(self._episode_cache),

            "semantic_concepts": len(self._semantic_concepts),

            "cached_turns": len(self.turn_cache),

            "storage_path": str(self.root_path)

        }



    def clear_cache(self):

        """Clear in-memory cache"""

        self._episode_cache = []

        self._cache_loaded = False

        print("[MSP] Cache cleared")



    def reload(self):

        """Reload all data from disk"""

        self.clear_cache()

        self._load_semantic_concepts()

        self._load_turn_cache()

        self._load_cache()

        print("[MSP] Reloaded from disk")










    def register_dashboard_metric(

        self,

        metric_id: str,

        value: float,

        category: str = "general"

    ):

        """

        Register a metric for the live dashboard.

        In this local version, we save it to a transient state.

        """

        if not hasattr(self, 'dashboard_state'):

            self.dashboard_state = {}

        

        self.dashboard_state[metric_id] = {

            "value": value,

            "category": category,

            "timestamp": datetime.now().isoformat()

        }



    # ============================================================

    # ACTIVE STATE BUS (STATE BUS PATTERN - PHASE 4)

    # ============================================================



    def set_active_state(self, slot: str, data: Any):

        """

        Set active state in the State Bus.

        Used by components (Physio, Psyche) to broadcast their current state.



        Args:

            slot: State slot identifier (e.g., 'physio_state', 'matrix_state')

            data: State data (dict or value)

        """

        # 1. Update In-memory cache

        self._active_state_cache[slot] = {

            "data": data,

            "timestamp": datetime.now().isoformat()

        }



        # 2. Persist to transient file (for crash recovery)

        try:

            state_file = self.active_state_dir / f"{slot}.json"

            with open(state_file, 'w', encoding='utf-8') as f:

                json.dump(self._active_state_cache[slot], f, ensure_ascii=False, indent=2)

        except Exception as e:

            print(f"[MSP] Error persisting active state {slot}: {e}")



    def get_active_state(self, slot: str) -> Optional[Any]:

        """

        Get active state from the State Bus.

        Used by components (Psyche, CIN) to pull the latest baseline.



        Args:

            slot: State slot identifier



        Returns:

            The latest state data or None

        """

        # 1. Check in-memory cache

        if slot in self._active_state_cache:

            return self._active_state_cache[slot]["data"]



        # 2. Check transient file

        state_file = self.active_state_dir / f"{slot}.json"

        if state_file.exists():

            try:

                with open(state_file, 'r', encoding='utf-8') as f:

                    cached = json.load(f)

                    self._active_state_cache[slot] = cached

                    return cached.get("data")

            except Exception as e:

                print(f"[MSP] Error loading active state {slot}: {e}")

        

        return None



    def get_all_active_states(self) -> Dict[str, Any]:
        """
        Get all current active states.
        """
        # Load any missing states from files
        for state_file in self.active_state_dir.glob("*.json"):
            slot = state_file.stem
            if slot not in self._active_state_cache:
                self.get_active_state(slot)
        
        return {slot: item["data"] for slot, item in self._active_state_cache.items()}

    def write_semantic_memory(self, concept_id: str, data: Dict[str, Any]):
        """
        Write or update a semantic concept (Supports JSONL + JSON).
        """
        # 1. Update In-memory
        self._semantic_concepts[concept_id] = data
        
        # 2. Append to JSONL Audit Log
        log_entry = {
            "concept_id": concept_id,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        try:
            with open(self.semantic_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"[MSP] Error appending to semantic_log.jsonl: {e}")

        # 3. Persist to main JSON concepts file
        self._save_semantic_concepts()
        print(f"[MSP] ✓ Semantic Concept recorded: {concept_id}")

    def log_state_history(self):
        """
        Snapshot all active states and append to consciousness_history.jsonl.
        """
        all_states = self.get_all_active_states()
        if not all_states:
            return

        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "states": all_states,
            "resonance_hash": hashlib.md5(json.dumps(all_states, sort_keys=True).encode()).hexdigest()
        }

        try:
            with open(self.consciousness_history, 'a', encoding='utf-8') as f:
                f.write(json.dumps(history_entry, ensure_ascii=False) + '\n')
            # print(f"[MSP] ✓ Consciousness History logged.")
        except Exception as e:
            print(f"[MSP] Error writing to consciousness_history.jsonl: {e}")



if __name__ == "__main__":

    """Test MSP Client with Filesystem Persistence"""

    # Fix Windows console UTF-8 encoding

    import sys

    import codecs

    if sys.platform == 'win32':

        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')



    print("="*60)

    print("Testing MSP Client with Filesystem Persistence")

    print("="*60)



    # Initialize

    msp = MSPClient()



    # Test 1: Write new episode

    print("\n--- Test 1: Write New Episode ---")

    episode_data = {

        "content": "ขอบคุณนะที่วันนี้มาส่งที่สนามบิน",

        "response": "ยินดีค่ะ บอส",

        "tags": ["gratitude", "airport"],

        "stimulus_vector": {

            "stress": 0.3,

            "warmth": 0.8,

            "arousal": 0.4,

            "valence": 0.9

        },

        "physio_state": {

            "cortisol": 0.3,

            "dopamine": 0.7,

            "oxytocin": 0.8,

            "ans_sympathetic": 0.3,

            "ans_parasympathetic": 0.7

        },

        "resonance_index": 0.75,

        "resonance_impact": 0.65,

        "qualia": {

            "intensity": 0.7,

            "tone": "warm",

            "texture": [0.8, 0.6, 0.5, 0.7, 0.4]

        }

    }

    episode_id = msp.write_episode(episode_data)

    print(f"Created episode: {episode_id}")



    # Test 2: Query by tags

    print("\n--- Test 2: Query by Tags ---")

    results = msp.query_by_tags(["gratitude"], max_results=3)

    print(f"Found {len(results)} episodes with tag 'gratitude'")

    for ep in results:

        content = ep.get("content", "")[:50]

        print(f"  - {ep['episode_id']}: {content}... (RI: {ep.get('resonance_index', 0)})")



    # Test 3: Query by physio similarity

    print("\n--- Test 3: Query by Physio Similarity ---")

    current_state = {

        "cortisol": 0.5,

        "dopamine": 0.6,

        "oxytocin": 0.7,

        "ans_sympathetic": 0.4

    }

    results = msp.query_by_physio_state(current_state, similarity_threshold=0.7)

    print(f"Found {len(results)} episodes with similar physio state")

    for ep in results:

        content = ep.get("content", "")[:50]

        similarity = ep.get("physio_similarity", 0)

        print(f"  - {ep['episode_id']}: {content}... (Similarity: {similarity:.2f})")



    # Test 4: Query recent

    print("\n--- Test 4: Query Recent Episodes ---")

    results = msp.query_recent(max_results=5)

    print(f"Found {len(results)} recent episodes")

    for ep in results:

        content = ep.get("content", "")[:50]

        recency = ep.get("recency_score", 0)

        print(f"  - {ep['episode_id']}: {content}... (Recency: {recency:.2f})")



    # Test 5: Turn cache

    print("\n--- Test 5: Turn Cache ---")

    msp.update_turn_cache("ctx_v8_260101_120000_abc123", "User thanked for airport ride")

    history = msp.get_recent_history(max_turns=3)

    print(f"Recent history: {len(history)} turns")

    for turn in history:

        print(f"  - {turn['context_id']}: {turn['summary']}")



    # Print stats

    print("\n--- Storage Statistics ---")

    stats = msp.get_stats()

    for key, value in stats.items():

        print(f"{key}: {value}")



    print("\n✅ All tests completed!")

    print(f"\nData stored in: {msp.root_path}")

